Created both required outputs in the working run directory:

- [trace.md](./trace.md)
- [answer.txt](./answer.txt)

The final prediction is:

```tsv
target_name	predicted_n_degs
Naa15	0
```

I also mechanically validated `answer.txt`:

- it contains one fenced `tsv` block and no prose outside it
- columns are exactly `target_name` and `predicted_n_degs`
- it has exactly one row, matching the requested manifest order
- `Naa15` appears exactly once
- `predicted_n_degs` is a non-negative integer

Key evidence behind the zero call was the focal `Naa10` NatA-subunit analog with `n_degs = 0`, the focal parquet recheck showing no `Naa10` gene passed FDR 0.10 or 0.05 across 17,259 measured genes, the same-experiment corpus report that `Naa10` was an FDR-level null in all 22 measured neuronal groups, and PubMed evidence that `NAA15` acts with `NAA10` in NatA rather than through a transcription-factor-like acute RNA program.