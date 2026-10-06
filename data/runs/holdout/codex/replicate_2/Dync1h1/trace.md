# Dync1h1 n_degs forecast

Target and endpoint:

- Target: `Dync1h1`
- Focal population: `151 TH Prkcd Grin2c Glut`
- Endpoint: number of measured genes in this population with BH-adjusted Wilcoxon `p < 0.05`.

Biology prior from the declared target bundle:

- `Dync1h1` is strongly in reach in the focal non-target population: 23,457/23,679 cells express it, with 8.17 mean raw UMI and 5.08 mean CP10K.
- DYNC1H1 is the force-generating heavy chain and scaffold of cytoplasmic dynein-1. Loss of new motor-domain-containing heavy chain should eventually impair retrograde microtubule transport, cargo movement, and organelle positioning.
- The expected functional stock at P37-P44 is not a hard null. Existing dynein-1 complexes can persist after editing, but adult postmitotic photoreceptor data place clear Dync1h1-dependent structural failure in the same 3-4 week interval. The characterization therefore supports material engagement by harvest, with uncertainty from pool- and cell-type-specific protein persistence.
- The related dynein-2 heavy chain `Dync2h1` is a distinct ciliary motor, so it is not strong redundancy evidence for buffering dynein-1 heavy-chain loss in thalamic neurons.

Training-scale evidence:

- The declared focal count table has 1,674 training perturbations. It is very sparse: median 0, 75th percentile 1, 90th percentile 2, 95th percentile 18, 99th percentile 430, with 1,205 zero-count targets. I therefore treated any nonzero tens-scale count as already an enriched response relative to the screen background.
- The closest assayed direct transport analogue was `Dctn1`, a dynactin component. In `151 TH Prkcd Grin2c Glut`, `Dctn1` had 75 DEGs at the requested `pvals_adj < 0.05` cutoff and its top calls were a coherent sterol/SREBF2-like induction (`Insig1`, `Msmo1`, `Hmgcs1`, `Cyp51`, `Hmgcr`, `Fdft1`, `Sqle`, `Dhcr24`) plus the self transcript.
- Same-experiment Dctn1 reports interpret this as a recurrent neuronal SREBF2/cholesterol feedback module, not as a generic dynein/dynactin mRNA autoregulatory program. That made `Dctn1` an informative but imperfect magnitude anchor for `Dync1h1`.
- Nearby transport and cytoskeletal controls show that the assay is not automatically high for every motor-associated perturbation: `Kif1a`, `Kif5a`, and `Kif5c` each had 1 DEG; `Tuba1a` had 7, `Tuba4a` had 2, `Map6` and `Nin` had 0, `Htt` had 3, and `Hap1` had 0.
- Endolysosomal and membrane-traffic responders set a broader upper context rather than a dynein-specific point: `Rab7` had 501 DEGs and induced late endosome/lysosome, sterol, proteasome, and neuronal downshift programs; `Vps35` had 17; `Vps54` had 31; `Tsc2` had 86. The `Rab7` count is too broad to transfer directly to a dynein motor but shows that this focal class can mount a large nuclear RNA response to organelle-traffic stress.
- The recurring sterol submodule around the Dctn1/Htt/Mib1/Marchf6/Selenoi/Srebf2 findings was usually weaker than `Dctn1` in the exact count table: `Mib1` 27, `Marchf6` 14, `Selenoi` 5, `Srebf2` 7, `Htt` 3.

Synthesis:

`Dync1h1` should be above the screen background because the target is expressed in essentially all focal neurons and the edited gene encodes an indispensable, nonredundant dynein-1 motor component whose functional stock is expected to decline over the harvest window. I did not project the 501-DEG `Rab7` state because that includes a strong lysosomal/proteasome stress layer not present in the dynein/dynactin sterol module. I also did not project the near-zero kinesin/cytolinker targets because DYNC1H1 is a direct core motor and has stronger stock-realization evidence than those mostly buffered perturbations.

The closest quantitative anchor is therefore an attenuated `Dctn1`-like response: real enough to cross FDR for a sterol/transport feedback program, but smaller than `Dctn1` because mosaic CRISPR may leave monoallelic or old-protein-buffered dynein-1 capacity in recovered thalamic neurons. I place the point in the tens, below `Dctn1`'s 75 and above the `Vps35`/`Mib1`/`Marchf6` range.

Forecast: `40`
