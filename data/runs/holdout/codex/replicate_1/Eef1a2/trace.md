# Direct forecast for Eef1a2 in 151 TH Prkcd Grin2c Glut

## Target and endpoint

- Target: `Eef1a2`, the only row of the declared holdout manifest.
- Endpoint: `n_degs`, measured genes with BH-adjusted Wilcoxon `p < 0.05` in `151 TH Prkcd Grin2c Glut`.
- I used the declared 151 training count table, the declared training differential-expression Parquet, the Eef1a2 biology bundle, and same-experiment corpus interpretations of training perturbations. The corpus reports and the Parquet are two views of the same experiment, so I treated corpus Findings as interpretation of the training measurements, not independent replication.

## Biology bearing

The biology bundle makes functional Eef1a2 loss plausible in the assay window but not guaranteed to be a large recovered-cell RNA state.

- EEF1A2 is the mature-neuronal translation-elongation GTPase that delivers aminoacyl-tRNAs to the ribosomal A site.
- The target is expressed across essentially the whole focal population: `23620 / 23679` non-target nuclei express `Eef1a2`, with mean raw UMI `13.98` and pseudobulk `876.1` CPM.
- The postnatal P16-to-P37/P44 interval should usually outlast pre-edit stock: the card adjudicates functional stock as `likely_substantially_depleted`; it combines the P14-P20 neuronal EEF1A1-to-EEF1A2 switch, a heterologous EEF1A2 half-life of about 95 h, and the wasted mouse syndrome around P21-P28.
- The main downward caveat is context transfer. The mouse null phenotype is severe but dominated by motor neurons and is germline; this task asks for a sparse P16 CRISPR response in surviving thalamic glutamatergic nuclei.

## Training magnitude anchors in the exact 151 table

The declared 151 count table contains 1,674 training targets and no `Eef1a2` row. Its distribution is sparse and heavy-tailed:

- median `0`
- 75th percentile `1`
- 90th percentile `2`
- 95th percentile `18`
- 97.5th percentile `100`
- 99th percentile `430`

The closest literal translation-control perturbations were weak in this focal class:

| target | n_degs |
|---|---:|
| Eef2 | 9 |
| Eif2ak4 | 0 |
| Eif4a2 | 2 |
| Eif4g1 | 1 |
| Eif4h | 1 |
| Eif5a | 0 |
| Mtor | 2 |
| Rptor | 0 |
| Tsc2 | 86 |

The filtered Parquet rows confirmed that these were not broad latent responses in 151: `Eef2` had only nine FDR < 0.05 genes and the Eif/Mtor positives were mostly self or singleton responses. The corpus makes the same boundary explicit for the same experiment: Eef2 was not phenocopied by Eif5a, Eif2ak4, Eif4a2, Eif4g1, Eif4h, Mtor, or Rptor, and Eif4g1 loss was pan-null or nearly flat in neuronal nuclear RNA.

I therefore did not extrapolate `Eef1a2` directly to the multi-hundred Uba5/Elp1 tail simply because it is a translation gene.

The upward anchors were training perturbations that forced amino-acid/translation or ER-ribosome stress in 151:

| target | n_degs |
|---|---:|
| Opa1 | 37 |
| Dhdds | 116 |
| Elp2 | 150 |
| Atp2a2 | 187 |
| Gfpt1 | 311 |
| Thap11 | 478 |
| Ufc1 | 572 |
| Elp1 | 645 |
| Uba5 | 2677 |

In the Parquet, the Elp1/Elp2/Atp2a2/Gfpt1/Dhdds group induced `Asns`, `Cars`, `Ddit3`, `Chac1`, `Shmt2`, `Herpud1`, amino-acid transporter, and aminoacyl-tRNA synthetase transcripts. `Uba5` and `Ufc1` formed a much broader ER-ribosome-quality-control/proteostasis state and both significantly induced `Eef1a1`, a possible elongation-factor compensation marker. The corpus packages these as Elongator/ATF4-like and UFMylation/proteostasis states, respectively.

## Synthesis

I put the Eef1a2 forecast above the flat Eif4F/Mtor/Eef2 anchors because the target is nearly universally and strongly expressed in the exact focal class, the postnatal neuronal EEF1A2 pool is expected to be the operative EEF1A isoform, and loss of the tRNA-delivery factor could plausibly induce a weak amino-acid/proteostasis compensation program.

I kept the forecast well below Elp1/Ufc1/Uba5 because those training states are specific large U34-tRNA-modification or UFMylation/RQC lesions with observed same-complex reinforcement, whereas the nearest assayed elongation factor `Eef2` produced only nine DEGs in 151 and no generic translation-control nuclear RNA program was present in the training data.

Point forecast: `64` DEGs.
