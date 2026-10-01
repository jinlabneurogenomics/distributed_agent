#!/usr/bin/env python3
"""Gold-calibrated, arm-blind three-arm literature-flag distribution.

The same 150 underlying response genes are represented by an older 260713
unshuffled report and the updated 260730 within-screen and out-of-screen target
label shuffles.  Whole reports are never split across model calls.  The grader
assigns finding admissibility and literature relationship separately; the
four-class flag and primary/sensitivity analysis gates are derived in code.
"""

from __future__ import annotations

import argparse
import copy
import csv
import importlib.util
import json
import os
import random
import re
from collections import Counter
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
GOLD_SCRIPT = (
    ROOT
    / "manuscript/fig2/_debug/260731/literature_flag_gold_set/gold_set.py"
)
SPEC = importlib.util.spec_from_file_location("final_distribution_gold", GOLD_SCRIPT)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"cannot load gold-set helpers: {GOLD_SCRIPT}")
gold = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(gold)

_BASE_NORMALIZE_FLAG = gold.normalize_flag


def _normalize_source_flag(value: Any) -> str:
    """Retain legacy null flags as host-only metadata; never expose them."""
    if value is None or not str(value).strip():
        return "unflagged"
    return _BASE_NORMALIZE_FLAG(value)


gold.normalize_flag = _normalize_source_flag

STYLE = ROOT / "src/figures/style.mplstyle"
PACKETS = HERE / "packets"
PROMPTS = HERE / "prompts"
SCHEMAS = HERE / "schemas"
RUNS = HERE / "runs"
MANIFEST = HERE / "manifest.json"
CANDIDATES = HERE / "source_findings.csv"
RUN_STATUS = HERE / "run_status.json"
CALIBRATION_COMPARISON = HERE / "gold_calibration_comparison.csv"
CALIBRATION_SUMMARY = HERE / "gold_calibration_summary.json"
CLASSIFIED = HERE / "final_classified_findings.csv"
OVERALL_DISTRIBUTION = HERE / "final_overall_distribution.csv"
PLACEMENTS = HERE / "final_celltype_signal_placements.csv"
LOCAL_DISTRIBUTION = HERE / "final_local_signal_distribution.csv"
FINDING_MAX_SIGNAL = HERE / "final_finding_max_signal_assignments_primary.csv"
FINDING_MAX_DISTRIBUTION = HERE / "final_flag_distribution_by_finding_max_signal_primary.csv"
POSITIVE_PAIR_COVERAGE = HERE / "final_positive_pair_flag_coverage_primary.csv"
POSITIVE_PAIR_COVERAGE_SUMMARY = HERE / "final_positive_pair_coverage_summary_primary.csv"
UNSHUFFLED_COVERAGE_BY_DEG = HERE / "final_unshuffled_positive_pair_coverage_by_deg_primary.csv"
SUMMARY = HERE / "final_summary.json"

ARMS = gold.ARMS
FLAGS = ("agree", "disagree", "inferred", "no_literature")
FLAG_LABELS = {
    "agree": "Agree",
    "disagree": "Disagree",
    "inferred": "Inferred",
    "no_literature": "No Literature",
}
COLORS = {
    "agree": "#6fc46f",
    "disagree": "#ec835a",
    "inferred": "#898781",
    "no_literature": "#c3c2b7",
}
LAYERS = ("primary", "sensitivity")
STRATA = ("Strong", "Moderate", "Low", "No local DEGs")
STRATUM_LABELS = {
    "Strong": "Strong local signal (≥100)",
    "Moderate": "Moderate local signal (25–99)",
    "Low": "Low local signal (1–24)",
    "No local DEGs": "No local DEGs (0)",
}
GENERATION = {
    ARMS[0]: "260713",
    ARMS[1]: "260730",
    ARMS[2]: "260730",
}
DEG_COVERAGE_BINS = (
    (1, 1, "1"),
    (2, 4, "2–4"),
    (5, 9, "5–9"),
    (10, 24, "10–24"),
    (25, 49, "25–49"),
    (50, 99, "50–99"),
    (100, 199, "100–199"),
    (200, 499, "200–499"),
    (500, None, "≥500"),
)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"refusing to write empty CSV: {path}")
    fields: list[str] = []
    seen: set[str] = set()
    for row in rows:
        for field in row:
            if field not in seen:
                fields.append(field)
                seen.add(field)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def production_prompt(blocks: list[dict[str, Any]]) -> str:
    rubric = gold.RUBRIC.replace(
        "constructing a gold-standard calibration set",
        "performing the final arm-blind corpus classification",
    )
    return (
        rubric
        + "\nThis is the production application of the frozen gold-set rubric. "
        "Do not target a desired arm distribution or finding count. Treat the "
        "structured finding gene list as potentially representative rather than "
        "exhaustive: judge program coherence from the complete report evidence and "
        "response material supplied. If the supplied evidence truly exposes only a "
        "sparse marker observation, do not invent additional members. Return only "
        "schema-valid JSON and do not guess the hidden arm.\n\n"
        + "COMPLETE ARM-BLIND REPORT BLOCKS:\n"
        + json.dumps(blocks, separators=(",", ":"), ensure_ascii=False)
        + "\n"
    )


def prepare() -> None:
    """Build 150 Latin-shift packets, each containing three complete reports."""
    for directory in (HERE, PACKETS, PROMPTS, SCHEMAS, RUNS):
        directory.mkdir(parents=True, exist_ok=True)
    records = gold.arm_records()
    lookup = gold.response_lookup(records)
    label_maps = gold.displayed_to_response(records)
    response_genes = sorted(set(lookup[ARMS[1]]) & set(lookup[ARMS[2]]))
    if len(response_genes) != 150:
        raise ValueError(f"expected 150 matched response genes, found {len(response_genes)}")
    missing_unshuffled = sorted(set(response_genes) - set(lookup[ARMS[0]]))
    if missing_unshuffled:
        raise ValueError(f"unshuffled reports missing matched genes: {missing_unshuffled}")
    index, baseline = gold.deg_index()
    cache = json.loads(gold.CACHE_PATH.read_text()).get("records", {})

    blocks: dict[tuple[str, str], dict[str, Any]] = {}
    host_blocks: list[dict[str, Any]] = []
    candidates: list[dict[str, Any]] = []
    block_number = 0
    for arm in ARMS:
        for response_gene in response_genes:
            record = lookup[arm][response_gene]
            findings = gold.base.jsonl_section(
                str(record.get("report") or ""), "Biological Findings JSONL"
            )
            scored_ids = {
                str(row.get("finding_id") or "")
                for row in findings
                if gold.finding_kind(row) not in gold.EXCLUDED_FINDING_TYPES
            }
            block_number += 1
            block_id = f"B{block_number:04d}"
            block, rows = gold.make_block(
                block_id=block_id,
                arm=arm,
                response_gene=response_gene,
                record=record,
                scored_ids=scored_ids,
                set_role="full_corpus",
                index=index,
                baseline=baseline,
                label_map=label_maps[arm],
                cache=cache,
            )
            blocks[(arm, response_gene)] = block
            candidates.extend(rows)
            host_blocks.append(
                {
                    "block_id": block_id,
                    "arm": arm,
                    "report_generation": GENERATION[arm],
                    "actual_response_gene": response_gene,
                    "report_gene_target": record.get("gene_target"),
                    "scored_finding_ids": sorted(scored_ids),
                }
            )

    randomizer = random.Random(260731)
    packet_rows: list[dict[str, Any]] = []
    block_to_packet: dict[str, str] = {}
    n_genes = len(response_genes)
    for index_gene in range(n_genes):
        packet_id = f"P{index_gene + 1:03d}"
        packet_blocks = [
            blocks[(arm, response_genes[(index_gene + arm_index) % n_genes])]
            for arm_index, arm in enumerate(ARMS)
        ]
        randomizer.shuffle(packet_blocks)
        expected_keys = [
            [block["block_id"], finding_id]
            for block in packet_blocks
            for finding_id in block["scored_finding_ids"]
        ]
        packet_path = PACKETS / f"{packet_id}.json"
        prompt_path = PROMPTS / f"{packet_id}.md"
        schema_path = SCHEMAS / f"{packet_id}.json"
        packet_path.write_text(
            json.dumps(packet_blocks, indent=2, ensure_ascii=False) + "\n"
        )
        prompt_path.write_text(production_prompt(packet_blocks))
        schema_path.write_text(
            json.dumps(gold.classification_schema(len(expected_keys)), indent=2) + "\n"
        )
        for block in packet_blocks:
            block_to_packet[block["block_id"]] = packet_id
        packet_rows.append(
            {
                "packet_id": packet_id,
                "block_ids": [block["block_id"] for block in packet_blocks],
                "expected_keys": expected_keys,
                "n_findings": len(expected_keys),
                "packet_path": str(packet_path.relative_to(ROOT)),
                "prompt_path": str(prompt_path.relative_to(ROOT)),
                "schema_path": str(schema_path.relative_to(ROOT)),
                "prompt_characters": len(prompt_path.read_text()),
            }
        )
    for row in candidates:
        row["packet_id"] = block_to_packet[row["block_id"]]
    candidates.sort(key=lambda row: (ARMS.index(row["arm"]), row["actual_response_gene"], row["finding_id"]))
    write_csv(CANDIDATES, candidates)

    forbidden = [*ARMS, "260713", "260730", "Within-screen", "Out-of-screen"]
    leaks = []
    for packet in packet_rows:
        prompt = (ROOT / packet["prompt_path"]).read_text()
        for phrase in forbidden:
            if phrase in prompt:
                leaks.append({"packet_id": packet["packet_id"], "phrase": phrase})
    if leaks:
        raise ValueError(f"arm/generation labels leaked into prompts: {leaks[:5]}")

    manifest = {
        "status": "prepared",
        "rubric_source": str(GOLD_SCRIPT.relative_to(ROOT)),
        "gold_summary_source": str(gold.SUMMARY_PATH.relative_to(ROOT)),
        "comparison_design": {
            "reports_per_arm": 150,
            "shared_underlying_response_genes": 150,
            "whole_report_blocks": True,
            "reports_split_across_packets": False,
            "arm_visible_to_grader": False,
            "reported_flag_visible_to_grader": False,
            "shuffle_report_generation_matched": True,
            "unshuffled_generation_matched": False,
            "unshuffled_generation": "260713",
            "shuffle_generation": "260730",
            "excluded_source_finding_types": sorted(gold.EXCLUDED_FINDING_TYPES),
        },
        "response_genes": response_genes,
        "blocks": host_blocks,
        "packets": packet_rows,
        "n_retained_findings": len(candidates),
    }
    MANIFEST.write_text(json.dumps(manifest, indent=2) + "\n")
    print(
        f"prepared {len(packet_rows)} arm-blind packets: {len(host_blocks)} complete "
        f"reports and {len(candidates)} retained findings"
    )
    for arm in ARMS:
        print(arm, sum(row["arm"] == arm for row in candidates), "findings")


_GOLD_VALIDATE = gold.validate_result


def validate_result(packet: dict[str, Any], result_path: Path) -> tuple[bool, str]:
    """Apply gold schema/key checks plus report-reference provenance checks."""
    valid, message = _GOLD_VALIDATE(packet, result_path)
    if not valid:
        return valid, message
    blocks = json.loads((ROOT / packet["packet_path"]).read_text())
    report_refs = {
        str(block["block_id"]): {
            str(ref.get("ref_id"))
            for ref in block["all_report_references"]
            if ref.get("ref_id")
        }
        for block in blocks
    }

    def external_identifiers(*values: Any) -> set[str]:
        """Return normalized strong identifiers, not fuzzy citation matches."""
        identifiers: set[str] = set()
        for value in values:
            if value is None:
                continue
            text = str(value).strip()
            lower = text.lower()
            identifiers.update(
                f"pmid:{match}" for match in re.findall(r"\bpmid\s*:?\s*(\d+)\b", lower)
            )
            identifiers.update(
                f"pmcid:{match.upper()}"
                for match in re.findall(r"\bpmcid\s*:?\s*(pmc\d+)\b", lower)
            )
            identifiers.update(
                f"doi:{match.rstrip('.,;').lower()}"
                for match in re.findall(r"\b10\.\d{4,9}/[^\s\]\[\"<>]+", text, flags=re.I)
            )
            identifiers.update(
                f"url:{match.rstrip('/').lower()}"
                for match in re.findall(r"https?://[^\s\]\[\"<>]+", text, flags=re.I)
            )
        return identifiers

    report_ref_identifiers: dict[str, set[str]] = {}
    for block in blocks:
        block_id = str(block["block_id"])
        aliases: set[str] = set()
        for ref in block["all_report_references"]:
            if ref.get("pmid"):
                aliases.add(f"pmid:{ref['pmid']}")
            if ref.get("pmcid"):
                aliases.add(f"pmcid:{str(ref['pmcid']).upper()}")
            aliases.update(
                external_identifiers(
                    ref.get("pmid"),
                    ref.get("pmcid"),
                    ref.get("url"),
                    ref.get("citation"),
                    ref.get("description"),
                )
            )
        report_ref_identifiers[block_id] = aliases
    rows = json.loads(result_path.read_text())["classifications"]
    for row in rows:
        for source in row.get("supporting_sources") or []:
            provenance = source.get("provenance")
            ref_id = str(source.get("ref_id") or "")
            if provenance in {"linked_reference", "report_reference"}:
                block_id = str(row["block_id"])
                # Some graders namespace report-local identifiers (for example,
                # ``B0005:R008``) because every report starts its references at
                # R001.  Accept that representation only when both the block
                # prefix and the underlying report ref_id match this row.
                local_ref_id = ref_id
                if ":" in ref_id:
                    prefix, local_ref_id = ref_id.split(":", 1)
                    if prefix.startswith("B") and prefix != block_id:
                        return False, "invalid report-reference provenance"
                local_tokens = [
                    token
                    for token in re.split(r"[/,;+\s]+", local_ref_id)
                    if token
                ]
                local_match = bool(local_tokens) and all(
                    token in report_refs[block_id] for token in local_tokens
                )
                identifier_match = bool(
                    external_identifiers(
                        ref_id,
                        source.get("url_or_identifier"),
                        source.get("citation"),
                    )
                    & report_ref_identifiers[block_id]
                )
                if not local_match and not identifier_match:
                    return False, "invalid report-reference provenance"
    return True, "ok"


def load_manifest() -> dict[str, Any]:
    return json.loads(MANIFEST.read_text())


def calibration_packet_ids() -> set[str]:
    manifest = load_manifest()
    gold_rows = read_csv(gold.GOLD_PATH)
    keys = {
        (row["arm"], row["actual_response_gene"], row["finding_id"])
        for row in gold_rows
        if row["set_role"] in {"core", "challenge"}
    }
    source = read_csv(CANDIDATES)
    packet_ids = {
        row["packet_id"]
        for row in source
        if (row["arm"], row["actual_response_gene"], row["finding_id"]) in keys
    }
    if not packet_ids:
        raise ValueError("no production packets overlap the gold set")
    return packet_ids


def run(*, calibration_only: bool, model: str, reasoning_effort: str, workers: int, timeout_seconds: int, force: bool) -> None:
    manifest = load_manifest()
    packets = manifest["packets"]
    if calibration_only:
        selected = calibration_packet_ids()
        packets = [row for row in packets if row["packet_id"] in selected]
    gold.validate_result = validate_result
    results = gold.run_packets(
        packets=packets,
        run_root=RUNS,
        model=model,
        reasoning_effort=reasoning_effort,
        workers=workers,
        timeout_seconds=timeout_seconds,
        force=force,
        phase="final-three-arm",
    )
    status = {
        "scope": "calibration" if calibration_only else "full",
        "model": model,
        "reasoning_effort": reasoning_effort,
        "workers": workers,
        "packet_counts": dict(Counter(row["status"] for row in results)),
        "packets": results,
    }
    RUN_STATUS.write_text(json.dumps(status, indent=2) + "\n")


def available_classifications(*, require_all: bool) -> dict[tuple[str, str], dict[str, Any]]:
    rows: dict[tuple[str, str], dict[str, Any]] = {}
    missing = []
    for packet in load_manifest()["packets"]:
        path = RUNS / packet["packet_id"] / "result.json"
        valid, message = validate_result(packet, path) if path.is_file() else (False, "missing")
        if not valid:
            if require_all:
                missing.append(f"{packet['packet_id']}: {message}")
            continue
        for row in json.loads(path.read_text())["classifications"]:
            key = (str(row["block_id"]), str(row["finding_id"]))
            if key in rows:
                raise ValueError(f"duplicate classification: {key}")
            rows[key] = row
    if missing:
        raise ValueError(f"{len(missing)} packets unavailable; first errors: {missing[:5]}")
    return rows


def calibrate() -> dict[str, Any]:
    """Compare production grades with every finalized gold finding."""
    grades = available_classifications(require_all=False)
    source = {
        (row["arm"], row["actual_response_gene"], row["finding_id"]): row
        for row in read_csv(CANDIDATES)
    }
    comparisons = []
    for truth in read_csv(gold.GOLD_PATH):
        key = (truth["arm"], truth["actual_response_gene"], truth["finding_id"])
        production_source = source.get(key)
        if production_source is None:
            continue
        grade = grades.get((production_source["block_id"], production_source["finding_id"]))
        if grade is None:
            continue
        new_flag = gold.derived_flag(grade)
        production_primary = grade["admissibility"] == "load_bearing" and bool(new_flag)
        production_sensitivity = grade["admissibility"] in {"load_bearing", "evidence_only"} and bool(new_flag)
        gold_primary = truth["valid_for_primary_metric"].lower() == "true"
        gold_sensitivity = truth["valid_for_sensitivity_metric"].lower() == "true"
        comparisons.append(
            {
                "candidate_id": truth["candidate_id"],
                "arm": truth["arm"],
                "actual_response_gene": truth["actual_response_gene"],
                "finding_id": truth["finding_id"],
                "set_role": truth["set_role"],
                "gold_admissibility": truth["admissibility"],
                "production_admissibility": grade["admissibility"],
                "admissibility_match": truth["admissibility"] == grade["admissibility"],
                "gold_source_relation": truth["source_relation"],
                "production_source_relation": grade["source_relation"],
                "source_relation_match": truth["source_relation"] == grade["source_relation"],
                "gold_flag": truth["derived_flag"],
                "production_flag": new_flag,
                "flag_match": truth["derived_flag"] == new_flag,
                "gold_primary": gold_primary,
                "production_primary": production_primary,
                "primary_gate_match": gold_primary == production_primary,
                "gold_sensitivity": gold_sensitivity,
                "production_sensitivity": production_sensitivity,
                "sensitivity_gate_match": gold_sensitivity == production_sensitivity,
                "exact_tuple_match": (
                    truth["admissibility"],
                    truth["claim_scope"],
                    truth["source_relation"],
                    truth["dataset_informativity"],
                )
                == (
                    grade["admissibility"],
                    grade["claim_scope"],
                    grade["source_relation"],
                    grade["dataset_informativity"],
                ),
            }
        )
    if not comparisons:
        raise ValueError("no completed production grades overlap gold findings")
    write_csv(CALIBRATION_COMPARISON, comparisons)
    summary: dict[str, Any] = {"n_gold_compared": len(comparisons)}
    for field in (
        "admissibility_match",
        "source_relation_match",
        "flag_match",
        "primary_gate_match",
        "sensitivity_gate_match",
        "exact_tuple_match",
    ):
        count = sum(bool(row[field]) for row in comparisons)
        summary[field] = {"count": count, "fraction": round(count / len(comparisons), 4)}
    summary["gold_flag_counts"] = dict(Counter(row["gold_flag"] for row in comparisons))
    summary["production_flag_counts"] = dict(Counter(row["production_flag"] for row in comparisons))
    CALIBRATION_SUMMARY.write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))
    return summary


def local_stratum(value: int) -> str:
    if value >= 100:
        return "Strong"
    if value >= 25:
        return "Moderate"
    if value >= 1:
        return "Low"
    return "No local DEGs"


def build_final_rows() -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    grades = available_classifications(require_all=True)
    classified = []
    for source in read_csv(CANDIDATES):
        grade = grades[(source["block_id"], source["finding_id"])]
        flag = gold.derived_flag(grade)
        classified.append(
            {
                **source,
                "admissibility": grade["admissibility"],
                "claim_scope": grade["claim_scope"],
                "source_relation": grade["source_relation"],
                "dataset_informativity": grade["dataset_informativity"],
                "flag": flag,
                "flag_label": FLAG_LABELS.get(flag, "Not assessable"),
                "confidence": grade["confidence"],
                "retrieval_status": grade["retrieval_status"],
                "admissibility_reason": grade["admissibility_reason"],
                "dataset_support_summary": grade["dataset_support_summary"],
                "baseline_or_power_check": grade["baseline_or_power_check"],
                "source_supported_edge": grade["source_supported_edge"],
                "missing_or_conflicting_edge": grade["missing_or_conflicting_edge"],
                "supporting_sources_json": json.dumps(grade["supporting_sources"], ensure_ascii=False),
                "search_summary": grade["search_summary"],
                "valid_for_primary": grade["admissibility"] == "load_bearing" and bool(flag),
                "valid_for_sensitivity": grade["admissibility"] in {"load_bearing", "evidence_only"} and bool(flag),
            }
        )
    write_csv(CLASSIFIED, classified)

    overall = []
    placements = []
    local = []
    for layer in LAYERS:
        field = f"valid_for_{layer}"
        for arm in ARMS:
            selected = [row for row in classified if row["arm"] == arm and row[field]]
            counts = Counter(row["flag"] for row in selected)
            total = len(selected)
            for flag in FLAGS:
                overall.append(
                    {
                        "analysis_layer": layer,
                        "arm": arm,
                        "flag": flag,
                        "flag_label": FLAG_LABELS[flag],
                        "count": counts[flag],
                        "percent": round(100 * counts[flag] / total, 3) if total else 0,
                        "n_findings": total,
                    }
                )
        for row in classified:
            if not row[field]:
                continue
            cell_types = json.loads(row["cell_types_json"] or "[]")
            profile = json.loads(row["signal_profile_json"] or "{}")
            for cell_type in cell_types:
                local_degs = int(profile.get(str(cell_type), 0))
                placements.append(
                    {
                        "analysis_layer": layer,
                        "arm": row["arm"],
                        "actual_response_gene": row["actual_response_gene"],
                        "report_gene_target": row["report_gene_target"],
                        "finding_id": row["finding_id"],
                        "finding_type": row["finding_type"],
                        "admissibility": row["admissibility"],
                        "cell_type": str(cell_type),
                        "local_deg_fdr_0.1": local_degs,
                        "local_signal_stratum": local_stratum(local_degs),
                        "flag": row["flag"],
                        "flag_label": row["flag_label"],
                        "summary": row["summary"],
                    }
                )
        for stratum in STRATA:
            for arm in ARMS:
                selected = [
                    row
                    for row in placements
                    if row["analysis_layer"] == layer
                    and row["arm"] == arm
                    and row["local_signal_stratum"] == stratum
                ]
                counts = Counter(row["flag"] for row in selected)
                total = len(selected)
                unique_findings = len(
                    {(row["actual_response_gene"], row["finding_id"]) for row in selected}
                )
                for flag in FLAGS:
                    local.append(
                        {
                            "analysis_layer": layer,
                            "local_signal_stratum": stratum,
                            "local_signal_label": STRATUM_LABELS[stratum],
                            "arm": arm,
                            "flag": flag,
                            "flag_label": FLAG_LABELS[flag],
                            "count": counts[flag],
                            "percent": round(100 * counts[flag] / total, 3) if total else 0,
                            "n_placements": total,
                            "n_unique_findings": unique_findings,
                        }
                    )
    write_csv(OVERALL_DISTRIBUTION, overall)
    write_csv(PLACEMENTS, placements)
    write_csv(LOCAL_DISTRIBUTION, local)
    return classified, overall, placements, local


def build_finding_max_signal_and_coverage(
    classified: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], dict[str, int]]:
    """Build one-vote finding strata and target×cell-type coverage diagnostics."""
    profiles: dict[str, dict[str, int]] = {}
    for row in read_csv(CANDIDATES):
        gene = row["actual_response_gene"]
        profile = {
            str(cell_type): int(value)
            for cell_type, value in json.loads(row["signal_profile_json"] or "{}").items()
        }
        if gene in profiles and profiles[gene] != profile:
            raise ValueError(f"inconsistent signal profile across arms for {gene}")
        profiles[gene] = profile
    if len(profiles) != 150:
        raise ValueError(f"expected profiles for 150 response genes, found {len(profiles)}")

    primary = [row for row in classified if row["valid_for_primary"]]
    assignments: list[dict[str, Any]] = []
    unassigned = Counter()
    for row in primary:
        cell_types = list(dict.fromkeys(json.loads(row["cell_types_json"] or "[]")))
        profile = profiles[row["actual_response_gene"]]
        if cell_types:
            values = {cell_type: int(profile.get(str(cell_type), 0)) for cell_type in cell_types}
            maximum = max(values.values())
            stratum = local_stratum(maximum)
            dominant = [cell_type for cell_type, value in values.items() if value == maximum]
        else:
            values = {}
            maximum = None
            stratum = "Unassigned"
            dominant = []
            unassigned[row["arm"]] += 1
        assignments.append(
            {
                "arm": row["arm"],
                "actual_response_gene": row["actual_response_gene"],
                "report_gene_target": row["report_gene_target"],
                "finding_id": row["finding_id"],
                "finding_type": row["finding_type"],
                "summary": row["summary"],
                "flag": row["flag"],
                "flag_label": row["flag_label"],
                "n_associated_cell_types": len(cell_types),
                "finding_max_local_deg_fdr_0.1": "" if maximum is None else maximum,
                "finding_max_signal_stratum": stratum,
                "dominant_cell_types_json": json.dumps(dominant, ensure_ascii=False),
                "associated_cell_type_degs_json": json.dumps(values, ensure_ascii=False, sort_keys=True),
            }
        )
    write_csv(FINDING_MAX_SIGNAL, assignments)

    distribution: list[dict[str, Any]] = []
    for stratum in STRATA:
        for arm in ARMS:
            selected = [
                row
                for row in assignments
                if row["arm"] == arm and row["finding_max_signal_stratum"] == stratum
            ]
            counts = Counter(row["flag"] for row in selected)
            total = len(selected)
            for flag in FLAGS:
                distribution.append(
                    {
                        "local_signal_stratum": stratum,
                        "local_signal_label": STRATUM_LABELS[stratum],
                        "arm": arm,
                        "flag": flag,
                        "flag_label": FLAG_LABELS[flag],
                        "count": counts[flag],
                        "percent": round(100 * counts[flag] / total, 3) if total else 0,
                        "n_findings": total,
                        "n_unassigned_findings_in_arm": unassigned[arm],
                    }
                )
    write_csv(FINDING_MAX_DISTRIBUTION, distribution)

    positive_pairs = {
        (gene, cell_type): int(value)
        for gene, profile in profiles.items()
        for cell_type, value in profile.items()
        if int(value) >= 1
    }
    coverage_rows: list[dict[str, Any]] = []
    coverage_summary: list[dict[str, Any]] = []
    for arm in ARMS:
        pair_findings: dict[tuple[str, str], list[dict[str, Any]]] = {
            pair: [] for pair in positive_pairs
        }
        for row in primary:
            if row["arm"] != arm:
                continue
            for cell_type in dict.fromkeys(json.loads(row["cell_types_json"] or "[]")):
                pair = (row["actual_response_gene"], str(cell_type))
                if pair in pair_findings:
                    pair_findings[pair].append(row)
        for (gene, cell_type), findings in sorted(pair_findings.items()):
            flags = sorted({row["flag"] for row in findings}, key=FLAGS.index)
            finding_ids = sorted({row["finding_id"] for row in findings})
            coverage_rows.append(
                {
                    "arm": arm,
                    "actual_response_gene": gene,
                    "cell_type": cell_type,
                    "local_deg_fdr_0.1": positive_pairs[(gene, cell_type)],
                    "covered_by_primary_finding": bool(findings),
                    "n_primary_findings": len(findings),
                    "n_distinct_flags": len(flags),
                    "multiple_findings": len(findings) > 1,
                    "multiple_distinct_flags": len(flags) > 1,
                    "finding_ids_json": json.dumps(finding_ids),
                    "flags_json": json.dumps(flags),
                }
            )
        arm_rows = [row for row in coverage_rows if row["arm"] == arm]
        covered = [row for row in arm_rows if row["covered_by_primary_finding"]]
        multiple_findings = [row for row in arm_rows if row["multiple_findings"]]
        multiple_flags = [row for row in arm_rows if row["multiple_distinct_flags"]]
        positive_cell_types = {row["cell_type"] for row in arm_rows}
        covered_cell_types = {row["cell_type"] for row in covered}
        coverage_summary.append(
            {
                "arm": arm,
                "n_positive_target_celltype_pairs": len(arm_rows),
                "n_pairs_covered_by_primary_finding": len(covered),
                "percent_pairs_covered": round(100 * len(covered) / len(arm_rows), 3),
                "n_pairs_uncovered": len(arm_rows) - len(covered),
                "n_positive_cell_type_categories": len(positive_cell_types),
                "n_cell_type_categories_covered": len(covered_cell_types),
                "uncovered_cell_type_categories_json": json.dumps(
                    sorted(positive_cell_types - covered_cell_types), ensure_ascii=False
                ),
                "n_pairs_with_multiple_findings": len(multiple_findings),
                "percent_all_pairs_with_multiple_findings": round(
                    100 * len(multiple_findings) / len(arm_rows), 3
                ),
                "percent_covered_pairs_with_multiple_findings": round(
                    100 * len(multiple_findings) / len(covered), 3
                ),
                "n_pairs_with_multiple_distinct_flags": len(multiple_flags),
                "percent_all_pairs_with_multiple_distinct_flags": round(
                    100 * len(multiple_flags) / len(arm_rows), 3
                ),
                "percent_covered_pairs_with_multiple_distinct_flags": round(
                    100 * len(multiple_flags) / len(covered), 3
                ),
            }
        )
    write_csv(POSITIVE_PAIR_COVERAGE, coverage_rows)
    write_csv(POSITIVE_PAIR_COVERAGE_SUMMARY, coverage_summary)
    return assignments, distribution, coverage_rows, coverage_summary, dict(unassigned)


def build_unshuffled_coverage_by_deg(
    coverage_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Bin unshuffled positive pairs by DEG count and summarize flag coverage."""
    unshuffled = [row for row in coverage_rows if row["arm"] == ARMS[0]]
    output: list[dict[str, Any]] = []
    for lower, upper, label in DEG_COVERAGE_BINS:
        selected = [
            row
            for row in unshuffled
            if int(row["local_deg_fdr_0.1"]) >= lower
            and (upper is None or int(row["local_deg_fdr_0.1"]) <= upper)
        ]
        uncovered = sum(not row["covered_by_primary_finding"] for row in selected)
        one_flag = sum(
            row["covered_by_primary_finding"] and int(row["n_distinct_flags"]) == 1
            for row in selected
        )
        multiple_flags = sum(int(row["n_distinct_flags"]) > 1 for row in selected)
        total = len(selected)
        covered = one_flag + multiple_flags
        output.append(
            {
                "deg_bin": label,
                "deg_lower_inclusive": lower,
                "deg_upper_inclusive": "" if upper is None else upper,
                "n_positive_pairs": total,
                "n_uncovered": uncovered,
                "n_covered_one_distinct_flag": one_flag,
                "n_covered_multiple_distinct_flags": multiple_flags,
                "n_covered_any_flag": covered,
                "percent_covered_any_flag": round(100 * covered / total, 3),
                "percent_with_multiple_distinct_flags": round(
                    100 * multiple_flags / total, 3
                ),
                "percent_covered_pairs_with_multiple_distinct_flags": round(
                    100 * multiple_flags / covered, 3
                )
                if covered
                else 0,
            }
        )
    if sum(row["n_positive_pairs"] for row in output) != len(unshuffled):
        raise ValueError("DEG coverage bins do not exhaust unshuffled positive pairs")
    write_csv(UNSHUFFLED_COVERAGE_BY_DEG, output)
    return output


def setup_matplotlib() -> Any:
    os.environ.setdefault("MPLCONFIGDIR", "/tmp/mplconfig_final_three_arm_distribution")
    Path(os.environ["MPLCONFIGDIR"]).mkdir(parents=True, exist_ok=True)
    import matplotlib.pyplot as plt

    if STYLE.is_file():
        plt.style.use(STYLE)
    plt.rcParams.update({"svg.fonttype": "none", "pdf.fonttype": 42})
    return plt


def save_figure(fig: Any, stem: Path) -> None:
    fig.savefig(stem.with_suffix(".png"), dpi=150, bbox_inches="tight")
    fig.savefig(stem.with_suffix(".svg"), bbox_inches="tight")
    fig.savefig(stem.with_suffix(".pdf"), bbox_inches="tight")


def plot_overall(rows: list[dict[str, Any]], layer: str) -> None:
    plt = setup_matplotlib()
    from matplotlib.patches import Patch

    lookup = {(row["arm"], row["flag"]): row for row in rows if row["analysis_layer"] == layer}
    fig, ax = plt.subplots(figsize=(9.1, 3.8))
    y_values = list(range(len(ARMS) - 1, -1, -1))
    for y, arm in zip(y_values, ARMS):
        left = 0.0
        for flag in FLAGS:
            row = lookup[(arm, flag)]
            width = float(row["percent"])
            ax.barh(y, width, left=left, height=0.62, color=COLORS[flag], edgecolor="white", linewidth=0.8)
            if width >= 6:
                color = "white" if flag in {"disagree", "inferred"} else "#333333"
                ax.text(left + width / 2, y, f"{width:.1f}%", ha="center", va="center", fontsize=9, color=color)
            elif width >= 1:
                color = "white" if flag in {"disagree", "inferred"} else "#333333"
                ax.text(
                    left + width / 2,
                    y,
                    f"{width:.1f}%",
                    ha="center",
                    va="center",
                    rotation=90,
                    fontsize=5.5,
                    color=color,
                )
            left += width
        ax.text(101.2, y, f"n={lookup[(arm, FLAGS[0])]['n_findings']:,}", va="center", fontsize=9, color="#555555", clip_on=False)
    ax.set_yticks(y_values, ARMS)
    ax.set_xlim(0, 100)
    ax.set_xlabel("Percent of retained findings")
    ax.set_title(
        "Literature relationship after arm-blind gold-calibrated review",
        loc="left",
        pad=18,
    )
    subtitle = "Load-bearing findings" if layer == "primary" else "Sensitivity: load-bearing + evidence-only"
    ax.text(0, 1.04, subtitle, transform=ax.transAxes, fontsize=9, color="#666666")
    ax.spines[["top", "right", "left"]].set_visible(False)
    ax.tick_params(axis="y", length=0)
    handles = [Patch(facecolor=COLORS[flag], label=FLAG_LABELS[flag]) for flag in FLAGS]
    ax.legend(handles=handles, loc="upper center", bbox_to_anchor=(0.5, -0.24), ncol=4, frameon=False)
    fig.subplots_adjust(left=0.25, right=0.92, bottom=0.30, top=0.80)
    save_figure(fig, HERE / f"final_flag_distribution_{layer}")
    plt.close(fig)


def plot_local(rows: list[dict[str, Any]], layer: str) -> None:
    plt = setup_matplotlib()
    from matplotlib.patches import Patch

    lookup = {
        (row["local_signal_stratum"], row["arm"], row["flag"]): row
        for row in rows
        if row["analysis_layer"] == layer
    }
    labels = [(stratum, arm) for stratum in STRATA for arm in ARMS]
    y_values = list(range(len(labels) - 1, -1, -1))
    fig, ax = plt.subplots(figsize=(10.8, 7.8))
    for y, (stratum, arm) in zip(y_values, labels):
        left = 0.0
        for flag in FLAGS:
            row = lookup[(stratum, arm, flag)]
            width = float(row["percent"])
            ax.barh(y, width, left=left, height=0.64, color=COLORS[flag], edgecolor="white", linewidth=0.7)
            if width >= 7:
                color = "white" if flag in {"disagree", "inferred"} else "#333333"
                ax.text(left + width / 2, y, f"{width:.1f}%", ha="center", va="center", fontsize=8, color=color)
            elif width >= 1:
                color = "white" if flag in {"disagree", "inferred"} else "#333333"
                ax.text(
                    left + width / 2,
                    y,
                    f"{width:.1f}%",
                    ha="center",
                    va="center",
                    rotation=90,
                    fontsize=5,
                    color=color,
                )
            left += width
        ax.text(101.2, y, f"n={lookup[(stratum, arm, FLAGS[0])]['n_placements']:,}", va="center", fontsize=8, color="#555555", clip_on=False)
    for index in range(1, len(STRATA)):
        y_line = len(labels) - index * len(ARMS) - 0.5
        ax.plot([-0.52, 1.06], [y_line, y_line], transform=ax.get_yaxis_transform(), color="#aaa89f", linewidth=0.8, linestyle=(0, (4, 3)), clip_on=False)
    ytick_labels = [f"{STRATUM_LABELS[stratum]} · {arm}" for stratum, arm in labels]
    ax.set_yticks(y_values, ytick_labels)
    ax.set_xlim(0, 100)
    ax.set_xlabel("Percent of finding × associated-cell-type placements")
    ax.set_title("Literature relationship by target × cell-type signal", loc="left", pad=20)
    subtitle = "Load-bearing findings" if layer == "primary" else "Sensitivity: load-bearing + evidence-only"
    ax.text(0, 1.025, subtitle, transform=ax.transAxes, fontsize=9, color="#666666")
    ax.spines[["top", "right", "left"]].set_visible(False)
    ax.tick_params(axis="y", length=0, labelsize=8.5)
    handles = [Patch(facecolor=COLORS[flag], label=FLAG_LABELS[flag]) for flag in FLAGS]
    ax.legend(handles=handles, loc="upper center", bbox_to_anchor=(0.5, -0.10), ncol=4, frameon=False)
    fig.subplots_adjust(left=0.41, right=0.92, bottom=0.15, top=0.89)
    save_figure(fig, HERE / f"final_flag_distribution_by_celltype_signal_{layer}")
    plt.close(fig)


def plot_finding_max_signal(rows: list[dict[str, Any]], unassigned: dict[str, int]) -> None:
    """Plot primary flags once per finding using its maximum listed local signal."""
    plt = setup_matplotlib()
    from matplotlib.patches import Patch

    lookup = {
        (row["local_signal_stratum"], row["arm"], row["flag"]): row
        for row in rows
    }
    labels = [(stratum, arm) for stratum in STRATA for arm in ARMS]
    y_values = list(range(len(labels) - 1, -1, -1))
    fig, ax = plt.subplots(figsize=(10.8, 7.8))
    for y, (stratum, arm) in zip(y_values, labels):
        left = 0.0
        for flag in FLAGS:
            row = lookup[(stratum, arm, flag)]
            width = float(row["percent"])
            ax.barh(
                y,
                width,
                left=left,
                height=0.64,
                color=COLORS[flag],
                edgecolor="white",
                linewidth=0.7,
            )
            color = "white" if flag in {"disagree", "inferred"} else "#333333"
            if width >= 7:
                ax.text(
                    left + width / 2,
                    y,
                    f"{width:.1f}%",
                    ha="center",
                    va="center",
                    fontsize=8,
                    color=color,
                )
            elif width >= 1:
                ax.text(
                    left + width / 2,
                    y,
                    f"{width:.1f}%",
                    ha="center",
                    va="center",
                    rotation=90,
                    fontsize=5,
                    color=color,
                )
            left += width
        ax.text(
            101.2,
            y,
            f"n={lookup[(stratum, arm, FLAGS[0])]['n_findings']:,}",
            va="center",
            fontsize=8,
            color="#555555",
            clip_on=False,
        )
    for index in range(1, len(STRATA)):
        y_line = len(labels) - index * len(ARMS) - 0.5
        ax.plot(
            [-0.52, 1.06],
            [y_line, y_line],
            transform=ax.get_yaxis_transform(),
            color="#aaa89f",
            linewidth=0.8,
            linestyle=(0, (4, 3)),
            clip_on=False,
        )
    ax.set_yticks(
        y_values,
        [f"{STRATUM_LABELS[stratum]} · {arm}" for stratum, arm in labels],
    )
    ax.set_xlim(0, 100)
    ax.set_xlabel("Percent of findings")
    ax.set_title(
        "Literature relationship by finding-level maximum local signal",
        loc="left",
        pad=20,
    )
    unassigned_text = " / ".join(f"{unassigned.get(arm, 0):,}" for arm in ARMS)
    ax.text(
        0,
        1.025,
        "Load-bearing findings; one finding = one vote; maximum DEG count among listed cell types. "
        f"Unassigned (U / W / O): {unassigned_text}",
        transform=ax.transAxes,
        fontsize=8.5,
        color="#666666",
    )
    ax.spines[["top", "right", "left"]].set_visible(False)
    ax.tick_params(axis="y", length=0, labelsize=8.5)
    handles = [Patch(facecolor=COLORS[flag], label=FLAG_LABELS[flag]) for flag in FLAGS]
    ax.legend(
        handles=handles,
        loc="upper center",
        bbox_to_anchor=(0.5, -0.10),
        ncol=4,
        frameon=False,
    )
    fig.subplots_adjust(left=0.41, right=0.92, bottom=0.15, top=0.89)
    save_figure(fig, HERE / "final_flag_distribution_by_finding_max_signal_primary")
    plt.close(fig)


def plot_unshuffled_coverage_by_deg(rows: list[dict[str, Any]]) -> None:
    """Plot positive-pair counts and coverage rates across local DEG bins."""
    plt = setup_matplotlib()
    from matplotlib.patches import Patch

    x_values = list(range(len(rows)))
    uncovered = [int(row["n_uncovered"]) for row in rows]
    one_flag = [int(row["n_covered_one_distinct_flag"]) for row in rows]
    multiple_flags = [int(row["n_covered_multiple_distinct_flags"]) for row in rows]
    totals = [int(row["n_positive_pairs"]) for row in rows]
    coverage_percent = [float(row["percent_covered_any_flag"]) for row in rows]
    multiple_percent = [
        float(row["percent_with_multiple_distinct_flags"]) for row in rows
    ]
    colors = {
        "uncovered": "#c3c2b7",
        "one": "#78a8c2",
        "multiple": "#3f6f8f",
    }

    fig, (ax_count, ax_rate) = plt.subplots(
        2,
        1,
        figsize=(9.4, 6.4),
        sharex=True,
        gridspec_kw={"height_ratios": [1.2, 1], "hspace": 0.16},
    )
    ax_count.bar(x_values, uncovered, color=colors["uncovered"], width=0.76)
    ax_count.bar(
        x_values,
        one_flag,
        bottom=uncovered,
        color=colors["one"],
        width=0.76,
    )
    covered_bottom = [a + b for a, b in zip(uncovered, one_flag)]
    ax_count.bar(
        x_values,
        multiple_flags,
        bottom=covered_bottom,
        color=colors["multiple"],
        width=0.76,
    )
    for x, total in zip(x_values, totals):
        ax_count.text(
            x,
            total + max(totals) * 0.018,
            f"n={total:,}",
            ha="center",
            va="bottom",
            fontsize=7.5,
            color="#555555",
        )
    ax_count.set_ylim(0, max(totals) * 1.14)
    ax_count.set_ylabel("Positive target × cell-type pairs")
    ax_count.legend(
        handles=[
            Patch(facecolor=colors["uncovered"], label="Uncovered"),
            Patch(facecolor=colors["one"], label="Covered: one flag"),
            Patch(facecolor=colors["multiple"], label="Covered: multiple flags"),
        ],
        loc="upper right",
        frameon=False,
        ncol=3,
        fontsize=8,
    )

    ax_rate.plot(
        x_values,
        coverage_percent,
        color="#3f8f68",
        marker="o",
        linewidth=2,
        label="Covered by any primary finding",
    )
    ax_rate.plot(
        x_values,
        multiple_percent,
        color=colors["multiple"],
        marker="o",
        linewidth=1.8,
        label="Assigned multiple distinct flags",
    )
    for x, value in zip(x_values, coverage_percent):
        ax_rate.text(
            x,
            min(value + 4, 102),
            f"{value:.1f}%",
            ha="center",
            va="bottom",
            fontsize=7.5,
            color="#2f6f50",
        )
    ax_rate.set_ylim(0, 108)
    ax_rate.set_yticks([0, 25, 50, 75, 100], ["0%", "25%", "50%", "75%", "100%"])
    ax_rate.set_ylabel("Percent of pairs")
    ax_rate.set_xlabel("DEGs in the target × cell-type combination (FDR < 0.1)")
    ax_rate.set_xticks(x_values, [row["deg_bin"] for row in rows])
    ax_rate.legend(loc="upper left", frameon=False, fontsize=8)

    for ax in (ax_count, ax_rate):
        ax.spines[["top", "right"]].set_visible(False)
        ax.grid(axis="y", color="#ddddda", linewidth=0.6, alpha=0.8)
        ax.set_axisbelow(True)
    fig.suptitle(
        "Unshuffled primary-finding coverage rises with local DEG count",
        x=0.11,
        ha="left",
        y=0.98,
        fontsize=12,
    )
    fig.text(
        0.11,
        0.945,
        "Positive target × cell-type pairs only (≥1 DEG; n=1,124). Multiple flags means multiple distinct literature categories.",
        ha="left",
        fontsize=8.5,
        color="#666666",
    )
    fig.subplots_adjust(left=0.11, right=0.97, bottom=0.12, top=0.88)
    save_figure(fig, HERE / "final_unshuffled_positive_pair_coverage_vs_deg_primary")
    plt.close(fig)


def summarize() -> None:
    calibration = calibrate()
    classified, overall, placements, local = build_final_rows()
    max_assignments, max_distribution, coverage_rows, coverage_summary, unassigned = (
        build_finding_max_signal_and_coverage(classified)
    )
    unshuffled_coverage_by_deg = build_unshuffled_coverage_by_deg(coverage_rows)
    for layer in LAYERS:
        plot_overall(overall, layer)
        plot_local(local, layer)
    plot_finding_max_signal(max_distribution, unassigned)
    plot_unshuffled_coverage_by_deg(unshuffled_coverage_by_deg)
    summary = {
        "status": "complete",
        "comparison_design": load_manifest()["comparison_design"],
        "n_classified_findings": len(classified),
        "admissibility_counts": dict(Counter(row["admissibility"] for row in classified)),
        "retained_findings_by_layer_and_arm": {
            layer: {
                arm: sum(row["arm"] == arm and row[f"valid_for_{layer}"] for row in classified)
                for arm in ARMS
            }
            for layer in LAYERS
        },
        "placement_counts_by_layer_and_arm": {
            layer: {
                arm: sum(row["analysis_layer"] == layer and row["arm"] == arm for row in placements)
                for arm in ARMS
            }
            for layer in LAYERS
        },
        "finding_max_signal_primary": {
            "n_assigned_by_arm": {
                arm: sum(
                    row["arm"] == arm and row["finding_max_signal_stratum"] != "Unassigned"
                    for row in max_assignments
                )
                for arm in ARMS
            },
            "n_unassigned_by_arm": {arm: unassigned.get(arm, 0) for arm in ARMS},
            "definition": "One load-bearing finding per vote; maximum FDR<0.1 DEG count among its listed cell types.",
        },
        "positive_pair_coverage_primary": {
            row["arm"]: {
                key: value for key, value in row.items() if key != "arm"
            }
            for row in coverage_summary
        },
        "gold_calibration": calibration,
        "local_signal_boundaries": {
            "Strong": "≥100 target×cell-type DEGs at FDR<0.1",
            "Moderate": "25–99",
            "Low": "1–24",
            "No local DEGs": "0; absent canonical target×cell pairs are treated as 0",
        },
        "outputs": {
            "classified_findings": str(CLASSIFIED.relative_to(ROOT)),
            "overall_distribution": str(OVERALL_DISTRIBUTION.relative_to(ROOT)),
            "placements": str(PLACEMENTS.relative_to(ROOT)),
            "local_distribution": str(LOCAL_DISTRIBUTION.relative_to(ROOT)),
            "finding_max_signal_assignments_primary": str(FINDING_MAX_SIGNAL.relative_to(ROOT)),
            "finding_max_signal_distribution_primary": str(FINDING_MAX_DISTRIBUTION.relative_to(ROOT)),
            "positive_pair_coverage_primary": str(POSITIVE_PAIR_COVERAGE.relative_to(ROOT)),
            "positive_pair_coverage_summary_primary": str(
                POSITIVE_PAIR_COVERAGE_SUMMARY.relative_to(ROOT)
            ),
            "unshuffled_positive_pair_coverage_by_deg_primary": str(
                UNSHUFFLED_COVERAGE_BY_DEG.relative_to(ROOT)
            ),
        },
    }
    SUMMARY.write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("prepare")
    for name in ("run-calibration", "run-full"):
        run_parser = sub.add_parser(name)
        run_parser.add_argument("--model", default="gpt-5.6-sol")
        run_parser.add_argument("--reasoning-effort", default="high")
        run_parser.add_argument("--workers", type=int, default=10)
        run_parser.add_argument("--timeout-seconds", type=int, default=1200)
        run_parser.add_argument("--force", action="store_true")
    sub.add_parser("calibrate")
    sub.add_parser("summarize")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.command == "prepare":
        prepare()
    elif args.command in {"run-calibration", "run-full"}:
        run(
            calibration_only=args.command == "run-calibration",
            model=args.model,
            reasoning_effort=args.reasoning_effort,
            workers=args.workers,
            timeout_seconds=args.timeout_seconds,
            force=args.force,
        )
    elif args.command == "calibrate":
        calibrate()
    elif args.command == "summarize":
        summarize()


if __name__ == "__main__":
    main()
