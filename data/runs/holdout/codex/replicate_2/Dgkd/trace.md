# Direct forecast trace

## Target and endpoint

- Target: `Dgkd`
- Focal population: `151 TH Prkcd Grin2c Glut`
- Endpoint: `n_degs`, the number of measured genes with BH-adjusted Wilcoxon `pvals_adj < 0.05` in the focal population.

## Target biology used

The declared biology bundle normalizes this perturbation to the historical `Dgkd` alias of `Dgkq`, DGKtheta, a diacylglycerol kinase that phosphorylates DAG to phosphatidic acid.  The exact in-assay non-target expression for the focal population is available and substantial enough to make the target transcript observable: mean raw UMI `0.7515`, mean log1p CP10K `0.3142`, pseudobulk CPM `47.10`, and expression in `11627 / 23679` non-target cells (`49.10%`).

The functional-stock card argues that new intact DGKtheta supply should stop after a disruptive edit and that the operative enzyme should be substantially depleted by P37-P44: the P16-to-P37/P44 interval is 21-28 days, while full-length endogenous protein turned over on an hours scale in cultured mouse cells.  The same source bundle also tempers this upward bearing: the direct neuronal loss phenotype is activity-evoked vesicle-recycling impairment in cultured cortical/hippocampal neurons, not an induced postnatal thalamic loss experiment, and the assay endpoint is steady-state survivor-conditioned nuclear RNA.

## Training measurements used

The declared count table has `1674` training perturbations in the same cell class.  It is highly sparse:

- `1205 / 1674` targets have `n_degs = 0`.
- The median is `0`.
- The 75th percentile is `1`.
- The 90th percentile is `2`.
- The 95th percentile is `18`.

I used the count table to anchor scale on lipid and synaptic-vesicle comparators that were actually present in training:

| comparator | count |
| --- | ---: |
| `Dgke` | 1 |
| `Pld3` | 1 |
| `Synj1` | 1 |
| `Dnm1` | 1 |
| `Bin1` | 1 |
| `Cltc` | 3 |
| `Stxbp1` | 1 |
| `Syn1` | 1 |
| `Unc13a` | 0 |
| `Unc13b` | 0 |
| `Plcb1` | 0 |
| `Pik3cb` | 0 |
| `Pik3r1` | 0 |
| `Pik3r2` | 0 |
| `Syngap1` | 0 |
| `Syn2` | 0 |
| `Stx1b` | 0 |

Direct Parquet reads for the same group showed that the one significant feature in `Dgke`, `Pld3`, `Synj1`, `Dnm1`, `Bin1`, `Stxbp1`, and `Syn1` was the perturbed gene itself.  In this count table, one-DEG outcomes are usually this kind of self-transcript-only event: `237 / 276` training targets with `n_degs = 1` had no significant non-self gene.

The same-experiment corpus supported treating `Cltc` as the stronger, non-identical boundary rather than as the best magnitude donor.  `Dgke` had no robust steady-state neuronal transcriptional output in any recovered cell group; `Dnm1` produced zero non-`Dnm1` FDR genes across 22 measured neuronal groups; and a `Cltc` report noted that canonical endocytosis/uncoating targets such as `Dnm1` and `Synj1` did not phenocopy the multi-group `Cltc` response.

Profile comparison of the 17 lipid/synaptic comparators in the focal population likewise showed a diffuse low-signal neighborhood, not a coherent DEG-bearing module: all 136 pairwise comparisons were available, the mean top-tail overlap was small in both directions (`0.068` positive, `0.102` negative), and no positive-tail significant programs overlapped inside the cohort.

## Point synthesis

The target is plausibly engaged and biologically reachable, and its 49% focal expression makes one on-target RNA hit plausible.  But DGKtheta is closest to vesicle-cycling and DAG/PI pathway perturbations that are transcriptionally buffered in this postnatal nuclear RNA screen; the available direct analog `Dgke` and the synaptic-vesicle comparators are all 0-1 DEG in this exact cell class, nearly always self-only.  I therefore assigned one count for likely detection of the perturbed `Dgkd` transcript and no extra downstream steady-state program.

Predicted `n_degs`: `1`
