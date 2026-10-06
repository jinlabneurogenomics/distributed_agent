# DEG-count prediction for `151 TH Prkcd Grin2c Glut`

## Question and resolved ambiguities

The requested endpoint is the integer number of measured genes with
Benjamini-Hochberg-adjusted Wilcoxon `pvals_adj < 0.05` after a held-out mouse
gene perturbation in the focal `151 TH Prkcd Grin2c Glut` thalamic
glutamatergic cell group. The only requested held-out perturbation in
`the single-target request` was `Sos2`.

I treated the focal training CSV as the observed endpoint for non-held-out
targets and the Parquet as the expression-signature substrate for the same
targets. `Sos2` itself was held out: it is not in the training count table and,
as the Map2k1 report's unrepresented-comparator evidence also notes, not a
perturbation target in the supplied Parquet. I therefore predicted by
mechanistic transfer from represented Ras/MAPK perturbations, especially the
direct paralog `Sos1`, and did not treat broad pathway membership as sufficient
for a nonzero count.

## Sources used

- Declared endpoint table:
  `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
- Declared differential-expression Parquet:
  `training differential-expression dataset`.
- Requested target manifest:
  `single-target request for Sos2`.
- Run-local manifests: `task_bindings.json`, `coverage.json`, `capabilities.json`,
  `dataset_context.md`, and `dataset_context.json`.
- The internal same-experiment corpus
  `perturbai-july-260713-sourceguard-1773-v1`, queried with
  `corpus.findings`, `corpus.report_evidence`, and `corpus.calibration`.
  The corpus is another representation of this Perturb-seq experiment, not
  an independent replicate.
- External literature from PubMed:
  Li et al. 1993, DOI `10.1038/363085a0`, PMID `8479541`;
  Esteban et al. 2000, DOI `10.1128/MCB.20.17.6410-6413.2000`,
  PMID `10938118`;
  Baltanas et al. 2013, DOI `10.1128/MCB.01026-13`, PMID `24043312`;
  Baltanas et al. 2020, DOI `10.1016/j.bbcan.2020.188445`,
  PMID `33035641`.

## Quantitative calibration

The focal training endpoint has 1,674 non-held-out targets. It is sparse:
1,205 targets have `n_degs = 0`, 469 are nonzero, the median is 0, the 75th
percentile is 1, and the maximum is 2,677. Thus a target-specific analog had
to overcome a strong baseline zero expectation before I would predict any DEG.

I first searched the focal count table for represented RTK/RAS/RAF/MEK/ERK
targets. In the requested cell group their FDR 0.05 endpoint counts were:

| training perturbation | relationship to `Sos2` | focal `n_degs` |
|---|---|---:|
| `Sos1` | closest represented paralog; upstream Ras/Rac GEF | 0 |
| `Braf` | downstream RAF kinase in the branch with a detectable response | 4 |
| `Map2k1` | downstream MEK1 kinase in the detectable response | 4 |
| `Ntrk2` | neurotrophin receptor that partially shares the VGF branch | 3 |
| `Shoc2` | SHOC2-MRAS-PP1 RAF activator, weak one-gene overlap | 1 |
| `Lztr1` | RASopathy-pathway regulator with different focal direction | 1 |
| `Map2k2` | MEK2 | 0 |
| `Mapk1` | ERK2 | 0 |
| `Ptpn11` | SHP2, upstream positive RTK/RAS signal relay | 0 |
| `Raf1` | RAF1/CRAF | 0 |
| `Hras` | classical RAS isoform | 0 |
| `Kras` | classical RAS isoform | 0 |
| `Rasa2` | Ras GAP | 0 |
| `Spred1`, `Spred2` | negative RAS/RAF regulators | 0, 0 |

I then queried the Parquet for the focal `Vgf`/`Ptpn5`/`Unc13a`/`Etv5`
module and for canonical immediate-early or ERK-feedback genes. The matched
rows showed:

- `Braf`: `Vgf` logFC -0.795, FDR 1.39e-4; `Ptpn5` -0.635, FDR 1.39e-4;
  `Atp2a2` -0.263, FDR 1.39e-4; `Unc13a` -0.315, FDR 0.00393.
- `Map2k1`: `Vgf` -0.785, FDR 7.85e-8; `Ptpn5` -0.436, FDR 9.37e-4;
  `Unc13a` -0.325, FDR 0.0119; `Etv5` -0.631, FDR 0.0119.
- `Ntrk2`: `Vgf` -0.618, FDR 0.00488; `Atp2a2` -0.230, FDR 0.00237.
- `Shoc2`: `Vgf` -0.660, FDR 0.00794.
- `Sos1`: `Vgf`, `Ptpn5`, `Unc13a`, `Etv5`, `Atp2a2`, `Fos`, `Egr1`,
  `Arc`, `Dusp6`, and `Spry2` were all nonsignificant in the focal cell group;
  the only near hit was `Cul7` up-regulation, logFC 1.005, adjusted
  p-value 0.0778, which is outside the requested FDR 0.05 endpoint.
- `Hras`, `Kras`, `Raf1`, `Map2k2`, `Mapk1`, `Ptpn11`, and `Spred2` did not
  share the focal RAF/MEK module at FDR 0.05.

The selected same-experiment corpus reports supported the same reading:

- `Sos1:F001`/`Sos1:E018`: the only FDR<0.10 downstream Sos1 response was
  `Cul7` in 151 TH Prkcd Grin2c Glut, with FDR 0.0778.
- `Sos1:F002`: `Sos1` did not recapitulate the `Braf` or `Map2k1` thalamic
  RAF/MEK attenuation signature.
- `Sos1:F004`: full transcriptome-wide residual matching found no stable
  positive or negative `Sos1` signature neighbor.
- `Braf:F004` and `Map2k1:F004`: most obvious RAS/MAPK comparators
  represented in the Parquet, including `Sos1`, `Raf1`, `Kras`, `Hras`,
  `Ptpn11`, `Mapk1`, and `Map2k2`, failed to phenocopy the small
  `Braf`/`Map2k1` VGF/PTPN5/UNC13A module.

## Target-specific prediction

### `Sos2`

`Sos2` encodes a Son of Sevenless guanine nucleotide exchange factor. SOS
proteins couple receptor-tyrosine-kinase/GRB2 complexes to RAS activation, and
SOS1 and SOS2 are homologous, ubiquitously expressed Ras/Rac GEFs
(Li et al. 1993, PMID 8479541; Baltanas et al. 2020, PMID 33035641). That
biology nominates `Sos1` as the nearest represented loss-of-function analog,
and `Braf`, `Map2k1`, `Raf1`, `Hras`, `Kras`, `Mapk1`, and `Ptpn11` as more
distant same-cascade checks.

The causal transfer model is:

`Sos2` CRISPR loss -> reduced SOS2-mediated Ras nucleotide exchange downstream
of activated receptors -> potentially lower RAF/MEK/ERK and RAC signaling,
depending on SOS1 compensation and stimulus routing -> survivor-conditioned
steady-state nuclear RNA 3-4 weeks later -> FDR-significant DEGs in recovered
151 thalamic glutamatergic nuclei.

For this assay and endpoint, the transfer from `Sos1` is same-direction but
low-magnitude. A `Sos2` hit should perturb an even more buffered point than
the measured `Sos1` hit: germline Sos2 catalytic-domain disruption in mouse
was compatible with normal development, growth, fertility, and histology
(Esteban et al. 2000, PMID 10938118), inducible adult single `Sos1` or `Sos2`
knockout animals were viable while combined Sos1/Sos2 loss was lethal
(Baltanas et al. 2013, PMID 24043312), and reviews emphasize a dominant
SOS1 contribution with SOS2 redundancy or context-specific roles rather than
a uniformly dominant SOS2 role (Baltanas et al. 2020, PMID 33035641).

The same-experiment data reinforce that expectation. The screen could detect a
small downstream `Braf`/`Map2k1` ERK-linked module in this cell group, but
direct `Sos1` loss failed to drive `Vgf`, `Ptpn5`, `Unc13a`, `Etv5`,
immediate-early genes, or ERK-feedback genes across the FDR 0.05 line. The
RAS isoforms, RAF1, MEK2, ERK2, and SHP2 were also focal-cell zeroes. Those
flat upstream and terminal perturbations are better counterexamples for
`Sos2` than the four-gene `Braf` and `Map2k1` positives, because the positives
are kinase-level lesions on the one branch that escaped upstream buffering.

I therefore predict no genes below adjusted p-value 0.05:

`predicted_n_degs(Sos2) = 0`.

## Limits

This is extrapolation from the represented `Sos1` perturbation and other
RAS/MAPK perturbations, because `Sos2` itself was completely withheld and no
`Sos1`/`Sos2` double perturbation exists in the input. The transfer assumes
that SOS1 compensation in postnatal thalamic glutamatergic neurons is at least
as effective after SOS2 loss as SOS2 compensation is after SOS1 loss; that is
well aligned with organismal mouse genetics, but was not directly assayed in
these nuclei. The Parquet is a chronic basal snRNA-seq readout in recovered
cells, so it can miss acute receptor-evoked pERK/RAS signaling, phosphoprotein
effects, and selection before sampling. A small one- or two-gene `Sos2`
signature near the multiple-testing boundary would therefore not be
biologically surprising, but the best focal quantitative analogs put the point
estimate at zero.
