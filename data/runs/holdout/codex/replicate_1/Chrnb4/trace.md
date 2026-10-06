# Chrnb4 DEG-count prediction

Target and endpoint: `Chrnb4` in `151 TH Prkcd Grin2c Glut`; predict the number
of focal-class measured genes with BH-adjusted Wilcoxon `p < 0.05`.

Evidence used:

- The one-row holdout manifest declares `Chrnb4` as the target.
- The declared `Chrnb4` biology bundle supports genuine beta4 nicotinic-receptor
  function and likely depletion of beta4-containing receptor stock within the
  P16 to P37-P44 window, but it also restricts that prior to a sparse
  cell-autonomous context: beta4 expression is strongest in ventral medial
  habenula/interpeduncular circuitry rather than broadly across thalamus.
- Exact non-target expression in the requested aggregate population was
  extremely low: 42 expressing nuclei among 23,679 non-target nuclei, only 45
  total target UMIs, `mean_raw_umi = 0.0019004`, and
  `pct_cells_expressing = 0.177%`. This exact in-assay reach superseded the
  broader adult-thalamus qualitative expression evidence for forecasting this
  focal aggregate.
- The focal training count table is sparse: among 1,674 visible biological
  perturbations, 1,205 have 0 DEGs, the median is 0, the 75th percentile is 1,
  and only 149 have at least 10 DEGs.
- The closest visible receptor-subunit comparators were quiet in the same
  focal class. `Chrna3`, an alpha subunit paired with beta4 in the biology
  bundle, had 0 DEGs. `Chrnb2`, the related alternative beta subunit, had
  1 DEG; direct Parquet inspection showed that this single hit was the
  self-transcript `Chrnb2` itself with adjusted `p = 7.37e-07`, while the next
  `Chrnb2` row had adjusted `p = 0.782`. The `Chrna3` contrast had no near-hit
  after BH correction; its smallest adjusted `p` was 0.499.
- A wider same-table receptor slice also stayed at the floor: visible
  cholinergic receptor targets were `Chrm2 = 0`, `Chrm3 = 0`, `Chrna1 = 0`,
  `Chrna2 = 0`, `Chrna3 = 0`, `Chrna4 = 2`, `Chrna6 = 0`, `Chrna7 = 0`,
  `Chrnb1 = 0`, `Chrnb2 = 1`, `Chrnb3 = 0`, `Chrnd = 0`, `Chrne = 0`, and
  `Chrng = 0`.

Synthesis:

Loss of beta4-containing nicotinic receptors should be functionally reachable
by harvest in genuinely `Chrnb4`-expressing neurons, so I did not treat this as
a failed or irrelevant edit. However, the endpoint aggregates all recovered
`151 TH Prkcd Grin2c Glut` nuclei, and the exact target reach shows that only a
tiny fraction of that aggregate expressed `Chrnb4` at baseline. A cell-autonomous
ion-channel-subunit perturbation in such a rare subpopulation is therefore
expected to be heavily diluted in pseudobulk differential expression. The two
best visible nicotinic comparators, including same-complex `Chrna3`, produced
zero downstream DEGs in the identical table, and the broader acetylcholine
receptor family was likewise at 0-2.

The sparse focal prior plus the near-zero exact expression reach and quiet
receptor analogs all point to the bottom of the count distribution. I therefore
predicted `0` DEGs for `Chrnb4`.
