# Held-out DEG prediction for 151 TH Prkcd Grin2c Glut

## Question and interpretation

The requested held-out target is `Lmx1a`, from
`127_Lmx1a.csv`. I interpreted `n_degs` as the number of measured genes with
Scanpy/Wilcoxon Benjamini-Hochberg adjusted `pvals_adj < 0.05` in the focal
`151 TH Prkcd Grin2c Glut` cell group after sparse postnatal AAV-CRISPR
loss-of-function. `Lmx1a` itself was withheld from both the per-gene DE parquet
and the focal-cell training count CSV, so the prediction is necessarily a
transfer from measured perturbations rather than a direct lookup.

## Sources used

- Input manifest: `127_Lmx1a.csv`; target list contained only `Lmx1a`.
- Training endpoint CSV:
  `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`, used for observed
  `n_degs` in the focal cell group.
- Training differential-expression parquet:
  `training_de_all_cell_groups.parquet`, used for focal-cell signatures and
  FDR status of candidate analogs.
- Distributed Agents same-experiment corpus release
  `perturbai-july-260713-sourceguard-1773-v1`. There was no direct `Lmx1a`
  corpus entry; `Lmx1b`, `En1`, `Foxa2`, `Otx2`, and `Pitx3` findings and the
  claim that represented midbrain dopaminergic developmental regulators do not
  form a shared acute postnatal module were used as same-experiment context.
- External literature found through PubMed:
  - Millonig, Millen and Hatten 2000, Nature, DOI 10.1038/35001573 / PMID
    10693804: positional cloning of the dreher phenotype established `Lmx1a`
    as a LIM-homeodomain roof-plate factor required for dorsal CNS patterning.
  - Nakatani et al. 2009, Developmental Biology, DOI
    10.1016/j.ydbio.2009.12.017 / PMID 20035737: Lmx1a/Lmx1b cooperate with
    Foxa2 in mesencephalic floor-plate and dopaminergic fate specification.
  - Yan et al. 2011, Journal of Neuroscience, DOI
    10.1523/JNEUROSCI.1077-11.2011 / PMID 21880902: `Lmx1a` and `Lmx1b`
    redundantly regulate proliferation, specification, and differentiation of
    midbrain dopaminergic progenitors through programs including Wnt1 and Ngn2.
  - Doucet-Beaupre et al. 2016, PNAS, DOI 10.1073/pnas.1520387113 / PMID
    27407143: sustained Lmx1a/b function supports mitochondrial function and
    survival in adult midbrain dopaminergic neurons after combined conditional
    ablation.
  - Chabrat et al. 2017, Nature Communications, DOI
    10.1038/s41467-017-01042-0 / PMID 29038581: Lmx1a/Lmx1b/Otx2 repress
    `Plxnc1` to guide mesodiencephalic dopaminergic circuit formation.

## Computational checks over the supplied data

I first read the focal training counts and checked exact or pathway-adjacent
analogs:

| training perturbation | focal `n_degs` |
| --- | ---: |
| `Lmx1b` | 0 |
| `En1` | 0 |
| `En2` | 0 |
| `Foxa2` | 0 |
| `Isl1` | 0 |
| `Lhx3` | 0 |
| `Lhx4` | 0 |
| `Msx2` | 0 |
| `Neurod1` | 0 |
| `Neurod2` | 0 |
| `Nr4a1` | 0 |
| `Nr4a3` | 0 |
| `Otx2` | 0 |
| `Pitx2` | 0 |
| `Pitx3` | 0 |
| `Ret` | 0 |
| `Tcf12` | 0 |

For scale, the focal training set had 1,674 observed perturbations, 72.0% of
which had zero FDR-significant DEGs; the median was 0 and the 75th percentile
was 1 DEG. The strong responders in this cell group were mostly general
proteostasis, RNA-processing, or chromatin perturbations rather than lineage
identity transcription factors.

I then used `mcp__distributed_agents_runtime.profile_neighbors` on the focal log-fold
change profiles for `Lmx1b`, `Otx2`, `Pitx3`, `En1`, `Foxa2`, and `Nr4a3`,
with `gene_target` as the profile entity, `names` as the feature, and
`logfoldchanges` as the signed value. The key point from those profiles was not
which weak whole-profile neighbor ranked first, because every one of these
anchors had 0 significant features, but that each anchor was itself classified
as `response_activity_status = no_significant_features` over 17,259 measured
genes. `Lmx1b`, for example, had 0 positive and 0 negative significant genes;
its nearest whole-profile neighbors shared only 0 to 7 of the top 50 positive
or negative tail genes, and those leading overlaps had adjusted p-values of
1.0 rather than forming a subthreshold LMX module.

A targeted parquet scan over the focal group also showed no FDR-significant
movement of the expected dopaminergic or Wnt-linked readouts after the best
analogs: under `Lmx1b`, the rows for `Ctnnb1`, `Ddc`, `En1`, `En2`, `Gsk3b`,
`Nr4a1`, `Nr4a3`, `Plxnc1`, `Ret`, `Slc6a3`, `Tcf7l2`, and `Th` all had
`pvals_adj = 1.0`; `En1`, `Foxa2`, `Otx2`, `Pitx3`, `Msx2`, `Nr4a3`, `Ret`,
and `Tcf12` showed the same all-null pattern for those marker rows. The large
placeholder-like log-fold changes for rarely observed factors such as `Lmx1a`,
`Lmx1b`, `Pitx3`, and `Wnt1` also had `pvals_adj = 1.0` and were not treated as
biological regulation.

## Target-specific reasoning

`Lmx1a` is a direct paralog of `Lmx1b`, and external biology makes `Lmx1b` the
most mechanistically relevant measured perturbation: the two LIM-homeodomain
proteins cooperate in embryonic roof-plate and midbrain dopaminergic
specification, with redundancy in Lmx1a/Lmx1b double-mutant embryos and with
adult functions becoming visible in true SN/VTA dopaminergic neurons after
combined ablation. The focal `151 TH Prkcd Grin2c Glut` population is a
postnatal thalamic glutamatergic group, not the embryonic roof plate or a
matched substantia nigra / ventral tegmental area dopaminergic subtype, so the
literature argues for a possible lineage mismatch rather than for a broad
focal-cell response.

The observed `Lmx1b` perturbation is the strongest within-dataset analog and
had `n_degs = 0` in the focal cell group. The Distributed Agents same-experiment corpus
further reports that acute `Lmx1b` CRISPR produced 0 downstream genes at
FDR < 0.10 in all 23 recovered neuronal groups, and that `Lmx1b` did not
converge with the represented midbrain-dopamine network perturbations
`Foxa2`, `Pitx3`, `En1`, `En2`, `Otx2`, and `Pbx1`. Thus the `Lmx1b` null was
not an isolated quirk of the 151 TH group; it sits inside a measured
neighborhood of postnatal developmental TF perturbations that were mostly flat.

The most relevant counterexamples were also flat in 151 TH cells:
`Foxa2 = 0`, `Otx2 = 0`, `Pitx3 = 0`, `En1 = 0`, and `En2 = 0`. Those genes
cover the same mesencephalic dopaminergic specification and maintenance
biology in which LMX factors are usually interpreted. `Msx2 = 0`, `Isl1 = 0`,
`Lhx3 = 0`, `Lhx4 = 0`, `Ret = 0`, `Nr4a1 = 0`, and `Nr4a3 = 0` provided
additional evidence that single developmental/homeodomain or dopamine-adjacent
TF perturbations rarely elicited a broad acute RNA state in this basal
postmitotic assay. `Ctnnb1` was a useful boundary rather than a positive analog:
it had 383 DEGs, showing that the focal cell group can detect a Wnt/core
beta-catenin response, but `Lmx1a` is not itself the beta-catenin effector and
the assayed upstream or transcriptional-neighbor perturbations did not
phenocopy `Ctnnb1`.

I therefore predict no FDR-significant focal response. A tiny response of one
or a few genes would not be biologically surprising given stochastic sparse
single-cell counts, but the requested output is an integer point prediction.
The most appropriate calibration, led by `Lmx1b = 0` plus flat En/Otx/Foxa/Pitx
comparators, is exactly 0 rather than a low positive number.

## Limits

The main limitation is extrapolation: `Lmx1a` itself was held out, `Lmx1b` is
close but not identical, and LMX1A biology is strongly context-dependent. The
experiment perturbed juvenile postmitotic neurons with mosaic CRISPR and read
out nuclear RNA after 3-4 weeks; it did not measure embryonic roof-plate
patterning, double `Lmx1a`/`Lmx1b` loss, long-term dopaminergic survival,
mitochondrial activity, dopamine release, or SN/VTA subtype abundance. The
negative training signatures also cannot prove editing was absent or present at
the DNA level. The prediction is therefore high-confidence for the assay
endpoint in this focal thalamic group, but not a claim that `Lmx1a` is
biologically dispensable in its canonical developmental or midbrain
dopaminergic contexts.
