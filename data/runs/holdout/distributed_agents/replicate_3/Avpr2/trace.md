# Prediction trace

## Question and endpoint

The requested held-out perturbation set contains one mouse target, `Avpr2`, from
`022_Avpr2.csv`.  I interpreted the requested endpoint as:

- focal cell group: `151 TH Prkcd Grin2c Glut`;
- response breadth: the count of measured genes with `pvals_adj < 0.05` in the
  Wilcoxon DE table for a target-gene knockout;
- perturbation target counts include any significant row, including the
  perturbed target's own transcript if it was detected as a DEG;
- prediction required: a single integer point estimate, preserving manifest
  order.

I also explicitly checked that `Avpr2` is not present as a held-in
`gene_target` in the parquet and is not present in the focal training count CSV;
there are zero `Avpr2` target rows in the parquet.  `Avpr2` does appear as a
measured expression feature for all 1,674 held-in focal perturbations, so its
absence is only as a perturbation target.

## Sources used

- `[local file: training_de_all_cell_groups.parquet]`,
  filtered to `group_name == "151 TH Prkcd Grin2c Glut"` for the held-in
  differential-expression signatures.
- `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`
  for observed focal-cell `n_degs` among the 1,674 non-held-out perturbations.
- Distributed Agents corpus release
  `perturbai-july-260713-sourceguard-1773-v1`, especially the Avpr1a,
  Avpr1b, and Oxtr reports and the shared nonapeptide-receptor claim
  `claim:8a7e4d2d7d5edb7595ca`.
- Distributed Agents runtime score-profile comparisons over the focal-cell parquet
  rows, written to `avpr_pathway_score_compare.json` and inspected through
  `avpr_pathway_score_inspect.json`.
- PubMed-indexed literature for AVPR2/V2R biology:
  Salhadar et al. 2020, DOI `10.1124/mol.120.119602`;
  Bockenhauer and Bichet 2015, DOI `10.1038/nrneph.2015.89`;
  Kato et al. 1995, DOI `10.1046/j.1432-0436.1995.5930163.x`;
  Schliebe et al. 2008, DOI `10.1152/ajprenal.00465.2007`.

## Computational calibration

The focal training file contains 1,674 perturbations.  Its count distribution is
very zero-inflated but not globally unresponsive: median `n_degs` is 0, mean is
14.05, the maximum is 2,677, 469 targets have at least one DEG, 106 have at
least 10 DEGs, and 59 have at least 50 DEGs.  A zero prediction is therefore
common in this assay, but it still needs target-specific support.

I filtered the parquet with PyArrow to the focal group and to mechanistically
related held-in perturbations, then sorted each perturbation by adjusted
p-value to verify whether the count endpoint hid near-threshold genes.  I also
compared Wilcoxon `scores`, rather than raw log-fold-changes, for a candidate
set of nonapeptide receptors and V2R/cAMP-pathway controls:

```python
filter = (field("group_name") == "151 TH Prkcd Grin2c Glut") &
         field("gene_target").isin(candidate_targets)
```

The score comparison used 17,259 focal measured genes per target and an FDR
threshold of 0.05.  LogFC was avoided for the final signature comparison
because very low-abundance genes often have extreme finite logFC values but
`pvals_adj == 1`; the Wilcoxon score vector better matches the DE statistic.

## Target-specific reasoning

### `Avpr2`

`Avpr2` encodes vasopressin V2 receptor, a Gs-coupled GPCR best known in renal
collecting duct principal cells.  AVP binding to V2R activates Gs, adenylyl
cyclase, cAMP, and PKA and regulates AQP2 trafficking and renal water
reabsorption; AVPR2 loss-of-function is a major cause of X-linked nephrogenic
diabetes insipidus rather than a canonical neuronal cell-autonomous
transcription-factor syndrome (Bockenhauer and Bichet 2015; Salhadar et al.
2020).  CNS V2R mRNA has been reported in developing rat brain, but Kato et al.
found cerebrum signal in newborn rather than adult rat and stable cerebellar
signal, which makes a robust V2R program in a P37-P44 thalamic glutamatergic
mouse group an extrapolation rather than the default expectation.  Germline
Avpr2-deficient mice also show secondary kidney and hypothalamic expression
changes in the setting of systemic water-balance disease (Schliebe et al.
2008), a very different perturbation from sparse postmitotic neuronal AAV
CRISPR loss.

The most direct same-family perturbations in the training set were
transcriptionally flat in the focal cell group:

- `Avpr1a`: `n_degs = 0`; 234 matched perturbed nuclei.  The lowest focal
  adjusted p-value was for `Polr3a`, `pvals_adj = 0.841`, so there was not even
  a near-threshold focal DEG.
- `Avpr1b`: `n_degs = 0`; 199 matched perturbed nuclei.  Its top focal row was
  `Mettl4`, `pvals_adj = 0.569`.
- `Oxtr`: `n_degs = 0`; 192 matched perturbed nuclei.  All focal rows had
  `pvals_adj = 1.0`.

These are not perfect biochemical substitutes for V2R, because V1a/V1b/OXTR are
predominantly Gq/PLC receptors whereas V2R is Gs/cAMP-coupled.  They are still
the closest assayed nonapeptide receptors, and the Distributed Agents corpus reports
that Avpr1a, Avpr1b, and Oxtr did not converge on a shared vasopressin/oxytocin
receptor or Gq/PLC/PKC module across the basal juvenile neuronal screen.  The
corpus also records that Avpr1b had no robust downstream transcriptome in any
measured neuronal group and that Oxtr produced only three isolated FDR<0.10
genes across all groups, none representing a broad receptor-family state.

Because V2R is Gs-coupled, I treated held-in cAMP components and other
Gs-coupled receptors as stronger pathway counterexamples than V1a/V1b/OXTR
alone:

- `Gnas`, the Gs alpha subunit: `n_degs = 0`.
- `Adcy1`, `Adcy3`, `Adcy5`: each `n_degs = 0`.
- cAMP phosphodiesterases `Pde4b` and `Pde4d`: each `n_degs = 0`.
- PKA genes `Prkaca` and `Prkar1a`: each `n_degs = 1`, and the only
  significant focal row was the target transcript itself
  (`Prkaca` adjusted p `7.91e-22`; `Prkar1a` adjusted p `0.00138`).
- `Creb1`: `n_degs = 10`.  This is a useful boundary: perturbing a downstream
  cAMP-responsive transcription factor can be seen by the assay, but the
  proximal Gs/ADCY/PDE/PKA nodes did not transmit a broad steady-state program.
- other represented Gs-linked GPCRs were also flat in the same focal group:
  `Adrb2 = 0`, `Adrb3 = 0`, `Drd5 = 0`, `Htr7 = 0`, and `Crhr1 = 0`.

The Wilcoxon-score signature comparison reinforced the count-level readout.
Within a 12-target cohort of `Avpr1a`, `Avpr1b`, `Oxtr`, `Gnas`, the adenylyl
cyclases, the PDE4 genes, PKA genes, and `Creb1`, nine targets had no
significant focal features.  `Avpr1a`, `Avpr1b`, `Oxtr`, and `Gnas` each had
zero significant features in the score-profile artifact; all receptor-to-cAMP
pairs had zero shared FDR-significant genes.  Their whole-score similarities
were essentially noise-scale: for example, `Avpr1a` versus `Gnas` was the
largest selected receptor/pathway Pearson correlation for `Avpr1a` at only
0.052, `Avpr1b` versus `Gnas` was 0.023, and `Oxtr` versus `Pde4b` was 0.032.
The full eligible-universe neighbor scan likewise failed to find a hidden
strong state: the top whole-profile Pearson neighbors were `Rora` for `Avpr1a`
at 0.153, `Kremen1` for `Avpr1b` at 0.071, and `Lhx3` for `Oxtr` at 0.063.
The nominated neighbors were unrelated and weak, not a recovered V2R-like or
nonapeptide module.

I therefore predicted no FDR-significant genes for `Avpr2` in
`151 TH Prkcd Grin2c Glut`.  The zero is driven primarily by within-dataset
evidence from the flat V1a/V1b/OXTR controls and the flat Gs/cAMP controls in
the focal group.  External AVPR2 biology only adjusts the prior further toward
zero, because V2R's large established effector axis is renal AQP2/water
handling and because a sparse, unstimulated, postnatal neuronal knockout is not
expected to reproduce the kidney or systemic NDI transcriptional contexts.

## Limits and extrapolations

- `Avpr2` itself was completely held out as a perturbation, so there is no
  direct same-assay Avpr2 signature to inspect.
- Raw Avpr2 expression in the control nuclei was not part of the supplied DE
  table.  The Avpr2 feature was measurable and always nonsignificant across
  held-in focal perturbations, but this is only weak support; low or unchanged
  target RNA is not a failed-editing call.
- The nearest family members in the dataset are V1a/V1b/OXTR, not V2R, and they
  couple mainly through Gq/PLC rather than Gs/cAMP.  I therefore weighted the
  Gs, adenylyl cyclase, PDE4, PKA, and CREB controls heavily.
- Acute AVP stimulation, vasopressin-release physiology, kidney collecting
  duct cells, choroid plexus, hindbrain, and behavior were not assayed.  The
  prediction is specifically for the basal P37-P44 NeuN+ thalamic glutamatergic
  snRNA endpoint after mosaic CRISPR loss.
- A one- or two-gene idiosyncratic sentinel response, analogous to the sparse
  Oxtr events outside this focal group, cannot be excluded.  In the focal group
  and with the assayed cAMP controls, the best point prediction is still the
  FDR floor of zero.

