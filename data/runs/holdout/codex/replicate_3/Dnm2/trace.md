# Dnm2 n_degs forecast for 151 TH Prkcd Grin2c Glut

## Target and endpoint

- Exact held-out target from the declared manifest and biology bundle: `Dnm2`.
- Endpoint: the number of measured genes in `151 TH Prkcd Grin2c Glut` with BH-adjusted Wilcoxon `pvals_adj < 0.05`.
- The declared target bundle exposed no `Dnm2` endpoint value and the training count table did not contain `Dnm2`.

## Evidence used

### Direct target biology

- `Dnm2` has exact focal-population expression reach: mean raw UMI 1.330, mean CP10K 0.846, and 16,437 of 23,679 non-target nuclei expressing the transcript in `151 TH Prkcd Grin2c Glut` (69.4%). This makes a self-transcript test technically reachable, but does not measure the held-out `Dnm2` perturbation contrast.
- The functional-stock bundle adjudicates DNM2 as likely substantially depleted by the harvest window. The key timing fact is a postnatal hippocampal-neuron conditional experiment in which DNM2 protein was reduced by 92.5% by DIV18, inside the P16 to P37-P44 atlas interval.
- The same bundle also flags attenuation by paralog buffering: DNM1 and DNM3 preserve much of the assayed neuronal function after `Dnm2` single loss. That pushes the forecast away from a broad downstream transcriptional response even if DNM2 itself is lost.
- The selected same-experiment corpus had no `Dnm2` Finding, Claim, or explicit-reference records, so there was no packaged `Dnm2` report evidence to use as target-specific same-experiment context.

### Training counts in the focal population

The 1,674-row `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` table is extremely zero-inflated:

| quantity | value |
|---|---:|
| median `n_degs` | 0 |
| 75th percentile | 1 |
| 90th percentile | 2 |
| 95th percentile | 18 |
| targets with 0 DEGs | 1205 / 1674 |
| targets with <=1 DEGs | 1481 / 1674 |
| targets with <=10 DEGs | 1571 / 1674 |

The closest measured biology around DNM2 was also low:

| training target | focal `n_degs` | interpretation |
|---|---:|---|
| `Dnm1` | 1 | closest measured classical-dynamin paralog |
| `Cltc` | 3 | core clathrin heavy chain |
| `Bin1` | 1 | membrane-remodeling BAR/adaptor target |
| `Synj1` | 1 | synaptic-vesicle recycling target |
| `Syp` | 1 | synaptic-vesicle target |
| `Syn1` | 1 | synaptic-vesicle target |
| `Dlg4` | 1 | postsynaptic scaffold |
| `Camk2a` | 0 | neuronal signaling boundary |
| `Camk2b` | 1 | neuronal signaling boundary |

Direct Parquet inspection in the matched `151 TH Prkcd Grin2c Glut` context showed that `Dnm1`, `Bin1`, `Synj1`, `Syp`, `Syn1`, `Dlg4`, `Camk2b`, and `Actg1` each had exactly one significant gene, and in every case that gene was the perturbed self transcript. `Cltc` had only three significant genes, all negative and just below the FDR threshold (`Ero1b`, `Gabra4`, `Rbms1`; adjusted p = 0.0424).

As boundaries, `Rab7` and `Ctnnb1` had 501 and 383 focal DEGs, respectively. Those counterexamples kept membrane trafficking or cytoskeletal involvement from being treated as generically quiet, but their late-endosomal or Wnt/cytoskeletal biology is much less like a buffered single classical-dynamin loss than `Dnm1` is.

### Profile review

I compared the observed `151 TH Prkcd Grin2c Glut` signed profiles of `Dnm1`, `Cltc`, `Bin1`, `Synj1`, `Syp`, `Syn1`, `Dlg4`, `Camk2a`, `Camk2b`, `Actg1`, `Rab7`, and `Ctnnb1`.

- The explicit cohort contained 12 available profiles and 66 pairwise comparisons.
- Nine of the 12 nodes had 1-9 significant features, one had no significant features, and only the two boundary nodes (`Rab7`, `Ctnnb1`) had at least 50 significant features.
- Pairwise whole-profile correlations among the low-count endocytic/synaptic nodes were near zero and FDR-significant intersections were negligible. I therefore used the profile review as support for low response activity, not as a signed centroid or a calibrated numeric model.

## Synthesis

`Dnm2` should be reachable and functionally edited by the experimental window, so a total null caused by absent target expression or persistent DNM2 stock is not the best point estimate. The stronger endpoint-matched evidence is that the closest assayed single-loss programs around classical dynamin, clathrin-mediated endocytosis, and synaptic-vesicle recycling are self-only or nearly silent in `151 TH Prkcd Grin2c Glut`. The postnatal DNM1/DNM3 redundancy in the biology bundle provides a mechanism for why `Dnm2` could follow `Dnm1` rather than the high-response `Rab7` or `Ctnnb1` boundaries.

The remaining quantitative ambiguity is mostly `0` versus `1`: a DNM2 self-transcript call is plausible because `Dnm2` is expressed in most focal control nuclei, but the target-mRNA readout is not a reliable editing-efficiency surrogate. I chose one DEG as the point forecast: no broad downstream response, with the significant gene most likely being the self transcript.

Forecast: `Dnm2` -> `1`
