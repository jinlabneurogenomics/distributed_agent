# Rhobtb2 DEG-count prediction trace

## Question and resolved ambiguities

The task is to predict, for the held-out perturbation in
`198_Rhobtb2.csv`, the number of genes that would pass
Benjamini-Hochberg FDR 0.05 in `151 TH Prkcd Grin2c Glut` nuclei after an
acute sparse AAV-CRISPR loss-of-function perturbation.

The manifest contains one held-out target:

| target_name |
|---|
| Rhobtb2 |

I interpreted `predicted_n_degs = 0` as a prediction that no measured output
gene would pass the same Wilcoxon BH-adjusted `pvals_adj < 0.05` threshold used
in `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.  I treated broad human
DEE phenotypes caused by dominant RHOBTB2 missense variants as informative that
RHOBTB2 is neural, but not as direct evidence for a broad CRISPR loss-of-function
mRNA state, because those variants often stabilize RHOBTB2 protein whereas the
screen produces mosaic loss of function.

## Sources used

Primary same-experiment evidence:

- `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`
  for focal-cell observed DEG counts from the 1,674 non-held-out perturbations.
- `[local file: training_de_all_cell_groups.parquet]`
  for focal-cell signed log fold changes, adjusted p-values, and matched cell
  counts for candidate analog perturbations.
- Distributed Agents same-experiment corpus
  `perturbai-july-260713-sourceguard-1773-v1`.  There was no Rhobtb2-centered
  report in the corpus, but the corpus had useful boundary reports for `Cdc42`,
  `Rac1`, `Kctd1`, and represented Rac/Cdc42/PAK pathway perturbations.
- Distributed Agents runtime profile tools, used to compare the focal-cell expression
  profiles of candidate analogs.

External biology:

- PubMed searches on `RHOBTB2`, `RhoBTB`, and `DBC2` for curated literature.
- RhoBTB/CUL3 adaptor mechanism: Berthold et al. 2008,
  PubMed 18835386, DOI 10.1016/j.yexcr.2008.09.005; Ji and Rivero 2016,
  PubMed 27314390, DOI 10.3390/cells5020028.
- DBC2/RHOBTB2 as a CUL3 substrate adaptor: Manjarrez et al. 2014,
  PubMed 24608665, DOI 10.1371/journal.pone.0090054; Choi et al. 2016,
  PubMed 27941885, DOI 10.1038/onc.2016.441.
- RHOBTB2 developmental epileptic encephalopathy and genotype/function
  separation: Straub et al. 2017, PubMed 29276004,
  DOI 10.1016/j.ajhg.2017.11.008; Belal et al. 2018, PubMed 29768694,
  DOI 10.1002/humu.23550; Langhammer et al. 2023, PubMed 37165955,
  DOI 10.1016/j.gim.2023.100885; Langhammer et al. 2025,
  PubMed 39849855, DOI 10.1093/hmg/ddae183.

## Computations over the training data

The focal endpoint file is strongly zero-inflated:

- 1,674 training perturbations.
- 1,205/1,674 have `n_degs = 0`.
- Median is 0, 75th percentile is 1.
- Mean is 14.1 because a few very large responses, for example `Uba5 = 2677`,
  `Tpr = 1768`, and `Sin3a = 1433`, dominate the tail.

Direct RhoBTB paralogs and several exact CUL3 complex genes were not available
as non-held-out training targets:

| candidate | focal count availability |
|---|---:|
| Rhobtb1 | absent |
| Rhobtb3 | absent |
| Cul3 | absent |
| Rbx1 | absent |
| Cand1 | absent |
| Keap1 | absent |
| Klhl13 | absent |
| Lrrc41 | absent |
| Msi2 | absent |

For available analogs, I used the training count CSV for `n_degs` and scanned
the row groups of the parquet whose `group_name` statistics covered
`151 TH Prkcd Grin2c Glut`.  I retained rows in that cell type with
`gene_target` in a candidate set and `pvals_adj < 0.05`, which gives the
identity and direction of the significant genes behind each count:

```python
for row_group in focal_row_groups:
    rows = parquet.read_row_group(
        row_group,
        columns=[
            "names", "logfoldchanges", "pvals_adj", "group_name",
            "gene_target", "n_pert_matched", "n_ctrl_matched",
        ],
    ).to_pandas()
    rows = rows[
        (rows.group_name == "151 TH Prkcd Grin2c Glut")
        & (rows.gene_target.isin(candidate_targets))
    ]
    significant = rows[rows.pvals_adj < 0.05]
```

The concrete focal-cell analog counts were:

| class | training perturbations and observed `n_degs` |
|---|---|
| BTB/KCTD/Kelch low-level CUL3-adaptor relatives | `Kctd1 = 2`, `Kctd8 = 0`, `Kctd16 = 0`, `Btbd9 = 0`, `Kbtbd7 = 0`, `Klhl7 = 0`, `Klhl20 = 0` |
| Rho/Rac/Cdc42 and actin-effectors | `Rac1 = 0`, `Cdc42 = 1`, `Pak1 = 1`, `Pak2 = 0`, `Pak3 = 0`, `Cyfip1 = 0`, `Cyfip2 = 1`, `Tiam1 = 0`, `Kalrn = 0`, `Dock3 = 0`, `Fgd4 = 0`, `Arhgap18 = 0`, `Arhgap32 = 0`, `Arhgef9 = 1`, `Baiap2 = 0`, `Limk1 = 0`, `Cfl2 = 0` |
| individual ubiquitin-ligase/proteostasis boundaries | `Ube3a = 0`, `Ddb2 = 0`, `Fbxo11 = 1`, `Fbxo38 = 0`; core proteostasis controls were much larger: `Psmb4 = 742`, `Psmc1 = 430`, `Ufc1 = 572`, `Uba5 = 2677` |
| ion-channel/AHC comparators | `Scn1a = 1`, `Scn2a = 1`, `Scn8a = 1`, `Kcnq2 = 1`, `Kcnq3 = 1`, `Atp1a3 = 80` |

The significant genes in the best analogs did not form a shared Rhobtb2-like
module.  In the BTB/CUL3-adaptor group, only `Kctd1` had any focal response:
`Resp18` was up and `Cluap1` was down.  `Kctd8`, `Kctd16`, `Btbd9`,
`Kbtbd7`, `Klhl7`, and `Klhl20` had no significant genes.  In the Rho/Rac/Cdc42
set, the rare one-gene calls were almost all self-knockdown events:
`Cdc42`, `Pak1`, `Cyfip2`, and `Arhgef9` were each the only FDR-significant
gene in the corresponding perturbation.

I also ran a runtime profile comparison on 20 focal-cell candidate profiles
spanning those BTB/CUL3 and Rho-axis candidates.  It reported 15/20 candidates
with no significant focal features and 5/20 with only 1 to 9 significant
features.  For the inspected focal nodes `Kctd1`, `Rac1`, `Cdc42`, `Fbxo11`,
and `Btbd9` against 10 nearby peers, every pair had zero FDR-significant
same-direction intersections.  That is why I did not average raw all-gene
correlations: the candidate profiles are near-null, and the sparse significant
outputs are target-specific.

## Target-specific reasoning

### Rhobtb2

`Rhobtb2` encodes one of the three mammalian RhoBTB proteins.  RhoBTB proteins
are atypical Rho-family proteins with tandem BTB domains that bind CUL3 and can
form CUL3-dependent ubiquitin-ligase complexes; RHOBTB2 also undergoes CUL3-
linked autoregulation and its BTB-domain pathogenic alleles often accumulate
because they are not degraded normally.  That makes the most appropriate in-
screen analogs either BTB/CUL3 substrate adaptors or Rho-family cytoskeletal
signaling nodes, not the core proteasome genes whose loss created hundreds to
thousands of DEGs.

The direct RhoBTB paralogs (`Rhobtb1`, `Rhobtb3`) and `Cul3` itself were absent,
so this is an extrapolation from weaker analogs.  The represented BTB and
KCTD/Kelch single adaptors were uniformly small in the focal group:
`Kctd1 = 2` was the maximum, and six other BTB/Kelch genes were 0.  `Kctd1`
is the closest positive counterexample because it is also a BTB-family CUL3-
adaptor-like target with a small TH response, but its two markers (`Resp18`,
`Cluap1`) are not a CUL3/RhoBTB program and the Distributed Agents Kctd1 reports
explicitly interpreted it as a tiny cell-type-restricted surface rather than a
canonical pathway response.

The Rho-side comparison also argues against a broad transcriptional response.
The Distributed Agents Cdc42 and Rac1 reports summarized represented Rac/Cdc42/PAK/WAVE,
GEF/GAP, and actin-cytoskeleton perturbations as transcriptionally buffered in
juvenile neurons.  The focal count file matches that: `Rac1`, `Pak2`, `Pak3`,
`Cyfip1`, `Tiam1`, `Kalrn`, `Dock3`, `Fgd4`, `Arhgap18`, `Arhgap32`, `Limk1`,
`Cfl2`, and `Baiap2` were all 0; `Cdc42`, `Pak1`, `Cyfip2`, and `Arhgef9` were
1 and their one gene was the targeted transcript itself.  Rhobtb2 is even less
likely than canonical Cdc42/Rac1 to drive an acute nuclear actin program because
RhoBTB proteins are atypical pseudo-GTPase-like scaffolds with CUL3/BTB
function, not classic membrane-localized GTPases switching PAK/LIMK output.

The external DEE literature keeps the prediction from being a trivial "unknown
BTB gene equals null" call.  De novo BTB-domain RHOBTB2 variants cause severe
developmental epileptic encephalopathy and stabilize the protein in vitro
and in Drosophila models, while later cohorts found that GTPase-domain missense
variants and biallelic truncating variants have different, often more variable
phenotypes.  The 2025 iPSC-neuron study specifically found altered neuronal
activity/excitability for BTB-domain variants but not for complete RHOBTB2
loss.  Therefore the strongest human phenotype is probably a dose/stabilization
or allele-specific substrate-adaptor phenotype, imperfectly modeled by a P16
mosaic loss-of-function perturbation.

Ion-channel disease comparators were also mostly null.  `Scn1a`, `Scn2a`,
`Scn8a`, `Kcnq2`, and `Kcnq3` each produced only a self-transcript hit in the
focal group.  `Atp1a3` was broader at 80 DEGs and is a phenotype-level
alternating-hemiplegia counterexample, but it is a plasma-membrane sodium/
potassium ATPase whose acute loss directly perturbs ionic homeostasis; it is
not a CUL3 adaptor and should not be pooled with Rhobtb2.

Finally, Rhobtb2 itself was a measured output gene for all 1,674 training
perturbations in the focal cell group but was significant after only two very
large perturbations (`Cic` and `Elp1`), with median adjusted p-value 1.0.  That
does not measure Rhobtb2 knockdown, but it argues that Rhobtb2 is not sitting
inside a common stress or proteostasis mRNA module in these neurons.

I therefore expect acute sparse `Rhobtb2` loss in `151 TH Prkcd Grin2c Glut`
to look like the null BTB-adaptor/Rho-axis perturbations rather than like core
proteasome or ion-pump perturbations.  The most likely count is zero; the main
alternative would be one or two target-specific sentinel genes analogous to
`Kctd1`, but I do not see support for a recurrent marker, so I did not round up.

Prediction: `Rhobtb2 -> 0`.

## Limits

- There is no within-dataset `Rhobtb2`, `Rhobtb1`, `Rhobtb3`, or `Cul3`
  perturbation to transfer from; the prediction uses weaker BTB/KCTD/Kelch and
  Rho/Rac/Cdc42 neighbors.
- The CUL3 substrate repertoire of RHOBTB2 in postnatal thalamic glutamatergic
  neurons is not well defined.  Tumor-cell substrates such as MSI2 and epithelial
  outputs such as CXCL14 are not represented as strong neuronal comparators.
- Human dominant BTB-domain variants are likely not simple loss-of-function
  alleles.  A stabilized RHOBTB2 missense protein could perturb neurons in a
  way that a mosaic CRISPR deletion does not.
- The endpoint is an FDR-count endpoint with finite matched cell numbers, not a
  measurement of protein loss, CUL3 ligase activity, dendrite morphology, or
  neuronal excitability.  A zero-DEG prediction still allows a local synaptic,
  electrophysiological, or developmental phenotype outside this snRNA-seq
  geometry.
