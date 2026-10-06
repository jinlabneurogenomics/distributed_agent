# Eef1a2 direct DEG-count forecast

## Target and endpoint

- Target: `Eef1a2`.
- Focal population: `151 TH Prkcd Grin2c Glut`.
- Endpoint: number of measured genes with BH-adjusted Wilcoxon `pvals_adj < 0.05`.
- The declared focal training table contains 1,674 training perturbations and excludes `Eef1a2`; its focal counts are very sparse overall, with median 0, 1,205/1,674 targets at 0, 106/1,674 at >=10, 43/1,674 at >=100, and a maximum of 2,677.

## Eef1a2 biology used

- The exact focal-population expression card shows strong target reach in the assayed non-target nuclei: `Eef1a2` is detected in 23,620/23,679 non-target `151` nuclei, 99.75%, with mean raw UMI 13.98 and pseudobulk CPM 876.1. That makes lack of thalamic expression an unlikely explanation for a zero.
- The functional-stock adjudication calls the harvest-time EEF1A2 pool `likely_substantially_depleted`: a P16 edit stops new functional synthesis, the P37-P44 harvest is 21-28 days later, the available heterologous 95-hour protein half-life spans several half-lives over that interval, and the mouse CNS EEF1A1-to-EEF1A2 neuronal isoform switch occurs around the same postnatal window.
- The observability card supports a postnatal neuronal dependency but in an imperfectly matched context. Germline `Eef1a2` loss produces a severe P21-P28 motor-neuron syndrome, while the Perturb-seq endpoint here is a P16 mosaic loss in surviving thalamic glutamatergic nuclei. I therefore treated Eef1a2 as biologically real and well expressed, but not as certain to produce a massive recovered-cell RNA signature.

## Training perturbations that set the scale

I used the focal count table and the focal Parquet score profiles for a compact translation/proteostasis cohort:

| training perturbation | focal n_degs | interpretation |
|---|---:|---|
| `Aimp1` | 0 | cytosolic aminoacyl-tRNA synthetase scaffold; corpus reports no FDR DE and no ISR/UPR/proteostasis RNA program after P16 loss |
| `Eif2ak4` | 0 | integrated-stress kinase; corpus reports no downstream DE |
| `Eif5a` | 0 | translation elongation factor; corpus reports a two-gene, two-cell-class screen-wide response rather than a pan-neuronal translation-failure signature |
| `Eif4g1` | 1 | cap-initiation scaffold; corpus reports no downstream FDR<0.10 response in any recovered neuronal group |
| `Eif4h` | 1 | eIF4F-associated training comparator from the Eef2/Eif4g1 corpus contrasts |
| `Eif4a2` | 2 | eIF4F helicase; corpus reports only two downstream FDR<0.10 genes screen-wide and no stress bounce-back program |
| `Mtor` | 2 | mTOR-side cap-initiation regulator |
| `Eef2` | 9 | the closest represented cytosolic elongation-factor comparator; broad elsewhere but only 9 focal DEGs in `151` |
| `Rptor` | 0 | mTORC1-side regulator |
| `Tsc2` | 86 | mTORC1 disinhibition; responsive but mechanistically indirect for Eef1a2 |
| `Opa1` | 37 | mitochondrial/ISR benchmark, useful as a weak stress lower-scale boundary |
| `Atxn10` | 52 | data-driven Eef2 neighbor in other groups, but not a translation factor |
| `Psmc1` | 430 | 19S proteasome ATPase |
| `Psmb4` | 742 | 20S proteasome beta subunit |
| `Ufc1` | 572 | UFMylation/proteostasis stress |
| `Elp1` | 645 | tRNA modification/ISR program |

The Parquet profile comparison over this same set in `151` separated these scales. The direct translation and cap-initiation targets had almost-null focal score profiles and no significant overlap with the proteasome/UFMylation/ISR signatures; `Eef2` had 9 focal DEGs with no shared FDR-significant positive or negative genes against `Aimp1`, `Eif4g1`, `Eif4h`, `Eif5a`, `Mtor`, or `Rptor`. By contrast, `Psmb4`, `Psmc1`, `Ufc1`, and `Elp1` each had hundreds of focal DEGs and shared large same-direction tails with one another, so I treated them as a different stress-state scale rather than a direct numeric donor for Eef1a2.

The same-experiment corpus supports that separation: the packaged `Eef2` comparison explicitly notes that `Eif5a`, `Eif2ak4`, `Eif4a2`, `Eif4g1`, `Eif4h`, `Mtor`, and `Rptor` were flat or nearly flat and that `Tsc2` was broad but nonconvergent; the `Aimp1` findings similarly report no amino-acid-starvation, ISR/UPR, or proteostasis transcriptional program after loss of a cytosolic translation-adjacent scaffold.

## Synthesis

The best same-assay evidence argues against transferring the high proteasome/UFMylation counts to Eef1a2: high-count proteostasis perturbations induce a recognizable NRF1/ISR/apoptosis/autophagy-style survivor state that was not a generic consequence of damaging translation-control genes. The direct translation series instead lands between 0 and 9 focal DEGs.

Within that low band I placed Eef1a2 at the upper edge. Relative to the flat cap-initiation and stress-kinase targets, it is highly expressed in nearly every focal neuron, it encodes the mature neuronal eEF1A isoform after the postnatal switch, and successful editing should reduce the operative elongation-factor pool by harvest. Those features make a true zero less likely than for the weaker or more condition-dependent translation-control comparators, but survivor conditioning, unknown biallelic editing, and the motor-neuron rather than thalamic null literature keep the forecast close to `Eef2` rather than near the broad stress programs.

Point prediction: `9` DEGs.
