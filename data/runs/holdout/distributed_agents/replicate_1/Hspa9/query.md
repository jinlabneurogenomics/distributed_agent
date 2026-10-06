Created both requested outputs in the run directory:

- [trace.md](./trace.md)
- [answer.txt](./answer.txt)

The final point prediction is:

```tsv
target_name	predicted_n_degs
Hspa9	1
```

I validated that `answer.txt` contains only one fenced `tsv` block, has the exact `target_name	predicted_n_degs` header, preserves the requested target order, includes `Hspa9` exactly once, and uses a non-negative integer prediction.