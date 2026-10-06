# DEG-count prediction trace

## Question and resolved ambiguities

The held-out manifest for this run contains one perturbation, `Lmbr1`. I interpreted the requested endpoint as:

- focal cell group: `151 TH Prkcd Grin2c Glut`;
- endpoint: the number of measured genes with `pvals_adj < 0.05` in the held-out `Lmbr1` CRISPR perturbation;
- point prediction: one non-negative integer, with zero meaning that no measured gene, including `Lmbr1` itself if present in the feature set, is expected to pass the BH-adjusted Wilcoxon threshold.

I treated the AAV perturbation as a sparse, postnatal, coding loss-of-function perturbation. I did not interpret it as a germline deletion of the `Lmbr1` locus, as deletion of the intronic ZRS limb enhancer, or as conditional deletion in an embryonic limb-bud context.

## Sources used

- `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`: observed training `n_degs` values for the focal cell group.
- `training_de_all_cell_groups.parquet`: focal expression signatures for mechanistic analogs and counterexamples.
- Distributed Agents corpus release `perturbai-july-260713-sourceguard-1773-v1`: queried `Lmbr1` target context, finding inventory, and pathway ledger. This release had no `Lmbr1`-scoped claims, findings, explicit references, or pathway records, so it did not provide a curated same-experiment mechanistic story for the target.
- Distributed Agents runtime `profile_neighbors`: used for a small declared cohort of LMBR, Hedgehog, ciliary, Wnt/LRP, FGF, and limb-patterning candidates. The artifact is `profile_neighbors_lmbr1_analogs.json`.
- External literature:
  - Lettice et al. 2003, PMID 12837695, DOI `10.1093/hmg/ddg180`: identified the ZRS as a long-range limb enhancer located in `Lmbr1` intron 5 that regulates `Shh`.
  - Lettice et al. 2014, PMID 24715461, DOI `10.1242/dev.095430`: dissected ZRS domains needed for robust long-range limb-bud `Shh` activation and five-digit patterning.
  - Laurell et al. 2012, PMID 22495965, DOI `10.1002/humu.22097`: showed that human noncoding variants in the ZRS/LMBR1 enhancer can drive ectopic enhancer activity and preaxial polydactyly.
  - Ushiki et al. 2021, PMID 33863876, DOI `10.1038/s41467-021-22470-z`: fine-mapped acheiropodia-associated deletions in the human `LMBR1` region to noncoding CTCF sites that alter ZRS-SHH enhancer-promoter communication.

## Computations over the input data

The focal training endpoint had 1,674 non-held-out perturbations. Its distribution was very sparse: median 0 DEGs, 75th percentile 1 DEG, and 469 perturbations with any DEG. The highest-count perturbations, such as `Uba5` at 2,677 DEGs and `Tpr` at 1,768 DEGs, showed that the cell group had ample power to score broad perturbation responses when present.

Because the parquet has 616,253,184 rows, I used Parquet row-group metadata to restrict reads to the `151 TH Prkcd Grin2c Glut` row groups. For each candidate analog I then filtered by `group_name` and `gene_target` and counted rows where `pvals_adj < 0.05`, matching the supplied count file:

```python
mask = pc.and_(
    pc.equal(table["group_name"], "151 TH Prkcd Grin2c Glut"),
    pc.equal(table["gene_target"], target),
)
n_sig = int((filtered["pvals_adj"] < 0.05).sum())
```

I also scanned the focal row groups for self-rows where `names == gene_target`. Of the 1,642 training targets with a measured self-row, 319 had a significant self-row, and 237 of those were exactly `n_degs = 1`. This made it important not only to ask whether `Lmbr1` should trigger a pathway response, but also whether the best family analog suggested a self-only count.

## Target-specific evidence

### `Lmbr1`

The strongest external biology around `Lmbr1` is not a neuronal regulatory role of the LMBR1 protein. It is the noncoding ZRS/MFCS1 enhancer embedded in intron 5 of `LMBR1`, which controls limb-bud `SHH/Shh` expression from long range and whose point mutations, insertions, duplications, or local chromatin-architecture deletions alter limb patterning in embryos. Those papers are highly relevant for annotating the locus, but the experiment here should disrupt the `Lmbr1` coding sequence in postmitotic juvenile neurons rather than the ZRS enhancer itself.

The focal training evidence around both plausible interpretations of `Lmbr1` was quiet:

| training perturbation | observed `n_degs` | focal expression evidence | relevance |
|---|---:|---|---|
| `Lmbrd1` | 1 | One significant row, `Lmbrd1` itself, log2FC = -0.606 and q = 0.00338; next best q = 0.247 | Only LMBR-domain coding perturbation in the training count file. It supports at most a self-transcript event, not a broader state. |
| `Smo` | 0 | No significant rows; target self-row log2FC = -0.152, q = 1 | Core Hedgehog transducer and a direct test of whether Hedgehog signaling is active in this focal postnatal population. |
| `Ptch1` | 0 | No significant rows; target self-row log2FC = -0.390, q = 1 | Canonical Hedgehog receptor and transcriptional target, silent here. |
| `Ptch2` | 0 | No significant rows; minimum q = 1 | Hedgehog receptor paralog, silent here. |
| `Gli1` | 0 | No significant rows; target self-row q = 1 | Canonical transcriptional effector and readout of high Hedgehog pathway activity. |
| `Gli2` | 0 | No significant rows; target self-row q = 1 | Hedgehog transcriptional activator, silent here. |
| `Gpr161` | 0 | No significant rows; minimum q = 1 | Negative ciliary regulator of Hedgehog signaling. |
| `Ift43`, `Ift81`, `Ift88`, `Bbs5` | all 0 | No significant rows; minimum q values 0.847, 0.391, 1, and 0.220 | Ciliary transport genes needed for Hedgehog transduction, used as counterexamples to a hidden cilia/Hedgehog state. |
| `Lrp6` | 4 | Four weakly significant off-target rows, all q = 0.0406; `Lrp6` self-row q = 1 | A low-count Wnt co-receptor perturbation, not close enough to override the Hedgehog and LMBR evidence. |
| `Lrp1`, `Lrp2`, `Lrp5` | all 0 | No significant rows | LRP-family counterexamples. |
| `Hoxa13`, `Hoxd13` | both 0 | No significant rows | Embryonic limb-patterning genes, included as developmental-context counterexamples. |
| `Zic1`, `Zic2` | 2 and 0 | `Zic1` had 2 DEGs including itself; `Zic2` had no DEGs | Developmental transcription-factor comparators with only self/small responses. |

Within the small declared analog cohort, `profile_neighbors` found no active signature cluster centered on Hedgehog genes. `Lmbrd1`, `Smo`, `Ptch1`, `Gli1`, `Gli2`, and `Gpr161` had 17,259 features in the focal context; `Lmbrd1` was classified as `1_to_9_significant_features` and the other five as `no_significant_features`. Whole-profile Pearson similarities among the quiet analogs were moderate, for example `Smo` to `Ptch1` at 0.683 and `Lmbrd1` to `Bbs5` at 0.692, but the overlap came from weak nonsignificant tails rather than a shared FDR-significant response.

### Zero/nonzero decision and count

I predict `Lmbr1` will have **0 DEGs**.

The decision is driven first by the within-dataset evidence: the direct Hedgehog signaling perturbations and the ciliary machinery needed for Hedgehog signal transduction were all exactly zero in `151 TH Prkcd Grin2c Glut`, and the only LMBR-domain analog was a one-DEG, target-only perturbation. It is driven second by the external mechanism: the dramatic `Lmbr1` locus phenotypes in the literature mostly reflect embryo-specific control of `Shh` by noncoding ZRS/CTCF elements, which are not what an exon-targeting AAV CRISPR coding perturbation should disrupt in postnatal neurons.

The main counterargument is the self-row calibration. Hundreds of otherwise quiet perturbations in the training set became `n_degs = 1` because their own transcript was significantly reduced, and `Lmbrd1` was one of them. That makes `1` a plausible alternate point prediction. I kept the point estimate at `0` because most focal perturbations had no significant self-row, direct Hedgehog components did not even score themselves, and I found no same-experiment evidence that `Lmbr1` belongs to an active transcriptional module in this cell group.

## Limits

- `Lmbr1` itself was held out completely, so there is no observed `Lmbr1` guide performance, target-RNA log fold change, or focal signature to inspect.
- The closest same-domain comparator was `Lmbrd1`, but `LMBRD1` has a lysosomal cobalamin-transport role whereas `LMBR1` is best known as a locus containing the ZRS enhancer; it is a structural family analog, not a clean pathway paralog.
- The Hedgehog/ZRS literature is embryonic and limb-bud focused. It supports low expected relevance in juvenile neurons, but it does not prove that the `Lmbr1` coding gene is inert in every postnatal neuronal class.
- The exact integer near zero is intrinsically assay-power dependent. A small difference in matched edited nuclei or guide knockdown could move a self-only perturbation between 0 and 1 DEG without implying a biologically broad state.
