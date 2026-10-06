Created both requested files in the working run directory:

- [trace.md](./trace.md)
- [answer.txt](./answer.txt)

The final submitted TSV is:

```tsv
target_name	predicted_n_degs
Taf1	14
```

I validated that `answer.txt` contains exactly one fenced `tsv` block, has the required header, preserves the requested-target CSV order, includes the single requested target exactly once, and uses a non-negative integer prediction.