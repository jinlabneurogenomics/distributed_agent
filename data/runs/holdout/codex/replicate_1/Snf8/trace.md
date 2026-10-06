# Snf8 DEG-count forecast

Endpoint: `n_degs` in `151 TH Prkcd Grin2c Glut`, defined as measured genes with BH-adjusted Wilcoxon `p < 0.05`.

Target and declared inputs:

- Target manifest: `[local file: Snf8.csv]`; single target `Snf8`.
- Training count table: `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`; 1,674 training perturbations, excluding `Snf8`.
- Training DE parquet: `[local file: training_de_all_cell_groups.parquet]`.
- Target biology bundle: `[local file: Snf8.json]`, SHA-256 `4216de720e264c5427bb52e0d9b2fd7ce3100ddb550a6d912ed849709ed6759e`.

Biology used:

- The canonical bundle places mouse `Snf8` in cytosolic/endosome ESCRT-II cargo sequestration and multivesicular-body vesicle formation.
- The exact in-assay reach is adequate but not ubiquitous: in the matched non-target `151` nuclei, `Snf8` was detected in 16,160/23,679 cells, with mean log1p CP10K 0.505 and pseudobulk CPM 80.20.
- Functional stock was adjudicated as `likely_substantially_depleted` by harvest because the perturbation stops new supply of a dynamic ESCRT-II subunit used for ongoing endosomal sorting. This is only partially grounded: target-specific SNF8 turnover in postmitotic neurons and a direct 21-28 day timing anchor are absent.
- Human biallelic SNF8 disease, severe fibroblast ESCRT-II subunit loss/autophagy phenotypes, mouse germline lethality, and zebrafish developmental data support importance of the pathway, but they do not prove that an acute P16 thalamic neuronal knockout will generate a broad nuclear RNA response in recovered cells.

Training measurements used:

- The declared `151` count table is sparse: 1,205/1,674 training targets have 0 DEGs; 469 are nonzero; 106 have at least 10; 63 have at least 30; and 43 have at least 100. The median is 0, the mean is 14.05, the 95th percentile is 18, the 97th percentile is 71.48, and the maximum is 2,677.
- Direct or nearby endolysosomal/autophagy/Golgi-traffic anchors in the training table were mixed:
  - `Rab7`: 501 DEGs
  - `Vps54`: 31
  - `Vps35`: 17
  - `Sqstm1`: 1
  - `Chmp4b`, `Lamp2`, `Atg5`, `Atg16l1`, `Vps41`, `Vps53`: 0
- A small signed-rank profile comparison of `Rab7`, `Vps35`, `Vps54`, `Sqstm1`, `Chmp4b`, `Lamp2`, `Atg5`, `Atg16l1`, and `Vps41` in `151` confirmed the same activity structure: 501 significant genes for `Rab7`, 31 for `Vps54`, 17 for `Vps35`, 1 for `Sqstm1`, and none for the other supplied anchors. `Rab7` was directionally correlated with the low/quiet vesicle and autophagy perturbations, but its DEG burden was much larger than the rest of the set, so it is an upper endolysosomal-stress boundary rather than a one-to-one donor for `Snf8`.
- Exact significant rows from the parquet showed that the broad `Rab7` response includes expected late-endosomal/lysosomal and sterol/autophagy markers such as `Sqstm1`, `Lamp2`, `Mcoln1`, `Slc38a9`, `Npc2`, `Grn`, and `Optn`. The lower `Vps35` and `Vps54` responses were real but narrower: `Vps35` had its self transcript plus genes such as `Ptgds` and `Ache`; `Vps54` had a mostly down-shifted immediate-early/neuronal-structure signature led by genes such as `Egr1`, `Rasgrp2`, `Nefm`, `Nefh`, and `Tuba1b`.

Same-experiment corpus context:

- `Snf8` itself had no selected-release Finding or Claim, so there was no target-specific packaged result to transfer.
- Packaged `Rab7` Findings interpret its 151 response as a recurrent late-endosomal/lysosomal compensation and sterol/lipid transcriptional state, with V-ATPase, `Lamp2`, `Mcoln1`, `Dpp7`, lysosomal hydrolase, autophagy, and stress-gene induction.
- The same corpus explicitly treats `Vps35` as a modest thalamic retromer response rather than a bulk lysosomal program, `Vps54` as a 151-restricted GARP response lacking the broader `Rab7` lysosomal/UPR/ISR/proteasome state, and `Chmp4b` as failing to form a robust recurrent ESCRT/autophagy/cargo signature.
- Those same-experiment interpretations are not independent replication of the parquet, but they are useful guards against converting every endolysosomal target into a `Rab7`-scale prediction.

Synthesis:

`Snf8` is a core ESCRT-II subunit with enough focal expression and likely enough 3-4 week functional-stock loss to justify a nonzero forecast above the zero-heavy class prior. The acute postnatal setting and survivor-conditioned nuclei make the severe developmental literature an uncertain magnitude prior, however, and the training measurements show that represented lysosomal, autophagy, retromer, GARP, HOPS, and ESCRT-adjacent perturbations often remained quiet or focal. I therefore weighted `Rab7 = 501` only as proof that a lysosomal compensation state is detectable in this class, and anchored the expected magnitude closer to the active but focal trafficking perturbations `Vps35 = 17` and `Vps54 = 31`.

Point prediction: `31` DEGs.
