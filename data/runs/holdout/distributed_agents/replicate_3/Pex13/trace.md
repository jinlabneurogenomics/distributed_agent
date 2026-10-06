# Question and endpoint

The requested held-out target list contains one perturbation, `Pex13`. I interpreted `n_degs` as the count of all measured genes, including the perturbed target transcript if it was measured, with `pvals_adj < 0.05` in `151 TH Prkcd Grin2c Glut` cells after the same Scanpy/Wilcoxon testing used for the training CSV.

The key ambiguity I resolved was whether to predict a broad downstream peroxisomal state or a possible self-transcript-only call. The endpoint counts both. I therefore reasoned about two pieces separately:

- downstream response breadth after loss of a PEX13 peroxisomal import component;
- whether the `Pex13` transcript itself might be reduced enough to add one FDR-significant row.

# Sources used

- `175_Pex13.csv`: confirmed the only requested held-out target is `Pex13`.
- `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`: provided exact `n_degs` values for 1,674 non-held-out perturbations in the focal cell group. The distribution is very zero-inflated: 469/1674 perturbations have any FDR < 0.05 DEG, 193 have more than one, and only 103 have more than 10.
- `training_de_all_cell_groups.parquet`: row-level expression evidence for non-held-out targets.
- Distributed Agents selected same-experiment corpus, release `perturbai-july-260713-sourceguard-1773-v1`: used as the internal curated interpretation layer over this Perturb-seq experiment. Relevant records were `Pex14:F001-F004`, `Pex1:F002-F004`, and the corpus claim `claim:a3b54f2b17cb911aec15`.
- Distributed Agents runtime profile comparison: I compared `Pex1`, `Pex14`, `Abcd3`, `Acbd5`, `Agps`, `Far1`, and `Hsd17b4` in the focal cell group and inspected `Pex1`/`Pex14` against the other peroxisome-linked peers.
- Reactome, `Peroxisomal protein import`, `R-HSA-9033241`, for placing PEX13/PEX14 at the PEX5/PEX7 docking/translocation step and PEX1 in receptor export/recycling.
- Literature on peroxisomal import and PEX13 biology:
  - Maxwell et al. 2003, DOI `10.1128/MCB.23.16.5947-5957.2003`, PMID `12897163`: germline mouse `Pex13` disruption blocks matrix-protein import, impairs fatty-acid oxidation and plasmalogen synthesis, and gives a Zellweger-like neonatal phenotype with cortical lamination defects.
  - Liu, Ma and Subramani 2012, DOI `10.1016/j.ceb.2012.05.003`, PMID `22683191`: review of PTS cargo import, PEX13/PEX14 docking, receptor ubiquitination, and ATP-dependent receptor recycling.
  - Otera et al. 2002, DOI `10.1128/MCB.22.6.1639-1655.2002`, PMID `11865044`: mammalian PEX5 uses WXXXF/Y motifs to interact with PEX14 and PEX13 during PTS1/PTS2 import.
  - Schell-Steven et al. 2005, DOI `10.1128/MCB.25.8.3007-3018.2005`, PMID `15798189`: PEX13 directly binds PEX14 and association with the docking complex is required for peroxisomal matrix protein import.
  - Braverman et al. 2015, DOI `10.1016/j.ymgme.2015.12.009`, PMID `26750748`: review of PEX-gene peroxisome biogenesis disorders in the Zellweger spectrum.
  - Berger et al. 2015, DOI `10.1016/j.bbamcr.2015.12.005`, PMID `26686055`: review of peroxisomal functions and disease mechanisms in brain development and function.

# Computations over the training data

I first filtered the training endpoint CSV for peroxisomal protein-import and metabolism genes represented in the focal-cell training set. The exact endpoint counts were:

| training perturbation | closest biology relative to PEX13 | observed focal `n_degs` |
|---|---|---:|
| `Pex14` | core PEX13 partner in the docking/translocation module | 1 |
| `Pex1` | AAA ATPase in PEX5 receptor export, same matrix-protein import cycle | 0 |
| `Abcd3` | peroxisomal membrane VLCFA/acyl-CoA transporter | 0 |
| `Acbd5` | peroxisomal tether and lipid-handling factor | 0 |
| `Hsd17b4` | peroxisomal beta-oxidation enzyme | 0 |
| `Agps` | ether-lipid synthesis enzyme | 1 |
| `Far1` | ether-lipid synthesis regulator | 2 |

I then loaded the focal-cell DE rows for these targets from the parquet:

```python
table = ds.dataset(parquet_path).to_table(
    columns=[
        "names", "scores", "logfoldchanges", "pvals_adj",
        "group_name", "gene_target", "n_pert_matched", "n_ctrl_matched",
    ],
    filter=(
        (pc.field("group_name") == "151 TH Prkcd Grin2c Glut")
        & pc.field("gene_target").isin(peroxisome_targets)
    ),
)
```

The row-level evidence matched the endpoint counts and showed that the nonzero counts were isolated:

| target | FDR < 0.05 rows in `151 TH Prkcd Grin2c Glut` | next-best rows |
|---|---|---|
| `Pex14` | one row, `Pex14` itself, log2FC `-0.907`, adjusted p `3.74e-7` | next genes `Hspa4l`, `Spock1`, `Inpp5b`, all adjusted p `0.382` |
| `Pex1` | none | all adjusted p-values were `1.0` in the top p-value sort |
| `Abcd3` | none | all adjusted p-values were `1.0` |
| `Acbd5` | none | best adjusted p `0.456` |
| `Hsd17b4` | none | all adjusted p-values were `1.0` |
| `Agps` | one row, `Dhcr24` up, log2FC `0.660`, adjusted p `0.00192` | `Lmtk3` and `Cyp51` were weaker at FDR 0.05, adjusted p `0.0769` |
| `Far1` | two rows, `Far1` itself down and `Tial1` up | `Tial1` did not overlap the `Agps` or PEX import signatures |

I also checked whether the `Pex13` measured gene was a hidden component of any represented peroxisome response. In the focal rows for `Pex1`, `Pex14`, `Abcd3`, `Acbd5`, `Agps`, `Far1`, and `Hsd17b4`, measured `Pex13` had adjusted p `1.0` every time, with small log2 fold changes from `-0.185` to `0.151`. Across all 1,674 training perturbations, `Pex13` was present as a measured focal-cell feature and its lowest adjusted p-value was `0.0935`, in the broad `Hnrnpu` signature. This argues that `Pex13` is testable but not a recurrent compensatory or stress-response transcript.

For a separate expression-pattern check, the Distributed Agents runtime profile comparison over `Pex1`, `Pex14`, `Abcd3`, `Acbd5`, `Agps`, `Far1`, and `Hsd17b4` classified four of the seven nodes as having no significant features and three as having only `1_to_9_significant_features`. Every `Pex1`/`Pex14` significant-feature intersection with the lipid and beta-oxidation comparators was zero. I did not give weight to high top-tail correlations among all-zero signatures because their leading genes were nonsignificant low-expression tails; the useful signal was the absence of shared FDR-supported genes.

# Target-specific reasoning

## `Pex13`

`Pex13` is a core peroxisomal import/docking factor. PEX13 and PEX14 interact at the peroxisomal membrane and help receive PEX5/PEX7 cargo complexes during PTS1/PTS2 matrix-protein import, while the PEX1/PEX6/PEX26 AAA machinery later extracts ubiquitinated PEX5 for receptor recycling. That external biology makes `Pex14` the best training analog and `Pex1` a same-import-cycle counterexample; `Abcd3`, `Acbd5`, `Hsd17b4`, `Agps`, and `Far1` are weaker same-organelle comparators for peroxisomal transport, beta-oxidation, and ether-lipid biology.

The biologically broad expectation from germline or congenital PEX13 loss is severe. Maxwell et al. showed that mouse `Pex13` inactivation disrupts peroxisome biogenesis, matrix import, fatty-acid oxidation, and plasmalogen synthesis and causes neonatal Zellweger-like disease. I did not transfer that breadth directly to the prediction because this assay perturbed sparse, postmitotic P16 neurons for only 3 to 4 weeks and measured nuclear RNA only in recovered NeuN-positive nuclei. Germline developmental migration defects, metabolic lipid endpoints, catalase mislocalization, pexophagy, and glial/neuroinflammatory responses are mostly outside the readout.

Within this exact Perturb-seq readout, the best analogs were transcriptionally buffered:

- `Pex14` had `n_degs = 1`, and its only focal FDR < 0.05 row was `Pex14` itself. The same-experiment Distributed Agents corpus further reports that `Pex14` loss produced no FDR < 0.10 downstream transcript in any of 23 neuronal cell groups and did not induce obvious peroxisome-biogenesis, lipid-metabolic, redox, ISR, autophagy/lysosomal, or BDNF-TrkB marker transcripts.
- `Pex1` had `n_degs = 0` in `151 TH Prkcd Grin2c Glut`. The corpus likewise summarized acute `Pex1` perturbation as failing to trigger peroxisome-import, lipid-metabolism, oxidative-stress, pexophagy/autophagy, ISR, or UPR RNA modules in any measured neuronal class.
- `Abcd3`, `Acbd5`, and `Hsd17b4` were zero in the focal endpoint, while `Agps` and `Far1` had only singleton or two-gene target-specific hits. `Dhcr24` up-regulation after `Agps` and `Tial1` up-regulation after `Far1` were not reproduced by `Pex1`, `Pex14`, `Abcd3`, `Acbd5`, or `Hsd17b4`. This makes them counterexamples rather than evidence for a shared peroxisome response.

I therefore predicted no downstream PEX13-induced module. The remaining question was the perturbed transcript itself. `Pex13` is measured in the focal rows, and the nearest direct docking analog, `Pex14`, contributed exactly one DEG via its own self-transcript reduction. On the other hand, `Pex1` did not show a focal self call, and the dataset documentation warns that target RNA loss is not a reliable editing-strength proxy. I treated a one-gene self call as slightly more likely than zero because the closest represented membrane-docking partner was self-only rather than absolutely flat.

Final point prediction: `Pex13 = 1`, with the single predicted DEG most likely to be `Pex13` itself, not a peroxisome stress or lipid-compensation program.

# Limits of the reasoning

The prediction is an extrapolation because `Pex13` has no held-out DE rows in the supplied inputs and no target-specific same-experiment corpus record. The exact FDR crossing of the `Pex13` self transcript depends on guide locations, mutant-transcript decay, focal recovered-cell count, and baseline detection; those are not visible for the held-out perturbation. A true value of 0 would be nearly as biologically plausible if the self transcript stayed above FDR.

The closest training analog is `Pex14`, but many import factors that would sharpen the estimate, including `Pex5`, `Pex6`, `Pex10`, `Pex12`, `Pex26`, `Pex3`, `Pex16`, and `Pex19`, were not represented in the focal training count table. The peroxisome beta-oxidation and ether-lipid comparators test the same organelle, not the same import step.

Finally, the null downstream prediction applies only to the acute sparse CRISPR, postmitotic NeuN-positive snRNA-seq endpoint. It should not be read as evidence that PEX13 loss preserves peroxisome import, peroxisomal lipids, cell survival, glial responses, or developmental phenotypes.
