# Trace

## Question and requested readout

The requested held-out perturbation file contains one target:

```tsv
target_name
Nr1h3
```

I interpreted the task as a point prediction of the number of genes with `pvals_adj < 0.05` in `151 TH Prkcd Grin2c Glut` nuclei after an acute sparse CRISPR perturbation of `Nr1h3`. The output is assay-specific: a count of Benjamini-Hochberg-corrected Wilcoxon discoveries in the focal cell group, not a ranking of biological importance or a claim that the edit had no nontranscriptional effect.

`Nr1h3` itself was held out, so neither its focal DEG count nor its held-out expression signature was available. I resolved the main ambiguity by prioritizing directly observed same-experiment behavior of measured LXR/RXR/lipid-pathway perturbations over broad developmental or glial LXR biology, because the focal dataset is postnatal, NeuN-enriched, and depleted for the astrocyte, microglial, endothelial, and oligodendrocyte settings in which LXR-alpha is often most active.

Final prediction: `Nr1h3` causes `0` DEGs in `151 TH Prkcd Grin2c Glut`.

## Sources

- Input target list: `[local file: 156_Nr1h3.csv]`.
- Training DEG-count endpoint: `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
- Differential-expression parquet: `[local file: training_de_all_cell_groups.parquet]`.
- Same-experiment knowledge layer: Distributed Agents corpus release `perturbai-july-260713-sourceguard-1773-v1`, especially target contexts for `Nr1h2`, `Abca1`, `Abca7`, `Srebf1`, `Srebf2`, `Rxra`, `Rxrb`, `Rxrg`, `Ppara`, `Ppard`, `Pparg`, and `Ncoa1`.
- Distributed Agents runtime profile-neighbor scan over the focal parquet rows, written to `nr1h3_lxr_profile_neighbors.json`. This compared observed LXR/RXR/ABCA/SREBP/PPAR anchors with all 1,674 eligible training perturbations using signed whole-profile and tail-overlap views.
- Public literature from NCBI PubMed via the BioEval literature search. I used these papers to establish the LXR-alpha mechanism and which within-dataset genes are appropriate analogs or controls:
  - Janowski et al. 1996, DOI `10.1038/383728a0`, PMID `8878485`: endogenous oxysterols activate LXR-alpha.
  - Lehmann et al. 1997, DOI `10.1074/jbc.272.6.3137`, PMID `9013544`: LXR-alpha and LXR-beta are oxysterol-activated nuclear receptors that bind LXR response elements.
  - Venkateswaran et al. 2000, DOI `10.1073/pnas.200367697`, PMID `11035776`: LXR-alpha activation induces `ABCA1` and drives cholesterol efflux.
  - Repa et al. 2000, DOI `10.1101/gad.844900`, PMID `11090130`: RXR/LXR induces `SREBP-1c` in mouse tissues through an LXR response element.
  - Laffitte et al. 2001, DOI `10.1073/pnas.98.2.507`, PMID `11149950`: LXR/RXR controls lipid-inducible `Apoe`, `Abca1`, and `Abcg1` expression in macrophage/adipocyte cholesterol efflux contexts.
  - Cao et al. 2007, DOI `10.2174/156720507780362173`, PMID `17430244`: brain LXR activation can regulate ABCA transporters and ApoE, with major astrocyte and microglial contributions relevant to Alzheimer disease.
  - Theofilopoulos et al. 2012, DOI `10.1038/nchembio.1156`, PMID `23292650`: endogenous LXR ligands regulate developing midbrain neuronal populations.
  - Terwel et al. 2011, DOI `10.1523/JNEUROSCI.6546-10.2011`, PMID `21562267`: astrocytic LXR-alpha and ApoE are important for microglial amyloid-beta phagocytosis in an AD model.
  - Wouters et al. 2019, DOI `10.3389/fimmu.2019.01811`, PMID `31417573`: LXR-alpha maintains blood-brain-barrier integrity in brain endothelial cells.

## Computational steps over the supplied data

1. I read the requested-target CSV and confirmed that the only target is `Nr1h3`.

2. I loaded the focal training-count CSV and used it as the calibrated endpoint for same-experiment analogs. The focal training distribution is very zero-inflated: 1,674 training perturbations, 469 nonzero, median `0`, 75th percentile `1`, 95th percentile `18`, and maximum `2677`.

3. I used Arrow filters on the 616,253,184-row parquet to read only `group_name == "151 TH Prkcd Grin2c Glut"` for a LXR/RXR/lipid calibration panel. For each loaded `gene_target` I counted `sum(pvals_adj < 0.05)` and verified that these counts reproduce the focal training-count CSV.

4. I inspected focal log-fold changes, Wilcoxon scores, and adjusted p-values for canonical LXR/RXR/sterol output genes:

   `Nr1h2`, `Nr1h3`, `Abca1`, `Abca7`, `Abcg1`, `Abcg4`, `Apoe`, `Srebf1`, `Srebf2`, `Rxra`, `Rxrb`, `Rxrg`, `Dhcr24`, `Insig1`, `Cyp51`, `Msmo1`, `Hmgcr`, `Hmgcs1`, `Sqle`, `Ldlr`, `Fdft1`, `Lss`, and `Fdps`.

   This was to check whether a nominally zero perturbation had a buried canonical LXR signal. For the closest analogs, the answer was no: `Nr1h2`, `Rxra`, `Rxrb`, `Rxrg`, `Abca1`, `Abca7`, and `Srebf1` all had `pvals_adj = 1.0` for these expected LXR/sterol sentinel genes in the focal group. By contrast, the positive controls behaved coherently: `Srebf2` down-regulated itself plus sterol genes including `Dhcr24`, `Insig1`, `Cyp51`, `Msmo1`, `Hmgcs1`, and `Sqle`; `Marchf6` up-regulated the same sterol block, including `Dhcr24`, `Insig1`, `Cyp51`, `Msmo1`, `Hmgcr`, `Hmgcs1`, `Sqle`, `Ldlr`, `Fdft1`, and `Fdps`.

5. I built a `names x gene_target` matrix of Wilcoxon `scores` for the focal LXR/RXR/ABCA/SREBP/PPAR analogs and computed pairwise Pearson, Spearman, and cosine similarities. All score correlations among these analogs were near zero; the largest absolute Pearson correlation among the pairs listed below was only `0.070`. That supported treating the zeros as independent absence of a recurrent LXR/RXR module, not as a coherent weak signature that missed FDR.

6. I ran `profile_neighbors` on the same focal rows using the full 1,674 training perturbations as the eligible universe. The generated neighbor artifact confirmed that the chosen anchors were compared independently in whole-profile Pearson/cosine and signed tail-overlap views. The downstream table reader in this environment rejected the writer's v2 schema, so I used direct Arrow summaries for auditable numeric values and used the runtime neighbor scan only as a qualitative check against a hidden high-similarity neighbor class.

## Same-experiment analogs and controls for `Nr1h3`

| training perturbation | focal `n_degs` | why it is relevant | focal expression-pattern evidence |
|---|---:|---|---|
| `Nr1h2` | 0 | The LXR-beta paralog is the closest represented LXR target. LXR-alpha/Nr1h3 and LXR-beta/Nr1h2 share oxysterol ligands, bind RXR partners, and regulate ABCA/APOE/SREBF1 lipid genes in responsive cells. | No focal DEGs. `Abca1`, `Abcg1`, `Abcg4`, `Apoe`, `Srebf1`, `Srebf2`, `Dhcr24`, `Insig1`, `Cyp51`, `Msmo1`, `Hmgcr`, `Hmgcs1`, `Sqle`, `Ldlr`, `Fdft1`, `Lss`, and `Fdps` all had `pvals_adj = 1.0`. The Distributed Agents corpus also curated `Nr1h2` as having no FDR<0.10 downstream signal in any of 23 measured groups. |
| `Rxra`, `Rxrb`, `Rxrg` | 0, 0, 0 | LXR proteins act as RXR heterodimers. A tonic LXR-alpha program should have some dependence on one or more RXR isoforms unless fully redundant. | All three were zero in the focal group and none moved the focal ABCA/APOE/SREBP/sterol sentinel panel at FDR 0.05. Distributed Agents `Rxra:F002`, `Rxrb:F003`, and `Rxrg:F002` also report that represented RAR/RXR and lipid nuclear-receptor perturbations do not produce a coherent shared acute neuronal module. |
| `Abca1` | 0 | Canonical downstream cholesterol-efflux transporter induced by LXR/RXR. | Focal `Abca1` loss was flat; it did not move `Apoe`, `Abcg1`, `Abcg4`, LXR/RXR transcripts, or the SREBF2 sterol genes. The corpus contrasts `Abca1` with `Srebf2`: `Abca1` did not trigger a cholesterol-transcription state, while `Srebf2` showed that sterol genes are readable when directly engaged. |
| `Abca7` | 0 | ABCA family lipid transporter, Alzheimer-risk gene, and useful counterexample for glial/myeloid cholesterol biology. | Focal `Abca7` was flat, and the corpus finding `Abca7:F002` specifically records that `Abca7` loss did not trigger the `Srebf2` cholesterol-biosynthesis module, whereas `Srebf2` did. This argues against treating any ABCA perturbation as an LXR-like neuronal sterol response. |
| `Srebf1` | 0 | `SREBF1` is an LXR-induced lipogenic transcription factor in liver/adipose and other responsive contexts. | Focal `Srebf1` was flat. Corpus `Srebf1:F002` contrasts this with direct `Srebf2` loss, showing the neuronal sterol block tracks `Srebf2` rather than generic SREBP-family activity. |
| `Srebf2` | 7 | Positive control for a cell-autonomous neuronal sterol transcription factor, not a close LXR-alpha phenocopy. | `Srebf2` had 7 focal DEGs: self plus `Dhcr24`, `Insig1`, `Cyp51`, `Msmo1`, `Hmgcs1`, and `Sqle` were all down-regulated at FDR 0.05. It did not move `Abca1`, `Abcg1`, `Apoe`, `Rxra`, `Rxrb`, or `Rxrg` in the focal group. This bounds the expected `Nr1h3` count: the sterol arm is detectable, but the LXR/RXR/efflux arm is absent. |
| `Hmgcr` | 0 | A rate-limiting cholesterol-biosynthesis enzyme downstream of SREBF2; a counterexample for sterol feedback. | No focal DEGs and no focal sterol rebound, unlike `Marchf6`. This supports the corpus claim that the SREBF2 sterol block is not phenocopied by every lipid enzyme. |
| `Marchf6` | 14 | ER-associated sterol-control node; positive inverse control for `Srebf2`. | Up-regulated `Srebf2` and the sterol genes `Dhcr24`, `Insig1`, `Cyp51`, `Msmo1`, `Hmgcr`, `Hmgcs1`, `Sqle`, `Ldlr`, `Fdft1`, and `Fdps` at FDR 0.05, showing that 151 TH Prkcd Grin2c Glut can mount a focal sterol response in this Wilcoxon assay. |
| `Ppara`, `Ppard`, `Pparg` | 0, 0, 0 | Lipid nuclear receptors that also use RXR and are good same-family negative controls for ligand-dependent programs in basal neurons. | All were exact zeros in the focal group. The corpus records that PPAR/RXR-family targets were broadly flat or singleton-only rather than converging on a basal ligand-activated module. |
| `Ncoa1`, `Ncoa3`, `Ppargc1a` | 0, 0, 0 | Nuclear-receptor coactivators or PPAR/PGC-axis components that should respond if a broad coactivator-dependent lipid receptor state were active. | All were exact zeros in the focal group; `Ncoa1` and `Ncoa3` did not reveal a hidden p160 nuclear-receptor module in the corpus. |
| `Rora`, `Nr1d1`, `Thra`, `Crebbp`, `Rab7`, `Tsc2`, `Dctn1`, `Phf12`, `Uba5` | 278, 116, 3, 8, 501, 86, 75, 403, 2677 | Not LXR-alpha analogs; positive controls for the same cell group and same endpoint. | These demonstrate that the focal group is not globally underpowered and that nuclear-receptor, chromatin, lysosomal, mTOR/sterol, and proteostatic perturbations can generate DEGs in this exact analysis. |

## Target-specific reasoning for `Nr1h3`

`Nr1h3` encodes LXR-alpha, one of two liver X receptors. LXR-alpha and LXR-beta are oxysterol-activated nuclear receptors; they heterodimerize with RXR family members and, in ligand-competent lipid-loaded cells, activate direct targets such as `ABCA1`, `ABCG1`, `APOE`, and `SREBF1` that promote cholesterol efflux and couple sterol to fatty-acid metabolism. Those mechanisms make `Nr1h2`, the three `Rxr` paralogs, `Abca1`, `Abca7`, `Srebf1`, and `Srebf2` the best represented same-experiment comparisons.

The within-dataset evidence points to no focal transcriptional response:

- The closest paralog, `Nr1h2`, has `0` DEGs in 151 TH Prkcd Grin2c Glut, and the expected direct LXR/RXR target transcripts are all FDR-flat in the same rows.
- The three available RXR partners also have `0` focal DEGs. Since RXRs are shared partners for retinoid, PPAR, LXR, thyroid, VDR, and other nuclear receptors, they are imperfect analogs, but the absence of a RXR/LXR/PPAR/RAR shared module argues that basal juvenile neurons are not sitting in a ligand-activated lipid nuclear-receptor state.
- The downstream efflux genes `Abca1` and `Abca7` have `0` focal DEGs and do not induce the APOE/ABCG/sterol signature. This is important because much of the public LXR literature in brain is glial cholesterol efflux and ApoE lipidation; those axes are off-lineage or poorly sampled in the NeuN-positive dataset.
- `Srebf2` and `Marchf6` are small but real focal sterol-positive controls. They show that genes such as `Dhcr24`, `Insig1`, `Cyp51`, `Msmo1`, `Hmgcs1`, `Sqle`, `Hmgcr`, `Ldlr`, `Fdft1`, and `Fdps` can pass the Wilcoxon/BH endpoint in this cell group. The LXR/RXR analogs simply do not move that module.
- Pairwise Wilcoxon-score similarities among the focal LXR/RXR/ABCA/SREBP/PPAR analogs were all close to zero. The largest absolute Pearson `r` in the retained analog set was `0.070`, so there was no broad sub-FDR expression geometry suggesting that `Nr1h3` should inherit a weak nonzero effect from a latent neighbor.

The public literature sharpens rather than overturns that conclusion. The strong LXR-alpha biology is ligand- and context-dependent: hepatic/adipose lipogenesis via `Srebf1`, macrophage cholesterol efflux via `Abca1`/`Abcg1`/`Apoe`, astrocyte/microglial ApoE lipidation and amyloid handling, and endothelial blood-brain-barrier maintenance. The focal experiment instead used P16 mosaic loss of function, sparse guides, basal juvenile-to-young-adult postmitotic neuronal nuclei, and a thalamic glutamatergic group. That setting can detect some nuclear-receptor perturbations, such as `Rora`, `Nr1d1`, and the small `Thra` response, but it did not expose an LXR/RXR module around `Nr1h2`.

I therefore made the zero/nonzero decision as follows: the direct LXR paralog and same-complex RXR partners are all zero in the focal count table, the canonical LXR efflux targets are zero, no related perturbation produces even a one-gene focal LXR-like signature, and the glial/endothelial/developmental literature contexts for `Nr1h3` are mostly absent from the cell population assayed here. The best point estimate is exactly `0`, not a small SREBF2-like value.

## Limits and extrapolation

- `Nr1h3` was held out, so there is no direct Nr1h3 signature to inspect and no focal guide-level editing measurement.
- The prediction depends on single-gene CRISPR perturbations. LXR-alpha and LXR-beta, and RXR isoforms, can be redundant; a double perturbation or ligand challenge could behave differently from acute sparse `Nr1h3` loss.
- The raw target mRNA rows are not a direct editing assay. Several nuclear receptors are lowly or burstily expressed in snRNA-seq, and the observed absence of self-downregulation for analogs is not evidence of failed indel formation.
- The strongest public LXR-alpha mechanisms in brain include astrocytes, microglia, oligodendrocytes, endothelium, amyloid/tau disease states, and embryonic midbrain neurogenesis. The whole-brain NeuN-positive screen does not test those contexts well.
- `Srebf2` and `Marchf6` prove that a sterol module is detectable in 151 TH Prkcd Grin2c Glut, but they are not same-complex analogs of `Nr1h3`; they only bound the claim that lipid genes are invisible.
- The endpoint is a thresholded BH-adjusted Wilcoxon count. A prediction of zero still allows small effect sizes or non-RNA phenotypes that do not cross `pvals_adj < 0.05`.
