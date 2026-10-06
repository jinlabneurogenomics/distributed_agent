Created both required outputs in the working run directory:

- [answer.txt](./answer.txt)
- [trace.md](./trace.md)

The final point prediction is:

```tsv
target_name	predicted_n_degs
Tbk1	0
```

I validated that `answer.txt` is exactly one fenced `tsv` block, has the exact required header, includes the one requested target in manifest order, has no duplicate or extra targets, and uses a non-negative integer prediction.