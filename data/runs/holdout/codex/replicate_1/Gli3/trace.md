# Gli3 direct DEG-count forecast

## Requested endpoint

- Target: `Gli3`, the single row in the declared holdout manifest.
- Cell class: `151 TH Prkcd Grin2c Glut`.
- Endpoint: `n_degs`, the number of measured genes with BH-adjusted Wilcoxon `p < 0.05`.

I treated the focal training count table as the direct endpoint measurement for visible perturbations, the Parquet as the exact row-level DE surface for spot checks in the focal class, and the July same-experiment corpus as a packaged interpretation of the same Perturb-seq experiment rather than as independent replication.

## Evidence used

- The canonical `Gli3` biology bundle supports functional realization by harvest but only partially: GLI3 is a Hedgehog zinc-finger transcriptional regulator carried by full-length and processed repressor pools, and the bundle adjudicates pre-edit functional stock as `likely_substantially_depleted` by P37-P44 after a P16 disruptive edit. The same bundle flags the best neural loss evidence as embryonic/developmental rather than a matched postnatal thalamic-neuron perturbation.
- Exact in-assay target reach in the requested focal class is extremely sparse: `Gli3` is detected in 83 of 23,679 matched non-target nuclei, or 0.3505%, with mean 0.00541 raw UMI, mean 0.00321 cp10k, and pseudobulk 0.3388 cpm. This argues that any direct GLI3-dependent state would be diluted across the aggregated `151 TH Prkcd Grin2c Glut` contrast.
- The focal training count table is strongly zero-inflated: among 1,674 visible training perturbations, 1,205 have `n_degs = 0`, the median is 0, and 1,546 have at most 5 DEGs.
- The biologically closest Hedgehog/GLI/ciliary training perturbations are all null in the requested class by the declared count table: `Cdon`, `Dync2h1`, `Dync2i1`, `Gli1`, `Gli2`, `Gpr161`, `Ift43`, `Ift81`, `Ift88`, `Kif3b`, `Ptch1`, `Ptch2`, and `Smo` each have `n_degs = 0`.
- Focal Parquet rows for key visible neighbors showed no near-threshold GLI module hidden under the count cutoff. In `151 TH Prkcd Grin2c Glut`, the minimum adjusted p-value was 1.0 for `Gli1`, `Gli2`, `Glis2`, `Glis3`, `Gpr161`, `Ift88`, `Ptch1`, `Ptch2`, and `Smo`; 0.348 for `Dync2h1`; 0.391 for `Ift81`; and 0.847 for `Ift43`.
- The same-experiment corpus had no `Gli3` Finding or Claim in the selected release. For visible Hedgehog comparators, it reinforced the training-table reading: `Gli1`, `Gli2`, `Gpr161`, `Ptch1`, and `Ptch2` are reported as global or near-global transcriptional nonresponders in P16-perturbed NeuN-enriched neurons, and `Dync2h1`, `Ift88`, and `Smo` reports specifically note failure to recover canonical Sonic Hedgehog/GLI transcriptional output.
- The focal class can produce large signatures when an expressed regulator controls an active program: `Cic` has 576 DEGs and `Yy1` has 720 DEGs in the same count table. More developmentally flavored regulators were mostly tiny or null in this class, however: `Bcl11a`, `Pax6`, `Tbr1`, `Neurod1`, `Neurod2`, `Sox4`, and `Zic2` have 0, while `Arid1b`, `Sox2`, `Sox5`, and `Zic1` have 1-2 and `Kmt2a` has 24.

## Synthesis

The edit should remove newly synthesized GLI3 protein within the 21-28 day window, so I did not interpret a zero forecast as failed editing. The limiting facts were endpoint reach and pathway state: the exact focal population has vanishingly low `Gli3` RNA, and every measured canonical Hedgehog/GLI neighbor that could reveal an active postmitotic Hedgehog transcriptional state was flat in this cell class and largely flat across the experiment.

The counterargument is that `Gli3` is a sequence-specific transcription factor and developmental regulators can have nonzero postnatal thalamic signatures. I downweighted that because the closest GLI-family members `Gli1` and `Gli2` were complete focal-class nulls with adjusted p-values of 1.0 throughout their top Parquet rows, and the packaged biology explicitly treats embryonic cortical `Gli3` loss as not timing- or context-transferable to acute P16 loss in postmitotic thalamic neurons.

Point forecast: `0` DEGs.
