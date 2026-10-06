# Nf1 forecast for 151 TH Prkcd Grin2c Glut

Target: `Nf1`

Prediction: `0` BH-adjusted Wilcoxon `p < 0.05` DEGs in `151 TH Prkcd Grin2c Glut`.

## Evidence used

The declared biology bundle argues that this is a reachable perturbation, not a simple expression null. In the exact focal population, `Nf1` RNA is measured in 20,079 of 23,679 non-target nuclei, 84.80%, with mean 2.22 raw UMI and mean 1.40 CP10K. Neurofibromin is annotated as a dynamic Ras-GAP homodimer; the functional-stock card calls pre-edit stock likely substantially depleted by P37-P44 after a P16 edit. So I did not downweight `Nf1` for absent expression or for protein stock that would obviously outlast the experiment.

The 151 training count table is extremely zero-heavy: 1,205 of 1,674 training perturbations have `n_degs = 0`, with quartiles `0, 0, 1`; the 90th percentile is only `2`. Most of the table-wide mean is driven by a small set of broad spliceosome, proteostasis, transcriptional, and chromatin perturbations rather than by signaling genes.

The direct Ras/MAPK neighborhood present in the 151 count table points to a very small basal RNA output:

| training perturbation | 151 `n_degs` |
|---|---:|
| `Spred1` | 0 |
| `Spred2` | 0 |
| `Hras` | 0 |
| `Kras` | 0 |
| `Sos1` | 0 |
| `Rasa2` | 0 |
| `Raf1` | 0 |
| `Map2k2` | 0 |
| `Mapk1` | 0 |
| `Ptpn11` | 0 |
| `Braf` | 4 |
| `Map2k1` | 4 |

The Parquet rows for the few positive RAF/MEK events were a tiny shared module: `Braf` significantly down-regulated `Vgf`, `Ptpn5`, `Atp2a2`, and `Unc13a`, while `Map2k1` significantly down-regulated `Vgf`, `Ptpn5`, `Unc13a`, and `Etv5`. The same all-cell Parquet scan found essentially no broader pan-neuronal response for these nodes: `Braf` had only one non-151 significant row across the other assayed groups, and `Spred1`, `Spred2`, `Hras`, `Kras`, `Sos1`, `Raf1`, `Rasa2`, and `Map2k2` were zero in every measured group scanned.

Packaged same-experiment Findings support the same interpretation. The `Braf` report describes the `Braf`/`Map2k1` response as a sparse `Vgf`/`Ptpn5`/`Unc13a` thalamic branch and explicitly separates it from `Kras`, `Hras`, `Sos1`, `Raf1`, `Rasa2`, `Map2k2`, and `Mapk1`. The `Spred1` report is the closer negative-regulator analogue for NF1 recruitment to Ras: acute single `Spred1` loss had no downstream FDR<0.10 genes across measured neuronal classes despite the detectable `Braf`/`Map2k1` benchmark.

`Tsc2` is the main counterweight: it has 86 DEGs in 151, and its report places the response in an mTORC1/SREBP/lysosomal program. I treated that as an upper contextual bearing rather than as a scale donor. `Tsc2` removes a direct mTORC1 brake, whereas `Nf1` is upstream at Ras; in the same training data `Mtor` has only 2 DEGs in 151 and upstream PI3K/Ras components are flat. The `Tsc2` branch therefore shows that caudal/thalamic neurons can mount a metabolic signaling response, but it does not overcome the repeated buffering of upstream Ras/MAPK and PI3K nodes under basal postnatal snRNA-seq.

## Synthesis

`Nf1` itself is expressed and should be functionally depleted enough for a cell-autonomous effect, so the null forecast is not based on target inaccessibility. The decisive quantitative evidence is instead that the closest assayed basal Ras/MAPK perturbations are nearly all FDR-zero, with only a 3-to-4-gene RAF/MEK output in 151, and that the closest assayed negative-feedback analogue, `Spred1`, is fully flat. A strict BH<0.05 DEG count for `Nf1` should therefore sit at the zero edge or at most a few genes; I place the point at the modal and median analogue value, `0`, rather than transferring the broader `Tsc2` mTORC1 magnitude.
