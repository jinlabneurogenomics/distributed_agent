# Mc3r n_degs forecast

## Declared target

- Holdout manifest target: `Mc3r`.
- Focal population: `151 TH Prkcd Grin2c Glut`.
- Endpoint: number of measured genes with BH-adjusted Wilcoxon `p < 0.05` in the focal population.

## Evidence used

### Mc3r biology-only bundle

- The exact in-assay non-target expression reach for `Mc3r` in `151 TH Prkcd Grin2c Glut` is very small:
  - `289 / 23679` non-target nuclei express detectable `Mc3r`.
  - `pct_cells_expressing = 1.2204907301828625`.
  - `mean_raw_umi = 0.01587904894632375`.
  - `pseudobulk_cpm = 0.9951963065342999`.
- Functional-stock adjudication argues that edited cells should eventually lose functional MC3R resupply:
  - operative entity: `dynamic_complex_component`;
  - edit effect: `new_supply_stops_existing_function_persists`;
  - conclusion: `likely_substantially_depleted` by the P37-P44 harvest, but with only partial evidence and unknown endogenous neuronal receptor half-life.
- The biological role has weak transfer into this exact endpoint:
  - MC3R is a melanocortin-activated Gs/cAMP receptor, not a broadly required transcriptional or RNA-processing component.
  - postnatal neural observability is supported only at low confidence from adult/germline neural evidence outside this thalamic class.
  - phenotype latency after P16 postmitotic editing is unresolved.

### Same-population training counts

The declared training count table contains 1,674 measured training perturbations for this same focal group. It is extremely zero-heavy:

- 1,205 / 1,674 have `n_degs = 0`.
- Median = 0; 75th percentile = 1; 90th percentile = 2.
- 469 / 1,674 are nonzero, while only 106 reach at least 10 DEGs and the upper tail is dominated by core chromatin, splicing, proteasome, transport, or transcriptional regulators.

Training perturbations closest to the MC3R operation favor a null or near-null count:

- Melanocortin/neuropeptide/GPCR examples in the count table:
  - `Mc1r = 0`, `Mc2r = 0`, `Mchr1 = 0`;
  - `Crhr1 = 0`, `Lepr = 0`, `Oxtr = 0`;
  - `Npy1r = 0`, `Npy2r = 0`, `Npy5r = 0`, `Ntsr1 = 0`;
  - `Oprd1 = 0`, `Oprk1 = 0`, `Oprl1 = 0`, `Oprm1 = 0`;
  - `Drd2 = 0`, `Drd4 = 0`, `Drd5 = 0`;
  - all listed serotonin receptors from `Htr1a` through `Htr7` have 0.
- Immediate cAMP-related training perturbations are also quiet in this group:
  - `Gnas = 0`, `Adcy1 = 0`, `Adcy3 = 0`, `Adcy5 = 0`;
  - `Camk2a = 0`, `Camk2g = 0`, `Camk2b = 1`, `Prkar1a = 1`.
- The larger apparent circadian examples are not operation-matched receptor perturbations:
  - `Rora = 278` and `Nr1d1 = 116` are nuclear transcriptional regulators with broad cell-intrinsic programs.
  - `Clock = 3`, `Cry1 = 1`, and `Cry2 = 3` show that even direct clock-gene perturbations can be small here.

Direct inspection of the declared expression Parquet for the selected same-population GPCR/cAMP/circadian controls was concordant with the count table: zero-count receptor and adenylate-cyclase perturbations had no focal rows with `pvals_adj < 0.05`, while the one-DEG kinase examples were self-target-only effects and the high-count `Rora`/`Nr1d1` signatures represented many significant non-self genes.

## Synthesis

The positive biology is that a successful edit could deplete MC3R over the 21-28 day window, and single-receptor MC3R loss is not globally redundant in mouse physiology. The negative quantitative bearings are stronger for this particular DEG-count endpoint: focal expression reaches only about 1.2% of matched non-target nuclei, the external phenotypes do not establish an acute thalamic transcriptional program, and same-class perturbation data put related GPCR and Gs/cAMP nodes at zero or one significant gene.

I therefore expect any true MC3R-dependent state to be too sparse or conditional to survive BH correction across the recovered `151 TH Prkcd Grin2c Glut` nuclei. My direct point prediction is:

```text
n_degs = 0
```
