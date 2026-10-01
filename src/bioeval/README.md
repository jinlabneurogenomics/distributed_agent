# BioEval

BioEval runs the same task through DistributedAgents, direct Codex, Claude Code, or
Biomni and writes each framework's outputs to a separate run directory. 

BioEval launches frameworks, isolates their inputs, records usage, and checks
that declared output files were created. 

## Quick start

Run commands from the repository root:

```bash
pixi install
pixi run bioeval --help
```

The bundled task TOMLs refer to data beneath `DISTRIBUTED_AGENTS_SHARED_ROOT`. Set it to
the directory containing the required `data/` and `debug/` inputs:

```bash
export DISTRIBUTED_AGENTS_SHARED_ROOT=/path/to/shared-distributed_agents-root
```

Preview a task without calling a model:

```bash
pixi run bioeval run \
  --task src/bioeval/benchmarks/depletion-odd-seed/task.toml \
  --frameworks distributed_agents codex claude-code biomni \
  --dry-run
```

`--dry-run` renders the prompts and prints each framework command and expected
outputs. Remove it to execute the run.

## Running frameworks

DistributedAgents is the default framework:

```bash
pixi run bioeval run \
  --task src/bioeval/benchmarks/depletion-odd-seed/task.toml
```

Select one framework explicitly:

```bash
# DistributedAgents query agent
pixi run bioeval run --task TASK.toml --frameworks distributed_agents

# Codex CLI baseline
pixi run bioeval run --task TASK.toml --frameworks codex

# Claude Code baseline
pixi run bioeval run --task TASK.toml --frameworks claude-code

# Biomni A1 baseline
pixi run bioeval run --task TASK.toml --frameworks biomni
```

Or compare all four on the same task:

```bash
pixi run bioeval run \
  --task TASK.toml \
  --frameworks distributed_agents codex claude-code biomni
```

Common framework overrides are:

```bash
--distributed_agents-model MODEL --distributed_agents-backend codex --corpus-release RELEASE
--codex-model MODEL --codex-auth chatgpt
--claude-model MODEL --claude-web off
--biomni-model MODEL --biomni-repo PATH --biomni-env ENV
```

Use `pixi run bioeval run --help` for the complete option list. Use `--rerun N`
for repeated runs and `--run-id NAME` for a stable batch name.

### Framework prerequisites

- **DistributedAgents:** the repository's normal Pixi environment and an installed
  corpus release. Its default `codex` backend uses the Codex CLI login.
- **Codex:** a `codex` executable and `codex login`. Alternatively, export
  `OPENAI_API_KEY` and pass `--codex-auth apikey`.
- **Claude Code:** a `claude` executable and `ANTHROPIC_API_KEY`.
- **Biomni:** a Biomni checkout at `modules/Biomni` (or `--biomni-repo`), a
  mamba environment named `biomni_e1` (or `--biomni-env`), and the appropriate
  OpenAI or Anthropic API key.

API keys may be exported or stored in the repository's untracked `.env` file.
The default Biomni cost tracker also requires:

```bash
pixi install -e litellm-proxy
```

Pass `--no-track-cost` to omit optional proxy-based accounting for an
unprotected run.

## Bundled benchmarks

| Benchmark | Task TOML |
|---|---|
| Four-direction literature flags | `benchmarks/literature-flags/task.toml` |
| Finding caveats, 30 findings | `benchmarks/finding-caveats/task-30.toml` |
| Finding caveats, 50 findings | `benchmarks/finding-caveats/task-50.toml` |
| Finding caveats, 50 findings without literature | `benchmarks/finding-caveats/task-50-no-literature.toml` |
| Finding caveats, 100 findings | `benchmarks/finding-caveats/task-100.toml` |
| Depletion odd-seed task | `benchmarks/depletion-odd-seed/task.toml` |
| Held-out DEG-count task | `benchmarks/holdout-prediction/deg-count.toml` |
| Held-out DEG-identity task | `benchmarks/holdout-prediction/deg-identity.toml` |

Paths in the table are relative to `src/bioeval/`.

## Protected literature tasks

Tasks containing `[source_policy]` hide the source paper and related identifiers.
They use Bubblewrap and mitmproxy; tasks that permit literature access also use
an Apptainer image containing the filtered PubMed service.

Install the TLS proxy environment once. Build the image as well when running a
task with filtered literature access:

```bash
pixi install -e tls-proxy
cd src/bioeval/containers
apptainer build bioeval-filtered-search.sif bioeval-filtered-search.def
cd ../../..
```

Protected Biomni runs also require the `litellm-proxy` environment described
above. The normal protected-run defaults already enable the required fairness
sandboxes, Codex backend, and disabled hosted web tools.

## Running an arbitrary prompt

Use `--prompt-file` instead of a task TOML for an ad hoc comparison:

```bash
pixi run bioeval run \
  --prompt-file path/to/question.md \
  --name my-question \
  --frameworks codex claude-code
```

A task TOML is preferred for repeatable runs because it declares the input
allowlist and required deliverables explicitly.

## Results

By default, runs are written beneath:

```text
src/bioeval/runs/<task>/<framework>/<batch>/r01/
```

Set `BIOEVAL_RUN_ROOT` or pass `--results-root PATH` to write elsewhere. Each
framework directory contains the rendered `prompt.md`, `run_metadata.json`,
`runner.log`, `runner_result.json`, framework-native output, and the task's
declared deliverables.

List recent runs with:

```bash
pixi run bioeval runs
pixi run bioeval runs --task depletion
pixi run bioeval runs --status completed --json
```
