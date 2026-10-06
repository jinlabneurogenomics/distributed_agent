# Prediction trace for `151 TH Prkcd Grin2c Glut`

## Question and interpretation

The requested held-out perturbation list contains one target, `St3gal3`. I interpreted `n_degs` exactly as in the focal training CSV: the number of measured genes with Scanpy Wilcoxon Benjamini-Hochberg adjusted `pvals_adj < 0.05` in `151 TH Prkcd Grin2c Glut`, including the perturbed transcript itself when it is measured and significant. This matters here because several glycosylation and sphingolipid pathway perturbations in the focal cell group have `n_degs = 1` only because the on-target mRNA is depleted, with no additional downstream genes passing FDR.

## Evidence sources

- `training_de_all_cell_groups.parquet`: used for focal-cell expression signatures, on-target rows, sample counts, and analog-specific FDR genes.
- `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`: used as the focal endpoint for all non-held-out perturbations. It contains 1,674 training targets; 1,205 have zero DEGs, 276 have one DEG, the median is 0, the 75th percentile is 1, and the mean is 14.05 because a small high tail reaches 2,677 DEGs.
- `225_St3gal3.csv`: used only for the requested target order; it contains only `St3gal3`.
- Distributed Agents corpus MCP, release `perturbai-july-260713-sourceguard-1773-v1`: used for same-experiment bottom-up findings and claims. `target_context(St3gal3)` was empty, so there was no direct internal claim about held-out `St3gal3`; I used claims and target findings for measured neighbors such as `St3gal5`, `Tmem165`, `Dpm1`, and `Pign`.
- Distributed Agents runtime `profile_neighbors`: used on the focal parquet rows to confirm that measured analogs with sparse or null FDR surfaces did not have strong full-rank score neighbors hidden below the FDR threshold.
- PubMed literature for outside function:
  - Sturgill et al. 2012, Glycobiology, DOI `10.1093/glycob/cws103`, PMID `22735313`.
  - Yoo et al. 2015, FASEB Journal, DOI `10.1096/fj.15-270983`, PMID `25846372`.
  - Edvardson et al. 2012, Epilepsia, DOI `10.1111/epi.12050`, PMID `23252400`.
  - van Diepen et al. 2018, European Journal of Human Genetics, DOI `10.1038/s41431-018-0220-5`, PMID `30089820`.
  - Indellicato et al. 2020, Glycobiology, DOI `10.1093/glycob/cwz079`, PMID `31584066`.
  - Gordon-Lipkin et al. 2018, Journal of Child Neurology, DOI `10.1177/0883073818791099`, PMID `30185102`.

## Computational checks

1. I loaded the focal training count CSV and used it to calibrate the overall sparsity of this endpoint. Most target perturbations in this cell group are FDR-null, and among positives the modal nonzero count is a singleton.
2. I filtered the parquet to `group_name == "151 TH Prkcd Grin2c Glut"` for mechanistically relevant measured targets. Each queried focal profile had 17,259 measured genes and shared 23,679 matched controls; matched perturbed counts for the local analogs ranged from 75 to 234 nuclei.
3. I recomputed `sum(pvals_adj < 0.05)` from the parquet for the local analogs and inspected their significant rows. This separated true downstream responses from one-DEG profiles where the sole DEG was the target mRNA.
4. I inspected `St3gal3` as a measured transcript across all 1,674 non-held-out perturbations in the focal cell group. It was present in all 1,674 signatures but never significantly regulated by other perturbations; its best adjusted p-value was 0.229. That does not predict guide activity against `St3gal3`, but it argues that no broad training perturbation in this group secondarily drives the `St3gal3` transcript.
5. I ran `profile_neighbors` over focal Wilcoxon `scores` for `St3gal5`, `Sptlc2`, `Asah1`, `Dpm1`, `Pign`, and `Tmem165`. Their strongest whole-profile Pearson neighbors were weak: `St3gal5` max 0.105, `Sptlc2` max 0.075, `Asah1` max 0.147, `Dpm1` max 0.124, `Pign` max 0.062, and `Tmem165` max 0.084. This supported the corpus interpretation that these are sparse or null surfaces, not members of a strong shared module.

## Target-specific reasoning

### `St3gal3`

**Closest same-experiment analogs**

| training perturbation | focal `n_degs` | focal expression-pattern evidence | use for `St3gal3` |
| --- | ---: | --- | --- |
| `St3gal5` | 1 | The only focal DEG was `St3gal5` itself, down in the knockout, `logfoldchanges = -0.788`, `pvals_adj = 1.96e-14`; Distributed Agents `St3gal5:F002-F005` and claim `claim:4b050bd7d7e8716535f4` report absence of canonical ganglioside, UPR/ISR, apoptosis, or coherent sphingolipid-neighbor programs after acute `St3gal5` loss. | Best measured same-family analog. It is also an alpha2,3-sialyltransferase acting on glycolipid substrates, but it makes GM3 at the entry to ganglio-series synthesis, whereas ST3Gal-III acts with ST3Gal-II in terminal GD1a/GT1b and glycoprotein sialylation, so it is not an enzyme-equivalent phenocopy. |
| `Sptlc2` | 1 | The only focal DEG was `Sptlc2` itself, `logfoldchanges = -0.685`, `pvals_adj = 1.45e-4`; its best focal whole-profile neighbor had Pearson 0.075. | Upstream de novo sphingolipid synthesis control; useful as a counterexample showing that disturbing a core lipid-biosynthesis step did not yield a broad ganglioside-related RNA state in this neuronal group. |
| `Asah1` | 0 | No focal FDR genes; in the Distributed Agents corpus `Asah1` is one of the anchors for the claim that represented sphingolipid and lysosomal relatives were flat, singleton-only, or divergent. | Sphingolipid catabolism neighbor, mechanistically more distant than `St3gal5` and therefore mainly a no-broad-module boundary. |
| `Psap` | 1 | The only focal DEG was `Psap` itself, `logfoldchanges = -1.277`, `pvals_adj = 1.70e-28`. | Lysosomal sphingolipid activator and upstream/catabolic comparator; supports sparse response rather than a common secondary lipid stress program. |
| `Sphk1` | 0 | No focal FDR genes; Distributed Agents `Sphk1:F003` reports no convergence with `Asah1`, `Cert1`, `S1pr2`, `Sptlc2`, or `St3gal5`. | Downstream sphingosine/S1P branch boundary. |
| `Cert1` | 0 | No focal FDR genes; Distributed Agents `Cert1:F003` found no data-driven or lipid-transfer convergence with `Sptlc2`, `Sphk1`, or `Stard7`. | Ceramide-transport counterexample, more about the lack of a generic lipid-transfer RNA state than a close prediction. |
| `Stard7` | 0 | No focal FDR genes; Distributed Agents `Stard7:F005` kept it separate from a general lipid-transfer signature. | Lipid-transfer counterexample. |

**Golgi and glycosylation controls**

| training perturbation | focal `n_degs` | focal expression-pattern evidence | use for `St3gal3` |
| --- | ---: | --- | --- |
| `Tmem165` | 0 | No focal FDR genes; Distributed Agents `Tmem165:F001-F003` describe a pan-neuronal FDR-null Golgi Mn/Ca and congenital-disorder-of-glycosylation perturbation, including absence of UPR/ERAD and Golgi-stress marker induction. | Same-organelle glycosylation homeostasis control showing that an active Golgi/CDG gene need not amplify into a nuclear RNA program in this assay. |
| `Cog4`, `Cog5` | 0, 0 | No focal FDR genes; corpus claim `claim:6a94b158a9de9a66a6c3` reports that represented ER-Golgi, COG, SNARE, and Golgi/CDG perturbations do not make one broad secretory-pathway module. | Counterexamples to projecting a generic Golgi-trafficking stress state onto `St3gal3`. |
| `Dpm1` | 0 | No genes pass FDR 0.05 in the focal CSV, and Distributed Agents `Dpm1:F001-F004` show only a tiny Pdia6/Ttyh3 signal at FDR 0.10 tracking dolichol/Dol-P-Man rather than distal glycosylation branches. | A broader glycan-precursor perturbation can be barely detectable, but its specific dolichol/ER-glycan signal is not the branch affected by ST3Gal-III. |
| `Pign`, `Fktn` | 0, 0 | Downstream GPI and O-mannosylation branch perturbations were flat in the focal CSV and did not phenocopy `Dpm1` in Distributed Agents claim `claim:691f740a7ddd8777ef62`. | Distal glycosylation disease genes are relevant negative controls. |
| `Gfpt1`, `Dhdds`, `Vps54` | 311, 116, 31 | These are broad or moderate responders in the same focal group. `Gfpt1` activated a UPR/HBP glycosylation program, and `Dhdds` induced ER-quality-control and ATF4-like amino-acid/tRNA-charging genes including `Hspa5`, `Ddit3`, `Herpud1`, and `Pdia6`. | Counterexamples showing the assay can see ER glycan and trafficking stress when it is actually induced, but they act upstream through hexosamine or dolichol/vesicle axes rather than terminal sialyltransferase chemistry. |

**External biology**

ST3Gal-III is a Golgi beta-galactoside alpha2,3-sialyltransferase. Germline and congenital data make it a real neural gene: Sturgill et al. showed that mouse St3gal2 and St3gal3 together produce nearly all terminal alpha2,3 sialylation of brain GD1a and GT1b gangliosides, and Yoo et al. showed that St3gal2/3 double-null mice have dysmyelination, node-of-Ranvier defects, smaller hippocampal dendritic arbors, and motor/cognitive phenotypes. Human biallelic ST3GAL3 variants cause developmental and epileptic encephalopathy or West syndrome, and patient-derived cortical neurons show altered surface sialylation and adhesion phenotypes. These facts make a subtle neuronal consequence plausible, but most of that evidence comes from germline or differentiating systems and from glycan-level defects rather than from acute postmitotic, mosaic loss in NeuN+ nuclei.

ST3GAL3 is not the rate-limiting entry enzyme for ganglio-series synthesis in the way ST3GAL5/GM3 synthase is. The strongest within-dataset analog, `St3gal5`, had a one-gene focal result consisting only of on-target `St3gal5` depletion; represented upstream and catabolic sphingolipid neighbors were also zero or self-only. I therefore expect `St3gal3` loss to lack a multi-gene downstream response in `151 TH Prkcd Grin2c Glut`. Because `St3gal3` is a measured transcript in this focal universe and the same-family `St3gal5` target mRNA was robustly depleted, my point prediction is a singleton DEG, most likely the `St3gal3` self row rather than a secondary stress or ganglioside-compensation gene.

**Prediction**

`St3gal3`: **1 DEG**.

## Limits

- There is no same-experiment `St3gal3` perturbation or direct Distributed Agents corpus finding for this held-out target, and `St3gal2`, `St3gal4`, `B4galnt1`, and most other ganglioside-pathway glycosyltransferases were not present as focal training perturbations. The closest direct analog is therefore `St3gal5`, which uses different acceptors and sits at a different step of ganglioside synthesis.
- The predicted nonzero call is driven mostly by expected on-target RNA depletion. The within-dataset evidence argues against additional downstream DEGs.
- snRNA-seq cannot see the primary ganglioside or glycoprotein sialylation lesion. A biologically meaningful surface-glycan phenotype could still produce zero nuclear DEGs.
- The external ST3GAL3 evidence is mostly germline, developmental, complete-loss, or human patient biology; this assay is sparse AAV CRISPR delivered at P16 and read out only 3-4 weeks later in surviving NeuN+ nuclei.
