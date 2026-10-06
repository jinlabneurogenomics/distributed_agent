# Sec31a DEG-count prediction

## Question and resolved ambiguities

The held-out manifest contains one requested perturbation, `Sec31a`. I treated
the requested endpoint as:

- cell group: `151 TH Prkcd Grin2c Glut`
- count rule: every measured gene with `pvals_adj < 0.05`
- count source for calibration: the supplied
  `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`
- inclusion of the target transcript: included, because the endpoint is a count
  of measured rows and the training CSV includes self-transcript-only cases

The same-experiment Distributed Agents findings usually summarize downstream genes at
FDR < 0.10 and often exclude the self transcript. I used those reports only as
a qualitative semantic layer, and I used the CSV/parquet directly for the
FDR < 0.05 focal-cell counts that define this prediction.

## Sources used

- The requested-target CSV
  `[local file: 205_Sec31a.csv]`.
- The focal training-count CSV
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
- The full differential-expression parquet
  `[local file: training_de_all_cell_groups.parquet]`.
- Distributed Agents same-experiment corpus release
  `perturbai-july-260713-sourceguard-1773-v1`, especially `target_context`
  for `Sec23a`, `Sar1b`, `Tfg`, `Trip11`, `Copg1`, and `Sec63`, plus a
  `candidate_set_topology` audit over the ER-Golgi / ER-stress comparator set.
- Distributed Agents runtime `profile_compare` over `151 TH Prkcd Grin2c Glut`
  `logfoldchanges` for ER-exit, COPI/COG/SNARE, and ER-stress targets.
- PubMed-indexed literature on the COPII coat and on SEC31A loss of function.

## Dataset computations

I first read the training count CSV. It contains 1,674 non-held-out targets in
the focal cell group; 1,205 have `n_degs = 0`, 363 have 1-9 DEGs, 63 have
10-99 DEGs, and 43 have at least 100. The endpoint is therefore strongly
zero-inflated, with a median of 0 and a 75th percentile of 1 DEG.

I then predicate-scanned the parquet for rows with:

```sql
group_name = '151 TH Prkcd Grin2c Glut'
and gene_target in (
  'Sec23a','Sar1b','Tfg','Trip11','Copg1','Copa','Stx5a','Cog4','Cog5',
  'Tmem165','Sec63','Hspa5','Manf','Atf6','Sil1','Ssr4','Bcap31',
  'Gfpt1','Dhdds','Atp2a2'
)
```

For each analog I counted `pvals_adj < 0.05` and inspected the leading rows.
Every focal profile had 17,259 measured genes. `Sec31a` itself is not present
as a `gene_target` in the inputs, as expected for the held-out task.

I also ran a Distributed Agents runtime `profile_compare` on the same focal rows using
`gene_target` as the entity, `names` as features, `logfoldchanges` as the signed
value, and `pvals_adj < 0.05` as the significance gate. This was a check for
whether the nominal signed profile of the null COPII/ER-exit targets resembled
ER-stress positives. It did not nominate a convincing hidden COPII stress
module: all four reviewed nodes, `Sec23a`, `Sar1b`, `Tfg`, and `Trip11`, had
zero significant features, and their leading rows were nonsignificant
low-detection extremes rather than recurrent `Hspa5`/`Chac1`/`Pdia4`/`Ddit3`
UPR genes.

## Sec31a-specific evidence

### Closest available COPII and ER-exit analogs

No perfect Sec13/Sec31 outer-coat perturbation was available in the training
set: `Sec31b`, `Sec13`, `Sec24a`, `Sec24b`, `Sec24c`, and `Sec24d` were absent
as perturbation targets. The nearest measured COPII nodes were therefore the
SAR1/SEC23 branch and an ER-exit scaffold:

| training perturbation | focal `n_degs` | focal expression evidence | interpretation for `Sec31a` |
|---|---:|---|---|
| `Sec23a` | 0 | 307 perturbed vs 23,679 control nuclei; no gene at FDR < 0.05; the `Sec23a` self row was -0.351 log2FC, FDR 0.873 | Direct inner-coat COPII comparator. A SEC23/24 perturbation did not generate an ER-export or UPR survivor state. |
| `Sar1b` | 0 | 112 perturbed nuclei; no gene at FDR < 0.05; the `Sar1b` self row was -0.615 log2FC, FDR 0.108 | Direct COPII initiation comparator. Its null makes a generic SAR1-to-COPII stress signature unlikely in this P16 neuronal assay. |
| `Tfg` | 0 | 118 perturbed nuclei; top focal rows all had FDR 1.0 | ER-exit-site scaffold upstream of COPII carriers; corpus findings report a pan-measured-neuron null and no hidden UPR/ISR/autophagy transcript program. |
| `Trip11` | 0 | 161 perturbed nuclei; top focal rows all had FDR 1.0 | A less direct Golgi tether/cargo-transport counterpoint. It shows that an essential secretory-pathway factor can be silent in recovered postmitotic neuronal nuclei. |

The Distributed Agents corpus connects `Sec23a`, `Sar1b`, and `Tfg` in a shared claim:
perturbing individual represented COPII initiation or ER-exit nodes was
transcriptionally buffered in this neuronal assay, unlike the ER-stress
response elicited by `Sec63`. The `Trip11` report independently placed
`Sec23a`, `Sar1b`, `Copa`, `Copg1`, `Stx5a`, `Cog4`, and `Cog5` in a broader
buffered or near-buffered ER-Golgi region.

### Secretory-pathway boundaries

Other represented ER-Golgi trafficking perturbations were also low:

| training perturbation | focal `n_degs` | relevance |
|---|---:|---|
| `Copa` | 0 | COPI alpha subunit; no focal response. |
| `Copg1` | 1 | COPI gamma subunit; the sole focal hit was the `Copg1` self transcript, not a downstream secretory collapse. |
| `Stx5a` | 0 | ER-Golgi SNARE; no focal response. |
| `Cog4` | 0 | COG tethering complex; no focal response. |
| `Cog5` | 0 | COG tethering complex; no focal response. |
| `Tmem165` | 0 | Golgi calcium/proton transporter and glycosylation-homeostasis gene; no focal response. |
| `Bcap31` | 1 | ER cargo receptor/chaperone-associated membrane protein; self transcript only in the focal group. |
| `Ssr4` | 1 | translocon-associated signal-sequence receptor subunit; self transcript only in the focal group. |

These are not as mechanistically close to `Sec31a` as `Sec23a` or `Sar1b`, but
they argue against a broad rule that acute perturbation of any ER-Golgi traffic
component creates many DEGs in surviving thalamic glutamatergic neurons.

### ER-stress positive controls

The zero calls above are not just a failure of nuclear RNA-seq to detect
ER-stress transcription. Several nearby ER proteostasis perturbations were
clearly nonzero in the same focal cell group:

| training perturbation | focal `n_degs` | leading focal signal |
|---|---:|---|
| `Sec63` | 11 | `Hspa5`, `Canx`, `Hyou1`, `Chac1`, and related ER client-handling genes were up. |
| `Hspa5` | 5 | `Hsp90b1`, `Nfe2l1`, `Pdia4`, and `Derl3` were up despite only 47 perturbed nuclei. |
| `Manf` | 3 | `Hspa5` and `Pdia6` were up, with `Manf` itself down. |
| `Dhdds` | 116 | UPR/ISR-associated genes including `Chac1` and `Shmt2` were induced. |
| `Gfpt1` | 311 | Strong ER/glycosylation stress, with `Herpud1`, `Asns`, `Ddit3`, and `Shmt2` among the top rows. |
| `Atp2a2` | 187 | ER calcium-loss/UPR signature including `Ddit3`, `Chac1`, and `Xbp1`. |

This split is the main calibration point: individual COPII/ER-exit structural
perturbations were silent at FDR < 0.05, whereas ER client folding, calcium,
glycosylation, and dolichol stressors yielded 5-311 focal DEGs.

## External biological rationale

SEC31A is biologically close to the COPII comparators. COPII vesicle budding was
defined as a coat system that drives ER export using Sar1, Sec23/24, and
Sec13/31 components in Barlowe et al. 1994, DOI
10.1016/0092-8674(94)90138-4, PMID 8004676. Yeast Sec31 was cloned as an
essential Sec13-complex component required for ER-derived vesicle budding by
Salama, Chuang and Schekman 1997, DOI 10.1091/mbc.8.2.205, PMID 9190202.
The outer coat can self-assemble as a Sec13/Sec31 cage (Stagg et al. 2006, DOI
10.1038/nature04339, PMID 16407955), and a Sec31 active fragment couples the
Sec13/31 outer coat to Sec23-Sar1 and stimulates Sar1 GTP hydrolysis
(Bi, Mancias and Goldberg 2007, DOI 10.1016/j.devcel.2007.10.006,
PMID 17981133). In mammalian cells, p125A/TANGO1-family machinery interacts
with SEC31A in the Sec13/Sec31A subcomplex and facilitates ER export
(Ong et al. 2010, DOI 10.1083/jcb.201003005, PMID 20679433).

So an unconstrained prior would not call `Sec31a` inert. Strong SEC31A loss can
damage ER homeostasis: recessive human SEC31A null variants cause a severe
neurodevelopmental syndrome, and CRISPR SEC31A-null HEK293T/SH-SY5Y cells show
reduced viability with ER-stress up-regulation (Halperin et al. 2018, DOI
10.1136/jmedgenet-2018-105503, PMID 30464055). A later family/model study
reported that homozygous disruption of the orthologous mouse `Sec31a` region
caused early embryonic lethality (Tobias et al. 2024, DOI
10.1007/s12020-024-03701-x, PMID 38400880).

Those facts are also exactly why the Perturb-seq context matters. This assay is
acute, mosaic, AAV CRISPR delivered at P16, sampled 3-4 weeks later in
postmitotic NeuN-enriched nuclei. The readout is the gene-expression state of
recovered nuclei, not ER-export flux, protein secretion, embryonic viability,
or loss of edited cells before sorting. A complete biallelic `Sec31a` knockout
could be selected out or buffered at the protein/paralog level and leave a quiet
survivor population, as happened for the represented proximal ER-exit targets.

## Prediction

The focal endpoint for `Sec31a` should be closest to the zeros from `Sec23a`,
`Sar1b`, and `Tfg`, with `Trip11` and the COPI/COG/SNARE set serving as broader
supporting nulls. I therefore predict no measured gene, including the `Sec31a`
self transcript, will pass BH FDR 0.05 in `151 TH Prkcd Grin2c Glut`.

`Sec31a` predicted `n_degs`: **0**

## Limits and extrapolations

- There is no exact Sec13/Sec31 or `Sec31b` training analog. Moving from inner
  COPII or ER-exit-site genes to the `Sec31a` outer coat is an extrapolation.
- The corpus reports are internal interpretations of the same Perturb-seq
  experiment. They help select mechanistic comparators but are not independent
  replication of the parquet.
- `Sec31a` may be less redundant than `Sec23a` or `Sar1b`, and full SEC31A
  loss is clearly deleterious in other systems. This is the main argument for a
  nonzero count.
- The focal count includes target self-transcripts. `Copg1`, `Bcap31`, and
  `Ssr4` show that a one-DEG endpoint can be purely an on-target RNA hit. I did
  not add a self-only DEG for `Sec31a` because the closest measured core COPII
  targets, `Sec23a` and `Sar1b`, did not pass FDR even for their own mRNAs.
- The prediction says the recovered neuronal nuclei will be FDR-flat. It does
  not say SEC31A is biologically unimportant, that editing failed, or that ER
  export would be normal in fully null cells.
