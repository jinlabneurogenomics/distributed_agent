Target: Notch3

Predicted n_degs in `151 TH Prkcd Grin2c Glut`: 0

Evidence and reasoning:

- The biology bundle places the perturbation in postmitotic mouse thalamic NeuN-positive neurons with P16 editing and P37-P44 harvest. In Notch3-expressing cells, the 21-28 day window should substantially deplete functional receptor stock because acute editing stops new intact receptor supply and Notch3 receptor domains are actively degradable.
- The same bundle makes the focal-cell reach very weak: Notch3 is localized in mouse neural tissues to vascular mural cells rather than the NeuN-positive neuronal population, and the exact in-assay non-target expression for `151 TH Prkcd Grin2c Glut` is only 72 total Notch3 UMIs across 23,679 nuclei, 61 expressing nuclei, 0.258% expressing, mean CP10K 0.00182, and mean log1p(CP10K) 0.00133.
- The declared `151 TH Prkcd Grin2c Glut` training count table contains 1,674 measured perturbations, excludes Notch3, and is strongly zero-inflated: median 0 DEGs, 75th percentile 1 DEG, 90th percentile 2 DEGs, and 95th percentile 18 DEGs at BH-adjusted Wilcoxon p < 0.05.
- The obvious represented Notch-pathway and Notch-receptor comparators are silent in the exact requested cell group: Notch1, Notch2, Notch4, Adam10, Psen1, and Dll1 each have 0 DEGs in the count table and in the filtered Parquet rows for `151 TH Prkcd Grin2c Glut`.
- Mib1 is the one active Notch-neighborhood outlier in this cell group, with 27 DEGs. The significant Parquet rows are an up-regulated sterol/cholesterol module headed by Insig1, Fdft1, Dhcr24, Ldlr, Msmo1, Hmgcs1, Hmgcr, Cyp51, Lss, and Idi1, not canonical HES/HEY/Nrarp/Dtx Notch-output genes.
- Packaged same-experiment Findings for Adam10, Notch1, Notch2, Psen1, and Mib1 independently interpret those measured surfaces the same way: represented Notch receptors, Dll1, Adam10, and Psen1 do not form a shared postnatal neuronal Notch RNA module; Mib1's response is a recurrent SREBF2-like sterol program that does not collapse onto receptor or protease perturbations.

Synthesis:

Functional Notch3 loss is plausible where Notch3 is present, but the assayed thalamic neuronal population has almost no Notch3 transcript and the closest receptor/cleavage perturbations are all zero in this same endpoint. The sole nonzero Notch-neighborhood comparator, Mib1, points to a distinct sterol state rather than receptor loss. With a zero-centered training distribution and no evidence for a Notch3-specific neuronal program in the reachable focal cells, the most likely BH < 0.05 DEG count is 0.
