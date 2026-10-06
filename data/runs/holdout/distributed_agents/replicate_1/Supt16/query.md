Created both required artifacts in the run directory:

- [trace.md](./trace.md)
- [answer.txt](./answer.txt)

I predicted a weak nonzero focal response for the single requested held-out perturbation:

```tsv
target_name	predicted_n_degs
Supt16	16
```

I mechanically validated that `answer.txt` contains only one fenced `tsv` block, has exactly the required `target_name`/`predicted_n_degs` columns, preserves the requested target order, includes `Supt16` exactly once and no extra targets, and uses a non-negative integer prediction.