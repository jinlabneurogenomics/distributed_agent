# Opn1mw prediction trace

## Question and resolved ambiguities

I interpreted the requested endpoint as the integer number of genes in `151 TH
Prkcd Grin2c Glut` cells with `pvals_adj < 0.05` after acute mosaic CRISPR
loss of the held-out target, using the same Wilcoxon/Benjamini-Hochberg
analysis as the supplied training file. The requested-target manifest contains
one held-out target, `Opn1mw`. DuckDB confirmed that `Opn1mw` has zero rows as a
`gene_target` in `training_de_all_cell_groups.parquet`, and `rg` found no
`Opn1mw` endpoint row in
`151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.

I treated zero as a prediction that no measured focal-cell transcript would pass
FDR 0.05, not as a claim that the AAV/CRISPR machinery cannot edit the locus.
For an opsin, the more relevant issue is whether editing a retinal cone
photopigment gene should perturb the transcriptome of the profiled postnatal
brain glutamatergic neurons.

## Sources used

- Input endpoint table:
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`
- Input differential-expression parquet:
  `[local file: training_de_all_cell_groups.parquet]`
- Requested-target manifest:
  `[local file: 163_Opn1mw.csv]`
- Distributed Agents same-experiment corpus release
  `perturbai-july-260713-sourceguard-1773-v1`
- Distributed Agents runtime profile comparison over the focal parquet rows, written to
  `opn1mw_retinal_analogs_profile_compare.json` and inspected through
  `opn1mw_retinal_analogs_profile_inspect.json`
- PubMed literature on cone opsin patterning and Opn1mw knockout phenotypes

External citations:

- Roberts MR, Srinivas M, Forrest D, Morreale de Escobar G, Reh TA. 2006.
  DOI `10.1073/pnas.0509981103`, PMID `16606843`.
- Satoh S, Tang K, Iida A, Inoue M, Kodama T, Tsai SY, Tsai MJ, Furuta Y,
  Watanabe S. 2009. DOI `10.1523/JNEUROSCI.0951-09.2009`, PMID `19812316`.
- Ji S, Mao X, Zhang Y, Ye L, Dai J. 2021. DOI
  `10.1016/j.exer.2021.108669`, PMID `34126082`.
- Deng WT, Li J, Zhu P, Chiodo VA, Smith WC, Freedman B, Baehr W, Pang J,
  Hauswirth WW. 2018. PMID `29386880`.
- Deng WT, Li J, Zhu P, Freedman B, Smith WC, Baehr W, Hauswirth WW. 2019.
  DOI `10.1167/iovs.19-27079`, PMID `31469404`.
- Ma X, Sechrest ER, Fajardo D, Zhu P, Dyka F, Wang Y, Lobanova E, Boye SE,
  Baehr W, Deng WT. 2022. DOI `10.1089/hum.2021.298`, PMID `35272502`.
- Corbo JC, Lawrence KA, Karlstetter M, Myers CA, Abdelaziz M, Dirkes W,
  Weigelt K, Seifert M, Benes V, Fritsche LG, Weber BHF, Langmann T. 2010.
  DOI `10.1101/gr.109405.110`.
- Peng GH, Ahmad O, Ahmad F, Liu J, Chen S. 2005. DOI
  `10.1093/hmg/ddi070`, PMID `15689355`.

## Computational checks

The focal training endpoint contains 1,674 non-held-out perturbations; 1,205 of
them, 72%, have `n_degs = 0`. The median is 0, the 75th percentile is 1, the
90th percentile is 2, the 95th percentile is 18, and the maximum is 2,677.
Thus most perturbations are silent in this cell group and broad DEG responses
are a small tail.

I filtered the focal DEG-count CSV for photoreceptor and retinal-lineage
training targets chosen from external biology and same-experiment corpus
findings. All directly relevant targets were zero in `151 TH Prkcd Grin2c
Glut`:

| training perturbation | focal `n_degs` | relevance to `Opn1mw` |
| --- | ---: | --- |
| `Opn1sw` | 0 | short-wave cone opsin; closest represented cone-opsin paralog |
| `Rho` | 0 | rod opsin; photoreceptor GPCR counterexample |
| `Crx` | 0 | photoreceptor transcription factor upstream of opsin programs |
| `Nr2e3` | 0 | photoreceptor nuclear receptor that cooperates with Crx and modulates rod/cone genes |
| `Thrb` | 0 | thyroid-hormone receptor needed for retinal M-opsin induction/S-opsin repression |
| `Rxrg` | 0 | cone subtype-patterning receptor included in the Opn1sw corpus comparison |
| `Gucy2e` | 0 | photoreceptor cGMP-recovery enzyme |
| `Spata7` | 0 | photoreceptor cilium/trafficking disease gene |
| `Rpgr` | 0 | photoreceptor ciliary disease gene |
| `Rpgrip1l` | 0 | ciliary RPGR-interacting gene |
| `Gpr179` | 0 | retinal ON-bipolar signaling gene; eye-specific sensory comparator |
| `Otx2` | 0 | retinal and neural developmental transcription factor |
| `Pax6` | 0 | broad eye/forebrain developmental transcription factor |
| `Vsx2` | 0 | retinal progenitor/bipolar-cell transcription factor |

I also queried the parquet for the eight closest focal analogs
`Opn1sw`, `Rho`, `Crx`, `Nr2e3`, `Gpr179`, `Otx2`, `Pax6`, and `Vsx2` in
`151 TH Prkcd Grin2c Glut`. Each had 17,259 measured rows and zero genes with
`pvals_adj < 0.05`; their minimum adjusted p values were:

| target | min focal `pvals_adj` |
| --- | ---: |
| `Gpr179` | 0.5193 |
| `Rho` | 0.6607 |
| `Nr2e3` | 0.8300 |
| `Otx2` | 0.8849 |
| `Crx` | 1.0000 |
| `Opn1sw` | 1.0000 |
| `Pax6` | 1.0000 |
| `Vsx2` | 1.0000 |

The Distributed Agents runtime profile comparison over those eight focal signatures
classified all eight as `no_significant_features`. This was not a case of
several near-threshold genes: for the closest analog, `Opn1sw`, even the
largest apparent positive and negative log-fold changes had adjusted p values
of 1.0 and inconsistent directions across the other retinal comparators.

## Same-experiment corpus evidence

The Distributed Agents same-experiment corpus contained no `Opn1mw` first-hop
neighborhood, as expected for a held-out target. It did contain direct findings
for represented photoreceptor targets:

- `Opn1sw:F003`, a `pathway_uncoupling` finding, reported that the obvious
  retinal module comparators `Rho`, `Crx`, `Nr2e3`, `Rxrg`, and `Thrb` were
  flat or nearly flat in matched postnatal brain-neuron groups and did not
  reveal a hidden photoreceptor-like state.
- `Opn1sw:E026` explicitly included `Opn1mw` among canonical cone/rod
  phototransduction and retinal transcription-factor genes that were not
  transcriptionally mobilized by `Opn1sw` perturbation in measured brain-neuron
  surfaces; listed genes present as Opn1sw DE rows had minimum FDR 1.0 across
  recovered groups.
- `Rho:F003` reported a shared flat retinal axis: `Gucy2e`, `Spata7`, `Crx`,
  `Nr2e3`, `Opn1sw`, `Rpgr`, and `Rpgrip1l` also failed to produce FDR<0.10
  signatures in Rho-matched brain groups.
- The same corpus had a moderate-confidence claim that represented
  photoreceptor-lineage perturbations fail to produce a shared
  photoreceptor-like transcriptional program in the assayed postnatal
  brain-neuron groups.

These corpus findings were useful because they asked a version of the same
question across all matched brain groups, not only in the one focal group.

## Target-specific biological reasoning

`Opn1mw` encodes the mouse medium-wave cone opsin, the green-light M-opsin
photopigment. In the retina, M-opsin and the short-wave cone opsin are
expressed in opposing dorsal/ventral cone gradients, with M-opsin patterning
regulated by thyroid hormone signaling and COUP-TF nuclear receptors
(Roberts et al. 2006; Satoh et al. 2009). Germline `Opn1mw` loss affects
M-cone photoreceptor outer segments and M-cone function, and AAV re-expression
of L- or M-opsin can rescue cone structure/function in `Opn1mw` mutant models
(Deng et al. 2018; Deng et al. 2019; Ma et al. 2022). Ji et al. 2021 also
studied `Opn1mw` null mice as M-opsin-deficient retinal models.

Those effects are retina- and cone-specific. The experiment profiled
NeuN-enriched postnatal brain nuclei, not retina, and the focal cell group is a
brain glutamatergic population. Effective editing of `Opn1mw` DNA in such cells
should not remove an active M-opsin phototransduction component, an outer
segment structural protein, or a retinal developmental regulator.

The most direct within-dataset analog is `Opn1sw`, the S-opsin paralog.
`Opn1sw` perturbation had:

- observed focal `n_degs = 0`
- 17,259 measured focal DE rows
- zero BH-significant genes
- minimum focal adjusted p value `1.0`
- same-experiment corpus evidence rejecting a hidden photoreceptor module with
  `Rho`, `Crx`, `Nr2e3`, `Rxrg`, and `Thrb`

`Rho` is a useful counterexample because rod rhodopsin is a photopigment GPCR
with strong germline retinal phenotypes, but it also had `n_degs = 0` in this
brain cell group. `Crx`, `Nr2e3`, `Thrb`, and `Rxrg` are upstream or
developmental retinal transcriptional regulators rather than opsin paralogs;
they are imperfect molecular analogs, but if the assay had been picking up a
cryptic retinal-lineage transcriptional state, these targets should have been
more likely than `Opn1mw` to expose it. They were all zero in the focal endpoint.

Putting those observations together, I predict no BH-significant downstream
genes for acute `Opn1mw` loss in `151 TH Prkcd Grin2c Glut`.

## Prediction

| target_name | predicted_n_degs |
| --- | ---: |
| `Opn1mw` | 0 |

## Limits

The prediction is an extrapolation because the actual `Opn1mw` DEG count and
signature were completely held out. None of the within-dataset comparators is a
perfect biochemical substitute for M-opsin in cones: `Opn1sw` is a cone opsin
paralog but has a different spectral and retinal-gradient identity; `Rho` is a
rod opsin; `Crx`, `Nr2e3`, `Thrb`, `Rxrg`, `Otx2`, `Pax6`, and `Vsx2` are
regulators with developmental functions outside phototransduction. The assay is
also a sparse postnatal brain CRISPR screen with modest average mRNA
downregulation, so it would miss retinal degeneration, cone outer-segment
defects, and non-cell-autonomous visual-system consequences that arise in
germline or retinal Opn1mw models. Those caveats affect biological importance,
but they do not supply a mechanism for a nonzero focal `TH Prkcd Grin2c Glut`
DEG count in this dataset.
