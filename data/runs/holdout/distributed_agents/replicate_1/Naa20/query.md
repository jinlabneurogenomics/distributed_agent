Created both requested outputs in the run directory:

- [trace.md](./trace.md)
- [answer.txt](./answer.txt)

The final prediction is:

```tsv
target_name	predicted_n_degs
Naa20	0
```

I validated `answer.txt` mechanically against the held-out manifest:

- exactly one fenced `tsv` block
- header is exactly `target_name	predicted_n_degs`
- exactly one row
- target membership and order match the requested CSV
- no duplicate targets
- prediction parses as a nonnegative integer

I also materialized the declared Perturb-seq target-level feature cache in `workbench/features.parquet` and filtered focal-class comparator rows into `workbench/focal_selected.parquet` for the `Naa20` trace.