# Irf7 DEG-count forecast

## Target and endpoint

- **Target:** `Irf7`, the single gene in the declared holdout manifest.
- **Focal population:** `151 TH Prkcd Grin2c Glut`.
- **Endpoint:** `n_degs`, measured-gene count at BH-adjusted Wilcoxon `pvals_adj < 0.05`.
- **Point prediction:** **0**.

## Evidence used

### Canonical Irf7 biology bundle

The declared Irf7 biology bundle reports endpoint-blind perturbation context and exact in-assay reach for the focal thalamic class.

- The edited product should be functionally depleted by harvest: IRF7 is a renewable, inducible transcription factor, and the stock card concluded `likely_substantially_depleted` over the P16-to-P37/P44 interval.
- The reason to expect an Irf7 loss phenotype is challenge-gated: packaged mouse evidence supports severe systemic and CNS antiviral phenotypes, but the best neural evidence comes from viral encephalomyelitis, not an unstimulated juvenile thalamic neuron state.
- Exact focal reach was low. In matched non-target nuclei from `151 TH Prkcd Grin2c Glut`, `Irf7` was detected in **762 / 23,679 nuclei = 3.218%**, with mean raw UMI **0.04785** and mean log1p CP10k **0.02075**.

I treated those facts as supporting real loss of IRF7 capacity where the gene is expressed, but as strong downward pressure on a population-level DE count in this uninfected NeuN-positive assay.

### Focal training count table

The declared training table `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` contains 1,674 visible perturbations and does not contain `Irf7`.

Its focal-count distribution is extremely sparse:

- **1,205 / 1,674** training perturbations have `n_degs = 0`.
- median `n_degs = 0`; 75th percentile `= 1`; 90th percentile `= 2`.
- the mean, 14.05, is dominated by a long tail of large housekeeping or broad regulatory responses, so I did not use the mean as a local expectation for an inducible interferon factor.

The visible innate immune / interferon-axis training genes nearest to the Irf7 operation were also silent in this exact cell class. `Irf1`, `Irf2`, `Irf3`, `Irf5`, `Irf8`, `Irf9`, `Stat2`, `Ifnar1`, `Ifnar2`, `Traf3`, `Nfkb1`, `Ifih1`, `Map3k7`, `Tlr3`, and `Tlr7` all have **0** DEGs in `151 TH Prkcd Grin2c Glut`; `Stat1` has **1**.

### Same-experiment corpus and profile checks

The July same-experiment Finding ledger independently interprets the same Perturb-seq measurements semantically, so I used it as interpretation of the training surface rather than as replication. I queried visible genes only. Its negative and pathway-uncoupling Findings for `Ifih1`, `Ifnar1`, `Ifnar2`, `Irf1`, `Irf2`, `Irf3`, `Irf5`, `Irf8`, `Irf9`, `Nfkb1`, `Stat1`, and `Stat2` consistently describe a basal postmitotic neuronal setting in which IFN/ISG, IRF, IFNAR-JAK/STAT, TLR, and NF-kB outputs are absent or singleton-flat rather than forming a hidden interferon module.

I then compared the 15 visible pathway genes
`Irf1`, `Irf2`, `Irf3`, `Irf5`, `Irf8`, `Irf9`, `Stat1`, `Stat2`,
`Ifnar1`, `Ifnar2`, `Traf3`, `Nfkb1`, `Ifih1`, `Tlr3`, and `Tlr7`
against each other in the focal group using `training_de_all_cell_groups.parquet`.
The profile comparison wrote `evidence/interferon_axis_profile_compare.json`;
14 of 15 nodes had no BH<0.05 significant features and the remaining node
was in the 1-to-9 significant-feature bin. The cohort projection
`evidence/interferon_axis_cohort.json` found no shared recurrent significant
program across all 105 visible pairs.

## Synthesis

An Irf7 edit should clear a short-lived transcription-factor stock, so I did
not call this a failed perturbation. The forecast is low because the target is
rarely detected in the assayed focal neurons, and because the nearest visible
losses throughout the basal viral-sensing, IFNAR, STAT/IRF, and NF-kB network
have almost no corrected transcriptional output in exactly this thalamic
population. The same-experiment corpus interprets this as quiescent,
stimulus-gated interferon circuitry rather than as one idiosyncratic silent
gene. A viral or exogenous type-I-IFN challenge could make Irf7 loss visible,
but that is outside the P16 sparse CRISPR, unchallenged, NeuN-enriched readout.

I therefore predict the held-out BH<0.05 DEG count for `Irf7` in
`151 TH Prkcd Grin2c Glut` as the modal and biologically matched value:

**0**

No held-out Irf7 perturbation signature, Irf7 DEG count, scalar-prior artifact,
relationship-review artifact, branch-calibration artifact, terminal-prediction
artifact, or calibrated response probability was used.
