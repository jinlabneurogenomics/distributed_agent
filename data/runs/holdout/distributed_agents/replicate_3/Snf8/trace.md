# DEG-count prediction trace

## Question and resolved ambiguities

I interpreted the task as a single held-out prediction: `Snf8` knockout in
`151 TH Prkcd Grin2c Glut` neurons.  The requested endpoint is the number of
measured genes in that cell group with Wilcoxon `pvals_adj < 0.05`; the count
includes the self-target transcript if it happens to pass the same FDR
threshold.

I treated `n_degs` as an assay-specific count over the supplied Perturb-seq
analysis, not as a direct readout of neuronal essentiality, editing efficiency,
or absolute RNA abundance.  I therefore used target self-RNA changes only as
possible DE rows contributing to the count, not as a filter for whether CRISPR
worked.

## Sources used

- Supplied held-out manifest
  `[local file: 217_Snf8.csv]`;
  it contains exactly one target, `Snf8`.
- Supplied focal-cell training endpoint
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
  This has 1,674 non-held-out targets; the endpoint distribution is zero-heavy:
  1,205 targets have `n_degs = 0`, the median is 0, the 75th percentile is 1,
  63 targets have 10-99 DEGs, and 43 have at least 100 DEGs.
- Supplied DE parquet
  `[local file: training_de_all_cell_groups.parquet]`.
  I filtered this file to `group_name = '151 TH Prkcd Grin2c Glut'` and to
  endosomal/ESCRT/autophagy comparator genes present in the training count file,
  then counted rows with `pvals_adj < 0.05` and inspected the leading
  `pvals_adj` rows for each comparator.
- Distributed Agents same-experiment corpus
  `perturbai-july-260713-sourceguard-1773-v1`.  The corpus has no `Snf8` node,
  no curated `Snf8` findings, and no `Snf8` claims, which is consistent with
  the held-out design.  I used its Rab7, Vps35, Vps35l, Vps41, Vps53, and Vps54
  claims as same-experiment interpretation of represented endolysosomal and
  trafficking perturbations.
- Distributed Agents runtime profile comparison.  I compared the full 17,259-gene
  focal-cell log-fold-change vectors for
  `Chmp4b,Rab7,Vps35,Vps54,Vps35l,Vps41,Vps53,Atg5,Becn1,Lamp2,Sqstm1,Map1lc3a`
  with `pvals_adj < 0.05` as the significance call.
- External literature from PubMed:
  Babst et al., 2002, PMID 12194858, DOI 10.1016/S1534-5807(02)00219-8;
  Hierro et al., 2004, PMID 15329733, DOI 10.1038/nature02914;
  Im and Hurley, 2008, PMID 18539118, DOI 10.1016/j.devcel.2008.04.004;
  Progida et al., 2006, PMID 16857164, DOI 10.1016/j.bbrc.2006.07.007;
  Malerod et al., 2007, PMID 17714434, DOI 10.1111/j.1600-0854.2007.00630.x;
  Raiborg et al., 2007, PMID 18031739, DOI 10.1016/j.yexcr.2007.10.014;
  and Brugger et al., 2024, PMID 38423010,
  DOI 10.1016/j.ajhg.2024.02.005.

## Computation over the training data

I first queried the focal training counts for genes in the ESCRT cascade and
nearby late-endosomal/autophagy systems.  No ESCRT-0, ESCRT-I, or ESCRT-II
subunit in the query was present as a training perturbation: `Hgs`, `Stam`,
`Stam2`, `Tsg101`, `Vps28`, `Vps37a-d`, `Mvb12a/b`, `Ubap1`, `Vps36`, and
`Vps25` were all absent.  The directly represented ESCRT target was the
downstream ESCRT-III gene `Chmp4b`.

The relevant observed focal-cell counts were:

| training target | focal `n_degs` | relevance to `Snf8` |
|---|---:|---|
| `Chmp4b` | 0 | downstream ESCRT-III subunit; closest represented ESCRT-cascade perturbation |
| `Rab7` | 501 | strong late-endosomal/lysosomal state; branch counterexample |
| `Vps35` | 17 | modest retromer branch response |
| `Vps54` | 31 | modest GARP/endosome-to-TGN response |
| `Vps35l` | 0 | Retriever/Commander retromer-like branch, flat |
| `Vps41` | 0 | HOPS late-endosome/lysosome tether, flat in this focal group |
| `Vps53` | 0 | GARP/EARP branch, flat in this focal group |
| `Atg5` | 0 | macroautophagy, flat |
| `Becn1` | 0 | autophagy and endosomal PI3K complex component, flat |
| `Lamp2` | 0 | lysosomal membrane gene, flat |
| `Map1lc3a` | 1 | the sole FDR hit was the target transcript |
| `Sqstm1` | 1 | the sole FDR hit was the target transcript |

Raw DE rows in the focal group confirmed that each of these targets had the
expected 17,259 measured-gene rows.  The closest ESCRT-cascade analog,
`Chmp4b`, had 129 matched perturbed nuclei and no FDR-significant gene; its
best row was `Ptar1`, log2FC -0.522, `q = 0.174`.  The major non-ESCRT
endosomal positive, `Rab7`, had 215 matched perturbed nuclei and 501 DEGs; its
top significant genes included `Atp6v1b2`, `Ptgds`, `Dpp7`, `Scpep1`,
`Dusp1`, `Insig1`, `Atp6v0b`, and `Slc20a1`.  `Vps35` had 17 DEGs, including
`Atp2a2`, `Brsk1`, `Grin2b`, `Ccdc136`, and `Vps35` itself.  `Vps54` had
31 DEGs, including `Egr1`, `Kctd16`, `Jun`, `Lef1`, `Stmn4`, and `Atp2a2`.

The profile comparison gave the same qualitative picture.  `Chmp4b` was in the
`no_significant_features` activity class, `Rab7` in `at_least_50_significant_features`,
`Vps35` and `Vps54` in `10_to_49_significant_features`, and the remaining
candidate comparators either had no significant features or only 1 self-like
feature.  Because `Chmp4b`, `Vps35l`, `Vps41`, `Vps53`, `Atg5`, `Becn1`, and
`Lamp2` were flat in this focal group, they did not share any significant
same-direction ESCRT/lysosomal module with the `Rab7` state.

## Biology and analog choice

SNF8 is the mammalian Vps22/EAP30 subunit of ESCRT-II.  Structural work places
one Vps22/SNF8, one VPS36, and two VPS25 molecules in the ESCRT-II core, and
yeast and human studies put ESCRT-II downstream of ESCRT-I and upstream of
ESCRT-III in MVB cargo sorting (Babst et al. 2002; Hierro et al. 2004; Im and
Hurley 2008).  Vps22/EAP30 depletion in cultured mammalian cells blocks
degradative sorting of EGFR/CXCR4 and reduces other ESCRT-II subunits, so a
complete SNF8 defect is a real ESCRT loss of function, not a peripheral
annotation (Malerod et al. 2007; Raiborg et al. 2007).  Human biallelic SNF8
variants can cause severe neurodevelopmental or neurodegenerative phenotypes,
and zebrafish `snf8` loss has forebrain and optic-nerve phenotypes (Brugger
et al. 2024).

Those outside facts select `Chmp4b` as the most relevant represented training
analog: it is in the same ESCRT-mediated MVB pathway, immediately downstream
of ESCRT-II.  `Chmp4b = 0` argues that an acute partial hit to this machinery
need not cross the Wilcoxon FDR threshold in recovered postnatal
`151 TH Prkcd Grin2c Glut` nuclei.  The comparison is imperfect because CHMP4B
has CHMP4A/CHMP4C paralogs whereas SNF8 is a single ESCRT-II core subunit, but
it is still a much tighter transcriptional prior than broad late-endosome
genes.

`Rab7 = 501` is the principal counterexample showing that this assay can detect
a late-endosomal/lysosomal compensation state.  I did not transfer that count
to `Snf8`: RAB7 regulates late endosome/lysosome maturation and positioning,
and the Distributed Agents corpus specifically describes Rab7 as a selective
late-endosomal/lysosomal compensation program, weakly shared by Vps41 and
absent from several adjacent perturbations.  VPS22/SNF8 can interact with the
Rab7 effector RILP (Progida et al. 2006), but that is not the same as a
Rab7-like loss, and `Vps41`, `Lamp2`, `Atg5`, and `Becn1` were all flat in the
focal training data.

I also treated `Vps35 = 17` and `Vps54 = 31` as boundaries rather than direct
priors.  They show that some vesicle-trafficking defects produce a small
thalamic response, but the same-experiment corpus calls both programs
branch-specific: retromer/Retriever/WASH neighbors did not phenocopy `Vps35`,
and represented Golgi, retrograde, endosome-to-TGN, retromer, SNARE, and
glycosylation perturbations did not collapse into a generic trafficking stress
state.  ESCRT-II-driven intraluminal vesicle formation is a different branch
from retromer recycling or GARP tethering.

## Target-specific prediction

For `Snf8`, the zero/nonzero decision is mostly dataset-driven.  The training
endpoint is dominated by zeros; the only close ESCRT-cascade perturbation,
`Chmp4b`, had zero DEGs; and multiple endolysosomal/autophagy genes adjacent
enough to report generic stress also had zero or only a self-transcript hit.
External biology says SNF8 is more central than many flat genes, so a very weak
nonzero response is plausible, but the represented same-experiment positives
belong to distinct Rab7, retromer, or GARP branches.

I therefore predict no FDR-significant genes in the focal cell group:

| target | predicted `n_degs` |
|---|---:|
| `Snf8` | 0 |

## Limits

The largest uncertainty is the missing ESCRT-II neighborhood: `Vps25`, `Vps36`,
`Tsg101`, `Vps28`, and ESCRT-0 targets were not available training
perturbations, so the comparison relies on a downstream ESCRT-III gene with
possible paralog buffering.  Full SNF8 loss can destabilize ESCRT-II and cause
neurodevelopmental phenotypes, but most external evidence comes from cell
culture, constitutive human disease, zebrafish development, or siRNA rather
than sparse acute postmitotic mouse neuronal CRISPR.  Finally, the requested
count is thresholded; a single self-target or lysosomal transcript could cross
FDR in the hidden data even if the broader biological state is effectively
quiet.
