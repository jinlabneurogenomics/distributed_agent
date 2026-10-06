# Reasoning trace

## Question and endpoint

The held-out target list contains one mouse perturbation, `Kansl1`. I interpreted
the task as a scalar prediction of the number of genes that would pass
Benjamini-Hochberg FDR 0.05 in the `151 TH Prkcd Grin2c Glut` single-nucleus
Wilcoxon comparison if `Kansl1` had not been held out. A prediction of zero
means no measured gene is expected to pass FDR 0.05 in this cell group. I did
not treat the held-out gene as present in the training parquet or training count
CSV; the prediction is transferred from non-held-out perturbations.

The requested endpoint is directly observed for the 1,674 training
perturbations in
`151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`. It is absent for `Kansl1`.
The gene-level parquet is direct evidence for the expression signatures and
matched recovered-nucleus counts of the visible analog perturbations, not for
the hidden `Kansl1` signature.

## Sources used

- Differential-expression parquet:
  `training differential-expression dataset`.
  I queried visible perturbations in the focal group and counted measured genes
  with `pvals_adj < 0.05` and, as a boundary check, `pvals_adj < 0.10`.
- Training DEG counts:
  `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
  I used this as the authoritative focal-cell endpoint for non-held-out genes.
- Requested-target manifest:
  `single-target request for Kansl1`.
  This supplied the sole held-out target and its output order.
- Internal same-experiment corpus:
  `perturbai-july-260713-sourceguard-1773-v1`, queried only for visible
  training perturbations. I used its Msl2, Ogt, and Crebbp Findings as packaged
  interpretation of the same experiment. These records are not independent
  replication of the parquet.
- External literature from PubMed:
  Cai et al. 2009, DOI `10.1074/jbc.C109.087981`, defined the human MOF/KAT8 NSL
  complex, including KANSL proteins, OGT, MCRS1, PHF20, WDR5, and HCFC1, and
  showed that MOF substrate specificity differs between MSL and NSL complexes.
  Zhao et al. 2019, DOI `10.3390/ijms21010173`, connected OGT to MOF/NSL by
  O-GlcNAcylation-dependent stabilization of NSL3. Zollino et al. 2012, DOI
  `10.1038/ng.2257`, established KANSL1 loss-of-function as sufficient for
  17q21.31/Koolen-de Vries syndrome. Li et al. 2022, DOI
  `10.1038/s41467-022-28613-0`, reported that Kansl1 haploinsufficiency in mice
  impairs STX17-dependent autophagosome-lysosome fusion, mitophagic clearance,
  and neuronal function.

## Quantitative calibration from the training set

The focal DEG-count distribution was sparse and strongly zero-inflated: 1,205 of
1,674 visible training perturbations had `n_degs = 0`, the median was 0, the
75th percentile was 1 DEG, the 90th percentile was 2 DEGs, the 95th percentile
was 18 DEGs, and only 1% of training targets exceeded about 436 DEGs. That
distribution made zero a realistic prior, and it made counts above roughly 20
DEGs require a specific visible analog rather than generic chromatin-regulator
status.

I then asked which visible perturbations represented the KANSL1 mechanism:

| training perturbation | focal FDR<0.05 DEGs | focal FDR<0.10 DEGs | focal matched perturbed nuclei | why considered |
| --- | ---: | ---: | ---: | --- |
| `Msl2` | 0 | 0 | 111 | MSL complex subunit using the same KAT8/MOF acetyltransferase; closest visible same-enzyme comparator |
| `Ogt` | 4 | 4 | 71 | O-GlcNAc transferase and MOF/NSL-associated regulator of NSL3, but also a broad O-GlcNAc enzyme with many non-NSL substrates |
| `Ep300` | 0 | 0 | 155 | neuronal HAT counterexample |
| `Kat6a` | 0 | 0 | 170 | MYST acetyltransferase counterexample |
| `Kat6b` | 0 | 0 | 150 | MYST acetyltransferase counterexample |
| `Brd1` | 4 | 5 | 178 | HAT-associated chromatin reader/adaptor counterexample |
| `Crebbp` | 8 | 16 | 61 | neuronal HAT counterexample with a small real focal response |
| `Atg5` | 0 | 0 | 114 | core autophagy machinery downstream-mechanism counterexample |
| `Map1lc3a` | 1 | 1 | 186 | autophagosome marker counterexample |
| `Rb1cc1` | 4 | 4 | 151 | autophagy-initiation counterexample |

Several other chromatin regulators showed that the assay can detect broad
focal responses when the visible perturbation drives one: `Sin3a` had 1,433
DEGs, `Yy1` 720, `Wac` 384, `Setd1a` 368, and `Brd4` 311. I therefore did not
interpret the low counts for MSL/NSL-neighborhood genes as a generic failure to
see chromatin perturbations. Those broad responders regulate different
chromatin programs, so they were counterexamples rather than count donors for
`Kansl1`.

Expression-pattern details supported the same boundary:

- `Msl2` was completely flat in the focal parquet. Its lowest adjusted
  p-values were all 1.0, and the internal corpus reported zero downstream
  FDR<0.10 genes for `Msl2` in every measured neuronal group.
- `Ogt` had exactly four focal FDR<0.05 genes: its own transcript and `Snhg11`
  decreased, while `Gin1` and `Noct` increased. In the same dataset Ogt was
  broad in other groups, especially `155 MB Glut` with 536 FDR<0.05 DEGs, so
  its low focal count was not simply a globally weak perturbation. The packaged
  Ogt report also emphasized RNA-processing, proteostasis, and lipid modules,
  consistent with Ogt being a pleiotropic upper-bound analog rather than a
  direct KANSL1 phenocopy.
- `Crebbp` and `Brd1` had only 8 and 4 focal DEGs at FDR 0.05. The Crebbp
  same-experiment report noted that its canonical KAT3 paralog `Ep300` did not
  phenocopy it in the matched thalamic signature. That reinforced that
  paralogy or HAT annotation alone was not enough to borrow a large DEG count.
- The FDR<0.05 sets among the small positive chromatin and autophagy
  perturbations barely overlapped. The only pair with more than two shared
  focal DEGs among the queried boundary cases was the unrelated
  `Kdm5c`/`Nsd1` pair. `Ogt` shared no FDR<0.05 focal genes with those
  HAT/chromatin boundary sets, so the observed four-gene Ogt footprint looked
  OGT-specific rather than a reusable NSL-like module.

## Target-specific prediction

### Kansl1

`Kansl1` encodes a KAT8/MOF NSL-complex subunit. Its loss is biologically real:
KANSL1 haploinsufficiency causes Koolen-de Vries syndrome in humans, and mouse
Kansl1 haploinsufficiency perturbs neuronal function through defective
STX17-dependent autophagosome-lysosome fusion. Those observations argue against
assuming that `Kansl1` is an inert gene.

The experimental chain is nevertheless only weakly endpoint-bearing for this
specific readout. Germline or organism-wide heterozygous Kansl1 deficiency can
alter development, autophagy, damaged-mitochondria clearance, and ROS, but the
PerturbAI intervention is sparse acute Cas9 loss of function delivered at P16
and sampled 3-4 weeks later in recovered NeuN-positive thalamic glutamatergic
nuclei. If the important KANSL1 effect requires early development, severe
selection before recovery, non-neuronal cells, or a strong chronic haploinsufficient
state, it can fail to appear as many FDR<0.05 nuclear-RNA changes in survivor
`151 TH Prkcd Grin2c Glut` cells.

Among measured training perturbations, the closest same-KAT8 comparator was
`Msl2`, and it produced zero focal DEGs and no looser FDR<0.10 downstream
signal across the corpus summary. The NSL-associated `Ogt` perturbation was
visible but only at four focal DEGs, with a broad non-NSL O-GlcNAc footprint in
other cell groups. Nearby KAT or HAT perturbations (`Ep300`, `Kat6a`, `Kat6b`,
`Brd1`, `Crebbp`) ranged from 0 to 8 focal DEGs. Autophagy perturbations
available in the training set (`Atg5`, `Map1lc3a`, `Rb1cc1`) ranged from 0 to 4.
Taken together, the visible same-experiment evidence puts `Kansl1` at the
zero/single-digit boundary rather than in the >20-DEG chromatin-regulator tail.

I therefore predicted no FDR<0.05 hits for `Kansl1` in the focal cell group:

`Kansl1 -> predicted_n_degs = 0`.

## Limits

The major limitation is missingness of the most direct complex-mate
perturbations: `Kat8`, `Kansl2`, `Kansl3`, `Mcrs1`, `Phf20`, and `Wdr5` were
not in the visible focal training-count CSV. `Msl2` shares MOF/KAT8 but belongs
to the MSL complex rather than the NSL complex, and `Ogt` is a pleiotropic
O-GlcNAc transferase rather than an obligate loss of the NSL scaffold. The
external Kansl1 mouse and human evidence is strong for developmental disease
biology but imperfect for a sparse postnatal neuronal CRISPR assay. Because
the predicted value sits at the zero/nonzero boundary, a hidden result of a few
DEGs would also be biologically plausible; I chose zero because the direct
visible MSL/NSL-neighborhood and autophagy endpoints were flat to very small in
the requested thalamic glutamatergic group.
