# Trace

## Question and endpoint

The requested prediction is the integer `n_degs` for the held-out perturbation `Cacna1c` in `151 TH Prkcd Grin2c Glut` thalamic glutamatergic neurons. I treated `n_degs` exactly as defined in the prompt: the number of measured genes with Scanpy Wilcoxon Benjamini-Hochberg `pvals_adj < 0.05` in perturbed recovered nuclei versus matched controls. The held-out `Cacna1c` expression signature and count were absent from the supplied Parquet and count CSV, so the endpoint for this target is absent from the declared inputs and had to be inferred from held-in perturbations plus calcium-channel biology.

The requested-target manifest was an unranked one-column CSV and contained a single target, `Cacna1c`; I preserved that exact order in `answer.txt`.

## Sources used

- Declared differential-expression Parquet: `training differential-expression dataset`. This was the direct within-experiment source for per-gene log fold changes, Wilcoxon scores, BH-adjusted p-values, and matched nucleus counts.
- Declared focal training counts: `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`. This was the direct within-experiment source for held-in `n_degs` at FDR 0.05 in the focal cell group.
- Declared requested target CSV: `single-target request for Cacna1c`.
- Run-local task bindings, coverage, capability manifest, and measurement registry under `codex_runtime/pipeline`.
- The same-experiment PerturbAI July 260713 sourceguard 1773 v1 corpus, via `corpus.report_evidence`, for the packaged Cacna1d, Cacna1g, and Grin1 evidence records. I used it as curated interpretation of the same Parquet surface, not as independent replication.
- External mechanism literature retrieved through PubMed:
  - Berger and Bartsch 2014, Cell and Tissue Research, DOI `10.1007/s00441-014-1936-3`, PubMed `24996399`: Cav1.2/Cacna1c and Cav1.3/Cacna1d are the major neuronal L-type alpha-1 channels and have overlapping but nonidentical roles in brain signaling and plasticity.
  - Baker, Lee, and Rajadhyaksha 2023, Channels, DOI `10.1080/19336950.2023.2176984`, PubMed `36803254`: CACNA1C and CACNA1D L-type channels couple calcium influx to neuronal development, differentiation, migration, and neuropsychiatric disease mechanisms.
  - Wheeler et al. 2012, Cell, DOI `10.1016/j.cell.2012.03.041`, PubMed `22632974`: Cav1 channels are privileged sources for local CaMKII aggregation and CREB-dependent gene expression relative to Cav2 channels.
  - Kim et al. 2001, Neuron, DOI `10.1016/S0896-6273(01)00343-9`, PubMed `11498049`: Cacna1g/Cav3.1 T-type channels are required for thalamocortical rebound burst firing, supporting the interpretation that Cacna1g is a thalamic low-voltage channel counterexample rather than a direct L-type analog.

## Within-dataset computations

1. I read the focal count CSV to get the background scale. It contained 1,674 held-in perturbations. The distribution was sparse: median 0 DEGs, 75th percentile 1 DEG, 90th percentile 2 DEGs, 95th percentile 18 DEGs, and 469/1,674 perturbations had any FDR 0.05 DEG.
2. I selected voltage-gated calcium-channel alpha-1, beta, alpha2/delta, and gamma subunits represented in training and checked their focal `n_degs`: `Cacna1a` 0, `Cacna1d` 0, `Cacna1e` 0, `Cacna1g` 12, `Cacna2d1` 1, `Cacna2d2` 0, `Cacnb2` 0, `Cacnb4` 1, `Cacng2` 0, `Cacng3` 0.
3. I also checked adjacent calcium/excitatory signaling perturbations to calibrate how a real focal calcium-dependent response can look: `Grin1` had 89 DEGs, `Grin2a` 1, `Grin2b` 2, `Calm1` 14, `Calm2` 0, `Calm3` 1, `Camk2a` 0, `Camk2b` 1, `Camk2g` 0, `Ppp3ca` 4, `Ppp3r1` 9, `Creb1` 10, and `Crebbp` 8.
4. From the Parquet I pulled exact `151 TH Prkcd Grin2c Glut` rows for the calcium-channel and comparator perturbations and recomputed FDR 0.05 counts from `pvals_adj`. This confirmed that `Cacna2d1` and `Cacnb4` were self-transcript-only at FDR 0.05 in the focal class; excluding the target transcript, every represented non-`Cacna1g` calcium-channel subunit perturbation had 0 downstream DEGs in this cell type.

## Cacna1c reasoning

`Cacna1c` encodes Cav1.2, a high-voltage L-type calcium-channel alpha-1 pore subunit. The closest held-in perturbation was `Cacna1d`/Cav1.3, the other principal neuronal L-type channel. It is the best within-dataset analog because it shares the same channel class and postsynaptic L-type calcium entry route implicated in CaMKII/CREB coupling, whereas `Cacna1g` is a low-voltage T-type thalamic channel and `Cacna1a`/`Cacna1e` are Cav2 presynaptic channels.

Key focal analogs and counterexamples were:

| held-in perturbation | observed focal `n_degs` | exact focal Parquet evidence | interpretation for `Cacna1c` |
| --- | ---: | --- | --- |
| `Cacna1d` | 0 | 160 perturbed nuclei versus 23,679 controls; all 17,259 measured rows had `pvals_adj >= 1.0` in the focal class | Strongest L-type alpha-1 analog; absence of even near-threshold rows argues that partial acute loss of an L-type channel was transcriptomically silent in this class. |
| `Cacna1a` | 0 | 117 perturbed nuclei; lowest FDR 0.415 | High-voltage P/Q-type presynaptic alpha-1 channel; less direct than L-type but supports the general quietness of Cav pore perturbations. |
| `Cacna1e` | 0 | 144 perturbed nuclei; lowest FDR 0.718 | R-type Cav2 alpha-1 channel; another high-voltage pore counterexample with no focal DEG response. |
| `Cacna2d1` | 1 | the only FDR 0.05 row was `Cacna2d1` itself, logFC -0.392, FDR `6.02e-07` | Auxiliary alpha2/delta perturbation engaged its transcript but did not create a downstream focal program. |
| `Cacnb4` | 1 | the only FDR 0.05 row was `Cacnb4` itself, logFC -0.363, FDR `9.84e-05` | Beta-subunit self row only; not a downstream cell-state response. |
| `Cacnb2`, `Cacna2d2`, `Cacng2`, `Cacng3` | 0 | focal `n_degs` all 0 | Additional channel-associated subunits were quiet in the same endpoint. |
| `Cacna1g` | 12 | 264 perturbed nuclei; 12 FDR 0.05 rows including `Ptprn` up, `Cacna1g` down, `Stmn4`, `Cpne7`, `Jun`, `Zdhhc22`, and `Lrrc7` down | Positive thalamic counterexample; it shows the assay can detect an ion-channel perturbation in 151 TH cells, but Cacna1g/Cav3.1 supports T-type rebound bursting in thalamocortical neurons rather than the L-type Cav1.2/Cav1.3 pathway. |
| `Grin1` | 89 | 247 perturbed nuclei; robust self down-regulation and broad synaptic/plasticity/stress-linked response | Positive excitatory-signaling control; it demonstrates that the focal class can mount an NMDA-receptor-linked response, but the obligatory GluN1 subunit is not a one-to-one analog for Cav1.2. |

The same-experiment Cacna1d report extended the focal observation: across 21 measured neuronal groups Cacna1d had only two downstream rows at FDR 0.10, its own transcript was FDR 1.0 in all 21 groups, and canonical calcium-regulated immediate-early, UPR, ISR, and autophagy markers were not robustly changed. The Cacna1g report provided the reciprocal comparison: its only robust downstream response was in `151 TH Prkcd Grin2c Glut`, and represented voltage-gated calcium-channel relatives did not reproduce that Cacna1g thalamic signature. I therefore treated Cacna1g as a sign that this thalamic cell type is capable of detecting a relevant Cav perturbation when the channel matches the circuit role, not as evidence that every Cav alpha-1 subunit should be nonzero.

The causal transfer model was:

`Cacna1c` CRISPR loss of function -> reduced Cav1.2-mediated L-type calcium entry at excitable membranes -> possible reduction of local CaMKII/CREB and activity-dependent transcription -> sampled survivor 151 TH nuclei 3-4 weeks after P16 AAV -> FDR 0.05 snRNA differential expression.

External literature supports the first three molecular links for Cav1.2 in neurons, but the held-in screen shows that this cascade did not turn into a broad FDR-significant nuclear RNA phenotype for the closest Cav1.3/L-type perturbation or for P/Q-, R-, alpha2/delta-, beta-, and gamma-channel perturbations in the focal group. The most likely explanation is that postnatal sparse Cav1.2 loss in this class is buffered, is functionally redundant with other calcium-entry routes, or changes electrophysiology/synaptic calcium without crossing the experiment's bulk single-nucleus FDR threshold.

I assigned `Cacna1c` a point prediction of 0 rather than 1-12 because the one-gene calcium-subunit counts in training were self-transcript artifacts and the only true downstream Cav family response was the mechanistically distinct thalamic T-type `Cacna1g` case. A value above the Cacna1d/Cacna1a/Cacna1e zero cluster would require assuming Cav1.2 is substantially less buffered than Cav1.3 in this exact class, but none of the internal analogs supported that.

## Limits and uncertainty

- `Cacna1c` itself was held out, so no Cacna1c matched nucleus count, target-transcript row, or expression signature was available.
- The DEG count is an assay-power endpoint. A zero prediction is not a claim that Cav1.2 is biologically irrelevant, unedited, or unexpressed; it only predicts no genes passing BH FDR 0.05 in recovered `151 TH Prkcd Grin2c Glut` nuclei.
- External Cav1.2/Cav1.3 literature mostly studies germline variants, conditional knockouts, pharmacology, or cultured/cortical systems. The requested experiment was acute, sparse AAV CRISPR in postnatal neurons and measured nuclear RNA rather than calcium transients, firing, synaptic plasticity, or survival before sorting.
- The input Parquet contains DE summaries, not raw UMIs or indel rates, so I could not test whether Cacna1c and Cacna1d are equally edited or equally expressed in the focal class.
- Cacna1g remains the main counterexample: a calcium-channel pore subunit can be detected in this exact focal class. I down-weighted transfer from Cacna1g only because its low-voltage Cav3.1 thalamic rebound-bursting role is channel-class and circuit specific, whereas `Cacna1c` is an L-type Cav1 analog whose closest held-in L-type neighbor was flat.
