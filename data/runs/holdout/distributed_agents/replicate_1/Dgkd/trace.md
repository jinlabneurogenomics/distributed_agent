# Dgkd DEG-count prediction for 151 TH Prkcd Grin2c Glut

## Question and endpoint

The task asks for one integer prediction for each gene in the held-out manifest:
the number of measured genes expected to pass BH-adjusted Wilcoxon `pvals_adj <
0.05` after that target is perturbed in `151 TH Prkcd Grin2c Glut` neurons. The
endpoint is the assay-specific DEG count among recovered single nuclei. It is
not viability, raw target engagement, total RNA output, or biological
importance. I treated `151 TH Prkcd Grin2c Glut` literally as the thalamic
glutamatergic class described by the PerturbAI atlas dataset portrait.

The only requested held-out perturbation in
`prepared/manifests/deg-count/the single-target request` was `Dgkd`, and its DEG count and
signature were absent from the supplied training count CSV and DE Parquet.

## Sources used

- Declared direct measurements:
  `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`
  for the observed focal-class `n_degs` of 1,674 non-held-out perturbations.
- Declared direct measurements:
  `training differential-expression dataset`
  for per-gene log2 fold changes and adjusted Wilcoxon p-values in the same
  non-held-out perturbations.
- Run-local requested-target manifest:
  `single-target request for Dgkd`.
- Internal same-experiment interpretation layer:
  `perturbai-july-260713-sourceguard-1773-v1`, queried with the
  `corpus.findings` capability for compact Dgke, Pitpna, Plcb1, Prkcg, and
  Synj1 Findings. These Findings summarize the same Perturb-seq experiment and
  are not independent replication of the Parquet.
- External mechanism priors from PubMed:
  Lu et al. 2018, DOI `10.1016/j.bbrc.2018.02.165`, PMID `29486157`;
  Lu et al. 2019, DOI `10.1016/j.bbalip.2019.158608`, PMID `31891772`;
  Lu et al. 2020, DOI `10.1002/1873-3468.13765`, PMID `32134507`;
  Murakami et al. 2020, DOI `10.1074/jbc.RA119.012369`, PMID `31980461`;
  Epand et al. 2016, DOI `10.3389/fcell.2016.00112`, PMID `27803897`.

## Quantitative calibration over the training inputs

I first used the focal training count table to set the response-breadth scale.
The visible perturbations are mostly transcriptionally quiet in this endpoint:

| quantity | value |
| --- | ---: |
| training targets | 1,674 |
| `n_degs = 0` | 1,205 |
| `n_degs = 1` | 276 |
| median `n_degs` | 0 |
| 75th percentile | 1 |
| 90th percentile | 2 |
| 95th percentile | 18 |
| maximum | 2,677 |

Within the visible target set I then looked for assayed perturbations in the
same enzyme family and in the DAG, phosphoinositide, PLC, PKC, and inositol
signaling neighborhood:

| training target | focal `n_degs` | focal pattern relevant to Dgkd |
| --- | ---: | --- |
| `Dgke` | 1 | only assayed diacylglycerol kinase; its one focal DEG was `Dgke` itself, log2FC -0.586, adjusted p = 5.97e-8 |
| `Plcb1` | 0 | no FDR 0.05 genes in the focal class |
| `Prkca` | 0 | no FDR 0.05 genes in the focal class |
| `Prkcg` | 1 | one focal DEG, `Prkcg` itself, log2FC -0.567, adjusted p = 2.21e-11 |
| `Pik3cb` | 0 | no FDR 0.05 genes in the focal class |
| `Pik3r1` | 0 | no FDR 0.05 genes in the focal class |
| `Pik3r2` | 0 | no FDR 0.05 genes in the focal class |
| `Ppip5k2` | 0 | no FDR 0.05 genes in the focal class |
| `Itpr1` | 0 | minimum focal adjusted p = 0.086 |
| `Pitpna` | 21 | a modest exception in PI-transfer biology, with a secretory/synaptic/microtubule response |
| `Pitpnm3` | 0 | no FDR 0.05 genes in the focal class |
| `Inpp5k` | 0 | no FDR 0.05 genes in the focal class |
| `Synj1` | 1 | one focal DEG, `Synj1` itself, log2FC -0.583, adjusted p = 3.11e-7 |

The Parquet queries used `WHERE group_name = '151 TH Prkcd Grin2c Glut'` and
the target list above, then counted rows with `pvals_adj < 0.05` and inspected
the significant genes per target. I also counted all significant rows across
cell groups for the same set. `Dgke` had only singleton calls in six groups,
whereas `Plcb1`, `Itpr1`, `Prkca`, `Pik3cb`, `Pik3r1`, `Pik3r2`, `Pip5k2`,
`Pitpnm3`, and `Inpp5k` were largely or completely flat in the focal thalamic
class. The modest `Pitpna` signal was therefore not a generic signature of
perturbing any gene near PIP2/DAG turnover.

The internal PerturbAI corpus agreed with these direct counts at the qualitative
level: `Dgke` was annotated as a buffered perturbation with no robust
steady-state neuronal output, the assayed PI-cycle/DAG/PKC neighbors did not
phenocopy it, `Plcb1` had zero robust downstream neuronal genes, `Prkcg` had a
singleton-positive surface with robust self-transcript loss in this focal class
but no downstream FDR<0.10 genes, and `Synj1` had a pan-surface downstream zero.

## Target-specific reasoning

### Dgkd

`Dgkd` encodes DGKdelta, a diacylglycerol kinase that phosphorylates DAG to
phosphatidic acid. External mechanism work supports a real neuronal role for
DGKdelta: brain-specific deficiency increased serotonin transporter protein,
reduced cortical serotonin, and altered tryptophan hydroxylase 2 and monoamine
oxidase A in mouse brain, and follow-up work placed DGKdelta-generated
18:0/22:6 phosphatidic acid upstream of Praja-1-dependent SERT ubiquitination
(Lu et al. 2018, 2019, 2020). That made a strict biological zero less plausible
than for a target with no neuronal prior at all.

I did not transfer a broad transcriptional program from those external brain
studies, however. The SERT/Praja-1 mechanism is protein- and lipid-signaling
centered and was described in whole cortex or biochemical systems rather than
in acute P16 mosaic CRISPR loss in thalamic glutamatergic nuclei 3-4 weeks
later. Murakami et al. 2020 further showed that DGKdelta preferentially uses
palmitic or palmitoleic DAG species and can interact with SMSr through SAM
domains in a pathway independent of canonical phosphatidylinositol turnover.
So the closest causal chain for the Perturb-seq endpoint is:

`Dgkd` CRISPR loss -> lower DGKdelta catalytic/scaffold activity -> altered DAG
species and DGKdelta-associated protein regulation -> possible local
serotonergic or membrane-signaling changes -> only if those changes occur in
recovered `151 TH Prkcd Grin2c Glut` neurons at sufficient strength do they
produce BH-significant nuclear RNA changes.

Several links in that chain are uncertain in the focal experiment. The
strongest within-dataset analog, `Dgke`, is a DGK but is mechanistically
non-identical: DGKepsilon is the constitutively membrane-bound DGK with
18:0/20:4 DAG specificity linked to the phosphatidylinositol cycle (Epand et
al. 2016), whereas DGKdelta has regulatory domains and the SMSr/Praja-1
biology above. Still, `Dgke` is the only visible DGK-family perturbation and it
produced exactly one focal DEG, its own transcript. That is the most endpoint-
matched evidence. The broader DAG/PIP2 pathway counterexamples also point
downward: focal `Plcb1`, `Prkca`, `Pik3cb`, `Pik3r1`, `Pik3r2`, `Itpr1`,
`Ppip5k2`, `Inpp5k`, and `Pitpnm3` were all zero, while `Prkcg` and `Synj1`
were self-transcript-only singletons. `Pitpna` at 21 DEGs is a counterexample
showing that this cell class can report a PI-transfer perturbation, but the
same-experiment corpus notes that measured phosphoinositide-transfer, PLC, and
PKC relatives did not phenocopy `Pitpna`; I therefore treated `Pitpna` as a
specific secretory/PITPalpha response rather than as a reason to inflate all
DAG/PI predictions.

Because `Dgkd` itself is a measured gene in the focal matrix and showed
moderate dynamic range across training perturbations, a one-gene self RNA call
is plausible, analogous to `Dgke`, `Prkcg`, and `Synj1`. Because the assayed
DGK and immediate pathway comparators were otherwise quiet, I predicted no
extra downstream FDR hits. Final point prediction: **1 DEG**.

## Limits

This is a direct prediction of an absent held-out endpoint; there is no
validated quantitative proxy for `Dgkd` itself in the supplied inputs. The
within-dataset anchor is only `Dgke`, and DGKepsilon is not a perfect substitute
for DGKdelta because the two enzymes differ in regulatory domains, acyl-chain
selectivity, localization, and associated pathways. External DGKdelta evidence
establishes neuronal and SERT-related biology, but much of it is protein/lipid
or whole-brain/cortical evidence rather than single-nucleus transcription in
postnatal thalamic glutamatergic neurons. The exact singleton call depends on
guide performance, expression in recovered cells, and FDR power for the Dgkd
self transcript; those are not directly observed for the held-out perturbation.
