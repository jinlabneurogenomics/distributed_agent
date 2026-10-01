# Supplementary Figure 9C source

Original analysis directory:

`/gpfs/home/asun/jin_lab/bioagents-node-neighborhood-inspection/debug/260923_toolbox_original_holdout272_3x`

The focused copy retains the exact original heatmap script, the materialized
272-target merged prediction table, and both archived figure exports:

- `analysis/plot_distributed_agents_spearman_heatmap.py`
- `analysis/distributed_agents_3x_merged.tsv`
- `source_outputs/distributed_agents_3x_spearman_heatmap.png`
- `source_outputs/distributed_agents_3x_spearman_heatmap.svg`

The source script obtains its prediction matrix through `load_data()` in the
adjacent broader comparison script. The materialized table makes the notebook
self-contained. Following the source column order and labels, rep1 is
`original_bioagents`, rep2 is `toolbox_rep_1`, and rep3 is `toolbox_rep_2`.
Spearman correlation across those 272 paired predictions gives 0.68086878,
0.75972224, and 0.74301912, displayed as 0.68, 0.76, and 0.74.
