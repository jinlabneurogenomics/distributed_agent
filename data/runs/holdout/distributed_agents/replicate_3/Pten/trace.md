# Held-out target

The task is to predict, for each target in
`190_Pten.csv`, the number of genes that would pass `pvals_adj < 0.05` in the
held-out `151 TH Prkcd Grin2c Glut` differential-expression readout.
The manifest contains one target, `Pten`. I treated the endpoint as an
assay-specific count of Wilcoxon/BH-significant measured genes in this one cell
group, not as a direct measure of biological importance or editing success.

The direct `Pten` differential-expression profile was absent by construction,
so the prediction below transfers from focal-cell responses of non-held-out
training perturbations plus external knowledge of PTEN biology.

# Sources used

- Input endpoint file:
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`
- Input DE parquet:
  `[local file: training_de_all_cell_groups.parquet]`
- Held-out manifest:
  `[local file: 190_Pten.csv]`
- Distributed Agents same-experiment corpus,
  `perturbai-july-260713-sourceguard-1773-v1`, especially claims
  `claim:28a4a006d8c87a92df98`,
  `claim:b7b2ba203c83fdb0ed2d`,
  `claim:99f8cf9b444b4d79cbbb`, and
  `claim:02eb96768645a7558896`.
- NCBI PubMed literature searches for PTEN, TSC2/RHEB/mTORC1, neuronal PTEN
  loss, and mTORC1/SREBP biology.

# Dataset calibration

The focal training count table has 1,674 observed perturbations. Counts are
highly zero-inflated:

- median `n_degs`: 0
- 75th percentile: 1
- 90th percentile: 2
- 95th percentile: 18
- 99th percentile: 436
- nonzero perturbations: 469/1,674
- maximum: 2,677

I then scanned the focal-cell rows of the parquet for PTEN/PI3K/mTOR and
nearby counterexample targets and counted `pvals_adj < 0.05`. The relevant
training counts were:

| training perturbation | focal n_degs | use in the Pten prediction |
|---|---:|---|
| `Tsc2` | 86 | Best direct mTORC1-gain analog. Loss of TSC2 releases RHEB/mTORC1, the same effector branch expected after PTEN loss via PI3K/AKT-mediated TSC inhibition. |
| `Depdc5` | 13 | Weaker mTORC1-gain analog through loss of a GATOR1 amino-acid-sensing brake. |
| `Mtor` | 2 | Counterexample, because loss of the positive catalytic node is not the same perturbation direction as `Pten` loss and is nearly flat here. |
| `Rptor` | 0 | Counterexample for the same reason: Raptor loss should reduce mTORC1 rather than phenocopy PTEN loss. |
| `Pik3r1` | 0 | Receptor-proximal/class IA PI3K loss-of-function counterexample. |
| `Pik3cb` | 0 | Receptor-proximal/class IA PI3K loss-of-function counterexample. |
| `Akt3` | 0 | Positive AKT-family loss-of-function counterexample. |
| `Gsk3b` | 6 | AKT downstream branch, but only weakly transcriptional and not a PTEN-like mTORC1-gain analog. |
| `Braf` | 4 | RAS/MAPK counterexample downstream of growth-factor receptors. |
| `Ctnnb1` | 383 | Strong Wnt/beta-catenin response but mechanistically inappropriate for PTEN/mTOR. |
| `Fmr1` | 0 | Translation/synaptic counterexample; did not recover the TSC2 response in this cell group. |
| `Magi2` | 0 | Scaffold-like PTEN-neighborhood candidate that was flat. |

For expression-pattern evidence, I compared signed log-fold-change profiles in
the focal cell group with the Distributed Agents runtime `profile_compare` tool across
the PI3K/mTOR/counterexample cohort and all 1,674 eligible observed
perturbations. The key signal was the significant-gene overlap rather than raw
whole-profile correlation, because whole-profile correlations among nearly flat
profiles were dominated by thousands of nonsignificant genes.

`Tsc2` and `Depdc5` shared 8 significant genes in the same direction:

| gene | `Tsc2` log2FC | `Depdc5` log2FC |
|---|---:|---:|
| `Amy1` | -0.439 | -0.568 |
| `Ldlr` | 1.100 | 1.270 |
| `Msmo1` | 0.602 | 0.699 |
| `Pik3r1` | 0.533 | 0.818 |
| `Pik3r3` | 1.222 | 1.055 |
| `Rnpc3` | -0.256 | -0.409 |
| `Snhg11` | -0.127 | -0.126 |
| `Tubb3` | 0.336 | 0.330 |

The `Tsc2` signature did not overlap the significant `Mtor` or `Braf` calls at
all, overlapped `Gsk3b` by only `Nrbp2`, and had partial but directionally
mixed overlap with the much broader `Ctnnb1` program. The nearest eligible
neighbors of `Tsc2` by whole-profile metrics, such as `Agtrap`, `Esr1`,
`Rnf220`, `Trip11`, and `Sh3kbp1`, had no stronger mechanistic tie to PTEN than
the mTORC1 negative regulators and were therefore not used as primary analogs.

# Same-experiment interpretation

The Distributed Agents corpus summarizes the same matrix as showing that receptor-
proximal PI3K/AKT components and positive mTORC1 components are mostly buffered
or mutually non-phenocopying in basal juvenile neurons, whereas loss of
negative regulators such as `Tsc2` and, more weakly, `Depdc5` can expose an
mTORC1/SREBP-linked sterol transcriptional state. This matches the direct focal
counts:

- `Pik3r1`, `Pik3cb`, and `Akt3` loss each produced 0 DEGs.
- `Mtor` loss produced only 2 and `Rptor` loss produced 0.
- `Depdc5` loss produced 13 DEGs with induced sterol/cholesterol genes.
- `Tsc2` loss produced 86 DEGs and included the same `Ldlr`, `Msmo1`,
  `Pik3r1`, `Pik3r3`, `Snhg11`, and `Tubb3` direction seen after `Depdc5`
  loss.

Those observations argue that simple pathway membership is not enough: the
appropriate transfer is from loss of pathway brakes that should activate
mTORC1, not from loss of AKT, PI3K, mTOR, or Raptor.

# External biological rationale

PTEN is a lipid phosphatase that lowers PIP3 and antagonizes PI3K/PKB-AKT
signaling, so PTEN loss increases AKT-pathway activity
(Stambolic et al., 1998, DOI: 10.1016/S0092-8674(00)81780-8,
PMID: 9778245). The TSC1/TSC2 complex acts as a GAP for RHEB upstream of
mTORC1; loss of TSC2 elevates RHEB-GTP and activates mTORC1
(Inoki et al., 2003, DOI: 10.1101/gad.1110003, PMID: 12869586; Tee et al.,
2003, DOI: 10.1016/S0960-9822(03)00506-2, PMID: 12906785). In mice, neuronal
Pten deletion activates AKT/mTOR/S6K signaling and causes neuronal hypertrophy,
aberrant arborization, seizures, and social-behavior phenotypes; mTOR inhibition
or disruption of mTORC1 suppresses several of those growth phenotypes
(Kwon et al., 2003, DOI: 10.1073/pnas.2132711100, PMID: 14534328; Kwon et al.,
2006, DOI: 10.1016/j.neuron.2006.03.023, PMID: 16675393; Tariq et al., 2022,
DOI: 10.1016/j.celrep.2022.111574, PMID: 36323257). mTORC1 also regulates
SREBP-dependent lipid transcription downstream of PI3K/AKT
(Porstmann et al., 2008, DOI: 10.1016/j.cmet.2008.07.007,
PMID: 18762023), matching the sterol/cholesterol genes observed in the
`Tsc2`/`Depdc5` focal signatures.

These mechanisms make PTEN loss closer to `Tsc2` and `Depdc5` loss than to
`Mtor`, `Rptor`, or `Akt3` loss. I nevertheless discounted below the `Tsc2`
count because PTEN is upstream of TSC2, the assay is acute and sparse in
postmitotic neurons, and the represented growth-factor/PI3K nodes in this
dataset show that this part of the pathway is buffered at the basal nuclear RNA
endpoint.

# Prediction

`Pten`: predicted nonzero. The best same-direction anchor is `Tsc2`
with 86 DEGs; `Depdc5`, a weaker parallel mTORC1 brake, has 13 DEGs and shares
the same sterol subset. Flat `Pik3r1`/`Pik3cb`/`Akt3`/`Rptor` profiles keep the
prediction below a generic "mTOR pathway is huge" value, while the robust
conditional-Pten neuronal literature argues against a strict zero. I predict a
moderate `Tsc2`-like response, approximately three quarters of `Tsc2`.

Point prediction: **64 DEGs**.

# Limits

The evidence is an extrapolation because no `Pten` profile or count appears in
either input. `Tsc2` is downstream of AKT and directly controls RHEB, whereas
PTEN loss requires tonic PI3K/AKT signaling to reach the TSC complex, so the
`Tsc2` count may overestimate PTEN in this assay. Conversely, complete neuronal
Pten deletion has PTEN-specific, sometimes mTOR-independent effects on dendrites
and microtubules, so `Tsc2` may underestimate the eventual biology of a strong
PTEN loss. The training endpoint is a BH-thresholded single-cell nuclear RNA
count and is sensitive to power, mosaic editing, protein half-life, and the
basal state of `151 TH Prkcd Grin2c Glut` neurons; it does not directly read out
mTORC1 phosphorylation, S6 phosphorylation, cell size, or translation.
