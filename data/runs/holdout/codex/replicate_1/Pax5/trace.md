# Direct DEG-count forecast for Pax5

## Declared endpoint

- Target manifest: one row, `Pax5`.
- Requested focal population: `151 TH Prkcd Grin2c Glut`.
- Endpoint: `n_degs`, the number of measured genes with Wilcoxon BH-adjusted `p < 0.05` in this focal population.
- The allowed training count table for this focal population contains 1,674 targets and does not contain `Pax5`.

## Biology that determined the direction

The exact in-assay reach of Pax5 in matched non-target nuclei is essentially absent in the focal thalamic class: 33 raw Pax5 UMIs total over 23,679 nuclei, 29 expressing nuclei, `0.1224713881498374%` expressing, pseudobulk CPM `0.08734435669051036`, and mean CP10k `0.0007810105740407115`.

The functional-stock card argues that a disruptive edit should deplete the operative Pax5 pool in the few cells where Pax5 is actually expressed: Pax5 is a renewable nuclear sequence-specific transcription factor, not a durable installed product, and its measured wild-type half-life in mouse pro-B cells is about 9.7 h, far shorter than the P16 to P37-P44 edit-to-harvest window.

That editable-if-expressed prior did not argue for a class-wide thalamic signature. The same bundle says the closest mouse neural loss evidence is developmental cerebellum/midbrain biology, not postnatal thalamic loss, and adult mouse brain evidence supports region-restricted Pax5 with no broad thalamic neuronal expression. Pax2 can compensate for Pax5 in embryonic midbrain-hindbrain patterning, but that has not been tested after postnatal Pax5 disruption in thalamic neurons.

## Training measurements used

The focal training count table is sparse and zero-heavy:

- 1,205/1,674 targets have `n_degs = 0`.
- The median is `0`; the 75th percentile is `1`; the 90th percentile is `2`; the 95th percentile is `18`.
- Large signatures are rare and dominated by broadly required core regulators or RNA/protein-homeostasis genes: the largest counts were `Uba5` 2677, `Tpr` 1768, `Sin3a` 1433, `Rnpc3` 868, `Zbtb7a` 841, `U2af2` 828, `Psmb4` 742, `Hnrnpu` 733, and `Yy1` 720.

I treated those high-count core-machinery perturbations as poor local analogs for Pax5. The more relevant training perturbations were Pax-family developmental transcription factors and B-lineage/Pax5-network genes that are present in the count table:

| group | training targets | focal `n_degs` |
| --- | --- | --- |
| Pax family | `Pax2`, `Pax3`, `Pax4`, `Pax6`, `Pax7`, `Pax8` | all `0` |
| B-lineage or Pax5-network genes | `Ebf1`, `Ebf2`, `Ebf3`, `Bcl11a`, `Tcf3`, `Spi1`, `Cd79a`, `Irf8` | all `0` |

I then checked the declared differential-expression parquet for the same focal class and those selected training perturbations. Across `Pax2`, `Pax3`, `Pax4`, `Pax6`, `Pax7`, `Pax8`, `Ebf1`, `Ebf2`, `Ebf3`, `Bcl11a`, `Tcf3`, `Spi1`, `Cd79a`, `Irf8`, and the additional focal-negative neural marker `Gad2`, there were 258,885 focal-class measured-gene rows. Every selected perturbation had:

- exactly `0` genes with `pvals_adj < 0.05`;
- exactly `0` genes with `pvals_adj < 0.10`;
- matched perturbed-cell counts between 138 and 251 against 23,679 matched controls.

So the local zero calls for this biologically nearby set were not one or two genes just missing BH 0.05.

## Synthesis

The strongest quantitative fact is the exact target reach: Pax5 RNA was detected in only `0.122%` of non-target nuclei in the requested aggregated thalamic population. A postnatal CRISPR edit can plausibly clear Pax5 protein in the rare cells with an operative Pax5 pool, but the perturbation is effectively applied to a Pax5-negative aggregate class. In that regime a small subpopulation response would be diluted below a BH-significant class-wide single-nucleus Wilcoxon signature.

The allowed training data support the same downward placement. Similar Pax-family transcription factors and several Pax5/B-lineage network genes were all full zeros in both the count table and the focal parquet, while the high-count tail came from broadly used homeostatic machinery unlike Pax5.

I therefore assign Pax5 to the silent focal-response mode and predict:

`n_degs = 0`
