# Direct DEG-count forecast for Pten in 151 TH Prkcd Grin2c Glut

## Target and endpoint

- Target: `Pten`, from the one-row holdout manifest.
- Endpoint: `n_degs`, the count of measured genes with Wilcoxon BH-adjusted `pvals_adj < 0.05` in `151 TH Prkcd Grin2c Glut`.
- I treated the Parquet and corpus reports as views of the same screen, not as independent replication, and did not query a Pten same-experiment report or a Pten target profile.

## Pten biology-only prior

The Pten biology bundle supports a real loss-of-function perturbation in the requested assay window:

- `Pten` is well observed in the focal non-target nuclei: mean CP10K 2.081, mean raw UMI 3.275, and 21,905 / 23,679 cells expressing it.
- PTEN is a PIP3 3-phosphatase and negative regulator of PI3K-AKT signaling, so loss should release PI3K-AKT-mTOR signaling rather than phenocopy loss of positive PI3K/AKT/mTOR nodes.
- The 21-28 day P16-to-P37/P44 interval spans many measured mouse-neuron PTEN protein half-lives, making retention of pre-edit PTEN enzyme an unlikely explanation for a flat endpoint if edited cells were recovered.
- Postnatal conditional Pten loss causes neuronal hypertrophy in other mouse neuronal populations, including an mTOR-sensitive granule-neuron phenotype. This supports biological observability, but in cortical, hippocampal, cerebellar, and dentate neurons rather than this thalamic Prkcd/Grin2c population.

## Training distribution

The declared `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` contains 1,674 training perturbations. The distribution is sparse and long-tailed:

| summary | n_degs |
|---|---:|
| median | 0 |
| 75th percentile | 1 |
| 90th percentile | 2 |
| 95th percentile | 18 |
| 99th percentile | 430 |
| mean | 14.05 |

The global mean is pulled upward by broad unrelated responders such as `Uba5`, `Tpr`, `Sin3a`, `Rnpc3`, and `Zbtb7a`, so I did not use it as the center for Pten.

## Pathway comparators from the training universe

Curated analog nomination against the actual 1,674-gene training universe recovered PI3K/AKT/mTOR and PTEN-pathway candidates before any endpoint values were inspected. Exact MSigDB BioCarta memberships showed that most canonical nodes closest to Pten were missing or quiet:

| curated set | available training members and 151-counts |
|---|---|
| `BIOCARTA_PTEN_PATHWAY` | `Itgb1 0`, `Mapk1 0`, `Pik3r1 0`, `Sos1 0`; `Pik3ca` absent; `Pten` held out |
| `BIOCARTA_MTOR_PATHWAY` | `Eif4a2 2`, `Mtor 2`, `Pik3r1 0`, `Tsc2 86`; `Eif4e`, `Pik3ca`, `Tsc1` absent; `Pten` held out |
| `BIOCARTA_IGF1MTOR_PATHWAY` | `Gsk3b 6`, `Igf1r 0`, `Mtor 2`, `Pik3r1 0`; `Eif4e`, `Pik3ca` absent; `Pten` held out |

Additional on-axis or adjacent training perturbations were also mostly weak in the exact `pvals_adj < 0.05` focal Parquet scan:

| gene | n_degs |
|---|---:|
| `Tsc2` | 86 |
| `Depdc5` | 13 |
| `Gsk3b` | 6 |
| `Map2k1` | 4 |
| `Braf` | 4 |
| `Eif4a2` | 2 |
| `Mtor` | 2 |
| `Synj1` | 1 |
| `Fmr1`, `Igf1r`, `Inpp5k`, `Itgb1`, `Mapk1`, `Pik3cb`, `Pik3r1`, `Pik3r2`, `Rptor`, `Sos1`, `Strada` | 0 |

The Parquet rows for these comparators all had the same 17,259 measured genes in `151 TH Prkcd Grin2c Glut`. `Tsc2` was powered comparably to the focal design with 177 matched perturbed nuclei; `Depdc5` had 121; several zero-count PI3K inputs had 84-260.

## Profile and same-experiment interpretation of training genes

The observed-profile comparison across 20 retained PI3K/mTOR/ERK/phosphoinositide candidates found 12 zero responders, six with 1-9 significant genes, one with 13, and only `Tsc2` above 50. A cohort diagnostic over their signed log-fold-change profiles showed weak shared positive tails: median positive-tail overlap coefficients around 0.05-0.075 per node. The strongest `Tsc2` outside-neighbors were not the canonical PI3K inputs, consistent with the corpus Finding that `Tsc2` has noncanonical proteostasis/endolysosomal neighbors and that `Mtor`, `Rptor`, `Igf1r`, `Irs1`, and `Akt3` do not robustly share the `Tsc2` FDR program.

The same-experiment corpus also bounds the signs:

- `Tsc2` loss gives the clearest derepressed mTORC1/SREBP/lysosome response and had 86 focal genes, so it is an upper local anchor for a negative regulator that activates downstream mTORC1.
- `Depdc5` loss, another mTORC1-releasing perturbation, was much smaller at 13 focal genes.
- `Mtor` loss itself was tiny at this stricter FDR threshold and opposite in sign to loss of Pten as an upstream brake.
- Single upstream positive nodes, including `Pik3r1`, `Pik3cb`, `Pik3r2`, `Igf1r`, and `Irs1`, were transcriptionally flat, implying strong buffering of basal upstream pathway loss in this assay.

## Synthesis

Pten should not be pushed all the way to the zero median because the focal class expresses `Pten` broadly, the protein stock should clear in the edit-to-harvest window, and loss of a brake can plausibly enter the same mTORC1/SREBP axis that is visible for `Tsc2` and weaker for `Depdc5`. Conversely, the observed training evidence argues against a large `Tsc2`-scale response: same-pathway perturbations are mostly flat, the nearest positive mTORC1-loss entries are much smaller, and `Tsc2` appears to be a relatively direct and unusually strong derepression of the pathway.

I therefore placed Pten just above the `Depdc5` anchor and below the 18-DEG 95th percentile of the full training table.

Predicted `n_degs`: **16**
