# Nyx held-out prediction trace

## Question and interpretation

The manifest for this run contains one held-out perturbation, `Nyx`. I interpreted the task as predicting the integer number of genes in `151 TH Prkcd Grin2c Glut` cells that would have `pvals_adj < 0.05` after acute AAV-PHP.eB sparse CRISPR loss of `Nyx`, using only non-held-out signatures and DEG counts plus external biology.

The endpoint is an assay-specific response breadth, not an estimate of whether a gene is important in its native tissue. I therefore treated a zero prediction as "no measured nuclear RNA feature is expected to clear Wilcoxon BH FDR 0.05 in this focal non-retinal neuronal class", not as a claim that `Nyx` has no retinal phenotype.

## Sources used

Internal same-experiment sources:

- `[local file: 161_Nyx.csv]` for the exact requested target list and order.
- `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]` for observed focal DEG counts of the non-held-out targets.
- `[local file: training_de_all_cell_groups.parquet]` for the focal `scores`, `logfoldchanges`, and `pvals_adj` values of mechanistic comparator perturbations.
- Distributed Agents corpus MCP release `perturbai-july-260713-sourceguard-1773-v1` for curated Grm6/Gpr179/Gnb5/R7 and metabotropic-glutamate pathway interpretations. `Nyx` itself had no record in that release, so I did not use a precomputed Nyx neighborhood.
- Distributed Agents runtime `profile_compare`/`profile_cohort` over the focal `scores` vectors to quantify whether candidate analog signatures had shared positive or negative tails.

External mechanism sources from PubMed:

- Bech-Hansen et al. 2000, Nature Genetics, DOI `10.1038/81619`, PMID `11062471`: human `NYX` mutations cause X-linked complete congenital stationary night blindness, placing nyctalopin in the retinal ON pathway.
- Gregg et al. 2003, Investigative Ophthalmology & Visual Science, DOI `10.1167/iovs.02-0501`, PMID `12506099`: the mouse `nob` phenotype is caused by an `Nyx` deletion; `Nyx` expression is strongest in retina/inner nuclear layer.
- Gregg et al. 2007, Journal of Neurophysiology, DOI `10.1152/jn.00608.2007`, PMID `17881478`: dendritic-tip expression of nyctalopin in retinal depolarizing bipolar cells rescues the `Nyx` `nob` visual phenotype.
- Pearring et al. 2011, Journal of Neuroscience, DOI `10.1523/JNEUROSCI.1014-11.2011`, PMID `21734298`: nyctalopin is needed to localize TRPM1 to depolarizing bipolar-cell dendrites.
- Cao et al. 2011, Journal of Neuroscience, DOI `10.1523/JNEUROSCI.1682-11.2011`, PMID `21832182`: nyctalopin complexes with TRPM1 and interacts with mGluR6 in the mouse ON-bipolar postsynaptic compartment.
- Hasan et al. 2020, eNeuro, DOI `10.1523/ENEURO.0002-20.2020`, PMID `31959619`: LRIT3 is upstream of nyctalopin/TRPM1 expression in the depolarizing bipolar signalplex.
- Orhan et al. 2021, International Journal of Molecular Sciences, DOI `10.3390/ijms22094424`, PMID `33922602`: GPR179 deficiency removes GPR179 and RGS7/RGS11/GNB5 from ON-bipolar dendritic tips but preserves GRM6/LRIT3/TRPM1 localization, showing an adjacent signalplex branch.

## Focal training-set calculations

The focal count CSV has 1,674 non-held-out targets; 469 have a nonzero focal `n_degs`, the median is 0, the mean is 14.05, and the top hits are hundreds to thousands of DEGs. A target with a local response therefore should be visible in the focal count table, but a large part of the library is exactly zero in this cell class.

I filtered the parquet to `group_name == "151 TH Prkcd Grin2c Glut"` and queried pathway comparators. For each target below there were 17,259 focal gene tests, and recomputing `sum(pvals_adj < 0.05)` matched the supplied count CSV:

| training perturbation | focal `n_degs` | focal expression evidence |
| --- | ---: | --- |
| `Gpr179` | 0 | No FDR hits; best rows were `Arhgef17` and `Ufc1`, both `pvals_adj = 0.519`. `Nyx`, `Trpm1`, `Lrit3`, `Grm6`, `Gnao1`, `Gnb3`, `Gnb5`, `Gng13`, `Rgs6`, `Rgs7`, and `Rgs11` were all FDR 1.0. |
| `Grm6` | 0 | No FDR hits; every tested row had `pvals_adj = 1.0`. `Nyx`, `Trpm1`, `Lrit3`, `Gpr179`, `Gnb3`, `Gnb5`, `Gng13`, `Rgs7`, and `Rgs11` were all FDR 1.0. |
| `Gnb5` | 0 | The guide measurably lowered the self transcript, but even `Gnb5` itself stopped at `pvals_adj = 0.343`; no downstream genes passed FDR. |
| `Gnao1` | 1 | The only hit was the self transcript, `Gnao1` at `pvals_adj = 9.42e-07`; the ON-bipolar signalplex genes above remained FDR 1.0. |
| `Rgs6` | 0 | G protein/R7-adjacent counterexample with no focal FDR response. |
| `Gpr158` | 1 | `Gpr179` paralog/R7-adjacent counterexample with only its self transcript significant. |
| `Grm1`, `Grm5`, `Grm7`, `Grm8` | 1, 0, 1, 0 | Broader metabotropic glutamate receptor controls; effects were absent or singleton self-transcript changes rather than a common transcriptional module. |
| `Vsx1`, `Vsx2` | 0, 0 | Retinal and V2-lineage homeobox controls; they had no focal response, matching the expectation that this sampled postnatal brain assay does not engage retina-development programs. |
| `Trpm7` | 0 | A measured TRP-channel counterexample; not a mechanistic substitute for retinal TRPM1 but useful for rejecting a generic TRP perturbation response. |

The Distributed Agents runtime comparison among these 13 candidates found the same thing from the signed focal score vectors: the exact `Grm6`-`Gpr179` whole-profile cosine was only 0.0079 and their top 200 positive and top 200 negative score tails shared 5 genes apiece, with no significant positive or negative intersection. Thus the relevant evidence is shared flatness of appropriate pathway perturbations, not a hidden Nyx-like expression module.

## Distributed Agents corpus evidence

`Nyx` had no target context in the selected corpus. The corpus did contain curated same-experiment claims for the measured ON-bipolar pathway relatives:

- `Grm6:F002` and `Grm6:F004` report that represented mGluR-family and ON-bipolar signalplex comparators failed to phenocopy `Grm6`, and that canonical ON-bipolar readout transcripts including `Gnao1`, `Gnb3`, `Gnb5`, `Gng13`, `Gpr179`, `Lrit3`, `Nyx`, `Rgs7`, `Rgs11`, and `Trpm1` did not move after `Grm6` perturbation.
- `Gpr179:F002` and `Gpr179:F003` report that the canonical mGluR6/TRPM1/RGS-GNB5 signalplex stayed unchanged after `Gpr179` perturbation and that `Gpr158`, `Gnb5`, `Grm6`, and `Gnao1` were flat or nearly flat relatives rather than substitute brain modules.
- Corpus claims `claim:b94ae2a0ac15df4a5e20` and `claim:944ca6185dd70e5a895c` summarize the same pattern: GPR179/GRM6/GNB5/R7-adjacent perturbations in these postnatal brain neuronal nuclei were largely uncoupled from a broad basal RNA program.

## Target-specific prediction

### `Nyx`

Biology: `Nyx` encodes nyctalopin, a small leucine-rich repeat membrane protein best known from the retina. Loss of NYX causes complete congenital stationary night blindness in humans, and the mouse `nob` `Nyx` mutant loses ON-bipolar signaling with no electroretinogram b-wave. Mechanistically, the literature places nyctalopin at depolarizing bipolar-cell dendritic tips where it organizes or stabilizes the mGluR6/TRPM1 postsynaptic cascade. That effect is mainly protein localization and synaptic physiology in retinal ON bipolar cells, not a documented broad nuclear RNA state in juvenile forebrain/midbrain neurons.

Training analogs: the exact closest partners were partly unavailable as perturbation targets (`Trpm1`, `Lrit3`, `Rgs7`, `Rgs11` were readouts but not training perturbations), so the best measured analogs were `Grm6`, `Gpr179`, `Gnb5`, and `Gnao1`. `Grm6` and `Gpr179` are in the same retinal ON-bipolar signalplex as Nyx; `Gnb5` and `Gnao1` sit in coupled G-protein/R7 signaling. In the focal cell group these had 0, 0, 0, and 1 DEG, respectively, and the single `Gnao1` hit was just the target's own mRNA. The focal Grm6/Gpr179 signatures were not positively or negatively coherent despite both being pathway neighbors; their canonical readout rows, including `Nyx`, `Trpm1`, `Lrit3`, and `Rgs11`, were FDR 1.0.

Counterexamples: broader class-C/metabotropic glutamate receptors (`Grm1`, `Grm5`, `Grm7`, `Grm8`) had only 0 or 1 focal hits, the `Gpr179` paralog `Gpr158` was a singleton self-transcript hit, `Rgs6` was 0, and the retinal homeobox genes `Vsx1`/`Vsx2` were both 0. These counterexamples argue that the P16 sparse CRISPR postnatal brain assay is downstream of neither the retinal ON-bipolar signalplex nor retinal developmental programs in a way that produces constitutive DE in `151 TH Prkcd Grin2c Glut`.

Decision: I predict `Nyx` will be nonresponsive in the focal cell group, with zero genes passing BH FDR 0.05. This is driven mainly by direct same-experiment flatness of the appropriate Grm6/Gpr179/Gnb5/Gnao1 comparators, and secondarily by external knowledge that Nyx's canonical phenotype is a retinal ON-bipolar localization/ERG phenotype in a tissue not sampled here.

## Limits

- `Nyx` itself, `Trpm1`, and `Lrit3` were absent as training perturbations, so the prediction extrapolates from adjacent measured signalplex components rather than from a direct paralog or complex-member knockout with a broad signature.
- Retina was not sampled, and the endpoint is snRNA abundance in postnatal NeuN+ brain nuclei. The data cannot see nyctalopin-dependent TRPM1 dendritic-tip localization, ON-bipolar currents, or electroretinogram b-waves.
- The platform's average target-mRNA downregulation is modest and indel rates are not directly measured; weak target RNA movement is therefore not proof of editing failure.
- A rare, noncanonical `Nyx` function in the TH/Prkcd/Grin2c population would be missed by the external retinal literature and poorly constrained by the flat available analogs.
