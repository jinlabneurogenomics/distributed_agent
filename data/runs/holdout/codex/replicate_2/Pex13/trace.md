# Pex13 direct n_degs forecast

## Target and endpoint

The declared one-row holdout target is `Pex13`; the requested focal population is `151 TH Prkcd Grin2c Glut`, and `n_degs` is the count of measured genes with BH-adjusted Wilcoxon `pvals_adj < 0.05` in that cell class.

Used outcome-blind sources:

- `codex_runtime/pipeline/task_bindings_receipt.json` identified the target manifest `Pex13.csv`, the focal-class training count table `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`, the all-class training parquet `training_de_all_cell_groups.parquet`, and the biology-only bundle `Pex13.json`.
- `reference.perturbation_characterization.characterization_bundle(target="Pex13", view="biology")` served the same canonical bundle with `target_outcome_exposed=false` and `labeled_neighbors_exposed=false`.
- The focal training count table supplied measured `n_degs` for training perturbations only.
- The training parquet supplied exact `151 TH Prkcd Grin2c Glut` Wilcoxon rows for selected training perturbations only.
- Same-experiment corpus Findings and Claims were used only for represented training perturbations `Pex1`, `Pex14`, `Abcd3`, `Acbd5`, `Agps`, `Hsd17b4`, and `Far1`.

## Pex13 biology

The biology bundle places PEX13 in the peroxisomal membrane docking / matrix-import apparatus: PEX13 collaborates with PEX14 and PEX5 / PEX7-dependent cargo import, and loss of `Pex13` disrupts matrix import in mouse loss systems. The functional-stock card adjudicates the P16 edit as `likely_substantially_depleted` by P37-P44: the pre-existing membrane component is not erased immediately, but peroxisomes and their import machinery renew within the 21-28 day window, and acute PEX13 depletion can destabilize peroxisome homeostasis.

That is an upward bearing relative to inert or permanently installed targets. In the exact non-target nuclei for `151 TH Prkcd Grin2c Glut`, `Pex13` was also within reach of the assay: `pct_cells_expressing = 80.8607%`, `mean_raw_umi = 1.9584`, and `mean_log1p_cp10k = 0.7052`. The caveats are material: no direct P16 thalamic-neuron PEX13 half-life was available, Nestin-Cre `Pex13` neural loss is prenatal / developmental rather than an acute postmitotic edit, and the Perturb-seq readout is survivor-conditioned nuclear RNA rather than a peroxisome-import, lipid, or viability endpoint.

## Training analogues in 151 TH Prkcd Grin2c Glut

I used the represented peroxisome cohort rather than arbitrary high-DE genes, because the count table is extremely skewed and most targets are quiet: among 1,674 training targets, the median count is 0, the 75th percentile is 1, the 95th percentile is 18, and only 43 targets reach 100 or more genes.

| training target | biological role for this forecast | `n_degs` at `pvals_adj < 0.05` in 151 TH |
|---|---|---:|
| `Pex1` | peroxisome matrix-import receptor recycling, closest represented import-arm comparator | 0 |
| `Pex14` | PEX13 docking-complex partner, closest represented direct docking comparator | 1 |
| `Abcd3` | peroxisomal membrane transporter boundary | 0 |
| `Acbd5` | peroxisomal lipid-tether boundary | 0 |
| `Agps` | ether-lipid enzyme, distal sparse support | 1 |
| `Hsd17b4` | peroxisomal beta-oxidation boundary | 0 |
| `Far1` | ether-lipid enzyme, distal sparse support | 2 |

The exact parquet rows show how weak those calls were. `Pex1`, `Abcd3`, `Acbd5`, and `Hsd17b4` had zero genes below 0.05 in the focal class. `Pex14` had exactly one, its own transcript (`Pex14`, adjusted p `3.74e-07`); the next smallest adjusted p-value was 0.382. `Agps` had one focal hit, `Dhcr24`, at adjusted p `0.00192`; `Far1` had two, `Far1` and `Tial1`, at adjusted p `0.00313` and `0.0243`.

Same-experiment corpus records for these measured comparators support treating the low counts as a real local pattern rather than a missed broad peroxisome module. `Pex14:F001` reports no downstream FDR<0.10 transcript in any of 23 measured neuronal classes. `Pex1:F002` reports no nuclear peroxisome-import, lipid-metabolism, oxidative-stress, pexophagy/autophagy, ISR, or UPR module in any measured neuronal class. The peroxisome claim `claim:a3b54f2b17cb911aec15` summarizes the represented transporter, import, lipid, beta-oxidation, ether-lipid, and maintenance perturbations as predominantly flat, sparse, or target-specific rather than a shared acute neuronal transcriptomic module.

I also compared the focal 151-class score vectors for `Pex1`, `Pex14`, `Abcd3`, `Acbd5`, `Agps`, `Hsd17b4`, and `Far1` using `dataset.candidate_profile_review`. The broader pathway graph was fully connected in the corpus, but measured profile overlap was weak: pairwise Pearson correlations within the cohort were near zero, the largest among queried pairs was about 0.095, and the cohort projection found positive- and negative-tail top-feature overlap coefficient means of only 0.0357 and 0.0269. That kept the direct PEX import comparators as the main quantitative anchors and used the lipid / transporter genes only as boundaries showing that peroxisome pathway membership alone does not yield a high-count RNA state.

## Point synthesis

The most relevant observed values are therefore the direct PEX import-arm counts `[0, 1]`; the wider represented peroxisome cohort stays at `[0, 1, 0, 0, 1, 0, 2]`. PEX13 is biologically stronger than a generic distal lipid enzyme because it is a docking-complex component with likely functional-stock depletion and exact expression reach in the focal class. The measured PEX import perturbations nevertheless argue against a broad stress or peroxisome-compensation transcriptome in recovered thalamic neurons.

I therefore place `Pex13` at the singleton scale: most likely zero or one downstream gene plus possible self-transcript significance, not a multi-gene program. The integer point forecast is:

`predicted_n_degs = 1`
