# Direct `n_degs` forecast for `Ptpa`

## Target and endpoint

Target: `Ptpa` in `151 TH Prkcd Grin2c Glut`.

Endpoint: number of measured genes with `pvals_adj < 0.05` in the held-out
`Ptpa` contrast for the thalamic glutamatergic class.

## Evidence used

- The declared biology bundle resolves `Ptpa` to mouse `Ptpra`, receptor-type
  protein tyrosine phosphatase alpha, rather than PP2A PTPA. In the assayed
  non-target nuclei from `151 TH Prkcd Grin2c Glut`, the target feature was
  widely detected: 20,151 of 23,679 non-target cells expressing it, 85.10%
  expressing, mean CP10K 1.423, pseudobulk CPM 142.16, total target UMI 53,710.
- The same bundle identifies the operative biology as active membrane PTPRA
  that activates Src-family kinases, including Src and Fyn. A P16 disruptive
  edit stops new receptor production but existing membrane or trafficking
  receptor protein persists initially; PTPRA can be lysosomally degraded, but
  no target-specific mature-neuron half-life was found, so functional stock by
  P37-P44 remains indeterminate. Germline-null mice show neural phenotypes in
  hippocampus and myelination, but these are developmental and not matched to a
  postnatal thalamic neuron transcriptomic response.
- The declared training count table
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`
  contains 1,674 observed training perturbations and does not contain `Ptpa`.
  The distribution is highly zero-inflated in this class: median 0, mean
  14.05, 1,205 of 1,674 targets at 0, 1,481 of 1,674 at `<= 1`, and 1,546 of
  1,674 at `<= 5`.
- The most relevant measured local perturbations were essentially null in the
  same count table:

  | target | `151` `n_degs` |
  | --- | ---: |
  | `Fyn` | 0 |
  | `Ptpn1` | 0 |
  | `Ptpn11` | 0 |
  | `Ptprc` | 0 |
  | `Ptprd` | 0 |
  | `Ptprf` | 0 |
  | `Ptprm` | 1 |
  | `Ptprn` | 1 |
  | `Ptprn2` | 1 |
  | `Ptpro` | 0 |
  | `Ptprt` | 0 |

- I checked those comparator rows directly in
  `[local file: training_de_all_cell_groups.parquet]`
  with `group_name == "151 TH Prkcd Grin2c Glut"`. `Ptprm`, `Ptprn`, and
  `Ptprn2` each had exactly one significant row, and in all three cases that
  row was the perturbed transcript itself. `Fyn`, `Ptpn1`, `Ptpn11`, `Ptprc`,
  `Ptprd`, `Ptprf`, `Ptpro`, and `Ptprt` had no significant row.
- Packaged same-experiment corpus findings gave the same biological reading:
  `Fyn` was buffered across recovered neuronal groups, `Ptpn11`, `Ptprd`, and
  `Ptprm` were atlas-scale or near-atlas-scale transcriptional nulls, and the
  represented receptor-type PTP perturbations did not form a shared acute
  postnatal neuronal snRNA-seq signature.
- The profile-neighborhood pass
  `workbench/ptpa_pathway_profile_neighbors.json` projected `Fyn`, `Ptpn1`,
  `Ptpn11`, `Ptprd`, `Ptprf`, `Ptprm`, `Ptpro`, and `Ptprt` against all 1,674
  eligible training nodes in the exact `151 TH Prkcd Grin2c Glut` Parquet
  context. Their whole-profile nearest-neighbor correlations were tiny
  (`Fyn` top Pearson 0.089, `Ptpn11` top Pearson 0.079, receptor-PTPs mostly
  below 0.12 except `Ptprd` to `Rora` at 0.169), consistent with isolated
  low-amplitude score vectors rather than a coherent responder module.

## Synthesis

The biology makes `Ptpa` present and potentially edited in the focal cells, but
the expected transcriptomic consequence of losing a membrane PTPRA/Src-Fyn
input in recovered juvenile thalamic neurons is weak: the direct measured Fyn
perturbation was `0`, the direct receptor-PTP comparators were `0` downstream,
and broader PTP pathway nodes were overwhelmingly silent.

The only reason to move above a strict zero forecast is endpoint scale: this
task counts the target transcript itself, and the closest `1`-DEG PTP-family
examples were self-transcript-only detections. Because `Ptpa/Ptpra` was very
widely expressed in the exact non-target population, a single self-feature hit
is more plausible than a multi-gene downstream thalamic response.

Point prediction: `1`.
