# Question

Predict `n_degs` for the held-out `Cdh2` perturbation in `151 TH Prkcd Grin2c Glut` cells.  I treated the endpoint exactly as specified: the count is the number of measured genes, including the perturbed gene itself if measured, with Wilcoxon Benjamini-Hochberg `pvals_adj < 0.05` in the focal `151 TH Prkcd Grin2c Glut` group.

The main ambiguity I resolved was how to handle genes such as N-cadherin whose best-known effects are local synaptic adhesion, receptor trafficking, and cytoskeletal regulation rather than sustained nuclear RNA changes.  I therefore separated two questions:

1. Is a broad downstream cell-state response expected?
2. If not, is a one-gene count plausible from the `Cdh2` self transcript?

# Sources

- Training DE parquet: `[local file: training_de_all_cell_groups.parquet]`.
- Focal training endpoint CSV: `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
- Held-out manifest: `[local file: 033_Cdh2.csv]`.
- Distributed Agents same-experiment corpus, release `perturbai-july-260713-sourceguard-1773-v1`, for curated in-dataset claims and perturbation-centered findings.
- Distributed Agents runtime profile comparison over the focal cell group, used to compare cadherin/catenin and synaptic-adhesion training perturbations by their 17,259-gene signed log-fold-change profiles.
- NCBI PubMed literature records:
  - Nuriya and Huganir 2006, DOI: `10.1111/j.1471-4159.2006.03740.x`.
  - Tai et al. 2007, DOI: `10.1016/j.neuron.2007.05.013`.
  - Fuentes et al. 2012, DOI: `10.1371/journal.pone.0041536`.
  - Nagaoka et al. 2014, DOI: `10.1016/j.celrep.2014.01.044`.
  - Nikitczuk et al. 2014, DOI: `10.1002/hipo.22282`.
  - Hoshina et al. 2021, DOI: `10.1126/science.aaz3893`.

# Dataset Checks

The manifest contains one requested target, `Cdh2`; `Cdh2` is absent from both the perturbation column of the DE parquet and the focal training-count CSV.

The focal training CSV has 1,674 non-held-out targets.  The focal endpoint is sparse:

- median `n_degs`: 0
- 75th percentile: 1
- targets with `n_degs = 0`: 1,205 / 1,674
- targets with `n_degs > 0`: 469 / 1,674
- 95th percentile: 18
- maximum: `Uba5`, 2,677

I used DuckDB and the profile runtime to filter the parquet to `group_name = '151 TH Prkcd Grin2c Glut'`.  This focal slice contains 28,891,566 rows: one 17,259-gene profile for each of 1,674 training perturbations.  For each candidate analog I joined its focal `n_degs` from the CSV and, where informative, inspected:

- all rows with `pvals_adj < 0.05`;
- the target-gene self row, `names = gene_target`;
- sentinel genes from the Ctnnb1/Wnt/adhesion response, including `Cdh2`, `Axin2`, `Lef1`, `Notum`, `L1cam`, `Epha4`, `Ptprj`, `Ptprm`, `Ptprz1`, `Slitrk6`, and `Vangl1`.

The self-row check was important because many low-count membrane-gene perturbations in this assay have exactly one focal DEG, and that DEG is the target transcript itself.  In all focal training targets with a self row, 319 / 1,642 had significant self-RNA downregulation; among one-DEG targets, 237 were self hits and 38 were not.

# Same-Experiment Analogs

## Cadherin and Catenin Scaffolds

`Cdh2` encodes N-cadherin, a classical cadherin that binds beta-catenin and p120/delta catenins through its cytoplasmic tail and recruits alpha-catenins to link the adhesion complex to the actin cytoskeleton.  The directly assayed cadherin-catenin perturbations in the focal group landed at the floor:

| perturbation | focal `n_degs` | focal expression-pattern evidence |
|---|---:|---|
| `Ctnna2` | 0 | no focal FDR genes; its own transcript was subthreshold (`logFC = -0.233`, `p_adj = 0.146`) and Wnt/adhesion sentinels including `Cdh2`, `Axin2`, `Lef1`, `L1cam`, `Ptprm`, and `Slitrk6` were all `p_adj = 1` |
| `Ctnna3` | 0 | no focal FDR genes and no cadherin/Wnt sentinel response |
| `Ctnnd2` | 1 | only the `Ctnnd2` self transcript passed FDR in the focal group (`logFC = -0.456`, `p_adj = 2.61e-4`); no `Cdh2`/Wnt/adhesion sentinels passed |
| `Ctnnb1` | 383 | strong exception: 100 up and 283 down focal DEGs, including `Ctnnb1` itself, `Cdh2`, canonical Wnt feedback genes `Axin2`, `Lef1`, `Notum`, and surface-recognition genes `L1cam`, `Epha4`, `Ptprj`, `Ptprm`, `Ptprz1`, `Slitrk6`, and `Vangl1` |

The Distributed Agents corpus explicitly summarizes this boundary in the claim "Represented cadherin/catenin scaffold perturbations do not produce a broad shared neuronal transcriptomic program, whereas Ctnnb1 is transcriptionally visible in this assay."  The underlying `Ctnnb1` finding also matters as a counterexample: beta-catenin loss had a large thalamic response in exactly the focal cell group, so the assay could read out Wnt/catenin transcription when the perturbed node reached that nuclear branch.  The alpha- and delta-catenin results argue that a cadherin scaffold perturbation by itself usually does not.

For `Cdh2`, I treated `Ctnnb1` as a mechanistic counterexample rather than a quantitative proxy.  N-cadherin can sequester beta-catenin at the membrane and regulate local beta-catenin-cadherin adhesion, but it is not itself the TCF/Wnt transcriptional effector.  The `Ctnna2`, `Ctnna3`, and `Ctnnd2` floor-level counts are closer to the missing direct N-cadherin scaffold branch.

## Cdh2-Adjacent Adhesion Genes

N-cadherin works at synapses together with other cell-adhesion and scaffold systems.  The represented neighbors again mostly gave zero or singleton focal surfaces:

| perturbation | focal `n_degs` | why it was informative |
|---|---:|---|
| `Pcdh19` | 0 | protocadherin-19 can interact functionally with N-cadherin at mossy fiber synapses, but P16 sparse loss had no focal DEGs and its corpus finding reports no robust downstream response in any recovered neuronal supergroup |
| `Nectin1` | 0 | nectin/afadin complexes colocalize with N-cadherin-catenin pairs during synaptogenesis; `Nectin1` had 0 focal DEGs and Distributed Agents reports 0 downstream FDR<0.10 genes in all measured neuronal groups |
| `Cadm2` | 1 | only the `Cadm2` self transcript was significant in the focal group (`logFC = -0.757`, `p_adj = 6.47e-16`) |
| `Nlgn3` | 1 | only the `Nlgn3` self transcript was significant |
| `Nrxn1` | 1 | only the `Nrxn1` self transcript was significant |
| `Nrxn2` | 0 | no focal DEGs |
| `Nrxn3` | 0 | no focal DEGs in the training count table |
| `Lrrtm1` | 1 | one singleton, `R3hdm2`; no broad adhesion response |
| `Lrrtm3` | 0 | no focal DEGs |
| `Lrrtm4` | 0 | no focal DEGs |
| `Dlg4` | 1 | only the `Dlg4` self transcript was significant |
| `Shank3` | 2 | `Shank3` self transcript plus `Uba5`; still a floor-level response |

Distributed Agents claims for synaptic adhesion and receptor-scaffold genes agree with these counts: represented neurexin, neuroligin, LRRTM, GluD, CADM, contactin-associated, and PSD-near perturbations were flat, singleton, or non-overlapping and did not define a shared broad postnatal neuronal RNA module.

This is the main within-dataset evidence for a near-zero `Cdh2` call.  N-cadherin is certainly synaptic, but the assay is a 3-4 week, sparse, postmitotic snRNA-seq readout.  It is not a spine ultrastructure, receptor trafficking, adhesion strength, beta-catenin phosphosite, or electrophysiology assay.  The nearest local analogs say that disrupting a single structural adhesion component usually leaves the cell-body nuclear RNA profile unchanged or leaves only the gRNA target transcript.

## Wnt/PCP and Phosphorylation Neighbors

The literature links N-cadherin trafficking to PCP proteins and to beta-catenin Tyr-654 phosphorylation.  I therefore also treated the following as counterexamples:

| perturbation | focal `n_degs` | interpretation |
|---|---:|---|
| `Prickle1` | 0 | Nagaoka et al. connected Prickle/Vangl PCP proteins to N-cadherin internalization, but `Prickle1` was focal-zero and did not derepress an `Axin2`/`Lef1` beta-catenin program in the corpus |
| `Ptpn1` | 0 | PTP1B can dephosphorylate beta-catenin at N-cadherin complexes, but `Ptpn1` was basal-RNA silent in the focal group and did not form a BDNF/TrkB, insulin/leptin, JAK/STAT, or UPR RNA program |
| `Met` | 0 | HGF/MET can interact with beta-catenin/N-cadherin synapse formation in developing cortex, but `Met` had no focal DEGs |

These are weaker analogs than the direct catenins, but they help reject the idea that every Cdh2-connected signaling input turns into a thalamic nuclear RNA state.

# External Biology

The outside literature raised the prior that `Cdh2` perturbation could have a synaptic phenotype but did not force a large transcriptional phenotype.

- Nuriya and Huganir 2006 found that N-cadherin and beta-catenin form complexes with AMPA receptors and modulate AMPAR surface trafficking.  That is a local receptor-trafficking mechanism, not necessarily a sustained mRNA program.
- Tai et al. 2007 showed that NMDA receptor activity regulates N-cadherin endocytosis through beta-catenin binding.
- Nikitczuk et al. 2014 conditionally ablated N-cadherin from late postnatal excitatory forebrain synapses in mice and observed altered GluA1/PSD95 and inhibitory markers with memory effects, while excitatory synapse number and dendritic spine structure were largely preserved.  This points to postnatal synaptic composition as the likely axis.
- Nagaoka et al. 2014 showed that Vangl2 can bind the N-cadherin cytoplasmic region and regulate its internalization, with beta-catenin competing for related binding.
- Hoshina et al. 2021 found that PCDH19 interacts with N-cadherin at hippocampal mossy fiber synapses and that N-cadherin overexpression can rescue Pcdh19 heterozygous phenotypes, but the same-experiment `Pcdh19` perturbation was transcriptomically flat.
- Fuentes et al. 2012 linked PTP1B to dephosphorylation of beta-catenin Tyr-654 in N-cadherin complexes and spine maturation, while the same-experiment `Ptpn1` perturbation was also flat in basal focal neurons.

Together these mechanisms make `Cdh2` biologically important, but mostly through adhesion, receptor localization, and cytoskeletal regulation that can be invisible to a single-nucleus RNA endpoint.

# Prediction For Cdh2

I predict `Cdh2` will be essentially buffered downstream in `151 TH Prkcd Grin2c Glut`.

The broad/nonzero decision is driven primarily by the within-dataset analogs: `Ctnna2 = 0`, `Ctnna3 = 0`, `Ctnnd2 = 1`, `Pcdh19 = 0`, `Nectin1 = 0`, `Cadm2 = 1`, `Nlgn3 = 1`, `Nrxn1 = 1`, `Nrxn2 = 0`, `Nrxn3 = 0`, `Prickle1 = 0`, `Ptpn1 = 0`, and `Shank3 = 2`.  `Ctnnb1 = 383` shows that the focal cell group can mount a cadherin/Wnt-related RNA program, but its direct nuclear TCF/Wnt function makes it too broad to transfer to `Cdh2`.

For the integer, I chose `1` rather than `0`.  The expected downstream response is zero, but `Cdh2` is expressed detectably in the focal group: `Ctnnb1` loss down-regulated the measured `Cdh2` transcript itself (`logFC = -0.447`, `p_adj = 9.03e-5`).  Several similarly expressed synaptic-adhesion perturbations in this focal group produce exactly one DEG by significant self depletion (`Cadm2`, `Nlgn3`, `Nrxn1`, `Dlg4`, `Ctnnd2`).  That makes a singleton `Cdh2` self hit more plausible than hundreds of downstream genes.

# Limits

- `Cdh2` itself was held out, and no direct `Cdh2` perturbation finding exists in the Distributed Agents corpus, so the prediction extrapolates from neighbors rather than validating a measured Cdh2 profile.
- The closest intracellular catenin analogs are imperfect.  `Ctnnb1` is both a cadherin-binding protein and a transcriptional Wnt effector; `Ctnna2`/`Ctnna3` are actin-coupling catenins; `Ctnnd2` is delta-catenin rather than the unrepresented p120-catenin `Ctnnd1`.
- The actual count could be `0` if the Cdh2 guide pool produces indels without enough NMD-coupled target-RNA depletion to pass BH correction.  The assay average is only partial target-mRNA downregulation.
- Conversely, Cdh2 could have structural or electrophysiological consequences with no nuclear transcriptomic footprint; the endpoint would still remain zero or one.
- The literature contains hippocampal, cortical, developmental, and adult conditional-loss evidence, whereas the queried cells are juvenile thalamic/hypothalamic-like glutamatergic neurons sampled by sparse P16 AAV CRISPR.
