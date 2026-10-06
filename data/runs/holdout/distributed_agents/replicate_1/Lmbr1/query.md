Created both requested outputs in the run directory:

- [trace.md](./trace.md)
- [answer.txt](./answer.txt)

The final prediction is:

```tsv
target_name	predicted_n_degs
Lmbr1	0
```

I validated that `answer.txt` is a single `tsv` fenced block, contains the exact required header, has exactly one row, preserves the requested target name/order, has no duplicate or extra targets, and uses a non-negative integer prediction.