"""Discovery and run-local indexing for packaged DistributedAgents skills."""

from .registry import (
    DATASET_SKILLS_DIR,
    LIFE_SCIENCES_SKILLS_DIR,
    PACKAGE_SKILLS_DIR,
    RUNTIME_SKILLS_DIR,
    load_local_skills_dirs,
    resolve_skills,
    write_active_skills_index,
)

__all__ = [
    "DATASET_SKILLS_DIR",
    "LIFE_SCIENCES_SKILLS_DIR",
    "PACKAGE_SKILLS_DIR",
    "RUNTIME_SKILLS_DIR",
    "load_local_skills_dirs",
    "resolve_skills",
    "write_active_skills_index",
]
