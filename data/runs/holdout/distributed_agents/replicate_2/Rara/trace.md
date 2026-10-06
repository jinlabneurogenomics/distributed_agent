# Rara prediction trace

## Question and resolved ambiguities

The requested readout is the number of genes with `pvals_adj < 0.05` after a
held-out `Rara` perturbation in `151 TH Prkcd Grin2c Glut` nuclei. I treated
`n_degs` as an assay-specific FDR-supported transcriptional-response breadth,
not as a general score for RARA biological importance, protein loss, survival,
or editing efficiency. The held-out manifest contains a single row:

| target_name |
|---|
| Rara |

`Rara` is absent from the supplied focal training-count CSV, so no direct
`151 TH Prkcd Grin2c Glut` DEG count or expression signature for `Rara` was
used.

## Sources used

- `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`
  for exact focal `n_degs` values of non-held-out training perturbations.
- `[local file: training_de_all_cell_groups.parquet]`
  for per-gene focal signatures, adjusted p-values, and matched nucleus counts.
- Distributed Agents corpus MCP, release `perturbai-july-260713-sourceguard-1773-v1`,
  especially the RAR/RXR claims and target reports for `Rarb`, `Rarg`, `Rxra`,
  `Rxrg`, `Stra6`, and `Greb1l`.
- Distributed Agents runtime profile tools for a run-local comparison of candidate
  retinoid and nuclear-receptor perturbation profiles in
  `151 TH Prkcd Grin2c Glut`.
- PubMed literature searches for public RARA/RAR/RXR biology:
  Chambon 1996, PMID: 8801176; Le Maire and Bourguet 2014,
  DOI: 10.1007/978-94-017-9050-5_3; Chen and Napoli 2007,
  DOI: 10.1096/fj.07-8739com; Chen et al. 2008,
  DOI: 10.1074/jbc.M802314200; Maghsoodi et al. 2008,
  DOI: 10.1073/pnas.0804801105; Soden and Chen 2010,
  DOI: 10.1523/JNEUROSCI.3660-10.2010; Ghyselinck et al. 1997,
  PMID: 9240560; Koshy et al. 2022, DOI: 10.26508/lsa.202201627.

The Distributed Agents corpus had no `Rara`-scoped target report or claim
(`target_found=false`), consistent with `Rara` being held out. I therefore used
same-experiment evidence from pathway neighbors and paralogs, not any hidden
`Rara` result.

## Computational checks over the inputs

1. The focal training endpoint has 1,674 training perturbations. It is heavily
   zero-inflated: median `n_degs = 0`, only 469 perturbations are nonzero, the
   90th percentile is only 2, and the very broad responses are rare core-process
   perturbations.

2. I queried the focal count CSV for RAR/RXR and nuclear-receptor neighbors.
   Direct retinoid-axis analogs were all exact zeros in this focal cell group:

   | training perturbation | focal `n_degs` | why it was compared with `Rara` |
   |---|---:|---|
   | `Rarb` | 0 | RAR paralog; same retinoic-acid receptor family |
   | `Rarg` | 0 | RAR paralog |
   | `Rxra` | 0 | RXR heterodimer partner for RARs |
   | `Rxrb` | 0 | RXR heterodimer partner |
   | `Rxrg` | 0 | RXR heterodimer partner |
   | `Stra6` | 0 | retinol/RA-pathway entry point and RA-starvation comparator |
   | `Greb1l` | 0 | reported RAR coactivator in the Distributed Agents retinoid module |
   | `Nr1h4` | 0 | RXR partner/lipid nuclear receptor boundary |
   | `Nr1h5` | 0 | RXR partner/lipid nuclear receptor boundary |
   | `Ppara`, `Ppard`, `Pparg` | 0, 0, 0 | PPAR/RXR heterodimer boundary |
   | `Vdr`, `Thrb` | 0, 0 | VDR/RXR and thyroid-receptor/RXR boundaries |
   | `Ncoa1`, `Ncoa3`, `Ep300` | 0, 0, 0 | nuclear-receptor cofactor controls |

   The useful nonzero counterexamples were small or different modules:
   `Thra` had 3 DEGs in the focal group and `Rora` had 278, showing that
   nuclear receptors can be detected in this group when the assayed receptor is
   tonically active. `Crebbp` had 8, but `Ep300` and the p160 coactivators
   `Ncoa1`/`Ncoa3` were zero, so a broad coactivator response is not the right
   analog for `Rara`.

3. I read a bounded focal slice of the DE parquet:

   ```python
   filter = (group_name == "151 TH Prkcd Grin2c Glut")
            & gene_target.isin(retinoid_and_counterexample_targets)
   ```

   The filtered slice contained 17,259 measured genes per selected target.
   Focal matched perturbation counts were adequate for the main RAR/RXR
   comparisons: `Rarb` 273, `Rarg` 168, `Rxra` 247, `Rxrb` 249, `Rxrg` 229,
   `Stra6` 195, and `Greb1l` 196 perturbed nuclei, all against 23,679 matched
   controls. The top focal adjusted p-values were far from threshold:
   `Rarb` min adjusted p = 1, `Rarg` = 1, `Rxra` = 1, `Rxrb` = 0.541,
   `Rxrg` = 0.438, `Stra6` = 1, and `Greb1l` = 0.758.

4. I used `profile_compare` on log2 fold changes for a declared focal cohort
   of `Rarb`, `Rarg`, `Rxra`, `Rxrb`, `Rxrg`, `Stra6`, `Greb1l`, `Nr1h4`,
   `Nr1h5`, `Thra`, `Vdr`, and `Rora`. With `pvals_adj < 0.05` as the
   significance criterion, all seven retinoid-axis analogs had
   `significant_feature_count = 0`; `Rora` and `Thra` were the expected active
   counterexamples. I used this runtime artifact only to check focal activity
   and not as a black-box `Rara` predictor.

## Same-experiment corpus evidence

The corpus had a moderate-confidence shared claim,
`claim:1352cb7a13bac707d254`, stating that represented
retinoid/RAR/RXR and lipid nuclear-receptor single-gene perturbations did not
produce a coherent shared acute neuronal transcriptional module. The claim
explicitly scoped out `Rara`, `Nr1h3`, ligand addition, and combinatorial
receptor loss.

Key target-specific findings behind that claim were:

- `Rarb:F002`: `Rarg`, `Rxra`, `Rxrb`, and `Rxrg` did not phenocopy the
  isolated `Rarb` event; the corpus interprets the rare `Rarb` signal as an
  L5 ET singleton rather than as a pan-RAR/RXR module.
- `Rarg:F001` and `Rarg:F002`: acute P16 `Rarg` loss produced no robust
  response in any recovered neuronal group, and `Rarb`/`Rxra`/`Rxrb`/`Rxrg`/
  `Stra6` were nonconvergent and nearly flat.
- `Rxra:F001` and `Rxra:F002`: `Rxra` was flat across 23 measured neuronal
  groups and uncoupled from measured RXR paralogs and canonical partner
  receptors.
- `Rxrg:F001`, `Rxrg:F002`, and `Rxrg:F005`: `Rxrg` was globally buffered,
  the obvious retinoid/RXR relatives mostly lacked robust output after
  individual loss, and `Rora`/`Thra` responded in `151 TH Prkcd Grin2c Glut`
  where `Rxrg` remained flat.
- `Stra6:F001` through `Stra6:F004`: `Stra6` was flat in all measured NeuN+
  groups, retinoid feedback genes did not move after `Stra6` loss, measured
  nuclear retinoid receptors did not phenocopy `Stra6`, and score-space
  nearest neighbors failed to reveal a hidden `Stra6` module.
- `Greb1l:F002`: represented RAR/RXR/Stra6 perturbations were nearly as flat
  as `Greb1l`, supporting broader absence of tonic retinoid nuclear-receptor
  dependence in the sampled postmitotic neurons.

I also checked the induced Distributed Agents corpus topology over
`Greb1l`, `Rarb`, `Rarg`, `Rxra`, `Rxrb`, `Rxrg`, and `Stra6`. All 21 possible
pairs were connected by the retinoid/RXR shared-claim or explicit-finding
lanes. I interpreted that dense graph as evidence that this is a biologically
coherent comparison set, not as evidence that their flat signatures should be
averaged mechanically.

## Biological rationale for `Rara`

RAR-alpha, encoded by `Rara`, is a ligand-regulated retinoic-acid receptor.
RAR proteins act primarily as RAR/RXR heterodimers on RA-response elements and
exchange corepressor for coactivator complexes upon ligand binding
(Chambon 1996, PMID: 8801176; Le Maire and Bourguet 2014,
DOI: 10.1007/978-94-017-9050-5_3). This makes the measured RAR paralogs
`Rarb`/`Rarg` and RXR partners `Rxra`/`Rxrb`/`Rxrg` the closest available
within-screen analogs, and every one of those is a zero in the focal endpoint.

The strongest argument for a possible `Rara` exception is the neuronal
RAR-alpha literature: all-trans RA can activate local dendritic translation,
GluR1/GluA1 expression, and spine formation through RAR-alpha; RAR-alpha is
present in dendritic RNA granules and participates in RA-dependent homeostatic
synaptic scaling (Chen and Napoli 2007; Chen et al. 2008; Maghsoodi et al.
2008; Soden and Chen 2010). I discounted that as a broad-DEG predictor for
three reasons. First, it is rapid, dendritic, and partly translational rather
than a canonical nuclear steady-state mRNA program. Second, direct focal
comparators for the translation/synaptic branch were also sparse:
`Fmr1` 0, `Gria1` 0, `Gria2` 0, `Gria3` 0, `Dlg4` 1, `Shank2` 0, `Shank3` 2,
`Cyfip1` 0, `Cyfip2` 1, `Mtor` 2, and `Mapk1` 0. Third, the acute mosaic P16
perturbation and nuclear RNA readout are unlikely to reproduce ligand-pulse
or electrophysiology/spine phenotypes.

Functional redundancy is another reason not to inflate the point estimate.
RAR paralogs can compensate in developmental settings, with stronger
phenotypes in compound receptor loss than in single mutants (Ghyselinck et al.
1997, PMID: 9240560; Koshy et al. 2022, DOI: 10.26508/lsa.202201627). The
experiment assayed only sparse single-gene CRISPR loss, so a buffered
single-`Rara` result is more plausible than a large RA-starvation collapse.

The point prediction is therefore:

| held-out target | predicted `n_degs` | rationale |
|---|---:|---|
| `Rara` | 0 | closest same-family and partner perturbations are exact focal zeros, focal analog p-values are far from FDR 0.05, the same-experiment corpus reports a flat/nonconvergent acute neuronal RAR/RXR neighborhood, and RARA-specific synaptic biology is mostly local/translational rather than a broad nuclear DEG program |

## Limits

This is still an extrapolation because `Rara` itself was not assayed in the
training signature matrix or represented in the corpus as a target. `Rara` is
not identical to `Rarb` or `Rarg`, and single-RAR paralogs can have distinct
DNA occupancy, expression, and ligand-response behavior. The dataset also lacks
RAR/RXR combinatorial knockouts, ligand addition or deprivation, guide-level
DNA indel calls, mature electrophysiology, dendritic translation, and spine
readouts. A rare `151 TH Prkcd Grin2c Glut`-specific RAR-alpha nuclear program
could therefore be missed by the analogs, but the supplied focal DE evidence
and same-experiment retinoid corpus both point to no FDR-supported genes.
