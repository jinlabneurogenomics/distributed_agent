# DEG-count prediction trace

## Question and resolved ambiguities

The requested target set contains one held-out perturbation:

| target_name | prediction |
|---|---:|
| Notch3 | held out; predict `n_degs` in `151 TH Prkcd Grin2c Glut` |

I interpreted `n_degs` exactly as the training-count endpoint: the number of measured genes in thalamic `151 TH Prkcd Grin2c Glut` nuclei with `pvals_adj < 0.05` for a perturbation versus matched non-targeting controls. A prediction of `0` means that no measured gene is expected to pass the same Benjamini-Hochberg Wilcoxon threshold. The held-out `Notch3` rows are absent from both the training endpoint CSV and the differential-expression Parquet, so every numerical comparison below uses only non-held-out perturbations.

This is a scalar count task rather than a ranking task. The run-local `dataset.perturbseq_features`, bounded predictive graph review, and ordering-validation tools were unavailable because there is no explicit ranked or partially ranked supervision. I therefore queried the declared focal-cell Parquet rows directly and used external Notch biology only to decide which measured training perturbations are appropriate analogs or counterexamples.

## Sources used

### Dataset-local sources

* Declared differential-expression Parquet:
  `training differential-expression dataset`.
* Declared focal training counts:
  `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
* Declared held-out target manifest:
  `single-target request for Notch3`.
* Run-local measurement registry, task bindings, compact coverage, and capability manifest under `codex_runtime/pipeline`.
* The internal PerturbAI July corpus release `perturbai-july-260713-sourceguard-1773-v1`; I used `corpus.calibration` to verify the corpus units and `corpus.findings` only for bounded same-experiment report summaries around `Adam10`, `Mib1`, `Notch1`, and `Notch2`. These reports are a packaged interpretation of the same Perturb-seq experiment, not an independent replicate.

### External mechanism sources

* PubMed. Kopan and Ilagan 2009, DOI `10.1016/j.cell.2009.03.045`, PMID `19379690`: canonical Notch signaling releases a receptor intracellular domain after ligand-triggered ADAM and gamma-secretase cleavage, then signals through CSL/RBPJ and Mastermind coactivators.
* PubMed. Itoh et al. 2003, DOI `10.1016/s1534-5807(02)00409-4`, PMID `12530964`: Mind bomb/Mib is a RING ubiquitin ligase that promotes Delta endocytosis in the signal-sending cell and is needed for efficient activation of Notch in neighboring cells.
* PubMed. Domenga et al. 2004, DOI `10.1101/gad.308904`, PMID `15545631`: mouse `Notch3` is required cell-autonomously for arterial vascular smooth-muscle-cell identity and maturation.
* PubMed. Joutel 2010, DOI `10.1002/bies.201000093`, PMID `20967782`: NOTCH3 is a CADASIL small-vessel-disease gene and is primarily expressed in smooth muscle cells of small arteries and in brain-capillary pericytes.

## Quantitative checks over the training data

I first checked all represented obvious Notch-pathway labels in the focal endpoint CSV. The focal `n_degs` values were:

| training target | relationship to Notch3 | `151 TH Prkcd Grin2c Glut` `n_degs` |
|---|---|---:|
| `Notch1` | paralogous Notch receptor | 0 |
| `Notch2` | paralogous Notch receptor | 0 |
| `Notch4` | paralogous Notch receptor | 0 |
| `Adam10` | S2 Notch receptor protease; APP/synaptic-substrate sheddase | 0 |
| `Psen1` | gamma-secretase catalytic subunit used for NICD release | 0 |
| `Dll1` | Delta-like ligand | 0 |
| `Mib1` | Delta/Jagged ligand E3 ligase; Notch-pathway counterexample | 27 |

The focal Parquet confirmed that these were measured contrasts rather than absent entries. Each of the seven training targets above had 17,259 measured focal rows and a shared matched-control pool of 23,679 nuclei. Their recovered perturbed nuclei ranged from 69 for `Adam10` and 89 for `Psen1` to 324 for `Notch4`; `Notch3` itself was not present as a `gene_target`, consistent with the held-out design.

For `Notch1`, `Notch2`, `Notch4`, `Adam10`, `Psen1`, and `Dll1`, the least adjusted focal p-values were:

| target | minimum focal `pvals_adj` |
|---|---:|
| `Adam10` | 1.000 |
| `Dll1` | 0.678 |
| `Notch1` | 1.000 |
| `Notch2` | 1.000 |
| `Notch4` | 0.490 |
| `Psen1` | 1.000 |

I also checked canonical Notch-output and proneural measured genes in the focal rows: `Hes1`, `Hes5`, `Hey1`, `Hey2`, `Heyl`, `Nrarp`, `Dtx1`, `Rbpj`, `Maml1`, `Maml2`, `Maml3`, `Ascl1`, `Neurog2`, `Neurod1`, and `Neurod2`. All had `pvals_adj = 1.0` after the focal `Notch1`, `Notch2`, `Notch4`, `Adam10`, `Psen1`, `Dll1`, and `Mib1` perturbations. Thus the zero counts for the receptor/protease analogs reflect a flat focal Notch transcriptional surface, not a broad subthreshold HES/HEY program.

`Mib1` is the main Notch-related nonzero counterexample. Its 27 focal FDR<0.05 genes were dominated by an up-regulated sterol/cholesterol module, including `Insig1`, `Dhcr24`, `Fdft1`, `Ldlr`, `Msmo1`, `Hmgcs1`, `Hmgcr`, `Cyp51`, `Lss`, `Hsd17b7`, `Idi1`, `Sqle`, `Nsdhl`, `Srebf2`, `Dhcr7`, `Fdps`, `Mvd`, `Sc5d`, `Mvk`, and `Fads1`. The internal July corpus likewise summarized that Mib1 loss produced an SREBF2-like sterol program while the represented `Dll1`, `Notch1`, `Notch2`, `Notch4`, `Adam10`, and `Psen1` receptor/processing perturbations did not converge with that program. I therefore treated `Mib1` as evidence that the assay could detect a Notch-pathway regulator with a small focal transcriptome, but not as a direct receptor-loss phenocopy.

## Target-specific prediction

### Notch3 -> `0`

`Notch3` is a Notch receptor and, in canonical signal-receiving cells, should use the same basic sequence as the other receptors: ligand engagement, ADAM-family S2 cleavage, gamma-secretase/S3 cleavage, nuclear NICD entry, and RBPJ/MAML-dependent transcription of HES/HEY-class genes. In the declared focal data, perturbing the three represented receptor paralogs gave the strongest local analog:

* `Notch1`: `n_degs = 0`.
* `Notch2`: `n_degs = 0`.
* `Notch4`: `n_degs = 0`.

The shared processing components point in the same direction:

* `Adam10`: `n_degs = 0`, no downstream FDR<0.05 focal genes.
* `Psen1`: `n_degs = 0`, no downstream FDR<0.05 focal genes.
* `Dll1`: `n_degs = 0`, no downstream FDR<0.05 focal genes.

Those are the closest assay-matched counterfactuals available. If `151 TH Prkcd Grin2c Glut` neurons maintained an acute, tonic, canonical Notch transcriptional state at P37-P44, knocking out a receptor paralog or a shared cleavage step should have been able to lower HES/HEY/Nrarp/Dtx1-class RNA. The focal Parquet did not show that. The exact focal rows instead left every inspected canonical readout at adjusted p-value 1.0.

The causal transfer chain further reduces the expected `Notch3` effect. The intervention is sparse postnatal neuronal CRISPR loss of function. A `Notch3` indel can remove a Notch-family receptor, but NOTCH3 biology in brain is enriched in vascular smooth muscle cells and capillary pericytes rather than NeuN-positive thalamic neurons. The major established Notch3 consequence therefore occurs in vascular mural cells, which this whole-brain NeuN-enriched screen explicitly under-samples. The expected propagation route into recovered `151 TH Prkcd Grin2c Glut` nuclei would require tonic Notch3 receptor signaling inside these postmitotic thalamic neurons; the paralog, protease, and ligand perturbations argue that this link is weak or absent at the steady-state 3-4 week readout.

`Mib1` is a biologically relevant challenge because it lies upstream of Notch receptor activation by promoting Delta/Jagged ligand endocytosis. It does not overturn the zero prediction. Its focal phenotype is a 27-gene SREBF2/sterol signature, and the internal same-experiment reports call this response uncoupled from canonical Notch transcription: receptor, ligand, ADAM10, and presenilin perturbations did not reproduce it and Mib1 did not regulate `Hes1`, `Hes5`, `Hey1`, `Hey2`, `Heyl`, `Nrarp`, `Dtx1`, `Rbpj`, or `Maml1-3`. Mib1 therefore supports an endpoint-specific nonzero only for the ligand E3-ligase perturbation, not for a held-out `Notch3` receptor perturbation.

I predicted `0` rather than a very small positive count because the best same-receptor analogs are all exact zeroes at the requested FDR<0.05 threshold, the shared processing analogs are also exact zeroes, and the external Notch3-specific prior points away from the assayed NeuN-positive thalamic population. A one-gene stochastic hit remains possible in this assay, but the evidence places `Notch3` on the flat side of the training distribution.

## Limits and uncertainty

`Notch3` itself was completely held out, so there is no direct focal `Notch3` expression signature or exact recovered-cell count. The prediction transfers from receptor paralogs and shared Notch-processing perturbations, and paralogs can have receptor-specific ligands, expression domains, and noncanonical behavior. `Adam10` and `Psen1` have modest focal perturbed-cell recovery, so a tiny response could have fallen below Wilcoxon/BH power. The screen is also survivor-conditioned, measures steady-state nuclear RNA after 3-4 weeks rather than NICD protein, ligand endocytosis, vascular morphology, or pericyte function, and removes most non-neuronal cells where NOTCH3 biology is strongest. For these reasons the prediction is only a count for recovered `151 TH Prkcd Grin2c Glut` neuronal nuclei, not a claim that Notch3 loss is biologically inert.
