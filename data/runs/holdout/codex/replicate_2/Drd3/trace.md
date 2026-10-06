# Drd3 direct n_degs forecast

## Target and endpoint

- Target: `Drd3`
- Focal population: `151 TH Prkcd Grin2c Glut`
- Endpoint: measured genes in the focal population with Wilcoxon BH-adjusted `p < 0.05`
- Point forecast: `0`

The holdout manifest and biology bundle both resolve the one requested perturbation to `Drd3`. `Drd3` is absent from the declared training count table, and I did not query or reconstruct a held-out Drd3 perturbation signature.

## Evidence used

### Biology-only Drd3 bundle

`distributed_agents_runtime.characterization_bundle(target="Drd3", view="biology")` served the canonical Drd3 biology bundle with `target_outcome_exposed=false` and `labeled_neighbors_exposed=false`.

Material fields:

- Drd3 is a seven-transmembrane dopamine receptor coupled to Gi/Go signaling at the plasma membrane and dopaminergic synapses.
- The focal population has exact but low target reach: 961 of 23,679 non-target nuclei express `Drd3`, or 4.06%; pseudobulk abundance is 4.99 CPM.
- Loss of new `Drd3` transcription stops new receptor supply but does not immediately disable pre-existing DRD3 protein.
- DRD3 can be endocytosed and lysosomally degraded under PKC stimulation, but no basal DRD3 protein half-life or post-edit clearance curve in postmitotic mouse neurons was found.
- Adult germline D3-receptor-deficient mice have neural behavioral phenotypes, so Drd3 is not a generic biological null; however, those data do not match acute P16 editing, P37-P44 thalamic nuclei, or survivor-conditioned snRNA-seq.
- DRD2 is the closest paralog and D2/D3 receptors can overlap functionally, but acute Drd3 compensation in thalamus is untested.

This made a large 151-TH aggregate transcriptional footprint unlikely: only a small fraction of the assayed nuclei have detectable target RNA, the amount of functional receptor removed by 21-28 days is unresolved, and the best positive phenotype evidence is germline/adult rather than matched to the assay.

### Training count table

The declared count table contains 1,674 measured training perturbations for `151 TH Prkcd Grin2c Glut`. Its empirical response scale is very sparse:

- 1,205 / 1,674 training targets have `n_degs = 0`
- 1,481 / 1,674 have `n_degs <= 1`
- median = 0
- 75th percentile = 1
- 90th percentile = 2

The closest obvious dopamine-receptor comparators are all silent in this same focal population:

| comparator | n_degs |
| --- | ---: |
| Drd2 | 0 |
| Drd4 | 0 |
| Drd5 | 0 |

Nearby neuromodulatory GPCRs and dopamine/cAMP effectors also cluster at zero. In the Drd3 analog nomination's first 20 training-available candidates, `Gnas`, `Htr1b`, `Htr2c`, `Htr2a`, `Adcy5`, `Htr6`, `Htr4`, `Htr2b`, `Adra2a`, `Adrb2`, `Adcy1`, and `Gnal` all had `n_degs = 0`; `Gnao1` and broad fallback `Dlg4` had `n_degs = 1`. The larger broad-fallback counts for `Atp1a3` and `Vps35` were not operation-scale dopamine-receptor analogues, so I did not use them as scale setters.

### Typed analog nomination and corpus checks

I ran the species-safe, training-universe-filtered analog nominator for `Drd3`. In the full 1,408-candidate JSONL artifact, the top training-available candidates were:

| rank | candidate | typed basis |
| ---: | --- | --- |
| 1 | Drd2 | closest Gi/Go dopamine-receptor annotation / D2-family |
| 2 | Drd4 | Gi/Go dopamine receptor and Reactome dopamine-receptor module |
| 3 | Drd5 | dopamine-receptor module |

The induced same-experiment explicit-Finding topology over `Drd2`, `Drd4`, and `Drd5` was fully connected and reciprocal. This is not independent replication of the Parquet, but it showed that the three dopamine-receptor comparators were a coherent report-interpreted set rather than a symbol-prefix-only selection.

The same-experiment Findings for these visible training perturbations were also uniformly quiet:

- `Drd4`: taxonomy-wide FDR-clean neuronal transcriptomic null; no cAMP, immediate-early, NMDA/AMPA, or GABA mRNA program.
- `Drd5`: transcriptionally silent in every recovered neuronal group, with zero downstream genes at FDR < 0.10.
- `Drd2`: one-gene cortical response only, no expected basal cAMP/immediate-early or indirect-pathway/autoreceptor marker panels, and no strong genome-scale signature neighbor.

### Focal Parquet and profile review

A focused Parquet query of the declared training DE table in `151 TH Prkcd Grin2c Glut` verified that each profiled dopamine/cAMP/monoamine comparator had 17,259 measured genes. The three D2-family dopamine receptors had no borderline focal signal:

| comparator | focal n_degs | minimum adjusted p |
| --- | ---: | ---: |
| Drd2 | 0 | 1.0 |
| Drd4 | 0 | 1.0 |
| Drd5 | 0 | 1.0 |

In the same query, `Adcy1`, `Adcy3`, `Adcy5`, `Gnas`, `Gnal`, `Htr1b`, `Htr2a`, and `Htr2c` also had `focal n_degs = 0`.

I then symmetrically compared the focal expression profiles of `Drd2`, `Drd4`, `Drd5`, `Adcy1`, `Adcy3`, `Adcy5`, `Gnas`, `Gnal`, `Htr1b`, `Htr2a`, and `Htr2c`. All 11 nodes had `response_activity_status = no_significant_features`. The `Drd2`/`Drd4`/`Drd5` pairwise comparisons had no significant positive or negative program overlap because every side had zero significant genes. Their nearest eligible whole-profile neighbors were generic quiet perturbations rather than a responsive dopamine-like module.

## Synthesis

The endpoint itself is a sparse count in this cell class, so the training-count prior already favors zero. Drd3 was then pushed further toward zero by three concordant observations:

1. the exact Drd3 reach is only about 4% of non-target nuclei in the aggregated 151-TH population;
2. installed DRD3 receptor may persist for an unknown portion of the 21-28 day post-edit window; and
3. every direct dopamine-receptor comparator available in training, including the closest D2-family receptors, had `n_degs = 0` in this focal population and showed no borderline adjusted-p signal in the Parquet.

The main upward uncertainty is that Drd3 is biologically active in mouse brain and a small one-gene survivor-state response is possible for low-yield neuronal GPCR perturbations. I still placed the integer forecast at zero because the matched receptor and monoamine/cAMP observations were consistently silent, while the nonzero analog-nominator hits came from broader pathway annotations rather than a Drd3-like operation.
