# DEG-count prediction trace

## Question and endpoint

The requested held-out perturbation list contains one mouse target, `Cacng8`.
The quantity to predict is `n_degs`, the number of genes with
Benjamini-Hochberg-adjusted Wilcoxon `pvals_adj < 0.05` in recovered
`151 TH Prkcd Grin2c Glut` nuclei after P16 sparse AAV-CRISPR loss of the
target and 3-4 weeks of postnatal propagation.

I treated the focal training count CSV as the direct endpoint for the 1,674
non-held-out perturbations. The all-cell differential-expression Parquet is
direct expression-pattern evidence for those same non-held-out perturbations.
The requested `Cacng8` endpoint and its own DE vector are absent by
construction: a direct Parquet query found 0 rows with `gene_target = 'Cacng8'`.
`Cacng8` remains a measured RNA for other perturbations, so its absence is only
as the held-out intervention.

## Sources

- Declared training endpoint:
  `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
- Declared differential-expression dataset:
  `training differential-expression dataset`.
- Requested held-out list:
  `single-target request for Cacng8`.
- Run-local measurement registry and dataset portrait, used to confirm that
  the Parquet measures recovered-nucleus relative expression and not editing
  efficiency, viability, guide-exposure denominators, or absolute RNA.
- The internal same-experiment corpus, `PerturbAI July 260713
  sourceguard-1773 v1`, queried through `corpus.findings`. This corpus is an
  interpreted representation of the same Perturb-seq experiment, not
  independent replication.
- External literature from PubMed:
  - Tomita et al. 2003, DOI `10.1083/jcb.200212116`, PMID `12771129`,
    defining stargazin/gamma-2, gamma-3, gamma-4, and gamma-8 as classical
    transmembrane AMPA receptor regulatory proteins that mediate AMPAR surface
    expression.
  - Nicoll, Tomita and Bredt 2006, DOI `10.1126/science.1123339`, PMID
    `16513974`, reviewing TARPs as AMPAR auxiliary subunits that control AMPAR
    trafficking and channel gating.
  - Kato et al. 2008, DOI `10.1016/j.neuron.2008.07.034`, PMID `18817736`,
    distinguishing type-II TARPs such as gamma-5/gamma-7 from the classical
    Cacng2/3/4/8 group.
  - Itakura et al. 2014, DOI `10.1111/febs.12708`, PMID `24418105`, showing
    that gamma-8 has a long C-terminal tail with a PSD-95/Dlg/ZO-1 binding
    motif and a calcineurin-binding region.
  - Zheng et al. 2015, DOI `10.1042/BJ20140806`, PMID `25495042`, showing
    that TARP gamma-8 glycosylation supports gamma-8 and GluA1 surface
    expression.

I did not use the unavailable `dataset.perturbseq_features` or
`corpus.predictive_graph_review` capabilities because this is a scalar count
prediction with no supplied ranked or partial-ranked gene supervision.

## Computation over the declared data

I counted `pvals_adj < 0.05` in the focal-cell Parquet for mechanistically
nearby training perturbations and checked those values against the training
count CSV. I also queried all cell groups for the closest TARP perturbations to
see whether their focal nulls hid a broad effect elsewhere.

The focal endpoint distribution is zero-inflated: 1,205 of 1,674 training
targets are zero, the median is 0, the 75th percentile is 1, the 90th
percentile is 2, and the maximum is 2,677. Thus a prediction of a nonzero
integer requires target-specific evidence for a transcriptional response,
not merely evidence that the gene matters synaptically.

For `151 TH Prkcd Grin2c Glut`, the relevant training perturbations were:

| training target | observed `n_degs` | focal DE evidence |
|---|---:|---|
| `Cacng2` | 0 | 17,259 tested RNAs, no FDR 0.05 genes; minimum adjusted p-value 1.0 |
| `Cacng3` | 0 | 17,259 tested RNAs, no FDR 0.05 genes; minimum adjusted p-value 1.0 |
| `Gria1` | 0 | no FDR 0.05 genes; minimum adjusted p-value 0.246 |
| `Gria2` | 0 | no FDR 0.05 genes; minimum adjusted p-value 1.0 |
| `Gria3` | 0 | no FDR 0.05 genes; minimum adjusted p-value 0.971 |
| `Dlg4` | 1 | the single FDR 0.05 gene was `Dlg4` itself |
| `Grik5` | 1 | the single FDR 0.05 gene was `Grik5` itself |
| `Grin2a` | 1 | the self transcript was the sole focal FDR hit |
| `Grin2b` | 2 | small NMDAR-subunit response |
| `Grin1` | 89 | broadest glutamate-receptor counterexample in this neighborhood |

Only `Cacng2` and `Cacng3` among the Cacng/TARP family were represented as
training perturbations. A full-Parquet scan showed that neither had any FDR
0.05 genes in any assayed neuronal group, not just in the focal thalamic group.
The internal corpus matched this: `Cacng2:F001-F004` and `Cacng3:F001-F003`
recorded Cacng2 and Cacng3 as pan-null or nearly flat, with no AMPAR-subunit,
TARP-paralog, postsynaptic-scaffold, immediate-early, BDNF, or hidden
correlation signature. `Dlg4:F001-F004` similarly recorded acute Dlg4/PSD-95
loss as transcriptionally flat aside from its self transcript and separated PSD
scaffolding from the stronger NMDAR-subunit responses.

## Target-specific reasoning

`Cacng8` encodes TARP gamma-8, a classical AMPAR auxiliary subunit. The direct
molecular effect of losing Cacng8 should be impaired trafficking and gating of
gamma-8-containing AMPAR complexes rather than loss of a transcription factor
or an obligatory nuclear RNA-processing component. Tomita et al. and Nicoll et
al. place gamma-8 in the same classical TARP family as `Cacng2` and `Cacng3`;
Zheng et al. support a gamma-8 role in AMPAR maturation and GluA1 surface
expression; Itakura et al. show that gamma-8 also has isoform-specific
postsynaptic interactions through its extended C terminus.

The causal chain I used was:

`Cacng8` CRISPR loss -> impaired gamma-8/TARP contribution to AMPAR surface
expression, gating, and postsynaptic anchoring -> possible changes in
excitatory synaptic transmission or plasticity -> any induced activity,
homeostatic, receptor-biogenesis, or stress program in surviving TH
glutamatergic nuclei -> FDR-controlled nuclear mRNA hits at the 3-4 week
snRNA-seq endpoint.

At the direct molecular stage, `Cacng2` and `Cacng3` are the closest available
training analogs because they are the represented classical TARPs. Both predict
the same qualitative direct direction, impaired TARP/AMPAR function, but they
also test whether a single TARP perturbation propagates to the requested
nuclear DEG-count endpoint. In this dataset it did not: both produced exactly
0 focal DEGs, and neither produced an FDR 0.05 signature anywhere else in the
Parquet. This is stronger than a local thalamic null because it argues that
acute loss of the represented TARPs is generally buffered or post-transcriptional
under the assay conditions.

The assayed AMPAR pore-forming genes were also counterexamples to a broad
"any AMPAR component perturbs the transcriptome" rule. `Gria1`, `Gria2`, and
`Gria3` each gave 0 focal DEGs. The AMPAR-associated scaffold `Dlg4` gave one
hit, the perturbed `Dlg4` transcript itself, without downstream compensation in
`Dlg1`, `Dlg2`, `Dlg3`, `Gria1-3`, `Cacng2`, `Shank2`, `Shank3`, `Syngap1`,
`Homer2`, `Nrxn1-3`, `Nlgn3`, or `Camk2a/b/g` in the focal query and internal
corpus summary. This makes an isolated one-DEG self-transcript outcome possible
for synaptic scaffolds, but the two Cacng analogs themselves had no significant
self-transcript row, and weak self-transcript change is not a reliable editing
efficiency readout in this experiment.

`Grin1`, with 89 focal DEGs, is a useful falsifier rather than the chosen
analog. Its response shows that a glutamate-receptor perturbation can be
visible to this focal cell group, so the Cacng nulls are not explained by a
complete inability of the assay to report synaptic perturbations. But `Grin1`
is an obligatory NMDAR pore subunit, while Cacng8 is an AMPAR auxiliary subunit
with redundancy across AMPAR complexes and an endpoint dominated by synaptic
trafficking and channel biophysics. The internal Cacng2 and Dlg4 Findings made
the same split: NMDAR subunits were transcriptionally active in settings where
AMPAR/TARP/PSD-95 perturbations stayed flat.

Putting those together, the closest endpoint-bearing evidence is the
within-dataset `Cacng2`/`Cacng3` pan-null pair, reinforced by focal nulls for
`Gria1-3` and the one-self-gene `Dlg4`/`Grik5` cases. External knowledge makes
those comparisons mechanistically appropriate by linking Cacng8 to classical
TARP-AMPAR trafficking, but it does not supply a reason to expect gamma-8 loss
to cross the FDR 0.05 nuclear response threshold in this specific thalamic,
postnatal, mosaic survivor-conditioned assay. I therefore predicted no
significant DEGs:

| held-out target | predicted `n_degs` |
|---|---:|
| `Cacng8` | 0 |

## Limits

This is an extrapolation from other AMPAR/TARP perturbations because the
requested `Cacng8` signature was completely held out. The best direct analogs
were only `Cacng2` and `Cacng3`; `Cacng4`, `Cacng5`, `Cacng7`, `Cnih2`,
`Cnih3`, and `Gria4` were not focal training perturbations in the supplied
count CSV. Gamma-8 has biochemical features not shared with stargazin/gamma-2,
notably the long C-terminal calcineurin-binding region, so a small Cacng8-only
activity or trafficking response could be missed by these analogs. The Parquet
measures nuclear RNA among recovered, class-assigned cells, not AMPAR surface
abundance, synaptic currents, homeostatic scaling, or pre-assay depletion.
Consequently the zero prediction means only "no measured gene passes FDR 0.05
in this assay"; it does not assert that Cacng8 loss is biologically inert.
