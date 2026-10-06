# Direct DEG-count forecast for `Gpr12`

## Target and endpoint

- Target manifest: one held-out perturbation, `Gpr12`.
- Cell class: `151 TH Prkcd Grin2c Glut`.
- Endpoint: `n_degs`, the count of measured genes in this class with BH-adjusted Wilcoxon `pvals_adj < 0.05`.

## Biology used

- `Gpr12` is expressed in the exact assayed focal population: 18,357 of 23,679 non-target nuclei express it, 77.52% of the class, with mean raw UMI 1.816 and mean log1p CP10k 0.657.
- The curated biology bundle places GPR12 as a constitutively active seven-transmembrane receptor coupled to Gs/cAMP signaling.
- Adult mediodorsal-thalamus AAV RNAi against `Gpr12` was functionally consequential, so the target is not an obviously irrelevant thalamic receptor.
- The same curated card adjudicated functional stock by the P37-P44 harvest as indeterminate: editing at P16 stops new receptor supply, but it does not directly remove pre-existing membrane receptor, adult RNAi only anchored a later eight-week histology point, and no target-specific receptor half-life or 21-28 day clearance curve was found.
- GPR3/GPR6 are related receptors, but the bundle found no same-context compensation test; that leaves buffering possible rather than established.

This makes a response biologically plausible, but the expected response axis is a receptor/second-messenger perturbation with uncertain realization by 3-4 weeks, not an obligate RNA biogenesis, proteasome, chromatin, or neuronal identity collapse.

## Training measurements used

- The declared `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` table has 1,674 measured training perturbations.
- Its DEG burden is zero-inflated: 1,205/1,674 targets are exactly 0; the median is 0, the 75th percentile is 1, the 90th percentile is 2, and only 43 targets reach at least 100 DEGs.
- The largest 151-class counts are dominated by essential expression-machinery or proteostasis regulators such as `Uba5` 2677, `Tpr` 1768, `Sin3a` 1433, `Rnpc3` 868, `Zbtb7a` 841, `U2af2` 828, and `Psmb4` 742. `Gpr12` does not resemble that high-burden class.

## Comparator measurements used

I used curated analog nomination only as a broad biological inspection pool. It found 1,163 training-available `Gpr12` nominees, all at the broad-functional-fallback tier; there were no exact paralog, exact complex, direct-interaction, narrow-module, or reciprocal same-experiment corpus comparators. The leading training-available broad GPCR/cAMP/membrane candidates were also quiet in the requested 151-class endpoint:

| comparator set | 151-class counts |
| --- | --- |
| Top 20 broad analog nominees | 17/20 were 0; median 0; mean 1.15; maximum 21 |
| Core GPCR/Gs/cAMP rows from the count table | `Gnas` 0, `Adcy1` 0, `Adcy3` 0, `Adcy5` 0, `Adrb2` 0, `Htr4` 0, `Htr6` 0, `Pde10a` 0, `Pde1c` 0, `Pde4b` 0, `Pde4d` 0, `Prkaca` 1, `Prkar1a` 1, `Gnao1` 1 |

Direct Parquet checks in `151 TH Prkcd Grin2c Glut` confirmed the key zeroes above were present measured profiles, not missing rows: for example `Gnas` had 306 matched perturbed nuclei and 0 significant genes; `Adcy1`, `Adcy3`, `Adcy5`, `Adrb2`, `Htr4`, and the sampled PDEs likewise had matched recovered nuclei and 0 features with adjusted `p < 0.05`.

Packaged same-experiment Findings for observed training genes gave the same interpretation at FDR < 0.10:

- `Adcy1`, `Adcy3`, and `Adcy5` were downstream-null or broadly buffered in the measured neuronal groups.
- `Gnas` had no downstream genes at FDR < 0.10 in `151 TH Prkcd Grin2c Glut` and did not induce the expected CREB/immediate-early module.
- `Htr4` was null across all 23 measured groups.
- `Prkaca` and `Prkar1a` were null for non-target downstream genes across their measured groups.

I also compared 23 broad GPCR/cAMP nominees over their observed 151-class expression profiles. Seventeen had no significant features at adjusted `p < 0.05`, four had one to nine, and two had 10-49. Among focal Gs/cyclase/PKA nodes (`Gnas`, `Adcy1`, `Adcy3`, `Adcy5`, `Prkaca`), the profile inspection recovered no shared significant intersections with the selected receptor and cAMP peers; the observed similarities were weak whole-profile correlations among near-null profiles.

## Synthesis

The exact reach makes `Gpr12` perturbable in this population, and the adult thalamic RNAi result argues against treating it as biologically inert. Those upward bearings are outweighed for this specific scalar endpoint by three downward bearings:

1. The short-window stock card is unresolved, so a P16 edit need not fully deplete the pre-existing receptor pool by P37-P44.
2. The closest assayed signaling layer is Gs/cAMP/PKA, and in the same 151 class `Gnas`, the measured adenylyl cyclases, GPCR comparators, PDEs, and PKA components are almost all zero or self-only singletons.
3. There is no tight training comparator with a nonzero multi-gene thalamic signature; the analog evidence is broad and its task-matched count distribution has a zero median.

I therefore forecast that the held-out `Gpr12` perturbation is a basal transcriptomic null in `151 TH Prkcd Grin2c Glut`.

`predicted_n_degs = 0`
