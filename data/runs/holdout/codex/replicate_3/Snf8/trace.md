# Snf8 direct DEG-count forecast

## Declared target and endpoint

- Target: `Snf8`
- Cell class: `151 TH Prkcd Grin2c Glut`
- Endpoint: `n_degs`, the number of measured genes with BH-adjusted Wilcoxon `pvals_adj < 0.05` in the focal class.

## Evidence used

The biology bundle supports target engagement as possible in the assay window but not guaranteed to make a broad nuclear RNA state. Snf8 is expressed in the exact focal population, with 16,160 of 23,679 non-target nuclei expressing it, 68.246% expressing cells, mean log1p CP10K 0.505, and pseudobulk CPM 80.20. The source card places Snf8 in ESCRT-II-mediated endosomal cargo sequestration and MVB formation; the functional-stock adjudication calls the operative entity a dynamic complex component and concludes that stock is likely substantially depleted by the P37-P44 harvest. The same bundle also leaves important downward/uncertainty terms: no acute postmitotic thalamic timing anchor was found, the closest phenotypes are developmental or human-genetic, and survivor conditioning could attenuate the recovered transcriptome.

The training count table for this same class is very sparse. Among 1,674 training perturbations, 1,205 have `n_degs = 0`; the median is 0, the 75th percentile is 1, and the 90th percentile is 2. Counts above tens of genes are a heavy tail rather than the central regime.

Curated pathway membership did not expose a direct ESCRT-II training analogue. Snf8 is the only perturbed target in the ESCRT-II CORUM set, and the Reactome ESCRT target set contributes only `Chmp4b` and held-out/absent ESCRT nodes as task-relevant neighbors. In the focal training count table:

| comparator class | training genes | focal `n_degs` |
| --- | --- | --- |
| Reactome ESCRT / MVB-adjacent exact hits | `Chmp4b`, `Rab27a` | `0`, `0` |
| KEGG endocytosis genes present in training | 28 targets including `Chmp4b`, `Cltc`, `Hspa8`, `Vps35`, `Rab7`, `Washc4` | median 0; 18/28 zero; only `Rab7` is very broad |
| Reactome membrane-trafficking genes present in training | 74 targets | median 0; 75th percentile 1; 90th percentile 1.7 |
| macroautophagy targets overlapping Snf8 GO biology | `Atg16l1`, `Atg5`, `Becn1`, `Map1lc3a`, `Myo5a`, `Rab3gap2`, `Sqstm1`, `Vcp`, `Vps13a`, `Vps13c`, `Vps41` | all 0-2 |

The same-experiment corpus made the upper-tail comparators interpretable rather than directly transferable. `Rab7` produced a broad late-endosomal/lysosomal, sterol, ISR/UPR, autophagy, proteasome, and synaptic-remodeling state in the 151 thalamic class, but it is a stronger late-endosome lesion than ESCRT-II cargo sorting. `Vps35` and `Vps54` were more modest 151-restricted trafficking responses, while `Chmp4b` did not form a robust ESCRT/autophagy/cargo signature.

The 151-only profile comparison of 20 endolysosomal and autophagy-adjacent training perturbations likewise separated a few broad stress profiles from many quiet neighbors. Eleven of the 20 had zero significant 151 genes. `Chmp4b` had no positive or negative significant features and only near-zero whole-profile similarity to `Rab7`, `Vps35`, `Vps54`, `Dctn1`, `Tsc2`, `Wdfy3`, `Vps41`, `Vps53`, or `Atp6ap2`; its cosine values to those peers ranged from -0.062 to 0.032. `Vps35` had 17 FDR<0.05 genes and `Vps54` had 31, but their similarity to one another was also weak, consistent with related trafficking perturbations producing branch-specific rather than interchangeable transcriptional outputs.

## Synthesis

The focal expression and lack of a known close paralog argue against an automatic zero for Snf8. However, the closest measured ESCRT/MVB, macroautophagy, and membrane-trafficking perturbations in this exact cell class are mostly quiet, and the broad `Rab7`/`Dctn1`/`Tsc2` stress regime requires a downstream lysosomal/sterol state that is not established for ESCRT-II loss in 21-28 days of sparse postnatal neuronal editing. I therefore place Snf8 just above the training median and exact ESCRT neighbor, but still in the low-count regime rather than near the `Vps35`/`Vps54` anchors.

Predicted `n_degs`: 2
