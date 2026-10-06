# Direct forecast for `Cep83`

## Endpoint and declared inputs

- Target: `Cep83`, the single row in the declared holdout manifest `Cep83.csv`.
- Endpoint: `n_degs` in `151 TH Prkcd Grin2c Glut`, defined as the count of measured genes with BH-adjusted Wilcoxon `pvals_adj < 0.05`.
- Direct training endpoint table: `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`, with 1,674 observed training targets. `Cep83` is absent from this table.
- Declared target biology bundle: `Cep83.json`; the canonical bundle reports biological source facts, exact non-target expression reach in the focal population, and functional-stock adjudication, but no target endpoint value.

## Cep83 biology used

The declared exact reach makes `Cep83` a biologically reachable perturbation in the focal thalamic glutamatergic population: the target transcript is detected in 14,148 of 23,679 non-target nuclei, 59.75%, with mean raw UMI 1.0555 and pseudobulk CPM 66.15.

CEP83 is a structural mother-centriole distal-appendage organizer required for basal-body membrane docking and primary-cilium formation. The strongest postmitotic-neuron evidence in the bundle comes from cortical and amygdalar excitatory neurons, where Cep83 deletion removes most primary cilia and changes cilia-dependent neuronal physiology/behavior, so a neural effect is plausible. The same functional-stock adjudication is the main downward modifier: by the P16 edit, distal appendages and primary cilia are already substantially installed; a disruptive edit should stop new CEP83 synthesis but does not instantly dismantle pre-existing appendages; and no source in the declared bounded search established how much CEP83-bearing distal-appendage or ciliary function is lost by the P37-P44 harvest. The bundle therefore leaves functional stock by harvest `indeterminate`, not clearly depleted.

## Training perturbations used

The focal count table is sparse overall: 1,205/1,674 training perturbations have 0 DEGs, the median is 0, 1,481/1,674 have at most 1 DEG, and only 43/1,674 have at least 100 DEGs. That base distribution makes zero the modal expectation unless a perturbation has evidence tying it to a strong recurrent transcriptional state.

I treated ciliary assembly, intraflagellar transport, BBSome/transition-zone, ciliary dynein/kinesin, and ciliary signaling perturbations as the most relevant observed local comparators, because they perturb the same organelle or pathways that depend on it without using `Cep83` itself:

| training target | n_degs |
|---|---:|
| `Bbs5` | 0 |
| `Cep112` | 0 |
| `Cep120` | 0 |
| `Cep290` | 0 |
| `Dync2h1` | 0 |
| `Dync2i1` | 0 |
| `Gli2` | 0 |
| `Gnas` | 0 |
| `Ift43` | 0 |
| `Ift81` | 0 |
| `Ift88` | 0 |
| `Iqcb1` | 0 |
| `Kif3b` | 0 |
| `Ptch1` | 0 |
| `Rpgrip1l` | 0 |
| `Sclt1` | 0 |
| `Smo` | 0 |
| `Ttc21b` | 0 |
| `Ttc8` | 1 |

The Parquet profile comparison of those 19 observed cilia/cilia-adjacent training nodes in exactly `group_name == "151 TH Prkcd Grin2c Glut"` gave the same qualitative result: 18 of 19 nodes had no significant features and the only nonzero node was in the `1_to_9_significant_features` activity stratum. A cohort diagnostic over all 171 supplied pairs found no overlap of significant positive or negative programs, which argues against a hidden recurrent ciliary response program that was being missed by looking only at endpoint counts.

## Synthesis

The expression reach and mature-neuron cilium phenotype keep `Cep83` from being an assay-ineligible or biologically impossible null. However, the perturbation acts on an already installed distal-appendage stock with unresolved 21-28 day loss kinetics, the closest assayed ciliary perturbations are almost uniformly zero in the same high-yield thalamic class, and their continuous profiles did not reveal a recurring significant program. I therefore place the prediction at the zero mode of the local training distribution rather than extrapolating to the rare large-response tail.

Predicted `n_degs`: **0**
