Created both required outputs in the run directory:

- [trace.md](./trace.md)
- [answer.txt](./answer.txt)

I predicted:

```tsv
target_name	predicted_n_degs
Aifm1	1
```

I validated that `answer.txt` contains only a single fenced `tsv` block, has the exact required header, preserves the requested-target order, includes `Aifm1` exactly once, and uses a non-negative integer prediction.