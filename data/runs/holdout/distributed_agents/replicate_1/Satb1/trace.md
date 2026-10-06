# Prediction target

The run asks for one held-out perturbation, `Satb1`, and the endpoint is a direct count: the number of measured genes in `151 TH Prkcd Grin2c Glut` cells whose Wilcoxon differential-expression `pvals_adj` is below 0.05 after sparse P16 AAV-CRISPR loss of function and P37-P44 snRNA-seq recovery.

I treated `151 TH Prkcd Grin2c Glut` as the exact focal thalamic glutamatergic class described in the task, not as tyrosine-hydroxylase positive neurons. `Satb1` was completely held out as a perturbation, so neither its focal DEG count nor its expression signature was present in the supplied training inputs. The declared endpoint is directly observed for the 1,674 non-held-out perturbations in `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`, and the expression signatures of those perturbations are directly observed in `training_de_all_cell_groups.parquet`; the held-out `Satb1` endpoint itself is absent and has to be inferred.

# Sources

- Declared input count table: `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
- Declared input differential-expression table: `training differential-expression dataset`.
- Requested-target manifest: `single-target request for Satb1`.
- Run-local task metadata: `task_bindings.json`, `coverage.json`, `capabilities.json`, and `measurement_registry.json`.
- Internal same-experiment corpus: `perturbai-july-260713-sourceguard-1773-v1`; I used its bounded Findings and Evidence/Reference records for visible analog perturbations `Satb2`, `Bcl11b`, and `Tcf7l2`.
- External literature from PubMed:
  - Denaxa et al. 2012, Cell Reports, doi:10.1016/j.celrep.2012.10.003.
  - Close et al. 2012, Journal of Neuroscience, doi:10.1523/JNEUROSCI.3583-12.2012.
  - Narboux-Neme et al. 2012, Journal of Neuroscience, doi:10.1523/JNEUROSCI.6068-11.2012.
  - Gongrich et al. 2020, Journal of Cell Biology, doi:10.1083/jcb.201905002.
  - Huang et al. 2011, Neuroscience Research, doi:10.1016/j.neures.2011.05.015.
  - Alcamo et al. 2008, Neuron, doi:10.1016/j.neuron.2007.12.012.
  - Britanova et al. 2008, Neuron, doi:10.1016/j.neuron.2007.12.028.
  - Srinivasan et al. 2012, PNAS, doi:10.1073/pnas.1216793109.

# Computation over the training inputs

I first calibrated the focal response scale from the training count CSV. In this cell group the endpoint is very zero-inflated: 1,205 of 1,674 training perturbations had `n_degs = 0`; the median was 0, the 75th percentile was 1, the 90th percentile was 2, and only 5% exceeded 18 DEGs. A prediction therefore needs evidence for a strong focal regulatory match before leaving the zero or one-to-two DEG regime.

For candidate analogs I filtered the Parquet to
`group_name == "151 TH Prkcd Grin2c Glut"` and to visible perturbations from the SATB/cortical-fate/chromatin-transcription-factor neighborhood, then counted FDR 0.05 rows and looked at their smallest adjusted p-values. The closest direct paralog and developmental fate-network comparators were flat or nearly flat in the focal cells:

| training perturbation | focal `n_degs` | focal expression-pattern evidence |
| --- | ---: | --- |
| `Satb2` | 0 | 236 perturbed nuclei; no FDR 0.05 genes; the smallest adjusted p-values in the focal Parquet were 1.0. |
| `Bcl11a` | 0 | 203 perturbed nuclei; no FDR 0.05 genes; smallest adjusted p-values were 1.0. |
| `Bcl11b` | 0 | 206 perturbed nuclei; no FDR 0.05 genes; smallest adjusted p-values were 1.0. |
| `Tbr1` | 0 | 288 perturbed nuclei; no FDR 0.05 genes in 151, although it is detectable in several cortical groups in the corpus. |
| `Sox5` | 2 | Only `Dgkh` and `Tnnt1` passed FDR 0.05. |
| `Cux1` | 0 | No focal FDR 0.05 genes. |
| `Cux2` | 1 | The only focal FDR 0.05 gene was `Cux2` itself. |
| `Foxp2` | 0 | No focal FDR 0.05 genes despite thalamic developmental associations. |
| `Pax6` | 0 | No focal FDR 0.05 genes. |
| `Neurod1` | 0 | No focal FDR 0.05 genes. |
| `Neurod2` | 0 | No focal FDR 0.05 genes. |
| `Rorb` | 0 | No focal FDR 0.05 genes. |

I also checked thalamic/chromatin counterexamples in the same table. `Tcf7l2` had 106 focal DEGs, `Ctnnb1` had 383, `Rora` had 278, and `Chd4` had 100, showing that the 151 class can produce a large corrected response when a perturbation hits a maintained thalamic Wnt/TCF state or a broadly active chromatin remodeler. Those are counterexamples to a blanket "all transcription factors are invisible" rule, but not positive Satb1 analogs: the internal July corpus describes `Tcf7l2` as a sharply 151-enriched thalamic terminal selector whose 151 signature down-regulated `Ramp3`, `Kcnc2`, `Pcsk2`, `Grin2b`, `Gabbr2`, `Gabra4`, `Gabra1`, `Prkcd`, `Pcp4`, and `Cpe`, and placed its strongest mechanistic convergence with `Ctnnb1`. SATB1 is not an obligate part of that TCF7L2/CTNNB1 thalamic module.

As one additional falsifier, I looked at `Satb1` as a measured gene in the focal Parquet for all training perturbations. It was significantly changed only downstream of high-burden general regulators such as `Cic`, `Tnpo3`, `Atxn1`, and `Tbcd`. That observation makes `Satb1` a responsive transcript in a few broad states, not evidence that perturbing `Satb1` itself should produce a broad focal 151 response.

# Target-specific rationale

## `Satb1`

The closest within-dataset anchor is `Satb2`, the other SATB-family special AT-rich DNA-binding chromatin organizer. The corpus record for the same July PerturbAI experiment reports that juvenile `Satb2` perturbation produced no corrected downstream response in any of the 23 recovered neuronal groups, and the exact focal count table gives `Satb2 = 0` in `151 TH Prkcd Grin2c Glut`. This is a strong same-platform analog because it shares the same DNA-binding/chromatin-organizer family, the same sparse P16 CRISPR modality, and a similarly developmental neuronal literature. It is also a warning against extrapolating from embryonic or conditional-null fate phenotypes to an acute postnatal baseline snRNA-seq DEG count.

The next biological neighbors reinforce the low-count expectation. `Bcl11a`, `Bcl11b`, `Tbr1`, `Cux1`, `Cux2`, `Sox5`, `Foxp2`, `Neurod1`, `Neurod2`, `Pax6`, and `Rorb` are visible transcription factors from cortical projection-neuron or neuronal-differentiation networks rather than perfect SATB1 interactors, but they test whether this class of developmental cell-fate regulators tends to give a latent 151 response. It mostly did not. In the focal class `Bcl11a`, `Bcl11b`, `Tbr1`, `Cux1`, `Foxp2`, `Neurod1`, `Neurod2`, `Pax6`, and `Rorb` all had zero DEGs; `Sox5` had two and `Cux2` had one. The internal `Bcl11b` report makes the same point at screen scale: `Bcl11a`, `Bcl11b`, and `Satb2` were flat across the postnatal neuronal DE surface, whereas only some related cortical determinants such as `Tbr1` had small cortical, not 151, signatures. Thus, the same-experiment expression evidence points to a buffered or wrong-context fate regulator, not to an active thalamic 151 regulator.

External knowledge further weakens a focal 151 transfer. SATB1 is a genome organizer/transcriptional regulator with clear neuronal functions, but the best mouse CNS perturbation evidence is in GABAergic interneurons: Denaxa et al. showed that Satb1 acts downstream of Lhx6 in MGE-derived cortical interneuron maturation; Close et al. showed that interneuron conditional Satb1 deletion impairs PV/SST interneuron terminal differentiation, connectivity, and survival; Narboux-Neme et al. linked reduced Satb1/Tbc1d5 locus expression to altered cortical GABAergic interneuron differentiation; and Gongrich et al. placed SATB1 in an ALK4/SMAD2 program for cortical somatostatin interneuron development. The focal cells here are postnatal thalamic glutamatergic neurons, so the causal chain breaks at cell context: acute partial Satb1 disruption in recovered Prkcd/Grin2c thalamic glutamatergic neurons is not expected to replay MGE-derived cortical interneuron differentiation or survival. Huang et al. did find Satb1-positive neurons in selected adult CNS areas, including smaller populations in centrolateral and parafascicular thalamic nuclei, so a thalamic effect is not impossible; however, the literature does not establish SATB1 as a limiting terminal selector for this broad 151 thalamic class in the way TCF7L2 is.

My zero/nonzero decision is therefore `0`: the direct paralog (`Satb2`) and the best visible developmental transcription-factor comparators are at 0 or one-to-two DEGs in the actual focal dataset, and the external SATB1 biology points mostly to cortical interneurons or other specific neuronal subsets outside the requested glutamatergic thalamic class. I would not round up to a small positive count just from SATB1's general chromatin-organizer function, because broad chromatin activity alone is too nonspecific here and the matched same-platform SATB2 result is a complete null.

# Limits and uncertainty

The prediction extrapolates because `Satb1` itself was held out and no baseline expression or protein-editing measurement for the focal 151 Satb1-gRNA nuclei is supplied. A very small one-or-two-gene signature would be plausible and still consistent with the `Sox5` and `Cux2` analogs, but the expected count is below the first FDR 0.05 crossing. The strongest Satb1 literature phenotypes use conditional deletion in interneuron lineages or developmental contexts, whereas the PerturbAI experiment is sparse AAV-CRISPR at P16 and is assayed only among recovered NeuN-positive nuclei. Conversely, adult Satb1 immunoreactivity in some thalamic neurons keeps open the possibility that a narrower thalamic subtype could respond, but a subtype-specific effect could be diluted inside the broad `151 TH Prkcd Grin2c Glut` aggregate.
