# DEG-count prediction trace

## Question and resolved ambiguity

The held-out manifest contains one requested perturbation, `Nf2`. I interpreted the endpoint as the exact training CSV endpoint: the count of measured genes with Wilcoxon Benjamini-Hochberg `pvals_adj < 0.05` in `151 TH Prkcd Grin2c Glut`, including the perturbed gene's own transcript if that measured row passes the same threshold. The held-out target is absent as a `gene_target` from the parquet and absent from the focal training-count CSV, so the task is to transfer information from non-held-out perturbations rather than inspect an `Nf2` signature.

## Sources used

- Differential-expression parquet: `[local file: training_de_all_cell_groups.parquet]`.
- Focal training counts: `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
- Requested-target manifest: `[local file: 149_Nf2.csv]`.
- Distributed Agents same-experiment corpus `perturbai-july-260713-sourceguard-1773-v1`, queried for the curated `Rdx`, `Tead1`, `Mtor`, `Tsc2`, and `Pak1` perturbation reports and same-experiment comparator notes.
- Distributed Agents runtime profile comparison over the focal rows of the parquet, comparing a hand-selected Nf2-neighborhood cohort with Wilcoxon `scores` as the signed profile and `pvals_adj < 0.05` as the significant-feature threshold.
- External mechanism priors from PubMed-indexed literature:
  - Merlin/NF2 is a FERM-domain tumor suppressor that links membrane/cytoskeletal inputs to nuclear growth-control programs; see Cooper and Giancotti 2014, DOI `10.1016/j.febslet.2014.04.001`.
  - Merlin inhibits CRL4-DCAF1 and thereby restrains YAP/TEAD signaling through LATS1/2; see Li et al. 2010, DOI `10.1016/j.cell.2010.01.029`, and Li et al. 2014, DOI `10.1016/j.ccr.2014.05.001`.
  - LATS phosphorylation inhibits YAP nuclear function in the Hippo pathway; see Zhao et al. 2007, DOI `10.1101/gad.1602907`, and Zheng and Pan 2019, DOI `10.1016/j.devcel.2019.06.003`.
  - Integrin/Rac/group-I PAK signaling can inhibit Merlin and activate YAP by Ser518 phosphorylation in adhesion contexts; see Sabra et al. 2017, DOI `10.1074/jbc.M117.808063`.
  - Radixin is an ERM-family scaffold that anchors alpha5-GABAA receptors to actin in neurons, so it is a relevant but not identical FERM/ERM comparator; see Loebrich et al. 2006, DOI `10.1038/sj.emboj.7600995`.
  - Merlin has been linked to RTK/Ras/MAPK, PI3K-AKT-mTORC1, Rac/PAK/JNK, Wnt/beta-catenin, and Hippo signaling in NF2-deficient tumors; see Zhou and Hanemann 2012, DOI `10.1016/j.febslet.2012.03.016`.

## Data operations

I first checked that `Nf2` was the only requested target. The focal training CSV contained 1,674 non-held-out perturbations; 1,205 had zero FDR<0.05 genes, the median was 0, the 75th percentile was 1, and only 5% exceeded 18 genes. This makes a zero-or-one prediction the default unless a target has strong evidence for one of the rare broad states.

I then filtered the parquet to `group_name == "151 TH Prkcd Grin2c Glut"` and to a curated set of Nf2-neighborhood perturbations that were actually present in training: `Rdx`, `Frmd5`, `Igsf8`, `Tead1`, `Mtor`, `Rptor`, `Tsc2`, PI3K/Akt nodes, Rac/Cdc42/PAK nodes, and Wnt/Hippo crosstalk controls such as `Ctnnb1`, `Tcf7l2`, and `Gsk3b`. For each of these I listed the focal rows with `pvals_adj < 0.05` and inspected the leading nonsignificant rows to distinguish a real downstream response from an isolated self-transcript decrease.

Finally, I used `profile_compare` with Wilcoxon `scores` as the signed feature vector for these candidates in the same focal cell group. This supplied pairwise Pearson/cosine similarities and same-direction significant-feature overlaps among the observed analogs. Because `Nf2` was held out, these pairwise values only calibrate the observed relatives; they are not a hidden measurement of `Nf2`.

## Target-specific reasoning for `Nf2`

`Nf2` encodes Merlin/schwannomin, a FERM-domain scaffold and tumor suppressor. External biology therefore suggested four possible same-experiment neighborhoods to test: an ERM/scaffold branch, a Hippo-YAP/TEAD branch, a PI3K/mTOR branch, and a Rac/Cdc42/PAK actin-signaling branch.

### FERM, ERM, and membrane-scaffold analogs

`Rdx` was the closest represented ERM-family perturbation. In the focal group it had exactly 1 DEG: `Rdx` itself was down (`log2FC = -0.610`, `p_adj = 0.0182`), while the next rows had `p_adj = 0.899` or 1. Distributed Agents' same-experiment `Rdx` report likewise summarized a one-gene `Rdx` surface and noted that the `151 TH Prkcd Grin2c Glut` row was self-transcript loss without downstream FDR genes.

Other membrane or actin-linked controls were also muted. `Frmd5`, another FERM-domain target in training, had 0 focal DEGs. `Igsf8`, a CD81/beta1-integrin/ERM-associated membrane scaffold, had exactly 1 focal DEG, its own transcript. The `Rdx` whole-score Pearson correlations to these focal signatures were tiny: `Rdx` to `Frmd5` was 0.0097 and `Rdx` to `Igsf8` was 0.0247. This makes ERM/FERM membership supportive of a buffered or self-only result, not of a broad thalamic RNA program.

### Hippo-YAP/TEAD and Wnt/Hippo crosstalk

NF2 sits upstream of the Hippo core and can restrain YAP/TAZ-TEAD output through LATS1/2. The only direct TEAD perturbation represented in the focal training set, `Tead1`, had 0 focal DEGs; the curated Distributed Agents `Tead1` report also classified sparse P16 `Tead1` loss as FDR-flat across measured neuronal groups. That is important because it says this acute postmitotic neuronal snRNA-seq endpoint did not detect a canonical TEAD maintenance program even when the transcription-factor node itself was perturbed.

The Wnt/beta-catenin controls were useful counterexamples rather than analogs. `Ctnnb1` produced 383 focal DEGs and `Tcf7l2` produced 106, with a real shared Wnt/thalamic component between them: in the focal profile comparison their Pearson correlation was 0.199 and they shared 5 positive plus 35 negative significant features in the same direction. However, `Tead1` did not enter that state: its Pearson correlation to `Tcf7l2` was -0.042, and the corpus explicitly noted that represented Hippo-adjacent and developmental crosstalk targets did not phenocopy `Tead1`. I therefore treated `Ctnnb1` and `Tcf7l2` as proof that this cell group can mount a broad developmental transcriptional response, but not as quantitative evidence that `Nf2` should have one.

### PI3K/mTOR branch

Merlin loss can derepress PI3K/AKT/mTORC1 signaling in proliferative NF2-deficient tumor contexts, so I compared the represented mTOR-axis perturbations. In the focal group, `Mtor` loss gave only 2 FDR<0.05 genes (`Rims3` up and `Tmed8` down), and `Rptor` had 0. Upstream PI3K/Akt entries were also buffered: `Pik3cb`, `Pik3r1`, `Pik3r2`, and `Akt3` had 0 focal DEGs. The broad `Tsc2` response was the exception, with 86 focal DEGs and sterol/lysosomal genes such as `Cyp51`, `Hmgcr`, `Ldlr`, `Msmo1`, `Atp6v0b`, `Grn`, and `Lamp2`, but `Tsc2` is a direct mTORC1 brake whose loss should activate the pathway much more strongly than partial loss of an upstream membrane scaffold. The Distributed Agents `Mtor` and `Tsc2` reports made the same point: basal juvenile neurons did not convert positive or upstream PI3K/Akt/mTOR perturbations into one shared RNA signature, while `Tsc2` occupied a stronger inhibitor-loss state.

### Rac/Cdc42/PAK actin-signaling branch

Rac/PAK signaling is mechanistically connected to Merlin phosphorylation, and Nf2-deficient schwannoma or adhesion systems can activate Rac1, Cdc42, and PAK. In this neuronal focal group that neighborhood was nearly flat. `Cdc42` had 1 DEG, `Cdc42` itself; `Rac1` had 0; `Pak1` had 1, `Pak1` itself; `Pak2` and `Pak3` each had 0. The focal `Rdx` signature did not align with this branch either: its Pearson correlation was only 0.0439 to `Cdc42`, 0.0178 to `Pak1`, -0.0098 to `Pak2`, and 0.0114 to `Pak3`. The curated `Pak1` report stated that group-I PAK paralogs did not form an interchangeable neuronal transcriptional module, and `Cdc42` was similarly reported to lack a shared Cdc42/Rac/PAK transcriptomic module.

## Prediction

The within-dataset evidence is dominated by buffered and self-only perturbations: `Rdx`, `Igsf8`, `Cdc42`, and `Pak1` each counted one FDR gene in the focal training CSV because their own transcript was depleted, whereas `Frmd5`, `Tead1`, `Rptor`, `Rac1`, `Pak2`, and `Pak3` were zero. The broad alternatives, `Ctnnb1`/`Tcf7l2` and `Tsc2`, were biologically interpretable but more downstream, more direct, or a different pathway sign than Nf2 loss. I therefore predict no propagated Merlin-loss transcriptional state in recovered thalamic neurons. The one-gene point prediction is a hedge for an `Nf2` self-transcript hit, because `Nf2` is part of the measured gene universe in this focal group and the nearest scaffold/GTPase analogs often had exactly that pattern.

Final point prediction:

| target_name | predicted_n_degs |
| --- | ---: |
| Nf2 | 1 |

## Limits

- `Nf2` itself had no Distributed Agents corpus report in the filtered release and no row as a perturbation in the input parquet, so all target-specific reasoning is transferred from imperfect neighbors.
- `Rdx` is an ERM protein and a neuronal GABAA-receptor anchor, not a full Merlin paralog. It calibrates the FERM/actin-scaffold end of the biology better than the nuclear CRL4-DCAF1 or Hippo roles of Merlin.
- `Tead1` loss is not the same as YAP/TAZ activation after Nf2 loss. A flat `Tead1` perturbation lowers the probability of a large canonical Hippo RNA state in postmitotic neurons but does not exclude a TEAD-independent or paralog-compensated Nf2 program.
- `Tsc2` is a strong direct mTORC1-repressor perturbation. Its 86 focal DEGs prove that an mTORC1-adjacent RNA program can be seen, but Nf2 is farther upstream and only partially perturbed, so using `Tsc2` numerically would overpredict.
- The focal endpoint is single-nucleus RNA in surviving NeuN-positive nuclei. Nf2 effects on protein localization, YAP phosphorylation, mTORC1 phosphorylation, actin state, Schwann cells, meninges, glia, or viability could be completely missed.
- The predicted count is sensitive to the self-transcript row. If the held-out `Nf2` guide set did not produce enough nonsense-mediated decay to make `Nf2` itself significant, the same reasoning would point to 0 downstream DEGs.
