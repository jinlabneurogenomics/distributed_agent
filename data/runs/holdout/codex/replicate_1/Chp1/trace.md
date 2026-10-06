# Chp1 direct DEG-count forecast

## Endpoint

- Target: `Chp1`
- Cell class: `151 TH Prkcd Grin2c Glut`
- Quantity forecast: `n_degs`, the count of measured genes with BH-adjusted Wilcoxon `p < 0.05`.
- Point forecast: `1`

## Evidence Used

The declared biology bundle shows that `Chp1` is detectably expressed in the focal recovered non-target thalamic nuclei, so lack of target reach is not the main reason to expect a quiet result:

- `n_non_target_cells = 23679`
- `n_cells_expressing = 15491`
- `pct_cells_expressing = 65.4208`
- `mean_raw_umi = 1.2108`
- `mean_log1p_cp10k = 0.4729`

The same bundle supports biological realization by P37-P44, but only partially. CHP1 maintains Na+/H+ exchanger maturation and membrane stability, and an NHE1 carrier proxy turns over on an approximately daily timescale, so a P16 edit can plausibly erode newly supplied CHP1-dependent function during the 21-28 day window. The caveats are large for this endpoint: the clearest mouse neural loss phenotype is a congenital hypomorph in cerebellar Purkinje cells, not acute thalamic editing, and CHP3 can restore much NHE1 in some postnatal neurons while failing in others. The bundle therefore adjudicates the assayed functional stock as `partially_depleted_or_leading_edge`, not uniformly cleared.

The selected same-experiment corpus release had no `Chp1` target Findings or Claims, so it supplied no outcome-like target report to transfer from. The deterministic mouse gene-analog nomination against the 1,674-gene training universe also found no `Chp1` exact-complex/paralog, bidirectional-corpus, narrow-module, or direct-interaction candidates. Its usable Chp1-like nominations were broad GO fallbacks, led by sodium:proton antiporter activity for `Slc9a9` and `Slc9a7` and intracellular-pH transport for `Slc4a7`.

The declared count table for this exact class is heavily concentrated at zero: among 1,674 training perturbations, 1,205 had `n_degs = 0`, 276 had `n_degs = 1`, the median was 0, the 75th percentile was 1, and 1,542 targets were at or below 4 DEGs. Large responses exist, but they are a small upper tail driven by regulators such as `Uba5`, `Tpr`, `Sin3a`, `Rnpc3`, `Zbtb7a`, and spliceosome/chromatin/proteostasis genes rather than NHE-like pH regulators.

The closest measured pH-homeostasis perturbations in the same count table were small:

| training perturbation | rationale for checking | n_degs |
|---|---:|---:|
| `Slc9a9` | nominated Na+/H+ exchanger / intracellular-pH analog | 0 |
| `Slc9a7` | nominated Na+/H+ exchanger / intracellular-pH analog | 1 |
| `Slc4a7` | nominated broader intracellular-pH transporter | 0 |
| `Gnas` | nominated acid-response fallback | 0 |
| `Trpv1` | nominated acid-response fallback | 0 |
| `Atp6ap2` | V-ATPase-associated pH boundary | 2 |
| `Atp6v0a1` | V-ATPase pH boundary | 1 |
| `Atp6v1a` | V-ATPase pH boundary | 0 |
| `Atp6v1b2` | V-ATPase pH boundary | 0 |
| `Atp6v1e1` | V-ATPase pH boundary | 0 |
| `Clcn3` | endolysosomal Cl-/H+ boundary | 0 |
| `Clcn4` | endolysosomal Cl-/H+ boundary | 1 |

I also compared a broader 21-node cohort in the declared Parquet for `151 TH Prkcd Grin2c Glut`. The cohort included the NHE/pH nodes above, top broad Chp1 fallback nominations, V-ATPase and chloride/proton boundaries, and `Calm1/2/3`. All requested profiles were present. Ten of the 21 had no significant features, nine had only 1-9, and two had 10-49. Pairwise profile support did not reveal a shared significant positive program: across all 210 cohort pairs, the positive significant-program overlap mean and median were both 0; the negative overlap median was also 0, with only sparse pair-specific sharing. This supports treating the nonzero boundary cases, especially `Calm1 = 14`, as weak boundary observations rather than as a module that should pull `Chp1` upward.

## Synthesis

`Chp1` has enough in-class expression and enough renewal of its CHP1/NHE functional stock that I do not want to predict a guaranteed transcriptional null. At the same time, its best-measured analogs are only broad pH-homeostasis fallbacks and sit at 0-1 DEGs, while the functional-stock card leaves thalamic CHP3 buffering and acute postnatal endpoint coupling unresolved. A large thalamic nuclear RNA response like chromatin, spliceosome, or proteasome perturbations is therefore not biologically supported. The most defensible point is a near-null response with room for a self-target or single downstream DEG.

I therefore forecast `n_degs = 1`.
