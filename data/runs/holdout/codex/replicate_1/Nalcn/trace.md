# Nalcn 151 TH Prkcd Grin2c Glut n_degs prediction

Prediction: 24 DEGs at BH-adjusted Wilcoxon p < 0.05.

Evidence used:

- Declared holdout target: `Nalcn` from the one-row `Nalcn.csv` manifest.
- Canonical target biology bundle:
  - NALCN is a voltage-independent, nonselective cation/leak sodium channel that sets resting excitability; function is carried by the membrane channel with UNC79, UNC80, and FAM155A partners.
  - The P16 edit is expected to stop new functional NALCN supply in edited cells, and the functional-stock adjudication judged the operative pool likely substantially depleted by the P37-P44 harvest window.
  - Exact focal-population reach was high in matched non-target 151 TH nuclei: `Nalcn` was detected in 19,324 / 23,679 cells, 81.61% expressing, with mean raw UMI 2.120 and mean CP10K 1.316.
  - No close NALCN paralog or demonstrated same-context compensating channel was identified in the supplied bounded-search evidence.
- Training endpoint table for this same 151 TH class:
  - 1,674 training targets were present; the distribution was sparse: median 0 DEGs, 75th percentile 1, 95th percentile 18, and 99th percentile 430.
  - The direct NALCN-complex genes `Unc79`, `Unc80`, and `Fam155a` were absent from the count table, so there was no same-complex measured donor.
  - Most represented ion-channel knockouts were transcriptionally quiet in 151 TH: `Cacna1a` 0, `Cacna1d` 0, `Cacna1e` 0, `Hcn1` 0, `Hcn2` 1, `Scn1a` 1, `Scn2a` 1, `Scn8a` 1, many `Kcn*` targets 0-1.
  - The nearest positive membrane-excitability donors were `Cacna1g` with 12 DEGs, `Atp1a3` with 80, and `Grin1` with 89.
- Same-experiment corpus context for those measured donors:
  - `Cacna1g:F001` reported a narrow thalamic Cav3.1 response, and `Cacna1g:F004` separated that effect from generic voltage-gated calcium-channel or auxiliary-subunit knockdown.
  - `Atp1a3:F001` and `Atp1a3:F003` described a dominant 151 TH response with ion-channel/synaptic remodeling after neuronal Na/K-pump loss.
  - `Grin1:F001`, `Grin1:F003`, and `Grin1:F004` described a 151-dominated GluN1 response mixing synaptic down-regulation with growth/plasticity and stress-linked induction.

Reasoning:

The exact 151 TH expression and the supplied stock adjudication make `Nalcn` unlike the many nearly silent channel targets whose transcript was likely absent, buffered, or weakly realized. I therefore forecast a real nonzero response. However, the closest assayed pore-forming channel with a thalamic role, `Cacna1g`, was only 12 DEGs at the p < 0.05 endpoint, and the larger `Grin1` and `Atp1a3` signatures reflect obligatory synaptic calcium signaling or a Na/K ion-gradient pump rather than a resting leak conductance. Because the direct NALCN accessory genes were not measured, I treated 80-89 DEGs as an upper scale rather than a transferable center.

I placed `Nalcn` just above the training 95th percentile and about twice the `Cacna1g` count, giving a modest thalamic homeostatic footprint rather than a broad adaptive-state forecast.
