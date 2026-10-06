## Question and resolved scope

The held-out manifest for this run contains one requested perturbation:
`Tubb4a`.  I interpreted the task as a point prediction of the number of genes
that would pass `pvals_adj < 0.05` in the completely held-out `Tubb4a`
Perturb-seq loss-of-function profile in `151 TH Prkcd Grin2c Glut` cells.

The count is therefore an assay-specific Wilcoxon/FDR endpoint, not an estimate
of the biological importance of `Tubb4a`, of protein depletion, or of cell
viability.  I treated target-RNA depletion as possible evidence for whether a
one-gene signature is plausible in this assay, but not as a required proof of
editing success.

## Sources

- `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`, the observed training
  endpoint for this focal cell group.
- `training_de_all_cell_groups.parquet`, especially the 17,259 measured-gene
  vectors for every non-held-out perturbation in `151 TH Prkcd Grin2c Glut`.
- Distributed Agents same-experiment corpus release
  `perturbai-july-260713-sourceguard-1773-v1`; I queried target contexts for
  `Tubb4a`, `Tubb4b`, `Tubb5`, `Tuba1a`, `Tuba4a`, `Tbcd`, and `Dctn1`.
  `Tubb4a` itself was absent from the corpus, while the represented tubulin and
  microtubule targets had curated findings about their in-assay contrasts.
- PubMed for external tubulin biology:
  - Simons et al. 2013, DOI `10.1016/j.ajhg.2013.03.018`, PMID `23582646`.
  - Sase et al. 2020, DOI `10.7554/eLife.52986`, PMID `32463361`.
  - Krajka et al. 2022, DOI `10.1126/sciadv.abj9229`, PMID `35275727`.
  - Sase et al. 2026, DOI `10.1016/j.ymthe.2026.01.016`, PMID `41566774`.

## Same-experiment computations

The input parquet has 616,253,184 rows, so I first inspected Parquet row-group
statistics on `group_name` and found that row groups 546-580 span the focal
cell group.  I then materialized only `151 TH Prkcd Grin2c Glut` into a local
parquet:

```python
for each row group with min(group_name) <= focal <= max(group_name):
    read columns names, gene_target, logfoldchanges, pvals_adj, n_pert_matched
    keep rows where group_name == "151 TH Prkcd Grin2c Glut"
```

The extracted focal table had 28,891,566 rows: 1,674 training perturbations x
17,259 measured genes.  Summing `pvals_adj < 0.05` in that table reproduced
the training counts for the tubulin and microtubule-neighbor targets below.

I then inspected observed paralogs and pathway neighbors.  The relevant focal
cell DEG counts were:

| training target | focal `n_degs` | focal expression-pattern evidence | interpretation for `Tubb4a` |
| --- | ---: | --- | --- |
| `Tubb4b` | 1 | only `Tubb4b` itself was significant: log2FC -0.597, FDR 1.07e-7; `Tubb4a` was not induced, log2FC +0.178, FDR 1.0 | closest beta-tubulin perturbation in the dataset; strong evidence that partial postnatal beta-tubulin loss can be almost transcriptionally silent except for the target transcript |
| `Tubb5` | 1 | only `Tubb5` itself was significant: log2FC -1.478, FDR 7.71e-23; `Tubb4a` was not induced, log2FC +0.108, FDR 1.0 | second direct beta-tubulin anchor; argues against a generic beta-tubulin loss response |
| `Tuba1a` | 7 | `Tuba1a` down plus `Tubb3`, `Tubb2a`, `Tuba4a`, `Tubb4a`, `Tubb4b`, and `Tubb5` up; `Tubb4a` itself was up, log2FC +0.506, FDR 2.85e-5 | positive control showing the assay can detect tubulin-isotype mRNA compensation, and that `Tubb4a` is expressed enough to move in this cell group |
| `Tuba4a` | 2 | `Tuba4a` down and `Mast1` up; no multi-tubulin induction | alpha-tubulin counterexample; even a structural tubulin paralog can be one- or two-gene sparse |
| `Tbcd` | 12 | strongest calls were `Tuba1a` and `Tuba1b` up, followed by a compact `Nfil3`/`Jun`/synaptic thalamic module | beta-tubulin folding machinery can elicit a modest alpha-tubulin feedback state, but the cofactor response is not a direct beta-tubulin phenocopy |
| `Dctn1` | 75 | broadest microtubule-neighbor response here, dominated by `Insig1`, `Msmo1`, `Hmgcs1`, `Hmgcr`, `Fdft1`, `Sqle`, `Ldlr`, and other sterol/lipid genes | counterexample proving that the focal-cell assay can see a cytoskeleton-linked secondary program, but dynactin/sterol feedback is mechanistically too distant from `Tubb4a` |
| `Map1b`, `Mapt`, `Stmn2`, `Kif5a`, `Kif1a`, `Kif5c`, `Mapre2` | 1 each | each was essentially a self-only or singleton response in the focal group | additional evidence that many postmitotic microtubule-track, MAP, and motor perturbations do not produce a broad nuclear mRNA state |
| `Spast`, `Kif1b`, `Kif2a`, `Kif3b`, `Ttll5`, `Dync2h1`, `Dync2i1` | 0 each | no FDR<0.05 focal-cell genes | same-pathway losses can be fully FDR-null in this endpoint |

I also compared signed top-200 log-fold-change tails among the observed
structural-tubulin and microtubule-neighbor signatures.  Structural tubulins
shared only 13-23 of their top 200 up-regulated genes and 18-47 of their top
200 down-regulated genes, with almost no shared FDR-level non-self genes.
This matched the Distributed Agents corpus claims that represented microtubule and
tubulin-related perturbations generally did not form a coherent shared
postnatal neuronal mRNA module, apart from the restricted `Tuba1a` tubulin
isotype response.

## Biological reasoning for `Tubb4a`

`Tubb4a` encodes a beta-tubulin isotype.  Dominant human `TUBB4A` mutations
cause a tubulinopathy spectrum including H-ABC and dystonia; Simons et al.
2013 mapped the recurrent H-ABC D249N allele to the alpha/beta tubulin dimer
interface, and Krajka et al. 2022 showed that H-ABC- and dystonia-associated
TUBB4A variants have allele-specific effects on microtubule polymerization and
integration.  Sase et al. 2020 showed in a D249N mouse model that mutant
`Tubb4a` can injure both oligodendrocytes and neurons.

Those disease data make `Tubb4a` biologically real, but they do not predict a
broad count here for three reasons.  First, the assay is acute sparse CRISPR
loss-of-function at P16-P37/P44, not expression of a dominant missense tubulin
that poisons heterodimers during development.  Second, the focal readout is
NeuN+ neuronal nuclei and largely excludes oligodendrocytes, a central H-ABC
lineage.  Third, the same-experiment beta-tubulin losses `Tubb4b` and `Tubb5`
were not inert as measured transcripts, yet each produced only one FDR<0.05
gene in this focal group.

The same-experiment evidence was therefore stronger than a generic
"tubulin genes matter" prior.  `Tuba1a` was an important positive control: it
up-regulated `Tubb4a`, `Tubb4b`, `Tubb5`, `Tubb2a`, `Tubb3`, and `Tuba4a`, so
the thalamic glutamatergic nuclei were capable of a tubulin transcript feedback
response.  But the beta-tubulin perturbations on the training side did not
activate that program, and the Distributed Agents corpus specifically records this as a
Tuba1a-specific alpha/beta-tubulin mRNA compensation module rather than a
generic response to direct `Tubb4b` or `Tubb5` perturbation.  `Tbcd` and
`Dctn1` bound the other side: cofactor or dynactin perturbations could be
detectable, but they generated alpha-tubulin or sterol programs rather than a
`Tubb4a`-like beta-tubulin state.

I therefore called `Tubb4a` nonzero, because `Tubb4a` is expressed and
responsive in the focal data and a direct CRISPR target row is likely to pass
FDR, but I kept the count at the one-gene scale of `Tubb4b` and `Tubb5` rather
than expanding it toward `Tuba1a`, `Tbcd`, or `Dctn1`.

## Prediction

`Tubb4a`: predicted `n_degs = 1`.

## Limits and extrapolation

This is an extrapolation from the closest observed beta-tubulin paralogs,
because `Tubb4a` was completely held out and the Distributed Agents same-experiment
corpus had no `Tubb4a` node.  `Tubb4a` is not identical to `Tubb4b` or `Tubb5`,
and subtle isotype-specific effects on microtubule mechanics, protein
stoichiometry, or axonal transport could be invisible to a nuclear RNA
Wilcoxon test.  The estimate also assumes that the `Tubb4a` guides reduce its
own nuclear RNA enough to create a target-row DEG; if the transcript escaped
NMD or was underpowered, the count could be 0, while an unanticipated
Tuba1a-like feedback would move it into the several-gene range.  I judged the
direct beta-tubulin one-gene observations to be the best calibrated evidence
for this specific P16 sparse-loss focal-cell endpoint.
