# DEG-count prediction trace

## Question and endpoint

I interpreted the task as a one-target holdout prediction for `Crebrf`: estimate the number of genes that would pass BH-adjusted Wilcoxon `pvals_adj < 0.05` after acute sparse CRISPR loss of `Crebrf` in the focal `151 TH Prkcd Grin2c Glut` thalamic glutamatergic class. The output is a scalar count, not a ranked list. I therefore used the supplied training `n_degs` column as the directly observed endpoint for held-in perturbations and the focal rows of `training_de_all_cell_groups.parquet` as the direct expression-pattern evidence for those same perturbations.

I resolved one ambiguity conservatively: `n_degs = 0` means that no measured transcript is predicted to survive the same FDR 0.05 threshold, not that `Crebrf` has no biological function or that editing failed. The training readout conditions on recovered NeuN-positive nuclei 3-4 weeks after P16 AAV CRISPR, so survivor-conditioned weak signatures and true biological buffering can both appear as small counts.

## Sources used

- Declared endpoint table: `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
- Declared DE table: `training differential-expression dataset`, filtered to `group_name == "151 TH Prkcd Grin2c Glut"` and to mechanistic comparator targets.
- Held-out manifest: `single-target request for Crebrf`; it contains only `Crebrf` and that target is absent from the training count table.
- Internal same-experiment interpretation: `perturbai-july-260713-sourceguard-1773-v1`, especially the `Atf6`, `Hspa5`, `Hsf1`, `Manf`, `Ogt`, and `Creb1` Finding ledgers. These reports are curated summaries of the same Perturb-seq experiment, not independent replication.
- External literature from PubMed:
  - Audas et al. 2008, DOI `10.1128/MCB.01439-07`, PMID `18391022`: CREBRF/Luman recruitment factor is a UPR-responsive unstable bZIP protein that binds Luman/CREB3, can recruit the nuclear form of Luman to nuclear foci, promotes its turnover, and in mouse embryonic fibroblasts Crebrf loss elevated only a few UPR genes such as `Ddit3`, `Edem`, and `Herp`.
  - Oh-Hashi et al. 2021, DOI `10.1007/s11033-021-06543-2`, PMID `34275032`: in Neuro2a cells, intrinsic CREBRF was negligible under tested conditions and overexpressed CREBRF positively regulated the CREB3 pathway in a way distinct from the canonical ER-stress pathway.
  - Le and Kimata 2021, DOI `10.1247/csf.21015`, PMID `33775971`: in metazoans, BiP/HSPA5, IRE1, PERK, and ATF6 form the core ER-stress sensor architecture, with BiP serving as one regulator of these sensors.

## Computation over the training data

I first read the training count CSV to establish the focal-count distribution and exact counts for plausible `Crebrf` comparators. The distribution is zero-inflated and heavy-tailed: 469 of 1,674 held-in perturbations are nonzero at FDR 0.05, the median is 0, the 75th percentile is 1, the 95th percentile is 18, and the highest outliers are essential regulators such as `Uba5`, `Tpr`, `Sin3a`, `Rnpc3`, `Zbtb7a`, and `Psmb4`.

For expression-pattern evidence, I did a bounded Parquet query rather than scanning every row:

```python
ds.dataset(parquet).to_table(
    columns=["names", "scores", "logfoldchanges", "pvals_adj",
             "group_name", "gene_target", "n_pert_matched", "n_ctrl_matched"],
    filter=(pc.field("group_name") == "151 TH Prkcd Grin2c Glut") &
           pc.field("gene_target").isin(comparator_targets),
)
```

## Target-specific reasoning

### `Crebrf`

**Direct status.** `Crebrf` is absent as a training endpoint and therefore has no focal DE signature or `n_degs` in the supplied inputs.

**Closest held-in pathway controls.**

| held-in perturbation | focal `n_degs` | focal expression evidence and interpretation |
| --- | ---: | --- |
| `Atf6` | 0 | No genes passed FDR 0.05 in 177 recovered 151 nuclei. The same-experiment `Atf6` report calls this a broad basal null across neuronal groups and notes that expected ER chaperone, ERAD, `Xbp1`, and `Ddit3`/`Atf4` readouts were absent at FDR 0.10. Because ATF6 is a canonical ER-stress bZIP sensor downstream of BiP, this is a strong counterexample to promoting `Crebrf` merely because it is connected to CREB3/UPR transcription. |
| `Hspa5` | 5 | The 151-class FDR 0.05 hits were `Erc1` down and `Hsp90b1`, `Nfe2l1`, `Pdia4`, `Derl3` up. The internal Hspa5 report confirms a compact ER folding/ERAD response rather than a broad neuronal program. This proves that the assay could detect an ER-quality-control response in this cell class, but direct BiP depletion itself was still only a 5-DEG event at the requested threshold. |
| `Manf` | 3 | `Hspa5`, `Pdia6`, and `Manf` were significant in 151. MANF is a BiP/IRE1-linked ER stress regulator in the internal report, and its perturbation produces an adaptive chaperone signature without the stronger terminal ISR markers. This is a partial positive analog for a mild ER-stress regulator and supports only a very small expected count. |
| `Sec63` | 11 | `Sec63`, a BiP-cycle ER-translocation cofactor, had `Hspa5`, `Canx`, `Hyou1`, and `Chac1` among 11 focal hits. It is more proximal to ER client handling than CREBRF, so its larger count is an upper comparator rather than a direct template. |
| `Edem3`, `Sil1`, `Vcp` | 0, 0, 2 | These same internal Hspa5-report relatives did not recapitulate the Hspa5 signature in matched 151 neurons. They argue against assigning every ER-proteostasis-associated target a detectable UPR count. |

**Stronger ER-load counterexamples.**

`Atp2a2`, `Gfpt1`, and `Dhdds` were much larger in the focal class, with 187, 311, and 116 DEGs. Their top rows contained direct ER-load or ISR/UPR markers: `Atp2a2` loss induced `Ddit3`, `Chac1`, `Xbp1`, `Herpud1`, `Hspa5`, and `Asns`; `Gfpt1` loss induced `Herpud1`, `Asns`, `Ddit3`, `Hspa5`, `Chac1`; `Dhdds` loss induced `Chac1` and `Shmt2`. I treated these as counterexamples, not as anchors for a high `Crebrf` prediction, because they perturb ER calcium, hexosamine/N-glycosylation supply, or dolichol supply directly. CREBRF instead regulates the CREB3/Luman branch and does not by itself create the same unfolded-protein load.

**CREB/transcription-factor comparisons.**

The nearest broad transcriptional controls were also small: `Creb1` had 10 focal DEGs and `Crebbp` had 8. The `Creb1` report showed a sparse 151 response centered on `Crem` induction and down-regulated ER/lipid/lysosomal/heme/membrane markers, while a canonical BDNF/Fos/Arc/Npas4 immediate-early program was absent. The focal Parquet rows showed no FDR 0.05 overlap between `Creb1` and `Crebbp`, or between either of these and `Atf6`; thus CREB-family naming does not transfer to the requested endpoint. Other single transcription/stress regulators with at least superficial relevance were zero or nearly zero: `Glis3` 0, `Nfe2l1` 0, `Nfe2l2` 0, `Jund` 0, `Fosl2` 0, and `Hif1a` 0. `Hsf1` had 6 genes, all a direct heat-shock/HSP90/HSP110 module, and did not activate a secondary UPR/ISR program.

**External mechanism and expected endpoint.**

External data establish CREBRF as a CREB3/Luman-interacting, proteasome-labile regulator of stress transcription, but not as an obligate ER chaperone, UPR sensor, or neuronal survival factor. Audas et al. found mild derepression of selected UPR transcripts in Crebrf-deficient MEFs; Oh-Hashi et al. found negligible intrinsic CREBRF in Neuro2a cells and a CREB3-potentiating overexpression effect distinct from canonical ER stress. This gives `Crebrf` a plausible connection to basal ER/CREB3 transcription but leaves the perturbation one or more steps upstream of the ER-load states that were broad in the training set:

`Crebrf` loss -> altered CREB3/Luman localization, turnover, or transactivation -> possible small change in ER-stress target transcription -> only if 151 thalamic neurons require that branch basally, a detectable Wilcoxon/FDR response among recovered nuclei.

The transfer to a high count fails at the "direct molecular consequence to ER load" step: no evidence shows that losing CREBRF in juvenile postmitotic thalamic neurons creates the same limiting ER calcium, glycosylation, or client-chaperone defect as `Atp2a2`, `Gfpt1`, `Dhdds`, `Sec63`, or `Hspa5` perturbation. The closest held-in TF/sensor analog, `Atf6`, was exactly zero with good focal recovery, and the positive `Hspa5` and `Manf` controls were only 5 and 3 DEGs.

**Point decision.**

I therefore predict that acute mosaic `Crebrf` loss will sit below the FDR 0.05 detection threshold in `151 TH Prkcd Grin2c Glut`: `predicted_n_degs = 0`. If it is not exactly zero, the plausible miss is a very small ER-chaperone tail of the same order as `Manf` or `Hspa5`, not a broad 100-300-gene UPR.

## Limits

The largest limitation is that the cleanest molecular comparator, `Creb3/Luman`, and the other CREB3-family factors were not available as held-in perturbations in the training endpoint table. The CREBRF literature is also cell-type limited: MEFs and Neuro2a overexpression constrain the molecular function but do not directly measure acute `Crebrf` loss in P16-edited thalamic neurons. The ER-stress comparisons are same-experiment evidence rather than independent replication, and the focal Parquet contains differential summaries, not raw counts, Xbp1 splicing, eIF2alpha phosphorylation, ATF6 or CREB3 cleavage, DNA indels, or loss of edited cells before nuclei were recovered. Those gaps all make the exact integer uncertain; they do not provide candidate-specific evidence for a broad focal DEG burden.
