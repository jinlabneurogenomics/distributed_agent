# Trem2 DEG-count forecast

## Endpoint

- Target: `Trem2`.
- Population: `151 TH Prkcd Grin2c Glut`.
- Requested value: `n_degs`, the count of measured genes with BH-adjusted Wilcoxon `pvals_adj < 0.05`.
- The held-out target profile was not present in the declared training count table: `Trem2` was absent from all 1,674 `151 TH Prkcd Grin2c Glut` training rows.

## Evidence used

### Target biology

The canonical `Trem2` biology bundle places the direct operation outside the recovered neuronal population. TREM2 is a rapidly renewed cell-surface receptor in microglia/myeloid cells that signals through TYROBP/DAP12, and the functional-stock card adjudicates the intact surface receptor as likely substantially depleted within the P16-to-P37/P44 window if an expressing cell is productively edited. The same bundle flags the important counterweight: Trem2 function is not intrinsic to NeuN-positive neurons, and the best mouse neural phenotypes are microglia-mediated and not matched to juvenile thalamic neurons.

The exact in-assay expression measurement made that mismatch concrete for the focal class:

- `Trem2` mean raw UMI in non-target `151 TH Prkcd Grin2c Glut` nuclei: `0.004729929`.
- `Trem2` pseudobulk CPM: `0.296441`.
- Expressing cells: `110 / 23679`, or `0.464547%`.

Thus a direct cell-autonomous thalamic-neuron response is biologically unlikely. An indirect route through edited microglia or local glial-neuronal coupling remains possible, but the bundle did not establish that P16 sparse editing would perturb microglia strongly enough, quickly enough, or thalamus-specifically enough to produce a recovered neuronal DEG program.

### Training counts

The declared `151 TH Prkcd Grin2c Glut` count table is already heavily concentrated at zero:

- `1205 / 1674` training perturbations had `n_degs = 0`.
- The median was `0`, the 75th percentile was `1`, and the 90th percentile was `2`.

The available training perturbations closest to a microglial, immune, or extracellular CNS route were flat in the exact endpoint:

| training target | `151` `n_degs` |
|---|---:|
| `Abca1` | 0 |
| `Abca7` | 0 |
| `Axl` | 0 |
| `C3` | 0 |
| `Cd14` | 0 |
| `Ccr2` | 0 |
| `Tnfrsf1a` | 0 |
| `Traf3` | 0 |

The closest Trem-family or TREM2-complex genes from the biology card, `Trem1`, `Treml1`, `Treml2`, and `Tyrobp`, were not available in the training count table, so they were not used as measured anchors.

### Same-experiment corpus and profile check

The packaged same-experiment Findings for training comparators agree with the count table boundary, while not constituting an independent replication. In the report layer, `Abca7:F001`, `Axl:F001`, `C3:F001`, and `Ccr2:F001` each summarized pan-neuronal null or near-null behavior for healthy NeuN-enriched neuronal groups, consistent with glial/immune genes failing to drive acute cell-autonomous neuronal transcriptional programs.

I also compared the eight listed training comparators in the declared Parquet restricted to `151 TH Prkcd Grin2c Glut`, using Wilcoxon `scores` as signed profiles and `pvals_adj < 0.05` as the significance cutoff. All eight nodes were present and all eight were classified as `no_significant_features`; across the 28 pairwise comparisons there was no significant positive or negative program overlap. Their weak tail sharing supported using them as a flat boundary set, not as a coherent nonzero module to transfer to `Trem2`.

## Synthesis

The forecast balances two facts. If `Trem2` were knocked out in a TREM2-positive microglial population, 21-28 days should be long enough to deplete the principal surface receptor pool. In this experiment, however, the endpoint is survivor-conditioned snRNA-seq from NeuN-positive thalamic neurons where `Trem2` is essentially absent, and the training genes that best represent innate-immune, glial, or extracellular receptor biology were exactly zero in the focal population. The residual indirect microglia-to-neuron possibility puts slight mass on one or a few DEGs, but not enough to move the integer point above the modal and biologically matched value.

Predicted `n_degs`: `0`.
