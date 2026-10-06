# Zfp329 direct `n_degs` forecast

## Target and endpoint

- **Target:** `Zfp329`, the single gene in the declared one-row holdout manifest.
- **Cell group:** `151 TH Prkcd Grin2c Glut`.
- **Endpoint:** number of measured genes with BH-adjusted Wilcoxon `pvals_adj < 0.05`.
- **Measurement surface used for outcomes:** the declared `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` count table and the matching `training_de_all_cell_groups.parquet`. The Zfp329 row/signature is absent from both.

## Biology prior from the declared bundle

- Zfp329 is annotated as a nuclear C2H2 zinc-finger protein predicted to bind RNA-polymerase-II regulatory DNA and regulate transcription (`ZFP329-OP-1`).
- The target transcript is measurably present in the exact focal population: `16,911 / 23,679` non-target 151 TH Prkcd Grin2c Glut nuclei expressed Zfp329 (`71.4%`), with mean raw UMI `1.386`.
- A P16 disruptive edit should affect the functional pool by P37-P44: the card calls the operative stock a renewable transcription-factor/DNA-associated pool and concludes that functional stock is **likely substantially depleted** over the 21-28 day interval.
- The same card leaves the endpoint coupling weak: no target-specific Zfp329 neuronal turnover was found, the known mouse loss phenotype is germline visual-system anatomy rather than postnatal thalamus, postnatal thalamic requirement is unresolved, and no close same-context compensator was demonstrated.

Net interpretation: the perturbation is likely expressed and at least partly realized in the focal cells, so it is not a stock-persistence null. But it is an understudied predicted TF with no direct evidence for a maintained juvenile thalamic program.

## Same-experiment corpus context

The packaged same-experiment corpus returned no Zfp329 Findings, Claims, or explicit comparator references in this release. I treated that only as absence of a released semantic record, not as independent null replication.

For observed zinc-finger exceptions, the corpus argues against transferring their larger counts wholesale to Zfp329:

- `Zfp423` has a distinct 151 TH subtype/adhesion response and known EBF/BMP/RA-related biology; its own report also says obvious relatives did not phenocopy that response.
- `Zfp236` has a narrow Ogt/Eif4a2/Cpt1c-centered module that did not reduce to generic zinc-finger or heterochromatin loss.
- `Zfp148` has a small 151-only spliceosome/synaptic response tied to GC-rich promoter biology and does not show a broad p53-like collapse.

Those active comparators are informative upper examples for C2H2/ZFP perturbations in 151 TH, but they carry specific state evidence missing for Zfp329.

## Training-count placement

The focal training count table has 1,674 targets. Its distribution is extremely zero-inflated:

- all training targets: `1,205 / 1,674` zeros, median `0`, 75th percentile `1`, 90th percentile `2`, mean `14.05`.
- transcription-factor functional class: `284 / 344` zeros, median `0`, 75th percentile `0`, 90th percentile `2`.
- genes sharing Zfp329's exact broad RNA-pol-II DNA-binding TF annotation (`GO:0000981`): `236 / 280` zeros, median `0`, 75th percentile `0`, 90th percentile `1`.
- training genes sharing all of Zfp329's non-nuclear GO/functional-class annotations: `21 / 24` zeros; the only nonzero members were `Pura` at 22, `Creb1` at 10, and `Cux2` at 1.
- `Zfp*` targets: `25 / 30` zeros, median `0`, 75th percentile `0`, 90th percentile `1`; the nonzero cases were `Zfp423` 150, `Zfp236` 19, `Zfp148` 8, `Zfp612` 1, and `Zfp692` 1.

I also checked the declared Parquet in the exact 151 group for the nonzero and nearby zero `Zfp*` comparators; the observed `pvals_adj < 0.05` counts matched the table and showed the same sparse family structure, with the large counts confined to the named idiosyncratic responders.

## Forecast

Zfp329's high focal expression and probable stock depletion push it above a pure unexpressed/failed-edit explanation, but the strongest matched quantitative evidence is that generic sequence-specific RNA-pol-II zinc-finger TF perturbations are usually silent in this endpoint. The active ZFP outliers are not close Zfp329 analogs by same-experiment state or curated Zfp329 biology.

The most likely integer is therefore the analog-cohort mode and median:

```tsv
target_name	predicted_n_degs
Zfp329	0
```
