# Trhr DEG-count prediction

## Question and interpretation

The held-out manifest contains one requested perturbation:

| target_name |
|---|
| Trhr |

I interpreted the task as a point prediction of `n_degs` for `Trhr` loss of function in `151 TH Prkcd Grin2c Glut` nuclei, where `n_degs` is the number of measured genes with Wilcoxon Benjamini-Hochberg `pvals_adj < 0.05` in perturbed cells versus matched controls. The target transcript itself can count if the guide reduces it enough to pass FDR. A prediction of 0 means no measured RNA, including `Trhr`, is expected to cross that assay threshold.

The held-out `Trhr` perturbation is absent from both the parquet and the focal training-count CSV, so there is no direct `Trhr` signature to average. I used the focal training endpoints and the focal expression signatures of mechanistically related non-held-out perturbations to estimate whether a TRHR loss would produce either a target-only knockdown or a broader downstream state.

## Sources

- `[local file: 245_Trhr.csv]`
  - Requested targets; one row, `Trhr`.
- `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`
  - Observed focal-cell `n_degs` for 1,674 non-held-out perturbations.
- `[local file: training_de_all_cell_groups.parquet]`
  - Per-gene log2 fold changes and adjusted p-values for the same 1,674 perturbations.
- Distributed Agents same-experiment corpus, release `perturbai-july-260713-sourceguard-1773-v1`
  - No `Trhr`-centered findings were present in the filtered release.
  - I used same-assay findings and claims around `Cckar`, `Cckbr`, `Crhr1`, `Gnrhr`, `Grm1`, `Grm5`, `Htr2c`, `Chrm2`, `Chrm3`, `Npy1r`, `Plcb1`, and other GPCR controls. In particular, corpus claim `claim:9f69c85a0a28574c603c` summarized repeated flat or nonconvergent basal neuronal signatures after single-gene perturbations of neuromodulatory GPCRs and proximal second-messenger effectors.
- PubMed-indexed pathway literature
  - TRH and GnRH receptors couple to pertussis-toxin-insensitive Gq/G11 proteins to activate phospholipase C: Hsieh and Martin 1992, PMID 1333052, DOI `10.1210/mend.6.10.1333052`.
  - TRHR and GNRHR stimulation both activate PLC, Ca2+ mobilization, and PKC in pituitary cells, while producing partly distinct promoter responses: Kaiser et al. 1994, PMID 7527898, DOI `10.1210/mend.8.8.7527898`.
  - Germline deletion of mouse TRH receptor 1 produces central-hypothyroid endocrine phenotypes without a reported gross neuronal developmental collapse: Rabeler et al. 2004, PMID 14988432, DOI `10.1210/me.2004-0017`.
  - Group-I metabotropic glutamate receptors, including GRM1 and GRM5, are neuronal GPCRs linked to PLC signaling: Bordi and Ugolini 1999, PMID 10416961, DOI `10.1016/s0301-0082(98)00095-1`.

## Computational steps over the supplied data

1. Confirmed that the manifest contains only `Trhr`.
2. Loaded the focal training endpoint table.
   - There are 1,674 non-held-out perturbations.
   - The distribution is very zero-heavy in `151 TH Prkcd Grin2c Glut`: median `n_degs = 0`, 75th percentile `= 1`, 469/1,674 perturbations have any DEG, and the large responses are concentrated in core chromatin, proteasome, splicing, and RNA-processing genes rather than cell-surface receptors.
3. Used parquet row-group statistics to restrict the full 616,253,184-row DE parquet to the focal group.
   - `151 TH Prkcd Grin2c Glut` is contained in row groups 546-580, about 29.9 million candidate rows.
   - For selected receptor and GPCR-effector perturbations, each target had 17,259 measured focal features.
4. Extracted TRHR-relevant analogs from the focal group and counted rows with `pvals_adj < 0.05`.

| training perturbation | focal `n_degs` | closest use in reasoning |
|---|---:|---|
| `Cckar` | 0 | Gq/PLC neuropeptide GPCR, no downstream or self transcript hit |
| `Cckbr` | 0 | paralogous CCK Gq/PLC neuropeptide GPCR, no hit |
| `Gnrhr` | 0 | the nearest endocrine Gq/PLC receptor comparator from the Hsieh/Kaiser TRHR-GNRHR literature, no hit |
| `Crhr1` | 0 | neuroendocrine GPCR comparator, no hit |
| `Htr2a` | 0 | Gq serotonin receptor comparator, no hit |
| `Htr2c` | 0 | Gq serotonin receptor comparator, no hit |
| `Chrm3` | 0 | Gq muscarinic receptor comparator, no hit |
| `Grm5` | 0 | Gq/PLC group-I mGluR, no hit |
| `Grm1` | 1 | Gq/PLC group-I mGluR; the single FDR hit was `Grm1` itself |
| `Grm7` | 1 | mGluR receptor; the single FDR hit was `Grm7` itself |
| `Plcb1` | 0 | proximal PLC beta effector downstream of Gq receptors, no hit |
| `Tacr3` | 0 | neuropeptide GPCR comparator, no hit |
| `Sstr5` | 0 | neuromodulatory GPCR comparator, no hit |
| `Npy1r`/`Npy2r`/`Npy5r` | 0 each | Gi/o neuropeptide receptors, useful as basal receptor-loss counterexamples |
| `Tshr` | 0 | endocrine GPCR in the thyroid-axis neighborhood, no hit |

5. Ran a Distributed Agents runtime `profile_compare` for a 15-member receptor/PLC cohort (`Cckar`, `Cckbr`, `Crhr1`, `Gnrhr`, `Grm1`, `Grm5`, `Htr2a`, `Htr2c`, `Npy1r`, `Npy2r`, `Npy5r`, `Plcb1`, `Sstr5`, `Tacr3`, `Tshr`) using `logfoldchanges` as the signed value and `pvals_adj < 0.05` as the activity threshold.
   - Fourteen of the fifteen perturbations had no significant focal features; `Grm1` had exactly one.
   - Pairwise whole-profile cosines among the five most TRHR-like Gq/PLC nodes and the receptor peers were about 0.70-0.76, but with weak Spearman correlations around 0.20-0.29 and no shared significant features. I treated this as evidence that these receptors sit together at the basal/noise floor, not as evidence for a coherent positive expression module.
6. Scanned `Trhr` as a measured feature across all 1,674 non-held-out focal perturbations.
   - `Trhr` was present in the 17,259-gene focal feature set for all 1,674 training perturbations.
   - It never passed FDR 0.05 as a downstream feature of any other knockout; the minimum adjusted p-value was 1.0. This is consistent with a sparse or weakly powered transcript in this cell group, so I did not assume the `Trhr` guide would necessarily contribute a target-only DEG.

The analog-extraction code was straightforward parquet filtering; the only non-obvious operation was selecting row groups by their `group_name` statistics before filtering inside the group:

```python
for rg in range(pf.num_row_groups):
    col = group_name_column_metadata(pf.metadata.row_group(rg))
    if col.statistics.min <= "151 TH Prkcd Grin2c Glut" <= col.statistics.max:
        focal_rgs.append(rg)
```

## Target-specific reasoning

### Trhr

`Trhr` encodes the thyrotropin-releasing hormone receptor, a class-A GPCR. Its canonical acute signaling is ligand-driven coupling to Gq/G11, phospholipase C, IP3/Ca2+, DAG/PKC, and MAPK/immediate-early outputs. The mechanistically closest training perturbation was `Gnrhr`: Hsieh and Martin directly compared TRHR and GNRHR PLC activation through Gq/G11, and Kaiser et al. showed that both receptor inputs can drive Ca2+/PKC-dependent pituitary promoter responses. In this exact focal cell type, however, `Gnrhr` produced zero DEGs across 17,259 measured genes. The same was true for the Gq/PLC neuropeptide receptors `Cckar` and `Cckbr`, the Gq serotonin receptors `Htr2a` and `Htr2c`, the Gq muscarinic receptor `Chrm3`, the group-I glutamate receptor `Grm5`, and the downstream PLC beta target `Plcb1`.

The weak nonzero GPCR examples did not support raising the prediction above zero. `Grm1`, `Grm7`, `Gnao1`, and `Cck` each had `n_degs = 1`, but in each case the significant gene was the targeted transcript itself, with no broader pathway response. That is a useful counterexample because a receptor perturbation can enter the endpoint if the target RNA is well detected and depleted, but the more TRHR-like receptors in the panel did not even show that target-only behavior in `151 TH Prkcd Grin2c Glut`.

The same-experiment Distributed Agents corpus reinforced this read of the training data. It had no `Trhr` entry, but it reported pan-neuronal or near-pan-neuronal flatness for `Cckar`, `Cckbr`, `Htr2c`, `Npy1r`, `Chrm2`, and `Chrm3`; a GNRHR finding in the corpus stated that the canonical pituitary GnRHR MAPK/immediate-early/gonadotropin program was absent from neuronal `Gnrhr` perturbations; a `Grm1` finding stated that `Grm1` loss did not alter activity-regulated group-I mGluR transcriptional targets; and a `Plcb1` claim grouped represented neuromodulatory GPCR and second-messenger perturbations as lacking a shared basal neuronal nuclear-transcriptome module. Those findings are especially relevant because the experiment is unstimulated, postmitotic, and several weeks after sparse AAV CRISPR delivery; it is well suited to detect sustained nuclear RNA states but not the minute-to-hour calcium and immediate-early bursts classically evoked by TRH ligand.

I therefore predicted no FDR-significant genes for `Trhr`. The integer point prediction is:

| target_name | predicted_n_degs |
|---|---:|
| Trhr | 0 |

## Limits and extrapolation

- This is an extrapolation from pathway neighbors; the held-out `Trhr` knockout profile itself is completely absent.
- The analog set is imperfect. TRHR has ligand, tissue, and endocrine-axis biology distinct from CCK, GnRH, serotonin, muscarinic, and glutamate receptors, and none is a true paralog of `Trhr`.
- The focal count endpoint includes the self-transcript. If the held-out guides happened to deplete `Trhr` RNA detectably in this cell group, the true value could be 1 even without downstream DEGs.
- The training data argue against a sustained basal GPCR-loss transcriptome, but they do not rule out evoked TRH responses, transient immediate-early changes missed by a 3-4 week endpoint, non-neuronal pituitary or thyroid phenotypes, or phenotypes that require germline loss, dense perturbation, or ligand stimulation.
