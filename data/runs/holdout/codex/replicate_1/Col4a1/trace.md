# Direct DEG-count forecast for Col4a1

## Target and endpoint

- Target: `Col4a1`
- Focal population: `151 TH Prkcd Grin2c Glut`
- Endpoint: count of measured genes with Wilcoxon BH-adjusted `p < 0.05`
- Declared training table: 1,674 non-held-out perturbations for this focal class

`Col4a1` was absent from the focal-class training count table, so the forecast did not use the withheld Col4a1 DEG count or signature.

## Quantitative training evidence

The visible focal-class count distribution was heavily zero-inflated: 1,205 of 1,674 training perturbations had `n_degs = 0`, 469 had any DEG, the median was 0, the 75th percentile was 1, the 90th percentile was 2, and the mean of 14.05 was driven by a small high-response tail whose largest counts were spliceosome, proteostasis, RNA-processing, transcriptional-regulatory, and signaling/chromatin targets.

The training perturbations closest to a collagen IV basement-membrane operation were quiet in this same thalamic class:

- The two visible collagen-family perturbations were both zero: `Col11a1 = 0`, `Col2a1 = 0`.
- A strict ECM-receptor annotation slice contained 16 training targets and only two single-DEG counts; direct members `Dag1`, `Reln`, `Itgb1`, `Itga2`, `Itga2b`, `Itga4`, `Itga6`, `Itga7`, `Itga8`, and `Itga9` were all zero.
- A basement-membrane annotation slice contained 16 training targets and only four single-DEG counts; `Dag1`, `Itgb1`, `Itga6`, and `Col2a1` were zero.
- The focal Parquet rows for an 18-gene matrix/adhesion panel confirmed the count-table values over 17,259 measured features per perturbation: only `Adam22` and `Timp3` had one FDR-significant feature; `Adam10`, `Adamts17`, `Col11a1`, `Col2a1`, `Cspg4`, `Dag1`, `Itga2`, `Itga2b`, `Itga4`, `Itga6`, `Itga7`, `Itga8`, `Itga9`, `Itgb1`, `Itgb2`, and `Reln` each had zero.

Packaged same-experiment Findings, used only as interpretations of training perturbations already present in the count table or Parquet, reinforced that this was not a thalamus-only accident: `Dag1` was an FDR-defined null across 22 recovered neuronal groups; `Itga2` was transcriptomically silent at FDR < 0.10 in every sampled neuronal group; `Itgb1` had zero downstream genes at FDR < 0.10 in 21 recovered neuronal groups; `Col11a1` produced no FDR < 0.10 downstream transcriptome in any measured postnatal NeuN+ group; and `Col2a1` had only two downstream FDR < 0.10 genes across all 23 groups.

## Col4a1 biology

The Col4a1 biology bundle established exact focal-population transcript reach: `Col4a1` was measured in the non-target `151 TH Prkcd Grin2c Glut` nuclei, with mean raw UMI 2.43, mean CP10K 1.52, and expression in 74.9% of 23,679 non-target nuclei. Thus the target RNA itself was present and a perturbation could in principle be observed in the focal assay.

The functional-stock card discounted immediate cell-autonomous transcriptome entry. COL4A1 is a secreted structural chain in the alpha1-alpha1-alpha2 type IV collagen network of basement membrane; the relevant product is an installed extracellular structure. The bundle adjudicated the network as substantially installed before P16 editing, with disruptive CRISPR expected to stop new edited-cell supply but not directly dismantle pre-existing extracellular heterotrimers. Postnatal cerebral-vessel tracking supports partial turnover over the P16-to-P37/P44 interval, but the card also noted that the closest turnover evidence is vascular rather than a direct selective thalamic-neuron loss test and that adult brain atlas evidence places the principal Col4a1 source in vascular/perivascular cells rather than neurons.

## Synthesis

The exact Col4a1 expression reach raised the forecast above a generic unexpressed-ECM null: the transcript is present in this thalamic population, so one self-feature or a very small local response is plausible. I still forecast the mode of the strict count as zero because the requested endpoint requires BH-significant nuclear RNA changes among recovered neurons, while Col4a1's operative stock is extracellular and pre-installed, its renewal and source-cell coupling are only partially matched to edited thalamic neurons, and the visible collagen, dystroglycan/Reelin, and integrin/focal-adhesion perturbations overwhelmingly produced zero or singleton counts in this assay.

Point prediction: `0`.
