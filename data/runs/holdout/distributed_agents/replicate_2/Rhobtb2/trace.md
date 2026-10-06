# Rhobtb2 held-out DEG-count prediction

## Question and resolved ambiguities

The task is to predict `n_degs` for the held-out perturbation `Rhobtb2` in `151 TH Prkcd Grin2c Glut` cells.

I interpreted `n_degs` exactly as in the training-count CSV: the number of measured genes, including the perturbed target transcript when it is significant, whose Benjamini-Hochberg-adjusted Wilcoxon `pvals_adj` is below 0.05 in the `151 TH Prkcd Grin2c Glut` comparison. The held-out `Rhobtb2` signature itself is absent from both supplied inputs, so all empirical evidence below comes from non-held-out targets.

## Sources used

- Supplied endpoint file: `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
- Supplied DE parquet: `[local file: training_de_all_cell_groups.parquet]`.
- Supplied held-out manifest: `[local file: 198_Rhobtb2.csv]`; it contains one target, `Rhobtb2`.
- Distributed Agents same-experiment semantic corpus, release `perturbai-july-260713-sourceguard-1773-v1`.
- Distributed Agents runtime `profile_compare` / `profile_inspect` for focal-cell logFC profile comparisons among represented Rho, BTB, KCTD, KLHL, and mTOR neighbors.
- External PubMed-indexed literature:
  - Wilkins, Ping, and Carpenter 2004, DOI `10.1101/gad.1177904`: RhoBTB2 binds CUL3 through a BTB domain and is itself degraded by a CUL3 ubiquitin-ligase complex.
  - Berthold et al. 2008, DOI `10.1016/j.yexcr.2008.09.005`: mammalian RhoBTB proteins interact with CUL3; RhoBTB2 and RhoBTB3 can dimerize; RhoBTB3 localizes to vesicles near microtubules.
  - Schenkova et al. 2012, DOI `10.1016/j.jmb.2012.06.016`: MUF1/LRRC41 interacts with RhoBTB proteins and is degraded by a RhoBTB3-CUL3 complex.
  - Belal et al. 2018, DOI `10.1002/humu.23550`: de novo RHOBTB2 variants cause epileptic encephalopathy and the tested mutants accumulate because CUL3-dependent degradation is impaired.
  - Langhammer et al. 2023, DOI `10.1016/j.gim.2023.100885`: RHOBTB2 BTB-domain missense variants and biallelic loss alleles give different neurodevelopmental spectra; complete loss can be pathogenic, but BTB missense variants cluster with severe DEE.
  - Langhammer et al. 2025, DOI `10.1093/hmg/ddae183`: RhoBTB overexpression in flies enriched ion-channel DE genes and interacted with the sodium-channel ortholog `paralytic`; human iPSC neurons with BTB-domain variants, not frameshift loss, had altered excitability.
  - Govek, Newey, and Van Aelst 2005, DOI `10.1101/gad.1256405`, plus Reactome `R-HSA-442586`, for the local Rho/Cdc42 actin-effector pathway used to choose `Cdc42`, `Rac1`, and Rho-axis comparators.
  - Lin et al. 2011, DOI `10.1083/jcb.201103015`, for the CUL3-KLHL20/PDZ-RhoGEF neurotrophin-neurite pathway used as an indirect CUL3-BTB/Rho comparator.

## Computational checks

1. Read the held-out CSV and confirmed that only `Rhobtb2` needed a prediction.
2. Read the 1674-row focal training-count CSV. The endpoint is very sparse in this cell class: 1205/1674 training perturbations had `n_degs=0`; the median was 0, the 75th percentile was 1, the 90th percentile was 2, and the mean of 14.05 was dominated by a small right tail such as `Uba5`, `Tpr`, `Sin3a`, `Rnpc3`, and `Zbtb7a`.
3. Searched the training targets for exact direct analogs and pathway genes.
   Direct `Rhobtb1`, `Rhobtb3`, `Cul3`, `Lrrc41`, `Tnfaip1`, `Arhgef11`, `Arhgef12`, `Kctd13`, `Rock1`, `Rock2`, `Rbx1`, and the cullins were not represented as perturbations.
4. Filtered the focal-cell rows in the DE parquet for represented candidates and listed their FDR<0.05 rows. This distinguished self-transcript-only counts from downstream RNA responses.
5. Ran a Distributed Agents runtime profile comparison over represented indirect neighbors:
   `Cdc42`, `Rac1`, `Rho`, `Arhgap32`, `Arhgap18`, `Arhgef9`, `Klhl20`, `Klhl7`, `Kctd1`, `Kctd8`, `Kctd16`, `Btbd9`, `Mtor`, `Rptor`, `Dock3`, and `Rasa2`.
   Whole-logFC correlations were not treated as mechanistic by themselves because almost all of these perturbations are near-null and their leading non-significant fold changes are often sparse-gene artifacts. The informative result was that the tiny FDR-supported responder sets of `Kctd1` and `Mtor` did not overlap with `Cdc42`, `Arhgef9`, `Klhl20`, `Rac1`, or `Rho`.
6. Queried `Rhobtb2` as a measured gene, rather than a target, in the focal training signatures. `Rhobtb2` was present in all 1674 focal non-held-out perturbations; only two strong, unrelated perturbations, `Cic` and `Elp1`, moved it at FDR<0.05. This argues that `Rhobtb2` mRNA is measurable but is not a recurrent activity-, stress-, Rho-, or BTB-state marker.

## Target-specific analogs and counterexamples

| Comparator | Focal `n_degs` | Focal FDR<0.05 rows | Relevance for `Rhobtb2` |
| --- | ---: | --- | --- |
| `Rhobtb1`, `Rhobtb3`, `Cul3` | not represented | not represented | These would have been the best direct paralog and scaffold controls for a RhoBTB-CUL3 hypothesis, but they were held out or absent from training. This is the main empirical gap. |
| `Cdc42` | 1 | `Cdc42` self only | A core Rho-family actin/spine GTPase. The Distributed Agents corpus reports no downstream Cdc42 response in any recovered neuronal class, despite significant `Cdc42` mRNA loss in 151 TH. Its same-experiment report also found zero FDR<0.10 calls among 43 actin, Rho-effector, and synaptic transcripts across Cdc42 tests. This is a strong counterexample to assuming that a postmitotic Rho GTPase perturbation must create a nuclear RNA footprint. |
| `Rac1`, `Rho` | 0, 0 | none | Represented Rho-family comparators with no focal FDR<0.05 genes. They are broader and less specific than `Rhobtb2`, but they bound the actin/GTPase branch as transcriptionally quiet. |
| `Arhgap18`, `Arhgap32`, `Dock3`, `Rasa2` | 0, 0, 0, 0 | none | Rho/Rac regulatory neighbors. They were all focal-null, supporting the Distributed Agents Cdc42 finding that represented Rho/Rac/Cdc42-axis relatives did not form a shared detectable module. |
| `Arhgef9` | 1 | `Arhgef9` self only | Collybistin is a Cdc42-directed RhoGEF at inhibitory synapses. It is not a RhoBTB paralog, but it tests an acute postnatal RhoGEF/synaptic disease gene with an mTORC1 literature connection. The same-experiment corpus reports a pan-measured downstream-null Arhgef9 surface and no FDR-supported Mtor-like RNA module. |
| `Klhl20`, `Klhl7`, `Btbd9` | 0, 0, 0 | none | BTB/Kelch or BTB-containing proteins, and `Klhl20` is a CUL3 adaptor that targets PDZ-RhoGEF in neurite outgrowth. The direct focal nulls and the Distributed Agents `Klhl20` report, which found only isolated non-focal singleton genes and no canonical Rho/autophagy/interferon module, make a broad basal CUL3-BTB adaptor response unlikely. |
| `Kctd1`, `Kctd8`, `Kctd16` | 2, 0, 0 | `Resp18` up and `Cluap1` down only for `Kctd1` | These are BTB/KCTD relatives, not RhoBTB proteins. `Kctd1` shows that a BTB-family target can give a tiny real two-gene 151 response, but represented KCTD family members did not phenocopy it. This supports, at most, a possible one- or two-gene idiosyncratic response, not a broad RhoBTB module. |
| `Mtor`, `Rptor` | 2, 0 | `Mtor`: `Rims3` up and `Tmed8` down | mTOR is an indirect counterexample because RHOBTB2 disease biology has been discussed beside proteostasis/excitability, and another RhoGEF, `Arhgef9`, has a reported mTORC1 link. The represented mTOR kinase loss had only two focal FDR<0.05 rows in this endpoint, while `Rptor` was null. |
| `Scn1a`, `Scn2a`, `Scn8a`, `Kcnq2`, `Kcnq3` | 1 each | self transcript only in 151 | These are not RhoBTB analogs. They bound the ion-channel interpretation suggested by the RHOBTB2 overexpression work: even direct sodium and Kv7 channel perturbations were self-only in the focal thalamic cells, so an upstream RhoBTB2 loss is not expected to phenocopy a large channelopathy-like nuclear program. |
| `Cacna1g`, `Atp1a3` | 12, 80 | multi-gene focal channel/ion-pump responses | These are positive controls showing that 151 TH cells can mount excitability-linked RNA states when a direct regulator is hit hard. They are mechanistic counterexamples, not positive analogs: `Cacna1g` and `Atp1a3` are primary ion transporters, whereas RhoBTB2 is a CUL3/Rho-family adaptor with largely unknown neuronal substrates. |

## Biological rationale for `Rhobtb2`

RhoBTB2 is an atypical Rho GTPase with BTB domains that couple it to CUL3 complexes; CUL3 can also ubiquitinate RhoBTB2 itself (Wilkins, Ping, and Carpenter 2004), and RhoBTB proteins share CUL3 binding and dimerization behavior (Berthold et al. 2008). That makes `Cul3`, `Rhobtb1`, and `Rhobtb3` the obvious same-complex/paralog comparators, but none was directly assayed as a perturbation in the non-held-out training set.

The best represented local biology was therefore indirect. The Cdc42/Rac/Rho and ArhGEF/GAP comparators tested whether an atypical Rho-family loss would project onto a postmitotic actin/spine or synaptic nuclear program. In this same experiment, that neighborhood was essentially silent in the focal cell class: `Rac1`, `Rho`, `Arhgap18`, `Arhgap32`, `Dock3`, and `Rasa2` had zero focal DEGs, while `Cdc42` and `Arhgef9` had only their own transcripts below FDR 0.05. Distributed Agents corpus reports for `Cdc42` and `Arhgef9` independently reached the same conclusion at a looser FDR<0.10 threshold across all recovered cell groups.

Other BTB/CUL3-adaptor comparators were also weak. `Klhl20` is a useful indirect CUL3 adaptor because CUL3-KLHL20 can ubiquitinate ARHGEF11/PDZ-RhoGEF in cultured cortical and hippocampal neurons to regulate neurotrophin-induced neurite outgrowth (Lin et al. 2011), but `Klhl20` itself had zero focal DEGs and no canonical Rho/autophagy program in the same-experiment corpus. `Kctd1` gave the strongest BTB-family focal response among the represented candidates, but even that was two genes, `Resp18` and `Cluap1`, and the KCTD family members `Kctd8` and `Kctd16` were null.

External RHOBTB2 disease evidence raised the prior for neuronal relevance but did not argue for a large acute loss-of-function snRNA footprint in these P37-44 thalamic neurons. The severe RHOBTB2 developmental and epileptic encephalopathy alleles first described by Belal et al. are heterozygous missense variants with impaired CUL3-dependent degradation and increased mutant protein abundance, not simple heterozygous loss. Langhammer et al. 2023 expanded the genotype spectrum and found that biallelic splice/truncating alleles can be pathogenic, but BTB-domain missense variants and complete loss had different functional consequences. Most importantly for direction, Langhammer et al. 2025 found ion-channel RNA enrichment after RhoBTB overexpression in Drosophila and altered excitability in human iPSC neurons with BTB-domain variants, but not with homozygous frameshift loss. The present assay is partial CRISPR loss of function, so it is much closer to a reduced-function allele than to the stabilizing BTB missense or overexpression states.

I therefore predicted no downstream FDR<0.05 genes for `Rhobtb2`. I also predicted that the self transcript would not be enough to make the count one. `Rhobtb2` is measurable in 151 TH cells, but in the training signatures its expression was a rare downstream event, FDR<0.05 only after the strong broad perturbations `Cic` and `Elp1`. Without guide-position, indel, or raw expression data, self-knockdown is uncertain; I treated the low, non-recurrent `Rhobtb2` mRNA behavior and the near-null indirect neighborhood as favoring an all-zero endpoint.

## Final point prediction

`Rhobtb2`: 0 DEGs.

## Limits and extrapolation

- No direct RhoBTB paralog, `Cul3`, or RhoBTB-CUL3 substrate perturbation was present in the training target table. The prediction is therefore extrapolated from indirect Rho-family and BTB/CUL3-adaptor controls.
- The assay does not measure RhoBTB2 protein, CUL3 substrate stability, ubiquitination, vesicle traffic, cytoskeletal morphology, ion-channel currents, seizures, survival, or non-neuronal phenotypes.
- Stabilizing human RHOBTB2 BTB-domain variants and Drosophila overexpression are mechanistically different from sparse CRISPR loss of function. If the held-out guides unexpectedly produce a transcript-depleting self row, the true endpoint could be `1` even with no downstream program.
- Whole-logFC similarities among near-null perturbations can be numerically high for reasons unrelated to biology; I used Distributed Agents profile comparisons mainly to check FDR-supported overlap and did not average candidates by correlation.
