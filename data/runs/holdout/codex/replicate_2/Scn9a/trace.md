# Scn9a direct n_degs forecast

## Endpoint

- Target: `Scn9a`
- Cell group: `151 TH Prkcd Grin2c Glut`
- Endpoint: count of measured genes with BH-adjusted Wilcoxon `pvals_adj < 0.05`
- Forecast: `0`

## Evidence used

The declared biology bundle identifies Scn9a/Nav1.7 as a pore-forming voltage-gated sodium-channel alpha subunit whose functional membrane-channel stock should substantially decline within the 21-28 day P16-to-P37/P44 window. That supports possible target engagement, but the evidence is mostly from adult peripheral sensory neurons rather than thalamus, and the bundle explicitly keeps thalamic compensation and survivor conditioning unresolved.

The exact in-assay reach in the focal population is weak and spatially restricted. In non-target nuclei from `151 TH Prkcd Grin2c Glut`, Scn9a was detected in 2,753 of 23,679 nuclei, `11.626%`, with mean raw UMI `0.1606` and pseudobulk CPM `10.07`. A real electrophysiological loss in the Scn9a-positive subset is therefore diluted in the class-level nuclear RNA endpoint; the low baseline also makes a self-transcript row less certain than for broadly expressed channel genes.

The full training count table for this exact cell group contained 1,674 measured training perturbations. Its distribution was very zero-heavy: 1,205/1,674 targets had `n_degs = 0`, the median was `0`, the 75th percentile was `1`, the 90th percentile was `2`, and the long upper tail was driven by broadly disruptive factors such as `Uba5`, `Tpr`, `Sin3a`, spliceosome, proteasome, and chromatin regulators rather than ion-channel paralogs.

The closest voltage-gated sodium-channel training perturbations were all flat or self-only in the same endpoint:

| target | training `n_degs` in 151 TH |
| --- | ---: |
| `Scn1a` | 1 |
| `Scn1b` | 2 |
| `Scn2a` | 1 |
| `Scn3a` | 0 |
| `Scn8a` | 1 |

Exact 151-class Parquet rows showed the significant entries behind those small counts:

| target | FDR-significant rows at `pvals_adj < 0.05` |
| --- | --- |
| `Scn1a` | `Scn1a` only |
| `Scn1b` | `Scn1b`, `Jun` |
| `Scn2a` | `Scn2a` only |
| `Scn3a` | none |
| `Scn8a` | `Scn8a` only |

Thus the sodium-channel alpha subunits most often contributed a detectable self-transcript drop but no downstream 151 TH state. `Scn3a`, a close assayed alpha-subunit comparator in the postnatal loss-of-function screen, had zero BH-significant genes in this class.

Packaged same-experiment Findings agreed with the raw rows: `Scn1a`, `Scn2a`, `Scn3a`, and `Scn8a` were described as sparse or buffered postnatal Nav perturbations, with the July corpus explicitly rejecting a shared pan-Nav/FHF transcriptional module. `Scn2a` in particular was contrasted against `Cacna1g` in 151 TH: Scn2a knocked down its own RNA without downstream FDR-level genes, whereas Cacna1g produced a real thalamic footprint.

The two active 151 TH ion-channel controls set an upper reference, not a direct scale transfer. `Cacna1g` had `12` DEGs here, including its self row and a narrow thalamic program; `Grin1` had `89` DEGs with a much broader synaptic/plasticity signature. Both are stronger, cell-state-shaping 151 TH perturbations than a low-reach Nav1.7 perturbation, so I treated them as evidence that the assay can respond to selected channels, not as evidence that Scn9a should have a multi-gene footprint.

The matched profile comparison across `Scn1a`, `Scn1b`, `Scn2a`, `Scn3a`, `Scn8a`, `Cacna1g`, and `Grin1` in the `151 TH Prkcd Grin2c Glut` Parquet rows preserved the same interpretation. Among the five Nav-family nodes, `Scn3a` had no significant features, the other four had 1-2 features, and pairwise FDR-significant intersections among the Nav nodes were zero.

## Synthesis

The biology says Scn9a loss can matter in neurons by this harvest, but the exact 151 TH reach is low and the readout is an aggregate, survivor-conditioned nuclear RNA contrast. The endpoint-matched training behavior of the assayed Nav-family perturbations is correspondingly quiet: no shared sodium-channel response, no channel-compensation module, and usually no downstream DEG after removing the self row.

For Scn9a specifically, the 11.6% expressing-fraction and very low mean target RNA make even a self-transcript hit uncertain. A one-DEG forecast would mostly be a bet on detectable Scn9a mRNA depletion rather than on a downstream thalamic program. I placed the point estimate at the mode of the close Nav comparators and the overall sparse count table, `0`, with residual uncertainty for a single self or `Jun`-like hit.
