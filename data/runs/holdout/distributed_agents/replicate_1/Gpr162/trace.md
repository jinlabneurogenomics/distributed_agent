# DEG-count prediction trace

## Question and endpoint

The requested held-out perturbation was `Gpr162`. I interpreted the task as a
point prediction for the assay endpoint `n_degs`: the number of measured genes
with Benjamini-Hochberg adjusted Wilcoxon `pvals_adj < 0.05` in `151 TH Prkcd
Grin2c Glut` nuclei after acute, sparse AAV-CRISPR loss of `Gpr162`. The
training endpoint directly observes the same count for 1,674 visible
perturbations in the focal cell group; the held-out `Gpr162` contrast itself is
absent from both the count CSV and the differential-expression parquet.

I treated target-transcript depletion as descriptive only. The count includes
self-transcript hits when they pass FDR, but weak self RNA loss is not evidence
of failed editing in this mosaic Cas9 design.

## Sources

- Declared inputs:
  - `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`
  - `training differential-expression dataset`
  - `single-target request for Gpr162`
- Run-local measurement registry and task bindings.
- Internal same-experiment corpus: `perturbai-july-260713-sourceguard-1773-v1`,
  used only as a packaged interpretation of the same Perturb-seq experiment.
  Its `Gpr161` report and evidence were useful because `Gpr161` was a visible
  orphan GPCR and ciliary/Hedgehog comparator for a held-out GPCR.
- External annotation and literature:
  - NCBI Gene record 14788 for mouse `Gpr162`, whose Alliance of Genome
    Resources annotation dated Jul 2025 predicts GPCR activity and broad
    nervous-system/gut/neural-retina expression.
  - Caruso et al. 2014, Gene, DOI 10.1016/j.gene.2014.09.042, PMID 25275856:
    GPR162 protein was anatomically mapped as a CNS-expressed rhodopsin-family
    orphan GPCR, with high expression in hypothalamic and hedonic-feeding
    areas.
  - Caruso et al. 2016, Gene, DOI 10.1016/j.gene.2016.01.044, PMID 26827797:
    additional rat/mouse expression and antisense knockdown data tied GPR162
    mRNA to food-intake and glucose-homeostasis phenotypes.
  - Lindqvist et al. 2023, iScience, DOI 10.1016/j.isci.2023.108416, PMID
    38077141: GPR162 acts as a CART receptor in pancreatic beta cells.
  - Long et al. 2023, Signal Transduction and Targeted Therapy, DOI
    10.1038/s41392-022-01224-3, PMID 36725837: GPR162 overexpression can
    potentiate radiation-induced STING/IRF3/type-I-interferon signaling in
    tumor models.
  - Mukhopadhyay and Rohatgi 2014, Seminars in Cell and Developmental Biology,
    DOI 10.1016/j.semcdb.2014.05.002, PMID 24845016, plus the packaged
    `Gpr161` report references to Mukhopadhyay et al. 2013, Cell, DOI
    10.1016/j.cell.2012.12.026, and Hwang et al. 2021, eLife, DOI
    10.7554/eLife.67121: these define GPR161, Smoothened, cAMP/PKA, and
    primary cilia as canonical Hedgehog pathway GPCR machinery.

## Dataset calculations

I first verified that the requested manifest contained only `Gpr162` and that
this target was held out. I then used the training count CSV to calibrate the
background in the focal class: 1,205 of 1,674 visible perturbations, 72.0%, had
`n_degs = 0`; the median was 0, the 75th percentile was 1, the mean was 14.1,
and the distribution was highly skewed by a few very broad chromatin and
proteostasis hits.

To inspect relevant analogs, I queried the parquet for rows satisfying:

```sql
group_name = '151 TH Prkcd Grin2c Glut'
AND gene_target IN (
  'Gpr161','Adcy3','Bbs5','Cplane1','Cspp1','Gli1','Gli2','Gnao1','Gnas',
  'Ift43','Ift88','Prkaca','Prkar1a','Ptch1','Ptch2','Smo','Gprc5b',
  'Cep290','Ift81','Kif3b','Rpgrip1l','Ttc21b'
)
```

For each comparator I recomputed `SUM(pvals_adj < 0.05)` and checked the
minimum adjusted P value in the focal group:

| perturbation | focal n_degs | min focal adjusted P | reason for comparison |
|---|---:|---:|---|
| `Gpr161` | 0 | 1 | closest visible ciliary orphan GPCR with a strong curated GPR161/SHH mechanism |
| `Gprc5b` | 0 | 1 | visible neuronal GPCR; internal Gpr161 nearest signature neighbor but still flat |
| `Adcy3` | 0 | 0.112 | ciliary cAMP effector; its best focal hit was the self transcript only at FDR 0.112 |
| `Gnas` | 0 | 1 | Gs alpha, upstream of cAMP |
| `Gnao1` | 1 | 9.4e-7 | neuronal Galpha/o GPCR effector; the single hit was `Gnao1` itself |
| `Prkaca` | 1 | 7.9e-22 | PKA catalytic subunit; the single hit was `Prkaca` itself |
| `Prkar1a` | 1 | 0.00138 | PKA regulatory subunit; the single hit was `Prkar1a` itself |
| `Smo` | 0 | 1 | ciliary Hedgehog GPCR |
| `Ptch1` | 0 | 1 | Hedgehog receptor/regulator upstream of Smo |
| `Ptch2` | 0 | 1 | Hedgehog receptor/regulator upstream of Smo |
| `Gli1` | 0 | 1 | Hedgehog transcriptional effector |
| `Gli2` | 0 | 1 | Hedgehog transcriptional effector |
| `Ift43` | 0 | 0.847 | intraflagellar-transport A component |
| `Ift88` | 0 | 1 | intraflagellar-transport B component |
| `Ift81` | 0 | 0.391 | intraflagellar-transport B component |
| `Bbs5` | 0 | 0.220 | BBSome component |
| `Cplane1` | 0 | 1 | CPLANE ciliogenesis component |
| `Cspp1` | 0 | 1 | ciliary protein present in the internal Gpr161 comparator set |
| `Cep290` | 0 | 0.650 | ciliary transition-zone disease gene |
| `Kif3b` | 0 | 1 | kinesin-II ciliary transport motor component |
| `Rpgrip1l` | 0 | 0.184 | ciliary transition-zone component |
| `Ttc21b` | 0 | 0.459 | retrograde IFT component |

The same-experiment `Gpr161` report sharpened this comparison: `Gpr161` had no
downstream genes at FDR < 0.10 in 21 robustly measured neuronal groups and its
canonical Hedgehog targets and neural-tube/granule-progenitor readouts all had
adjusted P = 1 in every `Gpr161` group where they were tested. The internal
report also showed that the visible Hedgehog, BBS/IFT, cAMP, and PKA targets
were almost all flat when matched to the same Gpr161 cell groups. This is
same-experiment interpretation, not independent replication, but it was useful
to reject the idea that acute loss of a ciliary GPCR should generically produce
a large juvenile neuronal snRNA response.

I also asked whether `Gpr162` itself was an FDR-level downstream marker in the
focal class. It was repressed by several very broad training perturbations:
`Sin3a`, `Hnrnpu`, `Thap11`, `Zbtb7a`, `Brd4`, `Psmc1`, `Psmb4`, `Smarcc2`,
`Tnpo3`, `Elp1`, `Gfpt1`, `Chd4`, and `Tsc2`; it was mildly induced by `Yy1`.
Those perturbations have large focal signatures, for example `Sin3a` 1,433
DEGs, `Hnrnpu` 733, `Zbtb7a` 841, `Yy1` 720, `Psmb4` 742, and `Tnpo3` 618.
They show that the `Gpr162` transcript can move inside stressed or
chromatin/proteasome-driven expression states, but they are upstream global
regulators rather than mechanistic analogs of a `Gpr162` receptor knockout.

## Target-specific decision

### `Gpr162`

`Gpr162` encodes an orphan class-A/rhodopsin-family GPCR. NCBI Gene/Alliance
annotate mouse `Gpr162` as predicted to enable GPCR activity and to be expressed
in the nervous system, gut, and neural retina, and the Caruso studies place
GPR162 in mouse hippocampal and hypothalamic/feeding circuits. That supports
expression in neurons but not a specific strong effector program in thalamic
Prkcd/Grin2c glutamatergic cells.

I considered three possible ways a `Gpr162` perturbation could have produced a
nonzero count:

1. A ciliary GPCR/Hedgehog/cAMP route. This was the most concrete GPCR analogy,
   but it argues for a small or absent focal response. The best characterized
   visible receptor, `Gpr161`, had `n_degs = 0` in the focal group; `Smo`,
   `Ptch1`, `Ptch2`, `Gli1`, `Gli2`, `Adcy3`, `Gnas`, `Bbs5`, `Cplane1`,
   `Cspp1`, `Ift43`, `Ift88`, `Ift81`, `Cep290`, `Kif3b`, `Rpgrip1l`, and
   `Ttc21b` also had zero focal DEGs. `Gnao1`, `Prkaca`, and `Prkar1a` each had
   a count of 1 driven by their own knocked-down transcript, not a broad
   downstream module. The causal transfer chain therefore fails at propagation:
   ciliary GPCR/Hedgehog machinery is visible enough to query in the screen, but
   acute partial loss in recovered postnatal neurons did not propagate to a
   robust snRNA state.
2. A CART/glucose-homeostasis route. Lindqvist et al. established GPR162 as a
   beta-cell CART receptor, and Caruso et al. tied `Gpr162` expression to
   feeding and glucose phenotypes. The focal assay contains thalamic
   glutamatergic neurons rather than pancreatic beta cells or a hypothalamic
   feeding nucleus, and the training file has no obvious focal analog in which
   this receptor-ligand axis created a broad expression signature. I therefore
   treated this as an external weak prior for function, not evidence for
   nonzero focal DEGs.
3. A STING/interferon route. Long et al. showed that GPR162 overexpression can
   activate a STING-dependent DNA-damage response in irradiated tumor models.
   The held-out experiment is loss-of-function in unirradiated NeuN+ nuclei; it
   lacks the overexpression, tumor, and radiation conditions needed for
   same-direction transfer. This route is not endpoint-bearing for the requested
   CRISPR contrast.

The most relevant observed perturbations are therefore all zero or
self-transcript-only singletons. I predicted `Gpr162` to land on the modal
zero-count class rather than assigning a one-gene effect, because no close
training comparator in `151 TH Prkcd Grin2c Glut` showed a downstream GPCR,
Hedgehog, ciliary, cAMP, or PKA transcriptional program, and the broad
perturbations that repress the `Gpr162` transcript are not good analogs for
removing the receptor.

Final point prediction: `Gpr162` -> `0` DEGs.

## Limits

The `Gpr162` biology is under-characterized. Its focal-cell expression level in
the unperturbed dataset was not directly available in these DE summaries, and
the held-out knockout might perturb non-transcriptional receptor signaling,
neuronal excitability, or a rare CART-responsive subpopulation without
producing any FDR-level bulk class signature. The useful within-dataset
comparators are mostly adjacent GPCR/cAMP/Hedgehog/ciliary genes rather than
obligate members of the same receptor complex, so they can calibrate the likely
DEG breadth only weakly. The pancreatic beta-cell and tumor STING studies
support molecular activities of GPR162 in other settings but require different
cell types or stress exposures and therefore were not transferred as strong
same-endpoint evidence.
