# Ap2s1 DEG-count prediction trace

Target: `Ap2s1`

Focal population: `151 TH Prkcd Grin2c Glut`

Endpoint: `n_degs`, the count of measured genes in the focal population with BH-adjusted Wilcoxon `p < 0.05`.

## Biology prior

- The held-out target bundle identifies AP2S1 as the sole sigma subunit of the heterotetrameric AP-2 clathrin adaptor and names `Ap2a1`, `Ap2a2`, `Ap2b1`, and `Ap2m1` as the other AP-2 subunits.
- The functional-stock adjudication favors AP-2 sigma-dependent capacity being substantially reduced by the P37-P44 harvest window: the P16 edit prevents new AP2S1 supply, AP-2 is a dynamic adaptor pool used repeatedly in clathrin-dependent cargo internalization and synaptic-vesicle membrane recycling, and the 21-28 day assay interval exceeds the available mouse-brain turnover proxy.
- The exact focal-expression measurement shows `Ap2s1` is detectable but not saturated in this class: 13,203 of 23,679 non-target nuclei expressed it, i.e. 55.76%, with mean raw UMI 0.908 and mean log1p(CP10k) 0.367. That makes target engagement plausible in recovered 151 nuclei, but it is not a broad, high-expression perturbation in which I would expect every edited survivor to carry a deep transcriptional footprint.
- The direct Ap2s1 mouse loss evidence is embryonic/systemic. The postnatal neural timing evidence comes from same-complex `Ap2m1`, so it supports AP-2 dependence in neurons but leaves Ap2s1-specific P16 thalamic latency unresolved.

## Training measurements that set scale

No AP-2 core subunit in the Ap2s1 bundle was present in the declared 1,674-target training count table, so I used functionally adjacent training perturbations instead.

Exact `151 TH Prkcd Grin2c Glut` counts from the declared `p_adj < 0.05` training table:

| training target | relation to Ap2s1 biology | n_degs |
|---|---:|---:|
| `Cltc` | core clathrin coat, broader and upstream of AP-2-mediated vesicle formation | 3 |
| `Dnm1` | synaptic-vesicle fission | 1 |
| `Synj1` | synaptic-vesicle uncoating/phosphoinositide turnover | 1 |
| `Bin1` | BAR/endocytic factor | 1 |
| `Syp` | synaptic-vesicle factor | 1 |
| `Ap1b1` | adaptor-complex subunit outside AP-2 | 1 |
| `Ap3b1` | adaptor-complex subunit outside AP-2 | 0 |
| `Ap1s2` | adaptor-complex sigma family, outside AP-2 | 0 |
| `Ap4s1` | adaptor-complex sigma family, outside AP-2 | 0 |

Broader trafficking perturbations in the same count table showed that this focal class can respond to endomembrane stress, but at a scale that should not be transferred directly to plasma-membrane AP-2:

| training target | process level | n_degs |
|---|---:|---:|
| `Vps35` | retromer cargo retrieval | 17 |
| `Vps54` | GARP retrograde traffic | 31 |
| `Rab7` | late endosome/lysosome/autophagy traffic | 501 |

The whole training distribution was heavily zero-inflated in this class: 1,205 of 1,674 targets were zero, the median was 0, the 75th percentile was 1, the 90th percentile was 2, and the 95th percentile was 18. Thus a forecast of 2 already places Ap2s1 at the upper edge of the ordinary sparse-response mass, while still far below clear trafficking stress programs such as `Vps35`, `Vps54`, or `Rab7`.

## Focal profile interpretation

I compared the declared Parquet signatures for `Cltc`, `Dnm1`, `Synj1`, `Bin1`, `Ap3b1`, `Rab7`, `Vps35`, and `Vps54` in exactly `151 TH Prkcd Grin2c Glut`.

- The direct endocytosis/adaptor anchors were transcriptionally tiny in the focal profile: `Cltc` had 3 significant features, `Dnm1`, `Synj1`, and `Bin1` each had 1, and `Ap3b1` had 0.
- `Rab7`, `Vps35`, and `Vps54` had 501, 17, and 31 significant focal features, but their significant-gene intersections with the direct endocytosis anchors were essentially absent. `Cltc` shared only 1 negative significant feature with `Rab7` and none with `Vps35` or `Vps54`; `Dnm1`, `Synj1`, `Bin1`, and `Ap3b1` shared no significant features with those larger endolysosomal profiles.
- Whole-profile correlations were positive but non-discriminating across the small cohort. They supported a weak shared direction among vesicle-trafficking perturbations, not a reason to assign Ap2s1 a `Rab7`-scale response.

The packaged same-experiment Findings for the measured comparators supported the same boundary. `Dnm1` and `Synj1` were described as pan-surface transcriptional zeros at FDR < 0.10, `Bin1` as an isolated sparse response, and `Cltc` as the clathrin-axis target that crosses a selective nuclear-response threshold but is not phenocopied by the canonical synaptic endocytosis and uncoating targets. The `Rab7` reports described a broad late-endosomal/lysosomal, sterol, UPR/ISR, and synaptic-downshift state concentrated in 151 and 155, while `Vps35` and `Vps54` were much narrower thalamic endomembrane responses. Those reports are different interpretations of the same perturbation experiment, so I used them only to explain which measured training profiles were plausible or excessive comparators.

## Synthesis

`Ap2s1` has better functional-stock evidence than the completely quiet adaptor-family controls, because AP2S1 is the unique AP-2 sigma subunit and AP-2 is continually renewed. That moved the point above a hard zero. The scale should still stay near the sparse clathrin/endocytosis anchors rather than near the high endolysosomal stress anchors: AP-2 is plasma-membrane adaptor machinery rather than `Rab7`-class late lysosome/autophagy control, the exact focal expression reaches only about half of recovered non-target nuclei, and survivor conditioning can erase cells with the most severe AP-2 failure.

The nearest measured p < 0.05 scale anchor is therefore `Cltc` at 3 focal DEGs, with `Dnm1`, `Synj1`, `Bin1`, `Syp`, and `Ap1b1` at 1 and outside-AP adaptor sigma targets at 0. I chose a point just under `Cltc`, because clathrin heavy-chain loss is broader than AP-2 sigma loss and already produces only three 151 DEGs.

Predicted `n_degs`: 2
