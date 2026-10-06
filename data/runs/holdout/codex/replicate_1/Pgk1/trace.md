# Pgk1 direct n_degs forecast

## Target and endpoint

- Target: `Pgk1`.
- Cell class: `151 TH Prkcd Grin2c Glut`.
- Endpoint: count of measured genes with Wilcoxon BH-adjusted `p < 0.05`.
- Prediction: `1`.

## Target biology used

The declared biology bundle identifies PGK1 as a soluble cytosolic phosphoglycerate
kinase that supplies the ATP-producing 1,3-bisphosphoglycerate-to-3-phosphoglycerate
glycolytic step. Pgk1 is measurable in the exact focal population
(`mean_raw_umi = 1.916`; `77.50%` of 23,679 non-target nuclei expressing it;
`pseudobulk_cpm = 120.07`). The functional-stock card judged loss of new enzyme
synthesis likely to have depleted much of the existing soluble PGK1 pool by the
P37-P44 harvest, because the P16 edit precedes harvest by 21-28 days and mouse
PGK1 peptide half-lives measured outside neurons are about 2.8-5.2 days.

That argues against treating Pgk1 as an unexpressed or permanently installed
protein whose edit would be invisible. The same card keeps two downward sources of
uncertainty: the turnover measurement is not from postmitotic thalamic neurons, and
the readout is survivor-conditioned nuclear RNA rather than glycolytic flux,
protein abundance, or neuronal survival.

## Training perturbations that set the scale

The direct Reactome/KEGG/GO glycolysis perturbations present in the 151 training
count table were sparse:

| training perturbation | n_degs at BH p_adj < 0.05 | FDR<0.05 feature in the expression parquet |
| --- | ---: | --- |
| `Hk1` | 1 | `Hk1` only |
| `Pfkm` | 1 | `Pfkm` only |
| `Tpi1` | 1 | `Tpi1` only |
| `Gpi1` | 1 | `Gpi1` only |
| `Eno1` | 0 | none |
| `Dlat` | 1 | `Dlat` only |
| `Pdha1` | 1 | `Pdha1` only |

Thus the closest central-carbon training genes did not induce a downstream
stress or synaptic program in this thalamic class; when they crossed threshold,
the count came from the perturbed transcript itself. Related TCA/OXPHOS and
bioenergetic targets reinforced that low scale: `Dld`, `Ndufs4`, `Cox4i1`,
`Cox6a1`, `Cox7b`, and `Cox8a` were zero, while `Sdha`, `Mdh2`, `Got1`, `Got2`,
and `Cox5a` were self-only at this threshold.

I did not use `Gfpt1` as a same-scale glycolytic donor even though it appears in
HALLMARK_GLYCOLYSIS and has 311 FDR<0.05 genes in the count table. The packaged
same-experiment Gfpt1 report calls the large signature an HBP-to-ER-glycosylation
and ER-proteostasis response, and explicitly notes that upstream glycolysis
perturbations such as `Hk1` and `Gpi1` did not phenocopy it. I also kept `Mdh1`
separate: it had a real 151 cytosolic malate-aspartate-shuttle signature
(`n_degs = 29` at BH 0.05), but reports localized that module to the cytosolic
`Mdh1`/`Got1` arm and showed the mitochondrial MAS half was largely self-only.

## Synthesis

The strongest anchor for Pgk1 is the direct-glycolysis group: a highly expressed
glycolytic enzyme whose transcriptional footprint in this endpoint is expected to
be absent or almost absent beyond the target transcript. Pgk1 has enough focal
expression that a modest guide-averaged transcript decrease could plausibly be
detected, so `0` seemed too low as the point estimate. The visible outliers
(`Gfpt1`, `Mdh1`, `Nrf1`, `Tsc2`) entered qualitatively as evidence that metabolic
or growth-control perturbations can be seen by the assay, but each reflects a
more specialized ER-proteostasis, cytosolic MAS, mitochondrial transcription-factor,
or mTORC1 state rather than PGK1-like glycolytic ATP generation.

I therefore assigned Pgk1 the central self-only glycolysis scale and predicted
one significant gene.
