Created both required outputs in the run directory:

- [trace.md](./trace.md)
- [answer.txt](./answer.txt)

The final prediction is:

```tsv
target_name	predicted_n_degs
Dlx5	0
```

I validated the required output mechanics:

- `answer.txt` contains only one fenced `tsv` block.
- Header is exactly `target_name	predicted_n_degs`.
- Row count is `1`, matching the requested-target CSV.
- `Dlx5` appears exactly once and in requested order.
- `predicted_n_degs` is a non-negative integer.
- `trace.md` is present.