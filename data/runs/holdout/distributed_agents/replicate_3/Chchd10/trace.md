# Predicting held-out DEG burden for `151 TH Prkcd Grin2c Glut`

## Question and resolved ambiguities

The requested readout is `n_degs`, the count of measured genes with Wilcoxon
`pvals_adj < 0.05` after sparse AAV-CRISPR loss of a held-out target in the
postnatal mouse focal class `151 TH Prkcd Grin2c Glut`.  The manifest for this
run contains one target:

| target_name |
| --- |
| Chchd10 |

I interpreted positive `logfoldchanges` as increased expression in perturbed
nuclei versus matched non-targeting controls, and I counted the target
transcript itself if it passed FDR, matching the supplied
`151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` endpoint.  I did not use
target-transcript knockdown as an editing-efficiency score; in this dataset it
is only one possible DEG.

## Sources used

- Same-experiment raw differential-expression table:
  `[local file: training_de_all_cell_groups.parquet]`.
- Same-experiment focal endpoint for non-held-out perturbations:
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
- Requested target manifest:
  `[local file: 037_Chchd10.csv]`.
- Distributed Agents same-experiment semantic corpus
  `perturbai-july-260713-sourceguard-1773-v1`.  I queried both shared-claim
  and explicit-finding neighborhoods for `Chchd10`; the release returned no
  `Chchd10` Claim or Finding paths, so this run had no curated corpus analog
  to transfer directly.
- Distributed Agents runtime profile tools.  I used `profile_compare`/`profile_inspect`
  over the focal parquet rows to compare signed log-fold-change profiles for
  mitochondrial structural, import, proteostasis, respiratory-chain, and
  mitophagy training perturbations.
- NCBI PubMed literature searches for CHCHD10, CHCHD2, MICOS, OPA1, and
  mitochondrial integrated stress biology.

Key external references:

- Bannwarth et al. 2014, DOI `10.1093/brain/awu138`, PMID `24934289`:
  pathogenic CHCHD10 mutations in ALS/FTD/myopathy and localization of
  CHCHD10 to the mitochondrial intermembrane space/cristae junctions.
- Genin et al. 2016, DOI `10.15252/emmm.201505496`, PMID `26666268`:
  CHCHD10 patient mutations disassemble MICOS and disrupt mitochondrial
  cristae.
- Huang et al. 2018, DOI `10.1093/hmg/ddy270`, PMID `30084972`:
  CHCHD2 and CHCHD10 form stress-responsive mitochondrial heterodimers.
- Burstein et al. 2018, DOI `10.1093/hmg/ddx397`, PMID `29112723`:
  CHCHD10 interacts with CHCHD2 and p32/C1QBP; homozygous Chchd10 knockout
  mice were viable and lacked gross brain, heart, or skeletal-muscle
  bioenergetic/ultrastructural phenotypes, whereas ALS-associated missense
  alleles behaved as toxic gain-of-function alleles.
- Anderson et al. 2019, DOI `10.1007/s00401-019-01989-y`, PMID `30877432`:
  Chchd10-S55L knock-in mice activate a tissue-specific mitochondrial
  integrated stress response, but Chchd10 ablation did not recapitulate that
  disease program.
- Liu et al. 2020, DOI `10.1093/hmg/ddaa077`, PMID `32338760`: Chchd2/Chchd10
  loss activates OMA1 and perturbs OPA1/cristae in a partially redundant
  system.
- Liu et al. 2020, DOI `10.1096/fj.201903133RR`, PMID `32369233`: CHCHD10 can
  regulate OPA1-mitofilin complexes and intersects with TDP-43 mitochondrial
  phenotypes, but this is indirect relative to CRISPR loss of CHCHD10.

## Computational evidence from the focal dataset

I used row-group statistics in the parquet metadata to restrict work to the
`151 TH Prkcd Grin2c Glut` row groups: 35 row groups can contain the focal
cell class rather than all 712 row groups in the 616,253,184-row file.  For
mechanistically chosen comparators, I loaded only:

```python
f = (
    (ds.field("group_name") == "151 TH Prkcd Grin2c Glut")
    & ds.field("gene_target").isin(comparator_targets)
)
table = dataset.to_table(
    columns=[
        "names", "gene_target", "logfoldchanges", "pvals_adj",
        "n_pert_matched", "n_ctrl_matched",
    ],
    filter=f,
)
n_degs = table.to_pandas().groupby("gene_target").pvals_adj.apply(
    lambda x: int((x < 0.05).sum())
)
```

Across all 1,674 training perturbations in the focal CSV, the distribution is
strongly zero-inflated: 1,205 targets have 0 DEGs, 276 have 1 DEG, and only
193 have more than 1 DEG.  This matters because a generic disease association
is not enough to predict a broad focal signature in this sparse CRISPR assay.

The relevant mitochondrial/cristae neighborhood is similarly quiet:

| training target | focal n_degs | expression-pattern evidence in `151 TH Prkcd Grin2c Glut` | use for Chchd10 |
| --- | ---: | --- | --- |
| `Chchd2` | 1 | The only significant row was `Chchd2` itself, logFC `-0.880`, adjusted p `3.18e-28`; 324 matched perturbed nuclei. | Best paralog and best loss-of-function analog.  CHCHD2 and CHCHD10 are homologous intermembrane-space proteins that heterodimerize.  The count argues for a singleton/self-transcript response rather than a broad downstream state. |
| `Opa1` | 37 | Significant genes included `Asns`, `Mars1`, `Chac1`, `Ddit3`, `Mthfd2`, `Slc7a5`, aminoacyl-tRNA synthetases, `mt-Co2`, and `Opa1` itself; 195 matched perturbed nuclei.  This is an ATF4/integrated-stress-like footprint. | Mechanistically connected through cristae remodeling and OMA1/L-OPA1 processing, but downstream of more direct inner-membrane fusion stress.  I used it as an upper bound, not a central estimate. |
| `Micos13` | 0 | No FDR-significant genes among 209 matched perturbed nuclei.  The signed profile correlated positively with `Chchd2` and `Opa1`, but without a significant tail. | MICOS/cristae counterexample: proximity to the cristae-organizing system alone was insufficient for a nonzero focal count. |
| `Micu1` | 0 | No significant genes; 171 matched perturbed nuclei. | Inner-membrane Ca2+ uptake counterexample. |
| `Mff` | 0 | No significant genes; 133 matched perturbed nuclei. | Mitochondrial dynamics counterexample; argues that changing fission/fusion balance did not automatically produce many DEGs. |
| `Tomm40` | 1 | Only `Tomm40` itself was significant, logFC `-0.923`, adjusted p `5.46e-7`; 224 matched nuclei. | Import-machinery singleton analog: mitochondrial targets can register only as a direct transcript hit. |
| `Yme1l1` | 0 | No significant genes; 106 matched nuclei. | OPA1-processing/proteostasis counterexample. |
| `Clpp` / `Clpx` / `Lonp1` | 0 / 0 / 0 | Mitochondrial matrix proteostasis genes were all null in the focal endpoint. | Counterexamples to a broad mitochondrial-stress transfer. |
| respiratory-complex genes including `Ndufs4` | mostly 0 or 1 | Among selected `Atp5*`, `Cox*`, `Nduf*`, and `Uqcr*` genes plus the hand-picked mitochondrial genes above, 29/49 had 0 DEGs, 19/49 had 1 DEG, and only `Opa1` had more than 1. | Respiratory perturbation by itself calibrated near 0-1 DEGs in this cell type. |
| `Nrf1` | 138 | Broader transcriptional footprint enriched for nuclear/mitochondrial biogenesis and RNA-processing effects. | Counterexample: a nuclear transcriptional regulator of mitochondrial genes is upstream and pleiotropic, not an analog of a small CHCH inner-membrane protein. |
| `Tardbp` | 210 | Large RNA-processing/neuron-state footprint with direct `Tardbp` down-regulation. | Disease-relevant but mechanistically inappropriate for this endpoint; the literature link between TDP-43 and CHCHD10/OPA1-mitofilin does not make CHCHD10 loss equivalent to TDP-43 loss. |

The Distributed Agents runtime profile comparison across an 18-target
mitochondria-centered cohort gave the same calibration.  `Chchd2` had
`significant_feature_count = 1`; `Opa1` had 37; 10 of the 18 selected nodes
had no significant features.  Whole-profile correlations were positive among
`Chchd2`, `Opa1`, and quiet mitochondrial nodes such as `Micos13`, `Micu1`,
`Mff`, `Yme1l1`, `Clpp`, `Clpx`, `Lonp1`, and `Ndufs4`, indicating weak
same-direction structure rather than an opposite signature; the significant
tails, however, stayed essentially absent for the close mitochondrial loss
comparators.

I also checked the held-out gene as a measured feature in the focal rows for
other training perturbations.  `Chchd10` was present as a measured gene in all
1,674 focal training profiles.  It was up-regulated in broad high-response
perturbations such as `Uba5` and `Elp1`, and was weakly increased after `Opa1`
perturbation, but those were stress-response consequences and not evidence for
a broad CHCHD10 knockout effect.

## Target-specific prediction

### `Chchd10`

Biology: CHCHD10 is a small mitochondrial intermembrane-space CHCH protein
linked to ALS/FTD and myopathy.  It interacts with CHCHD2 and can affect
MICOS/OPA1 cristae organization.  Dominant missense alleles such as S59L/S55L
can aggregate and drive a mitochondrial integrated stress response, but mouse
and cell data distinguish those toxic alleles from simple Chchd10 loss of
function: Chchd10 ablation alone is viable and often weak because CHCHD2 and
CHCHD10 have partial redundancy.

Within-dataset transfer: the most direct paralog, `Chchd2`, produced only one
focal DEG and that DEG was its own target transcript.  Other mitochondrial
structural or quality-control genes were at zero or a singleton.  `Opa1` was
the only close cristae-linked outlier with 37 DEGs and showed an ATF4-like
stress tail (`Asns`, `Chac1`, `Ddit3`, `Slc7a5`, `Mthfd2`), but direct OPA1
loss is expected to be a harsher inner-membrane/fusion stress than partial
CHCHD10 loss in sparse postnatal neurons.  I therefore predicted a nonzero but
minimal response: a singleton event, most plausibly the target transcript or a
single near-threshold mitochondrial stress gene, rather than an `Opa1`-like
multi-dozen-gene program.

**Prediction: `Chchd10 -> 1` DEG.**

## Limits

The same-experiment corpus had no curated `Chchd10` claim, so the target call
relies on raw profile transfer plus external CHCHD2/CHCHD10/OPA1 literature.
Most decisive external CHCHD10 work uses germline or knock-in animals,
patient fibroblasts, muscle, or motor-neuron contexts; those systems differ
from acute mosaic CRISPR in postnatal thalamic glutamatergic neurons.  The
training data also cannot reveal whether the held-out guides drove a
detectable `Chchd10` transcript decrease.  Thus the distinction between 0 and
1 DEG is intrinsically uncertain; the stronger conclusion is that a broad
`Opa1`- or `Tardbp`-scale focal response is unlikely for loss of CHCHD10.
