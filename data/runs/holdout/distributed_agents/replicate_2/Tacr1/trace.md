# Tacr1 DEG-count prediction for `151 TH Prkcd Grin2c Glut`

## Question and resolved ambiguities

I interpreted the task as a target-level prediction for one held-out perturbation:

```tsv
target_name
Tacr1
```

The endpoint is the integer number of measured genes with `pvals_adj < 0.05` after acute mosaic CRISPR loss of the target in `151 TH Prkcd Grin2c Glut`. `Tacr1` itself was absent as a perturbation from both the parquet and the count CSV, so I treated all `Tacr1` differential-expression rows as unobserved and did not infer a self-knockdown p value directly.

I counted target-transcript knockdown rows as part of the training endpoint when they were present, because the training counts do that: in the focal cell group `Prkcg`, `Camk2b`, and `Gnao1` each have one DEG and that single significant feature is the perturbed gene itself. That matters because a low point prediction can be either truly zero or a single self-transcript hit.

## Sources used

- Input training endpoint: `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
- Input DE parquet: `[local file: training_de_all_cell_groups.parquet]`.
- Requested-target manifest: `[local file: 230_Tacr1.csv]`.
- Distributed Agents same-experiment corpus MCP, release `perturbai-july-260713-sourceguard-1773-v1`. `Tacr1` had no target-scoped Finding or Claim in the frozen corpus, but `Tacr3`, `Plcb1`, `Chrm3`, `Grm5`, and `Htr2c` had relevant negative and pathway-uncoupling Findings.
- Distributed Agents runtime profile tools. I compared signed Wilcoxon-score profiles for the candidate observed analogs in the focal cell group in `profile_compare_tacr1_analogs.json` and projected the exact cohort diagnostic to `profile_compare_tacr1_analogs.cohort.json`.
- NCBI PubMed through the BioEval Literature MCP for external mechanism checks.

External mechanism references:

- Steinhoff MS, von Mentzer B, Geppetti P, Pothoulakis C, Bunnett NW. 2014. Review of tachykinins and NK1/NK2/NK3 GPCR signaling, trafficking, and physiology. DOI: `10.1152/physrev.00031.2013`; PMID: `24382888`.
- Li H, Leeman SE, Slack BE, Hauser G, Saltsman WS, Krause JE, Blusztajn JK, Boyd ND. 1997. Full-length and truncated substance P/NK1 receptors signal through phospholipase-C-dependent calcium pathways. DOI: `10.1073/pnas.94.17.9475`; PMID: `9256507`.
- Endo T, Yanagawa Y, Komatsu Y. 2014. Substance P depolarizes cortical nNOS GABAergic neurons through NK1 receptors, G proteins, and a PLC-dependent cation-channel pathway. DOI: `10.1093/cercor/bhu233`; PMID: `25316339`.

## Computations over the supplied dataset

1. I loaded the focal-cell training count CSV. It contains 1,674 non-held-out perturbations; 1,205 have `n_degs = 0`, 469 have at least one DEG, the median is 0, the 90th percentile is 2, the 95th percentile is 18, and the maximum is 2,677. Thus the endpoint is strongly zero-inflated and most receptors/signaling genes need a reason to escape zero.

2. I checked the held-out gene against training counts. `Tacr1` was absent, as required.

3. I searched the training target list for tachykinin, G protein, PLC, calcium, PKC, adenylyl-cyclase, and immediate-early/activity genes. Direct `Tacr1` ligands and several first transducers were not represented as perturbations (`Tac1`, `Tac2`, `Tac4`, `Tacr2`, `Gnaq`, `Gna11`, `Plcb2`, `Plcb3`, `Plcb4`, `Arrb1`, `Arrb2` were absent), but the screen did contain a useful partial analog set:

| training perturbation | focal `n_degs` | relevance to `Tacr1` |
| --- | ---: | --- |
| `Tacr3` | 0 | closest represented tachykinin receptor paralog, NK3R |
| `Plcb1` | 0 | immediate PLC effector for Gq-coupled receptors |
| `Itpr1` | 0 | IP3/Ca-release node downstream of PLC |
| `Prkca` | 0 | DAG/PKC node downstream of PLC |
| `Prkcg` | 1 | neuronal DAG/PKC node; only the target transcript was significant in the focal group |
| `Adcy1` | 0 | calcium-sensitive cAMP effector/counter-branch |
| `Chrm3` | 0 | Gq-coupled neuromodulatory GPCR counterexample |
| `Grm5` | 0 | Gq/PLC-coupled synaptic GPCR counterexample |
| `Htr2c` | 0 | Gq/PLC-coupled serotonin receptor counterexample |
| `Kiss1r` | 0 | Gq/PLC-coupled neuropeptide receptor counterexample |
| `Gnrhr` | 0 | neuroendocrine Gq GPCR in the same Tacr3/Kiss1r pathway neighborhood |
| `Cckar`, `Cckbr` | 0, 0 | Gq-coupled peptide receptor counterexamples |

4. I filtered the parquet to `group_name == "151 TH Prkcd Grin2c Glut"` and the main analog targets. The operation was:

```python
expr = (
    (pc.field("group_name") == "151 TH Prkcd Grin2c Glut")
    & pc.field("gene_target").isin(candidate_targets)
)
```

This returned 17,259 measured genes per observed analog. I then counted `pvals_adj < 0.05` and inspected the lowest adjusted p values for each perturbation.

Key focal-cell signature evidence:

- `Tacr3`: 115 perturbed cells, 23,679 matched controls, 0 FDR DEGs; the top adjusted p values were all 1.0.
- `Plcb1`: 160 perturbed cells, 0 FDR DEGs; the top adjusted p values were all 1.0.
- `Prkca`: 169 perturbed cells, 0 FDR DEGs; the top adjusted p values were all 1.0.
- `Prkcg`: 175 perturbed cells, 1 FDR DEG, `Prkcg` itself down (`score = -7.997`, `logfoldchanges = -0.567`, `pvals_adj = 2.21e-11`); the next genes had `pvals_adj = 1.0`.
- `Adcy1`: 88 perturbed cells, 0 FDR DEGs; its smallest adjusted p value was 0.139.
- `Itpr1`: 203 perturbed cells, 0 FDR DEGs; the target transcript was the closest row but still did not pass FDR (`pvals_adj = 0.08596`).
- `Chrm3`, `Grm5`, `Htr2c`, `Kiss1r`, `Gnrhr`, and `Oprk1`: 0 FDR DEGs in the focal group, with no near-threshold downstream pattern.

5. I used the runtime profile comparison on the signed Wilcoxon `scores` for the most relevant 10 observed analogs: `Tacr3`, `Plcb1`, `Prkca`, `Prkcg`, `Adcy1`, `Itpr1`, `Chrm3`, `Grm5`, `Htr2c`, and `Kiss1r`. The exact cohort comparison had 45 available pairs. Nine of the 10 anchors had no significant features and the tenth, `Prkcg`, had only one. Pairwise Pearson correlations across the full focal-cell score vectors were small, approximately `-0.057` to `0.054` for the PLC/PKC/Gq cohort except for the null self structure; the median top-tail overlap was 0.02 for both positive and negative tails. That supports the corpus statement that these are flat or mutually nonconvergent basal RNA profiles, not a hidden shared module.

6. I checked the Distributed Agents corpus for focal-cell responsiveness. The corpus contains broad positive programs in the same cell group for several other target classes, including Elongator/ATF4 stress, BAF/mSWI/SNF, Wnt/catenin, and selected ion-channel perturbations. Training counts agree: `Elp1` has 645 focal DEGs, `Ctnnb1` has 383, `Smarcc2` has 185, and `Grin1` has 89. The `Tacr1` prediction is therefore not based on the focal group being globally underpowered or inert.

## Target-specific reasoning and point prediction

### `Tacr1`

**Biological prior.** `Tacr1` encodes NK1R, the high-affinity substance-P receptor in the tachykinin GPCR family. NK1R can signal through G proteins into PLC, calcium, PKC, MAPK, and arrestin/trafficking pathways; stimulus-locked NK1R activation can be electrophysiologically potent in neurons. This prior makes `Tacr3`, other peptide GPCRs, and the PLC/Ca/PKC arm the right comparison set, but it does not by itself imply a persistent 3-4 week nuclear RNA signature after sparse postnatal loss of one receptor.

**Within-dataset analogs.** The strongest available same-family analog is `Tacr3`, which produced 0 DEGs in `151 TH Prkcd Grin2c Glut`. In the Distributed Agents corpus, `Tacr3` had only a one-gene response in a different broad group and no robust data-driven positive or negative signature neighbor; its `Tacr3:F003` Finding also noted that Gq/neuroendocrine comparators such as `Kiss1r`, `Oprk1`, `Plcb1`, and `Gnrhr` did not phenocopy it. The focal-cell parquet rows were even more direct: `Tacr3`, `Kiss1r`, `Gnrhr`, `Oprk1`, and `Plcb1` were all at 0 DEGs in this exact cell group.

The immediate biochemical arm did not argue for a nonzero count. `Plcb1`, `Itpr1`, and `Prkca` had no FDR-significant focal features; `Prkcg` had one feature, but it was the `Prkcg` target transcript itself rather than a downstream PKC program. Calcium/CaMK and adenylyl-cyclase neighbors were likewise either zero (`Adcy1`, `Camk2a`, `Camk2g`, `Gnas`) or singleton self-transcript events (`Camk2b`, `Gnao1`). In the corpus, `Plcb1` anchors claim `claim:9f69c85a0a28574c603c`, whose same-experiment summary is that represented neuromodulatory GPCR receptors and proximal second-messenger effectors generally failed to form a shared basal neuronal nuclear-transcriptome module.

Broader Gq-coupled receptors are informative counterexamples rather than direct phenocopies. `Chrm3`, `Grm5`, `Htr2c`, `Cckar`, `Cckbr`, and `Kiss1r` all connect extracellular neuromodulator binding to PLC/Ca/PKC-like signaling, yet all had 0 DEGs in the focal cell group. Corpus target contexts for `Chrm3`, `Grm5`, and `Htr2c` independently recorded pan-null or nonconvergent behavior across receptor-family and second-messenger comparators. This says that the basal snRNA assay is poor at reporting isolated neuromodulatory GPCR loss unless the perturbation crosses into a stable stress, identity, sterol, chromatin, or ion-channel state.

**Zero/nonzero decision.** I predict no FDR-significant genes for `Tacr1` in this cell group. The expected NK1R biology is ligand- and circuit-state dependent, and the relevant observed loss-of-function neighbors repeatedly sit at zero in the focal training counts. The only reason to nudge the call above zero would be a `Tacr1` self-transcript knockdown event; however, receptor perturbations in the same training set often failed to produce even the self row after BH correction, and no pathway neighbor suggests a stable downstream program. I therefore set the integer point prediction to:

```tsv
target_name	predicted_n_degs
Tacr1	0
```

## Limits and extrapolations

- The most direct first-hop tachykinin genes were not all assayed. `Tac1`, `Tac2`, `Tac4`, `Tacr2`, `Gnaq`, `Gna11`, `Plcb2`, `Plcb3`, `Plcb4`, `Arrb1`, and `Arrb2` were absent from the training perturbations, so I extrapolated from `Tacr3`, `Plcb1`, `Itpr1`, `Prkca`, `Prkcg`, and more distant Gq GPCRs.
- `Tacr3` is the only represented tachykinin receptor, but NK3R biology in KNDy/GnRH circuits is not the same as NK1R/substance-P biology in thalamic glutamatergic neurons.
- The assay reports basal nuclear RNA weeks after mosaic P16 CRISPR perturbation. It does not test substance-P stimulation, receptor internalization, calcium transients, membrane excitability, behavior, or acute immediate-early pulses.
- DNA indels, NK1R protein, and target RNA knockdown for the held-out `Tacr1` perturbation were not available. If `Tacr1` is unusually highly expressed in this focal group, the true count could be a one-gene target-transcript hit even without a downstream state.
- Correlations among near-null signatures are intrinsically noisy. I used them mainly to reject a strong hidden shared PLC/GPCR module; I did not rank the analogs by tiny differences in near-zero Pearson values.
