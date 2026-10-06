# Direct prediction trace

Target: `Uqcc2`

Cell class: `151 TH Prkcd Grin2c Glut`

Predicted `n_degs`: `0`

## Evidence Used

- The one-row holdout manifest names `Uqcc2`. The target was not present in the declared 151-class training count table.
- The declared biology bundle reports exact non-target expression for `Uqcc2` in `151 TH Prkcd Grin2c Glut`: 16,471 of 23,679 non-target nuclei express it, 69.56% expressing, mean raw UMI 1.423, mean log1p CP10K 0.538, pseudobulk CPM 89.20. This makes the target reachable in the assayed population, but it is expression reach rather than a perturbation outcome.
- The same bundle adjudicates UQCC2 as an early complex-III/cytochrome-b assembly factor whose loss should block new complex-III assembly. It favors substantial functional-stock depletion by the P37-P44 harvest, but with only partial evidence because mature pre-edit complex III initially persists and the turnover support is a human-cell mitochondrial-proteome proxy.
- The declared 151-class training count table is sparse and skewed: 1,205 / 1,674 targets have 0 DEGs, the median is 0, the 75th percentile is 1, the 90th percentile is 2, the mean is 14.05, and the maximum is 2,677.
- Endpoint-blind analog nomination for `Uqcc2` found no exact complex/paralog, bidirectional-corpus, narrow-module, or direct-interaction eligible nominee. All eligible nominees were broad functional fallbacks. The most relevant recovered community was GO:0034551, "mitochondrial respiratory chain complex III assembly"; it contained direct or graph-supported training genes including `Ttc19`, `Uqcrfs1`, `Cyc1`, `Ndufb3`, `Uqcrh`, `Uqcrq`, `Uqcrc2`, and `Uqcrb`.
- In the exact 151-class count table, direct complex-III-family counts were very small:

| target | 151-class `n_degs` |
|---|---:|
| `Uqcrb` | 0 |
| `Uqcrc2` | 1 |
| `Uqcrfs1` | 0 |
| `Uqcrh` | 0 |
| `Uqcrq` | 1 |
| `Cyc1` | 1 |
| `Ttc19` | 1 |

- The matched 151-class parquet rows showed that these were not broad transcriptional programs. `Uqcrc2`, `Cyc1`, and `Ttc19` had exactly one BH-significant row, and that row was the perturbed target transcript itself. `Uqcrq` had exactly one weak non-self call, `Gpr180`, at adjusted p = 0.0429. `Uqcrb`, `Uqcrfs1`, and `Uqcrh` had no BH-significant rows despite 127, 233, and 152 matched perturbed nuclei, respectively.
- Broader respiratory-chain controls in the same class were similarly quiet. Examples from endpoint-blind nominations and OXPHOS genes were `Ndufa4` = 1, `Ndufa6` = 1, `Ndufa8` = 0, `Ndufb3` = 0, `Ndufb7` = 0, `Ndufs4` = 0, `Ndufv1` = 0, `Ndufs2` = 1, `Ndufs8` = 1, `Cox7b` = 0, `Sdha` = 1, `Rmnd1` = 0, and `Lrpprc` = 0.

## Reasoning

UQCC2 loss should be a real mitochondrial lesion in successfully edited cells: the target is present in the focal thalamic nuclei, UQCC2 is required for cytochrome-b/complex-III biogenesis, and the biology card favors turnover of enough post-edit complex III by harvest for the perturbation to matter.

The expected 151-class DEG burden, however, is better matched by respiratory-chain training perturbations than by the screen-wide high tail. The closest measured complex-III and complex-III-assembly comparators produce 0 or 1 significant rows in this endpoint, not tens or hundreds. Their one-DEG cases are mostly target-transcript knockdown calls; the non-self response among `Uqcr*` genes was only one marginal `Gpr180` row for `Uqcrq`.

I therefore placed `Uqcc2` on the same quiet boundary as the `Uqcr*`/`Ttc19` comparators. Because UQCC2 is an assembly factor rather than a mature stoichiometric complex-III subunit, pre-existing complex III is initially retained, and survivor-conditioned nuclei can attenuate mitochondrial stress states. Those factors make a broad non-self signature less likely than a null or self-only count. The target transcript itself could cross the threshold, but target-mRNA loss is a noisy readout in this assay and several expressed respiratory-chain genes with matched nuclei still had 0 significant rows. Balancing 0 versus 1, the direct point forecast is `0`.
