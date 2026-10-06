# DEG-count prediction for `151 TH Prkcd Grin2c Glut`

## Question and resolved ambiguities

The requested held-out target list contains one perturbation:

```text
Zfp398
```

I interpreted `n_degs` as the exact endpoint in the task statement: in the focal thalamic glutamatergic class `151 TH Prkcd Grin2c Glut`, count measured genes with `pvals_adj < 0.05` in the Wilcoxon differential-expression table. `Zfp398` was absent from the supplied training parquet as a perturbation and absent from the supplied focal-cell training count CSV, so its own hidden count and expression signature were not available.

I did not use the measured target-transcript fold change as an editing-efficiency score. In this postnatal mosaic CRISPR/single-nucleus design, direct target RNA loss is not a calibrated proxy for functional knockout strength or downstream DEG burden.

## Sources

- `training_de_all_cell_groups.parquet`: focal rows from the non-held-out perturbations, especially adjusted p-values and log2 fold changes for zinc-finger and chromatin-regulatory perturbations.
- `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`: observed `n_degs` for 1,674 non-held-out targets in the focal cell group.
- Distributed Agents same-experiment semantic corpus, release `perturbai-july-260713-sourceguard-1773-v1`: queried `target_context` and `related_targets` for `Zfp398`; the target had no curated Findings, Claims, or graph neighbors in this release.
- PubMed literature:
  - Conroy et al. 2002, J. Biol. Chem., DOI `10.1074/jbc.M107702200`, PMID `11779858`: described ZER6, the human ZNF398 ortholog, as a C2H2 zinc-finger transcription factor with p52 and p71 isoforms.
  - Zorzan et al. 2020, Nature Communications, DOI `10.1038/s41467-020-16205-9`, PMID `32398665`: placed ZNF398 downstream of TGF-beta with SMAD3/EP300 at active regulatory elements in human pluripotent stem cells.
  - Kwag et al. 2025, Biochem. Biophys. Res. Commun., DOI `10.1016/j.bbrc.2025.151316`, PMID `39809138`: found that neuronal p52-ZER6 represses `MT3` and can raise reactive oxygen species in HT-22/SH-SY5Y models.
  - Bailey et al. 2008, Chromosoma, DOI `10.1007/s00412-008-0155-7`, PMID `18369653`: characterized ZNF397/Zfp397 as a SCAN C2H2 zinc-finger centromere protein and reported that mouse Zfp397 knockout was non-essential.
- Ensembl REST over mouse GRCm39, queried 2026-09-23: `Zfp398` maps to `ENSMUSG00000062519` and has a one-to-one high-identity human ortholog, `ZNF398`/`ENSG00000197024`.

## Computation over the supplied training data

1. Loaded the held-out manifest and confirmed that the only requested target is `Zfp398`.
2. Loaded the focal-cell training count CSV. Its distribution is strongly zero-heavy: 1,205/1,674 training perturbations have `n_degs = 0`, the median is 0, the 75th percentile is 1, the 90th percentile is 2, and the 95th percentile is 18. The extreme tail is made of broad core processes, for example `Uba5` at 2,677 DEGs, `Tpr` at 1,768, `Sin3a` at 1,433, splicing factors, proteasome components, and chromatin regulators.
3. Scanned the focal `151 TH Prkcd Grin2c Glut` rows of the parquet for all training perturbations whose names begin with `Zfp`, `Zbtb`, `Zkscan`, `Zmynd`, `Zswim`, `Zfpm`, or `Zc3h`. This yielded 43 zinc-finger-related perturbations; 33/43 had zero DEGs in the focal count file.
4. For candidate analogs and counterexamples, I counted focal rows with `pvals_adj < 0.05` and inspected the most significant genes. I used adjusted p-value support, not the largest absolute log-fold changes, because the biggest log-fold changes in sparse snRNA-seq were often unsupported rows with `pvals_adj = 1`.
5. I also looked for the proposed ZER6 neuronal marker `Mt3` in the focal signatures. `Mt3` is measurable and moves in several very broad signatures (`Wac`, `Elp1`, `Brd4`, `Sin3a`, `Psmb4`, `Zbtb7a`, `Zmynd8`, and others), but these regulators do not constitute a Zfp398-specific expression analog.

The exact operation for the focal analog table was:

```python
f = (
    (pc.field("group_name") == "151 TH Prkcd Grin2c Glut")
    & pc.field("gene_target").isin(selected_zinc_finger_targets)
)
df = dataset.to_table(
    columns=["names", "gene_target", "logfoldchanges", "pvals_adj",
             "scores", "n_pert_matched", "n_ctrl_matched"],
    filter=f,
).to_pandas()
```

## Target-specific reasoning

### `Zfp398`

**Mechanistic prior.** `Zfp398` is an ortholog of human `ZNF398`/ZER6 and encodes a protein-coding C2H2 zinc-finger transcription factor. Published work supports sequence-specific transcriptional regulation by ZER6 isoforms: the original ZER6 study identified p52 and p71 isoforms and an estrogen-receptor-alpha interaction (Conroy et al. 2002), ZNF398 can cooperate with SMAD3/EP300 downstream of TGF-beta in human pluripotent cells (Zorzan et al. 2020), and p52-ZER6 can repress `MT3` in neuronal cell lines with oxidative-stress consequences (Kwag et al. 2025). That argues against treating the gene as a pseudogene or as completely incapable of transcriptional effects.

**Closest within-dataset comparators.** The training set did not contain a direct paralog with a known shared ZER6 pathway. I therefore used the following as weak analogs that calibrate this assay for C2H2/KRAB or nearby zinc-finger transcription-factor perturbations rather than as mechanistically interchangeable replacements:

| training perturbation | observed `n_degs` | focal expression evidence |
| --- | ---: | --- |
| `Zfp397` | 0 | 147 matched perturbed nuclei; no FDR-significant genes; minimum adjusted p-value 1.0. This is a SCAN/C2H2 zinc-finger factor rather than a known ZER6 partner, and Bailey et al. found mouse Zfp397 knockout to be viable/non-essential, so it is a useful quiet C2H2 comparator. |
| `Zkscan1` | 0 | 180 matched perturbed nuclei; no significant focal genes; minimum adjusted p-value 1.0. |
| `Zkscan16` | 0 | 247 matched perturbed nuclei; no significant focal genes; minimum adjusted p-value 1.0. |
| `Zfp322a` | 0 | 215 matched perturbed nuclei; no significant focal genes; best adjusted p-value 0.927. |
| `Zfp664` | 0 | 222 matched perturbed nuclei; no significant focal genes; minimum adjusted p-value 1.0. |
| `Zfp950` | 0 | 202 matched perturbed nuclei; no significant focal genes; best adjusted p-value 0.949. |
| `Zfp961` | 0 | 161 matched perturbed nuclei; no significant focal genes; minimum adjusted p-value 1.0. |
| `Zfp846` | 0 | 183 matched perturbed nuclei; no significant focal genes; best adjusted p-value 0.500. |
| `Zfp451` | 0 | 178 matched perturbed nuclei; no significant focal genes; minimum adjusted p-value 1.0. |

Those nulls were not isolated low-power one-offs. They are embedded in a focal endpoint where most zinc-finger-related perturbations were silent: 33 of the 43 inspected `Zfp`/`Zbtb`/`Zkscan`/`Zmynd`/`Zswim`/`Zfpm`/`Zc3h` training perturbations had zero DEGs.

**Counterexamples considered.** I did not convert zinc-finger family membership directly into a zero call, because the training set contains clear active exceptions:

| training perturbation | observed `n_degs` | focal expression evidence and why it is an imperfect analog |
| --- | ---: | --- |
| `Zbtb7a` | 841 | A very broad signature with top hits `Pnma3`, `Col9a3`, `Gpc1`, `Usp11`, and `Sema4a` at adjusted p-values down to `1.2e-41`. It is a BTB/POZ zinc-finger regulator with a large phenotype in this exact cell group, but it is not a close Zfp398 paralog or ZER6 pathway member. |
| `Zfp423` | 150 | A coherent but distinct signature with `Grid2ip` and `Cd47` down and `Ntsr1` up; minimum adjusted p-value `3.1e-45`. This is a developmental multi-zinc-finger regulator, not a KRAB-like ZER6 analog. |
| `Zmynd8` | 74 | Significant `Ptgds`, `Msra`, `Lhcgr`, and `Capn3` up; minimum adjusted p-value `3.1e-19`. ZMYND8 is better viewed as a chromatin reader/coregulator than as a sequence-specific ZER6 counterpart. |
| `Zfp236` | 19 | A small but real signature led by `Ogt` and `Eif4a2` down. The signature is much narrower than the active `Zbtb7a`/`Zfp423` tail. |
| `Zfp148`, `Zc3h14`, `Zbtb18` | 8, 6, 5 | Detectable but very narrow responses, showing that the assay can assign single-digit counts to weak transcriptional regulators when a few genes clear BH correction. |

The broad counterexamples had little overlap with each other: `Zbtb7a` versus `Zfp423` shared 28 significant genes, `Zbtb7a` versus `Zmynd8` shared 17, and `Zfp423` versus `Zmynd8` shared 5. Thus the active zinc-finger examples do not define a common generic ZFP signature that could be transferred to `Zfp398`.

**Zero/nonzero decision.** The literature gives Zfp398 plausible direct targets, especially `Mt3`, but it does not tie Zfp398 to the large neuronal stress, splicing, proteasome, or chromatin-state signatures that dominate the high `n_degs` tail in this focal cell group. `Mt3` itself was assay-visible, yet its significant movement in the training data occurred downstream of broad regulators rather than in a ZER6-like module. Against that indirect prior, the strongest within-dataset calibration is that many focal C2H2/KRAB/SCAN zinc-finger perturbations with comparable recovered nucleus counts have no BH-significant genes at all.

I therefore predict that partial acute loss of `Zfp398` in recovered `151 TH Prkcd Grin2c Glut` neurons will be below the FDR 0.05 threshold, or at most a subthreshold/narrow `Mt3`-centered effect. The point prediction is:

```text
Zfp398    0
```

## Limits

- The Distributed Agents corpus was silent for `Zfp398`; absence from that target-scoped corpus is not proof that no relevant biology exists.
- The best mechanistic `Zfp398` literature comes from human pluripotent cells, cancer/estrogen signaling, and neuronal cell-line overexpression, not from acute loss of mouse Zfp398 in postmitotic thalamic glutamatergic neurons.
- The C2H2/KRAB/SCAN training perturbations are family-level calibrators, not validated Zfp398 paralogs or members of the same protein complex.
- A zero prediction means no measured gene is expected to pass BH FDR 0.05 in this assay. It does not imply absence of all molecular effects, absence of target engagement, or absence of a narrow direct-target effect below detection.
