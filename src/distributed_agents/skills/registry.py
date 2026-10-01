"""Resolve the skill catalogs visible to a runtime role."""

from __future__ import annotations

import re
from pathlib import Path

from ..corpus.registry import CorpusRelease, get_release


PACKAGE_SKILLS_DIR = Path(__file__).resolve().parent
LIFE_SCIENCES_SKILLS_DIR = PACKAGE_SKILLS_DIR / "life-sciences"
RUNTIME_SKILLS_DIR = PACKAGE_SKILLS_DIR / "runtime"
DATASET_SKILLS_DIR = PACKAGE_SKILLS_DIR / "dataset"


def resolve_skills(
    skills_destination: str,
    skills_index_container_path: str,
    *,
    include_project: bool,
    corpus_release: CorpusRelease | None = None,
) -> tuple[str, str, list[Path]]:
    """Resolve a catalog hint, index path, and role-visible skill roots."""

    if skills_destination:
        root = Path(skills_destination)
        index = skills_index_container_path or str(root / "SKILLS_INDEX.md")
        return skills_destination, index, [root]
    if include_project:
        release = corpus_release or get_release()
        return (
            str(PACKAGE_SKILLS_DIR),
            str(PACKAGE_SKILLS_DIR / "SKILLS_INDEX.md"),
            [
                LIFE_SCIENCES_SKILLS_DIR,
                RUNTIME_SKILLS_DIR,
                DATASET_SKILLS_DIR,
                release.skills_root,
            ],
        )
    return (
        str(LIFE_SCIENCES_SKILLS_DIR),
        str(LIFE_SCIENCES_SKILLS_DIR / "SKILLS_INDEX.md"),
        [LIFE_SCIENCES_SKILLS_DIR],
    )


def _parse_skill_frontmatter(skill_md: Path) -> dict[str, str]:
    text = skill_md.read_text(encoding="utf-8")
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.DOTALL)
    if not match:
        return {}
    fields: dict[str, str] = {}
    current_key: str | None = None
    for line in match.group(1).splitlines():
        key_match = re.match(r"^([A-Za-z_][\w-]*)\s*:\s*(.*)$", line)
        if key_match:
            current_key = key_match.group(1)
            fields[current_key] = key_match.group(2).strip()
        elif current_key and line.startswith((" ", "\t")):
            fields[current_key] = f"{fields[current_key]} {line.strip()}".strip()
    return fields


def _load_local_skills(skills_dir: Path) -> list[dict[str, str]]:
    if not skills_dir.is_dir():
        return []
    skills: list[dict[str, str]] = []
    for subdirectory in sorted(skills_dir.iterdir()):
        skill_md = subdirectory / "SKILL.md"
        if not subdirectory.is_dir() or not skill_md.is_file():
            continue
        metadata = _parse_skill_frontmatter(skill_md)
        skills.append(
            {
                "name": metadata.get("name", subdirectory.name),
                "description": metadata.get("description", ""),
                "path": str(subdirectory),
            }
        )
    return skills


def load_local_skills_dirs(
    directories: list[Path],
    *,
    query_role: bool = False,
) -> list[dict[str, str]]:
    """Load immediate skill directories, deduplicating them by declared name."""

    seen: set[str] = set()
    merged: list[dict[str, str]] = []
    for directory in directories:
        for skill in _load_local_skills(directory):
            if query_role and Path(skill["path"]).name == "research-router-skill":
                continue
            if skill["name"] in seen:
                continue
            seen.add(skill["name"])
            merged.append(skill)
    return merged


def write_active_skills_index(
    path: Path,
    directories: list[Path] | None = None,
    *,
    query_role: bool = False,
    skills: list[dict[str, str]] | None = None,
) -> Path:
    """Write a run-local catalog containing exactly the loaded skills."""

    active = skills
    if active is None:
        active = load_local_skills_dirs(directories or [], query_role=query_role)
    lines = [
        "# Active Skills Catalog",
        "",
        "This generated catalog contains only the skills loaded for this run.",
        "Read a skill's `SKILL.md` before invoking its helper scripts.",
        "",
    ]
    for skill in sorted(active, key=lambda row: row["name"]):
        lines.extend(
            [
                f"## {skill['name']}",
                f"- **Path:** `{Path(skill['path']).resolve()}/`",
                f"- **Description:** {skill['description']}",
                "",
            ]
        )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")
    return path
