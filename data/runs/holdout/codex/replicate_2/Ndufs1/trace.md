# Direct outcome-blind forecast trace

## Target and endpoint

- Target: `Ndufs1`
- Cell class: `151 TH Prkcd Grin2c Glut`
- Endpoint: number of measured genes with BH-adjusted Wilcoxon `p < 0.05` in the held-out Ndufs1 perturbation.
- Forecast: `1`

## Evidence used

### Declared target biology

I used the declared `Ndufs1` biology-only bundle at
`[local file: Ndufs1.json]`
through `distributed_agents_runtime.characterization_bundle(target="Ndufs1", view="biology")`.
This canonical bundle reported:

- NDUFS1 is a stoichiometric core N-module component of installed respiratory
  complex I.
- The exact focal-population expression measurement is available in
  `151 TH Prkcd Grin2c Glut`: 16,609 of 23,679 non-target cells expressed
  Ndufs1, 70.142% expressing, mean raw UMI 1.438, mean log1p CP10K 0.537.
- P16 editing should stop new NDUFS1 supply but leave pre-edit complex I
  initially intact; by the P37-P44 harvest the functional-stock adjudication
  favored only partial or leading-edge depletion.
- No target-specific experiment directly fixes NDUFS1 or complex-I functional
  stock loss in postmitotic mouse neurons over this 21-28 day window.

So the target is genuinely expressed in the focal population and is
biologically important, but the postnatal mosaic CRISPR intervention is not
expected to produce immediate complete loss of every pre-existing complex-I
pool.

### Same-experiment corpus

`distributed_agents_corpus.target_context(target="Ndufs1")` returned no same-release
Findings, Claims, or explicit Finding references for `Ndufs1`, so no packaged
Ndufs1 endpoint measurement or Ndufs1-specific comparator story was available.

I then queried the same-experiment Findings ledger for the closest visible
training perturbations around complex I, especially `Ndufs2`, `Ndufs7`,
`Ndufs8`, `Ndufv1`, and `Ndufv2`. The ledger summaries consistently described
acute NDUF perturbations as almost completely transcriptionally buffered:

- Ndufs2: only 3 downstream genes at FDR < 0.10 across 2 of 22 measured
  neuronal groups, despite significant self-transcript lowering in 6 groups.
- Ndufs8: one downstream FDR < 0.10 gene across 23 groups.
- Ndufv1: 0 downstream FDR < 0.10 genes in all 22 groups.
- Ndufs7 and Ndufv2: isolated single downstream events.
- These core N-module or adjacent complex-I perturbations did not induce a
  canonical mitochondrial ISR, UPRmt, redox, mitophagy, or OXPHOS-compensation
  transcriptome and did not phenocopy one another as a recurrent expression
  module.

These same-experiment reports were used as interpreted context for the
training measurements, not as independent replication.

### Visible `151 TH Prkcd Grin2c Glut` counts

The visible count table,
`[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`,
contains 1,674 training perturbations and omits `Ndufs1`. It is heavily sparse
in this cell class: 1,205/1,674 training targets have `n_degs = 0`; the median
is 0, the 75th percentile is 1, and the 90th percentile is 2.

The most direct complex-I cohort also lies at the null/singleton boundary:

| cohort | visible genes | mean `n_degs` | median `n_degs` |
| --- | ---: | ---: | ---: |
| N-module core relatives `Ndufs2,Ndufs7,Ndufs8,Ndufv1,Ndufv2` | 5 | 0.600 | 1 |
| Complex-I structural NDUF genes | 20 | 0.550 | 1 |
| Complex-I NDUF genes plus assembly factors | 23 | 0.478 | 0 |

The 23-gene complex-I plus assembly-factor vector in this exact class was:

`Ndufa10=1, Ndufa11=0, Ndufa12=0, Ndufa4=1, Ndufa6=1, Ndufa8=0, Ndufa9=0, Ndufaf2=0, Ndufaf4=0, Ndufaf5=0, Ndufb10=1, Ndufb11=1, Ndufb3=0, Ndufb7=0, Ndufb8=1, Ndufb9=1, Ndufc2=1, Ndufs2=1, Ndufs4=0, Ndufs7=0, Ndufs8=1, Ndufv1=0, Ndufv2=1`.

### Visible Parquet rows for NDUF genes

I inspected the declared Parquet at
`[local file: training_de_all_cell_groups.parquet]`
for the same 23 NDUF perturbations in `151 TH Prkcd Grin2c Glut`, limited to
significant rows or their self-target rows. The one-count NDUF cases were
mostly just self-transcript calls:

- significant self only: `Ndufa10`, `Ndufa4`, `Ndufa6`, `Ndufb10`,
  `Ndufb11`, `Ndufb8`, `Ndufb9`, `Ndufc2`, `Ndufs2`, `Ndufs8`
- one non-self singleton: `Ndufv2` up-regulated `Cdc40`
- no multi-gene downstream program was present in this focal class for any of
  the 23 visible NDUF targets

Across all neuronal groups represented by these 23 NDUF targets, significant
events remained dominated by self-transcript rows. In `151 TH Prkcd Grin2c
Glut` specifically there were 11 significant rows: 10 self rows and 1 trans
row.

## Synthesis

Ndufs1 is a strong direct biological match to the visible NDUF structural
subunits, especially the N-module genes `Ndufs2`, `Ndufs7`, `Ndufs8`,
`Ndufv1`, and `Ndufv2`. Those training perturbations are the appropriate
quantitative anchor because they impair the same installed complex-I machine in
the same postnatal mosaic Perturb-seq assay. Broader mitochondrial stress
targets are less specific and include phenotypes that NDUF subunit loss did not
reach in the atlas.

The expected Ndufs1 signature is therefore not a broad OXPHOS stress response.
The corpus and Parquet both show that acute complex-I subunit loss in recovered
neurons was transcriptionally buffered and usually yielded zero or one
significant row in `151 TH Prkcd Grin2c Glut`. The exact expression measurement
makes the Ndufs1 transcript observable in this focal population, which nudges
the singleton rather than complete-null side, but the functional-stock card
keeps the forecast near the direct-comparator mean rather than at a stress-like
multi-gene response.

I therefore forecast a single FDR-significant measured gene for held-out
`Ndufs1`: `predicted_n_degs = 1`.
