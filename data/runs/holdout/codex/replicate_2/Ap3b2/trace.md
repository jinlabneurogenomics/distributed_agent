# Ap3b2 direct DEG-count forecast

## Target and endpoint

- Target: `Ap3b2`
- Focal population: `151 TH Prkcd Grin2c Glut`
- Endpoint: `n_degs`, the number of measured genes with BH-adjusted Wilcoxon `pvals_adj < 0.05`
- Forecast: `0`

## Evidence used

1. **Prediction-safe target biology.** The declared biology bundle
   `[local file: Ap3b2.json]`
   reports `Ap3b2` as a neuron-specific beta3B subunit of the AP-3B adaptor,
   which sorts selected membrane proteins into synaptic vesicles and neuronal
   processes. It adjudicates the P16 to P37-P44 perturbation window as likely
   to substantially deplete functional AP3B2-containing stock, while noting no
   target-specific acute AP3B2 protein-turnover curve. The same bundle reports
   exact in-assay reach in the focal cell group: `Ap3b2` was detected in
   22,147 / 23,679 matched non-target nuclei, 93.530%, with mean raw UMI
   3.492 and mean CP10K 2.180.

2. **Same-experiment corpus context.** The July corpus had no target findings
   or claims for held-out `Ap3b2`. For the closest represented AP-3/BLOC axis,
   `Ap3b1:F001` reports that `Ap3b1` had zero downstream FDR<0.10 genes in all
   18 measured neuronal groups, `Ap3b1:F003` reports that `Dtnbp1` and
   `Slc32a1` were also FDR-null in `Ap3b1`-matched neuronal groups, and the
   reciprocal `Dtnbp1:F003` finding records that the related BLOC/AP-3
   comparator `Ap3b1` was likewise corrected-DE null in `Dtnbp1`-matched
   groups. Those packaged reports are semantic summaries of the same experiment,
   not independent replication.

3. **Typed analog nomination against the 151 training universe.** Running the
   declared mouse gene-analog nomination entrypoint with
   `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`
   as the explicit training universe placed `Ap3b1` as the sole
   `exact_complex_or_paralog` candidate for `Ap3b2`. The leading broader
   candidates were AP-3 binding, clathrin-coated vesicle cargo-loading,
   synaptic-vesicle transport, and AP-3 adaptor complex annotations rather than
   a stress or transcription-factor module.

4. **Exact 151 count table.** In the declared 151 training count table, the
   modal/median burden is zero: 1,205 / 1,674 targets had `n_degs = 0`, 1,481
   had `n_degs <= 1`, and 1,512 had `n_degs <= 2`. The retained AP-3/BLOC or
   AP-3-adjacent exact counts were:

   | training target | reason retained | 151 `n_degs` |
   | --- | --- | ---: |
   | `Ap3b1` | AP-3 beta subunit, sole exact complex/paralog nomination | 0 |
   | `Dtnbp1` | BLOC/AP-3 trafficking comparator from Ap3b1 Finding | 0 |
   | `Slc32a1` | synaptic-vesicle cargo/adjacent buffered comparator | 0 |
   | `Clcn3` | synaptic/endolysosomal cargo affected by AP3B2-null biology | 0 |
   | `Vps41` | AP-3/HOPS endolysosomal pathway boundary | 0 |
   | `Lamp2` | lysosomal/CMA boundary, borderline self/Ppm1g but no FDR<0.05 hit | 0 |
   | `Atp6v1a` | V-ATPase trafficking/stress boundary | 0 |
   | `Becn1` | autophagy/endosome boundary | 0 |
   | `Atp6v1b2` | V-ATPase boundary nominated through vesicle annotation | 0 |

   Broader vesicle-traffic nominees stayed small rather than Rab7-like in this
   focal group: `Ap1s2 = 0`, `Synj1 = 1`, `Dnm1 = 1`, `Cltc = 3`, and
   `Hspa8 = 9`. The strong alternatives were biologically farther away:
   `Grin1 = 89` and `Rab7 = 501` reflect NMDA-to-nucleus signaling or severe
   late-endosome/lysosomal stress, not a selective AP-3B cargo-sorting lesion.

5. **Declared expression Parquet for selected training profiles.** Direct
   Parquet rows for the retained candidates in `151 TH Prkcd Grin2c Glut`
   confirmed that each selected training target had 17,259 measured genes in
   the focal group and the same `pvals_adj < 0.05` counts as the count table.
   The nearest local analogs were not hiding subthreshold structure near the
   decision boundary: `Ap3b1`, `Dtnbp1`, and `Slc32a1` all had minimum adjusted
   p-value 1.0; `Clcn3` had minimum 0.620; `Atp6v1a` 0.855; `Vps41` 0.204; and
   `Becn1` 1.0. `Lamp2` was the only close boundary near the cutoff, with
   self-transcript FDR 0.0537 and `Ppm1g` FDR 0.0545, still yielding zero
   genes at the requested 0.05 threshold.

## Reasoning

`Ap3b2` is expressed broadly enough in the target thalamic class, and the stock
adjudication argues that a P16 edit should have time to reduce newly assembled
AP-3B by harvest. Those facts rule out a pure no-reach forecast.

The quantitative endpoint, however, is a survivor-conditioned nuclear RNA
response, not synaptic-vesicle cargo localization, zinc loading, electrophysiology,
or seizure latency. The closest measurable perturbations to AP-3 cargo sorting
were sharply buffered in the exact 151 context: the only exact AP-3 analog
`Ap3b1` had no corrected feature and no low-FDR tail, and the BLOC/synaptic
vesicle comparators `Dtnbp1`, `Slc32a1`, `Clcn3`, `Vps41`, `Lamp2`,
`Atp6v1a`, and `Becn1` also sat at zero. Larger signatures in `Rab7`, `Grin1`,
`Cltc`, `Vps54`, and `Hspa8` show that 151 can report endolysosomal stress,
NMDA-linked activity remodeling, and proteostasis states, but they require
more proximal lysosomal failure or receptor/chaperone perturbation than AP-3B
cargo selection.

I therefore treated `Ap3b2` as most likely to match the AP-3/BLOC buffered
branch. Its neuron-specific beta3B role makes a small one- or few-gene response
plausible, but the exact-complex and adjacent measured data put the modal
prediction at no BH-significant genes.
