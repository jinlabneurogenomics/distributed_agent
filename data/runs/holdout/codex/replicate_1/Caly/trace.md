# Caly direct n_degs forecast

## Target and endpoint

- Target: `Caly`
- Focal class: `151 TH Prkcd Grin2c Glut`
- Endpoint: number of measured genes with BH-adjusted Wilcoxon `p < 0.05`
- Point prediction: `0`

## Evidence

### Declared target biology

The canonical biology bundle is for the exact held-out target `Caly` and did not expose the target outcome or labeled-neighbor outcomes. Its exact in-assay expression measurement shows that `Caly` is present in the 151 thalamic population: 20,881 of 23,679 non-target nuclei expressed the feature, or 88.18%, with mean raw UMI 2.81, mean log1p CP10K 0.907, and pseudobulk CPM 176.1.

The biological source card places calcyon as a neuronal vesicular single-pass membrane component that binds clathrin light chain and promotes clathrin-mediated endocytosis and cargo sorting. Caly-null mouse work supports real postnatal neuronal function: impaired stimulated AMPA-receptor internalization and hippocampal LTD, and altered NRG1/ErbB4-linked signaling. The same bundle also records two important dampers for this assay: the loss evidence is not from an acute P16 thalamic edit, and no Caly-specific protein half-life, residence time, or induced loss-to-clearance clock was found. Its functional-stock adjudication therefore concludes that functional stock by the P37-P44 harvest is indeterminate.

### Packaged same-experiment evidence

`Caly` had no same-experiment Findings, Claims, or explicit comparator references in the selected report corpus, so there was no target-specific packaged profile interpretation to transfer.

### Training count table

The declared 151-class training count table contains 1,674 measured training perturbations and withholds `Caly`. It is heavily concentrated at zero or near-zero response:

- 1,205 of 1,674 training targets have `n_degs = 0`.
- 1,571 of 1,674 have `n_degs <= 10`.
- Median `n_degs` is 0; the 75th percentile is 1; the 90th percentile is 2; the 95th percentile is 18.

I used training perturbations tied to clathrin/endosomal/synaptic trafficking or to the NRG1/ErbB4 branch of the Caly biology bundle. The exact AP-2 subunits, NEEP21-family genes `Nsg1` and `Nsg2`, `Bace1`, and several other close trafficking genes were absent from the training count table, but the available analogs were quiet:

| training target | biological bearing for Caly | `n_degs` |
| --- | --- | ---: |
| `Ap3b1` | AP-dependent cargo sorting boundary | 0 |
| `Erbb4` | downstream receptor in the NRG1 branch | 0 |
| `Bin1` | endocytic adaptor | 1 |
| `Dnm1` | neuronal vesicle scission/endocytosis machinery | 1 |
| `Synj1` | synaptic-vesicle endocytosis machinery | 1 |
| `Cltc` | clathrin heavy-chain machinery | 3 |
| `Rab7` | broad late-endosome/lysosome boundary, not a close cargo-selective analog | 501 |

The closer analogs argue for a zero or very small count. I treated `Rab7` only as a broad endosomal stress boundary: it proves that some endosomal perturbations can be highly visible in this dataset, but its response scale should not be transferred to a cargo-selective calcyon knockout.

### Parquet profile check

I compared `Ap3b1`, `Bin1`, `Cltc`, `Dnm1`, `Erbb4`, `Rab7`, and `Synj1` in the declared differential-expression Parquet, restricted to `151 TH Prkcd Grin2c Glut`. All seven profiles were available. The cohort diagnostic showed weak recurrence rather than a single shared high-DEG state: across the 21 selected pairs, the mean top-tail overlap coefficient was 0.063 for positive tails and 0.073 for negative tails, the positive significant-program overlap count was 0, and the negative significant-program overlap median was 0. This reinforced the count-table interpretation that the observed high `Rab7` state is not the generic outcome of perturbing neuronal endocytic trafficking components.

## Synthesis

High 151-class `Caly` expression makes target reach plausible, and the germline-null phenotypes argue that calcyon is not functionally inert. The predicted endpoint, however, is a short-window survivor single-nucleus transcriptional DEG count, not receptor internalization, synaptic physiology, or long-horizon germline phenotype. Calcyon is cargo-selective and vesicular, and the target card could not establish that pre-existing functional stock is depleted enough by 21-28 days after a P16 edit to expose a large transcriptome. In the exact 151 training table, perturbations closer to the clathrin/AP/synaptic-trafficking part of Caly biology were all at 0-3 DEGs, while the broad `Rab7` endosomal hit was a poor scale match.

I therefore placed `Caly` at the modal quiet outcome rather than assigning the broader endosome/lysosome response, giving a direct point forecast of `0` DEGs.
