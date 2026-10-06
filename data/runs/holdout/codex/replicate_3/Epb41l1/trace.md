# Direct forecast trace

## Target and endpoint

- Target: `Epb41l1`.
- Endpoint: `n_degs`, the number of measured genes in `151 TH Prkcd Grin2c Glut` with BH-adjusted Wilcoxon `p < 0.05`.
- Declared training table: `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
- Declared profile table: `training_de_all_cell_groups.parquet`.
- Canonical target bundle: `Epb41l1.json`, biology-only view; it exposed no target outcome or labeled-neighbor outcome.

## Biology that anchored the forecast

The canonical Epb41l1 bundle supports a real but fairly local synaptic-scaffold perturbation, not a broad loss of an RNA-processing, proteasome, or transcriptional core factor. Its selected operation fact places 4.1N at neuronal membrane-cytoskeleton and postsynaptic receptor organization/trafficking. The stock card calls the harvest stock `likely_substantially_depleted`: a 7.46 day neuronal-culture protein half-life spans roughly three to four half-lives over the 21-28 day P16-to-P37/P44 interval. The bundle still leaves thalamic pool persistence, isoform escape, paralog buffering, and the thalamic match of reported hypothalamic/hippocampal phenotypes unresolved.

The exact focal expression reach argued that the target can be assayed but is not ubiquitous:

- `n_non_target_cells`: 23,679
- `n_cells_expressing`: 9,910
- `pct_cells_expressing`: 41.8514
- `mean_cp10k`: 0.4340
- `pseudobulk_cpm`: 44.2624

I therefore expected either no significant row or a solitary target/self-like row, rather than a large survivor-state transcriptional program.

## Training measurements that set scale

The declared count table has 1,674 training perturbations in the focal class. Its distribution is extremely sparse: 1,205/1,674 are zero, 276 are one, the median is 0, the 75th percentile is 1, and the 90th percentile is 2; large DEG burdens are a long tail.

Because the direct protein 4.1 paralogs were absent from the focal training universe, I used typed offline analog nomination to find training-available receptor-scaffold and cytoskeleton comparators. The strongest specific Epb41l1 communities were AMPA-receptor trafficking, AMPA-receptor/synaptic-plasticity, neurexin/neuroligin, and related postsynaptic modules; `Gria1` and `Rdx` were the only direct STRING-physical fallbacks in the bounded leading communities. Epb41l1 itself was absent from the same-experiment ledger, so no Epb41l1 profile or outcome was exposed through that step.

A matched Parquet profile comparison over 20 nominated perturbations in `151 TH Prkcd Grin2c Glut` found 10 with no significant features, 8 with 1-9, and only 2 with at least 50. The close scaffold/receptor-trafficking set excluding the broad outliers `Elp1` and `Grin1` was concentrated at 0-1 DEGs:

| perturbation | n_degs | interpretation |
| --- | ---: | --- |
| `Dlg4` | 1 | AMPA/NMDA postsynaptic scaffold; only self row significant |
| `Gria1` | 0 | direct AMPA receptor partner |
| `Camk2g` | 0 | AMPA trafficking/plasticity module |
| `Prkca` | 0 | AMPA trafficking/plasticity module |
| `Prkcg` | 1 | module comparator; only self row significant |
| `Camk2a` | 0 | module comparator |
| `Camk2b` | 1 | module comparator; only self row significant |
| `Cacng2` | 0 | AMPA trafficking auxiliary subunit |
| `Nsf` | 0 | AMPA receptor trafficking factor |
| `Myo6` | 0 | actin/receptor trafficking |
| `Nrxn1` | 1 | synaptic adhesion/module comparator; only self row significant |
| `Nrxn3` | 0 | synaptic adhesion/module comparator |
| `Cplx1` | 1 | neurotransmitter-release comparator; only self row significant |
| `Rdx` | 1 | direct physical cytoskeletal fallback; only self row significant |
| `Add2` | 0 | membrane-cytoskeleton fallback |
| `Actg1` | 1 | actin fallback; only self row significant |
| `Gphn` | 0 | postsynaptic scaffold, weaker lane match |
| `Grin2b` | 2 | glutamate receptor comparator |

`Elp1` had 645 DEGs and a stress/amino-acid response program, and `Grin1` had 89 DEGs led by the receptor self transcript. I treated those as upper boundaries for broader synaptic dysfunction rather than the center for a 4.1N scaffold loss, because Epb41l1 has neither Elp1's generic cellular role nor the direct ionotropic-receptor role of Grin1.

## Point synthesis

The closest endpoint-matched evidence supports a very small count: the median of the curated receptor/scaffold cohort is 0, the one-DEG cases are mostly just target self-transcript detections, and the cohort's Parquet signatures do not define a recurrent high-DE program that should be transferred to Epb41l1. The biology bundle nevertheless puts Epb41l1 in the assayed class, predicts substantial depletion of a renewable postsynaptic scaffold by harvest, and shows enough focal mRNA reach for one significant self or immediate scaffold-linked row to be plausible.

I therefore chose `1` as the integer forecast: a small bump over the zero-centered close-comparator distribution, while staying far below the high-response outliers.
