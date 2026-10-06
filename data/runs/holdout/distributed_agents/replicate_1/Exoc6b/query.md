Created the required outputs in the run directory:

- [trace.md](./trace.md): target-specific reasoning for `Exoc6b`, including the focal-cell training analogs, raw Parquet checks, same-experiment Rala corpus evidence, and external exocyst/Ral citations.
- [answer.txt](./answer.txt): the required single fenced TSV block.

The final point prediction is:

```tsv
target_name	predicted_n_degs
Exoc6b	0
```

I also mechanically validated that `answer.txt` is exactly one `tsv` fenced block, has the required header, contains one row, preserves the requested-target order from `the single-target request`, has no duplicate or extra targets, and uses a non-negative integer prediction.