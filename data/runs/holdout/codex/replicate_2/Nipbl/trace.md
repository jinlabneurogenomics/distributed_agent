# Nipbl direct n_degs prediction

Endpoint: `n_degs` for `Nipbl` in `151 TH Prkcd Grin2c Glut`, i.e. measured genes with BH-adjusted Wilcoxon `p < 0.05`.

## Inputs used

- Declared holdout manifest: one target, `Nipbl`.
- Declared Nipbl biology bundle.
- `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`, containing 1,674 non-held-out biological targets.
- `training_de_all_cell_groups.parquet`, queried only for non-held-out comparator profiles in `151 TH Prkcd Grin2c Glut`.
- Same-experiment corpus Findings for measured chromatin and cohesin comparators. The selected corpus had no packaged Nipbl report, Claim, or Finding, so the Nipbl target outcome was not available there.

## Evidence

The Nipbl card supports target reach and realization. In the exact focal population, the target transcript was available and detected in 20,373 of 23,679 non-target nuclei, 86.04%, with mean raw UMI 2.34 and pseudobulk CPM 146.6. The functional-stock adjudication treats NIPBL as a dynamic cohesin-loading/ATPase regulator whose operative stock should be substantially depleted by the P37-P44 harvest after P16 editing, rather than a stable product installed before the edit.

The qualitative prior is not a perfect endpoint match. The strongest stock evidence comes from acute depletion in human cell systems, including iPSC-derived glutamatergic neurons, plus fast chromatin exchange in HeLa cells; the postnatal mouse evidence is forebrain/Camk2a rather than thalamus and does not give a precise 21-28 day onset curve. Severe postnatal Nipbl loss could also be survivor-conditioned in this snRNA-seq assay, leaving a smaller recovered-cell signature than the full biological impact.

The focal training count table is sparse and heavy-tailed: among 1,674 training targets, 1,205 had `n_degs=0`, the median was 0, the 95th percentile was 18, and the 97.5th percentile was 100. Thus an expressed, realized chromatin regulator should be moved well above the median, but a count above a few hundred is an exceptional tail event.

The closest measured cohesin/loop-axis comparators were mixed:

| comparator | `n_degs` in 151 |
|---|---:|
| `Ctcf` | 270 |
| `Stag2` | 37 |
| `Smc1a` | 24 |
| `Stag1` | 0 |
| `Pds5a` | 0 |
| `Hdac8` | 0 |

The expression parquet confirmed these `p_adj < 0.05` counts directly in the 151 slice and showed that `Smc1a` and `Stag2` share a compact negative program with `Ctcf`, while being far smaller than `Ctcf`: `Ctcf` had 151 positive and 119 negative significant genes, `Smc1a` had 3 positive and 21 negative, and `Stag2` had 8 positive and 29 negative. In profile comparisons within the selected cohort, `Ctcf`'s nearest whole-profile peers were `Smc1a`, `Stag2`, and `Chd4`, but the signed correlations were modest rather than strong.

Broader chromatin regulators establish an upper scale but are less direct. `Chd4` had 100 genes, `Brd4` 311, `Setd1a` 368, `Yy1` 720, and `Sin3a` 1433 in the same count table, whereas `Crebbp`, `Ep300`, `Kat6a`, and `Setd2` were near-flat. Packaged same-experiment Findings likewise separated the `Ctcf` footprint from `Smc1a`/`Stag2` and reported that measured cohesin-machinery perturbations did not phenocopy the broader `Ctcf` response.

## Synthesis

I treated `Smc1a`/`Stag2` as the main quantitative floor because Nipbl loss should perturb the same cohesin-loading and loop-extrusion axis, but not every core/cofactor perturbation on that axis is large in recovered P16-edited neurons. I treated `Ctcf` and `Chd4` as the nearest high-response scale references, with `Brd4`/`Yy1`/`Sin3a` as broader chromatin tail examples rather than direct magnitude donors.

The point estimate is therefore above the 24-37 gene core-cohesin counts because NIPBL has no close replacement loader and is expressed across most focal nuclei, but below the 270-gene `Ctcf` count and far below the global transcription-regulator tail because NIPBL's best-matched measured machinery gave only compact recovered signatures and severe loss may be attenuated by survivor conditioning.

Predicted `n_degs`: 80.
