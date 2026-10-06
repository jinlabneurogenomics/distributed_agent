# Question

The requested held-out target was `Psmc5`. I interpreted the task as a point
prediction of the number of measured genes that would pass BH-adjusted
Wilcoxon `pvals_adj < 0.05` in `151 TH Prkcd Grin2c Glut` nuclei after acute
postnatal mosaic CRISPR loss of `Psmc5`.

Two ambiguities were resolved as follows.

- I treated `n_degs` as an assay- and power-dependent count, not as a direct
  score of proteasome essentiality or editing efficiency.
- I interpreted `151 TH Prkcd Grin2c Glut` as thalamic glutamatergic neurons,
  with `TH` as the atlas anatomic abbreviation, not tyrosine hydroxylase.

# Sources

- Requested-target manifest:
  `[local file: 188_Psmc5.csv]`.
- Focal-cell training endpoint:
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
- Training differential-expression parquet:
  `[local file: training_de_all_cell_groups.parquet]`.
- Distributed Agents same-experiment corpus,
  `perturbai-july-260713-sourceguard-1773-v1`, queried for `Psmc5`, `Psmc1`,
  `Psmb4`, and the induced `Psmc1`/`Psmb4` topology.
- Run-local Distributed Agents observed-profile neighborhood tool, run on log2 fold
  changes in `151 TH Prkcd Grin2c Glut`.
- External literature on the 26S proteasome ATPase ring and PSMC5/Rpt6:
  Forster et al. 2009, DOI `10.1016/j.bbrc.2009.07.145`, PMID `19653995`;
  Bar-Nun and Glickman 2011, DOI `10.1016/j.bbamcr.2011.07.009`, PMID
  `21820014`; Schweitzer et al. 2016, DOI `10.1073/pnas.1608050113`, PMID
  `27342858`; Radhakrishnan et al. 2010, DOI
  `10.1016/j.molcel.2010.02.029`, PMID `20385086`; Djakovic et al. 2012,
  DOI `10.1523/JNEUROSCI.4427-11.2012`, PMID `22496558`; Scudder et al. 2021,
  DOI `10.1523/ENEURO.0073-20.2021`, PMID `33658307`; Kury et al. 2025,
  DOI `10.1038/s41467-025-65556-8`, PMID `41298377`.

# Dataset computations

The manifest contained one row, `Psmc5`. As expected for a held-out target,
`Psmc5` was absent from the training endpoint and from the same-experiment
corpus target index.

I summarized the 1,674 focal-cell training counts. The distribution was very
sparse: mean 14.1, median 0, 75th percentile 1, 90th percentile 2, 95th
percentile 18, 99th percentile about 436, and maximum 2,677. A nonzero
prediction for `Psmc5` therefore needs specific mechanistic support, not just
the default distribution.

I then searched the training endpoint for represented proteasome subunits.
Only two `Psm*` structural proteasome targets were available in the focal
training table:

| training target | focal `n_degs` |
|---|---:|
| `Psmc1` | 430 |
| `Psmb4` | 742 |

I filtered the full DE parquet to
`group_name == "151 TH Prkcd Grin2c Glut"` and
`gene_target in {"Psmc1","Psmb4"}`, giving 17,259 measured genes for each
target. In these focal cells:

- `Psmc1` had 430 FDR 0.05 DEGs: 231 up and 199 down.
- `Psmb4` had 742 FDR 0.05 DEGs: 357 up and 385 down.
- The two signatures overlapped on 215 significant genes, and all 215 changed
  in the same direction.
- Across all 17,259 log-fold-change entries, `Psmc1` and `Psmb4` had Pearson
  correlation 0.611; across Wilcoxon scores the correlation was 0.652.
- Shared focal-cell features had the expected sign: proteasome and
  protein-quality-control transcripts rose (`Psmd1`, `Psmd4`, `Psmc4`,
  `Sqstm1`, `Optn`, `Zfand2a`, `Ddit3`, `Hspb1`), while mature neuronal
  signaling genes fell (`Gria2`, `Atp1a3`, `Syt1`, `Kifc2`, `C1qtnf4`).

I also asked the run-local profile-neighbor tool for unbiased neighbors of
`Psmc1` and `Psmb4` among all 1,674 eligible training targets in this same
cell group. That run confirmed that whole-profile metrics over all genes are
noisy and dominated by shared nonsignificant structure, while signed
top-feature overlap cleanly retrieves the proteasome pair: `Psmb4` was the
rank-1 overlap neighbor of `Psmc1`, and `Psmc1` was the rank-1 overlap neighbor
of `Psmb4`.

# Target-specific reasoning

## `Psmc5`

`Psmc5` encodes Rpt6, one of the six AAA+ ATPase subunits in the 19S
regulatory-particle base of the 26S proteasome. Those six Rpt/PSMC ATPases form
a heterohexamer that opens the 20S core gate, unfolds ubiquitinated substrates,
and translocates them into the 20S catalytic chamber; cryo-EM work places Rpt6
as a structural component of that ATPase ring, and a proteasomal ATPase review
describes the nonredundant division of work among Rpt1-6. This makes held-out
`Psmc5` a direct same-complex analog of training `Psmc1`, another 19S AAA
ATPase, rather than merely a distal ubiquitin-pathway or chaperone gene.

The strongest in-dataset analogs were:

| comparator | observed focal `n_degs` | relevance to `Psmc5` |
|---|---:|---|
| `Psmc1` | 430 | Same 19S AAA-ATPase ring as PSMC5/Rpt6; its perturbation produced proteasome bounce-back, autophagy/lysosome, ISR/heat-shock, redox/apoptosis-risk, and synaptic-withdrawal modules in the Distributed Agents corpus. |
| `Psmb4` | 742 | 20S beta-core structural subunit; less close structurally than `Psmc1`, but an orthogonal proteasome-subcomplex lesion. The corpus reported `Psmc1` as the top `Psmb4` neighbor and `Psmb4` as the only strong positive `Psmc1` neighbor. |

`Psmb4` is not the only stress-like broad target in the training data, but it
is the relevant broad anchor because it damages the constitutive 26S particle
itself. I treated `Uba5` at 2,677 DEGs and `Ufc1` at 572 DEGs as useful
evidence that protein-homeostasis lesions can be very visible in these
thalamic neurons, but not as quantitative PSMC5 analogs: UFMylation intersects
proteostasis downstream and produced a broader signature than the direct
19S/20S proteasome pair. Conversely, `Nfe2l1` 0, `Nfe2l2` 0, `Vcp` 2,
`Hsp90ab1` 1, and `Hspa8` 9 were counterexamples showing that knocking out a
stress regulator, a segregase, or a chaperone under basal juvenile-neuron
conditions does not recapitulate structural proteasome insufficiency. That
same boundary is recorded in the Distributed Agents `Psmb4:F008` and `Psmc1:F008`
findings.

The biological zero/nonzero decision is therefore strongly nonzero. PSMC5/Rpt6
is not an upstream sensor that might be silent until stress is applied; it is
part of the proteolytic machine whose activity is required for ubiquitinated
substrate processing. Proteasome inhibition canonically drives an
NFE2L1/NRF1-mediated compensatory increase in proteasome gene transcription
(Radhakrishnan et al. 2010), and the focal `Psmc1`/`Psmb4` data show that
this feedback plus HSP/ISR, autophagy/lysosome, redox, p53-like and synaptic
downshift arms are in fact recovered by this acute snRNA-seq screen.

For the count, I centered `Psmc5` near the only same-ATPase comparator rather
than near the extreme proteostasis tail. The 19S ATPase `Psmc1` had 430 DEGs;
the 20S core `Psmb4` had a somewhat broader 742-DEG state; all of their 215
shared focal FDR genes were sign-concordant. Rpt6/PSMC5 has well documented
neuronal regulation through CaMKII-dependent S120 phosphorylation, but mouse
phospho-dead/phosphomimetic alleles affected proteasome peptidase/ATPase
activity without recreating a severe basal hippocampal phenotype, so I did not
adjust the prediction upward for a special Rpt6 synaptic role. Human and model
PSMC5 loss-of-function data instead support the broad expectation that PSMC5
impairment reduces proteasome function and creates proteotoxic stress. I
therefore predicted a broad but not maximal focal response, slightly above
`Psmc1` and below `Psmb4`: **520 DEGs**.

# Limits

This prediction is an extrapolation from only two direct structural proteasome
subunits in the training endpoint; no other PSMC, PSMD, PSMA, or PSMB
perturbation was available in `151 TH Prkcd Grin2c Glut`. The numeric
difference between 430 and 742 DEGs could reflect true subunit biology, guide
performance, matched perturbed-nucleus counts, survivor bias, or stochastic
FDR thresholding. The external PSMC5 evidence comes from structural proteasome
work, cultured cells, Drosophila and human neurodevelopmental genetics rather
than the exact acute P16-to-P37/44 mouse thalamic CRISPR context. Finally,
single-nucleus RNA reports a recovered survivor state; it does not directly
measure indels, 26S proteasome activity, protein aggregates, or loss of edited
neurons.
