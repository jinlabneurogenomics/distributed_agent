# DEG-count prediction trace

## Question and endpoint

The requested prediction is the `151 TH Prkcd Grin2c Glut` held-out DEG count
for each gene in the run-local held-out manifest.  This run contains a single
held-out target:

- `Tubb4a`

I treated the count as the exact assay endpoint defined in the task: the number
of measured genes whose Wilcoxon Benjamini-Hochberg adjusted p value is below
0.05 in the focal thalamic glutamatergic class after acute P16 AAV-CRISPR loss
of function, harvested at P37-P44.  The DEG count includes the perturbed
target's own transcript when it passes the FDR threshold; I did not treat target
RNA reduction as an editing-efficiency estimate.

## Sources used

- Declared focal training counts:
  `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
- Declared full differential-expression table:
  `training differential-expression dataset`.
- Run-local held-out manifest:
  `single-target request for Tubb4a`.
- Run metadata and context:
  `codex_runtime/pipeline/task_bindings.json`,
  `codex_runtime/pipeline/coverage.json`,
  `codex_runtime/pipeline/capabilities.json`, and the PerturbAI atlas dataset
  portrait.
- Same-experiment semantic corpus:
  `perturbai-july-260713-sourceguard-1773-v1`.  The selected corpus had no
  target-scoped Findings/Claims for `Tuba1a`, `Tuba4a`, `Tubb4b`, `Tubb5`, or
  held-out `Tubb4a`; I used only a few report mentions that checked whether
  microtubule comparators generally converged in this screen.
- External literature retrieved from PubMed:
  Vulinovic et al. 2018, DOI `10.1002/humu.23602`, PMID 30079973; Curiel et al.
  2017, DOI `10.1093/hmg/ddx338`, PMID 28973395; Sase et al. 2020, DOI
  `10.7554/eLife.52986`, PMID 32463361; Xiao et al. 2022, DOI
  `10.1007/s12035-022-02900-9`, PMID 35668344; Sase et al. 2026, DOI
  `10.1016/j.ymthe.2026.01.016`, PMID 41566774; Aiken et al. 2017, DOI
  `10.3390/jdb5030008`, PMID 29057214.

## Quantitative calibration

The focal training endpoint has 1,674 non-held-out perturbations.  It is highly
sparse: 1,205 of 1,674 perturbations have `n_degs = 0`; the median is 0, the
75th percentile is 1, the 90th percentile is 2, the 95th percentile is 18, and
the maximum is 2,677.

I used the training count table to find structurally relevant observed
microtubule perturbations, then queried the Parquet at
`group_name = '151 TH Prkcd Grin2c Glut'` for those same perturbations.  The
direct tubulin-subunit analogs had the following focal counts:

| training perturbation | `n_degs` | focal FDR<0.05 expression evidence |
| --- | ---: | --- |
| `Tuba1a` | 7 | Self transcript was down (`Tuba1a` logFC -0.967, FDR 2.8e-20) and several other tubulin isoforms were induced: `Tubb3`, `Tubb2a`, `Tuba4a`, `Tubb4a`, `Tubb4b`, and `Tubb5`. |
| `Tuba4a` | 2 | Mostly self-local: `Tuba4a` was down (logFC -0.710, FDR 2.4e-6) and `Mast1` was the only other FDR<0.05 gene. |
| `Tubb4b` | 1 | Self-transcript-only: `Tubb4b` was down (logFC -0.597, FDR 1.1e-7).  `Tubb4a` moved only +0.178 log2, FDR 1.0. |
| `Tubb5` | 1 | Self-transcript-only: `Tubb5` was down (logFC -1.478, FDR 7.7e-23).  `Tubb4a` moved only +0.108 log2, FDR 1.0. |

More indirect microtubule, motor, or microtubule-associated training
perturbations were also at the flat boundary in the same endpoint:

| class of comparator | observed focal counts |
| --- | --- |
| neuronal microtubule MAP/stathmin genes | `Map1b` 1, `Stmn2` 1, `Mapt` 1, `Map6` 0 |
| kinesins | `Kif1a` 1, `Kif5a` 1, `Kif5c` 1, `Kif3b` 0 |
| intraflagellar/dynein-related controls | `Dync2h1` 0, `Dync2i1` 0 |

The raw-signature check is important because `Tuba1a` shows a small,
interpretable tubulin-compensation program in exactly the requested cell group:
`Tubb4a` itself was one of the transcripts induced after `Tuba1a` perturbation
(logFC +0.506, FDR 2.9e-5).  The two beta-tubulin perturbations did not induce
that program and counted only their self transcripts.  Thus the training data
place beta-tubulin loss near one DEG, not at a broad structural-remodeling
state.

The same-experiment corpus is consistent with this limited transfer.  In the
`Camsap1` report, the represented microtubule comparators `Mapre2`, `Nin`,
`Mapt`, `Tubb4b`, and `Tubb5` were described as transcriptionally mostly flat,
with `Tubb5` showing only isolated one-gene calls; in `Cep85l` and `Dpysl5`
reports, represented tubulin and MAP perturbations did not converge with
centrosome, migration, Reelin, semaphorin, plexin, GSK3B, or Fyn biology.  I
used these as qualitative checks on the Parquet-derived counts, not as
independent replication.

## Target-specific reasoning

### `Tubb4a`

`Tubb4a` encodes the beta-IVa tubulin isotype, a beta-tubulin structural subunit
that enters alpha/beta tubulin heterodimers.  It is mechanistically closer to
the observed beta-tubulin genes `Tubb4b` and `Tubb5` than to upstream
microtubule regulators or motor proteins.  Human TUBB4A variants perturb
microtubule stability, neurite outgrowth, dendritic-spine development, kinesin
binding, and mitochondrial transport in cellular and iPSC-neuron models
(Curiel 2017, PMID 28973395; Vulinovic 2018, PMID 30079973; Xiao 2022, PMID
35668344), and knock-in Tubb4a mutation in mice affects oligodendrocytes and
selected neurons (Sase 2020, PMID 32463361).  Those data establish a real
microtubule function, but most disease alleles are dominant missense alleles
that poison the microtubule lattice; they are not the same perturbation as a
sparse, postmitotic CRISPR loss-of-function allele.  The 2026 Tubb4a
suppression study is a further warning against equating mutant Tubb4a toxicity
with simple loss of the wild-type transcript: reducing Tubb4a improved a D249N
H-ABC mouse model rather than phenocopying the dominant disease allele.

Within the training screen, the two beta-tubulin losses are the best endpoint
analogs and both were almost silent in `151 TH Prkcd Grin2c Glut`: `Tubb4b = 1`
and `Tubb5 = 1`.  Their only FDR<0.05 calls were the targeted transcripts
themselves, and neither induced `Tubb4a` or the `Tuba1a`-like compensatory
isoform set.  That argues that loss of a beta-tubulin isoform is buffered in
these recovered postnatal thalamic nuclei at the mRNA level, with redundancy
across the beta-tubulin pool and with morphology/transport changes, if present,
mostly invisible to a DEG-count endpoint.

`Tuba1a` is the main counterexample.  It is the dominant neuronal alpha-tubulin
gene, and alpha tubulins are the obligatory heterodimer partners of
beta-tubulins; Aiken et al. 2017 summarize why `TUBA1A` is a special,
developmentally prominent neuronal isotype.  In this dataset, `Tuba1a`
knockout produced seven focal DEGs and actively induced beta isoforms including
`Tubb4a`.  I therefore did not predict a hard zero for `Tubb4a`.  However,
`Tuba1a` was a stronger alpha-subunit perturbation with a reciprocal
compensation pattern that was absent from `Tubb4b` and `Tubb5`, so it is an
upper comparator rather than the expected count for `Tubb4a`.

Given those observations, the most likely held-out count is a self-local or
near-self-local response.  I predict one FDR-significant gene: enough for the
target transcript itself or a single immediate compensatory transcript to pass
FDR, but not enough for a broad tubulin, stress, or neuronal remodeling module.

Predicted `n_degs`: **1**.

## Limits

The requested endpoint is directly observed for the beta- and alpha-tubulin
training analogs but is absent for `Tubb4a` itself, so this remains a transfer
prediction.  The Parquet contains differential expression, not raw baseline
expression, protein incorporation into microtubules, neurite morphology,
axon-transport measurements, cell abundance, or allele editing outcomes.
Dominant TUBB4A disease mutations and Tubb4a suppression studies are useful
for identifying mechanism but do not define the same intervention as mosaic
postnatal CRISPR loss of function.  Glial and oligodendrocyte consequences of
Tubb4a perturbation are also largely outside the NeuN-enriched assay.  The main
numeric uncertainty is whether the held-out Tubb4a self transcript would cross
the single-nucleus Wilcoxon FDR threshold; if not, the observed beta-tubulin
analogs make zero plausible, while the `Tuba1a` compensation program makes a
small count of two to seven a less likely upper alternative.
