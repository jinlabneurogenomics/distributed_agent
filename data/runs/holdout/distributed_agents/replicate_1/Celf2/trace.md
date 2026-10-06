# DEG-count prediction trace

## Question and endpoint

The requested endpoint is a point prediction of `n_degs` for held-out `Celf2`
loss of function in `151 TH Prkcd Grin2c Glut` neurons. I interpreted `n_degs`
literally as the number of measured genes whose Wilcoxon Benjamini-Hochberg
adjusted p-value is below 0.05 in that focal cell group.

`Celf2` was held out completely: it is absent as `gene_target` in the supplied
DE parquet and absent from the focal training DEG-count CSV. Therefore the
endpoint is absent for `Celf2` in the declared inputs; the training CSV is
direct observation for non-held-out perturbations, and the Parquet supplies
same-experiment expression signatures for those same non-held-out
perturbations.

## Sources used

- Declared endpoint table:
  `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
- Declared DE table:
  `training differential-expression dataset`.
- Requested held-out manifest:
  `single-target request for Celf2`.
- Run-local metadata: `task_bindings.json`, `coverage.json`,
  `dataset_context.md`, `dataset_context.json`, `measurement_registry.json`,
  and `capabilities.json`.
- Same-experiment internal semantic corpus:
  `perturbai-july-260713-sourceguard-1773-v1`. I used its calibration summary
  and BioKG graph only to test whether this release had Celf2-centered
  same-experiment report material. It did not expose `Celf2` as a target node
  and no Finding node in this release reported `Celf2` as a comparator.
- External literature from PubMed:
  - Ladd 2012, *Molecular and Cellular Neuroscience*,
    DOI `10.1016/j.mcn.2012.12.003`, PMID `23247071`.
  - Suzuki et al. 2012, *BMC Biochemistry*, DOI `10.1186/1471-2091-13-6`,
    PMID `22433174`.
  - Mallory et al. 2015, *PNAS*, DOI `10.1073/pnas.1423695112`,
    PMID `25870297`.
  - Schultz et al. 2017, *Molecular and Cellular Biology*,
    DOI `10.1128/MCB.00488-16`, PMID `28031331`.

## Dataset calculations

The focal training table contains 1,674 non-held-out biological targets. Its
endpoint distribution is extremely sparse:

| quantity | value |
| --- | ---: |
| targets with `n_degs == 0` | 1,205 |
| targets with `n_degs > 0` | 469 |
| median | 0 |
| 75th percentile | 1 |
| 90th percentile | 2 |
| 95th percentile | 18 |

The requested target list contains one entry, `Celf2`, and there are no CELF
family knockouts in the focal training CSV (`Celf1`, `Celf3`, `Celf4`, `Celf5`,
and `Celf6` are also absent). I therefore inspected focal-class DE rows for
available non-held-out RNA-binding and RNA-processing perturbations that are
mechanistically more relevant than arbitrary perturbations:

| training target | observed `n_degs` in `151 TH Prkcd Grin2c Glut` | focal expression-pattern evidence |
| --- | ---: | --- |
| `Tia1` | 0 | No gene reached FDR 0.05 among 85 matched perturbed nuclei. |
| `Rbm28` | 0 | No gene reached FDR 0.05 among 143 matched perturbed nuclei. |
| `Hnrnpdl` | 1 | A single significant gene, `Hnrnpu`, with log2FC 0.227 and adjusted p = 0.00609. |
| `Hnrnph2` | 4 | Small signature; the strongest hits were `Rsrp1` log2FC -0.302, adjusted p = 3.62e-09, and `Idh3g` log2FC 0.305, adjusted p = 7.08e-05. |
| `Hnrnpa2b1` | 11 | Weak but nonzero RNA-binding signature; top hits included `Rbm25` log2FC 0.369, adjusted p = 1.13e-05, and `Hnrnpa1` log2FC 1.080, adjusted p = 2.98e-05. |
| `Hnrnpc` | 122 | Moderate splicing/RNA-binding response; top hits included `Txnl1` log2FC 0.812, adjusted p = 7.38e-27, `Rbm25` log2FC -0.513, adjusted p = 4.95e-14, and `Luc7l2` log2FC -0.360, adjusted p = 5.20e-11. |
| `Matr3` | 149 | Moderate RNA-binding signature; top hits included `Ddhd1` log2FC 1.766, adjusted p = 2.64e-49, `Atp9b` log2FC 1.482, adjusted p = 3.53e-38, and `Rsrp1` log2FC -0.693, adjusted p = 1.26e-29. |
| `Tardbp` | 210 | Moderate-to-broad neuronal RNA-binding signature; top hits included target self-signal `Tardbp` log2FC -1.414, adjusted p = 1.60e-39, `Ppp6c` log2FC 1.985, adjusted p = 2.45e-41, and `Gabpa` log2FC 2.248, adjusted p = 1.74e-38. |
| `Hnrnpu` | 733 | Very broad RNA/chromatin-associated response; top hits included `Hnrnpu` log2FC 1.546, adjusted p = 4.45e-43, `Dmtf1` log2FC 1.418, adjusted p = 5.17e-30, and `Rsrp1` log2FC -0.417, adjusted p = 9.99e-24. |

These comparisons bracket `Celf2`. `Hnrnpc` is a particularly useful upper
analog because Schultz et al. showed that CELF2 and hnRNP C can bind the same
upstream intronic element to control TRAF3 exon 8 in activated T cells, but
`Hnrnpc` is a core hnRNP with a broader RNA-metabolism footprint than CELF2 is
expected to have in sparse postnatal thalamic CRISPR. `Tardbp`, `Matr3`, and
`Hnrnpu` are counterexamples against assuming every neuronal RNA-binding
protein is weak in this assay: all had 149 to 733 DEGs. `Tia1`, `Hnrnpdl`, and
`Hnrnph2` are counterexamples against promoting every RNA-binding perturbation
above the sparse background.

Within the focal DE rows, perturbing the inspected analogs did not
significantly change `Celf2` itself or other measured CELF family transcripts:
for example `Celf2` adjusted p-values were 1.0 after `Tardbp`, `Matr3`,
`Hnrnpa2b1`, `Hnrnph2`, `Hnrnpdl`, `Rbm28`, `Sptb`, and `Tia1`, 0.716 after
`Hnrnpu`, and 0.329 after `Hnrnpc`. I therefore did not treat any one of those
signatures as a direct upstream mimic of `Celf2` loss.

## Target-specific reasoning

### Celf2

CELF2/CUGBP2 is a CELF-family RNA-binding protein with three RNA-recognition
motifs. The CELF family is enriched in neural splicing programs and has known
brain and disease-related alternative-splicing roles (Ladd 2012, PMID
`23247071`). CUGBP2/CELF2 isoforms themselves are alternatively spliced during
neural differentiation and in brain, and different isoforms can exert distinct
effects on target exons such as `Actn1` and the insulin receptor in model
systems (Suzuki et al. 2012, PMID `22433174`). CELF2 can also drive widespread
regulated splicing in stimulated T cells (Mallory et al. 2015, PMID
`25870297`) and can cooperate with hnRNP C at an intronic TRAF3 splicing
silencer (Schultz et al. 2017, PMID `28031331`).

Those external data support a real post-transcriptional function, so I did not
assign `Celf2` to the generic all-target median of zero. However, the endpoint
here is not isoform count; it is a gene-level Wilcoxon DEG count among
surviving postnatal neurons after partial mosaic CRISPR loss of function.
CELF2 is more likely to shift splice isoforms than to cause immediate
large-amplitude changes in total nuclear RNA for hundreds of genes. The lack of
any CELF paralog knockout in training prevents a same-family numeric anchor.

The closest training evidence therefore points to a weak nonzero count. The
hnRNP/TIA-family neighborhood contains null to tiny responses (`Tia1` 0,
`Hnrnpdl` 1, `Hnrnph2` 4, `Hnrnpa2b1` 11), while broad RNA-processing
perturbations (`Hnrnpc` 122, `Matr3` 149, `Tardbp` 210, `Hnrnpu` 733) look too
strong for a CELF2-specific splicing regulator in this focal readout. I placed
`Celf2` just below `Hnrnpa2b1`, predicting a detectable but narrow response:
8 genes.

## Limits

This prediction is an extrapolation because the training endpoint has no CELF
paralog knockout and the same-experiment corpus has no Celf2-specific Finding
or comparator report in this release. External CELF2 literature establishes
RNA-binding and splicing biology, but much of the direct mechanistic evidence
comes from immune, P19, or non-mouse systems, not acute CRISPR loss in
postnatal thalamic glutamatergic neurons. Finally, a gene-level DEG count can
miss the primary consequence of a splicing-factor perturbation, so a low
predicted count should be read as a low expected number of FDR-significant
total-expression changes, not as a prediction that CELF2 has no neuronal
function.
