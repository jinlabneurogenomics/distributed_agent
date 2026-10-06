# Cep164 DEG-count prediction

## Question and interpretation

The manifest for this run contains one held-out target, `Cep164`. I interpreted the
endpoint as the exact training CSV endpoint: the number of measured genes in
`151 TH Prkcd Grin2c Glut` with `pvals_adj < 0.05` after acute, sparse P16 AAV
CRISPR loss of function, assayed 3-4 weeks later by NeuN-enriched snRNA-seq.
Self-transcripts are included if they cross the same FDR cutoff, but target RNA
knockdown was not used as an editing-quality weight because the dataset
documentation states that self RNA loss is a poor quantitative proxy for
functional editing in this platform.

## Sources

- Differential-expression rows:
  `[local file: training_de_all_cell_groups.parquet]`.
- Focal training endpoint:
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
- Requested targets:
  `[local file: 035_Cep164.csv]`.
- Distributed Agents same-experiment semantic corpus
  `perturbai-july-260713-sourceguard-1773-v1`, queried with `target_context`
  around ciliary analogs including `Cep290`, `Ift88`, `Ift43`, `Ift81`,
  `Kif3b`, `Sclt1`, `Rpgrip1l`, and `Dync2h1`.
- Distributed Agents runtime `profile_neighbors`, run on focal-cell Wilcoxon-score
  profiles for the ciliary anchors above against the 1,674-target training
  universe.
- External cilium biology from the CEP164 primary-cilium literature. CEP164 is a
  mother-centriole/distal-appendage protein that recruits TTBK2 for cilia
  initiation, and damaging CEP164 variants cause a ciliopathy/nephronophthisis
  syndrome: Chaki et al. 2012, Cell, DOI `10.1016/j.cell.2012.06.028`, PMID
  `22863007`; Cajanek and Nigg 2014, PNAS, DOI
  `10.1073/pnas.1401777111`, PMID `24982133`. Conditional mouse data also show
  that CEP164 is essential for multiciliated-cell differentiation in a ciliary
  tissue context: Siller et al. 2017, PLoS Genetics, DOI
  `10.1371/journal.pgen.1007128`, PMID `29244804`.

## Computation over the training data

I first loaded the focal training count CSV and used it as the authoritative
distribution of the requested endpoint for all non-held-out targets. The
training set is highly zero-inflated in this cell class:

| statistic | `n_degs` |
| --- | ---: |
| targets | 1,674 |
| median | 0 |
| 75th percentile | 1 |
| 90th percentile | 2 |
| 95th percentile | 18 |
| maximum | 2,677 |

I then filtered the parquet to `group_name == "151 TH Prkcd Grin2c Glut"` for
the ciliary/centrosomal training perturbations most relevant to CEP164. For each
candidate I counted `pvals_adj < 0.05`, checked the minimum adjusted p-value,
and retained `n_pert_matched`/`n_ctrl_matched` to verify that the focal rows were
present rather than structurally missing. Every listed candidate had the full
17,259 measured-gene focal surface and the same 23,679 matched controls:

| training perturbation | focal `n_degs` | matched perturbed nuclei | minimum focal q-value | why compared with `Cep164` |
| --- | ---: | ---: | ---: | --- |
| `Cep290` | 0 | 99 | 0.650 | transition-zone/ciliary-gate ciliopathy gene |
| `Sclt1` | 0 | 122 | 1.000 | distal-appendage/transition-fiber ciliogenesis gene |
| `Cep120` | 0 | 184 | 1.000 | centriole/cilia biogenesis comparator |
| `Cep112` | 0 | 106 | 1.000 | centrosomal/ciliary comparator |
| `Cep85l` | 0 | 173 | 1.000 | centrosome and neuronal migration comparator |
| `Ift43` | 0 | 328 | 0.847 | IFT-A ciliary transport |
| `Ift81` | 0 | 152 | 0.391 | IFT-B ciliary transport |
| `Ift88` | 0 | 143 | 1.000 | IFT-B ciliary transport |
| `Kif3b` | 0 | 156 | 1.000 | anterograde ciliary kinesin-2 motor |
| `Dync2h1` | 0 | 98 | 0.348 | dynein-2 retrograde ciliary transport |
| `Dync2i1` | 0 | 229 | 1.000 | dynein-2 retrograde ciliary transport |
| `Ttc21b` | 0 | 131 | 0.459 | IFT-A/ciliopathy gene |
| `Bbs5` | 0 | 121 | 0.220 | BBSome ciliary trafficking |
| `Rpgrip1l` | 0 | 137 | 0.184 | transition-zone/ciliary-gate ciliopathy gene |
| `Rpgr` | 0 | 108 | 0.648 | ciliary trafficking/retinal ciliopathy gene |

I also checked additional pathway readouts in the focal endpoint. `Cplane1`,
`Cspp1`, `Dzip1`, `Tbc1d32`, `Kiz`, `Lztfl1`, `Ptch1`, `Smo`, `Gli1`,
`Gli2`, `Adcy3`, `Htr6`, `Gpr161`, and `Mchr1` each had `0` focal DEGs.
`Ttc8` and `Arl3` each had one focal DEG, but in both cases the significant row
was the perturbed transcript itself, not a multi-gene ciliary response.

Finally, I ran `profile_neighbors` over the focal score profiles for `Cep290`,
`Sclt1`, `Ift88`, `Ift43`, `Ift81`, `Kif3b`, `Rpgrip1l`, `Dync2h1`, and
`Bbs5`. The best whole-profile Pearson neighbors were weak and mostly
non-ciliary: the top Pearson was 0.061 for `Cep290`, 0.074 for `Sclt1`, 0.155
for `Ift88`, 0.142 for `Ift43`, 0.146 for `Ift81`, 0.057 for `Kif3b`, 0.092
for `Rpgrip1l`, 0.076 for `Dync2h1`, and 0.073 for `Bbs5`. This was useful as a
negative control: the FDR-flat ciliary perturbations were not hiding in a strong
unthresholded signature neighborhood.

## Target-specific reasoning

### Cep164

**External biology.** CEP164 sits at distal appendages of the mother centriole
and is required for early ciliogenesis, including recruitment of TTBK2 to the
mother centriole. Human CEP164 mutations were found by Chaki et al. to cause a
renal-retinal ciliopathy/nephronophthisis phenotype, and Cajanek and Nigg showed
that CEP164 recruits TTBK2 to initiate ciliogenesis. This made `Sclt1`, other
distal-appendage/centrosomal targets, `Cep290` and `Rpgrip1l` transition-zone
targets, and core IFT/BBS/dynein/kinesin transport genes the biologically
appropriate training analogs.

**Within-dataset analogs.** The focal training data strongly favored a null
prediction for that analog class.

- The most directly structural comparators available in the training focal
  endpoint, `Sclt1`, `Cep120`, `Cep112`, and `Cep85l`, all had `n_degs = 0`.
  The Distributed Agents corpus specifically reports that `Sclt1` failed to recover
  Hedgehog, cilium-gene, UPR, or ISR transcription despite its structural
  requirement for ciliogenesis, and that weak `Sclt1` unthresholded neighbors
  such as `Kiz` had no FDR-supported overlap.
- `Cep290`, the closest assayed transition-zone comparator by disease logic,
  had `n_degs = 0` in the focal cell class. The corpus reports no robust
  downstream DE for `Cep290` in any assayed postmitotic neuronal group and
  summarizes a high-confidence claim that represented ciliary trafficking and
  signaling perturbations are buffered at the basal nuclear-RNA level rather
  than producing a coherent ciliary RNA module.
- Core machinery needed to build or traffic through cilia was also focal-null:
  `Ift43`, `Ift81`, `Ift88`, `Kif3b`, `Dync2h1`, `Dync2i1`, `Ttc21b`,
  `Bbs5`, and `Rpgrip1l` all had `n_degs = 0`. Corpus findings for
  `Ift43`, `Ift81`, `Ift88`, `Kif3b`, and `Dync2h1` converge on the same
  point: canonical IFT, BBSome, dynein-2, transition-zone, and Hedgehog
  perturbations were measured but remained null or singleton-only in postnatal
  neuronal snRNA-seq.
- The expected downstream ciliary signaling reporters did not supply a
  counterexample. Focal perturbations of `Ptch1`, `Smo`, `Gli1`, `Gli2`,
  `Adcy3`, `Htr6`, `Gpr161`, and `Mchr1` were also `0`, and corpus findings
  for IFT/dynein genes explicitly note that Gli/Ptch/Hhip/Shh and
  ciliary-GPCR programs were not detectably engaged.
- `Ttc8` and `Arl3` were the only single-DEG focal ciliary positives among the
  close panel I inspected, and both singleton hits were the target transcript
  itself. Since self-RNA reduction is target-specific in this CRISPR design and
  is not a reliable surrogate for downstream biology, those singleton self hits
  were weak counterexamples for `Cep164`.
- `Mib1` was a broader focal exception in this neighborhood, with 27 DEGs and a
  sterol-biosynthesis/Srebf2-like response, but corpus Cep120 findings
  separated that response from the flat structural IFT/BBS/transition-zone
  comparators. I treated `Mib1` as a Talpid3-linked counterexample, not as a
  transferable CEP164 analog.

**Prediction.** `Cep164` is biologically important, and its knockout could
disrupt distal appendage assembly, ciliary vesicle docking, or TTBK2-dependent
cilium initiation. In this experiment, however, the represented pathway says
that acute loss of postmitotic neuronal ciliary components usually does not
resolve into a basal nuclear RNA program in `151 TH Prkcd Grin2c Glut`. The
appropriate focal analogs have zero adjusted-significant genes, no convincing
hidden score-neighbor module, and no multi-gene Hedgehog, ciliary-GPCR, UPR, or
ISR counterexample. I therefore predict zero DEGs for `Cep164`.

## Limits

This is still an extrapolation because `Cep164` itself was held out and the
training universe lacks several very direct distal-appendage partners such as
`Cep83`, `Cep89`, `Fbf1`, and `Odf2`. The closest represented analog, `Sclt1`,
is related by distal-appendage function but is not the same complex, while IFT,
BBSome, dynein-2, and transition-zone genes are downstream or adjacent ciliary
machinery rather than CEP164 itself.

The prediction is specific to a 3-4 week, sparse, acute P16 neuronal CRISPR
experiment and to a steady-state snRNA endpoint. It should not be read as a
prediction that CEP164 protein, cilium morphology, TTBK2 recruitment, ciliary
vesicle docking, or evoked ciliary signaling would be normal. Retina, olfactory
bulb, hindbrain, ependymal cells, kidney, and embryonic progenitors were outside
the assay scope, and those are exactly the places where CEP164 ciliopathy
biology could be strongest. The largest remaining endpoint-specific uncertainty
is the self-transcript row: `Cep164` was measured in the focal expression
surface, but there is no held-out target-specific evidence that it would cross
FDR 0.05 as a self hit.
