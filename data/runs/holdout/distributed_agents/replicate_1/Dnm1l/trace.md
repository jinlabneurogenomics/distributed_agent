# DEG-count prediction for `151 TH Prkcd Grin2c Glut`

## Question and resolved ambiguities

The requested held-out perturbation set contains one target:

| target_name |
|---|
| Dnm1l |

I interpreted the endpoint as the integer `n_degs` in the focal
`151 TH Prkcd Grin2c Glut` cell group: the number of measured genes, including
the perturbed target transcript if it is measured, with BH-adjusted Wilcoxon
`pvals_adj < 0.05` in perturbed nuclei versus the matched non-targeting
controls. `Dnm1l` is absent from both supplied training inputs as a perturbation,
so its downstream signature must be inferred from non-held-out perturbations and
external biology. I did not treat measured self-transcript loss as a guide
efficiency score; it only matters because a significant self row itself counts
toward `n_degs`.

## Sources used

- Declared training endpoint:
  `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
- Declared differential-expression parquet:
  `training differential-expression dataset`.
- The run-local PerturbAI atlas dataset portrait, task bindings, compact corpus
  coverage, measurement registry, and capability manifest in
  `codex_runtime/pipeline/`.
- The selected same-experiment semantic corpus,
  `perturbai-july-260713-sourceguard-1773-v1`, via the bounded July Findings
  ledger for represented comparators `Dnm1`, `Mff`, `Opa1`, and `Yme1l1`.
- External literature retrieved through NCBI PubMed E-utilities:
  Toyama et al. 2016, Science, DOI `10.1126/science.aab4138`, PMID `26816379`;
  Shields et al. 2015, Cell Death Dis., DOI `10.1038/cddis.2015.94`, PMID
  `25880092`; Zhang et al. 2012, Autophagy, DOI `10.4161/auto.21213`, PMID
  `22732519`; Kleele et al. 2021, Nature, DOI `10.1038/s41586-021-03510-6`,
  PMID `33953403`; Kamerkar et al. 2025, J. Cell Sci., DOI
  `10.1242/jcs.263640`, PMID `40104946`.

## Quantitative calibration from the supplied data

The focal-cell rows were read from the declared parquet by filtering
`group_name = '151 TH Prkcd Grin2c Glut'`. This produced 28,891,566 rows,
1,674 training perturbations, 17,259 measured genes, and 23,526 significant
target/gene rows at `pvals_adj < 0.05`. Those counts match the scale of the
training endpoint file.

The training endpoint is extremely zero-inflated and right-skewed:

| statistic over 1,674 training perturbations | n_degs |
|---|---:|
| median | 0 |
| 75th percentile | 1 |
| 90th percentile | 2 |
| 95th percentile | 18 |
| 99th percentile | 436 |
| maximum | 2677 |

Therefore a represented perturbation needs direct evidence for a resolved
stress state to justify moving above the single-digit range. The relevant
mitochondrial-dynamics and mitochondrial-neighbor training perturbations in the
focal group were:

| training perturbation | n_degs | perturbed nuclei | matched controls | focal expression-pattern evidence |
|---|---:|---:|---:|---|
| `Mff` | 0 | 133 | 23679 | no row reached FDR 0.05; the best adjusted p-value was 1.0, including no significant `Asns`, `Ddit3`, `Chac1`, `Slc7a5`, `Mars1`, `Cars`, `mt-Co2`, or self-`Mff` row |
| `Yme1l1` | 0 | 106 | 23679 | no row reached FDR 0.05; no OPA1/ISR sentinel was significant |
| `Rhot1` | 0 | 114 | 23679 | no row reached FDR 0.05 |
| `Tomm40` | 1 | 224 | 23679 | only the self-`Tomm40` transcript was significant |
| `Dnm1` | 1 | 194 | 23679 | the self-`Dnm1` transcript was significant, adjusted p `4.09e-25`; the strongest non-self row had adjusted p `0.575`, and mitochondrial/ISR sentinels were all adjusted p `1.0` |
| `Opa1` | 37 | 195 | 23679 | an inner-mitochondrial fusion/cristae perturbation induced a small but real ATF4/ISR-like response: `Asns`, `Mars1`, `Chac1`, `Ddit3`, `Cars`, self-`Opa1`, `Mthfd2`, `Slc7a5`, and `mt-Co2` all passed FDR 0.05 |

The same-experiment July corpus supports the same split. `Mff:F001` reported
that `Mff` loss produced no FDR<0.10 downstream response in any recovered
neuronal group, and `Mff:F002` contrasted that null with the readily detected
`Opa1` amino-acid/ISR module. `Yme1l1:F001` and `Yme1l1:F003` likewise reported
a pan-null `Yme1l1` FDR surface and no `Opa1`-like ATF4 program despite the
known biochemical connection between YME1L proteolysis and OPA1 isoform
processing. `Dnm1:F001` and `Dnm1:F003` reported that `Dnm1` had only target
transcript loss without a downstream transcriptional module.

## Target-specific biological transfer

### `Dnm1l`

`Dnm1l` encodes DRP1, the cytosolic dynamin-family GTPase that assembles on the
outer mitochondrial membrane and executes mitochondrial fission. MFF is a DRP1
receptor and AMPK-regulated effector of stress-induced fission, while FIS1 and
MiD49/MiD51 provide additional DRP1-recruiting routes and different fission
modes; MFF is particularly tied to midzone divisions and FIS1 to peripheral
fission in the Kleele et al. imaging model. Direct `Dnm1l` perturbation should
therefore impair the same limiting fission process as `Mff`, but at the shared
GTPase step rather than at one receptor branch.

The causal chain I used was:

1. P16 AAV CRISPR loss of `Dnm1l` partially disrupts DRP1 in already
   postmitotic neurons.
2. DRP1 disruption reduces mitochondrial division and can impair mitochondrial
   turnover or axonal bioenergetics.
3. In complete Cre-lox neuronal models, those organelle defects can accumulate
   oxidative damage, respiration defects, synaptic dysfunction, and
   neurodegeneration: Zhang et al. observed mitochondrial oxidative damage,
   impaired respiration, and degeneration after postmitotic DNM1L loss, while
   Shields et al. found that forebrain Drp1 deletion disrupted CA1 axonal
   mitochondrial ATP supply and synaptic vesicle cycling even with long neuronal
   survival.
4. The PerturbAI endpoint, however, is a nuclear RNA FDR count from recovered
   thalamic glutamatergic nuclei only 3 to 4 weeks after sparse viral editing,
   not a morphology, ATP, axonal transport, or cell-loss assay.

The represented same-pathway perturbation that most directly tests this chain
is `Mff`. Its focal count was exactly 0, and its all-neuronal July Finding set
said the null extended across all 22 recovered neuronal groups. That is strong
within-dataset evidence that blocking a DRP1 receptor is usually buffered in
this assay and does not by itself enter the `Opa1` ATF4/ISR state. `Yme1l1`
provides the same caution for another mitochondrial-morphology input: even an
OPA1-processing protease did not copy direct `Opa1` loss at the RNA endpoint.

`Opa1` is the counterexample rather than the template. The direct inner-membrane
fusion/cristae target produced 37 focal DEGs and the expected mitochondrial
stress genes, showing that the assay could detect amino-acid/ATF4 and
respiratory-chain consequences in this exact focal class. But direct OPA1 loss
damages the inner membrane/cristae compartment, whereas loss of DRP1-mediated
fission is an outer-membrane division defect that can be delayed, receptor
branch-dependent, or expressed as axonal energy and quality-control phenotypes
without a broad 3-to-4-week nuclear ISR.

I therefore predicted a near-null `Dnm1l` signature, above the represented `Mff`
and `Yme1l1` nulls only because `Dnm1l` is the central fission GTPase and is
more likely than `Mff` to have a detectable own-transcript row or a single weak
downstream survivor-state row. The predicted count is:

| target_name | predicted_n_degs |
|---|---:|
| `Dnm1l` | 1 |

## Limits

The prediction extrapolates because none of `Dnm1l`, `Fis1`, `Mief1/MiD51`,
`Mief2/MiD49`, `Mfn1`, or `Mfn2` were represented as training perturbations.
`Mff` is the closest represented fission input but not an obligate one-to-one
surrogate for DRP1 itself: other DRP1 adaptors can bypass MFF, and direct DRP1
loss should be a stronger organelle intervention. Conversely, the complete
Cre-lox Drp1 studies used stronger, less mosaic perturbations and different
neuronal populations/time windows than the P16-to-P37/P44 thalamic
glutamatergic PerturbAI assay. The final integer is mainly within-dataset
evidence from `Mff`, `Yme1l1`, `Opa1`, `Dnm1`, `Tomm40`, and `Rhot1`, with the
external DRP1 literature used only to move `Dnm1l` from a strict zero to a
single expected FDR hit rather than to an `Opa1`-scale ISR count.
