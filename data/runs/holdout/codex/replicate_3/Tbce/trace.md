# Tbce direct n_degs forecast

Target and endpoint:

- Target: `Tbce`, the single gene in the declared holdout manifest.
- Focal class: `151 TH Prkcd Grin2c Glut`.
- Endpoint: number of measured genes with BH-adjusted Wilcoxon `pvals_adj < 0.05`.
- Declared training table: `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
- Declared expression surface: `[local file: training_de_all_cell_groups.parquet]`.
- Tbce biology bundle: `[local file: Tbce.json]`, schema `expected-transcript-impact-agent-bundle-v1`, sha256 `490feb2093a4237c8902f4ff9c9c62a5bab515d2d0a69b1135e04932ee27ce84`.

Biological prior:

- The exact in-assay expression card reports that `Tbce` is available in the focal class: 21,553 of 23,679 non-target nuclei express it, with mean CP10k 1.849 and mean raw UMI 2.885.
- The functional-stock card calls the P37-P44 operative state `likely_substantially_depleted`: TBCE supplies newly synthesized tubulin and axonal microtubule renewal, pre-edit protein and microtubules can initially persist, but pmn mouse evidence places material neuronal microtubule loss within a postnatal interval shorter than the 21-28 day assay window.
- The observability card supports a real but not necessarily large survivor-nucleus signature: there is direct mouse postnatal neuronal loss evidence, but it is from motor/sensory systems and a lifelong hypomorphic allele rather than P16 acute CRISPR in thalamic neurons; `Tbcel` compensation is unresolved.

Training measurements that anchored the scale:

- The `151 TH Prkcd Grin2c Glut` count table is highly zero-inflated: among 1,674 training targets, 1,205 have 0 DEGs, the median is 0, the 75th percentile is 1, and only 106 have at least 10 DEGs.
- The deterministic annotation store places `Tbce` with `Tbcd` in the exact GO `post-chaperonin tubulin folding pathway` and `tubulin complex assembly` target sets. In the focal count table, `Tbcd` has 12 DEGs.
- In the human-ortholog CORUM `TBCD-ARL2-tubulin(beta)-TBCE complex`, the measured target members with focal counts are `Tbcd` = 12 and `Tubb5` = 1.
- In the human-ortholog `TBCE-TBCB-tubulin(alpha) complex`, the measured non-Tbce member is `Tuba1a` = 7.
- Broader alpha/beta tubulin structural paralogs remain small in this exact class: `Tuba4a` = 2, `Tubb4b` = 1, `Tubb5` = 1.
- Direct Parquet re-counting of this observed tubulin cohort at `pvals_adj < 0.05` gave:

| target | n_degs | up | down |
| --- | ---: | ---: | ---: |
| `Tbcd` | 12 | 9 | 3 |
| `Tuba1a` | 7 | 6 | 1 |
| `Tuba4a` | 2 | 1 | 1 |
| `Tubb4b` | 1 | 0 | 1 |
| `Tubb5` | 1 | 0 | 1 |

Same-experiment corpus interpretation:

- The selected July sourceguard corpus has no `Tbce` Findings, Claims, or explicit target references, so it provided no direct endpoint evidence for the held-out target.
- The same corpus reports for `Tbcd` that `151 TH Prkcd Grin2c Glut` concentrated 12 of the 19 FDR<0.10 downstream gene-cell pairs and that the focal state coupled alpha-tubulin RNA induction to a small Jun/Nfil3/synaptic-identity module rather than to a broad proteotoxic stress response.
- The `Tbcd` and `Tuba1a` reports both argue against pooling all tubulin and microtubule genes as one interchangeable module: `Tuba1a`, `Tuba4a`, and `Arl2bp` did not phenocopy `Tbcd`, and direct `Tuba4a`, `Tubb4b`, and `Tubb5` perturbations did not phenocopy the `Tuba1a` multi-tubulin response.
- A matched profile comparison of `Tbcd`, `Tuba1a`, `Tuba4a`, `Tubb5`, and `Tubb4b` in the focal Parquet confirmed that the significant rows do not simply overlap into one large coherent response; the important quantitative fact for the forecast was therefore the individual count scale, not a centroid or averaged DEG set.

Synthesis:

`Tbce` should be observable in this population: it is expressed in nearly all focal non-target nuclei, acts in continuously renewed tubulin folding/routing rather than in a purely prenatal installation step, and belongs to the same post-chaperonin tubulin-folding machinery as the 12-DEG `Tbcd` perturbation. The best direct analog is therefore `Tbcd`, not the lower-count structural tubulin isoforms. At the same time, the closest same-experiment measurements show that postnatal tubulin biology in this class produces compact, target-specific signatures rather than a shared high-DE cytoskeletal injury program, and the Tbce card leaves acute wild-type TBCE clearance, thalamic vulnerability, and `Tbcel` buffering unresolved.

I therefore placed `Tbce` slightly below `Tbcd` but above the isolated tubulin-structural perturbations, yielding a low two-digit point forecast:

`predicted_n_degs = 10`
