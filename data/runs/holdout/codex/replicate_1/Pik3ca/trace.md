# Pik3ca forecast

Target: `Pik3ca`

Endpoint: `n_degs` in `151 TH Prkcd Grin2c Glut`, the count of measured genes with BH-adjusted Wilcoxon `p < 0.05`.

Predicted value: `0`

## Evidence used

- The declared holdout manifest contains one target, `Pik3ca`.

- The declared biology-only bundle says the in-assay target feature is present in this focal population: `Pik3ca` was detected in 16,402 of 23,679 non-target nuclei, or 69.27%, with mean CP10K 0.844 and mean log1p(CP10K) 0.521. The same bundle adjudicates the operative p110-alpha stock as likely substantially depleted over the P16 to P37-P44 interval, but flags partial evidence, no matched mouse thalamic neuronal half-life, only low-confidence observability transfer from other postnatal neural contexts, and possible class IA PI3K redundancy. I therefore treated target engagement as biologically plausible rather than as a reason to force a nonzero RNA count.

- The exact focal-class training count table is sparse: 1,205 of 1,674 held-in perturbations have `n_degs = 0`; 1,481 have at most one DEG; 1,512 have at most two. Counts of tens to thousands of DEGs are rare in this cell class.

- Curated mouse analogue nomination against the actual 1,674-target training universe placed `Pik3cb`, `Pik3r1`, and `Pik3r2` among the closest available PI3K candidates. Their exact `151 TH Prkcd Grin2c Glut` counts are all zero:

  | comparator | relationship to `Pik3ca` in the nomination | `n_degs` |
  | --- | --- | ---: |
  | `Pik3cb` | class IA catalytic isoform / PI3K modules | 0 |
  | `Pik3r1` | class IA regulatory-complex partner | 0 |
  | `Pik3r2` | class IA regulatory-complex partner | 0 |

- Broader pathway nominations were also mostly flat in the same count table. `Akt3`, `Rptor`, `Hras`, `Irs1`, `Igf1r`, `Insr`, `Mapk1`, and `Ptpn11` were each 0; `Syp` was 1; `Mtor` was 2. `Tsc2` was higher at 86, but it is a downstream mTOR-axis regulator rather than a direct PI3K catalytic/regulatory substitute.

- A profile comparison over `Akt3`, `Mtor`, `Pik3cb`, `Pik3r1`, `Pik3r2`, `Rptor`, and `Tsc2` in the exact focal group had no missing profiles, but five of the seven had no significant features. The 21 pairwise profiles had median positive and negative top-tail overlaps of 0.02 and 0.03, and no significant-program overlap, so these pathway members did not form a recurrent shared transcriptomic state that could justify averaging `Tsc2` upward into a `Pik3ca` forecast.

- The packaged same-experiment corpus was used only to interpret held-in comparators. Its summaries for `Pik3cb`, `Pik3r1`, `Mtor`, and `Tsc2` describe the same pattern seen in the table/profile analysis: basal receptor-proximal PI3K/AKT nodes were transcriptionally buffered, while `Tsc2` exposed a downstream mTORC1/sterol-lysosomal program and weak `Mtor` effects were detectable. This is semantic interpretation of the PerturbAI experiment, not independent replication.

## Synthesis

`Pik3ca` is expressed in many assayed thalamic nuclei and its protein stock should be renewable enough for an edited cell to lose function by harvest, so a biological effect is possible. The task endpoint, however, is not pathway activity itself; it is a BH-significant nuclear RNA footprint in recovered postnatal neurons. The closest measured class IA PI3K catalytic/regulatory perturbations, and several receptor-proximal PI3K/AKT neighbors, were exactly zero in the focal training counts. The few nonzero downstream mTOR-axis comparators were profile- and mechanism-bound outliers rather than a common PI3K neighborhood response.

Those observations put the expected `Pik3ca` count at the zero-inflated mode of the training distribution. I therefore predict `0` DEGs.
