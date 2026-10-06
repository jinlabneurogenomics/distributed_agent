# Naa15 direct DEG-count forecast

## Target and endpoint

- **Target:** `Naa15`, the single row in `[local file: Naa15.csv]`.
- **Endpoint:** number of `151 TH Prkcd Grin2c Glut` measured genes with BH-adjusted Wilcoxon `pvals_adj < 0.05`.
- **Declared outcome masking:** `Naa15` had 0 rows in `[local file: training_de_all_cell_groups.parquet]`; the point below uses the biology bundle, the training count table, and non-target training profiles.

## Evidence Used

### Naa15 perturbation biology

Source: `[local file: Naa15.json]`; served canonical `biology` view.

- Exact focal reach is high enough for an RNA phenotype to be measurable if one is produced: `Naa15` was detected in 18,674 of 23,679 non-target `151 TH Prkcd Grin2c Glut` nuclei, or 78.86%, with mean log1p CP10k 0.659 and mean raw UMI 1.79.
- The functional lesion is expected to be partial and delayed by harvest. NAA15 is the auxiliary NatA scaffold for cotranslational N-terminal acetylation with NAA10, but a P16 edit does not directly remove pre-existing NatA complexes or the already-acetylated carrier proteins made before editing.
- Carrier turnover in neurons is heterogeneous, direct NAA15/NatA residence in matching postmitotic thalamic neurons is not known, and NAA16 is a plausible alternative auxiliary NatA subunit with unknown same-context compensation. The bundle therefore adjudicates `functional_stock_by_harvest = partially_depleted_or_leading_edge`, not a fast complete depletion.

### 151-class training counts

Source: `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.

- The focal training endpoint is sparse: 1,205 of 1,674 targets had 0 significant genes at BH `pvals_adj < 0.05`; the median was 0, the 75th percentile was 1, the 90th percentile was 2, and only 106 targets reached at least 10 DEGs.
- The only NatA-complex training target present in the declared count table was `Naa10`, the catalytic partner of NAA15; it had `n_degs = 0`.
- Active protein-homeostasis and translation comparators were detectable in the same focal endpoint, for example `Psmb4 = 742`, `Psmc1 = 430`, and `Eef2 = 9`, so the NatA null should not be read as a universal inability to detect proteostasis-related RNA states.

### Naa10 measured profile

Source: `[local file: training_de_all_cell_groups.parquet]`; same-experiment Naa10 Findings from release `perturbai-july-260713-sourceguard-1773-v1`.

- In the exact `151 TH Prkcd Grin2c Glut` parquet slice, `Naa10` had 17,259 measured genes, 240 matched perturbed nuclei, 23,679 matched controls, and 0 genes with `pvals_adj < 0.05`.
- Across all 22 measured neuronal groups in the training parquet, `Naa10` had 2,123 total matched perturbed nuclei and 0 significant genes at BH `pvals_adj < 0.05`.
- The packaged Naa10 report summarized the broader signature as a pan-neuronal FDR-level transcriptomic null and found no compensatory NAT-family, integrated-stress, apoptosis, proteasome/ubiquitin rebound, or other robust downstream RNA program.
- The same report contrasted Naa10 with proteasome/translation targets whose matched groups generated many FDR-level genes, supporting interpretation of the Naa10 zero as a buffered or absent secondary transcriptomic state rather than a generic assay failure.

## Synthesis

The strongest quantitative analogue was the catalytic NatA subunit `Naa10`. Its complete FDR-level null across 22 groups says that acute P16 disruption of the core NatA operation is not sufficient to create a recovered-neuron RNA program in this assay window. `Naa15` is broadly expressed in the focal class, which keeps a nonzero response plausible, but it is not a faster or cleaner lesion than `Naa10`: loss of the auxiliary scaffold should have mixed stock depletion by P37-P44 because existing acetylated carriers persist and possible NAA16-containing NatA complexes could buffer new-substrate processing.

I therefore placed `Naa15` with the buffered NatA observation and at the zero-inflated mode of the 151-class training distribution, rather than with proteasome or UFMylation perturbations that induced hundreds to thousands of focal DEGs. The predicted integer DEG count is:

```tsv
target_name	predicted_n_degs
Naa15	0
```
