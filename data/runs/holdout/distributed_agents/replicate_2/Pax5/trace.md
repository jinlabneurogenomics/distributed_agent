# DEG-count prediction trace for `151 TH Prkcd Grin2c Glut`

## Question interpreted

The held-out target list for this run contains one mouse gene, `Pax5`.  I
interpreted the endpoint as the integer number of measured genes that would
have `pvals_adj < 0.05` in `151 TH Prkcd Grin2c Glut` after acute, sparse,
postnatal AAV-PHP.eB CRISPR loss of function, using the same Scanpy Wilcoxon
pipeline as the training data.

The important ambiguity is that `Pax5` has strong biology in B lymphocytes and
embryonic patterning, but the readout here is NeuN-enriched juvenile brain
nuclei after P16 mosaic editing.  I therefore treated a germline Pax5 phenotype
or a B-cell regulatory role as evidence only if the same pathway, paralogs, or
nearby lineage factors were active in the postnatal neuronal training data.

## Sources used

- Held-out manifest:
  `[local file: 167_Pax5.csv]`
  contained exactly `Pax5`.
- Endpoint training file:
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`,
  with 1,674 non-held-out targets and their observed focal-cell `n_degs`.
- Per-gene DE parquet:
  `[local file: training_de_all_cell_groups.parquet]`,
  filtered to `group_name == "151 TH Prkcd Grin2c Glut"` for the mechanistic
  comparator targets below.
- Distributed Agents corpus MCP, release
  `perturbai-july-260713-sourceguard-1773-v1`, queried for same-experiment
  claims and findings around Pax, EBF, and lymphocyte-immunoreceptor
  perturbations.
- PubMed literature searches for PAX5/Pax5 B-lineage and Pax2/Pax5/Pax8
  developmental biology.

## Computations over the supplied tables

The count table showed that the focal endpoint is zero-inflated but not
uniformly zero:

| quantity | value |
| --- | ---: |
| training targets | 1,674 |
| targets with `n_degs > 0` | 469 |
| median | 0 |
| 75th percentile | 1 |
| 95th percentile | 18 |
| 99th percentile | 436.48 |
| maximum | 2,677 |

Thus exact zeros are common in this assay, while broad transcriptional
responses can be detected in `151 TH Prkcd Grin2c Glut` when an active target is
perturbed.

For biologically selected comparators, I read only the focal-cell rows from the
large parquet and joined them to the focal count CSV.  The relevant operation
was:

```python
pq.read_table(
    "training_de_all_cell_groups.parquet",
    columns=[
        "names", "gene_target", "logfoldchanges", "pvals", "pvals_adj",
        "n_pert_matched", "n_ctrl_matched",
    ],
    filters=[
        ("group_name", "=", "151 TH Prkcd Grin2c Glut"),
        ("gene_target", "in", selected_comparators),
    ],
)
```

Each selected target had 17,259 measured downstream rows in the focal cell
group; `n_ctrl_matched` was 23,679.  I used the supplied count CSV as the
authoritative `n_degs` value and used the parquet rows to confirm that the
candidate signatures had no FDR-significant genes and no coherent
near-threshold Pax- or B-cell-like signature.

## Target-specific reasoning

### Pax5

**Closest family analogs in the focal training endpoint**

| training perturbation | `n_pert_matched` | focal `n_degs` | minimum focal `pvals_adj` |
| --- | ---: | ---: | ---: |
| `Pax2` | 251 | 0 | 0.936979 |
| `Pax8` | 195 | 0 | 1.0 |
| `Pax6` | 138 | 0 | 1.0 |
| `Pax3` | 196 | 0 | 1.0 |
| `Pax4` | 214 | 0 | 1.0 |
| `Pax7` | 237 | 0 | 1.0 |

`Pax2` and `Pax8` are the most relevant paralogous comparators because Pax2,
Pax5, and Pax8 form the same paired-box subfamily and can recognize related
paired-domain motifs.  That family relationship is old molecular biology, not
a superficial naming match: Phelps and Dressler 1996 showed Pax2 recognition
sites related to Pax5/Pax2 consensus sites, Kozmik et al. 1993 described Pax8
isoforms that recognize DNA in a manner similar to Pax2 and BSAP/Pax5, and
Roberts et al. 2001 showed Id proteins can antagonize Pax2/Pax5/Pax8 DNA
binding on the B-cell `mb-1`/`Cd79a` promoter.  At the organismal level, Pax2
and Pax5/Pax8 participate in an embryonic midbrain-hindbrain organizer
network; Ye et al. 2001 placed Pax2 upstream of FGF8 partly through Pax5 and
Pax8 at that boundary.

In the focal training data, however, every measured Pax-family perturbation was
exactly null at 5% FDR.  The closest Pax2/Pax8 branch was not even near the
threshold in `151 TH Prkcd Grin2c Glut`: the best Pax2 adjusted p-value was
0.936979 and the best Pax8 adjusted p-value was 1.0.  The Distributed Agents corpus
independently summarized this same-experiment pattern as a moderate-confidence
claim: represented Pax/Otx/Pitx/En developmental regulators, including Pax2
and Pax8, did not recover canonical thyroid, retinal, Pax/Otx, or
midbrain-hindbrain programs in sampled postnatal neuronal groups.  Pax2- and
Pax8-centered corpus findings specifically reported nearly flat postnatal
neuronal transcriptomes and no convergence among Pax8, Pax6, Pax2, En1, En2,
Otx2, Gata3, and Lbx1.

**B-cell lineage and immunoreceptor analogs**

| training perturbation | focal `n_degs` | reason it was considered |
| --- | ---: | --- |
| `Ebf1` | 0 | upstream B-lineage transcriptional network member |
| `Ebf2` | 0 | EBF/COE-family paralog |
| `Ebf3` | 0 | EBF/COE-family paralog |
| `Tcf3` | 0 | B-lineage transcription factor |
| `Ikzf3` | 0 | IKZF-family lymphoid regulator |
| `Irf8` | 0 | immune/B-myeloid transcriptional regulator |
| `Spi1` | 0 | immune-lineage ETS factor |
| `Cd79a` | 0 | BCR subunit and Pax5-linked B-cell target locus |
| `Cd79b` | 0 | obligate BCR partner of CD79A |
| `Cd247`, `Cd3d`, `Cd3e`, `Cd3g`, `Cd4` | 0 | TCR/CD3 lymphocyte receptor comparators |
| `Cd40`, `Cd80`, `Icos` | 0 | immune costimulation comparators |

Pax5 is a central B-cell commitment and identity factor.  Urbanek et al. 1994
found that Pax5/BSAP loss blocks early B-cell differentiation and affects
posterior midbrain patterning in germline mice.  Nutt et al. 1999 showed Pax5
is needed for B-lymphoid lineage commitment by repressing alternative lineage
programs, and Cobaleda et al. 2007 reviewed how Pax5 activates B-lineage genes
while repressing inappropriate programs to maintain B-cell identity.

Those mechanisms would predict a large expression response in a B-lineage
system.  They did not transfer to the NeuN-positive focal neurons.  In
`151 TH Prkcd Grin2c Glut`, the represented upstream or parallel B-lineage
transcription factors `Ebf1`, `Tcf3`, `Ikzf3`, `Irf8`, and `Spi1` all had
`n_degs = 0`; so did the BCR subunits `Cd79a` and `Cd79b` and the represented
TCR/costimulation controls.  The per-gene focal signatures for these
comparators were flat after BH correction as well: the best adjusted p-values
among `Ebf1`, `Tcf3`, `Ikzf3`, `Irf8`, `Spi1`, `Cd79a`, and `Cd79b` were
0.144989, 0.883689, 1.0, 0.121418, 1.0, 1.0, and 1.0, respectively.  The
Distributed Agents corpus also contained same-experiment claims that represented EBF
factors were largely buffered and non-interchangeable after P16 perturbation,
and that represented lymphocyte immunoreceptor components did not form a
latent shared BCR/TCR/CD3-like transcriptional module in NeuN-positive nuclei.

**Other off-lineage developmental transcription-factor controls**

Additional out-of-lineage lineage regulators were all null in the same focal
endpoint: `Hesx1 = 0`, `Lhx3 = 0`, `Pou1f1 = 0`, `Prop1 = 0`, `Gfi1 = 0`, and
`Gfi1b = 0`.  These are imperfect analogs for Pax5, but they are useful
counterexamples to a naive "transcription-factor perturbations should get a
positive count" rule.  In this juvenile postmitotic neuronal assay, acute loss
of a lineage-restricted TF usually produced no detectable broad response
unless that TF was coupled to a maintained transcriptional state in the sampled
neurons.

## Zero/nonzero call

I predict `Pax5` will have no genes below FDR 0.05 in
`151 TH Prkcd Grin2c Glut`.

This is driven mainly by within-dataset evidence:

- the focal count for every represented Pax-family perturbation was 0,
  including the closest Pax2/Pax8 branch;
- those Pax2 and Pax8 focal signatures were not borderline, with minimum
  adjusted p-values of 0.936979 and 1.0;
- represented B-cell-lineage transcription factors and BCR/TCR/immunoreceptor
  genes were also uniformly 0 in the focal endpoint;
- the same-experiment Distributed Agents claims around Pax2/Pax8, EBF factors, and
  lymphocyte immunoreceptors all frame those zeros as coherent off-lineage or
  off-window negatives in postnatal NeuN-positive nuclei rather than isolated
  guide failures.

External biology resolves why those zeros are the right analogs: Pax5's
well-established activities are B-cell identity/commitment and embryonic
midbrain-hindbrain development, neither of which is expected to be actively
maintained in postmitotic `151 TH Prkcd Grin2c Glut` neurons 3-4 weeks after
P16 editing.

## Prediction

| target | predicted `n_degs` |
| --- | ---: |
| `Pax5` | 0 |

## Literature cited

- Urbanek P, Wang ZQ, Fetka I, Wagner EF, Busslinger M. 1994. Pax5/BSAP loss
  in mouse blocks early B-cell differentiation and alters posterior midbrain
  patterning. PMID: 8001127. DOI: 10.1016/0092-8674(94)90079-5.
- Nutt SL, Heavey B, Rolink AG, Busslinger M. 1999. Pax5 is required for
  commitment to the B-lymphoid lineage and represses alternative lineage
  programs. PMID: 10524622. DOI: 10.1038/44076.
- Cobaleda C, Schebesta A, Delogu A, Busslinger M. 2007. Pax5 as a regulator
  of B-cell identity and function. PMID: 17440452. DOI: 10.1038/ni1454.
- Ye W, Bouchard M, Stone D, Liu X, Vella F, Lee J, Nakamura H, Ang SL,
  Busslinger M, Rosenthal A. 2001. Pax2 controls FGF8 at the midbrain-hindbrain
  boundary in part through Pax5/8. PMID: 11704761. DOI: 10.1038/nn761.
- Kozmik Z, Kurzbauer R, Dorfler P, Busslinger M. 1993. Pax8 splice isoforms
  retain the paired domain and share DNA recognition with Pax2 and BSAP/Pax5.
  PMID: 8413205. DOI: 10.1128/mcb.13.10.6024-6035.1993.
- Phelps DE, Dressler GR. 1996. Chromatin precipitation and binding assays
  identify Pax2 binding sites related to Pax2/Pax5 consensus sequences.
  PMID: 8626478. DOI: 10.1074/jbc.271.14.7978.
- Roberts EC, Deed RW, Inoue T, Norton JD, Sharrocks AD. 2001. Id proteins
  antagonize Pax2/Pax5/Pax8 DNA binding and Pax5-complex activity on the
  B-cell-specific `mb-1` promoter. PMID: 11134340. DOI:
  10.1128/MCB.21.2.524-533.2001.

## Limits

- `Pax5` itself is held out, so its editing rate, target transcript
  down-regulation, and expression signature were not available.
- The strongest analogs are negative signatures.  They support a zero prediction
  by repeatedly failing to show Pax-, EBF-, or lymphocyte-module activity in the
  sampled neurons, but they cannot estimate a hidden one- or two-gene Pax5-only
  effect with much precision.
- `Cd79a`, `Cd79b`, CD3/TCR genes, and immune costimulation genes are pathway
  comparators for Pax5's B-cell biology, not transcription-factor paralogs.
  Their nulls are useful only for judging whether a latent immune program was
  engaged in NeuN-positive nuclei.
- The result should not be extrapolated to embryonic hindbrain, spinal cord,
  kidney/thyroid lineages, or B cells.  The prediction is only for the
  single-nucleus RNA response in recovered juvenile `151 TH Prkcd Grin2c Glut`
  cells after the specified acute mosaic CRISPR perturbation.
