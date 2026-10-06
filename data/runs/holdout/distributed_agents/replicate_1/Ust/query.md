Created both required outputs in the working run directory:

- [trace.md](./trace.md)
- [answer.txt](./answer.txt)

The final point prediction is:

```tsv
target_name	predicted_n_degs
Ust	0
```

I validated that `answer.txt` contains only one fenced TSV block, has the exact required columns, includes the single requested target `Ust` exactly once in manifest order, and reports a non-negative integer prediction.