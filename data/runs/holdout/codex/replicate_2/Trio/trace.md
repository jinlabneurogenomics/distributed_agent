# Direct n_degs forecast for Trio in 151 TH Prkcd Grin2c Glut

## Target and endpoint

- Target: `Trio`
- Focal population: `151 TH Prkcd Grin2c Glut`
- Endpoint: `n_degs`, the count of measured genes in that target x cell-class contrast with BH-adjusted Wilcoxon `pvals_adj < 0.05`.
- Declared outcome state: `Trio` was absent from the 1,674-row 151-cell-class training count table and was not queried from any same-experiment Trio expression profile.

## Biology used

The canonical biology bundle supports target engagement being biologically plausible in the assay window: `Trio` is expressed in the exact 151 non-target population in 23,586 / 23,679 nuclei, with mean 5.78 CP10k / 9.14 raw UMI, and the 21-28 day P16-to-harvest interval spans many measured neuronal TRIO half-lives. That argues against a pure no-expression or immutable-stock null.

The same bundle also makes the downstream effect hard to transfer from prior mouse phenotypes. TRIO is a multi-pool Rho-family GEF/scaffold, the clearest mouse phenotypes are developmental cortex/hippocampus or embryonic guidance settings rather than acute juvenile thalamic loss, and Kalrn overlap remains an unresolved buffer. I therefore treated TRIO as locally expressed and probably depleted in edited cells, but not as a proteostasis/splicing/core-transcription target expected to enter the high-DEG tail.

## Training measurements used

The 151 training count table is zero-inflated: median `n_degs` is 0, the 75th percentile is 1, only 193 / 1,674 training targets have at least 2 DEGs, and only 106 / 1,674 have at least 10. The mean of 14.05 is dominated by a small stress/regulatory tail, so I did not use it as the anchor for a cytoskeletal RhoGEF.

I chose training perturbations from the proximal Trio mechanism and nearby thalamic structural/guidance biology, then verified their exact 151 Parquet rows. Counts were:

```tsv
candidate	n_degs	interpretation
Kalrn	0	closest paralog
Rac1	0	TRIO Rac effector
Cdc42	1	self-target only
Dcc	0	upstream netrin receptor in the Trio evidence bundle
Tiam1	0	Rac GEF
Dock3	0	Rac-family cytoskeletal GEF
Arhgef9	1	self-target only
Arhgap32	0	Rho-family regulator
Pak1	1	self-target only
Pak2	0	Rac/Cdc42 effector
Pak3	0	Rac/Cdc42 effector
Cyfip1	0	actin/synaptic regulator
Limk1	0	actin regulator
Map1b	1	self-target only
Mapk1	0	signaling effector
Epha4	1	self-target only
Ephb2	0	guidance/synaptic receptor
Robo1	1	self-target only
Robo2	0	guidance receptor
Slit2	0	guidance ligand
```

The Parquet check showed that the six 1-DEG analogs had exactly one significant row and that row was the perturbed transcript itself:

```tsv
candidate	significant_151_feature	logfoldchange	pvals_adj
Arhgef9	Arhgef9	-0.571	3.70e-08
Cdc42	Cdc42	-0.593	8.62e-05
Epha4	Epha4	-1.027	7.88e-32
Map1b	Map1b	-0.358	1.06e-05
Pak1	Pak1	-0.599	5.02e-08
Robo1	Robo1	-0.538	2.72e-06
```

Across the broader selected analog set, the symmetric 151-profile comparison also found no shared significant downstream program: 14 / 20 selected nodes had no significant feature and the remaining 6 were only in the 1-to-9 significant-feature bin described above.

## Synthesis

The close perturbations argue for 0 downstream DEGs in recovered 151 thalamic glutamatergic neurons, despite real cytoskeletal and synaptic biology. For `Trio` specifically, exact local RNA reach is stronger than a no-expression null, and the assay counts the self transcript as one measured gene if it crosses FDR. I therefore forecast a single significant feature, most likely the `Trio` row itself rather than a multi-gene response program.

Point prediction: `1`
