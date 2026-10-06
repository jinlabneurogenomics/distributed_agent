# Chrna5 direct DEG-count forecast

## Endpoint and target

- Target: `Chrna5`
- Cell class: `151 TH Prkcd Grin2c Glut`
- Endpoint: `n_degs`, the number of measured genes in the focal class with BH-adjusted Wilcoxon `p < 0.05`
- Point forecast: `0`

## Evidence used

1. The declared one-row manifest names `Chrna5`, and `Chrna5` is absent from the declared 1,674-row training count table for `151 TH Prkcd Grin2c Glut`. The training table is therefore usable only through other measured perturbations.

2. The canonical Chrna5 biology bundle reports exact focal-population reach but no target endpoint outcome. In non-target nuclei from `151 TH Prkcd Grin2c Glut`, Chrna5 was detected in only 129 of 23,679 nuclei, with 180 total UMIs, 0.545% expressing nuclei, and 0.476 pseudobulk CPM. I treated this exact in-assay reach as the strongest quantitative downward bearing, because the DE contrast is aggregated across the whole thalamic class.

3. The same bundle describes Chrna5 as an accessory alpha5 subunit of assembled heteromeric nicotinic acetylcholine receptors. Adult germline alpha5 loss has neural functional effects and alpha5-independent receptor complexes do not erase all alpha5-dependent function, so the perturbation is biologically capable of mattering. The stock adjudication, however, places the P37-P44 harvest in a partially depleted or leading-edge regime: a P16 edit stops new alpha5 supply but can leave pre-existing assembled receptors functional, and target-specific turnover in juvenile mouse thalamic neurons is unknown.

4. I used represented nicotinic receptor subunits as the closest hand-selected training comparators, because they share the ligand-gated receptor-subunit operation without requiring any endpoint labels for Chrna5. Their focal training counts were:

   `Chrna2:0`, `Chrna3:0`, `Chrna4:2`, `Chrna6:0`, `Chrna7:0`, `Chrnb2:1`, `Chrnb3:0`.

   Including the additional represented muscle-biased receptor genes did not change the pattern: `Chrna1`, `Chrnb1`, `Chrnd`, `Chrne`, and `Chrng` were also zero.

5. I checked the declared differential-expression Parquet in the exact focal class for these nicotinic comparators. Each had 17,259 measured genes. Only `Chrna4` and `Chrnb2` had any FDR-significant rows: `Chrna4` had its own transcript and `Cyp46a1`; `Chrnb2` had only its own transcript. `Chrna3`, `Chrna7`, and the other receptor subunits had no significant measured genes in this class. Same-experiment corpus summaries for those measured training targets describe the same boundary: `Chrna3` and `Chrna7` were buffered/null, `Chrnb2` was a self-transcript event rather than a downstream transcriptome event, and `Chrna4` had one isolated downstream responder rather than a shared cholinergic program.

## Synthesis

Chrna5 has enough external and packaged biology to make a nonzero effect possible in some alpha5-bearing postnatal neuronal context, but three details push the focal single-nucleus count to the floor:

- Chrna5 RNA reach in the assayed thalamic aggregate is far below 1% of non-target nuclei, so even a real cell-autonomous alpha5-loss state would be strongly diluted in the class-level contrast.
- Alpha5 acts through a pre-assembled membrane receptor pool whose depletion 21-28 days after P16 editing is expected to be partial or only emerging, not an immediate collapse of receptor function in every edited cell.
- Principal represented nicotinic receptor perturbations in this same class were transcriptionally quiet: even `Chrna4` and `Chrnb2` produced only two and one significant rows, respectively, dominated by the self transcript or a single isolated sentinel rather than a multi-gene downstream program.

The all-target training distribution is already sparse in this cell class, with a zero median, but the forecast was driven by the stronger family-specific evidence above. I therefore chose the floor of the plausible count range.
