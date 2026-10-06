# Gata2 prediction trace

## Question and interpretation

The requested held-out target is `Gata2` from `088_Gata2.csv`.  I interpreted the endpoint as the exact focal-class scalar

```
count of measured genes with pvals_adj < 0.05
for gene_target == Gata2
and group_name == "151 TH Prkcd Grin2c Glut"
```

where the differential-expression contrast is knockout nuclei versus the matched non-targeting control.  `Gata2` is absent from both the per-gene DE parquet and the focal training-count CSV, so there is no direct same-experiment Gata2 signature to score.  I used the training perturbations only as analogs.  I also treated `TH` in the cell label as the atlas abbreviation for thalamus, not tyrosine hydroxylase; the focal cells are thalamic glutamatergic neurons.

## Sources

- `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`
  - 1,674 non-held-out focal-class training counts.
  - Calibration in the supplied run files: 1,205/1,674 targets had `n_degs = 0`, 363 had 1-9, 63 had 10-99, and 43 had at least 100.
- `[local file: training_de_all_cell_groups.parquet]`
  - I filtered the 616,253,184-row DE table to `group_name == "151 TH Prkcd Grin2c Glut"` and counted `pvals_adj < 0.05` for candidate analogs.  The parquet is row-grouped by `group_name`; row groups 546-580 cover this focal block.
- Distributed Agents same-experiment corpus `perturbai-july-260713-sourceguard-1773-v1`
  - `target_context("Gata2")` returned no same-experiment Claims or Findings for the held-out target.
  - `target_context` and `inventory` for `Gata1`, `Gata3`, `Gata4`, `Gata6`, `Gfi1b`, `Klf1`, `Gatad2b`, `Etv6`, `Sox2`, and `Tcf3` supplied curated interpretations of their training signatures and explicit GATA-family / hematopoietic-TF comparisons.
- External biology
  - Tsai and Orkin 1997, PMID 9160668: mouse GATA-2 is required for proliferation and survival of early hematopoietic progenitors and mast-cell formation.
  - Kala et al. 2009, DOI `10.1242/dev.029900`, PMID 19088086: embryonic mouse Gata2 is a postmitotic selector for midbrain GABAergic neurons.
  - Haugas et al. 2016, DOI `10.1242/dev.136614`, PMID 27789623: Gata2 acts upstream of Gata3 in embryonic dorsal-raphe serotonergic and Vglut3-positive glutamatergic subtype differentiation.
  - Allen Mouse Brain Atlas / Lein et al. 2007, DOI `10.1038/nature05453`, PMID 17151600: adult in situ atlas used as a qualitative prior that `Gata2` is not a broad adult thalamic-neuron marker.

## Computational checks

I first loaded the requested-target manifest and verified that this run requests only `Gata2`.  I then read the focal training-count CSV and pulled all represented GATA-family and blood-lineage neighbor counts.  For exact focal expression-pattern evidence, I queried the parquet with:

```sql
SELECT
  gene_target,
  SUM(pvals_adj < 0.05) AS n_fdr05,
  SUM(pvals_adj < 0.10) AS n_fdr10,
  MIN(pvals_adj) AS min_padj,
  ARG_MIN(names, pvals_adj) AS min_padj_gene
FROM read_parquet('training_de_all_cell_groups.parquet')
WHERE group_name = '151 TH Prkcd Grin2c Glut'
  AND gene_target IN (...)
GROUP BY gene_target;
```

The closest focal-class counts were:

| training perturbation | focal `n_degs` | focal `n_fdr10` | minimum focal FDR | why I used it |
| --- | ---: | ---: | ---: | --- |
| `Gata1` | 0 | 0 | 0.989 | GATA-family hematopoietic paralog; corpus reports a pan-neuronal FDR 0.10 null and absent erythroid/megakaryocytic circuit |
| `Gata3` | 0 | 0 | 0.159 | closest represented neural GATA analog; Gata2 acts upstream of Gata3 in embryonic raphe work, but the Gata3 perturbation was silent in the focal class |
| `Gata4` | 0 | 0 | 1.000 | GATA paralog with strong non-neuronal developmental programs; focal response absent |
| `Gata6` | 0 | 0 | 1.000 | GATA paralog; corpus reports a single FDR 0.10 Nsun2 event in a different GABAergic class and no Gata1/3/4 convergence |
| `Zfpm2` | 0 | 0 | 1.000 | Friend-of-GATA family neighbor present in the parquet; no focal response |
| `Klf1` | 0 | 0 | 1.000 | erythroid TF downstream/adjacent to GATA programs; no focal response |
| `Gfi1b` | 0 | 0 | 0.267 | hematopoietic zinc-finger TF and GATA1/GATA2-lineage neighbor; no focal response |
| `Spi1` | 0 | 0 | 1.000 | represented hematopoietic TF countercheck; no focal response |
| `Epor` | 0 | 0 | 1.000 | represented erythroid effector expected in blood-lineage GATA circuitry; no focal response |
| `Mpl` | 0 | 0 | 1.000 | represented megakaryocytic effector; no focal response |
| `Etv6` | 1 | 1 | 1.99e-7 | weak hematopoietic TF response: one `Adora1` hit in the focal class, not a GATA-like program |
| `Zbtb7a` | 841 | 1079 | 1.22e-41 | broad active lineage/chromatin TF counterexample showing that hematopoietic associations alone were not forced to zero in this assay |

The corpus supported the same separation.  It reports that represented GATA perturbations do not form a shared postmitotic neuronal module; specifically, `Gata3:F003` found that `Gata1`, `Gata4`, `Gata6`, `Isl1`, `Lmx1b`, `Slc32a1`, and `Zfpm2` did not phenocopy `Gata3`, and `Gata6:F004` found that `Gata1`, `Gata3`, `Gata4`, and `Hnf4a` were nearly orthogonal to `Gata6`.  `Gata1:F002` directly named `Gata2`, `Zfpm1`, `Tal1`, `Lmo2`, and `Ldb1` as expected blood-circuit genes that were not recovered through the represented neuronal GATA1/KLF1/GFI1B perturbations.

## Target-specific reasoning

### `Gata2`

`Gata2` is a zinc-finger GATA transcription factor, so the most relevant within-dataset comparators are the assayed GATA paralogs and GATA-associated hematopoietic partners rather than all transcription factors in bulk.  In the focal thalamic glutamatergic class, every directly assayed GATA paralog was exactly zero at FDR 0.05: `Gata1 = 0`, `Gata3 = 0`, `Gata4 = 0`, and `Gata6 = 0`.  Their weakest focal-class adjusted p-values were not just barely above 0.05 for the off-axis paralogs (`Gata1`, `Gata4`, `Gata6` all had minimum FDR near 1), and the biologically closest neural paralog `Gata3` still had no FDR 0.10 genes in the focal class.

That comparison is mechanistically imperfect but useful.  `Gata2` has embryonic neuronal functions: it selects midbrain GABAergic identity and participates with `Gata3` in dorsal-raphe serotonergic / Vglut3-positive glutamatergic differentiation.  Those are developmental midbrain and hindbrain programs, however, whereas the held-out endpoint is an acute P16-to-P37/P44 knockout in recovered postmitotic thalamic glutamatergic neurons.  The same experiment directly tested `Gata3`, the represented partner in the raphe literature, and found it almost completely buffered in postnatal NeuN+ neurons rather than converting sampled glutamatergic cells into a raphe or GABAergic fate program.

The hematopoietic side of GATA2 biology also points toward no focal neuronal footprint.  `Gata2` is central to early hematopoietic progenitor survival and works in GATA/TAL/LMO/FOG/KLF circuits, but the NeuN-enriched screen lacks those blood lineages.  Represented pieces of the same lineage space were silent in the focal class: `Klf1`, `Gfi1b`, `Epor`, `Mpl`, and `Spi1` all had zero focal DEGs, and the corpus reports that canonical globin, heme, platelet, `Klf1`, and `Zfpm1` outputs were absent after the represented GATA1/KLF1/GFI1B perturbations.  `Zbtb7a` is the main counterexample, with 841 focal DEGs, but it is a pleiotropic chromatin/lineage regulator whose strong thalamic signature diverged from `Gfi1b` and from the null GATA-family surfaces; I therefore treated it as evidence that the assay could see broad TF responses, not as a quantitative proxy for Gata2.

Prediction: `Gata2` should be transcriptionally buffered in `151 TH Prkcd Grin2c Glut` and should not generate a gene passing FDR 0.05.  I assign `0`.

## Limits

- The largest limitation is that `Gata2` itself was held out completely and had no root entry in the same-experiment Distributed Agents corpus, so the prediction is extrapolated from paralogs and pathway neighbors.
- The closest developmental Gata2 evidence comes from embryonic midbrain and anterior-hindbrain nuclei, not juvenile thalamic glutamatergic neurons.  A rare Gata2-dependent subpopulation inside the broad `151` class could be diluted.
- Important GATA2 partners such as `Tal1`, `Lmo2`, `Ldb1`, and `Zfpm1` were checked as measured transcripts but were not perturbation targets in this training parquet.
- Sparse AAV CRISPR in recovered nuclei can miss survival or fate effects that deplete cells before capture.  Conversely, absence of measured target-RNA knockdown would not prove failed editing, so I did not use self-transcript fold change as an editing-efficiency filter.
- The final point estimate intentionally rounds a low expected count down to zero because all directly represented GATA-family focal counts were zero and the positive blood/TF counterexamples were mechanistically more distant.
