# Chchd10 DEG-count forecast

## Target and endpoint

- Target: `Chchd10`
- Focal population: `151 TH Prkcd Grin2c Glut`
- Endpoint: `n_degs`, the number of measured genes in this population with Wilcoxon BH-adjusted `p < 0.05`
- Forecast: `1`

## Evidence used

### Target biology

The declared `Chchd10` biology bundle says that CHCHD10 is a labile inner-mitochondrial-membrane-associated intermembrane-space protein that interacts with the paralog CHCHD2 and helps restrain OMA1-dependent OPA1 processing. Editing at P16 should deplete the pre-edit CHCHD10 stock well before the P37-P44 harvest, because the measured protein half-life was on the order of hours rather than weeks. The lesion is therefore likely realized at harvest.

That same bundle also argues against a large single-gene stress response. CHCHD2 and CHCHD10 are experimentally partially redundant, and effective constitutive `Chchd10` loss in mouse brain produced no gross early phenotype and no detected forebrain respiration/ATP-synthesis or substantia-nigra ultrastructural abnormality at the assayed postnatal time. The exact focal expression entry keeps the target in scope: `Chchd10` was detected in 17,776 of 23,679 non-target nuclei in `151 TH Prkcd Grin2c Glut` with mean raw UMI 1.735 and mean CP10k 1.062.

### Training counts in the focal population

The declared `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` table contains 1,674 training perturbations. It is strongly zero-inflated in this cell class: 1,205 perturbations have zero FDR-significant genes, the median is 0, the 75th percentile is 1, the 90th percentile is 2, and the extreme tail drives the mean to 14.054.

I treated generic mitochondrial annotation as a weak quantitative predictor and used a CHCHD10/Opa1/Chchd2-adjacent cohort instead:

`Aco2, Afg3l2, Agk, Chchd2, Clpp, Clpx, Coa8, Cox4i1, Gfm2, Isca2, Lonp1, Mff, Micos13, Ndufa4, Ndufb8, Ndufs2, Ndufv1, Opa1, Park7, Slc25a46, Slc52a2, Snca, Sod2, Sucla2, Timmdc1, Tomm40, Uqcrq, Yme1l1`

Within that 28-target represented mitochondrial cohort, 16 targets had 0 DEGs and 11 had 1 DEG. `Opa1` was the lone larger responder at 37 DEGs; excluding that downstream stress-axis exception, the cohort mean was only 0.407 DEGs.

### Same-experiment training profiles and reports

The Parquet rows for the focal population show that `Chchd2` had exactly one significant feature, `Chchd2` itself (`logfoldchanges = -0.880`, adjusted `p = 3.18e-28`). The same-experiment Chchd2 findings describe a 23-cell-group null for non-target downstream genes and specifically report absence of the Opa1/OMA1-DELE1-eIF2alpha mitochondrial ISR sentinels after `Chchd2` perturbation.

`Opa1` is the positive control for a detectable cristae/inner-membrane stress state in this assay, with 37 focal-population DEGs including `Asns`, `Mars1`, `Chac1`, `Ddit3`, aminoacyl-tRNA synthetases, and `Slc7a5`. The Opa1 report identifies this as a cell-class-selective ATF4/ISR-like amino-acid stress program, but the same report and the Chchd2 report both show that many represented mitochondrial comparators do not phenocopy `Opa1`.

Across the full focal-population training surface, the Parquet contained a self-target row for 1,642 training perturbations. Of 275 singleton responses among those, 237 consisted of the self transcript. Thus `n_degs = 1` is the common pattern for a perturbation whose transcript is detected and FDR-significant while its downstream survivor-state response is otherwise buffered.

## Synthesis

I placed `Chchd10` nearest the buffered CHCHD2/single-mitochondrial-loss regime rather than the `Opa1` stress regime. The realized lesion and high focal expression make a completely invisible target-transcript result less likely than for low-reach genes, but CHCHD2 redundancy and the quiet postnatal single-knockout brain phenotype argue that acute sparse single `Chchd10` loss should usually stop at a self transcript rather than cross the threshold for an Opa1-like ATF4 program. The resulting point forecast is one significant measured gene.
