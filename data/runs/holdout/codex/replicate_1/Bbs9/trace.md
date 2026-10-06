# Bbs9 DEG-count forecast

## Target and endpoint

- Target: `Bbs9`, the only row in the declared holdout manifest.
- Focal population: `151 TH Prkcd Grin2c Glut`.
- Endpoint: `n_degs`, the count of measured genes in that class with BH-adjusted Wilcoxon `pvals_adj < 0.05`.

## Target biology used

The declared endpoint-blind Bbs9 biology bundle places BBS9 in the core BBSome ciliary cargo-trafficking complex: BBS9 is a physical subunit at the BBS2-BBS7 interface of a dynamic, ARL6-regulated coat used for membrane-protein trafficking at primary cilia. The functional-stock card judged the P16-to-P37/P44 edit likely to substantially deplete functional BBS9 by harvest because BBSome subunits exchange and most measured adult mouse brain proteins turn over on a several-day scale, but the evidence was only partial because BBS9-specific persistence in postmitotic thalamic neurons is unknown.

The exact in-assay expression card weakens the case for a large focal response. In the matched non-target nuclei for `151 TH Prkcd Grin2c Glut`, `Bbs9` was detected in 7,699 of 23,679 nuclei, or 32.514%, with mean log1p CP10K 0.1937 and pseudobulk CPM 26.85. That is enough expression for the perturbation to be present, but not enough to infer broad functional dependence across the whole aggregated thalamic population.

## Training-count evidence used

The focal training table contains 1,674 observed targets. Its DEG-count distribution in `151 TH Prkcd Grin2c Glut` is extremely zero-heavy:

- median: 0
- 75th percentile: 1
- 90th percentile: 2
- 95th percentile: 18
- zero-count targets: 1,205 / 1,674
- targets with `n_degs <= 5`: 1,546 / 1,674

The represented BBSome and nearby ciliary perturbations were nearly all null in the same endpoint:

| perturbation | `n_degs` |
| --- | ---: |
| `Bbs5` | 0 |
| `Ttc8` | 1 |
| `Lztfl1` | 0 |
| `Ift43` | 0 |
| `Ift81` | 0 |
| `Ift88` | 0 |
| `Kif3b` | 0 |
| `Cep290` | 0 |
| `B9d1` | 0 |
| `Rpgrip1l` | 0 |
| `Gpr161` | 0 |
| `Adcy3` | 0 |
| `Htr6` | 0 |

A broader same-organelle set explicitly discussed in the BBSome/ciliary reports behaved the same way in the focal count table: `Alms1`, `Arl2bp`, `Armc9`, `B9d1`, `Bbs5`, `Cep120`, `Cep290`, `Cplane1`, `Cspp1`, `Dync2h1`, `Dync2i1`, `Dzip1`, `Gli1`, `Gli2`, `Gpr161`, `Ift43`, `Ift81`, `Ift88`, `Kif3b`, `Lztfl1`, `Mchr1`, `Pibf1`, `Rpgrip1l`, `Smo`, and `Ttc21b` each had 0, while `Arl3` and `Ttc8` each had 1.

## Expression-profile evidence used

I symmetrically compared 12 observed ciliary profiles from the exact focal Parquet slice: `Bbs5`, `Ttc8`, `Lztfl1`, `Ift81`, `Ift88`, `Kif3b`, `Cep290`, `B9d1`, `Rpgrip1l`, `Gpr161`, `Adcy3`, and `Htr6`.

That profile artifact found all 12 profiles available; 11 had no FDR-significant features and one had 1-9 significant features. In the bounded inspection, `Bbs5`, `Lztfl1`, `Ift81`, and `Ift88` each had `significant_feature_count = 0`; `Ttc8` had `significant_feature_count = 1`, specifically as a negative singleton. A cohort diagnostic over all 66 ciliary pairs found some shared weak negative tail structure, but no pair had an overlap of FDR-significant programs. Thus the signed profile data support a weak, subthreshold ciliary tendency rather than a robust DEG-producing module.

## Same-experiment semantic context

Packaged reports for the measured BBSome/ciliary analogs agree with the count and profile evidence without adding an independent assay. `Bbs5:F003` reported that represented BBSome/ciliary relatives did not phenocopy `Bbs5`, including flat `Ttc8` and sparse, non-overlapping `Lztfl1`, `Ift88`, `Kif3b`, `Cep290`, and `Htr6` behavior. `Ttc8:F003` reported no shared FDR convergence with Bbs5, IFT, Lztfl1, Rpgrip1l, Ttc21b, or Cep290 comparators. A high-confidence claim contributed by `Ttc8:F003` summarized the broader pattern as buffering of represented ciliary trafficking and ciliary signaling perturbations at the basal postnatal neuronal nuclear-RNA level.

The one focal `Ttc8` DEG is not evidence for a downstream ciliary expression module: the Ttc8 report states that downstream genes were absent across its measured neuronal taxonomy despite recurrent negative Ttc8 self-transcript signal. That makes the most direct measured BBSome example a likely self-RNA singleton rather than a scale-bearing analog for multiple Bbs9-regulated genes.

## Synthesis

Bbs9 is a reachable, likely depleted BBSome loss rather than an inert target. Still, all quantitative evidence from the matched focal endpoint points to the zero/one-count regime: the whole training prior has median 0, the direct BBSome entries are 0 and 1, represented ciliary transport/signaling relatives are almost uniformly 0 in `151 TH Prkcd Grin2c Glut`, and their focal expression vectors lack an FDR-level shared program.

I therefore used the ciliary/BBSome local empirical scale, not a disease-severity prior, as the dominant evidence. Bbs9 could plausibly produce a self-transcript singleton, as `Ttc8` did, but `Bbs5` and most ciliary targets did not; moderate Bbs9 reach in only about one third of the aggregate class was not enough to promote that singleton over the stronger zero-count evidence. My point forecast is:

`Bbs9	0`
