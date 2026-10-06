# DEG-count prediction trace

## Question and resolved ambiguity

The requested prediction is a point estimate for `n_degs`, the number of measured genes with BH-adjusted Wilcoxon `pvals_adj < 0.05` after a held-out genetic perturbation in `151 TH Prkcd Grin2c Glut` cells. The run's held-out CSV contains one target, `Opn1mw`; it is absent from both the supplied differential-expression parquet as a perturbation and from the focal training DEG-count CSV. I therefore treated the task as a transfer problem from non-held-out perturbations, not as a direct lookup.

The cell label was used literally as the Allen-style thalamic glutamatergic class name. I did not interpret `TH` as tyrosine hydroxylase, and I did not treat the reported count as an eye or retinal readout: the experiment assayed NeuN+ nuclei from whole brain excluding olfactory bulb and hindbrain after sparse postnatal AAV CRISPR loss of function.

## Sources

- Declared training endpoint file: `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
- Declared raw DE file: `training differential-expression dataset`.
- Requested targets: `single-target request for Opn1mw`.
- Run-local metadata: `task_bindings.json`, `coverage.json`, and `capabilities.json`.
- Internal same-experiment corpus: `perturbai-july-260713-sourceguard-1773-v1`; I used the Opn1sw Finding inventory and resolved Evidence/Reference records. This corpus is a semantic rendering of the same Perturb-seq experiment, not independent replication.
- External mechanism checks from Mouse Genome Informatics and PubMed. For cone opsins I used Deng et al. 2018, PMID:29386880; Deng et al. 2019, DOI:10.1167/iovs.19-27079; Ma et al. 2022, DOI:10.1089/hum.2021.298; Sechrest et al. 2023, DOI:10.1016/j.visres.2023.108221. For photoreceptor regulators I used Corbo et al. 2010, DOI:10.1101/gr.109405.110, and McNerney and Johnston 2021, DOI:10.1016/bs.vh.2021.03.001.

## Dataset calibration

I first calibrated the scale of the response using the 1,674 visible training targets in the focal cell group. The distribution was extremely zero-inflated and right-skewed:

| statistic | value |
|---|---:|
| zero-DEG targets | 1,205 / 1,674 |
| median `n_degs` | 0 |
| 75th percentile | 1 |
| 90th percentile | 2 |
| 95th percentile | 18 |
| maximum | 2,677 |

This means the prior for a lineage-restricted or silent target is a point mass at 0, while broad counts are reserved for targets with clear evidence that the perturbation should affect a pathway operating in the recovered thalamic neurons.

For biologically relevant training perturbations I read the focal-cell rows from the parquet and counted measured genes with `pvals_adj < 0.05`, checking the minimum adjusted p-value as a near-threshold guard. The direct cone-opsin analog and obvious retinal transcriptional or phototransduction controls were flat in the focal group:

| training perturbation | observed `n_degs` in `151 TH Prkcd Grin2c Glut` | smallest focal `pvals_adj` | relevance to `Opn1mw` |
|---|---:|---:|---|
| `Opn1sw` | 0 | 1.0000 | closest represented cone opsin; S-opsin counterpart of M-opsin |
| `Rho` | 0 | 0.6607 | retinal GPCR photopigment in rods, useful as a phototransduction specificity control |
| `Crx` | 0 | 1.0000 | retina/photoreceptor transcriptional activator |
| `Nr2e3` | 0 | 0.8300 | retinal nuclear receptor and rod/cone fate regulator |
| `Otx2` | 0 | 0.8849 | eye and photoreceptor developmental regulator |
| `Rxrg` | 0 | 0.4375 | RXR member implicated in mouse cone opsin patterning |
| `Thrb` | 0 | 1.0000 | thyroid-hormone receptor branch that regulates M-opsin/S-opsin fate in cones |
| `Gucy2e` | 0 | 1.0000 | retinal guanylate cyclase in cone/rod phototransduction |
| `Gucy2c` | 0 | 1.0000 | guanylate-cyclase paralog represented in the screen; no thalamic response |
| `Pax6` | 0 | 1.0000 | eye-development transcription factor, but not a postnatal thalamic opsin analog |
| `Six3` | 0 | 1.0000 | forebrain/eye-development transcription factor, also not an active cone-opsin analog |
| `Neurod1` | 0 | 1.0000 | neuronal/retinal developmental factor; no focal response |
| `Rorb` | 0 | 1.0000 | nuclear receptor in retinal and thalamic identity contexts |
| `Esrrb` | 0 | 1.0000 | nuclear receptor control represented in the screen |
| `Thra` | 3 | 0.0000023 | thyroid-hormone receptor control; small focal response only |

The Opn1sw same-experiment report was the most target-proximal internal evidence. Its negative-result Finding reported 0 genes at FDR<0.10 in all 22 recovered brain-neuron groups, including 0 FDR<0.10 downstream genes in `151 TH Prkcd Grin2c Glut` with 188 Opn1sw-perturbed nuclei against 23,679 controls. Its cross-perturbation Finding classified the top whole-signature neighbors as noise-floor neighbors rather than a shared FDR module, and its photoreceptor-pathway Finding reported that `Rho`, `Crx`, `Nr2e3`, `Rxrg`, and `Thrb` were flat or nearly flat across the matched brain-neuron surface. Those internal Findings agree with the focal raw counts above.

## Target-specific reasoning

### Opn1mw

`Opn1mw` encodes mouse M-opsin, a middle-wavelength cone photopigment. The biological action of losing Opn1mw is direct in retinal cone outer segments: Opn1mw-null mouse studies show loss of M-cone function and abnormal dorsal-cone outer segments that can be rescued by AAV expression of human M- or L-opsin (Deng et al. 2018, PMID:29386880; Deng et al. 2019, DOI:10.1167/iovs.19-27079). Combined loss of `Opn1mw` and `Opn1sw` accelerates cone degeneration in mouse retina and is a model for blue cone monochromacy (Ma et al. 2022, DOI:10.1089/hum.2021.298; Sechrest et al. 2023, DOI:10.1016/j.visres.2023.108221).

That intervention-to-endpoint chain should not transfer to the requested cells. Opn1mw loss removes a retinal cone opsin from an outer-segment phototransduction compartment; the assayed nuclei are thalamic glutamatergic neurons recovered from NeuN-enriched brain tissue, and retina was not the sampled organ. The closest same-experiment analog, `Opn1sw`, is also a cone opsin, and it produced no robust downstream DE anywhere in the recovered brain-neuron surface. The raw focal endpoint for `Opn1sw` is exactly 0 DEGs with all Opn1sw focal adjusted p-values equal to 1.0 at FDR resolution. If cone-opsin perturbation created an ectopic photoreceptor-like stress or phototransduction program in these neurons, the same-experiment checks of `Rho`, `Crx`, `Nr2e3`, `Rxrg`, and `Thrb` would be the obvious counterexamples; they were also 0 in the focal count file, and the Opn1sw internal corpus found no shared FDR photoreceptor module. Corbo et al. 2010 and McNerney and Johnston 2021 support the external side of this interpretation by placing CRX, TR-beta/RXR-gamma, Nr2e3, and the opsins in retinal photoreceptor or cone-subtype programs rather than in a generic postnatal thalamic-neuron response.

I therefore predict no FDR<0.05 transcriptional response for Opn1mw in `151 TH Prkcd Grin2c Glut`. This is primarily driven by within-dataset evidence from Opn1sw and represented retinal-program controls, with external gene-function knowledge used to justify that these are the mechanistically appropriate analogs and that their null responses should transfer to Opn1mw in a brain-neuron assay.

Predicted `n_degs`: **0**.

## Limits

`Opn1mw` itself was held out, so the prediction is extrapolated from `Opn1sw` and other represented retinal genes rather than measured directly. The CRISPR experiment measured recovered NeuN+ brain nuclei 3-4 weeks after P16 AAV delivery; it does not assay retina, M-cone survival, electroretinography, color vision, or congenital eye-development phenotypes. Some analogs such as `Crx`, `Pax6`, `Six3`, `Otx2`, `Thrb`, and `Rxrg` are developmental or nuclear-receptor regulators whose embryonic or retinal consequences are much broader than acute mosaic postnatal loss in thalamic glutamatergic neurons, so their focal zeros are specificity controls rather than proof that those genes are globally inert. Finally, a zero DEG-count prediction means I do not expect any measured gene to pass this assay's FDR 0.05 threshold; it does not prove perfect absence of biological perturbation or retinal inactivity of Opn1mw.
