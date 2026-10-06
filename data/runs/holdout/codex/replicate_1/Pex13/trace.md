# Pex13 n_degs forecast for 151 TH Prkcd Grin2c Glut

## Declared endpoint

- Target manifest: `Pex13`.
- Focal cell class: `151 TH Prkcd Grin2c Glut`.
- Endpoint: all measured genes with Wilcoxon `pvals_adj < 0.05` in that class.
- Training sources used: the declared focal-class count table, the declared full training DE Parquet, the canonical Pex13 biology bundle, bounded same-experiment Findings for observed peroxisome comparators, and a run-local profile-neighbor projection for `Pex1` and `Pex14`.

## Target biology

The Pex13 biology bundle places PEX13 at the peroxisomal PTS1/PTS2 matrix-import docking apparatus with PEX14/PEX5/PEX7 context. Its functional-stock adjudication predicts that a P16 disruptive edit should stop PEX13 resupply while pre-existing membrane/import stock decays over the 21-28 day edit-to-harvest interval; the stock call is `likely_substantially_depleted`, but with only partial completeness because no juvenile thalamic-neuron PEX13 half-life is known. The exact focal expression record shows `Pex13` is measurable in this class: 19,147 / 23,679 non-target nuclei express it, 80.8607%, with mean raw UMI 1.9584 and pseudobulk CPM 122.74. That supports target reach and a possible self-transcript count, but not a guaranteed broad downstream RNA program.

The closest measured training genes were PEX/peroxisome members rather than the genome-wide high responders. In the focal count table, the represented peroxisome-linked genes had very small all-gene counts:

| target | n_degs |
| --- | ---: |
| Pex1 | 0 |
| Pex14 | 1 |
| Abcd3 | 0 |
| Acbd5 | 0 |
| Agps | 1 |
| Far1 | 2 |
| Hsd17b4 | 0 |
| Mff | 0 |

The Parquet rows with `pvals_adj < 0.05` in this class explain those nonzero counts. `Pex14` contributes only its own transcript (`Pex14`, logFC -0.9073, adjusted p 3.74e-7); `Agps` contributes `Dhcr24`; `Far1` contributes its own transcript plus `Tial1`; and `Pex1`, `Abcd3`, `Acbd5`, `Hsd17b4`, and `Mff` contribute no significant row. Thus the direct PEX-import evidence is not a multi-gene downstream state; the plausible all-gene mass for Pex13 is either 0 or a self-transcript singleton.

The same-experiment corpus agrees with this interpretation, without adding independent replication. The `Pex14` report states that Pex14 loss produced no FDR<0.10 downstream transcript in any of 23 neuronal groups, did not induce peroxisome-biogenesis/lipid/redox/ISR/autophagy marker transcripts, and did not converge with represented peroxisome-linked comparators. The `Pex1` report likewise describes only two singleton DEGs outside this focal class and no robust nuclear peroxisome-import, lipid, oxidative-stress, pexophagy, ISR, or UPR module. Shared Claims for `Pex1` and `Pex14` summarize the broader boundary: represented peroxisome-linked perturbations were predominantly flat, sparse, or target-specific rather than a coherent acute neuronal peroxisome module.

I also projected `Pex1` and `Pex14` against all 1,674 eligible training profiles in the focal class. The measured anchor profiles were sparse (`Pex1` had 0 significant features; `Pex14` had 1 negative significant feature), and their nearest whole-profile neighbors were weak and not PEX/peroxisome genes: the top Pearson neighbor for `Pex1` was 0.0982, and for `Pex14` was 0.1298. This argued against replacing the flat direct comparators with a high-response profile-neighbor module.

For the all-gene count scale, the focal training distribution was heavily zero-inflated: 1,175 of 1,674 targets had `n_degs = 0`, 275 had `n_degs = 1`, and 1,481 had `n_degs <= 2`. Among targets with an available self row, singleton outcomes were usually self-transcript singletons: 237 of the 275 `n_degs = 1` rows had significant `names == gene_target` self signal. Because the Pex13 bundle shows broad exact expression in the focal population, and because the direct PEX14 docking comparator's only all-gene hit was its own transcript, I forecast one significant row for `Pex13` and no confident downstream FDR gene.

## Prediction

`predicted_n_degs = 1`
