# Nr2f2 direct DEG-count forecast

Target and endpoint:

- Target: `Nr2f2`
- Cell class: `151 TH Prkcd Grin2c Glut`
- Endpoint: count of measured genes with BH-adjusted Wilcoxon `p < 0.05`
- Forecast: `2`

Evidence used:

- Declared target biology bundle, served through `characterization_bundle(target="Nr2f2", view="biology")`; its serving metadata reported `target_outcome_exposed=false` and `labeled_neighbors_exposed=false`.
- Declared focal training count table, `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
- Declared all-cell training Parquet, `[local file: training_de_all_cell_groups.parquet]`, queried only for matched `151 TH Prkcd Grin2c Glut` rows of training perturbations.
- Deterministic `Nr2f2` analogue nomination from curated mouse annotations, with the 1,674-row training count table as the explicit availability universe, written to `evidence/nr2f2_analog_nominations.jsonl`.
- Matched profile comparison among the close nuclear-receptor and MEF2/NR2F2-complex nominees, written to `evidence/nr2f2_profile_compare.json` and inspected through `evidence/nr2f2_profile_inspect.json`.

The `Nr2f2` card makes a downstream transcriptional response biologically reachable but not guaranteed in this acute postnatal assay. `Nr2f2` is a nuclear-receptor DNA-binding transcription factor, not an installed structural product, and the exact in-assay reach was substantial: in the focal matched non-target population, 12,024 of 23,679 nuclei expressed `Nr2f2` with 0.714 mean CP10K and 74.8 pseudobulk CPM. Against that, a P16 edit stops new NR2F2 production but does not directly remove already synthesized receptor, the card found no constitutive mouse-neural NR2F2 half-life or chromatin-residence clock, and the direct mouse neural phenotypes came from developmental cerebellar or hippocampal deletion rather than an acute juvenile thalamic knockout. I therefore treated `Nr2f2` as an expressed transcriptional regulator with plausible but weak short-window realization.

The training endpoint distribution in this cell class argues for a very low count unless the target has a known class-state footprint. Among 1,674 visible training targets, 1,205 had zero DEGs, the median was 0, the 75th percentile was 1, the 90th percentile was 2, and only 103 targets exceeded 10 DEGs. Thus even a forecast of two genes is already at the 90th percentile of the focal training table.

The most relevant curated comparators also stayed in the near-null regime. In the nuclear-receptor WikiPathways set, excluding the held-out `Nr2f2`, 27 of 33 available training genes had zero focal-class DEGs and 29 of 33 had at most two; among the close `Nr2` nuclear receptors, `Nr2f1` had 2, `Nr2c2` had 3, and `Nr2f6`, `Nr2c1`, `Nr2e1`, and `Nr2e3` had 0. The broader deterministic `Nr2f2` nominee list behaved similarly: the first 30 training-available analogues had median 0, 24 zeros, and 25 of 30 at no more than two DEGs.

The declared Parquet profile rows confirmed that the close analogues were not hiding broad subthreshold activity. In the matched class, `Nr2f1` had only two FDR-significant genes, `Nr2c2` had three, `Mef2a` had four, and the zero-count receptors such as `Rxra`, `Pparg`, `Nr3c1`, and `Esr1` had no FDR-significant genes. `Rora` was the clear nuclear-receptor outlier at 278 DEGs, with a signed marker-state program including `Prkcg`, `Prkcd`, and `Grin2c`, but it is a different subfamily member with a realized large thalamic class-state response rather than the closest COUP-TF/Nr2f analogue.

Synthesis:

`Nr2f2` expression in roughly half of focal thalamic nuclei moves the forecast above a strict null, and single `Nr2f2` loss is not completely buffered by `Nr2f1` in developmental hippocampal evidence. The stronger quantitative cue, however, is that the nearest measured nuclear-receptor comparators are mostly zero-to-three DEGs in exactly the requested class, with `Nr2f1` itself at two, while the biology card leaves the 21-28 day functional-stock depletion unresolved. I therefore predicted the small nonzero analogue scale rather than the `Rora` outlier scale or the whole-table mean.
