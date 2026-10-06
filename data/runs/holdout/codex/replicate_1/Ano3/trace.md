# Ano3 direct DEG-count forecast

## Endpoint and declared target

- Target: `Ano3`, from the one-row holdout manifest `Ano3.csv`.
- Endpoint: `n_degs` in `151 TH Prkcd Grin2c Glut`, defined by the task as the count of measured genes with BH-adjusted Wilcoxon `p < 0.05`.
- Direct endpoint table used for training counts: `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
- Direct differential-expression table used for analogue profile checks: `training_de_all_cell_groups.parquet`, filtered to `group_name == "151 TH Prkcd Grin2c Glut"`.
- Target biology source: the declared canonical `biology_bundles/Ano3.json` card, served through `characterization_bundle(view="biology")`; the bundle reports `target_outcome_exposed=false` and `labeled_neighbors_exposed=false`.

## Quantitative base rate in the matched cell class

The matched `151` training count table contains 1,674 observed training perturbations.

- 1,205 / 1,674 were `0`, so the zero fraction was 0.720.
- The median count was `0`; the 75th percentile was `1`; the 90th percentile was `2`.
- The mean count was 14.05, but that was dominated by a small heavy tail headed by essential regulatory targets such as `Uba5`, `Tpr`, `Sin3a`, and spliceosome/proteasome factors. Those are not close Ano3 analogues.

So an unforced P16 neuronal membrane/channel perturbation starts near 0-1 DEGs in this focal class, not near the long-tailed arithmetic mean.

## Ano3 biology and reach

The declared Ano3 biology card supports a possible neuronal operation but not a large matched transcriptional state:

- In the exact focal population, `Ano3` was measurable but low: `mean_cp10k = 0.1083`, `pct_cells_expressing = 12.61`, and `mean_raw_umi = 0.1846` in non-target cells.
- ANO3/TMEM16C has calcium-dependent phospholipid-scrambling evidence and a Slack/KCNT1 regulatory relationship, but those functional data come from heterologous cells or rat DRG rather than mouse thalamic neurons.
- The card adjudicates the operative stock at the 21-28 day harvest as `indeterminate`: editing stops new intact ANO3 supply, but existing membrane-associated ANO3 protein, channel-associated state, or lipid state need not be fully cleared by harvest, and no Ano3-specific turnover clock was located.
- The card does not supply a same-context acute loss phenotype, and the adult rat DRG phenotype mainly establishes that complete ortholog loss can matter in another neuronal context.

Those features push downward: Ano3 is present in the target class, so I did not treat it as impossible, but low exact reach plus unresolved realization makes a broad snRNA-seq response unlikely.

## Training perturbations used as analogues

No `Ano*` paralog perturbation was present in the training count table. The closest declared functional link was KCNT1/Slack, so I inspected KCNT1, KNa/KCa relatives, and a small set of other neuronal channel perturbations in the exact `151` context.

Direct count-table values:

- `Kcnt1 = 0`
- `Kcnt2 = 0`
- `Kcnma1 = 1`
- `Kcnn2 = 0`
- `Kcnn3 = 0`
- among all 20 `Kcn*` perturbations in the count table, every value was `0` or `1`
- additional low channel checks were similar: `Clcn3 = 0`, `Clcn4 = 1`, `Grin2a = 1`, `Grin2b = 2`, `Grin2d = 0`, `Grin3a = 0`

The raw parquet confirmed that these were genuinely tiny observed profiles in the focal class. `Kcnt1` and `Kcnt2` each had zero significant genes with minimum adjusted p-value `1.0`; `Kcnma1`, `Kcnq2`, `Kcnq3`, `Clcn4`, and `Grin2a` each had exactly one significant gene, dominated by the perturbed transcript itself. The only channel-like perturbation I checked with a larger count was `Cacna1g`, at 12 DEGs; that is a thalamic T-type calcium-channel alpha subunit and is less operation-matched to an intracellular TMEM16C/KCNT1 modulator than the zero-count KNa/KCa set.

The same-experiment Kcnt1 corpus report was consistent with these measurements but not treated as independent replication. Its `Kcnt1:F001` Finding described Kcnt1 LoF as FDR-null across all recovered neuronal groups, and `Kcnt1:F002` described Kcnt2, Kcnma1, Kcnn2, and Kcnn3 as closest Na+/Ca2+-activated K+ channel relatives that were also nearly transcriptome-flat.

I also wrote a symmetric profile comparison for 16 channel/NMDA perturbations to `workbench/channel_profile_compare.json` and summarized it into `workbench/channel_profile_cohort.json`. In that cohort, 9/16 nodes had no significant features in the `151` profile, 6/16 had only 1-9 significant features, and only `Cacna1g` entered the 10-49 bin. There was no significant-program overlap among the closest Kcnt1/Kcnt2/Kcnn/Kcnma nodes, supporting use of the individual near-zero counts rather than a hidden shared module.

## Forecast

I assigned the most weight to the direct KCNT1/KNa/KCa comparators because Ano3's strongest neuronal operation in the card is KCNT1/Slack regulation. Those comparators are all flat to one-gene in this class, and `Kcnt1` itself is exactly `0`. The broader count distribution and exact Ano3 expression also favor `0`: 72% of all training perturbations are zero in the same focal class, and Ano3 expression reaches only a minority of non-target nuclei at low abundance.

Residual uncertainty is upward but small. Ano3 could score a single self-transcript DEG, as several K+ and NMDA receptor perturbations did, or a few subthreshold activity genes could cross FDR if target disruption is realized quickly enough. I did not see support for a many-gene thalamic survivor-state response.

Point prediction: `0`.
