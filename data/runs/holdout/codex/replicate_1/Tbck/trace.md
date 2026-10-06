# Direct forecast for `Tbck`

## Target and endpoint

- Target: `Tbck`
- Focal population: `151 TH Prkcd Grin2c Glut`
- Endpoint: `n_degs`, the number of measured genes with BH-adjusted Wilcoxon `pvals_adj < 0.05`.
- Outcome protection: I used the declared `Tbck` biology bundle, the 151 training count table, and the training Parquet. The bundle provenance reports `target_outcome_exposed=false` and `labeled_neighbors_exposed=false`; the `Tbck` expression signature and count were not in the training table.

## Target biology used

The `Tbck` characterization bundle gives a real but not endpoint-determined perturbation:

- `Tbck` is detectably expressed in the assayed non-target thalamic population: 10,831 / 23,679 non-target nuclei express it, with mean raw UMI 0.667, mean CP10K 0.415, and pseudobulk CPM 41.8.
- TBCK is the catalytic RAB5-GAP subunit of a TBCK/PPP1R21/C12orf4 complex and is also a subunit of the FERRY endosomal mRNA-transport complex.
- Loss is biologically consequential: mouse homozygous loss is developmentally lethal, adult heterozygotes have a behavioral phenotype, and human biallelic inactivating variants cause severe infantile encephalopathy.
- The acute P16-to-P37/P44 realization is uncertain. The edit should block new intact protein synthesis, but no TBCK protein half-life, GAP-complex residence time, FERRY residence time, or acute neuronal clearance curve was available, so pre-edit functional stock could persist into the assay window.
- The card found no close paralog with demonstrated same-context compensation, which argues against a hard null prior, but the evidence still does not prove that 21-28 days of sparse postnatal editing exhausts the operative endosomal complexes.

## Training measurements used

The declared count table contains 1,674 measured training targets for this same population. Its distribution is very sparse:

- 1,205 / 1,674 targets have `n_degs = 0`.
- 469 have nonzero signal.
- 106 have at least 10 DEGs.
- 43 have at least 100 DEGs.
- Median = 0, 75th percentile = 1, 95th percentile = 18, 99th percentile = 454.

Exact p<0.05 counts for the most relevant visible endosomal, autophagy, lysosomal, and mTOR comparators were:

| target | n_degs | interpretation |
| --- | ---: | --- |
| `Rab7` | 501 | strongest same-axis bearing; late endosomal/lysosomal compensation |
| `Tsc2` | 86 | mTORC1/sterol/lysosomal stress output |
| `Vps54` | 31 | GARP/retrograde trafficking response restricted to 151 |
| `Vps35` | 17 | retromer response concentrated in 151 |
| `Depdc5` | 13 | GATOR1 response restricted to 151 and converging weakly with `Rab7`/`Tsc2` |
| `Mtor` | 2 | small loss-of-kinase response in this class |
| `Fkbp1a`, `Gdi1` | 1 each | weak same-broad-axis comparators |
| `Abca7`, `Akt3`, `Ankfy1`, `Appl1`, `Atg16l1`, `Atg5`, `Bcl2`, `Becn1`, `Lamp2`, `Ocrl`, `Pik3cb`, `Pik3r1`, `Pik3r2`, `Rb1cc1`, `Rptor`, `Rubcn`, `Strada`, `Tbc1d23`, `Vps41` | 0 to 4 | many pathway-adjacent perturbations are transcriptionally buffered or below threshold in 151 |

The same-experiment corpus reinforced that these are not interchangeable pathway labels. `Rab7` directly induces a late-endosomal/lysosomal and sterol compensation program; `Tsc2` activates a caudal mTORC1/sterol/endolysosomal program; `Vps54` and `Vps35` produce smaller, 151-biased vesicle-trafficking responses; and canonical autophagy or PI3K/mTOR neighbors often fail to phenocopy those programs.

I also compared `Rab7`, `Tsc2`, `Mtor`, `Tbc1d23`, `Atg5`, `Becn1`, `Lamp2`, and `Tbcd` in the 151 training Parquet. All eight profiles were present. The comparison separated the response magnitudes exactly as the count table did: `Rab7` had 501 significant features, `Tsc2` 86, `Mtor` 2, `Tbcd` 12, and `Tbc1d23`/`Atg5`/`Becn1`/`Lamp2` had no p<0.05 genes in this population. It did not reveal a tight shared significant-gene module that would justify transferring the `Rab7` scale wholesale to `Tbck`.

## Point estimate

TBCK sits upstream of an actually responsive endosomal/lysosomal axis, is expressed in a substantial fraction of the focal thalamic nuclei, and has no obvious same-function paralog. Those features push the forecast above the all-target median of zero and above the many buffered autophagy/lysosome neighbors.

At the same time, the operative lesion is loss of a RAB5 GAP/FERRY subunit, not direct loss of late `Rab7`, and the postnatal 21-28 day stock-depletion evidence is indeterminate. The training table shows that even strong vesicle-trafficking biology often lands in the 10-30 DEG band in 151 rather than at the 501-DEG `Rab7` extreme. I therefore centered the forecast on the `Depdc5`/`Vps35`/`Vps54` band and nudged it upward for TBCK's direct RAB5 endosomal role.

Predicted `n_degs`: **24**
