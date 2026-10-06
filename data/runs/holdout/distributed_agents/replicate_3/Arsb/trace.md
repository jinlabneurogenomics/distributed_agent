# Task interpretation

The requested readout is a point prediction of `n_degs` for each gene in
`[local file: 018_Arsb.csv]`.
That manifest contains one held-out perturbation, `Arsb`. I interpreted
`n_degs` exactly as the training CSV defines it: the count of measured genes in
`151 TH Prkcd Grin2c Glut` nuclei with Benjamini-Hochberg adjusted Wilcoxon
`pvals_adj < 0.05`, including the perturbed gene itself if the self transcript
passes that threshold.

The main ambiguity was whether to treat all lysosomal disease genes as one
interchangeable class. I did not. `Arsb` encodes a soluble lysosomal sulfatase
whose loss blocks dermatan sulfate and chondroitin-4-sulfate degradation, so I
used single hydrolases, lysosomal hydrolase trafficking, and storage/cargo
perturbations as the most relevant calibration set. I treated `Rab7` and
`Tsc2` as endolysosomal/mTOR counterexamples rather than as equal-weight
analogs because their focal signatures are broad, late-endosomal, sterol, and
ISR-like states that were not reproduced by the soluble hydrolase nodes.

# Sources

Primary supplied data:

- `training_de_all_cell_groups.parquet`, filtered to
  `group_name == "151 TH Prkcd Grin2c Glut"` for focal log-fold changes,
  adjusted p-values, and matched nucleus counts.
- `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` for the authoritative
  focal `n_degs` endpoint of every non-held-out target.
- `018_Arsb.csv` for requested target order.

Same-experiment semantic layer:

- Distributed Agents corpus release `perturbai-july-260713-sourceguard-1773-v1`.
  `Arsb` itself had no corpus target context, as expected for this holdout, but
  this release contains curated findings for training analogs including `Gaa`,
  `Manba`, `Gnptab`, `Ppt1`, `Psap`, `Asah1`, `Ctsb`, `Sort1`, and `Rab7`.
- Distributed Agents runtime profile comparison over a 17-target lysosome-related
  cohort in the exact focal cell group. This used `logfoldchanges` as signed
  values, `pvals_adj < 0.05` as the significance threshold, and each measured
  gene symbol as a feature.

External biology:

- Valayannopoulos, Nicely, Harmatz and Turbeville 2010,
  DOI `10.1186/1750-1172-5-5`, PMID `20385007`: MPS VI is caused by ARSB
  deficiency and accumulation of dermatan sulfate and chondroitin sulfate; CNS
  involvement is not dominated by intellectual disability.
- Vairo, Federhen, Baldo, Riegel, Burin, Leistner-Segal and Giugliani 2015,
  DOI `10.2147/TACG.S68650`, PMID `26586959`: ARSB is the lysosomal enzyme
  required for glycosaminoglycan breakdown in MPS VI; intravenous galsulfase
  enzyme replacement is used clinically.
- Harmatz and Shediac 2017, DOI `10.2741/4490`, PMID `27814620`: review of
  ARSB deficiency, GAG accumulation, MPS VI diagnosis, and enzyme replacement.
- D'Avanzo, Zanetti, De Filippis and Tomanin 2021,
  DOI `10.3390/ijms222413456`, PMID `34948256`: recent overview of MPS VI and
  ARSB biology.

# Computational evidence from the supplied data

The focal training endpoint is very zero-inflated. Among 1,674 non-held-out
targets, 469 have any DEG in `151 TH Prkcd Grin2c Glut`, the median count is
0, the 75th percentile is 1, and a small number of broad perturbations produce
hundreds to thousands of DEGs.

I pulled the focal parquet rows for a lysosome-centered cohort:

`Gaa, Manba, Gnptab, Gnptg, Ppt1, Psap, Ctsb, Asah1, Scarb2, Grn, Tmem106b, Sort1, Lamp2, Atp6v0a1, Rab7, Tsc2, Vps41`

The filtered read returned 17,259 measured genes for each of the 17 targets.
The cohort was chosen before looking at `Arsb` outcome, using public ARSB
function plus same-experiment corpus findings for soluble lysosomal hydrolase,
mannose-6-phosphate trafficking, lysosomal cargo, late-endosome, and
mTOR-lysosome counterexamples.

I then classified the focal FDR hits. In the direct soluble-hydrolase and
M6P-trafficking analogs, the observed focal endpoint was either 0 or a single
self-transcript:

| target | focal `n_degs` | focal FDR<0.05 evidence | relevance for `Arsb` |
| --- | ---: | --- | --- |
| `Manba` | 0 | No significant genes; self `Manba` logFC -0.204, adjusted p = 1 | soluble lysosomal glycosidase and disease/storage analog |
| `Gnptab` | 0 | No significant genes; self `Gnptab` logFC -0.126, adjusted p = 1 | M6P tag-synthesis component affecting lysosomal hydrolase delivery |
| `Gnptg` | 0 | No significant genes; self `Gnptg` logFC -0.467, adjusted p = 0.459 | same GlcNAc-1-phosphotransferase pathway as `Gnptab` |
| `Asah1` | 0 | No significant genes; self `Asah1` logFC -0.273, adjusted p = 1 | soluble lysosomal lipid hydrolase |
| `Gaa` | 1 | only self `Gaa`, logFC -0.709, adjusted p = 8.97e-16 | soluble, secreted/M6P-routed lysosomal hydrolase |
| `Ppt1` | 1 | only self `Ppt1`, logFC -0.536, adjusted p = 1.34e-5 | soluble lysosomal NCL hydrolase |
| `Psap` | 1 | only self `Psap`, logFC -1.277, adjusted p = 1.70e-28 | soluble lysosomal prosaposin/cargo cofactor |
| `Ctsb` | 1 | only self `Ctsb`, logFC -1.480, adjusted p = 8.54e-43 | lysosomal hydrolase counterexample with no downstream program |

Slightly more distant lysosome/cargo genes also stayed at 0 to 1 DEG in this
focal class: `Sort1` 0, `Lamp2` 0, `Scarb2` 1 self hit, `Tmem106b` 1 self hit,
`Grn` 1 self hit, `Vps41` 0, and `Atp6v0a1` 1 self hit. Core autophagy
perturbations did not argue for a broad `Arsb` response either: `Atg16l1`,
`Atg5`, and `Becn1` each had 0 focal DEGs, and `Rb1cc1` had 4.

The important positive boundaries were:

- `Rab7`: 501 focal DEGs, with `Atp6v1b2`, `Dpp7`, `Atp6v0b`, `Lamp2`, `Grn`,
  `Mcoln1`, `Neu1`, `Hexb`, sterol biosynthesis genes, ISR/UPR genes, and
  proteostasis genes induced. The same-experiment corpus describes this as a
  selective late-endosomal/lysosomal compensation and sterol state, not a
  generic outcome of every lysosomal perturbation.
- `Tsc2`: 86 focal DEGs, sharing part of the sterol/endolysosomal induction
  seen after `Rab7`, but acting through mTORC1/SREBP and therefore a much less
  direct analog for ARSB enzymatic loss.

These boundaries show that the assay can detect lysosome-adjacent transcription
when the perturbation produces that state. The closer soluble hydrolase class
did not converge on such a state.

To check whether a `1` prediction should be assigned just from an on-target
RNA hit, I read all self rows in the focal class. Only 319 of 1,642 biological
targets with a measured self row had their own transcript pass FDR 0.05.
`Arsb` is measured in this focal cell group, but as a response gene across all
1,674 non-held-out perturbations it was almost always flat: median logFC
-0.016, 5th to 95th percentile -0.350 to 0.269, and only one unrelated
perturbation changed it at FDR 0.05. That does not tell us `Arsb` guide
efficiency, but it argues against automatically assigning a singleton.

# `Arsb` reasoning

`Arsb` is N-acetylgalactosamine-4-sulfatase/arylsulfatase B, a lysosomal enzyme
that removes the 4-sulfate group from dermatan sulfate and chondroitin
4-sulfate. Biallelic ARSB loss causes mucopolysaccharidosis VI
by long-term glycosaminoglycan storage. That external function places it closer
to `Gaa`, `Manba`, `Ppt1`, `Psap`, `Ctsb`, and M6P trafficking genes than to
late-endosomal GTPase `Rab7` or mTOR regulator `Tsc2`.

The same-experiment evidence for that close class consistently points to
buffering at the 3 to 4 week, sparse postnatal NeuN+ snRNA-seq readout:

- `Manba:F002` reports that `Gaa`, `Ppt1`, `Ctsb`, `Gnptab`, and `Gnptg` were
  shared downstream-null hydrolase/M6P comparators in matched neuronal groups.
- `Gnptab:F003` reports that representative lysosomal hydrolase or cargo
  perturbations `Ctsb`, `Gaa`, `Manba`, `Asah1`, `Ppt1`, and `Psap` were flat
  across `Gnptab`-matched neuronal groups.
- `Ppt1:F004` and `Psap:F003` report that NCL, PSAP-related, and lysosomal
  perturbations failed to form a shared multi-group neuronal FDR module.
- `Ctsb:F002` specifically found no canonical TFEB/CLEAR, lysosomal,
  autophagy, cathepsin, or generic stress rebound after a lysosomal hydrolase
  perturbation.
- Corpus claim `claim:2ea06b0f0f62f2fef4d7` summarizes represented soluble
  lysosomal hydrolase, cargo, and M6P-pathway perturbations as largely buffered
  at the acute neuronal mRNA level; claim
  `claim:56e1e77cd2cb9bb6604f` summarizes acute lysosomal/NCL/hydrolase/cargo
  and trafficking perturbations as lacking a shared neuronal
  storage-stress, TFEB/MiT, autophagy, ISR, or UPR nuclear RNA program.

The biology also makes an acute focal neuronal response unlikely. ARSB is a
single soluble hydrolase in a tissue-mosaic perturbation; residual enzyme,
unedited neighboring cells, extracellular enzyme uptake through M6P receptors,
and the short P16 to P37-P44 interval should all make a storage phenotype less
visible than congenital whole-body loss. In MPS VI, the dominant substrate
burden is dermatan/chondroitin sulfate in connective tissues and viscera rather
than a rapidly penetrant neuron-autonomous stress program. That differs from
`Rab7`, whose cell-autonomous late-endosome traffic block produced a strong
focal compensatory state.

Putting those pieces together:

- Downstream response: predict absent. The best within-dataset analogs are 0
  or singleton self-only signatures; none show a multi-gene lysosomal rebound.
- Self-transcript response: possible but not reliable. A few hydrolases such as
  `Gaa`, `Ppt1`, and `Psap` were counted as 1 solely because the target RNA
  crossed FDR, whereas `Manba`, `Asah1`, `Gnptab`, and `Gnptg` stayed at 0. I
  do not have direct guide or ARSB activity measurements for the held-out
  perturbation, and only about one fifth of focal self rows passed FDR in
  training.

The resulting point estimate for `Arsb` is therefore `0` DEGs.

# Limits

The prediction extrapolates from nearby lysosomal hydrolases rather than from a
same-complex or sulfatase paralog perturbation; canonical MPS genes such as
`Ids`, `Gusb`, `Naglu`, `Sgsh`, `Galns`, `Glb1`, and `Arsa` were measured as
expression features but were not training perturbations in the focal count
file. The assay did not measure ARSB protein, sulfatase activity, indels,
dermatan/chondroitin sulfate storage, TFEB localization, or lost/unrecovered
neurons. The final integer also depends on whether the `Arsb` transcript itself
would have crossed a statistical FDR threshold, which cannot be determined from
external gene function. I therefore put more weight on the repeated absence of
downstream hydrolase programs than on attempting to forecast a one-gene
self-transcript hit.
