"""Smoke-test a built DistributedAgents wheel without importing the source checkout."""

from __future__ import annotations

import os
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"


def _run(command: list[str], *, cwd: Path, env: dict[str, str]) -> None:
    subprocess.run(command, cwd=cwd, env=env, check=True)


def main() -> int:
    wheels = sorted(DIST.glob("distributed_agents-*.whl"))
    if len(wheels) != 1:
        raise SystemExit(
            f"expected exactly one DistributedAgents wheel in {DIST}, found {len(wheels)}"
        )

    with tempfile.TemporaryDirectory(prefix="distributed_agents-wheel-smoke-") as tmp:
        tmp_path = Path(tmp)
        venv = tmp_path / "venv"
        _run(
            [sys.executable, "-m", "venv", "--system-site-packages", str(venv)],
            cwd=tmp_path,
            env=os.environ.copy(),
        )
        python = venv / "bin" / "python"
        env = os.environ.copy()
        env.pop("PYTHONPATH", None)
        _run(
            [
                str(python),
                "-m",
                "pip",
                "install",
                "--no-deps",
                "--force-reinstall",
                str(wheels[0]),
            ],
            cwd=tmp_path,
            env=env,
        )
        smoke = "\n".join(
            [
                "from importlib.resources import files",
                "from pathlib import Path",
                "import distributed_agents, dotenv, jsonschema",
                "package_path = Path(distributed_agents.__file__).resolve()",
                "assert package_path.is_relative_to(Path.cwd() / 'venv')",
                "assert distributed_agents.__version__ == '0.0.0'",
                "assert sorted(",
                "    item.name",
                "    for item in files('distributed_agents').joinpath('build/prompts').iterdir()",
                ") == ['base_scientist_contract.md', 'findings_report.md']",
                "query_prompts = [",
                "    'adaptive_query_contract.md',",
                "    'adaptive_query_scientific_policy.md',",
                "    'direct_query_contract.md',",
                "]",
                "assert sorted(",
                "    item.name",
                "    for item in files('distributed_agents').joinpath('query/prompts').iterdir()",
                ") == query_prompts",
                "assert files('distributed_agents').joinpath(",
                "    'skills/runtime/exhaustive-corpus-sweep-skill/SKILL.md'",
                ").is_file()",
                "print(f'distributed_agents {distributed_agents.__version__} from {package_path}')",
            ]
        )
        _run([str(python), "-c", smoke], cwd=tmp_path, env=env)
        _run([str(python), "-m", "distributed_agents", "--version"], cwd=tmp_path, env=env)
        _run([str(python), "-m", "distributed_agents", "--help"], cwd=tmp_path, env=env)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
