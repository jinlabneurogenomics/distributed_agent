# Prediction trace

## Question and ambiguity resolution

The requested held-out target list contains one perturbation, `Pgk1`, for the focal
cell group `151 TH Prkcd Grin2c Glut`. The endpoint is the exact training endpoint:
the number of measured genes with Wilcoxon Benjamini-Hochberg `pvals_adj < 0.05`
in perturbed nuclei versus matched controls.

I counted the perturbed target transcript itself as eligible for the endpoint. This
is important here: in the focal count table, most glycolysis-related one-gene calls
are not downstream programs but significant depletion of the target gene RNA itself.

## Sources used

- Held-out manifest: `176_Pgk1.csv`, which contains only `Pgk1`.
- Focal-cell training endpoint: `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
- Same-experiment differential-expression Parquet:
  `training_de_all_cell_groups.parquet`. I used it only after filtering to
  `group_name == "151 TH Prkcd Grin2c Glut"` and selected analog targets or
  selected measured genes.
- Distributed Agents gene-annotation store over the PerturbAI closed gene universe, using
  KEGG, Reactome, MSigDB/WikiPathways, GO, and STRING-backed annotations to
  nominate pathway neighbors rather than relying on gene-name similarity.
- Distributed Agents gene-analog nomination, run with `Pgk1` and the actual 1,674-gene
  focal training universe. This prioritized central-carbon candidates including
  `Tpi1`, `Pfkm`, `Hk1`, `Mdh1`, `Mdh2`, `Got1`, `Eno1`, and `Slc2a1`.
- Distributed Agents same-experiment corpus release
  `perturbai-july-260713-sourceguard-1773-v1`, queried for non-held-out
  glycolysis targets. `Pgk1` was not found in that corpus, so I used it only for
  comparator interpretation.
- External pathway/function references: KEGG Glycolysis/Gluconeogenesis
  `mmu00010` (Kanehisa and Goto 2000, PMID:10592173,
  DOI:10.1093/nar/28.1.27), Reactome mouse Glycolysis `R-MMU-70171.1`
  (Reactome ContentService; Gillespie et al. 2022, PMID:34788843,
  DOI:10.1093/nar/gkab1028), and PGK1 deficiency literature showing that
  damaging PGK1 mutations impair a glycolytic enzyme with hematologic,
  myopathic, and neurologic phenotypes in humans (Chiarelli et al. 2012,
  PMID:22348148, DOI:10.1371/journal.pone.0032065; Fermo et al. 2012,
  PMID:22705348, DOI:10.1016/j.ymgme.2012.05.015).

## Computations over the supplied data

1. I read the training count CSV and confirmed the focal distribution is
   zero-heavy: 1,205 of 1,674 training perturbations have `0` DEGs, the median is
   `0`, and the 75th percentile is `1`.
2. I queried the annotation store for `Pgk1`. It belongs to KEGG `mmu00010`,
   Reactome glycolysis/glucose-metabolism sets `R-MMU-70171` and `R-MMU-70326`,
   Reactome gluconeogenesis `R-MMU-70263`, and WikiPathways glycolysis and
   gluconeogenesis `MM15928`. Within the available training targets, these sets
   nominate `Tpi1`, `Pfkm`, `Hk1`, `Eno1`, `Gpi1`, `Dlat`, `Pdha1`, `Mdh1`,
   `Mdh2`, `Got1`, `Got2`, and `Slc2a1` as useful observed comparators, with
   `Tpi1`, `Pfkm`, and `Hk1` the most specific linear-glycolysis examples.
3. I filtered the Parquet to the focal group and the analog targets, then
   selected only rows with `pvals_adj < 0.05`. This directly distinguishes
   self-RNA calls from propagated downstream responses.
4. I also used the runtime profile comparison tool on the same focal group for a
   glycolysis-centered cohort. Because the largest absolute log-fold changes in
   the mostly null profiles were non-significant pseudocount extremes, I used
   this only as a bounded inspection layer; the FDR-significant rows and the
   training count CSV were the quantitative evidence for the endpoint.

## Target-specific reasoning

### Pgk1

`Pgk1` encodes phosphoglycerate kinase, the glycolytic ATP-generating enzyme that
converts 1,3-bisphosphoglycerate to 3-phosphoglycerate. KEGG `mmu00010` and
Reactome `R-MMU-70171` place it in the core cytosolic glycolysis pathway between
the `Gapdh` and `Pgam` steps. There was no same-reaction paralog in the focal
training universe, so the closest dataset analogs were single perturbations of
other represented glycolytic nodes.

Focal observations from the exact DEG-count endpoint:

| analog | relation to `Pgk1` | focal `n_degs` | FDR-significant focal expression evidence |
|---|---:|---:|---|
| `Tpi1` | specific Reactome gluconeogenesis and WikiPathways glycolysis neighbor | 1 | only `Tpi1` itself, log2FC -1.010, q = 6.23e-12 |
| `Pfkm` | specific Reactome glycolysis neighbor, PFK1 step | 1 | only `Pfkm` itself, log2FC -0.857, q = 6.42e-14 |
| `Hk1` | KEGG glycolysis, glucose phosphorylation entry step | 1 | only `Hk1` itself, log2FC -0.768, q = 9.86e-5 |
| `Gpi1` | WikiPathways glycolysis, early glycolysis step | 1 | only `Gpi1` itself, log2FC -0.673, q = 2.14e-7 |
| `Eno1` | WikiPathways glycolysis, lower glycolysis | 0 | no focal FDR-significant gene |
| `Slc2a1` | glucose transport and HIF/glycolysis coupling, not an enzyme step | 0 | no focal FDR-significant gene |
| `Dlat` | pyruvate dehydrogenase complex, downstream mitochondrial carbon entry | 1 | only `Dlat` itself, log2FC -0.673, q = 2.81e-7 |
| `Pdha1` | pyruvate dehydrogenase complex | 1 | only `Pdha1` itself, log2FC -1.039, q = 1.31e-6 |
| `Got1` / `Got2` / `Mdh2` | malate-aspartate shuttle and TCA-adjacent counterexamples | 1 each | only the self transcript for each target |
| `Mdh1` | cytosolic malate dehydrogenase, a broader carbon-metabolism counterexample | 29 | self `Mdh1` plus 28 downstream calls |

The same-experiment corpus independently summarizes the same boundary. `Pfkm:F001`
reported no downstream FDR response in any neuronal group after `Pfkm` perturbation;
`Hk1:F003` and `Tpi1:F004` contrasted flat or nearly flat central glycolysis
perturbations with broader responses from the hexosamine/O-GlcNAc or proteasome
axes; `Gpi1:F001` interpreted `Gpi1` as nearly origin-centered, with only two
downstream genes over 22 cell groups at FDR < 0.10; and `Eno1:F001` reported no
corrected neuronal response in any measured group. `Gfpt1` was the key pathway
counterexample: it had 311 focal DEGs and a corpus-described ER/ISR response, but
it diverts fructose-6-phosphate into UDP-GlcNAc biosynthesis rather than testing
the linear ATP-generating glycolytic segment, so it is not an appropriate count
template for `Pgk1`.

This points to a nonzero but minimal prediction. The nonzero part is driven by the
raw within-dataset pattern that measured glycolytic targets with 148-248 matched
focal perturbed nuclei often cross FDR on their own RNA. The minimal part is driven
by the repeated absence of downstream FDR hits for `Hk1`, `Pfkm`, `Tpi1`, `Gpi1`,
and `Eno1`, together with the corpus interpretation that acute sparse loss of one
central glycolytic enzyme is transcriptionally buffered in surviving postmitotic
neurons. External PGK1 biology says that the enzyme can be disease-relevant and
metabolically essential, but it does not override the experiment-matched evidence:
the readout is a 3-4 week sparse neuronal snRNA profile, not enzyme flux, ATP,
erythrocytes, glia, or organismal viability.

Therefore my point estimate is `1`: one significant measured gene, most likely
`Pgk1` itself, and no propagated downstream focal program.

## Limits

- The major extrapolation is target engagement. `Pgk1` was held out, so its guide
  performance and self-RNA depletion are unknown. A weak Pgk1 guide set would make
  the correct count `0`; unusually efficient disruption or survivor selection could
  make it larger.
- `Gapdh`, `Pgam`, `Pkm`, and `Pgk2` were not usable focal training perturbations,
  so the closest observed enzymes bracket but do not duplicate the phosphoglycerate
  kinase reaction.
- The one DEG predicted here relies on the endpoint including self transcripts.
  The downstream biological prediction is closer to zero.
- A large metabolic phenotype could be invisible in this assay if it changes ATP,
  NADH/NAD+, glycolytic intermediates, firing, or survival without leaving an FDR
  RNA signature in recovered NeuN+ nuclei.
- The Parquet profile vectors contain many subthreshold log-fold changes; I did
  not treat nominal high-magnitude, q=1 features as mechanistic neighbors.

## Final prediction

`Pgk1`: predicted `n_degs = 1`.
