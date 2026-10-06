# Question and resolved ambiguity

The requested readout is the integer `n_degs` for each held-out CRISPR target in `151 TH Prkcd Grin2c Glut`: the number of measured genes with Benjamini-Hochberg adjusted Wilcoxon `pvals_adj < 0.05` in perturbed nuclei versus matched controls. The manifest for this run contains one target:

```tsv
target_name
Trpv4
```

`Trpv4` is held out as a perturbation target, so no `Trpv4` knockout signature or `Trpv4` row in the focal training count file is available. I treated the task as a same-assay transfer problem, not as a request to score biological importance in another model, and predicted a point count for the basal postnatal sparse AAV CRISPR/snRNA-seq context only.

# Sources used

- Input endpoint counts: `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
- Input expression statistics: `[local file: training_de_all_cell_groups.parquet]`, filtered to `group_name == "151 TH Prkcd Grin2c Glut"` for direct focal-cell comparisons.
- Requested-target manifest: `[local file: 248_Trpv4.csv]`.
- Same-experiment Distributed Agents corpus, release `perturbai-july-260713-sourceguard-1773-v1`. `Trpv4` itself had no target-centered claims or findings, but `Trpa1`, `Trpm3`, `Trpm7`, and `Trpv1` did.
- PubMed literature on TRPV4 biology: Mizuno et al. 2003, DOI `10.1152/ajpcell.00559.2002`; Filosa et al. 2013, DOI `10.1097/FJC.0b013e318279ba42`; Harraz et al. 2018, DOI `10.7554/eLife.38689`; Hoshi et al. 2018, DOI `10.1523/JNEUROSCI.2888-17.2018`; Pivonkova et al. 2018, DOI `10.1016/j.neuroscience.2018.10.028`; Hu et al. 2023, DOI `10.1172/JCI161507`; Sullivan et al. 2024, DOI `10.1126/scitranslmed.adk1358`.

# Computation over the training data

I first summarized the focal training endpoint to calibrate response size. Among 1,674 non-held-out targets in `151 TH Prkcd Grin2c Glut`, the median `n_degs` was 0, 1,205 targets were exactly 0, the 75th percentile was 1, the 90th percentile was 2, and only the strongest broad responders such as `Uba5`, `Tpr`, `Sin3a`, `Rnpc3`, `Zbtb7a`, and `U2af2` had hundreds to thousands of DEGs. Thus the empirical prior for a channel-like target with no strong matched evidence is 0 rather than a small positive count.

I then looked for direct and near-direct channel comparators in the observed target list. There were no `Piezo*` perturbations. The represented TRP-family perturbations in the focal endpoint were:

```tsv
target	n_degs
Trpa1	0
Trpm3	0
Trpm7	0
Trpv1	0
```

`Trps1` had 3 DEGs but was rejected as an analog because it is a transcriptional regulator, not a TRP channel. Other neuronal channel subfamilies were also mostly silent in the focal endpoint: `Kcna1`, `Kcna2`, `Kcnb1`, `Kcnb2`, `Kcnc1`, `Kcnd3`, `Kcnh1`, `Kcnh5`, `Kcnj6`, `Kcnn2`, `Kcnn3`, `Kcnt1`, `Kcnt2`, `Cacna1a`, `Cacna1d`, `Cacna1e`, `Cacna2d2`, `Cacnb2`, `Cacng2`, `Cacng3`, `Scn3a`, and all assayed `Gria*` targets had 0 DEGs. Several channel genes produced 1-2 DEGs, `Cacna1g` produced 12, and the main positive counterexample was `Grin1` with 89 DEGs. I used `Grin1` as a bound showing that this cell group can respond transcriptionally to a core excitatory receptor subunit, but it is a poor mechanistic match for TRPV4 because `Grin1` is an obligatory NMDA receptor subunit whereas TRPV4 is not a defining synaptic receptor of the `Grin2c` glutamatergic population.

To confirm the direct TRP counts in the parquet rather than only in the count CSV, I scanned focal rows for `Trpa1`, `Trpm3`, `Trpm7`, `Trpv1`, and `Trps1`. Each target had 17,259 measured genes. The four TRP-channel anchors had zero `pvals_adj < 0.05` genes in this cell group:

```tsv
target	n_pert_matched	n_ctrl_matched	min_padj	fdr_lt_0.05
Trpa1	191	23679	1.00000	0
Trpm3	154	23679	0.14584	0
Trpm7	81	23679	1.00000	0
Trpv1	187	23679	1.00000	0
```

I also computed a run-local Distributed Agents profile-neighbor artifact comparing `Trpa1`, `Trpm3`, `Trpm7`, and `Trpv1` against all 1,674 focal profiles using signed `logfoldchanges` over `names`, retaining the top 200 positive and negative tail genes. Each anchor's profile had `significant_feature_count = 0`, and the nearest-tail overlaps involved only low-significance rank structure rather than FDR-passing genes. I therefore used those profiles as null anchors rather than as positive neighbors for `Trpv4`.

# Target-specific reasoning

## Trpv4

`Trpv4` encodes a calcium-permeable, nonselective TRP channel responsive to cell swelling/osmotic and mechanical stimuli. Mouse knockout work established an osmotic role for TRPV4 in the brain and arginine vasopressin physiology (Mizuno et al. 2003, DOI `10.1152/ajpcell.00559.2002`). In the CNS literature, however, many prominent TRPV4 effects are localized to non-neuronal or injury/evoked contexts: astrocytic endfeet and vascular tone (Filosa et al. 2013, DOI `10.1097/FJC.0b013e318279ba42`), brain capillary endothelium (Harraz et al. 2018, DOI `10.7554/eLife.38689`), edema after ischemia or traumatic injury (Hoshi et al. 2018, DOI `10.1523/JNEUROSCI.2888-17.2018`), astrocyte swelling/volume regulation with reported rare adult astrocytic TRPV4 expression in situ (Pivonkova et al. 2018, DOI `10.1016/j.neuroscience.2018.10.028`), spinal microglia in neuropathic pain (Hu et al. 2023, DOI `10.1172/JCI161507`), and neural vascular endothelial cells in gain-of-function TRPV4 channelopathy (Sullivan et al. 2024, DOI `10.1126/scitranslmed.adk1358`). Those roles do not match a basal, whole-brain-minus-hindbrain, NeuN-enriched neuronal nuclei assay with sparse acute loss of function and no osmotic, mechanical, ischemic, inflammatory, or peripheral sensory challenge.

The most relevant measured analogs argue for no broad basal signature:

- `Trpv1`: 0 DEGs in this focal cell group, 187 perturbed nuclei. The same-experiment corpus finding `Trpv1:F005` reports that `Trpa1`, `Trpm3`, and `Trpm7` did not phenocopy `Trpv1`, and that represented thermoTRP/channel relatives did not reveal a generic TRP or endovanilloid transcriptional module.
- `Trpa1`: 0 DEGs, 191 perturbed nuclei. Corpus finding `Trpa1:F001` calls `Trpa1` a robust central-neuron negative result across recovered groups, and `Trpa1:F003` reports no shared central signature with the nociceptor relatives `Trpv1`, `Trpm3`, `Ntrk1`, or `Ret`.
- `Trpm3`: 0 DEGs in the focal group, 154 perturbed nuclei. Corpus finding `Trpm3:F003` reports that neither phenotype-first neighbors nor TRP/Ca2+ pathway relatives phenocopied `Trpm3`; the `Trpm3` program was not a generic TRP-channel or Ca2+-signaling transcriptomic state.
- `Trpm7`: 0 DEGs in the focal group, 81 perturbed nuclei. Corpus finding `Trpm7:F003` similarly reports no convergence with represented TRP or magnesium-homeostasis relatives.
- `Cacna1e`, `Cacna1a`, `Cacna1d`, most `Kcn*` potassium-channel targets, and most assayed sodium, AMPA, kainate, and calcium-channel auxiliary subunits were also 0 or nearly 0, so the dataset does not show that perturbing an ion channel generically creates a focal transcriptional response.
- `Grin1`, with 89 DEGs, is the counterexample I considered most carefully. It shows that the endpoint can detect a receptor perturbation in this cell type, but its NMDA-receptor role in a `Grin2c` glutamatergic neuronal population is much more proximal to neuronal state than TRPV4's vascular/glial/mechanosensory biology.

The zero/nonzero decision is therefore driven mostly by same-assay evidence: every observed TRP-channel comparator had no FDR-significant genes in the focal group and the internal same-experiment corpus rejects a shared basal TRP-channel module in sampled central neurons. External biology pushes the same way because the best documented TRPV4 transcriptional consequences are expected in astrocytes, endothelium, microglia, chondrocytes, peripheral sensory systems, disease gain-of-function, or injured/evoked conditions that this assay did not sample. I predict `Trpv4` will be a focal-cell null.

Point prediction: `Trpv4 = 0`.

# Limits

This is an extrapolation because the closest vanilloid paralogs `Trpv2`, `Trpv3`, `Trpv5`, and `Trpv6` were not perturbation targets in the training set, and `Trpv4` itself has no same-experiment Distributed Agents target context. Loss of TRPV4 could affect electrophysiology, Ca2+ entry, osmotic sensing, vasculature-neuron coupling, or injury responses without changing the basal nuclear transcriptome. The NeuN+ enrichment removes many of the astrocytic, microglial, vascular, and barrier cells in which TRPV4 is often studied, so the prediction should not be read as saying that TRPV4 is unimportant in the brain. It is only a prediction that sparse postnatal neuronal `Trpv4` loss will not push any gene below the stringent focal Wilcoxon FDR cutoff.
