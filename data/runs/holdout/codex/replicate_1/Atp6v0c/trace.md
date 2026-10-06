# Direct DEG-count forecast for Atp6v0c

## Target and endpoint

- Target manifest: `Atp6v0c`.
- Requested endpoint: `n_degs` in `151 TH Prkcd Grin2c Glut`, counting measured genes with BH-adjusted Wilcoxon `p < 0.05`.
- The declared 151-class training count table contains 1,674 targets and excludes `Atp6v0c`.
- The whole-brain training Parquet is the direct measurement surface used only for observed training perturbations.

## Target biology used

The declared `Atp6v0c` biology bundle supports target reach in the focal context but makes the functional realization call only partial:

- `Atp6v0c` was detected in 23,481 of 23,679 matched non-target nuclei in `151 TH Prkcd Grin2c Glut`, with 99.16% expression, mean CP10K 5.665, and mean raw UMI 9.162. Lack of focal expression therefore was not a reason to downweight the target.
- Atp6v0c encodes the membrane-integral V0 proton-pore c subunit of V-ATPase, and the bundle found no close same-subunit functional paralog after the bounded search. That favored a real cell-biological consequence once newly made Atp6v0c is removed.
- The functional-stock card judged the harvest state `partially_depleted_or_leading_edge`: a productive edit stops new c-subunit supply, but preassembled V0 complexes remain in existing vesicle and organelle membranes. The closest in-vivo kinetic estimate was an approximately 20.29-day mouse cortical synaptic-vesicle Atp6v0c lifetime, similar to but not much shorter than the 21-28 day P16-to-P37/P44 Perturb-seq interval.
- The bundle did not find a direct postnatal neuronal Atp6v0c loss study with the same timing; the clean Atp6v0c null phenotype is embryonic and non-neural. I therefore did not promote Atp6v0c to a broad expected stress response from germline essentiality alone.

Net effect: the biology argues for an on-target perturbation that should be possible to observe in 151 thalamic neurons, but also for delayed and compartment-specific realization rather than an acute, pan-lysosomal nuclear stress signature by harvest.

## Training perturbations used

The biologically closest measured training perturbations were the represented V-ATPase and accessory genes:

| target | 151-class n_degs |
| --- | ---: |
| Atp6ap2 | 2 |
| Atp6v0a1 | 1 |
| Atp6v1a | 0 |
| Atp6v1b2 | 0 |
| Atp6v1e1 | 0 |

The exact 151-class significant rows were:

- `Atp6ap2`: `Atp6ap2` down and `Atp6v0a1` down.
- `Atp6v0a1`: self transcript down.
- `Atp6v1a`, `Atp6v1b2`, `Atp6v1e1`: no genes at FDR < 0.05.

Across the full Parquet, these comparators were also sparse rather than selectively quiet only in the target class. `Atp6v0a1` had only one significant gene in each of six measured cell groups, including the single self hit in 151; `Atp6ap2` had mostly one-gene cell-group responses and reached two genes only in 151 and 155; `Atp6v1a` had only four singleton groups outside 151; `Atp6v1b2` was nonzero in one group; and `Atp6v1e1` had no FDR<0.05 gene in the queried training Parquet.

The same-experiment corpus reports the same qualitative boundary at a looser interpretive layer: `Atp6v0a1:F003`, `Atp6ap2:F004`, and `Atp6v1a:F004` support that represented V-ATPase subunits and regulators are flat, sparse, or divergent in postnatal neuronal snRNA-seq rather than forming a shared large V-ATPase perturbation module. I treated this as interpretation of the same experiment, not an independent replicate.

Profile comparison of the five V-ATPase comparators in `151 TH Prkcd Grin2c Glut` confirmed that all five profiles were available and low-activity: significant-feature counts were 2, 1, 0, 0, and 0, with no positive significant genes. Pairwise full-profile correlations were coherent but the significant intersections were essentially absent, so there was no hidden high-DE module among these direct comparators that would justify using a large-neighbor tail such as `Rab7`.

## Quantitative synthesis

The full 151-class training table is strongly zero-inflated: the median target has 0 DEGs, the 75th percentile has 1, the 90th percentile has 2, and the arithmetic mean of 14.05 is dominated by rare high-burden targets such as `Uba5`, `Tpr`, and `Sin3a`.

For Atp6v0c specifically, I put more weight on the direct V-ATPase set than on generic lysosomal or vesicle-trafficking genes. `Rab7`, `Vps35`, and `Vps54` can give larger counts, but they perturb trafficking switches or retromer/GARP biology rather than a membrane-installed V-ATPase pore subunit with a substantial pre-edit stock. The V-ATPase comparators instead anchor the expected count around 0-2. High focal Atp6v0c expression and the absence of a same-subunit paralog nudge the forecast above a strict zero; partial protein-stock depletion and the observed flatness of Atp6v0a1/Atp6ap2/V1 perturbations keep it near the single self-hit scale.

I therefore predicted **1** DEG for `Atp6v0c` in `151 TH Prkcd Grin2c Glut`.
