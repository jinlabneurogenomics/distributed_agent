# Kdm6a DEG-count prediction trace

## Question and resolved ambiguities

The requested endpoint is the integer number of FDR 0.05 Wilcoxon differentially
expressed genes in the held-out perturbation `Kdm6a` in the focal neuronal class
`151 TH Prkcd Grin2c Glut`. I treated `151 TH Prkcd Grin2c Glut` as an Allen
taxonomy thalamic glutamatergic class; `TH` is the thalamus label here, not
tyrosine hydroxylase. The requested target manifest contained one target,
`Kdm6a`, and that target is absent from both supplied training endpoints.

The point prediction below is a direct prediction for this assay-specific DEG
count, not a generic estimate of Kdm6a biological importance, viability, target
editing, or target-RNA knockdown.

## Sources used

* Input training count CSV:
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
  This held-in endpoint table contained 1,674 perturbations. Its distribution
  was very sparse: median 0 DEGs, 75th percentile 1, 90th percentile 2, 95th
  percentile 18, and maximum 2,677.
* Input DE parquet:
  `[local file: training_de_all_cell_groups.parquet]`.
  This is the exact row-level DE table for held-in perturbations, with
  log-fold-changes and adjusted p-values. It has 616,253,184 rows in the full
  file and 17,259 measured focal-cell features for the profiled Kdm6a
  candidate analogs inspected below.
* Distributed Agents selected same-experiment semantic corpus:
  `perturbai-july-260713-sourceguard-1773-v1`. `target_context(Kdm6a)`
  returned no Kdm6a findings or claims in this release; a candidate-set audit
  over Kdm6a plus nominated chromatin analogs found Kdm6a unresolved in the
  corpus while `Kdm6b`, `Kmt2c`, `Kmt2a`, `Kdm5c`, `Setd1a`, `Crebbp`,
  `Ep300`, and `Ogt` formed a report-connected component. I therefore used
  the corpus as a check on held-in analog connectivity, not as target-specific
  Kdm6a evidence.
* Distributed Agents deterministic gene-annotation and gene-analog layers. These supplied
  curated Kdm6a memberships and eligible training analogs from GO, Reactome,
  KEGG, MSigDB, native mouse CORUM, human CORUM complexes projected through
  strict MGI one-to-one orthology, and pinned STRING physical interactions.
  Important records included CORUM v5.0 complex 7785, `Hnf1a-Kdm6a complex`;
  human-ortholog-projected CORUM v5.0 complexes 3075, `UTX-MLL2/3 complex`,
  5195, `PTIP-HMT complex`, 6461, `MLL3 complex`, and 6467, `MLL4 complex`;
  Reactome mouse `R-MMU-3214842`, `HDMs demethylate histones`,
  `R-MMU-9772755`, `Formation of WDR5-containing histone-modifying
  complexes`, and `R-MMU-9818564`, `Epigenetic regulation of gene expression
  by MLL3 and MLL4 complexes`; GO:0071558, histone H3K27me2/H3K27me3
  demethylase activity; and STRING physical v12.0 Kdm6a-Kmt2c and Kdm6a-Crebbp
  links.
* NCBI PubMed/Entrez and prior literature for the core UTX mechanism:
  Agger et al. 2007, PMID 17713478, identified UTX/KDM6A and JMJD3/KDM6B as
  H3K27 demethylases in HOX regulation and development; Lan et al. 2007, PMID
  17923085, also described UTX as an H3K27 demethylase required for posterior
  development. Those papers support a close enzymatic link between Kdm6a and
  Kdm6b but do not show that acute mosaic postnatal neuronal Kdm6a knockout
  must phenocopy Kdm6b in this Perturb-seq cell class.

## Computational evidence

I first used the focal-cell count CSV to read off all held-in analog endpoints.
I then used the gene-analog nominator with the 1,674 focal-cell training targets
as the available universe:

```bash
python .../gene-analog-nomination-skill/scripts/nominate_gene_analogs.py \
  --requested-targets .../119_Kdm6a.csv \
  --species mouse \
  --training-universe .../151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv \
  --out analog_nominations.jsonl
```

That deterministic run ranked `Kdm6b` as the leading available H3K27-demethylase
module member, `Kmt2c` as an exact human-ortholog-projected UTX/MLL complex
member, then broader WDR5/MLL3-4 and chromatin candidates such as `Ogt`,
`Setd1a`, `Ep300`, `Kdm5c`, `Smarca4`, `Pparg`, and `Crebbp`.

For expression-pattern evidence, I ran the Distributed Agents runtime
`profile_compare` on these held-in candidates in context
`group_name = "151 TH Prkcd Grin2c Glut"`, with `gene_target` as the profile,
`names` as the feature, `logfoldchanges` as the signed value, and `pvals_adj <
0.05` as the significance call. I then inspected a Kdm6a-centered cohort and
the relevant pairwise tables. The profile comparison confirmed:

* `Kdm6b`: 0 significant features in the focal cell group.
* `Kmt2c`: 0 significant features.
* `Kmt2a`: 24 significant features, 12 up and 12 down.
* `Kdm5c`: 18 significant features, 17 up and 1 down.
* `Setd1a`: 368 significant features, 69 up and 299 down.

`Kdm6b` and `Kmt2c`, despite mechanistic proximity, had no FDR-significant
features to share with the low nonzero or broad outlier signatures. Their top
ranked log-fold changes in the profile artifact were also nonsignificant
(`pvals_adj = 1`), so I treated their signed tails as weak rank-space hints, not
as a hidden transcriptional program.

## Held-out target reasoning

### Kdm6a

`Kdm6a` encodes UTX, an H3K27me2/H3K27me3 demethylase and a component of
MLL3/MLL4 COMPASS-like enhancer-regulating complexes. The exact or near-exact
assayed analogs argued for a weak effect in this focal population:

| held-in target | n_degs | relevance to Kdm6a | interpretation |
|---|---:|---|---|
| `Kdm6b` | 0 | closest H3K27 demethylase by GO:0071558 and Reactome `HDMs demethylate histones` | strong null boundary; JMJD3/KDM6B shares the substrate class but is not a stable UTX/MLL3-4 subunit |
| `Kmt2c` | 0 | human-ortholog-projected CORUM partner in UTX-MLL2/3, PTIP-HMT, and MLL3 complexes; STRING physical v12.0 neighbor | strong complex-side null boundary; suggests that disrupting one available MLL3 subunit was not enough to make a detectable thalamic signature |
| `Hnf1a` | 0 | native mouse Hnf1a-Kdm6a CORUM complex | exact but likely tissue-specific complex, so a weak brain analog |
| `Ep300` | 0 | enhancer coactivator in the broader Reactome MLL3/4 axis | boundary against assuming every active-enhancer cofactor is broad in this assay |
| `Ogt` | 4 | WDR5-containing chromatin-complex module member | weak nonzero broad-complex support |
| `Crebbp` | 8 | chromatin coactivator with a curated STRING Kdm6a physical link | best low nonzero magnitude analog, though it is not a UTX/MLL3-4 core subunit |
| `Kdm5c` | 18 | histone demethylase in the Kdm/active-chromatin neighborhood | low nonzero chromatin benchmark, but it acts on H3K4 rather than H3K27 |
| `Kmt2a` | 24 | H3K4 methyltransferase complex member in the corpus neighborhood | low-to-moderate COMPASS-family counterpoint, not an MLL3/MLL4-specific subunit |
| `Setd1a` | 368 | WDR5/COMPASS writer with strong focal response | broad-response outlier; useful mainly as an upper bound, not a direct template |
| `Smarca4`, `Rxra`, `Pparg` | 0 each | broad Reactome MLL3/MLL4 or enhancer-regulation context | loose counterexamples that kept the estimate away from a broad chromatin average |

The zero/nonzero decision was not obvious. The direct H3K27 demethylase analog
`Kdm6b` and the exact MLL3 partner `Kmt2c` both landed at 0 DEGs, and those are
the cleanest within-dataset reasons to predict no detected Kdm6a effect. I
nevertheless put `Kdm6a` just above zero because UTX has complex-scaffold
roles in the KMT2C/KMT2D enhancer assemblies in addition to the demethylase
activity shared with Kdm6b, and because several nearby chromatin perturbations
(`Ogt`, `Crebbp`, `Kdm5c`, `Kmt2a`) were reproducibly nonzero but remained in
the 4-24 DEG range.

The final estimate is therefore 8 DEGs. This is deliberately near `Crebbp`
and below `Kdm5c`/`Kmt2a`, because the focal held-in data argue against
anything like the 368-DEG `Setd1a` footprint or the hundreds-DEG footprints of
generic strong chromatin regulators such as `Brd4` and `Smarcc2`.

## Limits

* Kdm6a itself had no target-scoped Finding or Claim in the selected Distributed Agents
  same-experiment corpus release, so the corpus could not provide a direct
  Kdm6a signature or same-report Kdm6a comparator.
* The strongest complex evidence for Kmt2c, MLL3, MLL4, and PTIP-HMT was
  human CORUM v5.0 projected to mouse through MGI one-to-one orthology. That is
  better than symbol guessing, but it is not a native thalamic neuron complex
  measurement.
* `Kdm6b` is a biochemical paralog rather than a KMT2C/KMT2D complex partner;
  `Kdm5c`, `Kmt2a`, `Ogt`, `Crebbp`, and `Setd1a` are pathway-level analogs
  with different marks or complexes.
* The runtime profile comparisons are over held-in perturbations only. Kdm6a
  has no measured held-out signature in the supplied parquet, so the predicted
  count is an extrapolation from analog counts and biology.
