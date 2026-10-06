# Direct forecast for Tbk1 in 151 TH Prkcd Grin2c Glut

## Target and endpoint

- Target manifest: `Tbk1`
- Cell population: `151 TH Prkcd Grin2c Glut`
- Endpoint: `n_degs`, the count of measured genes with BH-adjusted Wilcoxon `p < 0.05`
- Declared outcome surfaces used:
  - one-row manifest: `Tbk1`
  - declared biology bundle: `biology_bundles/Tbk1.json`
  - focal training count table: `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`
  - focal rows from the declared training DE Parquet through the measured-profile comparison tool

I did not use target outcome, labeled-neighbor outcome annotations, scalar priors, branch calibration, relationship-review, or terminal-prediction artifacts.

## Biology that set the prior

The declared biology-only `Tbk1` bundle says the focal feature is present in the assayed control population: `Tbk1` is detected in 19,805 of 23,679 non-target cells, or 83.64%, with mean raw UMI 2.50, mean CP10k 1.53, and pseudobulk CPM 156.6. That makes a loss-of-function edit reachable in `151 TH Prkcd Grin2c Glut`.

The same bundle supports substantial functional stock decline by the P37-P44 harvest only as a partial-evidence prior. TBK1 is a renewable diffusible serine/threonine kinase involved in IRF signaling and phosphorylation of selective-autophagy receptors such as OPTN; a P16 disruptive edit should stop new functional synthesis, and the 21-28 day interval is long relative to a multi-day neuronal-proteome turnover proxy. The uncertainty is important: no matched TBK1 half-life, residual-activity threshold, or 3-4 week thalamic-neuron loss phenotype was available. The closest in-vivo neural evidence came from motor-neuron or microglial deletion at later ages, not from juvenile thalamic NeuN-positive neurons. IKBKE compensation was plausible in some tissues but not tested in this neuronal context.

The selected same-experiment corpus had no `Tbk1` Findings, Claims, or explicit references in this release, so the corpus provided no direct `Tbk1` endpoint evidence to transfer.

## Training evidence that set the scale

The focal count table contains 1,674 training targets. It is extremely zero-heavy in this same `151` class:

- median `n_degs`: 0
- 75th percentile: 1
- 90th percentile: 2
- 95th percentile: 18
- zero-count targets: 1,205 / 1,674

I nominated training-available TBK1 comparators from typed mouse annotations and the selected corpus release using the declared focal training universe. The nomination retained 37 non-broad, training-available candidates supported by exact-complex/paralog, physical-interaction, or narrow-module evidence around STING/TBK1/IKBKE-IRF3/IRF7, TLR/TNFR1, and PINK1-PRKN mitophagy annotations.

Their observed focal counts were mostly null:

- top narrow or exact TBK1-pathway nominees with `n_degs = 0`: `Irf3`, `Traf3`, `Cyld`, `Tlr4`, `Ep300`, `Cd14`, `Tnfrsf1a`, `Chuk`, `Nfkb1`, `Tlr3`, `Map3k7`
- autophagy/xenophagy-side nominees were also quiet: `Sqstm1 = 1`, `Map1lc3a = 1`, `Atg5 = 0`, `Tomm40 = 1`, `Atg16l1 = 0`, `Tfg = 0`
- the direct or core-adjacent exceptions were still small: `Ddx3x = 8`, `Gsk3b = 6`, `Rack1 = 2`
- over all 37 specific nominees: 24 had zero DE genes, 11 had 1-9, `Csnk2b` had 25, and `Ctnnb1` had 383

The declared Parquet profile comparison over those same 37 nominees in exactly `151 TH Prkcd Grin2c Glut` also argued against treating the two larger nominated counts as a TBK1 scale. Across 666 pairwise comparisons, the cohort had weak top-tail sharing: median positive and negative top-tail overlap coefficients were both 0.025, and significant-program overlap was almost always zero. This is a diffuse annotation neighborhood, not one coherent high-count expression state.

The high-count outliers had mechanisms that did not transfer to TBK1. Packaged same-experiment Findings describe `Ctnnb1` as a thalamic Wnt/beta-catenin, excitability, adhesion, Ras/Rho/PKC, and neurosecretory state, with Ctnnb1/Tcf7l2/Lrp6 branch specificity and explicit non-phenocopy by Gsk3b and single Frizzled perturbations. `Csnk2b` was a caudal CK2/RNA-processing and neurite-remodeling state that did not phenocopy Ctnnb1. Neither state is the unstimulated TBK1-IKBKE/IRF/autophagy kinase axis, and using them would have imported a broad Wnt or CK2 transcriptional scale unsupported by the TBK1 biology bundle.

## Synthesis

`Tbk1` is expressed and should lose renewed kinase stock in edited neurons, so I did not treat it as unreachable. But its known signaling outputs are stimulus-, adaptor-, and substrate-dependent; glial inflammatory consequences are outside the NeuN-positive assay; and the strongest measured relatives of the basal TBK1/IKBKE/IRF, TLR/TNFR, and selective-autophagy neighborhoods were essentially silent in the focal class. The two nonzero high-end nominees are better explained by Wnt/beta-catenin or CK2 biology than by TBK1-like signaling.

Given a focal median of zero, a 90th percentile of two, zero counts in the top eleven specific TBK1-pathway nominees, and weak measured-profile cohesion among the broader nominees, the best direct point forecast is the modal quiet outcome.

Predicted `n_degs`: 0
