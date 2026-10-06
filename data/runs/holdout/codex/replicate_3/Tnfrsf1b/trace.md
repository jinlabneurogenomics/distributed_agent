# Tnfrsf1b n_degs forecast

## Endpoint

- Target: `Tnfrsf1b`
- Cell class: `151 TH Prkcd Grin2c Glut`
- Quantity predicted: count of measured genes with Wilcoxon BH-adjusted `p < 0.05`.
- I treated the declared same-experiment Parquet, training count table, and profile summaries as one measurement source, not as independent replication. I did not use a `Tnfrsf1b` outcome or signature.

## Evidence used

### Target biology and focal reach

The declared biology-only characterization bundle for `Tnfrsf1b` says TNFR2 is a plasma-membrane TNF receptor that can bind TRAF2 and is best modeled as a renewable signaling component rather than a durable installed stock. Its functional pool is therefore likely to be substantially depleted after P16 editing by the P37-P44 harvest window, although the turnover evidence is only partial because the shedding result is heterologous and ligand-stimulated.

The same bundle also marks the observable neuronal prior as context-mismatched. Neuron-specific TNFR2 loss has postnatal mouse evidence in hippocampal excitotoxic challenge, and germline `Tnfrsf1b` loss has a P0 sensory-root glial phenotype, but neither is an unchallenged thalamic glutamatergic-neuron phenotype.

The exact in-assay non-target expression reach was very low:

- `n_non_target_cells`: 23,679
- `n_cells_expressing`: 120
- `pct_cells_expressing`: 0.506778%
- `pseudobulk_cpm`: 0.336143
- `mean_raw_umi`: 0.005363

That exact reach superseded broad qualitative expression priors and made a large recovered-nucleus transcriptional footprint unlikely unless sparse TNFR2-positive nuclei non-cell-autonomously or state-inductively drove a broader program.

### Training counts in the focal population

The declared `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` table contains 1,674 observed training perturbations and excludes `Tnfrsf1b`. Its count distribution is zero-inflated:

- 1,205 / 1,674 targets have `n_degs = 0`.
- Median `n_degs` = 0.
- 75th percentile = 1.
- 90th percentile = 2.
- 95th percentile = 18.

Thus the focal cell class has a large response tail, but the modal and median perturbation are silent at this BH threshold.

Available TNF/NF-kB-axis training perturbations in the same count table were also silent:

| training target | `n_degs` |
| --- | ---: |
| `Tnfrsf1a` | 0 |
| `Tnfrsf11a` | 0 |
| `Tnfrsf13c` | 0 |
| `Tnfrsf4` | 0 |
| `Tnfrsf9` | 0 |
| `Traf3` | 0 |
| `Map3k7` | 0 |
| `Chuk` | 0 |
| `Nfkb1` | 0 |
| `Rel` | 0 |

`Tnf`, `Traf2`, `Traf6`, `Rela`, `Relb`, and `Ripk1` were not in the training count table. A matched profile comparison over the six closest available receptor-to-transcription-factor TNF/NF-kB nodes (`Tnfrsf1a`, `Traf3`, `Map3k7`, `Chuk`, `Nfkb1`, `Rel`) in the expression Parquet confirmed that all six had `response_activity_status = no_significant_features` and `significant_feature_count = 0` over 17,259 shared measured genes.

## Synthesis

`Tnfrsf1b` loss should remove newly supplied TNFR2 by the assay timepoint, so I did not treat it as an uneditable long-lived stock. The limiting evidence was instead context and reach: only about 0.5% of baseline focal nuclei expressed the transcript, adult thalamic regional evidence was low, and the strongest neuronal function for TNFR2 is under excitotoxic inflammatory challenge rather than the basal survivor-conditioned Perturb-seq state.

Training measurements agreed with that downward bearing. Every measured TNFR-superfamily receptor in the focal count table had zero DEGs, and the available downstream TNF/NF-kB signaling perturbations also had zero DEGs when checked in the matched Parquet context. That made the most biologically local training evidence the zero-count part of the distribution rather than the high-yield spliceosome/proteasome/transcriptional tail.

I therefore predict the modal silent outcome:

`predicted_n_degs = 0`
