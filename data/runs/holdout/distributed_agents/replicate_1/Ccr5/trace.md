# Trace

## Question and endpoint

I interpreted the task as a point prediction of the held-out scalar endpoint
`n_degs` for each requested perturbation in `151 TH Prkcd Grin2c Glut` cells.
Here `n_degs` is the count of measured transcripts with Wilcoxon
Benjamini-Hochberg adjusted `pvals_adj < 0.05` in the focal thalamic
glutamatergic class after acute AAV-CRISPR loss of function at P16 and harvest
at P37-P44. `TH` was interpreted as thalamus from the atlas label, not tyrosine
hydroxylase. The single requested held-out perturbation was `Ccr5`; its own DEG
count and expression signature were absent from the supplied training count CSV
and Parquet, so the requested endpoint is directly observed for analog
perturbations but absent for `Ccr5` itself.

## Sources used

- Declared focal training counts:
  `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
- Declared differential-expression Parquet:
  `training differential-expression dataset`.
- Requested-target manifest:
  `single-target request for Ccr5`.
- Run-local dataset portrait, task bindings, coverage, and measurement registry.
- The PerturbAI same-experiment semantic corpus,
  `perturbai-july-260713-sourceguard-1773-v1`, via its Findings/Reports ledger
  and BioKG graph. I used this only as packaged interpretation of the same
  experiment, not as independent replication.
- External PubMed literature on CCR5/C-C chemokine signaling in immune cells,
  glia, injury, and disease.

## Quantitative calibration

The focal training table contained 1,674 unique non-held-out biological
targets. Its response breadth was sparse and zero-inflated: 1,205/1,674
perturbations had `n_degs = 0`; the median was 0, the 75th percentile was 1,
the 90th percentile was 2, and the 95th percentile was 18. The broad responses
were concentrated in a small set of housekeeping or regulatory perturbations
such as `Uba5` with 2,677 DEGs, `Tpr` with 1,768, `Sin3a` with 1,433, and
spliceosome/proteasome-associated targets.

I then filtered the Parquet to the focal `151 TH Prkcd Grin2c Glut` row groups
and counted FDR-significant genes for mechanistically relevant immune,
chemokine, cytokine, GPCR, and MAPK comparators. The purpose was to ask whether
a visible target in the same receptor family or a plausible CCR5 downstream
branch gives a nonzero response in the exact endpoint, not to infer function
from shared pathway labels alone.

Representative focal counts were:

| visible perturbation | reason for comparison to `Ccr5` | focal `n_degs` or Parquet FDR0.05 count |
| --- | --- | ---: |
| `Ccr2` | closest represented C-C chemokine receptor; immune chemotaxis receptor | 0 |
| `Cx3cr1` | microglial chemokine GPCR, tests lineage-displaced chemokine receptor biology | 0 |
| `Cxcr4` | Gi-coupled chemokine receptor with strong CNS developmental functions | 0 |
| `P2ry12` | microglial GPCR, tests immune-lineage receptor activity in NeuN+ neurons | 0 |
| `Tlr2`, `Tlr3`, `Tlr4`, `Tlr5`, `Tlr7`, `Tlr8` | innate immune receptors that would expose a basal inflammatory state | 0 each |
| `Ifnar1`, `Ifnar2`, `Ifngr1`, `Ifngr2` | cytokine receptors for IFN pathways | 0 each |
| `Nfkb1`, `Rel`, `Stat2`, `Stat3`, `Stat4`, `Stat5b` | inflammatory transcriptional transducers | 0 each |
| `Stat1` | IFN transducer | 1, and the one DEG was `Stat1` itself |
| `Il1r1`, `Il1rap`, `Il6ra`, `Il6st` | cytokine receptors/co-receptors upstream of NF-kappaB/JAK-STAT | 0 each |
| `Gnal`, `Gnao1`, `Gnas`, `Hras`, `Kras`, `Raf1`, `Pik3cb`, `Pik3r1`, `Pik3r2` | GPCR/Ras/PI3K pathway context | 0 except `Gnao1` = 1, its own transcript |
| `Braf` | MAPK counterexample with a visible neuronal effect | 4 |
| `Mtor`, `Rptor`, `Akt3`, `Prkaca`, `Creb1`, `Tsc2` | mTOR/PKA/CREB branches reported downstream of CCR5 in disease models | 2, 0, 0, 1, 10, 86 |

The near-threshold structure was also weak. In the focal Parquet, `Ccr2`,
`Cx3cr1`, `P2ry12`, all six TLRs above, `Ifnar1/2`, `Ifngr1`, `Nfkb1`, and most
`Stat` perturbations had no genes even at FDR 0.20. `Cxcr4` had only one
sub-threshold focal gene, `Pum1` at adjusted `p = 0.067`; `Il1r1` had only
`Kdm3b` at adjusted `p = 0.081`.

Two additional focused Parquet checks addressed chemokine feedback. First,
the `Ccr5` measured-gene row was present but never significant in the focal
class under any visible perturbation: 0/1,674 rows had `Ccr5 pvals_adj < 0.05`,
the minimum `pvals_adj` was 1.0, and the largest absolute Wilcoxon score was
0.58. Second, focal `Ccl2`, `Ccl3`, `Ccl4`, `Ccl5`, `Ccl7`, `Ccl8`, `Ccl12`,
`Cxcl10`, `Il1b`, and `Mmp9` rows were all FDR 1.0 after `Ccr2`, `Cx3cr1`,
`Cxcr4`, `P2ry12`, `Il1r1`, `Il6ra`, `Ifngr1`, `Nfkb1`, `Stat1`, and `Stat3`
perturbation. Large signed log fold changes in some of these rows occurred
with scores near zero and FDR 1.0, consistent with pseudocount behavior for
very sparse immune transcripts rather than a coherent response.

## Same-experiment corpus evidence

The July PerturbAI Findings ledger had no `Ccr5` report because `Ccr5` is held
out, but it contained directly relevant reports for the visible analogs.

The `Ccr2` report recorded an all-neuronal null: no recovered neuronal cell
group had a downstream gene at FDR < 0.10. It also noted that represented
chemokine-receptor comparators did not phenocopy `Ccr2`: `Cx3cr1` was flat
across 23 tested groups and `Cxcr4` produced only two isolated single-gene
FDR < 0.10 hits. That argues that the screen did not contain a generic
chemokine-GPCR transcriptional program in basal NeuN-positive neurons.

The `Cx3cr1` report interpreted the zero as a lineage-match issue:
CX3CR1 is a fractalkine receptor whose established receptor-positive side is
microglial, whereas the experiment FACS-enriched NeuN-positive neuronal nuclei.
`P2ry12` gave the same lesson from an unrelated microglial GPCR: `P2ry12`,
`P2ry14`, `Cx3cr1`, `Csf1r`, `Ccr2`, `Axl`, and `Mertk` had no robust
downstream FDR < 0.10 genes in recovered neuronal groups.

The `Cxcr4` report supplied the strongest counterexample to a simple "chemokine
receptor means null" rule, because CXCL12/CXCR4 is a bona fide neuronal
developmental pathway. Even there, acute postnatal neuronal `Cxcr4` loss was
nearly flat: the canonical CXCL12/CXCR4/ACKR3 neurodevelopmental marker axis
was not recovered, and its focal response in `151 TH Prkcd Grin2c Glut` was
only the sub-FDR `Pum1` singleton. The visible Ccr5-like prior is therefore
that chemokine receptors with strong biology can be invisible when the ligand,
developmental time, or responsive lineage is outside this P16-to-P37 basal
neuronal assay.

The `Tlr4` and `Ifngr1` reports were broader inflammatory controls. `Tlr4`
loss was a pan-neuronal baseline null; the TLR4-to-NF-kappaB/IRF output genes
and all represented TLR/NF-kappaB/IRF relatives were absent or singleton.
`Ifngr1` loss likewise failed to expose a tonic IFNGR1/JAK/STAT1 or MHCI/IFN
module. These reports are not direct CCR5 evidence, but they make it less
likely that uninjured thalamic glutamatergic neurons in this dataset are
carrying a constitutive immune-cytokine program that CCR5 loss would broadly
collapse.

The BioKG graph for `Ccr2` only exposed explicit comparator mentions such as
`Cx3cr1` and `Cxcr4`; I used it as a bounded navigation check and did not use
graph topology or comparator count as a score.

## External mechanism

CCR5 is a C-C chemokine GPCR activated by inflammatory ligands including CCL3,
CCL4, and CCL5. Its most canonical in vivo roles are immune-cell chemotaxis and
inflammatory recruitment. For example, Joo et al. 2019 showed that the
CCR5-CCL5 axis is required for migration of HSV-2-specific effector cells to
vaginal mucosa after nasal immunization (doi:10.1038/s41385-019-0203-z,
PMID:31551493), and Yamagami et al. 2005 showed a CCR5 requirement for
MHC class II-positive Langerhans-cell recruitment in injured mouse corneal
epithelium (doi:10.1167/iovs.04-0658, PMID:15790880).

CCR5 also has CNS injury and neuroinflammation biology, but that evidence is
mostly ligand-rich, disease-associated, non-cell-autonomous, or glial/immune.
Gamo et al. 2008 reported that nerve injury induces CCR5 in microglia and that
CCR5-mediated neuron-glia signaling suppresses microglial neurotoxicity
(doi:10.1523/JNEUROSCI.2920-08.2008, PMID:19005063). Haruwaka et al. 2019
found that systemic inflammation drives CCR5-dependent migration of resident
microglia to cerebral vessels (doi:10.1038/s41467-019-13812-z,
PMID:31862977). Festa et al. 2023 showed that activated microglial CCL3/CCL4/
CCL5 can signal to neuronal CCR5 to activate PI3K-AKT-mTORC1 and inhibit
autophagy in Huntington and tauopathy models (doi:10.1016/j.neuron.2023.04.006,
PMID:37105172). Joy et al. 2019 showed that CCR5 antagonism or neuronal
knockdown after stroke or traumatic brain injury can improve recovery and alter
CREB/DLK-associated repair signaling in injured cortex
(doi:10.1016/j.cell.2019.01.044, PMID:30794775).

Those papers make `Ccr5` biologically real rather than a random null gene, but
their causal chains all require stages that are weak or absent here:

1. inflammatory or injury ligands from microglia, astrocytes, or infiltrating
   immune cells;
2. receptor-positive immune or injury-induced neuronal populations;
3. BBB or cell-recruitment endpoints, microglial activation, neuronal
   pyroptosis, autophagy, or circuit repair; and
4. often acute ligand addition, antagonist exposure, germline loss, disease
   injury, or shRNA before injury.

The declared experiment instead sparse-edited postmitotic NeuN-positive
neurons in mostly uninjured postnatal mouse brain and counted DEGs among
surviving recovered neuronal nuclei.

## Target-specific prediction

### `Ccr5`

I predicted `0` DEGs.

The strongest within-dataset analog is `Ccr2`, another C-C chemokine receptor:
its exact focal endpoint was `0`, no focal genes were close to FDR 0.20, and
the packaged same-experiment report recorded a pan-neuronal null and
noise-level signature neighbors. The transfer is same-direction because both
`Ccr2` and `Ccr5` are chemokine GPCRs whose dominant basal phenotypes occur
through chemokine sensing by immune-lineage cells rather than through tonic
cell-autonomous transcriptional maintenance in mature neurons.

`Cx3cr1` and `P2ry12` are not CCR5 paralogs, but they are useful counterexamples
because they are real brain immune/microglial GPCRs with disease biology. Both
had focal `n_degs = 0`, and their reports attributed the absence of neuronal
DE to lineage displacement under NeuN enrichment. `Ccr5` is expected to behave
similarly unless a disease-induced neuronal CCR5 ligand loop is present.

`Cxcr4` is the plausible pro-nonzero comparator: it is a chemokine GPCR with
established neuronal roles, but its focal count was still `0` at FDR 0.05 and
only a `Pum1` singleton at FDR 0.10. That pushes the expected CCR5 count toward
zero even if low-level receptor signaling exists, because this endpoint
requires a broad sustained nuclear RNA change 3-4 weeks after P16 editing.

The inflammatory receptor and transducer panel was also flat. `Ifnar1/2`,
`Ifngr1/2`, `Il1r1`, `Il1rap`, `Il6ra`, `Il6st`, `Nfkb1`, `Rel`, `Stat2`,
`Stat3`, `Stat4`, `Stat5b`, and six TLRs all produced zero focal DEGs, while
`Stat1` had only its self transcript. The expected CCR5 downstream cytokine
and chemokine readouts, including `Ccl3`, `Ccl4`, `Ccl5`, `Cxcl10`, `Il1b`,
and `Mmp9`, were FDR 1.0 in every close immune-receptor perturbation I checked.

I therefore treated `Ccr5` as a biologically meaningful receptor whose main
injury or glial contexts were not represented by the supplied endpoint. The
zero/nonzero decision is driven primarily by the within-dataset zeroes for
`Ccr2`, `Cx3cr1`, `P2ry12`, `Cxcr4`, TLRs, and IFN/IL/NF-kappaB components,
with external CCR5 literature explaining why those zeroes transfer: the causal
chain for a large CCR5 effect breaks at exposure and lineage in this uninjured
NeuN-positive assay.

## Limits

`Ccr5` was held out completely, so there is no direct `Ccr5` DEG count or
score-vector neighbor in the supplied data. The closest visible C-C receptor
was `Ccr2`; other analogs are pathway or lineage controls rather than exact
CCR5 ligand-receptor components. The Parquet contains DE summaries, not raw
expression or DNA-indel rates, so I could not confirm Ccr5 baseline abundance,
guide editing, or pre-assay selection. Injury papers show that neurons can
respond to CCR5 when CCL3/CCL4/CCL5 are supplied by activated microglia, and a
rare thalamic subpopulation or state-specific response could be averaged below
FDR in this coarse class. Despite those uncertainties, the best estimate for
the FDR < 0.05 DEG count in recovered basal `151 TH Prkcd Grin2c Glut` nuclei
is zero.
