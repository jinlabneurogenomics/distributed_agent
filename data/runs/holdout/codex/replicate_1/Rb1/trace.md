# Rb1 direct DEG-count forecast

Target: `Rb1`

Endpoint: `n_degs` in `151 TH Prkcd Grin2c Glut`, defined as the number of measured genes with BH-adjusted Wilcoxon `pvals_adj < 0.05`.

## Evidence used

- The held-out target manifest and the biology bundle both name `Rb1`; `Rb1` is not in the 1,674-row focal training count table.
- The focal training table is very sparse: median `n_degs = 0`, 75th percentile `= 1`, 95th percentile `= 18`, and only 43/1,674 training perturbations reach at least 100 significant genes. Large counts are restricted to a small set of broad transcription, chromatin, RNA-processing, and proteostasis lesions.
- The canonical `Rb1` bundle supports realization of the perturbation in the assay window:
  - pRB is a dynamic RB/E2F nuclear corepressor rather than a durable installed state.
  - the bundle adjudicates functional stock as `likely_substantially_depleted` by the P37-P44 harvest after P16 editing.
  - adult postmitotic forebrain deletion caused ectopic cell-cycle markers by one week and neuronal loss by four weeks, matching the 21-28 day latency well enough to argue against pure persistence.
  - exact in-assay focal expression is broad but not universal: 17,384/23,679 non-target nuclei expressed `Rb1` in `151 TH Prkcd Grin2c Glut` (`73.4%`, mean raw UMI `1.47`).
- Deterministic annotation placed the available exact or narrow RB/E2F-side training perturbations mainly at `E2f1`, `Tfdp1`, `Trp53`, and `Cdkn2a`.
  - The focal counts for these strongest specific nominees were `E2f1=0`, `Tfdp1=2`, `Trp53=0`, `Cdkn2a=0`.
  - Direct RB1-complex projected partners available in training were also quiet: `E2f1=0`, `Smarca4=0`; `Rbl1`, `Rbl2`, `E2f4`, and HDAC partners were absent from the focal training count table.
  - Training targets in the KEGG cell-cycle set that also contains `Rb1` were almost all null or single-digit in the focal table; the largest were `Smc1a=24` and `Stag2=37`, both cohesin-family perturbations rather than RB/E2F derepression.
- The same-experiment corpus supplied a high-confidence boundary claim that single represented E2F/DP perturbations do not engage a coordinated canonical G1/S replication, mitotic, or apoptotic program in settled postnatal neurons. The underlying `E2f1` Finding directly tested canonical DNA-replication, mitotic, and apoptotic transcripts and found no movement; `Tfdp1` had only a small thalamic response that was not phenocopied by `Tfdp2`, `E2f1`, or `E2f5`.
- I checked the declared Parquet for selected E2F/MYC/TRP53-side targets in the exact focal class. Across `E2f1`, `E2f5`, `Tfdp1`, `Tfdp2`, `Trp53`, `Trp73`, `Atr`, `Prkdc`, `Myc`, `Mycn`, `Mga`, `Mlxip`, and `Mnt`, there were only four significant rows: two `Tfdp1` genes and two `Mga` genes. The E2F/DP and p53 neighbors therefore did not hide a large signature behind the precomputed counts.

## Synthesis

The central tension is that `Rb1` is the brake on an E2F program, so loss of `E2f1` or `Tfdp1` is an imperfect opposite-side perturbation rather than a same-sign phenocopy. I therefore did not simply copy the 0-2 counts from the nearest E2F/DP knockouts. The biology bundle gives real upward pressure: `Rb1` is expressed in most focal non-target nuclei and pRB should be depleted within the experiment, with external postmitotic-neuron evidence that cell-cycle markers can appear well before the P37-P44 harvest.

At the same time, the focal screen showed strong transcriptional power for broad regulators but repeatedly failed to recover basal G1/S, E2F, p53, MYC/MAX, and cell-cycle programs from the measured neighboring perturbations. That argues that postnatal thalamic neurons are not poised to generate a large canonical cell-cycle RNA module after a single pathway-node loss, and any severe `Rb1`-positive cells may also be attenuated by survivor-conditioned sampling.

I therefore place `Rb1` above the exact-neighbor nulls but below the 95th percentile of the focal training distribution and far below broad off-axis regulators such as `Ctnnb1`, `Brd4`, or `Sin3a`.

Predicted `n_degs`: **8**
