Created both required outputs in the run directory:

- [trace.md](./trace.md)
- [answer.txt](./answer.txt)

The final prediction is:

```tsv
target_name	predicted_n_degs
Pafah1b1	40
```

I based the nonzero call primarily on the visible `Dctn1` perturbation, which had 75 focal `FDR < 0.05` DEGs and a coherent sterol/lipid plus neuronal downshift signature consistent with dynein/dynactin-endolysosomal transport disruption. I attenuated the estimate for `Pafah1b1` because LIS1 is an upstream dynein regulator and much of its strongest literature phenotype is embryonic migration/progenitor biology, while the assay perturbed juvenile postmitotic recovered neurons; the flat `Reln`/`Dab1`/`Vldlr`/`Lrp8`/`Fyn` branch and weak generic microtubule perturbations argue against assigning a large footprint from migration or microtubule membership alone.

I also mechanically checked the required output shape:

- `answer.txt` is exactly one fenced `tsv` block.
- The TSV has the exact header `target_name	predicted_n_degs`.
- It contains exactly one data row, matching the one requested target in order.
- `Pafah1b1` is unique and the prediction is a non-negative integer.
- `Pafah1b1` is absent from both the visible training-count CSV and the visible DE parquet as `gene_target`, as expected for a held-out perturbation.