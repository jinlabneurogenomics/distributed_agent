# Smpd3 DEG-count prediction

## Question and resolved details

The held-out manifest for this run contains one requested target, `Smpd3`. The endpoint to predict is the integer number of measured genes with `pvals_adj < 0.05` after that perturbation in `151 TH Prkcd Grin2c Glut` nuclei; the supplied focal-count CSV defines the same endpoint for all non-held-out training targets.

I treated a self-transcript call as part of `n_degs`, because the endpoint is "number of measured genes" and the training CSV includes examples where the sole DEG is the perturbed gene itself, such as `Sptlc2`, `St3gal5`, and `Psap` in the focal group. `Smpd3` itself is absent from both supplied training inputs and from the same-experiment Distributed Agents corpus, so this prediction extrapolates from other perturbations rather than from a direct neighbor row.

## Sources used

- `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`: observed `n_degs` for 1,674 non-held-out targets in the focal cell group.
- `[local file: training_de_all_cell_groups.parquet]`: per-gene Wilcoxon differential-expression rows. I filtered this table to `group_name == "151 TH Prkcd Grin2c Glut"` for lipid, sphingolipid, lysosomal, mTOR, and endolysosomal analogs, then counted `pvals_adj < 0.05` and inspected the significant rows to distinguish self-only calls from downstream programs.
- Distributed Agents corpus release `perturbai-july-260713-sourceguard-1773-v1`: I queried `Smpd3` directly, searched the corpus for sphingomyelin/sphingolipid/ceramide claims, and read target contexts for `Asah1`, `Cert1`, `Sphk1`, `Sptlc2`, `St3gal5`, and `Stard7`.
- PubMed literature on `Smpd3`/nSMase2 and ceramide-dependent trafficking:
  - Stoffel et al. 2005, DOI `10.1073/pnas.0406380102`, PMID `15764706`: `Smpd3` encodes neutral sphingomyelinase 2, hydrolyzes sphingomyelin to ceramide, is enriched in CNS neurons, and germline loss produces postnatal developmental/endocrine phenotypes.
  - Stoffel et al. 2018, DOI `10.1038/s41419-018-0560-7`, PMID `29725009`: Smpd3 deficiency in mouse brain perturbs neuronal Golgi vesicular protein transport and is associated with APP/Abeta/Tau proteostasis, unfolded-protein-response, apoptosis, and cognitive phenotypes.
  - Trajkovic et al. 2008, DOI `10.1126/science.1153124`, PMID `18309083`: ceramide produced by neutral sphingomyelinases can drive inward budding of exosome vesicles into multivesicular endosomes, motivating endosomal/exosome comparators but not proving an RNA-state phenocopy.
  - Qin et al. 2012, DOI `10.1074/jbc.M111.304857`, PMID `22383528`: nSMase2 deficiency in fibroblasts decreases ceramide and activates Akt/mTOR signaling, a reason to consider but not automatically accept `Tsc2`/`Depdc5`-like mTORC1/SREBP comparators.

## Training-set calibration

The focal training-count file has 1,674 targets. The response breadth distribution is heavily zero-inflated:

- median `n_degs`: `0`
- 75th percentile: `1`
- 90th percentile: `2`
- nonzero targets: `469 / 1674`
- maximum: `2677`

Thus the prior endpoint for an arbitrary held-out gene in this cell group is `0`, and even a real target-RNA depletion often yields only a one-gene count.

## Mechanistically relevant training perturbations

For all rows below, the counts are the observed `n_degs` in `151 TH Prkcd Grin2c Glut` at `pvals_adj < 0.05`.

| training perturbation | count | focal expression-pattern evidence | relevance to `Smpd3` |
| --- | ---: | --- | --- |
| `Asah1` | 0 | No gene reached FDR 0.05; the `Asah1` self row was not significant. The Distributed Agents corpus reports that `Asah1` loss was buffered at the snRNA-seq level across 21 recovered neuronal groups, with no downstream genes at FDR 0.10. | Acid ceramidase acts in lysosomal ceramide salvage, so it is a close biochemical counterpoint to a ceramide-generating sphingomyelinase. The flat result argues that perturbing neuronal ceramide turnover is often invisible to this nuclear RNA endpoint. |
| `Sptlc2` | 1 | The only focal FDR 0.05 row was `Sptlc2` itself, with log2FC `-0.685`; there was no downstream sphingolipid or stress program. The corpus specifically reports significant `Sptlc2` mRNA depletion in `151 TH Prkcd Grin2c Glut` without downstream FDR 0.10 genes. | `Sptlc2` is a de novo sphingolipid-synthesis subunit. It is the best represented loss of sphingolipid production, but the single self call shows the edited transcript can be detected while the pathway remains transcriptionally buffered. |
| `Sphk1` | 0 | No focal DEG. The corpus reports no FDR 0.10 downstream response after `Sphk1` in 23 assayed neuronal groups and absence of expected ceramide/S1P, apoptosis, ISR/UPR, NF-kappaB, and cytokine programs. | `Sphk1` consumes sphingosine to produce S1P downstream of ceramide. Its flatness makes a shared basal ceramide/S1P stress module unlikely. |
| `Cert1` | 0 | No focal DEG and a nonsignificant self-depletion row. The corpus reports no downstream FDR 0.10 response in any of 22 recovered neuronal groups and no convergence with `Sptlc2`, `Sphk1`, `Pi4kb`, or `Stard7`. | CERT transports ceramide from ER to Golgi. It tests whether disturbing subcellular ceramide delivery produces a contact-site or ER/Golgi lipid-stress RNA program; in this assay it did not. |
| `St3gal5` | 1 | The only focal FDR 0.05 row was `St3gal5` itself, with log2FC `-0.788`. The corpus describes the broader `St3gal5` surface as lacking canonical GM3/ganglioside, glucose/mitochondrial, immediate-early, UPR/ISR, or apoptosis programs. | `St3gal5` lies downstream of ceramide/glucosylceramide in ganglioside synthesis. Like `Sptlc2`, it supports self-only rather than broad downstream behavior. |
| `Stard7` | 0 | No focal DEG. Across all recovered groups the Distributed Agents corpus found an almost flat lipid-transfer surface, with only one FDR 0.10 responder outside the focal group and no broad ER-stress, ISR, redox, or mitochondrial program. | This is not a ceramide enzyme, but it is a useful lipid-transfer negative control and shows that perturbing lipid handling does not automatically cross an RNA-stress threshold. |
| `Psap` | 1 | The sole focal FDR 0.05 row was `Psap` itself. | PSAP supports lysosomal glycosphingolipid degradation, making it another ceramide/sphingolipid salvage comparator with no focal downstream program. |
| `Lamp2`, `Manba`, `Gnptab` | 0, 0, 0 | All were null in the focal count table. Corpus lysosomal-hydrolase/M6P claims report that represented lysosomal hydrolase and cargo perturbations were largely buffered rather than converging on a storage-stress, TFEB/MiT, UPR, or ISR program. | These are broader lysosomal counterexamples: a lipid-hydrolase or storage-related mechanism is not enough to imply a wide neuronal snRNA-seq response after sparse acute CRISPR. |
| `Rab7` | 501 | Broad focal response with lysosomal/V-ATPase and sterol genes such as `Atp6v1b2`, `Dpp7`, `Insig1`, `Lamp2`, `Msmo1`, and `Ldlr`. | Positive control showing late-endosomal/lysosomal compensation is detectable in this focal assay. I did not use it as a direct Smpd3 analog because corpus comparisons bound the `Rab7` state as selective and not a generic property of adjacent endolysosomal or Rab-related genes. |
| `Depdc5`, `Tsc2`, `Srebf2` | 13, 86, 7 | `Tsc2` and `Depdc5` induced overlapping sterol/endolysosomal genes in the focal group; `Srebf2` itself and sterol genes such as `Dhcr24`, `Insig1`, `Hmgcs1`, `Msmo1`, `Cyp51`, and `Sqle` were significant after `Srebf2`. | These were considered because external fibroblast work connects nSMase2 deficiency to Akt/mTOR. I treated them as upper-bound counterexamples: the training data show mTORC1/SREBP programs are visible when engaged, but directly represented sphingolipid perturbations did not collapse onto that state. |

The Distributed Agents corpus synthesized the directly relevant lipid results in claim `claim:4b050bd7d7e8716535f4`: represented sphingolipid-pathway and lipid-transfer perturbations in this postmitotic neuronal screen did not form a coherent shared multi-gene neuronal transcriptomic module. This claim included `Asah1`, `Cert1`, `Sphk1`, `Sptlc2`, `St3gal5`, and `Stard7` and is the main same-experiment reason to avoid projecting a broad Smpd3 response from lipid pathway membership alone.

## Target-specific prediction

`Smpd3` encodes neutral sphingomyelinase 2, a sphingomyelin-to-ceramide enzyme implicated in Golgi and multivesicular-body membrane remodeling. Germline or natural-loss `Smpd3` models can produce large organismal and neuronal phenotypes, including postnatal developmental defects and, in older knockout brain, protein-trafficking/proteostasis pathology. Those phenotypes make `Smpd3` a real neuronal lipid gene, not a safe-target-like locus.

However, the held-out readout is much narrower: sparse AAV CRISPR loss of function initiated at P16, measured only as nuclear RNA in surviving NeuN+ neurons at P37-P44. In the exact `151 TH Prkcd Grin2c Glut` training stratum, every close biochemical comparator for sphingolipid production, turnover, salvage, S1P production, and ceramide transfer had zero or one DEG, and the one-DEG cases were self-transcript depletion only. Broader lysosomal hydrolase/cargo genes were also flat. Stronger sterol/lysosomal responses were present after `Rab7`, `Tsc2`, `Depdc5`, and `Srebf2`, so a multi-gene compensation program should have been detectable if Smpd3 loss had driven one.

The zero/nonzero call therefore hinges mostly on whether edited `Smpd3` mRNA itself would be detected. `Sptlc2` and `St3gal5` show that a lipid enzyme can score as `1` through target depletion alone, whereas `Asah1`, `Cert1`, `Sphk1`, and `Stard7` stayed at `0` in the same endpoint. With no direct `Smpd` family perturbation represented and no same-experiment evidence that a neutral sphingomyelinase produces a downstream 151-cell RNA state, I predict no FDR 0.05 calls.

Predicted `n_degs` for `Smpd3`: `0`.

## Limits and extrapolation

- No `Smpd1`, `Smpd2`, `Smpd3`, or `Smpd4` perturbation was present in the focal training set, so the closest training genes are biochemical neighbors rather than neutral sphingomyelinase paralogs.
- The parquet contains snRNA differential-expression rows only. It cannot assay ceramide, sphingomyelin, exosome production, enzyme activity, Golgi morphology, or selective loss of successfully edited neurons.
- Germline `Smpd3` deficiency, the fragilitas ossium allele, and cell-line nSMase2 inhibition are stronger or differently timed than this sparse postnatal AAV CRISPR design.
- A one-gene self-transcript outcome is plausible if `Smpd3` is expressed and efficiently depleted in `151 TH Prkcd Grin2c Glut` neurons. The point estimate of `0` reflects the direct training analogs being downstream-null and the fact that comparable lipid genes often failed to make even their own transcript significant at FDR 0.05.
