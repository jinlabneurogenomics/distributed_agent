# Question and endpoint

I interpreted the task as a point prediction of `n_degs` for the held-out mouse
perturbation `Pcyt2` in `151 TH Prkcd Grin2c Glut` cells.  `n_degs` is the count
of measured genes with `pvals_adj < 0.05` from the Scanpy Wilcoxon
perturbed-versus-matched-control contrast.  The held-out Pcyt2 rows were absent
from both supplied input tables, so the prediction is extrapolation from visible
training perturbations rather than a re-count of Pcyt2 itself.

The endpoint is directly observed for the non-held-out training genes in
`151 TH Prkcd Grin2c Glut`, through
`151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.  The Parquet expression
signatures are direct same-experiment differential-expression evidence for
training perturbations and context for analog selection.  The same-experiment
PerturbAI July corpus `perturbai-july-260713-sourceguard-1773-v1` was used only
as packaged interpretation of the same experiment, not as independent
replication.

# Sources used

- Training endpoint CSV:
  `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
- Training DE Parquet:
  `training differential-expression dataset`.
- Requested-target manifest:
  `single-target request for Pcyt2`.
- Same-experiment internal corpus:
  `perturbai-july-260713-sourceguard-1773-v1`; I read the compact Finding
  inventory and resolved Evidence/Reference records for `Selenoi`.
- External mechanistic knowledge from PubMed and the packaged Selenoi
  references:
  Bakovic et al. 2007, DOI `10.1139/o07-006`; Fullerton et al. 2007, DOI
  `10.1128/MCB.01527-06`; Fullerton and Bakovic 2010, DOI
  `10.1016/j.metabol.2010.03.022`; Ahmed et al. 2017, DOI
  `10.1093/brain/aww318`; Horibata et al. 2018, DOI `10.1194/jlr.P081620`;
  Avery et al. 2020, DOI `10.1016/j.abb.2020.108444`; Reactome pathways
  `R-HSA-1655829` and `R-HSA-75896` as cited by the packaged July Selenoi
  report.

# Computation over the supplied inputs

The requested manifest has one row:

| target_name |
|---|
| Pcyt2 |

The focal training endpoint has 1,674 visible perturbations.  Its DEG-count
distribution is highly zero-inflated:

| quantity | value |
|---|---:|
| median | 0 |
| 75th percentile | 1 |
| 90th percentile | 2 |
| 95th percentile | 18 |
| mean | 14.1 |
| zeros | 1,205 |
| positive counts | 469 |

I first searched the visible target list for Kennedy-pathway and phospholipid
relatives.  The closest focal endpoint analogs available were:

| training target | pathway relationship to Pcyt2 | observed `n_degs` |
|---|---|---:|
| `Selenoi` | ethanolamine phosphotransferase/EPT1; consumes CDP-ethanolamine downstream of PCYT2 to make PE and plasmenyl-PE | 5 |
| `Agps` | ether-lipid/plasmalogen biosynthesis, upstream of plasmalogen PE species but not the CDP-ethanolamine cytidylyltransferase step | 1 |
| `Far1` | ether-lipid/plasmalogen biosynthesis, still more indirect | 2 |
| `Hmgcr` | cholesterol synthesis, a sterol-feedback comparator rather than a PE enzyme | 0 |
| `Srebf1` | SREBP paralog; weaker sterol-enzyme driver than Srebf2 | 0 |
| `Pld3` | lysosomal phospholipase D; membrane lipid biology but mechanistically distant from PE Kennedy synthesis | 1 |

`Pcyt1a`, `Pcyt1b`, `Etnk1`, `Etnk2`, `Cept1`, `Chpt1`, `Pisd`, `Chka`, and
`Chkb` were not visible training targets in the focal endpoint CSV.

For the focal cell group I queried exact DE rows for the Selenoi-centered
comparators.  The Selenoi focal signature consisted of five genes at FDR 0.05:
`Insig1`, `Msmo1`, `Selenoi`, `Fdft1`, and `Nos1ap`.  `Agps` had only `Dhcr24`
at FDR 0.05, and `Far1` had only `Far1` plus `Tial1` at FDR 0.10.  `Hmgcr` and
`Srebf1` had no focal FDR 0.10 gene.  I also computed signed-score correlations
against the Selenoi vector:

```sql
WITH focal AS (
  SELECT names, gene_target, scores, logfoldchanges, pvals_adj
  FROM read_parquet($parquet)
  WHERE group_name = '151 TH Prkcd Grin2c Glut'
), ref AS (
  SELECT names, scores AS ref_score
  FROM focal
  WHERE gene_target = 'Selenoi'
)
SELECT focal.gene_target,
       corr(focal.scores, ref.ref_score) AS score_corr,
       sum(focal.pvals_adj < 0.05) AS n_degs_fdr05
FROM focal JOIN ref USING (names)
GROUP BY focal.gene_target;
```

The positive Selenoi neighbors in the same cell group had low genome-wide
score correlations but a consistent sterol core: `Mib1` had 27 DEGs and induced
`Insig1`, `Fdft1`, `Dhcr24`, `Msmo1`, `Hmgcs1`, and `Hmgcr`; `Marchf6` had 14
DEGs and induced the same sterol-feedback genes; `Dctn1` had 75 DEGs and
induced sterol genes plus a broader trafficking state; `Rab7` had 501 DEGs and
only a partial sterol overlap within a much broader endolysosomal program.
Those training perturbations explain the Selenoi state but are not dose or
complex analogs of Pcyt2.

# Target-specific reasoning for Pcyt2

## Biological transfer model

`Pcyt2` encodes CTP:phosphoethanolamine cytidylyltransferase, the cytidylyl
transfer step in the CDP-ethanolamine Kennedy pathway.  In mammals this branch
is the major de novo route to ethanolamine phospholipids, including
diacyl-phosphatidylethanolamine and plasmalogen PE species (Bakovic et al.
2007; Pavlovic and Bakovic 2013, DOI `10.3390/ijms14022529`).  Mouse Pcyt2 loss
is not redundant at the organismal level: Fullerton et al. found no viable
`Pcyt2-/-` mice and showed that Pcyt2 heterozygotes had reduced PE biosynthesis
in liver, heart, and brain despite preserved total phospholipid pools
(Fullerton et al. 2007).  In primary hepatocytes, restoring wild-type Pcyt2,
but not a catalytically weakened mutant, normalized PE synthesis and secondary
DAG/TAG changes (Fullerton and Bakovic 2010).

The local causal transfer chain is therefore:

`Pcyt2` CRISPR loss -> less CDP-ethanolamine -> less substrate for terminal
ethanolamine phosphotransferases including SELENOI/EPT1 -> altered ER
PE/plasmenyl-PE and sterol sensing -> compact SREBP/INSIG cholesterol-feedback
transcription in surviving thalamic glutamatergic nuclei -> an FDR-limited DEG
count.

`Selenoi` is the closest measured training perturbation because it catalyzes a
terminal transfer from CDP-ethanolamine to lipid acceptors and SELENOI
deficiency reduces PE/plasmenyl-PE synthesis in mammalian cells.  Human
SELENOI/EPT1 loss causes Kennedy-pathway phospholipid defects and complicated
hereditary spastic paraplegia (Ahmed et al. 2017), patient fibroblasts and
EPT1-knockout HeLa cells show lower PE/plasmenyl-PE species (Horibata et al.
2018), and global Selenoi deletion is usually early embryonic lethal in mouse
(Avery et al. 2020).

The same-experiment Selenoi report showed that its acute neuronal knockout was
detectable but small: in `151 TH Prkcd Grin2c Glut`, Selenoi loss induced
`Insig1`, `Msmo1`, and `Fdft1`, repressed `Nos1ap`, and had the Selenoi
self-transcript as the fifth FDR 0.05 gene.  It did not produce a broad UPR,
ISR, autophagy-lysosome, or redox tail in recovered NeuN-positive nuclei.  That
is important because it makes a large Pcyt2 response unlikely under the same
sparse postnatal CRISPR design even though PE metabolism is essential in full
knockouts.

`Mib1`, `Marchf6`, `Dctn1`, and `Rab7` were useful expression-pattern analogs
only for the sterol module.  Their counts of 27, 14, 75, and 501 define a
possible upper tail for perturbations that converge on `Insig1`/`Msmo1`/`Fdft1`
through ERAD or endolysosomal cholesterol handling, but they are indirect:
`Rab7` in particular also triggered vacuolar/endolysosomal genes, and `Dctn1`
perturbed dynein/dynactin cargo transport.  I therefore did not transfer their
full response breadth to Pcyt2.

The main counterexamples pulled the estimate downward.  `Agps` and `Far1`,
which perturb ether-lipid/plasmalogen synthesis rather than the
CDP-ethanolamine cytidylyltransferase step, had only 1 and 2 FDR 0.05 genes.
Direct `Hmgcr` or `Srebf1` targeting was flat in the focal group, showing that
membership in lipid or sterol metabolism is not sufficient to generate the
Selenoi-like response.

## Final Pcyt2 prediction

I predict a small nonzero Pcyt2 response, `5` DEGs.  The nonzero call is driven
by pathway position: Pcyt2 and Selenoi are in the same limiting
CDP-ethanolamine branch, and Pcyt2 loss should deprive SELENOI/CEPT1 of
CDP-ethanolamine in the same PE-synthetic direction.  The magnitude is anchored
to the measured Selenoi count of 5 rather than to the broader Mib1/Dctn1/Rab7
counts because those neighbors recapitulate only the sterol-feedback component
of Selenoi.  I did not increase the point estimate above Selenoi despite Pcyt2
being upstream and rate-limiting because heterozygous Pcyt2 tissues can
partially maintain phospholipid mass, the experiment uses mosaic acute CRISPR
with incomplete average target-RNA reduction, and the closest visible
ether-lipid comparators were almost silent.

# Limits and extrapolation

This is a close biochemical interpolation, not a direct Pcyt2 measurement.
`Cept1`, `Chpt1`, `Pcyt1a/b`, and `Etnk1/2` were not visible training
perturbations, so the CDP-ethanolamine branch was represented by only one
direct terminal enzyme.  The observed Selenoi DEG count included its own
self-transcript; whether Pcyt2 itself would pass FDR in the held-out contrast is
unknown.  Lipid abundances, PE/plasmenyl-PE pools, editing rates, and
pre-harvest depletion were not measured in the DE Parquet.  Published global or
germline Pcyt2/Selenoi phenotypes establish essential lipid chemistry but are
stronger interventions in different tissues or developmental windows than
3-4 week postnatal mosaic neuronal CRISPR.  The final count should therefore be
read as a small-count estimate on a noisy, power-dependent assay, with zero to
low double digits plausible.
