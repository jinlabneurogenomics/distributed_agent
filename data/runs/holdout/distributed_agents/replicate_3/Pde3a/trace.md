# Pde3a prediction trace

## Question and resolved details

The held-out manifest `170_Pde3a.csv` contains one requested target:

```text
Pde3a
```

I interpreted the task as a point prediction of the number of genes with
`pvals_adj < 0.05` after acute AAV-CRISPR loss of `Pde3a` in the focal
`151 TH Prkcd Grin2c Glut` thalamic glutamatergic class. I treated the target
transcript itself as eligible for the count, matching the supplied training
CSV, and I treated `151` as the dataset class identifier rather than a nucleus
count.

`Pde3a` is absent from both the DE parquet and the training count table, and it
is not represented in the same-experiment Distributed Agents corpus. The prediction
therefore has to transfer from non-held-out PDE and cAMP/cGMP pathway
perturbations.

## Sources used

- Differential-expression parquet:
  `[local file: training_de_all_cell_groups.parquet]`.
  This was the source of exact focal-cell expression patterns, self rows,
  adjusted P values, and matched cell counts for comparator perturbations.
- Training counts:
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
  This gave the exact `n_degs` endpoint for 1,674 non-held-out targets in
  `151 TH Prkcd Grin2c Glut`.
- Held-out manifest:
  `[local file: 170_Pde3a.csv]`.
- Distributed Agents same-experiment corpus
  `perturbai-july-260713-sourceguard-1773-v1`, especially `Pde1c`, `Pde4b`,
  `Pde4d`, `Pde10a`, and cAMP-pathway findings and Claims.
- Distributed Agents gene-annotation store over the closed PerturbAI gene universe:
  GO:BP/CC/MF, KEGG, Reactome, MSigDB, mouse CORUM, human CORUM projected
  through MGI one-to-one orthology, and functional-class memberships.
- Distributed Agents gene-analog nomination skill, used with the actual 1,674-gene
  training universe rather than by symbol-prefix matching.
- Public literature via PubMed for PDE3/PDE family biology.

## Computational checks over the supplied dataset

1. I read the held-out manifest and confirmed that the only requested target is
   `Pde3a`.

2. I summarized the training endpoint in the focal cell group. Of 1,674
   training targets, 1,205 had zero DEGs and 469 had at least one DEG; the
   median was 0, the 75th percentile was 1, the 95th percentile was 18, and the
   top responses were very large. Thus the endpoint is highly zero-inflated.

3. I used the annotation store and analog-nomination output to identify
   mechanistically plausible training comparators. The most direct available
   cyclic-nucleotide PDE perturbations were `Pde10a`, `Pde1c`, `Pde4b`, and
   `Pde4d`. `Pde3b`, the exact same-family PDE3 paralog and human CORUM
   `PDE3A-PDE3B` complex partner, was not in the focal training count table.
   A human one-to-one ortholog-projected CORUM complex connected `Pde3a` to
   `Calm1`, but this is a `CALM1-PDE1A-PDE3A` complex and is much less direct
   for predicting a `Pde3a` loss-of-function count than assayed PDE genes.

4. I queried the parquet only for the focal class and selected cAMP/PDE
   comparators:

```python
f = (
    (pc.field("group_name") == "151 TH Prkcd Grin2c Glut")
    & pc.field("gene_target").isin(targets)
)
```

   That pulled 207,108 rows for 12 targets, rather than loading the full
   616-million-row parquet. The PDE and pathway counts in the focal class were:

| target | focal n_degs | matched perturbed nuclei | self log2 FC | self FDR | best non-self FDR in 151 |
| --- | ---: | ---: | ---: | ---: | ---: |
| `Pde10a` | 0 | 191 | -0.200 | 1 | 0.304 |
| `Pde1c` | 0 | 155 | 0.440 | 1 | 0.180 |
| `Pde4b` | 0 | 211 | -0.451 | 1 | 0.922 |
| `Pde4d` | 0 | 192 | -0.272 | 1 | 1 |
| `Adcy1` | 0 | 88 | -0.308 | 1 | 0.139 |
| `Adcy3` | 0 | 223 | -0.569 | 0.112 | 1 |
| `Adcy5` | 0 | 154 | -0.411 | 1 | 0.912 |
| `Gnas` | 0 | 306 | -0.006 | 1 | 1 |
| `Prkaca` | 1 | 192 | -0.940 | 7.9e-22 | 0.155 |
| `Prkar1a` | 1 | 98 | -0.569 | 0.0014 | 0.332 |
| `Calm1` | 14 | 208 | -0.924 | 1.7e-34 | 9.3e-09 |
| `Creb1` | 10 | 126 | 0.705 | 0.0136 | 3.8e-07 |

   The exact four available PDE analogs all had zero focal DEGs. Even their
   most nominal non-self focal rows stayed far from FDR 0.05.

5. I ran a signed `logfoldchanges` profile comparison across the focal class
   for a PDE/cAMP cohort. `Pde10a`, `Pde1c`, `Pde4b`, and `Pde4d` each had
   17,259 focal features available but zero significant features. Because the
   PDE anchors were all null in the focal class, the top-tail overlaps were
   necessarily based on FDR=1 nominal tails and were not used as positive
   phenocopy evidence.

6. I queried the Distributed Agents same-experiment corpus for PDE and cAMP neighbors.
   The induced explicit-reference topology over `Adcy1`, `Adcy3`, `Adcy5`,
   `Gnas`, `Pde10a`, `Pde1c`, `Pde4b`, `Pde4d`, `Prkaca`, `Prkar1a`, `Creb1`,
   and `Crebbp` was one connected component, reflecting that same-experiment
   reports repeatedly compared these genes. The report semantics, not just the
   density, were the important part: the dominant conclusion was nonconvergence
   of basal cAMP/PDE transcriptional responses.

## Target-specific reasoning

### `Pde3a`

**Biochemical prior.** `Pde3a` encodes a PDE3 cyclic-nucleotide
phosphodiesterase. Curated GO/KEGG/Reactome annotations placed it in
3',5'-cyclic-AMP phosphodiesterase activity, 3',5'-cyclic-GMP
phosphodiesterase activity, the KEGG cAMP and cGMP-PKG signaling pathways, and
Reactome G alpha (s) signalling events. These annotations justified looking at
assayed cAMP and cGMP PDEs rather than generic hydrolases.

The public PDE3 literature made the same comparison biologically sensible but
also weakened the expectation of a strong thalamic neuronal RNA phenotype.
Ahmad, Degerman, and Manganiello 2012 reported that PDE3A and PDE3B hydrolyze
cAMP and cGMP with high affinity in a mutually competitive manner and that
PDE3A is most enriched in heart, platelets, vascular smooth muscle cells, and
oocytes, while PDE3B is more prominent in metabolic cell types
(PubMed 22692928, DOI 10.1055/s-0032-1312646). Genetic mouse work showed the
best-established Pde3a-null phenotype in oocytes: `Pde3a`-deficient females
ovulated oocytes that remained arrested at the germinal-vesicle stage because
increased cAMP/PKA signaling blocked meiotic maturation (Masciarelli et al.,
2004, PubMed 15254586, DOI 10.1172/JCI21804). A review of the same models
also emphasized PDE3A in vascular smooth muscle growth and oocyte maturation
(Begum, Shen, and Manganiello 2011, PubMed 22051884,
DOI 10.1016/j.coph.2011.10.006).

Those contexts are largely absent from this NeuN-enriched, postmitotic
brain-nucleus assay. PDE10A and PDE4D are better established neuronal PDEs:
PDE10A is enriched in striatal neurons and regulates cAMP/cGMP signaling
(Wilson and Brandon 2015, PubMed 25159072,
DOI 10.2174/1381612820666140826114744), while PDE4D is part of brain cAMP/PKA
/CREB pharmacology (Gurney, D'Amato, and Burgin 2015, PubMed 25371167,
DOI 10.1007/s13311-014-0309-7). Kelly et al. 2013 mapped many PDE isoforms
across adult rodent CNS regions and reinforced that PDE isoforms have distinct
regional expression programs rather than one interchangeable neuronal PDE pool
(PubMed 24184653, DOI 10.1016/j.cellsig.2013.10.007).

**Training perturbations and pattern evidence.** The four closest trainable
PDE analogs in the focal `151 TH Prkcd Grin2c Glut` counts were all exact
zeros:

- `Pde10a`: `n_degs = 0`; 191 perturbed vs 23,679 control nuclei; self
  log2 FC -0.200, FDR 1; best focal adjusted P value 0.304.
- `Pde1c`: `n_degs = 0`; 155 perturbed nuclei; self log2 FC 0.440, FDR 1;
  best focal adjusted P value 0.180.
- `Pde4b`: `n_degs = 0`; 211 perturbed nuclei; self log2 FC -0.451, FDR 1;
  best focal adjusted P value 0.922.
- `Pde4d`: `n_degs = 0`; 192 perturbed nuclei; self log2 FC -0.272, FDR 1;
  best focal adjusted P value 1.

Same-experiment Distributed Agents reports make those zeros more informative than a
flat symbol-family lookup. `Pde1c` had a pan-measured central neuronal null
across the corpus and did not converge with `Pde10a`, `Pde4b`, `Pde4d`,
`Adcy1`, `Adcy3`, `Adcy5`, `Prkaca`, or `Prkar1a`. `Pde4d` was also fully
buffered across its recovered neuronal surface, and its corpus report
explicitly notes that `Pde4b` and `Pde10a` had only weak, non-overlapping
signatures. `Pde4b` had only two robust downstream hits, outside 151, and did
not induce a broad cAMP/CREB immediate-early program. `Pde10a` was the one
PDE with a recognizable canonical effect, but it was in the striatal/LGE GABA
class and did not generalize to the focal thalamic glutamatergic class.

The broader cAMP counterexamples point the same way in `151`: `Adcy1`,
`Adcy3`, `Adcy5`, `Gnas`, and `Rapgef4` were all zero, and even `Prkaca` and
`Prkar1a` only had their own transcripts pass FDR despite strong self
depletion. `Calm1` and `Creb1` were nonzero in 151, but they are less
specific: `Calm1` is an essential calcium sensor that participates in many
non-PDE processes, and `Creb1` is a nuclear transcription-factor node. Their
positive counts show that the 151 assay had power to detect calcium/CREB
states, not that `Pde3a` should be promoted above the direct PDE nulls.

**Zero/nonzero decision.** I therefore predict that `Pde3a` loss will not
produce a gene passing FDR 0.05 in 151. The decision is driven primarily by
within-dataset evidence: all direct measured cyclic-nucleotide PDE analogs had
`n_degs = 0` in the exact focal cell group, upstream membrane cyclases and
`Gnas` were also silent there, and corpus-level PDE reports show no
reproducible shared basal PDE transcriptome to transfer. External biology
supports the zero by placing the strongest PDE3A phenotypes in oocytes and
vascular/cardiac/platelet signalosomes, or in cAMP/cGMP/phosphorylation
modalities, rather than in broad basal RNA remodeling of juvenile thalamic
neurons. The final point estimate is:

```text
Pde3a -> 0
```

## Limits

- `Pde3a` itself was held out, so there is no direct expression signature or
  self-transcript row to inspect.
- The exact same-family PDE3 comparator `Pde3b` was not in the focal training
  universe; transfer used PDE1/PDE4/PDE10 and upstream cAMP nodes.
- Absence of focal snRNA-seq DE does not rule out Pde3a indels, PDE3A protein
  loss, local cAMP/cGMP changes, PKA/PKG phosphorylation changes,
  electrophysiology, or an evoked neuromodulator response.
- PDE3A biology in vascular smooth muscle, heart, platelets, and oocytes is
  off-panel in this NeuN-positive postnatal brain assay.
- The high-yield 151 group is still one thalamic glutamatergic class; a
  different brain cell type or a purified striatal/hypothalamic population
  could behave differently.
