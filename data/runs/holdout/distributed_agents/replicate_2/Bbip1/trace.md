# Held-out DEG-count prediction for 151 TH Prkcd Grin2c Glut

## Question and resolved ambiguity

The requested held-out target list contains one gene:

- `Bbip1`

For this gene I predict the number of genes that would pass `pvals_adj < 0.05` in the `151 TH Prkcd Grin2c Glut` cell group after acute sparse AAV-PHP.eB CRISPR loss of function. The held-out target itself is absent as a `gene_target` in the supplied differential-expression parquet and absent from the training-count CSV, so the prediction must be inferred from represented perturbations and gene function.

I treated `n_degs` exactly as the training CSV does: an integer count of all measured gene symbols whose Benjamini-Hochberg-adjusted Wilcoxon p-value is below 0.05 in the focal cell group. Self-transcript changes count when the target transcript passes FDR, as seen for `Ttc8` and `Arl3` below.

## Sources used

- Input target manifest: `023_Bbip1.csv`.
- Input focal endpoint file: `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
- Input DE parquet: `training_de_all_cell_groups.parquet`.
- Internal same-experiment knowledge layer: Distributed Agents corpus release `perturbai-july-260713-sourceguard-1773-v1`.
  - `target_context(Bbs5)`, `target_context(Ttc8)`, `target_context(Ift88)`, and `target_context(Lztfl1)` were used because those are the most relevant represented BBSome / IFT / BBSome-regulator perturbations.
  - The corpus had no `Bbip1` record, as expected for a held-out target.
- Distributed Agents runtime observed-profile analysis over the supplied parquet: `profile_compare` and `profile_inspect` on BBSome, IFT, transition-zone, and ciliary-signaling comparators in `151 TH Prkcd Grin2c Glut`.
- PubMed searches through the BioEval literature tool for primary BBIP1 / BBSome references:
  - Loktev et al., 2008, *Developmental Cell*, DOI `10.1016/j.devcel.2008.11.001`, PMID `19081074`.
  - Scheidecker et al., 2013, *Journal of Medical Genetics*, DOI `10.1136/jmedgenet-2013-101785`, PMID `24026985`.
  - Katoh et al., 2015, *Journal of Cell Science*, DOI `10.1242/jcs.168740`, PMID `25964651`.
  - Seo et al., 2011, *PLoS Genetics*, DOI `10.1371/journal.pgen.1002358`, PMID `22072986`.

## Computation on the supplied data

The target manifest had exactly one requested row, `Bbip1`.

The focal training count table contained 1,674 non-held-out perturbations. Its endpoint was highly zero-inflated:

| `n_degs` bin | training perturbations |
| --- | ---: |
| 0 | 1205 |
| 1 | 276 |
| 2-5 | 65 |
| 6-10 | 25 |
| 11-50 | 45 |
| 51-100 | 16 |
| 101-500 | 27 |
| >500 | 15 |

For mechanistic comparators I pulled all focal-group parquet rows for BBSome, IFT, transition-zone, and ciliary-signaling genes represented among the training perturbations:

```python
flt = (
    ds.field("group_name") == "151 TH Prkcd Grin2c Glut"
) & ds.field("gene_target").isin(ciliary_targets)
```

This returned 17,259 measured genes for each of 35 selected ciliary comparators. I then checked `pvals_adj < 0.05` counts, inspected the leading nominal features, and used the Wilcoxon `scores` vectors for pairwise full-profile comparisons.

Key profile results:

- `Bbs5` had 0 FDR<0.05 features in the focal cell group; its best FDR value was 0.220 for `Ptprn`.
- `Ttc8` had 1 FDR<0.05 feature, and that was its own target transcript, `Ttc8` (`log2FC = -0.663`, Wilcoxon score `-6.02`, FDR `3.07e-05`).
- `Arl3` likewise had exactly 1 FDR<0.05 feature, its own target transcript.
- Direct and adjacent ciliary comparators `Ift88`, `Ift81`, `Ift43`, `Kif3b`, `Dync2h1`, `Dync2i1`, `Cep290`, `Lztfl1`, `Ttc21b`, `Cplane1`, `B9d1`, `Rpgrip1l`, `Rpgr`, `Rfx3`, `Gli1`, `Gli2`, `Gpr161`, `Smo`, `Ptch1`, `Ptch2`, `Htr6`, and `Adcy3` all had 0 focal DEGs.
- BBSome and IFT score-vector similarity in this cell group was close to zero. Examples from the profile runtime:

| focal node | peer | focal `n_degs` | peer `n_degs` | Pearson on Wilcoxon scores | cosine | top-50 FDR feature intersections |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| `Bbs5` | `Ttc8` | 0 | 1 | 0.0309 | 0.0289 | 0 significant |
| `Bbs5` | `Ift88` | 0 | 0 | 0.0615 | 0.0598 | 0 significant |
| `Bbs5` | `Lztfl1` | 0 | 0 | 0.0480 | 0.0621 | 0 significant |
| `Bbs5` | `Ttc21b` | 0 | 0 | 0.0386 | 0.0442 | 0 significant |
| `Bbs5` | `Cep290` | 0 | 0 | 0.0029 | 0.0038 | 0 significant |
| `Ttc8` | `Ift88` | 1 | 0 | 0.0594 | 0.0596 | 0 significant |
| `Ttc8` | `Lztfl1` | 1 | 0 | 0.0553 | 0.0523 | 0 significant |
| `Ttc8` | `Kif3b` | 1 | 0 | 0.0347 | 0.0346 | 0 significant |
| `Ttc8` | `Ttc21b` | 1 | 0 | 0.0026 | 0.0016 | 0 significant |
| `Ttc8` | `Cep290` | 1 | 0 | -0.0047 | -0.0048 | 0 significant |

These pairwise values argue against a hidden coherent ciliary transcriptome in `151 TH Prkcd Grin2c Glut`: the direct BBSome comparators have no shared FDR genes and only noise-scale ranked-vector concordance.

## Biological comparison for `Bbip1`

`Bbip1`, also called BBIP10 or BBS18, encodes a small core BBSome component. Loktev et al. discovered BBIP10 as a BBSome-associated protein that localizes to primary cilia and is needed for ciliogenesis; Scheidecker et al. later identified BBIP1 as a Bardet-Biedl syndrome gene; Katoh et al. mapped BBIP1/BBS18 as a linker between BBS4 and TTC8/BBS8 in the BBSome. Seo et al. showed that LZTFL1 regulates BBSome and Smoothened ciliary trafficking, making `Lztfl1` an adjacent regulator rather than a core subunit.

The most appropriate measured training perturbations were therefore:

| training perturbation | focal `n_degs` | why it is informative for `Bbip1` |
| --- | ---: | --- |
| `Bbs5` | 0 | Core BBSome subunit; this is the most direct represented complex mate after `Bbip1` itself. In the focal group it had no FDR genes, and the Distributed Agents corpus report for `Bbs5` found no broad Hedgehog, ciliary-GPCR, UPR/ISR, autophagy, or BBSome/IFT module anywhere in the assayed neuronal atlas. |
| `Ttc8` / `Bbs8` | 1 | Core BBSome subunit, and Katoh et al. place BBIP1 as a linker to TTC8. The only focal FDR gene was `Ttc8` itself, not a downstream module. The corpus report for `Ttc8` describes transcriptional buffering across 22 neuronal groups despite target self-downregulation. |
| `Lztfl1` | 0 | BBSome trafficking regulator linked to ARL6/BBSome ciliary entry and Smoothened trafficking. It did not induce a focal DEG in this cell group and its sparse all-atlas `Cyld` response occurred in a different GABAergic class, not here. |
| `Ift88`, `Ift81`, `Ift43` | 0, 0, 0 | IFT-B/ciliary-trafficking comparators. None had a focal DEG, and the internal IFT88 report specifically notes that cilium-related perturbations converged mainly by transcriptional buffering rather than by a shared IFT knockout transcriptome. |
| `Kif3b`, `Dync2h1`, `Dync2i1`, `Ttc21b` | 0, 0, 0, 0 | Anterograde motor, dynein-2 retrograde motor, and IFT-A comparators. These probe whether general disruption of ciliary transport gives the focal cell group a nuclear RNA response; it did not. |
| `Cep290`, `Cplane1`, `B9d1`, `Rpgrip1l`, `Rpgr`, `Rfx3` | 0, 0, 0, 0, 0, 0 | Transition-zone, ciliary-gate, and ciliopathy-associated controls. They are less direct than BBSome components but useful counterexamples to a generic ciliopathy RNA state; all were focal-zero. |
| `Gli1`, `Gli2`, `Smo`, `Ptch1`, `Ptch2`, `Gpr161`, `Adcy3`, `Htr6`, `Mchr1` | 0 each | Ciliary signaling and ciliary GPCR nodes. Their focal-zero counts argue that the basal juvenile NeuN+ readout is not engaging a broad cilium-dependent Hedgehog or ciliary-GPCR transcriptional circuit. |
| `Arl3` | 1 | A ciliary lipidated-protein trafficking node that provides a positive counterexample: the assay can produce a singleton for a ciliary target, but in the focal group that singleton was the `Arl3` self-transcript. This does not support a multi-gene `Bbip1` effect. |

The same-experiment Distributed Agents corpus summarized the broader represented ciliary landscape with a high-confidence claim that acute perturbation of represented ciliary trafficking and ciliary signaling genes in postnatal NeuN+ neurons is largely buffered at the basal nuclear RNA level rather than producing a coherent ciliary transcriptional module. That corpus-level statement fits the focal endpoint: nearly every mechanistic neighbor of `Bbip1` had `n_degs = 0`, and the exceptions had only the target RNA itself as a DEG.

## Prediction rationale

I predict `Bbip1` will have no focal DEGs.

The decision is driven primarily by within-dataset evidence:

- The only represented core BBSome subunits were flat or self-only in `151 TH Prkcd Grin2c Glut`: `Bbs5 = 0`, `Ttc8 = 1` with only `Ttc8` down.
- The represented BBSome regulator `Lztfl1` and the nearby IFT / dynein / transition-zone perturbations were all zero in this same cell group.
- Whole-vector Wilcoxon-score similarities among these targets were near zero, so the nominal tails do not reveal a shared ciliary response hidden below FDR.

External biology determined which zeroes were the right zeroes to trust. `Bbip1` is a BBSome component, so `Bbs5` and `Ttc8` are much better analogs than unrelated training targets with large `n_degs`; `Lztfl1`, `Ift88`, `Ift81`, `Ift43`, and `Kif3b` are appropriate pathway neighbors, but their nonconvergence shows that ciliary membership alone does not imply a shared neuronal RNA signature.

I considered assigning 1 rather than 0 because `Ttc8` and `Arl3` each had self-transcript singletons, and a self-transcript `Bbip1` call would make the count nonzero without any downstream response. I kept the point estimate at 0 because the closest focal BBSome subunit, `Bbs5`, did not pass FDR for its own transcript, `Ift88`/`Ift81`/`Ift43` also did not pass for their own transcripts, and `Bbip1` was not directionally reduced by BBSome/IFT neighbor perturbations as a measured feature. With no represented BBIP1-specific microtubule-acetylation signature in the focal cell group, 0 is the best integer prediction.

## Limits

- `Bbip1` was held out completely; there is no direct BBIP1 perturbation signature in either input.
- Only `Bbs5` and `Ttc8` represented the core BBSome in training. `Bbs1`, `Bbs2`, `Bbs4`, `Bbs7`, `Bbs9`, `Arl6`, and the BBS chaperonin-like genes were absent as perturbation targets, so the BBSome comparison is strong but incomplete.
- A zero-DEG snRNA response does not mean cilia are intact. This assay did not image primary cilia, measure BBSome cargo localization, quantify BBIP1 protein, score tubulin acetylation, stimulate Smoothened, or assay photoreceptor, kidney, olfactory epithelial, or hypothalamic feeding phenotypes.
- Several focal ciliary comparators had only 99-328 matched perturbed nuclei, so weak single-gene effects can move between 0 and 1 depending on power and target RNA recovery.
- Acute P16-to-P37/44 mosaic neuronal CRISPR is mechanistically different from a germline BBS knockout. The prediction is for this FDR-count endpoint, not for organismal Bardet-Biedl syndrome severity or ciliary function.

## Final point estimate

`Bbip1`: **0**
