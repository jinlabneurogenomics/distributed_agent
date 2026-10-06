# DEG-count prediction trace

## Question and resolved ambiguities

I interpreted the task as a target-by-target point prediction of `n_degs` for
held-out perturbations in the focal `151 TH Prkcd Grin2c Glut` class, where
`n_degs` is the count of measured mouse genes whose Wilcoxon BH-adjusted
`pvals_adj` is below 0.05. The target itself is part of the measured gene list
when expressed, so a one-gene prediction can correspond to a self-transcript
or one very small downstream signature. `Ahdc1` was absent from both the
training DEG-count CSV and from `gene_target` in the parquet, so I treated all
Ahdc1 DEG evidence as held out and used only training targets plus external
mechanistic priors.

## Sources used

- Input endpoint table:
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
  This gave the exact focal-cell `n_degs` values for 1,674 training
  perturbations.
- Input differential-expression parquet:
  `[local file: training_de_all_cell_groups.parquet]`.
  I filtered it to `group_name == "151 TH Prkcd Grin2c Glut"` for selected
  chromatin, BAF, CHD, methyl-CpG, and transcriptional-regulator targets and
  recomputed `sum(pvals_adj < 0.05)` plus the significant up/down split and
  leading genes.
- Distributed Agents same-experiment corpus
  `perturbai-july-260713-sourceguard-1773-v1`. Its `target_context` query had
  no Ahdc1 report, but its reports and claims for training genes documented the
  same-experiment BAF module, Wac/Sin3a/Setd1a chromatin responses, and
  counterexamples in which same-family chromatin perturbations were flat.
- Distributed Agents runtime profile tools. I compared a declared cohort of active and
  inactive chromatin perturbations in the focal cell type to check that the
  focal signatures were present, broad, and directionally distinct rather than
  one interchangeable "chromatin" state.
- External PubMed literature:
  Xia et al. 2014, DOI 10.1016/j.ajhg.2014.04.006, PMID 24791903; Khayat et
  al. 2021, DOI 10.1016/j.xhgg.2021.100049, PMID 34950897; Collier et al.
  2022, DOI 10.1038/s41586-022-04727-9, PMID 35585237; Bochicchio et al.
  2025, DOI 10.1007/s00439-025-02765-7, PMID 40844525.

## Computational calibration

The requested manifest contained only `Ahdc1`. The training endpoint
distribution in the focal cell type was zero-inflated: 1,205 of 1,674 training
targets had `n_degs = 0`, 469 had a nonzero count, the median among nonzero
targets was 1, and the 75th percentile among nonzero targets was 7. The largest
training responses were rare and came from targets such as `Uba5` with 2677,
`Tpr` with 1768, and `Sin3a` with 1433 DEGs.

For mechanistic calibration I filtered the parquet to the focal cell group and
candidate training targets, then counted significant rows:

```python
sum((group_name == "151 TH Prkcd Grin2c Glut")
    & (gene_target == target)
    & (pvals_adj < 0.05))
```

This exactly reproduced the training CSV for the queried targets. The relevant
focal counts were:

| comparator | focal `n_degs` | focal expression-pattern evidence |
| --- | ---: | --- |
| `Sin3a` | 1433 | A very broad chromatin-corepressor response, 974 up and 459 down; strongest genes included `Odf2`, `Hcn3`, `Dzip1`, `Srrm2`, `Ache`. The corpus mapped this onto ER/proteostasis, splicing, lipid, lysosomal, and ciliary programs rather than a simple direct-repression signature. |
| `Wac` | 384 | 168 up and 216 down; decreased neuronal or synaptic markers such as `Lgi3`, `Eno2`, `Grid2ip`, `Ptpn3`, `Septin5`, `Gabrb2`, `Ache`, with an upward RNA-processing/chromatin arm including `Adarb1`. |
| `Setd1a` | 368 | Predominantly negative in 151, 69 up and 299 down, led by mitochondrial, GPI-anchor, ER/Golgi, ciliary, and autophagy/lysosomal genes such as `Foxred1`, `Nprl3`, `Pigq`, `Ufl1`. |
| `Brd4` | 311 | 61 up and 250 down; a neuronal maintenance/synaptic response with leading decreases including `Omg`, `Plch2`, `Rnf112`, `Irag1`, `Sparcl1`, and `Septin4`. |
| `Smarcc2` | 185 | The clearest focal BAF response, 71 up and 114 down, with `Ptpn3`, `Reep2`, `Tiam1`, `Prkcd`, `Ptprz1`, `Adarb1`, and `Begain` among the strongest down-regulated genes. The Distributed Agents corpus linked this to a subunit-selective BAF/mSWI/SNF module with `Arid1a` and `Smarce1`. |
| `Arid1a` | 22 | Same-direction but much smaller BAF response sharing `Ptpn3`, `Begain`, and synaptic/excitability genes with `Smarcc2`. |
| `Smarce1` | 11 | Small BAF-family response in the same focal group. |
| `Arid2` | 56 | Partial BAF/PBAF convergence with `Smarcc2`, not a full phenocopy. |
| `Arid1b` | 1 | Nearly flat; its only focal DEG was `Arid1b` itself. |
| `Smarca2` | 1 | Nearly flat despite being a remodeler ATPase. |
| `Smarca4`, `Smarcc1`, `Bicra` | 0 | Flat focal counterexamples inside the represented SWI/SNF/BAF neighborhood. |
| `Chd8`, `Chd2`, `Chd4`, `Chd7` | 61, 34, 100, 0 | CHD/NuRD remodelers showed diverse small-to-mid responses, not a generic remodeler burden. |
| `Mbd5`, `Dnmt3a`, `Gata3`, `Trp63`, `Kat6a`, `Kat6b`, `Ep300`, `Pogz`, `Tcf4`, `Dyrk1a` | 0 each | Disease or chromatin/transcription genes whose acute P16 loss was buffered in this focal cell group. |
| `Mecp2`, `Zbtb18`, `Auts2`, `Gatad2b` | 16, 5, 1, 1 | Small NDD transcriptional/chromatin responses that set a low-count alternative to the broad `Sin3a`/`Setd1a`/`Wac` state. |

## Target-specific reasoning: Ahdc1

`Ahdc1` encodes a large AT-hook DNA-binding protein. Human de novo truncating
variants were first tied to Xia-Gibbs syndrome by Xia et al. 2014, and Khayat
et al. 2021 extended the disease model to selected missense variants clustering
in conserved AHDC1 regions. That makes Ahdc1 a credible
neurodevelopmental-disease chromatin/transcription regulator, but not a member
of a known obligate complex represented in the training table.

The strongest direct mechanistic paper I found is Collier et al. 2022: AHDC1
protein, also called Gibbin, binds enhancers and promoters, interacts with many
sequence-specific zinc-finger transcription factors and methyl-CpG-binding
proteins, and regulates GATA3-dependent mesodermal gene expression and DNA
methylation during epithelial organoid development. That literature supports
the possibility of a transcriptional phenotype after Ahdc1 loss, but it is an
early human stem-cell and chimeric mouse developmental phenotype, not evidence
for a broad cell-autonomous response in P16-to-P37/44 postmitotic thalamic
neurons. The external mechanism therefore gave Ahdc1 a weak nonzero prior, not
a `Sin3a`- or `Smarcc2`-scale prior.

The nearest within-dataset analogs split into three groups:

- Core chromatin regulators such as `Sin3a`, `Setd1a`, `Wac`, and `Brd4`
  confirmed that `151 TH Prkcd Grin2c Glut` is capable of reporting large
  nuclear-regulatory perturbations, but their signatures involve specific
  complexes or pathways absent from AHDC1 biology: SIN3/HDAC scaffolding,
  COMPASS/H3K4 writing, WAC/RNF20-RNF40 H2Bub coupling, and BET/bromodomain
  enhancer maintenance. I treated their 311 to 1433 DEG counts as upper bounds,
  not as direct quantitative analogs.
- The BAF/mSWI/SNF examples supplied a more local chromatin-remodeler
  calibration. `Smarcc2` had 185 DEGs and its same-direction partners
  `Arid1a` and `Smarce1` had 22 and 11, but related subunits `Arid1b`,
  `Smarca2`, `Smarca4`, `Smarcc1`, and `Bicra` ranged from 0 to 1. The
  Distributed Agents claim for this module explicitly described the focal BAF response
  as subunit-selective rather than interchangeable. Because AHDC1 is not known
  as a BAF core subunit, the high `Smarcc2` count should not be transferred.
- Regulators closer to the external Gibbin biology were mostly flat or tiny in
  the focal readout: `Gata3` and `Trp63` were 0, `Dnmt3a` and `Mbd5` were 0,
  `Mecp2` was 16, `Zbtb18` was 5, `Auts2` was 1, and `Gatad2b` was 1. This is
  the most relevant numerical stratum for a weakly annotated, developmentally
  important chromatin-associated NDD gene in an acute postmitotic assay.

I therefore predict that Ahdc1 loss is more likely to be at the focal assay's
edge of detectability than to produce a broad multi-hundred-gene state. I made
the zero/nonzero decision as a minimal nonzero call: the AT-hook/chromatin and
Xia-Gibbs evidence make one FDR-supported row plausible, but the lack of a
direct same-complex training analog and the flat `Gata3`/`Trp63`/methyl-CpG
comparators argue against a larger burden.

Final point prediction: `Ahdc1 -> 1`.

## Limits

There is no same-experiment Ahdc1 report or Ahdc1 profile in the released
Distributed Agents corpus, and the DE parquet deliberately excludes the held-out
signature, so this is extrapolation from neighboring biology rather than
signature matching. AHDC1/Gibbin molecular work is still sparse and is strongest
in developmental skin/mesoderm systems; the postnatal neuronal substrate could
be much weaker, absent, or qualitatively different. Conversely, if acute Ahdc1
perturbation converges on an unannotated thalamic state, none of the BAF,
methyl-CpG, or broad chromatin counterexamples would reveal it. The one-DEG
prediction should be read as a low-confidence boundary estimate very near zero.
