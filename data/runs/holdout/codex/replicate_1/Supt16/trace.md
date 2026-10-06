# Direct outcome-blind forecast

## Target and endpoint

- Target: `Supt16`
- Cell class: `151 TH Prkcd Grin2c Glut`
- Endpoint: number of measured genes with Wilcoxon `pvals_adj < 0.05`
- Declared measured training endpoint: `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`
- Declared DE profiles: `training_de_all_cell_groups.parquet`, filtered only to `group_name == "151 TH Prkcd Grin2c Glut"` for profile checks

`Supt16` is withheld from the training count table and from the training Parquet. The selected same-experiment corpus release also has no `Supt16` Findings, Claims, or explicit report references, so no packaged same-experiment Supt16 outcome was used.

## Supt16 biology used

The declared biology-only bundle says that `Supt16` encodes the SPT16 large subunit of the SSRP1-SPT16 FACT histone-chaperone complex. FACT acts at transcribed chromatin, so an effective edit has a plausible direct route to an RNA-abundance phenotype in postmitotic neurons.

The exact non-target expression reach in the requested class was appreciable: `Supt16` was detected in 11,857 of 23,679 matched non-target nuclei, with 0.471 mean CP10k and 47.6 pseudobulk CPM. That made lack of target expression an unlikely explanation for a null response.

The functional-stock card tempered the expected magnitude. It adjudicated FACT/SPT16 loss at P37-P44 as `partially_depleted_or_leading_edge`: a P16 disruptive edit should stop synthesis of intact SPT16, but pre-existing assembled FACT can persist, and the card found no direct neuronal half-life establishing complete complex clearance after 21-28 days. `Ssrp1` was identified as an obligate stabilizing partner rather than a paralogous replacement, so I did not treat the perturbation as fully buffered.

## Training measurements used

The 1,674 measured training targets in the exact cell class were very sparse overall:

- 1,205/1,674 had `n_degs = 0`.
- The median was 0 and the mean was 14.05.
- The 90th, 95th, 97.5th, and 99th percentiles were 2, 18, 103, and 454.

Chromatin and transcription-regulator perturbations were heterogeneous rather than scale-equivalent:

| comparator | n_degs |
|---|---:|
| `Sin3a` | 1433 |
| `Zbtb7a` | 841 |
| `Setd1a` | 368 |
| `Brd4` | 311 |
| `Smarcc2` | 185 |
| `Chd4` | 100 |
| `Bptf` | 65 |
| `Chd8` | 61 |
| `Arid2` | 56 |
| `Kmt2a` | 24 |
| `Arid1a` | 22 |
| `Setdb1` | 22 |
| `Kdm5c` | 18 |
| `Smarce1` | 11 |
| `Crebbp` | 8 |
| `Ash1l`, `Arid1b`, `Baz1b` | 1 each |
| `Smarca4`, `Ep300`, `Kat6a`, `Kat6b`, `Dnmt3a` | 0 |

The same-cell Parquet profile comparison of 23 chromatin-regulator training targets confirmed that these counts do not collapse to a single generic chromatin-loss state. `Smarcc2`, `Chd8`, `Brd4`, `Setd1a`, and `Sin3a` all had available 17,259-gene profiles in this class and respectively had 185, 61, 311, 368, and 1,433 significant features, but pairwise FDR-supported overlaps among the chromatin candidates were usually small and sometimes direction-conflicted. For example, within selected focal comparisons, `Smarcc2` shared 13 same-direction significant genes with `Arid1a`, 7 with `Arid2`, 9 with `Smarce1`, 7 with `Bptf`, and 32 with `Zbtb7a`, while `Brd4` and `Setd1a` had broader but distinct mostly down-biased programs. The profile result made exact-module transfer inappropriate and pushed the forecast toward the moderate CHD/BAF range rather than the `Sin3a`/`Zbtb7a` broad-response range.

Packaged corpus context supported the same boundary. The BAF/mSWI/SNF claim was explicitly subunit-selective in 151 TH Prkcd Grin2c Glut: `Smarcc2`, `Smarce1`, and `Arid1a` converged, `Arid2` was partial, and related `Smarca4`, `Smarca2`, `Smarcc1`, `Bicra`, `Arid1b`, and `Brwd1` were flat, weak, or divergent. `Brd4`, `Setd1a`, `Sin3a`, and `Chd8` reports showed assay-detectable chromatin or elongation-regulator effects in this population, but they were cell-type-restricted and mechanistically specific.

## Point forecast

I forecast a real but muted Supt16 survivor-state response. The biology argues above a generic zero because the target is expressed in the exact class, belongs to an ongoing transcription-coupled chromatin complex, and lacks a close paralog. The partial-stock adjudication and the lack of a same-complex measured donor argue below the 151-active core regulators with hundreds of DEGs. I placed the point in the lower-middle of the active chromatin range, close to the `Chd8`/`Arid2` scale and above the small `Kmt2a`/`Arid1a`/`Setdb1` group.

Predicted `n_degs`: **48**
