# Supt16 direct `n_degs` forecast

## Target and endpoint

- **Target:** `Supt16`, the single row in the declared `Supt16.csv` holdout manifest.
- **Endpoint:** number of measured genes in `151 TH Prkcd Grin2c Glut` with BH-adjusted Wilcoxon `pvals_adj < 0.05`.
- **Direct endpoint inputs used:** the declared training count table `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` and the declared `training_de_all_cell_groups.parquet`.
- **Held-out target status:** `Supt16` had no target-specific Finding, Claim, or explicit reference in the selected same-experiment corpus release, and the target count/signature were absent from the visible count table. I therefore used the biology bundle as the Supt16 prior and only used visible training perturbations for observed counts.

## Supt16 biology prior

The declared Supt16 bundle makes the perturbation biologically plausible but not a clear high-response case in this exact assay:

- Supt16 encodes the SPT16 subunit of the SSRP1-SPT16 FACT histone-chaperone complex, so loss of intact Supt16 should impair chromatin-coupled transcription once the operative complex is depleted.
- Exact 151-population reach is present but modest: in non-target cells, Supt16 was detected in 11,857 / 23,679 nuclei, 50.07%, with mean CP10K 0.471 and pseudobulk CPM 47.6. This is enough that the target is available in the assayed population, but it does not establish editing or protein depletion.
- The functional-stock adjudication concluded `partially_depleted_or_leading_edge`: editing should stop new intact SPT16 supply, but pre-existing FACT can initially persist; human-cell data show both qualitative FACT stability and partner-coupled SPT16 loss; no neuronal half-life anchors full depletion by P37-P44.
- The strongest direct mouse phenotype evidence is developmental haploinsufficiency/neural-stem-cell biology, not acute biallelic loss in postmitotic thalamic neurons.

This made me expect a real but attenuated transcriptional footprint rather than a large pan-chromatin collapse.

## Visible training analogs

I used the deterministic mouse gene-analog nominator on the 1,674-gene training universe. `Ssrp1`, the obligate FACT partner, was not in the visible count table, so there was no same-FACT-core donor with an observed 151 `n_degs`.

The bounded high-priority available nominees were mostly BAF/SWI-SNF chromatin remodeler subunits plus weaker projected or physical interactors:

| perturbation | relationship to Supt16 from analog nomination / corpus context | visible 151 `n_degs` |
| --- | --- | ---: |
| `Arid1a` | BAF/PBAF chromatin module | 22 |
| `Smarca4` | BAF/PBAF chromatin module, report-flat in 151 | 0 |
| `Ep300` | projected human HES1 promoter-Notch complex, broad transcription | 0 |
| `Smarcc1` | BAF/PBAF chromatin module, report-flat in 151 | 0 |
| `Smarcd1` | BAF/PBAF chromatin module, very weak 151 response | 1 |
| `Smarce1` | BAF/PBAF module; same-release Findings tie its restricted 151 response to `Smarcc2`, `Arid1a`, and `Arid2` | 11 |
| `Gtf2h5` | Pol II / TP53 DNA-repair transcription module | 0 |
| `Csnk2b` | projected UV-activated FACT-associated complex; observed response is CK2/RNA-processing and caudal-neuronal rather than a direct FACT phenocopy | 25 |
| `Crebbp` | broad transcription / VDR / HES1 promoter context | 8 |
| `Nek9` | projected FACT-NEK9 complex but a mitotic/ciliary kinase; same-release Findings report no downstream FDR<0.10 response in any recovered neuronal group | 0 |
| broader chromatin outliers (`Smarcc2`, `Arid2`, `Cdk13`, `Chd4`, `Brd4`, `Elp2`) | endpoint-active chromatin/transcription perturbations, but not direct FACT loss | 56-311 |

The analog cohort therefore bracketed Supt16 rather than supplying a single scale-matched donor. The top 20 nominated observed analogs had a median visible 151 count of 8.5; the first 10 had a median of 4.5; the represented BAF subset had a median of 6.0; the two FACT-projected accessory nodes were 25 and 0. The six most specific quiet/near-quiet nodes (`Smarca4`, `Ep300`, `Smarcc1`, `Smarcd1`, `Gtf2h5`, `Nek9`) had median 0.

## Profile evidence

I compared the 20-node analog cohort directly in the `151 TH Prkcd Grin2c Glut` Parquet slice with `logfoldchanges` as the signed value and `pvals_adj < 0.05` as the response definition. The profile comparison observed all 20 nodes and reproduced a split activity distribution: six no-DEG perturbations, five with 1-9 significant genes, three with 10-49, and six with at least 50.

The same-release explicit-Finding topology separated the BAF/PBAF component from isolated FACT-projected nodes:

- `Smarce1`, `Smarcc2`, `Arid1a`, `Arid2`, `Smarca2`, `Smarca4`, `Smarcc1`, and related BAF/NuRD nodes formed a dense report-referenced component.
- `Csnk2b` and `Nek9` were isolated in this supplied report graph; `Csnk2b`'s own Findings described CK2beta caudal/diencephalic RNA-processing and neuronal-morphology modules, while `Nek9` was a robust negative perturbation.
- High `Brd4`, `Elp2`, and `Chd4` counts represented broader or different chromatin machinery states rather than a direct same-complex FACT perturbation.

The Parquet profile cohort had weak positive-tail recurrence but stronger negative-tail background recurrence across the 20 nodes; that showed the large chromatin profiles share broad signed structure without producing a precise FACT-like donor. I therefore used their counts only as evidence that chromatin lesions can become visible in this class, not as a high-scale anchor for Supt16.

## Point synthesis

The declared Supt16 card supports some FACT functional-stock loss by harvest and exact target reach in 151 neurons, which argues against a hard zero. However, the endpoint projection is muted by persistent pre-edit FACT pools, no transferable timing anchor, only developmental mouse neural loss evidence, and the lack of a visible `Ssrp1` donor. The visible analogs closest by operation are mostly zero or single-digit; the double- to triple-digit chromatin responses come from broader BAF, NuRD, BRD, or Elongator perturbations with their own recurrent modules.

I therefore placed Supt16 just below the median of the full bounded chromatin analog cohort and near the upper edge of the closest low/narrow perturbations: a small but detectable 151 response.

Predicted `n_degs`: **8**
