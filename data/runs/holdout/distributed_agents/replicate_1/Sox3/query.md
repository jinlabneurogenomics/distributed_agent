Created both requested outputs in the run directory:

- [trace.md](./trace.md)
- [answer.txt](./answer.txt)

The final prediction is:

```tsv
target_name	predicted_n_degs
Sox3	1
```

I mechanically validated that `answer.txt` is a single `tsv` fenced block, has the exact required header, contains exactly one row, preserves the requested-target order from `the single-target request`, has no duplicate or extra targets, and uses a non-negative integer prediction.