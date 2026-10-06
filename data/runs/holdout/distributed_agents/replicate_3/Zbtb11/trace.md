# Zbtb11 DEG-count prediction

## Question and interpretation

The held-out manifest for this run contains one perturbation, `Zbtb11`. I interpreted the endpoint as the number of measured genes in `151 TH Prkcd Grin2c Glut` whose `pvals_adj` in the perturbed-vs-control Wilcoxon test is strictly below 0.05. The row in `answer.txt` is therefore a count-like point estimate for the hidden `151 TH Prkcd Grin2c Glut` Zbtb11 CRISPR loss-of-function profile, not a score for ZBTB11 importance or a count of direct ZBTB11 binding targets.

Two ambiguities mattered:

- The experiment is an acute, sparse, postnatal neuronal CRISPR assay with partial average target-RNA depletion, so I did not transfer full germline, embryonic, tumor-cell, or hematopoietic knockout phenotypes literally.
- The Zbtb11 perturbation and its expression signature are completely held out. I used `Zbtb11` biology to pick measured training perturbations, then used their actual same-assay DEG counts to calibrate the breadth.

## Sources used

- `training_de_all_cell_groups.parquet`: all non-held-out differential-expression profiles. I filtered this table by `group_name == "151 TH Prkcd Grin2c Glut"` for focal counts and by selected `gene_target` values for the comparator profiles.
- `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`: the observed focal endpoint for 1,674 training perturbations.
- Distributed Agents same-experiment corpus, release `perturbai-july-260713-sourceguard-1773-v1`. `target_context(Zbtb11)` and `related_targets(Zbtb11)` had no Zbtb11 entry or explicit same-corpus edges; I therefore used the corpus mainly to vet the strong same-family comparator `Zbtb7a`. Its Zbtb7a findings report a broad 22-of-23-group neuronal response, lysosome/GPCR-sorting and synaptic-remodeling components, nearest FDR-backed `Uba5`/`Ufc1`/`Tpr` proteostasis neighbors, and poor phenocopy by canonical LRF/BCL11A/NuRD or ARF/TP53/MYC partners.
- Distributed Agents runtime profile comparison over the training parquet. I compared a hand-picked Zbtb11 analog/boundary cohort: `Zbtb7a`, `Nrf1`, `Esrra`, `Polr3b`, `Ddx3x`, `Ndufs2`, `Ndufa10`, `Ndufb8`, `Opa1`, `Nop56`, `Myc`, `Trp53`, `Ppargc1a`, `Uba5`, `Ufc1`, `Setd1a`, and `Sin3a`. This supplied significant-feature counts, top-feature overlap, and whole-profile similarities among the observed comparators.

I also used PubMed literature on ZBTB11:

- Wilson et al. 2020, Nature Communications, DOI `10.1038/s41467-020-19205-x`, PMID `33122634`: ZBTB11 cooperates with NRF-2/GABP, binds promoters of nuclear genes involved in complex I biogenesis and the mitoribosome, and its genetic inactivation impairs complex I assembly and mitochondrial respiration.
- Sumathipala et al. 2022, Brain, DOI `10.1093/brain/awac034`, PMID `35104841`: biallelic human ZBTB11 variants cause a neurodevelopmental disorder with brain abnormalities; ZBTB11 ChIP-seq in fibroblasts found promoter binding enriched for mitochondrial and RNA-processing genes, including `ACSF3`.
- Garipler et al. 2022, Cell Reports, DOI `10.1016/j.celrep.2022.110524`, PMID `35294876`: ZBTB11 and ZFP131 maintain embryonic stem-cell pluripotency by repressing pro-differentiation genes.
- Keightley et al. 2017, Nature Communications, DOI `10.1038/ncomms14911`, PMID `28382966`: Zbtb11 is a PU.1 target in granulopoiesis and links to Tp53 repression in that lineage.
- Cao et al. 2023, Blood Advances, DOI `10.1182/bloodadvances.2022009580`, PMID `37567157`: hematopoietic Zbtb11 deletion causes fetal hematopoietic failure with oxidative-phosphorylation down-regulation.

## Same-dataset calibration

The focal training endpoint is sparse: 1,205 of 1,674 training perturbations have zero DEGs, the median is 0, the 75th percentile is 1, and the 95th percentile is 18. I therefore needed positive evidence to call any nonzero count for Zbtb11.

I first enumerated genes that could stand in for ZBTB11's main known axes:

- ZBTB/BTB-ZF family members in training were heterogeneous: `Zbtb7a` was very broad with 841 DEGs in 151, whereas `Zbtb10`, `Zbtb16`, `Zbtb20`, and `Zbtb21` were 0, `Zbtb38` was 1, and `Zbtb18` was 5. This made simple family membership a boundary rather than a positive predictor.
- Direct respiratory-chain complex I perturbations were mostly silent or target-only in 151: `Ndufs2`, `Ndufa10`, `Ndufa6`, `Ndufb10`, `Ndufb11`, `Ndufb8`, `Ndufb9`, `Ndufc2`, `Ndufv2`, and `Ndufa4` were 1 each; `Ndufs4`, `Ndufs7`, `Ndufa9`, `Ndufa11`, `Ndufa12`, `Ndufaf2`, `Ndufaf4`, `Ndufaf5`, and `Ndufv1` were 0. Thus loss of one ETC subunit did not usually trigger a broad nuclear stress transcriptome.
- The more transcriptional mitochondrial-biogenesis regulators were detectable but much smaller than broad nuclear proteostasis signatures: `Nrf1` had 138 DEGs, `Esrra` had 57, `Opa1` had 37, `Nop56` had 25, `Polr3b` and `Ddx3x` had 8 each, while `Ppargc1a`, `Myc`, `Trp53`, `Cdkn2a`, `Nfe2l1`, and `Nfe2l2` were all 0.

For the analog cohort, the Distributed Agents profile comparison confirmed that formal DEG intersections are much more discriminating than whole-vector correlations:

| training target | 151 n_degs | profile evidence in `151 TH Prkcd Grin2c Glut` | relevance to Zbtb11 |
|---|---:|---|---|
| `Nrf1` | 138 | 23 up and 115 down FDR genes; down genes included `Sdha`, `Nrsn2`, `Haghl`, `Fam98a`, and `Tia1` | Best measured transcription-factor proxy for nuclear mitochondrial control, but NRF1 is not the NRF-2/GABP factor that Wilson et al. linked directly to ZBTB11. |
| `Esrra` | 57 | 16 up and 41 down FDR genes; the signal included self-knockdown plus metabolic genes such as `Mdh1` and `Got1` | A restrained mitochondrial-metabolism TF response, useful as a positive lower-breadth proxy. |
| `Opa1` | 37 | 26 up and 11 down FDR genes, including an integrated-stress-response-like arm with `Asns`, `Mars1`, `Chac1`, and `Ddit3` up | Shows that mitochondrial dysfunction can be detected in these cells, but Opa1 loss is a membrane-dynamics/cristae perturbation rather than a ZBTB11-like nuclear transcriptional loss. |
| `Nop56` | 25 | 10 up and 15 down FDR genes, including `Rsrp1`, `Ddx17`, `Srsf5`, `Srsf11`, and `Pabpn1` changes | A weak-moderate nucleolar/RNA-processing comparator for the RNA-processing enrichment of ZBTB11-bound genes in Sumathipala et al. |
| `Polr3b`, `Ddx3x` | 8, 8 | Small signatures with 1/7 and 2/6 up/down splits | RNA-synthesis or RNA-helicase counterexamples showing that nuclear RNA machinery perturbation alone need not broaden past single digits. |
| `Ndufs2`, `Ndufa10`, `Ndufb8` | 1, 1, 1 | Each was almost exclusively self-depletion at FDR 0.05 | Strong counterexamples against projecting a large response from complex I involvement alone. |
| `Ppargc1a`, `Myc`, `Trp53` | 0, 0, 0 | No FDR genes | Boundaries for PGC1/mitochondrial biogenesis and TP53/cell-cycle literature axes that can dominate proliferating-cell ZBTB11 studies but were flat here. |
| `Zbtb7a` | 841 | 512 up and 329 down FDR genes; Distributed Agents corpus described broad endomembrane, lysosomal, and synaptic remodeling and `Uba5`/`Ufc1`-like proteostasis neighbors | A high-BTB-family counterexample. It proves that a ZBTB TF can be broad in postmitotic neurons, but the corpus argues against a generic interchangeable ZBTB program. |
| `Ufc1`, `Uba5`, `Sin3a` | 572, 2677, 1433 | Very broad stress/chromatin signatures; `Ufc1` shared 57 down and 32 up FDR genes with `Zbtb7a`, and `Uba5` shared 138 down and 134 up | Boundaries on response magnitude. They are same-assay neighbors of several broad nuclear profiles, not direct ZBTB11 analogs. |

Across all cell groups, the moderate mitochondrial comparators had their strongest or only responses in the focal group: `Esrra` was nonzero only in 151, `Nop56` had 25 of its 31 total DEGs in 151, and `Nrf1` had 138 of 303 total in 151. That supports using their 151 counts directly instead of downweighting them as non-specific artifacts.

## Zbtb11-specific reasoning

I predict a nonzero but small Zbtb11 response.

The nonzero call comes from the ZBTB11-specific literature rather than from generic ZBTB family membership. Wilson et al. place ZBTB11 upstream of a nuclear mitochondrial regulon and show that loss of ZBTB11 function disrupts complex I assembly and respiration; Sumathipala et al. independently find ZBTB11 promoter binding enriched for mitochondrial and RNA-processing genes in patient fibroblasts. Those two mechanisms map onto measured assay-positive axes: `Nrf1`/`Esrra`/`Opa1` for mitochondrial regulation and `Nop56`/`Polr3b`/`Ddx3x` for nucleolar or RNA-processing perturbations.

The count should nevertheless be far below `Zbtb7a`, `Ufc1`, `Uba5`, or `Sin3a`. The training data show that most ZBTB TFs were flat, direct OXPHOS subunits rarely propagated beyond a self hit, and PGC1A, MYC, and TP53 programs were silent. That matters because the strongest ZBTB11 phenotypes in the literature often depend on proliferating embryonic, hematopoietic, ESC, or tumor cells, while this assay perturbs already postmitotic neurons with mosaic AAV CRISPR.

I therefore anchored Zbtb11 below `Opa1`/`Nop56` but above the Polr3b/Ddx3x and target-only complex-I cases: the point prediction is **18 DEGs**.

## Limits

- There is no exact same-experiment Zbtb11 signature and no measured GABP/NRF-2 or ZFP131 comparator in the training target set, so the central comparison is extrapolated through adjacent mitochondrial and RNA-processing regulators.
- Full-vector profile similarities among very weak perturbations were inflated by shared low-amplitude rank structure; I treated them as secondary and used FDR-backed DEG counts as the main calibration.
- ZBTB11's best literature-supported phenotypes were mostly observed in proliferating cells, fibroblasts, ESCs, or hematopoietic lineages. The link to mature thalamic glutamatergic neurons over a 3 to 4 week acute perturbation is imperfect.
- DEG count is assay-power dependent. A predicted count of 18 means I expect a detectable but threshold-fragile response, not that exactly 18 biological processes are affected.
