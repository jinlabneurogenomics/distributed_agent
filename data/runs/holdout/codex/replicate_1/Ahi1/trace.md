# Direct forecast trace

## Target and endpoint

- Target: `Ahi1`
- Focal population: `151 TH Prkcd Grin2c Glut`
- Endpoint: `n_degs`, the number of measured genes with BH-adjusted Wilcoxon `p < 0.05`
- Declared count table: `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`
- Declared expression table: `[local file: training_de_all_cell_groups.parquet]`
- Ahi1 biology bundle: `[local file: Ahi1.json]`
- Run-local profile comparison: `workbench/ahi1_ciliary_signal_profile_compare.json`
- Run-local profile cohort diagnostic: `workbench/ahi1_ciliary_signal_profile_cohort.json`

## Target biology used

The run-local Ahi1 characterization bundle places Ahi1 at two relevant but non-nuclear operations:

- a ciliary transition-zone/ciliary trafficking component required for neuronal ciliary MCHR1 localization and signaling;
- a neuronal endocytic/trafficking scaffold coupled to HAP1 and TrkB signaling.

The exact focal-population expression reach argues that Ahi1 is not absent from the assay: in non-target nuclei for `151 TH Prkcd Grin2c Glut`, Ahi1 was detected in 21,822 of 23,679 cells, `92.1576%`, with mean raw UMI `3.3923` and mean log1p CP10k `1.0404`.

The functional-stock card was the main downward modifier. It adjudicates the expected P16-to-P37/P44 edit as `partially_depleted_or_leading_edge`: the edit should stop new Ahi1 supply, but pre-existing cytoplasmic, trafficking, ciliary, and transition-zone pools are not directly inactivated. Generic mouse-brain protein renewal makes substantial loss of the dynamic pool plausible over 21-28 days, yet the Ahi1-specific half-life and persistence of installed ciliary/transition-zone material are unknown. The retinal and Nestin-Cre mouse phenotypes show that Ahi1 loss can matter in postnatal neural tissue, but they do not provide a transferable thalamic, acute-P16 transcriptional latency.

## Training measurements used

The `151 TH Prkcd Grin2c Glut` training endpoint is zero-inflated overall:

- 1,674 measured training targets
- 1,205 with `n_degs = 0`
- median `n_degs = 0`
- 75th percentile `n_degs = 1`
- 90th percentile `n_degs = 2`

I treated ciliary/transition-zone trafficking genes as the closest operation-matched measured analogs and the HAP1/NTRK2/MCHR1/MTOR genes as Ahi1-pathway context rather than direct equal-scale analogs. Their observed focal-class counts were:

```tsv
target_name	n_degs
Alms1	0
Arl2bp	0
Arl3	1
B9d1	0
Bbs5	0
Cep120	0
Cep290	0
Cltc	3
Dync2h1	0
Dync2i1	0
Gpr161	0
Hap1	0
Ift43	0
Ift81	0
Ift88	0
Lztfl1	0
Mchr1	0
Mtor	2
Ntrk2	3
Rpgrip1l	0
Rptor	0
Smo	0
Ttc8	1
Ttc21b	0
Ulk4	0
```

That 25-gene set had 20 zero-count perturbations, mean `n_degs = 0.4`, median `0`, and maximum `3`. The most direct ciliary comparators were even quieter: the Joubert/ciliary genes available in the count table were nearly all 0, with Arl3 and Ttc8 contributing isolated one-gene calls.

I then checked the same 25 perturbations in the declared Parquet with `dataset.candidate_profile_review` in exactly the focal population. All 25 profiles were present. The profile comparison found:

- 20 profiles with `no_significant_features`;
- 5 profiles with `1_to_9_significant_features`;
- no positive significant-program overlap in the selected cohort;
- no negative significant-program intersection among the 10 cohort pairs where both sides had a negative significant program.

The actual significant rows in this selected set were tiny and mostly self or local:

```tsv
gene_target	names	logfoldchanges	pvals_adj
Arl3	Arl3	-0.41779235	0.01835715721566928
Cltc	Rbms1	-1.1221862	0.042390361913415865
Cltc	Ero1b	-1.0040445	0.042390361913415865
Cltc	Gabra4	-0.63266313	0.042390361913415865
Mtor	Rims3	0.30039328	0.018509902287627666
Mtor	Tmed8	-0.8212863	0.02650336546068287
Ntrk2	Ntrk2	-0.42717528	0.000023300466953753727
Ntrk2	Atp2a2	-0.23030926	0.0023719158105791854
Ntrk2	Vgf	-0.6180336	0.004884795266084866
Ttc8	Ttc8	-0.66312397	0.000030688786216884106
```

## Synthesis

Ahi1 has enough focal expression that a CRISPR perturbation can be observed in principle, so I did not force a structural zero. However, the closest measured biology says that acute perturbation of ciliary assembly/trafficking genes in the same thalamic class is usually transcriptionally silent or self-only at FDR 0.05. Ahi1 is a localized trafficking/transition-zone scaffold rather than a transcription factor, spliceosome component, proteasome subunit, or other global expression regulator, and the declared functional-stock card leaves a realistic residual installed pool at harvest.

The strongest upward uncertainty is an isolated Ahi1 self-transcript call or a small post-transcriptional signaling response analogous to the `Ntrk2`, `Mtor`, or `Cltc` counts of 2-3. The direct ciliary cohort and profile check put most probability on no broader downstream signature, so my point forecast is:

`predicted_n_degs = 0`
