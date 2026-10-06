# Nr2f2 held-out DEG-count prediction

## Question and interpretation

The run asks for a point prediction of the number of genes with
`pvals_adj < 0.05` after each held-out knockout in the focal
`151 TH Prkcd Grin2c Glut` class. The manifest
`157_Nr2f2.csv` contains one held-out target:

| target | prediction task |
| --- | --- |
| `Nr2f2` | Predict `n_degs` in `151 TH Prkcd Grin2c Glut` after an acute AAV CRISPR loss-of-function perturbation. |

I treated `151 TH Prkcd Grin2c Glut` as the Allen thalamic
glutamatergic class specified by the dataset context; `TH` is an anatomical
thalamus token here, not tyrosine hydroxylase. I did not use any held-out
`Nr2f2` expression signature or count.

## Sources used

- Focal training endpoint:
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
- Differential-expression parquet:
  `[local file: training_de_all_cell_groups.parquet]`.
- Requested-target manifest:
  `[local file: 157_Nr2f2.csv]`.
- Same-experiment semantic layer: Distributed Agents corpus
  `perturbai-july-260713-sourceguard-1773-v1`. I queried `Nr2f2` and found no
  target-specific related-target edges in this release, so the corpus supplied
  no curated internal analog for this held-out gene.
- Run-local profile tools:
  `profile_neighbors` over the full set of 1,674 focal-cell training targets,
  plus a `profile_compare`/`profile_inspect` run for a hand-picked nuclear
  receptor cohort.
- External gene-function evidence:
  UniProtKB/Swiss-Prot mouse entries `P43135`/`COT2_MOUSE` for `Nr2f2`,
  `P16330`/`CN37_MOUSE` for `Nr2f1`, and `P49117`/`NR2C2_MOUSE`, last
  annotated 2026-09-02 by the UniProt REST API.
- Literature grounding:
  Kanatani et al. 2008, "COUP-TFII Is Preferentially Expressed in the Caudal
  Ganglionic Eminence and Is Involved in the Caudal Migratory Stream",
  DOI `10.1523/JNEUROSCI.2132-08.2008`;
  Cai et al. 2013, "Nuclear receptor COUP-TFII-expressing neocortical
  interneurons are derived from the medial and lateral/caudal ganglionic
  eminence and define specific subsets of mature interneurons",
  DOI `10.1002/cne.23186`;
  Alzu'bi et al. 2017, "The Transcription Factors COUP-TFI and COUP-TFII have
  Distinct Roles in Arealisation and GABAergic Interneuron Specification in
  the Early Human Fetal Telencephalon", DOI `10.1093/cercor/bhx185`;
  and Shibata et al. 1997 for the biochemical point that COUP-TFI repression
  can use N-CoR/SMRT corepressors, DOI `10.1210/mend.11.6.0002`.

## Computational checks over the supplied data

### Endpoint scale in the focal class

The training endpoint contains 1,674 non-held-out perturbations. The focal
response is very sparse:

| statistic | value |
| --- | ---: |
| mean `n_degs` | 14.1 |
| median `n_degs` | 0 |
| targets with `n_degs = 0` | 1,205 |
| targets with `n_degs <= 3` | 1,527 |
| targets with `n_degs >= 50` | 59 |
| maximum | 2,677 |

Thus a nearby factor producing 0-3 significant genes is part of the central
mass of the focal-cell distribution, not a failed or outlying result.

### Mechanistic analogs and counterexamples observed in training

I first looked for targets with the most direct biological relationship to
`Nr2f2`: the NR2F/COUP subfamily, other NR2 orphan nuclear receptors, and
several retinoid/ROR/REV-ERB receptors.

| training perturbation | focal `n_degs` | how I used it |
| --- | ---: | --- |
| `Nr2f1` | 2 | Closest observed paralog, COUP-TFI versus held-out COUP-TFII. |
| `Nr2f6` | 0 | Same NR2F subfamily but immune-biased and not a good positive analog. |
| `Nr2c1` | 0 | NR2 orphan receptor boundary. |
| `Nr2c2` | 3 | NR2 orphan receptor boundary with a tiny negative-only response. |
| `Nr2e1` | 0 | Developmental NR2 receptor boundary. |
| `Nr2e3` | 0 | NR2 receptor boundary; retina-biased biology makes it mostly a null control here. |
| `Rxra`/`Rxrb`/`Rxrg` | 0/0/0 | Nuclear receptor heterodimer partners; all quiet in this focal endpoint. |
| `Rorb` | 0 | Related thalamocortical/ROR receptor counterexample: receptor biology alone did not create DEGs. |
| `Rora` | 278 | Counterexample showing that some nuclear receptors do cause broad focal signatures. |
| `Nr1d1` | 116 | Counterexample for a broad clock/REV-ERB receptor response, not a COUP-TFII analog. |
| `Thra`/`Thrb` | 3/0 | Thyroid receptor boundaries with 0-3 DEGs. |
| `Esrra`/`Esrrg` | 57/0 | ERR-family contrast; `Esrra` has a modest metabolic-looking program, `Esrrg` is null. |

The closest paralog, `Nr2f1`, had only two FDR-significant genes in the
parquet:

| target | measured gene | log2 fold change | adjusted p |
| --- | --- | ---: | ---: |
| `Nr2f1` | `Sorl1` | 0.488 | 0.00994 |
| `Nr2f1` | `Sema7a` | -0.350 | 0.04075 |

`Nr2c2`, the only other selected NR2 factor with any signal, had three
negative DEGs:

| target | measured gene | log2 fold change | adjusted p |
| --- | --- | ---: | ---: |
| `Nr2c2` | `Stxbp2` | -0.804 | 0.000075 |
| `Nr2c2` | `Ccdc84` | -0.800 | 0.000570 |
| `Nr2c2` | `Miga1` | -0.404 | 0.01460 |

Those effects were not a shared receptor program: the `Nr2f1` DEGs were not
significant in `Nr2c2`, and the `Nr2c2` DEGs were not significant in `Nr2f1`.
Within the small receptor cohort, `Sema7a` was a significant negative feature
for `Nr2f1`, `Esrra`, and `Rora`, but `Sorl1` was significant only for
`Nr2f1`.

I also ran a full eligible-neighborhood profile for `Nr2f1`, `Nr2f6`,
`Nr2c2`, `Rora`, and `Nr1d1` against all 1,674 training targets in the focal
cell class, using signed log fold changes across 17,259 measured genes. The
closest whole-profile neighbors of `Nr2f1` were mostly quiet, unrelated
perturbations such as `Ngfr`, `Prdm5`, `Irf2`, `Fgfr3`, `Gabrg3`, `Runx2`,
`Ndufa11`, `Adar`, and `Satb2` with 0 DEGs, plus `Nr1d1` at rank 10. Because
`Nr2f1` itself has only two significant genes and its nearest profiles did
not reveal a coherent COUP-like module, I used that profile search as weak
evidence that the `Nr2f1` signal is near-null rather than as evidence for a
large `Nr2f2` footprint.

As an upstream-regulator sanity check, I asked when the measured `Nr2f2`
transcript itself was significantly changed by non-held-out perturbations in
this class. Only two of the 1,674 training knockouts, the broad-response
targets `Uba5` and `Zbtb7a`, changed `Nr2f2` at FDR 0.05. I therefore did not
treat either as a mechanistic analog for COUP-TFII loss.

## Target-specific reasoning

### `Nr2f2`

`Nr2f2` encodes COUP-TFII, an orphan nuclear receptor and close paralog of
`Nr2f1`/COUP-TFI. UniProtKB annotates the mouse protein as a nuclear
transcriptional regulator involved in forebrain and nervous-system
development, and the COUP factors can function as sequence-specific nuclear
receptor repressors through corepressor recruitment, as shown biochemically
for COUP-TFI by Shibata et al. 1997. Developmentally, the public literature
puts COUP-TFII in caudal ganglionic eminence and cortical interneuron
specification and migration programs: Kanatani et al. 2008 implicated
COUP-TFII in the caudal migratory stream; Cai et al. 2013 mapped
COUP-TFII-expressing mature neocortical interneuron subsets; and Alzu'bi et
al. 2017 contrasted COUP-TFI and COUP-TFII roles in human fetal telencephalic
arealization and interneuron specification.

Those external facts make `Nr2f1` the right within-dataset anchor and
`Nr2f6` a useful but weaker subfamily boundary. They do not argue for a broad
hundreds-of-DEGs footprint after an acute mosaic knockout in postmitotic
thalamic glutamatergic neurons. The known biology is heavily developmental
and, for neuronal fate, interneuron-oriented; the experiment perturbs juvenile
neurons after major embryonic migration and regionalization events. In the
same focal endpoint, the actual closest paralog `Nr2f1` gave only 2 DEGs,
`Nr2f6` gave 0, the other NR2 controls gave 0 or 3, and the RXR receptors and
`Rorb` all gave 0. The broad nuclear-receptor responses (`Rora`, `Nr1d1`,
`Esrra`) show that receptors can be visible in this class, but their observed
programs are not COUP-family programs and are better interpreted as
counterexamples than as evidence to lift `Nr2f2` above the near-null regime.

I therefore predict a real but barely detectable response. The paralog
evidence keeps the point estimate just above zero; the many null receptor
boundaries and the developmental/interneuron mismatch pull it below the
observed `Nr2f1` count of 2.

Final point prediction: `Nr2f2 = 1`.

## Limits of the reasoning

- The same-experiment Distributed Agents corpus release had no curated `Nr2f2` related
  targets, so the target-specific analog choice came from external knowledge
  plus direct inspection of the focal training table.
- `Nr2f1` is the best paralog in the observed dataset, but COUP-TFI and
  COUP-TFII have different spatial and developmental roles; two `Nr2f1`
  DEGs are weak evidence and could include threshold noise.
- The focal parquet has perturbational log fold changes but not raw baseline
  expression, so I could check regulation of the measured `Nr2f2` transcript
  by training knockouts, not whether `Nr2f2` is abundant in unperturbed
  `151 TH Prkcd Grin2c Glut` cells.
- Germline and embryonic Nr2f2 biology is only a prior here. It does not
  directly measure what an acute sparse CRISPR lesion does in recovered
  postnatal thalamic glutamatergic nuclei.
- The exact zero-versus-one outcome is underpowered. The evidence is strong
  against a broad tens-to-hundreds DEG response, but much weaker for
  distinguishing no passing genes from one or two genes at BH FDR 0.05.
