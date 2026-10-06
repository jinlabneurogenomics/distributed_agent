# DEG-count prediction trace

## Question and endpoint alignment

The requested endpoint is `n_degs` for each held-out perturbation in `151 TH Prkcd Grin2c Glut`: the number of measured genes whose Wilcoxon p-value has Benjamini-Hochberg adjusted `pvals_adj < 0.05` in perturbed versus matched control nuclei. The only requested target in this run is `Ophn1`, and it is absent from both visible training inputs.

I treated the endpoint as a direct focal-cell transcriptional breadth readout, not as a measure of biological importance, neuronal survival, target expression, or edit efficiency. Because `n_degs` includes the perturbed gene itself when that transcript passes FDR, visible one-DEG analogs were separated into self-only effects versus true downstream transcriptional responses.

## Sources used

- Declared endpoint table: `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`, 1,674 non-held-out training targets with observed focal-cell `n_degs`.
- Declared differential-expression Parquet: `training_de_all_cell_groups.parquet`, queried for `151 TH Prkcd Grin2c Glut` rows of mechanistically selected training analogs.
- Run-local manifests: `task_bindings.json`, `dataset_context.md`, `coverage.json`, `capabilities.json`, and `measurement_registry.json`.
- Same-experiment internal corpus: the July `perturbai-july-260713-sourceguard-1773-v1` corpus was only inspected through the capability/coverage manifests to establish what operations were available. I did not use graph topology, relation multiplicity, or Finding summaries to score `Ophn1`.
- External literature for OPHN1 mechanism:
  - Fauchereau et al. 2003, DOI `10.1016/s1044-7431(03)00078-2`, PMID `12932438`: OPHN1 is a neuronal F-actin-associated RhoGAP whose GAP domain regulates Rho-family cytoskeletal signaling.
  - Nakano-Kobayashi et al. 2009, DOI `10.1016/j.cub.2009.05.022`, PMID `19481455`: OPHN1 interacts with endophilin A1 and its loss impairs synaptic-vesicle endocytosis at hippocampal synapses.
  - Nadif Kasri et al. 2009, DOI `10.1101/gad.1783809`, PMID `19487570`: OPHN1 RhoGAP activity stabilizes AMPA-receptor-mediated glutamatergic synaptic maturation and plasticity.
  - Valnegri et al. 2011, DOI `10.1038/nn.2911`, PMID `21874017`: OPHN1 can couple synaptic activity to Rev-erb-alpha/Bmal1 circadian regulation in hippocampal neurons.
  - Nuovo et al. 2021, DOI `10.1002/ajmg.a.62144`, PMID `33638601`: human OPHN1 loss-of-function alleles cause an X-linked neurodevelopmental syndrome, supporting loss of OPHN1 as a real neuronal perturbation rather than a housekeeping-null expectation.

## Computation over the visible dataset

I read the focal-cell DEG-count table and then used PyArrow predicate filters on the declared Parquet to extract rows where

```python
group_name == "151 TH Prkcd Grin2c Glut"
gene_target in selected_OPHN1_analogs
```

For each selected training perturbation I recomputed:

- its endpoint count from `pvals_adj < 0.05`;
- the number of significant genes after excluding the self transcript, `names != gene_target`;
- the smallest adjusted p-value after self removal; and
- the matched perturbed/control nucleus counts, to flag very weak analog rows.

This matters because several visible synaptic perturbations have `n_degs = 1` only because the target transcript itself was significant; those runs provide little evidence for a propagated downstream state in recovered `151 TH Prkcd Grin2c Glut` nuclei.

## Target-specific evidence

### Ophn1

`Ophn1` encodes oligophrenin-1, a BAR/PH/RhoGAP protein. The external literature places OPHN1 at two local neuronal processes: it downregulates Rho-family small GTPases to shape the actin cytoskeleton, and it participates in synaptic-vesicle or membrane endocytosis through its BAR-domain interactions. Those functions make RhoGAP/Rac-Cdc42 effectors, postsynaptic actin regulators, and synaptic endocytosis genes the appropriate visible comparison set.

The most direct visible Rho-family and spine-actin analogs were quiet in the focal dataset:

| training target | role relative to OPHN1 biology | observed focal `n_degs` | focal downstream pattern |
| --- | --- | ---: | --- |
| `Arhgap32` | neuronal RhoGAP/p250GAP, closest visible GAP analog | 0 | no downstream FDR 0.05 genes; best nonself BH value `0.607` |
| `Arhgap18` | Rho-family GAP | 0 | no downstream FDR genes; best nonself BH value `1.0` |
| `Kalrn` | Rho/Rac GEF involved in dendritic spine signaling | 0 | no downstream FDR genes; best nonself BH value `1.0` |
| `Tiam1` | Rac1 GEF in synaptic actin signaling | 0 | no downstream FDR genes; best nonself BH value `0.312` |
| `Chn1` | Rac GAP/chimaerin family regulator | 0 | no downstream FDR genes; best nonself BH value `0.478` |
| `Dock3` | Rac GEF | 0 | no downstream FDR genes; best nonself BH value `0.584`, with only 69 matched perturbed nuclei |
| `Rac1` | Rho-family GTPase acted on by GEF/GAP modules | 0 | no downstream FDR genes; best nonself BH value `1.0` |
| `Cdc42` | Rho-family GTPase; OPHN1-linked cytoskeletal branch | 1 | the one FDR gene was `Cdc42` itself; no downstream FDR genes |
| `Pak1` | Rac/Cdc42 effector kinase | 1 | the one FDR gene was `Pak1` itself; no downstream FDR genes, best nonself BH value `0.323` |
| `Pak2` | Rac/Cdc42 effector kinase | 0 | no downstream FDR genes; best nonself BH value `0.807` |
| `Pak3` | Rac/Cdc42 effector kinase and XLID-linked OPHN1 pathway neighbor | 0 | no downstream FDR genes; best nonself BH value `0.910` |
| `Limk1` | downstream actin kinase in Rho/PAK signaling | 0 | no downstream FDR genes; best nonself BH value `1.0` |

This group is the strongest within-dataset evidence. OPHN1 loss is not identical to any one of these perturbations: GAP loss can hyperactivate rather than inhibit a GTPase branch, and OPHN1 also has BAR-domain trafficking functions. However, the fact that visible upstream activators, GAPs, GEFs, GTPases, and PAK/LIMK effectors were all at 0 or self-only 1 argues that acute partial CRISPR loss of a local Rho-actin regulator did not commonly produce a broad focal-cell transcriptional state in this assay.

The synaptic-vesicle/endocytosis arm pointed in the same direction:

| training target | role relative to OPHN1 biology | observed focal `n_degs` | focal downstream pattern |
| --- | --- | ---: | --- |
| `Dnm1` | synaptic-vesicle fission/endocytosis | 1 | self-only; no downstream FDR genes, best nonself BH value `0.575` |
| `Synj1` | vesicle recycling phosphatase | 1 | self-only; no downstream FDR genes |
| `Bin1` | BAR-domain membrane curvature/endocytosis | 1 | self-only; no downstream FDR genes |
| `Sh3kbp1` | SH3 adaptor connected to endocytic signaling | 0 | no downstream FDR genes; best nonself BH value `0.239` |
| `Dlg4` | postsynaptic density scaffold | 1 | self-only; no downstream FDR genes, best nonself BH value `0.738` |
| `Shank3` | postsynaptic density scaffold | 2 | one self call plus `Uba5`; broader pattern not shared by the OPHN1-proximal set |
| `Gria1` | AMPA receptor subunit, relevant to OPHN1 postsynaptic stabilization | 0 | no downstream FDR genes; best nonself BH value `0.246` |
| `Grin1` | obligatory NMDA receptor subunit | 89 | counterexample: direct loss of the core NMDA receptor produced a broader response, but this is a receptor-channel perturbation rather than a local RhoGAP/endocytosis perturbation |

`Grin1` shows that the `151 TH Prkcd Grin2c Glut` assay can detect a glutamatergic-synapse perturbation when the transcriptional consequence is strong. I did not transfer its 89-DEG count to `Ophn1`, because NMDA receptor loss directly changes excitatory calcium signaling, while OPHN1 mainly perturbs actin/endocytic regulation downstream or parallel to receptor trafficking. The more local AMPA/PSD and vesicle-recycling genes were at 0, 1 self-only, or 2.

#### Causal transfer for `Ophn1`

The experimental chain for OPHN1 is:

`Ophn1` CRISPR loss of function -> reduced OPHN1 RhoGAP/BAR activity -> altered Rho-family actin regulation and synaptic membrane recycling -> changes in synapse morphology or vesicle cycling in surviving postmitotic neurons -> possible recovered-nucleus transcriptional response -> FDR-significant focal DEGs.

External papers support the first three links and make a nonzero biological effect plausible. The visible dataset weakens the last two links for this exact endpoint: perturbing several comparable local Rho-actin and vesicle-endocytosis genes left the recovered `151 TH Prkcd Grin2c Glut` transcriptome essentially unchanged at BH FDR 0.05. Germline or developmental OPHN1 phenotypes, adult-born olfactory interneuron defects, and hippocampal synapse physiology do not guarantee a large 3-4 week snRNA-seq signature after sparse P16 AAV CRISPR in thalamic glutamatergic nuclei.

The predicted sign is therefore a biological effect with an indeterminate or very small focal DEG count, most likely zero. The only credible way to move the point estimate to 1 would be a significant `Ophn1` self-transcript call. Close large neuronal regulators such as `Arhgap32`, `Kalrn`, and `Dock3` failed even at the self row in this focal class, so I did not add a self-only DEG.

**Final point prediction for `Ophn1`: `0` DEGs.**

## Limits

- The held-out `Ophn1` signature and its matched perturbed nucleus count are absent by design. I could not verify baseline `Ophn1` expression, self-transcript detectability, or guide performance.
- `Ophn1` has both GAP-dependent actin and BAR-dependent trafficking roles; no visible training perturbation is an obligate loss of the exact same molecular function.
- The closest training analogs are local synaptic or cytoskeletal regulators, where the measured endpoint is often zero even for genes with well-established neuronal physiology. A predicted zero here means no measured genes are expected to pass BH FDR 0.05 in recovered focal nuclei, not no synaptic phenotype.
- Several analog rows had modest perturbed-cell counts, especially `Dock3` and `Synj1`; null calls in those rows are partly power-limited.
- The differential-expression Parquet and the July same-experiment corpus are representations of the same Perturb-seq experiment, so agreement between them would not be independent replication. I relied on external OPHN1 literature only for mechanism, not for a calibrated DEG-count distribution in this assay.
