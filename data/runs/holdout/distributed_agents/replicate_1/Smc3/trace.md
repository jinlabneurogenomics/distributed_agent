# Smc3 DEG-count prediction

## Question and endpoint

I treated the requested value as a point prediction for the number of genes that would pass `pvals_adj < 0.05` in `151 TH Prkcd Grin2c Glut` nuclei after an acute AAV-CRISPR loss-of-function perturbation of each held-out target. `151 TH Prkcd Grin2c Glut` was treated as the exact focal thalamic glutamatergic cell group. The output unit is an assay- and power-dependent DEG count, not a direct viability, editing, or importance score.

Only one target was requested:

| target_name | prediction |
|---|---:|
| Smc3 | 31 |

## Sources used

- Requested-target CSV: `single-target request for Smc3`.
- Focal training endpoint: `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
- Training differential-expression parquet: `training differential-expression dataset`.
- Cached target-level Perturb-seq feature summary from `dataset.perturbseq_features summarize`, written to `evidence/features.parquet`.
- Same-experiment PerturbAI July release `perturbai-july-260713-sourceguard-1773-v1`, used only as a packaged interpretation of the model-visible DE dataset, specifically the resolved `Smc1a`, `Stag2`, and `Pds5a` evidence reports.
- External mechanism references from the report package and PubMed:
  - Rittenhouse and Dowen 2024, cohesin regulation and chromosome structure/function review, PubMed 38382406.
  - Nasmyth et al. 2023, cohesin retention/release structural model, doi:10.7554/eLife.88656, PubMed 37975572.
  - Calderon et al. 2022, Rad21 depletion in postmitotic mouse neurons, doi:10.7554/eLife.76539, PubMed 35471149.
  - Fujita et al. 2017, decreased Smc3/cohesin in mouse brain, doi:10.1084/jem.20161517, PubMed 28408410.
  - Deardorff et al. 2012, HDAC8 and the SMC3 acetylation cycle, doi:10.1038/nature11316, PubMed 22885700.
  - Ansari et al. 2024, human SMC3 predicted loss-of-function variants, doi:10.1016/j.xhgg.2024.100273, PubMed 38297832.
  - Mouse Genome Informatics, NCBI Gene, and GeneReviews annotations cited inside the same-experiment reports for the identities of the mouse cohesin genes and human cohesinopathy genes.

## Quantitative checks over the supplied data

The requested `Smc3` row was not present in the training endpoint CSV and did not appear as a `gene_target` in the summarized training parquet features, as expected for a held-out perturbation.

The focal training-count distribution was highly sparse:

| statistic | value |
|---|---:|
| training perturbations | 1,674 |
| median `n_degs` | 0 |
| 90th percentile | 2 |
| 95th percentile | 18 |
| 99th percentile | 430 |
| maximum | 2,677 |

I used the advertised Perturb-seq feature summarizer rather than reimplementing a whole-parquet aggregation. Its cache summary covered all 616,253,184 visible DE rows and produced 1,674 target-level feature rows with FDR-burden and log-fold-change distribution fields. The all-cell FDR 0.05 burden recapitulated the focal cohesin comparators: `Smc1a` had 25 total FDR 0.05 DE rows across all visible cell groups and 24 in `151 TH Prkcd Grin2c Glut`; `Stag2` had 37 total and 37 in the focal group; `Pds5a`, `Stag1`, and `Hdac8` had 0 total at FDR 0.05.

For focal expression-pattern evidence I filtered the parquet to `group_name == "151 TH Prkcd Grin2c Glut"` and `gene_target in {"Smc1a","Stag2","Pds5a","Stag1","Hdac8"}`. Among measured cohesin-adjacent training perturbations, the observed focal FDR 0.05 counts were:

| training perturbation | focal `n_degs` | all-cell FDR 0.05 rows | interpretation for Smc3 |
|---|---:|---:|---|
| `Smc1a` | 24 | 25 | Best core structural comparator. SMC1A and SMC3 are the two SMC ATPase arms of the same cohesin ring, bridged by RAD21/SCC1; impairing either should reduce the same limiting cohesin function in postmitotic neurons. |
| `Stag2` | 37 | 37 | A positive same-complex comparator. STAG2 is a non-SMC cohesin subunit and showed a larger but still tens-scale version of the thalamic cohesin-like response. |
| `Stag1` | 0 | 0 | Counterexample. STAG1 is the alternative SA/STAG cohesin subunit and is partly redundant with STAG2, so its lack of a focal response argues against blindly transferring to all cohesin-associated genes but does not break the SMC3-to-SMC1A core transfer. |
| `Pds5a` | 0 | 0 | Counterexample. PDS5A regulates release/stabilization and can be buffered by PDS5B or act differently by cell state; its absence of a thalamic response makes accessory-regulator transfer weak. |
| `Hdac8` | 0 | 0 | Counterexample. HDAC8 deacetylates SMC3 during the cohesin cycle, but perturbing the deacetylase is mechanistically opposite from removing the SMC3 structural arm and was silent in this AAV neuronal assay. |

`Smc1a` and `Stag2` also shared a same-direction focal expression pattern, not merely a nonzero count. At FDR 0.05, 9 of the 24 `Smc1a` DEGs were also in the 37 `Stag2` DEGs, all with the same sign: `Adamts19`, `Adamts2`, `Inhbb`, `Necab2`, `Ptprm`, `Sema5a`, `Smtn`, `Sox13`, and `Utp14b`. The focal log-fold-change vectors for `Smc1a` and `Stag2` over 17,259 shared measured genes had Pearson correlation 0.658. The packaged same-experiment corpus reported the same relationship at a slightly looser FDR 0.10 boundary: 14 same-direction overlaps between the `Smc1a` and `Stag2` thalamic signatures, with `Stag2` the top same-direction neighbor of `Smc1a` and `Smc1a` the top restricted-signature neighbor of `Stag2`.

These same-experiment statistics set the scale. The appropriate positive comparators lie at 24 and 37 focal DEGs, just above the 95th percentile of the training-count distribution, and no core cohesin analog in the visible training set supports a hundred-gene or thousand-gene prediction.

## Causal transfer from the observed perturbations to Smc3

The transfer model was:

`Smc3 CRISPR loss of function -> reduced functional SMC3 cohesin arm -> impaired SMC1A-SMC3-RAD21 cohesin ring loading/loop extrusion/gene regulation -> altered expression of a small adhesion, guidance, calcium/NMDA, and synaptic thalamic program in recovered postnatal neurons -> Wilcoxon FDR 0.05 DEG count in the recovered 151 TH Prkcd Grin2c Glut nuclei`.

This model has the same causal sign for `Smc3` and `Smc1a`: each encodes an obligate SMC component of the cohesin ring. Structural and biochemical reviews describe cohesin as a tripartite ring containing SMC1 and SMC3 ATPase heads joined by RAD21/SCC1, with STAG/SA and NIPBL/SCC2 regulating chromatin association and loop extrusion. SMC3 loss should therefore remove the same limiting molecular machine as SMC1A loss rather than acting through an unrelated pathway. The Rad21-depletion study in immature postmitotic mouse neurons by Calderon et al. further supports that reducing cohesin after neuronal differentiation can down-regulate genes involved in synaptic transmission, adhesion/connectivity, signaling, and activity-regulated programs rather than acting only through cell division. Fujita et al. showed that reduced Smc3/cohesin dosage in mouse brain is sufficient to alter cortical expression and synapse maturation, and Ansari et al. reported human SMC3 loss-of-function intolerance with variable developmental phenotypes, confirming that SMC3 haploinsufficiency can matter biologically.

The counterexamples were candidate-specific rather than graph-level. `Stag1` has an alternative STAG paralog, so lack of response there is compatible with redundancy. `Pds5a` and `Hdac8` alter cohesin cycling rather than directly removing an SMC arm; HDAC8 loss affects SMC3 deacetylation and may have the opposite persistence/release consequence from SMC3 loss. They bound how far a generic cohesin-pathway analogy can be trusted, but they do not outweigh the direct SMC1A-SMC3 relationship.

## Target-specific prediction

### Smc3

I predicted a nonzero focal response because `Smc3` is the missing obligate partner of the strongest available same-complex comparator, `Smc1a`, and the observed `Smc1a` thalamic signature is recapitulated by `Stag2` with the same direction for the overlapping genes. The requested `Smc3` endpoint is absent from the declared inputs; the supplied inputs directly observe the DEG endpoint for `Smc1a` and `Stag2`, which I used as mechanistically matched proxy evidence.

For the point estimate I centered the response on the two positive structural comparators, 24 for `Smc1a` and 37 for `Stag2`. The midpoint is 30.5, and I rounded to 31. I did not expand toward `Ctcf`, `Brd4`, `Elp1`, or `Ctnnb1` despite partial same-direction overlaps, because those are broader chromatin or signaling perturbations with hundreds of focal DEGs and only share a subset of the cohesin-like thalamic module. I did not collapse to zero based on `Stag1`, `Pds5a`, or `Hdac8`, because each has a candidate-specific redundancy, accessory, or opposite-cycle interpretation that makes it a weaker causal proxy for the core SMC3 arm.

## Limits

- The exact `Smc3` perturbation was held out, so its guide performance, recovered perturbed-cell count, and focal DE signature are absent from the declared inputs.
- The `Smc1a`/`Stag2` transfer is same-experiment proxy evidence, not independent replication. It is strong for the existence and rough size of a cohesin-like thalamic response, but it cannot fix the exact FDR threshold crossing count for `Smc3`.
- The visible dataset lacks `Rad21`, `Nipbl`, `Mau2`, `Wapl`, `Pds5b`, `Esco1`, and `Esco2` perturbations, so the SMC3 prediction cannot be triangulated against the full loading, release, and acetylation cycle.
- Germline, conditional, cell-culture, and human cohesinopathy studies establish that SMC3 is a dosage-sensitive core cohesin gene, but they differ from an acute postnatal sparse AAV-CRISPR perturbation in mouse thalamic glutamatergic neurons.
- DEG burden is discrete and power-dependent. A prediction of 31 should be read as a tens-scale response near `Smc1a` and `Stag2`, not as a claim that exactly those 31 genes or the exact hidden count are mechanistically determined.
