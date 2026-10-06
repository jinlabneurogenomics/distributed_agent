# Trace

## Target and endpoint

- Target: `Tbck`.
- Cell group: `151 TH Prkcd Grin2c Glut`.
- Endpoint: `n_degs`, the count of measured genes with BH-adjusted Wilcoxon `p < 0.05` in the held-out target contrast.
- Outcome surfaces used: none for `Tbck`; the target DEG count and target expression signature were absent from the declared count table and training Parquet.

## Target biology used

The canonical `Tbck` biology bundle exposed a target prior but no endpoint value. Its exact focal-population expression measurement showed that `Tbck` is measurable in the thalamic class:

- mean log1p CP10K: `0.2818`
- mean raw UMI: `0.6667`
- cells expressing: `10831 / 23679`
- percent expressing: `45.74%`

This argued against an expression-reach null.

The same bundle put TBCK in two endosomal RAB5-associated assemblies:

- the TBCK-PPP1R21-C12orf4 RAB5-GAP complex, with loss expected to hyperactivate RAB5 and disturb early-to-late endosomal maturation, lysosomal enzyme delivery, and autophagic flux in non-neuronal mouse/human systems;
- the FERRY RAB5 effector complex, linking early endosomes and mRNA distribution.

Those facts made an endosomal or lysosomal transcriptional state plausible. I discounted a large obligatory footprint, however, because:

- the relevant TBCK protein half-life and GAP/FERRY residence time were not measured;
- developmental mouse lethality, lifelong heterozygous mouse behavior, and human infantile encephalopathy do not directly time an acute P16 postmitotic thalamic loss;
- the stock card adjudicated functional realization by P37-P44 as `indeterminate`.

## Training perturbations considered

The direct FERRY/GAP partners named by the biology card were not present as observed training targets in the `151 TH Prkcd Grin2c Glut` count table:

- absent: `Ppp1r21`, `C12orf4`, `Cryzl1`, `Gatd1`, `Rab5a`

I therefore used one-hop pathway analogs that were present in the declared count table: autophagy genes, lysosomal/vacuolar genes, retromer/GARP/endosomal genes, TBC/RAB relatives, and mTOR/Rag pathway regulators.

Across the full 1,674-target `151` training table the count distribution was sparse: median `0`, mean `14.05`, `469/1674` targets with at least one DEG, `106/1674` with at least 10 DEGs, and a strong right tail with maximum `2677`.

The selected endosomal/mTOR/RAB analog counts in the same held-out cell group were:

| target | `151` n_degs | interpretation |
| --- | ---: | --- |
| `Rab7` | 501 | strong late-endosome/lysosome perturbation; likely an upper-tail analog rather than the expectation for every endosomal gene |
| `Tsc2` | 86 | strong mTOR-axis response |
| `Vps54` | 31 | moderate GARP/endosomal trafficking response |
| `Vps35` | 17 | moderate retromer/endosomal response |
| `Depdc5` | 13 | moderate Rag/mTOR-regulatory response |
| `Mtor` | 2 | weak direct mTOR response |
| `Atg16l1`, `Atg5`, `Lamp2`, `Rptor`, `Tbc1d23`, `Tbc1d24`, `Tbc1d32`, `Vps13a`, `Vps13b`, `Vps13c`, `Vps35l`, `Vps41`, `Vps53` | 0 | no detected downstream DEGs in this class |

The expression Parquet agreed with these count-table values for the nonzero analogs in `151`; for example `Rab7`, `Tsc2`, `Vps54`, `Vps35`, `Depdc5`, and `Mtor` had `501`, `86`, `31`, `17`, `13`, and `2` BH-significant genes respectively. A symmetric `151` profile comparison over the 19 analogs found no missing profiles and bucketed the cohort as 13 no-response targets, one 1-to-9 response target, three 10-to-49 response targets, and two 50-plus response targets, which reinforced that the broad pathway neighborhood is mostly quiet with a few large outliers.

## Synthesis

I did not set `Tbck` to zero because it is expressed in 45.7% of the focal control nuclei and loss of its RAB5 endosomal complexes is mechanistically relevant to ongoing neuronal trafficking. I also did not treat `Rab7 = 501` as the central analog because `Rab7` is itself a core late-endosomal GTPase, whereas `Tbck` is an assembled RAB5 GAP/FERRY subunit with unresolved depletion of pre-existing functional stock after P16 editing.

The most comparable observed region was the lower moderate tail: `Depdc5 = 13`, `Vps35 = 17`, and `Vps54 = 31`, with `Mtor = 2` and the many zeros pulling downward, and `Tsc2 = 86`/`Rab7 = 501` acting as mechanistic upper bounds rather than central estimates. I placed `Tbck` near the lower-middle of the nonzero moderate analogs, at the `Vps35` scale.

Predicted `n_degs`: `17`.
