# Mc3r DEG-count prediction

## Question and resolved ambiguities

The held-out target for this run is `Mc3r`; it appears exactly once in the
requested-target CSV and was absent from the supplied training count table. I
interpreted the endpoint as a point prediction for the number of measured genes
with `pvals_adj < 0.05` in the focal `151 TH Prkcd Grin2c Glut` group after
P16 mosaic CRISPR loss of function, using the same definition as
`151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`. The count is assay- and
power-specific and includes any row that passes FDR, including a self-transcript
row when one happens to pass; I did not treat target-RNA knockdown as an editing
efficiency estimate.

The target list is unranked, so the only ordering constraint is that
`answer.txt` must preserve the CSV order.

## Sources used

- Declared PerturbAI whole-brain atlas training files:
  `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`
  and
  `training differential-expression dataset`.
- Run-local task bindings, compact source coverage, capability manifest, and
  dataset portrait under `codex_runtime/pipeline`.
- The internal `perturbai-july-260713-sourceguard-1773-v1` same-experiment
  corpus, using the bounded Findings and calibration query tools for curated
  reports on the measured melanocortin and feeding-circuit comparators
  `Mc1r`, `Mc2r`, `Agrp`, `Lepr`, and `Gnas`.
- PubMed-indexed external literature for prior MC3R and melanocortin biology:
  Lee et al. 2001, DOI `10.1046/j.1432-1327.2001.01900.x`, PMID 11168397;
  Wilczynski et al. 2005, DOI `10.1002/med.20037`, PMID 16044415;
  Rediger et al. 2012, DOI `10.1159/000334903`, PMID 22327910;
  Yanik and Durhan 2022, DOI `10.4274/jcrpe.galenos.2022.2022-5-21`,
  PMID 36053086; Gui et al. 2023, DOI `10.1016/j.celrep.2023.113188`,
  PMID 37792535.

## Quantitative calibration from the focal training endpoint

The training endpoint in `151 TH Prkcd Grin2c Glut` is sparse. Among 1,674
non-held-out perturbations, 469 had any FDR 0.05 hit and 1,205 were zero. The
distribution was median 0, 75th percentile 1, 90th percentile 2, and 95th
percentile 18, with the very high counts reserved for broad RNA-processing,
proteostasis, chromatin, or cell-essential targets such as `Uba5`, `Tpr`,
`Sin3a`, `Rnpc3`, and `Zbtb7a`.

I then read only the focal-cell Parquet rows for melanocortin, feeding-GPCR, and
Gs/cAMP genes represented in training. The directly relevant focal counts were:

| training perturbation | `151 TH Prkcd Grin2c Glut` `n_degs` | focal expression-pattern evidence |
| --- | ---: | --- |
| `Mc1r` | 0 | 257 perturbed nuclei; every row had `pvals_adj = 1.0`. |
| `Mc2r` | 0 | 160 perturbed nuclei; every row had `pvals_adj = 1.0`. |
| `Agrp` | 0 | 261 perturbed nuclei; every row had `pvals_adj = 1.0`. |
| `Lepr` | 0 | 202 perturbed nuclei; every row had `pvals_adj = 1.0`. |
| `Mchr1` | 0 | 196 perturbed nuclei; every row had `pvals_adj = 1.0`. |
| `Npy1r` | 0 | 67 perturbed nuclei; every row had `pvals_adj = 1.0`. |
| `Npy2r` | 0 | 120 perturbed nuclei; best focal row `q = 0.958`. |
| `Npy5r` | 0 | 100 perturbed nuclei; every row had `pvals_adj = 1.0`. |
| `Htr2c` | 0 | 126 perturbed nuclei; every row had `pvals_adj = 1.0`. |
| `Ghsr` | 0 | 229 perturbed nuclei; best focal row `q = 0.867`. |
| `Insr` | 0 | 198 perturbed nuclei; every row had `pvals_adj = 1.0`. |
| `Glp1r` | 0 | 132 perturbed nuclei; every row had `pvals_adj = 1.0`. |
| `Gipr` | 0 | 200 perturbed nuclei; every row had `pvals_adj = 1.0`. |
| `Gnas` | 0 | 306 perturbed nuclei; every row had `pvals_adj = 1.0`. |
| `Adcy1` | 0 | 88 perturbed nuclei; best focal row `q = 0.139`. |
| `Adcy3` | 0 | 223 perturbed nuclei; best focal row was self, `q = 0.112`. |
| `Adcy5` | 0 | 154 perturbed nuclei; best focal row `q = 0.912`. |
| `Pde10a` | 0 | 191 perturbed nuclei; best focal row `q = 0.304`. |
| `Pde4b` | 0 | 211 perturbed nuclei; best focal row `q = 0.922`. |
| `Pde4d` | 0 | 192 perturbed nuclei; every row had `pvals_adj = 1.0`. |
| `Prkaca` | 1 | the one significant row was the perturbed gene itself, not a downstream program. |
| `Prkar1a` | 1 | the one significant row was the perturbed gene itself. |
| `Gnao1` | 1 | the one significant row was the perturbed gene itself. |
| `Creb1` | 10 | small downstream TF response headed by `Crem`, consistent with a direct CREB-family perturbation but not with receptor-level GPCR loss. |

The internal July sourceguard corpus independently summarized the same raw
experiment. It called `Mc1r`, `Mc2r`, and `Agrp` pan-neuronal transcriptional
nulls and emphasized that represented Agrp-related or energy-balance targets
such as `Ghsr`, `Htr2c`, `Insr`, `Lepr`, `Npy1r`, `Npy2r`, `Npy5r`, `Mchr1`,
`Mc1r`, and `Mc2r` were flat or nearly flat across the same screen. Its `Gnas`
report likewise found that basal `Gnas` loss did not induce a canonical
GPCR-cAMP-CREB immediate-early module and did not phenocopy `Adcy`, `Pde`,
PKA, or `Creb1`-axis perturbations.

## Mc3r-specific reasoning

`Mc3r` encodes melanocortin receptor 3, a G protein-coupled receptor that is
activated by POMC-derived melanocortins and antagonized or inverse-agonized by
AgRP. Heterologous assays show that MC3R can drive cAMP/CRE-dependent
transcription (Lee et al. 2001), and AGRP is a structured endogenous antagonist
of MC3R/MC4R (Wilczynski et al. 2005). External mouse and review literature
places MC3R in central energy-homeostasis physiology, including presynaptic
and AgRP-neuron roles, interaction with the broader melanocortin-4 receptor
axis, and state-dependent responses to fasting or ghrelin (Rediger et al. 2012;
Yanik and Durhan 2022; Gui et al. 2023).

That prior increases confidence that `Mc3r` is a real neuroendocrine receptor,
but it does not predict a broad basal nuclear-RNA response in the requested
class. The PerturbAI focal class is thalamic glutamatergic, not an isolated
arcuate AgRP, POMC, or MC4R-output population; the perturbation is cell
autonomous and mosaic, so it removes the receptor from each gRNA-carrying
nucleus rather than changing melanocortin peptide tone throughout a circuit;
and there was no fasting, ghrelin, leptin, or MC3R/MC4R ligand challenge to
synchronize GPCR signaling.

The biologically closest measured perturbations therefore form a consistent
zero prior:

- The only measured melanocortin-receptor paralogs, `Mc1r` and `Mc2r`, had
  zero focal DEGs and no hidden same-screen signature neighbor. They are not
  central MC3R substitutes, but their nulls show that melanocortin-receptor
  family membership alone did not create a neuronal DEG response in this assay.
- `Agrp`, the endogenous ligand antagonist for the central MC3R/MC4R branch,
  was also zero in the focal group and pan-neuronal at FDR 0.10 in the July
  corpus. This is a more direct melanocortin-axis counterexample than `Mc1r`
  or `Mc2r`: the secreted peptide axis is biologically central but did not
  produce a recovered-cell DEG state under sparse P16 CRISPR.
- Related feeding and hormone GPCRs or receptors, including `Lepr`, `Ghsr`,
  `Htr2c`, `Mchr1`, `Npy1r`, `Npy2r`, `Npy5r`, `Glp1r`, `Gipr`, and `Insr`,
  were all zero in `151 TH Prkcd Grin2c Glut`; the same-experiment `Lepr` and
  `Agrp` reports specifically warned that the screen did not recover textbook
  hypothalamic neuropeptide/JAK-STAT/melanocortin marker panels.
- The immediate downstream receptor-transducer layer was also focal-zero:
  `Gnas`, `Gnal`, `Adcy1`, `Adcy3`, `Adcy5`, `Pde10a`, `Pde4b`, and `Pde4d`
  had no FDR 0.05 hits. `Creb1` itself gave 10 DEGs, but that is the effect of
  directly perturbing a nuclear transcription factor rather than evidence that
  loss of one unstimulated receptor reaches the same program.

I therefore predicted no gene passing FDR 0.05. The final point estimate is
anchored mainly by within-dataset zeros for the melanocortin, AgRP-related, and
Gs/cAMP training perturbations; external MC3R knowledge was used to decide that
those are appropriate analogs and to avoid treating unrelated high-DEG
housekeeping genes as informative.

## Limits

`Mc3r`, `Mc4r`, `Pomc`, `Mrap`, `Mrap2`, and `Asip` were not perturbation
targets in the training Parquet, so the strongest central melanocortin receptor
comparison is missing. The external MC3R literature usually measures whole-body
energy balance, ligand-stimulated second messengers, conditional knockouts, or
defined AgRP neurons; those are informative about mechanism but are not direct
measurements of P16 mosaic CRISPR in thalamic glutamatergic nuclei. A rare
MC3R-positive subpopulation could be diluted inside the broad `151` label, and
a peptide/receptor perturbation could alter firing, release probability, food
intake, autonomic tone, or survivor abundance without leaving a multi-gene
snRNA-seq signature in recovered cells.

