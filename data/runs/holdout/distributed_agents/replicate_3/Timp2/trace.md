# DEG-count prediction for `151 TH Prkcd Grin2c Glut`

## Question interpreted

The requested held-out manifest contains one perturbation target:

| target_name |
|---|
| Timp2 |

I interpreted `predicted_n_degs` as the integer number of measured genes expected to satisfy `pvals_adj < 0.05` after acute sparse AAV-CRISPR loss of `Timp2` in `151 TH Prkcd Grin2c Glut` mouse thalamic glutamatergic neurons. The count includes a possible self-transcript hit if the target RNA itself passes the Wilcoxon/BH threshold. Because `Timp2` was completely held out, no `Timp2` perturbation DE profile or DEG count was used.

## Sources used

- Input endpoint file: `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`, 1,674 non-held-out perturbations.
- Input DE parquet: `training_de_all_cell_groups.parquet`; I queried exact adjusted p-values, log-fold changes, and matched cell counts for focal-cell TIMP/ECM/metalloprotease/integrin/Wnt-neighbor perturbations.
- Distributed Agents same-experiment corpus, release `perturbai-july-260713-sourceguard-1773-v1`. `Timp2` itself had no target-centered Claims or Findings in this release, so I used the corpus mainly for same-dataset interpretations of `Timp3`, `Adam10`, `Adamts17`, `Fbn1`, and `Itgb1` comparators.
- NCBI PubMed for external TIMP2 biology:
  - Brew & Nagase 2010, DOI `10.1016/j.bbamcr.2010.01.003`: TIMPs are endogenous metalloproteinase inhibitors with additional non-MMP activities.
  - Caterina et al. 2000, PMID `10827176`, DOI `10.1074/jbc.M001271200`: mouse `Timp2` inactivation altered pro-MMP2 activation while homozygous mutants developed and reproduced grossly normally.
  - Worley et al. 2003, PMID `12630911`, DOI `10.1042/BJ20021573`: TIMP2 C-terminal residues are required for the MT1-MMP/TIMP2/pro-MMP2 activation complex.
  - Seo et al. 2003, PMID `12887919`, DOI `10.1016/S0092-8674(03)00551-8`: TIMP2 can suppress angiogenesis through alpha3-beta1 integrin in an MMP-independent, endothelial mechanism.
  - Castellano et al. 2017, PMID `28424512`, DOI `10.1038/nature22067`: systemic/hippocampal TIMP2 can support plasticity and cognition in aged mice.

## Dataset computations

The endpoint distribution in `151 TH Prkcd Grin2c Glut` is sparse: 1,205 of 1,674 training perturbations had `n_degs = 0`; 363 had 1-9 DEGs; 63 had 10-99; and 43 had at least 100. This makes zero the empirical default unless close same-assay neighbors show a reproducible nonzero module.

I then queried focal DE rows for TIMP2-relevant targets. The main operation was:

```sql
SELECT gene_target, names, logfoldchanges, pvals_adj, scores,
       n_pert_matched, n_ctrl_matched
FROM parquet_scan('training_de_all_cell_groups.parquet')
WHERE group_name = '151 TH Prkcd Grin2c Glut'
  AND gene_target IN (
    'Timp3','Adam10','Adam22','Adamts17',
    'Itga2','Itga4','Itga6','Itga7','Itga8','Itga9','Itgb1','Itgb2',
    'Lrp1','Lrp2','Lrp5','Lrp6','Lrp8'
  )
  AND pvals_adj < 0.05
ORDER BY gene_target, pvals_adj;
```

The exact focal significant rows were:

| perturbation | focal n_degs | significant focal rows |
|---|---:|---|
| `Timp3` | 1 | `Timp3`, logFC -0.8416, q = 1.45e-6; 223 perturbed vs 23,679 controls |
| `Adam10` | 0 | none; 69 perturbed vs 23,679 controls |
| `Adam22` | 1 | `Adam22`, logFC -0.5502, q = 1.07e-9; 115 perturbed vs 23,679 controls |
| `Adamts17` | 0 | none; closest nominal `Spata2l`, q = 0.274 |
| `Itga2`, `Itga4`, `Itga6`, `Itga7`, `Itga8`, `Itga9`, `Itgb1`, `Itgb2` | all 0 | no focal FDR rows |
| `Lrp1`, `Lrp2`, `Lrp5`, `Lrp8` | all 0 | no focal FDR rows |
| `Lrp6` | 4 | `Nsmf`, `Nrbp2`, `Atrnl1`, `Chgb`; weak focal Wnt-associated counterexample, not a TIMP/MMP analog |

I also scanned those analog perturbations across all groups for `pvals_adj < 0.05`. The only TIMP3 events were `Timp3` itself in `151 TH Prkcd Grin2c Glut` and a singleton `Syp` hit in `046 CTX-CGE GABA`; `Adam10` and `Adamts17` had no FDR 0.05 rows in any group; `Itga6` and `Itga8` each had one isolated non-focal singleton; `Lrp1`, `Lrp5`, and `Lrp6` had a few target-specific or Wnt-related hits. This supports reading the focal `Timp3` count of 1 as target-RNA depletion, not as a broad TIMP-family downstream response.

## Target-specific reasoning

### `Timp2`

`Timp2` encodes a secreted tissue inhibitor of metalloproteinases. Biochemically it can inhibit active MMPs, but it is unusual among TIMPs because low concentrations of TIMP2 promote cell-surface pro-MMP2 activation by forming an MT1-MMP/TIMP2/pro-MMP2 complex; mouse germline `Timp2` loss correspondingly perturbs pro-MMP2 activation (Caterina et al. 2000; Worley et al. 2003; Brew & Nagase 2010). TIMP2 also has non-catalytic extracellular receptor biology, including an endothelial anti-angiogenic alpha3-beta1-integrin mechanism (Seo et al. 2003). Those functions are real, but they are extracellular, matrix-, protease-, or vascular-context mechanisms rather than a direct neuronal transcription-factor circuit.

The closest represented paralog was `Timp3`, with `n_degs = 1` in the focal class. Its only focal FDR row was `Timp3` itself (`logfoldchanges = -0.8416`, `q = 1.45e-6`), so the TIMP paralog produced no detectable downstream target in the exact cell group being predicted. The corpus `Timp3` report likewise interpreted the screen as pathway-uncoupled from measured `Adam10`, `App`, `Kdr`, `Tnfrsf1a`, and `Notch` targets; several direct biochemical substrates such as `Mmp2`, `Mmp3`, `Mmp9`, `Mmp14`, `Adam17`, `Adamts4`, and `Adamts5` were not represented, which is an important gap, but the available same-assay metalloprotease-adjacent nodes did not phenocopy a TIMP response.

The closest measurable TIMP2 effector classes were also quiet:

- `Adam10`, an ADAM metalloprotease connected to APP and Notch shedding, had `n_degs = 0` in the focal class and no FDR 0.05 rows in the all-group scan.
- `Adamts17`, an extracellular ADAMTS-family metalloprotease, had `n_degs = 0` in the focal class and no FDR 0.05 rows in the all-group scan. The Distributed Agents corpus claim over `Adamts17`/`Fbn1` reports no detectable ECM-linked TGF-beta/BMP-SMAD transcriptional module in the assayed postmitotic neurons.
- `Itgb1` had `n_degs = 0` in the focal class. Its direct alpha-integrin comparators in the training endpoint were also focal nulls: `Itga2`, `Itga4`, `Itga6`, `Itga7`, `Itga8`, and `Itga9` were all `0`. The Distributed Agents corpus claim over represented integrins states that these perturbations did not produce a shared basal neuronal adhesion or beta1/focal-adhesion mRNA module, aside from isolated single-gene effects outside this focal class.
- `Lrp1`, a broad extracellular protease-clearance/scavenger receptor, had `n_degs = 0`; `Lrp2`, `Lrp5`, and `Lrp8` were also `0`. `Lrp6` was a weak positive at `4`, but the corpus identifies this as a selective thalamic beta-catenin/TCF signal rather than an LRP-wide extracellular-matrix response, so I treated it as a counterexample against simple family transfer.

The main external positive prior was Castellano et al. 2017, where systemic TIMP2 improved hippocampal function in aged mice and TIMP2 depletion blocked the benefit of umbilical-cord plasma. That result says TIMP2 can matter in the brain, but it is imperfect for the present readout: it involves aged hippocampus, circulating protein, extracellular protein depletion or replacement, and plasticity/electrophysiology rather than a sparse cell-autonomous CRISPR knockout in P37-P44 thalamic neurons. Similarly, TIMP2's alpha3-beta1-integrin anti-angiogenic mechanism is endothelial, whereas the experiment enriched NeuN-positive nuclei and under-sampled vascular cells.

Putting those pieces together, I predicted no FDR-significant genes for `Timp2` in `151 TH Prkcd Grin2c Glut`. A single self-transcript hit is plausible by analogy to `Timp3`, but I did not assign `1` because the same-assay evidence for any downstream TIMP/MMP/integrin program is absent and because the target-RNA behavior is guide-, expression-, and locus-dependent; weak or absent self-RNA depletion is common in this assay.

## Limits

This is an extrapolation from adjacent genes, not a direct `Timp2` measurement. The available training set lacked the most direct TIMP2 protease partners `Mmp2` and `Mmp14`, so the comparison relies on `Timp3`, `Adam10`, `Adamts17`, `Itgb1`/integrins, and LRP receptors as partial analogs and counterexamples. The assay measures nuclear RNA after sparse mosaic neuronal CRISPR and will miss extracellular proteolysis, secreted-protein abundance, MMP activity, vascular responses, glial responses, and synaptic physiology. Finally, a count of zero only predicts no gene crossing the BH FDR 0.05 threshold in this powered survivor nucleus set; it is not a claim that TIMP2 is biologically irrelevant.

