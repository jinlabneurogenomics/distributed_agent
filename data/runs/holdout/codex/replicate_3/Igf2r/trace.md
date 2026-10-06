# Direct Igf2r DEG-count forecast

## Target and endpoint

- Target: `Igf2r`, from the one-row holdout manifest.
- Population: `151 TH Prkcd Grin2c Glut`.
- Endpoint: number of measured genes in this population with BH-adjusted Wilcoxon `pvals_adj < 0.05`.

## Biology prior for Igf2r

I used the declared canonical Igf2r biology bundle as the target-specific prior.

- Exact focal-population expression is present but not saturated: Igf2r is detected in `12641 / 23679` matched non-target nuclei in `151 TH Prkcd Grin2c Glut` (`53.384855779382576%`), with mean raw expression `0.8564128552726045` UMI and mean `0.5267920432732965` cp10k.
- The functional-stock card adjudicates post-edit IGF2R/CI-MPR as `likely_substantially_depleted` by the P37-P44 harvest. The basis is that edited neurons stop resupplying a receptor that normally cycles through trans-Golgi, endosomal, and surface pools and turns over on a much shorter scale than 21-28 days.
- Igf2r loss is biologically real in postmitotic neurons, but the best direct phenotype is adult hippocampal neuron knockdown, not P16 thalamus. M6PR also overlaps with IGF2R for mannose-6-phosphate lysosomal-enzyme sorting, so partial buffering of cargo trafficking is plausible; M6PR does not replace IGF2 clearance.

## Same-class training measurements

The declared `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` table contains 1,674 training targets and is extremely sparse:

- `1205 / 1674` targets have `n_degs = 0`.
- `276 / 1674` have `n_degs = 1`.
- Median `n_degs` is `0`; the 90th percentile is `2`, and the 95th percentile is `18`.
- In the focal Parquet slice, 1,642 training targets have an assayed self-transcript row; 319 have a significant self transcript. Among the total-count-one perturbations, 237 are explained by a significant self transcript.

The closest hand-selected endosomal, lysosomal, and cargo-sorting perturbations were mostly quiet in this same population:

| training target | measured `n_degs` | interpretation |
| --- | ---: | --- |
| `Igf1r` | 0 | IGF-axis comparator present in the training table |
| `Sort1` | 0 | cargo receptor / retromer-binding comparator |
| `Scarb2` | 1 | human-ortholog-projected CORUM GBA1-IGF2R-SCARB2 complex partner; the only DEG is `Scarb2` itself |
| `Sorl1` | 0 | cargo receptor / protein-to-lysosome targeting comparator |
| `Lrp1` | 0 | cargo receptor / lysosomal-transport comparator |
| `Insr` | 0 | IGF2-binding and cargo-receptor annotation comparator |
| `Vps53` | 0 | retrograde trans-Golgi transport / lysosomal-transport module |
| `Vps54` | 31 | GARP/retrograde transport; modestly broader than receptor loss |
| `Vps35` | 17 | retromer/endosomal target, broader than receptor-specific loss |
| `Vps41` | 0 | late-endosome and STRING physical-interaction nominee |
| `Cltc` | 3 | clathrin coat / weak physical-interaction nominee |
| `Ap1b1` | 1 | AP-complex/trans-Golgi vesicle comparator, self-only |
| `Ap1s2`, `Ap3b1`, `Ap4s1` | 0 | AP-complex comparators |
| `Atp6v0a1` | 1 | V-ATPase comparator, self-only |
| `Atp6v1a`, `Atp6v1b2`, `Atp6v1e1` | 0 | V-ATPase comparators |

The curated mouse gene-analog nomination was useful mainly as a guard against missing a non-obvious measured comparator. After restriction to the 1,674-gene training universe it found `Sort1`, `Scarb2`, `Igf1r`, `Insr`, `Sorl1`, `Vps53`, `Vps54`, `Lrp1`, `Cltc`, `Vps41`, `Ap3b1`, `Becn1`, `Lrp2`, `Lamp2`, `Manba`, and `Lman2l` among the leading specific or cargo/lysosome-adjacent nominees, nearly all with 0 or self-only counts.

## Synthesis

Igf2r has enough expression and receptor turnover for target engagement to matter by harvest, so I did not treat it as an unreachable null. The measured analogs, however, argue against a broad stress, proteostasis, splicing, or core-vesicle-traffic response: direct cargo receptors and most M6P/lysosome-adjacent targets are 0 or 1 in the exact same high-yield thalamic class. `Rab7`, `Vps54`, and `Vps35` show that a large trafficking footprint is possible, but those perturb more central endosomal or GARP/retromer machinery than loss of the IGF2R cargo receptor itself.

The remaining signal most likely to clear FDR is Igf2r's own transcript. Focal expression in just over half of non-target nuclei makes a self hit plausible, while the low analog counts make several downstream hits unlikely. I therefore forecast a self-dominated minimal response rather than a complete null.

Predicted `n_degs`: `1`
