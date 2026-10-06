# Tspan12 DEG-count prediction

## Question interpreted

The requested held-out target list for this run contains exactly one perturbation, `Tspan12`. I interpreted the task as a point prediction for the number of genes that would have `pvals_adj < 0.05` after acute AAV-CRISPR loss of `Tspan12` in the focal `151 TH Prkcd Grin2c Glut` neuronal group, using only the supplied non-held-out Perturb-seq differential-expression data plus external biology. The reported endpoint is therefore the assay-specific focal-cell DEG count, not the organismal severity of a full germline or endothelial knockout.

## Sources used

- `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`: focal-cell training `n_degs` for 1,674 non-held-out genetic perturbations.
- `training_de_all_cell_groups.parquet`: per-gene Wilcoxon statistics. I used the row-group metadata to read only rows from `151 TH Prkcd Grin2c Glut` and then extracted the Wnt/Norrin and tetraspanin comparator targets.
- Requested manifest `251_Tspan12.csv`: confirmed that the only held-out target is `Tspan12`.
- Distributed Agents same-experiment corpus, release `perturbai-july-260713-sourceguard-1773-v1`: queried `target_context`, `related_targets`, and `story_count`. The corpus had no `Tspan12` target node, no claims, and no explicit references for `Tspan12`; it therefore did not contribute a same-experiment curated target neighborhood for this prediction.
- PubMed literature on TSPAN12/Norrin/FZD4/LRP5 signaling and endothelial phenotypes:
  - Junge et al. 2009, Cell, DOI `10.1016/j.cell.2009.07.048`, PMID `19837033`.
  - Ke et al. 2013, Genes & Development, DOI `10.1101/gad.228544.113`, PMID `24186977`.
  - Lai et al. 2017, Cell Reports, DOI `10.1016/j.celrep.2017.06.004`, PMID `28658627`.
  - Zhang et al. 2018, Arteriosclerosis Thrombosis and Vascular Biology, DOI `10.1161/ATVBAHA.118.311689`, PMID `30354230`.
  - Chidiac et al. 2021, EMBO Molecular Medicine, DOI `10.15252/emmm.202113977`, PMID `34105895`.
  - Chang et al. 2015, eLife, DOI `10.7554/eLife.06554`, PMID `26158506`.

## Dataset computations

I first summarized the focal training counts:

- 1,674 training targets in the focal count table.
- 1,205 of 1,674, or about 72%, had zero DEGs.
- The count distribution was heavily concentrated at zero: median 0, 75th percentile 1, 90th percentile 2, 95th percentile 18.

I then extracted focal-cell DE rows for biologically selected candidates from the 7.8 GB parquet instead of reading the full 616 million-row file. Parquet row-group statistics showed that rows for `151 TH Prkcd Grin2c Glut` were contained in row groups 546-580. I filtered those row groups to the comparator targets `Fzd4`, `Lrp5`, `Lrp6`, `Kremen1`, `Ctnnb1`, `Tcf7l2`, `Tspan7`, `Cd81`, `Cd47`, and `Cdc42`, retaining 17,259 measured features for each selected perturbation.

The focal training counts for the most relevant Wnt/Norrin receptor-side comparators were:

| training target | focal `n_degs` | expression-pattern evidence |
|---|---:|---|
| `Fzd4` | 0 | no FDR 0.05 genes; smallest adjusted p-value was 1.0 |
| `Lrp5` | 0 | no FDR 0.05 genes; smallest adjusted p-value was 1.0 |
| `Lrp6` | 4 | four weak significant genes: `Atrnl1`, `Nsmf`, `Nrbp2`, `Chgb`, with minimum adjusted p-value 0.0406 and absolute log2 fold changes about 0.35-0.40 |
| `Kremen1` | 0 | no FDR 0.05 genes; smallest adjusted p-value was 0.738 |

I used `Ctnnb1` and `Tcf7l2` as downstream pathway counterexamples rather than direct analogs:

| training target | focal `n_degs` | expression-pattern evidence |
|---|---:|---|
| `Ctnnb1` | 383 | broad response with 100 positive and 283 negative FDR-significant genes; strongest hits included `Plekhg1`, `Gabra4`, and `Ramp3`; self knockdown of `Ctnnb1` was significant |
| `Tcf7l2` | 106 | 39 positive and 67 negative FDR-significant genes; strongest hits included `Ramp3`, `Cck`, `Spock3`, `Kcnc2`, and `Pcsk2` |

Finally I checked generic tetraspanin or membrane controls in the same cell group:

| training target | focal `n_degs` | expression-pattern evidence |
|---|---:|---|
| `Tspan7` | 1 | the only DEG was `Tspan7` itself |
| `Cd81` | 1 | the only DEG was `Cd81` itself |
| `Cd47` | 1 | the only DEG was `Cd47` itself |
| `Cdc42` | 1 | the only DEG was `Cdc42` itself |

The broader family/pathway count table supported the same calibration: `Fzd2`, `Fzd4`, `Fzd6`, and `Fzd9` all had 0 DEGs; `Lrp1`, `Lrp2`, `Lrp4`, `Lrp5`, and `Lrp8` all had 0; only `Lrp6` had a small receptor-level response of 4.

## Target-specific reasoning

### `Tspan12`

External biology places TSPAN12 directly in the Norrin-specific FZD4 receptor complex. Junge et al. showed that mouse `Tspan12` promotes Norrin-induced, but not Wnt3A-induced, FZD4/beta-catenin signaling, that `Tspan12` loss phenocopies retinal vascular defects in `Fzd4`, `Lrp5`, and `Norrin` mutants, and that `Tspan12` genetically interacts with `Norrin` or `Lrp5`. Lai et al. subsequently showed that TSPAN12 is a component of the NDP receptor complex, interacting with FZD4 and NDP through extracellular loops and increasing FZD4 selectivity for NDP. Ke et al. and Chang et al. define the Norrin-FZD4-LRP5/6 complex structurally, making `Fzd4`, `Lrp5`, and `Lrp6` the most mechanism-matched training perturbations available here.

Those direct receptor-complex perturbations were nearly silent in the exact held-out readout: `Fzd4` and `Lrp5` each had 0 DEGs, `Kremen1`, another membrane-level Wnt regulator, had 0, and the partially redundant coreceptor `Lrp6` had only 4 weakly significant genes. This is stronger evidence than downstream canonical Wnt perturbations because losing a membrane co-receptor in postmitotic thalamic neurons is expected to be limited by ligand, receptor, and cell-type context, while `Ctnnb1` and `Tcf7l2` act directly on transcriptional regulation and can produce neuronal transcriptional changes without reproducing a selective Norrin-receptor loss.

The nonzero `Ctnnb1` and `Tcf7l2` counts therefore served as boundaries on the module, not as numeric analogs. `Ctnnb1` loss produced 383 DEGs and `Tcf7l2` loss 106 DEGs, including many neuronal/synaptic markers, but perturbing a transcriptional effector is much broader than perturbing one ligand-specific plasma-membrane enhancer. The profile comparison agreed with this: receptor-side `Fzd4`/`Lrp5`/`Lrp6`/`Kremen1` signatures had no to four significant features, whereas `Ctnnb1` and `Tcf7l2` had tens to hundreds.

Generic family membership also did not argue for a broad response. The only training target named `Tspan*`, `Tspan7`, produced just one focal DEG, its own mRNA, and membrane targets `Cd81`, `Cd47`, and `Cdc42` likewise had self-only one-DEG signatures. TSPAN12 is especially unlikely to trigger the endothelial retinal program in this focal readout: Zhang et al. showed that endothelial Tspan12 is required for blood-retina barrier formation and maintenance, and Chidiac et al. showed that a Norrin/Wnt surrogate can rescue retinal endothelial phenotypes in `Tspan12-/-` mice, but the Perturb-seq experiment samples NeuN-enriched neuronal nuclei from juvenile postmitotic brain, not endothelial or retinal vascular cells.

I therefore predict no genes passing FDR 0.05 in `151 TH Prkcd Grin2c Glut` cells after `Tspan12` perturbation. The count most consistent with the direct `Fzd4` and `Lrp5` analogs is 0; giving `Tspan12` the small `Lrp6` value would overstate evidence for an acute neuronal Norrin response that was absent from `Fzd4` itself.

Prediction: `Tspan12 -> 0`.

## Limits of the reasoning

- The Distributed Agents same-experiment corpus did not cover `Tspan12`, so the target-specific mechanism came from PubMed literature rather than from a curated corpus neighborhood.
- `Fzd4`, `Lrp5`, and `Lrp6` are close pathway analogs but not identical to `Tspan12`: TSPAN12 is Norrin-selective, whereas LRP5/6 can participate in other canonical Wnt receptor complexes.
- The strongest TSPAN12 biology is endothelial and retinal. It is biologically relevant because it identifies the receptor complex, but it is an imperfect match to sparse neuronal CRISPR in whole brain NeuN+ nuclei.
- The DEG count is sensitive to guide efficiency, target expression, and matched-cell statistical power. A self-transcript-only outcome like `Tspan7`, `Cd81`, or `Cd47` is possible if `Tspan12` is expressed and edited in this focal neuronal group, but the direct FZD4/LRP5 evidence makes a zero call more plausible.
