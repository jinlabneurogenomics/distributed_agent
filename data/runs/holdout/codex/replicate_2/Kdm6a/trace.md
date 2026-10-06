# Kdm6a n_degs forecast

## Task and endpoint

- Target manifest: one held-out perturbation, `Kdm6a`.
- Focal population: `151 TH Prkcd Grin2c Glut`.
- Endpoint: `n_degs`, the count of measured genes with BH-adjusted Wilcoxon `p < 0.05`.
- Declared outcome table: `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`; `Kdm6a` is absent from the 1,674 training rows.
- Declared DE matrix: `training_de_all_cell_groups.parquet`, same experiment, training perturbations only.
- Target biology: `biology_bundles/Kdm6a.json`, biology-only view; no Kdm6a response count or labeled neighbor outcomes were used.

## Kdm6a biology

The exact expression reach in the focal non-target nuclei is good for a sparse
CRISPR transcriptomic assay: `Kdm6a` is detected in 14,887 of 23,679 matched
non-target nuclei in `151 TH Prkcd Grin2c Glut`, or 62.87%, with mean raw UMI
1.142, mean CP10k 0.726, and pseudobulk CPM 71.56. This makes target reach a
positive factor, while not measuring editing efficiency or downstream effect.

The declared biology card places KDM6A as a nuclear H3K27me2/H3K27me3
demethylase and MLL3/4-associated chromatin-regulatory component. It judges
functional stock at harvest as `likely_substantially_depleted`: acute Cre
deletion in newborn mouse hippocampal neurons produced neuronal morphology
changes within 7 to 19 days, and P16 to P37-P44 gives 21 to 28 days for loss
of new KDM6A supply to propagate. Important caveats are that the direct timing
evidence is hippocampal culture rather than thalamus in vivo, KDM6A protein
half-life in postmitotic mouse neurons was not resolved, and UTY/KDM6B could
buffer part of the response.

## Training scale in the focal class

The declared 151-TH count table is highly sparse:

- 1,205 / 1,674 training perturbations have `n_degs = 0`.
- Median `n_degs = 0`; mean `n_degs = 14.05`.
- 90th percentile `n_degs = 2`; 95th percentile `n_degs = 18`.
- Only 43 / 1,674 perturbations have at least 100 DEGs.

The closest measured chromatin comparators put Kdm6a near the low-response
part of the table rather than near the broad outlier group:

| comparator | focal `n_degs` | interpretation |
| --- | ---: | --- |
| `Kdm6b` | 0 | closest assayed KDM6 paralog; H3K27 demethylase |
| `Kmt2c` | 0 | MLL3/4 enhancer writer associated with KDM6A biology |
| `Ep300` | 0 | enhancer coactivator/HAT |
| `Kat6a` | 0 | HAT and chromatin NDD gene |
| `Kat6b` | 0 | HAT and chromatin NDD gene |
| `Smarca4` | 0 | BAF ATPase |
| `Arid1b` | 1 | BAF subunit |
| `Crebbp` | 8 | enhancer coactivator/HAT |
| `Kdm5c` | 18 | histone demethylase, weak focal hit |
| `Setdb1` | 22 | histone methyltransferase, weak focal hit |
| `Kmt2a` | 24 | SET1/MLL-family H3K4 writer |
| `Chd8` | 61 | broader chromatin remodeler |
| `Brd4` | 311 | broad transcriptional coactivator |
| `Setd1a` | 368 | broad SET1/COMPASS writer |

The profile comparison over the declared Parquet, restricted to
`group_name == "151 TH Prkcd Grin2c Glut"`, also kept the H3K27/H3K4-adjacent
perturbations in the same low tier: `Kdm6b` and `Kmt2c` had no significant
features, `Kdm5c`, `Kmt2a`, and `Setdb1` had 10 to 49 significant features,
while only broader regulators such as `Setd1a`, `Brd4`, and `Chd8` crossed 50.

## Packaged same-experiment context

The selected corpus report for `Kdm6b` records a high-confidence all-neuron
negative result: acute postnatal `Kdm6b` loss produced no downstream
FDR-significant genes in any recovered neuronal group at the report's
FDR < 0.10 threshold. Its matched 151-TH contrast emphasized that the `Kdm6b`
null was selective: `Setd1a`, `Smarcc2`, `Rora`, `Kmt2a`, `Setdb1`, `Kdm5c`,
`Crebbp`, and `Setd5` were detectable in the same thalamic group.

The selected corpus report for `Kmt2c` likewise describes broad buffering:
15 of 16 measured `Kmt2c` groups had zero downstream genes at FDR < 0.10 and
the only robust effect was a single cortical `Prnp` hit. In matched thalamic
and midbrain groups, several enhancer/chromatin relatives responded while
`Kmt2c`, `Ep300`, `Kdm6b`, `Kat6a`, and `Kat6b` were flat.

## Forecast

Kdm6a has enough target expression and enough postnatal-neuron biology that I
do not treat the perturbation as a pure baseline zero. The scale-bearing
training evidence is nevertheless dominated by flat or weak responses among
the nearest KDM6, MLL3/4, and enhancer-axis perturbations; the several-hundred
DEG `Setd1a` and `Brd4` responses are visible proof that 151-TH can report
chromatin perturbation, but they are too broad to transfer quantitatively to
KDM6A.

I therefore place `Kdm6a` in the low nonzero band, above the direct
`Kdm6b`/`Kmt2c` nulls because of its exact focal expression and acute
postnatal loss evidence, but below the mild `Kdm5c`/`Kmt2a` counts because of
the H3K27/enhancer buffering seen in the training perturbations. The resulting
point forecast is:

`Kdm6a	n_degs = 8`
