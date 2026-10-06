# Trace

## Question and endpoint

I predicted `n_degs` for the one requested held-out perturbation, `Sim1`, in `151 TH Prkcd Grin2c Glut` cells. I treated `n_degs` as the exact focal-cell endpoint used in the supplied training CSV: the count of measured genes whose Wilcoxon Benjamini-Hochberg adjusted p-value is below 0.05 in perturbed nuclei versus matched controls.

The held-out `Sim1` differential-expression rows and focal DEG count are absent from both declared inputs, so the prediction is a transfer from visible perturbations and mechanism rather than a direct readout. I resolved `TH` in the cell label as thalamus, following the run-local PerturbAI atlas dataset portrait; it is not tyrosine hydroxylase.

## Sources used

- Declared endpoint table: `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
- Declared differential-expression parquet: `training differential-expression dataset`.
- Requested-target manifest: `single-target request for Sim1`.
- Run-local PerturbAI atlas portrait, task bindings, coverage, and capability/measurement registries in `codex_runtime/pipeline`.
- Same-experiment semantic layer: `perturbai-july-260713-sourceguard-1773-v1`. I queried its bounded BioKG and compact Findings inventory only to look for `Sim1`-linked visible perturbations and to interpret visible `Arnt`, `Bmal1`, `Gpr45`, and `Lepr` signatures. These are curated views of the same screen, not independent replication.
- External literature found through NCBI PubMed:
  - Michaud et al. 1998, DOI `10.1101/gad.12.20.3264`, PMID `9784500`.
  - Michaud et al. 2000, DOI `10.1016/s0925-4773(99)00328-7`, PMID `10640708`.
  - Goshu et al. 2004, DOI `10.1210/me.2003-0372`, PMID `14988428`.
  - Tolson et al. 2010, DOI `10.1523/JNEUROSCI.5444-09.2010`, PMID `20220015`.
  - Alvarez-Bolado 2018, DOI `10.1007/s00441-018-2859-1`, PMID `29869716`.

## Dataset calculations

I first used the training count CSV to calibrate the focal endpoint distribution. It contains 1,674 visible perturbations, of which 1,205 have `n_degs = 0`; the median is 0, the 75th percentile is 1, the 90th percentile is 2, and only the upper tail becomes broad, with the 95th percentile at 18 and the maximum at 2,677. A prediction above zero therefore requires an analog whose postnatal thalamic transcriptional effect is visible, not merely a developmental neural annotation.

I then compared `Sim1` with visible genes in three mechanistic groups:

- Direct SIM1 developmental partners or paralogs: `Arnt2`, `Otp`, `Pou3f2`, `Sim2`, and `Fezf2`.
- Broader hypothalamic transcription factors reviewed with the SIM1/OTP/POU3F2 module: `Nkx2-1`, `Neurog3`, `Isl1`, `Nr5a1`, and `Nr5a2`.
- Genes connected to mature SIM1-positive PVH circuits or the same receptor logic: `Lepr`, `Htr2c`, and `Gpr45`, plus the generic PAS partners `Arnt` and `Bmal1`.

The best molecular analogs were not in the visible focal training table: `Arnt2`, `Otp`, `Pou3f2`, `Sim2`, and `Fezf2` were absent from the supplied non-held-out counts. The visible focal counts were:

| training target | focal `n_degs` | interpretation |
|---|---:|---|
| `Arnt` | 0 | Generic ARNT is not the established in-vivo partner of SIM1 in PVN/SON development; its same-experiment Finding also reported a pan-neuronal FDR 0.10 null. |
| `Bmal1` | 103 | Clear positive PAS-family counterexample, but the DE genes were circadian/clock outputs such as `Dbp`, `Nr1d1`, `Nr1d2`, `Npas2`, `Per`, and `Cry`, not a PVN/SIM1 neuroendocrine state. |
| `Clock` | 3 | A weak visible partner of BMAL1, showing that even an obligate transcription-factor partner can be much weaker than the partner with the stronger assay state. |
| `Nkx2-1` | 0 | Hypothalamic developmental TF for a different progenitor axis than the SIM1/OTP/POU3F2 anterior parvocellular/magnocellular axis. |
| `Neurog3` | 0 | Same as above; a tuberal/arcuate developmental regulator, not a direct SIM1 partner. |
| `Isl1` | 0 | Downstream tuberal/arcuate regulator; no focal thalamic effect. |
| `Nr5a1` | 0 | VMH/tuberal regulator; no focal thalamic effect. |
| `Nr5a2` | 0 | Tuberal/anterior hypothalamic regulator; no focal thalamic effect. |
| `Lepr` | 0 | Leptin-receptor biology is hypothalamic and stimulus-dependent; the same-experiment report saw only a singleton FDR 0.10 signal in `110 CNU-HYa HY MM Glut`, not in the focal thalamic class. |
| `Htr2c` | 0 | A receptor in subsets of PVH/CRH neurons rather than a SIM1 transcriptional partner; no focal thalamic response. |
| `Gpr45` | 0 | Recently connected to SIM1-positive PVH energy-balance neurons, but the selected Perturb-seq corpus called it an all-null perturbation across broad neuronal classes. |

For these visible genes I also queried the focal DE parquet for `Sim1`, `Arnt2`, `Otp`, `Pou3f2`, `Oxt`, `Avp`, `Crh`, `Trh`, `Sst`, `Mc4r`, `Lepr`, `Htr2c`, and `Gpr45`. None of the zero-count analogs changed those SIM1/PVH marker genes at FDR 0.10 in `151 TH Prkcd Grin2c Glut`; every selected marker row had `pvals_adj = 1.0`. I ignored very large marker log-fold changes when `pvals_adj = 1.0`, because in this sparse snRNA-seq table those reflect low-count pseudocount behavior rather than reproducible regulation.

## Target-specific reasoning

### Sim1

SIM1 is a bHLH-PAS transcription factor with strong, specific hypothalamic-development biology. Germline `Sim1` loss eliminates late differentiation of PVN, aPV, and SON neuroendocrine neurons expressing oxytocin, vasopressin, thyrotropin-releasing hormone, corticotropin-releasing hormone, and somatostatin, and it acts upstream of `Pou3f2`/BRN2 in those lineages (Michaud et al. 1998). ARNT2, not generic ARNT, is the best-established SIM1 dimerization partner in vivo: `Sim1` and `Arnt2` are co-expressed in PVN/SON, form dimers in vitro, and their null mutants disrupt the same neuroendocrine lineages (Michaud et al. 2000). SIM2 and OTP participate in a related anterior-hypothalamic TF network, with SIM2 downstream of SIM1 for subsets of `Trh` and `Sst` expression (Goshu et al. 2004; Alvarez-Bolado 2018).

Those mechanisms argue that an exact acute `Sim1` perturbation would be meaningful in SIM1-positive PVH/SON/aPV neurons, especially if `Oxt`, `Mc4r`, or neuropeptide expression were measured in the affected hypothalamic cells. Postnatal CNS Sim1 deletion can cause hyperphagic obesity without gross PVN hypocellularity and can reduce hypothalamic `Oxt` and PVN `Mc4r` mRNA (Tolson et al. 2010), so the gene is not only embryonic.

The required cell group is different: `151 TH Prkcd Grin2c Glut` is a broad thalamic glutamatergic class, not the PVN/SON/aPV hypothalamic population that carries the direct SIM1 program. The screen delivered guides at P16 and assayed P37-P44 recovered NeuN-positive nuclei, so it is poorly matched to the embryonic terminal-differentiation phenotype and to rare PVH neuropeptide cells. In the supplied training endpoint, the visible hypothalamic developmental factors `Nkx2-1`, `Neurog3`, `Isl1`, `Nr5a1`, and `Nr5a2` all had 0 focal DEGs, and the mature PVH or energy-balance receptors `Lepr`, `Htr2c`, and `Gpr45` also had 0. Their parquet rows showed no FDR-supported movement of the canonical SIM1/PVH marker set in the focal thalamic class. The visible broad bHLH-PAS cofactor `Arnt` was flat as well, while `Bmal1` showed that a PAS-family perturbation can be detected in this assay only when it drives the active clock state and therefore is not a SIM1 surrogate.

I therefore predict no genes will pass FDR 0.05 for `Sim1` in `151 TH Prkcd Grin2c Glut`.

## Limits

This is a zero/nonzero extrapolation with the closest direct partners held out or absent: `Arnt2`, `Otp`, `Pou3f2`, and `Sim2` would have been better within-dataset controls than generic `Arnt` or hypothalamic receptors. The training zeros are assay zeros in broad recovered cell classes; they do not show that CRISPR failed or that SIM1 has no function in PVH/SON/aPV neurons. Conversely, Bmal1's strong focal response proves only that a bHLH-PAS transcriptional module can be measured in this thalamic class, not that every PAS-family transcription factor should be visible. The final integer is the most likely value for this assay-specific FDR-count endpoint, with uncertainty concentrated between a true zero and a very small singleton/doublet response.
