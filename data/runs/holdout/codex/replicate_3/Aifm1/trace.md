# Aifm1 DEG-count forecast

Target: `Aifm1`

Population: `151 TH Prkcd Grin2c Glut`

Predicted `n_degs`: `0`

## Evidence used

- The manifest target is `Aifm1`.
- The declared Aifm1 biology bundle was the only target-specific biology used. It contains no target outcome. In the exact focal population, the Aifm1 transcript is measured and present in 15,067 of 23,679 non-target nuclei, with mean CP10K 0.714 and 63.6% of non-target nuclei expressing the feature, so the perturbation is not excluded by lack of baseline RNA in this cell class.
- The functional-stock card adjudicates AIFM1 as a renewable mitochondrial flavoprotein pool needed for respiratory-complex maintenance. A null-like P16 edit is expected to stop new AIFM1 supply while initially sparing mature mitochondrial AIFM1 and already assembled respiratory material; inducible mouse-cell evidence and mouse-brain protein-turnover evidence make substantial decline by the P37-P44 harvest plausible but not immediate or certain in postmitotic thalamic neurons.
- The same card separates that constitutive mitochondrial pool from stress-released AIFM1 apoptosis biology. Adult neural phenotypes exist for strong Aifm1 hypomorphism, but the closest direct timed depletion series was in proliferating fibroblasts and the Harlequin neural phenotype is late and region-selective, so the bundle supports a reachable effect but not a large short-window thalamic transcriptional footprint.
- The requested thalamic training count table is zero-heavy: among 1,674 training perturbations, 1,205 have `n_degs = 0`, the median is 0, the mean is 14.1, and only 43 exceed 100 DEGs.
- I used respiratory-chain and mitochondrial-maintenance training genes as the main quantitative analogues because AIFM1 loss impairs complex-I/respiratory-chain maintenance indirectly. In the count table plus Parquet rows for `151 TH Prkcd Grin2c Glut`, 41 selected mitochondrial/OXPHOS perturbations had this distribution:
  - 23 with 0 DEGs, including `Clpp`, `Cox4i1`, `Cox6a1`, `Cox7b`, `Cox8a`, `Lonp1`, `Ndufa11`, `Ndufa12`, `Ndufa8`, `Ndufa9`, `Ndufaf2`, `Ndufaf4`, `Ndufaf5`, `Ndufb3`, `Ndufb7`, `Ndufs4`, `Ndufs7`, `Ndufv1`, `Timmdc1`, `Uqcrb`, `Uqcrfs1`, and `Uqcrh`;
  - 17 with 1 DEG, including complex-I, complex-II, complex-III, complex-IV, TOM, and oxidative-stress genes such as `Ndufs2`, `Ndufs8`, `Ndufa10`, `Ndufb10`, `Sdha`, `Uqcrc2`, `Cox5a`, `Tomm40`, and `Park7`;
  - only `Opa1` above one DEG, at 37.
- The Parquet significant rows showed that many of the one-DEG OXPHOS profiles were just a significant self-transcript row, while direct complex-I assembly or subunit perturbations such as `Ndufs4`, `Ndufs7`, `Ndufv1`, `Ndufaf2`, `Ndufaf4`, `Ndufaf5`, `Ndufa8`, and `Ndufa9` had no significant measured gene in this population.

## Synthesis

Aifm1 is expressed in the focal non-target nuclei and its mitochondrial stock should be perturbed by the 3-4 week assay window, so I did not treat it as biologically inaccessible. The quantitative scale, however, is anchored by the observed behavior of respiratory-chain perturbations in the same thalamic population: nearly all selected direct complex-I/III/IV, TOM, and mitochondrial-proteostasis knockouts produced either 0 or a lone significant row, and the lone larger mitochondrial-dynamics comparator, `Opa1`, is mechanistically more prone to an integrated-stress transcriptome than an AIFM1-maintenance lesion with residual pre-edit respiratory complexes.

That puts the expected total count at the zero/one floor. Because direct complex-I/assembly perturbations were often exactly zero and AIFM1 loss is indirect, delayed by protein and complex turnover, and observed only in recovered survivor nuclei, I placed the point at `0` rather than `1`.
