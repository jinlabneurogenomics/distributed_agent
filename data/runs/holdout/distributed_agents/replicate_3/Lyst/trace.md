# Question and prediction target

The requested held-out target is `Lyst`, from
`129_Lyst.csv`.  I interpreted the task as predicting one integer endpoint for
`151 TH Prkcd Grin2c Glut`: the number of measured genes with
Benjamini-Hochberg-adjusted Wilcoxon `pvals_adj < 0.05` after acute AAV/CRISPR
loss of the target gene.  `Lyst` is absent from the supplied differential
expression parquet and the training count CSV, so the estimate has to be
transferred from mechanistically related training perturbations rather than
read from a held-out signature.

The only ambiguity I resolved was how to treat disease severity evidence for
germline `Lyst` loss.  I treated Chediak-Higashi neurodegeneration as proof
that LYST is neuronal/lysosomal biology, but not as proof of a large P16-to-P37
single-nucleus FDR response, because the screen is acute, mosaic, partial at the
mRNA level, and much earlier than most progressive `Lyst` mouse or human
neurologic phenotypes.

# Sources used

- Focal training endpoint:
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
- Differential-expression parquet:
  `[local file: training_de_all_cell_groups.parquet]`.
- Distributed Agents same-experiment corpus
  `perturbai-july-260713-sourceguard-1773-v1`.  There was no target-context
  record for held-out `Lyst`, but the corpus did provide claims and findings for
  `Rab7`, `Vps41`, `Vps35`, `Vps54`, `Vps53`, and autophagy/lysosome
  comparators.
- Distributed Agents runtime `profile_compare`/`profile_inspect` for focal
  expression-pattern comparisons among observed Lyst-relevant perturbations.
  I compared `Rab7`, `Vps41`, `Vps35`, `Vps54`, `Vps53`, `Lrba`, `Nbea`,
  `Wdfy3`, `Ap3b1`, `Dtnbp1`, `Lamp2`, `Atg5`, `Atg16l1`, `Becn1`, `Mtor`,
  `Tsc2`, `Ctsb`, and `Gaa` in the `151 TH Prkcd Grin2c Glut` rows only.
- NCBI PubMed literature searches for LYST/Chediak-Higashi and lysosome
  trafficking biology.  Mechanistic anchors were Tchernev et al. 2002
  (PMID: 11984006) for LYST interactions with vesicle/SNARE components,
  Kaplan, De Domenico and Ward 2008 (doi: 10.1097/MOH.0b013e3282f2bcce) and
  Talbert, Malicdan and Introne 2023
  (doi: 10.1097/MOH.0000000000000766) for LYST as a conserved lysosomal
  trafficking regulator and Chediak-Higashi gene, Falkenstein and De Lozanne
  2014 (doi: 10.1242/jcs.138123) for the evidence that the LYST ortholog LvsB
  regulates endosomal vesicle fusion, Introne et al. 2017
  (doi: 10.1212/WNL.0000000000003622) for adult progressive neurologic disease
  in atypical Chediak-Higashi, and Hedberg-Buenz et al. 2019
  (doi: 10.1038/s41598-019-42159-0) for strain- and age-dependent neurologic
  effects in `Lyst` mutant mice.

# Computation over the training data

I used the training count CSV to place candidate analogs on the focal-cell
response scale.  The calibration distribution is sparse: among 1,674 observed
training targets in `151 TH Prkcd Grin2c Glut`, 469 have any FDR hit, the
median count is 0, the upper quartile is 1, and only a small set of core
proteostasis, splicing, transcriptional, and trafficking genes produce tens to
hundreds of DEGs.

For focal signatures, I read the parquet row groups whose `group_name` metadata
covered `151 TH Prkcd Grin2c Glut`, filtered exactly to that cell group, and
then filtered to candidate analog target names.  This avoided scanning the
whole 616-million-row parquet.  I then recounted `pvals_adj < 0.05` and
inspected FDR-passing genes and matched perturbed nucleus counts.

The most relevant observed counts were:

| training target | `n_degs` | focal matched perturbed nuclei | why it was considered |
|---|---:|---:|---|
| `Rab7` | 501 | 215 | Central late endosome/lysosome GTPase; positive control that this assay can detect late-endolysosomal stress |
| `Vps41` | 0 | 159 | HOPS late endosome/lysosome fusion subunit, on the RAB7 pathway |
| `Vps35` | 17 | 133 | Retromer endosomal sorting |
| `Vps54` | 31 | 161 | GARP retrograde endosome-to-TGN trafficking |
| `Vps53` | 0 | 147 | Same GARP complex as `Vps54`; counterexample to same-complex transfer |
| `Vps35l` | 0 | not re-read here | Retriever/Commander retromer-like trafficking |
| `Washc4` | 0 | not re-read here | WASH endosomal actin machinery |
| `Lrba` | 0 | 211 | BEACH-domain vesicle trafficking protein |
| `Nbea` | 0 | 99 | BEACH-domain neuronal vesicle trafficking protein |
| `Wdfy3` | 17 | 230 | Large BEACH/autophagy adaptor family member |
| `Ap3b1` | 0 | 85 | AP-3 lysosome-related organelle trafficking |
| `Dtnbp1` | 0 | 220 | BLOC-1/AP-3-associated lysosome-related organelle and synaptic vesicle trafficking |
| `Rab27a` | 0 | not re-read here | Lysosome-related organelle exocytosis axis |
| `Myo5a` | 1 | not re-read here | Organelle transport and Griscelli/LRO axis |
| `Lamp2` | 0 | 203 | Lysosomal membrane protein |
| `Ctsb` | 1 | 207 | Lysosomal protease; only its own transcript passed FDR |
| `Gaa` | 1 | 234 | Lysosomal hydrolase; only its own transcript passed FDR |
| `Tmem106b` | 1 | not re-read here | Lysosomal/endosomal disease modifier |
| `Grn` | 1 | not re-read here | Lysosomal disease gene |
| `Atg5` | 0 | 114 | Core autophagy conjugation |
| `Atg16l1` | 0 | 93 | Core autophagy conjugation |
| `Becn1` | 0 | 177 | Autophagy initiation |
| `Mtor` | 2 | 188 | Lysosomal nutrient-signaling kinase |
| `Tsc2` | 86 | 177 | mTORC1 suppressor; broader signaling perturbation, not a direct LYST analog |

For active focal analogs, the exact leading FDR genes supported a split between
a broad RAB7 late-endosomal state and smaller, target-specific responses:

- `Rab7` had 501 DEGs and induced lysosomal/acidification or sterol genes such
  as `Atp6v1b2`, `Dpp7`, `Atp6v0b`, `Msmo1`, and `Fdft1`.
- `Vps35` had 17 DEGs, including loss of the target transcript `Vps35` and
  same-direction overlap with the `Rab7` state on `Atp2a2`, `Grin2b`,
  `Ccdc136`, `Ptgds`, `Ache`, and `Kcnc2`.
- `Vps54` had 31 DEGs dominated by immediate-early and cytoskeletal genes
  (`Egr1`, `Jun`, `Stmn4`, `Tubb2a`, `Tuba1b`, `Nefm`), not a clean lysosomal
  CLEAR program.
- `Wdfy3` had 17 DEGs (`Jun`, `Stmn4`, `Gpm6a`, `Gls`, `Kcnc2`, and others),
  again without a broad lysosomal program.
- `Ctsb` and `Gaa` each produced exactly one FDR hit, the perturbed target
  transcript itself.

The runtime profile comparison confirmed that the FDR programs among the
active trafficking perturbations were shallow rather than interchangeable:
`Rab7` shared 2 positive and 5 negative significant genes with `Vps35`, 3
positive and 10 negative significant genes with `Vps54`, and 0 positive and 1
negative same-direction significant gene with `Wdfy3`.  `Vps35` and `Vps54`
shared only one negative significant gene, and `Wdfy3` had zero same-direction
significant overlap with `Vps54`.

# Same-experiment biological context

The Distributed Agents corpus captured several relevant boundaries from the same
dataset:

- `Rab7` loss induces a selective neuronal late-endosomal/lysosomal
  compensation program that is weakly shared by `Vps41` but absent after
  `Ocrl`, `Abca7`, or `Gdi1`.
- `Vps41` is a HOPS late-fusion subunit and showed weak same-pathway sharing
  with `Rab7` on `Mcoln1` and `Dpp7` in other cell groups, but it had no FDR
  genes in the requested `151 TH Prkcd Grin2c Glut` cells and only four FDR
  genes total across measured neuronal groups.
- Represented autophagy and lysosome perturbations are not transcriptomically
  interchangeable in this postnatal neuronal screen; `Atg5`, `Atg16l1`, and
  `Becn1` are mostly flat outside a restricted 155 MB Glut module.
- Same-complex or adjacent retrograde trafficking relationships were imperfect
  predictors: the corpus explicitly rejects `Vps53`/`Vps54` and
  `Vps35`/`Vps54` FDR-scale phenocopy in this assay.

Those observations are important for `Lyst` because LYST is real lysosomal
trafficking biology, but it is not RAB7 itself and does not imply the large
501-DEG `Rab7` count should be copied.

# Target-specific reasoning for `Lyst`

`Lyst` encodes the lysosomal trafficking regulator mutated in
Chediak-Higashi syndrome.  CHS cells have enlarged lysosomes or
lysosome-related granules and defects in vesicle trafficking, fusion/fission,
and secretory granule biology; the disorder can include progressive neurologic
disease that hematopoietic transplant does not correct (Kaplan et al. 2008;
Introne et al. 2017; Talbert et al. 2023).  LYST also has BEACH/ARM/HEAT/WD
domain architecture like vesicle-scaffolding proteins rather than the small
GTPase or core fusion roles of `Rab7` and HOPS.

The best positive in-dataset analog is `Rab7`: both `Rab7` and `Lyst` sit in
lysosomal trafficking, and `Rab7` proves that this focal cell group can produce
a large compensatory V-ATPase/hydrolase/sterol transcriptional state.  I used it
only as an upper bound.  Direct HOPS and lysosomal comparators closer to the
fusion/terminal-lysosome side were far weaker in the actual experiment:
`Vps41` had 0 DEGs in the focal cell group, `Lamp2` had 0, V-ATPase subunits
`Atp6v0a1`, `Atp6v1a`, and `Atp6v1b2` had 1, 0, and 0, and the lysosomal
enzyme perturbations `Gaa`, `Ctsb`, `Grn`, and `Tmem106b` sat at 1 DEG each or
less.  The corpus also notes that `Vps41` shares the `Rab7` pathway only weakly
at FDR level.  This argues against a broad `Rab7`-like count for `Lyst`.

The best protein-family analogs point still lower.  `Lrba` and `Nbea`, two
large BEACH-domain trafficking/scaffolding genes, had 0 DEGs in the focal
group.  `Wdfy3`, a large autophagy adaptor with BEACH-family links, reached
only 17 DEGs and did not share a lysosomal FDR program with `Rab7`.  These are
imperfect because their cargoes and subcellular roles differ from LYST, but
they show that perturbing a large vesicle-scaffolding BEACH-domain protein was
usually silent or narrow in the P37 neuronal assay.

The lysosome-related-organelle route is also a negative comparator.  AP-3,
BLOC, and RAB27/MYO5A pathways are connected to pigment granules and secretory
lysosome/LRO phenotypes adjacent to Chediak-Higashi biology, yet `Ap3b1`,
`Dtnbp1`, and `Rab27a` all had 0 DEGs and `Myo5a` had 1.  Their zero counts do
not prove LYST is silent, because LYST is not an AP-3 or BLOC-1 subunit, but
they show that the aspects of LRO biology heavily used by melanocytes and
immune cells did not expand into a neuronal FDR response in this focal group.

I therefore called the `Lyst` focal response absent rather than low-positive.
The progressive neurologic consequences of full `Lyst` loss are biologically
real, but the observed same-experiment analogs suggest that an acute sparse
CRISPR perturbation of a BEACH-domain lysosomal regulator in young
postmitotic neurons is more likely to resemble the silent AP-3/BLOC/BEACH and
VPS41/lysosomal-enzyme comparators than the broad central `Rab7` outlier.

Prediction: `Lyst -> 0` DEGs.

# Limits

The prediction is an extrapolation from neighbors; there is no same-experiment
`Lyst` signature in the corpus or parquet.  LYST has a distinctive role in
lysosomal size regulation, and the closest training genes are split across
late-endosome fusion, retromer/GARP sorting, AP-3/BLOC LRO trafficking, and
other BEACH proteins rather than true one-to-one paralogs.  The nearest
in-dataset positives (`Vps35`, `Vps54`, `Wdfy3`) are small but nonzero, so a
single-digit or teens count for `Lyst` would also be plausible.  Finally,
zeros in this screen can reflect limited acute knockdown, gRNA performance,
cell-state buffering, or power, not biological irrelevance of the gene.
