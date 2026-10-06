Created both required outputs in the run directory:

- [trace.md](./trace.md)
- [answer.txt](./answer.txt)

The prediction is:

```tsv
target_name	predicted_n_degs
Kmt2d	0
```

I validated that `answer.txt` contains exactly one `tsv` fenced block, has the required `target_name	predicted_n_degs` header, preserves the requested-target order, includes exactly one row for `Kmt2d`, has no duplicate or extra targets, and uses a non-negative integer prediction.