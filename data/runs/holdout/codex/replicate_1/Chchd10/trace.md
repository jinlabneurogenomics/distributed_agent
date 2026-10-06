# Direct Chchd10 DEG-count forecast

## Endpoint and measured training scale

- **Target:** `Chchd10`
- **Cell group:** `151 TH Prkcd Grin2c Glut`
- **Endpoint:** number of measured genes in that cell group with BH-adjusted Wilcoxon `pvals_adj < 0.05`.

The declared focal count table contains 1,674 training perturbations. Its focal counts are extremely sparse: 1,205/1,674 are `0`, 276 are `1`, the median is `0`, the 75th percentile is `1`, the 90th percentile is `2`, and only a small tail exceeds a few dozen DEGs. That makes a generic thalamic forecast near 0-1 before using Chchd10 biology.

## Chchd10 biology bundle

The declared Chchd10 biology-only bundle puts the target within measurable reach in the exact focal population: `Chchd10` was detected in 17,776 of 23,679 matched non-target nuclei in `151 TH Prkcd Grin2c Glut` (`75.0707%`), with mean raw UMI `1.7351`, mean CP10k `1.0615`, and pseudobulk CPM `108.7437`. Thus a near-null call would not be driven by absence of the transcript in this class.

The same bundle makes functional target depletion plausible after the P16 edit: CHCHD10 is a labile intermembrane-space / inner-membrane-associated mitochondrial protein, the edit-to-harvest interval is 21-28 days, and the curated turnover fact gives an approximately 4-hour cellular half-life, albeit from HEK293 cells. The consequence prior is much weaker than the realization prior: the card notes partial functional redundancy with `Chchd2`, and the closest mouse single-knockout evidence had loss of detectable CHCHD10 in brain but no gross abnormality through 200 days and no selected forebrain respiratory or substantia-nigra ultrastructural defect at 100 days.

## Training perturbations used

`Chchd10` is absent from the same-experiment corpus ledger, so I used the declared biology plus training-available mitochondrial comparators instead of a direct Chchd10 report. The typed offline analog nomination over the exact 1,674-gene training universe placed the strongest relevant candidates in mitochondrial membrane organization, MICOS/cristae, mitochondrial intermembrane-space, and broader mitochondrial communities. I interpreted those nominations biologically rather than as a score: `Opa1` is the assay-positive mitochondrial ISR benchmark; `Chchd2`, `Micos13`, `Yme1l1`, `Mff`, `Tomm40`, `Uqcrq`, `Park7`, and OXPHOS genes are the buffered side of the same neighborhood.

Exact focal `n_degs` values from the declared count table:

| perturbation | focal n_degs |
| --- | ---: |
| Opa1 | 37 |
| Chchd2 | 1 |
| Micos13 | 0 |
| Stard7 | 0 |
| Snca | 0 |
| Park7 | 1 |
| Yme1l1 | 0 |
| Mff | 0 |
| Tomm40 | 1 |
| Uqcrq | 1 |
| Ndufs2 | 1 |
| Ndufa4 | 1 |
| Afg3l2 | 0 |
| Lonp1 | 0 |
| Uqcrfs1 | 0 |
| Uqcrh | 0 |
| Uqcrb | 0 |
| Cox4i1 | 0 |
| Cox5a | 1 |
| Ndufs4 | 0 |

The focal Parquet slice confirmed that most `1` counts in this mitochondrial panel were not downstream programs. `Chchd2`, `Ndufs2`, `Ndufa4`, `Cox5a`, `Park7`, and `Tomm40` each had only the perturbed transcript itself significant at FDR < 0.05; `Uqcrq` had a single `Gpr180` hit. `Opa1`, in contrast, had a genuine 37-gene focal ATF4/amino-acid-stress signature including `Asns`, `Mars1`, `Chac1`, `Ddit3`, `Cars`, `Mthfd2`, `Slc7a5`, `mt-Co2`, and its own transcript.

## Same-experiment corpus interpretation

The packaged reports argue that Opa1 should be treated as a positive stress benchmark, not as a scale donor for every mitochondrial perturbation:

- `Chchd2:F002` and `Chchd2:F003` report that `Chchd2` did not induce the OMA1/DELE1/eIF2alpha mitochondrial ISR captured after `Opa1`, and that `Chchd2` grouped with weak or flat mitochondrial/Parkinson comparators rather than the Opa1 mtISR state.
- `Yme1l1:F001-F004` report a pan-null FDR surface and no Opa1-like ATF4/ISR program after `Yme1l1`.
- `Mff:F001-F002` report no downstream FDR response and explicit uncoupling from the Opa1-like mitochondrial integrated-stress program.
- `Micos13:F001-F003` report only two sparse non-thalamic GABA singleton hits and no Opa1-like canonical mitochondrial ISR/OXPHOS/lipid-stress program.

The report-derived topology among `Chchd2`, `Micos13`, `Opa1`, `Yme1l1`, `Mff`, `Tomm40`, `Uqcrq`, `Park7`, and `Snca` was connected except for the held-out `Chchd10`, but the edges themselves were mostly contrasts or boundary statements. The shared-Claim context likewise highlighted negative claims: Opa1 activates a detectable ISR-like amino-acid program while represented mitochondrial comparators such as `Ndufs2`, `Mff`, `Ndufa4`, and `Yme1l1` do not cross that threshold.

## Profile check in the focal class

I symmetrically compared 20 Chchd10-relevant mitochondrial training profiles in `151 TH Prkcd Grin2c Glut` using signed Wilcoxon scores from the declared Parquet. Twelve of the 20 had no significant feature at FDR < 0.05; seven had 1-9; only `Opa1` landed in the 10-49 bin. `Chchd2`, `Micos13`, `Yme1l1`, and `Mff` had no shared significant-feature intersections with `Opa1` or with the singleton OXPHOS/import comparators in the focal inspection, so the direct focal signatures support the corpus boundary between `Opa1` and the buffered comparators.

## Forecast

I did not transfer the 37-gene Opa1 response to `Chchd10`: CHCHD10 is a CHCHD2-interacting, partially redundant regulator, and the represented CHCHD2/MICOS/inner-membrane relatives mostly remained silent in the same P16-to-P37/P44 neuronal screen. At the same time, the exact focal expression of `Chchd10` is high enough that a self-transcript hit is plausible, mirroring `Chchd2`, `Ndufs2`, `Ndufa4`, `Cox5a`, `Park7`, and `Tomm40`, whose only focal DEGs were their own transcripts.

My point forecast is therefore **1 DEG**: a near-null recovered thalamic transcriptional response, with the single counted gene most plausibly arising from the target transcript rather than a downstream mitochondrial ISR program.
