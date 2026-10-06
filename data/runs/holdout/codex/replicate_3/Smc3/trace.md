## Forecast

Predicted `n_degs` for `Smc3` in `151 TH Prkcd Grin2c Glut`: **42**

## Evidence used

- The declared one-row holdout manifest names `Smc3`; the endpoint is the
  count of measured genes with BH-adjusted Wilcoxon `p < 0.05`.
- The exact target-expression bundle for the focal cell group shows that
  `Smc3` was measurable in the matched non-target population:
  17,963/23,679 nuclei expressed it, with 75.86% expressing, mean raw UMI
  1.615, and mean log1p CP10K 0.610. This supports in-assay reach but was not
  used as an editing-efficiency readout.
- The canonical `Smc3` biology bundle adjudicates SMC3 as a dynamic, obligate
  ATPase-core cohesin-ring component. The P16 edit is expected to stop new
  functional SMC3 production; cohesin exchange is much faster than the
  21-28-day harvest window, so functional stock should likely decline
  substantially. The residual uncertainty is that pre-existing rings are not
  directly destroyed and the postmitotic mouse-neuron SMC3 protein clearance
  curve is unknown.
- The declared focal training count table contains 1,674 observed perturbation
  targets and is sparse: median 0, 75th percentile 1, 95th percentile 18, 99th
  percentile 430. Only 43/1,674 targets had at least 100 DEGs.
- Direct cohesin/chromatin-loop comparators in the same count table were:
  `Smc1a` 24, `Stag2` 37, `Stag1` 0, `Pds5a` 0, `Hdac8` 0, `Naa10` 0, `Ctcf`
  270, and the boundary chromosome-architecture genes `Ncapd3`, `Prr12`,
  `Smchd1`, and `Zfp609` were 0.
- A profile comparison on the declared Parquet, restricted to
  `151 TH Prkcd Grin2c Glut`, confirmed that `Smc1a` and `Stag2` carry real
  but compact programs at `pvals_adj < 0.05`: 24 and 37 significant genes,
  respectively, with 8 shared down-regulated FDR genes, 1 shared up-regulated
  FDR gene, and no significant same-pair direction conflicts. `Ctcf` had a
  larger 270-gene profile, while `Stag1`, `Pds5a`, `Hdac8`, and `Naa10` were
  FDR-null.
- Packaged same-experiment Findings/Claims agree with that quantitative
  pattern but are not independent replication: `Smc1a` and `Stag2` share a
  restricted thalamic neuronal connectivity/signaling module; that module is
  not reproduced by represented `Stag1`, `Pds5a`, `Hdac8`, `Ncapd3`, `Prr12`,
  `Zfp609`, or `Smchd1` perturbations. The same corpus marks `Ctcf` as a
  larger, CTCF-dominant Pcdh response that the represented cohesin-machinery
  perturbations do not phenocopy.

## Reasoning

The best quantitative center is the observed core cohesin response rather than
the atlas-wide chromatin tail. `Smc1a` and `Stag2` show that this assay can
recover a postnatal thalamic cohesin-sensitive module, but the module is much
smaller than broad chromatin or proteostasis responses and far smaller than the
`Ctcf` Pcdh-heavy state. The flat responses of `Stag1`, `Pds5a`, `Hdac8`,
`Ncapd3`, `Prr12`, `Smchd1`, and `Zfp609` further argue that chromosome
architecture membership alone should not inflate the point forecast.

`Smc3` should still be placed a little above the `Smc1a`/`Stag2` pair instead
of at their simple mean: SMC3 is a shared ring-core subunit with no replaceable
paralog in the card evidence, and the focal population has strong exact Smc3
expression. I did not move the point toward hundreds of DEGs because the
functional-stock card leaves residual pre-edit cohesin uncertainty, the
matched P16 thalamic timing is not directly observed, the single-nucleus
endpoint is survivor-conditioned, and the released direct cohesin comparators
remained in the tens of DEGs at the requested FDR threshold.

The resulting synthesis is a compact but clearly nonzero focal response,
slightly stronger than `Stag2` and well below `Bptf`/`Ctcf`-scale chromatin
states: 42 DEGs.
