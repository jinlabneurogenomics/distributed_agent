# Rab28 direct DEG-count forecast

## Target and endpoint

- Target: `Rab28`.
- Focal population: `151 TH Prkcd Grin2c Glut`.
- Endpoint: count of measured genes with BH-adjusted Wilcoxon `pvals_adj < 0.05`.
- Exact target DEG rows for `Rab28` were held out. I used the declared `Rab28.json` biology bundle, the `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` training count table, the `training_de_all_cell_groups.parquet` expression summaries for selected training perturbations, and selected same-experiment corpus Findings for ciliary comparators.

The corpus Findings and Claims are preinterpreted views of the same Perturb-seq experiment represented in the Parquet, not independent replication.

## Biology prior from the declared Rab28 bundle

- `Rab28` is expressed in the exact focal population: 20,462 of 23,679 non-target nuclei expressed the feature, `86.414%`, with mean raw UMI `2.309`, mean CP10K `1.463`, and pseudobulk CPM `144.698`.
- The bundle adjudicates Rab28 as a dynamic prenylated trafficking GTPase whose functional stock is likely substantially depleted 21-28 days after a disruptive P16 edit.
- Direct operation evidence is strongest for PDE6D-dependent photoreceptor outer-segment delivery and cone disc shedding; the thalamic-neuron use case is extrapolated from ciliary/IFT biology and remains context-limited.

Interpretation: target absence or a durable protein stock is not the main reason to predict no transcriptional response; Rab28 is present and the edit should become functional. The limiting issue is whether loss of this ciliary trafficking operation creates a basal nuclear RNA state in recovered thalamic neurons.

## Same-experiment ciliary context

The selected corpus release had no packaged Rab28 Finding. I treated that as missing packaged coverage, not as evidence that Rab28 was transcriptionally null.

Packaged Findings for measured ciliary comparators were directly relevant:

- `Ttc8:F003` reported that represented ciliary comparators including `Bbs5`, `Ift43`, `Ift81`, `Ift88`, `Kif3b`, `Dync2h1`, `Lztfl1`, `Rpgrip1l`, `Ttc21b`, and `Cep290` did not converge into a robust shared transcriptional module.
- `Ift88:F003` anchored the same pattern for IFT-B, dynein-2, Cep290, BBSome, Ptch/Gli/Smo-adjacent perturbations: the common phenotype in postnatal NeuN+ nuclear RNA was buffering or singleton-only signal, not a shared IFT/ciliary knockout transcriptome.
- `Cep290:F003` likewise reported that expected ciliary GPCR, BBSome/IFT, and Hedgehog-effector transcription was absent or nearly absent after `Cep290` and related component perturbations.

Those reports do not prove intact cilia or normal Rab28 protein trafficking; they say the assayed endpoint is usually blind to represented ciliary subcellular defects unless a secondary nuclear program appears.

## Training count evidence in 151 TH Prkcd Grin2c Glut

The whole training endpoint distribution was already floor-heavy:

- 1,674 training perturbations.
- Median `n_degs = 0`; mean `14.05` because of a small heavy tail.
- 1,205 / 1,674 targets had `0` DEGs.
- 1,481 / 1,674 had `0` or `1` DEG.

I then restricted to a hand-selected set matching Rab28's ciliary / small-GTPase-trafficking biology:

| target | n_degs |
|---|---:|
| Arl3 | 1 |
| B9d1 | 0 |
| Bbs5 | 0 |
| Cep120 | 0 |
| Cep290 | 0 |
| Dync2h1 | 0 |
| Dync2i1 | 0 |
| Ift43 | 0 |
| Ift81 | 0 |
| Ift88 | 0 |
| Kif3b | 0 |
| Rab18 | 0 |
| Rab27a | 0 |
| Rab3gap1 | 0 |
| Rab3gap2 | 0 |
| Rpgrip1l | 0 |
| Ttc21b | 0 |
| Ttc8 | 1 |

This slice has 16/18 zeros and no count above one in the focal thalamic population. Broader ciliary targets named in the same-experiment corpus (`Adcy3`, `Alms1`, `Arl2bp`, `Cfap69`, `Dzip1`, `Iqcb1`, `Lztfl1`, `Mchr1`, `Rpgr`, `Smo`) were also at `0` in the same focal count table.

## Parquet spot-check

For the 18-gene ciliary/Rab slice above, the focal Parquet contained 17,259 measured-gene rows per training target. Sixteen targets had zero rows with `pvals_adj < 0.05`. The only singleton signals were self-transcript rows:

| target | top FDR row in focal Parquet | adjusted p |
|---|---|---:|
| Arl3 | `Arl3` down | 0.0184 |
| Ttc8 | `Ttc8` down | 0.0000307 |

Representative zeros had no near-threshold secondary program: `Cep290` min adjusted p `0.650`, `Ift88` min adjusted p `1.0`, `Rab18` min adjusted p `0.912`, `Rab3gap1` min adjusted p `1.0`, `B9d1` min adjusted p `1.0`, and `Ttc21b` min adjusted p `0.459`.

Generic Rab family membership alone was not transferred from `Rab7`: `Rab7` had 501 focal DEGs, but the corpus attributes that to a late-endosomal/lysosomal compensation and sterol-stress state. `Rab28`'s bundle points instead to a ciliary prenylated trafficking GTPase, and closer ciliary or Rab-regulatory training perturbations were flat.

## Synthesis

`Rab28` was not down-weighted for lack of expression: it is widely detected in the focal non-target nuclei. I also did not assume the edit failed. The decisive evidence was endpoint alignment: in this postnatal survivor-conditioned thalamic snRNA assay, represented ciliary trafficking genes repeatedly failed to induce a basal nuclear RNA module, and the matched training genes most analogous to Rab28 were almost all exactly zero in the requested count table.

The main residual uncertainty is whether the held-out `Rab28` contrast will count its self-transcript. The ciliary/Rab training set showed that self-only singletons occur (`Arl3`, `Ttc8`), but zero was still the modal and median outcome even among the nearest represented biology. I therefore predict the floor value.

Predicted `n_degs`: `0`
