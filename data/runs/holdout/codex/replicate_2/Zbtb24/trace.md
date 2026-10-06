## Target

- Held-out perturbation: `Zbtb24`
- Focal population: `151 TH Prkcd Grin2c Glut`
- Endpoint: measured genes with Wilcoxon BH-adjusted `pvals_adj < 0.05`

## Evidence used

### Biology-only target bundle

The canonical Zbtb24 bundle exposes focal-population baseline reach but not the held-out response. In the exact focal population, `Zbtb24` was detected in 13,491 of 23,679 non-target nuclei, with 56.97% of nuclei expressing it, mean raw UMI 0.911, mean CP10k 0.580, and pseudobulk CPM 57.12. This argues against treating the perturbation as unreachable purely because of absent target expression.

The same bundle identifies ZBTB24 as a sequence-specific transcription factor that activates `Cdca7` and thereby the CDCA7-HELLS chromatin-remodeling and DNA-methylation pathway. Its direct evidence is from mouse ESCs, biochemical assays, early mouse embryos, and hematopoietic conditional loss rather than postnatal thalamic neurons. The functional-stock card calls harvest-time loss only `partially_depleted_or_leading_edge`: the P16 edit should stop new ZBTB24 production, but pre-edit protein, pre-existing occupancy, and methylated chromatin can persist for part or all of the 21-28 day interval.

### Training count table

The declared `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` table contains 1,674 training perturbations after the Zbtb24 holdout. Its endpoint is extremely zero-inflated:

- 1,205 / 1,674 training targets had `n_degs = 0`.
- The median was 0.
- The 75th, 90th, and 95th percentiles were 1, 2, and 18 DEGs.
- Only 42 targets exceeded 100 DEGs.

The direct CDCA7-HELLS pathway was not available as a measured perturbation donor in this focal count table: `Cdca7`, `Hells`, and `Zbtb24` itself were absent.

I ran the local curated analog nomination against the exact 1,674-gene training universe. It resolved Zbtb24 but found no exact paralog, exact complex partner, narrow module partner, direct interaction/dependency, or bidirectional same-experiment comparator. All 826 available nominees were broad functional fallbacks, so I did not treat any nominee as a close scalar donor.

The most informative low-level TF fallbacks were quiet:

| comparator set | measured counts |
| --- | --- |
| early broad nominees | `Zbtb20=0`, `Gata3=0`, `Stat3=0`, `Rest=0`, `Trp53=0`, `Ahr=0`, `Litaf=0`, `Tbx1=0`, `Pax6=0`, `Ep300=0`, `Foxp3=0`, `Smad3=0`, `Crebbp=8`, `Zbtb7a=841`; median 0 |
| other ZBTB-family training targets | `Zbtb10=0`, `Zbtb16=0`, `Zbtb18=5`, `Zbtb20=0`, `Zbtb21=0`, `Zbtb38=1`, `Zbtb7a=841`; median 0 |
| manually retained low TF/chromatin fallbacks | `Zbtb20=0`, `Rest=0`, `Zfat=2`, `Gata3=0`, `Stat3=0`, `Ahr=0`, `Bcl11a=0`, `Zbtb16=0`, `Zbtb10=0`, `Zbtb21=0`, `Zbtb18=5`, `Zbtb38=1`, `Zfp148=8`; median 0, mean 1.23 |

There were chromatin perturbations with clear thalamic DEG burdens, for example `Mecp2=16`, `Setdb1=22`, `Chd8=61`, `Chd4=100`, and `Smarcc2=185`, with larger transcriptional hubs such as `Ctcf=270`, `Setd1a=368`, `Yy1=720`, and `Zbtb7a=841`. I used these as evidence that chromatin/transcription regulators can score in this population, but not as direct scale donors for Zbtb24 because they are core remodelers, methyl-CpG readers, chromatin architectural proteins, or broad transcriptional hubs rather than the sequence-specific ZBTB24-to-CDCA7 entry point with an uncertain installed methylation reserve.

### Focal expression-parquet comparison

I compared 18 measured TF/chromatin fallbacks in the declared expression parquet within `151 TH Prkcd Grin2c Glut`: `Zbtb20`, `Zbtb18`, `Zbtb38`, `Zbtb7a`, `Rest`, `Zfat`, `Mecp2`, `Dnmt3a`, `Setdb1`, `Smarca4`, `Chd4`, `Chd8`, `Arid1a`, `Smarcc2`, `Setd1a`, `Rora`, `Ctcf`, and `Yy1`.

The 153-pair cohort was not a single coherent Zbtb24-like state. Mean positive top-tail overlap was 0.076 and median significant-program overlap was 0 in the positive direction; the individual fallback counts also ranged from 0 to 841 DEGs. That dispersion reinforced treating high-count hub perturbations as upper context, while centering Zbtb24 near the broad TF/ZBTB mode.

## Synthesis

Zbtb24 has enough baseline expression in the target population for a response to be measurable, and the knockout could eventually impinge on chromatin maintenance through CDCA7-HELLS. The contrary evidence is stronger for this exact endpoint: the experimentally timed postmitotic neuron context is not directly established, the functional-stock card expects only partial or leading-edge depletion of the combined protein/chromatin state by P37-P44, exact pathway perturbations were absent from the training donor table, and the broad TF/ZBTB comparators in the same focal population were overwhelmingly `0` or low single-digit.

I therefore placed Zbtb24 in the modal quiet class rather than borrowing scale from large global chromatin hubs. My point forecast is:

`n_degs = 0`
