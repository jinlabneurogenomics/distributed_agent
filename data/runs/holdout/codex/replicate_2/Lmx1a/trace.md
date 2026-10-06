# Lmx1a direct DEG-count forecast

Target: `Lmx1a`

Focal population: `151 TH Prkcd Grin2c Glut`

Predicted `n_degs`: `0`

## Evidence used

- The canonical `Lmx1a` biology bundle was outcome-blind: it exposed biology, focal expression reach, and functional-stock adjudication, but not the held-out `Lmx1a` expression signature or `n_degs`.

- Exact focal-population reach was essentially absent. In matched non-target nuclei from `151 TH Prkcd Grin2c Glut`, `Lmx1a` had `21` total UMIs across `23,679` nuclei, `19` expressing nuclei, `0.0802399%` expressing nuclei, mean raw UMI `0.0008869`, mean CP10K `0.0006364`, and pseudobulk CPM `0.05558`. That exact in-assay measurement superseded the qualitative expression priors for this forecast.

- The functional-stock card argued that Lmx1a is a renewable nuclear LIM-homeodomain transcription factor whose pre-edit protein stock should be substantially depleted over a P16-to-P37/P44 experiment in successfully edited, expressing cells. The same bundle also limited the transferability of prior phenotypes: isolated Lmx1a loss evidence is developmental, combined Lmx1a/Lmx1b postmitotic evidence was from midbrain dopaminergic neurons, and Lmx1b compensation has not been tested in postnatal thalamic neurons. Thus the edit should be realized where the factor is made, but the biology bundle did not supply a reason to expect an isolated thalamic maintenance program in the nearly Lmx1a-negative `151` population.

- The focal-class training count table was zero-inflated: among `1,674` training perturbations, `1,205` had `n_degs = 0`; the median was `0`, the 75th percentile was `1`, the 90th percentile was `2`, the 95th percentile was `18`, and the mean was `14.05` because a small tail reached thousands of DE genes.

- Annotation-backed analog nomination against the actual training universe placed `Lmx1b`, `En1`, `Otx2`, `Pitx3`, `Neurod1`, `En2`, `Foxa2`, and `Sox2` as the leading specific comparators, all sharing the bounded `WP_DOPAMINERGIC_NEUROGENESIS` module before broader transcription-factor or signaling fallbacks entered. The same-experiment explicit-Finding topology connected `Lmx1b`, `En1`, `Otx2`, `Pitx3`, `En2`, and `Foxa2` into one fully connected developmental module, so these were a coherent comparator neighborhood rather than a symbol-prefix selection.

- The measured `151 TH Prkcd Grin2c Glut` burdens for those eight leading comparators were `0`, `0`, `0`, `0`, `0`, `0`, `0`, and `2` DE genes. A direct Parquet aggregation in the focal group confirmed the same counts over `17,259` measured genes for each of the first twenty analogs. Broader top analogs were also mostly silent: the top 20 had 16 zeros and median `0`; the nonzero outlier `Ctnnb1` had `383` DE genes but came from a broad Wnt/neuron-differentiation fallback rather than the Lmx1a/Lmx1b dopaminergic-development module.

## Reasoning

`n_degs` is an aggregate BH-adjusted Wilcoxon count over all recovered nuclei assigned to the focal class. Because `Lmx1a` was detected in only `0.08%` of matched non-target nuclei, most perturbed nuclei in this class should have no ongoing Lmx1a-regulated program to lose; any effect in a very rare expressing subpopulation would be diluted across the class aggregate and across the 17k-gene multiple-testing burden.

The target is a transcription factor with a plausible realized knockout window, which could have argued for a sizeable footprint if it were broadly active. The focal expression measurement and comparator measurements pushed the other way: the closest training-available Lmx1a/Lmx1b-developmental factors were overwhelmingly `0` in the same high-yield class, while the nonzero analogs were broader signaling/chromatin fallbacks with weaker context specificity. I therefore treated zero DE genes as more likely than a small positive tail count and used the point forecast `0`.
