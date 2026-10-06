# Direct Chrnb4 forecast for 151 TH Prkcd Grin2c Glut

## Prediction

Predicted `n_degs`: **0**

## Evidence used

- **Held-out target and context.** The declared one-row holdout manifest names `Chrnb4`; the requested context is the exact atlas class `151 TH Prkcd Grin2c Glut`.

- **Exact focal-population reach from the biology-only bundle.** `Chrnb4` is technically available as a measured feature in the focal class, but its baseline reach in matched non-target cells is extremely small: 42 expressing nuclei among 23,679 non-target nuclei, or 0.177%, with `mean_raw_umi = 0.0019004`, `mean_cp10k = 0.0012879`, and only 45 total target UMIs across the matched non-target nuclei. This supersedes the qualitative thalamic-expression prior for the aggregated class.

- **Functional realization prior.** The source card and functional-stock adjudication support an effect on a real neuronal nicotinic acetylcholine receptor: beta4 is a pentameric ligand-gated cation-channel subunit; a disruptive edit should stop new beta4 production; and beta4-containing native receptors plausibly turn over over the P16-to-P37/P44 window. The same card keeps uncertainty because the closest turnover evidence is not juvenile thalamic neurons, because pre-existing assembled channels initially persist, and because alternative beta subunits could partially buffer some contexts.

- **Anatomical dilution.** The strongest expression evidence localizes beta4 to the ventral medial habenula/interpeduncular system inside the broader diencephalic territory, not across most nuclei that are aggregated into `151 TH Prkcd Grin2c Glut`. Thus any true beta4-dependent response should be confined to a very small subset of the recovered thalamic neurons used by the DE contrast.

- **Training count base rate.** In the declared `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` table, 1,205 of 1,674 training perturbations have zero DEGs and 1,512 of 1,674 have two or fewer DEGs. The median is 0 and the 90th percentile is 2, so a count of 0 is the modal outcome for this class.

- **Mechanistically chosen receptor comparators.** I chose the measured cholinergic receptor/signaling perturbations as the closest empirical neighborhood available in the training table, rather than high-yield ubiquitous genes. Their exact `151 TH Prkcd Grin2c Glut` counts were:

  `Chrna2 = 0`, `Chrna3 = 0`, `Chrna4 = 2`, `Chrna6 = 0`, `Chrna7 = 0`, `Chrnb1 = 0`, `Chrnb2 = 1`, `Chrnb3 = 0`, `Chrm2 = 0`, `Chrm3 = 0`, `Ache = 1`.

- **Parquet profile check.** The full expression parquet for those same 11 training perturbations contained 17,259 focal-class genes per perturbation. Eight had no BH-significant genes. The nonzero cases had only isolated down-regulated features: `Ache` had only self-target `Ache`; `Chrnb2` had only self-target `Chrnb2`; and `Chrna4` had self-target `Chrna4` plus `Cyp46a1`. No broad acetylcholine-receptor response module appeared in the inspected profiles.

## Reasoning

The evidence supports Chrnb4 as a functional perturbation in cells that depend on beta4-containing receptors, but the target's exact measured reach in the aggregated focal class is so low that a cell-autonomous response would be diluted below genome-wide BH detection. The closest available perturbations of nicotinic and muscarinic acetylcholine-receptor biology are themselves nearly silent in this same class, and their few significant calls are mostly self-transcript reductions from more readily expressed genes. Because `Chrnb4` has only 45 baseline UMIs across 23,679 matched control nuclei, even a self-target call is unlikely to survive multiple testing.

I therefore place `Chrnb4` in the zero-DEG mode of the training distribution for this focal population. The main uncertainty is that a tiny medial-habenula subset could in principle mount a strong downstream state if beta4 receptor loss were highly consequential there, but the requested readout averages over recovered thalamic neurons and the declared biology bundle does not provide evidence for a broad postnatal transcriptional program within 21-28 days.
