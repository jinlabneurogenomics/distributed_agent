# Q3 Literature Specificity Methods

## Eligibility

I filtered the parquet to the 205 exact `gene_target` values in `n0205.targets.json`, retained only rows whose `group_name` was one of the 23 allowed cell groups, and called an eligible perturbation by cell-type pair when at least one downstream row satisfied:

```text
pvals_adj < 0.10 and lower(names) != lower(gene_target)
```

The target-transcript row was therefore excluded before eligibility was counted. This yielded 915 eligible pairs from 205 manifest perturbations; all 915 are emitted in `q3_cell_type_specificity.jsonl`, and no ineligible pair is emitted.

## Phenotype Characterization

For every eligible pair I tabulated all FDR-significant non-target genes, the number of up- and down-regulated genes, the matched perturbed and control cell counts, and the most significant genes ordered by adjusted Wilcoxon p-value with absolute log-fold change as a tie-breaker. Large responses were reduced to the dominant FDR-supported module only when the significant genes matched a coherent predefined marker set: ER/UPR or integrated stress response, heat-shock chaperones, SREBP/sterol biosynthesis, immediate-early neuronal activity genes, Wnt/beta-catenin targets, or RB1/E2F DNA-replication targets. Sparse pairs and pairs whose significant genes did not form one of these modules were summarized by their top measured genes.

## Literature Search and Flagging

PubMed queries were built from each target and its observed module or top genes, starting with specific target-plus-marker searches and then broadening to documented mechanisms when exact marker lists were over-constrained. The reviewed searches covered direct papers or reviews for MANF-BiP and MANF ER stress, SERCA2 loss and ER stress, GFPT1/O-GlcNAc control of eIF2alpha and CHOP, GRP78/BiP control of UPR sensors, HSF1 heat-shock transcription, SREBP2 sterol transcription, TSC/mTORC1/SREBP signaling, MARCH6/SREBP signaling, RB1/E2F replication programs, APC or LRP6 Wnt output, KCC2 hyperexcitability and Fos induction, and VGF-BDNF/TrkB feedback.

`Agree` was used when a target-specific relationship or a complete cited chain predicted the observed direction despite differences in species, cell type, stage, or perturbation modality. `Inferred` was used for biologically specific but incomplete chains, such as GFPT1 feeding O-GlcNAc/eIF2alpha ER-stress regulation or Ntrk2 perturbation intersecting a VGF-BDNF/TrkB loop without a decisive acute Ntrk2-loss RNA prediction. `No Literature` was reserved for pairs where searches for the target together with the measured top genes or module found no direct relationship and no biologically specific partial bridge.

## Multi-Module and Low-Confidence Cases

If a pair contained several significant modules, the pair-level flag follows the module with the strongest target-specific prior among the most significant downstream genes. Different incidental genes are still retained in the evidence top-gene list but do not drive the literature flag. The main low-confidence calls are the `Inferred` ER-stress calls for `Gfpt1` and `Hspa5` and the VGF call for `Ntrk2`, where the literature supplies a relevant pathway bridge but not a directly documented transcriptomic expectation in the screened neuronal groups.

## Totals

- Eligible pairs: 915
- Emitted pair rows: 915
- Evidence rows: 915
- Cited references: 17
- Flag counts: {"Agree": 50, "Inferred": 10, "No Literature": 855}
- Incompletely reviewed pairs: 0
