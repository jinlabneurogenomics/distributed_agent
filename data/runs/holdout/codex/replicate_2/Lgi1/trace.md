# Lgi1 n_degs forecast for 151 TH Prkcd Grin2c Glut

## Target and endpoint

- Target: `Lgi1`.
- Cell class: `151 TH Prkcd Grin2c Glut`.
- Endpoint: count of measured genes with BH-adjusted Wilcoxon `pvals_adj < 0.05` in the focal class.
- Prediction: `1`.

## Evidence used

### Exact focal expression and Lgi1 biology

- The declared canonical Lgi1 biology bundle reports exact in-assay baseline reach in the focal class: 10,872 of 23,679 non-target nuclei expressed `Lgi1` (`45.91410110224249%`), with mean `log1p(CP10K) = 0.321783558053142`, pseudobulk CPM `50.27858786948288`, and feature availability marked present.
- Functional-stock adjudication favored substantial loss by harvest: a P16 disruptive edit should stop new LGI1 secretion in successfully edited cells, and 21-28 days is long relative to the 2-5 day synaptic-protein turnover proxy.
- That stock inference was only partial. Existing secreted or receptor-bound LGI1 is not directly inactivated, target-specific extracellular residence was unresolved, and unedited neighboring cells can still supply LGI1.
- The closest severe postnatal mouse evidence is not a matched short-window thalamic transcriptional phenotype. Conditional deletion in forebrain glutamatergic neurons caused seizures with a months-long onset after deletion beginning around 5 weeks, whereas this experiment perturbs sparse P16 thalamic neurons and reads survivor-conditioned nuclear RNA at P37-P44.

### Focal-class training counts

I treated the supplied focal count table as the direct training endpoint. It contains 1,674 observed training targets after Lgi1 was held out.

- Median `n_degs`: 0.
- 75th percentile: 1.
- 90th percentile: 2.
- 95th percentile: 18.
- Nonzero targets: 469 / 1,674.
- Targets with at least 10 DEGs: 106 / 1,674.

The table therefore strongly favors 0-1 DEG for targets without clear evidence for a nuclear transcriptional state.

### LGI1-complex and synaptic comparators in the same focal class

I used named training perturbations that either sit in the LGI1/ADAM22/ADAM23 synaptic complex or perturb nearby excitatory-synapse machinery:

| target | focal `n_degs` | interpretation |
| --- | ---: | --- |
| `Adam22` | 1 | direct receptor-complex partner available in training |
| `Cacng2` | 0 | AMPAR auxiliary/trafficking partner near the postsynaptic side |
| `Dlg4` | 1 | postsynaptic AMPAR scaffold |
| `Gria1` | 0 | AMPAR subunit |
| `Gria2` | 0 | AMPAR subunit |
| `Kcna1` | 0 | Kv channel component near the presynaptic LGI1 complex |
| `Kcna2` | 0 | Kv channel component near the presynaptic LGI1 complex |
| `Nrxn1` | 1 | broader synaptic organizer comparator |
| `Nrxn2` | 0 | broader synaptic organizer comparator |
| `Shank3` | 2 | postsynaptic scaffold comparator |
| `Stxbp1` | 1 | synaptic release comparator |

A same-context profile comparison over these 11 training targets found 6 with no significant features and 5 with only 1-9 significant features. The exact BH<0.05 rows for this cohort were:

- `Adam22`: only `Adam22`, down.
- `Dlg4`: only `Dlg4`, down.
- `Nrxn1`: only `Nrxn1`, down.
- `Stxbp1`: only `Stxbp1`, down.
- `Shank3`: `Shank3` down and `Uba5` up.

Thus even the closest in-training LGI1 receptor partner, `Adam22`, showed a single self-target-significant row and no detected downstream FDR hit in this thalamic population.

## Synthesis

The strongest upward evidence is that `Lgi1` is not absent from the focal population and the extracellular LGI1 pool should be perturbed by harvest in many edited, expressing neurons. That supports a real molecular lesion and makes a count of exactly zero less compelling than for an unexpressed or permanently installed target.

The strongest downward evidence is the same-assay behavior of the nearest available training biology. `Adam22`, `Cacng2`, `Dlg4`, `Gria1`, `Gria2`, `Kcna1`, and `Kcna2` all land at 0-1 total DEGs, and the nonzero entries among `Adam22` and `Dlg4` are just the perturbed transcript itself. LGI1 loss has strong electrophysiologic and circuit consequences, but the declared evidence does not tie sparse juvenile thalamic LGI1 depletion to a broad P37-P44 nuclear RNA response.

I therefore expected at most a self/transcript-proximal hit plus little downstream signal. I placed the point forecast at the low single-hit value:

```tsv
target_name	predicted_n_degs
Lgi1	1
```
