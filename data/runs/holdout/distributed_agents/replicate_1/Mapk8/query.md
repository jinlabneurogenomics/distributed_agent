Created both required outputs in the run directory:

- [trace.md](./trace.md)
- [answer.txt](./answer.txt)

The final prediction is:

```tsv
target_name	predicted_n_degs
Mapk8	0
```

I validated that `answer.txt` is exactly a single `tsv` fenced block, preserves the requested `Mapk8` order, has the required header, contains one unique data row, and uses a non-negative integer prediction.