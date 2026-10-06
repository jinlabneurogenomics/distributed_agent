# Supt16 forecast for `151 TH Prkcd Grin2c Glut`

## Target and endpoint

- **Target:** `Supt16`, from the declared one-row holdout manifest.
- **Endpoint:** `n_degs`, the number of measured genes with BH-adjusted Wilcoxon `pvals_adj < 0.05` in `151 TH Prkcd Grin2c Glut`.
- **Outcome availability:** the declared training count table and expression parquet exclude the Supt16 endpoint and Supt16 expression signature. The selected same-experiment corpus had no Supt16 Finding or Claim record, so the prediction did not use a packaged Supt16 report.

## Target biology used

The biology-only Supt16 bundle says that Supt16 encodes the large SPT16 subunit of the SSRP1-SPT16 FACT histone-chaperone complex. FACT is a dynamic chromatin/transcription complex rather than a one-time developmental determinant, so loss of new SPT16 synthesis is plausibly relevant in P16-to-P37/P44 postmitotic neurons.

The focal expression reach is compatible with perturbing the intended state: in matched non-target nuclei from `151 TH Prkcd Grin2c Glut`, Supt16 was measured and expressed in 11,857 of 23,679 nuclei, with `pct_cells_expressing = 50.07`, `mean_raw_umi = 0.759`, `mean_log1p_cp10k = 0.317`, and `pseudobulk_cpm = 47.59`.

The same bundle argues for **partial depletion or a leading edge of functional-stock loss** by harvest. A disruptive edit should stop production of intact SPT16, and no close Supt16 paralog was found; however, pre-edit FACT complexes can initially persist, SPT16 stability is partner- and context-dependent, and the card has no direct half-life measurement in postmitotic mouse thalamic neurons. I therefore treated Supt16 as likely above the screen-wide null prior but below the very largest acute RNA-processing or chromatin-regulatory responses.

## Training measurements used

The focal training count table contains 1,674 measured perturbations:

- median `n_degs`: 0
- 75th percentile: 1
- 90th percentile: 2
- 95th percentile: 18
- 99th percentile: 430
- mean: 14.05
- zeros: 1,205 / 1,674

That distribution makes the default prior extremely quiet, but it has a long high-response tail. The closest literal FACT partner, `Ssrp1`, was not present in the training count table, so I used measured chromatin/transcription perturbations as imperfect quantitative brackets.

The focal-class counts and parquet profiles for the selected analog bracket were:

| measured perturbation | rationale for comparison | `n_degs` |
|---|---|---:|
| `Bptf` | chromatin remodeler with postmitotic caudal/thalamic response | 65 |
| `Chd8` | chromatin regulator with restricted thalamic/midbrain activity | 61 |
| `Chd4` | active ATP-dependent chromatin/NuRD remodeler in the same class | 100 |
| `Brd4` | chromatin reader tied to Pol-II elongation | 311 |
| `Setd1a` | broad H3K4/COMPASS transcriptional regulator | 368 |
| `Wac` | transcription-coupled H2B-ubiquitination / RNA-adjacent bracket | 384 |
| `Thoc1` | RNA-export/processing bracket, stronger than expected for FACT | 303 |
| `Cdc40` | spliceosome bracket, much stronger than expected for FACT | 624 |

The profile comparison over the expression parquet used exactly these nodes and the focal `151 TH Prkcd Grin2c Glut` context. It reproduced the focal counts above and showed all eight were genuine active responses in this cell class. The significant up/down splits were:

- `Bptf`: 22 up, 43 down
- `Chd8`: 22 up, 39 down
- `Chd4`: 52 up, 48 down
- `Brd4`: 61 up, 250 down
- `Setd1a`: 69 up, 299 down
- `Wac`: 168 up, 216 down
- `Thoc1`: 233 up, 70 down
- `Cdc40`: 446 up, 178 down

The selected reports also argued against pooling all chromatin genes as one signature family: Brd4, Wac, and Setd1a only partially overlapped Bptf despite larger signatures, Chd4/Chd8/BAF-family comparisons can diverge or oppose one another, and RNA-processing factors such as Cdc40 are broader secondary stress states rather than direct FACT analogs. The expression-profile comparison was consistent with that boundary: selected pairs had high whole-profile background correlation but small same-direction intersections among FDR-significant features, so I used the counts as scale brackets rather than as a transferable module.

## Synthesis

The data most strongly support an active but not extreme forecast:

- Supt16 is detectably expressed in the focal thalamic population and FACT has no close SPT16-replacing paralog, pushing the estimate well above the screen-wide zero/one-gene mass.
- The relevant measured chromatin perturbations that were active but not enormous in the same class landed at 61, 65, and 100 DEGs, giving a natural local anchor around 75.
- Fully exposed basal transcription/RNA-processing perturbations reached 300 to 600+ DEGs in the same class; Supt16 could in principle move toward that range because FACT couples to Pol-II chromatin passage, but the bundle's partial-stock adjudication and lack of a neuronal timing anchor argue against treating it like Cdc40, Thoc1, Setd1a, Wac, or Brd4.
- The final point estimate therefore sits slightly above the small active-chromatin trio to reflect no close paralog and ongoing FACT renewal demand, but far below the broad RNA-processing tail.

**Predicted `n_degs`: 80**
