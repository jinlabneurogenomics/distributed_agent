# Il10rb direct n_degs forecast

## Target and endpoint

- Target: `Il10rb`.
- Cell group: `151 TH Prkcd Grin2c Glut`.
- Endpoint: `n_degs`, the count of measured genes with BH-adjusted Wilcoxon `p < 0.05` in that cell group.
- The target biology bundle had `target_outcome_exposed=false` and `labeled_neighbors_exposed=false`; I treated the same-experiment corpus and Parquet as alternate views of the declared training experiment, not as independent replication.

## Evidence used

1. Biology-only `Il10rb` bundle
   - Exact focal-population expression was very low: `Il10rb` was detected in 818 of 23,679 matched non-target nuclei, `pct_cells_expressing=3.4545`, `mean_cp10k=0.02579`, and `pseudobulk_cpm=2.4774`.
   - IL10RB is a shared, nonredundant class-II cytokine receptor accessory chain; an Il10rb edit should stop synthesis of new functional IL10RB.
   - The functional-stock adjudication called the receptor stock by harvest `partially_depleted_or_leading_edge`, because IL10RB-containing receptor complexes can undergo ligand-triggered endocytosis but existing surface molecules are not directly inactivated by the edit and no matched degradation clock was available.
   - The strongest postnatal neural loss evidence was indirect and state-mismatched: Il10rb-deficient transferred CD4 T cells failed to protect injured adult facial motoneurons at 28 days. The bundle did not establish broad, tonic Il10rb demand in healthy juvenile thalamic glutamatergic neurons.

2. Declared `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`
   - The focal training distribution was extremely zero-heavy: 1,205 of 1,674 training perturbations were zero at FDR<0.05, the median was 0, the 75th percentile was 1, and only 5% of targets exceeded 18 DEGs.
   - The assayed same-pathway and inflammatory-receptor perturbations in the focal count table were almost all flat. `Il10ra`, `Il6ra`, `Il6st`, `Ifngr1`, `Ifngr2`, `Il1rap`, `Nfkb1`, and `Stat3` each had `n_degs=0`; among 39 broad `Il*`/`Ifn*`/`Osmr`/`Stat*`/`Irf*`/`Nfkb1`/`Rel` table entries, 38 had `n_degs=0`.

3. Declared focal Parquet rows
   - A direct query of `training_de_all_cell_groups.parquet` for the same 39 cytokine/JAK-STAT/inflammatory targets in `151 TH Prkcd Grin2c Glut` reproduced the count-table flatness.
   - `Il10ra` had 0 genes at both FDR<0.05 and FDR<0.10, with its smallest adjusted p-value still 0.4323.
   - `Stat3` had 0 genes at both FDR<0.05 and FDR<0.10, with its smallest adjusted p-value 1.0.
   - The only FDR<0.05 call in the 39-target panel was one `Stat1` self-transcript hit, so this panel supplied no evidence for a recurrent downstream cytokine response in the focal thalamic class.

4. Packaged same-experiment findings for training perturbations
   - `Il10ra:F001` reported that Il10ra loss of function was transcriptionally silent at FDR<0.10 in every recovered neuronal group.
   - `Il10ra:F002` reported that expected IL-10/STAT3 inflammatory and neuronal-survival transcriptional programs were absent after Il10ra perturbation.
   - `Stat3:F002` reported that represented STAT paralogs and IL-6/IL-10/IFN/OSM receptor nodes yielded only three isolated downstream FDR<0.10 genes across 219 target-by-cell tests and did not correlate with Stat3.

## Reasoning

IL10RB is a real receptor component and the edit should eventually reduce new IL10RB supply, so I did not treat `Il10rb` as a guaranteed assay null. The direct endpoint, however, asks for a persistent survivor-conditioned snRNA-seq signature aggregated over the thalamic `151` class. The exact reach measurement is the dominant target-specific fact: only 3.45% of matched non-target nuclei showed any `Il10rb` RNA, making a whole-class FDR-significant response unlikely unless a small receptor-positive subpopulation induced a very strong, coherent program.

The endpoint-matched training perturbations argue against that rescue scenario. The ligand-binding IL-10 receptor chain `Il10ra` is the closest measured operation-level comparator for IL-10 signaling and was completely flat in this atlas and in the focal class. The broader receptor/STAT panel was also flat in `151 TH Prkcd Grin2c Glut`, including `Il6ra`, `Il6st`, `Ifngr1`, `Ifngr2`, and `Stat3`. Those are not outcome-independent biological priors; they are measured training perturbations for the same endpoint, and they show that cytokine/JAK/STAT wiring in unstimulated postnatal neurons rarely leaves a persistent DEG footprint.

I therefore anchored the forecast at the modal training value of 0. Partial receptor-stock loss and the lack of a proven compensatory beta chain add a small upward uncertainty, but the low focal expression and the flat Il10ra/Stat3 training measurements keep the integer point estimate at zero.

## Prediction

`predicted_n_degs = 0`
