# Reasoning trace

## Question and endpoint

The held-out target list for this run contains one perturbation, `Gria4`.  I
therefore predicted one integer:

- the number of assayed genes expected to pass Benjamini-Hochberg-adjusted
  Wilcoxon `pvals_adj < 0.05` after acute sparse CRISPR loss of `Gria4` in
  `151 TH Prkcd Grin2c Glut` neurons.

The output count is an assay endpoint, not an estimate of GluA4 biological
importance.  The input parquet has no rows for `Gria4` as a `gene_target`, so
the `Gria4` signature and self-transcript p-value are absent.  Counts in the
training CSV include the target transcript when the target itself reaches FDR
0.05; this matters because several receptor or scaffold perturbations have
exactly one DEG, the self transcript.

## Sources used

- Declared Perturb-seq DE parquet:
  `training differential-expression dataset`.
  I queried exact `151 TH Prkcd Grin2c Glut` rows for glutamate-receptor,
  AMPAR-auxiliary, PSD, and CaMKII comparator perturbations.
- Declared focal-cell training endpoint:
  `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
- Declared held-out manifest:
  `single-target request for Gria4`.
- Internal same-experiment semantic corpus:
  `perturbai-july-260713-sourceguard-1773-v1`.  I used its bounded Findings
  inventory and null-cause records for `Gria1`, `Gria2`, `Gria3`, `Grin1`,
  `Grin2a`, `Grin2b`, `Dlg4`, and `Shank3`; these are curated interpretations
  of the same experiment and not independent replication.
- External literature for mechanism:
  - Traynelis et al. 2010, DOI `10.1124/pr.109.002451`, PMID `20716669`, and
    Hansen et al. 2021, DOI `10.1124/pharmrev.120.000131`, PMID `34753794`, for
    ionotropic glutamate receptor assembly and AMPA/NMDA receptor subunit
    physiology.
  - Kato et al. 2010, DOI `10.1016/j.tins.2010.02.004`, PMID `20219255`, and
    Diaz 2010, DOI `10.1111/j.1460-9568.2010.07357.x`, PMID `20946114`, for
    TARP and other AMPAR auxiliary control of receptor trafficking and gating.
  - Wang et al. 2011, DOI `10.1523/JNEUROSCI.4569-11.2011`, PMID `22090494`,
    for thalamic relay-synapse GluA3/GluA4 AMPAR dependence.
  - Luchkina et al. 2014, DOI `10.1073/pnas.1315769111`, PMID `24599589`, and
    Huupponen et al. 2016, DOI `10.1152/jn.00435.2015`, PMID `26961102`, for
    GluA4 roles in immature hippocampal AMPAR plasticity.
  - Fukuchi et al. 2015, DOI `10.1523/JNEUROSCI.3650-14.2015`, PMID
    `25855176`, for NMDAR calcium/CRTC1/CREB coupling to `Bdnf` and
    immediate-early gene induction.

## Quantitative checks over the declared data

I first verified that the requested file contains exactly `Gria4` and then
filtered the focal-cell training table for mechanistic comparators:

| training perturbation class | focal `n_degs` |
| --- | --- |
| AMPAR pore-forming paralogs | `Gria1 = 0`, `Gria2 = 0`, `Gria3 = 0` |
| kainate/delta/NMDA ionotropic receptor counterexamples | `Grid1 = 1`, `Grid2 = 0`, `Grik1 = 0`, `Grik3 = 0`, `Grik4 = 0`, `Grik5 = 1`, `Grin1 = 89`, `Grin2a = 1`, `Grin2b = 2`, `Grin2d = 0`, `Grin3a = 0` |
| AMPAR auxiliary or nearby PSD signaling genes | `Cacng2 = 0`, `Cacng3 = 0`, `Frrs1l = 1`, `Cpt1c = 1`, `Dlg4 = 1`, `Dlgap4 = 2`, `Homer2 = 0`, `Shank2 = 0`, `Shank3 = 2`, `Syngap1 = 0`, `Camk2a = 0`, `Camk2b = 1`, `Camk2g = 0` |

I then pulled the focal-cell DE rows for these comparators and ranked each
signature by absolute Wilcoxon score.  This checked whether a nominal
near-threshold tail was hidden under an exact zero count.

- `Gria1`: 174 perturbed nuclei, 23,679 matched controls, `0` DEGs at FDR 0.05;
  the best downstream gene was `Map4k4`, log2FC `0.384`, score `4.340`,
  adjusted p `0.246`.
- `Gria2`: 157 perturbed nuclei, `0` DEGs; all queried focal rows had adjusted
  p `1.0` among the strongest-score genes.
- `Gria3`: 132 perturbed nuclei, `0` DEGs; even the `Gria3` self transcript was
  not FDR-significant in this cell group, with log2FC `-0.413`, score `-4.028`,
  adjusted p `0.971`.
- `Cacng2` and `Cacng3`: 143 and 149 perturbed nuclei, respectively, and `0`
  DEGs; the best absolute scores were modest and FDR-nonsignificant.
- `Dlg4`, `Grid1`, `Grik5`, `Grin2a`, `Camk2b`, and `Dlgap4`: their one or two
  focal DEGs were dominated by self-transcript loss, with at most one
  downstream FDR hit for `Dlgap4` or `Shank3`.
- `Grin1`: 89 DEGs with 247 perturbed nuclei.  The strongest non-self genes
  were a coherent NMDAR-associated 151 signature, e.g. `Scg2`, `Stmn4`,
  `Kctd16`, `Gpm6a`, `Dync1li2`, and `Tspan7`, all with FDR below 1e-5 to
  1e-6 after `Grin1` loss.  This is a counterexample showing that the assay can
  detect an ionotropic-glutamate-receptor transcriptional response in the focal
  thalamic group when the perturbation impairs the obligate NMDAR subunit.
- `Grin2a`, `Grin2b`, `Grin2d`, and `Grin3a`: `Grin2a` contributed only its
  self transcript in the focal group, `Grin2b` had self plus `Pianp`, and
  `Grin2d`/`Grin3a` had zero DEGs.  The same-experiment corpus reports that
  `Grin2a` and `Grin2b` responses concentrate in cortical IT groups rather than
  phenocopying the thalamic `Grin1` state.

The relevant computation was the direct endpoint calculation
`sum(pvals_adj < 0.05)` over focal rows by `gene_target`, followed by sorting
the same filtered rows by `abs(scores)` to inspect whether the zero-count
analogs had substantial sub-FDR structure.

## Target-specific prediction

### `Gria4`

`Gria4` encodes GluA4, one of the four pore-forming AMPA receptor subunits.
External physiology makes it a legitimate AMPAR comparator for `Gria1`,
`Gria2`, and `Gria3`, and the thalamus is not an implausible context: Wang et
al. found that GluA3 and GluA4 contribute strongly to AMPAR currents at
developing thalamic relay synapses.  At the same time, this direct consequence
is channel composition and synaptic AMPAR current, with substantial control by
heteromeric subunit assembly and auxiliary trafficking proteins, rather than an
obligate nuclear-RNA program.  The Luchkina and Huupponen hippocampal studies
also put much of GluA4's best-defined role in early postnatal plasticity, while
this experiment perturbed sparsely at P16 and read resting P37-P44 nuclear RNA.

The most specific within-dataset analogs all predict no broad focal RNA
response:

- `Gria1`, `Gria2`, and `Gria3` are the closest pore-forming AMPAR paralogs and
  all had `0` focal DEGs at FDR 0.05.  The July same-experiment corpus
  separately summarizes all three as nearly downstream-null or buffered across
  the atlas: their direct phenotypes are expected to be AMPAR composition,
  localization, and plasticity rather than steady-state nuclear mRNA.  Because
  `Gria1` was explicitly 151-flat with best downstream FDR `0.246`, and because
  `Gria2`/`Gria3` were even flatter in the focal group, they are stronger
  analogs for `Gria4` than any generic excitatory-synapse gene.
- `Cacng2` and `Cacng3`, TARP-family AMPAR auxiliary subunits, were also `0`.
  Their biology is one step away from the pore: they regulate AMPAR trafficking
  and gating, so their null focal signatures support the interpretation that an
  AMPAR trafficking or gating perturbation can be physiologically meaningful
  without producing many FDR-significant nuclear transcripts.
- `Dlg4`, `Shank2`, `Shank3`, `Homer2`, and `Syngap1` show that nearby
  postsynaptic scaffolds/signaling adaptors are mostly 0 to 2 DEG perturbations
  in the same cell group.  They are imperfect because they perturb PSD
  organization rather than the AMPAR pore, but they argue against a hidden
  large shared PSD-injury RNA program.
- `Grin1` is the principal counterexample.  It was very active in the exact
  focal group, but it removes the obligatory NMDAR subunit and therefore blocks
  NMDAR calcium-dependent signaling to BDNF/immediate-early and homeostatic
  programs.  `Gria4` loss should first reduce a replaceable AMPAR subunit's
  contribution to fast excitatory current.  I therefore did not transfer the
  `Grin1 = 89` count to `Gria4`.
- `Grin2a`/`Grin2b` are partial NMDAR-subunit comparators that were 1 and 2 in
  the focal cell group and transcriptionally active mainly elsewhere.  They
  reinforce that subunit identity and regional receptor composition dominate
  over broad "ionotropic glutamate receptor" class membership.

The zero/nonzero decision is therefore mostly driven by the declared
within-dataset evidence from `Gria1`, `Gria2`, `Gria3`, `Cacng2`, and `Cacng3`.
External biology only decides that these are the right analogs for held-out
`Gria4` and that the large `Grin1` response is not an obligate consequence of
AMPAR loss.  I predict that sparse postnatal `Gria4` perturbation will not move
any measured gene, including the `Gria4` transcript itself, below focal
BH-adjusted p < 0.05.

Point prediction: `0` DEGs.

## Limits and extrapolation

- `Gria4` itself was held out, so no target-specific perturbation cells,
  self-transcript p-value, or signature neighbors are available.
- The prediction extrapolates from other AMPAR subunits.  GluA4 has thalamic
  and developmental roles that are not identical to GluA1/GluA2/GluA3, so a
  GluA4-specific downstream marker in this thalamic class would be missed by
  paralog transfer.
- Counts of 0 for `Gria1` and `Gria3` were measured with only 174 and 132
  perturbed nuclei.  The zeros are nonetheless more persuasive because
  multiple AMPAR pore and auxiliary perturbations were simultaneously flat and
  `Grin1` showed that this cell class is not globally incapable of a receptor
  response.
- The assay measured resting survivor nuclear RNA 3-4 weeks after sparse AAV
  CRISPR.  It did not measure DNA indels, surface AMPAR abundance, AMPAR/NMDAR
  currents, evoked plasticity, synaptic localization, or developmental circuit
  refinement.  A predicted DEG count of `0` should not be read as absence of a
  synaptic GluA4 phenotype.
