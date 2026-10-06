# Prediction trace for 151 TH Prkcd Grin2c Glut

## Question and resolved ambiguities

The requested held-out perturbation file, `132_Max.csv`, contains one target:
`Max`.  I interpreted the requested endpoint as a point prediction for the
number of measured genes with `pvals_adj < 0.05` in the focal
`151 TH Prkcd Grin2c Glut` cell group after acute mosaic CRISPR loss of the
mouse target gene.  The value to predict is the exact focal-cell DEG burden
that would have appeared in the training count table if `Max` had not been
held out.

Two choices were important:

- I treated a prediction of `0` as the claim that no measured transcript will
  pass BH FDR 0.05, not as a claim that MAX has no neuronal function.
- I treated measured same-experiment perturbations as endpoint evidence, and
  external MYC/MAX annotations as a way to decide which training perturbations
  are legitimate analogs or counterexamples.

## Sources

Same-experiment and run-local sources:

- `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`
  for exact focal-cell `n_degs` in 1,674 non-held-out perturbations.
- `[local file: training_de_all_cell_groups.parquet]`
  for focal-cell signed log-fold-change vectors.
- The Distributed Agents same-experiment corpus release
  `perturbai-july-260713-sourceguard-1773-v1` for report-level Findings,
  Claims, and explicit cross-perturbation references.
- Distributed Agents runtime profile comparison
  `max_focal_profile_compare.json`, inspected through
  `max_focal_profile_inspect_myc.json` and `max_focal_profile_inspect_e2f.json`,
  for symmetric expression-profile comparisons in the focal group.
- Distributed Agents gene-annotation and gene-analog nomination stores for curated
  CORUM, Reactome, GO, KEGG, MSigDB, and STRING relationships over the
  training universe.

External functional sources:

- Native mouse CORUM v5.0 and strict human CORUM v5.0 complexes projected by
  MGI one-to-one homology, MGI download `2026-09-13`, for MYC-MAX,
  MYC-MAX-KAT2A-TRRAP, c-Myc-Max-Arf, Mad-Max-mSin3a, E2F-6, and PRC1.6
  complex membership.
- STRING physical v12.0 for high-confidence physical links from Max to Myc,
  Mga, and Mycn inside the closed mouse universe.
- Reactome mouse pathway `R-MMU-8953750`, `Transcriptional Regulation by E2F6`,
  as the curated E2F-side comparator set for MGA/PRC1.6.
- PubMed via NCBI Entrez for the founding MAX literature:
  Blackwood and Eisenman, 1991, PMID:2006410, identifying MAX as a
  sequence-specific MYC dimerization partner; and Ayer, Kretzner, and
  Eisenman, 1993, PMID:8425218, showing MAD-MAX antagonism of MYC-dependent
  transcription.

## Computational evidence

I first checked the focal training-count table for biologically nominated MAX
neighbors and boundaries.

```text
Myc       0
Mycn      0
Mnt       0
Mga       2
Mlxip     0
E2f1      0
E2f5      0
Tfdp1     2
Tfdp2     0
Trp53     0
Cdkn2a    0
Dnmt3a    0
Setdb1   22
Sin3a  1433
```

This already put the direct MYC/MAX and MAX-repressor branch in the no-response
or two-gene tail.  In the full focal training distribution, the median was 0,
the 75th percentile was 1, the 90th percentile was 2, and the distribution was
very skewed: the 95th percentile was 18 and the maximum was 2,677.

To check whether the two-gene analogs hid a shared expression state, I compared
signed focal `logfoldchanges` among `Myc`, `Mycn`, `Mnt`, `Mga`, `Mlxip`,
`E2f1`, `E2f5`, `Tfdp1`, `Tfdp2`, `Sin3a`, `Trp53`, `Cdkn2a`, and `Setdb1`
with `pvals_adj < 0.05` as the significance threshold.  Each profile had 17,259
measured genes.  The runtime profile comparison found:

- `Myc`, `Mycn`, `Mnt`, `Mlxip`, `E2f1`, `E2f5`, `Tfdp2`, `Trp53`, and
  `Cdkn2a`: 0 focal significant genes.
- `Mga`: 2 focal significant genes, both positive.
- `Tfdp1`: 2 focal significant genes, both positive.
- `Setdb1`: 22 focal significant genes, 17 positive and 5 negative.
- `Sin3a`: 1,433 focal significant genes, 974 positive and 459 negative.

The sparse `Mga` and `Tfdp1` focal calls did not intersect each other or any
of the zero-DEG MYC/MAX or E2F comparators at FDR 0.05.  `Sin3a` likewise
shared zero FDR 0.05 genes with the inspected direct MYC/MNT/MGA branch in this
view.  I therefore used `Sin3a` as an assay-capacity and pleiotropic
corepressor counterexample, not as a weighted proxy for `Max`.

I also used the Distributed Agents corpus to avoid choosing analogs from name similarity
alone.  `Max` itself was absent from the corpus, matching its held-out status.
The comparator subgraph containing `E2f1`, `E2f5`, `Mga`, `Mlxip`, `Mnt`,
`Myc`, `Mycn`, `Sin3a`, `Tfdp1`, and `Tfdp2` had extensive explicit Finding
references, while `Max` was an isolate because its report was withheld.  The
important corpus Claims were:

- Represented MYC/MAX-network and adjacent E2F/Mondo/metabolic perturbations
  do not form a shared postmitotic neuronal transcriptomic module.
- The sparse `Mga` and `Mycn` neuronal signatures are target-specific rather
  than generic consequences of perturbing represented MYC/MAX-network or
  E2F-related genes.
- Single perturbations of represented E2F/DP family members do not engage a
  coordinated canonical G1/S, replication, mitotic, or apoptotic nuclear
  program in settled postnatal neurons.

## Target-specific reasoning

### Max

External biology makes `Myc` the most direct available comparator: MAX is the
obligate bHLH-Zip dimerization partner that lets MYC bind E-box DNA
(Blackwood and Eisenman, 1991, PMID:2006410), and the annotation layer places
mouse `Max` with `Myc` in native c-Myc-Max-Arf and projected human MYC-MAX and
MYC-MAX-KAT2A-TRRAP CORUM v5.0 complexes.  `Myc` had `n_degs = 0` in
`151 TH Prkcd Grin2c Glut`.  Its same-experiment corpus entry calls acute
`Myc` loss a pan-neuronal transcriptomic null in this P16-to-P37/44 NeuN+
screen and reports absence of the expected MYC growth, ribosome-biogenesis,
translation, and cell-cycle transcriptional panel.  That makes the default
transfer from the activating MYC-MAX branch zero.

`Mnt` is the available MAX-network repressor comparator.  It also had
`n_degs = 0` in the focal group.  The corpus reports that `Mnt` loss failed to
derepress a MYC-like growth, ribosome, cell-cycle, or apoptosis program and
that represented `Myc`, `Mycn`, `Mga`, `Mlxip`, E2F, and `Trp53`-axis
perturbations were flat or active in different cell groups rather than
converging with `Mnt`.  This is important because MAD/MAX antagonism is
canonical externally (Ayer, Kretzner, and Eisenman, 1993, PMID:8425218), but
the same-experiment data say that removing a related MAX repressor did not
make a focal thalamic MAX-network signature.

`Mga` probes the other major MAX-associated branch, PRC1.6/E2F6.  The strict
human-CORUM projection places MAX and MGA together in E2F-6 and PRC1.6a/b
complexes, and STRING physical v12.0 also links the mouse proteins with a
0.930 confidence edge.  In the focal group, however, `Mga` had only
`n_degs = 2`, both in the up direction, and no FDR 0.05 overlap with `Myc`,
`Mnt`, `Mlxip`, `E2f1`, `E2f5`, `Tfdp1`, or `Tfdp2`.  The corpus likewise
states that represented MAX/MYC and E2F-side perturbations failed to phenocopy
the small `Mga` response, keeping the signal tied to MGA-specific PRC1.6
derepression rather than a generic MAX effect.

`Mycn`, `Mlxip`, `E2f1`, `E2f5`, `Tfdp1`, and `Tfdp2` were useful boundaries.
`Mycn`, an additional STRING-supported MAX-family interactor, was 0-DEG in the
focal thalamic group; the corpus reports only a modest, separate Sst-neuron
response and no canonical MYC/MYCN growth program.  `Mlxip` was also 0-DEG,
and its corpus Findings report a transcriptomically silent Mondo/MYC metabolic
surface rather than a hidden carbohydrate or MYC-like program.  The E2F/DP
comparators were either zero in the focal group (`E2f1`, `E2f5`, `Tfdp2`) or
had only two nonoverlapping positive genes (`Tfdp1`), arguing that the
MGA/PRC1.6/E2F side of MAX biology is inactive or buffered at this endpoint.

Finally, `Sin3a` was the main counterexample.  It is in a native mouse CORUM
Mad-Max-mSin3a complex and had a huge focal burden, `n_degs = 1433`.  That
shows `151 TH Prkcd Grin2c Glut` was fully capable of detecting a broad
chromatin-corepressor response.  But the corpus explicitly reports that
`Sin3a` perturbation was broad where `Mnt` was flat, separating
postnatal neuronal SIN3A-dependent transcription from MNT-limited repression.
The focal profile inspection was consistent with that: there was no FDR 0.05
intersection between the broad `Sin3a` response and the direct zero-DEG
MYC/MNT/MGA branch.  I therefore used `Sin3a` to set an upper bound against a
generic "corepressor complex member" transfer, not to pull `Max` upward.

The combined evidence points to `Max` producing no focal FDR 0.05 DEGs.  A
small one- or two-gene response like `Mga` or `Tfdp1` would not be surprising,
but the direct MYC and MNT focal counts are both zero, the PRC1.6 and E2F
signals are target-specific, and no same-experiment evidence supports a
shared MAX module that would make `Max` broader than its represented partners.
I therefore predicted:

```text
Max 0
```

## Limits

- `Max` itself, the MXD genes, `Mlx`, `E2f6`, `Pcgf6`, `L3mbtl2`, `Trrap`,
  and `Kat2a` were absent from the focal training-count table, so the closest
  same-complex tests are incomplete.
- The prediction is a transfer across different gene perturbations, not a
  direct measurement of `Max`; loss of a shared cofactor can in principle
  differ from loss of any one activating or repressing partner.
- Same-experiment corpus comparisons often use FDR 0.10 and all cell groups,
  while the requested endpoint is FDR 0.05 in one cell group.  I used the
  corpus for mechanism and convergence, but the final count calibration came
  from the focal FDR 0.05 CSV and runtime profile comparison.
- External MYC/MAX literature comes largely from proliferating or tumor-like
  settings.  The assay here is acute sparse CRISPR in postmitotic postnatal
  NeuN+ nuclei, where the same-experiment data show those canonical growth and
  cell-cycle outputs were not active.
