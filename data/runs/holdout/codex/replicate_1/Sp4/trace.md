# Direct `n_degs` forecast for `Sp4`

## Target and endpoint

- **Target:** `Sp4`
- **Cell class:** `151 TH Prkcd Grin2c Glut`
- **Endpoint:** number of measured genes with BH-adjusted Wilcoxon `pvals_adj < 0.05`
- **Point forecast:** `150`

## Evidence used

- The one-row holdout manifest names `Sp4`, and the canonical `Sp4` bundle reports the exact focal-population baseline reach: `Sp4` is expressed in 12,209 of 23,679 non-target nuclei in `151 TH Prkcd Grin2c Glut` (`51.56%`), with mean log1p CP10K `0.3368` and pseudobulk CPM `50.1`. This makes target engagement in the assayed class biologically plausible, while not implying uniform expression across every recovered nucleus.
- The same biology bundle identifies SP4 as a nuclear GC/GT-box sequence-specific zinc-finger transcription factor. Its functional stock is expected to clear by the P37-P44 harvest because a disruptive P16 edit stops new SP4 production and SP4 protein turnover measured in primary mouse neurons is on an hours-to-one-day scale, far shorter than the 21-28 day post-edit interval.
- The Sp4 prior phenotype evidence supports a neural consequence of losing the gene but is not a matched thalamic, postnatal, mosaic CRISPR measurement: complete germline loss causes early postnatal mortality and reduced Sp4 causes hippocampal molecular/histological and behavioral abnormalities, while the bundle explicitly leaves juvenile thalamic demand and survivor conditioning uncertain.
- The declared `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` table is sparse: among 1,674 training perturbations, 1,205 have `0` DEGs, the median is `0`, the 95th percentile is `18`, the 97.5th percentile is about `101`, and only 43 training perturbations reach at least 100 DEGs. Therefore `Sp4` needs target-specific biological support to be placed in the tail.
- The strongest focal training responses come from globally important RNA-processing, proteostasis, transport, or chromatin/transcriptional regulators, for example `Uba5` `2677`, `Tpr` `1768`, `Sin3a` `1433`, `Zbtb7a` `841`, `Yy1` `720`, `Cic` `576`, and `Thap11` `478`. SP4 is a sequence-specific TF with only partial focal expression, so I treated these as an upper tier rather than as equal-scale analogues.
- A more moderate transcriptional-regulator bracket in the same focal count table is `Rora` `278`, `Ctcf` `270`, `Zfp423` `150`, `Nrf1` `138`, `Nr1d1` `116`, `Tcf7l2` `106`, and `Bmal1` `103`. I checked the focal Parquet rows for this panel; their significant calls were coherent, mixed up/down signatures rather than count-table artifacts, with examples such as `Zfp423` 76 up and 74 down DEGs, `Nrf1` 23 up and 115 down, `Nr1d1` 94 up and 22 down, `Tcf7l2` 39 up and 67 down, and `Bmal1` 69 up and 34 down.
- The nearest GC-box/KLF-like training entries were not strong in the focal count table: `Klf9` and `Zfp236` each had `19` DEGs, `Zfp148` had `8`, `Thap1` had `7`, `Klf7` had `1`, and `Klf13` had `0`. That lowered the forecast relative to the 270-800 DEG broad-regulator tier despite the positive SP4 stock and expression evidence.

## Synthesis

I placed `Sp4` above the low KLF/weak zinc-finger group because it is detectably expressed in about half of the focal thalamic nuclei, encodes a short-lived transcription factor whose post-edit functional stock should be gone by harvest, and has in vivo neural loss-of-function evidence despite related SP-family paralogs. I placed it below the largest chromatin and basal-regulatory training perturbations because the operation is a sequence-specific TF perturbation with uncertain postnatal thalamic target coverage rather than a core spliceosome, proteasome, mediator, or chromatin-complex hit.

The resulting scale is the lower tail of the high-response transcription-factor/chromatin group, centered on the `Zfp423`/`Nrf1`/`Nr1d1`/`Tcf7l2`/`Bmal1` focal training bracket rather than on the count-table median or on the `Zbtb7a`/`Yy1`/`Cic` tier. I therefore forecast **150 DEGs** for `Sp4` in `151 TH Prkcd Grin2c Glut`.
