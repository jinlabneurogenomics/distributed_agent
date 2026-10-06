Created the required outputs:

- [trace.md](./trace.md)
- [answer.txt](./answer.txt)

The prediction is:

```tsv
target_name	predicted_n_degs
Adora2a	0
```

I validated that `answer.txt` contains exactly one fenced `tsv` block, has the required `target_name` and `predicted_n_degs` columns, preserves the requested manifest order, contains exactly one row for `Adora2a`, has no duplicate or extra targets, and uses a non-negative integer prediction.