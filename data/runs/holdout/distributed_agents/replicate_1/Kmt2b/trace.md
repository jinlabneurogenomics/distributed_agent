# DEG-count prediction trace

## Question and endpoint

The task asks for a point prediction of `n_degs` for the held-out `Kmt2b`
perturbation in `151 TH Prkcd Grin2c Glut` cells. I interpreted `n_degs` in the
same way as the supplied training CSV: the count of measured genes with
`pvals_adj < 0.05` after BH correction for the Wilcoxon differential-expression
contrast of perturbed versus matched control nuclei in this one thalamic
glutamatergic cell group.

`Kmt2b` is absent from both declared training inputs. A direct DuckDB count over
`training_de_all_cell_groups.parquet` returned zero rows for
`gene_target = 'Kmt2b'`, and the requested-target CSV has one unique row,
`Kmt2b`, with no overlap to the 1,674 rows in
`151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`. The prediction is therefore
an extrapolation from non-held-out perturbations, not a readout of a KMT2B
signature.

## Sources used

- Declared endpoint table:
  `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
- Declared DE table:
  `training differential-expression dataset`.
- Internal same-experiment interpretation corpus:
  PerturbAI July `260713_sourceguard_1773_v1` Findings/Evidence/Reference
  ledgers. I used the `corpus.findings` and `corpus.report_evidence`
  capabilities for visible comparators, especially `Kmt2a`, `Kmt2c`,
  `Setd1a`, and `Crebbp`. These records are a curated interpretation of the
  same Perturb-seq experiment, not independent replication.
- External biological priors:
  - EpiFactors, COMPASS-like MLL1/2 complex entry, listing KMT2A/MLL1 and
    KMT2B/MLL2 with MEN1, HCFC1, ASH2L, DPY30, RBBP5, WDR5, and KAT8.
  - Lee et al. 2021, Nature Communications, DOI `10.1038/s41467-021-23268-9`,
    showing biochemical modulation of MLL/SET1 H3K4 methyltransferase activity
    on chromatin by WRAD subunits.
  - Klonou et al. 2021, Life, DOI `10.3390/life11080823`, reviewing KMT2B/MLL2
    structure, WRAD/Menin complex membership, H3K4 methylation, development,
    and disease links.
  - Meyer et al. 2016, Nature Genetics, DOI `10.1038/ng.3740`, reporting
    heterozygous pathogenic KMT2B variants in complex childhood-onset dystonia.
  - Kerimoglu et al. 2017, Cell Reports, DOI `10.1016/j.celrep.2017.06.072`,
    comparing hippocampal Kmt2a and Kmt2b knockdown and finding both memory
    functions and largely distinct H3K4/gene-expression loci.
  - Jakovcevski et al. 2015, Journal of Neuroscience, DOI
    `10.1523/JNEUROSCI.3004-14.2015`, showing a focused postmitotic-neuron
    requirement for Kmt2a/Mll1 and milder prefrontal behavioral effects after
    Mll2/Kmt2b ablation.
  - Kubo et al. 2024, Molecular Cell, DOI `10.1016/j.molcel.2024.02.030`,
    implicating acute KMT2B depletion in H3K4me1 at enhancers during mouse ES
    cell neural differentiation.

## Dataset computations

I queried the Parquet only for the focal `151 TH Prkcd Grin2c Glut` cell group
and biologically relevant visible comparator perturbations. The main operation
was:

```sql
SELECT gene_target, names, logfoldchanges, pvals_adj, scores
FROM read_parquet($parquet)
WHERE group_name = '151 TH Prkcd Grin2c Glut'
  AND gene_target IN (...KMT2/SET/chromatin comparator genes...)
```

I used `pvals_adj < 0.05` in those rows to confirm the training endpoint and to
inspect the leading genes in each comparator signature. I also correlated
Wilcoxon `scores` between `Kmt2a` and other focal comparator signatures to make
sure the chosen analog was not merely a high-count chromatin regulator with a
different expression pattern.

The visible endpoint distribution was zero-inflated and skewed: 1,205 of 1,674
training perturbations had `n_degs = 0`, 469 were nonzero, the median was 0,
the 75th percentile was 1, the 95th percentile was 18, and the maximum was
2,677. Thus a prediction near 20 is already in the upper tail of the focal
training distribution.

The focal-cell counts for relevant analogs and counterexamples were:

| training perturbation | observed `n_degs` in 151 | expression-pattern evidence |
| --- | ---: | --- |
| `Kmt2a` | 24 | Closest biochemical paralog present in training. The 24 FDR<0.05 genes split into a down-regulated neuronal identity/connectivity arm, including `Nr2f1`, `Pcdh7`, `Lhx9`, `Pcdh10`, `Grik2`, `Camk2d`, `Map1b`, `Sox2`, and `Elavl2`, and an up-regulated secondary arm, including `Igfbp5`, `Tnr`, `Cx3cl1`, `Atxn2l`, `Luc7l`, `Txndc5`, `Gabrd`, `Acsl3`, `Cry2`, and `Car4`. At FDR<0.10, 25 of the 30 total KMT2A downstream genes reported by the corpus were in this same thalamic cell group. |
| `Kmt2c` | 0 | Same broad SET1/MLL H3K4 family but not the MLL1/2 subcomplex. Its strongest focal rows all had `pvals_adj = 1`, and the corpus reported only a one-gene cortical responder across its measured surface. This is a counterexample against family-name transfer. |
| `Setd1a` | 368 | A much broader SET1-family H3K4 writer response with mitochondrial, ER/Golgi, GPI-anchor, cilium, lysosome, and RNA-processing down-modules. It shared only one of the 30 KMT2A FDR<0.10 loci in the same direction, so it is not the right count scale for KMT2B even though both are H3K4 writers. |
| `Ash1l` | 1 | Another H3K4-linked methyltransferase, but the sole FDR<0.05 focal hit was `Ash1l` itself. The corpus found only tiny neighbors and no validated KMT2A-like convergence. |
| `Crebbp` | 8 | A thalamic chromatin coactivator response on a small channel/neuronal-state module, not a KMT2/COMPASS response; its paralog `Ep300` was flat. This reinforced that paralogous chromatin factors can diverge strongly in this assay. |
| `Nsd1` / `Setdb1` / `Setd5` / `Ehmt1` / `Ep300` | 23 / 22 / 9 / 4 / 0 | Chromatin controls that showed the same cell group can detect modest epigenetic responses, but none shared FDR<0.05 genes with the 24-gene KMT2A set except for essentially no exact overlap. |

Across `Kmt2a` and the visible chromatin comparators above, focal Wilcoxon-score
correlations were weak: `Kmt2a` versus `Kmt2c` was `r = 0.021`, versus
`Setd1a` was `r = -0.038`, and versus `Crebbp` was `r = -0.021`. That supports
using gene-function transfer rather than a generic expression-neighbor score.

## Target-specific reasoning

### Kmt2b

**Intervention to direct consequence.** `Kmt2b` encodes MLL2/KMT2B, a large
SET-domain H3K4 methyltransferase. External biochemical summaries and EpiFactors
place KMT2B in the COMPASS-like MLL1/2 complex with the WRAD module
(`WDR5`, `RBBP5`, `ASH2L`, `DPY30`) and MENIN/HCFC subunits. The closest visible
Perturb-seq analog is therefore `Kmt2a`, not `Kmt2c`: the internal KMT2A
evidence explicitly notes that `Kmt2b`, `Kmt2d`, `Wdr5`, `Rbbp5`, `Ash2l`,
`Dpy30`, and `Men1` were absent from the training Parquet, leaving `Kmt2a` as
the only measured MLL1/2-complex catalytic paralog.

**Propagation through the chromatin program.** Acute `Kmt2a` loss in the focal
thalamic neurons gave a real but sparse transcriptional footprint: 24 FDR<0.05
genes, dominated by decreased neuronal identity/connectivity genes and a
matched smaller compensatory up-module. That is compatible with KMT2A/KMT2B
biology: MLL1/2 complexes activate selected promoters and nearby regulatory
regions through H3K4 methylation, so a partial loss after P16 mosaic editing is
expected to depress selected neuronal RNAs rather than globally collapse the
transcriptome.

**Exposure, selection, and sampling.** The measured `Kmt2a` analog had 161
matched perturbed nuclei in the focal cell group and the same 23,679 matched
control nuclei as the other focal contrasts, so its 24-gene count is within a
sample-size regime where a moderate response can pass FDR. `Kmt2c`, sampled
with 55 focal perturbed nuclei, was flat, but its failure is a mechanistic
counterexample rather than a reason to set all KMT2-family genes to zero,
because `Setd1a` had 154 focal perturbed nuclei and 368 DEGs and `Kmt2a` had a
well-resolved `Nr2f1`/`Pcdh7`/`Lhx9` signature.

**Measured endpoint prediction.** I predict a nonzero but modest count. The
zero option is disfavored because KMT2B is the same MLL1/2 writer subfamily as
`Kmt2a`, pathogenic human loss of KMT2B causes a movement disorder implicating
brain motor circuits, and acute KMT2B depletion can participate in neural
enhancer H3K4 methylation. A Setd1a-like count in the hundreds is also
disfavored: same-experiment KMT2A evidence showed that represented H3K4 writers
did not phenocopy each other, and Kerimoglu et al. found Kmt2a and Kmt2b act at
largely distinct hippocampal genomic regions. Jakovcevski et al. also reported
that prefrontal Kmt2b/Mll2 ablation produced milder behavioral effects than
Kmt2a/Mll1 ablation, supporting a slight downweight from the 24-DEG KMT2A
anchor rather than an upward adjustment.

I therefore used `Kmt2a = 24` as the quantitative anchor, treated `Kmt2c = 0`
and `Setd1a = 368` as boundary counterexamples, and adjusted downward for
KMT2B-specific locus selection and weaker mature-neuron PFC effects. The final
point prediction is **18 DEGs**.

## Limits

- There is no direct KMT2B Perturb-seq signature in either supplied input; the
  result is endpoint-bearing transfer from KMT2A/MLL1 complex biology.
- The full WRAD/Menin MLL1/2 complex was not represented in the visible
  training targets, so no core-subunit perturbation could test whether the
  focal KMT2A state is obligately reproduced by loss of the whole complex.
- `Kmt2c` and `Setd1a` show that H3K4 writers can be either flat or very broad
  in exactly this assay. Their divergence is useful as a warning, but it makes
  the precise KMT2B count uncertain.
- External studies used human genetics, ES-cell neural differentiation,
  hippocampal/PFC mouse systems, or non-mosaic genetic manipulations rather
  than sparse P16 AAV CRISPR in thalamic glutamatergic nuclei. They establish
  the expected direction of transfer from `Kmt2a` more than the exact number of
  BH-significant genes.
- `n_degs` is assay- and power-dependent. The prediction is a point estimate of
  FDR-crossing breadth, not a claim that KMT2B is only moderately important in
  all neuronal contexts.
