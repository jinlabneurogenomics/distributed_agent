# Nipbl direct n_degs forecast

## Target and endpoint

- Manifest target: `Nipbl`.
- Cell group: `151 TH Prkcd Grin2c Glut`.
- Endpoint: number of focal-cell measured genes with Wilcoxon `pvals_adj < 0.05`.
- Declared measured surface: `[local file: training_de_all_cell_groups.parquet]`.
- Declared count table: `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
- Target biology bundle: `[local file: Nipbl.json]`.

I treated the count table and Parquet as the same experiment, using the count table for the scalar training outcomes and the Parquet only to inspect observed training profiles in the matched 151 TH population. I used the `Nipbl` characterization bundle in its `biology` view only.

## Biological prior from the declared Nipbl bundle

The structured `Nipbl` card supports a real reachable perturbation in this assay:

- exact focal-population reach is high: `Nipbl` is detected in 20,373 of 23,679 matched non-target nuclei, 86.04%, with mean CP10K 1.477;
- NIPBL is a dynamic cohesin loader/ATPase activator rather than a stable product installed before P16;
- direct depletion experiments support loop loss on an hours-long scale, much shorter than the P16 to P37-P44 Perturb-seq window;
- the functional-stock adjudication concludes that operative NIPBL-dependent stock is likely substantially depleted by harvest in successfully edited, expressing cells;
- mammalian NIPBL has no close replacement loader identified in the bounded bundle evidence; and
- postnatal forebrain-neuron conditional loss is reported to affect brain cells and transcripts, but the exact 21-28 day juvenile thalamic latency is unresolved.

Those facts argue against forecasting a hard zero. The main downward uncertainty is survivor conditioning: severe or complete NIPBL loss could deplete edited nuclei before recovery or leave only partial functional loss in the assayed survivors.

## Training measurements used for scale

The declared 151-TH count table is zero inflated: among 1,674 observed training perturbations, 1,205 have `n_degs = 0`, the median is 0, the 75th percentile is 1, the 95th percentile is 18, and the 99th percentile is 454. A few broad stress/chromatin perturbations reach hundreds to thousands of DE genes, with `Uba5 = 2677`, `Tpr = 1768`, `Sin3a = 1433`, and `Yy1 = 720`.

I used the following focal counts as the closest quantitative anchors:

| training perturbation | 151 TH `n_degs` | interpretation |
| --- | ---: | --- |
| `Smc1a` | 24 | core cohesin subunit, nonzero restricted 151-TH response |
| `Stag2` | 37 | cohesin SA2 subunit, strongest direct same-pathway partner represented |
| `Stag1` | 0 | SA1 paralog, no FDR<0.05 focal response |
| `Pds5a` | 0 | cohesin-cycle regulator, no focal response |
| `Hdac8` | 0 | SMC3 deacetylation / CdLS-related regulator, no focal response |
| `Ctcf` | 270 | architectural loop anchor, much larger and mechanistically adjacent |
| `Chd8` | 61 | broader chromatin remodeler in a moderate 151-TH scale |
| `Brd4` | 311 | broad transcriptional chromatin regulator |

The matched Parquet profile comparison gave the same exact focal counts and showed that `Smc1a` had 21 down- and 3 up-regulated FDR<0.05 genes, while `Stag2` had 29 down- and 8 up-regulated genes. `Ctcf`, `Brd4`, and `Yy1` were far broader and had little FDR-level overlap with the cohesin subunit pair in this matched context.

Packaged same-experiment findings for `Smc1a` and `Stag2` summarize the small common state as a same-direction thalamic neuronal connectivity/signaling module. The same corpus explicitly separates that module from the `Ctcf` response: represented cohesin-machinery perturbations did not phenocopy the larger `Ctcf` clustered-protocadherin program in the acute P16 screen. I treated those findings as interpretation of the same Parquet rows, not independent replication.

## Synthesis

`Nipbl` should be more reachable than the quiet `Pds5a`/`Hdac8`/`Stag1` perturbations because its focal expression is broad, no stock should remain for 3-4 weeks after an effective edit, and no close paralog is expected to replace the loader. But the measured training data argue for a restricted cohesin-scale transcriptional response rather than a `Ctcf`-scale architectural collapse: the strongest direct represented cohesin perturbations, `Smc1a` and `Stag2`, produced only 24 and 37 BH<0.05 genes.

I therefore placed the point slightly above `Smc1a` and slightly below `Stag2`, allowing `Nipbl` to be active but still attenuated by partial editing and survivor conditioning.

Point forecast: **32**.
