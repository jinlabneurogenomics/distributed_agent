"""Download the pinned atlas and prepare the inputs for all bundled BioEval tasks.

Run with the minimal Pixi environment. Downloads resume from a .part file;
the original is accepted only after its size and SHA-256 match the source pin.
"""

from __future__ import annotations

import argparse
from collections import Counter
import csv
import hashlib
import json
import os
from pathlib import Path
import sys
import time

import requests

import pyarrow as pa
import pyarrow.compute as pc
import pyarrow.parquet as pq

ROOT = Path(__file__).resolve().parents[1]
SOURCE_PIN = Path(__file__).with_name("benchmark_data_source.json")
FOCAL_GROUP = "151 TH Prkcd Grin2c Glut"
COUNT_COLUMNS = ("n_pert_matched", "n_ctrl_matched")
REQUIRED_COLUMNS = (
    "names", "group_name", "gene_target", "logfoldchanges", "pvals", "pvals_adj",
    "scores", "control_label", *COUNT_COLUMNS,
)
TRAINING_PATH = Path("data/inputs/holdout/training_de_all_cell_groups.parquet")
PROVENANCE_PATH = Path("data/benchmark-data.provenance.json")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(8 * 1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def verify_file(path: Path, expected: dict) -> None:
    if not path.is_file():
        raise ValueError(f"Missing file: {path}")
    if "bytes" in expected and path.stat().st_size != expected["bytes"]:
        raise ValueError(f"Size mismatch: {path}")
    if sha256(path) != expected["sha256"]:
        raise ValueError(f"SHA-256 mismatch: {path}")


def download_source(destination: Path, pin: dict) -> None:
    if destination.exists():
        print(f"Verifying existing source: {destination}", flush=True)
        verify_file(destination, pin)
        return
    destination.parent.mkdir(parents=True, exist_ok=True)
    partial = destination.with_suffix(destination.suffix + ".part")
    url = (
        f"https://huggingface.co/datasets/{pin['repo_id']}/resolve/"
        f"{pin['revision']}/{pin['filename']}"
    )
    for attempt in range(5):
        offset = partial.stat().st_size if partial.exists() else 0
        if offset == pin["bytes"]:
            break
        if offset > pin["bytes"]:
            raise ValueError(f"Oversized partial download; remove it and retry: {partial}")
        headers = {"Accept-Encoding": "identity"}
        if offset:
            headers["Range"] = f"bytes={offset}-"
        try:
            with requests.get(url, headers=headers, stream=True, timeout=(20, 60)) as response:
                response.raise_for_status()
                if response.status_code == 206:
                    expected_range = f"bytes {offset}-{pin['bytes'] - 1}/{pin['bytes']}"
                    if response.headers.get("Content-Range") != expected_range:
                        raise ValueError("Unexpected Content-Range for pinned download")
                elif response.status_code == 200:
                    offset = 0  # The server did not honor Range; restart safely.
                else:
                    raise ValueError(f"Unexpected download status: {response.status_code}")
                print(f"Downloading {pin['bytes']:,} bytes, starting at {offset:,}.", flush=True)
                last_report = time.monotonic()
                with partial.open("ab" if offset else "wb") as handle:
                    for chunk in response.iter_content(chunk_size=8 * 1024 * 1024):
                        handle.write(chunk)
                        offset += len(chunk)
                        if offset > pin["bytes"]:
                            raise ValueError("Download exceeded pinned size")
                        if time.monotonic() - last_report > 15:
                            print(f"Downloaded {offset / pin['bytes']:.1%}.", flush=True)
                            last_report = time.monotonic()
            if offset == pin["bytes"]:
                break
            raise requests.ConnectionError("Download ended before the pinned byte count")
        except requests.RequestException as exc:
            if attempt == 4:
                raise RuntimeError(f"Download failed; rerun to resume {partial}") from exc
            print(f"Download interrupted; retrying ({attempt + 1}/4).", flush=True)
            time.sleep(min(2 ** attempt, 15))
    print("Checking source SHA-256.", flush=True)
    verify_file(partial, pin)
    partial.replace(destination)
    print(f"Verified source: {destination}", flush=True)


def read_registry(pin: dict) -> tuple[set[str], dict[str, int]]:
    for name in ("holdout_registry", "training_counts"):
        verify_file(ROOT / pin[name]["path"], pin[name])
    with (ROOT / pin["holdout_registry"]["path"]).open(newline="") as handle:
        rows = list(csv.DictReader(handle))
    heldout = {row["perturbation"] for row in rows}
    if len(heldout) != len(rows) or len(heldout) != pin["holdout_registry"]["targets"]:
        raise ValueError("Unexpected or duplicate targets in the holdout registry")
    with (ROOT / pin["training_counts"]["path"]).open(newline="") as handle:
        rows = list(csv.DictReader(handle))
    counts = {row["target_name"]: int(row["n_degs"]) for row in rows}
    if len(counts) != len(rows) or len(counts) != pin["training_counts"]["targets"]:
        raise ValueError("Unexpected or duplicate targets in training counts")
    if heldout & counts.keys():
        raise ValueError("Held-out targets appear in training counts")
    for path in (ROOT / "src/bioeval/benchmarks/holdout-prediction").glob("*-targets.csv"):
        with path.open(newline="") as handle:
            targets = {row["target_name"] for row in csv.DictReader(handle)}
        if not targets <= heldout:
            raise ValueError(f"Benchmark targets missing from holdout registry: {path}")
    return heldout, counts


def derive_parquets(
    source: Path, no_counts: Path, training: Path, heldout: set[str],
    *, batch_size: int = 262_144,
) -> tuple[dict, dict[str, int]]:
    """Stream every row, removing only count columns / held-out perturbations.

    Decode dictionary columns and drop pandas metadata so the training file
    does not carry excluded labels in unused dictionaries or category metadata.
    Significance is used only to calculate counts, never to filter DE rows.
    """
    parquet = pq.ParquetFile(source)
    missing = set(REQUIRED_COLUMNS) - set(parquet.schema_arrow.names)
    if missing:
        raise ValueError(f"Atlas is missing columns: {sorted(missing)}")
    schema = pa.schema([
        pa.field(field.name, field.type.value_type if pa.types.is_dictionary(field.type)
                 else field.type, nullable=field.nullable)
        for field in parquet.schema_arrow
    ])
    no_counts_schema = pa.schema([f for f in schema if f.name not in COUNT_COLUMNS])
    heldout_array = pa.array(sorted(heldout), type=schema.field("gene_target").type)
    all_targets: set[str] = set()
    train_targets: set[str] = set()
    cell_groups: set[str] = set()
    genes: set[str] = set()
    counts: Counter = Counter()
    source_rows = training_rows = 0
    last_report = time.monotonic()
    for path in (no_counts, training):
        path.parent.mkdir(parents=True, exist_ok=True)
    with (
        pq.ParquetWriter(no_counts, no_counts_schema, compression="zstd", compression_level=3) as no_writer,
        pq.ParquetWriter(training, schema, compression="zstd", compression_level=3) as train_writer,
    ):
        for batch in parquet.iter_batches(batch_size=batch_size):
            table = pa.Table.from_batches([batch]).cast(schema)
            targets = table["gene_target"]
            if targets.null_count:
                raise ValueError("Null perturbation labels in the atlas")
            all_targets.update(pc.unique(targets).to_pylist())
            cell_groups.update(pc.unique(table["group_name"]).to_pylist())
            genes.update(pc.unique(table["names"]).to_pylist())
            no_writer.write_table(table.select(no_counts_schema.names), row_group_size=batch_size)
            retained = table.filter(pc.invert(pc.is_in(targets, value_set=heldout_array)))
            if retained.num_rows:
                train_writer.write_table(retained, row_group_size=batch_size)
                train_targets.update(pc.unique(retained["gene_target"]).to_pylist())
                significant = retained.select(["gene_target"]).filter(pc.and_(
                    pc.equal(retained["group_name"], FOCAL_GROUP),
                    pc.less(retained["pvals_adj"], 0.05),
                ))
                frequencies = pc.value_counts(significant["gene_target"]).to_pylist()
                counts.update({row["values"]: row["counts"] for row in frequencies})
            source_rows += table.num_rows
            training_rows += retained.num_rows
            if time.monotonic() - last_report > 15:
                print(f"Prepared {source_rows:,}/{parquet.metadata.num_rows:,} rows.", flush=True)
                last_report = time.monotonic()
    if not heldout <= all_targets:
        raise ValueError(f"Held-out labels absent from source: {sorted(heldout - all_targets)}")
    if train_targets != all_targets - heldout:
        raise ValueError("Training target set does not match the declared exclusion")
    if source_rows != parquet.metadata.num_rows:
        raise ValueError("Source rows were lost while streaming")
    for path, expected_rows in ((no_counts, source_rows), (training, training_rows)):
        if pq.ParquetFile(path).metadata.num_rows != expected_rows:
            raise ValueError(f"Written row count mismatch: {path}")
    biological_counts = {
        target: counts[target] for target in sorted(train_targets)
        if not target.startswith("Safe_target_") and target != "Non_target"
    }
    return {
        "source_rows": source_rows,
        "training_rows": training_rows,
        "excluded_rows": source_rows - training_rows,
        "perturbation_labels": len(all_targets),
        "training_perturbation_labels": len(train_targets),
        "heldout_perturbation_labels": len(heldout),
        "cell_groups": len(cell_groups),
        "measured_genes": len(genes),
    }, biological_counts


def validate_counts(actual: dict[str, int], expected: dict[str, int]) -> None:
    mismatches = [
        (target, actual.get(target), expected.get(target))
        for target in sorted(actual.keys() | expected.keys())
        if actual.get(target) != expected.get(target)
    ]
    if mismatches:
        raise ValueError(
            f"Recomputed training counts disagree for {len(mismatches)} targets "
            f"(target, computed, bundled): {mismatches[:10]}"
        )


def validate_tasks(shared_root: Path) -> list[str]:
    sys.path.insert(0, str(ROOT / "src"))
    from bioeval.tasks import load_task_spec, render_task_prompt

    previous = os.environ.get("DISTRIBUTED_AGENTS_SHARED_ROOT")
    os.environ["DISTRIBUTED_AGENTS_SHARED_ROOT"] = str(shared_root)
    checked = []
    try:
        for path in sorted((ROOT / "src/bioeval/benchmarks").rglob("*.toml")):
            spec = load_task_spec(path)
            if "{{" in render_task_prompt(spec):
                raise ValueError(f"Unresolved prompt variable: {path}")
            checked.append(str(path.relative_to(ROOT)))
    finally:
        if previous is None:
            os.environ.pop("DISTRIBUTED_AGENTS_SHARED_ROOT", None)
        else:
            os.environ["DISTRIBUTED_AGENTS_SHARED_ROOT"] = previous
    print(f"Validated inputs and prompt rendering for {len(checked)} benchmark manifests.", flush=True)
    return checked


def recipe(pin: dict) -> dict:
    # Bump the recipe version when the transformation semantics change.
    return {
        "version": 1,
        "source": pin,
        "preparation_script_sha256": sha256(Path(__file__)),
        "pyarrow_version": pa.__version__,
        "no_counts": {"drop_columns": list(COUNT_COLUMNS)},
        "training": {"exclude_registry_targets_in_all_cell_groups": True},
        "training_counts": {
            "cell_group": FOCAL_GROUP, "pvals_adj_lt": 0.05,
            "include_self_target": True, "include_zero_counts": True,
            "exclude_safe_target_controls": True,
        },
        "writer": {"compression": "zstd", "compression_level": 3, "batch_size": 262_144},
    }


def record_file(path: Path) -> dict:
    record = {"bytes": path.stat().st_size, "sha256": sha256(path)}
    if path.suffix == ".parquet":
        parquet = pq.ParquetFile(path)
        record.update(rows=parquet.metadata.num_rows, columns=parquet.schema_arrow.names)
    return record


def verify_prepared(shared_root: Path, pin: dict) -> None:
    read_registry(pin)
    path = shared_root / PROVENANCE_PATH
    if not path.is_file():
        raise ValueError(f"No preparation provenance at {path}; run preparation first")
    provenance = json.loads(path.read_text())
    # Tool versions and code hashes record how files were produced. Reusing
    # checksum-verified data depends on the data recipe, not the reader version.
    implementation_fields = {"preparation_script_sha256", "pyarrow_version"}
    recorded_recipe = {k: v for k, v in provenance["recipe"].items() if k not in implementation_fields}
    current_recipe = {k: v for k, v in recipe(pin).items() if k not in implementation_fields}
    if recorded_recipe != current_recipe:
        raise ValueError("Preparation recipe changed; rerun with --rebuild")
    source_relative = Path("data") / Path(pin["filename"]).name
    expected_files = {
        str(source_relative), str(source_relative.with_name(source_relative.stem + "_nocounts.parquet")),
        str(TRAINING_PATH), pin["training_counts"]["path"],
    }
    if set(provenance["files"]) != expected_files:
        raise ValueError("Incomplete preparation provenance; rerun with --rebuild")
    source_record = provenance["files"][str(source_relative)]
    if any(source_record[key] != pin[key] for key in ("bytes", "sha256")):
        raise ValueError("Recorded source does not match the Hugging Face pin")
    for relative, expected in provenance["files"].items():
        print(f"Verifying {relative}", flush=True)
        verify_file(shared_root / relative, expected)
    validate_tasks(shared_root)
    print("Prepared benchmark data verified.", flush=True)


def prepare_data(shared_root: Path, source: Path, pin: dict, *, rebuild: bool = False) -> None:
    heldout, expected_counts = read_registry(pin)
    no_counts = source.with_name(source.stem + "_nocounts.parquet")
    training = shared_root / TRAINING_PATH
    provenance_path = shared_root / PROVENANCE_PATH
    counts_path = shared_root / pin["training_counts"]["path"]
    if counts_path.exists():
        verify_file(counts_path, pin["training_counts"])
    if provenance_path.exists() and not rebuild:
        verify_prepared(shared_root, pin)
        return
    if not rebuild and (no_counts.exists() or training.exists()):
        raise ValueError("Derived files exist without provenance; use --rebuild to replace them")
    no_counts_partial = no_counts.with_suffix(".parquet.part")
    training_partial = training.with_suffix(".parquet.part")
    print("Preparing no-counts and holdout inputs in bounded-memory batches.", flush=True)
    try:
        inventory, counts = derive_parquets(source, no_counts_partial, training_partial, heldout)
        for key, expected in pin["inventory"].items():
            if inventory[key] != expected:
                raise ValueError(f"Unexpected atlas inventory for {key}: {inventory[key]} != {expected}")
        validate_counts(counts, expected_counts)
        print(f"All {len(counts):,} recomputed training DEG counts match the bundled table.", flush=True)
        no_counts_partial.replace(no_counts)
        training_partial.replace(training)
    finally:
        no_counts_partial.unlink(missing_ok=True)
        training_partial.unlink(missing_ok=True)
    counts_path.parent.mkdir(parents=True, exist_ok=True)
    if not counts_path.exists():
        # Preserve canonical CSV formatting after checking every regenerated value.
        counts_path.write_bytes((ROOT / pin["training_counts"]["path"]).read_bytes())
    checked = validate_tasks(shared_root)
    files = {}
    for path in (source, no_counts, training, counts_path):
        print(f"Recording checksum: {path.name}", flush=True)
        files[str(path.relative_to(shared_root))] = record_file(path)
    provenance = {"recipe": recipe(pin), "inventory": inventory, "files": files, "benchmarks": checked}
    provenance_path.write_text(json.dumps(provenance, indent=2, sort_keys=True) + "\n")
    print(json.dumps(inventory, indent=2), flush=True)
    print(f"Preparation complete. Provenance: {provenance_path}", flush=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--shared-root", type=Path,
        default=Path(os.environ.get("DISTRIBUTED_AGENTS_SHARED_ROOT", ROOT)),
        help="Root containing data/ (default: DISTRIBUTED_AGENTS_SHARED_ROOT or checkout).",
    )
    parser.add_argument("--download-only", action="store_true")
    parser.add_argument("--verify-only", action="store_true", help="Verify recorded hashes and benchmark inputs without downloading.")
    parser.add_argument("--rebuild", action="store_true", help="Replace generated derivatives using the verified source.")
    args = parser.parse_args()
    if args.verify_only and (args.download_only or args.rebuild):
        parser.error("--verify-only cannot be combined with --download-only or --rebuild")
    pin = json.loads(SOURCE_PIN.read_text())
    shared_root = args.shared_root.expanduser().resolve()
    if args.verify_only:
        verify_prepared(shared_root, pin)
        return 0
    if not args.download_only and not args.rebuild and (shared_root / PROVENANCE_PATH).exists():
        verify_prepared(shared_root, pin)
        return 0
    source = shared_root / "data" / Path(pin["filename"]).name
    download_source(source, pin)
    if not args.download_only:
        prepare_data(shared_root, source, pin, rebuild=args.rebuild)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
