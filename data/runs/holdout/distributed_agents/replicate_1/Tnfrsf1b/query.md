Created both required outputs in the run directory:

- [trace.md](./trace.md)
- [answer.txt](./answer.txt)

The final TSV is:

```tsv
target_name	predicted_n_degs
Tnfrsf1b	0
```

I validated that `answer.txt` contains exactly one fenced `tsv` block, preserves the requested manifest order, has one row for `Tnfrsf1b`, has no duplicate or extra targets, uses a non-negative integer prediction, and does not include a training target.