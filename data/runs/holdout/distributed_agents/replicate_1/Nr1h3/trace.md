# Prediction trace

## Question and endpoint

I interpreted the task as a single held-out point prediction for the focal group
`151 TH Prkcd Grin2c Glut`. The endpoint is direct: `n_degs` is the count of
measured genes with Scanpy Wilcoxon Benjamini-Hochberg adjusted `pvals_adj <
0.05` in perturbed versus matched non-targeting control nuclei. The requested
target manifest contains one target, in this order:

```tsv
target_name
Nr1h3
```

`Nr1h3` was deliberately absent as a perturbation from both the DE Parquet and
the focal-cell training count table, so I did not try to read its held-out
signature or count. The useful prediction evidence was therefore the response
breadth of visible training perturbations in the same Parquet, especially
visible perturbations in the LXR/RXR and cholesterol-efflux neighborhood.

## Sources used

- Declared differential-expression input:
  `training differential-expression dataset`.
  This is the direct measured-gene x cell-class x perturbation surface for the
  non-held-out perturbations.
- Declared focal-cell training counts:
  `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
  This directly supplies `n_degs` for visible perturbations in `151 TH Prkcd
  Grin2c Glut`.
- Requested-target manifest:
  `single-target request for Nr1h3`.
- Run-local dataset portrait, task bindings, coverage summary, capability
  manifest, and measurement registry under `codex_runtime/pipeline/`.
- Internal same-experiment semantic corpus
  `perturbai-july-260713-sourceguard-1773-v1`. I used its bounded graph and
  direct-evidence operations only for navigation and for packaged
  interpretation of visible `Nr1h2` and `Abca1` Parquet results; I did not use
  graph multiplicity, comparator order, or Finding frequency as a score.
- External literature and curated knowledge:
  Edwards et al. 2002, Vascular Pharmacology, DOI
  `10.1016/s1537-1891(02)00175-1`; Courtney and Landreth 2016, Trends
  Endocrinol Metab, DOI `10.1016/j.tem.2016.03.018`, PMID `27113081`;
  Chen et al. 2012, Biochim Biophys Acta, DOI
  `10.1016/j.bbalip.2012.09.007`, PMID `23010475`; Song et al. 2022,
  Biomedicines, DOI `10.3390/biomedicines10092165`, PMID `36140266`;
  and the July corpus' UniProtKB entry for mouse LXR beta / `Nr1h2`
  (`Q60644`).

## Computation over the supplied dataset

I first summarized the complete declared Parquet with the advertised
`dataset.perturbseq_features` workbench:

```bash
python perturbseq_feature_workbench.py summarize \
  --parquet training_de_all_cell_groups.parquet \
  --cache-dir evidence/cache \
  --out evidence/tables/perturbseq_features.parquet
```

That scan read 616,253,184 DE rows and wrote graph-free distributional features
for 1,674 biological training targets. The focal training counts were highly
zero-inflated: 1,205/1,674 visible targets had `n_degs = 0`; the median was 0,
the 75th percentile was 1, and only the top 5% exceeded 18 DEGs. Across the
feature table, whole-surface FDR burden was a simple sanity check on breadth:
all 936 visible targets with zero FDR<0.05 genes anywhere in the 23-group DE
surface necessarily had zero in the focal group.

I then pulled the visible LXR and cholesterol/ApoE comparators from the training
count table and from the Parquet-derived feature table. Counts below are the
direct focal endpoint followed by all-cell FDR burdens from the declared
Parquet:

```tsv
target	focal_n_degs	all_groups_FDR05	all_groups_FDR10	min_FDR
Nr1h2	0	0	0	0.1716
Abca1	0	0	1	0.0846
Srebf1	0	0	0	0.1003
Srebf2	7	45	51	0
Hmgcr	0	2	3	0.0195
Rxra	0	0	0	0.8641
Rxrb	0	0	1	0.0957
Rxrg	0	0	0	0.3275
Abca7	0	0	0	0.1949
App	1	20	20	0
Lrp1	0	4	5	0.0003
Sorl1	0	9	9	0
Nr1h4	0	0	0	0.2676
Nr1h5	0	0	0	0.3227
```

This table was used as calibration, not as a blind family heuristic. `Srebf2`
is the counterexample: the same neuronal assay can detect a sterol program, but
its SREBP2 loss signature does not imply that all lipid regulators cause a
detectable focal response.

## Target-specific reasoning

### Nr1h3

`Nr1h3` encodes LXR alpha, one of the two oxysterol-activated liver X receptors.
Both LXR alpha / `Nr1h3` and LXR beta / `Nr1h2` heterodimerize with RXR family
members and regulate cholesterol and fatty-acid homeostasis genes after
oxysterol activation (Edwards et al. 2002). In the CNS, LXRs are best known for
cholesterol handling and inflammatory modulation across astrocytes, microglia,
oligodendrocytes, and lipid-rich challenged states rather than for a constitutive
high-amplitude basal transcriptome in every neuron (Courtney and Landreth 2016;
Song et al. 2022).

The closest assayed receptor analog was `Nr1h2`, the LXR beta paralog. In the
July corpus report, which is a packaged interpretation of the same Parquet,
`Nr1h2` had rows in all 23 neuronal groups and 0 of 388,023 downstream
contrasts at FDR < 0.10. In the requested `151 TH Prkcd Grin2c Glut` group it
had 200 perturbed nuclei, the `Nr1h2` self row was `logFC = -0.215` with
`FDR = 1.0`, and all 17,258 tested downstream genes were nonsignificant even
at FDR < 0.10. The expected LXR output genes were not borderline: `Abca1`,
`Abcg1`, `Apoe`, `Cyp46a1`, `Fasn`, `Ldlr`, `Lpl`, `Mylip`, `Scd1`, `Srebf1`,
and `Srebf2` each had minimum FDR 1.0 across all 23 `Nr1h2` contrasts.

`Abca1` was the strongest immediate downstream functional analog because LXR/RXR
induces ABCA1-mediated sterol efflux. It was also silent in the focal endpoint:
0 DEGs in `151 TH Prkcd Grin2c Glut`, 0 genes at FDR < 0.05 in the entire
23-group surface, and only one gene at FDR < 0.10 anywhere. Its report further
showed that ApoE/LXR/RXR/cholesterol genes were measured but did not move after
`Abca1` perturbation. This is important because Chen et al. found that ABCA1 and
ABCG1 mediate cholesterol efflux in astrocytes, whereas neurons use different
efflux wiring, and this screen is NeuN-enriched rather than astrocyte- or
microglia-rich.

The RXR partners did not provide an alternate same-pathway positive prior.
`Rxra`, `Rxrb`, and `Rxrg` were all 0-DEG perturbations in the focal group;
`Rxra` and `Rxrg` had no FDR < 0.05 genes anywhere in the full training surface,
and `Rxrb` had only one FDR < 0.10 gene. `Srebf1`, a lipid transcription-factor
neighbor, was also 0 in the focal group and 0 across the FDR < 0.05 surface.
`Srebf2` did show that sterol biosynthesis can be detected in this platform
with 7 focal DEGs and 45 all-surface FDR < 0.05 genes, so the LXR/ABCA1 silence
is not because cholesterol-related transcripts are globally invisible. The
causal difference is that `Srebf2` directly maintains cholesterol-biosynthetic
gene expression, while loss of a single LXR receptor in recovered juvenile
neurons is expected to be buffered by basal ligand availability, by `Nr1h2`, and
by glial/cell-extrinsic cholesterol supply.

My causal transfer model was:

`Nr1h3` CRISPR loss -> reduced LXR alpha-dependent oxysterol/RXR
transactivation -> strongest consequences in glial cholesterol efflux,
lipoprotein lipidation, and inflammatory states -> weak or redundant
cell-autonomous propagation in postnatal NeuN+ thalamic glutamatergic nuclei
without a lipid or injury challenge -> few or no survivor-conditioned
Wilcoxon-significant nuclear RNA shifts.

Under that model, the same endpoint direction is expected for `Nr1h2`, `Rxra`,
`Rxrg`, `Srebf1`, and `Abca1`: each should be small or zero in this exact assay,
and each was in fact 0 in the training focal endpoint. `Srebf2` is a
counterexample to over-generalizing the cholesterol label, not a reason to
promote `Nr1h3`, because SREBP2 loss blocks a different and more direct
biosynthetic arm. I therefore predict that `Nr1h3` will not pass the FDR 0.05
threshold for any gene in `151 TH Prkcd Grin2c Glut`.

Final point estimate:

```tsv
target_name	predicted_n_degs
Nr1h3	0
```

## Limits

The requested `Nr1h3` perturbation was completely held out, so no same-gene
signature, recovered perturbed-cell count, or DNA editing measurement was
available. All within-dataset evidence is transfer from visible perturbations,
chiefly `Nr1h2`, `Abca1`, `Rxra`, `Rxrb`, `Rxrg`, and `Srebf1`.

The strongest prior roles for LXR alpha are in lipid handling, ApoE-containing
particles, glia, macrophage-like cells, and challenged cholesterol states. Those
are exactly the contexts this NeuN-enriched juvenile neuronal assay undersamples
or does not perturb, so the prediction is a statement about this focal
snRNA-seq endpoint rather than about the biological importance of `Nr1h3`.

The `Nr1h2` and `Abca1` nulls are informative because they were recovered across
high-power groups and because the same Parquet detected `Srebf2`; they still do
not prove that every LXR alpha allele was edited effectively or that a rare
cell-extrinsic phenotype could not occur before survivor sampling.
