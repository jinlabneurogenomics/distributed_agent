# Task interpretation

The held-out readout is the integer `n_degs`: in `151 TH Prkcd Grin2c Glut`
cells, how many measured genes pass Benjamini-Hochberg FDR 0.05 after a
Wilcoxon comparison of a CRISPR loss-of-function perturbation against its
matched non-targeting controls.

The requested-target manifest contains one held-out target, `Tbce`. I treated
`151 TH Prkcd Grin2c Glut` as the Allen-style thalamic glutamatergic cell
group label used in the parquet, not as a count of 151 nuclei. I also treated
target-transcript knockdown as quality context only; the prediction is for
downstream FDR-significant transcriptional breadth among recovered nuclei.

# Sources used

Internal data from this run:

- Differential-expression parquet:
  `[local file: training_de_all_cell_groups.parquet]`.
- Focal-cell training DEG counts:
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
- Requested held-out manifest:
  `[local file: 232_Tbce.csv]`.
- Selected Distributed Agents same-experiment corpus:
  `perturbai-july-260713-sourceguard-1773-v1`. I used this as a curated
  semantic layer over the same Perturb-seq experiment, not as independent
  replication.

External biological references:

- Reactome, "Post-chaperonin tubulin folding pathway", `R-HSA-389977`, for
  the canonical TBCA/B/C/D/E, TBCD/TBCE/TBCC/ARL2 tubulin-folding pathway.
- Tian and Cowan 2013, DOI `10.1016/B978-0-12-407757-7.00011-6`,
  PMID `23973072`, for the model in which TBCE/alpha-tubulin and
  TBCD/beta-tubulin complexes form a TBCC-regulated supercomplex that releases
  native alpha/beta-tubulin heterodimer.
- Martin et al. 2002, DOI `10.1038/ng1016`, PMID `12389029`, and
  Bommel et al. 2002, DOI `10.1083/jcb.200208001`, PMID `12446740`, for the
  mouse `Tbce` progressive motor neuronopathy mutation, reduced microtubules in
  axons, and rescue by wild-type `Tbce`.
- Schaefer et al. 2007, DOI `10.1523/JNEUROSCI.1599-07.2007`,
  PMID `17699660`, and Bellouze et al. 2014, DOI `10.1093/hmg/ddu320`,
  PMID `24951541`, for TBCE-dependent axonal tubulin routing and Golgi-derived
  microtubule/COPI coupling in motor neurons.
- Serna et al. 2015, DOI `10.1242/jcs.167387`, PMID `25908846`, for the
  biochemical/structural TBCE-TBCB-alpha-tubulin complex and tubulin dimer
  dissociation mechanism.

# Computations over the training data

1. I verified that the manifest has exactly one requested target, `Tbce`, and
   that `Tbce` is absent from the focal training count CSV.

2. I summarized the 1,674 focal-cell training counts to calibrate scale:

   | focal training bin | number of targets |
   |---|---:|
   | `n_degs = 0` | 1205 |
   | `n_degs = 1-2` | 307 |
   | `n_degs = 3-12` | 65 |
   | `n_degs = 13-100` | 55 |
   | `n_degs > 100` | 42 |

   The median count was 0, the 75th percentile was 1, the 90th percentile was
   2, and the 95th percentile was 18. Thus a 10-15 DEG prediction is a clear
   positive response but still part of the sparse tail, not a broad stress
   response.

3. I checked which members of the tubulin-folding pathway were available as
   training perturbations. `Tbcd` was the only direct TBCE/TBCD/TBCC
   post-chaperonin cofactor in the focal count file. `Tbca`, `Tbcb`, `Tbcc`,
   `Arl2`, `Tcp1`, CCT subunits, and prefoldin subunits were not in the 1,674
   training targets. `Arl2bp` was present but is not the ARL2 GTPase used by
   the TBCD/TBCE/TBCC machine and had `n_degs = 0`.

4. I filtered the parquet to `group_name == "151 TH Prkcd Grin2c Glut"` and to
   focal candidate perturbations. The key observed counts and FDR<0.05 genes
   were:

   | training target | `n_degs` | focal expression-pattern evidence |
   |---|---:|---|
   | `Tbcd` | 12 | Direct cofactor analog. The 12 significant genes were `Tuba1a`, `Tuba1b`, `Ypel4`, `Nfil3`, `Kctd16`, `Lrrc7`, `Ptprn2`, `Samd5`, `Satb1`, `Slc25a23`, `Mturn`, and `Jun`; `Tuba1a` and `Tuba1b` were the top calls and were up-regulated. |
   | `Tuba1a` | 7 | Alpha-tubulin structural-gene perturbation. Its focal signature was mostly reciprocal tubulin compensation: `Tuba1a` itself down, with `Tubb3`, `Tubb2a`, `Tuba4a`, `Tubb4a`, `Tubb4b`, and `Tubb5` up. It did not copy the `Tbcd` adaptation module. |
   | `Tuba4a` | 2 | Only `Tuba4a` down and `Mast1` up in the focal cell group. |
   | `Tubb4b` | 1 | Only the `Tubb4b` self transcript passed FDR 0.05. |
   | `Tubb5` | 1 | Only the `Tubb5` self transcript passed FDR 0.05. |
   | `Map1b`, `Mapt`, `Stmn2`, `Kif5a` | 1 each | These microtubule-associated structural or motor/axon genes were self-transcript-only in this cell group. |
   | `Dctn1` | 75 | A microtubule transport adaptor but mechanistically different; its focal DEGs were dominated by `Insig1`, `Msmo1`, `Hmgcs1`, `Cyp51`, `Hmgcr`, `Fdft1`, and other sterol/lipid genes, not by the tubulin-folding-cofactor module. |

5. I then used the 12 focal `Tbcd` FDR<0.05 genes as a signed module and, for
   every training target, counted how many of those same genes were significant
   in the same versus opposite direction. The strongest same-direction
   overlaps were:

   | training target | `n_degs` | same of 12 | opposite of 12 | interpretation |
   |---|---:|---:|---:|---|
   | `Tbcd` | 12 | 12 | 0 | The direct local phenotype. |
   | `Cic` | 576 | 6 | 0 | Shares `Lrrc7`, `Tuba1a`, `Mturn`, `Samd5`, `Ptprn2`, and `Satb1`, but as part of a much broader transcriptional program. |
   | `Grin1` | 89 | 6 | 0 | Shares `Kctd16`, `Jun`, `Samd5`, `Lrrc7`, `Mturn`, and `Ypel4`; useful for confirming that those genes can move together in this cell group, not a tubulin cofactor analog. |
   | `Psmb4` | 742 | 3 | 2 | A broad proteasome signature that partly opposed `Tbcd`, including down-regulation of `Tuba1a`. |
   | `Psmc1` | 430 | 3 | 1 | Another broad proteasome signature with partial opposition. |
   | `Dctn1` | 75 | 0 | 2 | Opposed `Tbcd` at `Jun` and `Kctd16`. |

   This kept the calibration local and target-specific: `Cic`, `Grin1`,
   `Psmb4`, and `Psmc1` show that some `Tbcd` genes belong to broader
   high-count states, but they are not good count analogs for `Tbce`.

6. The selected Distributed Agents corpus independently summarized the in-dataset
   `Tbcd` result in the same way: `Tbcd:F001` reported a sparse but real
   response concentrated in `151 TH Prkcd Grin2c Glut`; `Tbcd:F002` called
   alpha-tubulin mRNA up-regulation the recurrent output; `Tbcd:F003` named
   the focal `Jun`/`Nfil3`/`Ypel4`/`Mturn`/`Satb1`/`Slc25a23`/`Kctd16`
   induction and `Lrrc7`/`Ptprn2`/`Samd5` repression module; `Tbcd:F006`
   noted that `Tuba1a`, `Tuba4a`, and `Arl2bp` failed to phenocopy `Tbcd`.
   Corpus findings for `Tuba1a`, `Tuba4a`, `Tubb4b`, and `Tubb5` likewise
   described sparse, buffered signatures rather than a large shared
   microtubule-stress state.

# Target-specific prediction

## `Tbce`

`Tbce` encodes tubulin-folding cofactor E. It is not a structural tubulin
isotype; it sits in the same post-chaperonin tubulin-heterodimer assembly and
disassembly machine as TBCD. The Reactome post-chaperonin pathway and Tian and
Cowan's biochemical model place TBCE on the alpha-tubulin side and TBCD on the
beta-tubulin side of a TBCC-regulated supercomplex. Serna et al. further showed
that TBCE with TBCB directly participates in alpha/beta-tubulin dimer
dissociation. This makes the training `Tbcd` perturbation the only direct
within-dataset analog for `Tbce`.

The biology also argues against calling `Tbce` a null. Mouse `Tbce` loss of
function in progressive motor neuronopathy destabilizes the protein, reduces
axonal microtubules, disrupts tubulin routing from the Golgi, and is rescued by
wild-type `Tbce` in transgenic complementation experiments. Those experiments
were in severe motor-neuron models rather than this assay's thalamic
glutamatergic neurons, but they establish that partial failure of TBCE can be
felt as neuronal microtubule proteostasis and trafficking stress.

I used `Tbcd = 12` as the quantitative anchor. The structural tubulin
perturbations define the lower boundary: `Tuba1a` had 7 DEGs and mainly induced
replacement tubulin transcripts, while `Tuba4a`, `Tubb4b`, and `Tubb5` had only
1-2 DEGs and no `Tbcd` module. Those lower counts are not enough to set `Tbce`
to zero because a folding cofactor should perturb shared alpha/beta dimer
biogenesis more directly than removing one isotype. Conversely, I did not use
`Dctn1`'s 75-DEG sterol/lipid response, or the 89- to 742-DEG `Grin1`, `Cic`,
`Psmc1`, and `Psmb4` signatures, to inflate the count: their focal expression
programs are broad receptor, transcriptional, dynactin, or proteasome states
that only partially intersect the `Tbcd` genes.

Predicted decision: nonzero, with a small sparse positive response comparable
to `Tbcd`. I assign `predicted_n_degs = 12`.

# Limits and extrapolations

- `Tbce` itself was held out, so there is no same-target DEG count or signature
  in the supplied input. The prediction extrapolates from `Tbcd` plus external
  tubulin-cofactor biology.
- `Tbcd` is the sole direct post-chaperonin cofactor training perturbation;
  `Tbca`, `Tbcb`, `Tbcc`, and `Arl2` would have been better triangulation
  targets but were absent.
- The `Tbcd` signature is small. With only 12 focal DEGs, adding or losing a few
  genes at the FDR boundary would materially change the count.
- PMN mouse and TBCE cell-biological studies describe strong germline,
  hypomorphic, or knockdown effects in motor neurons and other systems. This
  task is acute mosaic AAV-CRISPR loss of function in postnatal thalamic
  glutamatergic neurons among recovered NeuN-positive nuclei, so the literature
  supports the sign of "nonzero microtubule cofactor effect" more strongly than
  the exact DEG count.
- The endpoint is assay- and power-dependent. The estimate of 12 means that a
  sparse transcriptional footprint should be detectable at FDR 0.05 in this
  cell group, not that TBCE and TBCD have identical biochemical severity.
