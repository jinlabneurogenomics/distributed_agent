# Chrna5 direct forecast

## Target and endpoint

- Target: `Chrna5`
- Cell context: `151 TH Prkcd Grin2c Glut`
- Endpoint: number of measured genes with BH-adjusted Wilcoxon `pvals_adj < 0.05`.

The target perturbation profile and target count were held out. I used the
declared one-row manifest, the declared `151 TH Prkcd Grin2c Glut` training
count table, the declared training DE Parquet for selected observed
perturbations, the target biology-only bundle, and same-experiment Finding
records for measured non-target comparators.

## Biology bearing

The canonical biology bundle places Chrna5 in a low-reach, partial-realization
regime for this exact assay context:

- Exact focal-population reach was very sparse: in non-target `151 TH Prkcd
  Grin2c Glut` nuclei, Chrna5 had 180 total UMIs among 23,679 nuclei, 129
  expressing nuclei, `pct_cells_expressing = 0.5447865`, `mean_raw_umi =
  0.0076017`, and `pseudobulk_cpm = 0.4764`.
- Chrna5 encodes an accessory alpha5 subunit of assembled heteromeric nicotinic
  acetylcholine-gated channels, rather than a free soluble regulator or a core
  transcriptional component.
- The functional-stock card judged the P16-to-P37/P44 intervention as
  `partially_depleted_or_leading_edge`: editing should stop new alpha5 supply,
  but pre-existing alpha5-containing receptors can persist and exact
  alpha5-containing receptor turnover in postmitotic mouse thalamic neurons was
  not known.
- The observability evidence supported a real alpha5-dependent neural function
  in adult mouse thalamus or corticothalamic circuitry, but from germline adult
  physiology and behavior rather than a matched P16 mosaic CRISPR,
  NeuN-positive nuclear RNA readout.

That combination argues for biological reachability in the few cells that
carry the receptor, but weak bulk transcriptional visibility after aggregation
over this thalamic class.

## Training endpoint evidence

The declared `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` table is
zero-heavy for this endpoint: among 1,674 observed training perturbations,
1,205 had `n_degs = 0`, the median was 0, the 75th percentile was 1, the 90th
percentile was 2, and the mean was pulled upward to 14.05 by a long tail.

The represented cholinergic and nicotinic perturbations in the same count table
were nearly silent in this class:

| target | n_degs |
| --- | ---: |
| Chrna1 | 0 |
| Chrna2 | 0 |
| Chrna3 | 0 |
| Chrna4 | 2 |
| Chrna6 | 0 |
| Chrna7 | 0 |
| Chrnb1 | 0 |
| Chrnb2 | 1 |
| Chrnb3 | 0 |
| Chrnd | 0 |
| Chrne | 0 |
| Chrng | 0 |
| Chrm2 | 0 |
| Chrm3 | 0 |
| Ache | 1 |

Direct Parquet inspection in `151 TH Prkcd Grin2c Glut` showed that the few
nonzero family counts were not broad downstream states:

- `Chrna4`: 2 genes at `pvals_adj < 0.05`, its self transcript and `Cyp46a1`.
- `Chrnb2`: 1 gene at `pvals_adj < 0.05`, the self transcript.
- `Ache`: 1 gene at `pvals_adj < 0.05`, the self transcript.
- `Chrna3`, `Chrna7`, and `Chrm2`: 0 genes at `pvals_adj < 0.05`.

The same-experiment Chrna4 Finding records summarized the corresponding corpus
interpretation as an isolated `Cyp46a1` down-response in 151 TH and noted that
Chrnb2 plus other represented nicotinic relatives did not phenocopy it
(`Chrna4:F001`, `Chrna4:F003`). Chrnb2 Findings interpreted beta2 loss as a
self-transcript event with zero downstream genes across measured groups and no
convergent basal transcriptome among represented nAChR relatives. Chrna3,
Chrna7, Chrm2, and Ache Findings likewise described null or self-only
cholinergic receptor surfaces.

## Synthesis

Chrna5 is less compelling as a 151 TH bulk nuclear-RNA perturbation than the one
weakly positive alpha4 case: it is a lowly detected accessory subunit in the
focal population, its pre-edit membrane receptor stock may only be partly
depleted by harvest, and related principal nAChR or cholinergic perturbations
in the observed training table were overwhelmingly at 0 or self-only. Its
functional prior prevents treating the perturbation as a pure negative, but
there was no evidence for a multi-gene transcriptional program in this
cholinergic receptor neighborhood.

Point prediction: `n_degs = 0`.
