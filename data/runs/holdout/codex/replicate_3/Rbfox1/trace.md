# Rbfox1 direct forecast for `151 TH Prkcd Grin2c Glut`

## Declared target and endpoint

- Holdout manifest target: `Rbfox1`.
- Endpoint: `n_degs`, the number of measured genes in `151 TH Prkcd Grin2c Glut` with BH-adjusted Wilcoxon `p < 0.05`.
- The declared training count table contains 1,674 perturbations and does not contain `Rbfox1`; the declared training Parquet was used only for other training perturbations.

## Target biology

The canonical biology bundle supports target reach and a realizable perturbation, but not a high whole-gene DEG burden by itself.

- `Rbfox1` is well detected in the exact focal population: 22,901 of 23,679 non-target `151 TH Prkcd Grin2c Glut` nuclei express it, `96.714%` of cells, with mean raw UMI `4.685`.
- RBFOX1 is an RNA-binding regulator of neuronal alternative exon use with nuclear and cytoplasmic RNA-regulatory pools. Loss affects postnatal mouse CNS and interneuron physiology in published conditional models, but those models are hippocampal/cortical or developmental rather than acute P16 thalamic edits.
- The functional-stock card calls RBFOX1 operative stock `likely_substantially_depleted` by the P37-P44 harvest because new synthesis is stopped for 21-28 days and neuronal pre-mRNAs require ongoing splicing decisions.
- The main attenuation is the same-context paralog buffer: RBFOX2 protein increased after CNS `Rbfox1` loss and RBFOX2/RBFOX3 are close neuronal paralogs, even though compensation was incomplete in the published CNS model.

Thus I expect a real chance of a response in thalamic recovered nuclei, but the endpoint is whole-gene nuclear RNA abundance, not isoform usage, so an alternative-splicing regulator should be scaled nearer specialized neuronal RBPs than core spliceosome factors.

## Training-count anchors

The focal-class training distribution is highly skewed:

- 1,205 / 1,674 perturbations have `n_degs = 0`.
- 1,481 / 1,674 have `n_degs <= 1`.
- only 106 / 1,674 have `n_degs >= 10`.
- only 59 / 1,674 have `n_degs >= 50`.

The closest RBFOX paralogs and several classic neuron-specific splicing factors were absent from the training count table, so I used a bounded RNA-regulator panel rather than a direct family transfer.

Small or flat specialized RNA-binding anchors in `151 TH Prkcd Grin2c Glut`:

| perturbation | training `n_degs` | interpretation |
|---|---:|---|
| `Fmr1` | 0 | specialized neuronal RBP with no FDR-significant genes in this class |
| `Msi1` | 0 | neuronal RBP; corpus reports a pan-neuronal whole-gene transcriptional null |
| `Syncrip` | 0 | neuronal hnRNP-like RBP; corpus reports only two FDR<0.10 downstream genes across all measured groups |
| `Zc3h14` | 6 | narrow postmitotic RNA-response anchor |
| `Ddx3x` | 8 | narrow postnatal RNA/helicase response, confined mostly to high-yield glutamatergic classes |
| `Hnrnpa2b1` | 11 | weaker nuclear RBP response than broad hnRNP/spliceosome perturbations |

Broad RNA-processing boundary anchors in the same focal class:

| perturbation | training `n_degs` |
|---|---:|
| `Hnrnpc` | 122 |
| `Matr3` | 149 |
| `Tardbp` | 210 |
| `Snrnp70` | 213 |
| `Prpf6` | 454 |
| `Hnrnpu` | 733 |
| `U2af2` | 828 |
| `Rnpc3` | 868 |

The log1p center of the six low/specialized anchors above is `n_degs = 2.0`, while the positive subset `Zc3h14`, `Ddx3x`, and `Hnrnpa2b1` centers at `8.1`. The core-spliceosome/strong-hnRNP boundary is hundreds of DEGs and is not an equal-scale match for `Rbfox1`.

## Parquet profile check

I compared the 14 RNA-regulator training profiles in the declared Parquet after filtering to `group_name = "151 TH Prkcd Grin2c Glut"`, using `logfoldchanges` as the signed value and `pvals_adj < 0.05` as the significance threshold.

The profile review found all 14 selected nodes and kept the same split seen in the count table:

- `Syncrip`, `Msi1`, and `Fmr1`: `no_significant_features`.
- `Zc3h14` and `Ddx3x`: `1_to_9_significant_features`.
- `Hnrnpa2b1`: `10_to_49_significant_features`.
- eight core or broad RNP/spliceosome factors: `at_least_50_significant_features`.

Pairwise whole-profile correlations among these RNA factors were often positive even when one node had zero FDR-significant genes, confirming that weak continuous similarity is not enough to transfer the high spliceosome counts to `Rbfox1`. I therefore treated the high spliceosome nodes only as upper boundaries.

## Forecast

I put `Rbfox1` above the exact zeros because it is strongly expressed in the focal thalamic neurons, should lose a renewable RBFOX1 pool within the assay window, and has postnatal neural loss phenotypes that were not fully buffered by paralogs. I kept it below the broad hnRNP/spliceosome regime because RBFOX1 is a sequence-specific neuronal alternative-splicing regulator, many expected effects are exon/isoform-level rather than whole-gene abundance changes, acute thalamic timing is not directly established, and the RBFOX2/RBFOX3 buffer should blunt whole-gene nuclear-RNA output.

Those bearings put the point near the small positive RNA-binding anchors (`Zc3h14`, `Ddx3x`, `Hnrnpa2b1`) but pulled slightly downward by the flat specialized neuronal RBPs. My final point forecast is:

`predicted_n_degs = 6`
