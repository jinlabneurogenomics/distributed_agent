# DEG-count prediction for `151 TH Prkcd Grin2c Glut`

## Question and resolved ambiguity

The requested held-out target list contained one gene:

```text
Tubb2a
```

I interpreted the endpoint as the exact `n_degs` used in
`151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`: the number of measured
genes in `151 TH Prkcd Grin2c Glut` whose Wilcoxon `pvals_adj` is below 0.05,
including the perturbed target transcript itself if it crosses that threshold.
The held-out `Tubb2a` perturbation has no row in the training count CSV and no
`gene_target == "Tubb2a"` rows in the parquet, so I used only non-held-out
perturbations as observed calibration.

## Sources used

- Authoritative same-experiment inputs:
  - `[local file: training_de_all_cell_groups.parquet]`
  - `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`
  - `[local file: 252_Tubb2a.csv]`
- Same-experiment interpretation layer: Distributed Agents corpus
  `perturbai-july-260713-sourceguard-1773-v1`; I treated it as a curated
  semantic view over this Perturb-seq experiment, not as independent
  replication.
- Distributed Agents runtime profile-neighborhood tool, run with anchors
  `Tuba1a`, `Tuba4a`, `Tubb4b`, `Tubb5`, and `Dctn1` against the 1,674
  training targets in the same focal cell group.
- PubMed literature:
  - Romaniello et al. 2018, `10.1016/j.ejmg.2018.07.012`, PMID:30016746.
  - Maillard et al. 2022, `10.1016/j.semcdb.2022.07.009`, PMID:35915025.
  - Cai et al. 2020, `10.1038/s10038-020-0739-5`, PMID:32203252.
  - Cederquist et al. 2012, `10.1093/hmg/dds393`, PMID:23001566.

## Computational checks

I first read the 1,674-row endpoint CSV. In the focal cell group, 1,205 of
1,674 non-held-out perturbations had `n_degs == 0`; 276 had exactly one DEG;
only 106 had 10 or more. The count distribution is therefore zero-heavy, and a
single target transcript is a common response size.

I then used DuckDB over the parquet, always filtered to
`group_name = '151 TH Prkcd Grin2c Glut'`, to count the same endpoint for
microtubule and tubulin-neighborhood training targets and to inspect the genes
that actually crossed FDR. The core aggregation was:

```sql
SELECT gene_target,
       SUM(CASE WHEN pvals_adj < 0.05 THEN 1 ELSE 0 END) AS n_degs,
       MAX(n_pert_matched) AS n_pert,
       MAX(n_ctrl_matched) AS n_ctrl
FROM read_parquet(...)
WHERE group_name = '151 TH Prkcd Grin2c Glut'
GROUP BY gene_target;
```

For the direct tubulin perturbations available in training:

| training target | observed `n_degs` in 151 | focal FDR<0.05 genes |
| --- | ---: | --- |
| `Tuba1a` | 7 | `Tuba1a` down, `Tubb3` up, `Tubb2a` up, `Tuba4a` up, `Tubb4a` up, `Tubb4b` up, `Tubb5` up |
| `Tuba4a` | 2 | `Tuba4a` down, `Mast1` up |
| `Tubb4b` | 1 | `Tubb4b` down |
| `Tubb5` | 1 | `Tubb5` down |

The exact `Tubb2a` feature row under `Tuba1a` perturbation was a positive
log2 fold change of `0.523487` with `pvals_adj = 2.68e-07`, so `Tubb2a` is a
participant in the focal `Tuba1a` tubulin-isotype compensation signature.
However, the two represented beta-tubulin knockouts, `Tubb4b` and `Tubb5`,
were self-transcript-only at FDR 0.05 in this cell group, and `Tuba4a` added
only one non-self gene.

Other cytoskeletal comparators in the focal endpoint were similarly weak:
`Map1b`, `Mapt`, `Mapre2`, `Stmn2`, `Kif1a`, `Kif5a`, `Kif5c`, and `Kif21a`
each had one DEG; `Kifbp` and `Tuba4a` had two; `Map6`, `Kif1b`, `Kif2a`,
`Kif3b`, `Ttll5`, `Cep112`, `Cep120`, `Cep290`, and `Cep85l` had zero. The
important counterexample was `Dctn1`, with 75 DEGs in 151 and an FDR-supported
cholesterol/sterol program led by `Insig1`, `Msmo1`, `Hmgcs1`, `Cyp51`,
`Hmgcr`, `Fdft1`, `Sqle`, `Fdps`, and `Ldlr`. I treated `Dctn1` as a boundary
case rather than as a quantitative analog for `Tubb2a`: dynactin loss perturbs
retrograde trafficking and lysosome/sterol biology more broadly than a beta
tubulin isotype loss.

The Distributed Agents runtime profile-neighborhood artifact
`tubulin_profile_neighbors.json` was computed for `Tuba1a`, `Tuba4a`,
`Tubb4b`, `Tubb5`, and `Dctn1` across the exact 1,674 training targets. Its
profile-status summary matched the FDR counts above: the four tubulin anchors
had 1 to 9 significant features, while `Dctn1` had 75. Because whole-profile
correlations among such sparse snRNA-seq DE profiles are dominated by global
rank structure and low-information rows, I gave greater weight to the exact
FDR features and to the corpus' residualized same-experiment comparisons than
to raw all-gene Pearson neighbors.

## Same-experiment biological interpretation

The Distributed Agents corpus records several relevant high- or moderate-confidence
findings:

- `Tuba1a` loss produces a restricted compensatory alpha/beta-tubulin mRNA
  up-regulation module in the two responsive neuronal groups. In this focal
  group that module includes `Tubb2a`, but it contains only seven FDR<0.05
  genes.
- Direct `Tuba4a`, `Tubb4b`, and `Tubb5` perturbations do not phenocopy that
  `Tuba1a` multi-tubulin module; isotype identity matters.
- `Tubb4b` loss was transcriptomically buffered in recovered neurons, with no
  non-self genes at FDR<0.10 in any of 22 groups examined by the corpus.
- Literature-obvious microtubule relatives of `Tubb4b`, including `Tubb5`,
  `Tuba1a`, `Tuba4a`, `Stmn2`, `Mapt`, `Map1b`, `Map6`, `Mapre2`, `Kif5a`,
  `Kif5c`, and `Dctn1`, failed to form a `Tubb4b`-like profile.
- The broader corpus claim for MAP, tubulin, EB, dynactin, kinesin, CAMSAP,
  and MARK-related perturbations was that these targets generally do not form a
  shared postnatal neuronal cytoskeletal-stress mRNA module, apart from the
  restricted `Tuba1a` tubulin-isotype response.

These findings argue against simply transferring the 75-DEG `Dctn1` footprint
or the 7-DEG `Tuba1a` footprint to every tubulin family member.

## External biology

`TUBB2A` encodes a beta-tubulin isotype. Human heterozygous `TUBB2A`
pathogenic variants are a rare tubulinopathy cause of developmental delay,
infantile-onset epilepsy, corpus-callosum defects, and cortical dysplasia
(Cai et al. 2020, PMID:32203252). Reviews of tubulinopathy genetics place
`TUBB2A` with `TUBA1A`, `TUBB2B`, `TUBB3`, `TUBB4A`, `TUBB`, and `TUBG1` in a
family whose variants can alter tubulin heterodimer abundance, GTP binding,
protofilament contacts, motor interactions, neuronal migration, and axon
guidance (Romaniello et al. 2018, PMID:30016746; Maillard et al. 2022,
PMID:35915025). Beta-tubulin isotypes also have partly divergent functions:
the TUBB2B-E421K missense allele, for example, can perturb callosal axon
connectivity by altering microtubule dynamics and reducing kinesin localization
(Cederquist et al. 2012, PMID:23001566).

Those facts support `Tubb2a` as a genuine neuronal microtubule gene, but they
do not imply a broad transcriptome after sparse postnatal CRISPR loss of
function. Much of the disease literature concerns dominant missense alleles
during corticogenesis, whereas this assay perturbs a subset of postmitotic
neurons at P16 and samples recovered nuclei at P37-P44.

## Target-specific prediction

### `Tubb2a`

Relevant positive analogs:

- `Tubb4b`, observed `n_degs = 1`: the only focal FDR<0.05 gene was the
  self-transcript, matching a beta-tubulin knockout that was strongly buffered
  at the mRNA level.
- `Tubb5`, observed `n_degs = 1`: again self-transcript-only in 151, despite
  `Tubb5` being an abundant beta-tubulin isotype and a component of the
  `Tuba1a` compensation signature.
- `Tuba4a`, observed `n_degs = 2`: weak alpha-tubulin response, with target
  down-regulation and one non-self gene, not a broad tubulin replacement
  program.

Relevant counterexamples and boundaries:

- `Tuba1a`, observed `n_degs = 7`, is the strongest direct tubulin analog and
  induced `Tubb2a` itself. I used it as evidence that the assay can see
  tubulin-isotype compensation, not as the central numeric estimate, because
  the corpus found that `Tubb5`, `Tubb4b`, and `Tuba4a` did not reciprocally
  phenocopy this module.
- `Dctn1`, observed `n_degs = 75`, shows that a microtubule-transport target
  can make a much broader focal signature, but its sterol/SREBF2-like response
  is mechanistically tied to dynactin/retrograde-trafficking biology and did
  not extend to the sampled tubulin paralogs.
- MAPs and motors such as `Map1b`, `Mapt`, `Mapre2`, `Stmn2`, `Kif1a`,
  `Kif5a`, and `Kif5c` sat at 1 DEG, while `Map6` and several other motors or
  centrosomal genes were zero, bounding the generic microtubule-neighborhood
  expectation near null.

My zero/nonzero decision is nonzero because all four direct measured tubulin
training perturbations had a significant self-transcript in the focal cell
group, and `Tubb2a` is sufficiently expressed in 151 to be an FDR-significant
feature in the `Tuba1a` response. My approximate count is one rather than 2 to
7 because the closest beta-tubulin paralogs `Tubb4b` and `Tubb5` were
self-only, and the same-experiment corpus explicitly argues that the
`Tuba1a` compensation program is not a generic response to beta-tubulin loss.

Predicted count: `1`.

## Limits

- `Tubb2a` itself was held out as a perturbation target, so there is no direct
  focal expression profile to correlate.
- Tubb2a-specific biology may not match `Tubb4b` or `Tubb5`; tubulin isotypes
  can have distinct expression windows and protein interactions.
- The best external `TUBB2A` evidence concerns human developmental disease,
  often from dominant missense alleles, and is imperfect for acute mouse
  postnatal loss of function.
- A one-DEG prediction assumes the Tubb2a transcript itself will be depleted
  enough to pass FDR. The dataset warns that measured self-knockdown is not a
  reliable editing-efficiency measure, so this is an assay-calibrated
  expectation from neighboring tubulin perturbations rather than a mechanistic
  guarantee.
- Weak non-self effects near the FDR boundary could move the realized count
  between zero and a few DEGs without contradicting the central biological
  picture of a largely buffered beta-tubulin perturbation.
