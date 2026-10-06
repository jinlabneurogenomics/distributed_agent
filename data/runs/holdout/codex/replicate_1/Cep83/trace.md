# Direct Cep83 forecast for `151 TH Prkcd Grin2c Glut`

## Target and endpoint

- Target from the one-row holdout manifest: `Cep83`.
- Endpoint to predict: number of measured genes in `151 TH Prkcd Grin2c Glut` with BH-adjusted Wilcoxon `pvals_adj < 0.05`.
- The training count table contained 1,674 non-Cep83 perturbations for the same endpoint.

## Evidence used

### Cep83 biology bundle

- Cep83 is expressed in the exact focal population: 14,148 of 23,679 non-target nuclei expressed it; mean expression was 0.6567 cp10k and the pseudobulk abundance was 66.15 CPM.
- CEP83 is a proximal organizer of the mother-centriole distal appendage, recruiting distal-appendage components needed for basal-body docking and primary-cilium initiation.
- Mouse neural evidence establishes that Cep83 deletion can remove primary cilia in cortical radial glia and in postmitotic forebrain excitatory neurons.
- The same bundle leaves the decisive short-window stock question unresolved. By the P16 edit, postmitotic thalamic neurons should already have distal appendages and cilia installed; a disruptive edit stops new intact CEP83 synthesis but is not expected to dismantle the existing appendage immediately, and no source in the bounded search timed CEP83 protein, distal-appendage, or mature-neuronal cilium clearance over the 21-28 day P16-to-P37/P44 window.

Interpretation: the target is reachable, and Cep83 loss can matter in postmitotic neurons, but the biology does not force a fully realized cilium-loss state in the assayed recovered nuclei by harvest.

### Training endpoint distribution

The endpoint is zero-inflated in this cell group:

- 1,205 / 1,674 training targets had `n_degs = 0`.
- 1,546 / 1,674 had `n_degs <= 5`.
- The median was `0`, the 90th percentile was `2`, and the 95th percentile was `18`.

Thus, absent fast cell-state remodeling, the empirical base rate favors a zero or singleton response.

### Matched ciliary comparators

I used the declared training count table and the declared expression Parquet filtered to `group_name = "151 TH Prkcd Grin2c Glut"` for represented ciliary, basal-body, transition-zone, BBS/IFT, and Hedgehog-adjacent genes. Counts in this exact endpoint were:

```text
B9d1 0
Bbs5 0
Cep120 0
Cep290 0
Dync2h1 0
Dync2i1 0
Gli2 0
Ift43 0
Ift81 0
Ift88 0
Kif3b 0
Nek1 0
Ptch1 0
Rfx3 0
Rpgrip1l 0
Sclt1 0
Smo 0
Spata7 0
Ttc21b 0
Ttc8 1
Wdr37 0
```

The profile comparison over these 21 available ciliary-related perturbations found 20 with no significant features and one in the 1-9-significant-feature bin. A cohort diagnostic showed no FDR-supported shared positive or negative program across the panel; top-tail overlaps were small and the strongest Sclt1, Ift88, Kif3b, Dync2h1, and Cep290 rows remained `0`-DEG profiles.

These comparator genes are not exact Cep83 analogues: most test intraflagellar transport, transition-zone, BBSome, or ciliary signaling rather than the CEP83-installed distal appendage. Still, `Sclt1` is recruited downstream of CEP83 at the distal appendage and was exactly flat in this thalamic class, while `Cep290`, `Ift88`, `Ift81`, `Ift43`, `Kif3b`, and `Dync2h1` test whether loss of core primary-cilium transport machinery creates a basal nuclear RNA state. They did not.

### Same-experiment corpus context

Packaged reports for `Ift88`, `Cep290`, `Sclt1`, and `Ttc8` interpret the same experiment consistently: represented ciliary trafficking, BBSome, transition-zone, ciliary-GPCR, and Hedgehog-adjacent perturbations were generally absent, singleton-only, or orthogonal at the basal postnatal neuronal nuclear-RNA level. In particular:

- The `Ift88` report anchors a high-confidence claim that acute perturbation of represented ciliary trafficking and signaling genes in postnatal NeuN-positive neurons is largely buffered at the basal nuclear-RNA level rather than producing a coherent shared ciliary module.
- The `Sclt1` report separates SCLT1's strong structural requirement for ciliogenesis from the present assay output, noting that postnatal neuronal snRNA-seq saw little secondary nuclear remodeling after acute `Sclt1` perturbation.
- The `Cep290` and `Ttc8` reports likewise describe flat or singleton ciliary-comparator surfaces and caution that the assay did not image cilia or measure receptor/protein localization.

This corpus evidence is a curated view of the same Perturb-seq experiment, not independent replication, so I used it only to interpret the comparator class that was directly visible in the count table and Parquet.

## Synthesis

Cep83 has adequate baseline reach in the assayed thalamic neurons and no close-paralog rescue is established, so I did not discount it as unexpressed or categorically inert. The limiting factor is instead endpoint coupling: CEP83 is an installed distal-appendage scaffold, the P16 edit occurs after primary cilia are already built, and the biology bundle explicitly leaves 21-28 day mature-neuron stock depletion indeterminate.

The best measured local precedent is not a broad stress or RNA-processing perturbation from the right tail of the count distribution; it is the represented cilia group. That group is overwhelmingly flat in this exact high-yield class, including `Sclt1` and the IFT/dynein/transition-zone genes that should reveal a shared primary-cilium nuclear response if basal ciliary failure were a strong P37/P44 thalamic transcriptome driver.

I therefore forecast the modal endpoint value:

```text
Cep83 n_degs = 0
```
