# Question

Predict the number of genes that would pass `pvals_adj < 0.05` after CRISPR-Cas9 loss of `Minpp1` in `151 TH Prkcd Grin2c Glut` neurons.  The `Minpp1` perturbation was held out entirely, so I treated the observed 151-cell-group counts for non-held-out perturbations and focal expression-profile comparisons among mechanistic neighbors as calibration data, then used public MINPP1 biology only to decide which training genes were meaningful analogs or counterexamples.

There was only one requested target in `[local file: 137_Minpp1.csv]`.

# Sources used

- Focal training endpoint: `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
- Differential-expression profiles: `[local file: training_de_all_cell_groups.parquet]`.
- Same-experiment internal summaries from the Distributed Agents corpus, release `perturbai-july-260713-sourceguard-1773-v1`.  I queried `Minpp1`, `Inpp5k`, `Ocrl`, and `Synj1`.  The corpus had no `Minpp1` Claim or Finding, but it did contain same-experiment Findings for the phosphoinositide/endocytic comparators.
- PubMed literature:
  - Chi et al. 2000, Mol Cell Biol, PMID 10938126, DOI `10.1128/MCB.20.17.6496-6507.2000`: Minpp1 is an ER-luminal multiple inositol polyphosphate phosphatase; Minpp1-null mouse embryonic fibroblasts accumulate InsP5 and InsP6 by 30-45%, while Minpp1-null mice were viable and fertile without obvious gross defects.
  - Choi et al. 2007, J Biol Chem, PMID 17702752, DOI `10.1074/jbc.M704655200`: mammalian PPIP5K enzymes, including PPIP5K2, synthesize bisdiphosphoinositol tetrakisphosphate / inositol pyrophosphates from PP-InsP5.
  - Ucuncu et al. 2020, Nat Commun, PMID 33257696, DOI `10.1038/s41467-020-19919-y`: human MINPP1 loss of function causes a pontocerebellar hypoplasia syndrome and MINPP1-deficient cells, including differentiating neurons, accumulate inositol hexakisphosphate.

# Computation over the training data

I used the count CSV to calibrate the focal endpoint distribution and to read the exact `151 TH Prkcd Grin2c Glut` `n_degs` for candidate analogs.  This focal readout is very sparse: 1,205 of 1,674 training perturbations have zero DEGs, the median is 0, only 193 have at least 2 DEGs, and the 75th percentile is 1 DEG.  Large responses are mostly produced by core proteostasis, splicing, trafficking, and transcriptional regulators such as `Uba5`, `Tpr`, `Sin3a`, `Rnpc3`, `Zbtb7a`, and proteasome genes.

To test candidate pathway analogs beyond the scalar counts, I compared their full signed log2-fold-change vectors from the parquet after filtering to `group_name == "151 TH Prkcd Grin2c Glut"`.  The Distributed Agents runtime comparison computed vectors over 17,259 measured genes for each selected non-held-out perturbation, counted FDR-significant positive and negative genes, and computed pairwise Pearson, Spearman, cosine, and top-tail overlap statistics.  I ran this on a curated inositol-phosphate/phosphoinositide cohort:

`Ppip5k2`, `Inpp5k`, `Ocrl`, `Pi4kb`, `Pitpna`, `Pitpnm3`, `Plcb1`, `Synj1`, `Mtor`, `Tsc2`, `Pik3cb`, `Pik3r1`, `Pik3r2`, and `Itpr1`.

The direct high-phosphate inositol comparator was `Ppip5k2`, with 0 significant focal genes.  Among 14 selected PI/inositol/PI3K-mTOR-adjacent genes, 9 had no significant focal DEGs, 3 had 1-9, only `Pitpna` reached 21, and only `Tsc2` exceeded 50.  `Ppip5k2`, `Inpp5k`, and `Ocrl` were all FDR-flat in the focal cell group; their pairwise full-vector Pearson correlations were moderate and uninformative in the way expected for low-amplitude profiles (`Ppip5k2` vs `Inpp5k` r = 0.682; `Ppip5k2` vs `Ocrl` r = 0.684), with no shared significant genes because none existed.

# Target-specific reasoning

## Minpp1

`Minpp1` encodes an ER-luminal phosphatase that removes phosphates from highly phosphorylated soluble inositols such as InsP5 and InsP6.  It is mechanistically closer to soluble inositol polyphosphate and inositol pyrophosphate metabolism than to a membrane PI(4,5)P2 5-phosphatase.  The cleanest represented neighbor in the training panel was therefore `Ppip5k2`, an inositol pyrophosphate kinase, and `Ppip5k2` had 0 DEGs in the focal cell group.

The key focal training counts around this biology were:

| training perturbation | `n_degs` in `151 TH Prkcd Grin2c Glut` | interpretation |
| --- | ---: | --- |
| `Ppip5k2` | 0 | closest assayed high-phosphate inositol-pyrophosphate enzyme; supports no detectable Minpp1-like secondary RNA state |
| `Inpp5k` | 0 | ER-associated PI phosphatase and membrane/ER-contact comparator; same-experiment corpus reports no downstream FDR response across measured neuronal groups |
| `Ocrl` | 0 | PI(4,5)P2 5-phosphatase/endocytic comparator; corpus reports a pan-measured neuronal transcriptional null rather than a Lowe-like state |
| `Synj1` | 1 | synaptic PI(4,5)P2 phosphatase; essentially floor in the focal endpoint and corpus reports no broad neuronal nuclear module |
| `Pi4kb` | 1 | PI4P kinase and PI-turnover comparator; singleton focal response |
| `Pitpna` | 21 | PI-transfer protein; shows that some PI-transfer perturbations can barely rise above the assay floor, but its biology is membrane PI supply rather than soluble InsP6 hydrolysis |
| `Pitpnm3` | 0 | PI-transfer/contact-site comparator |
| `Plcb1` | 0 | PLC/IP3 production comparator |
| `Itpr1` | 0 | ER IP3 receptor / calcium-release comparator |
| `Pik3cb`, `Pik3r1`, `Pik3r2` | 0, 0, 0 | PI3K comparators all at the focal floor |
| `Mtor` | 2 | downstream growth/autophagy regulator with only singleton-scale focal activity |
| `Tsc2` | 86 | positive PI3K/mTOR boundary case, not a direct Minpp1 analog; TSC2 loss derepresses mTORC1 and is expected to have a broader growth/lysosome program |
| `Rab7` | 501 | positive lysosome boundary case showing the dataset can detect an endolysosomal program when the perturbation strongly reaches that axis |
| `Becn1`, `Atg5`, `Vps41` | 0, 0, 0 | autophagy/endolysosomal counterexamples that do not support a generic lysosome response for every adjacent gene |

The Distributed Agents corpus evidence around `Inpp5k`, `Ocrl`, and `Synj1` made the zero call more credible.  In release `perturbai-july-260713-sourceguard-1773-v1`, the synthesized Claim involving `Inpp5k`, `Ocrl`, and `Synj1` states that represented membrane-associated phosphoinositide and endocytic perturbations do not produce an interchangeable neuronal transcriptional module in this assay.  The underlying Findings reported that acute `Inpp5k` and `Ocrl` perturbation were broadly FDR-flat in measured neuronal groups, and that `Synj1` and `Dnm1` showed vesicle-endocytosis nulls at the basal snRNA-seq level despite strong physiological genetics.  That is not a direct MINPP1 fact, but it is useful same-experiment evidence that loss of a local phosphoinositide or inositol-phosphate enzyme often remains buffered from a juvenile neuronal nuclear RNA response.

The positive external facts on `Minpp1` do not overcome that in-dataset floor for this endpoint.  Complete MINPP1 deficiency can matter in neural development: Ucuncu et al. found biallelic human MINPP1 loss in pontocerebellar hypoplasia and IP6 accumulation in mutant differentiating neurons.  At the same time, Chi et al. showed that constitutive Minpp1 deletion in mice increased InsP5/InsP6 in fibroblasts yet produced viable, fertile animals without an obvious baseline gross phenotype, implying that MINPP1 loss can be metabolically buffered in vivo.  The Perturb-seq setting is even less likely to force a large compensatory state than a complete null: sparse P16 AAV CRISPR in postmitotic neurons, roughly 18% average mRNA knockdown per guide, a 3-4 week readout, and a nuclear RNA endpoint that will miss IP6 accumulation, cation chelation, ER-local metabolite flux, calcium transients, synaptic physiology, and protein-level compensation.

Putting those together, I predict that `Minpp1` will behave like `Ppip5k2`/`Inpp5k`/`Ocrl`/`Plcb1` rather than like `Tsc2` or `Rab7`: any biochemical perturbation should stay below the FDR 0.05 DEG threshold in `151 TH Prkcd Grin2c Glut`.

Predicted `Minpp1` count: 0.

# Limits

The strongest limitation is that direct soluble InsP pathway peers were mostly absent from the training panel: `Ipmk`, `Itpk1`, `Itpkb`, `Itpkc`, and `Ip6k1/2/3` were not in the focal training-count CSV, and the held-out `Minpp1` expression signature was unavailable by design.  `Ppip5k2` is in the same high-phosphate inositol space, but it is a kinase for pyrophosphate species rather than an ER-luminal InsP5/InsP6 phosphatase.  The `Inpp5k`/`Ocrl`/`Synj1` comparisons are therefore pathway-boundary evidence, not true paralog evidence.

The prediction also extrapolates from loss-of-function of one gene in young postmitotic neurons to a cell type that may or may not express enough MINPP1 substrate flux to respond.  Public MINPP1 disease data are developmental and often complete-loss settings; this experiment is acute, mosaic, partial, and transcriptional.  A positive Minpp1 response would be plausible if `151 TH Prkcd Grin2c Glut` neurons were uniquely sensitive to IP6/cation imbalance, but the non-held-out PI and inositol-phosphate perturbations make a detectable FDR-significant response less likely than the zero floor.
