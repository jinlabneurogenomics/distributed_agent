# Question

The held-out manifest contains one target, `Pax1`. I interpreted the task as a
point prediction of the number of genes that would pass Benjamini-Hochberg FDR
0.05 after acute AAV-CRISPR loss of `Pax1` in `151 TH Prkcd Grin2c Glut`
neurons, where `Pax1` itself and its expression signature were fully absent from
the supplied training parquet and focal-cell DEG-count CSV.

I therefore treated the training counts as the calibration endpoint and the
training parquet as the within-assay expression-signature evidence. I used
external biology only to decide which measured perturbations are relevant to
`Pax1`, not to replace the focal-cell counts.

# Sources Used

- `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`: observed `n_degs` for
  1,674 non-held-out perturbations in the focal cell group.
- `training_de_all_cell_groups.parquet`: signed Wilcoxon statistics for the
  same non-held-out perturbations. I queried the focal `151 TH Prkcd Grin2c Glut`
  rows and compared Wilcoxon `scores` across genes.
- Distributed Agents same-experiment corpus, release
  `perturbai-july-260713-sourceguard-1773-v1`: target contexts for `Pax2`,
  `Pax6`, `Tbx1`, and `Foxn1`. The corpus had no direct `Pax1` or `Pax9` node.
- PubMed literature for `Pax1`/`Pax9` sclerotome, vertebral-column, and
  pharyngeal-pouch biology:
  - Peters et al. 1999, PMID 10556064, DOI 10.1242/dev.126.23.5399.
  - Rodrigo et al. 2003, PMID 12490554, DOI 10.1242/dev.00240.
  - Wallin et al. 1996, PMID 8565834, DOI 10.1242/dev.122.1.23.
  - Su et al. 2001, PMID 11476574, DOI 10.1006/dbio.2001.0342.
  - Zou et al. 2006, PMID 16530750, DOI 10.1016/j.ydbio.2005.12.015.

# Computational Checks

The focal training endpoint is zero-inflated: 1,205 of 1,674 perturbations have
`n_degs = 0` and 469 are nonzero. Among genes most relevant to the known Pax1
program, every represented perturbation had zero focal-cell DEGs:

| training perturbation | focal n_degs | reason for comparison |
| --- | ---: | --- |
| `Pax2`, `Pax3`, `Pax4`, `Pax6`, `Pax7`, `Pax8` | 0 each | Measured PAX-family developmental transcription factors. `Pax9`, the closest Pax1 paralog, was not present in the training CSV or parquet. |
| `Tbx1` | 0 | Pharyngeal-endoderm/DiGeorge-axis comparator in the same embryonic compartment as Pax1. |
| `Hoxa3` | 0 | Thymus/parathyroid third-pouch regulator genetically interacting with Pax1. |
| `Foxn1` | 0 | Thymic epithelial downstream lineage regulator and epithelial counterexample. |
| `Sox9` | 0 | Chondrogenic/sclerotome effector context downstream of Pax1/Pax9 biology. |
| `Gli1`, `Gli2` | 0 each | Hedgehog-responsive sclerotome pathway comparators. |
| `Hoxa1`, `Pbx1`, `Pbx3`, `Meis1`, `Meis2` | 0 each | Hox/TALE axial and pharyngeal developmental comparators. |
| `Foxa2`, `Trp63` | 0 each | Additional epithelial/developmental boundary controls measured in the focal cell group. |

I then compared expression profiles for this 19-gene analog set using the
focal-cell Wilcoxon `scores`, with `pvals_adj < 0.05` as the activity threshold.
All 19 profiles were present, each had 17,259 measured genes, and all had
`significant_feature_count = 0`. Direct parquet aggregation gave the same
result; for the most important anchors:

```sql
SELECT gene_target, count(*) AS genes_tested,
       sum(pvals_adj < 0.05) AS n_fdr05,
       min(pvals_adj) AS min_padj,
       max(abs(scores)) AS max_abs_score
FROM training_de_all_cell_groups
WHERE group_name = '151 TH Prkcd Grin2c Glut'
  AND gene_target IN (...)
GROUP BY gene_target;
```

`Pax3`, `Pax4`, `Pax6`, `Pax7`, `Pax8`, `Tbx1`, `Hoxa3`, `Gli1`, `Gli2`,
`Hoxa1`, `Pbx1`, `Pbx3`, `Meis2`, `Sox9`, `Foxa2`, and `Trp63` all had minimum
adjusted p value 1.0; `Pax2` had 0.937, `Foxn1` had 0.811, and `Meis1` had
0.570. Thus even their most extreme signed ranks in the focal cell group were
far from FDR 0.05.

The score-vector correlations among biologically chosen analogs were also
noise-scale. Examples from the profile comparison:

- `Pax2` versus the other PAX genes: cosine 0.029 to `Pax3`, 0.040 to `Pax4`,
  0.050 to `Pax7`, and 0.038 to `Pax8`; all compared profiles had zero
  significant positive and zero significant negative genes.
- `Pax6` versus `Pax2` and `Pax8`: cosine 0.034 and 0.015; again no significant
  genes on either side.
- `Pax2` versus pharyngeal or sclerotome analogs was similarly flat: cosine
  0.004 to `Hoxa3`, 0.010 to `Gli1`, -0.004 to `Gli2`, 0.043 to `Tbx1`, and
  0.046 to `Sox9` in the focal cell group.
- In an unbiased scan against all 1,674 focal-cell training perturbations, the
  best whole-profile Pearson neighbor for `Pax2` was only 0.111 and the best for
  `Pax6` was only 0.058. Those nearest neighbors were not Pax1-like developmental
  regulators, so I did not treat them as positive mechanistic evidence.

# Same-experiment Corpus Evidence

The Distributed Agents corpus had no direct `Pax1` or `Pax9` finding, which is expected
because both are outside this local target context. Its measured-neighbor
reports nevertheless supported a null prediction:

- `Pax2`: the corpus summarizes a near-global no-effect profile after P16
  mosaic Pax2 loss; only one of 388,023 downstream tests reached even FDR 0.10
  across all 23 recovered cell groups, and Pax8, Pax6, En1, En2, Otx2, Gata3,
  and Lbx1 did not phenocopy Pax2.
- `Pax6`: the corpus reports that acute Pax6 loss after P16 was silent across
  22 recovered NeuN-positive groups and that Pax2, Pax3, Pax4, Pax7, and Pax8
  gave only sparse or null singleton effects rather than a shared PAX program.
- `Tbx1`: the corpus reports absence of the embryonic Tbx1-FGF/ERK program and
  no robust genome-wide convergence partner in postmitotic neurons.
- `Foxn1`: the corpus reports no FDR-supported downstream response in any
  recovered neuronal class and no activation of the canonical thymic-epithelial
  or hair-keratinocyte Foxn1 programs.

# Pax1 Biology and Target-specific Reasoning

`Pax1` is a paired-box transcription factor best known for embryonic
sclerotome, vertebral-body/intervertebral-disc, and pharyngeal-pouch epithelial
programs, not for maintenance of juvenile postmitotic glutamatergic neurons.
Defined mouse Pax1 null alleles perturb vertebral column, sternum, and scapula
development (Wilm et al. 1998), and the closest paralog `Pax9` synergizes with
`Pax1` in medial sclerotome derivatives: Pax1/Pax9 double-mutant embryos lack
vertebral bodies, intervertebral discs, and proximal ribs (Peters et al. 1999).
`Pax1` and `Pax9` directly activate `Bapx1`/`Nkx3-2` and promote chondrogenic
differentiation in the sclerotome (Rodrigo et al. 2003).

`Pax1` also acts in pharyngeal derivatives. Pax1 protein is expressed in thymic
epithelium, and undulated Pax1 mutants have thymic hypoplasia and abnormal
T-cell maturation (Wallin et al. 1996). In the third pharyngeal pouch, `Hoxa3`
and `Pax1` regulate epithelial proliferation, survival, and thymus/parathyroid
organogenesis, with `Gcm2` reduced in Pax1-deficient tissue (Su et al. 2001).
Eya/Six factors help set up the same pouch, but Zou et al. 2006 showed that
Eya1/Six1 expression there does not require Pax1/Pax9 function, placing Pax1 in
a specific embryonic endodermal circuit rather than a general neuronal state.

The best possible same-assay paralog, `Pax9`, was not measured as a training
perturbation. I therefore anchored on three imperfect but informative groups:
measured PAX paralogs, measured third-pouch/pharyngeal comparators
(`Hoxa3`, `Foxn1`, `Tbx1`), and measured sclerotome/chondrogenic/Hedgehog-side
comparators (`Sox9`, `Gli1`, `Gli2`, plus Hox/TALE factors). All were zero in
the actual focal-cell endpoint, and none had a focal-cell expression signature
with FDR-level genes or a coherent signed-score module. That combination argues
that this cell type and P16-to-P37/44 window are outside the active Pax1/Pax9
developmental context.

The zero/nonzero call is therefore `zero`. A small nonzero would require either
a postnatal TH/Prkcd/Grin2c glutamatergic Pax1 role absent from the sclerotome
and pharyngeal literature, or a generic PAX-family neuronal response absent
from `Pax2`, `Pax3`, `Pax4`, `Pax6`, `Pax7`, and `Pax8` in the same endpoint.
I found neither. I predict:

| held-out target | predicted n_degs |
| --- | ---: |
| `Pax1` | 0 |

# Limits

- `Pax9`, the closest Pax1 paralog, was not represented in the supplied training
  perturbations, so the strongest paralog comparison is external rather than a
  direct within-parquet signature.
- The analog genes are developmental relatives, not interchangeable members of
  one mature-neuron complex; their shared zero count is evidence for assay
  context mismatch, not proof that all use the same mechanism.
- Acute sparse AAV-CRISPR in juvenile NeuN-positive brain does not test
  embryonic sclerotome, thymic epithelium, parathyroid, or non-neuronal brain
  compartments. A zero focal-cell DEG count should not be read as Pax1 being
  biologically unimportant.
- The endpoint is an FDR-count at the available power. Very weak changes could
  exist below the Wilcoxon/BH threshold, and the point prediction does not carry
  an uncertainty interval.
