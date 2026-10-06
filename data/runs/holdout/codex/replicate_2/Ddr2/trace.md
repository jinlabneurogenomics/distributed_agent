# Direct forecast for Ddr2 in 151 TH Prkcd Grin2c Glut

## Prediction

- `target_name`: `Ddr2`
- `predicted_n_degs`: `0`

## Evidence used

- The held-out manifest contains only `Ddr2`; `Ddr2` is absent from the declared `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` table, so the forecast used only other measured training perturbations.
- The canonical biology bundle reports exact focal-population Ddr2 reach of `129 / 23679` non-target nuclei expressing Ddr2, or `0.5447865%`, with `161` Ddr2 UMIs total and `0.4261` pseudobulk CPM. This is extremely sparse expression in the assayed recovered thalamic neuronal class.
- The same canonical bundle judged DDR2 functional stock as likely substantially depleted by the P37-P44 harvest after a P16 disruptive edit, because DDR2 is a renewed cell-surface collagen receptor and the closest target-specific chase data place mature-receptor persistence around a day rather than weeks. That supports target engagement at harvest but does not by itself predict a broad snRNA response.
- The same bundle did not establish a postnatal neuronal Ddr2 requirement: known effective mouse loss is dominated by systemic, skeletal, fibroblast, craniofacial, and cardiac phenotypes; the baseline neural expression evidence is weak once the exact in-assay reach is considered; Ddr1 is a related collagen receptor but no same-context compensation test is available.
- The selected same-experiment corpus release has no Ddr2 Findings, Claims, or explicit Finding-reference links, so it contributed no Ddr2 endpoint observation.
- In the declared focal count table, the global distribution is zero-heavy: `1205 / 1674` training targets have `n_degs = 0`, the median is `0`, the 75th percentile is `1`, the 90th percentile is `2`, and the mean is inflated to `14.05` by a small tail of essential RNA-processing/proteostasis regulators.
- The closest receptor/ECM training perturbations were quiet in this exact population. The collagen/integrin group I used (`Col11a1`, `Col2a1`, `Itga2`, `Itga2b`, `Itga4`, `Itga6`, `Itga7`, `Itga8`, `Itga9`, `Itgb1`, `Itgb2`) had `0` DEGs for every member. A broader receptor-tyrosine-kinase-like group of 31 training genes had only 4 DEGs total, with a median of `0` and a maximum of `3`; the only nonzero members were `Ntrk2` with `3` and `Epha4` with `1`. A protein-tyrosine-phosphatase receptor group had only three one-DEG responses across eight targets.
- Direct Parquet aggregation for those 50 receptor/ECM comparators in `151 TH Prkcd Grin2c Glut` confirmed that all 17,259 measured rows per selected target were present and that only 7 of the 862,950 selected measured-gene contrasts crossed BH-adjusted `p < 0.05`.

## Reasoning

Ddr2 should lose functional receptor stock over the 21-28 day CRISPR window if edited, but the assayed aggregate contains very little Ddr2-expressing target transcript: only about half a percent of recovered non-target nuclei express it at baseline. The card supplies no matching evidence that juvenile thalamic neurons require DDR2 strongly enough to overcome that sparse reach, and the closest focal training perturbations are collagen, integrin, receptor-tyrosine-kinase, or receptor-phosphatase genes whose measured DEG counts are almost all exactly zero. I therefore placed Ddr2 at the zero mode of the focal training distribution rather than near the heavy-tailed training mean or the high-response regulatory genes.

Point forecast: `0` DEGs.
