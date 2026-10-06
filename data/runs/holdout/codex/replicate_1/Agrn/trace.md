## Target

- Held-out manifest target: `Agrn`
- Requested cell class: `151 TH Prkcd Grin2c Glut`
- Endpoint: count of focal measured genes with BH-adjusted Wilcoxon `p_adj < 0.05`.

## Evidence Used

### Declared target biology

The prediction-safe `Agrn` bundle reports exact in-assay focal expression:
`Agrn` is available as a measured feature in `151 TH Prkcd Grin2c Glut`, with
`23,534 / 23,679` non-target nuclei expressing it, `99.39%` expressing,
mean raw UMI `8.48`, and mean CP10K `5.49`. That makes target reach high and
rules out a simple absence-of-RNA explanation.

Functional-stock evidence points to a partial lesion at the P37-P44 harvest
rather than uniform AGRN loss. AGRN function is split across transmembrane,
secreted extracellular-matrix, and local synaptic pools. A disruptive edit
stops new synthesis, but installed protein has to clear: the biology bundle
adjudicates fast loss of a neuronal transmembrane pool, an aggregate cortical
neuron Agrin half-life near 23 days, and mixed functional stock after a
21-28 day P16-to-harvest interval. The bundle also records a postnatal neural
role in adult hippocampus, but that phenotype is not matched to thalamic
postmitotic neurons, and a neuron-associated SN-Agrn isoform knockout lacked
overt neurological signs.

### Training count scale

The declared `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` table contains
1,674 non-held-out training targets and no `Agrn` row. Its endpoint distribution
is dominated by the floor:

- `1,205 / 1,674` targets have `n_degs = 0`
- median `0`
- 75th percentile `1`
- 90th percentile `2`
- mean `14.05`, driven by a small high-count tail

The canonical or proximal agrin-axis perturbations represented in the same
focal count table were also flat:

- `Lrp4`: `0`
- `Musk`: `0`
- `Ror2`: `0`
- `Ache`: `1`
- Wnt receptor-layer comparators `Ror1`, `Ryk`, `Lrp5`, `Fzd2`, `Fzd4`,
  `Fzd6`, and `Fzd9`: all `0`

This is not because the focal population is generally incapable of Wnt-family
responses: downstream Wnt nodes in the same table were much larger
(`Lrp6 = 4`, `Tcf7l2 = 106`, `Ctnnb1 = 383`).

### Same-experiment corpus and focal profiles

The same-experiment corpus had no released `Agrn` Finding or Claim, so I did
not reuse a direct packaged `Agrn` interpretation. The `Lrp4`, `Musk`, and
`Ror2` Findings nevertheless supply a boundary around the obvious receptor
axis: postnatal NeuN+ perturbations of represented NMJ/agrin-LRP4-MuSK and
Wnt5a/ROR/PCP receptor-layer genes were sparse, buffered, or nonconvergent in
the neuronal nuclear-RNA endpoint.

I compared the focal Parquet profiles for `Lrp4`, `Musk`, `Ror2`, `Ache`,
`Lrp6`, `Ctnnb1`, and `Tcf7l2` in `151 TH Prkcd Grin2c Glut`. The exact
profile table has 17,259 focal features per node, with:

- `Lrp4`: `0` significant features
- `Musk`: `0` significant features
- `Ror2`: `0` significant features
- `Lrp6`: `4` significant features
- `Ctnnb1`: `383` significant features

Whole-profile similarities between the receptor-side anchors and the active
Wnt nodes were near zero; for example `Lrp4` versus `Ctnnb1` had Pearson
`0.0089`, `Musk` versus `Ctnnb1` had Pearson `0.0140`, and `Ror2` versus
`Ctnnb1` had Pearson `0.0525`. By contrast, `Lrp6` and `Ctnnb1` shared all
four of the sparse `Lrp6` significant features in the same direction. That
supports a real measured boundary between quiet receptor-side extracellular
perturbations and intracellular thalamic Wnt effectors.

## Synthesis

`Agrn` has excellent RNA reach in the focal nuclei, so a self-transcript call
or a very small response is possible. In the visible focal training data,
319 of 1,642 target-self rows were significant at `p_adj < 0.05`, so high
expression keeps a one-gene count on the table. I did not treat self-mRNA loss
as evidence for stronger functional knockout, because the dataset portrait
warns that target-transcript loss is uncoupled from functional engagement.

The quantitative point estimate is therefore set by the lower signal: the
class is zero-inflated, the direct receptor-side comparators are exactly
zero in the focal endpoint, the same-experiment corpus interprets represented
NMJ/agrin-axis perturbations as uncoupled from a shared neuronal module, and
the long extracellular AGRN stock should blunt a 3-4 week acute edit. I
predict no BH-significant focal genes.

Predicted `n_degs`: `0`
