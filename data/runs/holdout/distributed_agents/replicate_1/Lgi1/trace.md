# Reasoning trace

## Question and endpoint

The requested prediction is a scalar held-out endpoint for one perturbation,
`Lgi1`, in `151 TH Prkcd Grin2c Glut` thalamic glutamatergic neurons. I
interpreted `n_degs` exactly as in the supplied training CSV: the count of
measured genes with Benjamini-Hochberg adjusted Wilcoxon `pvals_adj < 0.05` in
this focal cell group, including the perturbed target transcript if it passes
the threshold. The held-out `Lgi1` rows themselves are absent from both the
Parquet and the training-count CSV, so the endpoint is absent for `Lgi1` and
must be predicted from represented perturbations plus gene-function knowledge.

The focal endpoint is direct for non-held-out perturbations in
`151 TH Prkcd Grin2c Glut`, because
`151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` was generated from the
declared differential-expression Parquet using the same `pvals_adj < 0.05`
definition. The same-experiment Findings corpus was used only as a compact
interpretation layer over those same Perturb-seq measurements, not as
independent replication.

## Sources used

- Declared training DEG counts:
  `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
- Declared differential-expression Parquet:
  `training differential-expression dataset`.
- Requested-target manifest:
  `single-target request for Lgi1`.
- Run-local dataset portrait, task bindings, coverage, and capability
  manifests in `codex_runtime/pipeline`.
- Internal same-experiment corpus:
  `perturbai-july-260713-sourceguard-1773-v1`, especially the `Adam22`,
  `Dlg4`, `Gria1`, and `Nrxn1` Findings and the resolved `Adam22` Evidence and
  Reference records.
- External mechanism references from the packaged corpus and bounded PubMed
  lookup: Fukata et al. 2006, PubMed 16990550; Lovero et al. 2015, PubMed
  26178195; Fukata et al. 2010, DOI `10.1073/pnas.0914537107`, PubMed
  20133599; Fukata et al. 2021, DOI `10.1073/pnas.2022580118`, PubMed
  33397806; Cuhadar et al. 2024, DOI `10.1016/j.celrep.2024.114186`, PubMed
  38700985; Fukata et al. 2021 review, DOI
  `10.1016/j.neuropharm.2021.108628`, PubMed 34089731; Reactome, LGI-ADAM
  interactions, `R-HSA-5682910`.

## Computation over the supplied dataset

1. I read the requested-target CSV and found exactly one target, `Lgi1`.
2. I summarized the focal training-count CSV. It contains 1674 represented
   perturbations; its median and 75th percentile are 0 and 1 DEG, respectively,
   with 1205 zero-DEG targets and a small heavy tail driven by broad chromatin,
   RNA-processing, proteostasis, and mitochondrial hits.
3. I searched the training-count CSV for direct LGI1-pathway and synaptic
   comparators. `Adam22` is present, whereas the more specific ligand/paralog
   perturbations `Lgi2`, `Lgi3`, `Lgi4`, `Adam11`, and `Adam23` are not present
   as training targets. `Adam10` was present but was not used because it is an
   unrelated metalloprotease compared with the ADAM22/23 LGI receptors.
4. I sliced the declared Parquet to the focal cell group and a small set of
   mechanistically motivated comparators:

   ```python
   filt = (
       pc.field("group_name") == "151 TH Prkcd Grin2c Glut"
   ) & pc.field("gene_target").isin(targets)
   columns = [
       "names", "scores", "logfoldchanges", "pvals_adj",
       "gene_target", "n_pert_matched", "n_ctrl_matched",
   ]
   ```

   The slice was 500,511 measured-gene rows. I used it to verify which rows
   drove the count for each analog and whether there were near-threshold
   downstream transcriptional effects.

## Target-specific transfer: Lgi1

### Direct receptor analog: Adam22

`Lgi1` encodes a neuronal LGI-family extracellular ligand. Its best represented
training analog is `Adam22`, the postsynaptic receptor that binds LGI1 and links
the ligand to PSD-95/MAGUK, TARP/AMPAR, NMDA receptor, Kv1-channel, and
LRRTM4/neurexin synaptic nanoalignment machinery. Reactome curates the LGI-ADAM
interaction pathway, and the experimental literature places LGI1 immediately
upstream of ADAM22/ADAM23 rather than in a transcription-factor or chromatin
module: Fukata et al. identified ADAM22 as an LGI1 receptor regulating AMPA
receptor synaptic transmission; Fukata et al. 2010 showed that loss of LGI1 in
mice disrupts an LGI1-ADAM22/23 transsynaptic complex and causes epilepsy;
Lovero et al. 2015 and Fukata et al. 2021 tied LGI1-ADAM22-MAGUK to PSD-95 and
excitatory synapse maturation and alignment.

The intervention chain for transfer is:

`Lgi1` CRISPR loss -> less secreted or surface-trafficked LGI1 ligand from the
edited neuron -> weaker ADAM22/23 LGI occupancy and MAGUK-coupled AMPAR/Kv1
organization -> altered local synaptic function and excitability -> the
surviving edited thalamic nuclei assayed 3-4 weeks later -> Wilcoxon DEG count.

On that chain, the primary direct consequences are extracellular protein-complex
and electrophysiological effects, not known broad transcriptional control.
Moreover, ligand loss is likely at least as buffered as receptor loss in this
sparse mosaic AAV-CRISPR setting: an `Adam22`-edited cell loses the receptor on
that cell, while an `Lgi1`-edited cell could still see LGI1 supplied by nearby
unedited neurons.

In the training data, `Adam22` had exactly 1 focal-class DEG:

- `Adam22`: `n_degs = 1`, 115 perturbed nuclei versus 23679 controls.
- The sole FDR < 0.05 row was the target transcript itself:
  `Adam22` score `-7.504`, log2FC `-0.550`,
  `pvals_adj = 1.07e-09`.
- There were 0 non-self downstream genes in this cell group even at
  FDR < 0.10.
- The Adam22 corpus report explicitly queried the expected AMPAR/MAGUK/TARP,
  Kv1, immediate-early, and ISR/UPR marker sets across Adam22-measured groups
  and found no Adam22-driven recurrent RNA module; its unbiased continuous
  neighbor search had only tiny cosine similarities, with the best positive
  neighbor at 0.0367.

Thus `Adam22` is strong same-experiment evidence that perturbing the LGI1
receptor complex does not make a broad, cell-autonomous nuclear RNA state in
the harvested nuclei. It is also the strongest reason not to extrapolate from
LGI1's epilepsy biology to dozens of DEGs in this assay.

### Synaptic protein counterexamples

I used represented postsynaptic and presynaptic synaptic genes as
counterexamples to a generic "famous synaptic disease gene gives a large DEG
footprint" rule.

In the focal cell group:

| training perturbation | focal `n_degs` | expression-pattern evidence |
|---|---:|---|
| `Dlg4` | 1 | only `Dlg4` itself was significant, log2FC `-0.444`, FDR `1.15e-08` |
| `Gria1` | 0 | no FDR < 0.05 rows; strongest non-self adjusted p-value was 0.246 |
| `Gria2` | 0 | no FDR < 0.05 rows |
| `Gria3` | 0 | no FDR < 0.05 rows |
| `Cacng2` | 0 | no FDR < 0.05 rows |
| `Cacng3` | 0 | no FDR < 0.05 rows |
| `Nrxn1` | 1 | only `Nrxn1` itself was significant, FDR `2.67e-23` |
| `Nrxn2` | 0 | no FDR < 0.05 rows |
| `Nrxn3` | 0 | no FDR < 0.05 rows |
| `Nlgn3` | 1 | only `Nlgn3` itself was significant, FDR `4.79e-11` |
| `Syngap1` | 0 | no FDR < 0.05 rows |
| `Shank2` | 0 | no FDR < 0.05 rows |
| `Shank3` | 2 | one self row plus one non-self row, `Uba5`, FDR `0.029` |
| `Homer2` | 0 | no FDR < 0.05 rows |
| `Magi2` | 0 | no FDR < 0.05 rows |
| `Kcna1` | 0 | no FDR < 0.05 rows |
| `Kcna2` | 0 | no FDR < 0.05 rows |
| `Kcnq2` | 1 | only `Kcnq2` itself was significant, FDR `2.12e-28` |
| `Kcnq3` | 1 | only `Kcnq3` itself was significant, FDR `0.0072` |
| `Sv2a` | 1 | only `Sv2a` itself was significant, FDR `1.86e-38` |
| `Stx1b` | 0 | no FDR < 0.05 rows |

These genes are not equally close to LGI1 mechanistically: `Dlg4`, `Gria1-3`,
and `Cacng2` sit in the postsynaptic AMPAR/MAGUK neighborhood; `Nrxn1-3` and
`Nlgn3` represent trans-synaptic adhesion; `Kcna1/2` represent the presynaptic
Kv1 axis affected by the LGI1/ADAM complex; `Kcnq2/3`, `Sv2a`, `Stx1b`,
`Syngap1`, and `Shank` genes are broader epilepsy or synaptic-localization
controls. The useful fact is their shared endpoint behavior: nearly all are
0- or 1-DEG perturbations in `151 TH Prkcd Grin2c Glut`, usually with any count
coming solely from the edited transcript. Dlg4 and Gria1 corpus Findings report
the same qualitative pattern across neuronal groups: core postsynaptic AMPAR
scaffold perturbations were mostly transcriptionally flat despite their
well-established synaptic functions.

`Grin1` is the main local counterexample. It is another glutamatergic receptor
gene and produced 89 focal DEGs, including `Scg2`, `Stmn4`, `Kctd16`, `Gpm6a`,
and `Dync1li2`. I did not transfer this larger count to `Lgi1` because direct
NMDAR disruption removes an ionotropic Ca2+-coupled receptor whose activity can
drive nuclear immediate-early transcription, whereas LGI1 acts primarily through
extracellular ADAM22/23 scaffolding of AMPAR/Kv1/MAGUK complexes. The low counts
for `Adam22`, AMPAR subunits, TARPs, and `Dlg4` are the closer test of LGI1's
causal neighborhood.

### Final zero/nonzero and count estimate

I predict that `Lgi1` will not cause any robust non-self transcriptional DEG in
this cell class. The acute perturbation affects a secreted synaptic ligand;
its direct consequence should be altered LGI1-ADAM22/23 complex function and
synaptic physiology, but `Adam22` loss in the same Perturb-seq experiment was
self-only in the focal class and flat across expected AMPAR/MAGUK/TARP, Kv1,
activity, and stress modules. Mosaic sparse editing should further buffer
ligand loss through extracellular LGI1 supplied from neighboring unedited cells.

I nevertheless used a point prediction of `1`, not `0`, because the endpoint
counts self-target RNA when significant. `Lgi1` was in the measured-gene matrix
for the focal Parquet slice, and in the analog set, well expressed neuronal
surface/synaptic targets often gave exactly one FDR-significant row through the
edited transcript itself: `Adam22`, `Dlg4`, `Nrxn1`, `Nlgn3`, `Kcnq2`, `Kcnq3`,
and `Sv2a` were all self-only in this focal group. This is a stronger fit to
`Lgi1` than either the zero-DEG cases with no detectable self-depletion or the
rare broader receptor case `Grin1`.

## Limits and uncertainty

The largest uncertainty is that the closest ligand and receptor perturbations
were held out or absent: `Lgi1` itself was held out, and `Lgi2`, `Lgi3`, `Lgi4`,
`Adam11`, and `Adam23` were not represented as training `gene_target` values.
`Adam22` is an excellent protein-complex analog but is not identical to ligand
loss, because ADAM22 is cell-autonomous and membrane anchored whereas LGI1 is
secreted. That difference biases the prediction toward fewer downstream DEGs
for `Lgi1`, but it does not by itself tell whether the `Lgi1` transcript will
cross FDR 0.05.

The prediction also depends on target-transcript detectability in the focal
thalamic neurons. The Parquet confirms that `Lgi1` is a measured row in this
cell group, but raw baseline expression is absent from the declared inputs.
Therefore the single predicted DEG is a self-transcript expectation, not
evidence for a downstream cell-state response. If `Lgi1` expression or gRNA-
induced nonsense-mediated decay were weaker than expected in this focal class,
the true count could be 0; if sparse LGI1 depletion unexpectedly crossed a
network excitability threshold, the true count could exceed 1. The represented
LGI1-ADAM22/AMPAR/Kv1 neighborhood makes the latter less likely than a 0-1 DEG
outcome.

