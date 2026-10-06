# Reasoning trace

## Question and resolved ambiguities

The requested prediction is the number of measured genes with `pvals_adj < 0.05`
after each held-out perturbation in `151 TH Prkcd Grin2c Glut`.  The held-out
manifest for this run contains one target, `Nr1h3`, and that target is absent
from both the raw differential-expression parquet and the focal-cell training
count CSV.

The Distributed Agents corpus often summarizes signatures at FDR < 0.10 across all 23
groups.  I used those records to identify and interpret LXR/RXR comparators,
but recalculated the endpoint from the parquet at the task cutoff, FDR < 0.05,
only within `151 TH Prkcd Grin2c Glut`.

## Sources used

Same-experiment inputs:

- `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`
  for the observed focal `n_degs` values of non-held-out perturbations.
- `[local file: training_de_all_cell_groups.parquet]`
  for exact focal rows, adjusted p values, log fold changes, and matched
  perturbed/control nucleus counts.
- Distributed Agents corpus release `perturbai-july-260713-sourceguard-1773-v1`,
  especially target contexts and findings for `Nr1h2`, `Rxra`, and `Abca1`.
- Distributed Agents runtime profile comparison artifacts generated in this run:
  `nr1h3_lxr_profile_compare.json` and
  `nr1h3_lxr_profile_inspect.json`.

External biology:

- Venkateswaran et al. 2000, PNAS, DOI `10.1073/pnas.200367697`,
  PMID `11035776`: LXRalpha activation induces `ABCA1` and stimulates
  cholesterol efflux through an LXR transcriptional pathway.
- Repa et al. 2000, Genes & Development, DOI `10.1101/gad.844900`,
  PMID `11090130`: LXRalpha/LXRbeta plus RXR regulate `Srebf1c` as an
  oxysterol-responsive target.
- Laffitte et al. 2001, PNAS, DOI `10.1073/pnas.98.2.507`,
  PMID `11149950`: LXR/RXR heterodimers control lipid-inducible `Apoe`
  expression and coordinate macrophage cholesterol-efflux genes.
- Whitney et al. 2002, Molecular Endocrinology, DOI `10.1210/mend.16.6.0835`,
  PMID `12040022`: both LXR subtypes are present in brain and LXR agonists
  induce cholesterol-homeostasis genes, but primary astrocytes respond much
  more strongly than primary neurons.
- Repa et al. 2007, Journal of Neuroscience, DOI
  `10.1523/JNEUROSCI.4823-07.2007`, PMID `18160655`: LXR activation can
  increase CNS cholesterol efflux and `ABCA1`/`ABCG1` in the NPC1 disease
  context, emphasizing that a challenged glial/sterol state is the setting in
  which this axis is easiest to expose.

## Computational evidence

I read the requested-target CSV and found exactly one row:

| target_name |
| --- |
| `Nr1h3` |

I then filtered the parquet to `group_name == "151 TH Prkcd Grin2c Glut"` and
to LXR/RXR, sterol-homeostasis, and nuclear-receptor-cofactor perturbations
represented in the training table.  For each perturbation I counted rows with
`pvals_adj < 0.05`, confirmed the count against the training `n_degs`, and
inspected canonical LXR/RXR target genes such as `Abca1`, `Abcg1`, `Abcg4`,
`Apoe`, `Insig1`, `Ldlr`, `Hmgcr`, `Hmgcs1`, `Msmo1`, `Cyp51`, `Sqle`,
`Srebf1`, and `Srebf2`.

The focal counts for the informative same-experiment analogs were:

| training perturbation | focal `n_degs` | focal minimum adjusted p value | matched perturbed nuclei | interpretation for `Nr1h3` |
| --- | ---: | ---: | ---: | --- |
| `Nr1h2` | 0 | 1.000 | 200 | Closest LXR paralog, encoding LXRbeta; no canonical LXR or sterol target survived correction. |
| `Rxra` | 0 | 1.000 | 247 | Heterodimer partner for many nuclear receptors including LXRs; no focal response. |
| `Rxrb` | 0 | 0.541 | 249 | RXR paralog; no focal response. |
| `Rxrg` | 0 | 0.437 | 229 | RXR paralog; no focal response. |
| `Abca1` | 0 | 1.000 | 227 | Canonical LXR efflux target; no focal response and no sterol feedback signature. |
| `Srebf1` | 0 | 1.000 | 202 | LXR lipogenic target branch; no focal response. |
| `Abca7` | 0 | 0.334 | 213 | Cholesterol/Alzheimer-related ABC transporter; no focal sterol module. |
| `Nr1h4` | 0 | 1.000 | 185 | FXR, the NR1H-family receptor adjacent to LXRs; flat in the focal group. |
| `Nr1h5` | 0 | 1.000 | 111 | NR1H-family comparator; flat in the focal group. |
| `Ncoa1` | 0 | 0.829 | 189 | Shared nuclear-receptor coactivator; no focal response. |
| `Ncoa3` | 0 | 1.000 | 147 | Shared nuclear-receptor coactivator; no focal response. |
| `Ppara`/`Ppard`/`Pparg` | 0 each | 1.000 each | 109-315 | RXR lipid-receptor comparators; no focal response. |
| `Hmgcr` | 0 | 0.126 | 109 | Cholesterol-synthesis enzyme; no focal FDR < 0.05 gene. |
| `Srebf2` | 7 | 2.70e-27 | 209 | Internal positive contrast: a sterol transcriptional module was detectable when the perturbation engaged one. |

The `Srebf2` counterexample was compact and coherent: the seven focal DEGs were
all down-regulated sterol-biosynthesis genes or `Srebf2` itself
(`Srebf2`, `Dhcr24`, `Insig1`, `Hmgcs1`, `Msmo1`, `Cyp51`, `Sqle`).  This argues
against a blanket claim that the focal assay cannot detect cholesterol-related
RNA programs.

For `Nr1h2`, by contrast, all inspected canonical LXR/RXR genes in the focal
group had `pvals_adj = 1.0`.  `Abca1`, `Abcg1`, `Abcg4`, `Apoe`, sterol
synthesis genes, `Srebf1`, and `Srebf2` therefore gave no sign of tonic LXR
transcriptional control in this cell group.  `Abca1` and `Rxra` showed the same
absence of these transcripts at FDR 0.05.

I also ran `profile_compare` over a 12-target cohort
(`Nr1h2`, `Rxra`, `Rxrb`, `Rxrg`, `Abca1`, `Abca7`, `Srebf1`, `Srebf2`,
`Nr1h4`, `Nr1h5`, `Ncoa1`, `Ncoa3`) with the focal parquet rows.  The runtime
classified 11 of the 12 profiles as `no_significant_features`; only `Srebf2`
was in `1_to_9_significant_features`.  I did not treat whole-vector logFC
similarity among these near-null signatures as a strong mechanistic ranking,
because it was dominated by nonsignificant, low-expression features.  The useful
profile-level evidence was the FDR-level absence of shared LXR/RXR activity.

## Distributed Agents corpus evidence

The same-experiment Distributed Agents corpus independently summarized the broader,
23-group behavior of the closest LXR/RXR comparators:

- `Nr1h2:F001`, high confidence: `Nr1h2` loss had no downstream gene at
  FDR < 0.10 in any measured group.
- `Nr1h2:F002`, high confidence: expected LXR cholesterol-efflux and
  sterol-regulatory transcripts, including the `ABCA1` and `SREBF1` branches,
  were absent from the `Nr1h2` DE surface.
- `Nr1h2:F003`, moderate confidence: represented `Rxra`, `Rxrb`, `Rxrg`,
  `Abca1`, and `Srebf1` perturbations did not uncover a hidden shared LXR/RXR
  module.
- `Rxra:F001`-`F003`: acute neuronal `Rxra` loss was FDR-flat, uncoupled from
  measured RXR paralogs and partner receptors, and did not recover the expected
  LXR/RXR `Apoe`-`Abca1` cholesterol axis in neurons.
- `Abca1:F002`-`F003`: `Abca1` loss did not move measured `Apoe`, `Abcg`,
  LXR/RXR, cholesterol-synthesis, or cholesterol-trafficking transcripts,
  whereas the `Srebf2` comparator demonstrated that sterol feedback can be
  visible in this assay.

Those findings are not independent experiments; they are a curated semantic
layer over the same Perturb-seq atlas.  They were useful because they forced
the analog selection onto the biologically local LXR/RXR pathway and away from
unrelated numeric neighbors of an almost-flat signature.

## Target-specific prediction

### `Nr1h3`

`Nr1h3` encodes LXRalpha.  Its closest assayed paralog is `Nr1h2`/LXRbeta, and
both LXRs act as oxysterol-responsive nuclear receptors that heterodimerize
with RXRs to regulate cholesterol efflux and lipogenesis genes.  The external
prior therefore points to `Nr1h2`, `Rxra`/`Rxrb`/`Rxrg`, `Abca1`, `Srebf1`, and
`Srebf2` as the right same-experiment tests rather than to arbitrary nuclear
receptors.

Every direct negative analog sat at zero in the exact focal endpoint:
`Nr1h2`, all three RXR genes, `Abca1`, `Abca7`, `Srebf1`, NR1H-family
comparators, PPAR/RXR comparators, and p160 coactivators had no FDR < 0.05
gene.  The absence was not restricted to unknown downstream RNAs: focal
`Nr1h2`, `Rxra`, and `Abca1` perturbations did not move `Abca1`, `Abcg1`,
`Abcg4`, `Apoe`, `Srebf1`, `Srebf2`, or the sterol-biosynthesis transcripts.
The closest positive counterexample, `Srebf2`, produced only 7 DEGs and did so
by directly decreasing `Srebf2` and its cholesterol-biosynthesis targets, not by
resembling an upstream LXR/RXR loss.

That pattern fits the literature.  `Nr1h3` is a ligand-regulated sterol sensor,
and the canonical `ABCA1`/`ABCG1`/`APOE` arm is strongest in macrophage,
astrocyte, and challenged lipid states.  Whitney et al. found that murine
primary astrocytes, but not primary neurons, strongly induced LXR targets and
cholesterol efflux after LXR agonism.  This task's cells are recovered,
NeuN-positive juvenile thalamic neurons in an unchallenged basal screen, a
context in which even the broadly expressed `Nr1h2` paralog and `Rxra` partner
were FDR-flat.

I therefore predict no gene will pass BH FDR 0.05 after acute sparse `Nr1h3`
loss in this focal cell group.

Predicted `n_degs`: **0**

## Limits

- The `Nr1h3` expression signature itself was fully held out, so the prediction
  is an extrapolation from `Nr1h2`, RXR, and downstream sterol perturbations.
- `Nr1h2` is the best paralog but not an identical proxy for `Nr1h3`; LXRalpha
  and LXRbeta can differ by tissue, ligand state, and redundancy.
- Single `Rxra`, `Rxrb`, or `Rxrg` perturbations are imperfect complex tests
  because each RXR paralog has multiple non-LXR partners and the experiment did
  not perform combinatorial receptor loss or ligand stimulation.
- The screen is NeuN-enriched and sparse after P16 AAV delivery, so it is
  poorly matched to glial, macrophage, liver, developmental, inflammatory, or
  high-sterol states where LXRalpha biology is well established.
- Low or bursty lipid transcripts can produce large uncorrected log fold
  changes.  I therefore put little weight on raw logFC spikes with
  `pvals_adj = 1.0` and used corrected focal counts as the calibration surface.
