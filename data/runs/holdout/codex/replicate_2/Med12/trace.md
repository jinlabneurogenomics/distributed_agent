# Direct Med12 n_degs forecast

Endpoint: number of measured genes in `151 TH Prkcd Grin2c Glut` with BH-adjusted Wilcoxon `p < 0.05`.

Target: `Med12`.

## Evidence used

The Med12 biology bundle supports a reachable but not guaranteed postnatal neuronal perturbation. MED12 is a structural/regulatory subunit of the dissociable CDK8 Mediator kinase module, contacting CDK8-cyclin C and MED13 and influencing transcriptional regulation. The functional-stock card concluded that a disruptive edit should halt new production of a dynamic nuclear complex component and that operative stock is likely substantially depleted by the P37-P44 harvest, but with partial evidence because no native thalamic-neuron MED12 turnover measurement was found. Exact target-population expression was available but modest: `Med12` was detected in 4,548 of 23,679 non-target 151-class cells, `19.2069%`, with mean raw UMI `0.2202` and pseudobulk CPM `13.8031`.

The visible 151-class training count table is strongly zero-inflated. Of 1,674 training targets, 1,205 had `n_degs = 0`; the median was `0`, the 90th percentile was `2`, and the 95th percentile was `18`. The closest visible Mediator and kinase-module rows were all low:

| target | n_degs at p_adj < 0.05 |
| --- | ---: |
| Cdk8 | 0 |
| Med13l | 1 |
| Med13 | 11 |
| Med23 | 13 |
| Med15 | 19 |

Bounded same-experiment corpus summaries for these measured training targets placed `Med13`, `Med15`, and `Med23` in a shared down-regulated thalamic Mediator module, with `Med13l` contributing only a narrow `Grm1` overlap and `Cdk8` acting as a flat boundary rather than a phenocopy. That made `Med13` the closest measured positive analogue for a MED12 scaffold effect, while `Cdk8` and `Med13l` argued that not every kinase-module component produces the module after acute P16 neuronal CRISPR.

Fresh profile comparison on the declared Parquet slice for `151 TH Prkcd Grin2c Glut` reproduced the same scale at the task's stricter FDR threshold: `Cdk8` had 0 significant features, `Med13l` had 1, `Med13` had 11, `Med23` had 13, and `Med15` had 19. The significant effects were almost entirely down-regulated, and the three multi-gene Mediator signatures shared a small core of thalamic state genes including `Atp2a2`, `Grm1`, `Pcp4`, `Plekhg1`, and `Prkcd`.

## Reasoning

I treated the all-target empirical table as the response-scale prior and then let the visible Mediator perturbations set the local bracket. The upper side of the bracket is the shared `Med13`/`Med15`/`Med23` module, roughly 10 to 20 BH-significant genes in this cell class. `Med12` could plausibly enter that module because MED12 and MED13 are both non-enzymatic CKM scaffolding/regulatory components, and the Med12 card supports loss of functional stock within the 21 to 28 day edit-to-harvest window.

The lower side deserves more weight than the broad Mediator tail subunits. `Cdk8` was fully flat in this same cell class, `Med13l` gave only one shared gene, and the Med12 bundle's exact expression reach shows the target transcript in only about one fifth of 151-class non-target nuclei. Those points argue against forecasting the full 11 to 19 gene module and against using high-burden chromatin/transcriptional regulators such as `Brd4` as quantitative donors.

The final point forecast is therefore a small positive count: above the zero-heavy population baseline and the `Cdk8` null because MED12 is a scaffold tied to MED13, but below the measured `Med13` response because the directly represented kinase-module neighborhood is heterogeneous and Med12 reach is modest.

`predicted_n_degs = 4`
