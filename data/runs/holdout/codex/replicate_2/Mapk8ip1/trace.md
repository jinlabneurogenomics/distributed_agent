# Mapk8ip1 direct forecast

## Prediction

`Mapk8ip1` in `151 TH Prkcd Grin2c Glut`: **1 DEG** at Wilcoxon BH `pvals_adj < 0.05`.

## Evidence used

- **Declared target**: the one-row holdout manifest contains `Mapk8ip1`; the declared 151-class training count table omits `Mapk8ip1`, so the withheld endpoint was not present in the visible count target set.
- **Canonical biology bundle**: `Mapk8ip1` is strongly expressed in the focal non-target population
  (`96.87%` expressing nuclei, mean `2.99 cp10k`, mean raw UMI `4.76`), and the card adjudicates the operative JIP1 stock as a dynamic signaling / kinesin-cargo scaffold that should likely be substantially depleted over the 21-28 day P16-to-P37/P44 window. Its phenotypic evidence is mouse postnatal neural but hippocampal/stress-plasticity rather than same thalamic population; JIP2/JIP3/JIP4 and JIP-independent JNK activation leave plausible buffering.
- **Visible 151-class DEG-count distribution**: in
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`,
  1,205 / 1,674 visible targets have `n_degs = 0`, 276 have `n_degs = 1`, and the 75th/90th percentiles are 1 and 2. The response distribution is therefore sparse with a heavy upper tail.
- **Immediate pathway availability**: the JIP/JNK family genes named in the biology card were mostly absent from the 151-class count table. The one direct catalytic JNK comparator that was present, `Mapk9`, had `n_degs = 0`.
- **Local measured comparators from the declared Parquet**:

  | perturbation | 151-class `n_degs` | bearing |
  | --- | ---: | --- |
  | `Mapk9` | 0 | same JNK pathway; FDR-silent in the focal raw rows |
  | `Map2k1` | 4 | MAPK but ERK rather than JNK; sparse response |
  | `Kif5a` | 1 | kinesin heavy chain adjacent to JIP1 cargo biology; only the self transcript passed |
  | `Kif5c` | 1 | kinesin family comparator; only the self transcript passed |
  | `Kif1a` | 1 | axonal kinesin comparator; only the self transcript passed |
  | `Dnm1` | 1 | synaptic-vesicle transport comparator; only the self transcript passed |
  | `Dlg4` | 1 | PSD scaffold comparator; only the self transcript passed |
  | `Grin2a` | 1 | NMDA-receptor subunit tied to the JIP1 literature axis; only the self transcript passed |

- **Same-experiment corpus layer, treated as interpretation of the same Parquet**: `Mapk9` Findings F001-F005 summarize a pan-neuronal FDR-silent JNK2 perturbation with no AP-1/IEG/autophagy signature; `Kif5a` Findings F001-F005 summarize a self-transcript-only / downstream-flat kinesin surface; `Dnm1` and `Dlg4` Findings likewise report downstream-flat synaptic or PSD perturbations. Those reports support using these genes as low-count context rather than as independent confirmations.

## Synthesis

The biology bundle argues that this is not a simple unexpressed-target null: `Mapk8ip1` is measured in almost all focal control nuclei, and new intact JIP1 supply should decline after a successful disruptive edit. However, the pathway is a selective scaffolded JNK / kinesin-adapter operation, not an obligate core transcriptional regulator, lysosome/proteasome stressor, or broad receptor subunit. The closest measured operations available in the focal count table are therefore the low end of the response distribution: direct JNK loss is silent, MAPK pathway loss is only a few DEGs, and several kinesin, vesicle, and PSD scaffold perturbations collapse to a single self-transcript hit.

I placed the point forecast at **1** rather than 0 because exact focal expression and dynamic-stock reach make at least a minimal measured perturbation more likely than for a randomly selected quiet target, but I did not borrow the large `Grin1` or `Rab7` signatures: those represent broader receptor or lysosomal stress states whose hundreds-of-DEGs scales are not justified for JIP1.
