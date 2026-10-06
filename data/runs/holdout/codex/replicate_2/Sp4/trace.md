# Sp4 DEG-count forecast

## Target and endpoint

- Target: `Sp4`, the only gene in the declared one-row holdout manifest.
- Focal class: `151 TH Prkcd Grin2c Glut`.
- Endpoint: `n_degs`, the number of measured genes with Wilcoxon BH-adjusted `pvals_adj < 0.05`.
- Same-experiment target leakage check: the selected corpus has no `Sp4` target Findings, Claim contributions, or explicit comparator edges in `target_context`; the forecast therefore used the `Sp4` biology bundle plus non-`Sp4` training measurements only.

## Biological prior from the declared Sp4 bundle

The bundle supports a realized but not obviously massive perturbation:

- In the exact focal population, `Sp4` was detected in 12,209 of 23,679 non-target nuclei, or 51.56%, with mean CP10K 0.510 and mean raw UMI 0.800. This made the target transcript reachable in only about half of assayed nuclei, not absent.
- SP4 is a nuclear sequence-specific zinc-finger transcription factor binding GC/GT promoter elements.
- The functional-stock card adjudicated SP4 as a short-lived, continuously replenished, free protein: a disruptive edit should stop new production, and measured neuronal half-life was hours to about one day, much shorter than the 21-28 day edit-to-harvest interval.
- The observability card found postnatal neural phenotypes despite SP1/SP3 relatives, so complete family buffering should not be assumed. However, the closest phenotypes were germline or lifelong hypomorphic and hippocampal/systemic rather than a P16 thalamic conditional loss, leaving the focal RNA program uncertain.

I treated these points as evidence against a pure failure/null prior but not as evidence for a Yy1/Zbtb7a-like broad chromatin response.

## Training-count scale

The declared `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` has 1,674 observed non-`Sp4` perturbations. It is highly sparse:

- median `n_degs`: 0
- 75th percentile: 1
- 90th percentile: 2
- 95th percentile: 18
- 1,205/1,674 targets have 0 DEGs
- only 43/1,674 have at least 100 DEGs

Annotation-store grouping put `Sp4` in `DNA-binding transcription factor activity`, `RNA polymerase II-specific DNA-binding transcription factor activity`, and `sequence-specific DNA binding`. The training targets in the matching TF bins are also mostly quiet in this focal class:

| Training subset | n | median | 90th pct | 95th pct | zeros | 1-9 | 10-49 | >=50 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| DNA-binding transcription factor activity | 251 | 0 | 3 | 12.5 | 206 | 30 | 5 | 10 |
| RNA pol II-specific TF activity | 280 | 0 | 1 | 7.15 | 236 | 30 | 6 | 8 |
| sequence-specific DNA binding | 191 | 0 | 4 | 71.5 | 156 | 21 | 2 | 12 |
| functional class transcription factor | 344 | 0 | 2 | 15 | 284 | 39 | 8 | 13 |

That made the all-target and all-TF empirical base rate much closer to 0-10 than to 100+.

## Expression-parquet comparator checks

I used `training_de_all_cell_groups.parquet`, restricted to `group_name == "151 TH Prkcd Grin2c Glut"`, to compare hand-selected observed transcription-factor profiles. Counts below are exact `pvals_adj < 0.05` counts from that matched class:

| Comparator | Why it informed the forecast | 151-class DEGs |
| --- | --- | ---: |
| `Klf9` | closest KLF/SP-like sparse thalamic responder in the corpus | 19 |
| `Zfp148` | GC-rich promoter-binding zinc-finger factor; small 151-restricted signature | 8 |
| `Zbtb18` | postmitotic neuronal zinc-finger TF with focal marker response | 5 |
| `Klf7` | KLF family comparator | 1 |
| `Zbtb38` | sparse ZBTB comparator | 1 |
| `Usf1` | GC/E-box DNA-binding TF comparator | 1 |
| `Egr2`, `Foxp2`, `Myc`, `Mycn` | assayed sequence-specific TFs that stayed flat here | 0 |
| `Yy1`, `Zbtb7a`, `Ctcf`, `Rora` | broad TF/chromatin upper-bound outliers, not close scale anchors | 720, 841, 270, 278 |

The profile comparison reinforced the count-table scale rather than revealing a tight high-response module:

- `Klf9`, `Zfp148`, `Zbtb18`, and `Zfp236` had 19, 8, 5, and 19 FDR<0.05 features respectively.
- `Yy1` was a clear outlier with 720 features, 277 up and 443 down.
- Significant-feature overlaps from the small KLF/zinc-finger profiles into broad outliers were partial: for example `Klf9` shared 11 of its 18 upregulated significant genes with the 512-gene positive arm of `Zbtb7a`, but it shared no significant positive or negative genes with `Ctcf`, `Yy1`, `Zfp423`, `Klf7`, `Zbtb38`, `Usf1`, `Egr2`, `Foxp2`, or `Myc` in the inspected pairs.

## Corpus interpretation of the same profiles

The same-experiment corpus supported treating KLF/SP and ZBTB family membership as only a weak predictor of a shared response:

- `Klf9` is the best mechanistic lower-scale anchor: its report describes a 19-gene, mostly upregulated 151-class response, but also states that represented KLF-family perturbations are paralog-specific rather than a generic KLF-family knockdown state.
- `Zfp148` produced a small, sharply 151-restricted response rather than a broad GC-box TF collapse.
- `Zbtb18` produced a focal 151 response and the BTB-ZF reports note that shared ZBTB/BTB-ZF family membership was insufficient to predict a common neuronal phenotype.
- `Zbtb7a` and `Yy1` were broad responders, but their reports place them in proteostasis/chromatin/RNA-processing states with many hundreds of DE genes; I used them as evidence that the class can report a broad nuclear-regulator hit, not as close SP4 analogs.

These reports come from the same Perturb-seq experiment as the Parquet, so they were used for semantic interpretation only, not as independent replication.

## Synthesis

`Sp4` is expressed in the focal thalamic population and its protein stock should be depleted by harvest, so a nonzero transcriptomic effect is more plausible than for an unexpressed or long-lived structural target. At the same time, the matched training distribution is zero-heavy, SP/KLF-adjacent factors in the count table are usually zero or single-digit, and the few hundreds-of-DEG DNA-binding outliers have broad secondary states not justified by the supplied SP4 biology.

I therefore anchored below `Klf9` and near the small GC/zinc-finger responders rather than near `Yy1`/`Zbtb7a`. The final point estimate is a small focal signature:

`predicted_n_degs = 6`
