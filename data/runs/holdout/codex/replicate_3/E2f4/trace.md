# Direct n_degs forecast for E2f4 in 151 TH Prkcd Grin2c Glut

Target and endpoint:

- Target perturbation: `E2f4`
- Cell group: `151 TH Prkcd Grin2c Glut`
- Endpoint: number of measured genes in this cell group with BH-adjusted Wilcoxon `p < 0.05`

Evidence used:

- The prediction-safe E2f4 biology bundle reports exact in-assay target expression in the focal non-target cells: 16,619 of 23,679 nuclei expressed E2f4, 70.1846% expressing, mean CP10K 0.8554, and pseudobulk CPM 84.4144. Thus the target RNA is present in this population, but expression reach alone does not establish either efficient functional editing or downstream dependence.
- The same bundle places E2F4 in E2F-DP/p107/p130 transcriptional complexes. It adjudicates functional stock by harvest as `partially_depleted_or_leading_edge`: a P16 disruptive edit should stop new E2F4 production and deplete unstable free protein, but p107/p130-bound E2F4 can be stabilized and the protected neuronal pool has no measured 21-28 day residence time.
- The loss evidence for E2f4 is mainly embryonic or systemic: ventral-telencephalon/neural-precursor phenotypes and neonatal systemic lethality. The card did not find a timed postnatal thalamic-neuron loss phenotype and explicitly leaves postnatal relevance unresolved. It also flags E2f5 as a partially overlapping paralog outside the assayed neuronal context.
- Same-experiment packaged E2F/DP context is quiet. The high-confidence Claim `claim:e16a32bdeefb0be7da9d` states that single perturbations of represented E2F/DP family members did not engage a coordinated canonical G1/S, replication, mitotic, or apoptotic nuclear transcriptomic program in settled postnatal neurons. Its contributing represented family targets were E2f1, E2f5, Tfdp1, and Tfdp2.
- The declared `151` count table matches that interpretation: `E2f1 = 0`, `E2f5 = 0`, `Tfdp2 = 0`, and `Tfdp1 = 2` DEGs. Adjacent MYC/cell-cycle comparators were also essentially flat in this cell class: `Myc = 0`, `Mycn = 0`, `Cdkn2a = 0`, and `Mga = 2`.
- A symmetric profile comparison over `E2f1`, `E2f5`, `Tfdp1`, `Tfdp2`, `Myc`, `Mycn`, `Cdkn2a`, and `Mga` in the same `151` class found six of eight profiles with no significant features and the other two with only 1-9 significant features. The only E2F/DP significant calls were the two Tfdp1 genes, `Cntrob` and `Dcaf15`, so there was no shared significant E2F/DP module to transfer to E2f4.

Reasoning:

The focal neurons express E2f4 often enough that a strong cell-autonomous transcriptomic dependency should have been observable. However, the expected knockout is biologically muted by partial persistence of stabilized E2F4 complexes, possible E2F5 overlap, and absence of a demonstrated postnatal thalamic requirement. More importantly for the requested RNA endpoint, the closest measured E2F/DP perturbations in the exact same cell class had counts of 0, 0, 0, and 2 and lacked the canonical cell-cycle or apoptotic program that would be the main high-count E2F4 loss signature.

I therefore put E2f4 at the mode of its nearest measured E2F/DP neighborhood rather than near the long right tail of the whole training table.

Point prediction: `0`
