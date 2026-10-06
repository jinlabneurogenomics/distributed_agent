# Clcn5 direct n_degs forecast

Target: `Clcn5` in `151 TH Prkcd Grin2c Glut`.

Endpoint: `n_degs`, the count of measured genes in the focal perturbation contrast with BH-adjusted Wilcoxon `p < 0.05`.

## Evidence that set the scale

- The declared holdout target is `Clcn5`; it is absent from the declared `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` training count table.
- In the exact focal expression reach supplied with the biology bundle, `Clcn5` is detected in 6,645 of 23,679 matched non-target nuclei in `151 TH Prkcd Grin2c Glut`, 28.06%, with mean CP10k 0.226 and pseudobulk CPM 22.74. This makes the transcript measurable but not broadly/highly expressed across the class.
- The biology bundle supports ClC-5 as a renewable endosomal chloride/proton exchanger whose functional stock should probably be substantially depleted by the P37-P44 harvest after a P16 disruptive edit. The direct loss phenotype in the bundle is renal proximal-tubule endocytosis, not a thalamic neuronal requirement, and the bundle leaves postnatal neural relevance, phenotype latency, and neural redundancy unresolved.
- The focal count table is strongly zero-inflated: 1,205 of 1,674 training targets have `n_degs = 0`, the median is 0, the 75th percentile is 1, and the 90th percentile is 2.

## Measured focal analogs

The closest represented acidification/chloride neighbors in the same focal count table were all quiet or nearly quiet:

| training perturbation | 151 TH n_degs |
| --- | ---: |
| Clcn3 | 0 |
| Clcn4 | 1 |
| Slc9a7 | 1 |
| Slc9a9 | 0 |
| Atp6v0a1 | 1 |
| Atp6v1a | 0 |
| Atp6v1b2 | 0 |
| Atp6v1e1 | 0 |
| Atp6ap2 | 2 |
| Lamp2 | 0 |
| Ocrl | 0 |

In the raw focal Parquet rows, several one-DEG analogs were self-only or essentially self-only events: `Clcn4`, `Atp6v0a1`, `Ctsb`, `Dnajc5`, and `Slc9a7` each had exactly one significant feature in `151 TH Prkcd Grin2c Glut`, while `Clcn3`, `Lamp2`, `Ocrl`, `Lrp2`, `Atp6v1a`, and `Atp6v1b2` had none. A profile comparison across 13 hand-selected endosomal/chloride/vesicle candidates found no significant Clcn3 features and only one negative Clcn4 feature, while the broad `Rab7` signature was 501 genes and the modest `Vps35` profile was 17 genes.

The broader trafficking responders set an upper boundary rather than a scale match. `Vps35`, `Vps54`, and especially `Rab7` can cross the FDR gate in this cell class, with 17, 31, and 501 DEGs respectively, so the assay can detect strong endolysosomal stress. The same-experiment Rab7 and Vps35 findings, however, interpreted the Rab7 response as a large late-endosomal/lysosomal compensation and proteostasis state that most HOPS, retromer, WASH, V-ATPase, and lysosomal targets failed to phenocopy at FDR level. The Clcn4 finding likewise anchored a same-experiment claim that represented ClC, NHE, and V-ATPase acidification perturbations did not form a conserved neuronal snRNA-seq module.

## Synthesis

`Clcn5` is expressed in a minority but material fraction of focal nuclei, and the intended perturbation should eventually deplete newly synthesized ClC-5. That supports the possibility of a measurable self-target transcript change. The best scale evidence, though, is the matched training behavior of endosomal acidification genes: the direct `Clcn3`/`Clcn4` CLC comparators and nearby NHE/V-ATPase genes cluster at 0-2 DEGs rather than at the 17-501 DEG retromer/Rab7 scale. Because the bundle provides no direct thalamic neuronal phenotype for Clcn5 and the measured acidification relatives are buffered, I expect no broad downstream program and at most a self-only call.

Point forecast: `1` significant gene.
