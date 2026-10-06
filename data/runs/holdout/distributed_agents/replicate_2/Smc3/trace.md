# Smc3 held-out DEG prediction

## Question and scope

The requested held-out perturbation was `Smc3`. I interpreted the endpoint as the exact scalar in
`151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`: the number of measured mouse genes with
`pvals_adj < 0.05` in the focal `151 TH Prkcd Grin2c Glut` neurons after acute AAV-CRISPR loss of
the target. The count includes the perturbed transcript itself if it passes the same FDR threshold.

`Smc3` was absent from both the differential-expression parquet and the focal training-count CSV, so
its count had to be inferred from same-assay non-held-out perturbations. I did not interpret weak
self-knockdown as a failed perturbation, because the screen is sparse, mosaic, and single-nucleus.

## Sources used

- Differential-expression parquet:
  `[local file: training_de_all_cell_groups.parquet]`.
- Focal-cell training counts:
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
- Requested-target manifest:
  `[local file: 214_Smc3.csv]`.
- Distributed Agents same-experiment semantic corpus `perturbai-july-260713-sourceguard-1773-v1`; I used `target_context`,
  `resolve_evidence`, and `candidate_set_topology` to audit curated reports and same-experiment Findings.
- Distributed Agents runtime profile comparison over the focal parquet rows for a cohesin/chromosome-architecture cohort.
- PubMed/NCBI literature:
  - Rittenhouse and Dowen 2024, `doi:10.1016/j.gde.2024.102159`, PMID 38382406.
  - Calderon et al. 2022, `doi:10.7554/eLife.76539`, PMID 35471149.
  - Deardorff et al. 2012, `doi:10.1038/nature11316`, PMID 22885700.
  - Casa et al. 2020, `doi:10.1101/gr.253211.119`.
  - Arruda et al. 2022, `doi:10.1186/s13072-022-00463-6`, PMID 35986423.

## Computations over the training data

I used the training CSV for the official `FDR < 0.05` endpoint and queried the parquet rows for the
focal group to verify the local expression patterns. DuckDB queries filtered
`group_name = '151 TH Prkcd Grin2c Glut'`, then either counted `pvals_adj < 0.05` by `gene_target`
or inspected overlaps among the significant gene sets of the relevant targets.

The focal parquet contains 28,891,566 rows: 1,674 training targets by 17,259 measured genes. The
focal training-count distribution is highly zero-inflated: 1,205 of 1,674 training targets have
zero DEGs, the median is 0, the 75th percentile is 1, the 95th percentile is 18, and only 59 targets
have at least 50 DEGs. Therefore a count near 30 is already a selected, above-95th-percentile
response in this endpoint, even though it is tiny beside stress/chromatin outliers such as `Uba5`.

The relevant focal `FDR < 0.05` counts were:

| training target | `n_degs` | role for `Smc3` |
| --- | ---: | --- |
| `Smc1a` | 24 | Obligatory SMC3 partner in the core cohesin ring; closest available core subunit. |
| `Stag2` | 37 | SA2 cohesin subunit; same-direction Smc1a neighbor in this cell group. |
| `Ctcf` | 270 | Chromatin-loop anchor comparator with a much broader, partly protocadherin-rich signature. |
| `Stag1` | 0 | SA1 paralog counterexample; no `FDR < 0.05` gene and only one `FDR < 0.10` singleton. |
| `Pds5a` | 0 | Cohesin-cycle accessory counterexample. |
| `Hdac8` | 0 | SMC3 deacetylase counterexample. |
| `Ncapd3` | 0 | SMC-family/condensin-II counterexample. |
| `Smchd1` | 0 | Noncanonical SMC-family chromatin-architecture counterexample. |
| `Prr12` | 0 | Cohesin-associated chromatin regulator counterexample. |

At `FDR < 0.05`, `Smc1a` and `Stag2` shared 9 significant genes and all 9 had the same direction:
`Adamts19`, `Adamts2`, `Inhbb`, `Necab2`, `Ptprm`, `Sema5a`, `Smtn`, `Sox13`, and `Utp14b`.
`Ctcf` shared only five significant rows with `Smc1a` and two with `Stag2` at this stricter cutoff.
`Stag1`, `Pds5a`, `Hdac8`, `Ncapd3`, `Smchd1`, and `Prr12` had no `FDR < 0.05` rows with which to
share a significant module.

The same pattern was present in the same-experiment Distributed Agents corpus at `FDR < 0.10`: `Smc1a:F003`
reported that `Stag2` was the strongest same-direction `Smc1a` neighbor in the focal group, sharing
14 of 34 downstream `Smc1a` genes, all in the same direction, while `Stag1`, `Pds5a`, `Hdac8`, and
`Ncapd3` were flat or divergent. Reciprocally, `Stag2:F004` reported a restricted-signature cosine
of 0.905 to `Smc1a` over the 55-gene `Stag2` signature, and `Stag2:F005` rejected `Stag1`, `Pds5a`,
and `Hdac8` as `Stag2` phenocopies.

## Target-specific reasoning

### `Smc3`

`SMC3` is not just in the same family as `SMC1A`; SMC3 and SMC1A form the V-shaped ATPase core of
cohesin with RAD21 and one SA/STAG subunit. Cohesin extrudes loops and organizes interphase
chromatin, and this loop architecture contributes to transcriptional control (Rittenhouse and Dowen
2024). In neurons, Rad21/cohesin depletion especially affects long-range loop-dependent synaptic,
adhesion, connectivity, and signaling genes rather than inducing a simple immediate-early-gene or
cell-cycle stress state (Calderon et al. 2022). That mechanism matches the focal assay's `Smc1a`
and `Stag2` modules, which were dominated by down-regulated adhesion, extracellular-matrix/guidance,
excitability, and neuronal-signaling transcripts such as `Ptprm`, `Sema5a`, `Adamts2`, `Adamts19`,
`Necab2`, `Grin2c`, and `Lrrc7`.

The best quantitative anchors are therefore:

- `Smc1a`, 24 DEGs at the requested `FDR < 0.05` endpoint. This is the direct core-ring analog. Its
  focal signature was mostly down-regulated, and 9 of its significant genes recurred in `Stag2` with
  the same sign.
- `Stag2`, 37 DEGs. This is not a core ATPase subunit but it independently recovered the same small
  151 TH thalamic cohesin module. Its larger 37-gene count sets the upper end of the appropriate
  compact-response range.
- `Ctcf`, 270 DEGs. CTCF is biologically connected to cohesin at loops, but in this screen it was a
  much broader responder with a dominant clustered-protocadherin component; only two `Stag2`
  `FDR < 0.05` genes and five `Smc1a` `FDR < 0.05` genes were also `Ctcf` significant in the focal
  group. I used `Ctcf` only as evidence that this cell group can report chromosome-architecture
  perturbations, not as a count anchor for `Smc3`.

The important counterexamples are:

- `Stag1`, 0 DEGs at `FDR < 0.05`, with only `Gabra1` reaching the looser `FDR < 0.10` threshold and
  with the opposite sign from the `Stag2` `Gabra1` call. STAG1 and STAG2 have overlapping but also
  separable chromatin-looping and gene-regulatory roles (Casa et al. 2020), and the assay strongly
  separated the SA1 and SA2 branches.
- `Pds5a`, 0 DEGs. PDS5 proteins affect cohesin regulation and SMC3 acetylation in embryonic stem
  cells (Arruda et al. 2022), but the same focal thalamic cells showed no FDR-supported response to
  `Pds5a`.
- `Hdac8`, 0 DEGs. HDAC8 deacetylates SMC3 and HDAC8 loss perturbs the cohesin acetylation cycle
  (Deardorff et al. 2012), yet `Hdac8` was flat in this acute postnatal neuronal readout.
- `Ncapd3`, `Smchd1`, and `Prr12`, all 0 DEGs, show that broader SMC-family or chromatin-architecture
  membership is insufficient for predicting a positive thalamic response.

These counterexamples keep the prediction from borrowing the 270-gene `Ctcf` scale or asserting that
any cohesin-cycle perturbation must fire. They do not erase the direct `Smc1a`/`Stag2` evidence,
because `Smc3` is an obligatory core-ring component rather than an SA paralog or a loading/release
regulator. STAG1/STAG2 redundancy in cycling cancer cells (van der Lelij et al. 2017) and differential
PDS5A/PDS5B gene-expression effects (Arruda et al. 2022) are also reminders that accessory or paralog
logic does not map one-to-one onto single-subunit acute neuronal CRISPR.

I predict `Smc3` will be nonzero and in the compact cohesin range bracketed by `Smc1a = 24` and
`Stag2 = 37`, not at zero and not at the `Ctcf` scale. The point estimate is the midpoint of those
two direct positive anchors, rounded to an integer: **31 DEGs**.

## Limits

This is still extrapolation. `Smc3`, `Rad21`, `Nipbl`, `Mau2`, `Wapl`, `Pds5b`, `Esco1`, and `Esco2`
were not available as training perturbations, so the prediction relies on `Smc1a` and `Stag2` plus
less-direct counterexamples. The training comparisons are all single-gene acute CRISPR perturbations
in recovered NeuN-positive nuclei; they do not measure indels, cohesin occupancy, SMC3 acetylation,
loop extrusion, cell loss, or glial phenotypes. A different effective guide set or stronger
survivor bias for `Smc3` could shift the final FDR count below `Smc1a` or above `Stag2` even if the
underlying target biology is core cohesin.
