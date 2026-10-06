# Question and endpoint

The task asks for one integer prediction for each target in the requested-target manifest:
the number of genes expected to pass Benjamini-Hochberg FDR 0.05 after acute
CRISPR loss of the held-out perturbation in `151 TH Prkcd Grin2c Glut`
neurons.  The manifest for this batch contained one held-out mouse target,
`Ddr2`.

I treated `n_degs` as an assay-specific focal-cell response-breadth endpoint.
The held-out `Ddr2` perturbation itself is absent from both supplied inputs:
`Ddr2` has 0 rows as `gene_target` in the Parquet and 0 rows in the training
count CSV.  The supplied count CSV is direct endpoint evidence for the 1,674
visible training perturbations; the Parquet is expression-pattern evidence for
those same visible perturbations.  Self-target transcript change was used only
as context and never as an editing-efficiency score.

# Sources used

- Declared endpoint table:
  `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
  This gives observed `n_degs` for non-held-out perturbations in the focal cell
  group.
- Declared differential-expression table:
  `training differential-expression dataset`.
  I queried only rows for `151 TH Prkcd Grin2c Glut` and visible candidate
  analogs.
- Requested-target manifest:
  `single-target request for Ddr2`.
- Run-local measurement registry and dataset portrait.  These established that
  the Parquet measures survivor-conditioned relative snRNA-seq differential
  expression, not absolute RNA content, editing exposure, or cell depletion.
- Internal PerturbAI July `july_260713_sourceguard_1773_v1` corpus and BioKG.
  The compact coverage summary had no matched `Ddr2` target, and a BioKG lookup
  returned no `Ddr2` gene or same-experiment Finding records.  I therefore did
  not use packaged same-experiment Findings for `Ddr2`; this is missing corpus
  coverage, not evidence that DDR2 has no biology.
- PubMed literature:
  - Leitinger 2014, DOI `10.1016/B978-0-12-800180-6.00002-5`,
    PMID `24725424`: review of DDR1/DDR2 as non-integrin collagen-activated
    receptor tyrosine kinases that regulate matrix remodeling, survival,
    proliferation, migration, and differentiation in collagen-dependent
    contexts.
  - Min et al. 2023, DOI `10.1038/s41467-023-42626-3`, PMID `37919278`:
    cross-species PSP analysis that prioritized DDR2 from glia-enriched
    disease expression modules, supporting a brain link but in glial tauopathy
    biology rather than in normal postnatal thalamic neurons.

# Quantitative calibration

The training endpoint distribution was strongly zero-inflated: among the 1,674
visible perturbations, the median was 0 DEGs, the 75th percentile was 1 DEG, the
90th percentile was 2 DEGs, and only the 95th percentile reached 18 DEGs.  The
largest responses were core regulatory or RNA/protein-homeostasis genes
(`Uba5`, `Tpr`, `Sin3a`, `Rnpc3`, `Zbtb7a`, `U2af2`, `Psmb4`, `Hnrnpu`, `Yy1`),
not extracellular receptors.

For receptor, collagen, and adhesion analogs of DDR2, I grouped focal-cell
Parquet rows by visible `gene_target` and counted `pvals_adj < 0.05`:

```sql
SELECT gene_target,
       sum(pvals_adj < 0.05) AS n_fdr05,
       min(pvals) AS min_p,
       min(pvals_adj) AS min_fdr
FROM read_parquet(:training_de_all_cell_groups)
WHERE group_name = '151 TH Prkcd Grin2c Glut'
  AND gene_target IN (:rtk_ecm_targets)
GROUP BY gene_target;
```

All close extracellular-matrix or receptor-tyrosine-kinase analogs that were
visible in training were at the same near-null endpoint:

| training perturbation | observed `n_degs` | expression-pattern evidence in `151 TH Prkcd Grin2c Glut` |
| --- | ---: | --- |
| `Axl` | 0 | no FDR 0.05 genes; lowest adjusted p-value 0.36 |
| `Mertk` | 0 | no FDR 0.05 genes; lowest adjusted p-value 0.89 |
| `Met` | 0 | no FDR 0.05 genes |
| `Pdgfrb` | 0 | no FDR 0.05 genes; lowest adjusted p-value 0.64 |
| `Kdr` | 0 | no FDR 0.05 genes |
| `Fgfr1`, `Fgfr2`, `Fgfr3` | 0, 0, 0 | no FDR 0.05 genes for any of the three |
| `Itgb1`, `Itga2`, `Itga4`, `Itga6`, `Itga7`, `Itga8`, `Itga9` | all 0 | no FDR 0.05 genes for any integrin alpha or beta subunit checked |
| `Col2a1`, `Col11a1` | 0, 0 | no FDR 0.05 genes |
| `Musk`, `Ror1`, `Ror2`, `Ntrk1`, `Ntrk3` | all 0 | no FDR 0.05 genes |

Two receptor counterexamples were intentionally kept in view.  `Epha4` had
1 DEG, but the only significant row was the targeted `Epha4` transcript itself
with log2 fold-change -1.03, not a broad downstream state.  `Ntrk2` had 3 DEGs
(`Ntrk2`, `Atp2a2`, and `Vgf`), consistent with a neuronally active BDNF/TrkB
axis; its small nonzero footprint shows that an RTK can be detectable in this
cell group when coupled to a neuronal program, but its biology is a poor match
to DDR2's collagen receptor role.

As a further focal-context check, I queried the measured gene `Ddr2` across all
1,674 visible perturbations in `151 TH Prkcd Grin2c Glut`.  It never passed
FDR 0.05; the smallest adjusted p-value was 0.781.  This does not prove that
the held-out `Ddr2` knockout would have no self-transcript change, but it is
consistent with `Ddr2` not being part of a readily detected, regulatable
transcriptional module in recovered focal neurons.

# Target-specific reasoning

## Ddr2

`Ddr2` encodes discoidin domain receptor 2, a collagen-activated receptor
tyrosine kinase.  Leitinger 2014 describes DDR1/DDR2 as a small RTK subfamily
activated by triple-helical collagens, with signaling most directly tied to
matrix remodeling, migration, proliferation, differentiation, and survival in
collagen-rich developmental and disease settings.  Min et al. 2023 makes the
brain connection for DDR2 in PSP, but through glia-enriched disease modules.
That is an imperfect match to this experiment, which perturbed sparse NeuN+
postmitotic neurons and then asked for survivor-conditioned snRNA-seq
transcriptional effects specifically in thalamic glutamatergic neurons.

Within the dataset, the strongest analogs are collagen/ECM receptors and
related RTKs rather than core transcriptional regulators.  `Itgb1` and the
tested integrin alpha subunits are collagen/adhesion receptor comparators:
every visible integrin comparator listed above had 0 observed focal DEGs.
`Axl`, `Mertk`, `Met`, `Pdgfrb`, `Kdr`, `Fgfr1`, `Fgfr2`, and `Fgfr3` are
counterexamples to a generic "RTK perturbation gives a broad response" rule:
all were 0 in the focal endpoint despite reasonable matched perturbed-cell
counts.  `Col2a1` and `Col11a1` also being 0 is a weaker comparison because
they are ligands or matrix components, not DDR2 itself, but it argues against a
large collagen-sensing transcriptional axis being visible in this neuronal
population.

The causal transfer model was therefore:
acute CRISPR impairment of neuronal `Ddr2` -> less collagen-dependent DDR2
signaling, if the receptor and collagen ligand are present in these neurons ->
less downstream SHC/MAPK/PI3K or adhesion crosstalk -> possible changes in
recovered neuronal gene expression.  The transfer has two weak links for this
endpoint.  First, external evidence places the clearest DDR2 biology in
collagen-rich skeletal, fibroblast, inflammatory, cancer, and glial disease
contexts rather than in postnatal thalamic neurons.  Second, multiple
same-experiment training perturbations at the ECM receptor, RTK, and downstream
MAPK/PI3K level were FDR-quiet in exactly the focal cell group.  No obligate
same-direction visible perturbation supported a small positive value.

I therefore predicted no measured FDR 0.05 genes:

| target | prediction |
| --- | ---: |
| `Ddr2` | 0 |

# Limits

This is an extrapolation from function and visible analogs, not a direct
measurement of held-out `Ddr2`.  The supplied tables have no absolute baseline
expression, no guide editing genotypes, and no pre-recovery depletion
measurement, so I cannot exclude a DDR2 effect hidden by low expression,
ineffective exposure in the relevant nuclei, or selection before snRNA-seq.
`Ddr1`, the closest paralog, was also held out or absent from the visible
training count table, so there was no direct DDR-family perturbation analog.
The external DDR2 brain literature points to glia-enriched tauopathy biology;
because non-neuronal cells are intentionally under-sampled here, that support
does not imply a detectable `151 TH Prkcd Grin2c Glut` response.  The final
integer should be read as a point prediction for this assay's FDR threshold,
not as a claim that DDR2 is biologically inert.
