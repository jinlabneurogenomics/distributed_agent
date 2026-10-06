# Pdhb DEG-count prediction trace

## Question and resolved ambiguities

The requested held-out target list contains one perturbation:

```tsv
target_name
Pdhb
```

The task is to predict `n_degs`: the number of measured genes with
Benjamini-Hochberg adjusted Wilcoxon `pvals_adj < 0.05` in the focal
`151 TH Prkcd Grin2c Glut` population after an acute sparse AAV-CRISPR
loss-of-function perturbation.

I treated the perturbed target transcript itself as eligible to count as a
DEG, because the training endpoint does: in this focal group `Pdha1`,
`Dlat`, `Idh3a`, `Mdh2`, `Got2`, `Sucla2`, `Sdha`, `Ndufb9`, and many other
low-response mitochondrial genes have `n_degs = 1` where the sole
FDR<0.05 feature is the perturbed mRNA. I verified that `Pdhb` is held out:
it has no row in the focal training-count CSV and no `gene_target` rows in
the supplied DE parquet.

## Sources used

- Input DEG parquet:
  `[local file: training_de_all_cell_groups.parquet]`
- Input focal endpoint table:
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`
- Held-out manifest:
  `[local file: 171_Pdhb.csv]`
- Distributed Agents same-experiment corpus
  `perturbai-july-260713-sourceguard-1773-v1`, especially claim
  `claim:5e92ede610df7967282e` and the source findings for `Pdha1:F004`,
  `Mpc1:F002`, `Dld:F003`, `Aco2:F003`, and `Ogdh:F004`.
- Distributed Agents run-local observed-profile tools, used on a 22-node focal
  PDC/TCA/mitochondrial-carbon panel written to
  `focal_pdc_tca_profiles.tsv`.
- Reactome, "PDH complex synthesizes acetyl-CoA from PYR",
  stable identifier `R-HSA-9861559`, reviewed 2024.
- Ganetzky, McCormick, and Falk 2021, GeneReviews,
  "Primary Pyruvate Dehydrogenase Complex Deficiency Overview",
  NCBI Bookshelf `NBK571223`.
- Okajima et al. 2008, "Mutations of the E1beta subunit gene (PDHB) in four
  families with pyruvate dehydrogenase deficiency",
  `Molecular Genetics and Metabolism`, doi: `10.1016/j.ymgme.2007.10.135`,
  PMID `18164639`.

Reactome places PDHB in the same mitochondrial pyruvate dehydrogenase
complex as PDHA1/E1 alpha, DLAT/E2, DLD/E3, and PDHX/E3-binding protein.
Ganetzky et al. and Okajima et al. support the external prior that damaging
PDHB alleles can cause primary pyruvate dehydrogenase complex deficiency,
but those sources are germline/human disease biology rather than direct
evidence for a broad postmitotic nuclear RNA response in this assay.

## Computational steps over the input data

1. Read the held-out manifest and focal training-count CSV. The focal
   training table has 1,674 non-held-out perturbations. Its `n_degs`
   distribution is highly zero-inflated: 1,205/1,674 are 0, 276/1,674 are
   1, and 88.5% are <=1.
2. Checked absence of `Pdhb` from the training endpoint and scanned the
   parquet for `gene_target == "Pdhb"`; the count was 0 rows.
3. Filtered the parquet with `pyarrow.dataset` to the focal cell group and
   to literature-obvious PDH, pyruvate-entry, TCA, malate/aspartate, BCKDH,
   and OXPHOS-adjacent comparators. For each comparator I counted genes
   with focal `pvals_adj < 0.05`, `<0.10`, and `<0.20`, and sorted the
   profile by adjusted p value to identify whether the few calls were
   target self effects or downstream features.
4. Compared the selected 22 focal log-fold-change profiles with the
   Distributed Agents `profile_compare` and `profile_inspect` runtime tools. The
   response-activity classes in this selected panel were nine nodes with no
   significant features, twelve with 1-9 significant features, and one
   with 10-49 significant features. For the four direct Pdhb-side observed
   nodes, `Pdha1` and `Dlat` each had exactly one significant negative
   feature, while `Dld` and `Mpc1` had none; their significant-feature
   intersections with PDC/TCA peers were 0, consistent with singleton
   target-transcript effects rather than a shared pathway module.

## In-dataset analogs and counterexamples

The most relevant training perturbations are the represented members of the
mitochondrial pyruvate dehydrogenase neighborhood:

| training target | role relative to Pdhb | observed focal n_degs | focal profile evidence |
|---|---:|---:|---|
| `Pdha1` | PDH E1 alpha, obligate partner of PDHB in E1 | 1 | The only FDR<0.05 call was `Pdha1` itself, logFC -1.039, adj. p 1e-6. |
| `Dlat` | PDH E2 core | 1 | The only FDR<0.05 call was `Dlat` itself, logFC -0.673, adj. p 2.8e-7; `Jarid2` was the next feature but stayed just outside the endpoint cutoff at adj. p 0.0577. |
| `Dld` | E3 subunit shared by PDC, OGDH, BCKDH, and other alpha-ketoacid dehydrogenases | 0 | No focal feature passed FDR<0.20. |
| `Mpc1` | mitochondrial pyruvate carrier directly upstream of PDC | 0 | No focal feature passed FDR<0.20. |

The next shell of mitochondrial-carbon perturbations showed the same
pattern in `151 TH Prkcd Grin2c Glut`: `Aco2`, `Ogdh`, `Dlst`, `Suclg1`,
`Bckdhb`, and `Bckdk` were 0; `Idh3a`, `Sucla2`, `Mdh2`, `Got2`, `Sdha`,
`Slc25a4`, `Slc25a46`, and `Ndufb9` were singleton perturbations. In most
singleton cases the only FDR<0.05 call was again the target transcript.
`Mdh1` is the important local counterexample with 29 focal DEGs, but it is
a cytosolic malate dehydrogenase/malate-aspartate perturbation with a
thalamic amino-acid/synaptic offshoot, not a PDC subunit or a direct
pyruvate-to-acetyl-CoA reaction component. I therefore used it as a guard
against assuming all carbon metabolism is silent, not as a positive count
anchor for `Pdhb`.

The Distributed Agents corpus independently captured this pattern. Claim
`claim:5e92ede610df7967282e` states that represented mitochondrial
carbon-entry, PDC, TCA, and Fe-S perturbations generally failed to induce a
coherent postmitotic neuronal nuclear DE module, with isolated singleton
and target-specific exceptions. The underlying `Pdha1:F004` finding
specifically noted that measured PDC comparators `Dlat`, `Dld`, and `Mpc1`
were flat or nearly flat and that unrepresented canonical PDH regulators
and subunits included `Pdhb`, `Pdhx`, `Pdk1-4`, and `Pdp1-2`.

## Target-specific prediction

### Pdhb

`Pdhb` encodes PDH E1 beta. The biologically closest observed target is
`Pdha1`, because PDHA1 and PDHB form the E1 alpha2-beta2 decarboxylase
component of the pyruvate dehydrogenase complex. `Pdha1` loss in the focal
group produced a singleton self-transcript response, not a downstream
mitochondrial-stress module. The two represented downstream PDC components
bound the likely response even more tightly: `Dlat` was self-only at
FDR<0.05 and `Dld` was entirely flat. `Mpc1`, which limits entry of
pyruvate into the same mitochondrial pathway, was also entirely flat.

Given that calibration, I predicted no broad downstream DE program for
`Pdhb`. I did keep a nonzero count because the two directly measured PDC
subunits with detectable focal self knockdown, `Pdha1` and `Dlat`, both
landed at exactly one DEG, and that is the most plausible outcome for an
expressed E1 beta transcript if the sgRNAs reduce `Pdhb` mRNA enough to
clear the Wilcoxon/BH threshold. This prediction is driven primarily by
within-dataset analogs; external gene-function knowledge was used to decide
that `Pdha1`, `Dlat`, `Dld`, and `Mpc1`, rather than generic OXPHOS stress
genes such as `Opa1`, are the relevant comparators.

Predicted `n_degs`: **1**.

## Limits

- No `Pdhb` perturbation profile or endpoint count is present in the inputs;
  the prediction extrapolates from same-complex and same-pathway genes.
- The endpoint is assay and power dependent. `Dld` and `Mpc1` show that a
  mitochondrial target can have no significant self transcript in this
  CRISPR/snRNA-seq design, so the `Pdhb = 1` call could fail downward to 0
  if the guides do not reduce nuclear `Pdhb` RNA detectably in this cell
  group.
- The assay does not measure PDH flux, acetyl-CoA, ATP production, lipoate
  chemistry, or protein abundance. A near-null RNA surface should not be
  read as evidence that Pdhb biology is unimportant.
- The main positive carbon-metabolism counterexample in the focal group,
  `Mdh1`, shows that this cell group can mount metabolic transcriptional
  responses, but its cytosolic malate/aspartate signature is an imperfect
  analog for mitochondrial E1 beta loss.
