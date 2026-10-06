# Ap2m1 direct n_degs forecast

## Target and endpoint

- Target: `Ap2m1`.
- Cell population: `151 TH Prkcd Grin2c Glut`.
- Endpoint: number of measured genes in this perturbation/cell-population contrast with BH-adjusted Wilcoxon `pvals_adj < 0.05`.
- I used only the declared endpoint-blind `Ap2m1` biology bundle, the `151 TH Prkcd Grin2c Glut` training count table, the training expression Parquet, and training-only local annotation/corpus/profile tools. I did not query an `Ap2m1` report or profile.

## Biology prior

- Exact focal reach is high: the declared target bundle reports `Ap2m1` expression in 21,579 of 23,679 non-target 151 TH nuclei, or 91.13%, with mean log1p CP10K 1.038.
- The card argues that AP-2 mu is the sole mammalian AP-2 mu subunit, participates in neuronal cargo sorting, synaptic-vesicle reformation, and TrkB-autophagosome transport, and should be mostly lost during the P16 to P37-P44 interval because the measured neuronal-culture AP-2 mu half-life is 5.35 days and conditional ablation can reduce AP-2 below 15% in mouse hippocampal neurons.
- The same bundle cites postnatal thalamic degeneration after neuron-specific Ap2m1 loss and a mature-neuron synaptic phenotype four weeks after AAV-Cre. That makes a real cellular consequence plausible in thalamic neurons, but also makes survivor conditioning a downward pressure for the snRNA-seq DEG endpoint: the most fully depleted thalamic cells may be under-recovered.

## Training anchors

- The focal training count table contains 1,674 perturbations; it is very sparse for this cell class: median 0 DEGs, 1,205/1,674 zeros, 75th percentile 1, 90th percentile 2, and 95th percentile 18.
- AP-2 core subunits were not present as training rows, so I used the local typed analog nominations to inspect the closest available clathrin/AP-adaptor/synaptic-vesicle candidates rather than symbol matching.
- The biologically closest available AP-2/clathrin-neighbor set stayed nearly flat in the observed endpoint:
  - `Cltc`: 3
  - `Dnm1`: 1
  - `Synj1`: 1
  - `Ap1s2`: 0
  - `Ap1b1`: 1
  - `Nsf`: 0
  - `Myo6`: 0
  - `Bin1`: 1
- The 33 specific non-fallback nominations from the analog step also had a median of 0, mean 0.67, maximum 7, and 20 zeros.
- Same-experiment corpus topology over the bounded nominated cohort separated the `Cltc`/`Dnm1`/`Nsf`/`Synj1` clathrin-synaptic-vesicle block from the `Gria1`/`Gria2`/`Cacng2` AMPA-cargo block, so I treated the latter as context rather than scale-bearing AP-2 donors.
- Expansion from the report topology added a few Cltc/Nsf/Dnm1-linked stress or trafficking comparators. The closest endolysosomal subunits `Atp6v1a` and `Atp6v1e1` had 0 DEGs, `Stxbp1` and `Bin1` had 1, while `Psmb4` had 742. I treated `Psmb4`, `Psmc1`, and `Rab7` as evidence that endolysosomal/proteostatic stress can be large in this assay, but not as direct magnitude donors because their 151 TH profiles are large response-state outliers and their proximal operations are farther from AP-2 mu than the quiet clathrin/adaptor anchors.

## Synthesis

The target-specific biology pushes above a pure zero forecast: `Ap2m1` is expressed in most focal cells, has no AP-2 mu paralog, and should be functionally depleted within the assay interval. The best training-scale evidence pushes strongly downward: available clathrin/adaptor/synaptic-vesicle perturbations were 0-3 DEGs, the complete specific annotation-nominated set was mostly 0, and even two expanded V-ATPase neighbors were 0. Severe thalamic Ap2m1 loss may also be lost from the recovered-nucleus pool rather than seen as a broad survivor signature.

I therefore place `Ap2m1` just above the direct-analog median but below the high stress-state branches:

`predicted_n_degs = 3`
