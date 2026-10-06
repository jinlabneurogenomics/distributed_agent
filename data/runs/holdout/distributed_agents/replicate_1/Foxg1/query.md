Created both required outputs in the working run directory:

- [trace.md](./trace.md)
- [answer.txt](./answer.txt)

The final prediction is:

```tsv
target_name	predicted_n_degs
Foxg1	0
```

I validated that `answer.txt` contains exactly one fenced `tsv` block, preserves the requested-target order, includes `Foxg1` exactly once and no extra targets, and uses a non-negative integer prediction.