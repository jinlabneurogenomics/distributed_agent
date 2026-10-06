# DEG-count prediction trace

## Question and endpoint

The requested endpoint is the scalar number of genes with `pvals_adj < 0.05` in
the held-out `Nme7` perturbation in the focal `151 TH Prkcd Grin2c Glut`
thalamic glutamatergic cell group. I treated `n_degs` as a direct,
assay-powered FDR count among recovered nuclei, not as a measure of target
importance, editing efficiency, viability, or ciliary strength. The `Nme7`
perturbation itself is absent from both supplied inputs, so the prediction has
to be transferred from non-held-out perturbations and external NME7 biology.

## Sources

- Declared training endpoint:
  `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
- Declared differential-expression parquet:
  `training differential-expression dataset`.
- Requested targets:
  `single-target request for Nme7`.
- Run-local dataset portrait, task bindings, coverage summary, capability
  manifest, and measurement registry. I used these only for schema, endpoint,
  and capability constraints; I did not read same-experiment reports or
  held-out `Nme7` signatures.
- HGNC REST record `HGNC:20461`, queried 2026-09-03, for human `NME7`
  membership in the NME/NM23 and cilia/flagella-associated gene groups and
  aliases `NM23-H7` and `CFAP67`.
- UniProtKB REST record `Q9QXL8`, queried 2026-09-03, and QuickGO annotations
  for mouse `Nme7`, queried 2026-09-03, for curated localization/function terms
  including centrosome, axonemal microtubule, intraciliary transport, cilium
  assembly, and left/right pattern formation.
- Lai et al. 2011, DOI `10.1091/mbc.E10-07-0596` / PMID `21289087`: siRNA
  screening placed NME7 among ciliary transport regulators affecting Hedgehog
  cargo transport.
- Vogel et al. 2010, DOI `10.1177/0300985809353553` / PMID `20080492`: mouse
  `Nme7` nulls showed situs inversus, hydrocephalus, and nasal exudates,
  implicating motile ciliary dysfunction.
- Vogel et al. 2011, DOI `10.1177/0300985811415708` / PMID `21746835`:
  congenital hydrocephalus in multiple engineered mouse lines, including
  `Nme7`, was linked mostly to dysfunctional motile cilia.
- Reish et al. 2016, DOI `10.1002/humu.22998` / PMID `27060491`: a homozygous
  human `NME7` mutation segregated with situs inversus totalis.
- Wang et al. 2022, DOI `10.1242/dmm.049568` / PMID `36533556`: multi-guide
  zebrafish crispants rapidly identified `nme7` as a cilia-associated gene
  candidate with ciliary phenotypes.
- Sedova et al. 2021, DOI `10.3390/ijms22083810` / PMID `33916973`: rat `Nme7`
  knockout caused primary-ciliary-dyskinesia-like phenotypes, including
  hydrocephalus, situs inversus totalis, and sterility.
- Ji et al. 2025, DOI `10.26508/lsa.202402933` / PMID `39824631`: NME7 localized
  to centrosomes/basal bodies, contributed to primary-cilium assembly and
  ciliary microtubule stability, and affected Hedgehog signaling through
  ciliary SMO accumulation in mammalian cells.

## Declared-dataset calibration

The focal training CSV had 1,674 distinct non-held-out targets. Its `n_degs`
distribution was zero-inflated:

- 1,205 / 1,674 targets had `n_degs = 0`;
- 469 / 1,674 had any nonzero focal-cell response;
- the median was 0, the 75th percentile was 1, and 1,512 / 1,674 targets had
  `n_degs <= 2`;
- a small tail was very large, with `Uba5 = 2677`, `Tpr = 1768`, `Sin3a = 1433`,
  and `Rnpc3 = 868`.

I searched the training count table for direct `Nme*` paralogs and found none,
so there was no same-family quantitative anchor. I then searched for ciliary,
transition-zone, dynein-2, BBSome, Hedgehog, basal-body, and kinesin training
targets and checked their exact focal-cell rows in the parquet by filtering

```python
(group_name == "151 TH Prkcd Grin2c Glut") & gene_target.isin(analog_targets)
```

and counting `pvals_adj < 0.05`. The parquet counts matched the count CSV:

| training perturbation | relevant analogy to `Nme7` | focal `n_degs` | focal expression-pattern evidence |
|---|---:|---:|---|
| `Ift43` | IFT-B / ciliogenesis | 0 | no adjusted-significant gene; min adjusted p = 0.847 |
| `Ift81` | IFT-B / anterograde ciliary trafficking | 0 | no adjusted-significant gene; min adjusted p = 0.391 |
| `Ift88` | IFT-B / anterograde ciliary trafficking | 0 | no adjusted-significant gene; min adjusted p = 1.000 |
| `Dync2h1` | dynein-2 retrograde IFT motor | 0 | no adjusted-significant gene; min adjusted p = 0.348 |
| `Dync2i1` | dynein-2 retrograde IFT motor | 0 | no adjusted-significant gene; min adjusted p = 1.000 |
| `Cep290` | ciliary transition-zone scaffold | 0 | no adjusted-significant gene; min adjusted p = 0.650 |
| `Rpgrip1l` | transition-zone ciliopathy gene | 0 | no adjusted-significant gene; min adjusted p = 0.184 |
| `Ttc21b` | IFT-A / retrograde trafficking | 0 | no adjusted-significant gene; min adjusted p = 0.459 |
| `Bbs5` | BBSome component | 0 | no adjusted-significant gene; min adjusted p = 0.220 |
| `Kif3b` | kinesin-2 anterograde ciliary motor subunit | 0 | no adjusted-significant gene; min adjusted p = 1.000 |
| `Smo` | Hedgehog receptor trafficked in primary cilia | 0 | no adjusted-significant gene; min adjusted p = 1.000 |
| `Gli1` | Hedgehog-pathway transcriptional effector | 0 | no adjusted-significant gene; min adjusted p = 1.000 |
| `Gli2` | Hedgehog-pathway transcriptional effector | 0 | no adjusted-significant gene; min adjusted p = 1.000 |
| `Ttc8` | BBSome component | 1 | only `Ttc8` itself passed FDR, log2FC = -0.663 |
| `Kifbp` | kinesin-binding/microtubule regulator, weaker ciliary analogy | 2 | `Kifbp` and `Srebf2` passed FDR |

The signed whole-transcriptome focal log-fold-change profiles of the zero-DEG
ciliary anchors were also weak rather than a coherent high-magnitude module:
Spearman correlations were `Ift43`/`Ift81` = 0.229, `Ift43`/`Ift88` = 0.174,
`Ift81`/`Ift88` = 0.239, `Dync2h1`/`Dync2i1` = 0.238,
`Cep290`/`Rpgrip1l` = 0.304, and `Ift88`/`Ttc21b` = 0.261.

## Target-specific reasoning

### `Nme7`

`Nme7` is a nucleoside-diphosphate kinase-family gene also classified as a
cilia/flagella-associated factor. External evidence makes a ciliary mechanism
more appropriate than a generic NME-family transfer: NME7 localizes to the
centrosome/basal body and a small ciliary pool, NME7 loss impairs primary-cilium
assembly and ciliary SMO accumulation in cultured mammalian cells, siRNA against
Nme7 altered ciliary cargo transport and Hedgehog readouts, and full animal
knockouts or crispants produce motile-cilia phenotypes such as situs inversus,
hydrocephalus, sterility, and other primary-ciliary-dyskinesia-like outcomes.

The experimental causal transfer is:

`Nme7` CRISPR disruption -> reduced basal-body/ciliary NME7 function -> altered
primary-cilium assembly, ciliary trafficking, microtubule stability, or
Hedgehog handling -> any resulting thalamic glutamatergic-cell state change
among edited cells that survive 3-4 weeks after P16 AAV delivery -> nuclear
RNA differences in recovered nuclei -> FDR-significant genes.

The external ciliary evidence enters at the direct molecular and organelle
stages of that chain, not at the final survivor-conditioned thalamic snRNA-seq
FDR-count endpoint. It supports a real ciliary prior for `Nme7`, but the
training perturbations that should impair stronger or equally central parts of
the same limiting ciliary function, especially `Ift43`, `Ift81`, `Ift88`,
`Dync2h1`, `Dync2i1`, `Cep290`, `Rpgrip1l`, `Ttc21b`, `Bbs5`, and `Kif3b`, were
all exactly zero in this cell group. The downstream Hedgehog anchors `Smo`,
`Gli1`, and `Gli2` were also zero. `Ttc8 = 1` is the closest nonzero BBSome
boundary case, but its sole FDR hit was the target transcript itself and does
not establish a broad ciliary response. `Kifbp = 2` is a weak microtubule
counterexample, but it is not an obligate IFT or NME7-complex analog. Together
these comparisons argue that the acute, mosaic loss of ciliary genes in
postnatal recovered `151 TH Prkcd Grin2c Glut` nuclei rarely creates enough
coherent nuclear RNA change to pass BH FDR 0.05.

I therefore predict a non-detected focal transcriptional response for `Nme7`
and set the point estimate to `0`.

## Limits

This is extrapolation because there was no non-held-out `Nme` paralog in the
training endpoint and no expression signature for held-out `Nme7`. The ciliary
analogs are mechanistically relevant but not identical: NME7 has reported
gamma-tubulin-ring-complex and nucleoside-diphosphate-kinase connections that
are not captured by individual IFT, BBSome, or transition-zone knockouts. The
external knockout phenotypes came from germline or constitutive systems,
zebrafish embryos, cultured cells, or non-neuronal motile cilia; those data
establish NME7's ciliary function but do not directly observe postnatal
thalamic neuronal snRNA-seq DEG breadth. Finally, a zero prediction means no
measured gene is expected to pass the experiment's BH-adjusted Wilcoxon
threshold in recovered nuclei; it does not mean the edit is biologically inert
or that NME7 is unimportant for cilia.
