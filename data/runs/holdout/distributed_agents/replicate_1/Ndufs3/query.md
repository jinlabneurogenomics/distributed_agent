Created both required outputs in the run directory:

- [trace.md](./trace.md)
- [answer.txt](./answer.txt)

I predicted `Ndufs3` at `1` DEG, using the focal training endpoint and direct focal-cell parquet rows for represented complex-I analogs. The closest held-in `Ndu*` perturbations were all at the floor in `151 TH Prkcd Grin2c Glut`: `Ndufs2` and `Ndufs8` had one significant self-transcript each, several other complex-I subunits had zero, and there was no recurring downstream mitochondrial-stress signature.

I also validated `answer.txt` mechanically:

- file exists
- contains a single fenced `tsv` block
- has the exact header `target_name	predicted_n_degs`
- contains exactly one row
- preserves requested order from `the single-target request`
- has no duplicate or extra targets
- has a non-negative integer prediction