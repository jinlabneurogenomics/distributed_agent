# Zfhx3 n_degs forecast

Target and endpoint:

- Target: `Zfhx3`, from the declared one-row holdout manifest and matched `biology_bundles/Zfhx3.json`.
- Focal population: `151 TH Prkcd Grin2c Glut`.
- Endpoint: `n_degs`, the number of measured genes in this class with Wilcoxon `pvals_adj < 0.05`.

Target biology used:

- The prediction-safe Zfhx3 bundle reports exact focal-class expression: 16,679 of 23,679 non-target nuclei expressed `Zfhx3` in `151 TH Prkcd Grin2c Glut`, or 70.44%, with mean log1p(CP10K) 0.540.
- The same bundle adjudicates Zfhx3 functional stock as `likely_substantially_depleted` by the P37-P44 harvest window: the evidence is strongest for adult SCN, where postnatal Zfhx3 deletion can eliminate detectable neural ZFHX3 protein on a shorter time scale than the 21-28 day Perturb-seq interval.
- I treated those facts as evidence that the CRISPR perturbation is biologically plausible in an expressing postmitotic neuron, but not as evidence that thalamic loss must reproduce the adult-SCN circadian phenotype.

Training measurements used:

- The declared training table for `151 TH Prkcd Grin2c Glut` contains 1,674 observed perturbations. It is highly zero-inflated: 1,205/1,674 have `n_degs = 0`, the median is 0, the 75th percentile is 1, the 90th percentile is 2, the 95th percentile is 18, and only 59/1,674 reach at least 50 DE genes.
- I selected a small biology-matched training panel before looking at their focal-class counts: the closest assayed Zfhx-family member; clock or clock-adjacent regulators suggested by the SCN Zfhx3 prior; and neuronal TF/chromatin regulators that test whether a postnatal transcriptional regulator automatically gives a broad recovered-nucleus signature.
- The selected training counts span the full zero-inflated pattern rather than a single high-response stratum:

```tsv
target	n_degs
Zfhx2	0
Clock	3
Bmal1	103
Nr1d1	116
Nr1d2	1
Rora	278
Rorb	0
Rorc	0
Arnt	0
Tcf4	0
Mef2c	1
Satb2	0
Chd7	0
Chd8	61
Crebbp	8
Ep300	0
Setd5	9
```

- I checked the same rows in the declared Parquet, restricted to `151 TH Prkcd Grin2c Glut`; every count above matched `sum(pvals_adj < 0.05)` over the focal-class differential-expression rows.
- A run-local profile comparison of those 17 training perturbations gave 8 nodes with no significant focal-class genes, 5 with only 1-9 significant genes, and 4 with at least 50. This made the high Bmal1/Nr1d1/Rora branch a possible but non-dominant exception rather than the base expectation for an unrelated AT-motif factor.

Same-experiment corpus used as interpretation:

- Zfhx2, the only assayed Zfhx-family member in the training count table, was essentially buffered in this experiment: its report-level Finding ledger records only one weak FDR<0.10 downstream hit in a different cortical/olfactory glutamatergic class, no detected central-brain recovery of its DRG pain/neuropeptide program, near-zero data-driven neighbors, and no mRNA rebound of `Zfhx3` or `Zfhx4`.
- Rora, Bmal1, Nr1d1, and Clock show that the thalamic class can report clock-related transcriptional perturbations when the perturbed factor is wired into that state. However, the same ledger emphasizes that the branch is specific: Rorb/Rorc failed to phenocopy Rora, Clock was only a sparse phenocopy of Bmal1, and Rora diverged from Bmal1/Nr1d1 despite partial clock-branch overlap.
- These Findings are packaged interpretations of the same Perturb-seq experiment, not independent replication of the count table.

Synthesis:

- The Zfhx3 edit should be realized in many target-expressing 151-TH nuclei, so I did not demote the target as unexpressed or persistent-stock protected.
- The evidence for a functional loss is still anchored outside thalamus, and the best same-family training perturbation, Zfhx2, has no focal-class FDR<0.05 hits despite adequate recovered perturbed nuclei.
- High-count clock and nuclear-receptor comparators are too pathway-specific to transfer wholesale to Zfhx3: nearby family or branch members can be flat, and the focal signatures of Bmal1, Clock, Nr1d1, Nr1d2, Rora, Rorb, and Rorc are very uneven.

Point forecast: the modal outcome for a thalamic transcription-factor perturbation with this evidence mix is still no detected focal-class DE genes. I therefore predict `n_degs = 0` for `Zfhx3`.
