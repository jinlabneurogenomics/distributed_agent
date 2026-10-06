# Lyst DEG-count forecast

Target and endpoint:

- Target: `Lyst`.
- Focal population: `151 TH Prkcd Grin2c Glut`.
- Endpoint: count of measured genes with BH-adjusted Wilcoxon `p < 0.05`.
- The prediction below does not use a Lyst perturbation signature, a Lyst observed DEG count, labeled-neighbor outcomes, or endpoint-selection metadata.

Biology that set the prior:

- The declared Lyst biology bundle places LYST on lysosome fission / autophagic lysosome reformation: LYST is recruited to LAMP1-positive organelles and its loss can impair lysosomal and autolysosomal membrane scission.
- The focal population expresses the target transcript, but not at an especially high level: `Lyst` was detected in `13941 / 23679` non-target nuclei, with `mean_raw_umi = 0.9933`, `mean_cp10k = 0.6288`, and `pct_cells_expressing = 58.875`.
- Functional realization by P37-P44 is unresolved. A disruptive P16 edit should stop new LYST synthesis while pre-existing protein may initially persist; no quantitative neuronal LYST protein half-life is known, and mouse neural phenotypes in germline Lyst models emerge months later and mainly outside the thalamic context. That makes a broad acute thalamic survivor-state RNA response possible but not the leading expectation.

Training measurements that set the local scale:

- The declared `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` table is very sparse: `1205 / 1674` training targets have `n_degs = 0`; the median is `0`, the 75th percentile is `1`, the 90th percentile is `2`, and only `43` targets reach `100` or more DEGs.
- Same-experiment Claim summaries for represented lysosomal, V-ATPase, autophagy, NCL, hydrolase/cargo, and endolysosomal-trafficking perturbations report that these perturbations were usually flat, divergent, or restricted rather than a common lysosomal-stress module. Material provenance: `claim:9ba3289b451540e57545` for autophagy/lysosome non-interchangeability, `claim:56e1e77cd2cb9bb6604f` for represented lysosomal disease genes lacking a shared acute lysosomal-stress / autophagy / TFEB / ISR program, `claim:d08f04d8507bae4de40b` for V-ATPase subunit specificity, `claim:726468d7afc216bc3be2` for Rab7 as a selective late-endosomal / lysosomal compensation positive control, and `claim:a251c65f7a3f32088f68` for detectable Rab7/Vps35 trafficking responses contrasting with flat `Vps35l` and `Washc4`. The `Nbea` training target was a direct BEACH-family comparator from the Lyst bundle; `Nbea:F001` and `Nbea:F003` reported a pan-null nuclear-transcriptome surface and no convergence with BEACH-family or data-driven comparators.
- In a manually chosen 21-target focal-class profile cohort spanning core autophagy genes, lysosomal hydrolase/cargo targets, V-ATPase components, late-endosomal/trafficking targets, and the BEACH-family comparator `Nbea`, the 151 TH count table gave:
  `Atg5 0`, `Becn1 0`, `Rb1cc1 4`, `Gnptab 0`, `Manba 0`, `Ppt1 1`, `Psap 1`, `Tmem106b 1`, `Atp6v0a1 1`, `Atp6v1a 0`, `Atp6v1e1 0`, `Vps41 0`, `Vps35l 0`, `Washc4 0`, `Rab7 501`, `Depdc5 13`, `Nbea 0`, `Lamp2 0`, `Rubcn 0`, `Gaa 1`, `Sort1 0`.
- The direct Parquet profile over those same 21 targets in `151 TH Prkcd Grin2c Glut` produced 13 no-significant-feature perturbations, 6 with only 1-9 significant features, 1 with 10-49, and only Rab7 with at least 50. Excluding the Rab7 high-response outlier left 22 DEGs across 20 comparator perturbations, mostly isolated self-transcript hits.

Synthesis:

Lyst is expressed enough in the focal nuclei that a self-transcript hit is possible, but the available biology does not make rapid nuclear compensation in thalamic neurons likely: the operative protein stock at harvest is indeterminate, long-horizon neural evidence is cerebellar/peripheral rather than acute thalamic, and the closest represented training perturbations are mostly transcriptional nulls in this focal class. I therefore use the modal outcome of the matched lysosome/autophagy/trafficking neighborhood, not the Rab7 tail, as the point forecast.

Predicted `n_degs`: `0`
