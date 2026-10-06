# Reasoning trace

## Question and resolved ambiguities

The held-out manifest for this run contains one requested target:

```tsv
target_name
Kmt2d
```

I interpreted the endpoint as the exact focal-cell scalar in the prompt: the number of measured genes with `pvals_adj < 0.05` after acute mosaic CRISPR loss of the requested target in `151 TH Prkcd Grin2c Glut` cells. `Kmt2d` was fully held out, so I did not have its own focal-cell DEG count or its expression signature. The prediction therefore has to be transferred from non-held-out perturbations in the focal DE table and from target biology. I treated weak or unchanged self-target RNA as non-decisive quality-control context, consistent with the experiment's average modest nuclear mRNA depletion.

## Sources used

- Differential-expression parquet:
  `[local file: training_de_all_cell_groups.parquet]`
- Focal-cell training counts:
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`
- Held-out manifest:
  `[local file: 122_Kmt2d.csv]`
- Run-local Distributed Agents same-experiment corpus:
  `perturbai-july-260713-sourceguard-1773-v1`, queried for Kmt2a, Kmt2c, and Setd1a curated findings.
- PubMed literature on KMT2C/KMT2D MLL3/MLL4 enhancer COMPASS biology and Kabuki syndrome.

Key external references were:

- Lee et al. 2013, eLife, DOI `10.7554/eLife.01503`, PMID `24368734`: MLL4/KMT2D is a major enhancer H3K4 mono- and di-methyltransferase with partial functional redundancy with MLL3/KMT2C, needed for enhancer activation in differentiation.
- Wang et al. 2016, PNAS, DOI `10.1073/pnas.1606857113`, PMID `27698142`: MLL4 can be dispensable for maintaining ESC cell-identity gene expression but is required for p300 enhancer recruitment and enhancer activation during cell-fate transition.
- Sze and Shilatifard 2016, Cold Spring Harbor Perspectives in Medicine, DOI `10.1101/cshperspect.a026427`, PMID `27638352`: review of the MLL3/MLL4/COMPASS family and enhancer regulation.
- Adam et al. 2018, Journal of Medical Genetics, DOI `10.1136/jmedgenet-2018-105625`, PMID `30514738`: Kabuki syndrome consensus criteria and the central roles of pathogenic KMT2D and KDM6A variants.
- Rots et al. 2024, American Journal of Human Genetics, DOI `10.1016/j.ajhg.2024.06.009`, PMID `39013459`: KMT2C loss-of-function as a neurodevelopmental disorder distinct from Kabuki syndrome.

## Computations over the training data

I first read the manifest and confirmed there was exactly one row, `Kmt2d`.

For calibration, I loaded the 1,674 focal-cell training counts. The distribution was strongly zero-inflated:

- `1205/1674` targets had `n_degs = 0`.
- `363/1674` had `1-9` DEGs.
- `63/1674` had `10-99` DEGs.
- `43/1674` had `>=100` DEGs.
- The median was `0`, the 95th percentile was `18`, and the maximum was `2677`.

To get expression-pattern evidence rather than relying only on those counts, I scanned the parquet with
`group_name == "151 TH Prkcd Grin2c Glut"` and read `names`, `gene_target`,
`logfoldchanges`, and `pvals_adj`. This produced `28,891,566` rows: `1,674`
training perturbations by `17,259` measured genes. I recomputed

```python
df["pvals_adj"].lt(0.05).groupby(df["gene_target"]).sum()
```

and verified that it exactly matched the supplied focal-cell training count CSV.

I then built a dense `gene_target x names` matrix of signed log2 fold changes.
For Kmt2d-relevant observed chromatin perturbations, I computed Pearson
correlations over all 17,259 genes and, separately, exact overlaps of
FDR-significant genes. The absolute all-gene Pearson correlations among many
chromatin targets were not very discriminating: even flat or weak perturbations
had correlations around `0.61-0.70`. The exact FDR overlaps were more useful.
For example, Kmt2a's 24 FDR genes overlapped Kmt2c by 0 genes, Setd1a by 1,
Crebbp by 0, and Ep300 by 0. Setd1a's broad 368-gene state overlapped Brd4 by
18 and Chd8 by 14, but still overlapped Kmt2a by only 1 and Kmt2c by 0.

## Kmt2d-specific analogs and counterexamples

### Kmt2c: closest enhancer-writer paralog, observed count 0

Kmt2c is the most direct in-dataset paralog of held-out Kmt2d. KMT2C/MLL3 and
KMT2D/MLL4 occupy the enhancer COMPASS branch and are repeatedly described as
partly redundant H3K4me1/2 enhancer methyltransferases rather than as promoter
H3K4me3 writers. That makes Kmt2c much closer to Kmt2d than Setd1a or Kmt2a
mechanistically.

In the focal endpoint, Kmt2c had `0` DEGs. The Distributed Agents corpus summarized the
same-experiment Kmt2c surface as a high-confidence buffered response:
acute P16 Kmt2c loss was broadly quiet, with only one Prnp response at the
FDR 0.10 threshold outside this focal class and no meaningful data-driven
signature neighbor. That is a strong within-dataset argument that at least one
MLL3/MLL4 enhancer writer can be buffered in the postnatal, postmitotic CRISPR
context even though KMT2C germline haploinsufficiency causes a human
neurodevelopmental disorder.

The difference between KMT2D and KMT2C matters: KMT2D is the more common
Kabuki syndrome gene, and Lee et al. found major MLL4-dependent enhancer
activation in differentiating lineages. Still, the exact in-assay paralog being
flat is the most specific calibration point, so I weighted it more heavily than
remote H3K4 regulators with strong signatures.

### Kmt2a: H3K4 writer but promoter-biased, observed count 24

Kmt2a had a small but real focal response with `24` DEGs. Its top FDR genes
included down-regulated thalamic identity/connectivity transcripts such as
`Nr2f1`, `Pcdh7`, `Lhx9`, `Pcdh10`, `Grik2`, `Camk2d`, `Map1b`, `Sox2`, and
up-regulated counter-module genes such as `Igfbp5`, `Tnr`, `Cx3cl1`, `Atxn2l`,
`Luc7l`, and `Txndc5`. The Distributed Agents corpus described this as a sparse,
glutamatergic-biased response concentrated in `151 TH Prkcd Grin2c Glut`.

Kmt2a is a useful ceiling for a small KMT-family effect, but not a direct
phenocopy. KMT2A/MLL1 sits in a different COMPASS-like branch and is more
closely tied to promoter H3K4 methylation than the enhancer MLL3/MLL4 branch.
The expression evidence also did not tie Kmt2a to the other represented H3K4
writers: its FDR overlap with Setd1a was one gene and with Kmt2c was zero.
So I used Kmt2a as evidence that a Kmt-family perturbation can cross the focal
FDR gate, but only at the low tens in this class.

### Setd1a: strong H3K4 COMPASS counterexample, observed count 368

Setd1a was much broader, with `368` focal DEGs. Its leading genes were largely
down-regulated mitochondrial, GPI-anchor, ER proteostasis, UFMylation,
Golgi/vesicle, ciliary, and lysosomal/autophagy transcripts, including
`Foxred1`, `Nprl3`, `Sfi1`, `Tafazzin`, `Pigq`, `Ufl1`, `Pigk`, `Fastk`, and
`Prkn`. Distributed Agents findings likewise summarized the Setd1a response as a broad
but nonuniform recurrent state and specifically noted that measured KMT2 and
chromatin-disorder comparators did not phenocopy Setd1a.

I therefore treated Setd1a as a counterexample against the simple rule "all
H3K4 writers are quiet", not as the quantitative prior for Kmt2d. SETD1A
operates in a promoter H3K4me3 COMPASS branch, whereas KMT2D is an
enhancer-associated MLL3/MLL4 subunit. The observed Setd1a footprint also had
almost no FDR-level overlap with Kmt2a or Kmt2c.

### Enhancer and chromatin regulators around the Kmt2d pathway

The training set had several additional chromatin regulators but lacked the
most direct KMT2D complex-specific partners: Kdm6a/UTX, Paxip1/PTIP, Ncoa6,
Ash2l, Rbbp5, Wdr5, and Dpy30 were not observed focal training targets.

The nearest available enhancer coactivator evidence was quiet to weak:

- `Ep300`: `0` DEGs.
- `Crebbp`: `8` DEGs.
- `Kdm6b`: `0` DEGs; informative only as a different H3K27 demethylase, not as UTX/KDM6A.
- `Kat6a`: `0` DEGs.
- `Kat6b`: `0` DEGs.
- `Arid1b`: `1` DEG.
- `Ehmt1`: `4` DEGs.

There were stronger chromatin perturbations, for example `Chd8` at 61,
`Chd4` at 100, `Brd4` at 311, and `Setd1a` at 368, but their FDR signatures
either did not share the Kmt2a/Kmt2c FDR loci or represented generic chromatin,
RNA-processing, or stress-like states rather than the MLL3/MLL4 enhancer module.

This pattern argues that Kmt2d should not be raised to a medium or strong
prediction just because it is a famous chromatin neurodevelopmental gene.
Most of the directly enhancer-adjacent training perturbations were flat or
single-digit in this acute neuronal endpoint.

## Zero/nonzero decision and point prediction for Kmt2d

KMT2D has real neurodevelopmental importance: pathogenic KMT2D variants are
the dominant known cause of Kabuki syndrome, and MLL4 loss can severely impair
lineage enhancer activation. That external evidence argues against calling the
gene biologically irrelevant.

The endpoint, however, is not developmental organismal fitness or enhancer
competence during a fate transition. It is a 3-4 week nuclear RNA footprint
after sparse P16 CRISPR in recovered postmitotic thalamic neurons. In that
context, the decisive within-dataset facts were that the enhancer-writer
paralog `Kmt2c` had `0` focal DEGs, p300/CBP perturbations were `0` and `8`,
and other Kabuki/chromatin-adjacent factors available in the training set were
mostly weak. Kmt2a's 24-gene focal response leaves room for a small KMT-family
effect, but it is a different H3K4 branch with a different expression module.
Setd1a's 368-gene response is too mechanistically distant to transfer to
Kmt2d.

I therefore predict that Kmt2d is at the null/near-null boundary and that no
gene will pass the BH `pvals_adj < 0.05` threshold in `151 TH Prkcd Grin2c
Glut` cells. A handful of subthreshold enhancer-maintenance changes would not
surprise me, but the closest observed enhancer branch says they are unlikely
to become FDR-significant in this assay.

Final point prediction:

- `Kmt2d`: `0`

## Limits

- Kmt2d itself was held out, and no Kmt2d-specific report was present in the
  selected Distributed Agents corpus. The prediction is necessarily extrapolated.
- Kmt2c is the closest measured paralog, but KMT2D and KMT2C have different
  disease penetrance and may not be redundant in this thalamic population.
- Core MLL3/MLL4 components such as Kdm6a, Paxip1, Ncoa6, Wdr5, Rbbp5, Ash2l,
  and Dpy30 were absent from the focal training count table, limiting direct
  within-complex triangulation.
- Whole-signature Pearson neighbors in the focal matrix were globally high
  even for many zero-count targets, so I treated them as weak background
  evidence and relied more on target-specific biology plus exact FDR modules.
- The FDR count is power- and assay-dependent. A prediction of zero does not
  imply that Kmt2d editing failed, that KMT2D is unimportant, or that enhancer
  chromatin was unchanged at all loci.
