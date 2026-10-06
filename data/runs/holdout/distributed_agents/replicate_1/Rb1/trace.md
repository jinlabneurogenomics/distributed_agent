# Task interpretation

The requested held-out perturbation was `Rb1`.  I interpreted the endpoint as a point prediction for the number of focal-cell measured genes with `pvals_adj < 0.05` after acute mosaic CRISPR loss of function in `151 TH Prkcd Grin2c Glut` neurons.  The held-out `Rb1` perturbation itself is absent from the supplied differential-expression parquet and from the `151 TH Prkcd Grin2c_Glut` training count CSV, so I did not look for a direct `Rb1` signature.

This is a scalar count prediction, not a ranked gene-output task.  I therefore used the declared training endpoint and direct parquet queries rather than the ranking-only `dataset.perturbseq_features`, `corpus.predictive_graph_review`, or `synthesis.ordering_validate` capabilities.

# Sources used

- Declared endpoint table: `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
- Declared differential-expression parquet: `training differential-expression dataset`.
- Requested-target manifest: `single-target request for Rb1`.
- Run-local normalized task metadata: `codex_runtime/pipeline/task_bindings.json`, `coverage.json`, `capabilities.json`, and `measurement_registry.json`.
- Internal same-experiment corpus: `perturbai-july-260713-sourceguard-1773-v1`, used through the compact `corpus.calibration`, `corpus.findings`, and `corpus.graph` entrypoints.  This corpus is a curated interpretation of the same Perturb-seq experiment, not independent replication of the parquet.
- External literature from PubMed:
  - Giacinti and Giordano 2006, DOI `10.1038/sj.onc.1209615`; Duronio and Xiong 2013, DOI `10.1101/cshperspect.a008904`; and Sengupta and Henry 2015, DOI `10.1016/j.bbagrm.2015.08.008`, for the standard model in which RB-family pocket proteins repress E2F-dependent G1/S transcription and cyclin/CDK phosphorylation releases E2F activity.
  - Cam and Dynlacht 2003, DOI `10.1016/s1535-6108(03)00080-1`, for activating versus repressive E2F subclasses and the use of E2F/DREAM target genes as cell-cycle readouts.
  - Sherr 2000, PubMed `10919634`, and James and Peters 2000, DOI `10.1007/978-1-4615-4253-7_7`, for the CDKN2A locus linking p16INK4a-CDK4/6-RB-E2F and ARF-MDM2-p53 circuitry.
  - Dagnino et al. 1997, DOI `10.1016/s0925-4773(97)00083-x`; Corbeil et al. 1995, PubMed `7675450`; and Kusek et al. 2001, DOI `10.1016/s0361-9230(00)00447-0`, for developmental expression of E2F and RB-family components during neuronal differentiation.
  - Hoglinger et al. 2007, DOI `10.1073/pnas.0611671104`; Hou et al. 2002, DOI `10.1074/jbc.M206336200`; Lu et al. 2013, DOI `10.1038/emboj.2013.25`; and Zhao et al. 2016, DOI `10.1074/jbc.M116.718049`, for examples where RB/E2F signaling can participate in neuronal cell-cycle re-entry, E2F target-gene derepression, or apoptosis in stressed, hypothalamic POMC, or embryonic neuronal contexts.

# Quantitative calibration

The focal training count table has 1,674 non-held-out perturbations.  It is highly sparse: median `n_degs = 0`, 75th percentile `= 1`, 90th percentile `= 2`, 95th percentile `= 18`, and maximum `= 2677`.  Thus a zero prediction is the empirical baseline unless a held-out target has a close analog among the minority of broadly active perturbations.

I queried the parquet for `151 TH Prkcd Grin2c Glut` rows of RB/E2F/p53-axis training genes and for the canonical downstream transcripts that would reveal an RB-loss response:

```
group_name == "151 TH Prkcd Grin2c Glut"
gene_target in {Cdkn2a, E2f1, E2f5, Tfdp1, Tfdp2, Myc, Trp53, Trp63, Trp73, Atr, Ep300, Crebbp}
names in {Rb1, Rbl1, Rbl2, E2f1-E2f8, Cdk1/2/4/6, Ccna2, Ccnb1, Ccnd1,
          Ccne1, Cdkn1a, Cdkn1b, Cdkn2a, Mdm2, Mki67, Pcna, Top2a, Bax, Bbc3}
```

The training endpoint and focal DE rows gave these relevant counts:

| training target | focal `n_degs` | focal expression-pattern evidence |
| --- | ---: | --- |
| `Cdkn2a` | 0 | 344 nominal `p < 0.05` genes but zero FDR genes; minimum adjusted p-value 0.539.  `E2f1`, `Pcna`, `Mki67`, `Top2a`, `Cdkn1a`, `Mdm2`, `Bax`, and `Bbc3` were all nonsignificant with `pvals_adj = 1`. |
| `E2f1` | 0 | 294 nominal genes but zero FDR genes; minimum adjusted p-value 1.0.  No corrected movement of `Pcna`, `Ccna2`, `Top2a`, or apoptosis markers. |
| `E2f5` | 0 | 369 nominal genes but zero FDR genes; minimum adjusted p-value 1.0.  No corrected G1/S or p53-family marker response. |
| `Tfdp1` | 2 | Two focal FDR genes, consistent with only a tiny DP/E2F-axis footprint. |
| `Tfdp2` | 0 | Null focal count, arguing against broad dependence on the tested E2F DP partner branch. |
| `Myc` | 0 | Null focal count; Myc was a same-experiment E2F comparator in the corpus but not an RB/E2F phenocopy in this cell group. |
| `Trp53` | 0 | 384 nominal genes but zero FDR genes; minimum adjusted p-value 0.338.  `Cdkn1a`, `Mdm2`, `Bax`, and `Bbc3` were all nonsignificant. |
| `Trp63` | 0 | Null focal p53-family counterexample. |
| `Trp73` | 0 | Null focal p53-family counterexample. |
| `Atr` | 0 | Null DNA-damage/p53-axis count. |
| `Ep300` | 0 | Null p53/coactivator-axis count. |
| `Crebbp` | 8 | A small focal response but not a p53/RB signature-specific perturbation. |

`Rb1` itself is the direct pocket-protein target and was held out.  `Rbl1`, `Rbl2`, `E2f2`, `E2f3`, `E2f4`, `E2f6`, `E2f7`, `E2f8`, `Cdk4`, `Cdk6`, and `Ccnd1/2/3` were not represented in the focal training endpoint table, so they could not be used as observed training perturbations.

# Rb1 reasoning

The external prior makes `Rb1` a plausible nonzero gene in many proliferating or stress-challenged cells: pRB represses activating E2F transcription factors, CDK4/6 phosphorylation relieves RB repression, and RB loss can induce E2F-dependent S-phase, checkpoint, and apoptotic genes.  Conditional or developmental CNS studies also show that the RB/E2F module can matter in neural lineages: Rb-pathway activation appears in damaged dopaminergic neurons, Fas-stressed cerebellar neurons, Rb1-deleted POMC neurons, and embryonic Nes-Cre;Rb1 loss, with E2F1- or Skp2-modulated cell-cycle/apoptotic outcomes in those settings.

The causal chain for the requested experiment is:

`Rb1` CRISPR loss -> less pRB repression of E2F-bound promoters -> possible G1/S, DNA-replication, ARF/p53, or apoptosis transcription -> selection and survival of postnatal thalamic glutamatergic nuclei -> snRNA-seq Wilcoxon DEGs in recovered `151 TH Prkcd Grin2c Glut` cells.

The same-experiment transfer evidence weakens the nonzero prior at the last two steps of that chain.  These cells were assayed 3-4 weeks after sparse P16 AAV CRISPR in a healthy postmitotic neuronal context, not under DNA damage, oncogenic drive, ischemia, dopamine toxicity, a high-fat hypothalamic state, or embryonic neural progenitor stress.  In the actual training data:

- `Cdkn2a` loss is the closest represented upstream same-direction intervention because p16INK4a normally inhibits CDK4/6 and thereby favors unphosphorylated active RB.  Removing it should move toward RB/E2F release when the checkpoint is engaged, yet it caused `n_degs = 0` and did not derepress `Pcna`, `Mki67`, `Mcm`/S-phase, `Top2a`, p53-effector, or SASP-like genes.
- `E2f1` and `E2f5` losses are not the same sign as RB loss, but they test whether the downstream E2F transcriptional layer is tonically active and easily read out.  Both were focal nulls, and the corpus described `E2f1` as pan-neuronal FDR-null with no canonical DNA-replication/mitotic/apoptotic program and `E2f5` as lacking E2F/DREAM G1/S derepression.
- `Tfdp1` and `Tfdp2`, the directly assayed E2F/DP partner branch, produced two and zero DEGs respectively rather than a broad coordinated state.  The same-experiment `E2f1` corpus report specifically used them as comparators and found that measured E2F/DP relatives did not converge on a hidden E2F module.
- `Trp53`, `Trp63`, `Trp73`, `Atr`, and `Ep300` were null in the focal count table.  The `Trp53` report found no pan-atlas p53 target-gene response, supporting the idea that recovered healthy juvenile neurons were not already in a p53-active damage or apoptosis state.
- A positive-control boundary exists: unrelated active regulators such as `Sin3a`, `Zbtb7a`, `Psmb4`, `Ctnnb1`, `Setd1a`, and `Brd4` produced hundreds to thousands of focal DEGs, so the RB-axis nulls are not explained by a generally powerless cell group.

I therefore predict no FDR 0.05 genes for `Rb1` in `151 TH Prkcd Grin2c Glut`.

# Limits

The largest uncertainty is that `Rb1` knockout is mechanistically stronger and more direct than `Cdkn2a` knockout.  A postmitotic neuron could require RB itself, while p16INK4a, E2F1, or E2F5 single loss remains buffered by RB-family proteins, repressive E2Fs, DREAM, or absent cyclin/CDK drive.  `Rbl1`, `Rbl2`, and several E2F genes were absent as perturbation targets, so the parquet does not contain direct pocket-protein redundancy tests.  The snRNA-seq readout is also survivor-conditioned: if the small edited `Rb1`-null fraction were eliminated before harvest, later recovered nuclei could look transcriptionally quiet.  Those caveats make the prediction uncertain, but the training data give more support to an inactive or buffered basal RB/E2F axis than to a broad focal response.
