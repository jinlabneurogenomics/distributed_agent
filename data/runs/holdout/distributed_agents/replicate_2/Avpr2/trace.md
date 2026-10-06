# Question and scope

The held-out request file contained one target, `Avpr2`.  I interpreted the
task as a point prediction of the number of genes that would pass
Benjamini-Hochberg FDR 0.05 in the `151 TH Prkcd Grin2c Glut` comparison after
acute mosaic CRISPR loss of `Avpr2`.  I did not treat this endpoint as a direct
measure of the physiological importance of the receptor, druggability, or edit
success: it is the breadth of the basal snRNA-seq differential-expression
surface in this focal thalamic neuron group.

The input manifest had no duplicate targets and `Avpr2` was absent from the
training-count CSV, as expected for a completely held-out perturbation.

# Sources used

Internal experimental data:

- `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`
  for observed FDR<0.05 DEG counts of non-held-out targets in the focal cell
  group.
- `[local file: training_de_all_cell_groups.parquet]`
  for per-gene signed Wilcoxon scores, log fold changes, adjusted p-values, and
  matched cell counts.
- Distributed Agents same-experiment corpus,
  `perturbai-july-260713-sourceguard-1773-v1`, for target-centered findings and
  bottom-up claims around `Avpr1a`, `Avpr1b`, `Oxtr`, and represented cAMP/PKA
  pathway perturbations.

External biology:

- Birnbaumer 2000, PMID 11091117, DOI `10.1016/s1043-2760(00)00304-0`:
  vasopressin receptor subtype signaling; V1a/V1b couple to Gq/11 and
  phospholipase pathways, whereas V2R/AVPR2 couples to Gs and adenylyl cyclase.
- Bockenhauer and Bichet 2015, PMID 26077742, DOI `10.1038/nrneph.2015.89`:
  AVPR2 controls water reabsorption in collecting duct via AQP-dependent
  antidiuresis; AVPR2 and AQP2 mutations cause primary nephrogenic diabetes
  insipidus.
- Chen et al. 2021, PMID 34579536, DOI
  `10.1146/annurev-pharmtox-052120-011012`: systems-biology review of the
  vasopressin V2 receptor, PKA activation, and aquaporin-2 regulation in renal
  collecting duct.
- Kato et al. 1995, PMID 7589900, DOI
  `10.1046/j.1432-0436.1995.5930163.x`: developmental rat brain V2 receptor
  mRNA was detected in newborn hippocampus/choroid/cerebellum and became much
  more restricted with age, with adult cerebrum below their RT-PCR detection.

# Computation over the training data

I loaded the focal training-count CSV to get the empirical scale.  Of 1,674
training perturbations in `151 TH Prkcd Grin2c Glut`, 1,205 had zero DEGs,
the median was 0, the 75th percentile was 1, the 95th percentile was 18, and
only 106 perturbations had at least 10 DEGs.  A zero or one count is therefore
the modal outcome, not a numeric rounding of a broad response.

I used DuckDB predicate pushdown into the parquet and restricted reads to the
focal cell group and mechanistically selected training perturbations:

```sql
SELECT gene_target,
       COUNT(*) AS n_rows,
       SUM(CASE WHEN pvals_adj < 0.05 THEN 1 ELSE 0 END) AS n_degs,
       SUM(CASE WHEN pvals_adj < 0.10 THEN 1 ELSE 0 END) AS n_degs_fdr10,
       MIN(n_pert_matched) AS n_pert,
       MIN(n_ctrl_matched) AS n_ctrl
FROM parquet_scan(...)
WHERE group_name = '151 TH Prkcd Grin2c Glut'
  AND gene_target IN (...)
GROUP BY gene_target;
```

Each selected target had 17,259 measured genes against 23,679 matched control
nuclei in the focal group.  I also sorted the same rows by adjusted p-value and
absolute Wilcoxon score to inspect whether nominal tails looked like a weak
version of a real program.  Very lowly detected receptor or kidney-marker genes
can show large sentinel log-fold changes with Wilcoxon scores near zero and
FDR 1.0, so I based the comparisons on signed scores and adjusted p-values, not
on those log-fold artifacts.

# Avpr2-specific reasoning

`Avpr2` encodes the vasopressin V2 receptor.  The closest direct receptor
comparators present in the training perturbations were the other neurohypophyseal
peptide receptors:

| training perturbation | focal n_degs | focal n_degs at FDR<0.10 | n_pert |
| --- | ---: | ---: | ---: |
| `Avpr1a` | 0 | 0 | 234 |
| `Avpr1b` | 0 | 0 | 199 |
| `Oxtr` | 0 | 0 | 192 |

This was the strongest within-dataset evidence.  The focal `Avpr1a`,
`Avpr1b`, and `Oxtr` signatures had no FDR<0.10 genes, not a few missed genes
just above 0.05: the best `Avpr1a`, `Avpr1b`, and `Oxtr` adjusted p-values in
the focal group were 0.841, 0.569, and 1.0, respectively.  The Distributed Agents
claim `claim:8a7e4d2d7d5edb7595ca` independently summarized the same release:
represented `Oxtr`, `Avpr1a`, and `Avpr1b` perturbations did not converge on a
shared vasopressin/oxytocin-receptor or Gq/PLC/PKC transcriptional module in
the assayed basal juvenile neuronal groups.  Target-specific Distributed Agents findings
were consistent with this:

- `Avpr1b:F001` reported no robust downstream transcriptome in any of the 23
  recovered neuronal groups, and `Avpr1b:F005` found no meaningful hidden
  whole-signature neighbors.
- `Avpr1a:F001-F005` described only a single robust non-focal Srsf6 event and
  explicitly separated chronic basal `Avpr1a` loss from acute V1a agonist
  signaling.
- `Oxtr:F001` described only three isolated FDR<0.10 genes across all measured
  cell groups, and `Oxtr:F005-F006` rejected a shared receptor/Gq/PLC/CaMK/CREB
  or immediate-early response.

`Avpr2` differs from `Avpr1a`, `Avpr1b`, and `Oxtr` because it is canonically
Gs rather than Gq coupled.  I therefore checked the represented Gs,
adenylyl-cyclase, PKA, PDE, AKAP, and CREB-related perturbations in the same
focal group:

| training perturbation | relationship to AVPR2 biology | focal n_degs |
| --- | --- | ---: |
| `Gnas` | Gs alpha downstream of V2R | 0 |
| `Adcy1`, `Adcy3`, `Adcy5` | cAMP production | 0, 0, 0 |
| `Pde4b`, `Pde4d` | cAMP degradation | 0, 0 |
| `Akap6`, `Akap9`, `Akap11` | PKA/cAMP scaffolding | 0, 0, 1 |
| `Prkaca`, `Prkar1a` | PKA catalytic/regulatory core | 1, 1 |
| `Gsk3b` | AKAP11-linked PKA/GSK3 node | 6 |
| `Creb1`, `Crebbp` | nuclear cAMP-responsive transcription | 10, 8 |

The receptor-proximal cAMP evidence again favored zero.  `Gnas` was completely
flat; the three adenylyl cyclases had no focal DEGs; `Prkaca` and `Prkar1a`
each produced only the edited transcript itself as a single FDR<0.05 gene.
Canonical activity or CREB-associated output genes were absent in these
receptor-proximal signatures: `Fos`, `Egr1`, `Npas4`, and `Arc` were all FDR
1.0 in the focal `Avpr1a`, `Avpr1b`, `Oxtr`, `Gnas`, `Adcy1`, `Prkaca`, and
`Prkar1a` comparisons.  The Distributed Agents cAMP/PKA claim
`claim:7a1996a6fb47a06717d0` reached the same qualitative conclusion for this
training universe: single-gene disruption of represented AKAP localizers and
PKA core nodes was generally buffered at the basal neuronal nuclear RNA level,
with `Gsk3b` a small, 151-specific exception rather than evidence for a shared
AKAP/PKA module.

`Creb1`, `Crebbp`, and `Gsk3b` are useful counterexamples because they show the
focal group is capable of small but real cAMP-adjacent nuclear responses.  They
are poorer quantitative analogs for `Avpr2`, however: `Creb1` and `Crebbp`
directly perturb transcriptional control, while `Gsk3b` is a multifunctional
kinase downstream of many pathways.  None is a ligand-gated, probably
lowly-expressed thalamic GPCR.  Several other GPCRs in the training set were
also zero in the focal group, including `Drd2`, `Drd4`, `Drd5`, all assayed Htr
serotonin receptors, `Crhr1`, `Pth1r`, `Hcrtr2`, `Kiss1r`, `Npsr1`, and
`Lepr`, which further argued against assigning `Avpr2` a broad autonomous
receptor-loss RNA program.

External knowledge pushes the prediction down rather than up.  V2R signaling is
well established as a renal collecting-duct AVP -> AVPR2 -> Gs -> cAMP/PKA ->
AQP2 axis, and human loss-of-function biology is dominated by nephrogenic
diabetes insipidus.  The postnatal, NeuN-enriched, whole-brain-minus-hindbrain
assay deliberately under-samples the renal and choroid/vascular compartments in
which V2 biology is easiest to see.  The only developmental CNS expression
paper I found detected V2 receptor mRNA in newborn rat cerebrum/hippocampus and
cerebellum but not adult cerebrum, which makes a large sustained response in a
P37-P44 mouse thalamic glutamatergic group unlikely.

I therefore predict that `Avpr2` will behave like the nearest assayed
nonapeptide receptors and Gs/cAMP receptor-proximal nodes in this basal neuronal
readout, with no genes passing FDR 0.05:

| target | predicted_n_degs |
| --- | ---: |
| `Avpr2` | 0 |

# Limits

The prediction is an extrapolation because `Avpr2` itself was held out and none
of the exact V2 receptor expression signature was visible.  The most relevant
assayed receptor relatives, `Avpr1a`, `Avpr1b`, and `Oxtr`, are nonapeptide
GPCRs but not V2R/Gs receptors; they mainly bound the expected scale for
neuromodulatory receptor knockouts under basal conditions.  Conversely,
`Gnas`, `Adcy*`, and PKA perturbations test the second-messenger axis but do not
test ligand occupancy, receptor localization, or AVPR2-specific trafficking.
The screen used sparse P16 AAV CRISPR and P37-P44 basal nuclei; it did not
measure acute vasopressin challenge, water/osmotic physiology, behavior,
phosphorylation, peptide release, DNA indels, or the peripheral kidney axis.
Those omissions all matter for AVPR2 biology, but they make a focal FDR<0.05
RNA response less likely rather than justifying a positive DEG count.
