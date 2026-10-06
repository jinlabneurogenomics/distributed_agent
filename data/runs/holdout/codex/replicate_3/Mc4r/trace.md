# Mc4r n_degs trace

## Target and endpoint

- Target manifest: `Mc4r`
- Cell class: `151 TH Prkcd Grin2c Glut`
- Endpoint: number of measured genes with Wilcoxon BH-adjusted `pvals_adj < 0.05` in this class.

## Target biology used

The declared Mc4r biology bundle supports realized loss only in a limited, expression-restricted way:

- MC4R is a melanocortin-responsive membrane GPCR coupled to adenylyl-cyclase/cAMP signaling, not a global chromatin, spliceosome, proteasome, or trafficking core factor.
- The functional-stock card calls MC4R stock "likely_substantially_depleted" by the 21-28 day harvest, but with partial evidence: the edit stops new receptor synthesis, the receptor traffics dynamically, and adult focal deletion has a behavioral effect within two weeks in another cortical population; endogenous juvenile thalamic receptor half-life is not resolved.
- Exact focal-population reach is extremely small. In non-target 151 TH nuclei, Mc4r has:
  - `80 / 23679` expressing nuclei
  - `pct_cells_expressing = 0.3378521052409308`
  - `total_target_umi = 97`
  - `pseudobulk_cpm = 0.2567394726963486`

That last point dominated the endpoint forecast. A real MC4R-dependent state in the few Mc4r-positive thalamic neurons would be mixed into the whole `151 TH Prkcd Grin2c Glut` contrast and should be diluted roughly 300-fold at class level before Wilcoxon testing.

## Training count scale

From the declared `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` table:

- `1674` training targets
- `1205` have `n_degs = 0`
- median `n_degs = 0`
- 75th percentile `= 1`
- 90th percentile `= 2`
- 95th percentile `= 18`
- 99th percentile `= 430`

The high tail is driven by perturbations such as `Uba5`, `Tpr`, `Sin3a`, RNA-processing factors, and protein-homeostasis regulators rather than cell-surface receptors.

## Training perturbations interpreted

I used the curated gene-annotation store to define GPCR comparators rather than selecting only by gene-symbol spelling.

In the exact same 151 TH count table:

- `functional_class=gpcr` / GO `G protein-coupled receptor activity`: 95 measured training GPCR perturbations, 85 zeros, and the 10 positive entries each had only `n_degs = 1`.
- GO `neuropeptide binding`: 9 training targets, all `0`.
- GO `melanocortin receptor activity`: the observed melanocortin receptors `Mc1r` and `Mc2r` were both `0`.
- WikiPathways `GPCRS_PEPTIDE`: 29 training targets, all `0`.
- Reactome `G alpha (s) signalling events`: 27 training targets, 25 zeros and two targets at `1`.

The available CORUM/GPCR neighbors that share curated MC4R heteromer or close peptide-receptor context were also silent in the held-out class:

| target | n_degs |
|---|---:|
| Adrb2 | 0 |
| Adrb3 | 0 |
| Crhr1 | 0 |
| Cxcr4 | 0 |
| Gprc5b | 0 |
| Htr2c | 0 |
| Npy1r | 0 |
| Npy2r | 0 |
| Npy5r | 0 |
| Ntsr1 | 0 |
| Oxtr | 0 |
| Mc1r | 0 |
| Mc2r | 0 |

## Parquet/profile check

I then checked the declared expression Parquet for those 13 GPCR peers in `151 TH Prkcd Grin2c Glut`. All 13 had observed profiles in the raw Parquet rows and none had any gene at `pvals_adj < 0.05`. The profile-comparison tool over the same 13 nodes likewise returned `response_activity_status_counts = {"no_significant_features": 13}`.

This confirmed that the zero counts above were raw endpoint zeros in the matched cell class, not a missing-profile artifact.

## Forecast synthesis

The upward evidence is that MC4R loss is functionally plausible by harvest and is not completely redundant with Mc3r in whole-animal melanocortin biology. The downward evidence is stronger for this endpoint: the exact class-level expression reach is only `0.3379%`, and the closest observed GPCR, peptide-GPCR, G-alpha-s, and curated MC4R-neighbor perturbations in the same 151 TH endpoint are nearly all exact zeros.

I therefore forecast no BH-significant class-level transcriptional genes:

`predicted_n_degs = 0`
