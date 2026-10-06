# Direct Naa15 n_degs forecast

Target: `Naa15`

Population: `151 TH Prkcd Grin2c Glut`

Point prediction: `0`

## Evidence used

1. The declared one-row target manifest and canonical biology bundle both name
   `Naa15` as the held-out target. The bundle provenance checksum is
   `8e0a86e1b5ce0d0fcf7aa7cfc11f4abbb8059e110bef6b3822b30b9f8b1d50ab`; its
   served biology view reports `target_outcome_exposed=false` and
   `labeled_neighbors_exposed=false`.

2. Exact focal-population reach is good: in matched non-target
   `151 TH Prkcd Grin2c Glut` cells, `Naa15` was detected in
   18,674 of 23,679 nuclei, 78.86%, with mean expression
   1.126 cp10k. This supports the possibility that CRISPR edits reach a
   transcribed locus in the assayed cells; per the bundle and dataset portrait,
   transcript abundance was used only as reach evidence, not as an editing-
   efficiency estimate.

3. The `Naa15` biology bundle places the target in the NatA N-terminal
   acetyltransferase complex: NAA15 is the auxiliary/ribosome-associated
   partner for catalytic NAA10, and the operative stock includes both active
   NAA15-containing NatA and pre-edit N-terminally acetylated carrier proteins.
   The functional-stock adjudication was
   `partially_depleted_or_leading_edge` at the P37-P44 harvest because a P16
   edit stops new NAA15 synthesis but existing NatA complexes, already
   acetylated carriers, a long-lived carrier tail, and possible NAA16-supported
   alternative NatA activity can all blunt acute loss over the 21-28 day
   window. The closest positive postnatal neural evidence was Purkinje-cell
   NatA inhibition, not Naa15-specific loss in thalamic neurons.

4. The direct NatA training comparator is `Naa10`, the catalytic subunit
   named repeatedly in the NAA15 source facts. In the declared
   `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` endpoint table,
   `Naa10` has `n_degs=0`. Direct Parquet aggregation for `Naa10` found
   zero BH-adjusted FDR < 0.05 rows and zero FDR < 0.10 rows across its
   22 measured neuronal groups, including `n_pert_matched=240` in the
   focal thalamic group.

5. The selected same-experiment corpus reports the same `Naa10` result as a
   pan-neuronal transcriptomic null at FDR < 0.10 and notes no compensatory
   NAT-family, integrated-stress, apoptosis, proteasome, or ubiquitin rebound
   program at FDR < 0.10. Its explicit active-boundary comparators separate
   this NatA null from detectable protein-homeostasis and translation
   perturbations: in the focal count table `Psmb4=742`, `Psmc1=430`, and
   `Eef2=9`, whereas flat full-vector neighbors named in the `Naa10` report
   such as `Mpc1`, `Rorb`, `Gli2`, and `Diaph2` all have `n_degs=0`.

6. A bounded profile comparison in the exact focal class for
   `Naa10`, `Psmb4`, `Psmc1`, `Eef2`, `Mpc1`, `Rorb`, `Gli2`, and `Diaph2`
   confirmed the count-scale contrast. `Naa10` had 17,259 available signed
   features and zero significant positive or negative features at FDR < 0.05.
   Its whole-profile cosine values versus the active guards were tiny
   (`Psmb4` 0.0208, `Psmc1` 0.0243, `Eef2` 0.0130), and its leading positive
   and negative features all had adjusted p-value 1.0. Thus there was no
   hidden focal-class NAA10 vector resembling a proteasome-like stress state.

7. The focal training endpoint itself is zero-inflated: among 1,674 observed
   biological targets, 1,205 have `n_degs=0`, 1,571 have `n_degs<=10`, and
   the empirical median is 0. Only 42 targets exceed 100 DEGs.

## Synthesis

`Naa15` is reachable and biologically credible, so I did not treat it as an
assay-absent or nonfunctional target. The requested scalar, however, is the
number of FDR < 0.05 nuclear-RNA DE genes among recovered postmitotic thalamic
neurons after an acute P16 edit. On that endpoint, the closest measured NatA
loss in the training set, `Naa10`, is not merely small in the focal class; it
is flat across all measured classes and lacks the expected secondary stress or
proteasome program. Direct proteasome or translation perturbations demonstrate
that this screen can see a protein-homeostasis RNA state in the same cell
class, but they are indirect upper boundaries rather than NatA subunit
phenocopies.

The NAA15-specific biology adds uncertainty in both directions. Loss of the
auxiliary scaffold could affect ribosome association and possible non-complex
pools differently from loss of catalytic NAA10, which argues against copying
`Naa10` mechanically. Conversely, pre-edit installed N-terminal acetylation,
slow carrier turnover, and possible NAA16 residual activity make a large
21-28 day survivor RNA state less likely. Given the zero-heavy local base
rate and the direct NatA comparator's complete null profile, the most
defensible integer forecast is at the mass point:

`predicted_n_degs = 0`
