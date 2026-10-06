# DEG-count prediction trace

## Question and resolved ambiguities

The held-out target list for this run contains one perturbation:

```tsv
target_name
Naa15
```

The requested endpoint is the integer number of genes with Benjamini-Hochberg
adjusted Wilcoxon `pvals_adj < 0.05` in `151 TH Prkcd Grin2c Glut` cells after
acute AAV-PHP.eB CRISPR loss of the target gene. I interpreted a prediction of
`0` literally: no measured gene is expected to pass the focal-cell FDR 0.05
threshold. I did not use Naa15's own expression signature or DEG count because
that target was held out from both input files.

## Sources used

- Input training endpoint:
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
  I used this to read the observed focal `n_degs` for all 1,674 non-held-out
  perturbations.
- Input DE parquet:
  `[local file: training_de_all_cell_groups.parquet]`.
  I filtered this to the focal cell group and the observed NatA analog Naa10,
  then counted `pvals_adj < 0.05` and inspected the strongest nominal rows.
- Distributed Agents runtime profile engine, using the same parquet, the same focal-cell
  filter, `gene_target` as the entity, `names` as the feature, and
  `logfoldchanges` as the signed value. I profiled Naa10 against the 1,674
  eligible focal-cell training targets.
- Distributed Agents corpus release
  `perturbai-july-260713-sourceguard-1773-v1`. Naa15 itself was not present in
  that corpus, but the Naa10 target context supplied same-experiment findings
  and explicit contrasts to protein-homeostasis perturbations.
- Local gene annotations from the Distributed Agents annotation layer:
  CORUM 5.0 human one-to-one ortholog projections through MGI homology
  downloaded 2026-09-13, STRING physical v12.0, and Gene Ontology terms.
- External literature:
  Cheng et al. 2018, DOI `10.1016/j.ajhg.2018.03.004`, PMID `29656860`;
  Varland and Arnesen 2018, DOI `10.1186/s13104-018-3513-4`, PMID `29929531`;
  McTiernan et al. 2020, DOI `10.1038/s41431-020-00728-2`, PMID `32973342`;
  Lyon et al. 2023, DOI `10.1038/s41431-023-01368-y`, PMID `37130971`.

## Training-set computations

The focal training-count distribution is highly sparse: among 1,674 training
perturbations, the median was `0`, the 75th percentile was `1`, the 90th was
`2`, the 95th was `18`, and the maximum was `2,677` DEGs. This makes a zero
prediction common, but not automatically correct, so I next looked for
same-complex evidence.

The local CORUM projection places Naa15 with:

| complex | represented members | focal training members |
| --- | --- | --- |
| CORUM 702, `NAA10-NAA15 complex` | Naa10, Naa15 | Naa10, `n_degs=0` |
| CORUM 7663, `HYPK-NAA10-NAA15 complex` | Naa10, Naa15 | Naa10, `n_degs=0` |
| CORUM 7854, `NAA10-NAA15_NAA50 complex` | Naa10, Naa15, Naa50 | Naa10, `n_degs=0` |
| CORUM 95, `Ku antigen-NARG1 complex` | Naa15, Xrcc5, Xrcc6 | none |

STRING physical v12.0 also connects Naa15 to Naa10 with high confidence
(`0.936`, database `0.720`, experimental `0.503`, text mining `0.581`) and to
Naa50 with high confidence (`0.948`), but Naa50 was not an observed training
perturbation in the focal count table. Thus Naa10 is the only direct NatA
training perturbation available.

I then filtered the parquet to
`group_name == "151 TH Prkcd Grin2c Glut"` and `gene_target == "Naa10"`.
This produced 17,259 measured genes with `240` matched Naa10-perturbed nuclei
and `23,679` matched controls. The recomputed focal endpoint was exactly
`sum(pvals_adj < 0.05) == 0`; the smallest adjusted p-values were still `1.0`.

For expression-pattern evidence, I profiled the full Naa10 focal
log-fold-change vector against the 1,674 eligible focal training profiles.
Naa10 had no FDR-significant features. Its top whole-vector Pearson neighbors
were also zero or sparse targets:

| training target | Pearson to Naa10 | observed focal DEGs |
| --- | ---: | ---: |
| Abca1 | 0.6968 | 0 |
| Copg1 | 0.6960 | 1 |
| Hcn2 | 0.6945 | 1 |
| Pde10a | 0.6935 | 0 |
| Sall1 | 0.6925 | 0 |
| Vldlr | 0.6924 | 0 |
| Dennd5a | 0.6918 | 0 |
| Arih1 | 0.6917 | 7 |
| Lamp2 | 0.6916 | 0 |
| Bmpr1a | 0.6915 | 0 |

The top whole-vector cosine neighbors told the same story: Abca1 `0`, Copg1
`1`, Vldlr `0`, Dennd5a `0`, Pde10a `0`, Arih1 `7`, Bmpr1a `0`, Sall1 `0`,
Hcn2 `1`, and Orc6 `0` were the top ten by cosine. Top-tail overlaps were weak.
For example, a broad splicing perturbation, Cdc40 with `624` DEGs, appeared
only in the top one-percent positive-tail list with an overlap coefficient of
`0.121` over 173 genes; I treated that as background tail overlap rather than
a mechanistic NatA neighbor.

The Distributed Agents corpus has direct same-experiment findings for Naa10. The
important ones here were:

- `Naa10:F001`: postmitotic P16 Naa10 perturbation was a pan-neuronal
  transcriptomic null across 22 measured neuronal groups, with 2,123 total
  matched perturbed nuclei and zero downstream genes at FDR 0.10.
- `Naa10:F002`: the Naa10-null surface did not contain a compensatory NAT-family,
  integrated-stress, apoptosis, or proteasome/ubiquitin rebound program at FDR
  0.10.
- `Naa10:F003`: the flat Naa10 profile contrasted with assay-detectable
  protein-homeostasis and translation perturbations. Psmb4, Psmc1, and Eef2
  generated 1,119 to 14,008 downstream FDR 0.10 genes across matched groups
  where Naa10 generated none.
- `Naa10:F004`: data-driven neighbors grouped Naa10 with other flat signatures,
  not with a specific NatA or proteotoxic-stress module.

## Target-specific reasoning

### Naa15

**Biologically relevant training analogs and counterexamples**

Naa10 is the central analog. It encodes the NatA catalytic subunit, while Naa15
is the NatA auxiliary/ribosome-anchoring subunit. The two form the
NAA10-NAA15 CORUM complex, and STRING v12.0 supports a direct physical
interaction. Varland and Arnesen 2018 report that NAA15 binds NAA10, folds it
for NatA substrate acetylation, and anchors NatA to ribosomes for
co-translational N-terminal acetylation. McTiernan et al. 2020 describe a
human NAA10 p.N101K allele that specifically disrupts NAA15 binding and NatA
complex activity while preserving monomeric NAA10, which reinforces that
NAA10-NAA15 complex formation is the relevant shared mechanism.

In the actual focal training data, Naa10 had `0` DEGs. The parquet confirmed
that this was not a rounding artifact: no gene had `pvals_adj < 0.05` and all
Naa10 adjusted p-values in `151 TH Prkcd Grin2c Glut` were `1.0`. Its nearest
same-cell expression neighbors were almost all similarly flat, with the top ten
whole-profile Pearson neighbors carrying `0, 1, 1, 0, 0, 0, 0, 7, 0, 0` DEGs.
That pattern argues for a null or below-threshold NatA transcriptional response
under this acute postnatal partial-perturbation assay.

I used Psmc1 and Psmb4 as counterexamples rather than positive analogs. Their
focal counts were large, `430` and `742`, and the Distributed Agents Psmc1 findings
describe proteasome-subunit perturbation as inducing an HSF1-linked
chaperone/integrated-stress program in responsive neurons. Naa10 did not
activate that module despite encoding a major co-translational protein
modification enzyme. This comparison makes it unlikely that every perturbation
of an abundant protein-biogenesis or protein-homeostasis process should be
assigned a broad 151 TH Prkcd Grin2c Glut DEG count.

**External biological prior**

NatA is unquestionably important for development. NAA15 truncating variants
cause dominantly acting neurodevelopmental disease with intellectual
disability, autism spectrum disorder, congenital anomalies, and evidence for
haploinsufficiency in patient cells and yeast functional assays
(Cheng et al. 2018). A larger NAA10/NAA15 genotype-first series found
overlapping NAA10- and NAA15-related neurodevelopmental spectra involving
intellectual disability, delayed milestones, autism, craniofacial and cardiac
features, seizures, and visual anomalies (Lyon et al. 2023).

Those disease data raise the prior that severe germline NatA dysfunction has
neuronal consequences, but they are imperfect for this endpoint. This experiment
is an acute, mosaic, P16-to-P37/44 CRISPR perturbation in already postmitotic
neurons, with average on-target RNA downregulation of only about 18 percent per
guide. The primary lesion is expected to be altered N-terminal acetylation and
protein stability rather than direct transcription-factor loss. Given that the
more catalytic same-complex target Naa10 had a pan-neuronal FDR-level null in
the same experiment, the strongest calibration is that Naa15 should also fall
below the focal FDR 0.05 threshold.

**Prediction**

I predict `0` DEGs for Naa15.

## Limits and extrapolations

- Naa15 was absent from the Distributed Agents same-experiment corpus and from the DE
  training parquet by construction; the prediction is transferred from Naa10
  and from external NatA biology.
- The direct Naa15-Naa50 and Ku antigen-NARG1 CORUM partners were not observed
  in the focal training counts, so the only same-complex empirical analog was
  Naa10.
- A zero DEG prediction does not mean Naa15 editing failed or that NatA biology
  is irrelevant. N-terminal acetylation, NAA10/NAA15 protein abundance,
  substrate stability, dendritic morphology, survival before nuclei harvest,
  and electrophysiology were not measured by the DEG endpoint.
- Naa15 could in principle have Naa10-independent roles, and sparse AAV CRISPR
  could perturb Naa15 and Naa10 proteins differently. I nevertheless treated
  this as weaker than the same-complex Naa10 null because the endpoint is a
  short-term steady-state nuclear RNA readout in postmitotic neurons.
- Dense correlations among all 17,259 log-fold-change entries are dominated by
  subthreshold structure when the anchor has zero FDR genes. I used the Naa10
  profile-neighbor result only to check that no strong high-DEG expression
  analog was being missed, not as a stand-alone mechanistic module.
