# Foxp1 direct DEG-count forecast

## Target

- `target_name`: `Foxp1`
- Focal population: `151 TH Prkcd Grin2c Glut`
- Predicted `n_degs`: `1`

## Evidence that determined the point

### Declared target biology

The declared one-row manifest contains only `Foxp1`, and the canonical biology
bundle for `Foxp1` was the only target-specific card used.

The exact focal-population expression row in that bundle puts `Foxp1` in the
assayed thalamic population, but not pan-cellularly:

- `n_cells_expressing`: 11,868 of 23,679 matched non-target nuclei
- `pct_cells_expressing`: 50.120%
- `mean_raw_umi`: 1.152
- `mean_cp10k`: 0.752
- `pseudobulk_cpm`: 72.221

The same bundle adjudicates FOXP1 as a soluble nuclear DNA-binding transcription
factor/dimer and calls its 21-28 day functional stock
`likely_substantially_depleted`, with partial evidence: editing should stop new
intact Foxp1 synthesis, but the turnover argument is extrapolated from a
heterologous FOXP2 chase rather than a direct neuronal FOXP1 half-life. The
observability fields support postnatal neural relevance, but only from striatal
or forebrain evidence; mature P16-to-P37/P44 thalamic loss remains untested.
Foxp1 expression is also regionally restricted in adult thalamus, so the exact
50% in-assay expression reach is a real dilution term for an aggregate thalamic
DE count.

### Training count scale

The visible `151 TH Prkcd Grin2c Glut` training table is very sparse:

- 1,674 training perturbations total
- 1,205 are zero at BH-adjusted Wilcoxon `p < 0.05`
- 1,398 have at most one DEG
- 1,469 have at most two DEGs
- 42 exceed 100 DEGs
- 15 exceed 500 DEGs

The curated `transcription_factor` subset from the same training table is even
more concentrated at zero:

- 344 training TFs
- 284 are zero
- 60 are nonzero
- 15 exceed 20 DEGs
- 11 exceed 100 DEGs
- log1p mean count: 0.391, equivalent to 0.478 on the count scale

Thus a sequence-specific TF prior in this exact population sits near 0-1 DEGs
unless there is a target-specific reason to enter the long high-response tail.

### FOXP and developmental-TF comparators

The declared Foxp1 card named `Foxp2` and `Foxp4` as the relevant FOXP
paralogs. `Foxp4` was not present in the 1,674-gene visible count table, and
the deterministic analog-nomination run found no training-available exact FOXP
paralog or reciprocal corpus comparator; all retained nominees were broad
functional-annotation fallbacks. I therefore treated `Foxp2` as the closest
available biological comparator, not as an automatic quantitative analogue.

`Foxp2` has `n_degs = 0` in the declared thalamic training count table. The
same-experiment Foxp2 Finding ledger reports that Foxp2 produced no
FDR<0.10 downstream response in any of 22 measured neuronal groups, including
the exact `151 TH Prkcd Grin2c Glut` contrast with 245 perturbed and 23,679
control nuclei, and did not recover expected FOXP target-gene regulation. That
is strong evidence that a postnatal neuronal FOXP perturbation can be fully
buffered or temporally displaced in this assay.

Other curated cortical or neuronal fate TFs in the thalamic count table were
also quiet or nearly quiet:

- `Bcl11b`: 0
- `Nfia`: 0
- `Nfib`: 0
- `Nfix`: 0
- `Rorb`: 0
- `Satb2`: 0
- `Tbr1`: 0
- `Tcf4`: 0
- `Mef2c`: 1
- `Sox5`: 2
- `Creb1`: 10

The same-experiment Foxp2 and Tbr1 reports frame this as factor-specific
postnatal TF visibility rather than global TF assay failure: some TF or
chromatin regulators can respond, but the Bcl11/Satb2/Cux/Foxp2
projection-neuron axis is flat or buffered after P16 sparse loss.

### High-count TF boundary

The high end of the TF distribution is real in this population but mostly
belongs to less specific chromatin or broadly required transcriptional
machinery:

- `Sin3a`: 1,433
- `Zbtb7a`: 841
- `Yy1`: 720
- `Cic`: 576
- `Thap11`: 478
- `Rora`: 278
- `Tcf7l2`: 106

I inspected a 53-node profile comparison over the broad Foxp1 analog nominees
and selected TF boundaries in the declared parquet, restricted to
`151 TH Prkcd Grin2c Glut`. Thirty-five of those 53 nodes had no significant
features, eight had 1-9, one had 10-49, and nine had at least 50. The large
outliers (`Sin3a`, `Zbtb7a`, `Yy1`, `Cic`) had hundreds of positive and
negative FDR<0.05 genes; by contrast the closest FOXP and fate-specification
comparators had zero to a few significant genes and did not share a recurrent
significant program with the outliers. I therefore used the high TFs as an
upper-tail boundary rather than as the scale center for Foxp1.

## Synthesis

The forecast balances two opposing facts:

- Upward from zero: Foxp1 is actually expressed in roughly half of the focal
  thalamic nuclei, and the biology card supports depletion of a soluble nuclear
  transcription-factor stock by harvest.
- Downward toward zero: exact thalamic reach is partial, the direct matched
  P16 thalamic loss phenotype is unknown, Foxp2 is completely flat in the
  same high-yield thalamic class and across 22 measured groups, and most
  postmitotic neuronal TF comparators in the training table are also flat.

I therefore placed Foxp1 above a strict no-effect call but still inside the
1-2 DEG band occupied by the low nonzero visible TFs, far below the broad
chromatin/transcription machinery outliers. The resulting integer point is
`1`.
