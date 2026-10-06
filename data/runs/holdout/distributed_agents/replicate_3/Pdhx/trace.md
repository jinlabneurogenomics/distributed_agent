# Pdhx DEG-count prediction

## Question and resolved ambiguities

The requested held-out target list contains one perturbation:

| target_name |
|---|
| Pdhx |

I interpreted `n_degs` exactly as the focal-cell endpoint in
`151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`: the number of measured
transcripts, including the target transcript itself if it passes the test, with
Benjamini-Hochberg-adjusted Wilcoxon `pvals_adj < 0.05` in `151 TH Prkcd Grin2c
Glut`. `Pdhx` is absent from both the training-count CSV and the DE parquet, so
there is no hidden Pdhx signature to read; the count has to be inferred from
other perturbations in the same experiment plus known PDH-complex biology.

## Sources used

Internal same-experiment sources:

- `training_de_all_cell_groups.parquet`, queried for focal-cell signatures of
  biochemically related measured perturbations.
- `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`, used as the authoritative
  focal endpoint for non-held-out training targets.
- Distributed Agents Corpus MCP, release
  `perturbai-july-260713-sourceguard-1773-v1`, used for the curated
  same-experiment Findings and Claims around measured pyruvate-dehydrogenase
  complex, mitochondrial pyruvate-entry, DLD-linked, and TCA perturbations.

External knowledge:

- MitoCarta3.0 for the mitochondrial localization of Pdhx/PDHX (Rath et al.,
  2021, Nucleic Acids Research, DOI `10.1093/nar/gkaa1011`).
- Biochemical work showing that protein X / E3BP is part of the mammalian PDC
  core and mediates high-affinity E3/DLD binding: Gopalakrishnan et al. 1989,
  DOI `10.1016/0006-291x(89)92492-3`; Sanderson et al. 1996, DOI
  `10.1111/j.1432-1033.1996.00068.x`.
- Human PDHX loss-of-function disease reports establishing that E3BP mutations
  can cause pyruvate dehydrogenase complex deficiency but often with residual
  activity in fibroblasts: Brown et al. 2002, PMID `11935326`;
  Brown et al. 2006, PMID `16904023`; Tajir et al. 2012, DOI
  `10.1016/j.ejmg.2012.06.006`; Pavlu-Pereira et al. 2020, DOI
  `10.1186/s13023-020-01586-3`.

## Computation over the DE data

I read the requested-target manifest, verified that it only contained `Pdhx`,
and summarized the focal training count distribution. In the 1,674 training
targets, `1,205` had `n_degs = 0`, the median was `0`, the 75th percentile was
`1`, and only `6.3%` of targets reached 10 or more DEGs. Therefore a prediction
near zero is not a generic "no biology" call in this cell group; it is the
dominant measured scale for many real perturbations.

For mechanistic calibration I filtered the parquet to
`group_name == "151 TH Prkcd Grin2c Glut"` and to measured targets in the
PDH/pyruvate-entry/DLD/TCA neighborhood, counted `pvals_adj < 0.05` and
`pvals_adj < 0.10`, inspected the lowest adjusted p-values, and computed
whole-vector correlations of Wilcoxon `scores` among those weak focal
signatures. The row-level filter was:

```python
dset = ds.dataset(training_de_all_cell_groups, format="parquet")
focal = dset.to_table(
    columns=["names", "scores", "logfoldchanges", "pvals", "pvals_adj",
             "group_name", "gene_target", "n_pert_matched", "n_ctrl_matched"],
    filter=(ds.field("group_name") == "151 TH Prkcd Grin2c Glut")
           & ds.field("gene_target").isin(targets),
)
```

## Pdhx-specific comparison

Pdhx encodes PDHX, the E3-binding protein of the PDC. It is a direct structural
neighbor of DLAT/E2 and DLD/E3 rather than a paralog of either one; E3BP binds
the E2 core and recruits the DLD E3 homodimer. This made `Pdha1`, `Dlat`, and
`Dld` the closest measured analogs, with `Mpc1` and TCA / 2-oxoacid
dehydrogenase targets serving as pathway-neighborhood counterexamples.

The observed focal counts and expression details were:

| measured target | focal `n_degs` | expression-pattern evidence in `151 TH Prkcd Grin2c Glut` |
|---|---:|---|
| `Pdha1` | 1 | the sole FDR<0.05 hit was the self transcript, `Pdha1`, log2FC `-1.04`, adjusted p `1.31e-6`; the next genes had adjusted p `1.0` |
| `Dlat` | 1 | the sole FDR<0.05 hit was the self transcript, `Dlat`, log2FC `-0.673`, adjusted p `2.81e-7`; the best downstream candidate was `Jarid2`, adjusted p `0.0577` |
| `Dld` | 0 | no transcript passed FDR; even the self transcript had adjusted p `1.0` |
| `Mpc1` | 0 | no transcript passed FDR; same immediate pyruvate-entry axis, but no PDC-like focal program |
| `Dlst` | 0 | alpha-ketoglutarate dehydrogenase E2; no focal DEG |
| `Ogdh` | 0 | alpha-ketoglutarate dehydrogenase E1; no focal DEG |
| `Bckdhb` / `Bckdk` | 0 / 0 | BCKDH-axis comparators linked through DLD also remained downstream-null |
| `Aco2` / `Ndufs4` / `Suclg1` | 0 / 0 / 0 | adjacent mitochondrial metabolism comparators were also null in the focal group |

Two exact PDC targets (`Pdha1`, `Dlat`) therefore landed at one DEG, but both
counts were explained by on-target RNA loss rather than by an induced
mitochondrial-stress or pyruvate-flux response. `Dld` and `Mpc1`, which would be
expected to touch the same carbon-entry state from the E3 side or from pyruvate
import, were strict zeros. The focal score correlations did not reveal a hidden
module: Pearson correlations were only `0.026` for `Pdha1` versus `Dlat`,
`0.014` for `Pdha1` versus `Dld`, `0.029` for `Dlat` versus `Dld`, and `0.005`
for `Dlat` versus `Mpc1`; cosine similarities of the signed-score vectors were
similarly near zero (`0.033`, `0.021`, `0.035`, and `0.003`, respectively).

The Distributed Agents Corpus supported that interpretation. `Pdha1:F004` reported that
measured PDC comparators `Dlat`, `Dld`, and `Mpc1` were flat or nearly flat and
that related TCA targets also failed to form a coherent neuronal PDH module.
`Dlat:F004` specifically treated the `Dlat`/`Jarid2` signal as a Dlat-specific
result in `151 TH Prkcd Grin2c Glut` because `Pdha1`, `Dld`, `Dlst`, `Ogdh`,
`Mpc1`, `Bckdhb`, `Aco2`, `Idh3a`, `Mdh2`, and `Ndufs4` did not move `Jarid2`.
`Dld:F003` and `Mpc1:F002` anchored the broader claim that acute postmitotic
neuronal perturbation of represented mitochondrial carbon-entry, PDC,
DLD-linked, and TCA genes was usually absent, singleton-only, or
non-phenocopying. The shared corpus claim
`claim:5e92ede610df7967282e` summarizes this as a failure of these perturbations
to induce a coherent nuclear DE module in this assay, with isolated target-
specific singleton exceptions.

## Prediction

The closest biological donors point to no broad downstream response for a Pdhx
knockout in recovered thalamic glutamatergic nuclei. PDHX loss should impair PDC
assembly by weakening E3 recruitment, but it is an E3-binding/scaffold component
rather than the E1 or E2 catalytic site; human E3BP-deficient cells can retain
measurable residual PDC activity. In this acute sparse AAV-CRISPR setting,
that makes it at least as likely as `Dld`/`Mpc1` to be transcriptionally
buffered. I also did not promote it to a one-DEG call on self-transcript grounds:
the two one-count exact PDC donors only crossed through their own mRNAs, while
several same-neighborhood targets with clear negative self log fold changes
(`Dld`, `Dlst`, `Mpc1`, `Bckdhb`, `Ndufs4`, `Ogdh`) still did not survive BH
correction.

I therefore predict that no measured gene, including `Pdhx` itself, will pass
FDR 0.05:

| target_name | predicted_n_degs |
|---|---:|
| Pdhx | 0 |

## Limits

This is an extrapolation from PDH-neighborhood training perturbations, not a
direct Pdhx observation. The best analogs are imperfect: `Pdha1` and `Dlat` are
catalytic PDC subunits, `Dld` is shared by several 2-oxoacid dehydrogenase
complexes, and `Mpc1` acts upstream of PDC. The count of one observed for
`Pdha1` and `Dlat` also shows that a self-transcript-only outcome is plausible,
so the difference between `0` and `1` is driven by unpredictable on-target RNA
detectability as much as by downstream biology. Finally, the assay observes
surviving postnatal neuronal nuclei after sparse CRISPR; it is not measuring
metabolite flux, enzyme assembly, seizure physiology, developmental
vulnerability, or pre-assay depletion.
