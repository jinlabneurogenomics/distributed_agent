# Epb41l1 DEG-count forecast

## Target and endpoint

- Target: `Epb41l1`
- Cell group: `151 TH Prkcd Grin2c Glut`
- Endpoint: number of measured genes with BH-adjusted Wilcoxon `pvals_adj < 0.05`
- Predicted `n_degs`: `1`

## Biology used

The declared biology bundle identifies `Epb41l1` as the neuronal protein 4.1N, a FERM-domain membrane/cortical-cytoskeletal scaffold involved in postsynaptic receptor organization rather than a catalytic or transcriptional regulator. Exact focal-population reach is moderate: in non-target cells from `151 TH Prkcd Grin2c Glut`, `Epb41l1` was detected in 9,910 of 23,679 nuclei, or 41.85%, with mean CP10k 0.434 and mean log1p(CP10k) 0.276.

The functional-stock evidence points to real target engagement by harvest but not to an intrinsically large nuclear RNA response. The source card reports a target-protein half-life estimate of 7.46 days in cultured cortical neurons, so a P16 edit followed by P37-P44 harvest spans roughly 3-4 half-lives of a renewable scaffold pool. At the same time, the strongest phenotypic facts are outside the focal thalamic context: complete germline loss gives postnatal neuroendocrine phenotypes, while juvenile hippocampal 4.1N/4.1G co-reduction changed GluR1 but left several CA1 glutamatergic physiology assays largely intact. I therefore treated `Epb41l1` as likely depleted enough to register if its transcript or a near-direct client is visible, but as biologically closer to buffered synaptic scaffolds than to high-burden nuclear, proteostasis, or core NMDA-receptor perturbations.

## Training measurements used

The declared focal count table contains 1,674 observed training targets. Its distribution is strongly concentrated near zero:

| statistic | focal-class `n_degs` |
| --- | ---: |
| median | 0 |
| 75th percentile | 1 |
| 90th percentile | 2 |
| 95th percentile | 18 |
| max | 2677 |

1,205 of 1,674 training targets had `n_degs = 0`, 1,512 had `n_degs <= 2`, and only 42 had `n_degs > 100`.

I then checked the training count table and expression Parquet for an outcome-visible cohort of synaptic, membrane-cytoskeletal, and glutamate-receptor perturbations:

| training target group | observed focal `n_degs` |
| --- | --- |
| adducin/spectrin/ankyrin cytoskeleton: `Add1`, `Add2`, `Add3`, `Ank`, `Ank1`, `Ank2`, `Sptan1`, `Sptb` | mostly 0; `Ank = 1`, `Sptan1 = 1` |
| postsynaptic scaffolds/adhesion: `Dlg4`, `Dlgap4`, `Homer2`, `Nlgn3`, `Nrxn1`, `Nrxn2`, `Nrxn3`, `Shank2`, `Shank3` | mostly 0-2: `Dlg4 = 1`, `Dlgap4 = 2`, `Nlgn3 = 1`, `Nrxn1 = 1`, `Shank3 = 2` |
| AMPA/NMDA receptor clients: `Gria1`, `Gria2`, `Gria3`, `Grin1`, `Grin2a`, `Grin2b`, `Grin2d`, `Grin3a` | AMPA genes 0; `Grin2a = 1`, `Grin2b = 2`, `Grin1 = 89`, `Grin2d = 0`, `Grin3a = 0` |

Direct Parquet inspection showed that the one-DEG calls for `Ank`, `Dlg4`, `Grin2a`, `Nlgn3`, `Nrxn1`, and `Sptan1` were the perturbed transcript itself. `Dlgap4`, `Grin2b`, and `Shank3` added only one extra significant gene. A profile comparison over these 25 outcome-visible perturbations gave 15 targets with no significant focal-class feature, 9 with 1-9 features, and only `Grin1` in the 50+ feature range, supporting use of `Grin1` as a core-receptor boundary rather than the expected scale for 4.1N.

## Synthesis

The prior from the full training table is zero or one DEG, and the most biologically adjacent measured perturbations sit in the same range. Because `Epb41l1` is expressed in a substantial minority of focal nuclei and its protein should have time to turn over after editing, I gave it slightly more than a pure-null expectation: the target transcript itself, or one tightly local downstream feature, could cross BH 0.05. I did not project a broad downstream signature because 4.1N is a peripheral scaffold with possible paralog buffering, the focal expression reach is partial, and the receptor/scaffold training examples are overwhelmingly self-only or silent.

The resulting point forecast is therefore:

```text
Epb41l1: 1
```
