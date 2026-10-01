"""Integrity and cross-artifact checks for one corpus release."""

from __future__ import annotations

import csv
import hashlib
import json
import re
import sqlite3
from pathlib import Path
from typing import Any, Iterable

import jsonschema

from .models import CorpusRegistryError, CorpusRelease, DoctorReport
from .registry import _read_json


LFS_POINTER_PREFIX = b"version https://git-lfs.github.com/spec/v1"


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _is_lfs_pointer(path: Path) -> bool:
    with path.open("rb") as handle:
        return handle.read(len(LFS_POINTER_PREFIX)) == LFS_POINTER_PREFIX


def _split_ids(value: str | None) -> Iterable[str]:
    if isinstance(value, list):
        return (str(item) for item in value if str(item))
    return (item for item in str(value or "").split("|") if item)


def _skill_frontmatter_name(path: Path) -> str | None:
    match = re.match(
        r"^---\s*\n.*?^name:\s*([^\s]+)\s*$.*?^---\s*$",
        path.read_text(encoding="utf-8"),
        re.MULTILINE | re.DOTALL,
    )
    return match.group(1) if match else None


def doctor_release(release: CorpusRelease) -> DoctorReport:
    """Verify artifact integrity and manifest-declared cross-artifact joins."""

    report = DoctorReport(release.release_id)
    integrity = release.manifest.get("integrity", {})
    retained_names = {
        "findings",
        "evidence",
        "references",
        "mgi_target_mapping",
        "publication_reference_mapping",
    }
    for spec in integrity.get("target_membership", []):
        retained_names.update(spec["artifacts"])
        retained_names.add(spec["reports_artifact"])
    for spec in integrity.get("joins", []):
        retained_names.update(spec["from_artifacts"])
        retained_names.update(spec["to_artifacts"])
    artifact_rows: dict[str, list[dict[str, Any]]] = {}
    report_targets: set[str] = set()

    skills_spec = release.manifest["capabilities"]["skills"]
    declared_skills = set(skills_spec["names"])
    installed_skills = (
        {
            path.name
            for path in release.skills_root.iterdir()
            if path.is_dir() and (path / "SKILL.md").is_file()
        }
        if release.skills_root.is_dir()
        else set()
    )
    if installed_skills != declared_skills:
        report.errors.append(
            "skills: installed/declaration mismatch "
            f"installed={sorted(installed_skills)} declared={sorted(declared_skills)}"
        )
    else:
        report.checks.append("skills: declared inventory")
    for skill_name in sorted(declared_skills):
        skill_md = release.skills_root / skill_name / "SKILL.md"
        if not skill_md.is_file():
            report.errors.append(f"skills: missing {skill_name}/SKILL.md")
        elif _skill_frontmatter_name(skill_md) != skill_name:
            report.errors.append(
                f"skills: {skill_name}/SKILL.md frontmatter name does not match"
            )
        else:
            report.checks.append(f"skills: {skill_name} frontmatter")
    for role, role_spec in sorted(skills_spec["roles"].items()):
        for entrypoint_name in sorted(role_spec["entrypoints"]):
            entrypoint = release.skill_entrypoint(role, entrypoint_name)
            if not entrypoint.is_file():
                report.errors.append(
                    f"skills: missing {role}.{entrypoint_name} entrypoint {entrypoint}"
                )
            else:
                report.checks.append(f"skills: {role}.{entrypoint_name}")

    for name, spec in release.manifest["artifacts"].items():
        record_validator: jsonschema.protocols.Validator | None = None
        try:
            path = release.resolve(str(spec["path"]))
        except CorpusRegistryError as exc:
            report.errors.append(str(exc))
            continue
        if not path.is_file():
            report.errors.append(f"{name}: missing artifact {path}")
            continue
        schema_path = spec.get("schema")
        if schema_path:
            resolved_schema = release.resolve(str(schema_path))
            if not resolved_schema.is_file():
                report.errors.append(f"{name}: missing schema {resolved_schema}")
            else:
                report.checks.append(f"{name}: schema")
                try:
                    record_schema = _read_json(resolved_schema)
                    jsonschema.Draft202012Validator.check_schema(record_schema)
                    record_validator = jsonschema.Draft202012Validator(record_schema)
                except (CorpusRegistryError, jsonschema.SchemaError) as exc:
                    report.errors.append(f"{name}: invalid record schema: {exc}")
        if _is_lfs_pointer(path):
            report.errors.append(
                f"{name}: unresolved Git LFS pointer at {path}; run git lfs pull"
            )
            continue
        actual_bytes = path.stat().st_size
        if actual_bytes != spec["bytes"]:
            report.errors.append(
                f"{name}: byte size {actual_bytes} != manifest {spec['bytes']}"
            )
        else:
            report.checks.append(f"{name}: byte size")
        actual_sha = _sha256(path)
        if actual_sha != spec["sha256"]:
            report.errors.append(
                f"{name}: sha256 {actual_sha} != manifest {spec['sha256']}"
            )
        else:
            report.checks.append(f"{name}: sha256")

        if spec["format"] == "jsonl":
            count = 0
            required = set(spec.get("required_fields", []))
            rows: list[dict[str, Any]] = []
            id_column = spec.get("id_column")
            scope_column = spec.get("scope_column", "target_gene")
            seen: set[tuple[str, str]] = set()
            with path.open(encoding="utf-8") as handle:
                for line_number, line in enumerate(handle, 1):
                    if not line.strip():
                        continue
                    count += 1
                    try:
                        row = json.loads(line)
                    except json.JSONDecodeError as exc:
                        report.errors.append(f"{name}:{line_number}: invalid JSON: {exc}")
                        continue
                    missing = sorted(required - set(row))
                    if missing:
                        report.errors.append(
                            f"{name}:{line_number}: missing fields {', '.join(missing)}"
                        )
                    if record_validator is not None:
                        validation_error = next(
                            record_validator.iter_errors(row), None
                        )
                        if validation_error is not None:
                            report.errors.append(
                                f"{name}:{line_number}: schema violation: "
                                f"{validation_error.message}"
                            )
                    if name in retained_names:
                        rows.append(row)
                    if id_column:
                        key = (
                            str(row.get(scope_column) or ""),
                            str(row.get(id_column) or ""),
                        )
                        if key in seen:
                            report.errors.append(
                                f"{name}: duplicate scoped ID {key[0]}:{key[1]}"
                            )
                        seen.add(key)
                    if spec.get("kind") == "per_target_reports":
                        target_field = str(spec.get("target_field") or "gene_target")
                        target = str(row.get(target_field) or "")
                        if target:
                            if target in report_targets:
                                report.errors.append(
                                    f"{name}: duplicate {target_field} {target}"
                                )
                            report_targets.add(target)
            if name in retained_names:
                artifact_rows[name] = rows
        elif spec["format"] == "csv":
            keep_rows = name in retained_names
            rows: list[dict[str, Any]] = []
            count = 0
            id_column = spec.get("id_column")
            scope_column = spec.get("scope_column", "target_gene")
            seen: set[tuple[str, str]] = set()
            with path.open(newline="", encoding="utf-8") as handle:
                reader = csv.DictReader(handle)
                header = set(reader.fieldnames or [])
                missing = sorted(set(spec.get("required_columns", [])) - header)
                if missing:
                    report.errors.append(
                        f"{name}: missing CSV columns {', '.join(missing)}"
                    )
                for row in reader:
                    count += 1
                    if keep_rows:
                        rows.append(row)
                    if id_column:
                        key = (
                            str(row.get(scope_column) or ""),
                            str(row.get(id_column) or ""),
                        )
                        if key in seen:
                            report.errors.append(
                                f"{name}: duplicate scoped ID {key[0]}:{key[1]}"
                            )
                        seen.add(key)
            if keep_rows:
                artifact_rows[name] = rows
        elif spec["format"] == "json":
            count = 1
            try:
                row = _read_json(path)
            except CorpusRegistryError as exc:
                report.errors.append(f"{name}: {exc}")
                continue
            missing = sorted(set(spec.get("required_fields", [])) - set(row))
            if missing:
                report.errors.append(
                    f"{name}: missing fields {', '.join(missing)}"
                )
            if record_validator is not None:
                validation_error = next(record_validator.iter_errors(row), None)
                if validation_error is not None:
                    report.errors.append(
                        f"{name}: schema violation: {validation_error.message}"
                    )
            if name in retained_names:
                artifact_rows[name] = [row]
        elif spec["format"] == "sqlite":
            table = str(spec["record_table"])
            count = -1
            try:
                connection = sqlite3.connect(
                    f"{path.as_uri()}?mode=ro",
                    uri=True,
                )
                try:
                    quick_check = str(
                        connection.execute("PRAGMA quick_check").fetchone()[0]
                    )
                    if quick_check != "ok":
                        report.errors.append(
                            f"{name}: SQLite quick_check returned {quick_check!r}"
                        )
                    else:
                        report.checks.append(f"{name}: SQLite quick_check")
                    columns = {
                        str(row[1])
                        for row in connection.execute(
                            f'PRAGMA table_info("{table}")'
                        )
                    }
                    missing = sorted(
                        set(spec.get("required_columns", [])) - columns
                    )
                    if missing:
                        report.errors.append(
                            f"{name}: missing SQLite columns {', '.join(missing)}"
                        )
                    else:
                        report.checks.append(f"{name}: SQLite columns")
                    count = int(
                        connection.execute(
                            f'SELECT count(*) FROM "{table}"'
                        ).fetchone()[0]
                    )
                finally:
                    connection.close()
            except sqlite3.Error as exc:
                report.errors.append(f"{name}: invalid SQLite artifact: {exc}")
        elif spec["format"] == "text":
            count = 1
            try:
                content = path.read_text(encoding="utf-8")
            except (OSError, UnicodeError) as exc:
                report.errors.append(f"{name}: invalid UTF-8 text artifact: {exc}")
                continue
            if not content.strip():
                report.errors.append(f"{name}: text artifact is empty")
            else:
                report.checks.append(f"{name}: UTF-8 text")
        else:
            report.errors.append(f"{name}: unsupported format {spec['format']!r}")
            continue

        if count != spec["records"]:
            report.errors.append(
                f"{name}: record count {count} != manifest {spec['records']}"
            )
        else:
            report.checks.append(f"{name}: {count} records")

    findings = artifact_rows.get("findings")
    evidence = artifact_rows.get("evidence")
    references = artifact_rows.get("references")
    if findings is not None and evidence is not None and references is not None:
        evidence_keys = {
            (row.get("target_gene", ""), row.get("evidence_id", "")) for row in evidence
        }
        reference_keys = {
            (row.get("target_gene", ""), row.get("ref_id", "")) for row in references
        }
        missing_evidence: list[str] = []
        missing_references: list[str] = []
        unknown_targets: set[str] = set()
        for row in findings:
            target = row.get("target_gene", "")
            finding_id = row.get("finding_id", "")
            if report_targets and target not in report_targets:
                unknown_targets.add(target)
            for evidence_id in _split_ids(row.get("evidence_ids")):
                if (target, evidence_id) not in evidence_keys:
                    missing_evidence.append(f"{target}:{finding_id}->{evidence_id}")
            for ref_id in _split_ids(row.get("ref_ids")):
                if (target, ref_id) not in reference_keys:
                    missing_references.append(f"{target}:{finding_id}->{ref_id}")
        for label, values in (
            ("findings with unknown report targets", sorted(unknown_targets)),
            ("missing evidence references", missing_evidence),
            ("missing publication references", missing_references),
        ):
            if values:
                report.errors.append(f"{label}: {', '.join(values[:20])}")
            else:
                report.checks.append(label)

    mgi_documents = artifact_rows.get("mgi_target_mapping", [])
    if mgi_documents:
        mgi_document = mgi_documents[0]
        mapped_targets = [
            str(row.get("input_target") or "")
            for row in mgi_document.get("mappings", [])
        ]
        if len(mapped_targets) != len(set(mapped_targets)):
            report.errors.append("mgi target mapping: duplicate input targets")
        elif set(mapped_targets) != report_targets:
            missing = sorted(report_targets - set(mapped_targets))
            extra = sorted(set(mapped_targets) - report_targets)
            report.errors.append(
                "mgi target mapping: release target mismatch "
                f"missing={missing[:20]} extra={extra[:20]}"
            )
        else:
            report.checks.append("mgi target mapping: exact release targets")
        actual_mgi_sha = str(mgi_document.get("source", {}).get("sha256", ""))
        if not re.fullmatch(r"[0-9a-f]{64}", actual_mgi_sha):
            report.errors.append("mgi target mapping: invalid source SHA-256")
        else:
            report.checks.append("mgi target mapping: source metadata")

    publication_documents = artifact_rows.get("publication_reference_mapping", [])
    if publication_documents and references is not None:
        publication_document = publication_documents[0]
        source_reference_ids = {
            str(row.get("doc_id") or "")
            or f"{row.get('target_gene', '')}:{row.get('ref_id', '')}"
            for row in references
        }
        mapped_reference_ids = [
            str(row.get("source_reference_id") or "")
            for row in publication_document.get("mappings", [])
        ]
        if len(mapped_reference_ids) != len(set(mapped_reference_ids)):
            report.errors.append(
                "publication reference mapping: duplicate source reference IDs"
            )
        elif set(mapped_reference_ids) != source_reference_ids:
            missing = sorted(source_reference_ids - set(mapped_reference_ids))
            extra = sorted(set(mapped_reference_ids) - source_reference_ids)
            report.errors.append(
                "publication reference mapping: release reference mismatch "
                f"missing={missing[:20]} extra={extra[:20]}"
            )
        else:
            report.checks.append(
                "publication reference mapping: exact release references"
            )
        publication_source = publication_document.get("source", {})
        expected_reference_sha = str(
            release.manifest["artifacts"]["references"].get("sha256", "")
        )
        if (
            publication_document.get("release_id") != release.release_id
            or publication_source.get("artifact") != "references"
            or publication_source.get("sha256") != expected_reference_sha
        ):
            report.errors.append(
                "publication reference mapping: source release/hash mismatch"
            )
        else:
            report.checks.append("publication reference mapping: source metadata")

    for spec in integrity.get("target_membership", []):
        reports_name = spec["reports_artifact"]
        report_field = spec["report_field"]
        known_targets = {
            str(row.get(report_field) or "")
            for row in artifact_rows.get(reports_name, [])
        }
        unknown: list[str] = []
        for artifact_name in spec["artifacts"]:
            for row in artifact_rows.get(artifact_name, []):
                target = str(row.get(spec["field"]) or "")
                if target not in known_targets:
                    unknown.append(f"{artifact_name}:{target}")
        label = "manifest target membership"
        if unknown:
            report.errors.append(f"{label}: {', '.join(unknown[:20])}")
        else:
            report.checks.append(label)

    for join in integrity.get("joins", []):
        destination: set[tuple[str, str]] = set()
        for artifact_name in join["to_artifacts"]:
            for row in artifact_rows.get(artifact_name, []):
                destination.add(
                    (
                        str(row.get(join["scope_field"]) or ""),
                        str(row.get(join["to_field"]) or ""),
                    )
                )
        missing: list[str] = []
        for artifact_name in join["from_artifacts"]:
            for row in artifact_rows.get(artifact_name, []):
                scope = str(row.get(join["scope_field"]) or "")
                for linked_id in _split_ids(row.get(join["field"])):
                    if (scope, linked_id) not in destination:
                        missing.append(f"{artifact_name}:{scope}->{linked_id}")
        label = (
            f"manifest join {','.join(join['from_artifacts'])}.{join['field']}"
        )
        if missing:
            report.errors.append(f"{label}: {', '.join(missing[:20])}")
        else:
            report.checks.append(label)

    tooling = release.tooling_root
    if not tooling.is_dir():
        report.errors.append(f"tooling: missing {tooling}")
    else:
        report.checks.append("tooling")
    for name in release.manifest["capabilities"]["tooling"]["entrypoints"]:
        entrypoint = release.tooling_entrypoint(str(name))
        if not entrypoint.is_file():
            report.errors.append(f"tooling: missing entrypoint {entrypoint}")
        else:
            report.checks.append(f"tooling: {name}")
    for name in release.manifest["capabilities"].get("projections", {}):
        projection = release.projection(name)
        if not projection.is_dir():
            report.errors.append(f"projection {name}: missing {projection}")
        else:
            report.checks.append(f"projection {name}")
    return report
