# Reasoning trace

## Question and resolved ambiguities

I treated the task as a scalar held-out prediction for `Tubb3`: estimate the
integer number of genes that would have `pvals_adj < 0.05` after acute mosaic
CRISPR loss of `Tubb3` in `151 TH Prkcd Grin2c Glut` neurons.

Two details mattered for calibration:

- The endpoint is the observed Wilcoxon/BH DEG count in this exact cell group,
  not a general severity, viability, or disease score.
- The count includes every measured RNA feature that passes FDR, including the
  perturbed gene's own transcript if that self row is significant. In the
  training data, `Tubb5`, `Tubb4b`, `Map1b`, `Mapt`, `Mapre2`, `Kif1a`,
  `Kif5a`, and `Kif5c` each have `n_degs = 1` in the focal class because only
  their own target transcript passes the 0.05 threshold.

## Sources used

- `training_de_all_cell_groups.parquet`: per-gene Wilcoxon statistics and
  signed `logfoldchanges` for all non-held-out perturbations.
- `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`: exact training labels for
  focal-cell `n_degs`.
- `253_Tubb3.csv`: the one requested held-out target, `Tubb3`.
- Distributed Agents corpus release `perturbai-july-260713-sourceguard-1773-v1`,
  especially curated same-experiment findings for `Tuba1a`, `Tubb5`,
  `Tubb4b`, `Tuba4a`, and `Tbcd`.
- Run-local Distributed Agents `profile_compare`/`profile_inspect` over
  `151 TH Prkcd Grin2c Glut` Wilcoxon-score signatures.
- PubMed literature on TUBB3 and tubulin dosage:
  Latremoliere et al. 2018, DOI `10.1016/j.celrep.2018.07.029`, PMID
  `30110642`; Tischfield et al. 2010, DOI `10.1016/j.cell.2009.12.011`, PMID
  `20074521`; Puri et al. 2023, DOI `10.3389/fnins.2023.1226181`, PMID
  `37600020`; Lin et al. 2019, DOI `10.1126/science.aaz4352`, PMID
  `31727855`.

## What I computed from the training data

I used DuckDB to scan only rows where
`group_name = '151 TH Prkcd Grin2c Glut'`, then counted
`pvals_adj < 0.05` per cytoskeleton-related `gene_target` and inspected the
near-threshold rows for tubulin features. Separately, I used the run-local
profile tool on Wilcoxon `scores`, with the same focal-cell filter and
`pvals_adj < 0.05` as the significance mask, to compare:

`Tuba1a, Tuba4a, Tubb5, Tubb4b, Tbcd, Map1b, Mapt, Mapre2, Kif1a, Kif5a, Kif5c, Dctn1`.

The relevant focal counts were:

| training target | focal `n_degs` | relevant focal expression evidence |
|---|---:|---|
| `Tuba1a` | 7 | One strong self decrease plus six significant positive tubulin-paralog rows: `Tubb3`, `Tubb2a`, `Tuba4a`, `Tubb4a`, `Tubb4b`, `Tubb5`. The `Tubb3` row was the top positive feature: score 7.17, logFC 0.576, FDR 6.4e-09. |
| `Tuba4a` | 2 | Self decrease plus one non-self DEG, `Mast1`; no tubulin-paralog replacement module. |
| `Tubb5` | 1 | Only the `Tubb5` self row passed FDR; `Tubb3` itself had score 2.82 but FDR 1.0. |
| `Tubb4b` | 1 | Only the `Tubb4b` self row passed FDR; no significant `Tubb3`, `Tuba1a`, `Tubb2a`, or `Tubb5` response. |
| `Tbcd` | 12 | A small but real TBCD-cofactor state: `Tuba1a` and `Tuba1b` up, plus `Jun`, `Nfil3`, `Ypel4`, `Kctd16`, `Satb1`, `Mturn`, `Slc25a23` up and `Lrrc7`, `Ptprn2`, `Samd5` down. It was not phenocopied by direct tubulin perturbations. |
| `Dctn1` | 75 | A much broader sterol/lipid and neuronal response, useful as proof that cytoskeletal transport perturbations can be visible but not a beta-tubulin isotype analog. |
| `Map1b`, `Mapt`, `Mapre2`, `Kif1a`, `Kif5a`, `Kif5c` | 1 each | Each was self-only in the focal class. |
| `Kif2a`, `Map6`, `Nin`, `Ttll5` | 0 each | No focal DEG. |

The profile comparison supported the same separation. `Tuba1a` had nearly zero
whole-profile correlation with the focal beta-tubulin perturbations
(`Tuba1a` versus `Tubb5`: Pearson 0.012, cosine 0.010; `Tuba1a` versus
`Tubb4b`: Pearson 0.041, cosine 0.053), and `Tubb5` versus `Tubb4b` was also
weak (Pearson 0.031, cosine 0.030). None of the focal `Tuba1a`, `Tuba4a`,
`Tubb5`, `Tubb4b`, or `Tbcd` rows shared same-direction significant features
with the MAP/kinesin/Dctn1 peers inspected by the profile artifact; the only
significant `Tbcd`/`Dctn1` intersections were opposite-direction `Jun` and
`Kctd16` calls. Thus a held-out structural tubulin target should not be
assigned the `Tuba1a` seven-gene program, the `Tbcd` 12-gene thalamic module,
or the `Dctn1` 75-gene stress/sterol state just because it is in the
microtubule neighborhood.

## Same-experiment semantic evidence

The Distributed Agents corpus had no direct `Tubb3` finding because `Tubb3` was held out.
The nearby curated findings were consistent and useful as boundaries:

- `Tuba1a:F004` and the high-confidence Claim
  `claim:ca803b2ea88defcf5d1a` report that `Tuba1a`, but not the measured
  `Tuba4a`, `Tubb5`, or `Tubb4b` perturbations, elicits a compensatory
  multi-tubulin mRNA program in the same 052 Pvalb and 151 thalamic responder
  groups.
- `Tubb5:F003` states the mirror image: beta-tubulins `Tubb5` and `Tubb4b` did
  not elicit the alpha/beta tubulin feedback signature that was visible after
  `Tuba1a` loss.
- `Tubb4b:F001-F003` report that `Tubb4b` loss was essentially buffered and
  did not induce the beta/alpha-tubulin mRNA replacement program, while
  comparisons against `Tubb5`, `Tuba1a`, `Tuba4a`, `Stmn2`, `Mapt`, `Map1b`,
  `Map6`, `Mapre2`, `Kif5a`, `Kif5c`, and `Dctn1` had near-zero residual
  signature cosines.
- `Tuba4a:F001-F005` bound the alpha-tubulin side: `Tuba4a` was two-gene
  sparse and did not phenocopy `Tuba1a`, despite `Dctn1` showing that broader
  cytoskeletal responses were detectable.
- `Tbcd:F001-F007` showed that a beta-tubulin folding cofactor can induce a
  12-gene thalamic response with alpha-tubulin induction, but its module
  diverged from direct `Tuba1a` and `Tuba4a` perturbations.

Together these same-experiment annotations argue that the focal assay senses
selected tubulin-dosage states, but that beta-tubulin structural loss is
usually RNA-buffered over the P16-to-P37/44 CRISPR window.

## Target-specific reasoning for `Tubb3`

`Tubb3` encodes neuronal class-III beta tubulin. Human pathogenic TUBB3 biology
is dominated by heterozygous missense alleles that perturb microtubule dynamics,
kinesin interactions, axon growth, and axon guidance; a Tubb3 disease knock-in
mouse in Tischfield et al. 2010 had axon-guidance abnormalities, and Puri et
al. 2023 review the TUBB3/KIF21A guidance and migration literature. That is a
poor direct match to this screen, which creates acute sparse loss of function
in already postmitotic juvenile neurons and reads nuclear mRNA rather than
axon morphology or microtubule dynamics.

The most on-point loss-of-function evidence is Latremoliere et al. 2018:
germline `Tubb3-/-` mice were overtly viable and had no large baseline
neurobehavioral or neuropathological phenotype because the remaining
beta-tubulin isotypes were up-regulated enough to preserve total beta-tubulin,
although dorsal-root-ganglion axon regeneration was slower. That makes
compensation plausible, but the context differs sharply from a 3-4 week,
partial, mosaic postnatal perturbation. The focal Perturb-seq data show that
other directly perturbed beta-tubulins did not transcriptionally recruit such
compensation in `151 TH Prkcd Grin2c Glut`; `Tubb5` and `Tubb4b` each only
registered a self row, even with their own mRNAs strongly down at FDR.

I therefore used `Tubb5` and `Tubb4b`, not `Tuba1a`, as the primary quantitative
analogs for `Tubb3`. `Tuba1a` was the key positive counterexample: it proved
that the same focal group can up-regulate `Tubb3`, `Tubb2a`, `Tubb4a`,
`Tubb4b`, and `Tubb5` when the alpha-tubulin dosage state requires it, so the
absence of that program after `Tubb5`/`Tubb4b` is informative. `Tbcd` and
`Dctn1` were also counterexamples: they show visible cytoskeletal or folding
cofactor states but are mechanistically too far from a single beta-tubulin
isotype to set the count.

The zero/nonzero decision comes down to the target self-transcript. A complete
flat zero would be plausible if `Tubb3` behaved like the many unresponsive
cytoskeletal perturbations, but the structural tubulin targets represented in
training all gave strong focal self-RNA rows when their transcript was
detectably expressed (`Tuba1a`, `Tuba4a`, `Tubb5`, `Tubb4b`). Because `Tubb3`
is abundant in neurons and was itself a measurable FDR feature downstream of
`Tuba1a`, I predict that `Tubb3` CRISPR would at least cross FDR on its own
transcript. I did not add extra paralog or stress genes because the two beta
analogs did not.

Final point prediction for `Tubb3`: `1` DEG.

## Limits

- `Tubb3` itself was absent as a perturbation, so the prediction extrapolates
  from `Tubb5`/`Tubb4b` and assumes the four `Tubb3` guides would make a
  significant self-RNA row in this focal class.
- `Tubb3` is more neuron-enriched than `Tubb5` or `Tubb4b`; a small
  beta-isotype feedback response is possible despite being absent from those
  training perturbations.
- Germline `Tubb3-/-` compensation and human TUBB3 missense disease mechanisms
  are developmental, chronic, structural, or allele-specific contexts. They
  inform direction but cannot override the acute postnatal snRNA-seq
  calibration.
- The screen does not measure DNA indels, tubulin protein, microtubule
  polymerization, axon regeneration, or long-term survival. The prediction is
  only for BH-significant nuclear RNA features in recovered thalamic
  glutamatergic nuclei.
