# Psmc5 n_degs forecast

Target and endpoint:

- Target: `Psmc5`
- Cell class: `151 TH Prkcd Grin2c Glut`
- Endpoint: measured genes with Wilcoxon BH-adjusted `p < 0.05`

Prediction:

- `predicted_n_degs = 560`

Evidence that determined the point:

- The held-out target was absent from the declared focal-class training count table; the manifest target is the single gene `Psmc5`.
- In the focal non-target cells, `Psmc5` is well within assay reach: 20,831 / 23,679 non-target nuclei expressed the gene, with 87.97% expressing, mean raw UMI 2.64, mean CP10K 1.64, and pseudobulk CPM 165.69.
- The endpoint-blind `Psmc5` biology bundle places PSMC5/Rpt6 in the 19S AAA ATPase ring of the 26S proteasome. Other PSMC proteins are partner subunits rather than documented drop-in replacements. The functional-stock card concluded that P16 editing is likely to substantially deplete operative PSMC5-dependent function by the P37-P44 harvest: assembled proteasome activity can persist at day 7 after knockdown, but sustained neural Psmc5 knockdown can give strong target loss, ubiquitinated-protein accumulation, and excitatory synapse loss by day 14.
- The `151 TH Prkcd Grin2c Glut` training count table is highly zero-inflated: 1,205 / 1,674 training perturbations were zero, the median was zero, the 95th percentile was 18, and only 43 targets had at least 100 DEGs. Two direct constitutive-proteasome anchors were extreme positives: `Psmb4 = 742` and `Psmc1 = 430`, ranked 7th and 18th of 1,674 respectively.
- Direct parquet aggregation in the same focal class recovered the same anchor counts and showed bidirectional responses rather than a one-sided artifact: `Psmb4` had 357 up and 385 down FDR-significant genes, while `Psmc1` had 231 up and 199 down.
- Same-experiment `Psmc1` and `Psmb4` Findings both annotate the state as direct 26S proteasome insufficiency with proteasome bounce-back, autophagy/endolysosomal compensation, heat-shock and integrated-stress-response induction, apoptotic or redox stress arms, and mature-neuronal/synaptic down-regulation. Each report identifies the other constitutive proteasome subunit as the specific same-state comparator.
- A small profile comparison in the focal expression parquet confirmed that `Psmc1` and `Psmb4` are directionally coherent: Pearson 0.611 across 17,259 shared features, 88 shared up-significant genes, 127 shared down-significant genes, and no significant direction conflicts in the selected pair. Accessory or sensor perturbations such as `Vcp = 2`, `Sqstm1 = 1`, and `Nfe2l2 = 0` were not used as scale anchors because their basal perturbation did not reproduce the core proteasome response.

Synthesis:

`Psmc5` should behave much closer to the direct 26S subunit bracket than to the focal-class null bulk. It is a stoichiometric 19S AAA ATPase like `Psmc1`, is expressed in nearly all focal non-target cells, and should have time for functional depletion before harvest. I did not extrapolate up to broad high-burden stress perturbations such as `Uba5` or `Tpr`, because the `Psmc1`/`Psmb4` reports separate a proteasome-specific core from more generic injury modules. I also kept the point below `Psmb4` because existing assembled proteasomes can buffer a new-supply defect for part of the 21-28 day window and the direct PSMC5 depletion evidence is from rat hippocampal systems rather than juvenile mouse thalamus. Centering the call inside the `Psmc1`/`Psmb4` 430-742 bracket gives a several-hundred DEG forecast: 560.
