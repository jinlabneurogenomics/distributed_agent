# Bbip1 forecast for 151 TH Prkcd Grin2c Glut

## Target and endpoint

- Target: `Bbip1`.
- Requested endpoint: `n_degs`, the number of measured genes in `151 TH Prkcd Grin2c Glut` with Wilcoxon `pvals_adj < 0.05`.
- The target biology bundle was used only for endpoint-blind biology and exact focal-population target reach; I did not query a `Bbip1` differential-expression profile or outcome.

## Target biology used

The canonical `Bbip1` bundle supports that the perturbation should be realized, but it does not by itself predict a broad survivor nuclear RNA program:

- `Bbip1` encodes BBIP1/BBS18, an obligate structural BBSome subunit that stabilizes the assembled cargo-adaptor complex.
- BBSome exchange at ciliary compartments is dynamic and BBSome subunit abundance is interdependent, so stopping new BBIP1 supply at P16 is expected to erode operative BBSome stock during the 21-28 day edit-to-harvest window.
- A matched postnatal thalamic latency measurement was absent; congenital mouse `Bbip1` loss supports neuronal-cilium relevance but in hypothalamic and hippocampal rather than `151 TH Prkcd Grin2c Glut` neurons.
- Exact non-target expression in the focal population showed the `Bbip1` RNA feature was measurable: 16,951 of 23,679 non-target nuclei expressed it, with mean log1p CP10K 0.5609 and pseudobulk CPM 90.55. This supports exposure of the assayed population but is not editing efficiency evidence.

## Training measurements used

The declared `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` table is the direct source for the scalar endpoint in the same cell class. Its 1,674 training targets were zero-heavy: 1,205 had `n_degs = 0`, the median was 0, 1,481 targets had `n_degs <= 1`, and the upper tail was driven by a small number of broad responders.

I used observed BBSome/cilium perturbations rather than the all-target mean as the transfer scale:

| comparison set | matched training counts |
| --- | --- |
| Same-complex BBSome anchors | `Bbs5 = 0`, `Ttc8 = 1` |
| BBSome plus BBSome-associated regulator | `Bbs5 = 0`, `Ttc8 = 1`, `Lztfl1 = 0` |
| Broader ciliary boundary set | `Bbs5 = 0`, `Ttc8 = 1`, `Lztfl1 = 0`, `Cep290 = 0`, `Rpgrip1l = 0`, `Ift88 = 0`, `Ift81 = 0`, `Kif3b = 0` |

The one `Ttc8` event was its own transcript (`Ttc8`, log fold-change -0.663, adjusted p = 3.07e-05), not a downstream ciliary program. Expanding to a larger hand-checked ciliary group kept the same scale: `Arl3 = 1`, `B9d1 = 0`, `Bbs5 = 0`, `Cep290 = 0`, `Cplane1 = 0`, `Dync2h1 = 0`, `Dync2i1 = 0`, `Ift43 = 0`, `Ift81 = 0`, `Ift88 = 0`, `Kif3b = 0`, `Lztfl1 = 0`, `Rpgrip1l = 0`, and `Ttc8 = 1`; the `Arl3` singleton was also its own transcript.

I then ran a matched profile comparison over `Bbs5`, `Ttc8`, `Lztfl1`, `Cep290`, `Rpgrip1l`, `Ift88`, `Ift81`, and `Kif3b` using the declared Parquet, restricted to `group_name = "151 TH Prkcd Grin2c Glut"`, `logfoldchanges` as the signed value, and `pvals_adj < 0.05` as the significance definition. All eight observed profiles were available; seven had no significant features and one had only a 1-9 feature footprint. Across all 28 supplied pairs, there was no positive or negative significant-program overlap, so the comparison did not reveal a hidden recurrent ciliary DEG state.

Same-experiment packaged Findings for the observed comparators were consistent with the direct rows but were not treated as independent replication: `Bbs5`, `Ttc8`, `Ift81`, `Ift88`, `Kif3b`, `Rpgrip1l`, `Cep290`, and `Lztfl1` reports all described absent, singleton, or non-recurrent ciliary/IFT/BBSome transcriptional responses rather than a shared neuronal nuclear RNA module.

## Synthesis

`Bbip1` loss is likely to perturb BBSome function by harvest in cells that express the target, so I did not set the count to zero because the edit was biologically implausible. The decisive scale evidence was that the closest measured same-complex perturbations in the exact requested thalamic group bracket only 0 to 1 significant feature, and the lone direct-BBSome significant feature was a self-transcript. Adding the BBSome-associated and IFT/transition-zone comparators pushed the center still closer to zero, and the profile comparison found no shared FDR-supported downstream state.

The remaining upward uncertainty is the possibility that `Bbip1` itself, which is measurably expressed in this population, could become the single FDR feature. In the observed ciliary cohort, however, self-transcript significance was uncommon and did not co-occur with a downstream program. I therefore placed the point forecast at the quiet endpoint:

`predicted_n_degs = 0`
