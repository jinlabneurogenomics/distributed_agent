# Sdccag8 DEG-count forecast

## Target and endpoint

- Target: `Sdccag8`
- Cell group: `151 TH Prkcd Grin2c Glut`
- Endpoint: `n_degs`, the count of measured genes with BH-adjusted Wilcoxon `p < 0.05`
- Point prediction: 0

## Evidence used

### Focal in-assay target reach

The declared biology bundle shows that the `Sdccag8` transcript is measurable in the
focal thalamic class: 18,573 of 23,679 non-target cells express it
(`78.44%`), with mean log1p CP10K `0.652` and pseudobulk CPM `108.62`.
This makes the target accessible to the assay, but the bundle explicitly warns
that exact target expression does not establish editing efficiency or functional
dependence.

The same bundle assigns the operative SDCCAG8 pool to centrioles and
centriolar satellites and adjudicates it as an installed complex or structure.
The strongest matched biology is constitutional or embryonic cortical loss;
there was no target-specific turnover or acute post-P16 depletion timecourse in
postmitotic thalamic neurons. I therefore treated acute P16 disruption as
biologically plausible but buffered by uncertain persistence of already installed
centrosomal/ciliary stock through the P37-P44 harvest window.

### Training count scale in the exact endpoint

The declared `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` table contains
1,674 training perturbations and no `Sdccag8` row. The endpoint is highly
zero-inflated:

- 1,205 of 1,674 training perturbations have `n_degs = 0`.
- The median is 0 and the 75th percentile is 1.
- Only 106 of 1,674 have `n_degs >= 10`.

The cilium/Hedgehog/BBS/IFT perturbations in that same table were almost all
flat in the focal cell group:

| training perturbation | n_degs |
|---|---:|
| Alms1 | 0 |
| Bbs5 | 0 |
| Cep120 | 0 |
| Cep290 | 0 |
| Cplane1 | 0 |
| Cspp1 | 0 |
| Gli1 | 0 |
| Gli2 | 0 |
| Htr6 | 0 |
| Ift43 | 0 |
| Ift81 | 0 |
| Ift88 | 0 |
| Lepr | 0 |
| Lztfl1 | 0 |
| Rpgrip1l | 0 |
| Smo | 0 |
| Ttc21b | 0 |
| Ttc8 | 1 |

The lone hit among these 18 genes was `Ttc8` itself. Re-reading the expression
Parquet for these exact training perturbations in `151 TH Prkcd Grin2c Glut`
confirmed that each had 17,259 measured genes, no downstream gene at FDR < 0.10,
and zero FDR < 0.05 genes except `Ttc8`, whose one FDR < 0.05 row was the
on-target transcript `Ttc8`.

`Mib1` was not used as a quantitative analogue despite ciliary adjacency: it had
27 focal DEGs, but those genes were a coherent sterol/cholesterol module
(`Insig1`, `Dhcr24`, `Fdft1`, `Ldlr`, `Msmo1`, `Hmgcs1`, `Hmgcr`, and related
SREBF2 targets), and the same-experiment corpus identifies this as a recurrent
sterol response rather than a generic ciliary transcriptional state.

### Packaged same-experiment interpretation

The same-experiment Finding ledger's packaged interpretations align with the
quantitative readout of ciliary buffering:

- `Alms1:F001`: 22 measured cell groups each had zero downstream genes at
  FDR < 0.10 after acute postmitotic `Alms1` perturbation.
- `Ttc8:F001`: all 22 measured groups had zero downstream genes at FDR < 0.10
  despite negative self-transcript trends.
- `Cep120:F001` and `Cep290:F001`: `Cep120` and `Cep290` produced pan-neuronal
  transcriptomic nulls.
- `Cplane1:F001`, `Rpgrip1l:F001`, `Ttc21b:F001`, `Ift88:F001`, `Cspp1:F001`,
  and `Lztfl1:F001`: the remaining structural cilium or ciliary-family
  perturbations produced at most isolated single-gene events in non-focal
  classes.
- `Bbs5:F003`, `Cep120:F002`, `Cep290:F003`, `Cplane1:F003`, `Ift88:F003`,
  `Rpgrip1l:F004`, and `Ttc21b:F002`: the ledger reports no robust shared
  BBSome/IFT/transition-zone/Hedgehog transcriptional module across those
  perturbations.

## Synthesis

`Sdccag8` reaches the focal cells and lacks a close paralog in the supplied
biology card, so I did not force an absolute null on targetability grounds. The
decisive feature was instead pathway behavior in the training experiment: acute
loss of several ciliary, BBSome, IFT, transition-zone, ciliary-GPCR, and
Hedgehog components is repeatedly silent in mature recovered neurons, including
this thalamic class. SDCCAG8 is another centriolar/ciliary scaffold with
developmental neuronal and retinal/renal ciliopathy evidence but no evidence
that P16 editing depletes an essential postmitotic thalamic stock by harvest.

Given the focal neighbor panel median of zero, the all-class corpus evidence for
ciliary buffering, and the absence of a specific Mib1-like sterol mechanism, the
most likely BH-significant DEG count for `Sdccag8` is a flat signature. I used a
point forecast of `0`, acknowledging residual uncertainty that an on-target
`Sdccag8` transcript loss could have produced a lone self hit analogous to
`Ttc8`.
