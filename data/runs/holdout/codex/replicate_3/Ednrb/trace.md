# Ednrb DEG-count forecast

## Target and endpoint

- Manifest target: `Ednrb`
- Cell class: `151 TH Prkcd Grin2c Glut`
- Endpoint: count of measured genes with Wilcoxon BH-adjusted `p < 0.05`

## Evidence used

1. **Declared Ednrb biology bundle**

   The card supports functional realization in receptor-positive cells but not broad aggregate reach. EDNRB is a cell-surface endothelin GPCR; a disruptive edit should remove newly synthesized ETB receptor, and ligand-occupied receptor is internalized into the endolysosomal pathway rather than simply recycled. Over P16 to P37-P44 this made substantial receptor-stock loss plausible in successfully edited cells, with only partial completeness because total receptor decay was not measured in postmitotic thalamic neurons and ligand demand in this population is unknown.

   The bundle's strongest phenotype prior is postnatal mouse spiral-ganglion degeneration in lifelong Ednrb-null animals. That supports a postnatal neuronal requirement in another sensory context, but it does not establish the effect size, latency, or cell-state coupling of a P16 somatic loss in thalamic glutamatergic neurons.

   Exact focal expression was extremely sparse: in matched non-target `151 TH Prkcd Grin2c Glut` nuclei, Ednrb had `mean_raw_umi = 0.0216225`, `pseudobulk_cpm = 1.35516`, and only `453 / 23679 = 1.913%` nuclei with any target UMI. I treated that exact in-assay reach as the dominant downward correction on otherwise plausible receptor loss.

2. **Training counts in the same cell class**

   The declared training table for `151 TH Prkcd Grin2c Glut` is strongly zero-skewed: among 1,674 observed perturbations, 1,205 had `n_degs = 0`; the median was 0, the 75th percentile was 1, the 90th percentile was 2, and large responses were rare and concentrated in unrelated chromatin, splicing, proteasome, and trafficking regulators.

   The nearest available endothelin-family perturbation, `Ednra`, had `n_degs = 0`. A hand-selected GPCR/receptor cohort with similar low-throughput signaling roles was also essentially flat in this class:

   - `Ednra`, `Avpr1a`, `Avpr1b`, `Cckar`, `Cckbr`, `Drd2`, `Drd4`, `Drd5`, `Glp1r`, `Grm5`, `Grm6`, `Grm8`, all tested `Htr` receptors, `Ntsr1`, `Oprd1`, `Oprk1`, `Oprm1`, `Sstr5`, and `Tacr3`: `n_degs = 0`
   - `Grm1`, `Grm7`: `n_degs = 1`

3. **Matched expression-parquet profile checks**

   A focal-class parquet profile comparison confirmed that `Ednra` had 0 significant measured genes among 17,259 available signed features and that 29 of the 31 receptor-family nodes above had no significant features. Ednra's nearest eligible whole-profile neighbors in the 1,674-gene training universe were generic flat profiles such as `Yeats2`, `Gsdme`, `Kat6b`, `Smarcad1`, and `Pparg`, and the highest tail-overlap neighborhoods were weak rather than a hidden large-response module.

4. **Packaged corpus on training perturbations**

   I used the same-experiment corpus only to interpret training analogs, not as independent replication. The `Ednra` cross-perturbation Finding explicitly noted no convergence between the small Ednra signature and represented endothelin/PLC/PKC/MAPK branch perturbations. Corpus expansion through flat Gq-coupled receptors pointed to `Plcb1`, `Mapk1`, `Prkca`, and `Prkcg`; their task-matched counts were `0`, `0`, `0`, and `1`, respectively.

## Synthesis

Ednrb has a real possible short-window molecular lesion, but the target-positive fraction in the assayed thalamic class is only about two percent and the closest receptor and second-messenger training perturbations are flat in the same endpoint. I therefore put almost all mass on the zero-inflated part of the focal-class training distribution rather than on the rare high-DEG tail.

`predicted_n_degs = 0`
