# Rbfox1 n_degs forecast

## Target and endpoint

- Target: `Rbfox1`
- Cell class: `151 TH Prkcd Grin2c Glut`
- Endpoint: measured genes in this class with Wilcoxon BH-adjusted `p < 0.05`
- Forecast: `12`

## Evidence used

### Declared Rbfox1 biology bundle

Source: `[local file: Rbfox1.json]`

- Exact focal-population reach was high: `Rbfox1` was detected in 22,901 of 23,679 non-target cells in `151 TH Prkcd Grin2c Glut` nuclei, `96.71438827653195%`, with mean raw UMI `4.684530596731281`, mean log1p CP10K `1.2863831511320576`, and pseudobulk CPM `293.5961444210564`.
- The functional-stock card adjudicated RBFOX1 as a continuously renewed RNA-binding/splicing regulator whose operative capacity should be substantially depleted by the P37-P44 harvest after a P16 disruptive edit, while noting that no acute Rbfox1-specific neuronal protein half-life is known.
- Prior mouse neural evidence supports biological consequence outside the exact thalamic P16 edit: CNS loss changed neuronal splicing and increased seizure/excitability phenotypes, and interneuron loss changed cell-type-specific splicing.
- The bundle also contains a downward modifier for this gene-level DEG endpoint: RBFOX2/RBFOX3 can partially buffer RBFOX1 loss, and the primary RBFOX1 operation is alternative exon use, which can be strong at the isoform level while producing only a small number of gene-level abundance changes.

### Matched visible count table

Source: `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`

- The visible table contained 1,674 training targets and did not contain `Rbfox1`.
- The class-level count distribution was sparse: 1,205 of 1,674 visible targets had `n_degs = 0`; the median was `0`, the 75th percentile was `1`, the 90th percentile was `2`, and the 95th percentile was `18`.
- The upper tail was made of broad essential machinery or stress states, for example `Uba5 = 2677`, `Tpr = 1768`, `Sin3a = 1433`, `Rnpc3 = 868`, `U2af2 = 828`, `Psmb4 = 742`, `Hnrnpu = 733`, and `Cdc40 = 624`. I treated these as upper boundaries unless their biology was close to RBFOX1.

### Analog nomination and corpus expansion

Artifacts: `evidence/analog_nominations.jsonl`, `evidence/profile_comparison.json`, `evidence/profile_review.tsv`, `evidence/profile_finalize.json`

- A species-safe annotation nomination against the exact 1,674-gene training universe found no training-available exact RBFOX paralog for `Rbfox1`.
- The leading nominees separated into a MECP2/REST/SIN3A regulatory module and an RNA-binding module. Their exact visible `n_degs` values were:

  | comparator | role in reasoning | n_degs |
  |---|---:|---:|
  | `Rest` | sequence-specific neuronal regulator, MECP2/Rett module | 0 |
  | `Mecp2` | MECP2/Rett module | 16 |
  | `Tia1` | RNA-binding/stress-granule branch | 0 |
  | `Fmr1` | sequence-specific RNA regulation and translation branch | 0 |
  | `Fxr1` | FMRP-family RNA branch | 0 |
  | `Atxn2` | physical and RNA-granule comparator | 8 |
  | `Hnrnpa2b1` | hnRNP/RNA-binding comparator | 11 |
  | `Hnrnpc` | broader hnRNP comparator | 122 |
  | `Tardbp` | broader hnRNP/stress-granule comparator | 210 |
  | `Snrnp70` | snRNP/core splicing boundary | 213 |
  | `Hnrnpu` | broad hnRNP/core RNA-processing boundary | 733 |
  | `U2af2` | essential spliceosome boundary | 828 |
  | `Sin3a` | pleiotropic chromatin/coregulator boundary | 1433 |

- The corpus cohort audit put these 13 nominated nodes in one explicit-Finding component but in distinct fully connected subsets: `Mecp2`/`Rest`/`Sin3a`, `Fmr1`/`Fxr1`, `Atxn2`/`Hnrnpa2b1`/`Tardbp`/`Tia1`, and `Hnrnpc`/`Hnrnpu`/`Snrnp70`/`U2af2`. I therefore did not collapse them into one average.
- Recurrence-based corpus expansion added 27 visible candidates. I symmetrically compared all 40 source-plus-expansion nodes in the declared thalamic Parquet context. All 40 profiles were available. I kept nine expansion candidates as RNA/module support, kept nine as high- or low-scale boundaries, and rejected nine mechanistic detours; the final review passed with `keep = 18`, `boundary = 9`, `module_support = 9`, and `reject = 9`.
- The retained expansion RNA/module-support counts had median `1` and mean `17.33`: `Cyfip1 = 0`, `Matr3 = 149`, `Dicer1 = 0`, `Cyfip2 = 1`, `Eif4g1 = 1`, `Hnrnpdl = 1`, `Ddx39b = 0`, `Hnrnph2 = 4`, and `Mbd2 = 0`.
- The retained boundary counts had median `430`, dominated by broad machinery/stress perturbations: `Prpf6 = 454`, `Cdc40 = 624`, `Psmb4 = 742`, `Psmc1 = 430`, `Thoc1 = 303`, `Rnpc3 = 868`, with `Ubr1 = 0`, `Snrpb = 0`, and `Vcp = 2` showing that even mechanistic boundaries could be endpoint-quiet.

## Forecast synthesis

`Rbfox1` has strong exact expression in the focal thalamic nuclei and likely loses an active, continuously renewed RNA-regulatory stock over the 21-28 day assay window, so I forecast a nonzero signature rather than the global visible-target median of zero. The expected magnitude should stay near the low RNA-regulator module, however: RBFOX1 is paralog-buffered, its direct output is exon choice more than total gene abundance, and the closest available sequence-specific or hnRNP-like visible perturbations were mostly 0-16 DEGs. I used the 122-213 DEG hnRNP/snRNP rows as weak upward pressure because a nuclear RNA-processing hit could leak into gene-level expression, and I treated the hundreds-DEG core-spliceosome/proteostasis rows as upper boundaries because they disrupt broad RNA or protein-homeostasis machinery rather than the RBFOX1 exon program.

A low-teens point preserves that synthesis: above the flat FMRP/TIA/FXR1/REST rows and close to `Atxn2`, `Hnrnpa2b1`, and `Mecp2`, but below broad hnRNP and spliceosome perturbations.

