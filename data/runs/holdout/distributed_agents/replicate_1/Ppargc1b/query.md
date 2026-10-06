Created both required outputs in the working run directory:

- [trace.md](./trace.md)
- [answer.txt](./answer.txt)

The prediction is:

```tsv
target_name	predicted_n_degs
Ppargc1b	0
```

I validated that `answer.txt` is exactly one fenced `tsv` block, contains the required header, has exactly one row, preserves the requested-target order, includes `Ppargc1b` exactly once, and uses a non-negative integer prediction.