# Fnip1 n_degs forecast

## Declared target and endpoint

- Target: `Fnip1`
- Focal class: `151 TH Prkcd Grin2c Glut`
- Endpoint: count of measured genes with BH-adjusted Wilcoxon `p < 0.05`
- Prediction: `3`

## Evidence used

### Biology-only Fnip1 bundle

Source: `[local file: Fnip1.json]`; SHA-256 `7d09e9cd854b9f97c779f611227617784192834ac3ba7c85109cbeb5e2f60c13`.

The target transcript is well represented in the focal control population: 17,909 of 23,679 non-target nuclei express `Fnip1`, or 75.63%, with mean CP10K 1.0198 and pseudobulk CPM 101.25. That makes the perturbation reachable in `151 TH Prkcd Grin2c Glut`, but it is only a reach measurement, not an editing-efficiency or outcome value.

The molecular prior is real but indirect for this assay. FNIP1 acts with FLCN and AMPK and as an Hsp90 co-chaperone, so a disruptive edit should stop new FNIP1 supply. Existing FNIP1-containing complexes are not directly inactivated, and the bundle found no quantitative FNIP1 half-life, FLCN-FNIP residence-time, or postmitotic-neuron clearance measurement over the 21-28 day P16-to-P37/P44 interval. Fnip2 overlap is known in non-neural systems but not quantified in juvenile thalamic neurons. The closest in-vivo loss phenotype is a B-cell developmental phenotype, not a postnatal neural loss experiment.

I therefore treated Fnip1 as expressed and plausibly perturbable, but not as guaranteed to enter a large lysosomal/metabolic RNA state by harvest.

### Training counts in the same focal class

Source: `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.

The count table contains 1,674 training perturbations. It is very zero-heavy: median 0, 75th percentile 1, 90th percentile 2, 95th percentile 18, and only 162/1,674 targets are above 2 DEGs.

The exact FLCN/FNIP core was not represented in the focal training counts: `Flcn`, `Fnip1`, and `Fnip2` were absent. The available same-axis perturbations were mostly quiet in `151 TH Prkcd Grin2c Glut`:

- TORC1/autophagy/metabolic nodes: `Mtor=2`, `Rptor=0`, `Tsc2=86`, `Depdc5=13`, `Akt3=0`, `Pik3r1=0`, `Prkaa2=0`, `Ywhaz=1`, `Becn1=0`, `Atg5=0`, `Atg16l1=0`, `Rb1cc1=4`
- Hsp90/protein-folding context: `Hsp90ab1=1`, `Hspa8=9`, `Hspa5=5`
- lysosomal/autophagy stress context: `Gaa=1`, `Lamp2=0`, `Sqstm1=1`, with `Vps35=17` and `Rab7=501` as broader trafficking/lysosomal upper-context perturbations

### Training-available analog nomination

Source artifact: `workbench/fnip1_analog_nominations.jsonl`, produced from the declared 1,674-gene training universe with the pinned mouse annotation store and `perturbai-july-260713-sourceguard-1773-v1` corpus release.

The nominator found no training-available `exact_complex_or_paralog`, `bidirectional_corpus_comparator`, `narrow_module`, or `direct_interaction_or_dependency` for `Fnip1`. It returned 1,280 broad functional fallback nominees. The top functional communities were ATPase inhibition, lysosome organization, TOR signaling, TORC1 signaling, and chaperone-binding/B-cell terms. I used those only to define a bounded inspection cohort, not as scalar weights.

The first biologically relevant training-available nominees were broad TORC1 and stress genes:

- `Mtor` rank 2, `n_degs=2`
- `Prkaa2` rank 4, `n_degs=0`
- `Tsc2` rank 6, `n_degs=86`
- `Rptor` rank 7, `n_degs=0`
- `Becn1` rank 10, `n_degs=0`
- `Pik3r1` rank 14, `n_degs=0`
- `Hsp90ab1` rank 15, `n_degs=1`
- `Akt3` rank 20, `n_degs=0`
- `Depdc5` rank 23, `n_degs=13`

The strongest top-ranked nominee, `Hdac5`, had `n_degs=0` and was an explicit-Finding isolate among the TORC1/autophagy cohort, so I treated it as an annotation side-effect rather than a useful Fnip1 comparator.

### Same-experiment corpus context

Source: selected July PerturbAI corpus, same experiment as the Parquet.

An explicit-Finding topology check over `Hdac5`, `Mtor`, `Gsk3b`, `Prkaa2`, `Ywhaz`, `Tsc2`, `Rptor`, `Becn1`, `Depdc5`, `Akt3`, `Pik3r1`, and `Atg5` yielded an 11-node TORC1/autophagy component and isolated `Hdac5`. `Mtor` and `Tsc2` were each connected to 10 of the other 11 nodes inside the supplied set; the topology was a report-derived audit of that bounded cohort, not an independent replicate.

Material Finding records pushed against a high transfer from `Tsc2` or other sterol/lysosome stress nodes:

- `Mtor:F005`: Rptor/Fkbp1a and upstream PI3K/AKT nodes did not phenocopy `Mtor` loss; the claim contribution states that basal juvenile neurons buffer or separate represented upstream PI3K/Akt and positive mTORC1-associated perturbations.
- `Tsc2:F007`: `Depdc5` partially matched `Tsc2`, `Srebf2` was branch-selective and opposite, while `Mtor`, `Rptor`, `Igf1r`, `Irs1`, and `Akt3` did not give a robust matched FDR overlap.
- `Atg5:F005`: `Atg5` was nearly flat while `Tsc2` produced a much broader sterol/lysosome transcriptomic response.

Together these reports indicate that same-pathway membership around mTOR/autophagy is not interchangeable at this basal neuronal RNA endpoint.

### Same-focal-profile check

Source artifact: `workbench/fnip1_profile_neighbors.json`, computed from `[local file: training_de_all_cell_groups.parquet]` in `151 TH Prkcd Grin2c Glut`.

The Parquet profile check used `Mtor`, `Tsc2`, `Rptor`, `Atg5`, `Becn1`, and `Prkaa2` as anchors against 18 FLCN/FNIP/TORC1/autophagy/chaperone/lysosome candidates. The exact profile counts matched the focal training table: `Mtor=2`, `Tsc2=86`, `Rptor=0`, `Atg5=0`, `Becn1=0`, and `Prkaa2=0`.

Important pairwise details:

- `Mtor` versus `Tsc2`: Pearson 0.6727, cosine 0.7320, but 0 shared positive significant genes out of 59 in the union and 0 shared negative significant genes out of 29.
- `Tsc2` versus `Rptor`: Pearson 0.6702, cosine 0.7279, with no shared significant positive or negative genes.
- `Tsc2` versus `Becn1`: no shared significant program despite broad negative-tail overlap.
- `Atg5`/`Becn1`/`Prkaa2` and several low-count PI3K/autophagy nodes formed a whole-profile component, whereas `Mtor`, `Tsc2`, `Rptor`, `Rab7`, `Psmb4`, and the Hsp90 nodes were isolates in the whole-profile Pearson/cosine topology.

Thus the large `Tsc2`, `Rab7`, and `Psmb4` counts look like endpoint-visible but mechanistically broader or opposite stress states, while the more direct positive TORC1/autophagy/Hsp90 candidates stay at zero to single digits.

## Synthesis

I forecast a low nonzero count rather than a zero. The upward evidence is strong focal `Fnip1` expression and a dynamic, regulated FNIP1 protein that can in principle turn over during the 3-4 week assay. The downward evidence is stronger for magnitude: Fnip1 has no exact measured donor; the characterized functional stock by harvest is indeterminate; Fnip2 buffering is unresolved; direct positive mTORC1 and autophagy perturbations in the same thalamic class are flat or nearly flat; and the only high same-axis rows are not scale-matched FLCN/FNIP loss analogues.

A point of `3` keeps Fnip1 just above the training-table 90th percentile, reflecting target reach and nonzero biological plausibility, but far below `Tsc2`, `Rab7`, or proteasome-like stress programs because those are broader or directionally different endpoints.
