Created the required files in the run directory:

- [trace.md](./trace.md)
- [answer.txt](./answer.txt)

The final `answer.txt` contains exactly one fenced `tsv` block, preserving the requested order:

```tsv
target_name	predicted_n_degs
Nup93	620
```

I validated the mechanical requirements after writing:

- `answer.txt` is a single `tsv` fence with no prose outside it.
- Columns are exactly `target_name` and `predicted_n_degs`.
- Row count is `1`, matching `the single-target request`.
- `Nup93` appears exactly once and matches the requested target exactly.
- `predicted_n_degs` is a non-negative integer.
- `trace.md` exists and is non-empty.

One broad exploratory all-cell Parquet scan for three comparator targets was stopped because it was still scanning the full 616M-row file; the final reasoning used the declared focal-cell training counts, narrow focal-cell Parquet reads, same-experiment corpus summaries for the represented analogs, and bounded PubMed-backed external mechanism evidence.