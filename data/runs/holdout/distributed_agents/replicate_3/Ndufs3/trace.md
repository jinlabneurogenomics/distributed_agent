# Prediction trace for 151 TH Prkcd Grin2c Glut

## Question and resolved ambiguities

The requested held-out perturbation is `Ndufs3`. I interpreted `n_degs` exactly as in the training CSV: for the focal `151 TH Prkcd Grin2c Glut` cell group, count every measured gene with `pvals_adj < 0.05` in the Wilcoxon differential-expression table. I therefore allowed the perturbed gene itself to count if its own transcript was significantly reduced. This matters for complex-I targets because most nonzero focal counts in this neighborhood are one-gene self-transcript calls, not secondary stress programs.

The target was absent from both supplied training inputs, so no `Ndufs3` endpoint or `Ndufs3` expression signature was used.

## Sources used

- Supplied endpoint table: `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
- Supplied differential-expression parquet: `training_de_all_cell_groups.parquet`, filtered to `group_name == "151 TH Prkcd Grin2c Glut"` for the focal endpoint.
- Distributed Agents same-experiment corpus, release `perturbai-july-260713-sourceguard-1773-v1`.
  - No `Ndufs3` target-centered findings were present.
  - I used target contexts for `Ndufs2`, `Ndufs4`, `Ndufs7`, `Ndufs8`, `Ndufv1`, and `Ndufv2`, which contain same-experiment claims that represented nuclear complex-I subunits and assembly factors are broadly buffered and fail to form a shared acute OXPHOS/mitochondrial-stress transcriptional module in this P16 mosaic neuronal CRISPR assay.
- Distributed Agents runtime profile tools.
  - I compared 12 represented NDUF/NDUFAF/`Timmdc1` targets in the focal cell group and inspected the Q/N-module core subunits against represented assembly and accessory subunits.
- PubMed literature.
  - Benit et al. 2004, DOI `10.1136/jmg.2003.014316`, PMID `14729820`: human `NDUFS3` mutations cause complex-I deficiency and Leigh/Leigh-like disease.
  - Peralta et al. 2020, DOI `10.1172/jci.insight.141183`, PMID `33148885`: a neuron-specific mouse `Ndufs3` conditional knockout reduced complex-I activity, altered brain energy metabolism, and caused neurological phenotypes.
  - D'Angelo et al. 2021, DOI `10.1016/j.celrep.2021.109002`, PMID `33882309`: graded NDUFS3 depletion disrupts complex-I maturation and shows NDUFS3 is a core subunit needed for normal complex-I assembly and function.
  - van de Wal et al. 2022, DOI `10.1093/brain/awab426`, PMID `34849584`: review of `Ndufs4` complex-I/Leigh mouse models, used only to anchor `Ndufs4` as a severe same-complex disease comparator whose sparse Perturb-seq response is therefore informative.

## Computation over the supplied DE data

1. Loaded the requested-target manifest and verified that it contains exactly one row, `Ndufs3`.
2. Loaded the focal training count CSV and summarized its calibration:
   - 1,674 training perturbations.
   - Median `n_degs = 0`.
   - 75th percentile `n_degs = 1`.
   - 95th percentile `n_degs = 18`.
   - The assay has a very long right tail, but most perturbations have no or one FDR-significant gene.
3. Selected focal rows from the 8.3 GB parquet with this predicate:

   ```python
   (group_name == "151 TH Prkcd Grin2c Glut") &
   gene_target.isin(complex_I_and_mitochondrial_comparators)
   ```

   and counted `pvals_adj < 0.05` per target. This is the same endpoint definition as the training CSV, but restricted to hand-selected mechanistic analogs and counterexamples.

4. Queried the focal signatures for canonical mitochondrial stress/ISR sentinels (`Asns`, `Chac1`, `Ddit3`, `Slc7a5`, `Shmt2`, `Lonp1`, `Clpp`, `Hspd1`, `Hspa9`, `Hspe1`, `Atf4`). These genes were flat at adjusted `p = 1` across represented NDUF subunit perturbations, whereas `Opa1` in the same focal cell group induced a clear amino-acid/ATF4-like stress response: `Asns` q `2.39e-7`, `Chac1` q `2.57e-5`, `Ddit3` q `2.75e-5`, and `Slc7a5` q `1.80e-3`.
5. Ran `profile_compare` on `Ndufs2`, `Ndufs4`, `Ndufs7`, `Ndufs8`, `Ndufv1`, `Ndufv2`, `Ndufa9`, `Ndufa10`, `Ndufaf2`, `Ndufaf4`, `Ndufaf5`, and `Timmdc1` in the focal cell group. Among 12 focal complex-I profiles, 8 had no significant features and 4 had only 1 to 9. Inspecting the closest Q/N-module core genes against the assembly/accessory peers showed zero intersections among their FDR-significant positive or negative features; shared top-tail rows were non-significant, with q-values of 1.0, and therefore were treated as low-prevalence rank noise rather than as a module.

## Target-specific evidence

### `Ndufs3`

`Ndufs3` encodes a nuclear core subunit of mitochondrial respiratory-chain complex I. Literature makes clear that this is a real complex-I loss, not a peripheral annotation: human pathogenic `NDUFS3` variants cause complex-I deficiency and Leigh syndrome (Benit et al. 2004), neuronal conditional `Ndufs3` deletion in mouse impairs complex-I activity and brain energy metabolism (Peralta et al. 2020), and graded NDUFS3 depletion in mammalian cells perturbs complex-I maturation (D'Angelo et al. 2021).

The appropriate within-dataset analogs are therefore other represented nuclear complex-I structural subunits, especially Q/N-module genes:

| training perturbation | focal `n_degs` | focal expression evidence | interpretation for `Ndufs3` |
|---|---:|---|---|
| `Ndufs2` | 1 | only significant row was `Ndufs2` itself, logFC `-0.728`, q `8.26e-12` | Closest Q-module core analog; supports self-transcript depletion but no secondary state. |
| `Ndufs4` | 0 | no focal FDR genes; Distributed Agents corpus reports no downstream FDR<0.10 genes across all 20 recovered neuronal groups | Strong same-complex disease comparator, but transcriptomically buffered in this assay. |
| `Ndufs7` | 0 | no focal FDR genes; same-experiment corpus found only one CA3-restricted hit across 23 groups and no mitochondrial ISR | Q-module core analog; argues against a broad `Ndufs3` downstream program. |
| `Ndufs8` | 1 | only significant focal row was `Ndufs8` itself, logFC `-0.650`, q `3.06e-8` | Q-module core analog with the same one-self-gene pattern predicted for `Ndufs3`. |
| `Ndufv1` | 0 | no focal FDR genes; corpus reports zero downstream FDR<0.10 genes in all 22 recovered groups | N-module catalytic-arm analog; supports buffering. |
| `Ndufv2` | 1 | focal singleton was `Cdc40`, logFC `+0.785`, q `0.0279`; no broad mitochondrial program | N-module analog with one idiosyncratic cell-type hit rather than a complex-I module. |

Broader NDUF/NDUFAF targets in the focal endpoint reinforced that these genes sit at the 0/1 boundary:

- Self-transcript singleton calls: `Ndufa10 = 1`, `Ndufa4 = 1`, `Ndufa6 = 1`, `Ndufb10 = 1`, `Ndufb11 = 1`, `Ndufb8 = 1`, `Ndufb9 = 1`, `Ndufc2 = 1`.
- Completely flat in the focal group: `Ndufa11 = 0`, `Ndufa12 = 0`, `Ndufa8 = 0`, `Ndufa9 = 0`, `Ndufaf2 = 0`, `Ndufaf4 = 0`, `Ndufaf5 = 0`, `Ndufb3 = 0`, `Ndufb7 = 0`, `Timmdc1 = 0`.

This was consistent with the Distributed Agents corpus claim that represented nuclear complex-I subunit and assembly-factor perturbations are broadly buffered in the postnatal neuronal nuclear transcriptome and do not form a recurrent acute OXPHOS-stress module. It was also consistent with direct focal marker checks: NDUF targets left `Asns`, `Chac1`, `Ddit3`, `Slc7a5`, `Lonp1`, and chaperone/protease sentinels below threshold, even though `Opa1` with 37 focal DEGs showed that the same cell group and snRNA-seq pipeline can report mitochondrial distress.

I treated `Opa1 = 37` as a counterexample, not a numeric analog. `Opa1` perturbs inner-membrane fusion/cristae biology and was the positive mitochondrial-stress readout in this dataset; the same-experiment evidence repeatedly showed that core complex-I knockouts did not share that ATF4/ISR-like state.

**Zero/nonzero decision.** The data argue strongly for no secondary complex-I stress module in `151 TH Prkcd Grin2c Glut`. The remaining question is whether the target transcript itself would be called. Among the closest focal core subunits, `Ndufs2` and `Ndufs8` had exactly one DEG and it was the edited transcript; `Ndufs4`, `Ndufs7`, and `Ndufv1` had zero; `Ndufv2` had a single non-self hit. Because `Ndufs3` is a core nuclear complex-I transcript like `Ndufs2`/`Ndufs8`, I put it just on the nonzero side and predicted one detectable self-transcript DEG, with no additional downstream DEGs.

Final point prediction: `Ndufs3 = 1`.

## Limits and extrapolation

- The focal experiment provides no observed `Ndufs3` rows. The prediction extrapolates from neighboring complex-I targets and from external `Ndufs3` biology.
- The DE assay measured nuclear RNA only. It did not measure guide indels, NDUFS3 protein, complex-I activity, ATP/NADH, ROS, or selective loss of edited neurons.
- The external `Ndufs3` and `Ndufs4` mouse literature uses strong germline or conditional loss. The screen was acute, sparse, postnatal, AAV-CRISPR loss of function with modest average mRNA depletion, so full disease models are evidence for biochemical importance but not for a broad snRNA DEG count here.
- Exact 0-vs-1 calls for this family depend on self-transcript guide efficiency and sample size. The observed complex-I panel is almost entirely zero or one DEG in the focal group, so one failed or successful self-transcript call changes the integer endpoint.
- Whole-profile similarities among near-flat signatures are not reliable mechanistic evidence. I therefore weighted exact FDR counts, the identity of singleton significant genes, and same-experiment corpus findings over low-rank logFC tail overlaps.
