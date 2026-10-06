Created both required deliverables in the run directory:

- [trace.md](./trace.md)
- [answer.txt](./answer.txt)

The final prediction is:

```tsv
target_name	predicted_n_degs
Cacng8	0
```

I mechanically validated that:

- `answer.txt` exists and contains only one `tsv` fenced block.
- Its header is exactly `target_name	predicted_n_degs`.
- It has exactly one data row, matching the single requested target `Cacng8`.
- Requested-target order is preserved.
- There are no duplicate or extra targets.
- `predicted_n_degs` is a non-negative integer.

The trace documents the direct endpoint calibration from the focal training DEG-count CSV, direct Parquet checks for the closest AMPA/TARP and glutamate-receptor training perturbations, use of the internal `PerturbAI July 260713 sourceguard-1773 v1` same-experiment corpus for `Cacng2`, `Cacng3`, and `Dlg4` analog evidence, and PubMed-backed external biology placing `Cacng8` as classical TARP gamma-8.