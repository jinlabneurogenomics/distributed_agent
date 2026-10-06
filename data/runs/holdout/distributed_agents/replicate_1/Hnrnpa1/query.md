Created both required outputs in the run directory:

- [trace.md](./trace.md)
- [answer.txt](./answer.txt)

The final prediction is:

```tsv
target_name	predicted_n_degs
Hnrnpa1	14
```

I verified `answer.txt` mechanically:

- exactly one fenced `tsv` block
- header is exactly `target_name	predicted_n_degs`
- one data row, matching the one requested target
- requested target order preserved
- no duplicate targets
- `predicted_n_degs` is a non-negative integer

I also confirmed from the declared Parquet that `Hnrnpa1` has no training `gene_target` rows.