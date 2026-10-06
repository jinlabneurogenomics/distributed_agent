# Acox1 direct `151 TH Prkcd Grin2c Glut` DEG-count forecast

## Target and endpoint

- Target in the declared one-row manifest: `Acox1`.
- Endpoint: count of measured genes with BH-adjusted Wilcoxon `p < 0.05` in `151 TH Prkcd Grin2c Glut`.
- The `Acox1` perturbation signature and held-out DEG count were absent from the count table and Parquet inputs used here.

## Biology prior

- The declared Acox1 biology bundle identifies ACOX1 as the first/rate-limiting peroxisomal oxidase for straight-chain long and very-long-chain acyl-CoAs. A disruptive edit should stop new functional ACOX1 synthesis, but pre-edit peroxisomal enzyme is not inactivated instantly.
- Exact focal reach is real: the Acox1 feature was detected in 16,272 of 23,679 non-target nuclei from `151 TH Prkcd Grin2c Glut`, or 68.719% expressing, with mean CP10k 0.827.
- The functional-stock card judged active ACOX1 by harvest as likely substantially depleted over the 21-28 day P16-to-P37/P44 window, with only partial evidence completeness because no direct ACOX1 half-life in mouse thalamic neurons was identified.
- Phenotype priors support biological relevance but not a fast thalamic nuclear-RNA response: germline mouse loss is hepatic, human ACOX1 deficiency is constitutional and evolves across childhood, and Acox2/Acox3 biochemical overlap does not establish thalamic compensation.
- The selected same-experiment corpus has no `Acox1` Finding, Claim, or explicit comparator record, so it did not provide a target-centered measured outcome or direct same-experiment comparator for Acox1.

## Training measurements that set the scale

- The focal count table is zero-heavy: 1,205 / 1,674 training perturbations have `n_degs = 0`, the median is 0, the 75th percentile is 1, and 1,481 / 1,674 have at most one DEG.
- I nominated training-available analogs using curated mouse annotations rather than a symbol prefix. The strongest Acox1-adjacent modules were peroxisomal lipid metabolism and very-long-chain/peroxisomal beta-oxidation.
- In `151 TH Prkcd Grin2c Glut`, the nearest peroxisome and beta-oxidation training perturbations were transcriptionally flat or nearly flat:

| training target | focal `n_degs` | non-self focal DEGs |
|---|---:|---:|
| `Hsd17b4` | 0 | 0 |
| `Acbd5` | 0 | 0 |
| `Abcd3` | 0 | 0 |
| `Pex1` | 0 | 0 |
| `Pex14` | 1 | 0 |
| `Agps` | 1 | 1 |
| `Far1` | 2 | 1 |

- Broader fatty-acid/peroxisome-context candidates did not argue for a larger count: `Ppara`, `Ppard`, `Pparg`, `Dpyd`, `Mff`, and `Gpx4` all had 0 focal DEGs, while `Acsl4`, `Tecr`, `Cpt1c`, and `Sod2` had only self-target transcript DEGs.
- Parquet inspection showed the single significant `Pex14`, `Acsl4`, `Tecr`, `Cpt1c`, and `Sod2` rows were the perturbed transcript itself. That makes a one-DEG outcome in this local neighborhood mostly a self-readout event, not a recurrent downstream peroxisomal state.
- Across all focal training self rows, only 319 / 1,642 were significant at adjusted `p < 0.05`; direct peroxisome neighbors also had several negative but non-significant self log-fold changes. I therefore treated possible Acox1 self-transcript reduction as uncertain QC context, not an automatic one-count floor.

## Corpus/profile interpretation

- A moderate same-experiment Claim over `Abcd3`, `Acbd5`, `Agps`, `Far1`, `Hsd17b4`, `Pex1`, and `Pex14` summarized the represented peroxisome-linked perturbations as predominantly flat, sparse, or target-specific rather than a shared acute neuronal transcriptomic module.
- The Parquet counts above are the primary endpoint evidence for the focal class; the Claim is the same experiment's report-derived interpretation of that sparse peroxisome neighborhood, not independent replication.

## Point prediction

The biology bundle says Acox1 editing should eventually deplete catalytic stock, and Acox1 is expressed in the focal population, so a material perturbation is reachable. The task-matched training evidence nevertheless places comparable peroxisomal beta-oxidation, peroxisome import, transporter, and ether-lipid perturbations at 0 to 2 focal DEGs, usually 0 non-self DEGs. Because the closest enzyme/comparator set does not show a downstream acute thalamic program and because self-transcript significance is not reliable enough to add one, my point forecast is:

`predicted_n_degs = 0`
