# Sec31a DEG-count forecast for `151 TH Prkcd Grin2c Glut`

Predicted `n_degs`: **0**

## Evidence used

- Target and context: the one-row manifest names `Sec31a`; the requested
  population is exactly `151 TH Prkcd Grin2c Glut`.
- Target reach: the declared `Sec31a` biology bundle reports focal
  non-target expression in 19,488 / 23,679 nuclei
  (82.3008%; mean 2.0247 raw UMI; pseudobulk 126.895 CPM), so the target RNA is
  readily detectable in the assayed thalamic population.
- Functional realization prior: SEC31A is the SEC13-SEC31 outer COPII-coat
  component for ER export, but the card adjudicates functional stock at the
  21-28 day harvest as indeterminate. Editing should stop new intact SEC31A
  production but does not directly inactivate pre-existing SEC31A protein, no
  endogenous mouse thalamic-neuron SEC31A degradation half-life is known, and
  the direct mouse loss phenotype is whole-animal early embryonic lethality
  rather than a transferable postnatal thalamic-neuron measurement.
- Focal training distribution from
  `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`: 1,205 / 1,674 training
  perturbations had zero DEGs, the median was 0, the 75th percentile was 1,
  and only 106 / 1,674 exceeded 10 DEGs. The endpoint is therefore sparse and
  needs target-specific evidence to justify leaving zero.
- Closest screened anterograde ER/COPII comparators in the focal count table:
  `Sec23a = 0` and `Sar1b = 0`. Both are in the same COPII export pathway as
  Sec31a, and the full Parquet confirmed zero FDR < 0.05 genes for each across
  17,259 measured focal features.
- Other focal ER/Golgi/trafficking anchors were mostly quiet or small:
  `Atf6 = 0`, `Copa = 0`, `Cog4 = 0`, `Cog5 = 0`, `Stx5a = 0`,
  `Copg1 = 1`, `Cltc = 3`, `Hspa5 = 5`, `Sec63 = 11`, `Vps35 = 17`,
  and `Vps54 = 31`.
- The strongest trafficking counterexample, `Rab7 = 501`, was treated as a
  boundary rather than a Sec31a proxy: it is lysosomal/endosomal rather than
  COPII ER export, and the profile inspection showed a high-burden state
  with 311 positive and 190 negative significant features, unlike `Sec23a`
  and `Sar1b`, each of which had no significant features.

## Synthesis

Sec31a has real biological plausibility because it is expressed in the focal
cells and belongs to essential COPII machinery. The measured training evidence
closest to that mechanism nevertheless favored a null focal footprint: the two
available COPII-pathway perturbations, `Sec23a` and `Sar1b`, were both exact
zeros in this same class, and neither showed a hidden multi-cell-class response
that would make the focal zeroes look anomalous. The ER-stress anchors provide
an upper small-effect scenario (`Hspa5 = 5`, `Sec63 = 11`) if Sec31a depletion
progressively limits export, but the target card leaves total SEC31A depletion
by P37-P44 unresolved and the screen is mosaic and survivor-conditioned. I
therefore anchored the forecast at the focal zero mode rather than at the
small ER-stress tail or the broad `Rab7` lysosomal state.
