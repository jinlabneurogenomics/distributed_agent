# Held-out DEG-count prediction trace

## Question and endpoint

The requested prediction is the integer number of measured genes with
Benjamini-Hochberg adjusted Wilcoxon `pvals_adj < 0.05` after acute mosaic
CRISPR loss of each held-out target in `151 TH Prkcd Grin2c Glut` nuclei.  The
held-out target file contains one target:

```tsv
target_name
Exoc6b
```

I treated `n_degs` as the assay-specific count of FDR-significant rows in the
focal-cell differential-expression surface, including the target transcript if
it became FDR-significant.  I did not interpret target-transcript loss as a
direct measure of editing efficiency, because the dataset context states that
self knockdown is not quantitatively coupled to downstream transcriptional
effect in this screen.  `151 TH Prkcd Grin2c Glut` was interpreted as the exact
Allen-taxonomy thalamic glutamatergic class named in the task.

## Sources used

- Declared endpoint table:
  `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
- Declared differential-expression table:
  `training differential-expression dataset`.
- Run-local requested-target manifest:
  `single-target request for Exoc6b`.
- PerturbAI July 260713 SourceGuard same-experiment corpus, especially the
  Rala report and Findings ledger.  This is the packaged interpretation layer
  over the same Perturb-seq experiment, not independent replication.
- PubMed and primary/review literature for the exocyst/Ral relationship:
  Hsu et al. 2004, DOI `10.1016/S0074-7696(04)33006-8`; Lalli 2009, DOI
  `10.1242/jcs.044339`; Das et al. 2013, DOI `10.1242/jcs.145037`;
  Simsek-Kiper et al. 2022, DOI `10.1002/humu.24478`.

The requested output is not a ranked gene list and there is no ranked or
partially ranked supervision.  I therefore did not run the Perturb-seq ranking
workbench, predictive graph review, or ordering validation capabilities.

## Quantitative work over the declared inputs

1. I loaded the training count CSV and checked the distribution of observed
   `n_degs` in the focal cell group: 1,674 non-held-out perturbations, median
   0, 75th percentile 1, 90th percentile 2, mean 14.1, and max 2,677.  Thus the
   empirical prior for an arbitrary held-out target in this cell group is a
   corrected-null or near-null response.
2. I searched the training count table for exocyst subunits and nearby vesicle
   or small-GTPase targets.  No `Exoc1`, `Exoc2`, `Exoc3`, `Exoc4`, `Exoc5`,
   `Exoc6`, `Exoc6b`, `Exoc7`, or `Exoc8` perturbation was represented in the
   training set, so there was no same-complex perturbation with a measured
   focal-cell count.
3. I queried the focal-cell Parquet rows for the represented analogs
   `Rala`, `Hras`, `Kras`, `Rac1`, `Cdc42`, `Rapgef2`, `Rapgef4`,
   `Cplx1`, `Cplx2`, `Stxbp1`, `Stx1b`, `Unc13a`, `Unc13b`,
   `Unc13c`, `Syt2`, `Syt14`, `Vamp1`, `Rab27a`, `Rab3gap1`,
   `Rab3gap2`, `Cadps2`, `Dnm1`, `Syp`, `Dnajc5`, `Pclo`, `Bsn`,
   `Kif1a`, `Kif1b`, `Kif5a`, `Kif5c`, `Madd`, `Reps1`,
   `Sec23a`, `Sec63`, `Rab18`, and `Rab7`.  For each target I counted
   FDR<0.05 rows, FDR<0.10 rows, and the lowest adjusted-p rows in
   `151 TH Prkcd Grin2c Glut`; I also correlated signed Wilcoxon-score vectors
   among these perturbations to check whether any weak individual analog hid a
   common focal-cell expression pattern.

The exact focal-cell training counts most relevant to `Exoc6b` were:

```tsv
target_name	n_degs	focal-cell interpretation
Rala	0	no FDR<0.05 or FDR<0.10 genes; 199 perturbed nuclei vs 23679 controls; best downstream FDR 0.975
Cdc42	1	only the Cdc42 self transcript reached FDR<0.05
Hras	0	no corrected genes
Kras	0	no corrected genes
Rac1	0	no corrected genes
Rapgef2	0	no corrected genes
Rapgef4	0	no corrected genes
Rab27a	0	no corrected genes
Rab3gap1	0	no corrected genes
Rab3gap2	0	no corrected genes
Unc13a	0	no corrected genes; target transcript had FDR 0.666
Unc13b	0	no corrected genes
Unc13c	0	no corrected genes
Cplx1	1	only the Cplx1 self transcript reached FDR<0.05
Cplx2	0	no corrected genes
Stxbp1	1	only the Stxbp1 self transcript reached FDR<0.05
Stx1b	0	no corrected genes
Vamp1	1	only the Vamp1 self transcript reached FDR<0.05
Syt2	0	no corrected genes
Cadps2	0	no corrected genes
Pclo	0	active-zone scaffold, no corrected genes
Bsn	0	active-zone scaffold, no corrected genes
Madd	0	Rab3 activator, no corrected genes
Reps1	0	Ralbp1/RalA exocytosis module, no corrected genes
Sec23a	0	COPII trafficking, no corrected genes
Sec63	11	ER translocation/UPR-like signal; a trafficking counterexample, not an exocyst analog
Rab7	501	endolysosomal stress response; a Rab-family counterexample, not a secretory exocyst analog
```

These counts were rechecked directly in the Parquet for the focal group.  The
nearest pathway analog, `Rala`, had seven nominal `p < 0.001` rows among 17,259
tested genes and no FDR<0.10 row.  Its focal-cell score vector was essentially
uncorrelated with nearby small GTPases and synaptic-vesicle perturbations:
`r = 0.0085` versus `Stxbp1`, `r = 0.0037` versus `Unc13a`,
`r = -0.0114` versus `Cplx2`.  The strongest lysosomal counterexample in this
set, `Rab7`, had 501 focal DEGs and was visibly a different state: its top
genes included lysosomal or stress-associated `Atp6v1b2`, `Ptgds`, `Dpp7`,
`Scpep1`, and `Dusp1`.

The same-experiment Rala report added two useful checks over the all-cell
surface.  First, `Rala` was downstream-null at FDR<0.10 in every one of its 22
measured neuronal classes, with the 151 focal group specifically at 199
perturbed cells, 23,679 controls, 17,259 genes, and 0 downstream FDR<0.10 genes.
Second, the report tested canonical RalA effector and exocyst sentinel
transcripts, including `Exoc1`, `Exoc2`, `Exoc3`, `Exoc4`, `Exoc5`, `Exoc6`,
`Exoc6b`, `Exoc7`, and `Exoc8`, and found minimum BH FDR 1.0 across all
Rala-measured groups.  The report also explicitly recorded that exact
exocyst-complex targets were absent as `gene_target` entries in the visible
Parquet universe, which prevents a direct same-complex calibration.

## Exoc6b-specific reasoning

`Exoc6b` encodes an EXOC6/Sec15-family component of the octameric exocyst
complex.  The exocyst tethers post-Golgi secretory vesicles at polarized plasma
membrane sites before membrane fusion, and canonical subunits include Sec3,
Sec5, Sec6, Sec8, Sec10, Sec15, Exo70, and Exo84 (Hsu et al. 2004).  In neurons,
RalA recruits or regulates the exocyst during axon specification, Par-complex
polarity, and activity-dependent postsynaptic membrane growth; RalA depletion
or exocyst-subunit depletion can disrupt these morphology programs in cultured
or developing neuronal systems (Lalli 2009; Das et al. 2013).  Biallelic human
`EXOC6B` loss causes spondylo-epi-metaphyseal dysplasia with joint laxity type 3
and patient fibroblasts show impaired exocytosis/primary ciliogenesis
(Simsek-Kiper et al. 2022).

That external evidence says the gene is a real exocyst component, but it does
not by itself predict a large 3-to-4-week soma-wide snRNA response in sparse
postmitotic thalamic glutamatergic neurons.  The strongest same-experiment
causal chain available here is:

```text
Exoc6b CRISPR LoF -> weaker Sec15/exocyst vesicle tethering
  -> altered secretory or membrane-addition traffic
  -> possible synaptic, ciliary, or polarity changes
  -> only if persistent in recovered postnatal neurons, secondary nuclear RNA
     remodeling detectable by Wilcoxon FDR in 151 TH Prkcd Grin2c Glut
```

The dataset argues that the last two steps are weak in this context.  `Rala`
is not an obligate subunit, so its focal-cell null does not prove that
`Exoc6b` will be null, but it is the represented perturbation nearest to the
Ral/exocyst node and it produced zero corrected genes, including no feedback
on the mRNAs of exocyst sentinel genes.  The more direct synaptic-vesicle
docking, priming, fusion, active-zone, and Rab3-axis perturbations were also
corrected-null or self-transcript-only in the requested cell group.  By
contrast, `Sec63` and `Rab7` show that the cell group can generate nonzero
trafficking-associated counts when the perturbation produces ER stress or
endolysosomal remodeling, but those mechanisms are not specific predictions of
an acute partial `Exoc6b` loss.

I therefore predict `Exoc6b` to be in the dominant corrected-null class rather
than in the small set of broad focal responders.  I also did not add one DEG
for the target transcript: observed self-transcript FDR is gene- and
guide-dependent in this assay, and the closest functional analogs frequently
lost only their own RNA while the nearest Ral/exocyst analog `Rala` was fully
corrected-null in this focal group.

Final point prediction:

```tsv
target_name	predicted_n_degs
Exoc6b	0
```

## Limits

The main limitation is that no `Exoc*` subunit perturbation was present in the
training data, so `Exoc6b` is extrapolated from `Rala`, small-GTPase inputs, and
synaptic-vesicle machinery rather than from an obligate exocyst member.  RalA
is an upstream regulator with redundant and context-dependent effectors, not
the same intervention as removing a Sec15 subunit.  The external `EXOC6B`
disease and ciliogenesis evidence is mostly developmental, skeletal, or
fibroblast evidence, while the requested assay is sparse P16 CRISPR in
postmitotic neurons assayed at P37-P44.  A local non-transcriptional axonal,
synaptic, secretory, or ciliary phenotype could therefore be missed by
single-nucleus RNA counts from recovered nuclei.  Finally, a zero point
prediction should be read as "no measured gene passes BH FDR 0.05 in this
assay", not as absence of functional exocyst biology.
