# Clcn5 DEG-count prediction

## Question and endpoint

The requested manifest contains one held-out perturbation, `Clcn5`. I interpreted the task as a point prediction for the number of measured genes with `pvals_adj < 0.05` after `Clcn5` CRISPR loss of function in the focal `151 TH Prkcd Grin2c Glut` neuronal group.

The endpoint is an assay-specific FDR count from the postnatal AAV-CRISPR Perturb-seq experiment. I did not treat it as a direct measure of kidney Dent-disease biology, cell viability, guide editing, or raw target expression. Counts include the perturbed gene's own RNA if it is measured and significant.

## Sources used

- Requested-target manifest: `[local file: 041_Clcn5.csv]`
- Focal training DEG counts: `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`
- Same-experiment differential-expression parquet: `[local file: training_de_all_cell_groups.parquet]`
- Distributed Agents corpus release `perturbai-july-260713-sourceguard-1773-v1`, queried for same-experiment target context around `Clcn3`, `Clcn4`, `Ocrl`, `Lrp2`, and the endomembrane-acidification claim.
- Distributed Agents runtime `profile_neighbors`, run in `151 TH Prkcd Grin2c Glut` to compare focal-class expression profiles of relevant held-in anchors against the 1,674 eligible training targets.
- PubMed literature on ClC biology and ClC-5/Dent disease:
  - Stauber, Weinert, and Jentsch 2012, DOI `10.1002/cphy.c110038`, PMID `23723021`
  - Novarino, Weinert, Rickheit, and Jentsch 2010, DOI `10.1126/science.1188070`, PMID `20430975`
  - Devuyst 2004, PMID `15615095`
  - Sakakibara and Nozu 2025, DOI `10.1007/s00467-025-06745-x`, PMID `40163114`

The selected Distributed Agents corpus had no direct `Clcn5` record, so `Clcn5` reasoning is an extrapolation from raw held-in profiles and public gene-function evidence rather than from a packaged `Clcn5` finding.

## Computational checks

1. Read the manifest. It has exactly one requested row, `Clcn5`, and `Clcn5` is absent from the focal training-count CSV as expected.

2. Summarized the 1,674 focal training counts. The empirical distribution is heavily zero-inflated:

| class | count |
|---|---:|
| zero DEGs | 1205 |
| 1-9 DEGs | 363 |
| 10-99 DEGs | 63 |
| >=100 DEGs | 43 |

3. Pulled focal DEG counts for biologically relevant held-in comparators:

| training target | focal `n_degs` | why inspected |
|---|---:|---|
| `Clcn3` | 0 | endosomal CLC exchanger paralog |
| `Clcn4` | 1 | closest CLC-3/CLC-4 endosomal exchanger relative |
| `Atp6v0a1` | 1 | V-ATPase V0 subunit; vesicular acidification counterparty |
| `Atp6v1a` | 0 | V-ATPase V1 core subunit |
| `Atp6v1b2` | 0 | V-ATPase V1 subunit |
| `Atp6v1e1` | 0 | V-ATPase V1 subunit |
| `Ocrl` | 0 | Dent/Lowe phosphoinositide endocytic gene, functionally close to ClC-5 in proximal-tubule endocytosis |
| `Inpp5k` | 0 | phosphoinositide 5-phosphatase/endocytic comparator from the Ocrl corpus neighborhood |
| `Appl1` | 0 | early-endosome adaptor comparator from the Ocrl corpus neighborhood |
| `Dnm1` | 1 | endocytic fission comparator from the Ocrl corpus neighborhood |
| `Synj1` | 1 | synaptic/endocytic PI(4,5)P2 phosphatase |
| `Lrp2` | 0 | megalin, the ClC-5/OCRL renal endocytic receptor axis |
| `Ap3b1` | 0 | vesicle/lysosome trafficking |
| `Atg5` | 0 | autophagy counterexample |
| `Atg16l1` | 0 | autophagy counterexample |
| `Cltc` | 3 | stronger clathrin-mediated vesicle-trafficking counterexample |
| `Hspa5` | 5 | ER-stress/trafficking stress counterexample |
| `Rab7` | 501 | late endosomal/lysosomal positive counterexample |

4. Ran a profile-neighbor search in the focal class for anchors `Clcn3`, `Clcn4`, `Atp6v0a1`, `Atp6v1a`, `Atp6v1b2`, `Ocrl`, and `Lrp2`, with `gene_target` as the entity, `names` as the features, `logfoldchanges` as the signed values, and `pvals_adj < 0.05` as the significant-program threshold. The runtime wrote `clcn5_anchor_neighbors.json`.

The key point was not the identity of the nearest unrelated neighbors but the lack of an FDR-level anchor module:

| anchor | FDR-significant features in focal profile | nearest-neighbor pattern |
|---|---:|---|
| `Clcn3` | 0 | top whole-profile neighbors such as `Hnrnpa2b1`, `Pcsk2`, and `Cep290` had only subthreshold tail overlap |
| `Clcn4` | 1 | top neighbors such as `Ptchd1`, `Nrg1`, and `Dcc` had no shared significant program |
| `Atp6v0a1` | 1 | top neighbors were unrelated low-breadth signatures |
| `Atp6v1a` | 0 | no FDR program |
| `Atp6v1b2` | 0 | no FDR program |
| `Ocrl` | 0 | no FDR program |
| `Lrp2` | 0 | no FDR program |

5. Scanned the focal parquet rows for the same anchors to see whether the one-gene calls represented downstream biology or self-target RNA. `Clcn4`, `Atp6v0a1`, and `Synj1` each had only their own transcript as the single FDR<0.05 row in this focal group. `Ocrl`, `Clcn3`, `Lrp2`, `Atp6v1a`, `Atp6v1b2`, and `Atp6v1e1` had no FDR<0.05 rows. That makes the direct paralog and acidification comparators effectively downstream-flat here.

## Target-specific reasoning

### `Clcn5`

`Clcn5` encodes ClC-5, a vesicular 2Cl-/H+ exchanger. Public biology makes it a strong renal proximal-tubule endocytic gene: ClC-5 loss impairs receptor-mediated reabsorption of filtered low-molecular-weight proteins, disrupts megalin/cubilin trafficking, and causes Dent disease type 1. ClC-5 raises endosomal chloride in exchange for protons accumulated by the V-ATPase; the Clcn5 uncoupling mouse showed that exchange-coupled chloride accumulation, not chloride conductance alone, is needed for normal proximal-tubule endocytosis (Novarino et al. 2010; Stauber et al. 2012; Devuyst 2004; Sakakibara and Nozu 2025).

Those facts nominate three useful in-dataset comparison lanes:

- CLC exchanger paralogs: `Clcn3` and `Clcn4`. Both are closer neuronal/endosomal ClC family members than `Clcn5` itself. In this focal class, `Clcn3` had `n_degs = 0`. `Clcn4` had `n_degs = 1`, and that one row was the `Clcn4` transcript itself (`logfoldchanges = -0.802`, adjusted `p = 6.7e-11`). The Distributed Agents corpus independently summarizes these perturbations as downstream-flat across measured neuronal groups and says the canonical endosomal Cl-/H+ axis was transcriptionally buffered or off-axis in the acute P16 snRNA readout.
- Vesicular acidification machinery: `Atp6v0a1`, `Atp6v1a`, `Atp6v1b2`, and `Atp6v1e1`. Their focal counts were 1, 0, 0, and 0, respectively; the `Atp6v0a1` count was self-RNA only. The Distributed Agents endomembrane claim likewise reports that CLC, NHE, and V-ATPase relatives do not collapse into a shared postnatal neuronal transcriptional state.
- Endocytic/Dent-neighborhood machinery: `Ocrl` is the best held-in Dent/Lowe comparator, and `Lrp2` is megalin, the endocytic receptor most directly affected in the renal ClC-5/OCRL disease axis. Both had `n_degs = 0` in `151 TH Prkcd Grin2c Glut`. Additional Ocrl-neighborhood genes were also silent or nearly silent: `Inpp5k` 0, `Appl1` 0, `Dnm1` 1, and `Synj1` 1 with only self-RNA significant for `Synj1` in this class.

I treated `Rab7` as an important counterexample, not as the main analog. It produced a broad focal response (`n_degs = 501`) with late endosomal/lysosomal compensation genes such as `Atp6v1b2` and `Dpp7` among the strongest rows, showing that lysosomal stress can be visible in these thalamic nuclei. But ClC-5 is an early/recycling endosomal exchanger with a renal receptor-recycling phenotype, and the closer `Clcn3`/`Clcn4`/`Ocrl`/`Lrp2` perturbations did not engage a Rab7-like program. `Cltc` and `Hspa5` also show that vesicle or proteostasis perturbations can produce nonzero calls, but their focal responses were small and are mechanistically less direct than the null ClC/OCRL comparators.

Putting those together, the best point prediction for `Clcn5` is zero FDR<0.05 genes. The count should stay at the empirical null floor because the directly assayed endosomal CLC exchangers, V-ATPase acidification genes, and Dent/endocytic comparators were all downstream-flat or self-only in the focal cell group, while the public ClC-5 disease mechanism is strongest in renal proximal-tubule receptor recycling rather than in postnatal thalamic glutamatergic neurons.

## Limits and uncertainty

- `Clcn5` itself was held out, and the selected Distributed Agents corpus has no direct `Clcn5` target record, so there is no same-experiment `Clcn5` expression signature to compare.
- The single-nucleus parquet does not contain raw baseline expression. I therefore did not try to prove that focal neurons lack `Clcn5`; I used held-in functional analogs instead.
- Complete ClC-5 loss in proximal tubule cells is not the same perturbation as sparse P16 CRISPR loss in surviving NeuN+ neuronal nuclei. This makes renal Dent-disease literature useful for mechanism and comparator choice, not for quantitative DEG transfer.
- `Clcn3` and `Clcn4` are paralogs, not ClC-5 replicas. They have different expression patterns and vesicle compartments, and ClC exchangers can homo- or heterodimerize in subfamily-specific ways.
- A prediction of 0 means no measured gene is expected to pass BH FDR 0.05 in this assay. It does not imply ClC-5 is biologically irrelevant, unedited, or harmless in every cell type.
