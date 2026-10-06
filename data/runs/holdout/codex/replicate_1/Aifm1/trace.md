# Aifm1 forecast for 151 TH Prkcd Grin2c Glut

## Endpoint

`n_degs` is the number of measured genes in `151 TH Prkcd Grin2c Glut` with Wilcoxon BH-adjusted `pvals_adj < 0.05`.

## Evidence used

- Target: the one-row holdout manifest and canonical biology bundle both identify `Aifm1`.
- Exact focal-population reach: in matched non-target `151 TH Prkcd Grin2c Glut` nuclei, `Aifm1` was a measured gene, was detected in 15,067 of 23,679 nuclei, and had mean raw expression 1.129 UMI, mean log1p CP10K 0.453, and pseudobulk CPM 70.76. This is enough expression for a possible self-transcript call, but I did not treat self-transcript loss as a functional-knockout-strength measurement.
- Functional biology: the bundle supports AIFM1 as a mitochondrial flavoprotein needed for respiratory-chain complex-I maintenance, with a distinct stress-released death-effector pool. The stock adjudication judged a P16 disruptive edit likely to substantially deplete the relevant AIFM1-supported mitochondrial pool by P37-P44, while preserving uncertainty from pre-edit protein and complex persistence in postmitotic neurons.
- Prior timing and context: Aifm1 hypomorph phenotypes are postnatal but progressive and region-selective; the direct 1-18 day AIFM1/complex-I/complex-IV loss kinetics came from proliferating mouse fibroblasts, not thalamic neurons. I therefore used this as evidence against an absolute null, not as evidence for a guaranteed large DEG burst at 21-28 days.

## Training measurements used

The declared `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` has 1,674 training targets. It is highly sparse in this focal class: median 0 DEGs, 75th percentile 1, 90th percentile 2, 95th percentile 18, and 98th percentile 150.

I then checked the declared Parquet in the same focal group for mitochondrial perturbations closest to AIFM1's respiratory-chain role.

- Nuclear complex-I structural or assembly factors present in the training table: 23 targets, total 11 DEGs, maximum 1.
- Nuclear respiratory-chain set comprising the represented NDUF genes, COX genes, UQCR genes, `Sdha`, and `Timmdc1`: 36 targets, total 15 DEGs, maximum 1; 21/36 were zero and 15/36 were singleton calls.
- Inspecting those singleton calls in the Parquet showed that the count was almost always just the perturbed transcript itself. `Cox5a`, `Ndufa10`, `Ndufa4`, `Ndufa6`, `Ndufb10`, `Ndufb11`, `Ndufb8`, `Ndufb9`, `Ndufc2`, `Ndufs2`, `Ndufs8`, `Sdha`, `Tomm40`, and `Uqcrc2` each had the self-transcript as their only FDR<0.05 hit in `151 TH Prkcd Grin2c Glut`; only `Ndufv2` and `Uqcrq` among the checked singleton ETC perturbations had a non-self hit.
- Same-experiment packaged interpretation of `Ndufs2` agreed with the raw table: represented nuclear complex-I perturbations were broadly buffered and failed to produce a shared acute OXPHOS-stress transcriptional module in the juvenile postmitotic neuronal assay.
- The main positive mitochondrial-stress comparator was `Opa1`, with 37 DEGs in the count table and 36 non-self DEGs in the Parquet for `151 TH Prkcd Grin2c Glut`; its leading genes included `Asns`, `Mars1`, and `Chac1`, matching the packaged report's ATF4/ISR-like amino-acid stress program.
- `Nrf1` was broader at 138 DEGs, but it is a nuclear transcription factor with a noncanonical RNA/proteostasis-heavy state in the same-experiment report, so I treated it as an upper boundary rather than a close AIFM1 analogue.

## Synthesis

The count I would expect if `Aifm1` simply followed its complex-I/respiratory-chain comparators is 0-1, often just a self-transcript. The strongest reason to move above that floor is that AIFM1 loss is not a single structural subunit lesion: the biology bundle supports progressive depletion of an AIFM1-dependent mitochondrial maintenance pool by harvest and leaves open possible entry into the Opa1-like stress state that is demonstrably visible in this assay. The strongest reason not to forecast an Opa1/Nrf1-scale response is that represented complex-I and broader respiratory-chain perturbations stayed transcriptomically buffered even when their own transcripts fell.

I therefore place `Aifm1` above the pure ETC singleton regime but well below `Opa1`, with a low single-digit-to-low-teens signature as the most plausible outcome.

Point prediction: **8**.
