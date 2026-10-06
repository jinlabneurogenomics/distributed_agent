# Chp1 direct n_degs forecast

## Target and endpoint

Target: `Chp1` in `151 TH Prkcd Grin2c Glut`.

Endpoint: `n_degs`, the count of measured genes in that focal class with
BH-adjusted Wilcoxon `p < 0.05`.

The held-out `Chp1` differential-expression profile and its target DEG count
were not used. Training outcomes came from the declared
`151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`; profile-level checks used
the declared `training_de_all_cell_groups.parquet`, filtered to
`group_name == "151 TH Prkcd Grin2c Glut"`.

## Chp1 biology used

The declared Chp1 biology bundle supports observability but not an expectation
of a broad nuclear stress program:

- In the focal non-target nuclei, `Chp1` was measured in
  15,491 / 23,679 cells, or 65.4%, with mean raw UMI 1.21 and mean
  log1p-CP10K 0.473. This means the target is present in a substantial
  fraction of the assayed population.
- CHP1 is an EF-hand cofactor for plasma-membrane Na+/H+ exchangers, especially
  NHE1/SLC9A1, and supports NHE1 maturation, membrane localization, stability,
  and activity.
- Functional stock was adjudicated as
  `partially_depleted_or_leading_edge`: NHE1 carrier turnover on an
  approximately one-day proxy scale makes loss of renewable CHP1-supported
  exchanger complexes plausible across the 21-28 day edit-to-harvest interval,
  but pre-edit CHP1/NHE complexes initially persist.
- The mouse vacillator Chp1 hypomorph has postnatal Purkinje-cell axon
  pathology, so the gene is not biologically inert in neurons. Transfer to
  acute P16 thalamic editing is limited because that phenotype was congenital,
  cerebellar, and cell-type selective.
- CHP3/TESC can restore much NHE1 in some postnatal brain neurons but not in
  all vulnerable terminals; thalamic buffering is therefore unresolved rather
  than confidently absent.

## Task-matched training measurements

The focal training count table is sparse and heavily right-tailed:

- 1,205 / 1,674 training targets had `n_degs = 0`.
- Median `n_degs` was 0.
- 90th percentile was 2.
- 95th percentile was 18.
- Mean was 14.05 because a small upper tail reached 2,677.

The directly named NHE1/CHP comparators `Slc9a1`, `Chp2`, and `Tesc` were not
present in the training count table. Among the closest available families:

| target | rationale | training `n_degs` |
|---|---:|---:|
| `Slc9a7` | represented Na+/H+ exchanger relative | 1 |
| `Slc9a9` | represented Na+/H+ exchanger relative | 0 |
| `Atp6v0a1` | acidification/V-ATPase context | 1 |
| `Atp6ap2` | V-ATPase accessory context | 2 |
| `Calm1` | EF-hand calcium sensor | 14 |
| `Calm2` | EF-hand calcium sensor | 0 |
| `Calm3` | EF-hand calcium sensor | 1 |
| `Atp2b1` | plasma-membrane calcium extrusion | 22 |
| `Vps35` | selective retromer trafficking | 17 |
| `Vps54` | GARP trafficking | 31 |
| `Atp1a3` | direct neuronal Na/K-pump loss | 80 |
| `Atp2a2` | direct ER-calcium pump loss | 187 |
| `Rab7` | late-endosomal/lysosomal trafficking | 501 |

The 24 hand-picked ion, NHE, endosomal, retromer/AP, and EF-hand analogs had a
median of 1 DEG. Ten of the 24 had zero significant focal features, seven had
1-9, four had 10-49, and only `Atp1a3`, `Atp2a2`, and `Rab7` had at least 50.

## Same-experiment corpus and profile interpretation

Packaged same-experiment findings around the training comparators supported a
low projection for Chp1:

- `Slc9a7` had no downstream FDR<0.10 response across 20 measured neuronal
  groups in its report, and its comparison finding stated that obvious
  acidification relatives, including `Slc9a9`, `Atp6v0a1`, `Atp6v1a`,
  `Atp6v1b2`, `Atp6v1e1`, `Clcn3`, and `Clcn4`, were flat, sparse, or
  non-convergent. This made NHE/acidification membership weak evidence for a
  broad snRNA-seq response.
- `Atp2a2` and `Atp1a3` were genuine high-response ion-homeostasis examples,
  but the reports attributed them to a direct SERCA2 ER-stress/UPR state and a
  distinct Na/K-pump thalamic excitability state. Those mechanisms are more
  acute and more globally coupled to ionic gradients than CHP1 loss.
- `Rab7` produced the strongest endolysosomal stress example, including
  lysosomal, sterol, ISR/UPR, amino-acid, autophagy, redox, and proteasome
  transcripts. That broad state looked like a proximal late-endosomal block,
  not a natural scale projection for an NHE1 maturation cofactor buffered by
  paralogy.
- `Vps35` produced only a sharply restricted 151 TH program despite being a
  core trafficking gene; other retromer/WASH/Retriever and AP-complex
  neighbors were mostly flat.

The profile comparison over the 24 selected training analogs agreed with this
boundary. The focal NHE-family analogs were quiet (`Slc9a9`, 0; `Slc9a7`, 1),
and their FDR-significant overlap with stronger candidates such as `Vps35`,
`Vps54`, `Atp2b1`, `Calm1`, `Atp2a2`, and `Rab7` was effectively absent in
the inspected pairs. Thus the large-count analogs were treated as upper-scale
counterexamples, not as pooled neighbors for Chp1.

## Synthesis

I forecast a sparse but detectable endpoint rather than a hard zero. Chp1 has
measurable focal expression and a plausible 21-28 day route to partial loss of
CHP1-dependent exchanger capacity, so the biology bundle modestly lifts the
forecast above the global zero median. But its closest measured acidification
and NHE-family training analogs were 0-1 DEG, EF-hand paralog-like comparators
were mostly 0-1 with one modest `Calm1` exception, and the large ion-pump or
Rab7 profiles corresponded to direct ER/Na/K/lysosomal stress mechanisms.

The point estimate is therefore the median of the selected mechanistic analog
cohort:

`predicted_n_degs = 1`
