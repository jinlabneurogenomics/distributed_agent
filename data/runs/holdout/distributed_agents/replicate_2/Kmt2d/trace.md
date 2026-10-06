# Reasoning trace

## Question and resolved ambiguities

The requested held-out target file contains one perturbation, `Kmt2d`. I interpreted the endpoint as:

- cell group: `151 TH Prkcd Grin2c Glut`;
- statistic: the number of measured genes in the raw differential-expression parquet for the `Kmt2d` perturbation with `pvals_adj < 0.05`;
- perturbation direction: CRISPR-Cas9 loss of function by P16 AAV delivery, measured 3-4 weeks later in recovered NeuN+ mouse nuclei;
- point prediction: one non-negative integer, with `0` meaning that no genes cross the requested BH-adjusted Wilcoxon cutoff.

The held-out target was absent from the focal training-count CSV, absent as a `gene_target` in the training parquet, and absent from the selected Distributed Agents corpus release, as intended by the task. I therefore treated the observed signatures and DEG counts of non-held-out chromatin perturbations as direct calibration data, and used outside biology only to decide which training perturbations were mechanistically meaningful.

## Sources

- Raw training counts: `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`
- Raw DE parquet: `[local file: training_de_all_cell_groups.parquet]`
- Requested targets: `[local file: 122_Kmt2d.csv]`
- Distributed Agents same-experiment semantic corpus: `perturbai-july-260713-sourceguard-1773-v1`
- PubMed-indexed external literature:
  - Ng et al., 2010, Nature Genetics, DOI `10.1038/ng.646`, PMID `20711175`
  - Hu et al., 2013, Molecular and Cellular Biology, DOI `10.1128/MCB.01181-13`, PMID `24081332`
  - Cheng et al., 2014, Molecular Cell, DOI `10.1016/j.molcel.2014.02.032`, PMID `24656132`
  - Bjornsson et al., 2014, Science Translational Medicine, DOI `10.1126/scitranslmed.3009278`, PMID `25273096`
  - Rickels et al., 2017, Nature Genetics, DOI `10.1038/ng.3965`, PMID `28967912`
  - Froimchuk, Jang and Ge, 2017, Gene, DOI `10.1016/j.gene.2017.06.056`, PMID `28669924`

## Training data calibration

The focal training count table has 1,674 non-held-out biological perturbations. Its empirical distribution is very sparse: 1,205/1,674 targets have `n_degs = 0`, the median is 0, the 75th percentile is 1, the 90th percentile is 2, and the 95th percentile is 18. Thus the first decision for `Kmt2d` is whether its acute postmitotic loss should be a visible transcriptional perturbation at all; the prior over arbitrary genes is strongly zero-inflated.

I then filtered the parquet to `group_name == "151 TH Prkcd Grin2c Glut"` and to represented KMT2/H3K4 or enhancer/chromatin comparators. I recomputed the requested endpoint by counting `pvals_adj < 0.05`, matching the supplied training-count CSV. The key same-cell counts were:

| training perturbation | relationship to Kmt2d | observed `n_degs` in 151 TH | focal evidence |
| --- | --- | ---: | --- |
| `Kmt2c` | closest represented MLL3/4 paralog; same COMPASS-like enhancer branch | 0 | 55 perturbed vs 23,679 controls; no FDR 0.05 genes; all adjusted p-values were 1.0 in the focal group |
| `Kmt2a` | H3K4 writer in a different SET1/MLL branch | 24 | mixed but small thalamic signature; strongest down genes included `Nr2f1`, `Pcdh7`, `Lhx9`, `Kmt2a`, `Camk2d` |
| `Setd1a` | H3K4 writer in the SETD1 promoter H3K4me3 branch | 368 | much broader down program including mitochondrial, GPI-anchor, ER/Golgi, cilium, and autophagy transcripts |
| `Kdm6b` | H3K27 demethylase related to UTX/KDM6A biology but not the MLL3/4 complex subunit itself | 0 | no focal FDR hits; adjusted p-values all 1.0 |
| `Ep300` | enhancer acetyltransferase recruited at activated enhancers downstream of KMT2D/KMT2C | 0 | no focal FDR hits; adjusted p-values all 1.0 |
| `Crebbp` | p300 paralog and enhancer coactivator | 8 | weak focal response, led by `Stxbp2`, `Rtn4rl1`, `Dgkz`, `Rbfox2`, `Ccdc141` |
| `Ogt` | O-GlcNAc transferase and indirect chromatin cofactor, reported by the corpus as a weak Setd1a neighbor | 4 | one clear self row plus `Snhg11`, `Gin1`, `Noct` |
| `Nsd1` | developmental histone methyltransferase outside the H3K4 branch | 23 | small focal response with several very large positive marker-like effects |
| `Kat6a`, `Kat6b` | MYST acetyltransferase chromatin-disorder comparators | 0, 0 | no focal FDR hits |

These computations argue for a small effect rather than a broad one. Kmt2c is the closest measured family member and was fully null in this exact endpoint. Several single enhancer/HAT perturbations that might have converged with Kmt2d were also null or weak (`Ep300 = 0`, `Crebbp = 8`, `Kat6a/Kat6b = 0`). At the same time, the focal cell group clearly can report acute chromatin perturbations: `Kmt2a`, `Setd1a`, `Smarcc2`, `Brd4`, and `Sin3a` had 24, 368, 185, 311, and 1,433 DEGs, so a zero cannot be blamed on global thalamic insensitivity.

## Same-experiment corpus evidence

The Distributed Agents corpus did not contain `Kmt2d`, confirming that the target itself was held out from the pre-interpreted layer. I used corpus reports for the measured analogs.

The `Kmt2c` report was the most relevant. It found that acute P16 Kmt2c loss was almost completely buffered across the mature-neuron transcriptome: 15 of 16 measured groups had zero downstream genes at FDR 0.10, and the only nonzero group had a single cortical `Prnp` hit. The report explicitly contrasted Kmt2c with `Setd1a`, `Chd8`, `Kmt2a`, `Kdm5c`, `Crebbp`, `Ehmt1`, `Ep300`, `Kdm6b`, `Kat6a`, `Kat6b`, `Arid1b`, and `Setd2`, concluding that available H3K4/enhancer and chromatin-neurodevelopmental relatives did not phenocopy Kmt2c in matched neurons. That is strong within-dataset negative evidence for the naive rule "all KMT2 or enhancer factors are broad in 151 TH neurons".

The `Kmt2a` and `Setd1a` reports supplied the positive counterexamples. Kmt2a had a sharply restricted response with most of its genome-wide FDR 0.10 calls in 151 TH neurons, whereas Setd1a was broad and largely non-overlapping, mapping toward organelle-maintenance and RNA-biogenesis states rather than to other KMT2-family writers. This means Kmt2d should not be copied from Setd1a solely because both write H3K4 methyl marks.

The `Ep300`, `Crebbp`, and `Kdm6b` corpus cards further constrained the enhancer prior. Ep300 was FDR-null in all 21 recovered groups; Crebbp had only a small 151-specific signature; Kdm6b was FDR-null everywhere while other chromatin regulators responded in the same thalamic group. These same-experiment findings make isolated perturbation of one enhancer cofactor compatible with buffering over the P16 to P37/44 window.

## External biological rationale for Kmt2d

KMT2D, historically MLL4 in mouse literature and MLL2 in older human literature, is not an arbitrary chromatin gene. KMT2D and KMT2C define the mammalian MLL3/MLL4 COMPASS-like branch and are major regulators of enhancer H3K4 monomethylation. Hu et al. showed preferential MLL4 binding at enhancers and major MLL3/MLL4 control of H3K4me1, with redundancy in mouse embryonic fibroblasts. Froimchuk, Jang and Ge reviewed KMT2D as a large H3K4 methyltransferase that complexes with WRAD components, NCOA6, PTIP/PA1, and UTX/KDM6A, supports enhancer activation, and promotes CBP/p300 recruitment. Cheng et al. also showed that MLL3/4-associated H3K4me1 biology can mark promoters as well as enhancers. Rickels et al. cautioned that the methyltransferase activity itself is not equivalent to the whole protein: catalytic SET-domain loss can leave surprisingly mild transcriptional effects in some systems.

The disease prior points to a real neural requirement. Ng et al. identified loss-of-function `KMT2D` mutations as a major cause of Kabuki syndrome, and Bjornsson et al. showed that a heterozygous `Kmt2d` mouse model has reduced H3K4me3 in dentate granule cells, impaired postnatal neurogenesis, and hippocampal memory defects that can be rescued by histone deacetylase inhibition. However, those effects are concentrated in developmental/progenitor or hippocampal neurogenesis settings. They do not require a broad steady-state mRNA collapse in already specified thalamic glutamatergic neurons after sparse P16 editing.

## Kmt2d prediction

I predicted `Kmt2d` to be visible but weak in 151 TH neurons, with 8 DEGs.

The zero/nonzero call is a compromise between two signals. The closest measured paralog, `Kmt2c`, is exact-zero in the focal endpoint and almost null across the Distributed Agents same-experiment corpus, and several enhancer coactivator comparators are also weak or null. That pushed the prediction away from the `Setd1a`, `Brd4`, `Smarcc2`, and `Sin3a` range. Against a strict zero, KMT2D is generally the more disease- and enhancer-central MLL3/4 paralog, and the published Kabuki syndrome mouse work makes complete postnatal neuronal buffering less likely for `Kmt2d` than for `Kmt2c`. Among training analogs, the weakest focal chromatin effects provide the best numerical scale: `Crebbp = 8`, `Ogt = 4`, `Ehmt1 = 4`, `Setd5 = 9`, with `Kmt2a` and `Nsd1` at 24 and 23 as upper guardrails. I therefore placed Kmt2d at the upper end of the weak class but below the 10-gene threshold for a medium response.

## Limits

The core uncertainty is that the exact same KMT2D complex was not represented: `Kdm6a`, `Paxip1`, `Pagr1`, `Ncoa6`, `Wdr5`, `Rbbp5`, `Ash2l`, and `Dpy30` were absent from the focal training-count CSV. `Kdm6b` is only a paralog-level and H3K27-axis comparator, not UTX. `Ep300` and `Crebbp` act downstream or in parallel at enhancers and are not KMT2D scaffold perturbations.

The `Kmt2c` analogy is biologically strong by branch membership but imperfect because KMT2D and KMT2C are not interchangeable in development or disease. The `Kmt2a` and `Setd1a` comparisons demonstrate that H3K4 writers can score in this assay, but they use different complexes and promoter/enhancer biases. Finally, external Kmt2d evidence comes largely from constitutive haploinsufficiency, embryonic cell states, or dentate neurogenesis, all displaced from this acute sparse postmitotic thalamic assay. The value 8 is therefore an extrapolated small-effect prediction, not a direct transfer from an observed same-complex signature.
