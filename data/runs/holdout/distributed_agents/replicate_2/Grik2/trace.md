# DEG-count prediction trace

## Question and ambiguity resolution

The requested readout is the held-out `n_degs` for `Grik2` in `151 TH Prkcd Grin2c Glut` cells: the number of measured mouse genes with Benjamini-Hochberg-adjusted Wilcoxon `pvals_adj < 0.05` after acute AAV-CRISPR loss of the requested target.

I treated `Grik2` as completely unobserved in the supplied differential-expression parquet and in the focal training-count CSV. I used its biological relatives only when they were non-held-out perturbations in the training data. I did not reinterpret the endpoint as effect size, lethality, editing efficiency, or electrophysiology; a zero prediction means no measured gene is expected to cross this particular FDR threshold in this cell group.

## Sources used

- Primary endpoint data: `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
- Primary expression-signature data: `[local file: training_de_all_cell_groups.parquet]`, restricted to `group_name == "151 TH Prkcd Grin2c Glut"` for focal profile checks.
- Requested-target manifest: `[local file: 099_Grik2.csv]`.
- Distributed Agents same-experiment corpus release `perturbai-july-260713-sourceguard-1773-v1`; `Grik2` itself had no corpus record, but `Grik1`, `Grik3`, `Grik4`, and `Grik5` did.
- PubMed literature for kainate-receptor subunit biology: Crepel and Mulle 2014, DOI `10.1016/j.coph.2014.11.012`, PMID `25506747`; Tang et al. 2011, DOI `10.1523/JNEUROSCI.6617-10.2011`, PMID `21734292`; Fisher 2015, DOI `10.1016/j.neuropharm.2015.08.018`, PMID `26277340`; Brown et al. 2016, DOI `10.1113/JP271690`, PMID `26682513`; Stolz et al. 2021, DOI `10.1016/j.ajhg.2021.07.007`, PMID `34375587`.

## Training-data calibration

The focal training endpoint is very sparse: 1205 of 1674 non-held-out perturbations have `n_degs = 0`, 276 have exactly one DEG, 87 have 2-9 DEGs, 63 have 10-99, and 43 have at least 100.

I first extracted counts for receptor and postsynaptic targets that could plausibly bracket `Grik2`:

| training target | focal `n_degs` | use in this prediction |
| --- | ---: | --- |
| `Grik1` | 0 | kainate receptor subunit and closest family analog |
| `Grik3` | 0 | kainate receptor subunit and closest family analog |
| `Grik4` | 0 | high-affinity kainate subunit, heteromeric-family analog |
| `Grik5` | 1 | high-affinity kainate subunit, heteromeric-family analog; focal singleton only |
| `Gria1`, `Gria2`, `Gria3` | 0, 0, 0 | AMPA-receptor counterexamples showing other ionotropic glutamate receptors were also mostly buffered |
| `Grid1`, `Grid2` | 1, 0 | ionotropic glutamate receptor relatives, again near zero |
| `Cacng2`, `Cacng3`, `Frrs1l` | 0, 0, 1 | AMPAR auxiliary/trafficking comparators |
| `Dlg4`, `Shank2`, `Shank3`, `Homer2`, `Syngap1`, `Tanc2` | 1, 0, 2, 0, 0, 0 | postsynaptic-density counterexamples; perturbing neighboring scaffolds did not create a broad focal program |
| `Grin1`, `Grin2a`, `Grin2b`, `Grin2d`, `Grin3a` | 89, 1, 2, 0, 0 | NMDA-receptor contrasts; `Grin1` proves that a glutamate-receptor perturbation can be visible in this cell group |

I then compared the focal-cell log-fold-change profiles for the available glutamate-receptor cohort with Distributed Agents runtime `profile_compare` and `profile_inspect`. The focal profile had 17,259 measured features for each available `Grik` node. `Grik1`, `Grik3`, and `Grik4` had zero FDR<0.05 features, while `Grik5` had one. Pair inspection found no FDR-supported feature intersection between any `Grik` node and the AMPA, NMDA, delta-receptor, or PSD peers above, because the kainate signatures were empty or singleton. Whole-vector logFC similarities were therefore not used as mechanistic evidence: they were dominated by subthreshold, q=1 tails rather than shared FDR-supported biology.

The same-experiment Distributed Agents corpus independently summarizes the training perturbations in the same direction. It reports that represented kainate-receptor subunits `Grik1`, `Grik3`, `Grik4`, and `Grik5` did not form a shared basal neuronal transcriptomic response module. In particular, `Grik1` was pan-measured null in the release, `Grik4` had no robust downstream response, `Grik5` had no non-on-target downstream transcriptional response, and `Grik3` produced only a few sparse, idiosyncratic cortical hits outside the focal thalamic group. The corpus also explicitly notes that `Grik2` and `Neto1/2` were absent from that release, so I used these findings as analog evidence only, not as a direct observation of `Grik2`.

## Target-specific reasoning

### `Grik2`

`Grik2` encodes GluK2, a principal pore-forming kainate receptor subunit. Kainate receptors are tetrameric ionotropic glutamate receptors assembled from GluK1-GluK5 subunits; GluK2-containing receptors can operate with auxiliary NETO proteins and in heteromeric combinations such as GluK2/GluK5 (Crepel and Mulle 2014; Fisher 2015; Brown et al. 2016). NETO1 is required for native synaptic kainate-receptor function at hippocampal mossy fiber-CA3 synapses and regulates GluK2-containing receptor abundance in postsynaptic densities (Tang et al. 2011). Human GRIK2 variants perturb GluK2 receptor function and can cause neurodevelopmental disease, so this is a real synaptic receptor rather than an inert family member (Stolz et al. 2021).

Those biological facts make `Grik1`, `Grik3`, `Grik4`, and `Grik5` the right first analogs, with AMPA, NMDA, delta, and PSD genes as boundaries. The focal data argue that the endpoint is almost always silent for this local family: the four measured kainate perturbations are `0, 0, 0, 1`, and the broader AMPA/delta/PSD set is also concentrated at 0-2 DEGs. The most responsive direct counterexample is `Grin1` with 89 focal DEGs, but that looks like an NMDA-specific nuclear response rather than a generic ionotropic-glutamate-receptor response, because `Gria1/2/3`, `Grik1/3/4`, `Grid2`, `Grin2d`, and `Grin3a` were all zero in the same endpoint.

The corpus strengthens the zero call because it finds no coherent kainate-family RNA module across the represented subunits. That matters more here than the fact that GluK2 is central to kainate electrophysiology: the measured relatives show that individual kainate-receptor CRISPR perturbations can leave basal single-nucleus RNA essentially unchanged for 3-4 weeks after P16 infection. Since `Grik2` was absent and may have GluK2-specific roles not captured by `Grik1/3/4/5`, I considered a singleton plausible, especially because `Grik5` has one focal DEG in the exact training endpoint. I still put the point estimate at zero because three of the four kainate paralogs are exact zeros, the `Grik5` response is only a singleton, and there is no within-dataset evidence that a GluK2-related downstream program recurs in this focal class.

Predicted `n_degs`: 0.

## Limits

- `Grik2` itself was held out from both the supplied DE parquet and the training-count CSV, so this is extrapolation from neighboring perturbations.
- `Neto1` and `Neto2` are central GluK2 auxiliary subunits but were missing from the inspected training profiles, leaving no direct NETO-loss analog.
- Kainate receptors can have large effects on channel gating, synaptic localization, plasticity, seizures, and behavior without producing a steady-state nuclear RNA program. The forecast is only for the FDR<0.05 snRNA-seq DEG count in recovered `151 TH Prkcd Grin2c Glut` nuclei.
- The endpoint includes the perturbed target transcript if it passes FDR. I did not promote `Grik2` to one DEG on that basis because self-transcript loss is weak and inconsistent in this assay, and the focal counts for `Grik1`, `Grik3`, and `Grik4` show that on-target kainate transcripts often do not cross the threshold.
