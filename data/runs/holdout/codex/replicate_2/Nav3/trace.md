target_name: Nav3
cell_group: 151 TH Prkcd Grin2c Glut
predicted_n_degs: 1

Evidence used

- The declared holdout manifest contains the single target `Nav3`.
- The exact focal-population expression card shows that `Nav3` is assayed and well expressed in this population: 22,647 / 23,679 non-target cells expressed it, 95.6417% of cells were positive, mean raw UMI was 4.3937, and pseudobulk expression was 275.37 CPM. This supports target reach in recovered thalamic neurons but was used only as reach/QC context, not as an editing-efficiency scalar.
- The canonical Nav3 biology bundle describes NAV3 as a large microtubule-associated neuron-navigator protein that binds/stabilizes microtubules. Its strict postnatal P16-to-P37/P44 realization is unresolved: disrupting the locus should stop new full-length NAV3 supply, but existing protein and cytoskeletal organization are not removed instantly, no target-specific turnover clock was found, and the only loss phenotypes were human developmental genetics plus embryonic zebrafish knockdown rather than a postnatal mouse-thalamus experiment.
- Deterministic training-universe analog nomination found no training-available exact paralog, exact complex/module, or bidirectional same-experiment corpus analog for `Nav3`. All nominated available genes were broad fallback links, with the highest-priority communities centered on positive regulation of microtubule polymerization, negative regulation of microtubule depolymerization, microtubule binding, and microtubule cytoskeleton organization.
- The full declared count table for this cell group has 1,674 training perturbations; 1,205 are zero, 469 are positive, 106 are >=10, 59 are >=50, 15 are >=500, and 3 are >=1000. That puts the unconditional mode and median at 0 with a long right tail.
- The closest broad microtubule nominees were low-yield in the same 151 TH Prkcd Grin2c Glut endpoint:
  - top 10 analog nominations: median 1 DEG, max 75, only `Dctn1` >=10;
  - top 20 analog nominations: median 1 DEG, 7/20 equal 0, 12/20 in the 0-1 range, max 75;
  - top 30 analog nominations: median 1 DEG, 14/30 equal 0, only `Dctn1` >=10.
- Individual leading analog counts were `Map1b` 1, `Mapt` 1, `Dctn1` 75, `Fgf13` 2, `Camsap1` 0, `Hdac5` 0, `Atxn7` 0, `Taok1` 0, `Kif5a` 1, `Kif5c` 1, `Tuba1a` 7, `Kif1a` 1, `Tubb5` 1, `Mapre2` 1, `Tubb4b` 1, `Kif3b` 0, `Kif2a` 0, `Stmn2` 1, `Map6` 0, and `Kif21a` 1.
- In the exact GO:0031116 positive-regulation-of-microtubule-polymerization target set available to training for this cell group, the observed counts were `Akap9` 0, `Dctn1` 75, `Map1b` 1, `Mapt` 1, and `Rac1` 0. `Nav3` is in that GO set but is withheld.
- A symmetric profile comparison of the top 20 microtubule nominees in the exact `151 TH Prkcd Grin2c Glut` Parquet rows produced 7 nodes with no FDR-significant features, 12 with 1-9 features, and only one, `Dctn1`, with at least 50 features. Across all 190 within-cohort pairs, the FDR-significant program-overlap coefficient was 0 wherever defined, so the broad shared cytoskeletal biology did not correspond to a shared FDR-supported expression module.
- Direct Parquet checks showed that the one-DEG analogs `Map1b`, `Mapt`, `Kif5a`, `Kif5c`, `Kif1a`, `Tubb5`, `Mapre2`, `Tubb4b`, `Stmn2`, and `Kif21a` each called only their own target transcript at FDR < 0.05. `Tuba1a` called a small tubulin-family set of 7. `Dctn1` called 75 genes, but its significant sterol/lipid/membrane trafficking program did not recur as a significant shared program with the quieter microtubule genes, so I treated it as an upward boundary rather than the central Nav3 scale.

Synthesis

`Nav3` has excellent focal expression, so a solitary self-transcript detection is plausible even if postnatal downstream biology is weak. The biological prior does not support a large response: the available Nav3 loss evidence is developmental or orthologous, strict functional stock by harvest is indeterminate, and no exact training paralog or complex mate is available. The task-matched training evidence around the nearest microtubule fallbacks sits at 0-1 DEGs for most candidates, with `Dctn1` as a nonrecurrent outlier. I therefore placed Nav3 just above the screen-wide zero mode, at a single detectable DEG.
