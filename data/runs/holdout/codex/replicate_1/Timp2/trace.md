# Timp2 DEG-count forecast

## Target and endpoint

The manifest target is `Timp2` in `151 TH Prkcd Grin2c Glut`. The endpoint is the number of measured genes in this focal thalamic glutamatergic population with BH-adjusted Wilcoxon `pvals_adj < 0.05`.

The held-out `Timp2` differential-expression signature and held-out `n_degs` were not used. Evidence came from the declared one-row manifest, the declared `Timp2` biology bundle, the 151-class training count table, and direct Parquet rows for training perturbations in the same cell class.

## Biological prior

The exact focal-population reach in the declared biology bundle is strong: `Timp2` is detected in 18,431 of 23,679 non-target 151-class nuclei, with 77.84% expressing cells, mean CP10K 2.01, and pseudobulk CPM 198.37. Thus a loss perturbation can plausibly be assayed in this population.

The operative TIMP2 entity is a secreted extracellular/pericellular metalloproteinase regulator rather than a core intracellular transcription, splicing, ribosome, or proteasome component. The functional-stock card adjudicates that a P16 disruptive edit is likely to substantially deplete the renewable TIMP2 pool by the P37-P44 harvest, but also notes partial evidence, possible residual extracellular protein, and unmatched juvenile thalamic kinetics.

Prior neural phenotypes support observability in postnatal or adult mouse neural settings, but the closest loss evidence is cerebellar, neuromuscular, or adult hippocampal rather than this thalamic neuronal population. Together this argues for a real perturbation with only a weak or local cell-state footprint in the recovered 151-class nuclei.

## Training evidence

The declared 151-class count table is sparse: 1,205 of 1,674 training perturbations have `n_degs = 0`, 276 have `n_degs = 1`, the median is 0, the 75th percentile is 1, and the 90th percentile is 2. The high-count tail is dominated by broad cell-intrinsic regulators such as `Uba5`, `Tpr`, `Sin3a`, splicing factors, proteasome genes, and transcriptional regulators rather than extracellular matrix regulators.

The closest TIMP-family training perturbation is `Timp3`, which has `n_degs = 1` in the focal count table. Reading the same 151-class rows from the expression Parquet showed that the sole significant `Timp3` row is the self transcript (`Timp3`, log fold change -0.842, BH-adjusted p = 1.45e-6). Other extracellular, adhesion, and surface-receptor comparators were likewise nearly silent: `Adam10` 0, `Adam22` 1, `App` 1, `Epha4` 1, `L1cam` 1, `Ncam1` 1, `Nrg3` 1, `Nrxn1` 1, `Cst3` 1, `Serpine2` 2, and `Lrp6` 4. The one-count cases were self-transcript hits in the Parquet slice I inspected.

## Synthesis

Because `Timp2` is well detected in the exact focal population, a BH-significant self-transcript row is plausible even though self-knockdown is not a reliable quantitative measure of editing strength. The secreted, buffered ECM biology and the observed `Timp3`/ECM-neighbor training counts do not support assigning a broad non-self transcriptional response. I therefore forecast a lone significant gene, most likely the self transcript.

Point prediction: `n_degs = 1`.
