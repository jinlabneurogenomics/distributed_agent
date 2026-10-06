# DEG-count prediction for held-out Atp6ap1

## Question and endpoint

The requested held-out target set contains one perturbation, `Atp6ap1`. I
predicted its `151 TH Prkcd Grin2c Glut` DEG burden, where the endpoint is the
number of measured genes with `pvals_adj < 0.05` after acute AAV-CRISPR
loss-of-function in recovered postnatal mouse neuronal nuclei. Counts include
the target transcript itself when that row passes FDR. The held-out
`Atp6ap1` expression signature and DEG count are absent from both supplied
inputs, so I transferred from non-held-out training perturbations.

The prediction is for this sparse, mosaic, survivor-conditioned snRNA-seq
assay. I did not interpret absent DE as a complete biological null, and I did
not use measured loss of the target transcript as an editing-efficiency score.

## Sources used

- Declared differential-expression Parquet:
  `training differential-expression dataset`.
  This is the direct source for focal-cell log fold-changes, adjusted
  Wilcoxon p-values, and matched-nucleus counts.
- Declared focal training counts:
  `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
  This is the direct source for the observed `n_degs` endpoint on training
  targets.
- Requested-target manifest:
  `single-target request for Atp6ap1`.
- Internal same-experiment corpus `perturbai-july-260713-sourceguard-1773-v1`,
  through the declared `corpus.report_evidence` capability, for compact
  report Evidence around `Atp6ap2`, `Atp6v0a1`, `Rab7`, `Mtor`, and `Tsc2`.
  The corpus is a structured interpretation of this Perturb-seq experiment, not
  an independent replicate.
- Independent PubMed literature for the held-out gene and V-ATPase biology:
  Jansen et al. 2016, doi:10.1038/ncomms11600; Abbas et al. 2020,
  doi:10.1126/science.aaz2924; Rujano et al. 2017,
  doi:10.1084/jem.20170453; Jansen and Martens 2012,
  doi:10.2174/138920312800493160; Yang et al. 2012,
  doi:10.1002/jbmr.1623; and Schoonderwoert and Martens 2002,
  doi:10.1080/09687680110112910.

## Quantitative work over the declared inputs

The training endpoint is highly zero-inflated in the focal cell group: 1,205 of
1,674 training targets had `n_degs = 0`, 469 were nonzero, the median was 0, and
the largest response was `Uba5` with 2,677 DEGs.

I first intersected a hand-defined V-ATPase, endolysosomal, and mTORC1
mechanistic set with the 1,674 available training targets. The direct
V-ATPase/accessory perturbations present were only:

| training target | focal `n_degs` |
|---|---:|
| `Atp6ap2` | 2 |
| `Atp6v0a1` | 1 |
| `Atp6v1a` | 0 |
| `Atp6v1b2` | 0 |
| `Atp6v1e1` | 0 |

I also retained nearby counterexamples that were present in training:

| training target | focal `n_degs` |
|---|---:|
| `Ctsb` | 1 |
| `Lamp2` | 0 |
| `Mtor` | 2 |
| `Psen1` | 0 |
| `Rab7` | 501 |
| `Rptor` | 0 |
| `Tsc2` | 86 |
| `Vps35` | 17 |
| `Vps41` | 0 |

For these 14 perturbations I queried the Parquet with `group_name =
'151 TH Prkcd Grin2c Glut'` and exact `gene_target` filters. I wrote compact
intermediate tables under `workbench/`:

- `related_all_cell_deg_counts.tsv`: per-target, per-cell-group counts at
  FDR < 0.05 and FDR < 0.10.
- `related_focal_fdr25.tsv`: every focal-cell row for the 14 targets with
  `pvals_adj < 0.25`.
- `related_focal_top20.tsv`: the top 20 focal-cell rows per target by adjusted
  p-value.
- `vatpase_target_gene_lfcs.tsv`: the focal-cell log fold-changes and adjusted
  p-values of `Atp6ap1`, `Atp6ap2`, `Atp6v0a1`, `Atp6v1a`, `Atp6v1b2`, and
  `Atp6v1e1` inside each retained training perturbation.

The direct V-ATPase/accessory signatures were sparse even in the high-yield
focal group. `Atp6ap2` produced 2 FDR < 0.05 rows in `151 TH Prkcd Grin2c
Glut`: its own transcript, logFC -1.667, FDR 1.90e-28, and `Atp6v0a1`, logFC
-0.341, FDR 1.30e-04. Its next focal rows, `Prkcg` and `Asb18`, were already
above FDR 0.20. `Atp6v0a1` produced exactly 1 FDR < 0.05 row, its own
transcript, logFC -0.640, FDR 4.52e-12; the nearest downstream row was `Kcnc2`
at FDR 0.125. `Atp6v1a`, `Atp6v1b2`, and `Atp6v1e1` had no focal rows even
near FDR 0.25. Across cell groups, `Atp6v0a1` had no robust downstream response
at FDR < 0.10 after excluding the target transcript, and the internal corpus
records the same finding for the full Atp6v0a1 surface.

The high-count endolysosomal hits were not treated as same-endpoint phenocopies.
`Rab7` loss gave 501 focal DEGs and strongly up-regulated lysosomal and
V-ATPase-adjacent transcripts, including `Atp6v1b2`, `Dpp7`, `Atp6v0b`,
`Lamp2`, `Atp6ap1`, and `Atp6v1a`. The direction of this signal is consistent
with a late endosomal stress or compensatory lysosomal biogenesis state after
loss of Rab7-dependent trafficking, not with the almost silent signature of
core V-ATPase loss. `Tsc2` loss gave 86 focal DEGs and a sterol/PI3K/lysosomal
program; it is also not a same-sign analog because TSC loss derepresses
Rheb-mTORC1, whereas a V-ATPase assembly or lysosomal sensing defect is
expected to reduce lysosomal mTORC1 activation. The direct `Mtor` perturbation
itself had only 2 focal DEGs, and `Rptor` had 0, which argues that the
inhibitory side of this branch is low-yield in the assay.

## Target-specific causal transfer

`Atp6ap1` encodes Ac45, an accessory factor of the V0 sector of the V-ATPase.
It participates in V0 assembly and the assembled mammalian brain V-ATPase
structure contains cleaved ATP6AP1/Ac45 and ATP6AP2/PRR in the membrane sector
(Abbas et al. 2020). ATP6AP1 disease alleles impair V-ATPase-dependent growth in
yeast complementation and cause an X-linked congenital disorder with abnormal
glycosylation, immunodeficiency, hepatopathy, and neurocognitive phenotypes
(Jansen et al. 2016). ATP6AP2 mutants can reduce interaction with ATP6AP1 and
impair V-ATPase assembly, lysosomal acidification, and autophagy in model
systems (Rujano et al. 2017). These data make the training `Atp6ap2` and
`Atp6v0a1` perturbations the nearest same-complex analogs in the focal DEG-count
dataset.

The causal chain I used was: acute `Atp6ap1` CRISPR loss of function -> impaired
V0 assembly/accessory activity of the V-ATPase -> altered organellar
acidification and possibly weaker Rheb/mTORC1 activation -> stress or
compensatory lysosomal transcription only in recovered `151 TH Prkcd Grin2c
Glut` nuclei if the perturbation crosses the assay's threshold. The closest
training perturbations affect the same chain but show that this experiment did
not convert partial V-ATPase disruption into a broad detectable focal
transcriptional state. The `Atp6ap2` focal surface was essentially a self row
plus lower `Atp6v0a1`; the `Atp6v0a1` surface was self-only; three V1-sector
perturbations were FDR-zero.

`Rab7` is a useful counterexample, not a count donor. Rab7 controls late
endosome to lysosome traffic and recruitment of effectors such as RILP and HOPS
(Guerra and Bucci 2016; Yang et al. 2012 also link Ac45 to Rab7-dependent
lysosomal trafficking in osteoclasts). The intervention stage differs:
`Rab7` loss blocks late-endosome transport and triggers a strong compensatory
up-regulation of lysosomal and V-ATPase genes, including `Atp6ap1` itself; loss
of `Atp6ap1` is a structural/accessory V-ATPase lesion and the measured V-ATPase
lesions did not trigger the Rab7 state. `Tsc2` is also a counterexample because
it acts as a negative regulator upstream of Rheb; losing it increases rather
than decreases mTORC1 drive, producing the opposite branch of the lysosomal
nutrient-sensing network.

I therefore predict a very small but nonzero focal response. The nonzero part is
driven mainly by the probability that the `Atp6ap1` transcript itself will pass
FDR, as `Atp6ap2` and `Atp6v0a1` did in this cell group, rather than by an
expectation of hundreds of downstream lysosomal genes. I used 1 as the point
prediction: close to the 0 to 2 direct V-ATPase/accessory counts, lower than
`Atp6ap2` because its second row was specifically `Atp6v0a1` rather than a
general stress program, and far below `Rab7` and `Tsc2` because those perturb a
different causal stage or sign.

## Prediction

| target_name | predicted_n_degs |
|---|---:|
| `Atp6ap1` | 1 |

## Limits

This is an extrapolation from related genes because the `Atp6ap1` Perturb-seq
signature was held out completely. The direct V-ATPase comparison set is small,
and the trained V1 subunits had modest matched perturbed-cell counts in
`151 TH Prkcd Grin2c Glut` (`Atp6v1b2` had 32, `Atp6v1e1` 52, `Atp6v1a` 76),
so a weak downstream V-ATPase state could fall below FDR. Conversely, the
`Atp6ap2` and `Atp6v0a1` signatures had strong self-transcript rows or more
cells yet still lacked broad downstream lysosomal, CLEAR, UPR, or mTORC1-marker
programs, supporting a low count. Literature from embryonic null, human
germline disease, cancer, beta-cells, and osteoclasts establishes the V-ATPase
and lysosomal roles of ATP6AP1 but does not determine the DEG burden after
sparse postnatal neuronal CRISPR editing. The final integer is therefore a
best focal-assay prediction, not a statement that ATP6AP1 biology is weak.
