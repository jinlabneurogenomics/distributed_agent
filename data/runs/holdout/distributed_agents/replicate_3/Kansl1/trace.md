# DEG-count prediction for `Kansl1`

## Question and resolved ambiguities

The requested held-out target file contains one perturbation:

```text
Kansl1
```

I interpreted the task as a point prediction for the number of genes that would
have `pvals_adj < 0.05` in the held-out `Kansl1` perturbation in the focal
`151 TH Prkcd Grin2c Glut` cell group. The output endpoint is therefore not
effect size, essentiality, target knock-down, or disease relevance; it is the
BH-adjusted Wilcoxon DEG count that would have appeared in
`151 TH Prkcd Grin2c Glut` if `Kansl1` had not been held out.

## Sources used

- Held-out manifest:
  `[local file: 116_Kansl1.csv]`.
- Training endpoint counts:
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
- Training differential-expression parquet:
  `[local file: training_de_all_cell_groups.parquet]`.
- Run-local focal profile-neighbor search over the parquet, written to
  `kansl1_profile_neighbors.json`.
- Distributed Agents internal corpus release
  `perturbai-july-260713-sourceguard-1773-v1`. `Kansl1` itself was not present
  in the corpus, but the corpus contained relevant same-assay summaries for
  `Ogt`, `Msl2`, `Crebbp`, `Setd1a`, and `Chd8`.
- External mechanism priors:
  CORUM 4.0 places KANSL1, KANSL2, KANSL3, KAT8/MOF, MCRS1, OGT, PHF20, and
  WDR5 in the human NSL histone-acetyltransferase complex
  (Giurgiu et al. 2019, DOI: 10.1093/nar/gky973). KANSL1
  haploinsufficiency is the causal lesion for Koolen-de Vries syndrome
  (Koolen et al. 2012, DOI: 10.1038/ng.2262). These external facts were used
  only to decide which represented perturbations were biologically plausible
  analogs; the count scale came from the supplied dataset.

## Dataset calibration

The focal training count table contains 1,674 non-held-out targets. Its median
`n_degs` is 0; 469/1,674 perturbations are nonzero in this focal cell group;
the mean is 14.1 and the maximum is 2,677. Thus a nonzero prediction needs
specific support, and chromatin or neurodevelopmental annotation alone is not
enough.

The parquet is sorted by `group_name`; the `151 TH Prkcd Grin2c Glut` rows
span 35 row groups, about 29.9 million measured rows. I used a PyArrow dataset
filter on

```python
(field("group_name") == "151 TH Prkcd Grin2c Glut")
```

and then restricted `gene_target` to candidate analogs to recover their focal
signatures without scanning unrelated cell groups. I also ran a profile-neighbor
comparison for representative chromatin and acetylation targets using
`gene_target` as the profile entity, measured genes as features, signed
`logfoldchanges` as values, and `pvals_adj < 0.05` as the significance mask.

## Represented analogs and counterexamples

Most literal NSL subunits or closest KAT8 partners were unavailable in the
training endpoint table: `Kansl2`, `Kansl3`, `Kat8`, `Mcrs1`, `Phf20`, `Wdr5`,
and `Hcfc1` were absent. The relevant represented focal counts were:

| training perturbation | focal `n_degs` | relevance to `Kansl1` |
|---|---:|---|
| `Ogt` | 4 | NSL-complex constituent in CORUM; also a pleiotropic O-GlcNAc transferase, so only a partial analog. Its significant focal rows were `Ogt`, `Snhg11`, `Gin1`, and `Noct`. |
| `Msl2` | 0 | Component of the alternative MOF/KAT8 MSL complex rather than NSL; useful because it tests whether another H4K16ac-associated MOF module is detectably active in the same assay. |
| `Crebbp` | 8 | Histone acetyltransferase and neurodevelopmental-disease comparator; focal response was real but small. |
| `Ep300` | 0 | KAT3 paralog of `Crebbp`; flat despite biochemical similarity. |
| `Kat6a` | 0 | Histone acetyltransferase disease gene, outside the NSL/MOF axis. |
| `Kat6b` | 0 | Histone acetyltransferase disease gene, outside the NSL/MOF axis. |
| `Kmt2a` | 24 | COMPASS-family chromatin writer; shares WDR5-related H3K4 biology but not the KANSL1 scaffold or KAT8 H4K16ac reaction. |
| `Setd1a` | 368 | Broad H3K4 methyltransferase perturbation and a cautionary upper-bound counterexample; its signature is much broader and organelle/RNA-biogenesis biased. |
| `Chd8` | 61 | ASD chromatin remodeler active in 151 TH but not a same-complex analog. |
| `Arid1a` | 22 | BAF remodeler with a small-to-moderate 151 TH response; mechanistically indirect. |
| `Arid1b` | 1 | BAF remodeler paralog of `Arid1a`; essentially buffered in this assay. |
| `Kdm5c` | 18 | Chromatin disease gene with a modest response. |
| `Mecp2` | 16 | Chromatin/readout disease gene with a modest response. |

The profile-neighbor pass did not reveal a hidden strong NSL-like module among
these candidates. The closest whole-profile Pearson neighbors of weak anchors
such as `Ogt`, `Msl2`, `Crebbp`, `Ep300`, `Kat6a`, and `Kat6b` were mostly
unrelated zero-DEG targets, while `Setd1a`, `Brd4`, and `Phf12` sat on broad
signatures that the Distributed Agents corpus interprets as RNA/organelle/proteostasis
states rather than generic consequences of losing any chromatin regulator.
I therefore used `Setd1a = 368`, `Brd4 = 311`, and `Phf12 = 403` as
counterexamples showing that the assay can detect broad chromatin effects in
this cell group, not as quantitative `Kansl1` templates.

## Target-specific reasoning

### `Kansl1`

`Kansl1` encodes a scaffold of the NSL KAT8/MOF histone acetyltransferase
complex. A full or germline reduction in KANSL1 dosage is biologically
meaningful: heterozygous loss causes Koolen-de Vries syndrome, and CORUM
places KANSL1 in the same NSL assembly as KAT8/MOF, KANSL2, KANSL3, MCRS1,
OGT, PHF20, and WDR5.

The closest same-complex perturbation represented in the training set was
`Ogt`, and in the focal cell group `Ogt` had 4 significant rows. That is the
strongest direct reason to predict a nonzero but small `Kansl1` endpoint:
the assay can pick up a local NSL-associated perturbation, but in this
thalamic class the response is a handful of genes, not hundreds.

`Ogt` is not a clean KANSL1 phenocopy, because OGT also controls global
O-GlcNAcylation and the Distributed Agents corpus reports broad OGT signatures in other
cell groups that align with RNA-processing, proteostasis, and metabolic
stress. To counterbalance that pleiotropy, I treated `Msl2` as the nearest
represented MOF/KAT8-axis negative comparator. `Msl2` is outside NSL, but it
acts in the alternative MSL H4K16ac complex; it had `n_degs = 0` in
`151 TH Prkcd Grin2c Glut`, and the Distributed Agents corpus calls its all-cell-group
profile downstream-flat. That argues against projecting a large MOF/H4K16ac
signature onto acute postmitotic `Kansl1` loss.

Other acetylation writers reinforced the low end of the scale: `Crebbp` gave
only 8 focal DEGs, while `Ep300`, `Kat6a`, and `Kat6b` gave 0. Broader
neurodevelopmental chromatin genes showed that the assay itself was not blind
to nuclear regulators, but their counts were either modest
(`Kmt2a = 24`, `Arid1a = 22`, `Kdm5c = 18`, `Mecp2 = 16`) or attached to very
different broad programs (`Setd1a = 368`, `Brd4 = 311`, `Phf12 = 403`).
Those broad signatures are poor same-mechanism analogs for a missing NSL
scaffold.

I therefore predict `Kansl1` to be a very small positive responder, closest to
`Ogt` and below the modest `Crebbp`/`Kmt2a` range:

```text
Kansl1 predicted_n_degs = 4
```

## Limits

This is an extrapolation. No `Kansl1` signature is available in the supplied
parquet or in the Distributed Agents same-experiment corpus, and the exact NSL enzymatic
core `Kat8` plus `Kansl2`, `Kansl3`, `Mcrs1`, `Phf20`, and `Wdr5` were absent
from the training endpoint counts. `Ogt` is in the NSL complex but has many
NSL-independent substrates; `Msl2` tests a MOF/H4K16ac route but belongs to the
MSL complex, not NSL. Published KANSL1 and Koolen-de Vries biology mostly
comes from human genetics, germline dosage, or developmental models, whereas
this screen is sparse AAV CRISPR loss of function beginning at P16 and reads
single-nucleus RNA 3-4 weeks later. Protein abundance, H4K16 acetylation, DNA
indels, survival, and activity-evoked transcription were not measured, so the
prediction is only about this assay's steady-state BH-significant DEG count.
