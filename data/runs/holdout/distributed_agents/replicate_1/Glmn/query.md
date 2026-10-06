Created both required outputs in the working run directory:

- [trace.md](./trace.md)
- [answer.txt](./answer.txt)

The final prediction is:

```tsv
target_name	predicted_n_degs
Glmn	0
```

I validated that `answer.txt` contains only one fenced `tsv` block, has the exact required header, contains exactly the single requested target `Glmn` in manifest order, has no duplicate targets, and uses a non-negative integer prediction.