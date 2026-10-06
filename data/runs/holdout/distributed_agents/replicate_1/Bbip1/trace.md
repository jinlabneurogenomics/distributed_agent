# Prediction trace

## Question and resolved scope

I interpreted the task as a scalar point prediction for the held-out `n_degs`
endpoint in `151 TH Prkcd Grin2c Glut` thalamic glutamatergic neurons: for each
requested perturbation, predict the number of measured genes with
Wilcoxon Benjamini-Hochberg-adjusted `pvals_adj < 0.05` in the perturbed nuclei.
The endpoint includes a significant self-target transcript if the target's own
RNA passes FDR, but the dataset portrait warns that self-RNA depletion is not an
editing-efficiency measurement, so I did not use self knockdown as a continuous
effect-strength proxy.  The only requested target was `Bbip1`; it is absent from
both the training-count CSV and the Parquet as a perturbation target.

The target list has one column and no supplied ranks, so file order is used only
for the required output order.  This is a scalar/count prediction, not a ranked
prediction; the rank-calibration workbench, `corpus.predictive_graph_review`,
and `synthesis.ordering_validate` were not policy-available for this run and
were not used.

## Sources used

- Declared training endpoint:
  `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
- Declared differential-expression Parquet:
  `training differential-expression dataset`.
- Requested held-out targets:
  `single-target request for Bbip1`.
- Run-local dataset portrait and task bindings in `codex_runtime/pipeline`.
- Internal same-experiment semantic corpus:
  `perturbai-july-260713-sourceguard-1773-v1`; I used the bounded Findings and
  Evidence/Reference ledgers for `Bbs5`, `Ttc8`, and `Ift88`, which are
  interpreted surfaces over the same Perturb-seq experiment, not independent
  replication.
- External mechanism priors from PubMed and Reactome:
  Nachury et al. 2007, Cell, doi:10.1016/j.cell.2007.03.053, PMID 17574030;
  Loktev et al. 2008, Developmental Cell,
  doi:10.1016/j.devcel.2008.11.001, PMID 19081074;
  Jin et al. 2010, Cell, doi:10.1016/j.cell.2010.05.015, PMID 20603001;
  Scheidecker et al. 2013, Journal of Medical Genetics,
  doi:10.1136/jmedgenet-2013-101785, PMID 24026985;
  Guo et al. 2016, PLoS Genetics, doi:10.1371/journal.pgen.1005890,
  PMID 26926121;
  Huangfu et al. 2003, Nature, doi:10.1038/nature02061, PMID 14603322;
  Reactome mouse IFT-B assembly `R-MMU-5617824`; Reactome BBSome-mediated
  cargo targeting to cilium `R-HSA-5620922`.

## Dataset calculations

From the focal training-count table, I computed the distribution of observed
`n_degs` across the 1,674 non-held-out targets.  It is heavily zero-inflated:
1,205/1,674 visible perturbations have zero DEGs, the median is 0, the 75th
percentile is 1, the 90th percentile is 2, and the 95th percentile is 18.  Thus
the background prior for a random held-out gene in this cell group is zero or
near zero unless there is strong analog evidence for a broad response.

I then restricted the Parquet to `group_name == "151 TH Prkcd Grin2c Glut"` for
literature-obvious ciliary and BBSome-adjacent perturbations.  The immediate
comparators in the training CSV were:

| analog perturbation | observed focal `n_degs` | focal matched perturbed nuclei | key focal DE evidence |
|---|---:|---:|---|
| `Bbs5` | 0 | 121 | no gene at FDR<0.05; best adjusted p-value 0.220 for `Ptprn` |
| `Ttc8` / BBS8 | 1 | 180 | the only FDR<0.05 gene was `Ttc8` itself, log2FC -0.663, FDR 3.07e-5 |
| `Cep290` | 0 | 99 | no focal FDR<0.05 gene; best FDR 0.650 |
| `Ift88` | 0 | 143 | no focal FDR<0.05 gene |
| `Kif3b` | 0 | 156 | no focal FDR<0.05 gene |
| `Dync2h1` | 0 | 98 | no focal FDR<0.05 gene; best FDR 0.348 |

I also checked a wider ciliary, IFT, transition-zone, Hedgehog, and ciliary
receptor panel in the same training-count file.  `Ift43`, `Ift81`, `Dync2i1`,
`Lztfl1`, `Rpgrip1l`, `Ttc21b`, `Cep120`, `Cspp1`, `Cplane1`, `Smo`, `Ptch1`,
`Ptch2`, `Gli1`, `Gli2`, `Lepr`, `Glp1r`, and `Htr6` all had `n_degs = 0` in
`151 TH Prkcd Grin2c Glut`.

The internal Bbs5/Ttc8/Ift88 reports supported the same interpretation across
the whole training atlas.  `Bbs5:F003` noted that represented BBSome and ciliary
relatives did not phenocopy `Bbs5`; `Ttc8:F003` reported no shared
FDR-significant module for `Bbs5`, IFT-B, dynein-2, `Lztfl1`, `Rpgrip1l`,
`Ttc21b`, and `Cep290`; and `Ift88:F003` reported that IFT, dynein, BBSome,
transition-zone, `Ptch`, and `Gli` perturbations converged mainly by having no
robust transcriptional response.  The corresponding evidence records are
same-experiment summaries over the Parquet; their role here was to identify and
check biologically appropriate comparators, not to create an independent score.

## Target-specific reasoning

### `Bbip1`

`Bbip1` encodes BBIP1/BBIP10/BBS18, a small BBSome-associated subunit.
`BBIP10` localizes to cilia, is present in the BBSome fraction, interacts with
HDAC6, and its depletion caused ciliogenesis and tubulin-acetylation phenotypes
in cell and zebrafish assays (Loktev et al. 2008, PMID 19081074).  Human
loss-of-function `BBIP1` variants cause Bardet-Biedl syndrome and the null
protein was unable to associate with BBS4, tying BBIP1 to BBSome assembly
(Scheidecker et al. 2013, PMID 24026985).  The BBSome was defined as a ciliary
membrane biogenesis and cargo-sorting complex by Nachury et al. 2007 and
Jin et al. 2010; Reactome likewise places BBSome components in
ARL6/BBSome-mediated cargo targeting to cilia.

The causal chain for transfer to the focal endpoint is therefore:

`Bbip1` perturbation -> impaired BBIP1/BBSome-dependent ciliary cargo handling,
with possible microtubule-acetylation effects -> altered ciliary receptor
localization or signaling -> any basal thalamic neuronal state change that
survives P16 AAV CRISPR, sparse editing, and P37-P44 nucleus recovery ->
BH-significant nuclear-RNA changes.

The direct molecular step is strong, but the later links in this specific assay
are weak.  The training perturbation closest in complex membership, `Bbs5`, had
zero focal DEGs.  `Ttc8`/BBS8 had one focal DEG, but that was just the `Ttc8`
self-transcript; it did not show downstream FDR changes in the focal group.
`Lztfl1`, a BBSome and Smoothened trafficking regulator, was also zero in the
focal group.  Broader ciliary machinery did not rescue a nonzero prediction:
IFT-B (`Ift43`, `Ift81`, `Ift88`), dynein-2 (`Dync2h1`, `Dync2i1`), kinesin-2
(`Kif3b`), and transition-zone or ciliopathy genes (`Cep290`, `Cep120`, `Cspp1`,
`Cplane1`, `Rpgrip1l`, `Ttc21b`) were all zero in `151 TH Prkcd Grin2c Glut`.
The Hedgehog/receptor arm also argued against a broad basal nuclear readout:
`Smo`, `Ptch1`, `Ptch2`, `Gli1`, `Gli2`, `Lepr`, `Glp1r`, and `Htr6` were all
zero locally, consistent with the same-experiment Bbs5 and Ift88 reports that
neither ciliary GPCR cargo biology nor the canonical IFT-Hedgehog axis became a
shared postnatal neuronal snRNA-seq program.  Guo et al. 2016 show that BBSome
loss can be important in neuronal leptin-receptor trafficking, but that study
places the main phenotype in LRb-expressing metabolic circuitry and receptor
trafficking, not in the resting thalamic `151 TH Prkcd Grin2c Glut` transcript
count requested here.

I therefore predicted a focal `n_degs` of 0 for `Bbip1`.  The nonzero
possibilities are a lone self-transcript hit, by analogy to `Ttc8`, or a
BBIP1-specific HDAC6/microtubule-acetylation effect not shared by other BBSome
subunits.  Both are extrapolations: `Bbs5`, `Ift88`, `Kif3b`, `Cep290`, and
`Dync2h1` all had no focal self or downstream DEG despite adequate matched
focal nuclei, BBIP1's distinctive microtubule role has not been shown to create
a broad basal neuronal nuclear-RNA signature, and the supplied Parquet has no
direct `Bbip1` perturbation rows because `Bbip1` was held out.

## Limits

The prediction is not a direct observation of `Bbip1`; its DEG count and
signature were withheld from both supplied inputs.  The BBSome-complex transfer
is mechanistically specific at the ciliary-cargo step, but `Bbs1`, `Bbs2`,
`Bbs4`, `Bbs7`, `Bbs9`, `Arl6`, and `Bbip1` themselves were not visible
training targets, so the most relevant direct training perturbations were
`Bbs5` and `Ttc8`.  The internal corpus is useful because it packages exact
same-experiment comparator checks, but it is another representation of the same
Parquet and not an independent validation cohort.  Finally, a zero prediction
means no gene is expected to pass this assay's focal FDR 0.05 threshold; it
does not imply ineffective genome editing, intact cilia, or biological
unimportance of `Bbip1`.
