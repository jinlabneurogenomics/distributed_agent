"""Run one rendered prompt through Biomni A1 in Biomni's environment.

This helper is meant to be launched from Biomni's own environment, for example:

  mamba run -n biomni_e1 python src/bioeval/frameworks/biomni_runner.py ...

It intentionally does not import ``bioeval`` so the environment only needs
Biomni and its runtime dependencies.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.request
from pathlib import Path


def _filtered_literature_call(name: str, arguments: dict) -> str:
    """Call one read-only tool on BioEval's filtered PubMed broker."""
    base_url = os.environ.get("BIOEVAL_FILTERED_MCP_URL", "").rstrip("/")
    if not base_url:
        return "Filtered literature access is unavailable for this run."
    payload = json.dumps(
        {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/call",
            "params": {"name": name, "arguments": arguments},
        }
    ).encode()
    request = urllib.request.Request(
        f"{base_url}/mcp",
        data=payload,
        headers={"Content-Type": "application/json", "Accept": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=60) as response:
        result = json.loads(response.read())
    content = (result.get("result") or {}).get("content") or []
    return "\n".join(
        str(item.get("text", ""))
        for item in content
        if isinstance(item, dict) and item.get("type") == "text"
    )


def search_pubmed(query: str, max_results: int = 10) -> str:
    """Search independent PubMed literature through the protected eval broker."""
    return _filtered_literature_call(
        "search_pubmed", {"query": query, "max_results": max_results}
    )


def fetch_pubmed(pmid: str) -> str:
    """Fetch one PubMed abstract and citation through the protected eval broker."""
    return _filtered_literature_call("fetch_pubmed", {"pmid": pmid})


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--prompt-path", required=True, type=Path)
    p.add_argument("--run-dir", required=True, type=Path)
    p.add_argument("--model", default="gpt-5.4")
    p.add_argument("--data-path", default="./data")
    p.add_argument("--biomni-repo", type=Path, default=Path("modules/Biomni"))
    args = p.parse_args(argv)

    repo_path = args.biomni_repo.resolve()
    if repo_path.exists() and str(repo_path) not in sys.path:
        sys.path.insert(0, str(repo_path))

    args.run_dir.mkdir(parents=True, exist_ok=True)
    prompt = args.prompt_path.read_text()

    from biomni.agent import A1

    agent = A1(path=args.data_path, llm=args.model, expected_data_lake_files=[])
    if os.environ.get("BIOEVAL_FILTERED_MCP_URL"):
        agent.add_tool(search_pubmed)
        agent.add_tool(fetch_pubmed)
    log_entries, final_output = agent.go(prompt)

    (args.run_dir / "biomni_log.txt").write_text("\n\n".join(map(str, log_entries)))
    (args.run_dir / "biomni_final_output.md").write_text(str(final_output))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
