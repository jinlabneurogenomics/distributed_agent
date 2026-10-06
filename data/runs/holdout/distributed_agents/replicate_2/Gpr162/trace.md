# Gpr162 held-out DEG-count prediction

## Question and resolved ambiguities

I interpreted the requested endpoint as the integer number of genes that would
have `pvals_adj < 0.05` for the held-out `Gpr162` perturbation in
`151 TH Prkcd Grin2c Glut`, using the same Wilcoxon/Benjamini-Hochberg calling
used for the supplied training perturbations. A zero prediction means that no
measured gene, including the targeted transcript itself, is expected to pass FDR
0.05. I kept the manifest order from
`096_Gpr162.csv`, which contains a single requested target.

The held-out perturbation has no observed differential-expression rows in the
parquet and no observed `n_degs` row in the training endpoint CSV. I therefore
used only non-held-out training perturbations as empirical calibration and used
external biology only to decide which of those perturbations were reasonable
analogs or counterexamples.

## Sources used

- Input training DEG counts:
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`
- Input differential-expression parquet:
  `[local file: training_de_all_cell_groups.parquet]`
- Held-out manifest:
  `[local file: 096_Gpr162.csv]`
- Distributed Agents same-experiment corpus, release
  `perturbai-july-260713-sourceguard-1773-v1`, queried for `Gpr162` and for
  receptor, GPCR, Wnt/PCP, GABA receptor, and Hedgehog/ciliary claims.
- Distributed Agents runtime `profile_neighbors`, run against the 151-cell-group parquet
  profiles for `Gpr161`, `Gpr156`, `Gpr158`, `Gprasp2`, `Gabrd`, `Lrp6`,
  `Ror1`, and `Ryk`; the lossless artifact was written to
  `gpr162_analog_profile_neighbors.json`.
- NCBI PubMed via E-utilities for GPR162/GPR153/CART biology:
  Gloriam et al. 2005, DOI 10.1016/j.bbagen.2004.12.001, PMID 15777626;
  Sreedharan et al. 2011, DOI 10.1111/j.1742-4658.2011.08388.x,
  PMID 21981325; Caruso et al. 2014, DOI 10.1016/j.gene.2014.09.042,
  PMID 25275856; Caruso et al. 2016, DOI 10.1016/j.gene.2016.01.044,
  PMID 26827797; Lindqvist et al. 2023, DOI 10.1016/j.isci.2023.108416,
  PMID 38077141.

## Empirical calibration

The focal-cell training table has 1674 non-held-out perturbations. Its endpoint
distribution is very sparse: 1205/1674 perturbations have `n_degs = 0`, the
median is 0, the 75th percentile is 1, the 90th percentile is 2, and the mean is
inflated to 14.1 by a small high-response tail. This makes zero the empirical
default unless the held-out target can be tied to an observed broad-response
program.

I queried the parquet after filtering to
`group_name = '151 TH Prkcd Grin2c Glut'`. Each non-held-out perturbation in
this group has 17,259 measured genes. Because the parquet is sorted by
`group_name`, I used row-group pruning and avoided reading all 7.8 GB for each
slice.

Computations over the DE parquet:

- counted FDR-positive rows for biologically selected receptor analogs and
  verified they matched the training endpoint CSV;
- inspected the strongest rows by adjusted p-value to distinguish a true small
  downstream response from a target-only self-knockdown;
- checked whether `Gpr162`, the closest paralog `Gpr153`, and the CART ligand
  transcript `Cartpt` were present in the focal-cell measured gene set;
- compared candidate analog signatures with the runtime signed-profile
  neighbor search, using whole-profile Pearson/cosine and top-tail overlaps, to
  see whether sparse receptor perturbations nonetheless formed a repeated
  expression state.

The GPCR/receptor subset I considered was itself nearly all flat: among 36
training targets matching orphan or neurotransmitter GPCR/receptor-adjacent
names, 32 had zero DEGs and the maximum was 2. Among Wnt/ROR/RYK receptor-layer
comparators, 10/11 were zero and the maximum was the 4-DEG `Lrp6` response.

## `Gpr162`-specific analogs and counterexamples

Public biology places `Gpr162` in a receptor/signaling rather than direct
transcriptional-regulator class. Gloriam et al. identified `GPR162` as a
conserved orphan rhodopsin-family GPCR. Sreedharan et al. found that `Gpr153`
and `Gpr162` share an ancient common GPCR ancestor; however, `Gpr153` was not a
training perturbation here. Caruso et al. mapped GPR162 broadly in the CNS and
especially in hypothalamus, amygdala, and ventral tegmental area in mouse, then
associated rodent `Gpr162` expression and human variants with feeding and
glucose-homeostasis phenotypes. Lindqvist et al. identified GPR162 as a CART
receptor in pancreatic beta cells and connected it to CART-induced exocytosis
and cytoskeletal rearrangement. None of these mechanisms is a known
cell-autonomous, constitutive nuclear transcriptional program in postnatal
thalamic glutamatergic neurons.

The same-experiment Distributed Agents corpus had no frozen `Gpr162` claims, findings,
or pathway-ledger rows. It did have relevant boundaries from represented
receptor pathways: the corpus states that Gbeta5/R7-adjacent GPCR, `Gpr158`,
and `Gpr179` perturbations are flat/sparse rather than a common neuronal
program; that single perturbations of represented Wnt/Frizzled/ROR/RYK/PCP
receptor-layer genes are largely buffered, sparse, or nonconvergent; that
`Lrp6` and `Ctnnb1/Tcf7l2` define a selective detectable Wnt branch not shared
by `Lrp5`, single Frizzled receptors, `Ror1`, or `Ryk`; that represented GABA_A
subunits such as `Gabra3`, `Gabra2`, and `Gabrd` do not reproduce the
multi-gene `Gabrb2` activity response; and that acute perturbation of
represented Hedgehog/PTCH-SMO-cilium-GLI components, including `Gpr161`, does
not engage a detectable postnatal neuronal Gli/Ptch/Hhip circuit.

Biologically relevant training perturbations in the focal cell group:

| training target | observed `n_degs` | expression-pattern evidence | relevance to `Gpr162` |
| --- | ---: | --- | --- |
| `Gpr161` | 0 | no FDR-positive features; even the `Gpr161` self row was not depleted at FDR 0.05 (`logfoldchanges = 0.187`, `q = 1`) | A ciliary GPCR counterexample. It is not the close `Gpr153` paralog, but it tests whether a neuronal ciliary/GPCR signaling receptor automatically gives a postnatal Hedgehog-like RNA response; it did not. |
| `Gpr156` | 0 | no FDR-positive features; `Gpr156` self row `logfoldchanges = -0.186`, `q = 1` | Brain GPCR-family comparator. Its complete flatness argues that receptor identity and expression are insufficient for a 151-cell DEG response. |
| `Gpr158` | 1 | only significant feature was the target transcript itself (`Gpr158`, `logfoldchanges = -0.991`, `q = 3.39e-26`); no downstream FDR-positive genes | Orphan GPCR comparator in the same endpoint. The singleton endpoint is a self-knockdown, not an analog transcriptional state to transfer. |
| `Gprasp2` | 1 | only significant feature was `Gprasp2` itself (`logfoldchanges = -0.491`, `q = 0.00711`) | GPCR sorting/adaptor comparator and member of an mGluR/Homer/IP3R neighborhood reviewed by the corpus as lacking a shared basal RNA module. |
| `Gabrd` | 2 | `Gabrd` was strongly self-depleted (`logfoldchanges = -0.957`, `q = 2.56e-28`) and only one additional gene, `Cttnbp2`, passed FDR | Receptor-subunit counterexample showing that a neuronal membrane receptor can generate only a self/singleton effect despite adequate matched cells. |
| `Lrp6` | 4 | four small DEGs: `Nsmf`, `Nrbp2`, `Atrnl1`, and `Chgb`; the canonical `Axin2` row was near but not FDR-positive (`q = 0.073`) | Positive but tiny receptor-layer Wnt/catenin comparator. It shows that receptor-level signaling can be detected in 151 cells, yet even an established branch produced only four calls. |
| `Ror1` | 0 | no FDR-positive features | ROR receptor tyrosine kinase and Wnt/PCP counterexample from the corpus receptor-layer claim. |
| `Ror2` | 0 | no FDR-positive features | Same Wnt/PCP counterexample class as `Ror1`. |
| `Ryk` | 0 | no FDR-positive features | Wnt receptor counterexample with no endpoint response. |

The runtime neighbor artifact was consistent with these endpoint calls. Three
of the eight anchored analogs had `no_significant_features`; the other five
were in the `1_to_9_significant_features` bin. Their nearest whole-profile
neighbors were mostly other 0- or 1-DEG perturbations, for example `Gpr161`
nearest neighbors `Ywhae`, `Otx2`, `Hsd17b4`, and `Ifih1` all had zero DEGs,
and `Gpr156` nearest neighbors `Acvr1`, `Gabrr2`, `Tenm4`, and `Mest` all had
zero DEGs. Broader endpoints appeared only as weak tail-overlap neighbors
without a GPR162-like mechanism, such as `Zmynd8` near `Gpr158` or `Elp2` near
`Ryk`, so I treated them as non-mechanistic coincidences rather than positive
analogs.

`Gpr162`, `Gpr153`, and `Cartpt` were all present as measured genes in the
focal-cell DE matrix, so the prediction is not based on the gene being absent
from the assay. However, across all non-held-out perturbations in this cell
group, secondary changes of the measured `Gpr162` row were modest
(`logfoldchanges` from -0.685 to 0.190), and `Gpr153` was similarly quiet
(-0.628 to 0.418). The putative ligand `Cartpt` was measured but not connected
to an assayed CART/GPR162 perturbation, so it did not identify a transferable
same-experiment state.

## Prediction

I predict `Gpr162` will have `0` DEGs in `151 TH Prkcd Grin2c Glut`.

The zero/nonzero decision is driven mostly by within-dataset evidence:
biologically adjacent receptor and GPCR perturbations are overwhelmingly zero
or self-only in the focal group, and the Distributed Agents corpus specifically marks
several represented receptor-layer pathways as flat, sparse, or
nonconvergent in this P16 postmitotic neuronal snRNA-seq assay. Public
literature makes `Gpr162` a plausible neuronal GPCR and CART receptor, but does
not connect acute single-gene `Gpr162` loss to a broad thalamic glutamatergic
nuclear RNA program. The best calibrated count is therefore no FDR-positive
genes rather than a singleton or small positive value.

## Limits

The strongest limitation is absence of the true closest comparator: `Gpr153`
was not present as a training perturbation. `Gpr161`, `Gpr156`, `Gpr158`, and
the Wnt/ROR/RYK receptors are receptor-level counterexamples but are not
orthologous CART receptors. The CART/GPR162 evidence comes from pancreatic beta
cells, not juvenile thalamic neurons, and Caruso et al. mapped prominent
GPR162 expression in hypothalamic and hedonic-feeding regions rather than this
exact Allen thalamic `Prkcd`/`Grin2c` population. The assay also measures
steady-state nuclear RNA after mosaic CRISPR; it can miss physiology,
trafficking, cAMP, cytoskeletal, peptide-evoked, or protein-localization
phenotypes. Finally, some flat receptor perturbations still had significant
self-knockdown rows, so a one-DEG `Gpr162` outcome remains possible if the
target transcript itself were unusually well powered in the hidden
perturbation; the training analogs did not make that singleton outcome more
likely than zero.
