# Ap2m1 DEG-count forecast

Target and endpoint: `Ap2m1` in `151 TH Prkcd Grin2c Glut`; `n_degs` counts measured genes with BH-adjusted Wilcoxon `pvals_adj < 0.05`.

## Evidence used

### Prediction-safe target biology

The declared Ap2m1 biology bundle supports target reach and functional realization in this exact focal population without exposing the held-out response. In non-target `151 TH Prkcd Grin2c Glut` nuclei, `Ap2m1` is detected in 21,579 of 23,679 cells, or 91.13%, with mean raw UMI 3.57 and mean log1p CP10K 1.04, so the target is present in the assayed thalamic population.

The functional-stock card calls the post-P16 perturbation likely to substantially deplete AP-2 by harvest: Ap2m1/AP-2 mu protein had a 5.35 day neuronal-culture half-life, conditional mouse hippocampal Ap2m1 ablation can reduce AP-2 below 15% of wild type, and adult hippocampal AAV-Cre deletion produces mature-neuron spine effects by four weeks. The observability card also gives a same-region prior, because neuron-specific Ap2m1 loss causes postnatal thalamic neuronal degeneration. AP-2 mu is the single mammalian AP-2 mu subunit, so same-complex paralog buffering is not expected.

Those priors push the forecast above a generic null: Ap2m1 should be expressed and its stock should turn over during the 21-28 day experiment. The main downward bearings are that AP-2 is a trafficking adaptor rather than a Rab7-like terminal late-endosome gate, the edit disables new production rather than pre-existing AP-2 complexes, and the single-nucleus readout is conditioned on edited neurons that survived and were recovered.

### Declared focal count table

The declared `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` table has a sparse but heavy-tailed distribution: 1,205/1,674 training targets are zero, the median is 0, the 90th percentile is 2, the 95th percentile is 18, the 97.5th percentile is 100, and only 15 targets have at least 500 DEGs. A forecast for Ap2m1 therefore needs to choose between the near-zero trafficking majority and the rarer endolysosomal/proteostatic tail.

Direct AP/clathrin/synaptic-endocytic comparators in the same table mostly sat near zero in `151 TH`: `Ap1b1` 1, `Ap1s2` 0, `Ap3b1` 0, `Ap4s1` 0, `Cltc` 3, `Dnm1` 1, `Bin1` 1, `Synj1` 1, `Hspa8` 9, `Stxbp1` 1, `Dnajc5` 1, and `Nsf` 0. Endolysosomal comparators were heterogeneous: `Vps35` 17 and `Vps54` 31 were modest; `Atp6ap2` 2, `Vps41` 0, `Becn1` 0, `Lamp2` 0, `Sqstm1` 1, and V-ATPase subunits were 0-1; `Rab7` was the clear upper-bound outlier at 501.

I checked matched focal Parquet rows for the main analogs. `Dnm1`, `Bin1`, `Vps35`, `Vps54`, `Ap1b1`, and `Ap4s1` each had 133-276 perturbed nuclei where they were still weak-to-modest, so the low adaptor/endocytic counts were not simply all low-power zeros. `Cltc` had only 32 and `Ap3b1`/`Synj1` had 85/90, so those specific quiet rows carry a power caveat.

### Training profile and corpus interpretation

The measured profile comparison over selected training analogs kept the same scale split. At `pvals_adj < 0.05`, `Rab7` had 501 significant features, `Vps35` 17, `Vps54` 31, `Cltc` 3, and `Dnm1` 1. Rab7 and Vps35 shared only 2 positive and 5 negative significant genes, Rab7 and Cltc shared 1 negative significant gene, and Cltc and Dnm1 shared no significant genes despite being in the same broad vesicle-cycle neighborhood.

Same-experiment corpus summaries of the training perturbations, interpreted as annotations of the same data rather than independent replication, supported using Rab7 only as an upper boundary. Rab7 induced a recurrent late-endosomal/lysosomal and sterol/proteostasis compensation state; Vps35 produced a much smaller thalamic retromer response without the Rab7 lysosomal program; and canonical clathrin/synaptic-endocytic genes such as Dnm1, Synj1, Bin1, and several AP-family perturbations failed to phenocopy core Cltc or Rab7 responses.

## Synthesis

I placed Ap2m1 above the 0-3 DEG adaptor cluster because its focal expression is very high, AP-2 mu lacks a replacement subunit, and postnatal thalamic neurons have a documented Ap2m1 requirement. I placed it below Rab7 and below the Vps35/Vps54 17-31 range because the measured training set shows that pathway proximity to clathrin/endosomal trafficking usually does not create a large 151 TH nuclear program, even for several represented AP-family and synaptic-vesicle genes, unless the perturbation hits a late endosome/lysosome or broad proteostasis state. The Cltc row is low-powered in this class, but Hspa8 at 9 and Vps35 at 17 provide a plausible local scale for a realized but adaptor-tier trafficking lesion.

Point forecast: `12` DEGs.
