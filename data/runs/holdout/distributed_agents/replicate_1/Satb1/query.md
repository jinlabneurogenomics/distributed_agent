Created the required outputs in the run directory:

- [trace.md](./trace.md)
- [answer.txt](./answer.txt)

The final point prediction is:

```tsv
target_name	predicted_n_degs
Satb1	0
```

I validated that `answer.txt` has exactly one fenced `tsv` block, preserves the requested-target order, includes `Satb1` exactly once and no extra targets, and uses a non-negative integer prediction. The broader all-cell downstream-`Satb1` scan was stopped after the focal-cell scan had already resolved the only rows needed for this prediction.