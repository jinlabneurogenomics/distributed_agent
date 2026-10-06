# Cxcr2 direct n_degs forecast

Target: `Cxcr2`

Cell group: `151 TH Prkcd Grin2c Glut`

Prediction: **0** measured genes with BH-adjusted Wilcoxon `p < 0.05`.

## Evidence used

- The declared one-row holdout manifest names `Cxcr2`.
- The declared biology bundle reports exact focal-population reach for the assayed non-target controls:
  - `group_name = 151 TH Prkcd Grin2c Glut`
  - `n_non_target_cells = 23679`
  - `n_cells_expressing = 0`
  - `pct_cells_expressing = 0.0`
  - `total_target_umi = 0.0`
  - `mean_raw_umi = 0.0`
  - `mean_cp10k = 0.0`
  This exact in-assay expression measurement supersedes the less direct literature uncertainty about healthy thalamic neuronal Cxcr2 reach.
- The same bundle characterizes CXCR2 as a cell-surface chemokine GPCR whose operative receptor stock should substantially decline by P37-P44 once a P16 disruptive edit stops new intact receptor supply. That supports target engagement in a Cxcr2-expressing neuron, but it does not create an expected transcriptional effect when the assayed baseline population has no detectable Cxcr2 RNA.
- The training count table for this focal class contains 1674 visible perturbations. Its endpoint is strongly zero-inflated:
  - 1205 / 1674 targets have `n_degs = 0`
  - 276 / 1674 have `n_degs = 1`
  - 193 / 1674 have `n_degs >= 2`
  - median `n_degs = 0`, 75th percentile `= 1`
- The closest visible immunologic and chemokine-side comparators in the declared training table are also silent at the requested threshold in this thalamic population:
  - `Ccr2 = 0`
  - `Cxcr4 = 0`
  - `Ager = 0`
  - `Tlr2/Tlr3/Tlr4/Tlr5/Tlr7/Tlr8 = 0`
  - `Ifnar1/Ifnar2/Ifngr1/Ifngr2 = 0`
  - `Il6ra = 0`, `Il6st = 0`, and the queried `Il*` receptor targets were all `0`
  - `Nfkb1 = 0`, `Stat2 = 0`, `Stat3 = 0`
- A direct Parquet query of the same focal group confirmed that selected immune-receptor comparators are not hiding near-threshold FDR<0.05 profiles: `Ccr2`, `Ager`, `Tlr4`, `Il6ra`, `Il6st`, `Ifnar1`, and `Nfkb1` each had zero FDR<0.05 genes and best adjusted p-value `1.0`; `Cxcr4` had zero FDR<0.05 genes and only one FDR<0.10 singleton (`Pum1`, adjusted `p = 0.0672`).
- The packaged same-experiment corpus was used only as interpretation of the training measurements, not as independent replication. It described `Ccr2` and `Tlr4` as pan-neuronal nulls, `Ager` as inert across all recovered neuronal groups, and `Cxcr4` as near a global transcriptional null with a sparse two-island FDR<0.10 response.

## Reasoning

The biology card makes the CRISPR lesion plausible in cells that actually maintain CXCR2, because the receptor pool turns over and a successful edit should stop replacement during the 21-28 day interval. The bottleneck is not protein persistence; it is focal-cell reach. In the exact `151 TH Prkcd Grin2c Glut` non-target baseline, Cxcr2 has no detected UMIs in 23,679 nuclei, and the curated external evidence places its established mouse expression in granulocytes and oligodendrocyte-lineage CNS cells rather than in healthy postnatal thalamic neurons.

The training set says that most perturbations in this population are zero by the BH 0.05 endpoint, and the genes closest to a chemokine/inflammatory receptor program are especially flat. `Ccr2` is the same broad chemokine-receptor class and is `0`; `Cxcr4` is the visible CXC-family receptor comparator and is still `0` at the requested threshold; upstream innate and cytokine receptor targets are similarly `0`. I therefore did not transfer magnitude from high-response neuronal ion-channel, calcium, chromatin, or core-cell-process perturbations, because those are expressed cell-autonomous neuronal operations and are biologically farther from a non-detected chemokine receptor.

Remaining uncertainty is mostly power and sampling: a very rare Cxcr2-expressing subpopulation or non-RNA receptor carryover could be missed by the exact baseline expression readout. That residual uncertainty could produce an isolated singleton, but the requested point forecast should follow the dominant evidence.

I predict:

`n_degs = 0`
