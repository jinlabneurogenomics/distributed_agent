Created the required outputs in the run directory:

- [trace.md](./trace.md)
- [answer.txt](./answer.txt)

The final point prediction is:

```tsv
target_name	predicted_n_degs
Ppp2r1a	0
```

I validated that `answer.txt` is exactly one fenced `tsv` block, has the required header, includes the single requested target `Ppp2r1a` in manifest order, has no duplicate or extra targets, and contains a non-negative integer prediction.