# Direct DEG-count forecast for Slc24a5

## Prediction

- `target_name`: `Slc24a5`
- Predicted `n_degs` in `151 TH Prkcd Grin2c Glut`: **0**

## Evidence used

The declared biology-only `Slc24a5` bundle supported a low postnatal thalamic-neuron transcriptional-impact prior even though the edit should be able to deplete newly supplied NCKX5 by the P37-P44 harvest:

- `Slc24a5`/NCKX5 is an intracellular potassium-dependent sodium/calcium exchanger tied to trans-Golgi and pigment-organelle biology.
- The established mouse loss phenotype is ocular and coat pigmentation, not a postnatal neuronal phenotype.
- Adult mouse brain evidence in the card points to low average brain signal with strong choroid-plexus localization, which is outside the NeuN-positive neuronal nuclei assayed here.
- The exact focal-population non-target expression was only 73 UMI across 23,679 nuclei: 64 expressing nuclei, `0.270%` cells expressing, mean raw UMI `0.00308`, mean log1p CP10K `0.00123`, and pseudobulk `0.193` CPM.
- Same-species paralogs listed in the biology card, `Slc24a2`, `Slc24a3`, `Slc24a4`, and `Slc8b1`, were not present in the `151 TH Prkcd Grin2c Glut` training count table, so there was no exact NCKX-family donor outcome to transfer.

The declared focal training count table was sparse:

- 1,674 perturbations were visible.
- Median `n_degs` was `0`.
- `1,205 / 1,674 = 72.0%` had `0` DEGs.
- `1,481 / 1,674 = 88.5%` had `<= 1` DEG.
- `1,546 / 1,674 = 92.4%` had `<= 5` DEGs.

I used the closed annotation store and the declared training universe to look for biologically typed substitutes rather than selecting by symbol prefix. It found no `exact_complex_or_paralog` and no bidirectional corpus comparator among training-available genes. The highest-priority candidates were broad calcium/homeostasis or metal-ion-transporter fallbacks. Their focal counts did not justify lifting `Slc24a5` above the null-heavy baseline: among the closest transporter/calcium handling candidates checked directly in the Parquet, `Tmem165`, `Ryr2`, and `Slc9a9` had 0 DEGs, `Atp2b3` and `Slc9a7` had 1 DEG, and only the less target-like broad fallbacks `Atp2b1` and `Calm1` reached 22 and 14 DEGs.

## Synthesis

The decisive quantitative feature was the in-assay expression reach: a gene detected in only 0.27% of non-target thalamic nuclei offers little substrate for a cell-autonomous CRISPR loss response in an aggregate survivor-conditioned snRNA-seq contrast. The decisive biological feature was that the well-established operation and phenotypes are pigment-cell/Golgi rather than thalamic neuronal. With no exact same-family measured donor and with even curated transporter fallbacks mostly at 0 or 1 DEG, the heavy zero mass of the focal training table was the most appropriate numerical prior.

I therefore predict that `Slc24a5` loss will not produce any BH-adjusted Wilcoxon hits at `p < 0.05` in `151 TH Prkcd Grin2c Glut`.
