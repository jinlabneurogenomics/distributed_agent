# Reasoning trace

## Question and endpoint

The task is to predict `n_degs` for every requested held-out perturbation in
`151 TH Prkcd Grin2c Glut` cells. I interpreted `n_degs` as exactly the
training endpoint: the number of measured genes whose Wilcoxon
Benjamini-Hochberg-adjusted p-value is `< 0.05` in that focal cell group, using
the supplied Perturb-seq differential-expression table.

The held-out manifest contains one perturbation:

| held-out target | prediction |
|---|---:|
| Bbs9 | 0 |

The requested output is a scalar count, not a ranking. `Bbs9` is completely
withheld as a perturbation from both the Parquet and the focal-cell training
count CSV, so its focal expression signature is absent. The endpoint itself is
directly observed for training perturbations in
`151 TH Prkcd Grin2c Glut`; no viability, cell-abundance, ciliary-localization,
or ligand-response endpoint is directly observed in these inputs.

## Sources used

- Declared training endpoint:
  `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
- Declared differential-expression data:
  `training differential-expression dataset`.
  I queried focal-cell rows for represented BBS/ciliary comparators to confirm
  DEG counts, matched perturbed-cell counts, and the identity of any focal
  FDR-significant row.
- Internal same-experiment corpus:
  PerturbAI July release `perturbai-july-260713-sourceguard-1773-v1`, especially
  Finding and Evidence records for `Bbs5`, `Ttc8`, `Lztfl1`, `Ift88`, and
  `Cep290`. These reports are interpretations of the same experiment, so I used
  them as compact Parquet-derived evidence, not as independent replication.
- External biological priors:
  Reactome, BBSome-mediated cargo-targeting to cilium, `R-HSA-5620922`;
  Nachury et al. 2007, Cell, doi:10.1016/j.cell.2007.03.053;
  Seo et al. 2011, PLoS Genetics, doi:10.1371/journal.pgen.1002358,
  PMID:22072986;
  Zhang et al. 2012, Journal of Biological Chemistry,
  doi:10.1074/jbc.M112.341487, PMID:22500027;
  Veleri et al. 2012, PLoS ONE, doi:10.1371/journal.pone.0034389,
  PMID:22479622;
  Nozaki et al. 2018, PLoS ONE, doi:10.1371/journal.pone.0195005,
  PMID:29590217;
  Nozaki et al. 2019, Biology Open, doi:10.1242/bio.043786,
  PMID:31471295.

## Dataset calibration

The focal training-count table has 1,674 visible perturbations. It is strongly
zero-inflated: 469 perturbations have `n_degs > 0`, the median is 0, the
75th percentile is 1, the 95th percentile is 18, and large signatures are rare
right-tail events. A zero prediction is therefore common, but I did not use that
bulk rate alone for `Bbs9`; I conditioned on BBSome and ciliary neighbors.

For focal rows I counted, per represented analog,

```sql
sum(case when pvals_adj < 0.05 then 1 else 0 end)
```

after filtering `group_name = '151 TH Prkcd Grin2c Glut'`. This exactly matches
the training-count definition. The relevant focal counts were:

| training perturbation | relationship to Bbs9 | focal n_degs |
|---|---|---:|
| Bbs5 | represented core BBSome subunit | 0 |
| Ttc8 / Bbs8 | represented core BBSome subunit | 1 |
| Lztfl1 / Bbs17 | BBSome trafficking regulator | 0 |
| Ift88, Ift81, Ift43 | IFT-B/ciliary transport | 0, 0, 0 |
| Kif3b, Dync2h1, Dync2i1, Ttc21b | anterograde/retrograde IFT machinery | 0, 0, 0, 0 |
| Cep290, Rpgrip1l, B9d1, Cplane1, Cspp1, Pibf1 | transition-zone or ciliopathy comparators | 0, 0, 0, 0, 0, 0 |
| Smo, Gli1, Gli2, Ptch1, Ptch2 | Hedgehog effectors read through cilia | 0, 0, 0, 0, 0 |
| Adcy3, Htr6, Gpr161, Mchr1, Lepr | neuronal ciliary GPCR / BBSome-linked cargo axes | 0, 0, 0, 0, 0 |

The one focal `Ttc8` hit is the target transcript itself
(`Ttc8` log2FC = -0.663, adjusted p = 3.07e-5; 180 matched perturbed nuclei
versus 23,679 controls), with no FDR-significant downstream focal gene. `Bbs5`
had 121 matched perturbed nuclei, `Lztfl1` 199, and `Ift88` 143 in the same
focal group, enough to detect the large focal signatures seen for unrelated
genes such as `Uba5`, `Tpr`, `Sin3a`, and `Rnpc3`, but all three were focal
zeros.

## Target-specific reasoning

### Bbs9

External biology makes `Bbs9` a good match to `Bbs5` and `Ttc8`, not a random
ciliary gene. The BBSome is an octameric coat/adaptor for ciliary membrane
proteins; Reactome curates BBSome-mediated cargo targeting to cilia, Nachury et
al. defined the BBSome as cooperating with Rab8 in ciliary membrane biogenesis,
and Zhang et al. showed that BBS7, BBS2, and BBS9 form a core BBSome assembly
intermediate before BBS1, BBS5, BBS8, and BBS4 are added. Veleri et al. showed
that BBS9 loss perturbs cilia in zebrafish and mouse IMCD3 cells. Nozaki et al.
also place BBS9 at functional interfaces in the core BBSome: BBS9 reinforces
the ARL6-BBS1 interaction used for retrograde trafficking of Smoothened and
GPR161, and BBS1/BBS2/BBS9 contact IFT38 in the IFT-B/BBSome export axis.

That causal chain predicts that acute `Bbs9` loss could disrupt the same
subcellular process as `Bbs5` or `Ttc8`: BBSome assembly and ciliary cargo
export. In this postnatal neuronal snRNA-seq experiment, however, the measured
endpoint is a basal nuclear transcriptional response among recovered neurons,
not cilium morphology or receptor localization. The directly represented
same-complex and same-pathway perturbations show that impairing this ciliary
transport system was transcriptionally quiet in the focal thalamic glutamatergic
class:

- `Bbs5`, the only other represented core BBSome subunit besides `Ttc8`, had
  0 focal DEGs.
- `Ttc8/Bbs8` had 1 focal DEG, but it was just the depleted `Ttc8` transcript
  and there was no downstream focal hit.
- `Lztfl1`, which interacts with the BBSome and regulates BBSome/Smoothened
  trafficking, had 0 focal DEGs.
- `Ift88`, other IFT genes, ciliary transition-zone genes, and the basal
  Hedgehog/neural-ciliary-GPCR readout genes listed above were all focal nulls.

The July same-experiment corpus supports the same transfer. `Bbs5:F003`
reported that `Ttc8`, `Lztfl1`, `Ift88`, `Cspp1`, `Gli1`, `Smo`, `Lepr`, and
`Htr6` produced only isolated, non-overlapping one-gene effects across the
atlas, not a shared BBSome/ciliary module. Its Evidence record `Bbs5:E009`
quantified Bbs5-to-ciliary-comparator 21-group Wilcoxon-score correlations near
zero, including `Ttc8` r = 0.0205, `Ift88` r = 0.0128, `Lztfl1` r = 0.0122,
`Smo` r = 0.0066, `Gli1` r = 0.0059, and `Htr6` r = 0.0002. `Ttc8:F003` and
`Ttc8:E027` likewise found that represented BBSome, IFT, and transition-zone
perturbations were nearly orthogonal to `Ttc8` and had no shared FDR-significant
downstream response in matched neuronal groups. `Lztfl1:F003`/`E010` showed
that even in the one cell class with a weak `Lztfl1` signal, Bbs5, Ttc8, IFT,
transition-zone, and related ciliopathy genes did not phenocopy it.
`Ift88:F004` and `Cep290:F003` further checked the expected Hedgehog, GPCR, BBS,
and IFT axes and found no broad basal transcriptomic response.

I therefore predict that a held-out `Bbs9` perturbation would impair the same
BBSome function but, in recovered postnatal `151 TH Prkcd Grin2c Glut` nuclei,
would usually remain subcellular or ligand-context-dependent rather than
crossing the FDR < 0.05 threshold for a stable basal mRNA program. The best point
prediction is exactly the Bbs5/Lztfl1/Ift88 focal behavior, `0`, rather than the
self-only `Ttc8 = 1`, because the `Ttc8` count does not represent a downstream
transcriptional state and Bbs5 itself did not even yield a detectable focal
self-transcript hit.

## Limits and uncertainty

- The prediction extrapolates from `Bbs5`, `Ttc8`, and BBSome regulators because
  `Bbs9`, `Bbs1`, `Bbs2`, `Bbs4`, `Bbs7`, `Bbip1`, `Arl6/Bbs3`, `Bbs10`,
  `Bbs12`, and `Mkks` were not represented as perturbation targets.
- A zero focal DEG count does not mean no Bbs9 editing, no cilium phenotype, or
  no neuronal consequence. The input assay did not image cilia, localize
  Smoothened/GPR161/SSTR3/HTR6/MCHR1/Lepr proteins, stimulate Hedgehog or
  leptin signaling, or quantify pre-assay selection.
- The BBSome evidence is strongest for ciliary trafficking and retinal,
  epithelial, IMCD3, fibroblast, or embryonic phenotypes. Transfer to sparse
  P16-to-P37/44 NeuN+ thalamic glutamatergic nuclei is specifically limited by
  cell type, developmental stage, and basal unstimulated snRNA-seq modality.
- The BBSome is an obligate complex, but individual subunit deletions can have
  specialized or tissue-specific behavior. That is why I used `Bbs5`, `Ttc8`,
  `Lztfl1`, and IFT/transition-zone counterexamples as bounded endpoint
  evidence, not as a universal rule that every ciliary perturbation is silent.
- The integer point prediction hides substantial uncertainty at the 0-versus-1
  boundary: a detectable `Bbs9` self-transcript knockdown alone could produce
  `n_degs = 1` without contradicting the expectation of no downstream response.
