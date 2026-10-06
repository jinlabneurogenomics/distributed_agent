# Trace

## Target and endpoint

The one-row holdout manifest names `Trrap`; it is absent from the declared
`151 TH Prkcd Grin2c Glut` training count table, so the target count was not
used.  The requested endpoint is the number of measured genes in this class
with Wilcoxon BH-adjusted `p < 0.05`.

The declared Trrap biology bundle gives two target-specific anchors that moved
the forecast upward from the screen-wide null-heavy baseline:

- `Trrap` is measurably present in the focal non-target nuclei:
  21,438/23,679 nuclei express it, `pct_cells_expressing = 90.5359`,
  `mean_raw_umi = 2.9008`, and `pseudobulk_cpm = 181.806`.
- The functional-stock adjudication calls TRRAP a renewable, noncatalytic
  scaffold in NuA4/TIP60 and SAGA/STAGA-family HAT complexes and concludes
  `functional_stock_by_harvest = likely_substantially_depleted`.  The source
  card cites direct mouse postnatal-neuron evidence in which Trrap deletion
  produced broad early molecular remodeling and later postmitotic neuronal
  structural phenotypes, while keeping the caveat that the edit timing and
  regions were not the exact P16 thalamic population.

## Training measurements used

The supplied 151-class training count table has 1,674 targets.  Its empirical
distribution is sparse:

- median: `0`
- 75th percentile: `1`
- 90th percentile: `2`
- 95th percentile: `18`
- 97.5th percentile: `100`
- nonzero targets: `469/1674`
- targets with at least 100 DEGs: `43/1674`

Thus a large prediction needs target-specific justification; it is not the
generic expectation for a recovered perturbation.

I nominated training-available biological analogs from the mouse annotation
store and selected same-experiment corpus.  `Trrap` itself was absent from the
training universe and absent from the selected same-experiment ledger/BioKG
projection.  The tight HAT/MYC/Mediator nominees were mostly quiet in the
declared FDR<0.05 count table:

| relationship to Trrap | training target | n_degs |
|---|---:|---:|
| STAGA/TFTC human one-to-one CORUM projection | `Atxn7` | 0 |
| MYC-TRRAP complex projection | `Myc` | 0 |
| TFTC-type HAT projection | `Med13` | 11 |
| TFTC-type HAT projection | `Med23` | 13 |
| H2A.Z/p400-TIP60 projection | `Prkdc` | 0 |
| TIP60-C projection | `Tubb5` | 1 |
| p300/CBP HAT module | `Crebbp` | 8 |
| p300/CBP HAT module | `Ep300` | 0 |

Those low counts argue against treating every HAT-complex or MYC-axis member
as a high-DEG perturbation in postmitotic thalamic neurons.  The corpus
summaries for `Atxn7` and `Ep300` likewise describe them as transcriptomically
buffered or flat across recovered groups, and the `Crebbp` report describes
only a small, 151-restricted response rather than an EP300-like broad
phenocopy.  The graph audit over the 19 non-broad Trrap nominees also split
them into several directed components rather than one connected response
module, reinforcing that complex proximity alone should not be pooled into a
large count.

I nevertheless did not collapse Trrap to the exact-complex median of zero.
TRRAP is a shared scaffold for multiple acetyltransferase assemblies, has no
close replacement scaffold in the source-card search, and the focal class has
high in-assay Trrap RNA reach.  Broader training chromatin/transcription
regulators show that the same cell class can generate large nuclear-regulator
responses when the perturbed factor has a continuing postmitotic role:
`Yy1 = 720`, `Ctnnb1 = 383`, `Brd4 = 311`, `Smarcc2 = 185`, `Tcf7l2 = 106`,
`Camta1 = 78`, and `Arid2 = 56`.  Packaged findings place `Yy1` and `Brd4`
in broad posterior/thalamic programs and `Ctnnb1` in a Wnt/excitability/
adhesion program, so I treated them as upper-tail context rather than direct
numeric surrogates for Trrap.

The profile comparison of the analog cohort in `151 TH Prkcd Grin2c Glut`
supported the same split: exact HAT/MYC candidates, Wnt candidates, and broad
chromatin responders shared weak positive-tail overlap overall, while their
larger negative tails and significant programs were only partially recurrent.

## Synthesis

The final point prediction is that Trrap loss should be visibly non-null but
well below the major stress-like `Sin3a`/`Yy1`/`Brd4` responses.  I placed it
near the top few percent of the training distribution, just under the 97.5th
percentile, because its biology is stronger than the flat STAGA/MYC/p300
singletons but the matched training data repeatedly show that represented HAT
subunits do not behave as one broad thalamic module.

Predicted `n_degs`: `96`.
