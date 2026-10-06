# Task interpretation

The requested endpoint is a scalar count for each held-out perturbation: the number of genes with Benjamini-Hochberg adjusted Wilcoxon `pvals_adj < 0.05` in the `151 TH Prkcd Grin2c Glut` focal cell group after acute, mosaic, P16 AAV-CRISPR loss of function and P37-P44 snRNA-seq. `Minpp1` is completely held out: it is not a `gene_target` in the Parquet and has no `n_degs` row in the training CSV. I therefore treated its transcript in held-in perturbations as allowable measured-gene evidence, but did not use any held-out `Minpp1` perturbation signature.

# Sources

- Declared training endpoint CSV: `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
- Declared DE Parquet: `training_de_all_cell_groups.parquet`.
- Requested-target manifest: `b0034.csv`, containing only `Minpp1`.
- Run-local dataset portrait, task bindings, coverage, and capability manifest.
- Internal same-experiment semantic corpus `perturbai-july-260713-sourceguard-1773-v1`. `Minpp1` had no packaged Findings and no BioKG comparator edges, so I used the corpus only for bounded held-in analog reports: `Inpp5k`, `Atp2a2`, `Atf6`, and `Hspa5`.
- External mechanism priors from PubMed and named databases:
  - NCBI Gene/RefSeq summaries for ATP2A2/SERCA2 and HSPA5/BiP.
  - Chi et al. 2000, Molecular and Cellular Biology, PMID 10938126, DOI 10.1128/MCB.20.17.6496-6507.2000: mouse `Minpp1` deletion removes ER MINPP1 activity, raises InsP5/InsP6 in fibroblasts, but produces viable and fertile mice with no obvious gross phenotype.
  - Ucuncu et al. 2020, Nature Communications, PMID 33257696, DOI 10.1038/s41467-020-19919-y: human biallelic `MINPP1` loss causes pontocerebellar hypoplasia; MINPP1-null cells and differentiating neurons accumulate IP6 and show inefficient neuronal differentiation plus increased cell death.
  - Appelhof et al. 2020, European Journal of Human Genetics, PMID 33168985, DOI 10.1038/s41431-020-00749-x: independent human biallelic `MINPP1` variants in pontocerebellar hypoplasia.
  - Yu et al. 2023, Biomolecules, PMID 37371464, DOI 10.3390/biom13060885, and Nguyen Trung et al. 2022, ACS Central Science, PMID 36589890, DOI 10.1021/acscentsci.2c01032: MINPP1 is normally confined to the ER and controls a MINPP1-dependent branch of cellular inositol-polyphosphate metabolism.
  - Wiessner et al. 2017, American Journal of Human Genetics, PMID 28190456, and Osborn et al. 2017, American Journal of Human Genetics, PMID 28190459: `INPP5K` phosphoinositide-phosphatase mutations cause congenital muscular dystrophy with cataracts and cognitive involvement.
  - Manzolillo et al. 2024, Frontiers in Molecular Neuroscience, PMID 38559586, DOI 10.3389/fnmol.2024.1356343: `INPP5K` knockdown impairs N2A neuronal differentiation and glycosylation.
  - Britzolaki et al. 2018, Cellular and Molecular Neurobiology, PMID 29663107, DOI 10.1007/s10571-018-0583-8, and Hetz et al. 2020, Nature Reviews Molecular Cell Biology, DOI 10.1038/s41580-020-0250-z: SERCA2 biology and canonical UPR branches used to interpret the ER-stress counterexamples.

# Quantitative calibration from held-in perturbations

The focal training table has 1,674 held-in perturbations. The endpoint is extremely zero-inflated:

- 1,205/1,674 training targets have `n_degs = 0`.
- Median = 0; 75th percentile = 1; 90th percentile = 2; 95th percentile = 18; maximum = 2,677.

Thus a held-out perturbation with no close, high-burden held-in analog should be predicted near zero; a nonzero count needs evidence that the acute perturbation will induce a detectable recovered-cell transcriptional program, not just that germline loss has organismal consequences.

I inspected the focal-cell DE rows for mechanistically plausible held-in neighbors, using Parquet row-group statistics to restrict reading to the `151 TH Prkcd Grin2c Glut` row groups and then filtering by `gene_target`. The closest available inositol/phosphoinositide and ER-calcium controls were:

| held-in perturbation | focal `n_degs` at FDR 0.05 | focal pattern |
| --- | ---: | --- |
| `Inpp5k` | 0 | 159 perturbed vs 23,679 control nuclei; top focal genes all had adjusted P = 1; no UPR, lysosome, autophagy, dystroglycan, or PI3K marker reached even FDR 0.10 in any measured group in the same-experiment corpus. |
| `Itpr1` | 0 | IP3-gated ER calcium release channel; no focal corrected genes and self transcript only FDR 0.086. |
| `Ocrl` | 0 | phosphatidylinositol 4,5-bisphosphate 5-phosphatase; no focal corrected genes. |
| `Synj1` | 1 | the single focal DEG was `Synj1` itself, not a downstream state. |
| `Plcb1` | 0 | produces IP3 from PIP2; no focal corrected genes. |
| `Pik3cb`, `Pik3r1`, `Pik3r2` | 0, 0, 0 | PI3K pathway components; no focal corrected response. |
| `Atf6` | 0 | canonical ER-stress transcription-factor arm; zero corrected genes across the recovered neuronal groups. |
| `Ryr2`, `Ryr3` | 0, 0 | ER calcium-release channels; no focal corrected genes. |
| `Atp2b2`, `Atp2b3`, `Atp2c1` | 1, 1, 1 | each count was essentially self/isolated rather than a UPR-like program. |
| `Hspa5` | 5 | the assay can see focal ER-proteostasis stress: `Hsp90b1`, `Nfe2l1`, `Pdia4`, and `Derl3` were induced. |
| `Sec63` | 11 | another detectable but small ER-proteostasis response, led by `Hspa5`, `Canx`, `Hyou1`, and `Chac1`. |
| `Atp2a2` | 187 | a strong counterexample, with `Ddit3`, `Chac1`, `Xbp1`, `Herpud1`, amino-acid/one-carbon genes, and synaptic-state changes after SERCA2 loss. |

`Minpp1` itself is present as a measured gene in all 1,674 held-in focal comparisons, but it was never a strong recurrent focal marker: the largest absolute Wilcoxon score among held-in perturbations was only 3.54 and no adjusted P-value for the `Minpp1` measured gene was close to 0.05. That check does not estimate MINPP1 editing, but it argues that the held-in expression manifold did not contain an obvious `Minpp1`-marked state to borrow from.

# Target-specific reasoning

## Minpp1

`Minpp1` encodes the ER-localized multiple inositol-polyphosphate phosphatase. At the intervention stage, knocking it out should impair luminal MINPP1 catalytic activity and perturb highly phosphorylated inositol phosphates, especially InsP5/InsP6. That direct molecular consequence is established: complete mouse deletion abolishes Minpp1 enzyme activity and raises InsP5/InsP6 in fibroblasts, while human MINPP1-null cells accumulate IP6. The propagation question for this experiment is whether that metabolic imbalance will, within 3-4 weeks in sparse postmitotic thalamic glutamatergic neurons, become a broad nuclear-RNA UPR, calcium-stress, lysosomal, or survival-state signature among recovered NeuN+ nuclei.

The best held-in direct analog is not `Atp2a2`. SERCA2 loss directly prevents ER Ca2+ reuptake and in the focal class gives a broad UPR/ISR phenotype with 187 DEGs at FDR 0.05, including `Ddit3`, `Chac1`, `Xbp1`, and `Herpud1`. By contrast, the declared same-experiment report for `Atp2a2` shows that related calcium and UPR genes do not generically phenocopy SERCA loss: `Atf6`, `Itpr1`, `Ryr3`, `Atp2b2`, and `Atp2c1` were flat across their surfaces or had only isolated self effects, and `Itpr1`, `Ryr2`, and `Ryr3` all had zero focal DEGs. `Minpp1` is more indirect than SERCA2 for ER Ca2+ depletion because IP6 chelation and inositol-polyphosphate changes must propagate across compartment boundaries before they would engage the same CHOP/HSPA5/XBP1 response.

`Inpp5k` is the sharper within-dataset caution. Like `Minpp1`, it is an inositol/phosphoinositide phosphatase with congenital neuromuscular and neuronal-differentiation literature, and its external phenotypes could have suggested ER/glycosylation/autophagy stress. In this screen, however, acute `Inpp5k` loss produced zero genes even at FDR 0.10 in every measured neuronal group, including a well-powered focal comparison with 159 perturbed nuclei, and none of the expected ER-stress, autophagy-lysosome, dystroglycan-glycosylation, or PI3K/mTOR readouts was corrected. That intervention -> lipid/phosphate-metabolism -> ER/autophagy propagation chain is close enough to `Minpp1` to be a stronger endpoint proxy than generic developmental disease severity.

The external `Minpp1` prior points in two directions. Biallelic human MINPP1 mutations cause pontocerebellar hypoplasia and genome-edited differentiating neurons have inefficient differentiation plus increased death, so the gene is not biologically inert. But the severe human phenotype is congenital and likely involves development and selection, whereas the assay perturbs juvenile postmitotic neurons and then observes only nuclei that survived and were recovered. The original mouse germline knockout was viable and fertile without obvious defects despite biochemical IP5/IP6 changes, making a massive, cell-autonomous postnatal thalamic transcriptome unlikely.

My prediction is therefore that acute `Minpp1` loss will be a corrected-transcriptome null or near-null in recovered `151 TH Prkcd Grin2c Glut` cells. I assign zero rather than one because the focal held-in inositol/phosphoinositide analogs were all zero except `Synj1`, whose lone DEG was self; a self-only count is not predictable for a held-out target from pathway membership, and `Minpp1` does not have a held-in paralog with a reliable self knockdown signature.

# Limits

This is an extrapolation over a missing perturbation, not a direct observation. The closest exact enzymes in MINPP1's cytosolic InsP5/InsP6 network (`Ipmk`, `Ippk`, `Itpk1`, `Impa1`, `Impa2`) were not held-in focal targets, and mammalian MINPP1 has no simple redundant paralog to average. `Inpp5k` is a phosphoinositide 5-phosphatase rather than an ER-luminal InsP5/InsP6 phosphatase, so its null response is only a pathway-stage analog. Conversely, the strong `Atp2a2` and `Hspa5` signatures prove that this assay can see ER stress but do not rule out MINPP1-driven ion chelation, nontranscriptional physiology, developmental defects, or edited-cell loss that would be absent from the recovered-nucleus DE endpoint. Weak target-RNA loss would not prove failed editing, and a zero DEG count here means only no predicted BH-corrected Wilcoxon hits in this one focal class.
