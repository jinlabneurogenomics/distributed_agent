# Trace

## Target and endpoint

Target perturbation: `Adrb1`

Endpoint to forecast: `n_degs` in `151 TH Prkcd Grin2c Glut`, the count of measured genes with BH-adjusted Wilcoxon `pvals_adj < 0.05`.

## Evidence used

- The declared target biology bundle reports that `Adrb1` is measurably present in the focal non-target population: 9,071 of 23,679 nuclei express the RNA, or 38.31%, with low average abundance of 0.539 raw UMI and 0.328 CP10K per nucleus. This supports possible target engagement in the assayed thalamic class but also leaves most nuclei without detectable `Adrb1` RNA at baseline.
- The same bundle adjudicates the Adrb1 receptor stock as likely substantially depleted by the 21-28 day harvest. Adrb1 is a renewable beta-adrenergic GPCR, a heterologous total beta-1 receptor half-life was about 13 h, and postnatal conditional Adrb1 deletion in adult mouse mPFC produced a neural phenotype after four weeks. I therefore treated the perturbation as plausibly realized, not as a durable-protein null.
- The focal training count table is dominated by null or near-null perturbations. Among 1,674 training targets, 1,205 had `n_degs = 0`, the median was 0, the 75th percentile was 1, the 90th percentile was 2, and the mean of 14.05 was driven by a long tail of large proteostasis, spliceosome, and chromatin responses.
- I chose same-pathway training perturbations around ligand-gated monoamine GPCRs, proximal cAMP signaling, and a few adjacent excitability nodes. In the exact focal Parquet slice, every close adrenergic and proximal cAMP comparator was zero at FDR 0.05:
  - `Adrb2`: 0, `Adrb3`: 0
  - `Adra1a`: 0, `Adra2a`: 0, `Adra2b`: 0
  - `Adcy1`: 0, `Adcy3`: 0, `Adcy5`: 0
  - `Gnas`: 0, `Gnal`: 0, `Pde10a`: 0
  - `Drd2`: 0, `Drd4`: 0, `Drd5`: 0
  - Gs-linked serotonin receptors `Htr4`, `Htr6`, and `Htr7`: all 0
- More distal nodes were still sparse rather than broad in the same focal slice: `Prkaca` and `Prkar1a` had one DEG each, `Kcnq2` and `Kcnq3` had one each, and direct `Creb1` had 10. That pattern argues that the screen could recover a focal thalamic CREB-axis RNA response, but that receptor/G-protein/adenylyl-cyclase loss was usually transcriptionally buffered.
- Same-experiment corpus reports reinforced the exact focal counts without acting as independent replication. `Adrb2` was reported as a complete basal neuronal transcriptomic null across 23 recovered groups at FDR < 0.10. `Adra1a` had no downstream FDR < 0.10 response in 22 recovered neuronal groups. `Adcy5` had zero downstream genes across 22 groups, and the represented adenylyl-cyclase paralogs `Adcy1`, `Adcy3`, and `Adcy5` shared absence of a downstream FDR < 0.10 module. The `Adrb2` report specifically contrasted flat beta-adrenergic and proximal cAMP perturbations with a detectable direct `Creb1` response.

## Synthesis

`Adrb1` differs from the completely flat `Adrb2` and `Adrb3` training rows because it is detectably expressed in this focal thalamic population and its functional stock should have turned over before harvest. That makes a small nonzero effect possible.

The better-supported direction, however, is a basal nuclear-RNA null. The target is a ligand-regulated GPCR rather than a transcriptional regulator or housekeeping complex, the focal expression reach is only partial and low-abundance, and the training evidence shows a broad measured buffer around catecholamine receptors and the Gs/cAMP arm. The distal `Creb1` exception makes the upstream flatness more informative: receptor loss did not constitutively drive the same transcriptomic state in the represented training perturbations.

I therefore forecast that `Adrb1` will sit with the close adrenergic and adenylyl-cyclase comparators, not with the rare broad-response tail or the direct CREB perturbation.

Predicted `n_degs`: 0
