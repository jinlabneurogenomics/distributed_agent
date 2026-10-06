Created both requested outputs in the run directory:

- [trace.md](./trace.md)
- [answer.txt](./answer.txt)

The final prediction is:

```tsv
target_name	predicted_n_degs
Xpo1	37
```

I used the declared parquet through the cached Perturb-seq feature workbench, joined it to the focal training DEG-count CSV, extracted focal signatures for the nuclear transport and RNA-processing comparator panel, and used the July 260713 PerturbAI same-experiment corpus plus bounded PubMed literature for the target-specific transfer rationale. The nested workbench `calibrate` operation could not run because this run’s `task_bindings.json` has no ranked or partially ranked supervision set; the focal `n_degs` training CSV was therefore used directly as the count supervision.

I also mechanically checked that `answer.txt` is exactly one fenced `tsv` block, has the required `target_name` and `predicted_n_degs` columns, contains exactly one row, preserves the requested `Xpo1` order, has no duplicate or extraneous target, and uses a non-negative integer prediction.