# Hspd1 direct n_degs forecast

Endpoint: `n_degs` is the count of measured genes in `151 TH Prkcd Grin2c Glut`
with BH-adjusted Wilcoxon `p < 0.05`. The declared manifest contains the single
target `Hspd1`; `Hspd1` is absent from the 1,674-row focal-class training count
table.

## Biology used for Hspd1

- The canonical Hspd1 bundle reports exact in-assay expression in the focal
  non-target population: 13,638 of 23,679 cells expressed `Hspd1`
  (`57.595%`), with `0.9536` mean raw UMI and `0.5866` mean CP10K. So this is
  not a target-presence failure in the assayed thalamic population.
- The target biology is real but delayed. HSPD1/Hsp60 is the ATP-dependent
  mitochondrial chaperonin component that cycles with Hsp10 and imported
  clients, so new supply should matter continuously. However, adult mouse brain
  HSPD1 half-lives are about 25 to 30 days, comparable to the 21 to 28 day
  P16-to-harvest window; the bundle therefore adjudicates the functional stock
  at harvest as `partially_depleted_or_leading_edge`, not cleared.
- Hspd1 haploinsufficiency has postnatal neural relevance through a late,
  progressive mitochondrial motor phenotype, but that evidence comes from a
  lifelong heterozygous model rather than a 3-4 week juvenile thalamic knockout.
  The card did not identify a matched acute timing anchor or a matched
  thalamic-neuron compensation experiment.

## Training scale in the focal class

The focal training count table is strongly zero-inflated:

- 1,205/1,674 training perturbations have `n_degs = 0`.
- Median = 0; 75th percentile = 1; 90th percentile = 2; 95th percentile = 18.
- Only 43/1,674 training perturbations have `n_degs >= 100`.

So the prior for a held-out perturbation in this exact endpoint is near zero
unless the biology points to one of the rare broad-response regimes.

## Training perturbations that set the scale

I used typed analog nomination only to find eligible training perturbations
related to mitochondrial chaperone/proteostasis biology, then interpreted their
actual `151 TH Prkcd Grin2c Glut` counts from the declared table and their
matched profiles from the declared Parquet.

The closest mitochondrial/proteostasis or mitochondrial-import candidates were
quiet:

| target | reason for considering | training `n_degs` |
| --- | --- | ---: |
| `Clpx` | mitochondrial ATP-dependent chaperone/protease axis | 0 |
| `Lonp1` | mitochondrial ATP-dependent chaperone/protease axis | 0 |
| `Clpp` | mitochondrial matrix protease | 0 |
| `Afg3l2` | mitochondrial protease/ortholog-projected HSPD1 complex annotation | 0 |
| `Dld` | Reactome mitochondrial import/protein metabolism | 0 |
| `Aco2` | mitochondrial matrix protein metabolism | 0 |
| `Yme1l1` | mitochondrial protease | 0 |
| `Dnajc19` | mitochondrial inner-membrane chaperone/import machinery | 0 |
| `Prep` | Reactome mitochondrial protein import | 1 |
| `Ndufb8` | Reactome mitochondrial protein import / inner membrane | 1 |
| `Tomm40` | mitochondrial import channel | 1 |

That 11-member mitochondria/proteostasis set has median `0`, mean `0.27`, and
a maximum of `1` DEG. I also kept a broader chaperone/stress boundary:

| target | relationship to Hspd1 biology | training `n_degs` |
| --- | --- | ---: |
| `Hsp90ab1` | cytosolic chaperone, STRING physical edge | 1 |
| `Stub1` | chaperone-linked ubiquitin ligase | 1 |
| `Hspa5` | ER Hsp70 chaperone | 5 |
| `Hspa8` | cytosolic Hsc70/Hsp70 chaperone | 9 |
| `Opa1` | mitochondrial inner-membrane dynamics, broader injury boundary | 37 |

The 15-member chaperone plus mitochondrial cohort, excluding `Opa1`, still had
median `0`, mean `1.27`, and only `Hspa5`/`Hspa8` above one DEG. The `Opa1`
profile is useful as a mitochondrial boundary, but its 37 DEGs come from
inner-membrane dynamics rather than from the HSP60/HSP10 matrix folding cycle,
so I did not treat it as a central scale donor.

## Parquet profile check

I compared 21 eligible analog/boundary profiles in the focal thalamic context
using `gene_target` x measured-gene `logfoldchanges` from
`training_de_all_cell_groups.parquet` with `pvals_adj < 0.05` as the
significance field.

- All 21 supplied profiles were available.
- 11/21 had no significant features, 9/21 had 1-9 significant features, and
  only 1/21 had 10-49 significant features.
- Among the 15 chaperone/mitochondrial candidates, the mean significant-program
  overlap coefficient was `0.0` in both positive and negative directions. Thus
  the low counts are not hiding a recurrent significant module that would argue
  for a larger Hspd1 response.
- The focal chaperone rows from the Parquet matched the declared count table:
  `Clpx = 0`, `Lonp1 = 0`, `Hsp90ab1 = 1`, `Hspa5 = 5`, and `Hspa8 = 9`
  significant features.

## Forecast

The exact Hspd1 focal expression and essential mitochondrial chaperonin biology
argue against a target-absence zero by fiat, but the short survivor-conditioned
window samples only partial HSP60 stock depletion. The closest measured
mitochondrial matrix/proteostasis perturbations were almost all 0, and the
broader chaperone comparators only reached 1-9 DEGs. I therefore placed Hspd1
just above the direct-mitochondrial median and rounded the broadened
chaperone/mitochondrial log-scale center to the nearest integer.

Predicted `n_degs`: **1**.
