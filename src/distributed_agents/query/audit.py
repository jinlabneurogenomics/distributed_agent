"""Structural audits for completed direct/adaptive query runs."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path
from typing import Any

from ..skills.registry import RUNTIME_SKILLS_DIR
from .context import sha256_path


def _validate_sweep_result_file(
    path: Path,
    *,
    expected_ids: list[str],
) -> list[str]:
    """Independently verify a reader ledger without trusting its generated audit."""

    errors: list[str] = []
    seen: list[str] = []
    allowed_keys = {
        "unit_id",
        "decision",
        "records",
        "rationale",
        "evidence_ids",
        "uncertainty",
    }
    try:
        handle = path.open(encoding="utf-8")
    except OSError as exc:
        return [f"cannot read reader results: {exc}"]
    with handle:
        for line_number, raw in enumerate(handle, 1):
            if not raw.strip():
                continue
            try:
                row = json.loads(raw)
            except json.JSONDecodeError as exc:
                errors.append(f"result line {line_number} is invalid JSON: {exc}")
                continue
            label = f"result line {line_number}"
            if not isinstance(row, dict):
                errors.append(f"{label} is not an object")
                continue
            if set(row) != allowed_keys:
                errors.append(f"{label} has the wrong fields")
            unit_id = row.get("unit_id")
            if not isinstance(unit_id, str) or not unit_id:
                errors.append(f"{label} has an invalid unit_id")
            else:
                seen.append(unit_id)
            decision = row.get("decision")
            records = row.get("records")
            if decision not in {"emit", "reject"}:
                errors.append(f"{label} has an invalid decision")
            if not isinstance(records, list) or not all(
                isinstance(record, dict) for record in records
            ):
                errors.append(f"{label} has invalid records")
            elif decision == "emit" and not records:
                errors.append(f"{label} emits no records")
            elif decision == "reject" and records:
                errors.append(f"{label} rejects with nonempty records")
            if not isinstance(row.get("rationale"), str) or not str(
                row.get("rationale", "")
            ).strip():
                errors.append(f"{label} has no rationale")
            evidence_ids = row.get("evidence_ids")
            if not isinstance(evidence_ids, list) or not all(
                isinstance(value, str) for value in evidence_ids
            ):
                errors.append(f"{label} has invalid evidence_ids")
            if row.get("uncertainty") not in {"low", "medium", "high"}:
                errors.append(f"{label} has invalid uncertainty")

    expected = set(expected_ids)
    actual = set(seen)
    duplicates = sorted(
        unit_id for unit_id, count in Counter(seen).items() if count > 1
    )
    missing = sorted(expected - actual)
    extra = sorted(actual - expected)
    if duplicates:
        errors.append(f"duplicate unit IDs: {', '.join(duplicates)}")
    if missing:
        errors.append(f"missing unit IDs: {', '.join(missing)}")
    if extra:
        errors.append(f"extra unit IDs: {', '.join(extra)}")
    return errors


def audit_adaptive_artifacts(
    *,
    mode: str,
    pipeline_dir: Path,
    capability_manifest: Path | None,
) -> dict[str, Any]:
    """Return structural diagnostics and fail-closed sweep errors."""

    if mode not in {"direct", "adaptive"}:
        return {
            "status": "not_applicable",
            "warnings": [],
            "blocking_errors": [],
            "artifacts": {},
        }
    artifacts: dict[str, str] = {}
    warnings: list[str] = []
    for name in (
        "capabilities",
        "measurement_registry",
        "task_bindings",
        "coverage",
        "adaptive_plan",
        "adaptive_plan_validation",
        "answer_audit",
    ):
        path = pipeline_dir / f"{name}.json"
        if path.is_file():
            artifacts[name] = str(path)
    execution = pipeline_dir / "execution.jsonl"
    if execution.is_file():
        artifacts["execution"] = str(execution)
    if mode == "adaptive":
        if "coverage" not in artifacts:
            warnings.append("adaptive run did not receive coverage.json")
        plan = pipeline_dir / "adaptive_plan.json"
        if plan.is_file() and capability_manifest is not None:
            validator = (
                RUNTIME_SKILLS_DIR
                / "adaptive-query-skill"
                / "scripts"
                / "validate_plan.py"
            )
            out = pipeline_dir / "adaptive_plan_host_validation.json"
            done = subprocess.run(
                [
                    sys.executable,
                    str(validator),
                    "--plan",
                    str(plan),
                    "--capabilities",
                    str(capability_manifest),
                    "--out",
                    str(out),
                ],
                capture_output=True,
                text=True,
                timeout=30,
                check=False,
            )
            artifacts["adaptive_plan_host_validation"] = str(out)
            if done.returncode:
                warnings.append("adaptive plan failed host structural validation")
    warnings.extend(_audit_semantic_graph_policy(pipeline_dir))
    selection = _audit_candidate_selection_process(pipeline_dir)
    warnings.extend(selection["warnings"])
    graph_review = _audit_predictive_graph_review(pipeline_dir)
    warnings.extend(graph_review["warnings"])
    artifacts.update(graph_review["artifacts"])
    corpus_sweep = _audit_exhaustive_corpus_sweep(pipeline_dir)
    artifacts.update(corpus_sweep["artifacts"])
    blocking_errors = list(corpus_sweep["blocking_errors"])
    return {
        "status": (
            "failed"
            if blocking_errors
            else "warning" if warnings else "passed"
        ),
        "warnings": warnings,
        "blocking_errors": blocking_errors,
        "artifacts": artifacts,
        "selection_process": selection,
        "predictive_graph_review": graph_review,
        "exhaustive_corpus_sweep": corpus_sweep,
    }


def _audit_exhaustive_corpus_sweep(pipeline_dir: Path) -> dict[str, Any]:
    """Fail closed when a declared exhaustive sweep lacks exact accounting."""

    sweep_dir = pipeline_dir / "corpus_sweep"
    plan_path = sweep_dir / "sweep_plan.json"
    if not plan_path.is_file():
        return {
            "status": "not_applicable",
            "blocking_errors": [],
            "artifacts": {},
            "counts": {},
        }

    artifacts = {"corpus_sweep_plan": str(plan_path)}
    errors: list[str] = []
    try:
        plan = json.loads(plan_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        plan = {}
        errors.append(f"invalid exhaustive corpus sweep plan: {exc}")
    if plan.get("schema_version") != "distributed_agents-corpus-sweep-plan-v1":
        errors.append("exhaustive corpus sweep plan has the wrong schema")
    units = plan.get("units")
    unit_entries = units if isinstance(units, list) else []
    planned_ids = (
        [
            str(row.get("unit_id"))
            for row in unit_entries
            if isinstance(row, dict) and row.get("unit_id") is not None
        ]
    )
    if not planned_ids or len(planned_ids) != len(set(planned_ids)):
        errors.append("exhaustive corpus sweep plan has invalid unit accounting")
    if plan.get("unit_count") != len(planned_ids):
        errors.append("exhaustive corpus sweep plan unit count does not match units")
    for label in ("input", "task"):
        identity = plan.get(label)
        if not isinstance(identity, dict):
            errors.append(f"exhaustive corpus sweep plan lacks {label} identity")
            continue
        identity_path = Path(str(identity.get("path", "")))
        if not identity_path.is_file():
            errors.append(f"exhaustive corpus sweep {label} is missing")
        elif identity.get("sha256") != sha256_path(identity_path):
            errors.append(f"exhaustive corpus sweep {label} hash changed")
        if label == "task":
            expected_task = pipeline_dir.resolve().parents[1] / "task.md"
            if identity_path.resolve() != expected_task.resolve():
                errors.append("exhaustive corpus sweep references another task")
    release_identity = plan.get("release_manifest")
    if release_identity is not None:
        if not isinstance(release_identity, dict):
            errors.append("exhaustive corpus sweep has an invalid release identity")
        else:
            release_path = Path(str(release_identity.get("path", "")))
            if not release_path.is_file():
                errors.append("exhaustive corpus sweep release manifest is missing")
            elif release_identity.get("sha256") != sha256_path(release_path):
                errors.append("exhaustive corpus sweep release manifest hash changed")

    slices = plan.get("slices")
    slice_entries = slices if isinstance(slices, list) else []
    if not slice_entries or plan.get("slice_count") != len(slice_entries):
        errors.append("exhaustive corpus sweep plan has invalid slice accounting")
    planned_slice_ids: set[str] = set()
    for entry in slice_entries:
        if not isinstance(entry, dict) or not isinstance(entry.get("slice_id"), str):
            errors.append("exhaustive corpus sweep plan has an invalid slice")
            continue
        slice_id = entry["slice_id"]
        if slice_id in planned_slice_ids:
            errors.append("exhaustive corpus sweep plan repeats a slice ID")
        planned_slice_ids.add(slice_id)
        slice_path = Path(str(entry.get("path", "")))
        expected_slice_path = sweep_dir / "slices" / f"{slice_id}.jsonl"
        if slice_path.resolve() != expected_slice_path.resolve():
            errors.append(f"exhaustive corpus sweep {slice_id} has the wrong path")
        if not slice_path.is_file():
            errors.append(f"exhaustive corpus sweep {slice_id} is missing")
        elif entry.get("sha256") != sha256_path(slice_path):
            errors.append(f"exhaustive corpus sweep {slice_id} hash changed")
        assigned = sum(
            isinstance(row, dict) and row.get("slice_id") == slice_id
            for row in unit_entries
        )
        if entry.get("unit_count") != assigned:
            errors.append(
                f"exhaustive corpus sweep {slice_id} unit count is inconsistent"
            )
    unit_slice_ids = {
        str(row.get("slice_id"))
        for row in unit_entries
        if isinstance(row, dict) and row.get("slice_id") is not None
    }
    if unit_slice_ids != planned_slice_ids:
        errors.append("exhaustive corpus sweep units and slices do not match")

    audit_path = sweep_dir / "sweep_audit.json"
    audit: dict[str, Any] = {}
    if not audit_path.is_file():
        errors.append("exhaustive corpus sweep was planned but not reconciled")
    else:
        artifacts["corpus_sweep_audit"] = str(audit_path)
        try:
            loaded = json.loads(audit_path.read_text(encoding="utf-8"))
            audit = loaded if isinstance(loaded, dict) else {}
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"invalid exhaustive corpus sweep audit: {exc}")
        if audit.get("schema_version") != "distributed_agents-corpus-sweep-audit-v1":
            errors.append("exhaustive corpus sweep audit has the wrong schema")
        if audit.get("status") != "passed":
            errors.append("exhaustive corpus sweep audit did not pass")
        if audit.get("plan_sha256") != sha256_path(plan_path):
            errors.append("exhaustive corpus sweep audit references another plan")
        counts = audit.get("counts")
        if not isinstance(counts, dict):
            errors.append("exhaustive corpus sweep audit lacks counts")
            counts = {}
        if counts.get("planned") != len(planned_ids):
            errors.append("exhaustive corpus sweep planned count is inconsistent")
        if counts.get("covered") != len(planned_ids):
            errors.append("exhaustive corpus sweep did not cover every planned unit")
        disposition_counts = (
            counts.get("emitted_units"),
            counts.get("rejected_units"),
            counts.get("emitted_records"),
        )
        if not all(
            isinstance(value, int) and value >= 0 for value in disposition_counts
        ):
            errors.append("exhaustive corpus sweep has invalid disposition counts")
        elif counts["emitted_units"] + counts["rejected_units"] != len(
            planned_ids
        ):
            errors.append("exhaustive corpus sweep dispositions are incomplete")
        for name in ("missing_ids", "extra_ids", "duplicate_ids", "errors"):
            values = audit.get(name)
            if not isinstance(values, list) or values:
                errors.append(f"exhaustive corpus sweep audit has nonempty {name}")
        audited_slices = audit.get("slices")
        audit_slice_entries = (
            audited_slices if isinstance(audited_slices, list) else []
        )
        audited_slice_ids: set[str] = set()
        for entry in audit_slice_entries:
            if not isinstance(entry, dict) or not isinstance(
                entry.get("slice_id"), str
            ):
                errors.append("exhaustive corpus sweep audit has an invalid slice")
                continue
            slice_id = entry["slice_id"]
            if slice_id in audited_slice_ids:
                errors.append("exhaustive corpus sweep audit repeats a slice ID")
            audited_slice_ids.add(slice_id)
            if entry.get("status") != "passed" or entry.get("errors") != []:
                errors.append(f"exhaustive corpus sweep {slice_id} did not pass")
            results_path = Path(str(entry.get("results_path", "")))
            expected_results_path = (
                sweep_dir / "workers" / slice_id / "slice_results.jsonl"
            )
            if results_path.resolve() != expected_results_path.resolve():
                errors.append(
                    f"exhaustive corpus sweep {slice_id} results have the wrong path"
                )
            if not results_path.is_file():
                errors.append(f"exhaustive corpus sweep {slice_id} results are missing")
            elif entry.get("results_sha256") != sha256_path(results_path):
                errors.append(
                    f"exhaustive corpus sweep {slice_id} result hash changed"
                )
            else:
                expected_result_ids = [
                    str(row["unit_id"])
                    for row in unit_entries
                    if isinstance(row, dict)
                    and row.get("unit_id") is not None
                    and row.get("slice_id") == slice_id
                ]
                errors.extend(
                    f"exhaustive corpus sweep {slice_id}: {error}"
                    for error in _validate_sweep_result_file(
                        results_path,
                        expected_ids=expected_result_ids,
                    )
                )
            slice_counts = entry.get("counts")
            planned_count = sum(
                isinstance(row, dict) and row.get("slice_id") == slice_id
                for row in unit_entries
            )
            if not isinstance(slice_counts, dict) or (
                slice_counts.get("planned") != planned_count
                or slice_counts.get("covered") != planned_count
            ):
                errors.append(
                    f"exhaustive corpus sweep {slice_id} coverage is inconsistent"
                )
        if audited_slice_ids != planned_slice_ids:
            errors.append("exhaustive corpus sweep audit does not cover every slice")
        merged_path = sweep_dir / "merged_candidates.jsonl"
        if not merged_path.is_file():
            errors.append("exhaustive corpus sweep lacks reconciled candidates")
        else:
            artifacts["corpus_sweep_candidates"] = str(merged_path)
            if audit.get("merged_sha256") != sha256_path(merged_path):
                errors.append("exhaustive corpus sweep candidate hash changed")

    return {
        "status": "failed" if errors else "passed",
        "blocking_errors": list(dict.fromkeys(errors)),
        "artifacts": artifacts,
        "counts": audit.get("counts", {}) if isinstance(audit, dict) else {},
    }


def _audit_candidate_selection_process(pipeline_dir: Path) -> dict[str, Any]:
    """Diagnose evidence ordering when a run emits candidate-selection artifacts."""

    evidence_dir = pipeline_dir / "evidence"
    paths = {
        name: evidence_dir / filename
        for name, filename in (
            ("candidate_pool", "candidate_pool.json"),
            ("ordering_basis", "ordering_basis.json"),
            ("candidate_evidence", "candidate_evidence.jsonl"),
            ("candidate_adjudication", "candidate_adjudication.json"),
        )
    }
    present = {name: path for name, path in paths.items() if path.is_file()}
    if not present:
        return {
            "status": "not_applicable",
            "warnings": [],
            "artifacts": {},
            "evidence_before_selection": None,
        }

    warnings: list[str] = []
    evidence_before_selection: bool | None = None
    if (
        "ordering_basis" in present
        and "candidate_evidence" in present
        and "candidate_adjudication" in present
    ):
        evidence_before_selection = (
            present["ordering_basis"].stat().st_mtime_ns
            <= present["candidate_evidence"].stat().st_mtime_ns
            <= present["candidate_adjudication"].stat().st_mtime_ns
        )
        if not evidence_before_selection:
            warnings.append(
                "candidate ordering basis, evidence, and adjudication are out of order"
            )
    return {
        "status": "warning" if warnings else "passed",
        "warnings": warnings,
        "artifacts": {name: str(path) for name, path in present.items()},
        "evidence_before_selection": evidence_before_selection,
    }


def _audit_predictive_graph_review(pipeline_dir: Path) -> dict[str, Any]:
    """Summarize bounded graph-review use and flag incomplete telemetry."""

    names = {
        "predictive_graph_review": "predictive_graph_review.json",
        "predictive_graph_review_dispositions": (
            "predictive_graph_review_dispositions.tsv"
        ),
        "predictive_graph_review_telemetry": (
            "predictive_graph_review_telemetry.json"
        ),
    }
    found: dict[str, Path] = {}
    for key, filename in names.items():
        matches = sorted(pipeline_dir.rglob(filename))
        if matches:
            found[key] = matches[0]
    if "predictive_graph_review" not in found:
        return {
            "status": "not_applicable",
            "warnings": [],
            "artifacts": {},
            "counts": {},
        }

    warnings: list[str] = []
    counts: dict[str, Any] = {}
    try:
        review = json.loads(found["predictive_graph_review"].read_text())
    except (OSError, json.JSONDecodeError) as exc:
        warnings.append(f"invalid predictive graph review: {exc}")
        review = {}
    if review.get("schema_version") != "distributed_agents-predictive-graph-review-v2":
        warnings.append("predictive graph review has the wrong schema")
    candidates = review.get("candidates")
    if isinstance(candidates, list):
        counts["nominated"] = len(candidates)
    if "predictive_graph_review_dispositions" not in found:
        warnings.append("predictive graph review lacks a disposition ledger")
    telemetry_path = found.get("predictive_graph_review_telemetry")
    if telemetry_path is None:
        warnings.append("predictive graph review was not finalized")
    else:
        try:
            telemetry = json.loads(telemetry_path.read_text())
        except (OSError, json.JSONDecodeError) as exc:
            warnings.append(f"invalid predictive graph-review telemetry: {exc}")
            telemetry = {}
        if telemetry.get("schema_version") != (
            "distributed_agents-predictive-graph-review-telemetry-v2"
        ):
            warnings.append("predictive graph-review telemetry has the wrong schema")
        if telemetry.get("status") != "passed":
            warnings.append("predictive graph-review telemetry did not validate")
        telemetry_counts = telemetry.get("counts")
        if isinstance(telemetry_counts, dict):
            counts.update(telemetry_counts)
            if (
                isinstance(candidates, list)
                and telemetry_counts.get("nominated") != len(candidates)
            ):
                warnings.append(
                    "predictive graph-review nomination and telemetry counts differ"
                )
    return {
        "status": "warning" if warnings else "passed",
        "warnings": warnings,
        "artifacts": {key: str(path) for key, path in found.items()},
        "counts": counts,
    }


_GRAPH_ORDERING_PATTERN = re.compile(
    r"\b(?:prioriti[sz]|score|weight|rank(?:ing)?|order(?:ing)?|promot|demot)"
    r"\w*\b",
    flags=re.IGNORECASE,
)
_GRAPH_CONTEXT_PATTERN = re.compile(
    r"\b(?:graph|relational|topology|edge|lane|path|reciprocal|shared[- ]term)"
    r"\w*\b",
    flags=re.IGNORECASE,
)
_GRAPH_NEGATION_PATTERN = re.compile(
    r"\b(?:without|never|not|avoid|forbid(?:den)?|prohibit(?:ed)?|"
    r"must\s+not|do\s+not)\b.{0,100}"
    r"\b(?:prioriti[sz]|score|weight|rank(?:ing)?|order(?:ing)?|promot|demot)"
    r"\w*\b",
    flags=re.IGNORECASE,
)
_GRAPH_SCORE_KEYS = {
    "combined_score",
    "graph_score",
    "relational_score",
    "lane_rank",
}


def _json_keys(value: Any) -> set[str]:
    if isinstance(value, dict):
        return {
            *(str(key).casefold() for key in value),
            *(
                nested
                for child in value.values()
                for nested in _json_keys(child)
            ),
        }
    if isinstance(value, list):
        return {
            nested
            for child in value
            for nested in _json_keys(child)
        }
    return set()


def _asserts_graph_ordering(text: str) -> bool:
    """Return true only for affirmative graph-derived ordering language."""

    if not (
        _GRAPH_ORDERING_PATTERN.search(text)
        and _GRAPH_CONTEXT_PATTERN.search(text)
    ):
        return False
    return not _GRAPH_NEGATION_PATTERN.search(text)


def _audit_semantic_graph_policy(pipeline_dir: Path) -> list[str]:
    """Flag graph-derived candidate scoring without blocking answer recovery."""

    warnings: list[str] = []
    plan_path = pipeline_dir / "adaptive_plan.json"
    if plan_path.is_file():
        try:
            plan = json.loads(plan_path.read_text())
        except (json.JSONDecodeError, OSError):
            plan = {}
        for step in plan.get("steps", []) if isinstance(plan, dict) else []:
            if not isinstance(step, dict):
                continue
            if step.get("capability") not in {
                "corpus.relational_candidates",
                "corpus.predictive_graph_review",
            }:
                continue
            evidence_role = str(step.get("evidence_role") or "")
            if _asserts_graph_ordering(evidence_role):
                warnings.append(
                    "relational graph policy violation: plan uses graph evidence "
                    "to score or order candidates"
                )
                break

    evidence_dir = pipeline_dir / "evidence"
    if evidence_dir.is_dir():
        for path in evidence_dir.rglob("*"):
            if not path.is_file() or "relational" not in path.name.casefold():
                continue
            if _GRAPH_ORDERING_PATTERN.search(path.stem):
                warnings.append(
                    "relational graph policy violation: graph-derived ranking "
                    f"artifact {path.name}"
                )
                continue
            try:
                if path.suffix.casefold() == ".json":
                    keys = _json_keys(json.loads(path.read_text()))
                elif path.suffix.casefold() == ".csv":
                    header = path.open(encoding="utf-8").readline()
                    keys = {
                        value.strip().casefold()
                        for value in header.split(",")
                        if value.strip()
                    }
                else:
                    continue
            except (json.JSONDecodeError, OSError):
                continue
            forbidden = sorted(keys & _GRAPH_SCORE_KEYS)
            if forbidden:
                warnings.append(
                    "relational graph policy violation: candidate scoring fields "
                    f"in {path.name}: {', '.join(forbidden)}"
                )

    answer_audit_path = pipeline_dir / "answer_audit.json"
    if answer_audit_path.is_file():
        try:
            answer_audit = json.loads(answer_audit_path.read_text())
        except (json.JSONDecodeError, OSError):
            answer_audit = {}
        claims: list[Any] = []
        if isinstance(answer_audit, dict):
            for field in ("critical_claims", "claims"):
                values = answer_audit.get(field, [])
                if isinstance(values, list):
                    claims.extend(values)
        for claim in claims:
            if not isinstance(claim, dict):
                continue
            evidence = " ".join(
                str(value) for value in claim.get("evidence", [])
            ).casefold()
            if (
                "relational" in evidence
                and _asserts_graph_ordering(
                    f"{claim.get('claim') or ''} {evidence}"
                )
            ):
                warnings.append(
                    "relational graph policy violation: answer audit cites graph "
                    "evidence as candidate ordering support"
                )
                break
    return list(dict.fromkeys(warnings))
