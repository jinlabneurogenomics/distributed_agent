Created the required outputs:

- [trace.md](./trace.md)
- [answer.txt](./answer.txt)

The final point prediction is:

```tsv
target_name	predicted_n_degs
Fth1	0
```

I validated that `answer.txt` contains only the required fenced `tsv` block, preserves the requested-target CSV order, has exactly one row for `Fth1`, has no duplicate or extra targets, and uses a non-negative integer prediction. I also checked that `Fth1` is absent from both the focal training count CSV and the Parquet `gene_target` column, matching the held-out setup.