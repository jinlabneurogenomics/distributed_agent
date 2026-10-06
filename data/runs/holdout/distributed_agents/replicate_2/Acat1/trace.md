# DEG-count prediction trace

## Question and resolved ambiguities

The held-out manifest contains one target, `Acat1`, to be predicted in `151 TH Prkcd Grin2c Glut`.
The endpoint is the focal-cell count of measured genes with `pvals_adj < 0.05` after an acute, mosaic AAV-PHP.eB CRISPR loss-of-function perturbation in postnatal mouse neurons. I treated a gene as a positive count only if it would plausibly pass the same Wilcoxon/BH threshold in this assay; partial target-RNA reduction alone was not enough, because many training targets show negative self log-fold changes without producing a significant self row or a downstream program.

The main symbol ambiguity is that mouse `Acat1` is mitochondrial acetyl-CoA acetyltransferase 1/acetoacetyl-CoA thiolase T2, used in ketone-body utilization and isoleucine catabolism. I did not treat it as the ER cholesterol acyltransferase/sterol O-acyltransferase `Soat1`.

## Sources

- `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`: observed `n_degs` for 1,674 non-held-out training perturbations in the focal cell group.
- `training_de_all_cell_groups.parquet`: per-gene signed log2 fold changes and Wilcoxon FDR values. I filtered this to `group_name == "151 TH Prkcd Grin2c Glut"` and candidate metabolic perturbations.
- Distributed Agents same-experiment corpus, release `perturbai-july-260713-sourceguard-1773-v1`. `target_context(Acat1)` had no direct Acat1 records, so I used corpus claims and findings for represented comparator genes: `Auh`, `Bckdhb`, `Bckdk`, `Ivd`, `Pcca`, `Dld`, `Dlat`, `Pdha1`, `Aco2`, `Hmgcr`, `Srebf1`, `Srebf2`, and `Ppargc1a`.
- Distributed Agents runtime profile comparison over a hand-selected 24-gene metabolic comparator panel in the focal cell group. This was used to audit signed-expression behavior and response activity, not to weight null vectors as if they were strong neighbors.
- PubMed literature:
  - Abdelkreem et al. 2019, Human Mutation, DOI `10.1002/humu.23831`, PMID `31268215`: ACAT1 encodes mitochondrial acetoacetyl-CoA thiolase/T2; biallelic loss causes beta-ketothiolase deficiency of ketone-body and isoleucine metabolism.
  - Grunert et al. 2017, Molecular Genetics and Metabolism, DOI `10.1016/j.ymgme.2017.06.012`, PMID `28689740`: beta-ketothiolase deficiency often presents episodically with metabolic ketoacidosis, and many diagnosed individuals are cognitively normal.
  - Horton, Goldstein and Brown 2002, Journal of Clinical Investigation, DOI `10.1172/JCI15593`, PMID `11994399`: SREBPs, especially SREBP2/Srebf2, drive sterol and cholesterol-biosynthesis transcriptional programs.

## Dataset calibration

The focal training endpoint is heavily zero-inflated:

| Count bin | Number of training targets |
|---|---:|
| `0` | 1205 |
| `1-5` | 341 |
| `6-25` | 62 |
| `26-100` | 24 |
| `101-500` | 27 |
| `>500` | 15 |

The median training target had 0 DEGs and the 75th percentile had 1 DEG. The hundreds-to-thousands counts were reserved for broad RNA-processing, ubiquitin/proteasome, and chromatin/transcriptional regulators such as `Uba5` with 2677, `Tpr` with 1768, `Sin3a` with 1433, and `Rnpc3` with 868. A single mitochondrial catabolic enzyme therefore needs direct evidence before assigning a nonzero or broad count.

For the focal cell group, I extracted 17,259 tested genes for each of the following Acat1-adjacent or counterexample perturbations:

| Training target | Focal `n_degs` | Acat1 relevance |
|---|---:|---|
| `Auh` | 0 | Leucine catabolism; same broad BCAA/organic-acid compartment as ACAT1. |
| `Ivd` | 0 | Leucine catabolism feeding organic-acid metabolism. |
| `Bckdhb` | 0 | BCKDH E1-beta, upstream of branched-chain amino-acid catabolism. |
| `Bckdk` | 0 | Regulator of BCKDH flux. |
| `Pcca` | 0 | Organic-acid mitochondrial carboxylase comparator. |
| `Dld` | 0 | Shared lipoamide dehydrogenase for several mitochondrial alpha-ketoacid dehydrogenases. |
| `Etfa` | 0 | Electron-transfer flavoprotein, adjacent fatty-acid/amino-acid oxidation. |
| `Aco2` | 0 | TCA-cycle mitochondrial aconitase. |
| `Mpc1` | 0 | Mitochondrial pyruvate carrier. |
| `Ogdh` | 0 | TCA alpha-ketoglutarate dehydrogenase. |
| `Pank2` | 0 | Mitochondrial CoA biosynthesis branch. |
| `Hmgcr` | 0 | Sterol/mevalonate counterexample connected to acetyl-CoA but not to ACAT1 ketolysis. |
| `Srebf1` | 0 | SREBP paralog counterexample. |
| `Ppargc1a` | 0 | Mitochondrial transcriptional regulator counterexample. |
| `Hsd17b4` | 0 | Peroxisomal beta-oxidation counterexample. |
| `Dlat` | 1 | PDC component; significant row was `Dlat` itself. |
| `Mdh2` | 1 | Mitochondrial malate dehydrogenase; significant row was `Mdh2` itself. |
| `Pdha1` | 1 | PDC E1-alpha; significant row was `Pdha1` itself. |
| `Sdha` | 1 | TCA/Complex II; significant row was `Sdha` itself. |
| `Ndufs2` | 1 | Complex I; significant row was `Ndufs2` itself. |
| `Uqcrc2` | 1 | Complex III; significant row was `Uqcrc2` itself. |
| `Srebf2` | 7 | A clear but small SREBP2 sterol response: `Srebf2`, `Dhcr24`, `Insig1`, `Hmgcs1`, `Msmo1`, `Cyp51`, `Sqle`. |

The self-transcript rows showed why I did not automatically assign one DEG. `Auh`, `Bckdhb`, `Bckdk`, `Dld`, `Ivd`, `Pcca`, and `Hmgcr` all had negative target-gene log-fold changes in the focal group but had self-row adjusted p values of 1.0. The positive singletons required stronger self rows, for example `Pdha1` log2FC `-1.039`, FDR `1.3e-6`, `Mdh2` `-0.840`, FDR `7.4e-5`, `Sdha` `-0.781`, FDR `2.1e-12`, and `Dlat` `-0.673`, FDR `2.8e-7`. Thus a mild Acat1 on-target change would still be counted as zero.

The Distributed Agents corpus broadened the focal-group evidence: `Auh` produced no BH-significant downstream response in any of 21 recovered neuronal groups; `Bckdhb` was pan-neuronal null; `Bckdk`, `Ivd`, `Mmaa`, and `Pcca` similarly lacked the expected ISR, mitochondrial-stress, redox, or autophagy programs. The represented mitochondrial carbon-entry/PDC/TCA genes were summarized as generally failing to induce a coherent postmitotic neuronal nuclear DE module, with only isolated self or singleton events. Conversely, the same corpus showed that a sterol module is readable in this assay when the perturbed gene is the direct transcription factor `Srebf2`, but `Hmgcr`, `Srebf1`, and `Ppara` do not reproduce that response.

The runtime profile comparison agreed with the count table. The five closest catabolic comparators for Acat1 that are actually in training, `Auh`, `Bckdhb`, `Bckdk`, `Ivd`, and `Pcca`, were all classified as `no_significant_features` in `151 TH Prkcd Grin2c Glut`. I inspected profile similarities among the 24 comparator genes only as a guardrail, because near-null signed profiles share sparse rare-gene tails and should not be interpreted as evidence for a real pathway module.

## Target-specific reasoning

### `Acat1`

`Acat1` acts at mitochondrial acetoacetyl-CoA/acetyl-CoA thiolase chemistry and at 2-methylacetoacetyl-CoA cleavage in isoleucine degradation. Its best represented analogs in the training set are therefore the BCAA/leucine/organic-acid mitochondrial genes, not sterol esterification genes.

Direct ketone-body enzymes or thiolase paralogs were absent from the 1,674 training targets: no `Oxct1`, `Bdh1`, `Aacs`, `Acaa2`, `Acaa1a`, `Acaa1b`, or `Acat2`. I therefore used weaker biochemical neighbors. Those were consistently flat in the focal group: `Auh = 0`, `Ivd = 0`, `Bckdhb = 0`, `Bckdk = 0`, `Pcca = 0`, and `Dld = 0`. The internal corpus says the same null pattern held across their broader neuronal surfaces and that those perturbations did not evoke an ATF4/ISR, mitochondrial-stress, or autophagy/lysosomal RNA program. This argues that acute partial perturbation of a postmitotic organic-acidemia enzyme is usually buffered at the nuclear snRNA level.

The carbon-metabolism counterexamples do not force a nonzero call. `Dlat`, `Pdha1`, `Mdh2`, `Sdha`, `Ndufs2`, and `Uqcrc2` were one-DEG perturbations in this cell group, but the passing DEG was the target transcript itself in each case. Their self log2FC values ranged from `-0.576` to `-1.039` and were more statistically resolved than the observed self rows of the BCAA/organic-acid comparators. `Acat1` is not a respiratory-chain structural subunit, and there is no evidence from `Auh`/`Ivd`/`Bckdhb` that this catabolic branch reliably produces a significant self row or a secondary stress marker.

The sterol branch was treated as a boundary rather than as positive evidence. `Srebf2 = 7` proves that this cell group can report cholesterol-biosynthesis genes, but `Hmgcr = 0`, `Srebf1 = 0`, `Ppargc1a = 0`, and the corpus finding that HMG-CoA reductase did not reproduce the SREBP2 response make Srebf2 a poor template for a ketolysis enzyme. `Acat1` consumes or produces acetyl-CoA/acetoacetyl-CoA in mitochondria; it is not the transcriptional activator of the `Dhcr24`/`Hmgcs1`/`Sqle` sterol module.

External biology pushes the same direction. Human ACAT1 deficiency is episodic and stress-dependent rather than a constitutive lethal mitochondrial lesion in all cells, which is compatible with no broad basal neuronal RNA response three to four weeks after a sparse partial perturbation. The sampled experiment also lacks the liver, glia-rich, and ketogenic-stress contexts where ketone and organic-acid metabolism would be most challenged.

Prediction: `Acat1` is most likely a transcriptional zero in `151 TH Prkcd Grin2c Glut`, so I assign `0` DEGs.

## Limits

- No direct Acat1 Perturb-seq signature, ketone-body enzyme, or mitochondrial thiolase paralog was present in the training data, so the prediction extrapolates from adjacent BCAA/organic-acid nodes.
- A zero predicted count does not mean Acat1 editing would be absent or biologically irrelevant; it means no measured nuclear transcript is expected to cross BH FDR 0.05 in this readout.
- The available assay was acute, sparse, postnatal, and basal. ACAT1 biology is most obvious under ketogenic or catabolic stress, and that stress was not imposed.
- The profile-neighbor cosines among mostly null genes were used only for quality control. They are not strong mechanistic similarity evidence because significant-feature overlap was absent for the direct catabolic comparators.
