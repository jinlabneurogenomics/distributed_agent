# DEG-count prediction trace for `151 TH Prkcd Grin2c Glut`

## Question and resolution of ambiguities

The requested held-out perturbation list contains one mouse target:

| target_name |
|---|
| Grm3 |

I interpreted `n_degs` exactly as the requested endpoint: for `Grm3` knockout in the `151 TH Prkcd Grin2c Glut` class, predict the number of measured genes with `pvals_adj < 0.05` in the Perturb-seq Wilcoxon table. The count includes the target transcript itself if it passes FDR. `Grm3` is absent as a `gene_target` from the Parquet and absent from the training count CSV, but `Grm3` can still occur as a measured expression feature in other perturbations.

I did not use measured target-RNA reduction as an editing-efficiency score. The target transcript is useful only as part of the endpoint: in this data release, several neuronal signaling KOs have a single FDR hit that is just the targeted receptor or G-protein transcript.

## Sources used

- Differential-expression table: `[local file: training_de_all_cell_groups.parquet]`.
- Focal training endpoints: `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
- Requested target manifest: `[local file: 101_Grm3.csv]`.
- Same-experiment internal semantic layer: Distributed Agents corpus release `perturbai-july-260713-sourceguard-1773-v1`.
- Same-experiment profile tooling: Distributed Agents `profile_compare`/`profile_inspect` over signed `logfoldchanges` in `151 TH Prkcd Grin2c Glut`.
- External mechanism references:
  - HGNC, "Glutamate metabotropic receptors (GRM)" gene-group nomenclature, referenced by the Distributed Agents corpus.
  - Conn and Pin 1997, Annual Review of Pharmacology and Toxicology, DOI `10.1146/annurev.pharmtox.37.1.205`.
  - Nicoletti et al. 2010, Neuropharmacology, DOI `10.1016/j.neuropharm.2010.10.022`.
  - Harrison et al. 2008, Journal of Psychopharmacology, DOI `10.1177/0269881108089818`.
  - Lea et al. 2001, Journal of Neurophysiology, DOI `10.1152/jn.2001.85.3.1097`.
  - Trepanier et al. 2013, Scientific Reports, DOI `10.1038/srep00926`.
  - Betke et al. 2012, Progress in Neurobiology, PMID `22307060`.

## Computational steps over the same-experiment data

1. Loaded the manifest and confirmed that the only requested target was `Grm3`.

2. Read the `151 TH Prkcd Grin2c Glut` training-count CSV. It contained 1,674 non-held-out perturbations; 1,205 were zero at FDR 0.05, the median was 0, the 75th percentile was 1, and the 95th percentile was 18. This establishes that small receptor-level responses are common and that a prediction of zero is a real endpoint claim, not a missing-value convention.

3. Queried the training counts for metabotropic glutamate receptors and adjacent signaling genes:

| training target | observed `n_degs` in `151` | relationship to `Grm3` |
|---|---:|---|
| Grm1 | 1 | group-I mGluR, Gq/PLC rather than Gi/o |
| Grm5 | 0 | group-I mGluR, Gq/PLC |
| Grm6 | 0 | group-III mGluR, retinal ON-bipolar biased, Gi/o-family branch |
| Grm7 | 1 | group-III presynaptic Gi/o-coupled mGluR |
| Grm8 | 0 | group-III presynaptic Gi/o-coupled mGluR |
| Gnao1 | 1 | neuronal Gi/o alpha subunit used by inhibitory GPCRs |
| Gnas | 0 | Gs/cAMP counter-branch |
| Gnal | 0 | Gs/olfactory G-alpha relative |
| Adcy1 | 0 | calcium/calmodulin-stimulated adenylyl cyclase |
| Adcy3 | 0 | adenylyl cyclase |
| Adcy5 | 0 | adenylyl cyclase |
| Plcb1 | 0 | group-I mGluR PLC effector |
| Itpr1 | 0 | PLC/IP3 calcium-release effector |
| Prkaca | 1 | PKA catalytic subunit |
| Prkar1a | 1 | PKA regulatory subunit |
| Prkca | 0 | PKC node downstream of PLC/DAG |
| Homer2 | 0 | group-I mGluR/PSD scaffold |
| Shank2 | 0 | PSD scaffold |
| Shank3 | 2 | PSD scaffold; one hit was Shank3 itself |
| Dlg4 | 1 | PSD-95; one hit was Dlg4 itself |
| Grin1 | 89 | ionotropic NMDAR obligatory subunit; positive counterexample |
| Grin2a | 1 | ionotropic NMDAR subunit |
| Grin2b | 2 | ionotropic NMDAR subunit |
| Grin2d | 0 | ionotropic NMDAR subunit |
| Grin3a | 0 | ionotropic NMDAR subunit |

4. Filtered the Parquet itself to `group_name == "151 TH Prkcd Grin2c Glut"` and these analog perturbations, then recomputed `(pvals_adj < 0.05).sum()` per `gene_target`. This exactly matched the training CSV for all inspected nodes. It also showed that the one-DEG calls for `Grm1`, `Grm7`, `Gnao1`, `Dlg4`, `Prkaca`, and `Prkar1a` were their own transcripts, while `Grm5`, `Grm6`, `Grm8`, the adenylyl cyclases, `Plcb1`, `Itpr1`, `Prkca`, `Homer2`, and `Shank2` had no FDR<0.05 genes at all.

5. Ran Distributed Agents `profile_compare` on the signed `logfoldchanges` of the metabotropic receptor, G-protein, cAMP, PLC/IP3, scaffold, and NMDAR analogs in the same focal group. The selected receptors had 0 or 1 significant feature; receptor-to-effector whole-profile cosines were moderately positive, but every inspected pair had 0 shared significant positive features, 0 shared significant negative features, and 0 significant direction conflicts. Thus the subthreshold profiles do not expose a hidden shared mGluR module that would justify inflating `Grm3` above the directly observed analog counts.

## Target-specific reasoning

### `Grm3`

`Grm3` encodes mGluR3. By receptor family, it is a close paralog of `Grm1`, `Grm5`, `Grm6`, `Grm7`, and `Grm8`, all of which were observed in the training endpoint. Functionally, mGluR3 is a group-II metabotropic glutamate receptor: group II mGluRs couple through Gi/o, inhibit adenylyl cyclase, and modulate glutamatergic neurotransmission and synaptic plasticity rather than acting as ion channels. Harrison et al. 2008 describe mGluR3 as glial and neuronal, with a predominantly presynaptic distribution and inhibitory autoreceptor/heteroreceptor roles; Lea et al. 2001 showed NAAG/mGluR3 control of cAMP-dependent dentate LTP; and Trepanier et al. 2013 showed that group-II mGluR2/3 signaling can also modulate NMDARs through the cAMP/PKA/Src axis.

The closest observed pathway analogs all argue for a zero/single-gene response in the requested assay:

- `Grm7` and `Grm8` are not group-II receptors, but they share the presynaptic Gi/o, cAMP-inhibitory metabotropic architecture more closely than group-I `Grm1`/`Grm5`; their focal counts were `1` and `0`.
- `Gnao1`, a central neuronal Gi/o alpha, had count `1`; its only focal FDR<0.05 hit was `Gnao1` itself.
- The cAMP branch downstream or opposed to mGluR3 was quiet: `Adcy1`, `Adcy3`, `Adcy5`, `Gnas`, and `Gnal` were all `0`; `Prkaca` and `Prkar1a` were each self-only at `1`.
- Group-I mGluR comparators gave no evidence that metabotropic glutamate signaling leaves a durable basal snRNA footprint here. `Grm1` had `1` hit, its own mRNA; `Grm5` had `0`; `Plcb1`, `Itpr1`, `Prkca`, and `Homer2` were all `0`.
- PSD counterexamples were also small: `Dlg4` and `Shank3` were self-only or two-gene calls, and `Shank2` was `0`.
- `Grin1` was the important positive counterexample. It had `89` DEGs in `151 TH Prkcd Grin2c Glut`, demonstrating that this focal class and the local Wilcoxon setup can report a glutamatergic receptor perturbation when an NMDAR-dependent transcriptional axis is engaged. However, other NMDAR subunits were small (`Grin2a` `1`, `Grin2b` `2`, `Grin2d` `0`, `Grin3a` `0`), and Distributed Agents corpus Finding `Grin1:F007` explicitly notes that the subunit perturbations did not phenocopy `Grin1`. I therefore treated `Grin1` as a boundary, not as evidence for a broad `Grm3` signature.

The same-experiment Distributed Agents corpus had no direct `Grm3` Findings or Claims, so direct same-experiment semantic evidence is missing for the held-out gene. Around the observed paralogs, though, the corpus supports the raw endpoint result: `Grm1` produced no downstream DEGs in its measured neuronal groups after excluding its own transcript; `Grm5` was pan-null for the basal nuclear transcriptome and its report grouped `Grm1`, `Grm6`, `Grm7`, `Grm8`, `Homer2`, `Itpr1`, `Plcb1`, `Prkca`, `Dlg4`, and `Shank2` as mostly flat comparators; `Grm7` and `Grm8` had no FDR-resolved downstream nuclear RNA response after sparse P16 loss of function. Those corpus calls were often made at FDR<0.10, so they are a conservative qualitative check on the exact FDR<0.05 endpoint used here.

I considered whether to predict one DEG to allow for the `Grm3` self-transcript. I rejected that because the within-dataset mGluR pattern is not uniformly self-positive (`Grm5`, `Grm6`, `Grm8` were zero), and rows measuring `Grm3` in the selected analog perturbations had `pvals_adj = 1` with unstable signed log fold changes, consistent with sparse or noisy detection of that measured feature in this focal class. The experiment also sampled NeuN-positive recovered nuclei and under-sampled astrocytes, one of the compartments in which mGluR3 has recognized biology. Taken together, the appropriate analogs place `Grm3` in the mGluR/Gi-o buffered regime, not in the `Grin1` transcriptome-coupled regime.

**Prediction for `Grm3`: `0` DEGs.**

## Limits

- This is an extrapolation because `Grm3` itself was completely held out as a perturbation and the Distributed Agents corpus release has no direct `Grm3` report.
- No observed training perturbation is a perfect mechanistic substitute: `Grm1`/`Grm5` share the mGluR family but couple through Gq/PLC; `Grm7`/`Grm8` share Gi/o coupling but are group III rather than group II; and `Gnao1`/adenylyl-cyclase perturbations sit downstream of many GPCRs rather than specifically below mGluR3.
- The endpoint is assay- and power-dependent. A prediction of `0` means I expect no gene to pass BH FDR 0.05 in this recovered-nucleus snRNA contrast; it does not mean mGluR3 is biologically irrelevant, not edited, or unable to affect synaptic physiology.
- The training counts include self-transcript hits. For `Grm3`, whether its own mRNA would pass FDR is uncertain because the related receptors split between self-only and fully null outcomes.
