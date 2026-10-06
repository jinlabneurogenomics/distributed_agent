# Direct forecast trace

## Target and endpoint

- Target manifest: `Naa20`
- Endpoint: number of measured genes in `151 TH Prkcd Grin2c Glut` with BH-adjusted Wilcoxon `p < 0.05`

## Evidence used

- The declared `151 TH Prkcd Grin2c Glut` training count table contains 1,674 observed biological perturbations and is extremely zero-inflated: 1,205 are zero, the median is 0, the 75th percentile is 1, the 90th percentile is 2, and only 43 have at least 100 DE genes. The target `Naa20` is absent from this table.
- The declared `Naa20` biology bundle reports direct target reach in the focal population: Naa20 is detected in 21,132 of 23,679 non-target thalamic glutamatergic nuclei, 89.24% expressing, with mean raw UMI 2.82 and pseudobulk 176.44 CPM.
- The same bundle adjudicates the P16-to-P37/P44 loss as likely functionally realized: Naa20 and its Naa25 NatB partner are renewable protein pools with days-scale turnover, and most adult-thalamic proteins with measured turnover should renew the majority of their pre-edit molecules over a 21-28 day interval. The bundle also emphasizes residual uncertainty: the best direct mouse knockout timing is fibroblast, the best neural evidence is human CRISPRi or human genetics, and no acute postnatal mouse thalamic-neuron Naa20 loss experiment was found.
- NatB biology gives a reason to expect a protein/acetylome perturbation but not necessarily a large nuclear RNA state. Naa20 catalyzes NatB N-terminal acetylation of a broad nascent-protein substrate class, and an edit blocks new NatB activity without removing N-terminal acetylation already installed on surviving substrate molecules.
- The selected same-experiment corpus has no `Naa20` Findings, Claims, or explicit references, but it contains the nearby observed NAT-family catalytic perturbation `Naa10`. `Naa10:F001` reports a pan-neuronal FDR-level transcriptomic null across 22 measured neuronal groups, and `Naa10:F002` reports no compensatory NAT-family, integrated-stress, apoptosis, proteasome, or ubiquitin rebound program at FDR < 0.10.
- I checked the training Parquet for `151 TH Prkcd Grin2c Glut` rows for the relevant observed comparators. `Naa10` had 17,259 measured genes, 0 DE genes at both FDR < 0.05 and FDR < 0.10, and a minimum adjusted p-value of 1.0. In the same cell class, responsive protein-homeostasis comparators were readily detectable when they created a nuclear RNA state: `Psmb4` had 742 DE genes, `Psmc1` had 430, `Ufc1` had 572, `Uba5` had 2,677, and `Eef2` had 9.

## Synthesis

I upweighted `Naa20` above an unexpressed or stock-protected target because it is broadly present in the focal thalamic population and should lose a substantial fraction of renewable NatB capacity by harvest. I did not convert that to a broad DEG burden, because the endpoint is survivor-conditioned nuclear RNA rather than an N-terminome or protein-stability readout, the direct mouse Naa20 phenotypes are either proliferating-cell or developmental evidence, and the closely analogous N-terminal acetyltransferase target `Naa10` was transcriptionally flat in this exact assay family. The local count prior is also dominated by zero or one-gene outcomes, so the biology supports possible observability but not enough to move the point estimate above zero.

Predicted `n_degs`: 0
