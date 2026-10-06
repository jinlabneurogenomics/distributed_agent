# Direct outcome-blind prediction trace

## Target and endpoint

- Manifest target: `Stt3b`
- Cell group: `151 TH Prkcd Grin2c Glut`
- Predicted endpoint: number of measured genes with Wilcoxon BH-adjusted `p < 0.05` in the held-out `Stt3b` perturbation profile.

I used the declared one-row manifest, the canonical `Stt3b` biology bundle, the focal-class training count table, and small focal-class parquet slices for biologically related measured training targets. I did not use a held-out `Stt3b` expression signature, a held-out `Stt3b` DEG count, calibrated probabilities, or labeled-neighbor outcomes.

## Evidence used

### Biology bundle for `Stt3b`

- `Stt3b` is well within reach in the focal non-target nuclei: `84.898%` of `151 TH Prkcd Grin2c Glut` non-target cells express the feature, with mean raw UMI `2.706` and mean log1p-CP10K `0.854`.
- The source card places STT3B in the OST-B oligosaccharyltransferase complex, where it post-translocationally glycosylates sites skipped by cotranslational STT3A-OST.
- Functional stock was adjudicated as `likely_substantially_depleted` by harvest, because the edit should stop new STT3B-OST supply and replacement secretory-pathway proteins should increasingly lack STT3B-selective glycans over the 21-28 day interval.
- The same biology bundle weakens the case for a large matched neuronal RNA response: existing glycosylated carriers persist until turnover, STT3A has partially overlapping substrate coverage, direct STT3B/OST-B protein timing in postmitotic thalamic neurons is unknown, and available severe phenotypes are embryonic/systemic or human developmental rather than acute postnatal thalamic neuron loss.

### Training counts in the focal class

The declared `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` has 1,674 observed training perturbations. It is highly zero-inflated:

- `1205 / 1674` have `n_degs = 0`.
- `469 / 1674` have at least one DEG.
- `132 / 1674` have at least five DEGs.
- `69 / 1674` have at least 25 DEGs.
- `43 / 1674` have at least 100 DEGs.
- Median `n_degs` is `0`; the mean is `14.05`, driven by a small tail of very large responses.

Selected relevant or boundary training perturbations in this class:

| training target | n_degs | interpretation |
|---|---:|---|
| `Dpm1` | 0 | closest measured N-glycosylation/dolichol precursor target I found in the count table |
| `Atf6` | 0 | canonical ER-stress branch, but no focal transcriptional footprint |
| `Ssr4` | 1 | ER translocon-associated target; one significant row and it was the self transcript |
| `Hspa5` | 5 | ER chaperone target; small response including `Hsp90b1`, `Nfe2l1`, `Pdia4`, and `Derl3` |
| `Sec63` | 11 | ER import/proteostasis-adjacent target; positive but still small |
| `Caml` | 28 | ER-membrane target with a broader but still moderate footprint |
| `Ufc1` | 572 | UFMylation/ER-homeostasis response, much broader than OST-B substrate-selective loss |
| `Uba5` | 2677 | UFMylation activation target; treated as a distant high-response boundary, not a direct scale analogue |

The matched parquet slice confirmed that the small ER/glycosylation-adjacent counts were not hiding a broad significant ER module:

- `Dpm1` and `Atf6`: no significant genes in the focal class.
- `Ssr4`: only `Ssr4` itself was significant.
- `Hspa5`: five significant genes.
- `Caml`: 28 significant genes.
- `Ufc1` and `Uba5`: hundreds to thousands of significant genes, with strong `Ddit3`/stress-associated signal, so these look like a different UFMylation-centered response state rather than a quantitative donor for `Stt3b`.

A profile-neighborhood projection of `Dpm1`, `Atf6`, `Hspa5`, `Ssr4`, `Caml`, `Ufc1`, and `Uba5` against the 1,674 training nodes in the focal cell class did not provide a coherent high-count observed neighborhood for the direct glycosylation anchors. The nearest whole-profile and signed-tail neighbors of the low-count anchors were also mostly 0- or 1-DEG profiles, supporting a low forecast.

## Synthesis

I assigned most weight to the exact N-glycosylation and immediate ER/translocation targets rather than to the large UFMylation profiles. STT3B should be present and at least partly depleted by harvest, so a pure biological null is too strong, and its own highly detected transcript makes a self-only FDR hit plausible. But OST-B loss is substrate-selective, partially backed up by STT3A, buffered by pre-edit carrier glycosylation, and not supported by a matched postnatal thalamic loss phenotype. The closest measured training targets around glycosylation and ER stress are 0, 0, 1, 5, and 11 DEGs in this same cell class.

I therefore forecast an isolated detectable response, most likely a self row or one small stress/processing feature rather than a multi-gene UPR program.

Predicted `n_degs`: `1`
