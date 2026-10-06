# Cdh2 direct DEG-count forecast

## Target and endpoint

- Target: `Cdh2`
- Focal population: `151 TH Prkcd Grin2c Glut`
- Endpoint: `n_degs`, the count of measured genes with BH-adjusted Wilcoxon `pvals_adj < 0.05`
- The declared one-row manifest contains only `Cdh2`. `Cdh2` is absent from the 1,674-row training count table, so no target count was present in the declared endpoint table.

## Evidence used

### Target biology bundle

The exact focal-population non-target expression record shows broad, measurable `Cdh2` expression in this thalamic class:

- `n_cells_expressing = 23116 / 23679`
- `pct_cells_expressing = 97.62236580936695`
- `mean_raw_umi = 7.0440896997339415`
- `mean_cp10k = 4.318081704929729`

The functional-stock adjudication calls the operative Cdh2 product an installed N-cadherin adhesion complex at neuronal membranes/synapses. Existing membrane complexes should initially persist after a P16 edit, but the stock is actively renewed; the card concludes that functional N-cadherin is `likely_substantially_depleted` by the P37-P44 harvest. The observability card supports a postnatal neuronal phenotype outside thalamus, while also leaving two important dampening terms: the closest direct phenotypes were late-postnatal hippocampal/excitatory rather than thalamic, and the exact 21-28 day latency in thalamus was unmeasured.

### Training count table

The exact 151-class training endpoint is very sparse:

- 1,674 training perturbations
- 1,205 have `n_degs = 0`
- 469 have any significant DEG
- median `n_degs = 0`
- 75th percentile `n_degs = 1`
- 90th percentile `n_degs = 2`
- 95th percentile `n_degs = 18`
- mean `n_degs = 14.05`, driven by a small tail of large core-machinery responses

### Cdh2-related training perturbations

I used Cdh2's biology bundle to choose perturbations touching cadherin/catenin regulation, cleavage, and synaptic adhesion, then read their declared 151-class counts:

| training perturbation | 151 TH Prkcd Grin2c Glut n_degs | interpretation for Cdh2 |
|---|---:|---|
| `Adam10` | 0 | N-cadherin turnover/cleavage neighbor; no broad measured state |
| `Ctnna2` | 0 | alpha-catenin cadherin linker; quiet in this class |
| `Ctnna3` | 0 | alpha-catenin paralog; quiet in this class |
| `Ctnnd2` | 1 | cadherin-associated delta-catenin; tiny response |
| `Fyn` | 0 | synaptic/cadherin signaling neighbor; quiet |
| `Pcdh19` | 0 | cadherin-superfamily adhesion comparator; quiet |
| `Adam22` | 1 | synaptic adhesion complex member; tiny response |
| `Cadm2` | 1 | synaptic adhesion molecule; tiny response |
| `Cntnap1` | 1 | neuronal adhesion molecule; tiny response |
| `Dlg4` | 1 | postsynaptic scaffold; tiny response |
| `Ncam1` | 1 | neuronal adhesion molecule; tiny response |
| `Nlgn3` | 1 | synaptic adhesion molecule; tiny response |
| `Nrxn1` | 1 | synaptic adhesion molecule; tiny response |
| `Ctnnb1` | 383 | direct beta-catenin partner, but much broader and mechanistically pleiotropic |

I then compared these 14 perturbations with the exact expression profiles in the declared Parquet, restricted to `151 TH Prkcd Grin2c Glut`. The profile comparison recovered all 14 requested nodes. Five had no significant features, eight had only 1-9 significant features, and only `Ctnnb1` had a broad response. In the focused profile inspection, `Ctnnb1` had 383 significant features, `Adam10` had 0, and the inspected low-response adhesion genes `Ctnnd2`, `Ncam1`, and `Nlgn3` had 1 each. The cohort diagnostic found weak recurrence in the positive tails and no shared significant negative program: among the 91 selected pairs, median positive top-tail overlap was 0.07, median negative top-tail overlap was 0.135, and every pair with defined significant-program overlap had coefficient 0.

## Synthesis

The Cdh2 biology rules out a confident zero in the way I would use it for an unexpressed or unrealized target: `Cdh2` is expressed in almost all focal nuclei, and a disruptive edit should materially deplete the N-cadherin carrier pool by harvest. That makes a small recovered-neuron transcriptional response plausible.

The magnitude should nevertheless stay near the bottom of the task-matched training distribution. N-cadherin is an installed homophilic adhesion protein, not a transcription factor or constitutive RNA-processing/proteostasis component, and its closest postnatal loss phenotypes are selective synaptic and circuit effects rather than an acute whole-cell state switch. In the exact 151-class training table, direct or near-direct cadherin/adhesion comparators are almost all 0 or 1 DEG. `Ctnnb1` is the important upward counterexample because it is physically coupled to cadherins, but its 383-DEG response is not a clean Cdh2 scale donor: beta-catenin has cadherin-independent Wnt/nuclear roles, and its significant genes were not shared with the low-count adhesion comparators in the bounded profile inspection.

I therefore set the point prediction just above the mode, equal to the dominant nonzero count among the local adhesion/synaptic comparators:

`predicted_n_degs = 1`
