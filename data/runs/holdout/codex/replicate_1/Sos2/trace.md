# Sos2 n_degs forecast

## Declared target

- Held-out target manifest: `[local file: Sos2.csv]`
- Target: `Sos2`
- Cell class: `151 TH Prkcd Grin2c Glut`
- Endpoint: number of measured genes with BH-adjusted Wilcoxon `p < 0.05`

I treated the training count CSV and training Parquet as the only same-experiment quantitative measurements for this endpoint. The same-experiment corpus Finding summaries were used only to interpret already measured training comparators; they are another representation of the same experiment, not an independent replicate. I did not query or use a `Sos2` endpoint profile or count.

## Target prior

The biology-only bundle for `Sos2` reports exact focal expression of 10,374 / 23,679 non-target nuclei, or 43.81%, with mean `Sos2` abundance of 0.391 cp10k in `151 TH Prkcd Grin2c Glut`. That gives real but partial reach rather than a target absent from the focal population.

The same bundle makes functional stock loss plausible by harvest: Sos2 is a receptor-linked Ras-family guanine-nucleotide exchange factor, not a durable structural stock, and mouse Sos2 has a measured sub-3-hour fibroblast half-life. A successful edit that blocks resupply should therefore have ample time to deplete the operative protein during the 21-28 day P16-to-P37/P44 window.

The major downward biological bearing is buffering. `Sos1` is the close paralog; direct young-neuron data in the bundle show Sos2-null cortical neurons retained the tested NMDA-, depolarization-, and BDNF-induced ERK responses, and P14 hippocampal LTP was normal. Those assays do not prove thalamic RNA dispensability, but they make a broad basal transcriptional response less likely than functional loss alone would suggest.

## Training measurements used

The focal count table has 1,674 training perturbations. It is highly zero-inflated in this same cell class:

- `n_degs = 0`: 1,205 / 1,674
- `n_degs = 1`: 276 / 1,674
- `n_degs <= 1`: 1,481 / 1,674
- `n_degs <= 4`: 1,542 / 1,674

I then used Ras/MAPK and neurotrophin-adjacent measured perturbations as biology-first comparators for a Ras GEF. Their exact `151 TH Prkcd Grin2c Glut` FDR<0.05 counts were:

| target | n_degs |
| --- | ---: |
| Sos1 | 0 |
| Ptpn11 | 0 |
| Braf | 4 |
| Map2k1 | 4 |
| Map2k2 | 0 |
| Mapk1 | 0 |
| Raf1 | 0 |
| Hras | 0 |
| Kras | 0 |
| Rasa2 | 0 |
| Spred1 | 0 |
| Spred2 | 0 |
| Shoc2 | 1 |
| Ntrk2 | 3 |
| Lztr1 | 1 |

Those 15 comparators had a median of 0 and only 13 DEGs total. A matched Parquet profile comparison over the same 15 targets confirmed that 10 / 15 had no significant features and the remaining 5 were all in the `1_to_9_significant_features` activity bin.

The corpus summaries for the measured Ras pathway targets agree with that quantitative readout. They flag a small Braf/Map2k1 all-down thalamic module involving `Vgf`, `Ptpn5`, `Unc13a`, and `Etv5`, but also explicitly note that `Raf1`, `Map2k2`, `Kras`, `Hras`, `Sos1`, `Ptpn11`, and `Mapk1` did not phenocopy that module. Direct Parquet rows at FDR<0.05 show exactly 4 DEGs for `Braf` and 4 for `Map2k1`; the closest same-family measured target, `Sos1`, had 0.

## Forecast

I assign `Sos2` to the silent end of this local Ras/MAPK distribution. The edit should remove a short-lived protein in the expressing subset, so I would not call the perturbation unreachable, but the most operation-proximal measured node, `Sos1`, is null at the requested threshold, most direct pathway relatives are also null, and the biology bundle gives direct evidence that Sos1 can buffer Sos2 loss in young neurons. The Braf/Map2k1 thalamic module is the main counterweight, but it is already sparse even when a downstream RAF/MEK node is hit.

Point prediction: `0`.
