# Trrap held-out DEG-count prediction

## Question interpreted

The requested target manifest contains one held-out perturbation:

```tsv
target_name
Trrap
```

I interpreted `n_degs` as the number of measured genes with `pvals_adj < 0.05` in the `151 TH Prkcd Grin2c Glut` contrast for the requested perturbation, matching the supplied training-count CSV. The target was completely held out, so no `Trrap` rows from the supplied differential-expression parquet were used or present. I preserved the requested target spelling and order.

## Sources used

- Supplied endpoint table: `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`, containing `n_degs` for 1,674 non-held-out perturbations in `151 TH Prkcd Grin2c Glut`.
- Supplied DE parquet: `training_de_all_cell_groups.parquet`, filtered to `group_name == "151 TH Prkcd Grin2c Glut"` for exact per-gene log fold changes, adjusted Wilcoxon p-values, and matched perturbed/control nucleus counts of training analogs.
- Distributed Agents same-experiment corpus `perturbai-july-260713-sourceguard-1773-v1`; especially target contexts for `Atxn7`, `Brd4`, `Crebbp`, and `Ep300`, plus same-experiment claims about BAF/mSWI/SNF and KAT3 non-interchangeability.
- Distributed Agents runtime profile comparison over a hand-selected 26-target cohort of SAGA/HAT/Mediator/MYC-E2F-p53/chromatin comparators in the focal cell group. This computed significant-feature counts and pairwise overlap among the chosen training perturbations, and it searched all 1,674 eligible training perturbations for profile neighbors of focal comparators.
- PubMed literature:
  - Elias-Villalobos, Fort, and Helmlinger 2019, PMID 31769470, DOI `10.1042/BST20180496`: Tra1/TRRAP is the sole PIKK pseudokinase and a large scaffold of SAGA and NuA4/TIP60.
  - Yang et al. 2024, PMID 39088653, DOI `10.1126/science.adl5816`: structural work placing TRRAP in NuA4/TIP60 and showing that TRRAP loss mislocalizes NuA4/TIP60 and redistributes H2A.Z acetylation in human cells.
  - Herceg et al. 2001, PMID 11544477, DOI `10.1038/ng725`: complete mouse `Trrap` disruption causes peri-implantation lethality and proliferation/cell-cycle defects.
  - Tapias et al. 2014, PMID 24792116, DOI `10.1016/j.stem.2014.04.001`: neural progenitor `Trrap` deletion impairs HAT/transcriptional-machine recruitment to E2F cell-cycle genes and changes cortical progenitor fate.
  - Yin, Lazaro, and Wang 2022, PMID 36618986, DOI `10.1016/j.csbj.2022.12.024`: `Trrap` deletion compromises adult neural stem-cell self-renewal and differentiation through an Sp1/HAT mechanism.

## Computation over the supplied data

1. Read the held-out manifest and verified that only `Trrap` is requested.
2. Read the training `n_degs` table to calibrate the endpoint. The focal class is sparse: 1,205 of 1,674 training targets have 0 DEGs, the median is 0, the 75th percentile is 1, the 90th is 2, the 95th is 18, and only 59 targets have at least 50 DEGs.
3. Enumerated likely training analogs and counterexamples by Trrap mechanism: the direct SAGA subunit `Atxn7`, the HAT/acetylation-adjacent targets `Yeats2`, `Brd1`, `Kat6a`, `Kat6b`, `Crebbp`, and `Ep300`, transcription-factor axes through which TRRAP is often recruited (`Myc`, `Mycn`, `E2f1`, `Trp53`), Mediator comparators, and broad chromatin regulators that were active in this exact focal cell group.
4. Queried the parquet only for `151 TH Prkcd Grin2c Glut` and these training targets. The core aggregation was:

```sql
SELECT gene_target,
       min(n_pert_matched) AS n_pert,
       min(n_ctrl_matched) AS n_ctrl,
       sum(CASE WHEN pvals_adj < 0.05 THEN 1 ELSE 0 END) AS n_degs
FROM parquet_scan('training_de_all_cell_groups.parquet')
WHERE group_name = '151 TH Prkcd Grin2c Glut'
  AND gene_target IN (...)
GROUP BY gene_target;
```

5. Used `profile_compare` on 26 focal-cell signatures to test whether the small or zero HAT/SAGA signatures were nevertheless embedded in a broader recurrent pattern. In the FDR-positive overlap layer, `Atxn7`, `Yeats2`, `Ep300`, `Myc`, `Mycn`, `E2f1`, `Trp53`, `Kat6a`, `Kat6b`, and `Cdk8` each had no FDR-positive feature to share. `Crebbp` shared no same-direction FDR-positive gene with `Brd1`, `Kat6a`, `Kat6b`, `Myc`, `E2f1`, `Arid1a`, or the stronger broad controls in the inspected cohort. The broad controls (`Brd4`, `Smarcc2`, `Sin3a`, `Yy1`, `Wac`, `Setd1a`) did have large DEG sets, confirming that the focal class and matched control pool could detect large chromatin effects.

## Target-specific analogs and prediction

### Trrap

Public mechanism makes `Trrap` a plausible chromatin regulator: TRRAP scaffolds SAGA and NuA4/TIP60 and helps recruit these HAT complexes to chromatin; total loss is lethal in proliferating embryos, and conditional loss in neural progenitors perturbs E2F/cell-cycle programs. Those priors, however, come mainly from dividing cells or stem/progenitor populations, whereas the requested Perturb-seq condition is sparse postnatal CRISPR loss in recovered NeuN-positive, postmitotic neurons.

The most directly relevant training perturbations were low or null in the exact endpoint:

| training target | focal `n_degs` | focal matched perturbed nuclei | expression-pattern evidence and interpretation |
| --- | ---: | ---: | --- |
| `Atxn7` | 0 | 124 | The only represented SAGA subunit in this local analog set. The same-experiment corpus reports `Atxn7:F001`: zero FDR<0.10 downstream genes across all 20 measured neuronal groups and no meaningful whole-signature neighbors. This is the strongest within-dataset argument that partial wild-type SAGA perturbation after P16 does not necessarily create a broad neuronal RNA state. |
| `Yeats2` | 0 | 99 | An ATAC/H3-acetylation neighbor rather than a Trrap subunit. It had no FDR-positive focal genes, and the corpus places represented H3-acetylation neighbors such as `Atxn7`, `Ep300`, and `Crebbp` as non-phenocopies for `Yeats2`. |
| `Kat6a`, `Kat6b` | 0, 0 | 170, 150 | MYST HAT catalytic subunits in another acetyltransferase family; both were flat in the focal group. In the Brd1 same-experiment report, represented MYST/HAT comparators did not phenocopy one another. |
| `Brd1` | 4 | 178 | BRPF/MOZ-MORF HAT complex scaffold; the four focal FDR genes were all down (`Gabbr2`, `Ndufa13`, `Ptpn3`, `Rgs11`) and did not overlap the KAT3 or broad Brd4 programs. |
| `Ep300`, `Crebbp` | 0, 8 | 155, 61 | Closest represented KAT3 paralogs, both indirect comparators. `Ep300` was fully FDR-null in the focal group and across its measured neuronal groups. `Crebbp` had only eight focal DEGs (`Stxbp2`, `Cfap298`, `Leng8` up; `Rtn4rl1`, `Ccdc141`, `Dgkz`, `Rbfox2`, `Stmn4` down). The Distributed Agents corpus claim `claim:47099...` states that `Crebbp`, `Ep300`, and `Creb1` were not interchangeable in the matched assay. |
| `Myc`, `Mycn`, `E2f1`, `Trp53` | 0, 0, 0, 0 | 210, 320, 253, 251 | These are not SAGA/NuA4 subunits, but they are canonical proliferative transcription-factor axes for TRRAP. Their null focal counts argue that the embryonic MYC/E2F/p53-centered TRRAP literature should be strongly discounted in basal postmitotic neurons. |
| `Med13`, `Med13l`, `Med15`, `Med23`, `Cdk8` | 11, 1, 19, 13, 0 | 154, 200, 158, 160, 192 | Mediator perturbations supplied a small thalamic down-module (`Prkcd`, `Grm1`, `Atp2a2`, `Plekhg1`, `Pcp4` recurring for several targets), but the counts stayed in the 0-19 range and did not support a Brd4-like broad coactivator collapse. |

The main counterexamples were broad chromatin/transcription responders in the same focal group: `Brd4` had 311 DEGs, `Setd1a` 368, `Wac` 384, `Yy1` 720, `Sin3a` 1,433, and `Smarcc2` 185. These are important because they show that `151 TH Prkcd Grin2c Glut` had enough power to detect strong chromatin-regulator states. They are weaker quantitative analogs for Trrap, though: Distributed Agents `Brd4:F008` explicitly reports that represented p300/CBP, Mediator, and MYC-axis comparators did not phenocopy `Brd4`, and the high-confidence BAF/mSWI/SNF claim reports subunit selectivity rather than a generic chromatin phenotype. `Arid1a` was only 22 DEGs while `Arid1b` and `Smarca4` were 1 and 0, reinforcing that even same-complex chromatin subunits did not transfer counts uniformly.

I therefore predict a thresholded null rather than a broad effect. The prediction is driven mostly by the focal training data for `Atxn7`, HAT comparators, and MYC/E2F/p53 targets; external literature is used to identify why those are the relevant analogs and why their stem/proliferative TRRAP biology should not be copied wholesale into postmitotic recovered neurons.

Predicted `Trrap` `n_degs`: **0**.

## Limits and extrapolation

- The most direct NuA4/TIP60 subunits (`Kat5`, `Ep400`, `Brd8`, `Dmap1`, `Mrgbp`, `Ruvbl1`, `Ruvbl2`, `Epc1`, `Epc2`, `Ing3`, `Morf4l1`, `Morf4l2`, `Vps72`) and most SAGA core subunits (`Tada*`, `Taf5l`, `Taf6l`, `Taf9b`, `Supt3`, `Supt7l`, `Sgf29`, `Kat2a`, `Kat2b`, `Usp22`) were absent from the training-count table, so the complex-level comparison rests mainly on `Atxn7` plus indirect HAT/chromatin neighbors.
- TRRAP is a scaffold for two large acetyltransferase complexes, so it could be less redundant than `Atxn7`, `Yeats2`, `Ep300`, or `Kat6a/Kat6b`. The zero prediction means any recovered-cell RNA effect is expected to fall below BH FDR 0.05, not that Trrap protein is irrelevant.
- Germline or conditional deletion phenotypes of `Trrap` are dominated by proliferation, mitosis, and neural stem/progenitor fate. Those mechanisms are real, but they are an imperfect match to acute, mosaic editing in postnatal postmitotic neurons.
- No Trrap editing, indel, protein, HAT activity, H2A.Z acetylation, viability, or absolute RNA-content measurement is present for the held-out target. The predicted count is an assay-calibrated survivor-nucleus transcriptional endpoint, not a statement about cell viability or developmental importance.
