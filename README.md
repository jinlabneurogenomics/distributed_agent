# Distributed Agents

DistributedAgents is an agent interface for exploring whole-brain Perturb-seq results. This repository contains the code for the framework, and notebooks to reproduce the manuscript figures and supplementary data tables.

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
