# Grip1 DEG-count prediction for 151 TH Prkcd Grin2c Glut

## Question and resolved ambiguities

The requested held-out readout is the integer `n_degs` for each held-out perturbation in `151 TH Prkcd Grin2c Glut`: the number of measured genes with Scanpy/Wilcoxon Benjamini-Hochberg adjusted `pvals_adj < 0.05` after sparse postnatal AAV-CRISPR loss of function, compared with matched non-targeting controls. The only target in this shard is `Grip1`, which is absent as a `gene_target` from the supplied Parquet and absent from the training count table.

I treated the self-transcript as countable if it would pass FDR, because the endpoint counts all measured genes. I did not treat weak self-knockdown in related targets as failed editing: the dataset portrait notes that measured nuclear target RNA is not a calibrated editing-efficiency readout in this CRISPR design.

## Sources

- Declared endpoint table: `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
- Declared DE Parquet: `training differential-expression dataset`.
- Requested-target CSV: `single-target request for Grip1`.
- Run-local dataset portrait, task bindings, compact corpus coverage, capability manifest, and measurement registry.
- Internal same-experiment corpus: `perturbai-july-260713-sourceguard-1773-v1`. Its `Grip1` BioKG target query returned no `Grip1` findings, so I used the corpus only for narrow packaged interpretations of measured postsynaptic comparators (`Gria1`, `Dlg4`, `Grin1`, `Shank3`, `Syngap1`). Those reports are a semantic representation of the same experiment, not independent replication.
- External literature resolved through PubMed and through references packaged in the internal corpus: Sheng and Kim 2011, PMID 22046028; Diering and Huganir 2018, doi:10.1016/j.neuron.2018.10.018; Mao et al. 2010, doi:10.1073/pnas.1013494107; Hoogenraad et al. 2005, doi:10.1038/nn1487; Pfennig et al. 2017, doi:10.1016/j.celrep.2017.09.019; Tan et al. 2020, doi:10.1073/pnas.2014827117.

I did not use the ranking-only `dataset.perturbseq_features`, `synthesis.ordering_validate`, or `corpus.predictive_graph_review` capabilities because this task asks for a scalar count, not a supervised ranked output.

## Quantitative calibration

The 151-class training table contains 1,674 non-held-out targets, with no duplicate `target_name` values. The distribution is sharply zero-inflated:

| statistic | n_degs |
| --- | ---: |
| fraction equal to 0 | 0.720 |
| median | 0 |
| 75th percentile | 1 |
| 90th percentile | 2 |
| 95th percentile | 18 |
| maximum | 2677 |

I filtered the Parquet to `group_name == "151 TH Prkcd Grin2c Glut"` for 31 biologically adjacent AMPA, NMDA, PSD, adhesion, and trafficking training targets, then recomputed `(pvals_adj < 0.05).sum()` per `gene_target`. The recomputed counts matched the supplied CSV exactly for this analog set, confirming that the table and Parquet were aligned to the same endpoint.

The focal counts for GRIP1-relevant perturbations were:

| training target | 151 TH count | 151 FDR<0.05 genes and pattern |
| --- | ---: | --- |
| `Gria1` | 0 | no DEG; best adjusted p was 0.246 |
| `Gria2` | 0 | no DEG; all adjusted p values were 1 |
| `Gria3` | 0 | no DEG; `Gria3` self logFC -0.413 but FDR 0.971 |
| `Cacng2`, `Cacng3` | 0, 0 | AMPAR auxiliary targets were flat by the training counts |
| `Grid1`, `Grid2` | 1, 0 | `Grid1` was self only; no broad downstream glutamate-receptor response |
| `Grik1`, `Grik3`, `Grik4`, `Grik5` | 0, 0, 0, 1 | `Grik5` was self only |
| `Grin1` | 89 | clear exception; a GluN1/NMDAR loss signature with `Scg2`, `Stmn4`, `Kctd16`, `Gpm6a`, `Tspan7`, and other downstream genes |
| `Grin2a`, `Grin2b`, `Grin2d`, `Grin3a` | 1, 2, 0, 0 | GluN2/3 subunits were self-only or nearly flat in 151; `Grin2b` added `Pianp` |
| `Dlg4` | 1 | PSD-95 self only |
| `Dlgap4` | 2 | self plus `Vgf` |
| `Shank2`, `Shank3` | 0, 2 | `Shank3` had self plus `Uba5`; `Shank2` had no DEG |
| `Homer2`, `Magi2`, `Syngap1` | 0, 0, 0 | no 151-class DEG |
| `Nlgn3`, `Nrxn1`, `Nrxn2`, `Nrxn3` | 1, 1, 0, 0 | `Nlgn3` and `Nrxn1` were self only |
| `Ephb1`, `Ephb2`, `Lrp8` | 0, 0, 0 | receptor systems reported in GRIP1 trafficking studies were flat in training |
| `Kif5a`, `Kif5c`, `Atad1` | 1, 1, 1 | weak or self-limited trafficking-adjacent counts |

Whole-transcriptome signed-score correlations among the closest focal analogs were also near zero: `Gria1` versus `Gria2` Spearman r = 0.013, `Gria1` versus `Gria3` r = 0.0069, `Gria1` versus `Dlg4` r = 0.0063, `Dlg4` versus `Shank3` r = 0.016, and `Dlg4` versus `Syngap1` r = 0.0046. These correlations are not a score for `Grip1`; they are a check that the measured AMPAR/PSD perturbations did not hide a shared subthreshold 151-class transcriptional state.

## Grip1 reasoning

GRIP1 is a multi-PDZ postsynaptic adaptor that binds AMPAR GluA2/GluA3 and controls receptor trafficking rather than being a transcription factor or RNA-processing component. Mao et al. showed that GRIP1/2 loss selectively impairs exocyst-dependent, activity-dependent AMPAR recycling without disrupting basal steady-state AMPAR trafficking. Hoogenraad et al. connected GRIP1 to KIF5-dependent dendritic transport of EphB receptors in cultured hippocampal neurons, Pfennig et al. placed GRIP1 in an ephrinB2/ApoER2 complex needed for activity-dependent AMPAR insertion, and Tan et al. found that neuronal Grip1 deletion impairs AMPAR accumulation during LTP and learning and memory. Those mechanisms all act through synaptic receptor localization, local protein complexes, and activity-dependent trafficking.

The best within-dataset analogs for that causal chain are therefore AMPAR subunits and postsynaptic scaffolding/trafficking adaptors, not generic large-response genes. In the same 151 thalamic glutamatergic class, `Gria1`, `Gria2`, and `Gria3` were all zero at FDR 0.05. The AMPAR auxiliary targets `Cacng2` and `Cacng3` were also zero in the training table. The PSD scaffolds that could propagate AMPAR trafficking changes into a postsynaptic state were almost all zero or self-only: `Dlg4` 1, `Dlgap4` 2, `Shank2` 0, `Shank3` 2, `Homer2` 0, `Magi2` 0, and `Syngap1` 0. Adhesion or receptor partners implicated in GRIP1-linked receptor delivery, such as `Ephb1`, `Ephb2`, and `Lrp8`, were also zero in the focal count table.

The main counterexample is `Grin1` with 89 DEGs, but that is an obligate GluN1 NMDA-receptor subunit. The same-experiment `Grin1` report emphasizes that GluN2 and GluN3 perturbations did not phenocopy GluN1, that non-NMDA ionotropic receptor perturbations had essentially no overlapping downstream FDR genes, and that the 151-class `Grin1` state joined membrane-trafficking and stress-like modules outside the receptor itself. Because GRIP1 is an AMPAR trafficking scaffold and AMPAR subunit loss was flat, the `Grin1` response is a mechanistic upper-bound/counterexample rather than a same-outcome prior for `Grip1`.

I therefore predict no FDR-significant 151-class DEG for `Grip1`. A value of 1 would be plausible if `Grip1` self-RNA happened to pass FDR, but several high-confidence synaptic genes in this local neighborhood (`Gria1`, `Gria2`, `Gria3`, `Shank2`, `Syngap1`, `Homer2`, `Magi2`) had no significant self or downstream gene in the focal class. The within-dataset evidence puts a near-null AMPAR/PSD scaffold response ahead of the external evidence for strong synaptic physiology.

## Limits

`Grip1` itself is completely held out, and the July same-experiment corpus had no direct `Grip1` report, so the prediction extrapolates from related perturbations rather than from a `Grip1` signature. The assay measures nuclear RNA in recovered neurons 3-4 weeks after sparse P16 editing; it cannot assay GRIP1 protein loss, AMPAR recycling, synaptic currents, spine morphology, LTP, or activity-evoked insertion. GRIP2 was not present as a focal 151-class count-table analog, and GRIP1/GRIP2 redundancy is protein-level and activity-dependent, so a silent snRNA-seq endpoint does not imply absent synaptic function. Finally, at the 0/1 boundary the self-transcript call is statistically idiosyncratic; the integer prediction of 0 mainly means that I do not expect a downstream FDR 0.05 program and that the self-transcript alone is not strong enough to force a nonzero point estimate.
