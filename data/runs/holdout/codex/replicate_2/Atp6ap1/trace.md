# Direct forecast: Atp6ap1 in 151 TH Prkcd Grin2c Glut

## Target and endpoint

The one-row manifest target is `Atp6ap1`. The requested endpoint is the count of measured genes in `151 TH Prkcd Grin2c Glut` with BH-adjusted Wilcoxon `pvals_adj < 0.05`.

`Atp6ap1` was absent from the declared `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`; the same-experiment corpus also had no packaged `Atp6ap1` report or Finding, so no Atp6ap1 endpoint value or Atp6ap1 profile was available.

## Biology used

The declared Atp6ap1 biology bundle places ATP6AP1/Ac45 as a membrane V0-region V-ATPase component, together with ATP6AP2 helping create the V0/V1 assembly interface. The target is reachable in the focal population: the exact non-target measurement for `151 TH Prkcd Grin2c Glut` has Atp6ap1 detected in 23,268 of 23,679 nuclei, `pct_cells_expressing = 98.2643`, and `mean_log1p_cp10k = 1.5509`. The bundle adjudicates operative stock as likely substantially depleted by P37-P44, but with only partial evidence because postnatal neuronal ATP6AP1/V-ATPase residence kinetics were not directly measured.

That argues against treating the perturbation as unreachable. It does not argue for a large nuclear RNA footprint, because the same bundle notes that the closest loss phenotypes are developmental rather than a synchronized acute postnatal thalamic-neuron response.

## Training measurements used

I used biochemically nearest measured V-ATPase perturbations as the quantitative center in the declared 151 TH count table and profile Parquet:

| training target | reason for inclusion | n_degs in 151 |
| --- | --- | ---: |
| `Atp6ap2` | paired V0/accessory-interface component named by the Atp6ap1 bundle | 2 |
| `Atp6v0a1` | neuronal V0 proton-pore a subunit | 1 |
| `Atp6v1a` | core V1 A subunit | 0 |
| `Atp6v1b2` | core V1 B subunit | 0 |
| `Atp6v1e1` | core V1 E subunit | 0 |

In the matched Parquet rows, the 151-significant calls for these closest V-ATPase perturbations were minimal:

| training target | FDR<0.05 151 genes |
| --- | --- |
| `Atp6ap2` | `Atp6ap2`, `Atp6v0a1` |
| `Atp6v0a1` | `Atp6v0a1` |
| `Atp6v1a` | none |
| `Atp6v1b2` | none |
| `Atp6v1e1` | none |

The packaged same-experiment Findings reinforced this as a V-ATPase boundary rather than just a single count-table accident: `Atp6ap2` was summarized as a nearly silent survivor transcriptome with only recurrent Atp6v0a1 down-regulation, `Atp6v0a1` as self-detected in several groups without downstream FDR<0.10 response, and `Atp6v1a`/`Atp6v1e1` as sparse, non-convergent V-ATPase responses. The release-level Claim around these Findings states that same-pump membership was insufficient to produce a shared postnatal neuronal snRNA-seq module among represented V-ATPase components.

I treated `Rab7`, `Tsc2`, `Vps35`, and `Vps54` as upper-bound/context perturbations rather than numeric donors. They show that `151 TH Prkcd Grin2c Glut` can support large endomembrane or growth-control signatures in the same table (`Rab7 = 501`, `Tsc2 = 86`, `Vps35 = 17`, `Vps54 = 31`), but their significant features did not overlap the V-ATPase singleton profiles in the matched profile comparison, and the Atp6ap2 report specifically contrasted Rab7 as an opposite lysosomal/V-ATPase compensation program rather than a phenocopy.

## Forecast synthesis

The direct biochemical donors in this class sit at 0-2 DEGs, with a mean of 0.6 and median of 0 among the five represented accessory/core V-ATPase targets above. Atp6ap1's closest available analogue is `Atp6ap2`, whose 151 count was 2 and consisted of its self-transcript plus Atp6v0a1; direct `Atp6v0a1` loss yielded only its self-transcript; the other core V-ATPase subunits yielded zero.

I therefore placed Atp6ap1 near the top of the flat V-ATPase group, because the focal cells express Atp6ap1 broadly enough for either a self transcript or one V0-adjacent downstream change to be detectable, but far below the Rab7/Tsc2 endolysosomal stress programs because represented direct pump perturbations did not convert acidification biology into a broad BH-significant nuclear response.

Predicted `n_degs`: **1**
