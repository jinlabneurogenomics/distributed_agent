# Trace

## Question and resolved ambiguities

The held-out target list for this run contains one gene:

| target_name |
| --- |
| Psmc5 |

I interpreted the task as a point prediction of the number of genes with `pvals_adj < 0.05` in `151 TH Prkcd Grin2c Glut` after acute AAV-CRISPR loss of mouse `Psmc5`. `Psmc5` was absent from both supplied training inputs, so I did not try to recover a target-specific signature. I transferred from non-held-out perturbations in the focal cell type and used external biology only to decide which training perturbations were mechanistically close.

The endpoint is a thresholded, assay-powered DEG count rather than an effect size. A broad biological perturbation can therefore move from hundreds to fewer calls if the recovered perturbed-cell count is low.

## Sources used

- `training_de_all_cell_groups.parquet`, filtered to `group_name == "151 TH Prkcd Grin2c Glut"` for same-experiment log-fold changes and FDR calls.
- `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` for observed focal-cell `n_degs` in all 1,674 training perturbations.
- `188_Psmc5.csv` for the held-out target order.
- Distributed Agents corpus MCP, release `perturbai-july-260713-sourceguard-1773-v1`, especially `target_context`, `search_claims`, `get_finding`, and `resolve_evidence`. This corpus contained no `Psmc5` target node, but it did contain same-experiment findings for `Psmc1` and `Psmb4`.
- Distributed Agents runtime profile comparison over the focal-cell parquet profiles. I used log2 fold changes for 17,259 measured genes, `pvals_adj` for FDR-thresholded overlap, and the 1,674 focal training targets as the eligible universe.
- PubMed searches for 26S proteasome architecture, the NRF1/NFE2L1 proteasome recovery pathway, and PSMC5/RPT6 insufficiency.

External references that mattered:

- Bard et al. 2018, Annual Review of Biochemistry, DOI `10.1146/annurev-biochem-062917-011931`: review of 26S proteasome architecture and 19S ATPase-driven substrate processing.
- Forster et al. 2009, Biochemical and Biophysical Research Communications, DOI `10.1016/j.bbrc.2009.07.145`: 26S proteasome model placing the six AAA ATPases in the 19S base.
- Bar-Nun and Glickman 2011, Biochimica et Biophysica Acta, DOI `10.1016/j.bbamcr.2011.07.009`: review of proteasomal AAA ATPase structure and function.
- Reactome `R-HSA-9907900`, "Proteasome assembly", and UniProt Knowledgebase entries for `Psmc1` and `Psmb4`, used through the Distributed Agents corpus as curated support that `Psmc1` is a 19S ATPase and `Psmb4` a 20S beta-core subunit of the 26S proteasome.
- Radhakrishnan et al. 2010, Molecular Cell, PMID `20385086`: NRF1/NFE2L1 mediates proteasome-gene recovery after proteasome inhibition.
- Koizumi et al. 2016, eLife, DOI `10.7554/eLife.18357`: DDI2 cleaves and activates NRF1 after proteasome dysfunction.
- Hatanaka et al. 2023, Scientific Reports, DOI `10.1038/s41598-023-41492-9`: NRF1 can induce p62/SQSTM1 and GABARAPL1 to link proteasome impairment with aggrephagy.
- Yu et al. 2024, Human Molecular Genetics, DOI `10.1093/hmg/ddae085`: PSMC5 insufficiency and a P320R variant impair proteasome function and activate apoptosis.
- Kury et al. 2025, Nature Communications, DOI `10.1038/s41467-025-65556-8`: human PSMC5/RPT6 variants and model-system loss of PSMC5 impair proteasome activity and perturb protein aggregation, mitochondrial, lipid, immune, and synaptic/neurodevelopmental processes.

## Same-experiment computations

I first read the manifest and confirmed that `Psmc5` is the only requested target.

For the focal-cell training counts, I summarized the distribution:

- `n = 1674` training perturbations
- min `0`, median `0`, 75th percentile `1`
- 90th percentile `2`, 95th percentile `18`, 99th percentile about `436`
- max `2677`

Thus a count in the several-hundred range is an extreme, broad response in this assay.

I then filtered the parquet to `151 TH Prkcd Grin2c Glut` and counted `pvals_adj < 0.05` calls for the proteasome and proteostasis candidate set:

| target | focal `n_degs` | up | down | role in reasoning |
| --- | ---: | ---: | ---: | --- |
| `Psmc1` | 430 | 231 | 199 | primary same-19S-ATPase 26S proteasome analog |
| `Psmb4` | 742 | 357 | 385 | primary orthogonal 20S-core 26S proteasome analog |
| `Nrf1` | 138 | 23 | 115 | downstream proteasome-stress transcription factor; partial/indirect |
| `Ufc1` | 572 | 348 | 224 | UFMylation/proteostasis state; parallel, not a proteasome subunit |
| `Uba5` | 2677 | 1820 | 857 | broad UFMylation/proteostasis state; much larger than direct proteasome hits |
| `Tpr` | 1768 | 1315 | 453 | broad Tpr/nuclear pore-proteostasis state; not same machine |
| `Rab7` | 501 | 311 | 190 | endolysosomal/sterol stress state |
| `Gfpt1` | 311 | 142 | 169 | HBP/O-GlcNAc stress state |
| `Hsf1` | 6 | 0 | 6 | HSF/chaperone regulator; does not phenocopy proteasome damage |
| `Hspa5` | 5 | 4 | 1 | ER chaperone perturbation; mostly buffered here |
| `Vcp` | 2 | 1 | 1 | proteostasis regulator; mostly buffered here |

The profile comparison between `Psmc1` and `Psmb4` in the focal cells supported their use as the only direct quantitative anchors:

- 17,259 shared measured genes.
- Pearson `0.611`, Spearman `0.431`, cosine `0.671`.
- Of the FDR 0.05 genes, 88 were jointly up and 127 were jointly down, for 215 shared focal DEGs with zero significant sign conflicts.
- Topology over multiple tail scales made `Psmc1`/`Psmb4` a mutual neighbor in whole-profile Pearson, whole-profile cosine, and every positive/negative tail layer inspected.
- At the corpus' broader cross-cell, FDR 0.10 level, `Psmb4` and `Psmc1` agreed in sign for 5,107 of 5,113 shared significant gene-cell features; in `151 TH Prkcd Grin2c Glut`, the corpus recorded 347 same-direction overlaps at FDR 0.10.

I also checked specific proteotoxic-stress features in the focal parquet. Direct proteasome perturbations up-regulated proteasome or aggregate-clearance genes such as `Psmd1`, `Psmd4`, `Psmc3`, `Psmc6`, `Sqstm1`, and `Optn`, and ISR/apoptosis-risk genes including `Ddit3`, `Bax`, `Cdkn1a`, `Btg2`, `Mt2`, `Dnajb1`, and `Prdx1`. The same selected genes stayed FDR-flat after `Hsf1`, `Hspa5`, and `Nrf1` perturbation in this cell group, except for the target-specific `Nrf1` program around `Kifc2`, `Snhg11`, `Rsrp1`, `Cdc7`, and `Pigp`.

One useful negative computational result was that several high whole-profile neighbors of `Psmc1` among all 1,674 eligible training targets were not mechanistic proteasome perturbations and had no focal DEGs: `Npy2r`, `Trip11`, `Tfg`, `Sipa1l3`, and `Ptchd1` were all `0`. I therefore used the mechanistic same-complex hits and significant-gene overlap, not whole-vector proximity alone.

## Target-specific reasoning

### Psmc5

`Psmc5` encodes RPT6/PSMC5, one of the six AAA+ ATPases in the 19S regulatory-particle base of the 26S proteasome. Its most direct training analog is `Psmc1`, another 19S AAA ATPase; the best orthogonal analog is `Psmb4`, a 20S beta-core subunit. Those two training perturbations damage different physical subcomplexes of the same proteolytic machine and nevertheless converged strongly in this exact experiment. That convergence is the main reason for a nonzero prediction.

Primary analogs:

- `Psmc1`: `430` DEGs in `151 TH Prkcd Grin2c Glut`. The Distributed Agents corpus finding `Psmc1:F007` reported `Psmb4` as the only other assayed constitutive 26S proteasome subunit and as the single strong positive `Psmc1` signature neighbor. In the focal parquet, the `Psmc1` signature included up-regulation of proteasome and clearance/stress genes (`Psmd1`, `Psmd4`, `Psmc3`, `Psmc6`, `Sqstm1`, `Optn`, `Ddit3`, `Btg2`, `Mt2`, `Dnajb1`, `Prdx1`) and down-regulation of neuronal/synaptic markers such as `Kifc2`, `C1qtnf4`, `Gria2`, `Nrxn1`, and `Grin2c`.
- `Psmb4`: `742` DEGs in the same focal cells. The Distributed Agents corpus finding `Psmb4:F007` called `Psmc1` the top data-driven neighbor and noted that 20S beta-7 and 19S ATPase signatures agreed in sign for almost all shared significant features across measured groups. `Psmb4:F011` further resolved the response as the expected proteasome bounce-back plus p62/OPTN/lysosomal and pro-apoptotic RNA response. The focal `Psmb4` profile had the same-sign overlap with `Psmc1` described above.

Counterexamples and boundary analogs:

- `Nrf1`, the mouse homolog of NFE2L1/NRF1, produced a real but smaller focal response (`138` DEGs) centered on down-regulated `Snhg11`, `Rsrp1`, `Nrsn2`, `Kifc2`, `Haghl`, and `Cdc7`, with only 13 strict FDR overlaps with `Psmc1` and 23 with `Psmb4`. It is a downstream adaptive regulator for proteasome insufficiency, not a structural proteasome lesion, so I did not shrink `Psmc5` toward 138.
- `Uba5`, `Ufc1`, `Tpr`, `Rab7`, and `Gfpt1` all fall in broad proteostasis or endomembrane stress neighborhoods and share many same-direction genes with the proteasome hits, but their counts range from 311 to 2677 and their primary lesions are UFMylation, nuclear-pore/Tpr, endolysosomal, or hexosamine/O-GlcNAc biology rather than 26S proteasome structure.
- `Hsf1`, `Hspa5`, and `Vcp` show that generic chaperone or proteostasis labels are insufficient: they had 6, 5, and 2 focal DEGs even though cells were fully capable of mounting a large proteasome-failure program after `Psmc1` or `Psmb4`.

I therefore predicted a broad but not extreme response, near the middle of the two structural-proteasome anchors. I set `Psmc5` to `560`: above `Psmc1` because human/model evidence says PSMC5 itself is dosage-sensitive and can impair proteasome activity when insufficient, but below `Psmb4` because the two measured direct hits in this focal group spanned 430-742 and there is no held-out `Psmc5` sample-size or target-RNA information to justify pushing to the much larger UFMylation/Tpr range.

## Limits of the reasoning

- `Psmc5` had no node in the Distributed Agents corpus release, so there was no same-target within-experiment report; the prediction is an extrapolation from other 26S proteasome subunits plus public PSMC5/RPT6 biology.
- Only two direct structural 26S proteasome perturbations were in the training counts for this focal cell group. They disagreed in breadth by about 1.7-fold (`430` vs `742`), so the exact point estimate is less secure than the zero/nonzero decision.
- The external `Psmc5` literature used human variants, cell models, and Drosophila or neuronal-developmental assays; those are stronger perturbations and different contexts than the sparse P16-to-P37/44 mouse CRISPR snRNA-seq experiment here.
- I did not use `Nrf1`, `Hsf1`, `Hspa5`, or `Vcp` as primary anchors even though they are proteostasis-related, because the same dataset shows that loss of stress regulators or chaperones can be nearly flat and need not reproduce direct proteasome structural damage.
- The requested endpoint is FDR-thresholded and power-dependent. The focal matched perturbed-cell medians for the two anchors were 89 nuclei for `Psmc1` and 62 for `Psmb4`; the unknown recovered-cell count for held-out `Psmc5` could move the observed count substantially even if the biology were the same.
