# Cul3 direct n_degs forecast

Target and endpoint:

- Target: `Cul3`
- Cell group: `151 TH Prkcd Grin2c Glut`
- Endpoint: measured genes with BH-adjusted Wilcoxon `pvals_adj < 0.05`

Declared target biology:

- The focal non-target nuclei express `Cul3` broadly: 21,435 of 23,679 nuclei, or
  90.5%, had detected `Cul3`, with mean raw UMI 2.97 and mean log1p CP10K
  0.953. This supports target reach in the assayed thalamic glutamatergic
  population.
- The perturbation is expected to stop new intact CUL3 production but not
  directly inactivate pre-existing CUL3-containing BTB-CUL3-RBX1 complexes.
  The functional-stock card therefore adjudicated operative CUL3 loss over
  P16 to P37/P44 as `partially_depleted_or_leading_edge`.
- The source facts support a real postnatal neuronal role outside this exact
  thalamic context, but the closest mouse neural deletions were forebrain/PFC
  or striatal, not 21-28 day thalamic perturbations. The bundle contains no
  neuronal CUL3 half-life, and the only turnover measurement is a non-neural
  mpkCCD treatment/control half-life ratio that cannot time protein clearance.

Training endpoint context in the same focal class:

- The declared 151 TH count table has 1,674 training perturbations. Its
  endpoint is extremely sparse: 1,205 targets have 0 DEGs; the median is 0,
  the 75th percentile is 1, the 95th percentile is 18, and the largest tail
  reaches Uba5 at 2,677 DEGs.
- Core proteostasis failures were large in this cell class:
  `Uba5 = 2677`, `Psmb4 = 742`, and `Psmc1 = 430`.
- The closer E3-ligase and CUL3-adaptor side of the training table was much
  weaker: `Huwe1 = 158`, `Arih1 = 7`, `Fbxo11 = 1`, `Kctd1 = 2`, `Kctd16 = 0`,
  `Kctd8 = 0`, `Klhl20 = 0`, `Klhl7 = 0`, and `Ube3a = 0`.
- Other neurodevelopmental but mechanistically different comparators also
  occupied the small-to-moderate range in this class: `Chd8 = 61`,
  `Tsc2 = 86`, `Mecp2 = 16`, `Fmr1 = 0`, and `Pogz = 0`.

Profile/corpus interpretation:

- The matched Parquet slice for the nominated training genes confirmed the
  exact signed burdens: Huwe1 had 158 DEGs, split 90 up and 68 down; Chd8 had
  61; Tsc2 had 86; Kctd1/Fbxo11 had only 1-2; the measured KCTD/KLHL and
  Ube3a nulls were not caused by missing 151 TH rows.
- Same-experiment report context kept `Psmb4` and `Uba5` separate from the
  Cul3 expectation: their reports describe broad proteotoxic and UFMylation
  stress programs rather than an adaptor-specific CUL3-like state.
- Huwe1 was the most informative positive E3-ligase comparator: its report
  describes a visible but selected postmitotic RNA/mitochondrial response and
  explicitly contrasts it with flat represented HECT-family perturbations such
  as Ube3a. That supports treating E3 ligases as heterogeneous rather than
  transferring the proteasome-scale count to Cul3.

Synthesis:

`Cul3` should be more visible than most single BTB/KCTD/F-box adaptor
perturbations because it is a broadly expressed scaffold for multiple
BTB-CUL3 ligases. However, the 21-28 day sparse CRISPR window probably leaves
substantial pre-edit CUL3 capacity, and the measured training analogs show that
postnatal E3-ligase perturbations often stay sparse unless they hit a special
high-response module such as Huwe1. I therefore project a low double-digit
response, above the 95th percentile of all training targets but well below the
Huwe1 positive analog.

Point forecast: 41
