# Trip12 direct n_degs forecast

## Declared target and endpoint

- Target: `Trip12`
- Focal population: `151 TH Prkcd Grin2c Glut`
- Endpoint: `n_degs`, the count of measured genes with BH-adjusted Wilcoxon `pvals_adj < 0.05` in the focal population.
- Declared measured inputs used:
  - `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` for training `n_degs`
  - `training_de_all_cell_groups.parquet` for focal signed expression profiles of selected training perturbations
  - `Trip12.json`, served through the prediction-safe biology characterization bundle, for Trip12 biology and focal non-target expression reach

The Trip12 target outcome and Trip12 perturbation signature were not in the declared training inputs. The July same-experiment corpus also had no Trip12 Findings, Claims, or explicit comparator references in `corpus.target_context`, so the forecast used the biology bundle plus training perturbations rather than any packaged Trip12 response.

## Trip12 biology prior

The prediction-safe Trip12 bundle supported real target reach in the exact assayed population: 23,379 of 23,679 non-target nuclei expressed Trip12 in `151 TH Prkcd Grin2c Glut` (`98.733%`), with mean raw UMI `6.249`, mean CP10K `3.942`, and pseudobulk CPM `391.655`. This supports CRISPR access to a transcript that is broadly present in the focal class, while the bundle explicitly notes that expression does not establish editing efficiency or functional dependence.

The functional-stock card judged the TRIP12 HECT E3 ligase stock as `likely_substantially_depleted` by the P37-P44 harvest. The main basis was that Trip12 encodes a diffusible catalytic ubiquitin ligase with measured half-lives of `25.733` and `29.106` hours in non-dividing primary mouse neurons, so a 21-28 day P16-to-harvest interval spans many starting-protein half-lives. That pulled the forecast away from a pure technical null.

The same bundle also limited upward transfer. TRIP12 is a substrate-selective HECT E3 in ubiquitin-fusion degradation and K48-linked GCase ubiquitination, not a core proteasome or UFMylation enzyme. The only direct postnatal mouse neural Trip12 loss evidence was adult substantia-nigra AAV-shRNA in an alpha-synuclein challenge at a six-month endpoint; no healthy acute postnatal mouse-neuron series matching the screen window was found. HUWE1 and other E3s can overlap with TRIP12 for some UFD substrates, so focal Trip12 loss has a credible buffered-or-substrate-limited branch.

## Training measurements

The declared focal count table contained 1,674 training perturbations. It was strongly zero-inflated:

- `1205 / 1674` targets had `n_degs = 0`.
- Median `n_degs = 0`.
- 75th percentile `= 1`.
- 90th percentile `= 2`.
- 95th percentile `= 18`.
- 97.5th percentile `= 100`.
- 99th percentile `= 430`.

The closest available substrate-selective HECT/ubiquitin-ligase training rows were heterogeneous rather than one scale family:

| training perturbation | focal `n_degs` | interpretation |
|---|---:|---|
| `Huwe1` | 158 | active HECT E3 and functional UFD-parallel comparator |
| `Hectd4` | 1 | self-transcript only in the focal parquet query |
| `Herc1` | 0 | quiet large E3 comparator |
| `Herc2` | 0 | quiet large E3 comparator |
| `Ube3a` | 0 | quiet HECT E3 comparator |
| `Vcp` | 2 | proteostasis accessory row, nearly quiet |
| `Usp48` | 10 | deubiquitinase/stress-adjacent row, sparse |

Core proteostasis and endolysosomal rows were much larger but less direct:

| training perturbation | focal `n_degs` | why not used as direct scale |
|---|---:|---|
| `Uba5` | 2677 | core UFMylation E1 with a large ER/proteostasis state |
| `Ufc1` | 572 | same UFMylation cascade, strong same-direction Uba5 neighbor |
| `Psmb4` | 742 | 20S proteasome subunit; core proteasome insufficiency |
| `Psmc1` | 430 | 19S ATPase; validated Psmb4-like proteasome state |
| `Rab7` | 501 | endolysosomal state, not a TRIP12 biochemical analogue |

Direct Parquet inspection of the selected rows in `151 TH Prkcd Grin2c Glut` matched the count table and showed that the Huwe1 signature was moderate and RNA-processing/trafficking-rich, not the same as the core UFMylation or proteasome programs. Huwe1 had 90 positive and 68 negative significant features. Its top significant positive rows included `Rsrp1`, `Tcea2`, `Kcnk9`, `Dusp11`, `Begain`, and `Aifm3`; its top negative rows included `Ccdc136`, `Ramp3`, `Pabpn1`, and `L1cam`. In contrast, Uba5 had 2,677 significant rows and strong same-cascade support from Ufc1, while Psmb4/Psmc1 represented a proteasome-failure state.

The selected profile comparison reinforced this separation. Huwe1 was only weakly similar to the larger protein-quality-control profiles in the same group: whole-profile Pearson correlations were `0.071` to Uba5, `0.060` to Ufc1, `0.130` to Psmb4, and `0.131` to Psmc1. By comparison, the true same-pathway UFMylation pair Uba5-Ufc1 had Pearson `0.751`, showing that the profile metric can recover close cascade relatives when they exist. I therefore treated Uba5/Ufc1/Psmb4/Psmc1/Rab7 as upper-state evidence that the focal class can report proteostasis damage, not as equal-scale analogs for Trip12.

The same-experiment corpus supplied the same boundary from curated reports. Huwe1 was a real responder in `151 TH Prkcd Grin2c Glut` with a recurrent Rsrp1/SR-factor RNA-processing module, but its report concluded that the Huwe1 postmitotic signature was not a generic HECT/E3-ligase neurodevelopmental phenotype: Ube3a, Hectd4, Herc2, Ubr1, Trp53, Myc, and Mycn did not reproduce the Huwe1 FDR-level module. Ube3a's own report emphasized a broad weak/null basal snRNA-seq surface with 0 downstream FDR<0.10 genes in all 18 recovered groups. This made the Huwe1 count useful as the nearest active comparator but too high to transfer wholesale.

## Forecast

Upward evidence:

- Trip12 is expressed in almost every focal non-target nucleus.
- The 21-28 day window should be long enough to clear a disrupted TRIP12 protein pool in edited cells.
- The same focal class can produce large proteostasis signatures, and a UFD-parallel HECT ligase, Huwe1, produced 158 significant genes.

Downward evidence:

- Most focal training perturbations are zero, and the 95th percentile is only 18.
- Represented HECT/E3 comparators near Huwe1 were flat or nearly flat.
- TRIP12 is a substrate-selective ligase with HUWE1/other-E3 buffering for some UFD substrates, not a core UFMylation or proteasome component.
- No direct acute healthy thalamic Trip12-loss evidence established a large postnatal transcriptomic state.

I therefore placed Trip12 above the zero/one-gene HECT rows but far below Huwe1 and far below the core proteostasis donors, using the empirical 95th percentile of the training count table as a small-active point.

Final direct point prediction: `18`.
