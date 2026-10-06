Created both requested outputs in the run directory:

- [trace.md](./trace.md)
- [answer.txt](./answer.txt)

The final prediction is:

```tsv
target_name	predicted_n_degs
Med12	14
```

I validated the required output mechanics:

- `answer.txt` contains exactly one fenced `tsv` block and no extra prose.
- Header is exactly `target_name	predicted_n_degs`.
- Row count matches the requested-target CSV: `1`.
- Target order is preserved: `Med12`.
- There are no duplicate or extra targets.
- `predicted_n_degs` is a nonnegative integer.

One declared tool note: `dataset.perturbseq_features summarize` succeeded and wrote `evidence/features.parquet`; its `calibrate` subcommand was not applicable because this task has no supplied ranked or partial-ranked gene set in `task_bindings.json`.