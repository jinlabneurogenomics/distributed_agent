# P2rx2 focal-class DEG-count forecast

## Target and endpoint

- Target manifest: `P2rx2`
- Cell class: `151 TH Prkcd Grin2c Glut`
- Endpoint: `n_degs`, the count of measured genes with BH-adjusted Wilcoxon `p < 0.05`
- Point prediction: `0`

The declared target outcome and target signature were not used; the reasoning below combines the declared biology bundle, the focal-class training count table, and same-input focal-class profile comparisons among training perturbations.

## Evidence used

### P2rx2 prior from the declared biology bundle

The exact in-assay expression reach for `P2rx2` in non-target `151 TH Prkcd Grin2c Glut` nuclei was extremely small:

- `167 / 23679` non-target nuclei expressed `P2rx2`, or `0.7053%`
- total `P2rx2` UMI count was `196`
- `mean_raw_umi = 0.008277`
- `pseudobulk_cpm = 0.519`

The functional-stock adjudication still makes the edit biologically credible in cells that actually use P2X2: P2X2 is an ATP-gated trimeric cation-channel subunit, loss of new P2X2 supply is expected after a disruptive edit, and adult postmitotic-neuron evidence supports P2X2 protein depletion on an at-least-21-day clock. That evidence is partial and was in adult mPFC rather than juvenile thalamus. In this screen, the very small focal-class expression reach means any true effect should be heavily diluted in the aggregate recovered `151 TH Prkcd Grin2c Glut` contrast.

### Focal training-count distribution

The focal training count table contained 1,674 non-held-out perturbations.

- `1205 / 1674` had `n_degs = 0`
- `1481 / 1674` had `n_degs <= 1`
- median `n_degs = 0`
- 75th percentile `n_degs = 1`
- 90th percentile `n_degs = 2`
- maximum `n_degs = 2677`

Thus, zero is the dominant focal-class outcome before adding target-specific biology, and a lowly expressed channel target needs positive evidence to move it away from zero.

### Training analogs and measured profiles

No `P2rx` family member was present in the focal training table. The only focal purinergic receptor perturbations available were `P2ry12` and `P2ry14`, both with `0` DEGs.

Database-backed analog nomination for `P2rx2` returned 11 training-available candidates above the broad functional fallback tier. Their focal-class counts were:

| candidate | typed basis | n_degs |
| --- | --- | ---: |
| `Itpr1` | narrow calcium module | 0 |
| `Grin1` | physical interaction / ligand-gated-channel biology | 89 |
| `Grin2d` | physical interaction / ligand-gated-channel biology | 0 |
| `Grin2a` | physical interaction / ligand-gated-channel biology | 1 |
| `Chrna3` | human-ortholog-projected CHRNA3-P2RX2 complex | 0 |
| `Atp2b2` | narrow calcium module | 1 |
| `Atp2b1` | narrow calcium module | 22 |
| `Atp2b3` | narrow calcium module | 1 |
| `Chrna7` | direct-interaction / channel biology | 0 |
| `Calm1` | narrow calcium module | 14 |
| `Atp2a2` | narrow calcium module | 187 |

The leading broad ligand-gated and ion-channel nominees were also mostly zero or nearly zero: `Trpv1 = 0`, `Grik1 = 0`, `Grin2b = 2`, `Chrnb1 = 0`, `Grik5 = 1`, `Grik4 = 0`, `Htr3b = 0`, `Grid2 = 0`, `Gria1 = 0`, `Gria2 = 0`, `Grin3a = 0`, `Chrnd = 0`, `Chrng = 0`, `Gria3 = 0`, `Cacna1a = 0`, `Chrnb3 = 0`, and `Chrna6 = 0`.

The focal Parquet profile comparison was consistent with those integer counts. In the key comparator projection, `Itpr1`, `Chrna3`, and `P2ry12` had zero significant features; `Grin1` had 89 and `Atp2a2` had 187. Across the 17 analog/cofactor/purinergic profiles I compared, positive top-tail overlap was weak, with mean overlap coefficient `0.027` and median `0.02`; significant-program overlap was usually absent. The report-derived corpus topology also separated the calcium/NMDA component, the `Chrna3`/`Chrna7` component, and an isolated `Trpv1`, supporting the same interpretation: these perturbations are mechanistically adjacent but do not define one generic P2X-like transcriptional program.

### Outlier interpretation

The two large relevant outliers are poor numeric transfers to `P2rx2`.

- `Grin1` is an obligatory NMDA receptor subunit. Corpus findings report a strong `151 TH Prkcd Grin2c Glut` state after `Grin1` loss, but they also emphasize that represented NMDA subunit losses are subunit- and cell-context-specific rather than a generic receptor-loss signature.
- `Atp2a2` is SERCA2, an ER calcium pump. Corpus findings attribute its large focal response to an ER-stress/UPR/ISR state, and explicitly note that related PMCA, SPCA, and calcium-release-channel perturbations do not reproduce it.

P2X2 loss is a plasma-membrane ATP receptor-subunit lesion with very low in-class transcript reach, not an obligatory NMDAR lesion and not an ER calcium-store lesion. The quiet values for `Chrna3`, `Chrna7`, `Itpr1`, `Grin2d`, `Trpv1`, the purinergic `P2ry12/P2ry14` controls, and the AMPA/kainate receptor fallbacks therefore carried more weight than the stress-state outliers.

## Synthesis

I expect functional P2X2 depletion in the small minority of focal-class neurons where the channel is installed, but the target is nearly absent from the aggregate thalamic population measured by the endpoint. In the same focal class, most training knockouts are zero, most ligand-gated-channel and purinergic comparators are zero, and the nonzero calcium/NMDAR responses trace to mechanisms stronger than or qualitatively different from P2X2.

The most likely BH-significant DEG count is therefore exactly zero.
