# Coordinator protocol

The root agent is the only coordinator and the only writer of global outputs.
It must remain available to reconcile results; it must not take a reader slice
while readers are active.

## 1. Establish a closed universe

Materialize one JSONL or CSV row per review unit. Each row needs a stable,
unique identifier. Record the exact task and, when applicable, the selected
release manifest. If the universe cannot be enumerated, this protocol cannot
claim exhaustiveness.

Choose the smallest useful slice count, no larger than the number of units and
no larger than half of `DISTRIBUTED_AGENTS_MAX_SUBAGENTS`; the second bound reserves one
possible retry for every slice. Slices may run in multiple waves. If a slice is
too large for one reader to adjudicate reliably, do not silently weaken the
retry reserve: report that the configured total-reader budget is insufficient.

Create deterministic, content-hashed partitions:

```bash
python <skill-dir>/scripts/plan_sweep.py \
  --input UNIVERSE.jsonl \
  --id-field RECORD_ID \
  --slice-count N \
  --task "$DISTRIBUTED_AGENTS_OUTPUT_DIR/task.md" \
  --release-manifest RELEASE.json \
  --out-dir "$DISTRIBUTED_AGENTS_PIPELINE_DIR/corpus_sweep"
```

Omit `--release-manifest` only when no release owns the corpus. Inspect
`sweep_plan.json`; do not edit its partitions by hand.

## 2. Dispatch bounded readers

When native collaboration tools are available, call `spawn_agent` once for
each ready slice, then use `wait_agent` to collect that wave before starting
more. Use `send_message` only to clarify an already-running slice; it does not
create another attempt. In the API backend, call the `corpus_sweep_reader` tool
once per slice instead. Start no more than
`DISTRIBUTED_AGENTS_MAX_CONCURRENT_SUBAGENTS` readers concurrently and no more than
`DISTRIBUTED_AGENTS_MAX_SUBAGENTS` readers in total, counting retries.

Each reader task must state all of the following:

1. Read `<skill-dir>/references/reader.md` in full and follow it.
2. Read the unchanged task at the exact task path.
3. Read exactly one slice at `slices/<slice-id>.jsonl` plus only the evidence
   necessary to adjudicate those rows.
4. Write only
   `workers/<slice-id>/slice_results.jsonl` and optional notes inside that same
   slice directory.
5. Return the slice ID, assigned count, disposition count, output path, and any
   uncertainty. Do not make global claims and do not create child agents.

Partitions are disjoint. Never assign one slice to two live readers. When a
reader fails or its output does not validate, diagnose the existing artifacts
and retry that slice once with a fresh reader. Do not retry a slice more than
once. If the retry fails, stop and report the sweep as incomplete.

Validate each result:

```bash
python <skill-dir>/scripts/validate_slice.py \
  --plan "$DISTRIBUTED_AGENTS_PIPELINE_DIR/corpus_sweep/sweep_plan.json" \
  --slice-id slice-0000 \
  --results "$DISTRIBUTED_AGENTS_PIPELINE_DIR/corpus_sweep/workers/slice-0000/slice_results.jsonl" \
  --out "$DISTRIBUTED_AGENTS_PIPELINE_DIR/corpus_sweep/workers/slice-0000/slice_validation.json"
```

## 3. Reconcile before synthesis

After every slice passes, run:

```bash
python <skill-dir>/scripts/reconcile_sweep.py \
  --plan "$DISTRIBUTED_AGENTS_PIPELINE_DIR/corpus_sweep/sweep_plan.json" \
  --out-dir "$DISTRIBUTED_AGENTS_PIPELINE_DIR/corpus_sweep"
```

Continue only if `sweep_audit.json` has `status: "passed"`, planned and covered
unit counts are equal, and missing, extra, and duplicate ID lists are empty.
The host independently checks this audit. A missing or failed audit makes the
query fail closed rather than merely warn.
