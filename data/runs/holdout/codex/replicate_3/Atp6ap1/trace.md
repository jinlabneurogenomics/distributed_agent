# Direct forecast trace

## Target and endpoint

- Target: `Atp6ap1`
- Cell group: `151 TH Prkcd Grin2c Glut`
- Endpoint: number of measured genes in the focal class with BH-adjusted Wilcoxon `p < 0.05`
- Point forecast: `1`

## Evidence used

The declared one-row manifest and biology bundle both resolve to `Atp6ap1`. The biology bundle reports that Atp6ap1 is broadly expressed in the exact focal population: 23,268 of 23,679 non-target cells expressed it, or 98.264%, with mean raw UMI 6.752 and mean CP10K 4.124. That makes the perturbation reachable in the assayed population, but I treated this only as expression reach rather than as observed knockdown or endpoint evidence.

The same bundle places ATP6AP1/Ac45 as a cleaved membrane-anchored V-ATPase accessory component in the V0 region that helps form the V0/V1 assembly interface. Its functional-stock adjudication calls the 21-28 day P16-to-harvest window likely long enough to substantially deplete new ATP6AP1-containing stock, while retaining low-confidence uncertainty because no ATP6AP1-specific neuronal half-life or assembled V-ATPase residence measurement was available. Developmental mouse phenotypes and the Atp6ap1l paralog were discounted for endpoint scale because they do not measure acute postnatal thalamic-neuron loss.

The declared `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` table contains 1,674 visible training targets and does not contain `Atp6ap1`. Its distribution is extremely sparse: 1,205 of 1,674 targets have zero DEGs, the median is 0, the 90th percentile is 2, and the 95th percentile is 18. Counts for the closest represented V-ATPase perturbations in the exact focal class were:

| training target | n_degs |
|---|---:|
| `Atp6ap2` | 2 |
| `Atp6v0a1` | 1 |
| `Atp6v1a` | 0 |
| `Atp6v1b2` | 0 |
| `Atp6v1e1` | 0 |

I checked these same targets in the declared expression parquet for `151 TH Prkcd Grin2c Glut`. The only FDR<0.05 hits for `Atp6ap2` were its self transcript and `Atp6v0a1`; `Atp6v0a1` had only its self transcript; `Atp6v1a`, `Atp6v1b2`, and `Atp6v1e1` had no significant genes. Their matched perturbed-cell counts were 116, 197, 76, 32, and 52 respectively, so the weakest V1 observations are low-powered, but the accessory and V0-a1 observations had enough recovered nuclei to show self-detection without broad downstream DE.

I used a bounded profile-neighborhood projection over those five V-ATPase anchors against all 1,674 visible training targets in the focal group. The anchor response activities matched the direct parquet counts: two, one, zero, zero, and zero significant features. The emitted nearest whole-profile neighbors were dominated by other zero or very-low DEG profiles and did not reveal a hidden high-DE V-ATPase-like neighborhood.

The same-experiment corpus was used only to interpret visible training perturbations. `Atp6ap2:F001` describes `Atp6ap2` loss as a nearly silent survivor transcriptome; `Atp6ap2:F004` reports that core V-ATPase perturbations failed to phenocopy `Atp6ap2`; `Atp6v0a1:F001` reports self-detection without downstream FDR<0.10 response across neuronal groups; and `Atp6v0a1:F003` summarizes represented V-ATPase relatives and lysosomal disease comparators as flat or near-flat. The paired `Atp6ap2:F005` contrast against `Rab7` matters because `Rab7` showed that an endolysosomal/V-ATPase compensation program can be visible in this atlas, so I did not treat weak V-ATPase counts as global assay failure.

## Synthesis

ATP6AP1 is close enough to ATP6AP2 and ATP6V0A1 that a direct V-ATPase comparator set should dominate the forecast. Those visible comparators argue for a near-null nuclear RNA response after postnatal sparse CRISPR loss in recovered thalamic neurons: the most directly comparable counts are 2 and 1, with the extra `Atp6ap2` downstream hit being the V0-a1 transcript rather than a broad lysosomal, autophagy, unfolded-protein, or TFEB/CLEAR program.

I therefore did not project the much larger counts from indirect endolysosomal or protein-homeostasis perturbations such as `Rab7`, `Psmb4`, `Psmc1`, or `Uba5`. They prove the focal class can yield large responses, but their operations are downstream or broader than ATP6AP1 loss and do not match the measured direct V-ATPase behavior.

The final point is `1`: broad in-assay `Atp6ap1` expression and likely stock turnover make a self-transcript hit plausible, while the closest training biology places the downstream component near zero.
