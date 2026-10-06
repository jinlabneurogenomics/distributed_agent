# Direct forecast trace

Target: `Grik2`

Cell class: `151 TH Prkcd Grin2c Glut`

Endpoint: number of measured genes in this target/cell-class contrast with BH-adjusted Wilcoxon `pvals_adj < 0.05`.

Predicted `n_degs`: `1`

## Evidence used

### Target biology

- The declared biology bundle identified `Grik2`/GluK2 as a low-affinity kainate-receptor subunit in dynamic tetrameric membrane receptors.
- Exact focal-population reach was high: in non-target nuclei from `151 TH Prkcd Grin2c Glut`, `Grik2` was detected in 23,374 of 23,679 nuclei, or 98.71%, with mean raw UMI 7.13 and mean log1p CP10k 1.62.
- The functional-stock card judged the P16 disruptive edit likely to substantially deplete operative GluK2-containing receptors by P37-P44 because new production should stop and surface GluK2 can enter endocytic, recycling, and lysosomal trafficking routes. The same card kept an important uncertainty: basal thalamic GluK2 clearance after editing has not been directly measured.
- The closest organismal phenotypes for `Grik2` loss are germline hippocampal or broad adult mouse observations, so they support neural relevance but not a matched acute thalamic transcriptional program.

### Focal count distribution

- The declared `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` table contains 1,674 training perturbations.
- Counts are very sparse in this cell class: 1,205 targets have `n_degs = 0`; the median is 0; the 75th percentile is 1; the 90th percentile is 2; the 95th percentile is 18.
- The high-count tail is made of broad regulatory and proteostasis hits such as `Uba5` 2,677, `Tpr` 1,768, `Sin3a` 1,433, `Rnpc3` 868, and `Zbtb7a` 841. `Grik2` is not that kind of global RNA-processing, chromatin, or proteostasis perturbation.

### Training perturbations I treated as most informative

Kainate-receptor peers in the focal count table:

```text
Grik1  0
Grik3  0
Grik4  0
Grik5  1
```

The declared Parquet rows for the same focal class showed that `Grik5`'s single BH<0.05 row was the `Grik5` transcript itself (`logfoldchanges = -0.508`, `pvals_adj = 0.000454`), not a downstream module. The other represented kainate subunits had no BH<0.05 focal-class row.

Nearby glutamate-receptor and postsynaptic controls were also mostly self-only or flat:

```text
Gria1   0
Gria2   0
Gria3   0
Grid1   1
Grid2   0
Grin2a  1
Grin2b  2
Grin2d  0
Dlg4    1
Shank2  0
Shank3  2
Syngap1 0
```

The main receptor counterexample was `Grin1`, with 89 BH<0.05 focal DEGs. I treated it as an upper biological contrast rather than a close point donor: `Grin1` encodes the obligatory NMDA-receptor subunit, and the packaged report evidence describes a strong thalamic synaptic/activity state for `Grin1` that did not generalize to `Grik5`, `Dlg4`, or the represented kainate family.

Packaged same-experiment findings for training comparators were concordant with the raw table:

- `Grik5:F001` reported that acute P16 `Grik5` loss was globally transcriptionally buffered outside the on-target transcript.
- `Grik5:F002` reported near-zero convergence among represented kainate-receptor paralogs and explicitly noted that `Grik2` was not a represented training perturbation.
- `Grik5:F003` contrasted flat `Grik5` with active NMDA-receptor perturbations, including the `Grin1` response in `151 TH Prkcd Grin2c Glut`.
- `Dlg4:F001` and `Dlg4:F004` similarly supported the idea that several postsynaptic structural perturbations can be physiologically important yet nearly silent in this postnatal snRNA-seq endpoint.

## Synthesis

`Grik2` is strongly expressed in the focal population, so I did not use the zeros for `Grik1`, `Grik3`, and `Grik4` as evidence that target engagement will be unobservable. A single significant self-transcript row is plausible.

The kinase/chromatin/proteostasis tail of the training table is a poor biological match, while the close kainate and broader glutamatergic synapse perturbations argue against a many-gene downstream state. `Grik5` is the closest assayed kainate-receptor component and produced only its self row in this exact cell class. I therefore forecasted the same endpoint scale for `Grik2`: target-transcript detection plus no durable downstream thalamic RNA program.

Final integer prediction: `1`.
