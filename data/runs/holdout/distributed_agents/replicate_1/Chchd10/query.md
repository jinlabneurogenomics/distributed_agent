Created both required outputs in the run directory:

- [trace.md](./trace.md)
- [answer.txt](./answer.txt)

The final prediction is:

```tsv
target_name	predicted_n_degs
Chchd10	1
```

I validated that `answer.txt` is exactly one fenced `tsv` block, has the required two-column header, preserves the requested-target order, contains exactly one row for `Chchd10`, has no duplicate or extra targets, and uses a non-negative integer prediction.