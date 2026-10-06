# DEG-count prediction trace

## Question and resolved ambiguities

The requested held-out target list contains one perturbation, `Trem2`. I interpreted
`n_degs` as the number of measured genes with `pvals_adj < 0.05` in the
`151 TH Prkcd Grin2c Glut` cell group for a mouse gene knockout, where the log
fold-change convention is perturbed over matched control. The count is therefore
an assay-specific breadth endpoint, not a direct score of biological importance.

`Trem2` itself was absent from the training count CSV and absent from the
model-visible DE parquet by design, so there is no direct Trem2 profile to read.
I treated zero as a valid prediction meaning that no measured transcript is
expected to pass the focal cell group's FDR 0.05 threshold.

## Sources used

- Focal endpoint counts:
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`
- Differential-expression parquet:
  `[local file: training_de_all_cell_groups.parquet]`
- Requested target manifest:
  `[local file: 244_Trem2.csv]`
- Distributed Agents same-experiment corpus:
  `perturbai-july-260713-sourceguard-1773-v1`
- Distributed Agents runtime profile comparison over the run-local parquet, using
  `gene_target` as the entity, `names` as features, `logfoldchanges` as signed
  values, `pvals_adj < 0.05` as the significance flag, and
  `group_name == "151 TH Prkcd Grin2c Glut"` as the context.
- PubMed-indexed literature for TREM2 and microglial biology.

## Computational checks over the training data

The training focal endpoint was zero-inflated: 1205 of 1674 non-held-out
perturbations had no FDR-significant gene in `151 TH Prkcd Grin2c Glut`, and
469 had at least one. That prior alone is insufficient for Trem2, so I
intersected the endpoint CSV and the focal rows of the parquet with genes whose
biology is closest to the Trem2 axis:

```python
import pyarrow.compute as pc
import pyarrow.dataset as ds

targets = [
    "Abca7", "Axl", "C3", "Ccr2", "Cd47", "Csf1r",
    "Cx3cr1", "Cxcr4", "Irf8", "Mertk", "P2ry12", "Pld3", "Spi1",
]

dataset = ds.dataset(TRAINING_DE_PARQUET, format="parquet")
filt = (
    (pc.field("group_name") == "151 TH Prkcd Grin2c Glut")
    & pc.field("gene_target").isin(targets)
)
table = dataset.to_table(
    columns=[
        "gene_target", "names", "logfoldchanges", "pvals_adj",
        "n_pert_matched", "n_ctrl_matched",
    ],
    filter=filt,
)
```

The exact focal counts and expression surfaces for the biologically relevant
comparators were:

| training target | focal `n_degs` | focal DE evidence | matched perturbed nuclei | why it was compared with Trem2 |
|---|---:|---|---:|---|
| `Csf1r` | 0 | no measured gene at FDR 0.05 | 146 | microglial survival and CSF1/IL34 receptor axis |
| `Cx3cr1` | 0 | no measured gene at FDR 0.05 | 258 | homeostatic microglial chemokine receptor |
| `P2ry12` | 0 | no measured gene at FDR 0.05 | 102 | homeostatic microglial purinergic receptor |
| `Axl` | 0 | no measured gene at FDR 0.05 | 198 | TAM/efferocytosis receptor in the phagocytic neighborhood |
| `Mertk` | 0 | no measured gene at FDR 0.05 | 121 | TAM/efferocytosis receptor in the phagocytic neighborhood |
| `Spi1` | 0 | no measured gene at FDR 0.05 | 178 | myeloid-lineage transcription factor |
| `Irf8` | 0 | no measured gene at FDR 0.05 | 203 | myeloid and microglial transcription factor |
| `Abca7` | 0 | no measured gene at FDR 0.05 | 213 | Alzheimer/phagocytic lipid-handling gene linked to microglia |
| `C3` | 0 | no measured gene at FDR 0.05 | 231 | complement component, a neuroimmune counterexample |
| `Ccr2` | 0 | no measured gene at FDR 0.05 | 170 | immune chemokine receptor counterexample |
| `Cd47` | 1 | only `Cd47` itself, log2FC -0.740, adjusted p = 3.40e-15 | 104 | phagocytic "don't eat me" signaling comparator |
| `Pld3` | 1 | only `Pld3` itself, log2FC -1.052, adjusted p = 2.24e-16 | 255 | lysosomal/AD-adjacent counterexample |

Thus the nearest represented immune, microglial, TAM/efferocytosis, phagocytic,
complement, and AD-axis perturbations did not produce a downstream focal
neuronal program. The two nonzero analogs had a single self-transcript hit,
which shows target-RNA depletion can be detected in this cell group but does not
argue for a broader state.

I also compared `Abca7`, `Axl`, `Cd47`, `Csf1r`, `Cx3cr1`, `Mertk`, `P2ry12`,
`Pld3`, and `Spi1` as a small candidate cohort using the full focal
log-fold-change vectors. Seven of the nine had no significant focal features;
the two remaining nodes had only one feature each. The cohort diagnostic showed
zero overlapping significant same-direction genes among these perturbations and
only weak overlap of the 250 most positive or negative ranked features. I used
this as evidence for joint flatness, not as a hidden positive module.

## Same-experiment corpus evidence

The Distributed Agents corpus had no direct `Trem2` entry, consistent with Trem2 being a
held-out target. It did have repeated same-experiment findings that are
mechanistically adjacent and directly constrain the prediction:

- Claim `claim:8bd7e3c8a73422ba8b45`, high confidence:
  represented microglial and neuroimmune receptor perturbations did not produce
  recurrent cell-autonomous neuronal nuclear transcriptional programs in this
  NeuN-positive screen. The contributing targets were `Axl`, `Csf1r`, `Cx3cr1`,
  `Mertk`, `P2ry12`, and `Spi1`.
- Claim `claim:f5f24d7e56937c869699`, moderate confidence:
  `Abca7`, phagocytic, and myeloid-lineage perturbations did not expose a shared
  neuronal program in the healthy NeuN-enriched screen, despite unrelated
  neuronal benchmark perturbations producing clear responses.
- Claim `claim:518cfce75e3613ae1c2b`, high confidence:
  the expected `Axl`/`Mertk` efferocytosis axis was not detectable as a shared
  neuronal transcriptional state after single-gene perturbation.
- `Csf1r:F002` specifically reported that `Cx3cr1`, `Spi1`, `Irf8`, and `Pdgfrb`
  were flat in Csf1r-matched neuronal groups, while `P2ry12` had only a
  borderline single-gene event outside the focal group; its caveat explicitly
  noted that `Trem2` and `Tyrobp` were unavailable and microglia themselves were
  not sampled.
- `P2ry12:F003` reported that other represented microglia-lineage receptors
  were likewise flat in neuronal groups, including `P2ry14`, `Cx3cr1`, `Csf1r`,
  `Ccr2`, `Axl`, and `Mertk`.

The candidate-set topology over `Abca7`, `Axl`, `Cd47`, `Csf1r`, `Cx3cr1`,
`Mertk`, `P2ry12`, `Pld3`, and `Spi1` formed one component, with 28 connected
pairs among 36 possible pairs. `Pld3` was only weakly connected in that graph,
so I kept it as a counterexample rather than a primary Trem2 analog.

## External biological rationale for Trem2

TREM2 is a lipid-sensing immunoreceptor whose canonical CNS role is in
microglia. It signals through TYROBP/DAP12 and SYK-family pathways to regulate
microglial survival, proliferation, phagocytosis, lipid handling, and
disease-associated microglial responses to amyloid, demyelination, or cell
damage rather than a basal postmitotic neuronal transcription factor program.
Key external support:

- Zhang et al. 2014, PMID 25186741, DOI 10.1523/JNEUROSCI.1860-14.2014,
  profiled purified mouse brain cell classes and cataloged cell-type-enriched
  expression across neurons, glia, vascular cells, and microglia.
- Butovsky et al. 2013, PMID 24316888, DOI 10.1038/nn.3599, defined a
  microglial molecular signature among CNS and immune cells.
- Poliani et al. 2015, PMID 25893602, DOI 10.1172/JCI77983, showed that
  `Trem2` loss impairs microglial expansion and transcriptional activation
  during aging and demyelination.
- Zheng et al. 2017, PMID 28077724, DOI 10.1523/JNEUROSCI.2459-16.2017,
  connected TREM2/DAP12 to microglial survival through the
  Akt/GSK3beta/beta-catenin pathway.
- Krasemann et al. 2017, PMID 28930663, DOI 10.1016/j.immuni.2017.08.008,
  identified a TREM2-APOE pathway driving a neurodegenerative microglial
  transcriptional phenotype.
- Nugent et al. 2020, PMID 31902528, DOI 10.1016/j.neuron.2019.12.007,
  showed that TREM2 regulates microglial cholesterol metabolism under chronic
  myelin phagocytic challenge.
- Wang et al. 2022, PMID 36306735, DOI 10.1016/j.cell.2022.09.033, placed TREM2
  upstream of SYK-dependent and -independent microglial responses to amyloid
  plaques.

Those mechanisms make Csf1r/Cx3cr1/P2ry12/Axl/Mertk/Spi1 better in-dataset
analogs than generic Alzheimer's or receptor targets: they share the microglial
lineage and phagocytic/neuroimmune axis whose cells were largely removed by
NeuN FACS. The represented analogs were flat in the exact focal neuronal group,
and the assay was a healthy P16-to-P37/44 acute mosaic CRISPR experiment rather
than aged amyloid, demyelination, injury, or purified microglia.

## Target-specific prediction

### Trem2

I predict **0 DEGs** for `Trem2` in `151 TH Prkcd Grin2c Glut`.

The zero/nonzero decision is driven primarily by the within-dataset evidence:
all strong represented microglial-lineage receptor and myeloid comparators
available in the focal group were at zero DEGs (`Csf1r`, `Cx3cr1`, `P2ry12`,
`Axl`, `Mertk`, `Spi1`, `Irf8`, `Abca7`, `C3`, `Ccr2`), while the only nearby
singletons (`Cd47`, `Pld3`) were self-transcript depletion events. The
same-experiment corpus specifically summarized this as flat neuronal surfaces
for microglial and neuroimmune receptors rather than a recurrent NeuN-positive
program.

The external biology decides that these zero analogs are the right direction for
`Trem2`: TREM2 is a microglial TYROBP/DAP12-associated receptor whose strongest
transcriptional outputs arise in microglia after amyloid, apoptotic-cell, or
myelin challenges. Those cells and contexts are absent from this focal neuronal
readout. Because `Tyrobp`, `Apoe`, `Syk`, and `Fcer1g` were not represented in
the focal training CSV, I could not calibrate the exact TREM2-DAP12 branch
directly and relied on the broader Csf1r/Cx3cr1/P2ry12/Axl/Mertk/Spi1 panel.
That limitation argues against assigning a finely tuned small positive count;
it does not supply evidence for a broad focal response.

## Limits and extrapolations

- This prediction extrapolates to a held-out perturbation with no Trem2
  expression signature in the supplied parquet.
- The strongest TREM2 biology is in microglia, but the experiment profiled
  NeuN-positive nuclei and the target was knocked out sparsely and acutely in
  juvenile healthy brain. A Trem2 effect in amyloid, demyelination, aging,
  injury, macrophages, or sorted microglia would not be expected to appear here.
- `Tyrobp`, `Apoe`, `Syk`, `Lyn`, and `Fcer1g` were not available as focal
  training-count comparators, so the closest represented analogs are
  lineage/pathway neighbors rather than the receptor-adapter complex itself.
- The whole-vector profile similarities among flat perturbations are weakly
  interpretable because they compare subthreshold rank noise; the decisive
  within-dataset observation is the absence of significant downstream genes in
  many microglial/neuroimmune comparators, not a positive shared signature.
