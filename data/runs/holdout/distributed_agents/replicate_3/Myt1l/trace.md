# Held-out DEG-count prediction

## Question and interpretation

The requested held-out target list contains one gene, `Myt1l`. I interpreted the
task as asking for the integer number of genes that would pass
Benjamini-Hochberg FDR < 0.05 in the focal `151 TH Prkcd Grin2c Glut`
population after acute sparse AAV CRISPR loss of `Myt1l`, using the same
single-nucleus Wilcoxon pipeline as the supplied training parquet.

I treated `n_degs` as a calibrated screen endpoint, not as a direct measure of
target importance or viability. A prediction of zero would mean no measured
transcript is expected to cross the focal-cell FDR cutoff; it would not mean
that MYT1L has no neuronal function. The held-out perturbation was absent from
both the parquet's `gene_target` column and the focal-cell count CSV, so every
numerical transfer below comes from non-held-out training perturbations.

## Sources used

- Input training endpoint:
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
- Input differential-expression parquet:
  `[local file: training_de_all_cell_groups.parquet]`.
- Requested-target manifest:
  `[local file: 140_Myt1l.csv]`.
- Distributed Agents selected same-experiment corpus:
  `perturbai-july-260713-sourceguard-1773-v1`, queried with
  `target_context` for `Myt1l`, `Rest`, `Ehmt1`, `Mecp2`, and `Zbtb18`.
- PerturbAI curated gene-annotation / analog-nomination store, using GO
  biological-process and molecular-function memberships plus the
  `functional_class:transcription_factor` class over the closed perturbation
  universe.
- NCBI Entrez / PubMed for external MYT1L literature.

## Dataset computations

I first verified that `Myt1l` was not present among the 1,674 training
perturbations in the focal endpoint table. The training endpoint distribution
is highly zero-inflated:

- 1,205 / 1,674 training targets have `n_degs = 0`.
- 341 have 1-5 DEGs.
- 50 have 6-20 DEGs.
- 36 have 21-100 DEGs.
- 42 have more than 100 DEGs.
- The median is 0, the 75th percentile is 1, and the 95th percentile is 18.

For nominated analogs and counterexamples I queried the parquet in the exact
focal context, grouping by `gene_target` and counting `pvals_adj < 0.05`.
I also pulled the FDR-significant genes and leading adjusted p-values for the
low-count analogs to avoid transferring from a target that was formally zero
but just below threshold. Whole-vector profile-neighborhoods were written to
`profile_neighbors_myt1l_analogs.json`, but I did not use their nearest
whole-profile correlations for the point estimate because they were dominated
by thousands of nonsignificant, pseudo-count-sensitive log-fold changes; the
FDR-supported DEG lists are the statistic being predicted.

## Analog search

`Myt1l` itself was absent from the selected Distributed Agents corpus snapshot; no
same-experiment Findings, Claims, or explicit references were attached to the
held-out target. The deterministic annotation/analog search resolved `Myt1l`
as a mouse DNA-binding zinc-finger transcription factor annotated to neuronal
development / differentiation and RNA polymerase II transcriptional regulation,
but all available nominated training candidates were only
`broad_functional_fallback`; there was no available perturbed MYT-family
paralog, exact complex member, narrow pathway member, or STRING physical
interactor. Thus the training analog set had to be bounded by imperfect
functional comparators rather than by a direct MYT1L complex.

### Sparse positive analogs

These were the main positive-count anchors for the final estimate.

- `Ehmt1`: 4 DEGs with 207 matched perturbed nuclei. Its significant focal
  genes were `Abhd12b`, `Endou`, `Smtn`, and `Stxbp2`, all up. The Distributed Agents
  corpus describes `Ehmt1` as a very sparse postnatal neuronal chromatin
  perturbation and notes a tiny thalamic module partly shared with other
  chromatin repressors such as `Chd4`, `Setdb1`, and `Sin3a`.
- `Zbtb18`: 5 DEGs with 208 matched perturbed nuclei: `Endou`, `Pxdn`,
  `Clstn2`, `Man2a2`, and the `Zbtb18` transcript, all up. The corpus notes
  that postnatal `Zbtb18` loss did not derepress the expected embryonic
  cortical-neurogenesis program, and that BTB-ZF family membership was a weak
  predictor of the actual neuronal RNA phenotype.
- `Sox2`, `Sox5`, and `Nr2f1`: each had only 2 DEGs in the focal population.
  These are broad neural transcription factors rather than direct MYT1L
  analogs, but they show that named neuron/fate regulators often land in the
  1-5 DEG tail after P16 sparse CRISPR.
- `Mecp2`: 16 DEGs with 167 matched perturbed nuclei. MECP2 is not a sequence
  or complex analog of MYT1L, but it is a postmitotic neuronal chromatin
  maintenance factor with a real, still sparse, focal signal. I treated 16 as
  an upper-ish bound for a direct identity-maintenance factor rather than as
  the center for `Myt1l`.

### Flat counterexamples

Several training transcription-factor perturbations with enough matched nuclei
were silent in the exact same cell group: `Rest` 0 DEGs with 271 matched
nuclei, `Neurod1` 0 with 304, `Neurod2` 0 with 260, `Bcl11a` 0 with 203,
`Bcl11b` 0 with 206, `Sox4` 0 with 230, and `Tcf4` 0 with 250. These are not
MYT1L phenocopies, but they are important boundaries: developmental
neurogenic or lineage TF function in the literature frequently became nearly
invisible when perturbed acutely after cell fate specification.

`Rest` is the closest conceptual counterexample because REST and MYT1L both
live near neuronal/non-neuronal identity repression. The same-experiment
Distributed Agents corpus calls acute P16 `Rest` loss a pan-neuronal transcriptional
zero, with 23/23 cell groups lacking downstream FDR < 0.10 genes, and
explicitly separates the flat `Rest` result from active chromatin-repressor
programs driven by `Sin3a`, `Chd4`, `Zmynd8`, and `Mecp2`. In the focal
FDR < 0.05 parquet, the lowest adjusted p-values for `Rest`, `Neurod1`,
`Neurod2`, `Bcl11a`, and `Bcl11b` were all 1.

### Too-broad counterexamples

I also checked broad nuclear regulators and zinc-finger/chromatin genes that
were strong in `151 TH Prkcd Grin2c Glut`: `Sin3a` 1433 DEGs, `Zbtb7a` 841,
`Yy1` 720, `Thap11` 478, `Phf12` 403, `Wac` 384, `Setd1a` 368, `Brd4` 311,
`Tcf7l2` 106, and `Prdm10` 52. I used these mostly as upper controls. Their
training signatures demonstrate that the focal class could detect broad TF or
chromatin responses, but they were too global or pathway-divergent to justify
predicting a large MYT1L footprint. For example, `Prdm10` significantly
down-regulated measured `Myt1`, but the same rows showed no significant effect
of `Prdm10`, `Mecp2`, `Ehmt1`, `Zbtb18`, `Rest`, `Sox2`, `Sox5`, `Tcf7l2`,
`Neurod1`, `Neurod2`, `Bcl11a`, or `Bcl11b` on `Myt1l` itself.

## External MYT1L biology

MYT1L is a neuronal zinc-finger transcription factor that participates in the
Ascl1/Brn2/Myt1l induced-neuron conversion program described by Vierbuchen et
al. 2010 (Nature, PMID: 20107439, DOI: 10.1038/nature08797). Mall et al. 2017
showed that MYT1L safeguards neuronal identity by actively repressing multiple
non-neuronal fates (Nature, PMID: 28379941, DOI: 10.1038/nature21722). Woehr
et al. 2022 then showed that Myt1l haploinsufficiency in mice causes obesity
and multifaceted behavioral phenotypes (Molecular Autism, PMID: 35538503,
DOI: 10.1186/s13229-022-00497-3).

Those papers make a pure no-effect prior too harsh: MYT1L is active in neuronal
identity maintenance, not just embryonic patterning. However, they are not
direct readouts of an acute P16 mosaic CRISPR perturbation in recovered
thalamic glutamatergic nuclei. The training data repeatedly show that factors
with compelling developmental or neurodevelopmental-disease biology can be
silent once edited sparsely after neurons have differentiated.

## Target-specific prediction

### `Myt1l`

I predict a low but nonzero focal response. The zero-DEG decision was rejected
because MYT1L has a literature-supported role in maintaining neuronal identity
and because sparse postmitotic chromatin/TF anchors such as `Ehmt1`, `Zbtb18`,
`Sox2`, `Sox5`, and `Nr2f1` show that very small FDR-positive responses are
well within the assay's observed regime. A count above 10 looked too high:
`Mecp2`, at 16 DEGs, is already one of the stronger direct neuronal chromatin
maintenance examples; `Prdm10`, `Tcf7l2`, `Zbtb7a`, `Yy1`, and `Sin3a` were
broader, target-selective programs rather than close MYT1L analogs.

My point estimate is therefore 4 DEGs, centered on the `Ehmt1` / `Zbtb18`
small chromatin-repressor tail and nudged only slightly upward from the
flat postmitotic TF majority.

## Limits

The main limitation is the lack of a close measured analog. No `Myt1`, `St18`,
RCOR/LSD1/HDAC REST-corepressor member, or MYT1L physical partner was available
as a training perturbation in this focal endpoint. Broad GO coannotation gave
many transcription factors but was not specific enough to transfer counts
mechanistically. The prediction also extrapolates from postnatal thalamic
glutamatergic survivor nuclei; it may miss effects that would be larger in
progenitors, in non-neuronal lineages that MYT1L normally represses, in denser
or earlier knockout, or at protein/physiology levels rather than nuclear RNA.

Finally, the endpoint is an integer threshold count. A target with four
predicted DEGs is close to the 0-5 boundary, so one or two genes crossing the
FDR line would move the realized count substantially even if the underlying
biological effect size were almost unchanged.
