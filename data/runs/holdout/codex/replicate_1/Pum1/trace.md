# Direct Pum1 DEG-count forecast

## Target and endpoint

- Target manifest: `Pum1`
- Cell group: `151 TH Prkcd Grin2c Glut`
- Endpoint: count of measured genes with Wilcoxon BH-adjusted `p < 0.05`

## Evidence used

The canonical biology bundle identifies Pum1 as a cytoplasmic sequence-specific
RNA-binding regulator whose direct output is mainly post-transcriptional
repression through target translation and mRNA stability. Exact in-assay
non-target expression in the focal population is present and fairly broad:
`pct_cells_expressing = 72.45`, `mean_raw_umi = 1.426`, and
`pseudobulk_cpm = 89.39` for Pum1 in `151 TH Prkcd Grin2c Glut`. The functional
stock card calls Pum1 a renewable free protein regulator and concludes that
functional stock is likely substantially depleted by the P37-P44 harvest after
the P16 disruptive edit, with residual uncertainty because no Pum1-specific
neuronal half-life was available. The same bundle places Pum1 neural phenotypes
in postnatal mouse but mainly through cerebellar/progressive readouts rather
than an exactly matched juvenile thalamic snRNA endpoint.

The declared 151-class training count table is sparse: among 1,674 visible
targets, 1,205 have zero DEGs, the median count is 0, the 75th percentile is 1,
and only 106 visible perturbations reach at least 10 DEGs. This makes a
functional, expressed perturbation insufficient by itself to predict a large
BH<0.05 footprint.

I used visible RNA-regulatory and translational/decay perturbations as the
nearest quantitative boundaries. In the count table, the FMRP/FXR/CYFIP/eIF4G,
miRNA, CCR4-NOT, NMD, and TIA group was almost flat in 151:
`Fmr1=0`, `Fxr1=0`, `Cyfip1=0`, `Cyfip2=1`, `Eif4g1=1`, `Eif4a2=2`,
`Eif4h=1`, `Eif5a=0`, `Ago1=1`, `Ago2=0`, `Tnrc6a=0`, `Tnrc6b=0`,
`Cnot1=0`, `Upf3b=1`, `Dicer1=0`, and `Tia1=0`; median 0, mean 0.44.
Adding the visible narrow cytoplasmic RNA helicase/decay comparators gave the
same median 0 and a mean of 2.27, with `Ddx3x=8` and `Xrn1=20` as the only
members above two DEGs. A direct Parquet scan of the selected 151 profiles
confirmed the same BH<0.05 counts for these comparators.

Packaged same-experiment Findings for the visible comparators matched that
quantitative picture. Ddx3x and Xrn1 produced real but narrow 151/155
glutamatergic responses; Fmr1's expected target-mRNA and secondary stress
programs were absent from the acute nuclear transcriptome; and measured miRNA,
CCR4-NOT, and NMD perturbations did not phenocopy Xrn1. The broad
hundreds-of-DEG RBP profiles in the training table, such as Hnrnpu, Hnrnpc,
Tardbp, Matr3, spliceosome factors, and Rnpc3, are mostly nuclear
RNA-processing or stress-compensation states, so I treated them as evidence
that thalamic neurons can respond to RNA-machinery lesions, but not as
scale-matched analogs for a Pumilio 3'UTR regulator.

Atxn1 is a documented Pum1-regulated transcript and Atxn1 loss has a sizable
151 response in the training count table (`n_degs = 187`), so it keeps the
forecast above a pure null. I did not use it as a magnitude donor because
Pum1 loss should derepress Atxn1 rather than remove Atxn1, and the Atxn1
Finding ledger did not identify a strong opposite measured signature that
would make Atxn1 LoF a calibrated mirror for Pum1 LoF.

## Synthesis

The target is expressed and the edit should reach renewable Pum1 protein by
harvest, so a zero prediction would underweight target reach and the possibility
of direct destabilized mRNAs. The closest assay-matched perturbations show that
acute loss of a sequence-selective translational or decay regulator is usually
silent at nuclear BH<0.05, while Ddx3x and Xrn1 show that a low-count 151
response is plausible for a cytoplasmic RNA regulator without spliceosomal
stress. I therefore placed Pum1 just above the empirical floor but below Ddx3x,
predicting a low single-digit response.

Predicted `n_degs`: 2
