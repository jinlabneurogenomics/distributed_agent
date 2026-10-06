# Dnm1l n_degs forecast

## Declared target

- Target: `Dnm1l`
- Population: `151 TH Prkcd Grin2c Glut`
- Endpoint: number of measured genes with BH-adjusted Wilcoxon `pvals_adj < 0.05`

## Evidence used

- The manifest contains the single held-out target `Dnm1l`. `Dnm1l` is absent from the 1,674-row `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`, as expected for a held-out forecast.
- The biology-only Dnm1l bundle supports real perturbation reach in the focal cells: `Dnm1l` is detected in 22,992 of 23,679 matched non-target nuclei in this population, with 97.10% expressing cells, mean raw UMI 4.81, mean log1p CP10K 1.308, and pseudobulk CPM 301.39.
- The same bundle supports target-stock loss inside the P16 to P37-P44 window: DRP1 is a dynamic mitochondrial/peroxisomal fission GTPase, adult forebrain Dnm1l loss depleted hippocampal DRP1 maximally within 14 days, and an independent neuronal SILAC estimate put DNM1L protein half-life at about 3.14 days.
- The training endpoint in the exact same population is extremely zero-inflated: 1,205/1,674 targets have `n_degs = 0`, the median is 0, the 75th percentile is 1, the 95th percentile is 18, and only the 1% tail exceeds about 436 DEGs.
- Curated training-available analog nomination made `Mff` the nearest specific comparator: it is in a native mouse CORUM `Dnm1l-Mff` complex, has a high-confidence STRING physical interaction to Dnm1l, and shares mitochondrial/peroxisomal fission terms. In the focal count table, `Mff` has 0 DEGs.
- Other close fission or mitochondrial-dynamics targets in the same table stayed small: `Gdap1 = 0`, `Ppp2r2b = 0`, `Slc25a46 = 1`, and the classical dynamin `Dnm1 = 1`. `Opa1`, a broader mitochondrial inner-membrane fusion/stress comparator rather than a DRP1 receptor, had 37 DEGs.
- A bounded explicit-Finding topology check over the nominated mitochondrial-dynamics cohort put `Mff`, `Opa1`, `Slc25a46`, and `Ppp2r2b` in the same small report-reference component, while broader GTPase comparators such as `Cdc42` and `Rac1` formed a separate component and `Vps35` was isolated within the supplied cohort.
- Direct Parquet queries in `151 TH Prkcd Grin2c Glut` confirmed the exact matched counts and significant-row patterns for the main analogs: `Mff` had 0/17,259 significant measured genes with 133 matched perturbed nuclei; `Slc25a46` had 1 with 201 perturbed nuclei; `Dnm1` had 1 with 194; `Gsk3b` had 6 with 108; `Vps35` had 17 with 133; and `Opa1` had 37 with 195.
- The `Opa1` DE profile was dominated by amino-acid/integrated-stress-response genes such as `Asns`, `Mars1`, `Chac1`, `Ddit3`, and aminoacyl-tRNA synthetases, while `Vps35` had a distinct retromer/endolysosomal pattern. In the 12-node matched profile comparison, the exact mitochondrial-dynamics candidates shared essentially no FDR-significant genes with one another, so these were useful upper local bounds rather than transferable Dnm1l signatures.

## Forecast reasoning

The in-assay expression and short DRP1 turnover make a functional Dnm1l lesion plausible by harvest, so I would not collapse the forecast to the focal-class background median of zero. However, the nearest measured fission perturbations were quiet: the exact Dnm1l-Mff receptor complex member was 0, the mitochondrial membrane fission member `Slc25a46` was 1, and broader fission annotations were also 0-1 except for `Opa1`.

`Opa1` and `Vps35` set a reasonable upper local scale, but both look mechanistically displaced from Dnm1l in the observed endpoint: `Opa1` reports inner-membrane/ISR biology, `Vps35` reports retromer biology, and neither supplied a shared significant program with `Mff`, `Slc25a46`, or `Dnm1`. I therefore placed Dnm1l below the 17-37 DEG analogs but above the 0-1 fission-receptor analogs, in the low-teens range.

Predicted `n_degs`: 12.
