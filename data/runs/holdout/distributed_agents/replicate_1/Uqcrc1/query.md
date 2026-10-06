Created both requested outputs in the working run directory:

- [trace.md](./trace.md)
- [answer.txt](./answer.txt)

The final prediction is:

```tsv
target_name	predicted_n_degs
Uqcrc1	1
```

I validated the required output shape mechanically:

- `answer.txt` contains exactly one fenced `tsv` block and no outside prose.
- Columns are exactly `target_name` and `predicted_n_degs`.
- Row count is `1`, matching the requested-target manifest.
- `Uqcrc1` appears exactly once, in requested order, with no extra targets.
- `predicted_n_degs` parses as a non-negative integer.
- The held-out target has no overlap with the focal training count CSV.