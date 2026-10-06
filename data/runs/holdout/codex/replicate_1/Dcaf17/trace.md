# Dcaf17 n_degs forecast

Target and endpoint: `Dcaf17` in `151 TH Prkcd Grin2c Glut`; `n_degs` counts measured genes with BH-adjusted Wilcoxon `p < 0.05` in this cell class.

## Evidence

- The declared target bundle characterizes acute P16 disruption of `Dcaf17` with harvest at P37-P44 in postmitotic mouse thalamic NeuN-positive nuclei. `Dcaf17` is detected in the exact focal non-target population, but at low abundance: mean 0.306 cp10k, mean raw UMI 0.480, and 8,578 of 23,679 cells expressing the transcript, or 36.2%.
- The same bundle places DCAF17 as a putative nuclear/nucleolar DCAF-family CRL4-DDB1 substrate receptor. The edited allele should stop new intact DCAF17 production, but pre-existing protein and assembled complexes are not directly erased; no DCAF17 protein half-life, CRL4-DCAF17 residence, or postmitotic-neuron persistence measurement was available. Mouse germline loss shows a postnatal testis phenotype and human biallelic variants cause Woodhouse-Sakati syndrome, but neither source times a P16-to-P37/44 thalamic neuron response.
- In the declared `151 TH Prkcd Grin2c Glut` training count table, the held-in distribution is sparse: 1,205 of 1,674 training perturbations have `n_degs = 0`, the median is 0, the 75th percentile is 1, the 95th percentile is 18, and only 59 perturbations have at least 50 DEGs.
- The closest represented CRL4/DCAF-side perturbations were quiet in the same endpoint. `Dcaf8` had 0 genes at BH `p < 0.05` with 165 matched perturbed nuclei; `Ddb2` had 0 with 215 matched perturbed nuclei. Same-experiment corpus Findings also summarize these as transcriptomic nulls at FDR < 0.10: `Dcaf8:F001` reports no downstream FDR-significant genes in 22 recovered groups, and `Ddb2:F001` reports no downstream genes in all 23 measured groups despite recovery of the `Ddb2` transcript itself.
- Broader ubiquitin-system perturbations likewise favored a near-null prior over a large stress response: `Ube3a = 0`, `Ube2e2 = 0`, `Wdr37 = 0`, `Wdr48 = 0`, `Rnf216 = 0`, `Rnf220 = 0`, `Trim37 = 1`, `Vcp = 2`, `Arih1 = 7`, `Usp48 = 10`, and `Wdr26 = 13` in this exact count table. Filtered Parquet rows confirmed these counts against the BH `p < 0.05` endpoint.
- `Psmb4` and `Psmc1` were large outliers at 742 and 430 DEGs, respectively, but the corpus describes them as constitutive 26S proteasome lesions that trigger proteasome bounce-back, heat-shock, integrated-stress, p53, redox, autophagy, and synaptic-repression programs. `Dcaf17` is instead a poorly resolved candidate substrate receptor with unknown neuronal substrate demand; `Psmb4:F008` explicitly notes that accessory proteostasis genes and E3/ubiquitin relatives including `Ube3a`, `Ube2e2`, `Usp48`, and `Vcp` did not reproduce the `Psmb4` program.

## Synthesis

The biology bundle establishes that some DCAF17 function could exist in the assayed population, so I did not treat the perturbation as a technical absence. The evidence nevertheless points to a sparse or null recovered RNA signature: transcript reach is modest, acute loss must wait for turnover of the relevant protein or complex pool, no physiological thalamic substrate is known, and the direct DCAF/CRL4 training analogs were complete nulls in the same assay. The high-count proteasome subunits are mechanistically too distal because they remove core degradation capacity and induce a broad proteotoxic state that was absent from several accessory ubiquitin-system perturbations.

Point prediction: `n_degs = 0`.
