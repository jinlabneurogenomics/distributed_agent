# Tacr1 DEG-count forecast

Target: `Tacr1` in `151 TH Prkcd Grin2c Glut`.

The target biology bundle says the edit should be able to deplete functional
NK1/Tacr1 receptor stock by harvest: Tacr1 encodes a dynamic membrane
tachykinin GPCR, adult postmitotic-neuron Tacr1 CRISPR can nearly abolish an
agonist-evoked firing response in another neuronal context, and the bundle
adjudicates functional stock by P37-P44 as likely substantially depleted.
That is only a realization prior, however. The exact focal expression reach is
very low: in the declared non-target TH Prkcd Grin2c Glut population, Tacr1 was
detected in 628 of 23,679 nuclei, or 2.65%, with 783 total UMIs, 2.07
pseudobulk CPM, and mean raw UMI 0.033 per nucleus. A successful receptor loss
is therefore strongly diluted in the aggregated thalamic class unless a very
small Tacr1-positive subset drives a broad basal RNA state.

The declared focal count table had 1,674 training perturbations. Its empirical
mass is already concentrated at zero: 1,205/1,674 targets had `n_degs = 0`,
the median was 0, the 75th percentile was 1, and the 90th percentile was 2.

I used the gene-analog nomination output only to choose biologically typed
comparators. It nominated `Tacr3` as the only training-available narrow
tachykinin receptor module member; the closest receptor or immediate GPCR
effector comparators that were available and relevant were:

`Tacr3`, `Oxtr`, `Oprm1`, `Avpr1a`, `Trpv1`, `Crhr1`, `Grm5`, `Cckbr`,
`Oprk1`, `Kiss1r`, `Adcy1`, and `Plcb1`.

All 12 had `n_degs = 0` in the declared TH Prkcd Grin2c Glut count table. A
direct slice of the expression parquet for those 12 perturbations in the same
focal class likewise found 17,259 measured genes per perturbation and no
BH-significant gene for any of them; even the smallest adjusted p-value across
these receptor anchors was nonsignificant, 0.139 for `Adcy1`, with the other
anchors having minimum adjusted p-values at or above 0.759. Their matched
perturbed-nucleus counts were small but in the same sparse regime expected for
low-reach receptor labels.

The packaged same-experiment corpus also treated these as real receptor-pathway
comparisons rather than just symbol matches. The 12-anchor induced explicit
Finding graph had 11 of the 12 genes in one component and 15 connected pairs
among 66 possible pairs. The target-expanded set from those anchors yielded 22
additional eligible connected neighbors, but these were mostly kinases,
G-protein/second-messenger nodes, or unrelated report comparators; their
focal-class counts were still weak, with 14/22 zeros, a median of 0, and a
maximum of 10. This did not outweigh the more direct zero counts from the
receptor anchors.

The material same-experiment Findings explain why receptor identity should not
be upweighted to a larger count. `Tacr3:F003` reported that represented
KNDy/GnRH-axis comparators including `Kiss1r`, `Oprk1`, `Plcb1`, and `Gnrhr`
did not phenocopy the `Tacr3` response. `Oprm1:F002` and `Oprk1:F002`
described a family-wide basal null for single opioid-receptor losses in this
unstimulated neuronal nuclear RNA assay. `Oxtr:F005` reported no shared
FDR-supported overlap between `Oxtr` and vasopressin-receptor or
Gq/PLC/PKC-related comparators.

Synthesis: Tacr1 is probably functionally editable on a 21-28 day window, so I
would not treat it as an immutable stock target. But its exact TH
Prkcd/Grin2c reach is only 2.65% of assayed non-target nuclei, the closest
tachykinin/GPCR receptor training perturbations are flat in the requested
class, and the broader GPCR report layer is dominated by buffered basal
receptor losses. The forecast is therefore a strict null rather than a small
positive count.
