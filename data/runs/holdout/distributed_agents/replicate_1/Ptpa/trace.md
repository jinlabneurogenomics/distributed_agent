# DEG-count prediction trace

## Question and endpoint alignment

The requested endpoint is the count of genes reaching `pvals_adj < 0.05` after
Wilcoxon testing in `151 TH Prkcd Grin2c Glut` cells for each held-out
perturbation. The requested-target manifest contains one target:

- `Ptpa`

`Ptpa` is held out, so neither its focal DEG count nor any of its expression
signature rows are present in the supplied training inputs. The outcome is a
directly observed endpoint for the non-held-out training perturbations in
`151 TH Prkcd Grin2c Glut`, but it is absent for `Ptpa`. I therefore treated
the focal training counts as the quantitative calibration surface and used
within-dataset analogs plus outside PP2A biology to transfer expected response
breadth to `Ptpa`.

I resolved `151 TH Prkcd Grin2c Glut` exactly as the focal thalamic
glutamatergic class described by the dataset portrait. I did not interpret
target-transcript depletion as editing success or failure, because this
postnatal sparse AAV-Cas9 design can create functional indels without large
nuclear mRNA loss and because the requested endpoint is the number of
FDR-significant downstream genes.

## Sources

- Requested-target CSV:
  `single-target request for Ptpa`.
  It supplied the exact ordered target set.
- Training focal DEG-count CSV:
  `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
  This was the direct measurement of `n_degs` for 1,674 non-held-out
  perturbations in the focal cell group.
- Differential-expression Parquet:
  `training differential-expression dataset`.
  I queried it with DuckDB for the focal cell group and PP2A/phosphorylation
  comparators to verify their exact focal rows, FDR minima, significant genes,
  and recovered nucleus counts.
- PerturbAI July same-experiment corpus,
  `perturbai-july-260713-sourceguard-1773-v1`. I used bounded Findings and
  Evidence for the represented PP2A-adjacent perturbations `Ppp2r2b`,
  `Ppp2r5d`, and `Ppm1g`. These reports are packaged interpretations of the
  same experiment, not independent replication.
- NCBI PubMed literature search for PTPA/PPP2R4 and PP2A biogenesis:
  Sents et al. 2012, FEBS J, doi:10.1111/j.1742-4658.2012.08579.x,
  PMID:22443683; Leulliot et al. 2006, Mol Cell,
  doi:10.1016/j.molcel.2006.07.008, PMID:16885030; Magnusdottir et al. 2006,
  J Biol Chem, doi:10.1074/jbc.C600100200, PMID:16782712; Sents et al. 2017,
  Cancer Res, doi:10.1158/0008-5472.CAN-16-2911, PMID:29046336; Fevga et al.
  2023, Brain, doi:10.1093/brain/awac326, PMID:36073231.

## Computation over the training data

I first read the focal DEG-count CSV to calibrate the integer endpoint. The
distribution was extremely sparse:

| quantity | value |
|---|---:|
| training perturbations | 1,674 |
| mean focal `n_degs` | 14.1 |
| median focal `n_degs` | 0 |
| 75th percentile | 1 |
| 90th percentile | 2 |
| 95th percentile | 18 |
| nonzero training perturbations | 469 |

I then searched the training-count target names for phosphatase and PP2A
components. The represented PP2A regulatory genes most closely related to PTPA
biochemistry were `Ppp2r2b` and `Ppp2r5d`; both had `n_degs = 0` at FDR 0.05 in
the focal cell group. `Ppm1g`, a different PP2C-family phosphatase with an
reported interaction with B56delta/PPP2R5D in adherens junctions, had
`n_degs = 3`. Calcineurin-family comparators were only slightly above baseline
(`Ppp3ca = 4`, `Ppp3r1 = 9`, `Ppp3cc = 0`), and generic phosphorylation
downstream nodes were also mostly quiet in the focal endpoint (`Mtor = 2`,
`Rptor = 0`, `Akt3 = 0`, `Gsk3b = 6`, `App = 1`, `Mapt = 1`, `Ptpn11 = 0`,
`Mapk1 = 0`, `Mapk9 = 0`, `Map2k6 = 0`).

For exact expression-pattern evidence I queried the Parquet for
`group_name = '151 TH Prkcd Grin2c Glut'`. The two direct PP2A regulatory
comparators had adequate focal recovery but no FDR-level genes:

| training perturbation | focal perturbed nuclei | focal control nuclei | `n_degs`, FDR 0.05 | minimum focal FDR |
|---|---:|---:|---:|---:|
| `Ppp2r2b` | 151 | 23,679 | 0 | 0.362 |
| `Ppp2r5d` | 141 | 23,679 | 0 | 0.405 |
| `Ppm1g` | 182 | 23,679 | 3 | 0.00539 |
| `Mtor` | 188 | 23,679 | 2 | 0.0185 |
| `Tsc2` | 195 | 23,679 | 86 | 3.29e-6 |
| `Opa1` | 195 | 23,679 | 37 | 2.39e-7 |

The `Ppm1g` focal effect was a tiny, idiosyncratic three-gene module
(`Col4a2` down, `Col4a1` down, `H2ac25` up) rather than a PP2A-regulatory
phenocopy. The strong responses of `Tsc2` and `Opa1` are useful
counterexamples: this assay can see a thalamic transcriptional consequence of
mTOR or mitochondrial-dynamics perturbation when the perturbation produces one,
so the `Ppp2r2b`/`Ppp2r5d` nulls are not explained by universal failure of the
focal cell group to respond to phosphorylation or mitochondrial pathways.

## Target-specific reasoning

### `Ptpa`

`Ptpa` encodes the phosphotyrosyl phosphatase activator of PP2A, also called
PPP2R4 in human literature. Biochemically, PTPA is upstream of individual PP2A
holoenzymes: it binds and activates PP2A catalytic core enzyme, supports
proper C-subunit maturation, and participates with alpha4, LCMT1, PME-1, and
TIPRL1 in PP2A biogenesis and reactivation. That placement makes loss of PTPA
a real PP2A perturbation rather than a remote annotation. Human structural and
biochemical work places a conserved cleft in PTPA at the PP2A-interaction and
activation surface, and the PP2A-biogenesis review by Sents et al. describes
PTPA as one of the dedicated modulators that regulate assembly and activity of
PP2A holoenzymes. In vivo, partial Ppp2r4 loss in mice reduces total PP2A
activity and methylation with selective holoenzyme effects in tumor-prone
tissues, and recessive missense PTPA variants that destabilize the RNA/protein
and impair PP2A activation cause early-onset parkinsonism with intellectual
disability.

The closest same-assay training perturbations point to a much smaller
snRNA-seq response in postnatal recovered neurons than those external
loss-of-function phenotypes might imply:

| comparator | observed focal `n_degs` | expression-pattern evidence | relevance to `Ptpa` |
|---|---:|---|---|
| `Ppp2r2b` | 0 | In the July PerturbAI corpus, `Ppp2r2b` had no downstream FDR<0.10 genes in any of 22 measured neuronal classes. In the focal Parquet rows it had 151 perturbed nuclei, 23,679 controls, 0 genes at FDR<0.05, and no focal row near threshold. | Direct PP2A B55beta regulatory subunit; tests whether losing a neuronal PP2A substrate-targeting branch creates a basal nuclear RNA program. |
| `Ppp2r5d` | 0 | The same-experiment corpus reported only 3 downstream FDR<0.10 genes in all measured groups for B56delta, restricted to `007 L2-3 IT CTX Glut` and `009 L2-3 IT PIR AON ENT Glut`. In the focal class it had 141 perturbed nuclei, 0 genes at FDR<0.05, and minimum FDR 0.405. | Direct PP2A B56 regulatory subunit and a neurodevelopmental PP2A disease gene; it is not a catalytic activator, but it is the closest represented PP2A substrate-targeting knockout. |
| `Ppm1g` | 3 | Three focal genes passed FDR<0.05: `Col4a2`, `Col4a1`, and `H2ac25`; whole-transcriptome neighbors were near the correlation noise floor, and `Ppp2r5d` did not reproduce the thalamic module. | A serine/threonine phosphatase comparator and a counterexample showing that a phosphatase perturbation can produce a small focal response without establishing a broad PP2A transcriptional state. |
| `Tsc2` / `Mtor` / `Akt3` / `Gsk3b` / `Mapt` | 86 / 2 / 0 / 6 / 1 | `Ppp2r5d` did not induce the expected AKT-mTOR/RPS6 or tau/CDK5/GSK3beta nuclear-RNA markers; the mTOR-axis itself was detectable for `Tsc2` but not shared by PP2A regulatory-subunit loss. | PP2A intersects these signaling axes, but pathway membership did not transfer to a common PP2A-like focal DEG burden. |
| `Opa1` / `Mff` / `Dnm1` | 37 / 0 / 1 | `Ppp2r2b` was uncoupled from the broad `Opa1` mitochondrial response and from the flat `Mff`, `Mapt`, `Prkar1a`, and `Dnm1` surfaces in the same-experiment corpus. | B55beta has literature links to Drp1 phosphorylation and mitochondrial fission; the represented perturbations show that this is not a shared basal transcriptome in the screen. |

The intervention-to-readout chain for `Ptpa` is:

`Ptpa` CRISPR loss -> reduced PTPA-dependent PP2A catalytic maturation and
reactivation -> altered activity of only the subset of PP2A holoenzymes whose
turnover is limiting in these postmitotic thalamic cells -> possible changes in
substrate phosphorylation, with most immediate readouts expected at the
phosphoprotein level -> only secondary transcriptional effects in nuclei that
survive, are recovered, and remain assigned to `151 TH Prkcd Grin2c Glut` ->
FDR-thresholded snRNA-seq DEG count.

This causal chain has the same sign as PP2A impairment in the external
PTPA/PPP2R4 literature, but it has several lossy steps before the requested
endpoint. PTPA is a holoenzyme biogenesis factor rather than a sequence-specific
transcriptional regulator. The best represented PP2A regulatory branches did
not show an FDR-supported focal response, and the corpus explicitly rejected a
robust whole-transcriptome neighbor for both `Ppp2r2b` and `Ppp2r5d`
(`Ppp2r2b`'s strongest positive Wilcoxon-score correlations were only about
0.03 and `Ppp2r5d`'s strongest non-safe correlations were about 0.03-0.04).
Those observations make a broad `Ptpa` response less likely than a buffered
or phosphosite-level phenotype.

I considered assigning a tiny nonzero count because PTPA sits upstream of many
PP2A holoenzymes, whereas `Ppp2r2b` and `Ppp2r5d` each perturb one regulatory
arm. I rejected that escalation for the point estimate. The upstream/global
argument is strong for PP2A enzyme activity, but none of the direct focal
training analogs measured a common PP2A transcriptional output; `Ppm1g`'s
three collagen/histone genes are mechanistically distant from PP2A biogenesis;
and pathway neighbors that should capture downstream mTOR, tau, or Drp1 stress
states were either flat or divergent. In an assay where the 75th percentile
training perturbation has only 1 DEG and both focal PP2A B-subunit perturbations
have 0, the best calibrated point prediction for acute postnatal `Ptpa` loss is
therefore:

| target | predicted `n_degs` |
|---|---:|
| `Ptpa` | 0 |

## Limits

The prediction is an extrapolation because the screen did not include `Ptpa`,
PP2A catalytic subunits (`Ppp2ca`, `Ppp2cb`), scaffold subunits (`Ppp2r1a`,
`Ppp2r1b`), LCMT1, PME-1, alpha4, or TIPRL1 as focal training perturbations in
the supplied count table. `Ppp2r2b` and `Ppp2r5d` are direct PP2A regulatory
subunits, but they each perturb one substrate-targeting branch rather than the
PTPA-dependent PP2A activation cycle. The literature evidence comes from
crystallography, cultured cells, cancer-prone mouse tissues, Drosophila
neurons, and recessive human disease; it supports PTPA as an authentic PP2A
activator but does not directly measure nuclear RNA after partial acute CRISPR
loss in juvenile mouse thalamic neurons. A `0` prediction should therefore be
read as "no gene crosses this assay's FDR 0.05 threshold", not as absence of
PTPA protein disruption, PP2A activity changes, phosphorylation changes, or
longer-term phenotypes.
