Created the requested outputs in the working run directory:

- [trace.md](./trace.md) with the quantitative calibration, focal-cell parquet checks, `Tsc2`/`Depdc5` mTOR analog reasoning, PI3K/mTOR counterexamples, external citations, and limits.
- [answer.txt](./answer.txt) with the single required fenced TSV row:

```tsv
target_name	predicted_n_degs
Pten	96
```

I mechanically validated that `answer.txt` is a lone `tsv` fenced block, has the exact header, contains exactly one row, preserves the requested manifest order, has no duplicate or extra targets, and uses a non-negative integer prediction.