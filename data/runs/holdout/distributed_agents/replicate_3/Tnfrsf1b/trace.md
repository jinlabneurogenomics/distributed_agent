# Predicting held-out DEG count for `151 TH Prkcd Grin2c Glut`

## Question and resolution

The requested readout is the number of measured genes passing BH-adjusted
Wilcoxon `pvals_adj < 0.05` after a held-out acute CRISPR loss-of-function
perturbation in `151 TH Prkcd Grin2c Glut` neuronal nuclei. The manifest for
this run contains one held-out target, in the requested order:

```text
Tnfrsf1b
```

I treated `n_degs` as a point prediction for this exact assay and cell group,
not as a gene-essentiality or editing-efficiency estimate. The CRISPR design
was sparse, postnatal, unchallenged, and neuronal/NeuN-enriched; therefore I
weighted same-assay loss-of-function profiles in the focal thalamic group
above developmental knockout, peripheral immune-cell, glial, injury, or
ligand-addback literature.

## Sources used

- Input endpoint CSV:
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
- Input DE parquet:
  `[local file: training_de_all_cell_groups.parquet]`.
- Manifest:
  `[local file: 243_Tnfrsf1b.csv]`.
- Same-experiment Distributed Agents corpus, release
  `perturbai-july-260713-sourceguard-1773-v1`.
  `Tnfrsf1b` itself was absent from the corpus, as expected for a held-out
  target, so I used Tnfrsf1a-, Traf3-, Chuk-, Map3k7-, Nfkb1-, TNFRSF-, and
  TLR/NF-kappa-B-centered findings and claims.
- PubMed literature for the external TNFR2/TNF pathway facts:
  Grell et al. 1995, Cell, DOI `10.1016/0092-8674(95)90192-2`, PMID 8521496;
  Rothe et al. 1995, Science, DOI `10.1126/science.7544915`, PMID 7544915;
  Wajant and Scheurich 2001, Int J Biochem Cell Biol, DOI
  `10.1016/S1357-2725(00)00064-9`, PMID 11167129;
  Borghi et al. 2016, Biochemical Pharmacology, DOI
  `10.1016/j.bcp.2016.03.009`, PMID 26993379;
  Pegoretti et al. 2018, Front Immunol, DOI `10.3389/fimmu.2018.00925`,
  PMID 29760711;
  Medler and Wajant 2019, Expert Opin Ther Targets, DOI
  `10.1080/14728222.2019.1586886`, PMID 30856027;
  Papazian et al. 2021, J Neuroinflammation, DOI
  `10.1186/s12974-021-02200-4`, PMID 34565380.

## Computational evidence from the training data

I first loaded the training DEG counts for the focal cell group and tabulated
mechanistic neighbors of `Tnfrsf1b`. All close represented TNFR, TLR/IL-1,
IKK/NF-kappa-B, TAK1/MAPK, and TNF-survival/death comparators were null in the
held-out target's exact endpoint:

```tsv
target_name	n_degs
Tnfrsf1a	0
Cd40	0
Tnfrsf4	0
Tnfrsf9	0
Tnfrsf11a	0
Tnfrsf13c	0
Fas	0
Traf3	0
Chuk	0
Map3k7	0
Nfkb1	0
Rel	0
Cyld	0
Bcl2	0
Il1r1	0
Il1rap	0
Tlr2	0
Tlr3	0
Tlr4	0
Tlr5	0
Tlr7	0
Tlr8	0
Map2k6	0
Mapk1	0
Mapk9	0
```

The full focal-cell training distribution was heavily zero-inflated
(`469/1674` nonzero perturbations; median `0`, 75th percentile `1`), but the
cell group was not globally insensitive: `Uba5`, `Tpr`, `Sin3a`, `Rnpc3`,
`Zbtb7a`, `U2af2`, `Psmb4`, and `Hnrnpu` each had hundreds to thousands of DEGs.
Thus the TNF-axis zeroes were interpreted as pathway-context evidence, not as a
failure of the focal group to ever produce broad responses.

To check whether the zero counts concealed a shared subthreshold TNFR/TLR
state, I used the Distributed Agents runtime `profile_compare` over the focal-cell
Wilcoxon `scores`, with `pvals_adj` as the significance column and 20
mechanistic comparators:

```text
Tnfrsf1a, Traf3, Chuk, Map3k7, Nfkb1, Rel, Cd40, Tnfrsf4,
Tnfrsf9, Tnfrsf11a, Tnfrsf13c, Fas, Tlr2, Tlr3, Tlr4, Tlr5,
Tlr7, Tlr8, Il1r1, Il1rap
```

All 20 had `response_activity_status = no_significant_features` across 17,259
measured genes in `151 TH Prkcd Grin2c Glut`. Pairwise whole-profile cosines
from the primary anchors were near zero: for example, `Tnfrsf1a` to the queried
peers ranged from `-0.0197` to `0.0265`, and `Traf3` to those peers ranged from
`-0.0510` to `0.0648`. The nearest eligible whole-profile neighbors for
`Tnfrsf1a` in all 1,674 training targets were only about `0.06` correlated.
This supported the interpretation that the focal profiles are flat rather than
members of a coherent low-amplitude module.

For a direct marker check, I filtered the Parquet to
`group_name == "151 TH Prkcd Grin2c Glut"` and to pathway neighbors above, then
looked up TNF/NF-kappa-B/AP-1/inflammatory sentinel genes. In the closest
receptor control `Tnfrsf1a`, the adjusted p value was `1.0` for `Nfkbia`,
`Tnfaip3`, `Birc2`, `Birc3`, `Jun`, `Fos`, `Nfkb1`, `Rel`, `Traf3`, `Tnf`,
`Ccl2`, `Cxcl10`, and `Tnfrsf1b`; the target's own RNA was also not changed
(`Tnfrsf1a` log2FC `-0.124`, adjusted p `1.0`, `173` perturbed versus `23679`
control nuclei). `Traf3` likewise left `Nfkbia`, `Tnfaip3`, `Birc2`, `Birc3`,
`Jun`, `Fos`, `Nfkb1`, `Rel`, `Tnf`, `Ccl2`, `Cxcl10`, and `Tnfrsf1b`
uncorrected at adjusted p `1.0` in this cell group. The same sentinel panel was
adjusted-null in `Cd40`, `Chuk`, `Map3k7`, `Nfkb1`, `Rel`, the represented
TNFRSF-family targets, and the TLR/IL-1 comparators that were queried.

The same-experiment Distributed Agents corpus reinforced the local measurements. The
high-confidence claim `claim:778b2c45f226febe4372` states that represented
`CD40`/`TNFR`/`TLR`/`IL-1` to `TAK1`/`IKK`/`NF-kappa-B`/`JNK`/`p38`
perturbations are broadly transcriptionally silent as a basal module in
unchallenged postnatal NeuN-positive neurons. The high-confidence claim
`claim:c5ebf285abfd6f803965` states that represented TNFR-superfamily,
death-receptor, and NF-kappa-B-adjacent perturbations are refractory to forming
shared basal immune-like or death-receptor modules. The Tnfrsf1a-specific
finding `Tnfrsf1a:F002` reports no basal TNF/NF-kappa-B immediate program after
`Tnfrsf1a` perturbation, and the Traf3-specific finding `Traf3:F004` reports
that `Cd40`, `Chuk`, `Map3k7`, `Nfkb1`, `Rel`, `Tlr2`, `Tlr4`, and
`Tnfrsf1a` each had zero downstream FDR < 0.10 genes in their matched neuronal
surfaces, while `Tlr3` and `Tnfrsf13c` yielded only isolated tiny responses in
the broader atlas. In a graph audit of the `Tnfrsf1a`/`Traf3`/`Nfkb1` expansion
set, the exact eligible expansion candidates were `Tlr4`, `Chuk`, `Map3k7`,
`Rel`, and `Tlr2`; all five are represented in the focal endpoint above and all
had `n_degs = 0`.

## Target-specific reasoning

### Tnfrsf1b

`Tnfrsf1b` encodes TNFR2, the 75/80-kDa TNF receptor. Unlike TNFR1
(`Tnfrsf1a`), which is broadly expressed and contains a death domain, TNFR2 is
preferentially engaged by membrane TNF and signals by recruiting TRAF adaptors,
especially TRAF2, into NF-kappa-B, MAPK/JNK, survival, and cell-type-specific
immune-regulatory programs. Grell et al. 1995 established the preferential
activity of transmembrane TNF on the 80-kDa receptor; Rothe et al. 1995 showed
that TRAF2 can mediate NF-kappa-B activation downstream of TNFR2 and CD40; and
Wajant and Scheurich 2001 and Borghi et al. 2016 review the receptor-proximal
TRAF2 logic. In the CNS and periphery, TNFR2 biology is strongly context- and
ligand-gated: reviews by Pegoretti et al. 2018 and Medler and Wajant 2019
emphasize immune/endothelial and oligodendrocyte/Treg protective contexts, and
Papazian et al. 2021 found neuronal TNFR2 effects in inflammatory demyelination
and excitotoxicity models rather than an unchallenged basal neuronal
transcriptome.

The strongest within-dataset analog is `Tnfrsf1a`, because it is the other TNF
receptor and should be the most likely represented perturbation to reveal a
basal TNF-responsive neuronal state. It had `0` DEGs in the focal cell group,
no corrected movement in `Nfkbia`, `Tnfaip3`, `Birc2`, `Birc3`, `Jun`, `Fos`,
`Nfkb1`, `Rel`, `Ccl2`, `Cxcl10`, or `Tnf`, and no meaningful whole-profile
similarity to any candidate neighbor. That does not prove TNFR2 equals TNFR1,
because TNFR2 lacks the TNFR1 death domain and can instead signal through
TRAF2/cIAP and noncanonical NF-kappa-B. I therefore checked the TNFR2/CD40-like
TRAF arm: `Cd40`, `Tnfrsf4`/OX40, `Tnfrsf9`/4-1BB, `Tnfrsf11a`/RANK,
`Tnfrsf13c`/BAFFR, `Fas`, and `Traf3` were each `0` DEGs in the focal endpoint,
and the Distributed Agents corpus specifically noted that represented TNFRSF and
NF-kappa-B-neighbor perturbations did not reveal a reusable immune/death
receptor module in NeuN-positive postmitotic neurons.

I also treated intracellular common signaling nodes as counterexamples to a
simple "TNFR2 should produce canonical NF-kappa-B" forecast. In
`151 TH Prkcd Grin2c Glut`, `Chuk`, `Map3k7`, `Nfkb1`, `Rel`, `Cyld`, and
`Traf3` each produced zero DEGs. Represented receptor systems that converge on
the same NF-kappa-B/AP-1 machinery in immune cells, namely `Tlr2`, `Tlr3`,
`Tlr4`, `Tlr5`, `Tlr7`, `Tlr8`, `Il1r1`, and `Il1rap`, were also all zero in
the same endpoint. The Tnfrsf1b prediction is therefore driven primarily by
same-assay, same-cell-type nulls in a coherent TNF/TNFR/TLR/IKK/TAK1
neighborhood, with external literature used to choose the appropriate
neighborhood and to avoid over-weighting unrelated TNFRSF genes.

The point prediction is `0` DEGs. The expected effect is below the FDR 0.05
threshold, because the assay is an unchallenged sparse neuronal CRISPR readout
that largely excludes microglia, astrocytes, oligodendrocytes, endothelial
cells, activated lymphocytes, membrane-TNF stimulation, demyelination, and
excitotoxic injury. All of those are better contexts for TNFR2 signaling than
healthy juvenile thalamic neurons.

## Limits

The closest exact TNFR2 adapter, `Traf2`, was not a training perturbation in
the focal endpoint, and neither `Tnf`, `Nfkb2`, `Map3k14`, `Rela`, `Relb`,
`Ikbkb`, `Ikbkg`, `Birc2`, nor `Birc3` was directly perturbed, so the TRAF2/cIAP
and noncanonical NF-kappa-B arms are inferred through imperfect nodes such as
`Traf3`, `Cd40`, `Tnfrsf13c`, `Chuk`, `Nfkb1`, and `Rel`. TNFR2 can act in
neurons under injury or excitotoxic conditioning, but those settings have
strong glial and ligand components missing from this assay. Some queried
receptor perturbations had only about 90 to 200 perturbed nuclei in the focal
cell group, so isolated very small effects could be below power. The prediction
therefore means "no gene is expected to pass this screen's BH-adjusted
Wilcoxon threshold", not "TNFR2 has no CNS biology."
