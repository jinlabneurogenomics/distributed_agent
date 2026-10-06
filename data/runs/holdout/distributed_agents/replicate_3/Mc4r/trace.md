# Reasoning trace for `151 TH Prkcd Grin2c Glut`

## Question and interpretation

The held-out readout is the number of measured genes with `pvals_adj < 0.05` after an acute, sparse, AAV-delivered CRISPR loss-of-function perturbation in the focal Allen taxonomy group `151 TH Prkcd Grin2c Glut`.  The run manifest contains one held-out target:

| target_name |
|---|
| Mc4r |

I interpreted `n_degs` literally as the assay endpoint for the focal group, including the possibility that the perturbed target transcript itself can contribute one DEG if it is detectably reduced.  I did not interpret it as a phenotype-size score, viability score, or a germline/null knockout severity score.

## Sources used

- Input endpoint counts: `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
- Input per-gene DE table: `[local file: training_de_all_cell_groups.parquet]`; I filtered this to `group_name == "151 TH Prkcd Grin2c Glut"` for the observed non-held-out targets.
- Requested held-out target manifest: `[local file: 135_Mc4r.csv]`.
- Distributed Agents same-experiment corpus MCP, release `perturbai-july-260713-sourceguard-1773-v1`.  `target_context("Mc4r")` returned no same-experiment claims, findings, or explicit references, so the corpus did not supply a direct `Mc4r` analog.
- Public melanocortin biology:
  - Balthasar et al. 2005, Cell, DOI `10.1016/j.cell.2005.08.035`: re-expression of MC4R in `Sim1` PVH/amygdala neurons rescues hyperphagia, separating feeding and energy-expenditure arms of melanocortin signaling.
  - Ghamari-Langroudi et al. 2010, PNAS, DOI `10.1073/pnas.1016785108`, PMID `21169216`: PVH MC4R neurons are second-order melanocortin neurons regulated by alpha-MSH, NPY, leptin, and constitutive MC4R activity.
  - Shah et al. 2014, PNAS, DOI `10.1073/pnas.1407843111`, PMID `25157144`: the feeding-relevant MC4R neurons are `SIM1+` PVH glutamatergic neurons connected to the parabrachial nucleus.
  - Fenselau et al. 2016, Nature Neuroscience, DOI `10.1038/nn.4442`, PMID `27869800`: ARC glutamatergic input converges on PVH MC4R satiety neurons and is potentiated by POMC-derived alpha-MSH.
  - Zhang et al. 2024, Nature, DOI `10.1038/s41586-024-08164-8`, PMID `39506113`: AgRP/NPY and POMC/alpha-MSH signals compete to control cAMP in PVH MC4R neurons during satiation.
  - Lein et al. 2006, Nature, DOI `10.1038/nature05453`, PMID `17151600`: Allen Mouse Brain Atlas in-situ expression resource used as background for the restricted adult-brain distribution of receptor transcripts such as `Mc4r`.

## Computations over the training data

1. Loaded the held-out manifest and confirmed there was exactly one requested target, `Mc4r`.
2. Summarized the focal-cell training counts.  There were 1,674 observed training perturbations; the response distribution was highly zero-inflated:

| statistic | `n_degs` |
|---|---:|
| median | 0 |
| 75th percentile | 1 |
| 90th percentile | 2 |
| 95th percentile | 18 |
| maximum | 2677 |
| perturbations with `n_degs > 0` | 469 / 1674 |

3. Scanned the focal rows of the parquet for receptor and MC4R-pathway analogs.  Each observed perturbation has 17,259 measured genes in this cell group.  I sorted each profile by adjusted p-value and counted genes at `pvals_adj < 0.05` to verify agreement with the supplied count table.
4. Queried a runtime profile-neighbor view for the observed anchors `Mc1r`, `Mc2r`, `Agrp`, `Lepr`, `Gnas`, `Adcy3`, `Npy1r`, and `Htr2c`.  Because the profiles for these anchors were almost all zero-DEG, their top-tail overlaps produced a large and noisy neighbor union rather than a compact broad-response module; I therefore used the neighbor pass only as a sanity check that these perturbations were not hidden members of a high-DEG program.

The mechanistic analog and counterexample set was:

| training perturbation | focal `n_degs` | use in reasoning |
|---|---:|---|
| `Mc1r` | 0 | Melanocortin receptor paralog in training; no significant genes in the focal group. |
| `Mc2r` | 0 | Melanocortin receptor paralog in training; no significant genes in the focal group. |
| `Agrp` | 0 | Endogenous MC3R/MC4R inverse agonist/antagonist from arcuate neurons; silent when perturbed in this focal thalamic population. |
| `Lepr` | 0 | Upstream metabolic-state receptor that controls arcuate melanocortin tone; silent in the focal group. |
| `Npy1r`, `Npy2r`, `Npy5r` | 0, 0, 0 | NPY receptor perturbations adjacent to the AgRP/NPY arm; all zero. |
| `Htr2c` | 0 | Serotonin receptor upstream of arcuate POMC/melanocortin signaling; zero. |
| `Gnas` | 0 | Gs alpha subunit linking MC4R to cAMP; zero. |
| `Adcy1`, `Adcy3`, `Adcy5` | 0, 0, 0 | cAMP effectors downstream of Gs-coupled receptors; all zero.  `Adcy3` itself had the smallest adjusted p-value in its own profile but was still subthreshold, `log2FC = -0.5689`, `p_adj = 0.1123`. |
| `Gpr156`, `Gpr161`, `Gpr179`, `Gpr45`, `Gprc5b` | 0 each | Other observed GPCR perturbations in the same assay; zero. |
| `Gpr158`, `Gprasp2` | 1 each | GPCR/GPCR-associated counterexamples showing that receptor loci can yield only a target-proximal DEG; `Gpr158`'s lone DEG was its own transcript, `log2FC = -0.9911`, `p_adj = 3.39e-26`. |
| `Ntrk2` | 3 | Receptor counterexample with an expressed target transcript and only two additional significant genes, not a broad state shift. |
| `Fto` | 7 | Obesity-associated but mechanistically distant RNA-demethylase perturbation; a poor analog for acute loss of a lowly expressed neuropeptide GPCR. |

## Target-specific rationale

### `Mc4r`

`Mc4r` encodes a Gs-coupled melanocortin GPCR.  Its best-established central role is in energy balance: arcuate POMC neurons provide alpha-MSH agonist tone and AgRP/NPY neurons provide antagonistic or inverse-agonist tone onto MC4R-expressing neurons, especially PVH `SIM1+` glutamatergic satiety neurons.  Those data make `Agrp`, `Lepr`, `Htr2c`, `Npy*` receptors, `Gnas`, and adenylyl cyclases biologically relevant controls for the same ligand/cAMP axis, while also making it clear that most canonical MC4R biology is hypothalamic PVH/arcuate biology rather than a generic effect in thalamic `Prkcd`/`Grin2c` glutamatergic neurons.

The within-dataset evidence points to no detectable transcriptional response in this focal group:

- The two available melanocortin receptor paralogs, `Mc1r` and `Mc2r`, both had `n_degs = 0`.
- The MC4R-adjacent ligand and metabolic regulators present in training were uniformly zero: `Agrp = 0`, `Lepr = 0`, `Npy1r = 0`, `Npy2r = 0`, `Npy5r = 0`, and `Htr2c = 0`.
- Downstream cAMP signaling perturbations were also zero in this endpoint: `Gnas = 0`, `Adcy1 = 0`, `Adcy3 = 0`, and `Adcy5 = 0`.
- Broader GPCR perturbations in the assay were overwhelmingly silent in this focal group.  In the receptor comparison set I inspected, 36 of 38 GPCR/neuropeptide-receptor perturbations had `n_degs = 0`, and the two nonzero profiles each had only one DEG.

I considered assigning `1` on the possibility that the target transcript itself would be significantly depleted, as happened for `Gpr158`.  I rejected that because the `Adcy3` profile shows that even a clear receptor-pathway transcript can be reduced without passing FDR in this assay, and MC4R is not expected to be a high, canonical marker of the `151 TH Prkcd Grin2c Glut` thalamic population.  I also considered the obesity-associated `Fto` response (`n_degs = 7`) but treated it as a poor counterexample: `Fto` is a nuclear RNA-modification enzyme rather than a sparse cell-surface satiety receptor whose acute, cell-autonomous loss only matters in MC4R-expressing postsynaptic neurons.

Predicted `n_degs`: **0**.

## Limits and extrapolation

- The requested `Mc4r` perturbation was fully held out, so the exact target knockdown, guide performance, perturbed-cell count, and expression signature in this cell group were unavailable.
- The same-experiment Distributed Agents corpus had no `Mc4r` node; external biology therefore supplied the pathway interpretation, while the actual response calibration came from the training DE table.
- `Mc3r`, `Mc5r`, `Pomc`, and `Sim1` were not available as focal training perturbations, leaving `Mc1r`/`Mc2r` and the `Agrp`/`Lepr`/cAMP neighborhood as imperfect analogs.
- A sparse CRISPR receptor knockout can produce an electrophysiological effect without a stable snRNA-seq differential-expression signature.  Conversely, a low count could arise from the target mRNA alone if the transcript is expressed and efficiently downregulated.
- The cell label identifies a broad thalamic glutamatergic group; MC4R biology is strongest in hypothalamic PVH and connected feeding circuits.  The prediction extrapolates that this off-canonical cell group has little active MC4R signaling during the postnatal AAV experiment.
