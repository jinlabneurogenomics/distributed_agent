---
name: exhaustive-corpus-sweep-skill
description: Exhaustively review an enumerable corpus when the task explicitly requires full-corpus semantic inspection or complete per-unit accounting. Use bounded reader subagents with deterministic partitions and fail-closed reconciliation; do not use for ordinary searches, samples, top-k retrieval, or deterministic scans that one process can complete directly.
---

# Exhaustive corpus sweep

Use this skill only in `adaptive` mode when the requested answer requires
semantic judgment over every unit in an enumerable corpus. A request for a
count, aggregate, exact filter, inventory, or other deterministic full scan is
not a reason to delegate: run the appropriate corpus tool directly. Do not use
this skill for open-ended web or literature search, where the universe is not
closed and exhaustiveness cannot be established.

Read [references/coordinator.md](references/coordinator.md) before beginning.
The coordinator owns partitioning, budgets, retries, reconciliation, global
deduplication, and the final answer. Reader agents only classify their assigned
slice using [references/reader.md](references/reader.md). Apply
[references/reduction.md](references/reduction.md) after all slices validate.

The runtime publishes these controls:

- `DISTRIBUTED_AGENTS_PIPELINE_DIR`: backend-owned pipeline directory;
- `DISTRIBUTED_AGENTS_MAX_CONCURRENT_SUBAGENTS`: maximum readers running at once;
- `DISTRIBUTED_AGENTS_MAX_SUBAGENTS`: maximum reader starts, including retries.

If either budget is absent, zero, or cannot cover the planned slices, do not
start a delegated sweep. Reduce the slice count without making any slice
ambiguous, perform the work locally, or state that exhaustive completion could
not be established. Never describe a partial or sampled result as exhaustive.

All sweep artifacts belong under
`$DISTRIBUTED_AGENTS_PIPELINE_DIR/corpus_sweep/`. Use the packaged scripts rather than
inventing an accounting format. Their schemas are in `schemas/`.

