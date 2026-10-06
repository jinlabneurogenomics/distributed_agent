Created both required outputs in the run directory:

- [trace.md](./trace.md)
- [answer.txt](./answer.txt)

The final prediction is:

```tsv
target_name	predicted_n_degs
Acat1	0
```

I validated that `answer.txt` contains exactly one fenced `tsv` block, has the required `target_name` / `predicted_n_degs` header, includes the single requested target `Acat1` exactly once in manifest order, and uses a non-negative integer prediction.