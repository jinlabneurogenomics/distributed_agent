# Prediction trace

## Question and interpretation

The manifest for this run contains one held-out perturbation, `Adrb1`. I
therefore need to predict one value: the number of measured genes that would
have had `pvals_adj < 0.05` after acute mosaic CRISPR loss of `Adrb1` in
`151 TH Prkcd Grin2c Glut` nuclei.

I treated `n_degs` as the same endpoint used in the supplied focal training CSV:
an integer count of FDR 0.05 Wilcoxon hits in the focal cell group. The target
was held out completely, so there is no `Adrb1` DE profile to correlate against.
The main ambiguity was whether to extrapolate from beta-adrenergic biochemical
signaling to a nonzero CREB-like transcriptional state. I resolved that in favor
of the direct in-assay receptor and proximal cAMP loss-of-function controls,
because this experiment measured a chronic basal snRNA-seq state 3-4 weeks after
partial CRISPR perturbation, not acute agonist-evoked cAMP or phospho-CREB.

## Sources

- Focal DEG-count endpoint:
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
- Per-gene DE profiles:
  `[local file: training_de_all_cell_groups.parquet]`.
- Requested target:
  `[local file: 005_Adrb1.csv]`.
- Distributed Agents same-experiment corpus release
  `perturbai-july-260713-sourceguard-1773-v1`. `Adrb1` itself had no target
  context in this release, but beta-adrenergic/cAMP claims involving measured
  `Adrb2`, `Adrb3`, `Adcy1`, `Adcy3`, `Adcy5`, `Gnas`, `Pde10a`, `Prkaca`,
  `Creb1`, and `Crebbp` were relevant:
  - `claim:d95ecee58b8268b10ac1`: beta-adrenergic receptor and proximal
    cAMP/PKA perturbations were transcriptionally uncoupled from the measurable
    CREB node.
  - `claim:656aceab8249ce38f0c2`: single loss of represented membrane
    adenylyl-cyclase paralogs was buffered at the basal neuronal RNA readout.
  - `claim:5778f7e46773642bd0bd`: represented dopamine/GPCR and cAMP-pathway
    perturbations did not collapse into one shared durable basal neuronal mRNA
    module.
  - `claim:048020ff80dbf39d0ad1`: measured adrenergic receptor perturbations
    showed sparse, subtype-divergent neuronal RNA responses rather than a shared
    adrenergic program.
- Distributed Agents runtime profile comparison over the focal group, written to
  `codex_runtime/adrb1_camp_profile_compare.json` and inspected via
  `codex_runtime/adrb1_camp_profile_inspect.json`.
- External mechanism literature from PubMed:
  - Ali et al. 2020, DOI `10.1007/s10741-019-09825-x`, review: beta-adrenergic
    receptors are GPCRs coupled to Gs, adenylyl cyclase, and cAMP.
  - Wang et al. 2021, DOI `10.1124/molpharm.121.000359`, PMID `34561298`:
    beta1-adrenergic receptors primarily couple to Gs and activate adenylyl
    cyclase/cAMP pathways, with additional beta-arrestin-biased signaling.
  - Kasamatsu and Imamura 2020, DOI `10.1002/cne.25001`, PMID `32737874`,
    review: noradrenergic beta-adrenoceptor signaling can feed through
    cAMP/PKA to CREB in neuronal plasticity contexts.
  - Chai et al. 2014, DOI `10.1038/npp.2014.42`, PMID `24553734`: hippocampal
    norepinephrine effects on long-term extinction memory involved a
    beta-receptor/PKA/CREB pathway.

## Computational checks

The focal count CSV contains 1,674 training perturbations. Its distribution is
very zero-inflated: 1,205 perturbations have `n_degs = 0`, 276 have exactly one
DEG, and only 193 have more than one DEG. That background matters because a
near-zero receptor perturbation should be rounded to exactly zero unless its
closest measured relatives escape the null.

I filtered the parquet to `group_name == "151 TH Prkcd Grin2c Glut"` and a
manually curated adrenergic/cAMP comparator set. The essential operation was:

```python
ds.dataset(parquet, format="parquet").to_table(
    columns=[
        "names", "gene_target", "logfoldchanges", "pvals", "pvals_adj",
        "scores", "n_pert_matched", "n_ctrl_matched",
    ],
    filter=(pc.field("group_name") == focal)
        & pc.field("gene_target").isin(candidates),
)
```

I then counted focal genes with `pvals_adj < 0.05`, checked whether there were
weaker `pvals_adj < 0.10` signals, and inspected the best adjusted p-value per
candidate. Key focal counts were:

| Perturbation | Biological relation to Adrb1 | Focal `n_degs` | Best focal `pvals_adj` | Perturbed cells |
| --- | --- | ---: | ---: | ---: |
| `Adrb2` | beta-adrenergic paralog, Gs/cAMP receptor | 0 | 0.551 | 252 |
| `Adrb3` | beta-adrenergic paralog, Gs/cAMP receptor | 0 | 1.000 | 274 |
| `Adra1a` | other adrenergic GPCR, Gq rather than Gs | 0 | 1.000 | 154 |
| `Adra2a` | other adrenergic GPCR, Gi/o rather than Gs | 0 | 1.000 | 168 |
| `Adra2b` | other adrenergic GPCR, Gi/o rather than Gs | 0 | 1.000 | 196 |
| `Gnas` | canonical Gs-alpha transducer | 0 | 1.000 | 306 |
| `Gnal` | Gs-like Golf transducer | 0 | 1.000 | 148 |
| `Adcy1` | membrane adenylyl cyclase | 0 | 0.139 | 88 |
| `Adcy3` | membrane/ciliary adenylyl cyclase | 0 | 0.112 | 223 |
| `Adcy5` | membrane adenylyl cyclase | 0 | 0.912 | 154 |
| `Pde1c` | cyclic-nucleotide phosphodiesterase | 0 | 0.180 | 155 |
| `Pde4b` | cAMP phosphodiesterase | 0 | 0.922 | 211 |
| `Pde4d` | cAMP phosphodiesterase | 0 | 1.000 | 192 |
| `Pde10a` | striatal cAMP/cGMP phosphodiesterase | 0 | 0.304 | 191 |
| `Rapgef2` | cAMP/Epac-adjacent effector family member | 0 | 1.000 | 113 |
| `Rapgef4` | Epac2 cAMP effector | 0 | 1.000 | 177 |
| `Prkaca` | PKA catalytic subunit | 1 | 7.91e-22 | 192 |
| `Prkar1a` | PKA regulatory subunit | 1 | 1.38e-03 | 98 |
| `Creb1` | direct nuclear CREB transcription factor | 10 | 3.82e-07 | 126 |
| `Crebbp` | CREB/CBP nuclear coactivator | 8 | 5.01e-04 | 61 |
| `Ppargc1a` | CREB/thermogenic transcriptional neighbor | 0 | 0.190 | 135 |
| `Ppara` | thermogenic PPAR comparator | 0 | 1.000 | 158 |
| `Pparg` | thermogenic PPAR comparator | 0 | 1.000 | 109 |

For `Prkaca` and `Prkar1a`, the lone focal DEG was the targeted transcript
itself. In contrast, direct `Creb1` loss gave a small nonzero TH signature headed
by `Crem` up-regulation, and `Crebbp` loss gave eight focal hits. Thus the assay
was capable of registering the downstream nuclear CREB/CBP layer, but the
beta-receptor/Gs/adenylyl-cyclase/PKA source arm was essentially silent.

The runtime profile comparison gave the same interpretation. `Adrb2`, `Adrb3`,
`Gnas`, and `Adcy3` all had `response_activity_status =
no_significant_features`, while `Creb1` had 10 significant focal features.
Among inspected beta/Gs/ADCY/PKA/CREB pairs there were no significant feature
intersections involving `Adrb2`, `Adrb3`, `Gnas`, or `Adcy3`, because these
nodes had no focal FDR hits to share.

## Target-specific reasoning

### Adrb1

`Adrb1` encodes the beta1 adrenergic receptor. External biology puts beta1-AR
next to `Adrb2` and `Adrb3`: beta receptors are catecholamine GPCRs with
canonical coupling through Gs-alpha, adenylyl cyclase, cAMP, and PKA, and
beta-adrenoceptor activity can reach CREB in neurons in ligand- and
activity-dependent settings. Those facts make measured `Adrb2`, `Adrb3`,
`Gnas`, `Adcy1/3/5`, `Prkaca`, and CREB-axis perturbations the right comparator
surface.

The closest same-family perturbations, however, are focal zeroes. `Adrb2` had
0 genes at FDR 0.05 and none at FDR 0.10; its smallest focal adjusted p-value
was 0.551. `Adrb3` was even flatter in this cell group, with all adjusted
p-values equal to 1. The alpha-adrenergic receptors measured in the same focal
endpoint, `Adra1a`, `Adra2a`, and `Adra2b`, were also 0-DEG perturbations, so
the local data do not suggest a general adrenergic receptor loss signature that
would override the beta-paralog evidence.

The downstream cAMP controls are also against a nonzero `Adrb1` call. Direct
loss of the canonical Gs transducer `Gnas` gave 0 DEGs despite 306 matched
perturbed nuclei; `Gnal` was also zero; and the three represented membrane
adenylyl cyclases `Adcy1`, `Adcy3`, and `Adcy5` were all zero. cAMP degradation
and PKA/Epac-adjacent perturbations were similarly absent or target-only in the
focal group: `Pde1c`, `Pde4b`, `Pde4d`, `Pde10a`, `Rapgef2`, and `Rapgef4` were
zero, while `Prkaca` and `Prkar1a` recovered only their own transcripts.
Distributed Agents corpus claims over the same screen extend this beyond the focal table:
the beta-adrenergic/proximal cAMP findings report that `Adrb2` and `Adrb3` were
flat like `Gnas`, `Adcy1`, `Adcy3`, `Adcy5`, and `Prkaca`, while the represented
membrane adenylyl cyclases showed no shared FDR<0.10 module.

The best counterexample is direct perturbation of the CREB/CBP nuclear endpoint,
not another receptor. `Creb1` had 10 focal DEGs, led by `Crem`, and `Crebbp`
had 8. I used those as proof that the screen can detect a small CREB-axis
response in `151 TH Prkcd Grin2c Glut`; I did not use them to assign a positive
count to `Adrb1`, because none of the receptor, G-protein, cyclase, or PKA
perturbations phenocopied that state. Mechanistically, that is plausible for a
basal juvenile snRNA-seq readout because loss of one neuromodulatory receptor
is upstream of ligand availability, receptor subtype redundancy,
compartmentalized cAMP pools, and partial AAV CRISPR editing.

**Prediction:** `Adrb1 = 0` DEGs. This is driven mostly by within-dataset
evidence from the beta paralogs and proximal cAMP controls, with external
knowledge used to choose those controls rather than to force a canonical
CREB-positive extrapolation.

## Limits

- There is no direct `Adrb1` perturbation profile in the parquet or in the
  Distributed Agents corpus. The prediction assumes beta1 loss resembles the measured
  beta2/beta3 and Gs/cAMP source-arm losses more than direct `Creb1` or `Crebbp`
  loss.
- ADRB1 has subtype-specific coupling and expression, so a beta1-only thalamic
  program could be missed by `Adrb2`/`Adrb3` if `Adrb1` is uniquely expressed or
  wired in `151 TH Prkcd Grin2c Glut`.
- The experiment measured basal nuclear RNA weeks after partial CRISPR loss.
  It does not test acute norepinephrine stimulation, cAMP production, PKA
  activity, receptor trafficking, beta-arrestin signaling, or phospho-CREB.
- The endpoint is power- and expression-dependent. A zero prediction means I do
  not expect any measured gene to pass the Wilcoxon FDR 0.05 threshold; it does
  not mean ADRB1 is biologically inert, absent from every profiled nucleus, or
  unsuccessfully edited.
