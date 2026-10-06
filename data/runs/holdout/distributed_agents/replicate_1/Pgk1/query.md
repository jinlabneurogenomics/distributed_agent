Created the requested outputs in the working run directory:

- [trace.md](./trace.md)
- [answer.txt](./answer.txt)

The final prediction is:

```tsv
target_name	predicted_n_degs
Pgk1	1
```

I validated the answer mechanically against the requested-target manifest:

- required files exist
- `answer.txt` contains only one fenced `tsv` block
- header is exactly `target_name	predicted_n_degs`
- exactly one data row is present
- `Pgk1` appears exactly as requested and in requested order
- no duplicate targets
- `predicted_n_degs` is a non-negative integer

The reasoning trace records the focal training counts for the relevant glycolysis analogs (`Eno1`, `Gpi1`, `Hk1`, `Pfkm`, `Slc2a1`, `Tpi1`), exact focal Parquet evidence showing the `Gpi1`/`Hk1`/`Pfkm`/`Tpi1` count of 1 is a self-transcript-only result, the `Gfpt1` stress-response counterexample, bounded same-experiment corpus evidence from `perturbai-july-260713-sourceguard-1773-v1`, and external PubMed literature supporting PGK1’s glycolytic and disease context.