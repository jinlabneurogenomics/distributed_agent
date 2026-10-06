# Task interpretation

The held-out target list for this run contains a single perturbation:

```tsv
target_name
Dnm2
```

The requested quantity is the integer number of genes with `pvals_adj < 0.05`
in `151 TH Prkcd Grin2c Glut` after acute AAV CRISPR loss of the target gene. `Dnm2`
was absent from both supplied training files as a perturbation target, so I
treated `Dnm2` as an unseen target and used the non-held-out perturbations only
for calibration. A count of 1 can mean "the target transcript itself is
significantly reduced" with no separate downstream transcriptional response; the
focal training examples make that distinction important.

# Sources used

* Input DEG parquet:
  `[local file: training_de_all_cell_groups.parquet]`.
* Input focal training endpoint:
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
* Input held-out manifest:
  `[local file: 060_Dnm2.csv]`.
* Internal same-experiment corpus: Distributed Agents
  `perturbai-july-260713-sourceguard-1773-v1`, queried for curated findings and
  pathway records around `Dnm1`, `Synj1`, `Bin1`, `Cltc`, `Vps35`, and `Rab7`.
  The corpus did not contain a prebuilt `Dnm2` claim.
* Run-local profile tools over the supplied parquet. I used Wilcoxon `scores`
  over the 17,259 measured focal genes to compare the score-vector
  neighborhoods of observed endocytic perturbations.
* PubMed/literature and prior biological knowledge:
  * Ferguson and De Camilli 2012, DOI `10.1038/nrm3266`, PMID `22233676`: review
    of dynamin as a membrane-fission GTPase in clathrin-mediated endocytosis.
  * Raimondi et al. 2011, DOI `10.1016/j.neuron.2011.04.031`, PMID `21689597`:
    mouse `Dnm1` and `Dnm3` are the dominant brain dynamins and have overlapping
    presynaptic roles in activity-dependent synaptic-vesicle endocytosis, while
    low `Dnm2` can still support residual transmission in their absence.
  * Lee and De Camilli 2002, DOI `10.1073/pnas.012607799`, PMID `11782545`:
    dynamin 2 links membrane remodeling to actin at endocytic membranes.
  * Viplav et al. 2019, DOI `10.1242/jcs.226530`, PMID `30926623`: `DNM2`
    marks late clathrin-mediated endocytic sites in cultured cells.

# Computation over the focal training data

I first confirmed that the manifest contains only `Dnm2` and that neither the
DE parquet nor the focal count CSV has `Dnm2` as a training perturbation.

I then filtered the parquet to `group_name == "151 TH Prkcd Grin2c Glut"` and
counted, for each observed target, rows with `pvals_adj < 0.05`. This exactly
matches the supplied endpoint and yielded 1,205 zero-count targets out of 1,674;
the median count is 0, the 75th percentile is 1, and the 95th percentile is 18.
This focal response breadth is therefore very sparse except for a small number
of broad stress-like perturbations.

For the endocytic genes most relevant to `Dnm2`, I pulled their focal
significant rows directly from the parquet:

| training target | focal `n_degs` | significant focal rows and pattern |
|---|---:|---|
| `Dnm1` | 1 | only `Dnm1` itself, log2FC -0.712, FDR `4.09e-25` |
| `Synj1` | 1 | only `Synj1` itself, log2FC -0.583, FDR `3.11e-7` |
| `Bin1` | 1 | only `Bin1` itself, log2FC -0.331, FDR `2.89e-6` |
| `Cltc` | 3 | `Gabra4`, `Rbms1`, and `Ero1b` down, all at FDR 0.042 |
| `Vps35` | 17 | a small TH program including `Atp2a2` and `Grin2b` down, `Brsk1`, `Coch`, `Ptgds`, and `Ache` up |
| `Rab7` | 501 | a broad lysosomal/sterol/stress state, with `Atp6v1b2`, `Dpp7`, `Insig1`, `Atp6v0b`, `Lamp2`, and `Msmo1` up and `Atp2a2`/`Grin2b`/`Gabra4` down |

I also checked nearby represented targets. Most upstream or adjacent trafficking
genes had zero or nearly zero counts in the focal endpoint: `Cd2ap` 0, `Sorl1`
0, `Abca7` 0, `Psen1` 0, `Ocrl` 0, `Inpp5k` 0, `Vps41` 0, `Vps35l` 0, `Washc4`
0, `Atp6v1a` 0, `Atp6v1b2` 0, `Atp6v0a1` 1, `Atp6ap2` 2, `Htt` 3, and `Hspa8`
9. The larger endolysosomal and signaling responses, such as `Dctn1` 75 and
`Tsc2` 86, were mechanistically farther from the immediate dynamin-2 membrane
fission step.

The score-vector comparisons across all 17,259 measured focal genes showed that
the observed endocytic comparators are not a single expression module. Whole
profile cosine similarities were essentially background for the flat
synaptic-endocytic genes: `Dnm1` vs `Synj1` 0.018, `Dnm1` vs `Bin1` 0.053,
`Dnm1` vs `Cltc` 0.003, `Dnm1` vs `Rab7` 0.029, and `Synj1` vs `Rab7` -0.016.
`Cltc` and `Vps35` were modestly positive against `Rab7` because they share some
negative synaptic/excitability genes in this TH cell group, but even
`Cltc`-`Rab7` was only cosine 0.189 and `Vps35`-`Rab7` only 0.143. Thus, the
within-dataset expression evidence supported treating `Rab7` as a late
endosomal stress counterexample, not as a direct predictor for `Dnm2`.

# Target-specific reasoning for Dnm2

`Dnm2` encodes dynamin 2, a ubiquitously expressed mechanoenzyme that drives
membrane fission during clathrin-mediated endocytosis and interfaces with
actin-regulated membrane remodeling. The closest loss-of-function analog in the
training set is `Dnm1`, another dynamin GTPase. `Dnm1` is actually the more
brain-enriched dynamin isoform, and with `Dnm3` accounts for most brain dynamin
at synapses in the Raimondi et al. mouse work. Its acute postnatal CRISPR
profile is therefore informative: in `151 TH Prkcd Grin2c Glut`, `Dnm1` loss
produced only a self-transcript hit, and the Distributed Agents corpus summarizes the
full same-experiment surface as 0 non-`Dnm1` downstream genes at FDR 0.10 in
22/22 neuronal groups despite recurrent target-RNA depletion. Because `Dnm2` is
not the dominant synaptic-vesicle dynamin and because partial mosaic editing can
leave substantial residual dynamin function, I considered a `Rab7`- or
`Cltc`-scale effect unlikely.

`Synj1` strengthens the zero-downstream call. It is a synaptic-vesicle
endocytosis partner immediately downstream of dynamin-mediated vesicle fission:
after fission, synaptojanin hydrolyzes PI(4,5)P2 to promote coat removal. In
this focal cell group it again produced only its own depleted transcript as an
FDR 0.05 hit. The internal corpus notes that this was pan-surface-flat in 21
recovered neuronal groups and that `Dnm1` phenocopied `Synj1` at the
transcriptomic level with no downstream FDR 0.10 genes in the matched groups.
That makes the most mechanism-specific training evidence point to no induced
downstream DEG program for an acute dynamin-family perturbation.

`Bin1` was another near neighbor but a weaker one. BIN1/amphiphysin binds
dynamin at curved membranes, and `Dnm2` is genetically and biophysically tied
to BIN1 in muscle membrane remodeling, yet the represented `Bin1` perturbation
in this screen was self-down only in 151 TH cells. The corpus specifically
reports Bin1 transcript suppression without downstream remodeling in several
null groups and lack of a shared clathrin/endosomal Alzheimer-risk
transcriptional module. This again argues against a broad response.

`Cltc` is the main counterweight because it is a core coated-vesicle component
rather than an accessory synaptic-vesicle gene. It did elicit transcriptional
responses in selected neuronal populations in the same experiment, including
AP-1/ISR and synaptic-gene changes in the corpus. In the focal 151 TH cells,
however, `Cltc` had only 3 FDR 0.05 genes and did not reproduce a `Dnm1` or
`Synj1` pattern. Because knocking down the coat itself should be a more global
block of clathrin-mediated traffic than a partial `Dnm2` perturbation in
neurons that also express `Dnm1` and `Dnm3`, I used `Cltc=3` as an upper local
calibrator rather than the center of the `Dnm2` prediction.

`Vps35` and `Rab7` are later endosome/retromer and late-endosome routing genes,
respectively. `Vps35` had a small, 17-DEG TH-specific synaptic/calcium pattern,
while `Rab7` had 501 DEGs driven by lysosome, sterol, proteasome, and stress
compensation. These are useful negative controls for pathway distance: they
show that the assay can see endomembrane disruption in this cell group, but
their signatures are dominated by degradative organelle homeostasis rather than
early dynamin-mediated scission. I therefore did not transfer the `Rab7` breadth
to `Dnm2`.

The remaining question is whether to predict zero or one. The sole significant
rows for `Dnm1`, `Synj1`, and `Bin1` are their own target RNAs, and `Dnm2` is a
measured focal transcript in the parquet. Given dynamin 2's ubiquitous
expression and the ability of the assay to detect comparable self-RNA depletion
for the closest flat endocytic examples, my point prediction is one DEG: the
`Dnm2` transcript itself passes FDR 0.05, but no separate downstream gene does.

# Limits and extrapolation

The prediction is close to the zero/one boundary. `n_degs = 1` depends on
detectability of the `Dnm2` target transcript under this exact gRNA pool, and
the supplied training data show many true perturbations with no significant
self-hit. The biological downstream call is more confident than the self-hit
call: `Dnm1`, `Synj1`, `Bin1`, and many adjacent trafficking genes were
downstream-flat, whereas the larger `Rab7`/`Tsc2`/`Dctn1` programs are distal
stress states. The comparison is still imperfect because `Dnm2` has non-synaptic
plasma-membrane and cytoskeletal functions that `Dnm1` does not fully cover,
and because this assay is sparse, mosaic, postnatal, and transcriptomic; it may
miss physiological endocytosis defects that do not resolve into BH-significant
single-nucleus RNA changes by P37-P44.

# Final point estimate

I predict `Dnm2` will have 1 DEG in `151 TH Prkcd Grin2c Glut`.
