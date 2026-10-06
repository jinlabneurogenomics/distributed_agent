# Nfkb2 direct DEG-count prediction

## Prediction

`Nfkb2` is predicted to have **0** BH-FDR-significant DEGs in `151 TH Prkcd Grin2c Glut`.

## Evidence used

- **Target and focal population.** The declared holdout manifest and the canonical biology bundle both name `Nfkb2`. The focal population is the exact `151 TH Prkcd Grin2c Glut` thalamic glutamatergic neuronal class.
- **Endpoint.** The requested scalar is the count of measured genes in this class with Wilcoxon BH-adjusted `p < 0.05`.
- **Target expression reach.** In matched non-target cells for `151 TH Prkcd Grin2c Glut`, `Nfkb2` is detected in 301 of 23,679 nuclei, or 1.271% of nuclei, with mean raw UMI 0.0138 and pseudobulk 0.863 CPM. The feature is present, but focal reach is extremely sparse.
- **Functional-stock prior.** The Nfkb2 card adjudicates that the CRISPR edit should stop resupply of both p100 and p52 and that NFKB2 functional stock is likely substantially depleted over the P16 to P37/P44 interval. This supports biological realization of loss of function, but not a strong focal transcriptional effect by itself.
- **Neural observability prior.** The same biology bundle finds no postnatal thalamic or other matched neuron-specific Nfkb2 loss experiment. The closest causal mouse phenotype is germline/systemic and immune-focused, CNS expression is only a broad annotation, and Nfkb1 redundancy is documented in non-neural lineages rather than postmitotic thalamic neurons.
- **Training count distribution.** The declared `151 TH Prkcd Grin2c Glut` training table has 1,674 labeled perturbations. It is zero-heavy: 1,205 targets, or 71.98%, have zero DEGs; the median is 0; the 75th and 80th percentiles are 1; only 11.53% of targets have at least 2 DEGs and only 7.89% have at least 5.
- **Training pathway comparators.** The assayed NF-kappaB-adjacent training entries that were labeled in the same table are all transcriptionally quiet in this class: `Nfkb1`, `Rel`, `Chuk`, `Traf3`, and `Nod2` each have 0 DEGs.
- **Same-experiment corpus.** The selected packaged corpus has no report Findings, Claims, or explicit comparator references for `Nfkb2`, so it did not add a same-experiment semantic reason to move the estimate upward.

## Synthesis

The target should be functionally perturbed by harvest, so the estimate is not forced to zero by persistence of the protein pool. The endpoint, however, is a survivor-conditioned snRNA-seq DEG count in a thalamic glutamatergic population where `Nfkb2` is barely expressed at baseline. The biology bundle does not provide matched evidence that noncanonical NF-kappaB maintenance is a strong driver of postmitotic thalamic transcription, while immune/systemic mouse phenotypes and non-neural Nfkb1 redundancy are too context-mismatched to imply a broad neuronal expression footprint.

Against the count table, this places `Nfkb2` with the many low-visibility signaling/regulatory perturbations rather than with the rare high-burden chromatin, splicing, proteostasis, or ion-homeostasis outliers. The direct NF-kappaB pathway training entries being 0-DEG observations in the same focal class further make a 0 or 1 count more plausible than the long-tailed training mean. I therefore choose the mode and median of the compatible low-response region:

```tsv
target_name	predicted_n_degs
Nfkb2	0
```
