# Rnf13 held-out `n_degs` forecast

## Target and endpoint

- **Target:** `Rnf13`
- **Cell group:** `151 TH Prkcd Grin2c Glut`
- **Endpoint:** number of measured genes with BH-adjusted Wilcoxon `p < 0.05`
- **Forecast:** `1`

I treated the `151 TH Prkcd Grin2c Glut` count table as the scalar training endpoint and used the training expression Parquet only for observed training perturbations. `Rnf13` is absent from the count table, so no held-out target count or target signature entered the estimate.

## Biology-only target prior

The canonical `Rnf13` bundle supports a real but probably modest perturbation in the assayed thalamic neurons:

- Exact focal-population reach is not limiting: in the non-target nuclei from `151 TH Prkcd Grin2c Glut`, `Rnf13` is detected in `16,324 / 23,679` cells, `68.94%`, with mean CP10K `0.855`.
- Functional stock is expected to be **likely substantially depleted** by the 21 to 28 day post-edit harvest. The target is an actively processed PA-TM-RING E3 ligase with endosomal full-length and cytoplasmic RING-containing pools, so stopping synthesis should deplete much of the pool over this window.
- The strongest loss phenotype is adult hippocampal and synaptic: constitutive `Rnf13` loss affects synaptic-vesicle density, SNARE-complex assembly, and learning behavior. That makes a neuronal consequence plausible but does not prove an acute P16-to-P37/P44 thalamic transcriptional program.
- PA-TM-RING family membership with `Rnf167`, `Rnf128`, and `Rnf130` leaves compensation unresolved; it is not direct evidence of either failure or rescue in this population.

This put the target above a hard assay-failure/null prior, but the operation is a specialized synaptic/endosomal E3 rather than a chromatin, spliceosome, ribosome, or proteasome lesion that usually yields a broad 151 TH response.

## Training count evidence

The focal count table has `1,674` training perturbations. It is very zero-heavy:

| threshold | count | fraction |
|---:|---:|---:|
| `n_degs = 0` | 1,205 | 0.720 |
| `n_degs <= 1` | 1,481 | 0.885 |
| `n_degs <= 2` | 1,512 | 0.903 |
| `n_degs >= 50` | 59 | 0.035 |

Training perturbations closest to the documented `Rnf13` hippocampal SNARE/synaptic-vesicle axis were all quiet or nearly quiet in `151 TH Prkcd Grin2c Glut`:

| training target | `n_degs` |
|---|---:|
| `Ap3b1` | 0 |
| `Cplx1` | 1 |
| `Cplx2` | 0 |
| `Nsf` | 0 |
| `Rab27a` | 0 |
| `Rab3gap1` | 0 |
| `Rab3gap2` | 0 |
| `Stx1b` | 0 |
| `Stx5a` | 0 |
| `Stxbp1` | 1 |
| `Sv2a` | 1 |
| `Syn1` | 1 |
| `Syn2` | 0 |
| `Synj1` | 1 |
| `Syp` | 1 |
| `Syt2` | 0 |
| `Unc13a` | 0 |
| `Unc13b` | 0 |
| `Unc13c` | 0 |
| `Vamp1` | 1 |

The direct `Snapin`/`Snap25` substrate pair and the closest PA-TM-RING family members were not present in the observed training count table, so I did not assign a direct same-family empirical center.

I also checked two broader but biologically adjacent observed perturbations:

| training target | rationale for checking | `n_degs` | interpretation |
|---|---|---:|---|
| `Rab7` | core endolysosomal trafficking GTPase | 501 | broad endosomal failure; upper-context, not RNF13-scale |
| `Huwe1` | broad neuronal E3 ubiquitin ligase | 158 | broad ubiquitin-regulatory lesion; upper-context, not membrane PA-TM-RING-scale |
| `Ube3a` | neuronal E3 ligase | 0 | E3 loss can be transcriptionally silent in this assay |

## Matched Parquet profile check

I compared the exact `151 TH Prkcd Grin2c Glut` expression profiles for `Nsf`, `Stx1b`, `Syt2`, `Vamp1`, `Ube3a`, `Huwe1`, and `Rab7`.

The Parquet-derived significant-feature counts match the count table: `Nsf`, `Stx1b`, `Syt2`, and `Ube3a` had no significant features; `Vamp1` had one; `Huwe1` and `Rab7` were broad with at least 50 significant genes. The low-count synaptic nodes did not share a reproducible significant program. `Huwe1` and `Rab7` shared only a partial high-count state, with `5` positive and `15` negative same-direction significant overlaps but `14` direction conflicts, so I treated them as high upper-context observations rather than as a transferable magnitude for `Rnf13`.

## Synthesis

The exact expression and turnover evidence argue that a successful `Rnf13` edit should remove functional material from many focal neurons, so I did not collapse the forecast to an assay-failure zero. The endpoint-relevant training evidence argues just as strongly against a large footprint: perturbing synaptic-vesicle/SNARE machinery in this same thalamic population almost always gave `0` or `1` DEGs, and broader endosomal/E3 perturbations are not scale-matched.

I therefore placed `Rnf13` at the tiny-response edge of the empirical synaptic distribution and forecast **1 DEG**.
