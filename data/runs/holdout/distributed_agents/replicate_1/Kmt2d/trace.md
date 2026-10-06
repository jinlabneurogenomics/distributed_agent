# Kmt2d hold-out DEG-count prediction

## Question and endpoint

The requested prediction is the number of measured genes that would pass
Wilcoxon Benjamini-Hochberg FDR < 0.05 after acute mosaic CRISPR loss of
`Kmt2d` in `151 TH Prkcd Grin2c Glut` neurons. `151 TH Prkcd Grin2c Glut` was
treated as the exact Allen-style thalamic glutamatergic class in the supplied
dataset, and `n_degs` was treated as an assay- and power-dependent count of
significant relative-expression contrasts among recovered nuclei, not as a
direct count of cells lost, edited nuclei, or biological importance.

The held-out target list contained one gene:

| target_name | predicted_n_degs |
|---|---:|
| Kmt2d | 0 |

## Sources used

- Declared Perturb-seq input Parquet:
  `training differential-expression dataset`.
  I used it as the direct source for non-held-out expression signatures and
  exact `pvals_adj < 0.05` DEG counts in `151 TH Prkcd Grin2c Glut`.
- Declared focal-cell training endpoint:
  `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
  This supplied observed `n_degs` for 1,674 non-held-out biological
  perturbations.
- Declared held-out manifest:
  `single-target request for Kmt2d`.
  This supplied the one requested held-out target, `Kmt2d`.
- `perturbai-july-260713-sourceguard-1773-v1`, the run-local same-experiment
  Findings/Report corpus, used only for bounded interpretation of represented
  analog perturbations such as `Kmt2c`, `Kmt2a`, `Setd1a`, and `Crebbp`. This
  corpus is another representation of the same Perturb-seq experiment, not
  independent replication.
- PubMed-indexed external literature for target function:
  - Hu et al. 2013, DOI `10.1128/MCB.01181-13`, PMID `24081332`: mammalian
    MLL3/KMT2C and MLL4/KMT2D are the COMPASS-family enhancer H3K4
    monomethylases and can redundantly regulate enhancer H3K4me1.
  - Rickels et al. 2020, DOI `10.1101/gad.339762.120`, PMID `33033055`:
    Trr/MLL3/MLL4 proteins share a conserved UTX-stabilization function,
    supporting a mechanistic relation between KMT2C- and KMT2D-COMPASS.
  - Ng et al. 2010, DOI `10.1038/ng.646`, PMID `20711175`: truncating MLL2,
    now KMT2D, variants are a major genetic cause of Kabuki syndrome.
  - Bjornsson et al. 2014, DOI `10.1126/scitranslmed.3009278`, PMID
    `25273096`: a mouse Kmt2d haploinsufficiency model has hippocampal
    neurogenesis and memory phenotypes that can be modified by postnatal
    chromatin treatment.

## Quantitative calibration

I first materialized the declared cached Perturb-seq feature table with
`dataset.perturbseq_features summarize`; it scanned the 616,253,184-row
training Parquet and wrote 1,674 biological target summaries. I then joined
that feature table to the focal training-count CSV. The endpoint distribution
was very sparse and long-tailed:

- 1,674 training perturbations in the focal cell group
- median `n_degs`: 0
- 75th percentile: 1
- 90th percentile: 2
- 95th percentile: 18
- mean: 14.1, inflated by a small number of very broad responses
- maximum: 2,677

The materialized feature summary was useful as a quality check but not as a
predictor for `Kmt2d` because it contained no held-out-target row. Therefore I
used exact, biologically selected represented analogs and rescanned the raw
Parquet for those analogs in `151 TH Prkcd Grin2c Glut`. For each comparator I
counted rows with `pvals_adj < 0.05`; I also retained the matched perturbed
nucleus count and the top significant genes as expression-pattern evidence.

| training perturbation | `151 TH` n_DEGs | matched perturbed nuclei | expression evidence and interpretation |
|---|---:|---:|---|
| `Kmt2c` | 0 | 55 | Closest represented MLL3/MLL4 paralog and same enhancer-COMPASS branch as `Kmt2d`; no focal-cell gene passed FDR 0.05 and its focal Wilcoxon-score correlations with `Kmt2a`, `Setd1a`, and `Crebbp` were 0.021, 0.005, and -0.002. The same-experiment corpus also summarized acute `Kmt2c` as broadly buffered, with only one FDR 0.10 downstream gene across 16 measured groups. |
| `Kmt2a` | 24 | 161 | A SET1/MLL H3K4 writer, but a different COMPASS branch from MLL3/MLL4; the 24-gene focal signature centered on down-regulated neuronal identity/connectivity genes such as `Nr2f1`, `Pcdh7`, `Lhx9`, `Pcdh10`, `Grik2`, and `Camk2d`, with no evidence that this was an MLL3/MLL4 enhancer phenotype. |
| `Setd1a` | 368 | 154 | Another H3K4 methyltransferase and the clearest chromatin positive control in the family, but the corpus and the raw signature placed it in a broad mitochondrial, GPI-anchor, ER/Golgi, ciliary, lysosomal, and RNA-processing state. It is a counterexample to technical failure of H3K4-writer perturbations, not a close donor for `Kmt2d`. |
| `Crebbp` | 8 | 61 | A p300/CBP enhancer coactivator produced only a small thalamic response with `Stxbp2`, `Rtn4rl1`, `Cfap298`, `Leng8`, `Stmn4`, `Rbfox2`, `Ccdc141`, and `Dgkz` significant. This shows that a small low-cell-count chromatin signature was detectable, but it was target-specific. |
| `Ep300` | 0 | 155 | The KAT3 paralog of `Crebbp` and a cooperating enhancer acetyltransferase had no focal-cell DEGs. |
| `Ncoa1`, `Ncoa3` | 0, 0 | 189, 147 | Nuclear-receptor coactivators, more distant from KMT2D than NCOA6 but relevant to enhancer coactivation, were flat in the focal endpoint. |
| `Kat6a`, `Kat6b`, `Kdm6b` | 0, 0, 0 | 170, 150, 203 | Additional chromatin modifiers, including a KDM6-family demethylase related to KDM6A/UTX, were flat at FDR 0.05. They argue against a broad default chromatin-modifier response. |
| `Sin3a`, `Smarcc2`, `Chd4`, `Chd8` | 1,433; 185; 100; 61 | 176; 162; 163; 197 | Large chromatin-repressor/remodeler responses proved the thalamic assay had power to detect broad chromatin-induced expression changes, but these complexes have different direct molecular consequences from enhancer H3K4me1 writing and are inappropriate quantitative analogs for MLL4. |

## Kmt2d-specific causal transfer

`Kmt2d` encodes MLL4, the paralog of MLL3/`Kmt2c`; both occupy the MLL3/MLL4
branch of COMPASS-like complexes and are linked to enhancer H3K4me1 rather
than to the promoter H3K4me3 branch sampled by SETD1/KMT2A. Hu et al. showed
that MLL3 and MLL4 are major enhancer H3K4me1 regulators and can be redundant
in mouse embryonic fibroblasts, and Rickels et al. further supported an
MLL3/MLL4-shared noncatalytic route through UTX stabilization. The best
same-experiment intervention to transfer from is therefore `Kmt2c`, not
`Setd1a`.

Following the experiment's causal chain:

- Intervention: acute sparse P16 Cas9 loss of `Kmt2d`, not germline deletion
  or a chronic developmental model.
- Direct consequence: partial impairment of MLL4-containing enhancer COMPASS.
  This should reduce some enhancer activity and may destabilize the UTX module
  when alleles are fully disrupted, but the screen's average per-guide RNA
  down-regulation is modest and target RNA loss itself is not an editing
  strength measure.
- Propagation: the closest measured propagation test, `Kmt2c`, was essentially
  silent in mature recovered neurons; `Ep300`, `Kat6a`, `Kat6b`, `Kdm6b`,
  `Ncoa1`, and `Ncoa3` were also focal nulls. Only the different H3K4 writer
  branches or other chromatin complexes produced multi-gene responses.
- Exposure and selection: the readout samples NeuN-positive recovered neuronal
  nuclei 3-4 weeks after P16 perturbation. It can miss early developmental
  requirements or cells lost before recovery.
- Measured endpoint: FDR-significant relative-expression changes in recovered
  `151 TH` neurons.

External evidence raises the prior that KMT2D is biologically important:
truncating KMT2D variants cause Kabuki syndrome, and Kmt2d haploinsufficient
mice have postnatal dentate-gyrus neurogenesis and memory defects. However,
those are developmental, germline/haploinsufficient, or hippocampal
progenitor/granule-cell contexts. They do not override the represented MLL3
paralog's near-null response in a sparse postmitotic thalamic snRNA-seq assay.
They mainly keep the zero prediction uncertain: a small `Kmt2d` response like
`Crebbp` or `Kmt2a` is plausible, but a Setd1a/Sin3a-scale broad response is
not mechanistically supported.

I therefore predicted `Kmt2d` as a focal-cell nonresponder, with a point
estimate of zero genes passing FDR 0.05.

## Limits

The key extrapolation is from represented analogs to a fully held-out
perturbation; there is no `Kmt2d` expression signature or target-specific DEG
count in the supplied inputs. `Kmt2c` is the closest measured paralog but had
only 55 focal matched perturbed nuclei, so a weak MLL3/MLL4 enhancer response
could have fallen below FDR correction. `Kdm6a`, `Ncoa6`, `Paxip1`, `Pagr1`,
and core WRAD complex subunits were not represented in the training table, so
the MLL3/MLL4 complex could not be triangulated as directly as `Setd1a` or
`Kmt2a`. The external KMT2D/Kabuki literature demonstrates biological
importance in neural development and hippocampal neurogenesis, but it is not
the same intervention, cell class, or survivor-conditioned basal snRNA-seq
endpoint used here.
