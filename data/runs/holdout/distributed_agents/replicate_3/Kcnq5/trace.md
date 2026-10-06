# Reasoning trace

## Question and endpoint

I interpreted the task as a scalar prediction for the held-out perturbation in
`151 TH Prkcd Grin2c Glut`: the number of rows in the focal cell group with
`pvals_adj < 0.05` after CRISPR loss of each requested target.  This count
includes the perturbed transcript itself when the self mRNA row is significant;
it is not restricted to secondary downstream genes.  The only requested
held-out target in `118_Kcnq5.csv` was:

```tsv
target_name
Kcnq5
```

I treated `0` as "no measured gene, including the target transcript, crosses
BH-adjusted Wilcoxon FDR 0.05" and positive counts as assay-specific
FDR-significant transcript rows in the focal cell group.  I did not treat a
weak or absent self-mRNA log fold change as failed editing, because this AAV
CRISPR screen reports modest average RNA decreases and does not measure DNA
indels.

## Sources used

Same-experiment data:

- `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`
  for the observed `n_degs` distribution and for focal-cell counts of all
  represented analog perturbations.
- `[local file: training_de_all_cell_groups.parquet]`
  for the actual focal-cell DE rows, effect directions, adjusted p values, and
  matched perturbed/control nucleus counts for KCNQ and other channel
  perturbations.
- Distributed Agents same-experiment corpus
  `perturbai-july-260713-sourceguard-1773-v1`, queried through
  `mcp__distributed_agents_corpus`, for curated Kcnq2/Kcnq3/Kcnq1 perturbation
  interpretation in this Perturb-seq screen.
- Distributed Agents runtime `profile_compare`/`profile_inspect`, queried over the focal
  rows, to verify that the nominated Kv7 and broader channel analogs do not
  share a hidden high-dimensional expression module in `151 TH Prkcd Grin2c
  Glut`.

External mechanism evidence:

- Lerche et al., 2000, Journal of Biological Chemistry,
  DOI `10.1074/jbc.M002378200`, PMID `10787416`: KCNQ5/Kv7.5 forms
  slowly activating M-current-like potassium channels and coexpression with
  KCNQ3 increases currents, indicating functional KCNQ3/KCNQ5 heteromers.
- Schroeder et al., 2000, Journal of Biological Chemistry,
  DOI `10.1074/jbc.M003245200`, PMID `10816588`: KCNQ5 is expressed in brain,
  overlaps with KCNQ2/KCNQ3, forms heteromeric channels with KCNQ3, and is
  inhibited by M1 muscarinic receptor activation like neuronal M-current.
- Jensen et al., 2005, Molecular Brain Research,
  DOI `10.1016/j.molbrainres.2005.05.007`, PMID `15963599`: cloned mouse
  KCNQ5 is a voltage-dependent M-current-like channel, is activated by
  retigabine and blocked by linopirdine/XE-991, and is broadly expressed in the
  mouse nervous system.
- Wei et al., 2022, Journal of Neurophysiology,
  DOI `10.1152/jn.00509.2021`, PMID `35583973`: human KCNQ5 de novo variants
  include gain- and loss-of-function alleles associated with epilepsy and
  intellectual disability; germline Kcnq5 loss-of-function mouse lines show
  handling/thermal induced seizures and abnormal cortical EEGs.

## Computational checks on the supplied data

I loaded the requested-target CSV and the focal training-count CSV.  The focal
training endpoint has 1,674 non-held-out targets.  It is highly zero-inflated:
1,205 targets have `n_degs = 0`, 363 have 1-9, 63 have 10-89, and only 43 have
100 or more.

I then filtered the parquet to:

- `group_name == "151 TH Prkcd Grin2c Glut"`
- represented channel and nearby synaptic controls:
  `Kcnq1`, `Kcnq2`, `Kcnq3`, the represented voltage-gated and
  calcium/sodium-activated potassium channels, represented neuronal sodium
  channels, `Cacna1g`, `Grin1`, `Grin2a`, `Grin2b`, and `Tsc2`

Each represented focal profile contained 17,259 measured genes.  The key
observations at `pvals_adj < 0.05` were:

| target | focal `n_degs` | significant focal rows relevant to interpretation |
|---|---:|---|
| `Kcnq1` | 0 | none |
| `Kcnq2` | 1 | `Kcnq2` self, logFC -0.776, FDR `2.12e-28`; the best downstream row, `Agap2`, was just above the endpoint at FDR 0.0509 |
| `Kcnq3` | 1 | `Kcnq3` self, logFC -0.379, FDR 0.00717 |
| `Kcnab2` | 1 | `Kcnab2` self only |
| `Kcnc2` | 1 | `Kcnc2` self only |
| `Kcnc3` | 1 | `Kcnc3` self only |
| `Kcnma1` | 1 | `Kcnma1` self only |
| `Kcna1`, `Kcna2`, `Kcnb1`, `Kcnb2`, `Kcnd3`, `Kcnh1`, `Kcnh5`, `Kcnj6`, `Kcnn2`, `Kcnn3`, `Kcnt1`, `Kcnt2` | 0 | none |
| `Scn1a` | 1 | `Scn1a` self only |
| `Scn1b` | 2 | `Scn1b` self plus `Jun` up |
| `Scn2a` | 1 | `Scn2a` self only |
| `Scn8a` | 1 | `Scn8a` self only |
| `Cacna1g` | 12 | a real but still small thalamic channel response including `Cacna1g` self, `Ptprn`, `Stmn4`, `Cpne7`, `Jun`, `Ly6e`, and related rows |
| `Grin1` | 89 | a much broader thalamic NMDAR response |
| `Grin2a` | 1 | `Grin2a` self only |
| `Grin2b` | 2 | `Grin2b` self plus `Pianp` |
| `Tsc2` | 86 | a broad PI3K/mTOR-related transcriptional state, used as a non-channel positive control |

The profile comparison over the focal rows used signed Wilcoxon `scores`,
`pvals_adj < 0.05` as the significance threshold, and a handpicked channel
cohort.  It found no shared FDR-significant features between `Kcnq2` or
`Kcnq3` and the broader potassium/sodium-channel peers.  `Kcnq2` and `Kcnq3`
themselves were only weak whole-profile neighbors in this cell type
(`pearson = 0.0409`, `cosine = 0.0444`), despite being the closest Kv7 pair in
the represented training data.  `Cacna1g` was the only small nonzero channel
counterexample with more than a self hit, and it did not share its significant
features with `Kcnq2` or `Kcnq3`.

Finally, I checked `Kcnq5` as a measured gene in these focal profiles.  `Kcnq5`
was present among the measured rows but was not a significant downstream row
for any inspected channel control; for example its adjusted p value was 1.0
under `Kcnq2`, `Kcnq3`, `Cacna1g`, and `Grin1` perturbation.  This argues
against a recurrent within-dataset Kcnq5-compensation module.

## Target-specific reasoning

### Kcnq5

Relevant same-assay analogs:

- `Kcnq2`, focal `n_degs = 1`: the best biological analog among represented
  perturbations.  Kv7.2 is one of the canonical neuronal M-current subunits.
  In the focal cell group the only counted DEG was the self transcript
  (`Kcnq2`, logFC -0.776, FDR `2.12e-28`); its leading downstream candidate
  `Agap2` was subthreshold for this endpoint at FDR 0.0509.  This is the
  cleanest evidence that a neuronal Kv7-channel perturbation can be detected
  in this group without producing a downstream transcriptome.
- `Kcnq3`, focal `n_degs = 1`: KCNQ3/Kv7.3 is the direct heteromerization
  partner for both KCNQ2 and KCNQ5.  It again produced only a self-transcript
  focal hit (`Kcnq3`, logFC -0.379, FDR 0.00717), not a broader activity,
  stress, heat-shock, or channel-compensation signature.
- `Kcnq1`, focal `n_degs = 0`: a Kv7 family member, but less appropriate than
  `Kcnq2`/`Kcnq3` because KCNQ1 is primarily the cardiac/epithelial Kv7
  member.  It provides a lower bound showing that Kcnq paralogy alone is not
  sufficient for a neuronal self or downstream hit.
- Other represented potassium channels in the focal group are mostly 0 or 1:
  `Kcna1 = 0`, `Kcna2 = 0`, `Kcnb1 = 0`, `Kcnb2 = 0`, `Kcnh5 = 0`,
  `Kcnn2 = 0`, `Kcnn3 = 0`, `Kcnt1 = 0`, `Kcnt2 = 0`; `Kcnab2`,
  `Kcnc2`, `Kcnc3`, and `Kcnma1` each have exactly one, in every case the
  target transcript itself.  These are not direct Kv7 analogs, but they are
  useful counterexamples to any rule that ion-channel disease genes should
  induce a stable secondary RNA response in this assay.
- `Scn1a = 1`, `Scn2a = 1`, `Scn8a = 1`, and `Grin2a = 1` are similar
  one-DEG channel/receptor self-hit comparators.  `Scn1b = 2` and
  `Grin2b = 2` show that an occasional second downstream gene can appear, but
  the neighborhood is still in the 1-2 row stratum.
- `Cacna1g = 12` is the strongest local counterexample among intrinsic
  excitability genes.  It proves that this thalamic group can mount a small
  transcriptional response to an ion-channel perturbation, but its calcium
  channel signature did not match `Kcnq2`/`Kcnq3`.  I therefore used it as an
  upper counterexample rather than as the point estimate.
- `Grin1 = 89` and `Tsc2 = 86` show that broad thalamic responses are
  available in this same cell group, but they are mechanistically too far:
  NMDAR core loss and mTOR-pathway loss do not justify assigning Kv7.5 to the
  80-90 DEG tier.

The curated Distributed Agents corpus agrees with this direct readout.  It has no
Kcnq5 perturbation context, as expected for a held-out target, but it
summarizes Kcnq2/Kcnq3/Kcnq1/Akap9 observations from the same experiment as:
"Represented Kv7-family channel perturbations produce sparse, paralog-specific
neuronal transcriptional outputs rather than a shared Kcnq1/Kcnq2/Kcnq3
response program."  The Kcnq2 report specifically notes an `Agap2` up row in
`151 TH Prkcd Grin2c Glut` at FDR 0.0509 and contrasts it with oppositely
directed proteasome/RNA-processing states; because the held-out endpoint is
FDR 0.05, that candidate is not counted.  The Kcnq3 report emphasizes that
even Kcnq3, the expected Kcnq2 channel partner, did not phenocopy Kcnq2.

External biology makes `Kcnq2` and `Kcnq3` the correct training anchors for
`Kcnq5`: KCNQ5 forms M-current-like channels, is expressed in brain, is
modulated by M-current blockers/openers, and can assemble with KCNQ3
(Lerche et al. 2000; Schroeder et al. 2000; Jensen et al. 2005).  Wei et al.
2022 shows that KCNQ5 loss of function can be pathogenic in vivo, because
Kcnq5 loss-of-function mice have inducible seizures and epileptiform cortical
EEGs.  That disease evidence supports a real neuronal excitability role but
does not imply a broad resting nuclear RNA signature in sparse P16 CRISPR
mutants: the nearest same-assay Kv7 losses already show that M-current biology
is mostly buffered at the snRNA level in recovered postmitotic neurons.

I therefore predicted that `Kcnq5` will behave like `Kcnq2`/`Kcnq3` rather
than like `Cacna1g` or `Grin1`: one focal significant row at most, most likely
the `Kcnq5` self transcript if Kv7.5 is expressed and edited strongly enough
in this thalamic group, and no reproducible downstream rows.  The point
prediction is:

```tsv
target_name	predicted_n_degs
Kcnq5	1
```

## Limits and extrapolation

- The dominant uncertainty is the `Kcnq5` self row.  `Kcnq2` and `Kcnq3`
  provide one-DEG self-hit precedents, but the held-out data are required to
  know whether `Kcnq5` transcript abundance in `151 TH Prkcd Grin2c Glut` is
  high enough for an FDR-significant on-target decrease.
- `Kcnq5` was absent as a perturbation target from both the parquet and the
  Distributed Agents corpus.  The estimate is therefore a transfer from Kcnq2/Kcnq3 and
  not a direct measurement of Kv7.5 loss.
- The same-experiment profile correlations among weak channel perturbations
  are close to zero because the vectors are dominated by null rows.  I used
  those correlations only to reject broad shared modules, not to rank subtle
  M-current biology.
- KCNQ5 physiology is electrophysiological.  The snRNA-seq endpoint misses
  current amplitude, action-potential threshold, channel localization,
  network synchrony, and survival/depletion before nuclei were recovered.
- Germline or dense Kcnq5 knockout mouse phenotypes and human KCNQ5 epilepsy
  alleles are imperfect analogs for acute, mosaic, sparse P16 AAV CRISPR loss
  in already specified mouse neurons.
