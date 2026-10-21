# Distributed Agents

DistributedAgents is a framework for scaling biological interpretation across large perturbation screens. Applied to a whole-brain in vivo CRISPR Perturb-seq atlas, the pipeline assigns independent AI agents to individual perturbations, integrates cell-type-resolved expression data with literature databases, and creates narrative and structured reports for each perturbation. The framework synthesizes across reports to recover known biology, predict held-out responses, identify relationships between perturbations, and prioritize hypotheses for follow-up. This repository provides the agent runtime, corpus tooling, and notebooks used for the manuscript’s analyses, figures, and supplementary tables.

## Use the hosted service

Browse the corpus on the [Distributed Agents hosted site](https://sites-publish-check-20261021.as-alexander-sun.chatgpt.site).
This temporary address is in use while the custom domain is unavailable.
No repository installation or local corpus download is required.

You can also connect an MCP-compatible AI assistant to the hosted corpus.
The public endpoints provide read-only access to Findings, Claims, supporting
evidence, and release-specific analysis tools.

The hosted experience differs from running locally: the MCP server does not
include the raw dataset files, so it cannot perform operations that require
accessing or recomputing statistics directly from the dataset. For the full
experience, clone or download this repository, fetch the data files with Git LFS
as described below, and [run locally](#run-locally).

### Connect with Codex

With Codex installed, add the corpus connections you want to use:

```bash
# Shi corpus
codex mcp add distributed-agents-shi \
  --url https://sites-publish-check-20261021.as-alexander-sun.chatgpt.site/api/shi-mcp

# Shi holdout corpus
codex mcp add distributed-agents-shi-holdout \
  --url https://sites-publish-check-20261021.as-alexander-sun.chatgpt.site/api/shi-holdout-mcp
```

Check your configuration:

```bash
codex mcp list
```

Start a new Codex chat and try:

> Using the Shi corpus, explain the relationships between proteasome
> subunits and cite the supporting Findings.

These endpoints require no separate Distributed Agents account or API key.
Your normal account and usage requirements still apply.

## Run locally

Use the local installation below to run the Distributed Agents query
framework, work with local data, or reproduce the manuscript analyses.
The local runtime uses the bundled corpus releases and a local MCP server.

Install the minimal environment from the repository root:

```bash
pixi install -e minimal
```

DistributedAgents uses the Codex CLI by default for ease of integration. Authenticate once before the first run:

```bash
codex login
```

## Environment

Copy the example environment file and edit it for your setup:

```bash
cp .env_example .env
```

The bundled `shi` corpus is selected by default; `shi_holdout` is also included. Leave `DISTRIBUTED_AGENTS_CORPUS_RELEASE_ROOTS` unset unless you keep the releases elsewhere. Set `OPENAI_API_KEY` only if you use API-key authentication.

Load the variables into your shell:

```bash
set -a
source .env
set +a
```

## Run a query

```bash
pixi run -e minimal distributed_agents query \
  "What is the relationship between the proteasome subunits?" \
  --out-dir runs/starter
```

To make local data available to the agent, add `--codex-input-root /path/to/data`. Results and run artifacts are written to the selected output directory.

Add `--corpus-release shi_holdout` to query the holdout corpus instead.

## Start a chat

```bash
pixi run -e minimal distributed_agents chat \
  --out-dir runs/chat
```

Run the same command again to resume that chat. Use a different output directory to start a separate session.

For API-key authentication with the Codex CLI, add `--codex-auth apikey` to either command.

## Manuscript analyses

Large datasets and workbooks are stored with Git LFS. After installing Git LFS
and cloning this repository, download them before preparing the analyses:

```bash
git lfs install
git lfs pull
```

The manuscript uses a single data preparation step followed by the figure notebooks:

```text
data/runs/ + data/inputs/ → data/tables/ → notebook/
```

```bash
pixi run prepare-manuscript
pixi run notebook
```

Alternatively, install the analysis dependencies with `pip install -e '.[manuscript]'`
and run `python -m manuscript_figures.prepare`. An editable installation resolves
data paths from the checkout, so the command and notebooks can run from any
working directory. Reproducing the saved analyses requires no model calls or API
credentials. Notebooks display figures inline and do not export images or HTML.

```text
data/
  runs/                 Saved predictions, reports, prompts, and run measurements
  inputs/               Reference data, experimental measurements, reviewed annotations
  tables/               Prepared notebook inputs and supplementary Excel workbooks
notebook/               Main and supplementary figure notebooks
src/manuscript_figures/ Preparation methods and shared plotting style
```

## License

The software and its accompanying documentation are licensed under the
[MIT License](LICENSE).

## Citation

If you use Distributed Agents in your research, please cite:

Sun, A., Park, J. J., DeTomaso, D., Kim, S., Liu, A., Shringarpure, S.,
Kim, K., Thompson, P. C., Shi, T., Wang, Y., Mukamel, E. A., Zheng, G. X.,
Jiao, Y. J. & Jin, X. Distributed AI agents enable comprehensive discovery of
biological insights at scale. *bioRxiv* (2026). Preprint.
[doi:10.64898/2026.10.15.759436](https://doi.org/10.64898/2026.10.15.759436).
