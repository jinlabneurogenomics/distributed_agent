# Pdss1 n_degs forecast

Target: `Pdss1` in `151 TH Prkcd Grin2c Glut`.

Prediction: `1` measured gene with BH-adjusted Wilcoxon `p < 0.05`.

## Evidence used

- Focal endpoint scale from the declared training count table:
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`
  contains 1,674 training targets in this cell class. The distribution is
  very sparse: 1,205/1,674 targets have `n_degs = 0`, the median is 0,
  1,481/1,674 are below 2, and 1,542/1,674 are below 5.

- `Pdss1` biology from the declared canonical bundle
  `[local file: Pdss1.json]`
  supports real target engagement but not a large RNA response. PDSS1 is an
  obligate PDSS1/PDSS2 polyprenyl-diphosphate synthase subunit for CoQ
  side-chain synthesis; pre-existing CoQ is not instantly removed by editing,
  but the brain CoQ product pool turns over on a multi-day clock. The stock
  card therefore calls the relevant functional stock likely substantially
  depleted by P37-P44, with partial evidence because PDSS1 protein lifetime and
  the thalamic functional reserve threshold were not measured directly.

- The same bundle says `Pdss1` is visible in the exact focal baseline
  population: 19,123/23,679 non-target nuclei express the gene
  (`80.76%`), with mean raw UMI 2.03 and mean CP10K 1.28. I used this only as
  focal reach and as weak support that the target transcript itself could be
  counted if the edit causes detectable RNA loss.

- The closest available CoQ-biosynthesis training perturbation is `Coq5`.
  In the declared focal count table it has `n_degs = 0`. The packaged
  same-experiment report for `Coq5` records an even broader negative result:
  22 measured neuronal groups had zero downstream genes at FDR < 0.10, the
  expected mitochondrial ISR/UPR markers were absent, and unbiased plus
  textbook mitochondrial comparators including UQCRC/CYC1/NDUF, `Lonp1`, and
  `Clpp` were essentially zero-correlation against the `Coq5` score vector.

- Other represented mitochondrial/OXPHOS or mitochondrial-proteostasis
  training counts in the focal class also favored no downstream module:
  `Aco2`, `Afg3l2`, `Clpp`, `Lonp1`, `Yme1l1`, `Ndufs4`, and `Ndufv1` were
  all 0; `Uqcrc2`, `Tomm40`, `Park7`, and `Sdha` were 1; `Opa1` was the main
  mitochondrial-stress exception at 37.

- The focal profile comparison I computed from
  `[local file: training_de_all_cell_groups.parquet]`
  was consistent with the corpus interpretation. `Coq5` had zero significant
  focal features and its best whole-profile neighbor among the inspected
  mitochondrial/stress cohort was only `Opa1` at Pearson 0.032/cosine 0.032.
  `Opa1` itself had 37 significant focal features and an ATF4/ISR-like
  program, but the same-experiment report explicitly treats that state as
  branch-specific: OPA1-processing, fission, respiratory-chain, and CoQ/Complex
  III neighbors generally did not phenocopy it.

- Because the endpoint includes the perturbed transcript itself, I separately
  checked the self rows for all available training targets in the focal
  Parquet. Among 1,642 available self rows, 319 passed FDR < 0.05; examples in
  the selected mitochondrial set with a count of exactly 1 were `Sdha`,
  `Uqcrc2`, `Tomm40`, and `Park7`, each dominated by its own target transcript.

## Synthesis

I treated `Coq5` as the most direct measured pathway comparator for the
downstream CoQ-biosynthesis state and treated the broader mitochondrial/OXPHOS
panel as a boundary. That evidence argues against borrowing the 37-gene
`Opa1` focal ISR response or the much larger proteostasis/UFMylation signatures:
in this screen, acute sparse loss of several respiratory-chain and CoQ-related
targets is buffered or limited to the target transcript in survivor-conditioned
neuronal nuclei.

The `Pdss1` card still makes a complete zero too low as a point estimate: the
gene is broadly detected in the exact focal population, and the perturbation is
expected to deplete a real renewing CoQ-production stock by harvest. I therefore
forecast one FDR-significant row, most likely a target-transcript effect, with
little support for additional downstream significant genes.

No `Pdss1` same-experiment report, `Pdss1` DE profile, or held-out `Pdss1`
outcome was used.
