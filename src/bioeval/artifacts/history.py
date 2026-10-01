"""Discover current BioEval run manifests under an artifact root."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Iterable


@dataclass(frozen=True)
class RunRecord:
    created_at: str
    status: str
    task: str
    framework: str
    run_id: str
    path: str
    kind: str

    def to_dict(self) -> dict[str, str]:
        return asdict(self)


def _read_object(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    return value if isinstance(value, dict) else {}


def _prompt_records(path: Path) -> list[RunRecord]:
    metadata = _read_object(path)
    frameworks = metadata.get("frameworks")
    if not isinstance(frameworks, list):
        return []
    items = [item for item in frameworks if isinstance(item, dict)]
    matching = [
        item
        for item in items
        if Path(str(item.get("run_dir") or "")).resolve() == path.parent.resolve()
    ]
    # Current manifests are copied into each framework directory; historical
    # manifests sometimes lived once above all framework directories.
    selected = matching or items
    records: list[RunRecord] = []
    for current in selected:
        run_dir = Path(str(current.get("run_dir") or path.parent)).resolve()
        result = _read_object(run_dir / "runner_result.json")
        if result:
            returncode = result.get("returncode")
            outputs = result.get("output_status")
            complete_outputs = not isinstance(outputs, dict) or all(outputs.values())
            status = "completed" if returncode == 0 and complete_outputs else "failed"
        else:
            status = "prepared"
        records.append(
            RunRecord(
                created_at=str(metadata.get("created_at") or ""),
                status=status,
                task=str(metadata.get("question_id") or ""),
                framework=str(current.get("framework") or ""),
                run_id=str(metadata.get("run_id") or ""),
                path=str(run_dir),
                kind="framework",
            )
        )
    return records


def discover_runs(root: Path) -> list[RunRecord]:
    """Return recognized runs newest-first, ignoring unrelated JSON files."""

    root = root.expanduser().resolve()
    if not root.exists():
        return []
    records: list[RunRecord] = []
    records.extend(
        record
        for path in root.rglob("run_metadata.json")
        for record in _prompt_records(path)
    )
    return sorted(records, key=lambda record: record.created_at, reverse=True)


def filter_runs(
    records: Iterable[RunRecord],
    *,
    task: str | None = None,
    status: str | None = None,
) -> list[RunRecord]:
    return [
        record
        for record in records
        if (task is None or task.lower() in record.task.lower())
        and (status is None or record.status == status)
    ]


def format_runs(records: Iterable[RunRecord]) -> str:
    rows = list(records)
    if not rows:
        return "No BioEval runs found."
    headers = ("WHEN (UTC)", "STATUS", "TASK", "FRAMEWORK", "RUN ID", "PATH")
    values = [
        (
            row.created_at.replace("+00:00", "Z"),
            row.status,
            row.task,
            row.framework,
            row.run_id,
            row.path,
        )
        for row in rows
    ]
    widths = [
        max(len(headers[index]), *(len(row[index]) for row in values))
        for index in range(len(headers))
    ]

    def render(row: tuple[str, ...]) -> str:
        return "  ".join(value.ljust(widths[index]) for index, value in enumerate(row))

    return "\n".join(
        [
            render(headers),
            render(tuple("-" * width for width in widths)),
            *(render(row) for row in values),
        ]
    )
