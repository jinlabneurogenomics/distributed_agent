# Rara DEG-count forecast for 151 TH Prkcd Grin2c Glut

## Declared target

- Target: `Rara`
- Endpoint: `n_degs`, the number of measured genes in `151 TH Prkcd Grin2c Glut` with BH-adjusted Wilcoxon `p < 0.05`.
- Declared target expression reach: `Rara` was detected in 2,949 of 23,679 matched non-target nuclei in this focal group, or 12.454% of cells, with mean raw UMI 0.145741 and mean log1p CP10K 0.064670.
- Biology bundle interpretation: a disruptive edit is expected to deplete functional RARalpha across the 21-28 day edit-to-harvest window, and related RAR isotypes do not universally compensate for RARalpha loss in postnatal neurons. The same bundle also leaves thalamic Prkcd/Grin2c dependence unresolved and the exact focal-population reach is minority-cell reach.

## Training scale

The declared `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` table contains 1,674 training perturbations. Its focal count distribution is very sparse:

- 1,205 / 1,674 perturbations have `n_degs = 0`.
- The median is 0 and the 75th percentile is 1.
- 469 perturbations have any positive count.
- 106 perturbations reach at least 10 DEGs.
- The 95th percentile is 18 and the largest outliers are hundreds to thousands of DEGs.

So a strong biological prior has to overcome a high focal null rate, especially for a lowly expressed or diluted target.

## Biological comparators used

I treated the measured RAR/retinoid axis and receptor regulators as the closest scale references:

- Directly related retinoid-axis rows in the focal count table were quiet: `Rarb = 0`, `Rarg = 0`, and `Stra6 = 0`.
- Steroid or ligand-dependent nuclear receptor comparators were also mostly quiet in this focal group: `Ar = 0`, `Esr1 = 0`, `Esr2 = 0`, `Pgr = 0`, `Vdr = 0`, `Thrb = 0`.
- Broader bHLH/nuclear receptor comparators were mixed but not automatically high: `Ahr = 0`, `Arnt = 0`, `Rorb = 0`, `Rorc = 0`, `Thra = 3`, `Clock = 3`.
- The high nuclear-receptor rows, `Rora = 278`, `Nr1d1 = 116`, and `Esrra = 57`, looked like distinct active thalamic ROR/REV-ERB/ERR programs rather than retinoic-acid receptor analogs.

Same-experiment corpus context supported that separation. `Rarb` and `Rarg` Findings/Claims described represented RAR/RXR/retinoid perturbations as flat, singleton, or nonconvergent after acute single-gene perturbation; those Claims explicitly did not include `Rara`. `Rora` Findings instead described a selective thalamic transcriptional program that `Rorb` and `Rorc` did not phenocopy. Thus I used `Rora`, `Nr1d1`, and `Esrra` as evidence that this cell class can detect some ligand-dependent receptor programs, not as equal-scale predictors for `Rara`.

## Profile check

I compared 15 observed nuclear-receptor/regulatory perturbation profiles in the declared Parquet, restricted to `group_name == "151 TH Prkcd Grin2c Glut"`, in `workbench/nuclear_receptor_profile_compare.json`.

The profile tool reported:

- `Rarb` and `Rarg` had zero significant features in the focal group.
- `Rora`, `Nr1d1`, and `Esrra` were the only nominated receptor rows with at least 50 significant features.
- The null RAR paralogs did not carry an overlapping FDR program with those high-yield receptor states; their apparent whole-profile neighbors were weak, nonsignificant-rank similarities.

This profile evidence reinforced the count-table interpretation that high `Rora`/`Nr1d1` output should not be transferred wholesale to `Rara`.

## Forecast

I assign upward weight to the `Rara` biology because RARalpha has nuclear and dendritic neuronal functions, should turn over within the harvest window, and has postnatal mouse-neural loss phenotypes. I assign stronger downward weight to the specific endpoint because the focal assay averages a broad thalamic class in which only 12.454% of control nuclei expressed `Rara`, while the closest observed RAR/retinoid single-gene perturbations were zero in this focal class and the corpus found no shared acute neuronal retinoid module among represented relatives.

My point estimate is therefore the null focal count with a small-singleton upper shoulder:

```tsv
target_name	predicted_n_degs
Rara	0
```

No withheld `Rara` differential-expression signature or `Rara` target outcome was used.
