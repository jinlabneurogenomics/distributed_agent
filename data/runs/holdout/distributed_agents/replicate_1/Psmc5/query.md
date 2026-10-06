Created the requested files in the run directory:

- [trace.md](./trace.md)
- [answer.txt](./answer.txt)

The final prediction is:

```tsv
target_name	predicted_n_degs
Psmc5	520
```

I mechanically checked that `answer.txt` contains only one fenced `tsv` block, has the exact `target_name	predicted_n_degs` header, includes the single requested target `Psmc5` exactly once in requested-manifest order, and uses a non-negative integer prediction.