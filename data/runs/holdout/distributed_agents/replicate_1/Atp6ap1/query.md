Created both required outputs in the run directory:

- [trace.md](./trace.md)
- [answer.txt](./answer.txt)

The final point prediction is:

```tsv
target_name	predicted_n_degs
Atp6ap1	1
```

I based the prediction on the focal training DEG counts plus exact focal-cell Parquet rows for the V-ATPase/accessory and endolysosomal comparators present in training. The closest direct analogs were low in `151 TH Prkcd Grin2c Glut`:

```text
Atp6ap2   2
Atp6v0a1  1
Atp6v1a   0
Atp6v1b2  0
Atp6v1e1  0
Mtor      2
Rptor     0
```

I treated `Rab7` and `Tsc2` as measured counterexamples rather than same-sign analogs: both can touch lysosome/mTOR biology, but they act at different causal stages and produced large, compensatory signatures that the direct V-ATPase perturbations did not phenocopy.

I also wrote compact review tables under `workbench/` from the declared Parquet scan:

- `workbench/related_all_cell_deg_counts.tsv`
- `workbench/related_focal_fdr25.tsv`
- `workbench/related_focal_top20.tsv`
- `workbench/vatpase_target_gene_lfcs.tsv`

Mechanical validation passed: `answer.txt` is exactly one `tsv` fenced block, has the required two columns, contains exactly one row, preserves the requested manifest order, has no duplicate or extra targets, and uses a non-negative integer prediction.