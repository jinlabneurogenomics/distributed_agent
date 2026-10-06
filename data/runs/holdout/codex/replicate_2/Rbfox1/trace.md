# Rbfox1 DEG-count prediction

## Target and endpoint

- Target: `Rbfox1`
- Endpoint: `n_degs` in `151 TH Prkcd Grin2c Glut`, counted as measured genes with Wilcoxon BH-adjusted `pvals_adj < 0.05`.
- Declared quantitative evidence used:
  - `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`
  - `training_de_all_cell_groups.parquet`, restricted to `group_name == "151 TH Prkcd Grin2c Glut"`
  - `biology_bundles/Rbfox1.json`, also checked through `distributed_agents_runtime.characterization_bundle(target="Rbfox1", view="biology")`

The Parquet/profile summaries and the training count table are two views of the same experiment, so I used them as a single source of observed endpoint scale, not as independent replication.

## Biology prior

The Rbfox1 card supports an observable but likely buffered postmitotic effect.

- The exact in-assay expression bundle reports `Rbfox1` expression in 22,901 of 23,679 non-target nuclei in this thalamic class, or 96.714%, with mean raw UMI 4.685 and mean log1p CP10K 1.286. This makes target reach in `151 TH Prkcd Grin2c Glut` broad enough that dilution by absent cells is unlikely to force a null.
- RBFOX1 is a nuclear/cytoplasmic RNA-binding regulator of neuronal alternative exon use. Stopping new protein synthesis should matter over the 21-28 day P16-to-P37/P44 perturbation window because splicing decisions are continuously regenerated.
- The functional-stock adjudication concluded `likely_substantially_depleted`: no acute target-specific RBFOX1 half-life is available, but a dynamic RNA-regulatory protein is not expected to persist intact across the whole window.
- Postnatal neural loss phenotypes exist in mouse CNS and cortical interneurons, including altered neuronal splicing and excitability/seizure phenotypes, but those experiments used different regions, lineages, and developmental timing rather than an acute P16 thalamic edit.
- RBFOX2/RBFOX3 paralogs are coexpressed in mature neurons; RBFOX2 protein rose after Rbfox1 CNS loss, so compensation should attenuate the acute single-gene whole-gene RNA response even though published phenotypes show compensation is incomplete.

Net effect: the biology argues against treating `Rbfox1` as an inert zero, but the measured endpoint is 3-prime whole-gene abundance rather than exon usage, so the core RBFOX1 molecular effect can be partly invisible.

## Training scale

The declared thalamic count table is sparse:

- 1,674 training perturbations.
- 1,205/1,674 have `n_degs = 0`.
- The median is 0; 75th percentile is 1; 90th percentile is 2; 95th percentile is 18; 98th percentile is 150; 99th percentile is 436.

RNA-processing perturbations define a long but heterogeneous tail:

| training target | n_degs | interpretation |
| --- | ---: | --- |
| `Rnpc3` | 868 | minor-spliceosome component |
| `U2af2` | 828 | essential spliceosome factor |
| `Hnrnpu` | 733 | broad hnRNP/RNA-binding factor |
| `Cdc40` | 624 | spliceosome/PRP19-associated factor |
| `Prpf6` | 454 | spliceosome factor |
| `Thoc1` | 303 | RNA export/processing |
| `Tardbp` | 210 | sequence-specific disease RBP, broad secondary response |
| `Hnrnpc` | 122 | broad hnRNP |
| `Hnrnpa2b1` | 11 | hnRNP-family RBP |
| `Ddx3x` | 8 | RNA helicase |
| `Hnrnph2` | 4 | hnRNP-family RBP |
| `Hnrnpdl` | 1 | hnRNP-family RBP |
| `Ddx39b` | 0 | RNA helicase/splicing-export factor |
| `Snrpb` | 0 | spliceosomal snRNP factor |
| `Rbm28` | 0 | RNA-binding/nucleolar factor |

I treated the 100-800+ DEG rows as upper-scale evidence from disabling broad spliceosome or ubiquitous RNA-processing machinery, not as equal-scale donors for a neuronal paralog-buffered exon regulator. `Tardbp` is the closest high-count sequence-specific RBP in the training set, but the packaged same-experiment Tardbp report explicitly found a broad ER/lysosomal, mitochondrial, and RNA-processing whole-gene response and noted that ALS-linked or RBP relatives did not automatically phenocopy Tardbp. That makes `Tardbp = 210` a ceiling-like point, not a center for `Rbfox1`.

The narrower RNA/neurodevelopmental comparators are a better count scale for a high-confidence neural regulator whose primary defect is not fully captured by whole-gene DE: `Hnrnpa2b1 = 11`, `Ddx3x = 8`, `Hnrnph2 = 4`, `Fmr1 = 0`, `Mecp2 = 16`, and `Ube3a = 0`.

## Same-class profile check

The bounded `profile_compare` run used the declared Parquet in `151 TH Prkcd Grin2c Glut` with `logfoldchanges` as the signed profile and `pvals_adj < 0.05` as the significance definition. All 20 manually selected RNA-processing or neuronal-control training nodes had profiles.

Among the nine high-count RNA-processing rows (`Rnpc3`, `U2af2`, `Hnrnpu`, `Cdc40`, `Prpf6`, `Thoc1`, `Snrnp70`, `Tardbp`, `Hnrnpc`), directional cohesion was stronger for the negative tail than the positive tail, and significant-program overlap was partial rather than module-wide. Thus these broad perturbations show that the assay can see RNA-processing disruption in this class, but they do not define a single transcriptomic state that should be copied to `Rbfox1`.

## Point estimate

I place `Rbfox1` slightly above the 2-50 DEG small-response band mean and just below the 95th percentile of all training perturbations:

- upward bearings: near-universal thalamic expression, likely substantial loss of a continuously renewed RNA-regulatory function, and published postnatal neural phenotypes;
- downward bearings: primary effect is alternative splicing rather than whole-gene abundance, close RBFOX paralogs should buffer single loss, and training sequence-/RNA-binding regulators without core spliceosome failure are often 0-16 DEGs in this class.

The resulting point forecast is **12 DEGs**.
