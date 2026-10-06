# Uqcc2 held-out DEG-count prediction

## Question and resolved ambiguities

The requested endpoint is the integer `n_degs` for each target in `256_Uqcc2.csv`: the number of measured genes with Benjamini-Hochberg-adjusted Wilcoxon `pvals_adj < 0.05` in `151 TH Prkcd Grin2c Glut` nuclei after AAV CRISPR loss of function. The requested manifest contains one held-out target, `Uqcc2`; `Uqcc2` is absent from both the training DE parquet as a `gene_target` and the focal training count CSV, as expected.

I interpreted the endpoint as assay-calibrated response breadth, not as the severity of a constitutive null phenotype. Thus human mitochondrial disease and assembly-factor literature were used to choose the right training analogs, while the final magnitude was calibrated from focal-cell DEG counts in the supplied training set.

## Sources used

- `training_de_all_cell_groups.parquet`: focal-cell log-fold changes, adjusted p-values, and matched cell counts for mechanistic analogs.
- `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`: observed `n_degs` for all non-held-out focal perturbations.
- `256_Uqcc2.csv`: exact held-out target list and order.
- Distributed Agents corpus MCP, release `perturbai-july-260713-sourceguard-1773-v1`: `target_context("Uqcc2")` returned no target-scoped findings, no claims, and no explicit references, so no same-experiment corpus relationship was available for this target.
- Distributed Agents runtime profile comparison: signed focal log-fold-change profiles were compared for complex III and OXPHOS candidates using `gene_target` as the profiled entity, `names` as the feature, `logfoldchanges` as the value, `pvals_adj < 0.05` as the significance label, and `group_name == "151 TH Prkcd Grin2c Glut"` as the context.
- MitoCarta3.0 mitochondrial proteome and MitoPathway annotations (Rath et al. 2021, DOI: `10.1093/nar/gkaa1011`, PMID: `33174596`).
- UQCC/complex III literature:
  - Tucker et al. 2013, DOI: `10.1371/journal.pgen.1004034`, PMID: `24385928`: UQCC2 is a UQCC1-interacting complex III assembly factor required for normal cytochrome b biogenesis.
  - Wanschers et al. 2014, DOI: `10.1093/hmg/ddu357`, PMID: `25008109`: UQCC3 acts downstream of UQCC1/UQCC2 in complex III assembly and supports cytochrome b stability.
  - Feichtinger et al. 2017, DOI: `10.1155/2017/7202589`, PMID: `28804536`: biallelic UQCC2 mutations can produce severe combined respiratory-chain deficiency with complex I/III defects, consistent with loss of complex III destabilizing respiratory supercomplexes.
  - Liang et al. 2022, DOI: `10.1016/j.celrep.2022.111204`, PMID: `35977508`: mammalian UQCC1/2 act in a COMA complex in stepwise CIII/CYTB biogenesis.
  - Dennerlein et al. 2021, DOI: `10.7554/eLife.68213`, PMID: `34969438`: early complex III assembly factors interact with nascent cytochrome b near the mitochondrial ribosome.

## Computational calibration

1. Read the held-out manifest and confirmed it contains only `Uqcc2`.
2. Summarized the focal training-count CSV: 1,674 training perturbations, median `n_degs = 0`, 75th percentile `= 1`, 469 perturbations with any nonzero DEG count. This made the zero-vs-one boundary important.
3. Nominated mitochondrial analogs from complex III biology and intersected them with the training targets. The tightest UQCC partners `Uqcc1`, `Uqcc3`, `Bcs1l`, and `Lyrm7` were not in the training target universe, so the closest observed analogs were complex III structural targets and `Ttc19`.
4. Extracted exact focal DE rows for the nominated genes and counted `pvals_adj < 0.05` to verify the CSV counts and to see which gene(s) passed FDR.
5. Compared log-fold-change profiles for `Ttc19`, `Cyc1`, `Uqcrb`, `Uqcrc2`, `Uqcrfs1`, `Uqcrh`, `Uqcrq`, several complex I/IV controls, and mitochondrial remodeling controls. This showed that the complex III signatures had very few significant genes and no shared significant module; whole-profile correlations were broadly high even for weak unrelated OXPHOS profiles, so I used the profile comparison as shallow-response evidence rather than as a reason to inflate the count.

## Target-specific reasoning

### `Uqcc2`

**Biology.** UQCC2 is an inner-mitochondrial-membrane complex III assembly factor. The literature places it at the early cytochrome b biogenesis step with UQCC1, upstream of UQCC3 and before later complex III maturation. Human UQCC2 loss can produce respiratory-chain complex III deficiency and can secondarily reduce complex I through respiratory-supercomplex instability. That argues that Uqcc2 is a real OXPHOS target, not a passenger gene. However, the experimental system here is mosaic, postnatal, and acute with incomplete mRNA depletion, so severe germline mitochondrial disease is a weak guide to transcriptional breadth.

**Closest observed analogs in the training set.**

| training target | focal `n_degs` | focal expression evidence | why I used it |
| --- | ---: | --- | --- |
| `Ttc19` | 1 | the only significant gene was `Ttc19` itself, logFC -0.517, padj `1.42e-22`; 267 perturbed nuclei | a complex III assembly factor and the closest available assembly-factor analog, though it acts later/differently than UQCC2 |
| `Uqcrc2` | 1 | the only significant gene was `Uqcrc2` itself, logFC -0.576, padj `0.0030`; 142 perturbed nuclei | nuclear complex III core subunit |
| `Cyc1` | 1 | the only significant gene was `Cyc1` itself, logFC -0.739, padj `2.94e-15`; 221 perturbed nuclei | nuclear complex III catalytic subunit |
| `Uqcrb` | 0 | no FDR genes; own transcript logFC -0.118, padj 1; 127 perturbed nuclei | complex III subunit counterexample with no detected focal response |
| `Uqcrfs1` | 0 | no FDR genes; own transcript logFC -0.340, padj 0.199; 233 perturbed nuclei | Rieske iron-sulfur complex III subunit; important but still FDR-silent here |
| `Uqcrh` | 0 | no FDR genes; own row had padj 1; 152 perturbed nuclei | complex III hinge protein; counterexample for the broader complex |
| `Uqcrq` | 1 | one significant gene, `Gpr180`, padj 0.0429; `Uqcrq` itself was not significant; 345 perturbed nuclei | small complex III subunit, showing that occasional one-gene calls need not be a coherent stress program |
| `Cox5a` | 1 | only `Cox5a` itself passed FDR, logFC -1.231, padj `5.39e-21` | complex IV positive control for a well-detected OXPHOS self-hit that still lacks a broad transcriptome response |
| `Ndufa8`, `Ndufs4`, `Ndufs7`, `Ndufv1` | 0 each | no focal FDR genes | complex I counterexamples; respiratory-chain membership alone did not imply DEGs in this assay |
| `Opa1` | 37 | amino-acid/ISR-like genes such as `Asns`, `Mars1`, `Chac1`, and `Ddit3` were up, and `Opa1` itself was down | boundary example showing that some mitochondrial perturbations can trigger a broader stress state, but it is not what the complex III analogs did |

Across the UQCR/TTC19 analogs, the observed counts were `{0, 0, 0, 1, 1, 1, 1}`. The runtime profile comparison likewise found the nominated complex III genes in the `no_significant_features` or `1_to_9_significant_features` classes, with no shared significant feature intersections among the inspected complex III pairs. The strongest individual significant calls in `Ttc19`, `Uqcrc2`, `Cyc1`, and `Cox5a` were simply their own targeted transcripts. I therefore expect an `Uqcc2` knockout to be a one-gene or zero-gene event rather than an `Opa1`-like mitochondrial stress program.

I chose **1 DEG** rather than 0 because `Uqcc2` itself was a measurable feature in this focal cell group in all 1,674 non-held-out contrasts; its cross-contrast logFC standard deviation was similar to other detectable complex III genes, and it reached FDR in three unrelated training contrasts. That means a direct CRISPR effect on `Uqcc2` mRNA is plausibly detectable if the target had reasonable guide/cell coverage. The direct analog median was also 1 when restricted to the available complex III set. I did not add extra genes for a respiratory-chain transcriptional program because the in-dataset complex III perturbations overwhelmingly failed to induce one.

Prediction: `Uqcc2 -> 1`.

## Limits

- The strongest mechanistic partners for UQCC2, especially `Uqcc1`, `Uqcc3`, `Bcs1l`, and `Lyrm7`, were absent from the supplied training endpoint, so the prediction extrapolates from structural complex III subunits and `Ttc19`.
- The Distributed Agents same-experiment corpus had no `Uqcc2` coverage in this release.
- Profile similarities among the weak OXPHOS perturbations were dominated by very small and often non-significant log-fold changes; I did not treat those as evidence for a robust shared state.
- The exact `Uqcc2` guide performance and matched perturbed-cell count are hidden with the held-out profile. If the `Uqcc2` guides underperformed or if the target was poorly captured in those nuclei, the count could be 0; if early complex III assembly loss happened to exceed the observed UQCR/TTC19 analogs, the count could be a few genes. The training data make a broad response unlikely.
