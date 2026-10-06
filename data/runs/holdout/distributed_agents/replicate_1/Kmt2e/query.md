Created the requested outputs in the run directory:

- [trace.md](./trace.md)
- [answer.txt](./answer.txt)

The final point prediction is:

```tsv
target_name	predicted_n_degs
Kmt2e	6
```

I validated that `answer.txt` contains exactly one fenced `tsv` block, has the required `target_name` and `predicted_n_degs` columns, includes the single requested target exactly once in requested order, has no extras or duplicates, and uses a non-negative integer prediction.