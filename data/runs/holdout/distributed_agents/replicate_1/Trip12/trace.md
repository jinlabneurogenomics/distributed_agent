# DEG-count prediction for `Trip12` in `151 TH Prkcd Grin2c Glut`

## Question and resolved ambiguities

The task is to predict, for each requested held-out perturbation, the integer
number of genes that would pass Benjamini-Hochberg adjusted Wilcoxon
`pvals_adj < 0.05` in the focal thalamic glutamatergic cell group,
`151 TH Prkcd Grin2c Glut`. The only requested held-out target in
`the single-target request` is `Trip12`.

I treated the supplied differential-expression parquet and the supplied
`151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` as the direct same-assay
evidence for non-held-out perturbations. `Trip12` is absent as a `gene_target`
from both training inputs, so the endpoint for `Trip12` is absent from the
declared inputs and must be inferred from nearby non-held-out perturbations and
external gene-function knowledge. The endpoint is response breadth in recovered
nuclei, not editing efficiency, cell death, developmental indispensability, or
protein abundance.

## Sources

Internal and same-experiment sources:

- Declared training DEG counts for `151 TH Prkcd Grin2c Glut`:
  `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
- Declared differential-expression parquet:
  `training differential-expression dataset`.
- Run-local task bindings, dataset context, coverage, capability manifest, and
  measurement registry in `codex_runtime/pipeline`.
- The selected internal PerturbAI July same-experiment corpus,
  `perturbai-july-260713-sourceguard-1773-v1`, queried through the declared
  `corpus.findings` and `corpus.calibration` capabilities. I used the corpus as
  a packaged interpretation layer over this same experiment, not as independent
  replication.

External sources:

- PubMed and the review by Brunet et al. 2020, DOI
  `10.3390/ijms21228515`, PMID `33198194`, for TRIP12 being a HECT-family E3
  ubiquitin ligase with roles in cell-cycle progression, DNA damage repair,
  chromatin regulation, differentiation, and intellectual-disability/autism
  genetics.
- Aerden et al. 2023, DOI `10.1038/s41431-023-01307-x`, PMID `36747006`, for
  heterozygous TRIP12 variants causing Clark-Baraitser syndrome with global
  developmental delay, language impairment, epilepsy/autistic features in a
  subset, and dysmorphism.
- Gudjonsson et al. 2012, DOI `10.1016/j.cell.2012.06.039`, PMID `22884692`,
  for TRIP12 and UBR5 limiting RNF168-dependent chromatin ubiquitylation at DNA
  double-strand breaks.

## Computed same-assay quantities

From the focal training-count CSV I used the empirical count distribution to
calibrate scale. Among 1,674 non-held-out perturbations, 469 had any
FDR-significant DEG, the median was 0, the 90th percentile was 2, the 95th
percentile was 18, and the 99th percentile was about 436. `Huwe1` had 158
DEGs, rank 33 of 1,674 in descending count order, so a HUWE1-like response is
large relative to most targets in this cell group.

I then filtered the parquet to the focal cell group and to mechanistic
comparators. The key focal-cell counts were:

| Training perturbation | `n_degs` in `151 TH Prkcd Grin2c Glut` | Why inspected |
| --- | ---: | --- |
| `Huwe1` | 158 | Brain-relevant HECT E3 ligase and the only strong HECT-family response represented in the same assay |
| `Hectd4` | 1 | Disease-linked HECT E3 ligase; near-null in the screen |
| `Ube3a` | 0 | Angelman/ASD HECT E3 ligase |
| `Herc1` | 0 | Large HERC/HECT E3 ligase; neurological phenotypes |
| `Herc2` | 0 | Large HERC/HECT E3 ligase and UBE3A regulator |
| `Ubr1` | 0 | HECT-family comparator from the internal Huwe1 contrast |
| `Myc` | 0 | HUWE1 substrate-axis / proliferation counterexample |
| `Mycn` | 0 | HUWE1 substrate-axis / neural progenitor counterexample |
| `Trp53` | 0 | DNA-damage and HUWE1 substrate-axis counterexample |
| `Cdkn2a` | 0 | ARF/p53 tumor-suppression axis touched by TRIP12 biology |
| `Bap1` | 16 | Chromatin and deubiquitinase comparator in the broad TRIP12/ASXL/Polycomb neighborhood |
| `Asxl3` | 0 | Neurodevelopmental chromatin comparator in the ASXL family |
| `Kat6a` | 0 | Neurodevelopmental chromatin acetyltransferase comparator |
| `Kat6b` | 0 | Neurodevelopmental chromatin acetyltransferase comparator |

The focal `Huwe1` signature was a real expression pattern, not a singleton:
158 genes passed FDR 0.05 and the leading genes included `Rsrp1` up,
`Tcea2` up, `Kcnk9` up, `Dusp11` up, `Aifm3` up, `Sf3b1` up, and `L1cam`
down. The internal same-experiment corpus summarized this as a recurrent
RNA-processing/SR-factor module coupled to mitochondrial/redox and trafficking
genes, enriched in a few subcortical classes including the requested 151 TH
class. It also reported that this was not the canonical N-Myc, Notch, or p53
program expected from developmental HUWE1 studies.

The same corpus explicitly contrasted `Huwe1` with represented HECT/E3 genes:
`Ube3a`, `Hectd4`, `Herc2`, `Ubr1`, `Trp53`, `Myc`, and `Mycn` failed to
reproduce the HUWE1 FDR-level RNA/mitochondrial module. Direct parquet checks
agreed in the focal group: full-rank Wilcoxon-score correlations between
`Huwe1` and `Ube3a` or `Huwe1` and `Hectd4` were near zero to slightly
negative in the 151 TH rows, while the known Huwe1 signature neighbors
`Vps35` and `Dctn1` had only weak positive whole-rank correlations and are
endomembrane/transport comparators rather than TRIP12 substrate-axis genes.

## Target-specific reasoning

### `Trip12`

`Trip12` encodes thyroid hormone receptor interactor 12, a HECT-domain E3
ubiquitin ligase. It is biologically credible in neurons: human heterozygous
loss-of-function variants cause Clark-Baraitser neurodevelopmental syndrome
(Aerden et al. 2023), and the TRIP12 literature connects the ligase to
genome-stability, chromatin, differentiation, and ubiquitin-mediated turnover
(Brunet et al. 2020). At the molecular level, TRIP12 participates with UBR5 in
a DNA double-strand-break circuit by limiting RNF168 and preventing runaway
chromatin ubiquitylation (Gudjonsson et al. 2012).

Those facts support real disease relevance but only weakly support a broad
acute mRNA response in the recovered P16-to-P37/44 thalamic neurons assayed
here. The intervention-to-endpoint chain is:

`Trip12` CRISPR loss -> altered degradation of selected TRIP12 substrates,
including DNA-damage/chromatin regulators in the external literature ->
possible changes in chromatin stress, differentiation state, or survivor
homeostasis -> sampling of NeuN-positive, recovered, class-assigned 151 TH
nuclei -> Wilcoxon FDR-significant steady-state nuclear RNA differences.

The weakest transfer link is between the early protein-level ubiquitin circuit
and a durable, cell-autonomous snRNA-seq footprint in already postmitotic
juvenile thalamic neurons. UBR5, RNF168, RNF8, MDC1, TP53BP1, and BRCA1 were
not present as focal training perturbations, so the most direct TRIP12 DNA
damage pathway could not be calibrated. The available indirect checks were
flat: `Trp53`, `Myc`, `Mycn`, and `Cdkn2a` all had 0 DEGs in the focal count
CSV, arguing that simply perturbing canonical p53/MYC/ARF transcriptional axes
does not generate the requested response in this assay.

I considered `Huwe1` the only serious nonzero analog because it is a
brain-relevant HECT E3 ligase and produced 158 focal DEGs. I did not transfer
that count directly for two reasons. First, the same-experiment Huwe1 report
showed a specific RNA-processing/mitochondrial/trafficking program and noted
that other represented HECT-family perturbations did not converge with it.
Second, TRIP12's best-established biochemical axis in the searched external
literature, RNF168 restraint at DNA lesions, is not the HUWE1 postmitotic
module. Thus `Huwe1` raises the prior above a pure zero but is a loose analog.

The counterexamples pull harder. `Ube3a`, `Herc1`, and `Herc2` each caused
0 focal DEGs despite neurological ubiquitin-ligase biology; `Hectd4` caused
only a single significant row, its own transcript; `Ubr1` was also 0; and
several chromatin/neurodevelopmental neighbors in the training table were
quiet or near quiet. The best prediction is therefore that `Trip12` would be at
most a sparse response in this focal cell group. I assigned a small positive
count, 4 DEGs, to reflect that TRIP12 is closer to HUWE1 than to unrelated
RING/F-box ligases and is a haploinsufficient neurodevelopmental gene, while
keeping it near the assay median because the HECT-family and pathway
counterexamples do not support a broad HUWE1-like response.

Predicted `Trip12` count: **4**.

## Limits and uncertainty

The prediction is extrapolative. `Trip12` itself is completely absent from the
training DE parquet, and several of the cleanest pathway genes for its
DNA-damage role, especially `Ubr5`, `Rnf168`, `Rnf8`, `Mdc1`, `Tp53bp1`, and
`Brca1`, were not represented in the 151 TH training count table. Most
external TRIP12 mechanisms come from cancer, DNA-damage, developmental, or
human genetics settings rather than acute sparse P16 CRISPR in recovered mouse
neurons. Protein ubiquitination, substrate stabilization, DNA repair, and
selective depletion before nucleus recovery were not directly measured by the
snRNA-seq endpoint. Conversely, a focal count near zero would not mean that
TRIP12 is biologically unimportant; it would only mean that its acute loss was
buffered or not converted into enough survivor-state nuclear RNA changes to
pass FDR 0.05 in this assay and cell group.
