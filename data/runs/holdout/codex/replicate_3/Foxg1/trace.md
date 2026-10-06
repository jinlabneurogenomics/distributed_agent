# Foxg1 direct `n_degs` forecast

## Target and endpoint

- Target: `Foxg1`, from the one-row holdout manifest `Foxg1.csv`.
- Cell group: `151 TH Prkcd Grin2c Glut`.
- Endpoint: count of measured genes in that focal group with BH-adjusted Wilcoxon `p < 0.05`.
- Point forecast: `0`.

## Evidence used

The declared biology bundle, `biology_bundles/Foxg1.json` with SHA-256 `995e59d134ee1048835a5039539d5ad766e72bf16967aa535dc5e8b2ae066d1c`, was the primary target prior. FOXG1 is a nuclear forkhead DNA-binding transcriptional regulator; other postnatal or postmitotic mouse neuronal systems show phenotypes after Foxg1 loss or knockdown well within the 21-28 day Perturb-seq window, and the bundle concluded that functional FOXG1 stock is likely substantially depleted in successfully edited Foxg1-expressing cells by harvest. Those facts argue against protein persistence, paralogy, or a slow loss-of-function clock as the main reason for a null.

The same bundle also gave the decisive focal-population reach. In non-target nuclei from `151 TH Prkcd Grin2c Glut`, Foxg1 RNA was detected in only 2,151 of 23,679 nuclei, `9.083998479665526%`, with mean raw UMI `0.13594324084631954`, mean log1p CP10k `0.051452107245709165`, and pseudobulk CPM `8.520044975356146`. Its curated literature card recorded an affirmative thalamic mismatch: Foxg1 is a telencephalic factor and was reported as not expressed in mouse thalamus, with later heterozygote thalamic anatomy interpreted as indirect cortex-thalamus effects. Exact same-assay reach supersedes that qualitative call but preserves the same direction: most nuclei in this thalamic glutamatergic aggregate should not be directly Foxg1 dependent.

The selected July same-experiment corpus had no Foxg1 entry: `target_context(Foxg1)` returned zero Findings, zero Claims, and zero explicit references, and `related_targets(Foxg1, basis=explicit_finding_reference)` returned zero related targets. Thus no packaged same-experiment Foxg1 report or report-derived comparator was available.

I therefore nominated training-available analogs from typed offline annotations and the selected corpus release, writing `evidence/foxg1_analog_nominations.jsonl`. Foxg1 itself was absent from the 1,674-target training universe. The strongest exact or narrow nominees were not other forkhead genes with matching thalamic expression; they were FOXG/FOXO/SMAD transcriptional-module partners:

| nominee | nomination basis | observed `n_degs` in `151 TH Prkcd Grin2c Glut` |
|---|---|---:|
| Smad3 | projected SMAD3-SMAD4-FOXO3-FOXG1 complex; FOXO-mediated transcription | 0 |
| Smad4 | projected SMAD3-SMAD4-FOXO3-FOXG1 complex; FOXO-mediated transcription | 0 |
| Smad2 | FOXO-mediated transcription narrow module | 1 |
| Ep300 | FOXO/FoxO signaling narrow modules | 0 |
| Ywhaz | FOXO-mediated transcription narrow module | 1 |
| Akt3 | FOXO/FoxO signaling narrow modules | 0 |

Broader developmental/neural transcription-factor candidates in the leading nomination tranche were also almost all quiet in the declared focal count table: among the top 40 nominees, 32 had `0` DEGs and 6 had exactly `1`. `Ctnnb1` was the one strong outlier at `383`, but it came through broad Wnt/neuroblast-proliferation annotations, not a Foxg1-specific operative match, so I treated it as evidence that the cell group can show a large response for a broad active pathway rather than as a scale donor for low-reach Foxg1 loss.

The direct Parquet profile comparison of the top 30 nominees in `151 TH Prkcd Grin2c Glut` wrote `evidence/foxg1_profile_compare.json`. Its focal BH-significant feature counts were: 21/30 nominees with no significant features, 8/30 with 1-9 significant features, and only 1/30 with at least 50, the same broad `Ctnnb1` outlier. An exact inspection of the specific SMAD/FOXO nominees confirmed `Smad3=0`, `Smad4=0`, `Smad2=1`, `Ep300=0`, while `Ctnnb1=383`.

The report-derived topology audit of the top 20 nominees in the July release found the specific `Smad2`, `Smad3`, `Smad4` triad as a fully connected explicit-Finding component, but that whole component was empirically null to near-null in the focal count table. Other broad neural-development candidates formed a looser 13-node component; several nominees were isolated. I did not interpret topology density as an endpoint score.

For calibration against the whole supplied count table, the 1,674 training perturbations in `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` are zero-inflated: 1,205 have `0` DEGs, 276 have `1`, the median is `0`, and the 75th percentile is `1`.

## Synthesis

Foxg1 has a credible loss-of-function operation and should lose functional protein within the perturbation window wherever it is normally needed. The requested aggregate, however, is thalamic: the exact focal population contains Foxg1 transcript in only about 9% of non-target nuclei, and the curated mouse literature expects little or no expression in thalamus proper. That turns a biologically potent telencephalic transcription-factor knockout into a very low-reach aggregate perturbation for `151 TH Prkcd Grin2c Glut`.

The quantitative training evidence did not reveal an expression-profile or typed-annotation analogue that would overcome that reach penalty. The most specific SMAD/FOXO partners were 0-1 DEG perturbations in the same focal group, and the broader neurodevelopmental transcription-factor candidates were mostly 0-1 as well. A single high-count broad fallback, `Ctnnb1`, showed that this population can respond to widely deployed pathway perturbations but did not provide a Foxg1-scale match.

Balancing realized loss in the minority of Foxg1-positive nuclei against very restricted aggregate reach and a near-null specific analogue set, the most likely BH-significant count is the floor of the training distribution:

`predicted_n_degs = 0`
