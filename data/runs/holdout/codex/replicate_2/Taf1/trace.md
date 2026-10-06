# Taf1 direct DEG-count forecast

## Target and endpoint

- Target: `Taf1`
- Focal population: `151 TH Prkcd Grin2c Glut`
- Endpoint: measured genes with Wilcoxon BH-adjusted `p < 0.05`
- Prediction: `12`

## Evidence used

### Endpoint-blind Taf1 biology

The declared `Taf1` biology bundle identifies TAF1 as the largest TFIID subunit, a scaffold for promoter recognition and RNA polymerase II preinitiation-complex assembly, with annotated histone acetyltransferase and kinase activities. It also reports adult neural Taf1 expression, mouse thalamic RNA detection, and no close same-species Taf1 paralog with demonstrated neuronal compensation after bounded search.

Exact non-target expression reach in the focal population was high: Taf1 was detected in 19,528 of 23,679 non-target nuclei, or 82.47%, with mean raw UMI 2.03 and mean CP10K 1.296 in `151 TH Prkcd Grin2c Glut`.

The same bundle raised the main downward uncertainty for an acute P16 CRISPR forecast: editing should stop new intact TAF1 supply, but it does not directly remove pre-existing TAF1 protein or promoter-bound TFIID assemblies. TAF1 protein turnover, TFIID residence time, and neuronal persistence over the 21-28 day P16-to-harvest interval were explicitly not established. Developmental Taf1 phenotypes and an XDP-like neural-lineage hypomorph support target importance, but they do not time acute postmitotic thalamic functional-stock loss.

### Training measurements

The declared focal count table contains 1,674 training perturbations and omits Taf1. Its distribution is sparse: 1,205 training targets had 0 FDR<0.05 genes, 469 were nonzero, the median was 0, the 90th percentile was 2, and the 95th percentile was 18. The high tail was real but rare: Uba5 had 2,677 DEGs, Tpr 1,768, Sin3a 1,433, Rnpc3 868, U2af2 828, Psmb4 742, and Hnrnpu 733.

I used the Parquet rows for `151 TH Prkcd Grin2c Glut` to inspect biologically adjacent transcriptional comparators. The closest available basal-transcription, Mediator, and Pol-related targets were compact rather than broad:

| comparator | n_degs at FDR<0.05 |
| --- | ---: |
| Taf1b | 0 |
| Gtf2h5 | 0 |
| Cdk8 | 0 |
| Med13l | 1 |
| Gtf2ird1 | 4 |
| Polr3b | 8 |
| Gtf2i | 10 |
| Med13 | 11 |
| Med23 | 13 |
| Med15 | 19 |
| Cdk13 | 56 |

The same Parquet slice showed that the Med13, Med15, and Med23 responses were mostly down-regulated thalamic state genes, while Gtf2i and Polr3b were similarly small. Packaged same-experiment Findings independently annotate those Mediator/Gtf2i profiles as selective, compact `151` responses and report convergence among Med13/Med15/Med23; these reports are semantic summaries of the same experiment, not an external replicate.

Larger transcriptional or chromatin regulators were treated as upper-context, not direct scale donors. Brd4, Setd1a, Sin3a, and U2af2 gave 311, 368, 1,433, and 828 focal DEGs, showing that this assay can capture large nuclear-regulator states in the same population. Their same-experiment Findings describe bromodomain/chromatin, Setd1a mitochondrial/proteostasis, Sin3a ER quality-control and splicing, or spliceosome/RNA-processing programs rather than a direct TFIID supply-loss state.

## Synthesis

Taf1 has stronger focal reach and central transcription-initiation biology than the all-training null baseline, so I did not place it at 0-1 DEGs. But the most operation-proximal measured perturbations were all sparse in the exact endpoint, and the target-specific functional-stock card made broad TFIID collapse by P37-P44 indeterminate rather than expected. The nearest numeric scale was therefore the low-double-digit Mediator/GTF2I group, with upward allowance for TAF1 centrality and downward allowance for pre-existing TFIID persistence and survivor conditioning.

I used `12` as the integer point: slightly above Med13/Gtf2i/Polr3b, below Med15/Med23/Cdk13 and far below the Brd4/Setd1a/Sin3a upper-context states.
