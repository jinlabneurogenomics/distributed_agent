# Avpr2 DEG-count prediction for `151 TH Prkcd Grin2c Glut`

## Question and endpoint

I interpreted the task as a scalar holdout prediction for one requested perturbation, `Avpr2`, in the focal thalamic glutamatergic class `151 TH Prkcd Grin2c Glut`. The endpoint is the number of measured genes with `pvals_adj < 0.05` in the focal class after sparse postnatal AAV-CRISPR loss of the held-out gene.

`Avpr2` itself is withheld: it has 0 `gene_target` rows in `training_de_all_cell_groups.parquet` and is absent from `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`. I therefore used the training counts and DE rows for represented nonapeptide receptors and Gs/cAMP pathway genes as the same-experiment evidence, then used gene-function priors to decide which of those perturbations are biologically transferable.

## Sources

- Declared direct endpoint: `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
- Declared DE dataset: `training differential-expression dataset`.
- Requested-target manifest: `single-target request for Avpr2`.
- Internal same-experiment corpus: `perturbai-july-260713-sourceguard-1773-v1`, queried through `corpus.findings`, `corpus.graph`, and `corpus.report_evidence`. This corpus is a packaged interpretation of the same Perturb-seq experiment, not independent replication.
- External knowledge from curated databases and literature:
  - NCBI Gene annotations for AVPR1A, AVPR1B, GNAS, and AVPR2; UniProtKB annotations for vasopressin receptors.
  - Bockenhauer and Bichet 2015, Nature Reviews Nephrology, DOI `10.1038/nrneph.2015.89`, PMID `26077742`, for the canonical renal AVPR2 -> cAMP -> AQP2 water-reabsorption axis.
  - Balla and Hunyady 2019, Experientia Supplementum, DOI `10.1007/978-3-030-25905-1_15`, PMID `31588538`, for AVPR2/AQP2 physiology in nephrogenic diabetes insipidus.
  - Dumais and Veenema 2016, Frontiers in Neuroendocrinology, DOI `10.1016/j.yfrne.2015.04.003`, PMID `25951955`, for brain vasopressin and oxytocin receptors being receptor-, region-, and sex-dependent rather than interchangeable pan-neuronal basal transcriptional regulators.
  - Ocampo Daza et al. 2022, Frontiers in Endocrinology, DOI `10.3389/fendo.2021.792644`, PMID `35185783`, for the shared evolutionary origin of oxytocin/vasopressin receptor subtypes.
  - Ostrom et al. 2022, Physiological Reviews, DOI `10.1152/physrev.00013.2021`, for redundancy and compartmentalization among mammalian transmembrane adenylyl cyclase isoforms.
  - Nestler and Duman 1999 and Eberwine 1999, Basic Neurochemistry, NCBI Bookshelf, for Gs/Golf-to-adenylyl-cyclase-to-cAMP/PKA/CREB coupling in neurons.

## Computation over the declared dataset

I first summarized the training endpoint distribution in the focal class. It is zero-inflated: 1,205 of 1,674 training biological perturbations have `n_degs = 0`, the median is 0, the 75th percentile is 1, and only 5% of training targets exceed 18 DEGs. Thus an isolated weak receptor-pathway prior should predict zero unless same-experiment analogs show that this family has a focal RNA footprint.

For `Avpr2`, the biologically relevant training comparisons were:

| training perturbation | relation to Avpr2 | focal `n_degs`, FDR 0.05 | focal minimum FDR | focal matched perturbed nuclei | same-experiment expression-pattern evidence |
|---|---:|---:|---:|---:|---|
| `Avpr1a` | nonapeptide GPCR paralog; V1a is mainly Gq/PLC rather than V2/Gs | 0 | 0.841 | 234 | No 151 TH response; only one FDR<0.10 event in the full screened neuronal surface, `Srsf6` up in `110 CNU-HYa HY MM Glut`. |
| `Avpr1b` | nonapeptide GPCR paralog; V1b is mainly Gq/PLC and sparse in brain | 0 | 0.569 | 199 | No FDR<0.10 downstream genes in any of 23 measured neuronal groups. |
| `Oxtr` | closest oxytocin-family receptor, mainly Gq/PLC | 0 | 1.000 | 192 | 0 focal DEGs; only isolated one-gene effects in non-focal groups. |
| `Gnas` | direct Gs-alpha transducer used by AVPR2 | 0 | 1.000 | 306 | Zero focal DEGs; in the full surface only one sub-FDR0.10 `Snx29` event in cortical L5-6 IT. The expected CREB/immediate-early module was absent. |
| `Adcy1` | neuronal cAMP synthesis downstream of Gs | 0 | 0.139 | 88 | Zero focal DEGs and zero FDR<0.10 genes in 20 measured groups. |
| `Adcy3` | cAMP synthesis downstream of Gs, cilia-enriched | 0 | 0.112 | 223 | Zero focal DEGs; family-wide adenylyl-cyclase responses were buffered. |
| `Adcy5` | cAMP synthesis downstream of Gs/Golf | 0 | 0.912 | 154 | Zero focal DEGs and no broad downstream FDR signal across recovered neuronal groups. |
| `Pde4b` | cAMP degradation; biochemical sign is opposite to AVPR2 loss | 0 | 0.922 | 211 | Zero focal DEGs; only sparse singleton effects in `155 MB Glut` and `191 MB P MY GABA`. |
| `Pde4d` | cAMP degradation; biochemical sign is opposite to AVPR2 loss | 0 | 1.000 | 192 | Zero focal DEGs and no FDR<0.10 focal genes. |
| `Prkaca` | PKA catalytic subunit downstream of cAMP | 1 | 7.91e-22 | 192 | The single focal DEG is `Prkaca` itself; downstream genes remain subthreshold. |
| `Creb1` | nuclear transcriptional effector, downstream rather than receptor-level | 10 | 3.82e-7 | 126 | Focal `Crem` up-regulation and a small CREB-family transcriptional response show that the assay can detect the endpoint once perturbation hits the nuclear branch. |
| `Crebbp` | nuclear co-activator downstream of CREB-dependent transcription | 8 | 5.01e-4 | 61 | Nonzero focal effect, but this is a chromatin/co-activator perturbation rather than loss of a ligand-gated membrane GPCR. |

The Parquet query grouped rows by `gene_target` and `group_name`, counted `pvals_adj < 0.05` and `< 0.10`, took the minimum adjusted p-value, and averaged the matched perturbed/control counts. I then inspected the top ten focal rows by adjusted p-value for the receptor and cAMP candidates to check for near-threshold genes. There was no hidden focal Avpr-family pattern: in the focal class the best `Avpr1a`, `Avpr1b`, and `Oxtr` rows had adjusted p-values 0.841, 0.569, and 1.000, respectively. `Avpr2` exists as a measured transcript in other perturbations, but because `Avpr2` itself is held out there is no `gene_target = Avpr2` DE surface and therefore no Avpr2 self row for the requested perturbation.

## Avpr2-specific causal transfer

The causal chain I used was: acute sparse CRISPR loss of `Avpr2` -> reduced V2 receptor signaling where the receptor is expressed -> reduced Gs-stimulated adenylyl cyclase/cAMP/PKA output -> possible CREB-dependent nuclear transcription -> recovered postnatal NeuN+ nuclei in `151 TH Prkcd Grin2c Glut` -> Wilcoxon/BH DEG count.

`Avpr1a`, `Avpr1b`, and `Oxtr` are the nearest represented receptor-family comparisons, but they are not obligate partners of AVPR2. They bind the same nonapeptide hormone family and share GPCR ancestry, yet V1a/V1b/OXTR signal predominantly through phosphatidylinositol-calcium/Gq while V2 is a Gs/cAMP receptor. The fact that all three represented family perturbations have 0 focal DEGs argues against a generic nonapeptide-receptor RNA state in the focal thalamic population. It does not by itself prove `Avpr2` should be identical, so I treated it as directional same-family evidence only after checking the downstream Gs/cAMP nodes.

`Gnas` is a stronger pathway analog for AVPR2 than V1a/V1b/OXTR at the level of second messenger, because V2 uses Gs to activate adenylyl cyclase. The transfer also points to zero: `Gnas` loss in the same focal group had 306 perturbed nuclei, 0 FDR0.05 DEGs, and minimum adjusted p-value 1.000. The same-experiment corpus reported no broad Gs/cAMP/CREB immediate-early state after `Gnas` across all 23 assayed classes. Single adenylyl-cyclase isoforms `Adcy1`, `Adcy3`, and `Adcy5` were also zero in the focal group, and the `Adcy1`/`Adcy3`/`Adcy5` corpus reports interpreted them as buffered basal cAMP perturbations rather than FDR-supported CREB-module perturbations. The only positive counterexamples, `Creb1` and `Crebbp`, sit downstream in the nucleus; they establish endpoint detectability in `151 TH Prkcd Grin2c Glut`, but they do not rescue the receptor-level AVPR2 prediction because the Gs and ADCY steps upstream of CREB were silent.

External AVPR2 biology makes a broad thalamic neuronal signature still less likely. AVPR2 is best established as the renal collecting-duct V2 receptor that couples vasopressin to Gs/cAMP/PKA-dependent aquaporin-2 regulation and urinary concentration; loss causes X-linked nephrogenic diabetes insipidus. That canonical target-cell chain is in collecting-duct epithelium, not a whole-brain NeuN+ thalamic glutamatergic nucleus population. The experiment also lacked an AVP pulse or osmotic/endocrine challenge, so even low off-target expression in a tiny neuronal subset would have to generate a durable basal nuclear RNA program that was not seen for `Avpr1a`, `Avpr1b`, `Oxtr`, `Gnas`, or the represented adenylyl cyclases.

## Prediction and limits

I predict `Avpr2` will have no measured genes passing BH FDR 0.05 in `151 TH Prkcd Grin2c Glut`, so the point prediction is `0`.

The key limitation is that this is extrapolation from related training perturbations because the held-out DE signature and DEG count are absent by construction. AVPR2 itself was not perturbed in the training Parquet, so there is no way to verify guide recovery, target DNA editing, or rare receptor expression directly. The central vasopressin-family comparators are imperfect because V1a/V1b/OXTR use Gq/PLC rather than V2/Gs, while Gnas/ADCY/PKA comparisons are pathway-level and can diverge through receptor localization, ligand dependence, redundancy, and compartmentalized cAMP signaling. Those uncertainties would matter most near a small nonzero count, but all receptor-level and membrane-cAMP analogs were focal zeros, making zero the best calibrated point estimate.
