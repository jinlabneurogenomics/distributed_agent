# Distributed Agents

DistributedAgents is a framework for scaling biological interpretation across large perturbation screens. Applied to a whole-brain in vivo CRISPR Perturb-seq atlas, the pipeline assigns independent AI agents to individual perturbations, integrates cell-type-resolved expression data with literature databases, and creates narrative and structured reports for each perturbation. The framework synthesizes across reports to recover known biology, predict held-out responses, identify relationships between perturbations, and prioritize hypotheses for follow-up. This repository provides the agent runtime, corpus tooling, and notebooks used for the manuscript’s analyses, figures, and supplementary tables.

## Setup

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

Manuscript data uses `distributed_agents` in run paths and field names, and
`Distributed Agents` in plot labels and prose. All data needed to regenerate the
manuscript tables and figures is bundled under `data/`.
