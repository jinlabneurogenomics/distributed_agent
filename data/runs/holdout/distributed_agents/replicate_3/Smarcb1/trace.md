# Prediction trace for `Smarcb1`

## Question and resolved ambiguities

The held-out readout is the number of measured genes with Benjamini-Hochberg adjusted Wilcoxon `pvals_adj < 0.05` after each genetic perturbation in `151 TH Prkcd Grin2c Glut` neurons.  The target list for this run contains one held-out perturbation, in order:

```text
Smarcb1
```

I interpreted the task as predicting an integer endpoint for this exact focal cell group and this exact juvenile, sparse AAV CRISPR loss-of-function assay.  I used the `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` counts as the calibrated endpoint, because those are already the FDR 0.05 counts requested in the prompt.  Some same-experiment Distributed Agents corpus findings describe FDR 0.10 surfaces; I used those for biological direction and neighbor context but kept all point estimates anchored to the FDR 0.05 training counts.

## Sources used

- `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`: the exact observed `n_degs` endpoint for 1,674 held-in perturbations in the focal cell group.
- `training_de_all_cell_groups.parquet`: focal-group log fold changes, Wilcoxon scores, adjusted P values, and matched cell counts for BAF/mSWI/SNF and nearby chromatin perturbations.
- Distributed Agents corpus MCP, release `perturbai-july-260713-sourceguard-1773-v1`: frozen same-experiment findings and claims, especially the high-confidence 151 TH BAF/mSWI/SNF claim over `Arid1a`, `Arid2`, `Bicra`, `Brwd1`, `Smarca2`, `Smarca4`, `Smarcc1`, `Smarcc2`, `Smarcd1`, and `Smarce1`.
- Distributed Agents runtime `profile_compare`/`profile_cohort`: same 151 profile comparisons over the selected BAF-family cohort.
- External literature and databases:
  - Kadoch et al. 2013, Nature Genetics, DOI `10.1038/ng.2628`, PMID `23644491`, for the composition of mammalian BAF/PBAF complexes and the broad involvement of mSWI/SNF subunits in disease.
  - Mashtalir et al. 2018, Cell, DOI `10.1016/j.cell.2018.09.032`, PMID `30343899`, for modular cBAF, PBAF, and ncBAF organization and the placement of SMARCB1 in the conserved core of final-form complexes rather than in the ncBAF-specific module.
  - Lessard et al. 2007, Neuron, DOI `10.1016/j.neuron.2007.06.019`, PMID `17640523`, for the neural-progenitor to neuron-specific BAF switch and the principle that neuronal BAF function is subunit-combinatorial.
  - Wang et al. 2016, Nature Genetics, DOI `10.1038/ng.3746`, PMID `27941797`, for the observation that SMARCB1 loss compromises SWI/SNF complex integrity and enhancer targeting rather than behaving as an inert accessory loss.

## Computation over the supplied signatures

The training count CSV was read directly to recover endpoint counts.  It has 1,674 held-in targets in `151 TH Prkcd Grin2c Glut`; 469 were nonzero, the median count was 0, and the observed range was 0 to 2,677 DEGs.

The parquet is sorted by `group_name` in row groups, so I inspected Parquet row-group metadata and then read only row groups 546-580, which cover `151 TH Prkcd Grin2c Glut`.  I filtered those rows to a predeclared BAF/chromatin comparator set:

```text
Arid1a, Arid1b, Arid2, Bicra, Brd1, Brd4, Brwd1, Chd4,
Smarca2, Smarca4, Smarcad1, Smarcc1, Smarcc2, Smarcd1, Smarce1
```

For each comparator I checked:

- the number of rows with `pvals_adj < 0.05`, to make sure the parquet-derived counts agreed with the endpoint CSV;
- the target-specific matched perturbed-cell count, since this endpoint is power-sensitive;
- the actual FDR genes and their effect directions;
- exact FDR-overlap counts and whether overlaps moved in the same or opposite logFC direction.

The key endpoint counts in this cell group were:

| target | observed `n_degs` | matched perturbed nuclei | role for `Smarcb1` |
| --- | ---: | ---: | --- |
| `Smarcc2` | 185 | 162 | strongest same-complex shared-core analog |
| `Arid2` | 56 | 170 | PBAF selector, partial analog |
| `Arid1a` | 22 | 316 | cBAF selector, same-direction compact analog |
| `Smarce1` | 11 | 273 | cBAF BAF57 subunit, same-direction compact analog |
| `Smarcd1` | 1 | 208 | weak partial BAF member |
| `Arid1b` | 1 | 173 | flat/near-flat ARID1 paralog counterexample |
| `Smarca2` | 1 | 152 | ATPase paralog counterexample |
| `Smarca4` | 0 | 146 | ATPase paralog counterexample |
| `Smarcc1` | 0 | 165 | BAF155 paralog of active BAF170/Smarcc2; counterexample |
| `Bicra` | 0 | 229 | ncBAF-specific counterexample |
| `Brwd1` | 0 | 117 | BAF-associated reader counterexample |
| `Smarcad1` | 0 | 133 | SWI/SNF-like ATPase family counterexample |
| `Chd4` | 100 | 163 | active NuRD remodeler, often opposite to BAF |
| `Brd4` | 311 | 93 | active chromatin reader but not a BAF structural analog |
| `Brd1` | 4 | 178 | weak chromatin counterexample |

Expression-pattern checks supported the mechanistic subset rather than just the counts.  `Smarcc2` and `Smarce1` shared nine FDR 0.05 genes in the same direction in 151, including `Abhd12b`, `Begain`, `Prkcd`, `Ptpn3`, `Rasa4`, `Reep2`, `Serinc2`, and `Slc25a37`.  `Smarcc2` and `Arid1a` shared 13 FDR genes and all 13 were same-direction, including down-regulation of `Begain`, `L1cam`, `Lrrc7`, `Prkcb`, `Ptpn3`, `Ptprz1`, and `Rasa4` and up-regulation of `Clstn2` and `Nexn`.  `Arid2` was related but less interchangeable: it shared nine FDR genes with `Smarcc2`, seven same-direction and two opposite-direction.  `Chd4` provided an important active counterexample, because it reversed `Abhd12b`, `Begain`, `Ccdc141`, and `Msra` relative to `Smarce1`, and reversed `Begain` relative to `Arid1a`; its 100-gene response is not a simple SWI/SNF phenocopy.

## Target-specific biological reasoning

### `Smarcb1`

`Smarcb1` encodes SMARCB1/BAF47/SNF5/INI1, a core mSWI/SNF subunit.  It is not an ATPase with the obvious `Smarca2`/`Smarca4` single-gene buffering issue, it is not a mutually exclusive ARID selector such as `Arid1a`, `Arid1b`, or `Arid2`, and it is not the ncBAF-specific paralogous axis represented by `Bicra`.  Mashtalir et al. place SMARCB1 in the conserved cBAF/PBAF architecture, and Wang et al. showed that SMARCB1 loss can compromise SWI/SNF integrity and enhancer targeting.  Those external facts make a zero prediction biologically less plausible than for `Smarca4`, `Smarcc1`, `Bicra`, or `Brwd1`: the 151 neurons clearly can report mSWI/SNF disruption, and `Smarcb1` is a nonredundant core member of that active complex family.

The strongest within-dataset analog is therefore `Smarcc2`, not the flat same-family genes.  `Smarcc2` produced 185 DEGs at FDR 0.05, down-regulating the recurrent 151 BAF genes `Ptpn3`, `Reep2`, `Prkcd`, `Prkcb`, `Begain`, `Ptprz1`, `L1cam`, and `Rasa4` and sharing same-direction FDR genes with both `Smarce1` and `Arid1a`.  `Arid1a` and `Smarce1` are narrower cBAF analogs with only 22 and 11 DEGs, while `Arid2` gives a 56-gene PBAF-skewed response that only partly overlaps the `Smarcc2` surface.  Since SMARCB1 should sit upstream of both the compact cBAF recurrent module and at least some PBAF activity, I expect it to be broader than `Smarce1`/`Arid1a`/`Arid2` alone.

I discounted the estimate below simply copying or exceeding `Smarcc2` for three reasons.  First, the Distributed Agents same-experiment claim explicitly found that the 151 BAF response was subunit-selective: `Smarca4`, `Smarca2`, `Smarcc1`, `Bicra`, `Arid1b`, and `Brwd1` were flat, weak, or divergent rather than interchangeable phenocopies.  Second, `Smarcd1` is a shared BAF-family subunit but had only one FDR 0.05 gene here, showing that "complex member" is not sufficient.  Third, the CRISPR readout is a sparse postnatal nuclear-RNA assay; severe or early SMARCB1 biology from tumors and germline disease need not translate into a thousand-gene mature-neuron signature.

Putting those together, I made a nonzero prediction close to, but a little below, the `Smarcc2` count: **150 DEGs**.

## Limits and extrapolation

`Smarcb1` itself was fully held out, so there was no self-signature, no matched 151 nucleus count, and no target-RNA row available.  The point estimate is an extrapolation from other subunits, and the weakest part of the inference is deciding whether SMARCB1 behaves like the active BAF core member `Smarcc2` or like one of the surprisingly flat relatives.  The training data make the latter a real possibility for individual mSWI/SNF genes.  External SMARCB1 evidence is mostly from assembly studies, tumor systems, or developmental contexts; it supports a nonredundant core function but does not calibrate the FDR 0.05 DEG count in postmitotic thalamic mouse neurons after mosaic P16 CRISPR editing.

