# DEG-count prediction for `151 TH Prkcd Grin2c Glut`

## Question and endpoint

The requested prediction is the integer number of genes expected to pass
`pvals_adj < 0.05` after an acute AAV-PHP.eB, sparse CRISPR-Cas9
loss-of-function perturbation in recovered `151 TH Prkcd Grin2c Glut`
postmitotic mouse neurons.  I interpreted the target list literally and found
one held-out target:

| target | requested order |
| --- | ---: |
| `Fth1` | 1 |

`Fth1` is absent from the focal-cell training count CSV and was held out as a
`gene_target` from the differential-expression Parquet.  The count to predict is
therefore absent from the declared inputs and must be transferred from
non-held-out perturbations.  I treated the Parquet and the July
`perturbai-july-260713-sourceguard-1773-v1` same-experiment corpus as two
representations of the same screen, not independent replication.

## Sources used

- Declared focal-cell training counts:
  `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`
- Declared differential-expression table:
  `training differential-expression dataset`
- Run-local requested-target manifest:
  `single-target request for Fth1`
- Run-local task bindings, measurement registry, coverage, and capability
  manifest under `codex_runtime/pipeline/`
- Internal same-experiment corpus:
  `perturbai-july-260713-sourceguard-1773-v1`, queried through the declared
  `corpus.findings` capability
- External literature:
  Harrison and Arosio 1996, DOI `10.1016/0005-2728(96)00022-9`, PMID
  `8695634`; Rouault 2006, DOI `10.1038/nchembio807`, PMID `16850017`;
  Meyron-Holtz, Ghosh and Rouault 2004, DOI `10.1126/science.1103786`, PMID
  `15604406`; Mancias et al. 2014, DOI `10.1038/nature13148`, PMID
  `24695223`; Chen et al. 2015, DOI `10.1074/jbc.M115.680090`, PMID
  `26400084`; Hambright et al. 2017, DOI `10.1016/j.redox.2017.01.021`, PMID
  `28212525`.

## Computations over the declared dataset

The training-count file has 1,674 non-held-out biological perturbations.  It is
very sparse in the focal thalamic class: median `n_degs = 0`, the 75th
percentile is 1, the 90th percentile is 2, and only the top 5% of perturbations
have at least 18 DEGs.

I selected training perturbations that test FTH1's immediate neighborhood:

- `Ireb2` and `Tfrc` for IRP/IRE control and transferrin iron uptake.
- `Gpx4` and `Acsl4` for iron-dependent lipid-peroxidation/ferroptosis biology.
- `Atg5`, `Atg16l1`, `Becn1`, and `Map1lc3a` for ferritinophagy/autophagy.
- `Aco2`, `Nfs1`, and `Hif1a` as mitochondrial iron-sulfur or iron/HIF stress
  counterexamples.

For these perturbations I filtered the Parquet to
`group_name == "151 TH Prkcd Grin2c Glut"` and counted rows with
`pvals_adj < 0.05`; each target had 17,259 measured genes in this cell group.
I also extracted the focal-cell rows for a hand-curated iron and stress sentinel
set: `Fth1`, `Tfrc`, `Ireb2`, `Aco1`, `Slc11a2`, `Slc40a1`, `Ncoa4`, `Hif1a`,
`Hmox1`, `Fdx1`, `Fxn`, `Glrx5`, `Steap3`, `Gpx4`, `Slc7a11`, `Slc3a2`,
`Nfe2l2`, `Atf4`, and `Ddit3`.

### Focal-cell analog counts

| training perturbation | mechanistic relationship to `Fth1` | focal `n_degs` |
| --- | --- | ---: |
| `Tfrc` | transferrin-bound iron import; upstream of labile iron supply | 0 |
| `Ireb2` | IRP regulator of ferritin and TFRC IRE-containing mRNAs | 1 |
| `Gpx4` | detoxifies phospholipid hydroperoxides in ferroptosis | 0 |
| `Acsl4` | generates PUFA-CoA substrates that sensitize to ferroptosis | 1 |
| `Atg5` | core autophagy lipidation machinery, required upstream of ferritinophagy | 0 |
| `Atg16l1` | ATG12-ATG5-ATG16L1 lipidation complex partner | 0 |
| `Becn1` | PI3KC3/autophagy initiation and endosomal scaffold | 0 |
| `Map1lc3a` | LC3/ATG8 autophagosome effector | 1 |
| `Hif1a` | hypoxic/pseudohypoxic iron-stress transcription factor | 0 |
| `Nfs1` | mitochondrial Fe-S cluster biogenesis | 0 |
| `Aco2` | mitochondrial aconitase, Fe-S enzyme | 0 |

In the focal-cell sentinel extraction, neither the iron-homeostasis genes
(`Fth1`, `Tfrc`, `Ireb2`, `Aco1`, `Slc11a2`, `Slc40a1`, `Ncoa4`) nor the stress
genes (`Hif1a`, `Hmox1`, `Nfe2l2`, `Atf4`, `Ddit3`, `Slc7a11`) passed FDR 0.05
after any of `Tfrc`, `Ireb2`, `Gpx4`, `Atg5`, `Atg16l1`, `Becn1`, `Map1lc3a`,
`Nfs1`, or `Aco2`.  The only focal-cell FDR hit among the direct iron uptake
and regulatory comparators was `Abhd12b` after `Ireb2` perturbation; for `Tfrc`,
`Pfkp` was the top expected thalamic stress/glycolysis fragment but it was just
below this task's cutoff (`pvals_adj = 0.0523`) and the training endpoint is
therefore `n_degs = 0`.

The across-cell-group check gave the same qualitative result.  `Tfrc` had only
two FDR 0.05 singleton groups outside the focal class, `Ireb2` had only the one
focal hit, `Gpx4` had no FDR 0.05 hit anywhere, `Atg5` and `Becn1` had their
small responses in `155 MB Glut`, and `Aco2`/`Nfs1` were flat or nearly flat.

## Same-experiment corpus evidence

The July internal corpus packages the same experiment's report-level
interpretation:

- `Ireb2` produced only a single robust downstream event in the focal cell type,
  down-regulation of `Abhd12b`, and the report explicitly found no corrected
  canonical iron-homeostatic or iron-stress mRNA changes including `Tfrc`,
  `Fth1`, `Aco1`, `Slc11a2`, `Slc40a1`, `Ncoa4`, `Hif1a`, `Hmox1`, `Fdx1`,
  `Fxn`, `Glrx5`, and `Steap3` across all measured `Ireb2` cell groups.  This
  argues that acute partial IRP2 loss is not a broad ferritin/TFRC RNA phenotype
  in recovered juvenile neurons.
- `Tfrc` was the closest represented iron-uptake perturbation.  The packaged
  report found a punctate rather than global neuronal iron-starvation response:
  only five corrected downstream genes at FDR 0.10 across 21 measured neuronal
  groups, no broad IRP, ferritin, HIF, redox, or ferritinophagy program, and no
  phenocopy of `Ireb2`, `Hif1a`, `Abcb7`, or `Nfs1`.  In the focal class the
  only biologically interpretable trend was the near-threshold `Pfkp` increase.
- `Gpx4` was completely FDR-null in every recovered neuronal group and did not
  induce ferroptosis, NRF2/glutathione, iron-handling, or ATF4/CHOP/ISR
  sentinel transcripts.  The report warns that this does not prove successful
  GPX4 loss is safe, because a survivor-conditioned snRNA assay can miss early
  lethal ferroptosis.
- `Acsl4` did not phenocopy `Gpx4`, `Nfe2l2`, or `Tfrc`; its one robust cortical
  hit was a sterol-feedback signal rather than an iron or ferroptosis module.
- `Atg5`, `Becn1`, and `Map1lc3a` showed weak, restricted, or null
  transcriptional effects rather than canonical p62/ubiquitin, lysosome,
  GABARAP/LC3, NRF2, or UPR stress programs.  This makes it unlikely that a
  single ferritin subunit perturbation will trigger a larger
  ferritinophagy-linked nuclear mRNA response than the core autophagy factors
  themselves.

## Target-specific reasoning

### `Fth1`

`Fth1` encodes ferritin heavy chain.  Ferritin cages are 24-subunit
iron-storage assemblies; vertebrate ferritin uses heavy and light chains, with
the H chain carrying the ferroxidase activity that oxidizes Fe(II) during
storage and the L chain assisting core formation (Harrison and Arosio 1996).
Mammalian ferritin and the transferrin receptor are classically controlled
post-transcriptionally through iron-responsive elements and iron-regulatory
proteins; IRP binding represses ferritin translation while stabilizing `Tfrc`
mRNA under iron limitation (Rouault 2006; Meyron-Holtz, Ghosh and Rouault
2004).  Ferritin turnover is also controlled at the protein level through
NCOA4-mediated ferritinophagy, which delivers ferritin heavy and light chains to
lysosomes and changes bioavailable iron (Mancias et al. 2014).

Those mechanisms made `Ireb2` and `Tfrc` the closest available training tests.
Neither produced a broad mRNA response in the focal class: `Tfrc` had zero
FDR 0.05 DEGs, and `Ireb2` had one (`Abhd12b`) that was not an iron-storage,
transferrin, NRF2, HIF, or ISR effector.  The focal Parquet rows show all
canonical iron sentinel p-values adjusted to 1.0 for the `Ireb2` perturbation,
including `Fth1` itself, `Tfrc`, `Aco1`, `Ncoa4`, `Slc11a2`, `Slc40a1`, `Hif1a`,
`Hmox1`, `Glrx5`, and `Atf4`.  `Tfrc` generated a possible sub-FDR HIF/glycolysis
fragment, but even its nearest relevant focal marker, `Pfkp`, did not reach
this task's FDR 0.05 endpoint.

The ferroptosis and ferritinophagy counterexamples also point toward a zero.
Reducing FTH1 could raise labile iron and oxidative risk, but in this exact
screen `Gpx4` loss did not yield a recovered-cell lipid-peroxidation, NRF2,
glutathione, iron-handling, or ISR program despite GPX4 being an established
ferroptosis suppressor in neurons in stronger conditional models (Chen et al.
2015; Hambright et al. 2017).  `Atg5`, `Atg16l1`, `Becn1`, and `Map1lc3a`
likewise did not produce any focal-cell FDR 0.05 response resembling
ferritinophagy collapse.  Because the endpoint counts genes in recovered nuclei
3-4 weeks after partial mosaic CRISPR rather than measuring ferritin protein,
labile iron, lipid peroxidation, or pre-harvest survival, the expected direct
FTH1 biochemical lesion is only weakly coupled to a detectable nuclear DEG
burden.

My point prediction for `Fth1` is therefore `0`: a nonzero singleton is
possible, by analogy to `Ireb2`'s `Abhd12b` and the many one-gene perturbations
near the dataset noise boundary, but the best mechanistic analogs available in
the training set have `0` or `1` focal DEGs and do not share a coherent
iron-homeostasis expression state.

## Limits

- `Ftl1`, `Ncoa4`, `Slc11a2`, `Slc40a1`, `Ftmt`, and `Tfr2` were not available
  as training perturbations, so the closest ferritin-subunit and ferritinophagy
  perturbation tests were missing.
- The declared Parquet has no raw single-nucleus UMI counts, indel rates,
  guide-exposure denominators, ferritin protein, labile iron, or survival
  readouts.  A biochemical ferritin phenotype could therefore be present but
  invisible to the recovered-nucleus DEG count.
- External complete-knockout or conditional ferroptosis/autophagy phenotypes
  are stronger interventions than this sparse P16 CRISPR design.  I used them
  only to set mechanistic direction and as counterexamples, not to override the
  measured focal training analogs.
- The prediction is extrapolative because no within-dataset perturbation removes
  the 24-mer ferritin cage itself.  The best available evidence is that adjacent
  iron-uptake, IRP, autophagy, and ferroptosis perturbations were transcriptionally
  buffered in `151 TH Prkcd Grin2c Glut`.
