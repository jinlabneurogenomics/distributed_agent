# Question and endpoint

The held-out target for this run is `Thoc2`. I interpreted the task as a scalar prediction of how many measured genes would have `pvals_adj < 0.05` in the held-out `Thoc2` perturbation in `151 TH Prkcd Grin2c Glut` neurons. The number to predict is a screen-specific DEG count among recovered nuclei, not a direct measure of viability, editing efficiency, or THOC2 mRNA loss.

The requested manifest contains one unranked target:

| target | prediction |
|---|---:|
| Thoc2 | 303 |

The output preserves the request order because there is only one row.

# Sources Used

Primary quantitative evidence:

- `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`: direct training endpoint, one row per non-held-out perturbation in `151 TH Prkcd Grin2c Glut`.
- `training differential-expression dataset`: the held-in differential-expression table used to verify DEG counts, focal matched cell counts, top focal genes, and focal same-direction overlaps.

Same-experiment interpretation layer:

- Internal corpus `perturbai-july-260713-sourceguard-1773-v1`, especially the bounded reports and Findings for the held-in TREX perturbations `Thoc1` and `Ddx39b`. This corpus is a curated interpretation of the same Perturb-seq experiment, so I used it to orient mechanistic comparisons, not as an independent replicate.
- The selected corpus BioKG graph was used only to list same-experiment comparators reported around `Thoc1`; graph multiplicity and topology were not used as scores.

External mechanism:

- Puehringer et al. 2020, eLife, DOI `10.7554/eLife.61503`, PMID `33191911`: cryo-EM structure placing THOC1, THOC2, other THO subunits, DDX39B/UAP56, ALYREF, and NXF1-NXT1 in the transcription-export route.
- Kumar et al. 2015, American Journal of Human Genetics, DOI `10.1016/j.ajhg.2015.05.021`, PMID `26166480`: human THOC2 missense variants implicate TREX-mediated mRNA export in syndromic X-linked intellectual disability and can destabilize THOC2 and its TREX-complex partners.
- Kumar et al. 2020, Frontiers in Molecular Neuroscience, DOI `10.3389/fnmol.2020.00012`, PMID `32116545`: expanded THOC2 variant cohort with language disorder/intellectual disability, growth phenotypes, and reduced stability of multiple missense THOC2 proteins.
- Bhattacharjee et al. 2024, Nature Communications, DOI `10.1038/s41467-024-45121-5`, PMID `38331934`: a mouse Thoc2 exon 37-38 deletion model linking compromised THOC2/TREX function to R-loop accumulation, DNA damage, cell death, and adverse neurodevelopment.

I did not use STRING, Gene Ontology, Reactome, or graph degree as quantitative scoring inputs.

# Quantitative Calibration

The focal training count distribution was sparse and heavy-tailed: 469 of 1674 non-held-out perturbations had any `151 TH Prkcd Grin2c Glut` DEG at FDR 0.05, the median was `0`, the 95th percentile was `18`, and the 99th percentile was approximately `436`. `Thoc2` therefore needed a specific same-process analog before predicting a count in the hundreds.

The computational focal query was:

```python
SELECT names, gene_target, logfoldchanges, pvals_adj, scores,
       n_pert_matched, n_ctrl_matched
FROM read_parquet(training_de_all_cell_groups.parquet)
WHERE group_name = '151 TH Prkcd Grin2c Glut'
  AND gene_target IN (... biologically selected analogs and counterexamples ...)
```

I then counted rows with `pvals_adj < 0.05`, inspected the top genes by adjusted p-value, and intersected the `names` sets to check whether a comparator shared `Thoc1` focal DEGs in the same log-fold-change direction.

Key focal training counts were:

| held-in target | focal `n_degs` | focal perturbed nuclei | interpretation for `Thoc2` |
|---|---:|---:|---|
| `Thoc1` | 303 | 121 | Best quantitative anchor: core THO/TREX subunit; induced the focal RNA-processing/export signature. |
| `Ddx39b` | 0 | 48 | TREX-associated UAP56 helicase but not a core THO subunit; a same-route counterexample showing accessory TREX membership alone is not enough. |
| `Snrnp70` | 213 | 135 | Spliceosomal/RNA-processing neighbor; 62 genes overlapped the `Thoc1` focal DEG set and 59 of 62 had the same sign. |
| `Prpf6` | 454 | 72 | Spliceosome neighbor with a broader focal footprint; 45 of 49 overlapping `Thoc1` DEGs were same-direction. |
| `Cdc40` | 624 | 159 | Splicing factor; 48 of 60 overlapping `Thoc1` focal DEGs were same-direction. |
| `U2af2` | 828 | 222 | Splicing factor on the same broad mRNA-biogenesis axis; 66 of 75 overlaps with `Thoc1` were same-direction. |
| `Rnpc3` | 868 | 149 | Spliceosome-related neighbor; 110 of 115 overlaps with `Thoc1` were same-direction. |
| `Tpr` | 1768 | 114 | Nuclear pore/export neighbor; far broader than THO with 103 of 114 overlapping `Thoc1` DEGs same-direction. |
| `Hnrnpu` | 733 | 163 | RNA-binding/chromatin neighbor; 64 of 78 overlaps with `Thoc1` were same-direction. |
| `Ranbp2` | 0 | 65 | Nuclear pore-associated negative counterexample in the focal group. |
| `Setx` | 0 | 153 | R-loop-resolution counterexample; argues against a generic R-loop score. |
| `Ddx3x` | 8 | 138 | Neurodevelopmental RNA helicase but poor focal phenocopy. |
| `Eif4a2` | 2 | 135 | Neurodevelopmental RNA helicase but poor focal phenocopy. |

The `Thoc1` focal signature itself was not a one-gene artifact. Its strongest `151` DEGs included `Sart1`, `Snhg11`, `Anxa6`, `Dgkz`, `Gtf2i`, `Noc2l`, `Brsk1`, `Kif1a`, `Map7d1`, and `Sf3b2`, matching the internal `Thoc1` report's RNA-processing/export plus chromatin and neuronal-traffic interpretation. The packaged `Thoc1` report also showed that the same program was concentrated in a few high-yield neuronal groups; at FDR 0.10 the largest responses were in `151 TH Prkcd Grin2c Glut`, `191 MB P MY GABA`, `155 MB Glut`, and `066 CNU-HYa HY GABA`, with no overt p53/apoptosis, DNA-damage, UPR, or integrated-stress program.

# Target-Specific Reasoning

## Thoc2

`Thoc2` encodes the largest THO/TREX core subunit. The intervention requested here is acute postnatal CRISPR loss of one THO component. Its direct molecular consequence should be impaired THO-dependent mRNP biogenesis and export licensing; that propagates through DDX39B/UAP56, ALYREF/NXF1 handoff, spliceosome-associated RNA processing, and transcription-coupled compensatory programs. The measured endpoint is the downstream nuclear RNA abundance state of recovered thalamic glutamatergic nuclei.

The strongest within-dataset analog is `Thoc1`, not `Ddx39b`. `Thoc1` is the only other represented core THO subunit in the training target list and has `303` observed focal DEGs. It directly lands in the requested cell group with 121 perturbed nuclei and a clear RNA-export/spliceosome-compatible state. The same-experiment report for `Thoc1` also noted that its positive neighbors included `Snrnp70`, `Ddx39b`, `Rnpc3`, `Tpr`, and `U2af2`; in the focal cell group, these spliceosome/export factors shared 49-115 FDR 0.05 genes with `Thoc1`, mostly in the same direction. That pattern makes the `Thoc1` signature a real mRNA-biogenesis response rather than an isolated marker.

The closest counterexample is `Ddx39b`, which had `0` focal DEGs despite acting in TREX. I treated it as a dampening counterexample rather than as the primary estimate. DDX39B is an accessory helicase with the partially related DDX39A/AREX route, while THOC2 and THOC1 are both core THO subunits whose missense or deletion variants can destabilize THO/TREX. The internal `Ddx39b` report also showed that Ddx39b's strongest training response was restricted to `191 MB P MY GABA`; in the requested `151` group its closest downstream p-values all adjusted to 1.0. Thus the `Ddx39b` null says that focal THO/TREX output is component-specific, not that core THO perturbations are buffered.

External THOC2 biology reinforces a nonzero prediction. Human THOC2 variants cause syndromic X-linked neurodevelopmental disease with altered TREX stability, and a hypomorphic mouse Thoc2 deletion produced R-loops, DNA damage, cell death, and adverse neurodevelopment. Those studies differ from this screen because they involve inherited or modelled hypomorphic alleles with developmental exposure, whereas the Perturb-seq assay edits postmitotic P16 neurons and observes only surviving nuclei at P37-P44. I therefore transferred the "core THO disruption is consequential in neurons" part of the prior to the same direction as `Thoc1`, but I did not transfer the full embryonic cell-death or p53/DNA-damage endpoint.

I chose `303` DEGs, equal to the observed focal `Thoc1` count. Values near the broader spliceosome and nuclear-pore perturbations (`Cdc40`, `U2af2`, `Rnpc3`, `Tpr`) seemed too high because `Thoc2` is expected to be a core THO phenocopy rather than a more global spliceosome or pore-basket hit. Values near `0` seemed too low because the exact core THO anchor was already strongly active in the focal cell group and had a pathway-coherent expression pattern.

# Limits

This is an extrapolation from `Thoc1`; no second held-in core THO target such as `Thoc3`, `Thoc5`, `Thoc6`, or `Thoc7` was present in the training DEG-count file. The Parquet cannot score indel formation, THOC2 protein loss, mRNA export flux, R-loop accumulation, intron retention, nuclear/cytoplasmic RNA partitioning, or apoptosis before FACS recovery. The PubMed literature establishes THOC2/TREX neurodevelopmental sensitivity but in alleles, stages, and cell populations that do not exactly match sparse postnatal AAV CRISPR in thalamic glutamatergic neurons. The predicted count is therefore anchored mostly to within-dataset `Thoc1` behavior, with `Ddx39b`, `Ranbp2`, `Setx`, `Ddx3x`, and `Eif4a2` used as counterexamples to avoid a generic RNA-factor or R-loop heuristic.
