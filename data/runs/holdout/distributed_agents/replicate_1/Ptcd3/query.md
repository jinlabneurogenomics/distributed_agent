Created both requested files in the run directory:

- [trace.md](./trace.md)
- [answer.txt](./answer.txt)

I predicted `Ptcd3` as `0` DEGs. The trace documents the focal training-count distribution, the focal Parquet queries over mitochondrial translation/OXPHOS analogs, the same-experiment `perturbai-july-260713-sourceguard-1773-v1` corpus checks, and the PTCD3/DAP3/LRPPRC mitochondrial literature used to decide that the closest visible perturbations support no downstream FDR-resolved nuclear response in recovered `151 TH Prkcd Grin2c Glut` nuclei.

I also mechanically verified `answer.txt`:

- exactly one fenced `tsv` block
- header is exactly `target_name	predicted_n_degs`
- exactly one data row
- `Ptcd3` appears once, in requested order
- prediction is a non-negative integer
- no extra targets or duplicate targets