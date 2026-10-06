# Rrn3 held-out DEG-count prediction

## Question and endpoint

I interpreted the task as a point prediction for the number of genes that would
pass Benjamini-Hochberg-adjusted Wilcoxon `pvals_adj < 0.05` after acute
`Rrn3` loss of function in recovered `151 TH Prkcd Grin2c Glut` nuclei.  The
requested output is not a rank and not a general essentiality score: `n_degs` is
an assay- and power-dependent count of polyadenylated nuclear RNA changes in one
postnatal thalamic glutamatergic class.

The held-out `Rrn3` endpoint was absent from the declared inputs.  The
training-count CSV provided the directly observed endpoint for visible
perturbations; the full differential-expression Parquet provided the same
experiment's per-gene Wilcoxon rows for those visible perturbations; the July
PerturbAI same-experiment corpus provided packaged interpretations for visible
analogs only; and PubMed supplied external mechanism priors for RRN3/TIF-IA,
Pol I initiation, and nucleolar stress.

## Quantitative dataset work

I first inspected the training focal-class count table.  It contained 1,674
non-held-out biological targets.  The focal endpoint distribution was highly
zero-inflated: 469/1,674 visible targets had `n_degs > 0`, the median was 0, the
75th percentile was 1, the 90th percentile was 2, and the 95th percentile was
18.  Thus a perturbation needs target-specific evidence to be moved away from
zero or the single-digit boundary.

I then ran the declared `dataset.perturbseq_features summarize` capability over
`training_de_all_cell_groups.parquet`; it read the 616,253,184 declared DE rows
and wrote one row per visible target to `workbench/features.parquet`.  Its
nested calibration mode requires a ranked or partially ranked supervision set,
which this task does not provide, so it failed with
`task bindings contain no active ranked or partial-ranked gene set`.  I used the
training `n_degs` values as the direct endpoint rather than replacing them with
a graph score or an unsupported learned rank.

For the focal class, I filtered the Parquet to biologically relevant visible
analogs and checked the minimum adjusted p-value and leading signed Wilcoxon
rows:

```python
pq.read_table(
    parquet_path,
    columns=["names", "scores", "logfoldchanges", "pvals_adj",
             "group_name", "gene_target"],
    filters=[
        ("group_name", "==", "151 TH Prkcd Grin2c Glut"),
        ("gene_target", "in", targets),
    ],
)
```

The visible counts that were most informative for `Rrn3` were:

| training target | role as analog or counterexample | focal `n_degs` | relevant focal DE pattern |
|---|---|---:|---|
| `Taf1b` | closest Pol I initiation neighbor: SL1/TIF-IB subunit that works with TIF-IA/RRN3 at the rDNA promoter | 0 | no FDR-significant gene; all 17,259 focal measured genes had `pvals_adj = 1`; maximum absolute Wilcoxon score 3.897 |
| `Nop56` | core box C/D snoRNP / pre-rRNA-processing factor; shows that some nucleolar ribosome-biogenesis perturbations are detectable in the focal class | 25 | mostly down RNA-processing/SR-splicing branch headed by `Rsrp1`, `Ddx17`, `Srsf5`, `Srsf11`, `Tcea2`, `Ddx5`, with `Snu13` induction |
| `Rbm28` | 60S assembly / rRNA-processing factor; ribosomopathy-linked counterexample | 0 | no focal FDR gene; minimum `pvals_adj = 0.543` |
| `Las1l` | 60S ITS2 processing factor; ribosome-biogenesis counterexample | 0 | no focal FDR gene; all focal adjusted p-values were 1 |
| `Polr3b` | related small-RNA polymerase machinery, not Pol I | 8 | small but nonzero focal response |
| `Myc`, `Mycn` | upstream growth-coupled Pol I/ribosome-biogenesis activators | 0, 0 | no focal DEGs |
| `Trp53` | canonical downstream nucleolar-stress effector, but opposite causal intervention | 0 | no focal DEGs; no basal p53 transcript program |

The target-wide cached features were consistent with the focal counts:
`Taf1b`, `Rbm28`, `Las1l`, and `Trp53` had zero FDR<0.05 rows across their
measured neuronal surfaces, whereas `Nop56` had only 31 FDR<0.05 rows across all
23 cell groups.

## Mechanistic transfer

`Rrn3` encodes TIF-IA, the mammalian homolog of yeast Rrn3p and a Pol
I-specific initiation factor.  TIF-IA associates with the initiation-competent
fraction of RNA polymerase I and bridges Pol I to the SL1/TIF-IB initiation
complex at rDNA promoters (Bodem et al. 2000, DOI:10.1093/embo-reports/kvd032;
Yuan et al. 2002, DOI:10.1093/embo-reports/kvf212).  TIF-IA is also a
growth- and stress-regulated Pol I control point: mTOR, ERK/RSK, CK2, and JNK
phosphorylation modulate TIF-IA activity and Pol I transcription
(Mayer et al. 2004, DOI:10.1101/gad.285504; Zhao et al. 2003,
DOI:10.1016/s1097-2765(03)00036-4; Mayer et al. 2005,
DOI:10.1101/gad.333205; Bierhoff et al. 2008, DOI:10.1128/MCB.00492-08).
Complete neural or medium-spiny-neuron TIF-IA ablation disrupts nucleolar
function and engages a protracted p53/PTEN-associated neurodegenerative
response in mice (Parlato et al. 2008, DOI:10.1523/JNEUROSCI.2439-08.2008;
Kreiner et al. 2013, DOI:10.1038/cdd.2013.66).  More generally, ribosome
biogenesis defects can signal through the ribosomal-protein/5S-RNP-MDM2-p53
axis (Sloan et al. 2013, DOI:10.1016/j.celrep.2013.08.049).

The causal chain I used was therefore:

`Rrn3` CRISPR loss -> reduced functional TIF-IA/Pol I initiation at rDNA ->
nucleolar/rRNA-biogenesis stress if the perturbation exceeds buffering ->
possible p53, ISR/UPR, snoRNP, or RNA-processing propagation ->
survival and recovery of edited juvenile neurons after 3-4 weeks ->
polyadenylated snRNA-seq DEGs among recovered `151 TH Prkcd Grin2c Glut` nuclei.

At the direct molecular-consequence step, `Taf1b` is the strongest within-
dataset same-outcome prior because TAF1B/TAFI68 is in the SL1/TIF-IB complex
that TIF-IA contacts to assemble Pol I initiation complexes.  The experiment
found `Taf1b` mRNA-transcriptionally flat in `151 TH Prkcd Grin2c Glut` and in
the other recovered neuronal groups, and the July PerturbAI corpus specifically
records absence of p53, unfolded-protein, and integrated-stress sentinel mRNA
induction after `Taf1b` perturbation.  This is endpoint-bearing same-experiment
evidence against a broad recovered-cell polyadenylated response to partial Pol I
initiation impairment.

`Nop56` is the main counterexample: it is not a Pol I initiation factor, but a
core box C/D snoRNP/pre-rRNA-processing perturbation, and it did produce 25
focal DEGs.  That keeps a small nonzero `Rrn3` response plausible.  However,
the Nop56 signature was selective and factor-specific rather than a generic
nucleolar-stress program: the same-experiment report found no canonical p53,
ISR, UPR, or autophagy transcriptional induction, and `Rbm28` and `Las1l`, two
other visible large-subunit/rRNA-processing factors, were FDR-null across the
postnatal neuronal surface.  Thus broad ribosome-biogenesis membership alone
does not transfer the 25-DEG `Nop56` state to `Rrn3`.

Downstream p53 signaling also does not force a positive prediction.  `Trp53`
loss is the opposite intervention from nucleolar-stress activation, and the
visible `Trp53` knockout being flat only says basal recovered neurons were not
in a p53-driven transcriptome.  The useful part is the negative stress-sentinel
context from `Taf1b`, `Las1l`, and `Nop56`: if the surviving cells had mounted a
large Cdkn1a/Mdm2/Bax/Bbc3 or ATF4/UPR mRNA program, the assay should have been
able to see it.

## Prediction

I therefore treated `Rrn3` as closest to the `Taf1b` Pol I-initiation null, with
`Nop56` setting an upper boundary for a modest ribosome-biogenesis response and
`Rbm28`/`Las1l` showing that the default focal answer for nucleolar assembly
factors can still be zero.  The direct external mechanism says `Rrn3` is
important for rRNA transcription; the within-dataset endpoint evidence says
this juvenile mosaic snRNA-seq assay often does not convert that primary
nucleolar lesion into FDR-significant polyadenylated mRNA changes in recovered
neurons.  My integer point prediction is:

| held-out target | predicted `n_degs` | rationale |
|---|---:|---|
| `Rrn3` | 0 | Pol I initiation factor; closest visible initiation analog `Taf1b` was focal- and atlas-wide FDR-null; rRNA-processing factors were mixed and at most modest in 151 TH, making nonzero possible but less likely than the zero-inflated direct endpoint baseline |

## Limits

The largest uncertainty is missing same-complex coverage: no visible focal
training target was another core RRN3/Pol I enzyme subunit such as `Polr1a` or
`Polr1b`.  `Taf1b` is initiation-proximal but not identical to RRN3, and the
AAV-CRISPR perturbation can leave residual protein that differs by target
half-life and guide efficacy.  The Parquet measures polyadenylated nuclear RNA,
not 47S pre-rRNA synthesis, rRNA processing intermediates, ribosome production,
protein synthesis, nucleolar morphology, or pre-assay loss of edited neurons.
The zero prediction should therefore be read narrowly as "no measured mRNA is
expected to pass FDR 0.05 among recovered `151 TH Prkcd Grin2c Glut` nuclei",
not as evidence that RRN3 is dispensable for Pol I transcription.
