Created both required outputs in the working run directory:

- [trace.md](./trace.md)
- [answer.txt](./answer.txt)

Final prediction:

```tsv
target_name	predicted_n_degs
Prkn	0
```

I validated that `answer.txt` is exactly a single `tsv` fenced block, contains the required header, preserves the requested manifest order, includes the single requested target exactly once, and uses a non-negative integer prediction.