Created both required outputs in the run directory:

- [trace.md](./trace.md)
- [answer.txt](./answer.txt)

I predicted `Nr4a2` as a focal null:

```tsv
target_name	predicted_n_degs
Nr4a2	0
```

The trace documents the central within-dataset evidence: `Nr4a1` and `Nr4a3` both have `n_degs = 0` in `151 TH Prkcd Grin2c Glut`, their exact focal Parquet rows have no FDR-level NR4A-family response, RXR/NCOA and immediate-early neighbors are also focal-null or very small, and positive focal nuclear-receptor controls like `Rora` and `Esrra` reflect different maintained thalamic/metabolic programs rather than NR4A basal activity.

I also ran the required mechanical checks:

- `trace.md` and `answer.txt` exist.
- `answer.txt` contains only one fenced `tsv` block.
- Columns are exactly `target_name` and `predicted_n_degs`.
- Row count matches the requested-target CSV: `1`.
- Target identity and order match the manifest exactly.
- No duplicate target rows.
- `predicted_n_degs` is an integer and nonnegative.