Created both required outputs in the run directory:

- [trace.md](./trace.md)
- [answer.txt](./answer.txt)

The final point prediction is:

```tsv
target_name	predicted_n_degs
Tubb2a	1
```

I verified that `answer.txt` contains only a single fenced `tsv` block, has the exact required columns, preserves the requested target order, includes `Tubb2a` exactly once, and uses a non-negative integer prediction.