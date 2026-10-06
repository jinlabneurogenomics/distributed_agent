# Reasoning trace

## Question and resolved ambiguities

I interpreted the task as a one-target held-out prediction for `Cox6b1`: estimate the number of measured genes that would have `pvals_adj < 0.05` in the `151 TH Prkcd Grin2c Glut` cell group after acute AAV CRISPR-Cas9 loss of `Cox6b1`.

The endpoint is the assay-specific DEG count, not an estimate of whether complex IV is essential in general. In particular, I treated a count of `1` as possible self-target RNA depletion and a count of `0` as possible even for an important mitochondrial gene if the perturbation was partial or transcriptionally buffered in this postmitotic neuronal assay.

## Sources used

- Held-out manifest: `[local file: 046_Cox6b1.csv]`; it contains exactly `Cox6b1`.
- Focal-cell training counts: `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`; 1,674 non-held-out perturbations, with `Cox6b1` absent.
- Differential-expression parquet: `[local file: training_de_all_cell_groups.parquet]`; I filtered it to `group_name = '151 TH Prkcd Grin2c Glut'`.
- Distributed Agents same-experiment corpus, release `perturbai-july-260713-sourceguard-1773-v1`. `corpus.target_context` and `corpus.story_count` had no precomputed `Cox6b1` claims or perturbation-centered findings, so the corpus did not supply a curated same-experiment Cox6b1 neighborhood.
- Distributed Agents runtime `profile_compare` / `profile_cohort`, run on the focal-cell signatures of complex-IV and OXPHOS analogs.
- External function evidence from MitoCarta3.0 and PubMed:
  - Rath et al. 2021, MitoCarta3.0, Nucleic Acids Research, DOI `10.1093/nar/gkaa1011`, PMID `33174596`.
  - Massa et al. 2008, COX6B1 mutation causing cytochrome c oxidase deficiency, American Journal of Human Genetics, DOI `10.1016/j.ajhg.2008.05.002`, PMID `18499082`.
  - Balsa et al. 2012, NDUFA4 as a complex-IV subunit, Cell Metabolism, DOI `10.1016/j.cmet.2012.07.015`, PMID `22902835`.
  - Signes et al. 2019, APOPT1/COA8 in COX assembly, EMBO Molecular Medicine, DOI `10.15252/emmm.201809582`, PMID `30552096`.
  - Ruzzenente et al. 2011, LRPPRC control of mitochondrial mRNA stability/polyadenylation and translation, EMBO Journal, DOI `10.1038/emboj.2011.392`, PMID `22045337`.

## Data processing

To avoid scanning the 616M-row all-cell-type parquet for every query, I materialized the focal group once with DuckDB:

```sql
COPY (
  SELECT names, scores, logfoldchanges, pvals, pvals_adj,
         group_name, gene_target, control_label,
         n_pert_matched, n_ctrl_matched
  FROM read_parquet('[local file: training_de_all_cell_groups.parquet]')
  WHERE group_name = '151 TH Prkcd Grin2c Glut'
) TO 'codex_runtime/151_TH_Prkcd_Grin2c_Glut_de.parquet'
  (FORMAT PARQUET, COMPRESSION ZSTD)
```

The focal slice has 28,891,566 rows: 1,674 training perturbations by 17,259 measured genes. The supplied training-count distribution for this cell group is strongly zero-weighted: 1,205 of 1,674 targets have 0 DEGs and 276 more have exactly 1 DEG.

I then inspected genes in and around the mitochondrial electron-transport chain, and in particular complex IV. The relevant training counts were:

| analog | focal `n_degs` | focal significant rows |
| --- | ---: | --- |
| `Cox4i1` | 0 | no FDR 0.05 genes; self `Cox4i1` q = 0.176 |
| `Cox5a` | 1 | only self `Cox5a`, log2FC -1.231, q = 5.39e-21 |
| `Cox6a1` | 0 | no FDR 0.05 genes; self `Cox6a1` was just above threshold, q = 0.0726 |
| `Cox7b` | 0 | no FDR 0.05 genes; self q = 1 |
| `Cox8a` | 0 | no FDR 0.05 genes; self q = 1 |
| `Cox11` | 0 | no FDR 0.05 genes; self q = 1 |
| `Coa8` | 0 | no FDR 0.05 genes; self q = 1 |
| `Ndufa4` | 1 | only self `Ndufa4`, log2FC -0.803, q = 1.08e-5 |
| `Lrpprc` | 0 | no FDR 0.05 genes; best row `Emc1` q = 0.174 |

I also compared the signed focal log-fold-change vectors of these nine analogs with Distributed Agents runtime profile tools using the top 400 positive and negative features. The cohort had no shared significant expression program: only `Cox5a` and `Ndufa4` had any FDR 0.05 features, and those were their own target RNAs. Pairwise signed cosines were moderately high, 0.665 to 0.746, but the leading high-absolute-logFC features were almost all q = 1 rare-gene spikes. I therefore treated the profile comparison as a warning against over-interpreting raw signature similarity and put more weight on the adjusted-p-value counts and the mechanistic complex-IV membership.

## Target-specific rationale

### `Cox6b1`

`Cox6b1` encodes a nuclear intermembrane-space-facing subunit of cytochrome c oxidase, respiratory-chain complex IV. MitoCarta3.0 assigns COX6B1 to the mitochondrial oxidative-phosphorylation/complex-IV pathway, and human recessive COX6B1 variants cause cytochrome c oxidase deficiency, so the relevant within-dataset comparison is not a generic mitochondrial group but complex-IV structural and assembly genes.

The closest assayed structural subunits were `Cox5a`, `Cox6a1`, `Cox7b`, `Cox8a`, and `Cox4i1`; `Ndufa4` was included because Balsa et al. reassigned it from complex I to complex IV. Their focal responses were 1, 0, 0, 0, 0, and 1 DEGs respectively. The two one-DEG cases were self-target-only signatures, not broader COX stress states. `Cox6a1` and `Cox4i1` showed subthreshold self knockdown without any FDR-significant downstream genes, and `Cox7b`/`Cox8a` were fully zero. Thus, even when the CRISPR perturbation hit a bona fide complex-IV subunit in the same neuronal population, the observed endpoint clustered at 0 or at self-only 1.

I used `Cox11` and `Coa8` as mechanistically adjacent counterexamples rather than as exact paralogs. `Cox11` participates in CuB-site biogenesis and `COA8/APOPT1` assists COX assembly, but both had 0 DEGs in this cell group. `Lrpprc` is upstream of mitochondrial transcript stability and can reduce mitochondrially encoded COX subunits, so it is a broader OXPHOS perturbation than `Cox6b1`; it also had 0 DEGs. Additional ETC training targets outside complex IV were likewise nearly all at 0 or 1 DEG: examples include `Ndufa10` 1, `Ndufa11` 0, `Ndufa12` 0, `Ndufaf2` 0, `Ndufs4` 0, `Uqcrb` 0, `Uqcrfs1` 0, `Uqcrc2` 1, and `Tomm40` 1.

The zero/nonzero decision is therefore driven mainly by the input dataset. External biology says loss of COX6B1 can be severe when complex IV assembly is genuinely impaired, but the acute, sparse, juvenile neuronal Perturb-seq assay did not show a broad FDR-significant transcriptional response to nearby complex-IV genes. The best integer prediction is 0 rather than 1 because five of six `Cox*` training analogs and seven of nine extended complex-IV/OXPHOS analogs had 0 focal DEGs; the rare nonzero analogs stopped at self RNA depletion only.

Predicted `n_degs`: **0**.

## Limits

This prediction extrapolates from other complex-IV subunits and assembly factors because `Cox6b1` itself was held out completely. The analogs are imperfect: COX6B1 is a structural subunit whose absence may destabilize assembled complex IV differently from `COA8` or `COX11`, and the hidden `Cox6b1` guide set could have produced stronger or weaker target-mRNA loss than the guide sets for `Cox5a`, `Cox6a1`, or `Ndufa4`. The available DE table also reports only rank-test statistics, not raw expression, editing indel rates, protein abundance, respiratory flux, or viability. For that reason the call is high-confidence for "no broad program" but lower-confidence on the exact distinction between 0 and a self-target-only 1.
