# Minpp1 n_degs forecast

## Target and endpoint

- Target: `Minpp1`
- Requested cell group: `151 TH Prkcd Grin2c Glut`
- Endpoint: number of measured genes with BH-adjusted Wilcoxon `p < 0.05`
- Point forecast: `0`

## Evidence used

The declared one-row manifest identifies `Minpp1` as the held-out target. I used the declared biology bundle for Minpp1 and the declared 151-class training count table plus filtered Parquet rows for training perturbations; I did not query a Minpp1 same-experiment report or a Minpp1 DE profile.

### Biology of Minpp1

- Minpp1 is an ER-lumen histidine phosphatase for higher inositol polyphosphates including InsP5 and InsP6.
- The biology bundle adjudicates the functional stock as likely substantially depleted by the 21-28 day harvest window: a disruptive P16 edit stops new enzyme production, the best target-specific turnover anchor is about 14.7 h in mouse epithelium, and the operative pool is a renewable soluble-metabolite enzyme rather than a long-lived installed structure.
- Endpoint coupling remains weak. The closest positive mouse neural evidence is developmental and germline, with P21 cortical and E14.5 neural-progenitor findings, not acute loss in postmitotic thalamic neurons.
- Exact non-target expression in the focal population is present but not high: mean 0.899 CP10K, mean raw UMI 1.466, and 16,758 of 23,679 non-target nuclei expressing Minpp1, or 70.8%. This makes the perturbation reachable, but it does not imply strong target-mRNA loss or a downstream response.

### Training-count context

The 151 TH Prkcd Grin2c Glut training count table is highly zero-inflated:

- `n = 1674` training targets
- median `n_degs = 0`
- 75th percentile `= 1`
- 90th percentile `= 2`
- only 132 of 1,674 targets had at least 5 DEGs

The largest responses were broad stress/proteostasis or RNA-processing states, for example `Uba5 = 2677`, `Tpr = 1768`, `Sin3a = 1433`, `Rnpc3 = 868`, and proteasome/RNA factors in the several-hundred range. Minpp1 is not in that regulatory class.

### Local metabolic and inositol-phosphate comparators

The closest available training perturbation to soluble inositol polyphosphate biology was quiet:

- `Ppip5k2`: `0` DEGs in 151; same-experiment Findings report no robust downstream transcriptional response in any measured postnatal brain-neuron group and no durable PPIP5K2-InsP8-XPR1 phosphate-efflux program.

Other phosphoinositide and endomembrane-lipid perturbations in the exact 151 count table were also zero or singleton responses:

- `Inpp5k = 0`
- `Ocrl = 0`
- `Pik3r1 = 0`
- `Plcb1 = 0`
- `Cert1 = 0`
- `Osbpl2 = 0`
- `Acbd5 = 0`
- `Pi4kb = 1`
- `Synj1 = 1`, and that one significant 151 gene was the `Synj1` self transcript

The same-experiment corpus independently describes `Inpp5k`, `Ocrl`, and `Synj1` as part of a membrane-associated phosphoinositide/endocytic neighborhood that did not produce an interchangeable neuronal RNA module. That is a same-screen interpretation, not an external replicate, but it matches the count table and argues that local PI/inositol-phosphate perturbations commonly remain under the nuclear-RNA FDR threshold.

Calcium-pathway comparators similarly separated direct ER-store stress from buffered signaling:

- `Atp2a2`, SERCA2, had `187` DEGs at FDR 0.05 in the exact 151 count table and a clear UPR/ISR signature.
- Related Gq/IP3 or calcium-plasticity components were flat or tiny in 151: `Itpr1 = 0`, `Grm5 = 0`, `Homer2 = 0`, `Ryr2 = 0`, `Ryr3 = 0`, `Atp2b2 = 1`, `Ppp3ca = 4`.

Because Minpp1 loss perturbs inositol-polyphosphate metabolism rather than ER calcium refilling, I treated `Atp2a2` as an upper mechanistic outlier, not as a magnitude donor.

## Synthesis

Minpp1 loss should be realized by harvest in cells where editing succeeds, and Minpp1 RNA is detectable across most focal non-target nuclei. Those facts prevent treating the perturbation as unreachable. The response is nevertheless expected to be a metabolite-level biochemical perturbation with uncertain coupling to steady-state nuclear RNA, and the nearest measured branches of inositol-phosphate, phosphoinositide, IP3/Ca2+, and endomembrane-lipid biology are dominated by 0-1 DEG outcomes in the exact 151 training table.

I therefore forecast that Minpp1 is more likely to sit on the assay floor than to enter even a small multi-gene thalamic response state. The integer point prediction is:

```tsv
target_name	predicted_n_degs
Minpp1	0
```
