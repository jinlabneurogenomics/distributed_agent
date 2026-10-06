# Kcnq5 n_degs prediction trace

## Endpoint

- Target: `Kcnq5`
- Cell group: `151 TH Prkcd Grin2c Glut`
- Endpoint: `n_degs`, the number of measured genes with BH-adjusted Wilcoxon `pvals_adj < 0.05`
- Point prediction: `1`

## Evidence used

1. Declared Kcnq5 biology bundle

   - The exact focal-population expression card reports detectable but limited `Kcnq5` expression in the matched non-target nuclei of `151 TH Prkcd Grin2c Glut`: 4,350 / 23,679 cells expressing, 18.3707%, mean CP10K 0.2133, and pseudobulk CPM 21.25.
   - The functional-stock adjudication calls KCNQ5 a dynamic membrane-channel component whose existing stock should be substantially depleted by the P37-P44 harvest after a P16 disruptive edit. The strongest timing evidence is endogenous KCNQ5 protein loss within about 10-12 days after AAV-SaCas9 editing in primary mouse hippocampal neurons; the bundle keeps residual uncertainty because no thalamic in vivo half-life was available.
   - The observability card supports a real single-gene phenotype despite KCNQ2/KCNQ3 paralogs, but the demonstrated phenotypes are hippocampal or pallidal channel physiology rather than an acute `151 TH` transcriptional state.

2. Declared `151 TH Prkcd Grin2c Glut` training counts

   - `Kcnq5` is absent from the 1,674-row training count table.
   - The training distribution is very sparse in this cell group: median 0, 75th percentile 1, 90th percentile 2, 1,481 / 1,674 targets at `n_degs <= 1`, and only 78 / 1,674 targets above 20.
   - The closest represented Kv7 perturbations in the same count table were tiny: `Kcnq1 = 0`, `Kcnq2 = 1`, and `Kcnq3 = 1`.
   - The broader channel/receptor context was also near-null in this group: `Hcn1 = 0`, `Hcn2 = 1`; sodium-channel pore/subunit targets ranged from 0-2; most potassium-channel targets were 0-1; high-voltage calcium-channel relatives were mostly 0-1. `Cacna1g = 12` and `Grin1 = 89` were positive outliers rather than the rule for ion-channel genes.

3. Declared expression parquet checks on matched training perturbations

   - In `151 TH`, the sole significant rows for `Kcnq2` and `Kcnq3` at `pvals_adj < 0.05` were their self-transcripts. `Hcn2`, `Kcnab2`, `Kcnc2`, `Kcnc3`, `Kcnma1`, `Scn1a`, `Scn2a`, and `Scn8a` likewise had exactly one significant row, the perturbed channel transcript itself.
   - `Scn1b` had two significant rows, the self-transcript plus `Jun`.
   - `Cacna1g` was the main thalamic channel exception, with 12 significant rows, including the self-transcript and 11 downstream features.

4. Same-experiment corpus summaries for training comparators

   - The Kcnq2 and Kcnq3 reports explicitly interpret represented Kv7-family perturbations as sparse and paralog-specific rather than a shared `Kcnq1`/`Kcnq2`/`Kcnq3` transcriptional program.
   - The Hcn2 report describes a channel perturbation with target mRNA decreases in many recovered groups but no non-Hcn2 downstream FDR calls.
   - The Cacna1g report records a real thalamus-restricted CaV3.1 response, while emphasizing that it did not phenocopy represented voltage-gated calcium-channel relatives and should not be read as a generic calcium-channel knockdown signature.

## Synthesis

KCNQ5 is an expressed, renewable Kv7 pore subunit, so the perturbation is not a biological null. The in-assay reach is only low to moderate, however, and the most proximal functional evidence is channel physiology outside the target thalamic class. The matched perturbation table says that acute sparse loss of electrical channel subunits usually leaves resting snRNA either flat or with only the self-transcript detectable in `151 TH`; this includes the closest Kv7 comparators `Kcnq2` and `Kcnq3`, both at one significant measured gene in this exact endpoint.

I therefore place `Kcnq5` above a pure zero but far below the `Cacna1g`/`Grin1` outliers. The most likely visible event is a single self or sentinel transcript rather than a coordinated downstream program.

## Prediction

`predicted_n_degs = 1`
