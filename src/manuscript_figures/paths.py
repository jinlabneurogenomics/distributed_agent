"""Locate manuscript data relative to a source checkout or editable install."""
from pathlib import Path
import os


def project_root() -> Path:
    override = os.environ.get("DISTRIBUTED_AGENTS_PROJECT_ROOT")
    candidates = [Path(override).expanduser()] if override else list(Path(__file__).resolve().parents)
    for path in candidates:
        if (path / "pyproject.toml").is_file() and (path / "notebook").is_dir():
            return path.resolve()
    raise FileNotFoundError(
        "Install the repository in editable mode, or set DISTRIBUTED_AGENTS_PROJECT_ROOT "
        "to the checkout containing data/ and notebook/."
    )


ROOT = project_root()
DATA = ROOT / "data"
INPUTS = DATA / "inputs"
RUNS = DATA / "runs"
TABLES = DATA / "tables"
STYLE = Path(__file__).with_name("style.mplstyle")
