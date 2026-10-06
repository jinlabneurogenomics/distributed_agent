# Reasoning trace

## Question and endpoint

The requested prediction is the number of measured genes that would pass
Benjamini-Hochberg FDR 0.05 after acute AAV-CRISPR loss of each held-out target
in `151 TH Prkcd Grin2c Glut` thalamic glutamatergic neurons. The requested
manifest contains one held-out gene:

```tsv
target_name
Irf6
```

I treated `n_degs` as this experiment's assay- and cell-type-specific DEG
count, not as a general score of gene essentiality or biological importance.
The focal population name contains the marker `Prkcd`; I did not interpret that
as tyrosine hydroxylase or as evidence that an epithelial PKCdelta/RIPK4/IRF6
axis is active.

## Sources used

- Exact training endpoint:
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
- Exact differential-expression rows from:
  `[local file: training_de_all_cell_groups.parquet]`.
- Same-experiment semantic layer:
  Distributed Agents corpus release `perturbai-july-260713-sourceguard-1773-v1`.
  I used `target_context` for `Irf2`, `Irf9`, `Trp63`, `Grhl2`, `Tfcp2`,
  and `Zeb1`, and lexical claim search for IRF/IFN, Grainyhead/CP2, and
  EMT-adjacent comparisons.
- External literature from PubMed, used only to place `Irf6` into epithelial,
  craniofacial, p63, AP-2, RIPK4, and junctional biology:
  - Moretti et al. 2010, DOI `10.1172/JCI40267`, PMID `20424325`: a
    DeltaNp63/IRF6 feedback loop in keratinocyte proliferation and
    differentiation.
  - Thomason et al. 2010, DOI `10.1172/JCI40266`, PMID `20424327`: p63 binds
    and activates an IRF6 enhancer and cooperates with IRF6 in secondary-palate
    development.
  - Botti et al. 2011, DOI `10.1073/pnas.1110931108`, PMID `21807998`: IRF6
    regulates squamous epithelial differentiation, adhesion and cell-contact
    programs and has tumor-suppressive activity in squamous carcinomas.
  - Biggs et al. 2014, DOI `10.1242/jcs.139246`, PMID `24777480`: IRF6
    regulates keratinocyte migration through adhesion/RhoA/Arhgap29-related
    behavior.
  - Kousa et al. 2018, DOI `10.1016/j.jid.2018.05.030`, PMID `29913133`: IRF6
    and TFAP2A interact in an epidermal developmental network.
  - Antiguas et al. 2021, DOI `10.1016/j.jid.2021.06.031`, PMID `34310950`:
    IRF6 contributes to delivery of E-cadherin and other adhesion proteins to
    the keratinocyte plasma membrane.
  - Yan et al. 2023, DOI `10.3390/cancers15030737`, PMID `36765696`: RIPK4
    acts upstream of IRF6 in a Notch/RIPK4/IRF6/Elovl4 squamous epithelial
    axis.
  - Wright et al. 2024, DOI `10.1016/j.mucimm.2024.03.013`,
    PMID `38604478`: IRF6 shapes intestinal epithelial development and
    interferon responses.
  - Lopez-Pajares et al. 2025, DOI `10.1016/j.stem.2025.02.017`,
    PMID `40120584`: IRF6 dimerization supports epidermal differentiation and
    induction of GRHL1/GRHL3/HOPX/PRDM1 in that epithelial context.

## Computational calibration

The 151 TH training set has 1,674 non-held-out perturbations. Its DEG counts are
highly sparse:

- `0` DEGs for 1,205 targets, or 71.98 percent.
- `1-9` DEGs for 363 targets.
- `10-99` DEGs for 63 targets.
- `>=100` DEGs for 43 targets.
- median `0`, 75th percentile `1`, 90th percentile `2`, 95th percentile `18`.

So a nonzero call needs evidence that `Irf6` belongs to one of the specific
neuronal response classes that were active in the screen.

From the parquet I pulled all rows in the focal cell group for mechanistically
nearby training targets and counted `pvals_adj < 0.05`, matching the endpoint.
For epithelial/IFN marker checks I also pulled the focal rows for measured
genes such as `Irf6`, `Trp63`, `Grhl1`, `Grhl3`, `Hopx`, `Prdm1`, `Elovl4`,
`Arhgap29`, `Cdh1`, `Nectin4`, `Krt10`, `Krt14`, `Ifit1`, `Ifit2`, `Ifit3`,
`Oas1a`, `Oasl2`, `Isg15`, `Stat1`, and `Stat2` under the same analog
perturbations. This was meant to test whether a sparse but biologically
recognizable IRF6/IFN or epithelial differentiation module was present below
the full DEG count.

## Target-specific analogs

### Irf6

`Irf6` was absent from the corpus, the training-count CSV, and the training DE
signatures by construction. I therefore compared three biologically motivated
neighborhoods and one positive counterexample.

**1. IRF/IFN/JAK-STAT neighborhood: null in 151 TH.**

The obvious family or pathway analogs in the focal training set were all flat
or self-only:

```tsv
target	n_degs in 151 TH Prkcd Grin2c Glut
Irf1	0
Irf2	0
Irf3	0
Irf5	0
Irf8	0
Irf9	0
Ifnar1	0
Ifnar2	0
Ifngr1	0
Ifngr2	0
Stat1	1
Stat2	0
Stat3	0
Ifih1	0
Nfkb1	0
Rel	0
Tlr3	0
Tlr4	0
Adar	0
Spi1	0
```

The single `Stat1` hit in the focal data is `Stat1` itself
(`logfoldchanges = -1.300`, `pvals_adj = 0.027`), not a downstream ISG module.
In the same focal rows, canonical IFN-stimulated transcripts queried under
`Irf2` and `Irf9` perturbations were not significant: `Ifit1`, `Ifit2`,
`Ifit3`, `Ifitm3`, `Oas1a`, `Oasl2`, `Isg15`, `Usp18`, `Stat1`, and `Stat2`
all had adjusted p-values of `1.0`.

The Distributed Agents corpus independently annotates the represented IRF, IFN receptor,
STAT, NF-kB-neighbor, and pathogen-sensor genes as lacking a basal neuronal
IFN/ISG/MHC-I inflammatory module in unchallenged juvenile NeuN+ nuclei. In
particular, the `Irf2` and `Irf9` contexts support the high-confidence claim
that basal postnatal NeuN-enriched neurons lack a detectable tonic
type-I-IFN/IFNAR-ISGF3 program. That is relevant because it makes IRF family
membership a poor argument for a large `Irf6` response in this assay.

**2. p63 and craniofacial epithelial differentiation neighborhood: null in
151 TH.**

External biology puts mammalian IRF6 most strongly in p63-controlled
epidermal, oral periderm, palate, keratinocyte migration, and cell-adhesion
programs rather than in a constitutive neuronal circuit. The closest directly
measured p53-family epithelial regulator, `Trp63`, had `0` DEGs in the focal
cell group; its paralogs `Trp53` and `Trp73` also had `0`. The Distributed Agents
`Trp63` findings describe this as a pan-measured neuronal transcriptional null:
neither p53/PUMA stress genes, precursor-loss markers, nor epithelial
`Perp`/keratin targets were recovered after acute P16 `Trp63` loss.

The focal parquet rows agree with that interpretation. Under `Trp63`
perturbation, measured genes that would report an IRF6/p63 epithelial state
were all nonsignificant in `151 TH`: `Irf6`, `Grhl1`, `Grhl2`, `Grhl3`, `Hopx`,
`Prdm1`, `Elovl4`, `Arhgap29`, `Cdh1`, `Cdh3`, `Nectin1`, `Nectin4`, `Perp`,
`Dsp`, `Pkp1`, `Krt10`, `Krt14`, `Tfap2a`, `Tfap2b`, and `Tfap2c` all had
`pvals_adj = 1.0`.

**3. Grainyhead/CP2, AP-2, Notch/RIPK4, and junctional relatives: mostly
null.**

IRF6-adjacent epithelial genes that were training perturbations had the
following focal counts:

```tsv
target	n_degs in 151 TH Prkcd Grin2c Glut
Grhl2	0
Tfcp2	0
Ubp1	0
Ovol2	0
Tfap4	0
Notch1	0
Notch2	0
Notch4	0
Nectin1	0
Klf1	0
Klf7	1
Klf9	19
```

`Grhl2` is not a paralog of `Irf6`, but it is a useful counterfactual because
the recent epidermal literature places GRHL-family factors among IRF6-associated
epithelial differentiation outputs. Distributed Agents reports that `Grhl2` lost the
canonical apical-junction, epithelial-barrier and EMT-suppression program in
all measured neuronal groups, and that the represented CP2/Grainyhead single
perturbations `Ubp1`, `Tfcp2`, and `Grhl2` were weak or silent in postmitotic
neurons rather than forming a shared module. In the focal parquet rows,
`Grhl2`, `Tfcp2`, `Ubp1`, and `Ovol2` had no significant changes in `Irf6`,
`Trp63`, `Grhl1`, `Grhl3`, `Hopx`, `Prdm1`, `Elovl4`, `Arhgap29`, `Cdh1`,
`Nectin4`, `Perp`, or keratin markers.

`Klf9` is a useful boundary: it did produce a detectable focal response
(`19` DEGs), so the conclusion is not that all transcription factors are
invisible in 151 TH. However, its effect belongs to a KLF9/Sin3a/Zbtb7a-like
thalamic de-repression class annotated in the same-experiment corpus, not to
IRF6 epithelial differentiation.

**4. EMT-adjacent counterexample: Zeb1 is positive but not a reason to make
Irf6 nonzero.**

`Zeb1` had `15` focal DEGs, and `Ctbp1` had `5`. Distributed Agents annotates this as a
small all-up thalamic module involving `Stxbp2`, `F11r`, `Ap1m2`, `St3gal4`,
`Hook2`, and `Usp43`, partly shared between `Zeb1` and its co-repressor
`Ctbp1`. In the raw focal rows the strongest `Zeb1` genes were `Stxbp2`
(`pvals_adj = 3.97e-25`), `Ap1m2` (`1.24e-20`), and `F11r` (`1.49e-10`).

That is the main positive nearby counterexample, but it argues only for a
narrow ZEB/CtBP polarity or membrane-trafficking branch. The corpus explicitly
notes that `Zeb2`, TGF-beta receptors, SMADs, `Snai2`, `Twist2`, and E-protein
perturbations did not recover the `Zeb1` module. The training counts in 151 TH
match that boundary: `Zeb2 = 0`, `Snai2 = 0`, `Twist2 = 0`, `Tgfbr1 = 0`,
`Tgfbr2 = 0`, `Tgfbr3 = 0`, `Smad3 = 0`, `Smad4 = 0`, with only `Smad2 = 1`.
Under `Zeb1` perturbation itself, the IRF6/p63 markers that were queried had
`pvals_adj = 1.0`, so this positive module is not a hidden IRF6-like epithelial
program.

## Zero/nonzero decision and point estimate

I predict `Irf6` will have no FDR 0.05 DEGs in `151 TH Prkcd Grin2c Glut`.

The within-dataset evidence dominates the count: every focal analog on the
basal IRF/IFN side is zero or self-only, the p63-family epithelial axis is zero,
and the Grainyhead/CP2/Notch/OVOL comparisons around epithelial
differentiation are zero. The few positive counterexamples either belong to
different 151 TH response classes (`Klf9`) or to a narrow ZEB/CtBP module that
does not bring along the IRF6/p63/keratinocyte markers (`Zeb1` and `Ctbp1`).
Given the training distribution, a target in this mechanistic region is more
likely to sit in the 72 percent zero class than in the weak 1-9 class, so the
integer point prediction is exactly `0`.

## Limits and caveats

- There is no same-experiment `Irf6` report in the Distributed Agents corpus; the
  in-corpus evidence is all by analog or counterexample.
- `Grhl1`, `Grhl3`, `Ripk4`, `Prkcd`, and `Tfap2a` were available as measured
  transcripts in the focal DE rows but not as represented training
  perturbations for the focal count comparison, so the strongest epithelial
  IRF6 pathway could not be perturbed node by node.
- `Irf6` biology is mostly epithelial, craniofacial, wound-healing, and
  ligand/infection-dependent in the cited literature. Extrapolating those
  programs to sparse postnatal NeuN+ thalamic neurons is inherently imperfect.
- A predicted zero DEG count does not prove lack of editing or lack of
  non-transcriptional phenotypes. The endpoint only counts recovered nuclear
  mRNA changes crossing BH FDR 0.05.
- The point estimate is calibrated for squared log1p-style DEG count error and
  this exact FDR threshold. Very small nominal shifts could still exist below
  the multiple-testing cutoff.
