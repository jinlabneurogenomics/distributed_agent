Created both requested outputs in the run directory:

- [trace.md](./trace.md)
- [answer.txt](./answer.txt)

The final point prediction is:

```tsv
target_name	predicted_n_degs
Epha6	0
```

I validated that `answer.txt` is exactly one fenced `tsv` block, has the required header, preserves the requested manifest order, contains exactly one row, has no duplicate or extra targets, and uses a non-negative integer prediction.