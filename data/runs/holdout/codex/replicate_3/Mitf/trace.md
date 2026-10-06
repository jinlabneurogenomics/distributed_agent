# Direct held-out DEG-count prediction for Mitf

## Target and endpoint

- Requested endpoint: `n_degs` in `151 TH Prkcd Grin2c Glut`, counted as measured genes with BH-adjusted Wilcoxon `p < 0.05`.
- Manifest target: `Mitf`.
- Direct target outcome/signature: not used.

## Target biology from the declared bundle

- The screen label `Mitf` maps here to the packet target Entrez Gene 667838, official symbol `Naip3`, with `Mitf` as an alias; I therefore treated it as a Naip-locus pseudogene edit rather than as the microphthalmia-associated transcription-factor gene.
- The source card establishes pseudogene status: NCBI classifies Gene 667838 as `Naip3`, and mouse genomic analysis found no `Naip3` cDNA plus a missing exon-10-equivalent region predicted to frameshift an exon-9-to-exon-11 transcript.
- The exact focal-population non-target expression reach is low but present: `Mitf` is available as a feature in `151 TH Prkcd Grin2c Glut`, with mean CP10K 0.113160498, mean raw UMI 0.188648169, pseudobulk CPM 11.823249737, and expression in 3,740 of 23,679 non-target nuclei, or 15.7945859%.
- Functional-stock adjudication is indeterminate: there is no established protein product or pre-edit protein stock to track through P16 to P37-P44, but a possible uncharacterized regulatory RNA was not affirmatively excluded.
- The observability card found no `Naip3`-specific mouse loss phenotype, no postnatal thalamic or neural perturbation evidence, and only an official spinal-cord expression annotation as the nearest neural context. Functional `Naip1`, `Naip2`, `Naip5`, and `Naip6` paralogs exist in C57BL/6, but their macrophage/epithelial innate-immune roles are not evidence for a thalamic `Naip3` molecular stock.

## Training measurements used

- The focal-class training count table has 1,674 observed biological targets. Its distribution is strongly zero-inflated: 1,205/1,674 targets are exactly 0, the median is 0, 1,481/1,674 are `<=1`, and 1,546/1,674 are `<=5`. The arithmetic mean is 14.05 only because of a small high-burden tail.
- The declared training parquet filtered to `151 TH Prkcd Grin2c Glut` contains the same 1,674 training targets by 17,259 measured genes. It contains no `Mitf`, `Naip*`, or `Safe_target_*` focal rows, so the focal training data provide neither a close measured paralog nor a safe-control row for this target.
- I used the count table to inspect a weak boundary cohort of innate-immune or non-neuronal receptor targets whose biology is closer to the Naip-locus card than the chromatin, spliceosome, proteasome, and synaptic targets in the high tail. All of the following focal-class training targets had `n_degs = 0`: `C3`, `Ccr2`, `Cd14`, `Cd3d`, `Cd3e`, `Cd3g`, `Cd4`, `Cd79a`, `Cd79b`, `Cd80`, `Ifnar1`, `Ifnar2`, `Ifngr1`, `Ifngr2`, `Il10ra`, `Il12b`, `Il12rb1`, `Il17ra`, `Il17rd`, `Il1r1`, `Il1rap`, `Il2ra`, `Il2rb`, `Il2rg`, `Il4ra`, `Il6ra`, `Tlr2`, `Tlr3`, `Tlr4`, `Tlr5`, `Tlr7`, `Tlr8`, `Tnfrsf1a`, `Tnfrsf4`, and `Tnfrsf9`.
- Direct parquet checks in the same focal class confirmed that each of those 35 boundary targets had 17,259 tested genes and zero adjusted-significant genes at `pvals_adj < 0.05`. Their matched perturbed-nucleus counts ranged from 89 to 239 against the same 23,679 matched controls, so the zero counts were not a missing-profile artifact.

## Synthesis

The held-out edit has low but real transcript reach in the focal population, so I did not treat absence of expression as a mechanical null. The decisive feature is instead the operation: this packet targets a well-supported `Naip3` pseudogene, not a known thalamic neuronal protein or a transcriptional regulator. The target bundle leaves room for an unrecognized RNA or locus effect, which makes `1` plausible, but there is no established operative stock, loss phenotype, or matched thalamic function to connect the edit to the heavy-tail response programs seen for essential chromatin, splicing, proteostasis, or ion-transport targets.

Given the 72% zero rate among all focal training perturbations, the lack of a measured close paralog, the uniformly zero observed response of immune/receptor boundary targets in the same focal class, and the pseudogene adjudication, I used the distribution's point mass at zero rather than the high-tail mean as the point forecast.

Predicted `n_degs`: 0
