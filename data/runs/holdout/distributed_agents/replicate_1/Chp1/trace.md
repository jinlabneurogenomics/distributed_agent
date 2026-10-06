# Chp1 held-out DEG-count prediction

## Question and endpoint alignment

The requested held-out target is `Chp1`. I interpreted the endpoint as the count
of measured genes in `151 TH Prkcd Grin2c Glut` whose Scanpy Wilcoxon
Benjamini-Hochberg adjusted p-value is `<0.05` after acute, mosaic AAV-CRISPR
loss of `Chp1`, using the same focal-cell analysis used in the supplied
training CSV. This is a focal-cell, FDR-thresholded response-breadth endpoint;
it is not a count of total biological effects, viability, axon maintenance,
editing efficiency, or all genes with subthreshold shifts.

The held-out endpoint is absent from the declared inputs: `Chp1` is not in the
training DEG-count CSV and the same-experiment July 260713 sourceguard corpus
has no `Chp1` report. The training counts are direct observations for
non-held-out perturbations and the parquet rows are the corresponding
per-gene DE statistics. The July corpus is a packaged interpretation of the
same Perturb-seq experiment, so I treated it as same-experiment context rather
than independent validation. External PubMed literature was used only to decide
which non-held-out perturbations were molecularly relevant.

## Quantitative checks over the declared data

I used the supplied training endpoint file,
`151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`, to inspect the empirical
scale of the focal-cell endpoint. It contained 1,674 training targets: 469 were
nonzero; the median was 0; the 75th percentile was 1; the 90th percentile was 2;
the 95th percentile was 18; and the largest signatures ranged from hundreds to
2,677 DEGs. Thus an endpoint of 0-2 genes is ordinary for weakly active
perturbations, while 20 genes is already above the 95th percentile.

For training analogs, I queried
`training_de_all_cell_groups.parquet` in the focal cell group and counted
`pvals_adj < 0.05` per `gene_target`. I checked three local neighborhoods:

- plasma-membrane or endomembrane Na+/H+ and pH-homeostasis relatives:
  `Slc9a7` had 1 DEG, `Slc9a9` had 0, `Slc4a7` had 0, `Atp6v0a1` had 1, and
  `Atp6v1a`, `Atp6v1b2`, and `Atp6v1e1` each had 0.
- EF-hand / calcineurin-adjacent calcium signaling: `Ppp3r1` had 9 DEGs,
  `Ppp3ca` had 4, `Ppp3cc` had 0, `Fkbp1a` had 1, `Nfatc3` had 0, `Prkca` had
  0, `Itpr1` had 0, `Calm1` had 14, `Calm2` had 0, and `Calm3` had 1.
- broader Ca2+ transport counterexamples: `Atp2b1` had 22 DEGs and `Atp2a2`
  had 187, much larger than the Na+/H+ exchanger family and larger than the
  calcineurin core.

Exact focal-cell significant genes confirmed the same scale. `Ppp3r1` produced
a nine-gene FDR<0.05 signature whose top genes were `Pcsk1n`, `Ptprs`,
`Atp2a2`, and `Coro6`. `Ppp3ca` produced four FDR<0.05 genes, sharing only the
secretory-pathway marker `Pcsk1n` with `Ppp3r1` at the looser FDR<0.10 level in
the corpus summary. `Slc9a7` produced only self-target `Slc9a7` at FDR<0.05 in
this focal cell group, and `Slc9a9` produced no FDR<0.05 genes. `Atp2b1`
produced a more activity-like 22-gene FDR<0.05 signature including up-regulated
`Fos`, `Nr4a1`, `Vgf`, and `Cck`, but `Ppp3ca` and `Ppp3r1` reports explicitly
noted that these canonical immediate-early/activity genes and RCAN/NFAT
feedback genes were not robustly induced by calcineurin perturbation.

## Biological model for Chp1

`Chp1` encodes calcineurin-like EF-hand protein 1, a myristoylated
calcineurin-B-homolog protein. Its strongest established direct role is to bind
the juxtamembrane regulatory region of plasma-membrane NHE transporters:
Pang et al. showed that CHP1 binding supports physiological NHE1/NHE2/NHE3
Na+/H+ exchange activity and that loss of the CHP-binding site or competitive
CHP depletion markedly reduces exchanger activity (Pang et al. 2001,
DOI: 10.1074/jbc.M100296200). Later biochemical work showed that CHP1 is
needed for NHE1 pH sensing and stimulus regulation (Pang et al. 2004,
DOI: 10.1021/bi0360004) and structurally binds the NHE1 cytoplasmic
juxtamembrane helix (Mishima, Wakabayashi and Kojima 2006,
DOI: 10.1074/jbc.M604092200). In mice, a recessive hypomorphic `Chp1`
vacillator mutation reduces CHP1 protein, disrupts NHE1 maturation and axon
terminal membrane localization in cerebellar Purkinje cells, and eventually
causes Purkinje axon degeneration; `Nhe1` ablation phenocopies that axonal
maintenance defect (Liu et al. 2013, DOI: 10.1523/JNEUROSCI.0406-13.2013).
Janzen et al. found that PLS3 overexpression delayed this ataxic/axon-swelling
phenotype without fully preventing later disease (Janzen et al. 2019,
DOI: 10.3389/fnins.2019.00993).

The causal transfer chain for the focal assay is therefore:

`Chp1` CRISPR loss -> less CHP1 cofactor activity -> altered NHE1 maturation,
surface localization, and Na+/H+/pH homeostasis -> possible axonal,
endosomal/trafficking, actin, or calcium-coupled stress -> selection of
successfully edited nuclei over three to four postnatal weeks and recovery of
surviving NeuN+ neuronal nuclei -> single-nucleus DE in thalamic
`151 TH Prkcd Grin2c Glut` cells.

That chain has two major breaks relative to the strongest literature phenotype.
The mouse neurodegeneration phenotype was most direct in Purkinje cells and in
presynaptic axon terminals, whereas the requested readout is thalamic nuclear
RNA in recovered nuclei. The endpoint would miss earlier depletion of severely
affected neurons and could also miss axon-terminal or pH defects that did not
feed back to nuclear RNA by FDR<0.05. Conversely, the perturbation is only a
sparse postnatal CRISPR loss, not a germline NHE1/CHP1-null situation.

## Target-specific analogs and prediction

`Slc9a1`, the clearest direct transporter client of CHP1/NHE1 biology, was not
present as a non-held-out training perturbation. The closest represented NHEs
were `Slc9a7` and `Slc9a9`; they control organelle rather than plasma-membrane
pH, so they are imperfect analogs, but they ask whether disrupting this
transporter family creates a broad secondary nuclear response in this atlas.
They did not: the exact focal-cell training counts were 1 for `Slc9a7` and 0
for `Slc9a9`. The same-experiment July report for `Slc9a7` concluded that
endomembrane pH relatives, including `Slc9a9`, V-ATPase subunits, and
`Clcn3`/`Clcn4`, were flat or nonconvergent, and that acute postmitotic
`Slc9a7` loss was largely off-axis for the nuclear transcriptomic endpoint.
This argues for a Chp1 count near the null boundary rather than for tens or
hundreds of DE genes.

`Ppp3r1` and `Ppp3ca` are biochemical counterpoints because CHP1 is an
EF-hand calcineurin-B homolog but is not the canonical calcineurin regulatory
subunit. `Ppp3r1` loss gave 9 focal-cell DEGs and `Ppp3ca` loss gave 4. The July
corpus characterized these as a small, partly convergent calcineurin response
centered on `Pcsk1n`, not as a broad NFAT, immediate-early, or stress program;
the represented catalytic paralog `Ppp3cc` was flat. Calcineurin therefore sets
an upper local bound for a Chp1-like EF-hand cofactor perturbation in the same
cell group, but it is not a direct same-complex analog and likely overstates
CHP1 because CHP1's best-established direct client is NHE1, not nuclear
NFAT-regulated transcription. I therefore weighted the NHE/pH-homeostasis
analogs more than the calcineurin analogs.

`Atp2b1` and `Atp2a2` were deliberately treated as counterexamples, not
templates. They show that this thalamic class can mount broader transcriptional
programs when ion homeostasis is pushed through plasma-membrane calcium
extrusion or ER calcium stores. `Atp2b1` had 22 DEGs with an IEG/neuropeptide
signature and `Atp2a2` had 187. CHP1/NHE1 can interact with pH and indirectly
with calcium, but the calcineurin and NHE-family training perturbations show
that broad pathway labels do not automatically collapse into the same
FDR-supported nuclear state.

Based on those analogs I predict `Chp1` will be nonzero but only barely:
`predicted_n_degs = 1`. The nonzero call reflects CHP1's obligate biochemical
role in NHE1 maturation and its demonstrated neuronal axon phenotype. The count
is held to one, close to the `Slc9a7`/`Slc9a9` focal counts and below the
`Ppp3ca`/`Ppp3r1` counts, because the direct `Slc9a1` analog is missing, the
strong external phenotype is axonal/cerebellar and may be survivor-conditioned
in this snRNA assay, and the pH-homeostasis training perturbations are mostly
FDR-flat in `151 TH Prkcd Grin2c Glut`.

## Limits

The largest uncertainty is the absent `Slc9a1` training perturbation: direct
NHE1 loss would have been a much cleaner comparator for `Chp1` than
endomembrane `Slc9a7`/`Slc9a9`. The parquet does not contain raw expression,
guide-specific editing rates, cell abundances before sorting, axon-terminal
localization, glycosylation, pH, or calcium imaging, so a predicted value near
zero is only a prediction of the FDR<0.05 nuclear DEG count in surviving focal
neurons. It should not be read as evidence that CHP1/NHE1 is biologically
irrelevant. I also did not transfer the Purkinje-cell degeneration phenotype as
a same-outcome prior because the requested population is a thalamic
glutamatergic class, the perturbation is acute mosaic P16 CRISPR, and the
observed endpoint is recovered-cell nuclear RNA rather than axon survival.
