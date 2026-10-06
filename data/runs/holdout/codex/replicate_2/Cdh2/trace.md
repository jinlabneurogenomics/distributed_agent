# Cdh2 n_degs forecast

## Target and endpoint

- Target: `Cdh2`, from the declared one-row holdout manifest.
- Cell class: `151 TH Prkcd Grin2c Glut`.
- Endpoint: count of measured genes with Wilcoxon BH-adjusted `pvals_adj < 0.05`.
- The declared training count table contains 1,674 focal-class training targets and does not contain `Cdh2`.

## Evidence used

### Biology bundle

The exact focal-population reach for `Cdh2` is high: in non-target nuclei from `151 TH Prkcd Grin2c Glut`, `Cdh2` is expressed in 23,116 of 23,679 nuclei, or 97.62%, with mean log1p CP10K 1.556 and mean raw UMI 7.04. Reach therefore is not the main reason to predict a null.

The functional-stock card points to real postnatal target engagement by harvest, but with delayed structural biology rather than an immediate nuclear regulatory lesion:

- `Cdh2` encodes N-cadherin, an installed calcium-dependent homophilic adhesion protein at neuronal contacts and mature synapses.
- Existing membrane/synaptic N-cadherin complexes would initially persist after genome editing, but the bundle adjudicates the pool as `likely_substantially_depleted` by the P37-P44 harvest because late-postnatal mouse Cdh2 deletion measurably reduces hippocampal N-cadherin by four weeks and the synaptic pool is renewed.
- Late-postnatal loss has selective hippocampal synaptic, plasticity, circuit, and behavioral phenotypes; the bundle did not establish an acute thalamic transcriptional cascade at 21-28 days.
- Cdh4/Cdh6 substitution in vitro leaves unresolved redundancy in the assayed thalamic setting.

### Training target counts

The focal count table is heavily zero-inflated:

- 1,205 / 1,674 targets have `n_degs = 0`.
- 276 have exactly `1`.
- 31 have exactly `2`.
- Only 106 have more than `9`.
- The median among nonzero targets is `1`.

The closest measured membrane, adhesion, and synaptic-organization comparators were flat or nearly flat in the same focal class:

| target | focal `n_degs` | interpretation |
|---|---:|---|
| `Adam10` | 0 | cadherin/neurexin/APP/Notch sheddase; same-experiment report found no downstream FDR response in any recovered group |
| `Dscam` | 0 | surface-recognition molecule |
| `Ptprd` | 0 | synaptic adhesion receptor phosphatase |
| `Ncam1` | 1 | self-transcript only in the parquet slice |
| `Nrxn1` | 1 | self-transcript only |
| `Nrxn2` | 0 | no focal FDR gene |
| `Nrxn3` | 0 | no focal FDR gene |
| `Nlgn3` | 1 | one focal FDR gene |
| `Dlg4` | 1 | self-transcript only |
| `Epha4` | 1 | self-transcript only |
| `App` | 1 | self-transcript only |
| `Shank2` | 0 | no focal FDR gene |
| `Shank3` | 2 | self plus one additional gene |

The physically related catenin/Wnt branch was split. `Ctnnb1` was large at 383 DEGs and `Tcf7l2` at 106, but the same-experiment `Ctnnb1` findings attribute that response to a 151-class beta-catenin/TCF Wnt-feedback and excitability program. More cadherin-adjacent catenins did not reproduce it: `Ctnna2` = 0, `Ctnna3` = 0, and `Ctnnd2` = 1. Upstream Wnt receptors were also mostly small: `Lrp6` = 4, `Gsk3b` = 6, `Lrp5` = 0, and single Frizzled receptors `Fzd2`, `Fzd4`, `Fzd6`, `Fzd9` = 0.

The run-local profile comparison over these 26 adhesion/synapse/catenin/Wnt comparators reinforced that only `Ctnnb1` and `Tcf7l2` formed a high-count transcriptional branch: 14 of the 26 selected comparators had no FDR<0.05 focal features, 10 had one to nine, and only 2 had at least 50.

## Synthesis

`Cdh2` is strongly expressed in the assayed thalamic glutamatergic nuclei and the perturbation should deplete the operative N-cadherin stock by harvest, so I did not treat it as biologically unreachable. I nevertheless project it onto the low end of the training distribution because its closest measured class consists of surface-adhesion and synaptic scaffolding perturbations with zero or self-only DEG counts, while the large `Ctnnb1` response appears to be the beta-catenin/TCF nuclear branch rather than a generic cadherin-adhesion consequence.

The resulting forecast is a near-null focal signature with at most a self or idiosyncratic single-gene call:

`predicted_n_degs = 1`
