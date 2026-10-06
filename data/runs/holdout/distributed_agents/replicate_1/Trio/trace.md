# DEG-count prediction for `Trio`

## Question and endpoint

The requested output is a point prediction for the number of FDR-significant
measured genes after loss of `Trio` in `151 TH Prkcd Grin2c Glut` thalamic
glutamatergic neurons. The endpoint is the scalar `n_degs`, defined as the
count of measured genes with Benjamini-Hochberg-adjusted Wilcoxon `pvals_adj <
0.05` in the held-out perturbation. `Trio` was completely held out, so neither
its DEG count nor its expression signature was available in the declared
training files. The output must preserve the requested-target CSV order; there
was one requested target, `Trio`.

I treated the training count CSV as the directly observed endpoint for
non-held-out perturbations in the focal cell group, and the Parquet as direct
gene-level evidence for those same visible perturbations. The internal
same-experiment corpus was used only as packaged interpretation of the same
Perturb-seq experiment; it was not counted as independent replication. The
requested endpoint is directly observed for training perturbations and absent
for `Trio`, so the `Trio` prediction is a transfer from mechanistically related
training genes.

## Sources used

- `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`
  for the exact `151 TH Prkcd Grin2c Glut` endpoint of visible training
  perturbations.
- `training differential-expression dataset`
  for the per-measured-gene Wilcoxon statistics behind selected training
  perturbations.
- `perturbai-july-260713-sourceguard-1773-v1`, the run-selected internal
  same-experiment Findings corpus, for bounded summaries of visible
  `Kalrn`, `Rac1`, `Cdc42`, `Dock3`, `Tiam1`, `Arhgef9`, and `Pak1`
  perturbations.
- NCBI PubMed literature for external Trio biology:
  Pengelly et al. 2016, DOI `10.1136/jmedgenet-2016-103942`, PMID `27418539`;
  Katrancha et al. 2017, DOI `10.1093/hmg/ddx355`, PMID `28973398`;
  Backer et al. 2018, DOI `10.1242/dev.153692`, PMID `30177526`;
  Tao et al. 2019, DOI `10.1016/j.jgg.2019.02.003`, PMID `30850274`;
  Grubisha et al. 2022, DOI `10.1016/j.cellsig.2022.110416`, PMID `35872089`.

## Quantitative calibration

I first checked the training `n_degs` distribution because this is a scalar
count prediction, not a ranked-output task. Among 1,674 visible perturbations
in the focal class, 1,205 had `n_degs = 0`; the median was 0, the 75th
percentile was 1, the 90th percentile was 2, and the mean was pulled to 14.1 by
a small tail of very broad responses such as `Uba5`, `Tpr`, `Sin3a`, `Rnpc3`,
and `Zbtb7a`. I therefore did not borrow from the screen-wide mean. I treated
the local Rho-family and actin-regulatory neighborhood as the informative
quantitative stratum for `Trio`.

For the focal Parquet rows I filtered:

```text
group_name == "151 TH Prkcd Grin2c Glut"
gene_target in the selected Rho/Rac/GEF/GAP/WAVE/NMDAR analog set
pvals_adj < 0.05
```

Every selected visible perturbation had 17,259 measured-gene rows in the focal
class. The biologically closest or most useful comparators were:

| training perturbation | observed `n_degs` | focal FDR 0.05 expression-pattern evidence |
| --- | ---: | --- |
| `Kalrn` | 0 | 0 significant genes among 17,259 |
| `Rac1` | 0 | 0 significant genes among 17,259 |
| `Dock3` | 0 | 0 significant genes among 17,259 |
| `Tiam1` | 0 | 0 significant genes among 17,259 |
| `Arhgap32` | 0 | 0 significant genes among 17,259 |
| `Arhgap18` | 0 | 0 significant genes among 17,259 |
| `Limk1` | 0 | 0 significant genes among 17,259 |
| `Fgd4` | 0 | 0 significant genes among 17,259 |
| `Cyfip1` | 0 | 0 significant genes among 17,259 |
| `Ephb1` | 0 | 0 significant genes among 17,259 |
| `Ephb2` | 0 | 0 significant genes among 17,259 |
| `Pak2` | 0 | 0 significant genes among 17,259 |
| `Pak3` | 0 | 0 significant genes among 17,259 |
| `Cdc42` | 1 | the only significant gene was `Cdc42` itself, log2FC -0.593, adjusted p = 8.6e-5 |
| `Arhgef9` | 1 | the only significant gene was `Arhgef9` itself, log2FC -0.571, adjusted p = 3.7e-8 |
| `Pak1` | 1 | the only significant gene was `Pak1` itself, log2FC -0.599, adjusted p = 5.0e-8 |
| `Cyfip2` | 1 | the only significant gene was `Cyfip2` itself, log2FC -0.489, adjusted p = 4.4e-11 |
| `Grin1` | 89 | direct NMDA-receptor loss was detectable and induced downstream genes such as `Scg2`, `Stmn4`, `Kctd16`, and `Gpm6a` |
| `Grin2a` | 1 | self transcript only |
| `Grin2b` | 2 | self transcript plus `Pianp` |

`Kalrn` was the closest visible paralog-like prior because Trio and Kalirin are
dual Rac/Rho guanine-nucleotide exchange factors that impose local,
spatiotemporally constrained Rac1/RhoA control on neuronal structure
(Grubisha et al. 2022). `Rac1`, `Cdc42`, `Pak1-3`, `Limk1`, `Cyfip1/2`,
`Dock3`, `Tiam1`, `Arhgap32`, `Arhgap18`, `Fgd4`, `Ephb1`, and `Ephb2` tested
nearby Rac/Cdc42/actin, WAVE, PAK/LIMK, and synaptic upstream branches. Their
focal responses were null or self-transcript-only, which is stronger evidence
than generic family membership because it shows that the same assay did not
convert perturbation of this local cytoskeletal pathway into a multi-gene
nuclear RNA program. The `Grin1` counterexample was useful for specificity:
the focal Wilcoxon workflow could recover downstream activity-linked and
synaptic RNA responses when a channel component itself was perturbed, but the
downstream RhoGEFs did not phenocopy that response.

The same-experiment internal corpus supported the raw extraction. Its `Kalrn`
report stated that acute P16 `Kalrn` loss produced a completely FDR-flat
nuclear transcriptome in 22 neuronal groups and that represented
Rac1/PAK/LIMK/actin and PSD/NMDAR pathway genes were not transcriptionally
induced. Its `Rac1`, `Cdc42`, `Dock3`, and `Tiam1` reports likewise described
the canonical Rac/Cdc42/PAK/WAVE/GEF/GAP neighborhood as transcriptionally
buffered, with no meaningful screen-wide signed-score neighbors. I used those
records as the experiment authors' structured interpretation of the measured
training perturbations; no `Trio` same-experiment target record was available.

## Target-specific transfer to `Trio`

`Trio` is not a transcription factor or core RNA-processing/proteostasis gene
like the large-tail focal responders. It is a large neuronal Dbl-family RhoGEF:
its GEF1 domain activates Rac1/RhoG and, in some neuronal contexts, Cdc42, and
its GEF2 domain activates RhoA. External studies make the biological effect of
Trio loss plausible but place the proximal consequence at cytoskeletal and
axon/synapse signaling stages rather than at direct nuclear transcription:

- patient variants in the Rac-GEF domain reduce Rac1 activation and cause
  neurodevelopmental phenotypes (Pengelly et al. 2016);
- de novo and rare variants alter Trio GEF1 or GEF2 activity toward Rac1 or
  RhoA (Katrancha et al. 2017);
- Trio can mediate Slit2-dependent RhoA signaling needed for embryonic
  thalamocortical and telencephalic wiring (Backer et al. 2018);
- Trio-domain manipulations in cerebellar granule neurons impair F-actin
  rearrangement and axon outgrowth through Cdc42/Rac/Rho signaling rather than
  through a broad RNA-output mechanism (Tao et al. 2019).

The causal transfer model was therefore:

acute mosaic `Trio` CRISPR loss in postmitotic P16 neurons -> reduced local
Rac/Cdc42/RhoA exchange and altered growth-cone or synaptic actin signaling ->
possible changes in neurite, axon-branching, and spine morphology -> recovered
NeuN+ nuclei 3-4 weeks later -> Wilcoxon nuclear-RNA `n_degs`.

The direct molecular consequence matches `Kalrn`, `Dock3`, `Tiam1`, `Rac1`,
`Cdc42`, and `Pak` pathway perturbations well enough that their quiet focal
endpoint is the main quantitative evidence. The transfer is not exact:
`Trio` is more pleiotropic than `Kalrn`, has Rac/Rho domain structure, and is
central in embryonic wiring. Those differences could make it less buffered
than the visible single-node Rac-axis perturbations. Against that, the
experiment perturbed postmitotic juvenile neurons by sparse AAV CRISPR, not
embryonic progenitors, thalamocortical corridor cells, or dense germline
Trio-null tissue. The local actin/GTPase steps are also protein-activation and
localization events, while the requested endpoint is steady-state nuclear RNA
in surviving nuclei. Because the nearest visible perturbations were repeatedly
zero in this same endpoint and `Kalrn`, the closest broad dual-GEF comparator,
was exactly zero in the focal class and flat across the measured atlas, I
predicted no FDR 0.05 gene rather than assigning `Trio` a response from the
global upper tail.

Final point prediction: `Trio = 0`.

## Limits and uncertainty

This is an extrapolation for a held-out gene; no `Trio` expression signature
was present in the supplied inputs. `Kalrn` is the closest visible structural
analog but is not an obligate Trio complex member, and `Rac1`, `Cdc42`, `Pak`,
`Dock3`, and `Tiam1` are pathway neighbors rather than exact phenocopies. A
single significant self transcript in `Cdc42`, `Arhgef9`, or `Pak1` is not
evidence of a downstream program, and the held-out `Trio` self transcript
could in principle add one DEG if its edited transcript happened to drop
strongly enough. External Trio work is concentrated in embryonic migration,
axon wiring, cerebellar granule neurons, patient variants, or protein-level
GEF activity assays; those are mechanistic priors, not measurements of acute
sparse P16 `Trio` loss in `151 TH Prkcd Grin2c Glut` nuclei. The zero
prediction means only that no measured nuclear transcript is expected to pass
FDR 0.05 in this assay; it should not be read as evidence that Trio is
dispensable for neuronal morphology or synaptic function.
