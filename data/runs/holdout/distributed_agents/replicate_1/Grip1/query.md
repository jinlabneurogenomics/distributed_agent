Created both requested outputs in the run directory:

- [answer.txt](./answer.txt)
- [trace.md](./trace.md)

The final prediction is:

```tsv
target_name	predicted_n_degs
Grip1	0
```

I verified that `answer.txt` is exactly one fenced `tsv` block, has the required header, preserves the requested target order, includes `Grip1` exactly once and no extra targets, and contains a non-negative integer prediction.