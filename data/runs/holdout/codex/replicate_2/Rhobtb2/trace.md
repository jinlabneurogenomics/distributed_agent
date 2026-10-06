# Rhobtb2 n_degs forecast

## Endpoint

Forecast target: `Rhobtb2`.

Endpoint: `n_degs` in `151 TH Prkcd Grin2c Glut`, defined as the number of measured genes with BH-adjusted Wilcoxon `pvals_adj < 0.05`.

## Evidence used

### Target biology and focal-population reach

The declared `Rhobtb2` biology bundle reports exact in-assay reach in the requested population: `Rhobtb2` was detectable in 16,698 of 23,679 matched non-target nuclei, or 70.52%, with `mean_raw_umi = 1.377`, `mean_cp10k = 0.876`, and `pseudobulk_cpm = 86.30`. This argues against a forecast based on absent target expression in the thalamic glutamatergic population.

The same bundle adjudicates the operative entity as a dynamic CUL3 ubiquitin-ligase substrate adaptor and calls functional RhoBTB2 stock by harvest `likely_substantially_depleted`, with only partial evidence completeness because there is no quantitative RhoBTB2 half-life in postmitotic thalamic neurons. This makes loss over the P16 to P37-P44 window plausible, but does not itself establish a large recovered-cell transcriptional response.

### Training-count scale

The declared `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` table is very sparse:

- 1,674 training perturbations.
- 1,205 / 1,674 have `n_degs = 0`.
- The median is 0 and the 90th percentile is 2.
- The arithmetic mean is 14.05 only because a small group of core-machinery genes has hundreds to thousands of DEGs.

So a gene without a close observed analogue should be forecast near 0 unless a task-matched mechanism points to a broad response state.

### Typed analogue nomination

`gene-analog-nomination-skill` over the exact training universe resolved `Rhobtb2` as absent from the training table and absent from the selected corpus ledger. It found no training-available exact paralog or exact-complex candidate; the strongest specific set consisted of four Reactome `RHOBTB2 GTPase Cycle` / `RHOBTB GTPase Cycle` narrow-module co-members:

| candidate | observed `n_degs` |
| --- | ---: |
| `Hsp90ab1` | 1 |
| `Myo6` | 0 |
| `Ddx39b` | 0 |
| `Hnrnpc` | 122 |

I did not treat `Hnrnpc = 122` as a scale-matched center because it is an RNA-binding/nuclear gene that only shares bounded Reactome module membership with `Rhobtb2`, not a CUL3 substrate-adaptor role.

The nearest broad CUL3/adaptor fallbacks were much quieter:

| candidate | relationship used for inspection | observed `n_degs` |
| --- | --- | ---: |
| `Lztr1` | CUL3-RING ubiquitin ligase complex; ubiquitin-like ligase-substrate adaptor | 1 |
| `Klhl20` | CUL3-RING ubiquitin ligase complex; ubiquitin-like ligase-substrate adaptor | 0 |
| `Kbtbd7` | CUL3-RING ubiquitin ligase complex; ubiquitin-like ligase-substrate adaptor | 0 |
| `Klhl7` | CUL3-RING ubiquitin ligase complex; ubiquitin-like ligase-substrate adaptor | 0 |
| `Fbxo11` | ubiquitin-like ligase-substrate adaptor, but not the CUL3-RING annotation | 1 |
| `Fbxw7` | ubiquitin-like ligase-substrate adaptor, but not the CUL3-RING annotation | 1 |
| `Arih1` | broader E3 / CUL3-RING fallback | 7 |
| `Depdc5` | CUL3-RING annotation through a broader mTOR/GATOR context | 13 |

### Matched Parquet profile inspection

I compared the four Reactome nominees and eight CUL3/E3 fallback nodes directly in the declared Parquet restricted to `151 TH Prkcd Grin2c Glut`, using `gene_target` as the perturbation column, `names` as the measured-gene column, `logfoldchanges` as the signed value, and `pvals_adj < 0.05` as the significant-program definition.

The cohort was not a hidden high-response cluster. Of the 12 inspected nodes, five had no significant measured gene, five had 1-9 significant genes, one had 13, and only `Hnrnpc` exceeded 50. The profile-cohort diagnostic also found no shared positive significant program: across all 66 candidate pairs, positive significant-program overlap was 0 wherever defined. Negative significant-program overlap was weak as well, with mean overlap coefficient 0.022 and median 0. This made the `Hnrnpc` response and the moderate `Depdc5` response isolated upper-boundary observations rather than a recurrent Rhobtb2-like state.

## Synthesis

I forecast slightly above the population median because `Rhobtb2` is detectably expressed in most focal nuclei and should lose a renewable adaptor pool over the edit-to-harvest window. I kept the point at the low end because:

- neither `Rhobtb1` nor `Rhobtb3` is available as a training analogue;
- no exact CUL3-RhoBTB complex analogue is available;
- three of the four closest CUL3 substrate-adaptor fallbacks have `n_degs = 0`, and the fourth has `n_degs = 1`;
- broader ubiquitin/E3 fallbacks are still mostly 0-1 DEGs; and
- the few larger counts in the inspected cohort come from mechanistically broader or off-axis perturbations and do not form a recurrent significant profile.

The point prediction is therefore:

`Rhobtb2 -> 1`
