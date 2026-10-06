# Direct forecast for `Agrn`

## Endpoint

Predicted endpoint: `n_degs` in `151 TH Prkcd Grin2c Glut`, counted as measured genes with BH-adjusted Wilcoxon `p < 0.05`.

The one-row holdout manifest declares `Agrn` as the only target.

## Evidence used

- **Target biology bundle:** `biology_bundles/Agrn.json`, schema `expected-transcript-impact-agent-bundle-v1`, sha256 `08cbcc82f288f851209c921920aaf22ed7a08f142db7242056eb5972c381c83e`.
- **Exact focal reach:** `Agrn` is detected in the exact non-target focal population, with `23,534 / 23,679` cells expressing it, `pct_cells_expressing = 99.3876`, `mean_raw_umi = 8.478`, and `mean_log1p_cp10k = 1.783`.
- **Functional-stock prior from the biology bundle:** AGRN is split across transmembrane, secreted extracellular-matrix, and processed synaptic pools. A P16 edit should stop new AGRN supply, but installed AGRN is not removed directly; the bundle adjudicates harvest stock as `partially_depleted_or_leading_edge` because the fast neuronal transmembrane pool can be lost within days while aggregate cortical-neuron Agrin has an approximately 23-day half-life.
- **Postnatal observability prior from the biology bundle:** neuronal `Agrn` loss has a postnatal neural phenotype in adult hippocampus, but the evidence is region- and endpoint-shifted from P16-to-P37/P44 thalamic neuronal snRNA-seq; phenotype latency in the matched interval is unreported.
- **Training count table:** `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]` contains 1,674 non-`Agrn` targets. In this exact focal class, 1,205 of 1,674 training perturbations are zeros; median `n_degs` is 0, the 75th percentile is 1, and the mean is 14.05 because a small upper tail dominates the distribution.
- **Closest measured agrin-axis perturbations in the count table:** `Lrp4 = 0`, `Musk = 0`, and `Ror2 = 0`. The broader matrix/receptor-like set that I used, `Lrp4`, `Musk`, `Ror2`, `Dag1`, and `Reln`, was also all-zero in this focal class.
- **Broader synaptic-adhesion comparators:** among `Nrxn1`, `Nrxn2`, `Nrxn3`, `Nlgn3`, `Lrrtm1`, `Lrrtm3`, `Lrrtm4`, `Grid1`, `Grid2`, `Robo1`, `Robo2`, `Epha4`, `Epha5`, and `Cadm2`, the observed focal counts were `[1, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1]`, with median 0.5.
- **Parquet check of those focal profiles:** filtering `[local file: training_de_all_cell_groups.parquet]` to `151 TH Prkcd Grin2c Glut` showed 0 BH<0.05 genes for `Lrp4`, `Musk`, `Ror2`, `Dag1`, and `Reln`. For singletons such as `Nrxn1`, `Nlgn3`, `Grid1`, `Robo1`, and `Cadm2`, the sole significant row was the perturbed transcript itself; these were not multi-gene downstream states.
- **Same-experiment corpus interpretation for training targets:** the July 260713 sourceguard ledger marks `Lrp4` as globally buffered with no focal LRP4 response (`Lrp4:F002`, `Lrp4:F004`, `Lrp4:F005`, `Lrp4:F006`), `Dag1` as a global downstream null (`Dag1:F001`), `Musk` as uncoupled from the canonical agrin-LRP4-MuSK module in sampled neurons (`Musk:F002`), and `Nlgn3` as a pan-surface downstream transcriptomic null despite measurable self-transcript depletion (`Nlgn3:F001`, `Nlgn3:F002`).

## Synthesis

`Agrn` has excellent focal RNA reach, so a missing or low-expression target feature is not a reason to force a zero. The deciding biology, however, points away from a broad acute recovered-cell mRNA program: the CRISPR edit should mainly remove new supply of an extracellular/synaptic organizer whose installed stock can persist through much of the 21-28 day window, and the closest matched perturbations on the LRP4/MuSK/ROR2 and dystroglycan/extracellular-matrix side were all transcriptionally flat in the exact thalamic class.

The remaining upward bearing is a possible self-transcript call because the screen's low-end `n_degs = 1` cases are often self depletion. I did not project a singleton for `Agrn`: the direct agrin receptors were exact zeros, the broader synaptic-adhesion singleton cases lacked downstream convergence, and AGRN's isoform-specific, matrix-associated stock makes the held-out P16 edit less likely to yield a clean focal nuclear signature than a directly depleted RNA/protein complex member.

Predicted `n_degs`: **0**
