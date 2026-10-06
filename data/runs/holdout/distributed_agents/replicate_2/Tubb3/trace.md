# Question

Predict the held-out `n_degs` for each requested perturbation in `151 TH Prkcd Grin2c Glut`, where `n_degs` is the count of measured genes with Benjamini-Hochberg-adjusted Wilcoxon `pvals_adj < 0.05` in the focal class. The manifest for this run contains one target:

```text
Tubb3
```

I treated target rows as part of the DEG count because the supplied training endpoint counts them: for example, in this focal group `Tubb4b` and `Tubb5` each have exactly one DEG and the only significant row is their own mRNA.

# Sources

Primary same-experiment measurements:

- `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`
- `[local file: training_de_all_cell_groups.parquet]`

Same-experiment interpretation layer:

- Distributed Agents corpus release `perturbai-july-260713-sourceguard-1773-v1`

External mechanism checks:

- NCBI PubMed
- PubMed 20074521, Tischfield et al. 2010, DOI `10.1016/j.cell.2009.12.011`: human TUBB3 missense variants perturb microtubule dynamics, kinesin interactions, and axon guidance.
- PubMed 30110642, Latremoliere et al. 2018, DOI `10.1016/j.celrep.2018.07.029`: complete mouse Tubb3 knockout is compatible with largely normal nervous-system formation and induces compensation by other beta-tubulin isotypes, with a specific defect in timely adult axon regeneration.
- PubMed 20406197, Tischfield and Engle 2010, DOI `10.1042/BSR20100025`: review supporting the idea that different alpha- and beta-tubulin isotypes have specialized nervous-system functions.
- PubMed 23246003, Breuss et al. 2012, DOI `10.1016/j.celrep.2012.11.017`: the beta-tubulin Tubb5 acts in embryonic neurogenesis/migration and is a useful developmental beta-tubulin comparator rather than a perfect postnatal loss-of-function analog.
- PubMed 31727855, Lin et al. 2019, DOI `10.1126/science.aaz4352`, and PubMed 37295431, Hopfler et al. 2023, DOI `10.1016/j.molcel.2023.05.020`: tubulin availability is coupled to tubulin mRNA stability by nascent-chain/TTC5-dependent autoregulation.

# Computation over the input dataset

I first read the held-out manifest and the training scalar table. The focal training distribution has 1674 targets; 1205 are zero, 363 are weak nonzero `1-9`, 63 are medium `10-99`, and only 43 have at least 100 DEGs. The median is 0 and the 90th percentile is 2, so a structural-gene prior alone should remain close to zero unless a close training perturbation has a clear observed response.

I used PyArrow dataset filters to avoid reading the 616M-row parquet into memory. The material query was:

```python
fil = (
    (pc.field("group_name") == "151 TH Prkcd Grin2c Glut")
    & pc.field("gene_target").isin(targets)
    & pc.field("names").isin(features)
)
```

with `targets` set to represented tubulin, MAP, stathmin, kinesin, dynamin, and dynactin perturbations, and `features` set to measured tubulin/MAP/stathmin transcripts. I also queried all significant focal rows for those targets.

The relevant focal `n_degs` from the scalar file were:

| training target | focal n_degs | interpretation |
| --- | ---: | --- |
| `Tuba1a` | 7 | self down plus a six-gene alpha/beta-tubulin paralog induction module |
| `Tuba4a` | 2 | mostly self down; one other thalamic hit |
| `Tubb4b` | 1 | self down only |
| `Tubb5` | 1 | self down only |
| `Stmn2` | 1 | self down only at FDR 0.05 in this group |
| `Map1b` | 1 | self down only |
| `Mapt` | 1 | self down only |
| `Map6` | 0 | flat |
| `Mapre2` | 1 | self down only |
| `Kif1a` | 1 | self down only |
| `Kif5a` | 1 | self down only |
| `Kif5c` | 1 | self down only |
| `Dnm1` | 1 | self down only |
| `Dctn1` | 75 | a broader dynactin/sterol response, mechanistically less direct |
| `Tbcd` | 12 | beta-tubulin folding cofactor with a small alpha-tubulin and thalamic adaptation signature |

For the three training tubulin subunits most comparable to `Tubb3`:

- `Tubb5`: `Tubb5` itself was lower, logFC `-1.4783`, FDR `7.71e-23`; no `Tubb3`, `Tubb2a`, `Tubb2b`, `Tubb4a`, `Tubb4b`, or alpha-tubulin row was significant.
- `Tubb4b`: `Tubb4b` itself was lower, logFC `-0.5966`, FDR `1.07e-07`; no measured beta- or alpha-tubulin paralog was significant.
- `Tuba4a`: `Tuba4a` itself was lower, logFC `-0.7095`, FDR `2.43e-06`; `Mast1` was the only other focal FDR 0.05 row.

`Tuba1a` was the important positive counterexample. In this same focal group, its self-row was lower, logFC `-0.9669`, FDR `2.78e-20`, and it induced `Tubb3`, `Tubb2a`, `Tuba4a`, `Tubb4a`, `Tubb4b`, and `Tubb5` with FDR from `6.37e-09` to `2.86e-04`. That proves the assay can detect tubulin-isotype RNA feedback, and also shows that the measured beta-tubulin perturbations did not phenocopy the major `Tuba1a` state.

I also ran `profile_compare` over a cytoskeleton cohort in the focal cell group. The whole-profile logFC correlations among the sparse tubulin/MAP perturbations were high, but the top-tail rows were dominated by extreme nonsignificant values for rarely expressed genes. I therefore used the exact FDR rows and named tubulin-gene submatrix above for quantitative calibration and treated the profile artifact only as a check that there was no hidden broad shared FDR module among the direct tubulin perturbations.

# Same-experiment corpus evidence

The Distributed Agents corpus had no held-out `Tubb3` target context, which is expected for this prediction task. It did have direct findings for the training neighbors:

- `Tuba1a`: the corpus reports that postnatal `Tuba1a` loss uniquely elicits a compensatory alpha/beta-tubulin paralog mRNA module among measured tubulin and microtubule-related perturbations in `052 Pvalb Gaba` and `151 TH Prkcd Grin2c Glut`.
- `Tubb5`: the corpus explicitly contrasts `Tuba1a` with beta-tubulins, stating that `Tubb5` and `Tubb4b` do not engage the same tubulin-paralog feedback even in the Pvalb and thalamic groups where `Tuba1a` does.
- `Tubb4b`: the corpus records zero non-self genes at FDR 0.10 across recovered neuronal groups and absence of the `Tuba1a`-like beta/alpha-tubulin replacement program.
- `Tuba4a`: the corpus records a near-null somatic response and notes that the alpha-tubulin paralog `Tuba1a`, not `Tuba4a`, is the one that triggers the multi-tubulin compensation module.
- `Stmn2`, `Map1b`, `Mapt`, `Map6`, `Mapre2`, and kinesin comparators are summarized as buffered or nonconvergent with direct tubulin-subunit perturbations. This bounds the prediction away from a generic "microtubule damage" module.
- `Dctn1` and `Tbcd` show that the focal thalamic class can produce larger cytoskeleton-related responses, but their biology is not a direct beta-tubulin loss: `Dctn1` is a dynein/dynactin transport perturbation with a sterol/lipid program, and `Tbcd` is a tubulin-folding cofactor with alpha-tubulin up-regulation plus a small thalamic adaptation module.

# Target-specific reasoning

## Tubb3

`Tubb3` encodes beta-III tubulin, a neuron-enriched beta-tubulin isotype. Human missense variants are well known to alter microtubule dynamics, kinesin interactions, and axon guidance rather than behaving as clean partial loss-of-function alleles (Tischfield et al. 2010; Tischfield and Engle 2010). Complete mouse `Tubb3` knockout can be buffered by up-regulation of remaining beta-tubulin isotypes and leaves development and baseline behavior surprisingly normal, with a clearer defect in the rate of adult peripheral axon regeneration (Latremoliere et al. 2018). Thus external biology supports `Tubb3` as a real neuronal microtubule gene, but not as a target expected to cause a large 3-4 week postnatal cell-body RNA stress signature when partially disrupted.

The best within-dataset analogs were the beta-tubulin knockouts `Tubb5` and `Tubb4b`. Both are structural beta-tubulin genes, both had detectable target-mRNA decreases in `151 TH Prkcd Grin2c Glut`, and both had exactly one FDR 0.05 focal DEG. Crucially, neither induced a compensatory beta/alpha-tubulin mRNA panel: all candidate tubulin paralog rows were nonsignificant with adjusted p-values equal to 1.0 or, for the strongest `Tubb5` response in `Tubb4b` cells, FDR `0.621`. This argues that beta-tubulin loss in this sparse postnatal assay is usually reported as a narrow target-transcript effect, not as a medium or strong module.

`Tuba1a` was the main counterexample rather than the main quantitative analog. It caused 7 focal DEGs, including up-regulation of `Tubb3`, `Tubb2a`, `Tuba4a`, `Tubb4a`, `Tubb4b`, and `Tubb5`, so the Tuba1a state proves that the focal thalamic neurons and Wilcoxon model can see tubulin-dosage feedback. However, the same corpus comparison and the direct parquet rows show that `Tuba4a`, `Tubb4b`, and `Tubb5` do not phenocopy this module. Because the Tuba1a response is isotype-specific in the training data, I did not transfer its count of 7 wholesale to `Tubb3`.

`Tuba4a`, `Map1b`, `Mapt`, `Mapre2`, `Map6`, `Stmn2`, `Kif1a`, `Kif5a`, `Kif5c`, and `Dnm1` are useful negative boundaries: most are self-only or flat in the focal class. `Dctn1` at 75 and `Tbcd` at 12 demonstrate that a microtubule-related gene can be nonzero beyond a self-row, but `Dctn1` changes dynein/dynactin transport and sterol signaling, and `Tbcd` perturbs tubulin folding, so they are mechanistically weaker for a direct `Tubb3` subunit loss than `Tubb5` and `Tubb4b`.

I therefore predict a weak nonzero result. `Tubb3` is well expressed enough in the focal group to be detected as an up-regulated gene after `Tuba1a` loss, so a CRISPR-induced decrease of its own mRNA is likely to cross FDR 0.05. The best beta-tubulin training analogs say that any downstream compensation should stay below threshold. Point prediction: 1 DEG.

# Limits and extrapolation

- `Tubb3` itself was held out completely and absent from the Distributed Agents same-experiment corpus, so this is a prediction by analogy rather than a retrieval of a measured `Tubb3` surface.
- The closest assayed beta-tubulins were `Tubb5` and `Tubb4b`, not `Tubb3`; beta-III tubulin is more neuron-specific, so it could have a distinct paralog-compensation pattern.
- The external complete-knockout mouse result may overstate compensation relative to sparse P16 AAV CRISPR, where only a subset of alleles and cells are edited.
- The endpoint is an assay- and power-dependent nuclear RNA count. A predicted count of 1 does not mean `TUBB3` protein, axonal microtubule dynamics, regeneration, or guidance are biologically unaffected.
- Target self-mRNA depletion is not a general editing-efficiency metric. I used it only to calibrate the scalar endpoint because the FDR 0.05 count explicitly includes measured target transcripts and close beta-tubulin training targets were self-only.
