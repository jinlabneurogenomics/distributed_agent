Created both required outputs in the run directory:

- [trace.md](./trace.md)
- [answer.txt](./answer.txt)

The final point prediction is:

```tsv
target_name	predicted_n_degs
Srgap3	1
```

I validated that `answer.txt` is exactly one fenced `tsv` block, has the required `target_name	predicted_n_degs` header, contains exactly the single requested target in manifest order, has no duplicate or extra targets, and uses a nonnegative integer prediction.