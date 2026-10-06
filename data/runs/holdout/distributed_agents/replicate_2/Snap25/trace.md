# Prediction trace

## Question I answered

The held-out target list for this run contains one perturbation, `Snap25`.  I
predicted its `n_degs` in `151 TH Prkcd Grin2c Glut` nuclei, where `n_degs` is
the count of measured genes with Scanpy Wilcoxon Benjamini-Hochberg adjusted
`pvals_adj < 0.05`.

I treated the perturbed gene itself as eligible to contribute to `n_degs`, because
the supplied training DE tables do so: for several training perturbations the
single focal-cell DEG is the target mRNA itself.

## Sources used

- The requested-target manifest:
  `[local file: 216_Snap25.csv]`.
- Focal-cell training endpoint counts:
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
- Full training differential-expression parquet:
  `[local file: training_de_all_cell_groups.parquet]`.
- Distributed Agents same-experiment corpus `perturbai-july-260713-sourceguard-1773-v1`, queried for `Snap25`, `Stx1b`, `Stxbp1`, `Nsf`, and `Unc13a`.
- PubMed literature, queried through NCBI E-utilities, for the SNAP25/SNARE/Munc13/Munc18 mechanism.

External mechanism citations used below:

- Sudhof and Rizo 2011, DOI `10.1101/cshperspect.a005637`, PMID `22026965`.
- Rizo and Xu 2015, DOI `10.1146/annurev-biophys-060414-034057`, PMID `26098518`.
- Wang and Ma 2022, DOI `10.1002/2211-5463.13394`, PMID `35278279`.
- Jiao et al. 2018, DOI `10.7554/eLife.41771`, PMID `30540253`.
- Monteggia et al. 2018, DOI `10.1016/j.neuroscience.2018.08.014`, PMID `30144509`.

## Dataset checks and computations

The focal training-count file has 1,674 non-held-out targets.  Its response
distribution is very sparse in this cell group despite this being a responsive
cell group overall:

- 469 of 1,674 targets have any FDR 0.05 DEG.
- 72.0% of targets have `n_degs = 0`.
- The 75th percentile is `1`, the 90th percentile is `2`, and the 95th percentile
  is `18`; the very large RNA-processing, proteasome, and stress perturbations
  occupy only the extreme tail.

I scanned the DE parquet with DuckDB, filtering to
`group_name = '151 TH Prkcd Grin2c Glut'`.  This slice contains 28,891,566 rows:
1,674 training perturbations times 17,259 measured genes.  `Snap25` was absent
from both the training endpoint and `gene_target`, as expected.

I then pulled the focal counts and focal DE rows for represented presynaptic
release analogs of SNAP25.  The relevant `n_degs` calibration points were:

| training perturbation | focal `n_degs` | relevance to `Snap25` |
| --- | ---: | --- |
| `Stx1b` | 0 | Syntaxin-1 paralog in the core neuronal plasma-membrane SNARE branch. |
| `Vamp1` | 1 | Vesicular R-SNARE; a VAMP2-like synaptobrevin paralog represented in the training set. |
| `Stxbp1` | 1 | Munc18-1, a direct syntaxin/SNARE assembly factor and informative high-sensitivity counterexample. |
| `Cplx1` | 1 | Complexin clamp/regulator of assembled neuronal SNARE complexes. |
| `Cplx2` | 0 | Complexin paralog. |
| `Nsf` | 0 | ATPase that disassembles post-fusion cis-SNARE complexes. |
| `Unc13a` | 0 | Munc13-1, priming factor that opens syntaxin and cooperates with Munc18. |
| `Unc13b` | 0 | Munc13 paralog. |
| `Unc13c` | 0 | Munc13 paralog. |
| `Syt2` | 0 | Synaptotagmin calcium-sensor branch represented in the target set. |
| `Syn1` | 1 | Synaptic vesicle pool regulator. |
| `Syn2` | 0 | Synapsin paralog. |
| `Bsn` | 0 | Active-zone scaffold. |
| `Pclo` | 0 | Active-zone scaffold. |
| `Sv2a` | 1 | Synaptic vesicle glycoprotein. |
| `Syp` | 1 | Abundant synaptic vesicle protein. |
| `Dlg4` | 1 | Postsynaptic scaffold; useful as a synaptic target with only a self mRNA call here. |
| `Nrxn1` | 1 | Synaptic adhesion target with only a self mRNA call here. |

The single-DEG calls in this neighborhood were mostly the target transcript, not
secondary programs:

- `Cplx1`: only `Cplx1` passed FDR, log2FC `-0.863`, `q = 4.29e-24`.
- `Stxbp1`: only `Stxbp1` passed FDR, log2FC `-0.663`, `q = 9.38e-19`.
- `Syn1`: only `Syn1` passed FDR, log2FC `-0.834`, `q = 1.59e-24`.
- `Vamp1`: only `Vamp1` passed FDR, log2FC `-0.465`, `q = 1.87e-3`.
- `Dlg4`: only `Dlg4` passed FDR, log2FC `-0.444`, `q = 1.15e-8`.
- `Nrxn1`: only `Nrxn1` passed FDR, log2FC `-0.518`, `q = 2.67e-23`.

In contrast, same-pathway genes with no focal FDR genes often also failed to
call the self transcript after multiple-testing correction: `Stx1b` had self
log2FC `-0.390`, raw `p = 1.14e-4`, `q = 1`; `Nsf` had self log2FC `-0.389`,
raw `p = 2.37e-3`, `q = 1`; and `Unc13a` had self log2FC `-0.301`, raw
`p = 3.86e-5`, `q = 0.666`.

## Same-experiment corpus evidence

The Distributed Agents corpus had no direct `Snap25` findings, consistent with the
held-out status.  The observed SNARE-cycle findings were still directly relevant:

- `Stx1b:F001` described `Stx1b` as a pan-measured neuronal transcriptomic null,
  with zero downstream genes at FDR 0.10 in every recovered cell group.
- `Stx1b:F003` concluded that `Stx1b` had no meaningful presynaptic-pathway
  neighbor and that most represented SNARE-cycle comparators were
  transcriptionally null or singleton responders.
- `Stxbp1:F009` found that canonical release-machinery perturbations represented
  in the screen, including `Stx1b`, `Vamp1`, `Cplx1`, `Cplx2`, `Unc13a/b/c`,
  `Syt2`, `Cacna1a`, and `Cacna1e`, largely failed to phenocopy `Stxbp1`.
  This makes the broad `Stxbp1` surface a Munc18-specific exception, not a
  generic core-SNARE template.
- `Nsf:F004` similarly found that `Nsf` did not phenocopy `Stxbp1`, AMPAR
  subunit perturbations, or most represented SNARE-cycle perturbations.
- `Unc13a:F002` and `Unc13a:F003` showed that single Munc13-family perturbations
  were almost flat and were not interchangeable transcriptomic phenocopies.

Those same-experiment observations put `Snap25` in a local empirical band of
zero or a single focal-cell DEG, far from the hundreds-to-thousands DEG
perturbations in chromatin, splicing, proteasome, or severe stress pathways.

## Target-specific reasoning for `Snap25`

SNAP25 is one of the two plasma-membrane Q-SNARE contributors to the neuronal
synaptic-vesicle fusion complex: syntaxin-1 and SNAP25 pair with the vesicular
R-SNARE synaptobrevin/VAMP2 to form the four-helix SNARE bundle that drives
fusion.  NSF recycles post-fusion SNARE complexes, while Munc13 and Munc18-1
control priming and the ordered assembly of syntaxin, SNAP25, and
synaptobrevin/VAMP2 (Sudhof and Rizo 2011; Rizo and Xu 2015; Jiao et al. 2018;
Wang and Ma 2022).

On mechanism alone, the closest assayed perturbations are therefore the SNARE
and SNARE-regulating targets `Stx1b`, `Vamp1`, `Stxbp1`, `Nsf`, `Cplx1/2`, and
`Unc13a/b/c`; they are closer than broad synaptic adhesion genes, postsynaptic
receptor genes, endosomal stress genes, or generic vesicle-trafficking targets.
In the focal cell group those close analogs had counts of `0, 1, 1, 0, 1, 0,
0, 0, 0`, respectively.  Their DE rows showed no shared downstream activity
or stress program: when a count was one, the one gene was the directly targeted
mRNA for `Vamp1`, `Stxbp1`, or `Cplx1`.

I used `Stxbp1` as a counterexample but not as the point estimate.  Munc18-1
has direct SNARE templating activity and produced broader responses in other
neuronal classes in this experiment, proving that a presynaptic perturbation can
be nuclear-visible.  But Distributed Agents same-experiment findings showed that the
`Stxbp1` response was not reproduced by loss of canonical SNARE-cycle members.
SNAP25 should be closer to `Stx1b` and `Vamp1`, whose primary outputs are
synaptic vesicle fusion and release probability, than to the non-generic
Munc18-1 transcriptional state.

I therefore predicted no broad secondary homeostatic program in
`151 TH Prkcd Grin2c Glut`.  The only reason to move above zero is the self
transcript: `Snap25` is an abundant core neuronal SNARE and is measured in the
focal DE matrix, and several similarly abundant synaptic targets had a lone
FDR-significant self knockdown in this exact cell group.  That makes `1` a
better point prediction than `0`, but still keeps `Snap25` at the floor of the
response distribution rather than in the `Stxbp1` multi-cell-type exception or
large stress-response tail.

Prediction for `Snap25`: `1`.

## Limits and extrapolation

- The most direct same-complex perturbations, `Snap25`, `Vamp2`, and `Stx1a`,
  were not in the training perturbation set, so the estimate transfers from
  `Stx1b`, `Vamp1`, `Cplx1/2`, `Nsf`, `Stxbp1`, and `Unc13a/b/c`.
- The prediction depends on the held-out guides causing enough `Snap25` mRNA
  depletion for the self row to pass BH correction.  The training set contains
  both outcomes among close genes: `Cplx1`, `Stxbp1`, and `Vamp1` passed by
  self knockdown, while `Stx1b` and `Nsf` did not.
- The assay is sparse, postnatal, mosaic CRISPR snRNA-seq.  It does not measure
  DNA indels, SNAP25 protein, vesicle pools, release probability, or loss of
  rare edited neurons.  A flat or one-gene RNA response is therefore compatible
  with a strong electrophysiological release phenotype.
- Adult or germline SNAP25 biology is not equivalent to P16 acute mosaic loss:
  SNAP25 and synaptobrevin-2 haploinsufficiency in mice can be phenotypically
  mild, implying that partial abundance changes can be buffered at the organism
  level despite the core role of the proteins in release (Monteggia et al. 2018).
