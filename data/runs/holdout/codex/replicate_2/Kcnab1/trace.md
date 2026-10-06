# Kcnab1 n_degs forecast

Target and endpoint:

- target: `Kcnab1`
- focal population: `151 TH Prkcd Grin2c Glut`
- endpoint: number of measured genes in this population with BH-adjusted Wilcoxon `pvals_adj < 0.05`

## Evidence used

### Declared biology bundle

The `Kcnab1` biology bundle supports target reach but not a broad transcriptional-response prior:

- In focal non-target nuclei, `Kcnab1` is directly detected: mean raw UMI `2.039`, mean log1p CP10K `0.692`, `18,265 / 23,679` nuclei expressing, `77.14%` expression reach.
- Kvbeta1 is an auxiliary cytoplasmic component of Kv1 potassium-channel complexes, associated with Kv1 alpha subunits and affecting channel inactivation/repetitive firing.
- The strongest postnatal functional evidence comes from hippocampal or cultured-neuron systems, not juvenile thalamic CRISPR. Antisense in mature postmitotic neurons shows function can be replaced or depleted, but the interval to functional loss was not reported.
- Pre-existing Kv1-Kvbeta1 complexes are not directly removed by DNA editing. The 21-28 day window should stop new Kvbeta1 supply, but the residual stock at harvest is unresolved.

I treated that as: high in-assay expression makes a target-transcript DEG plausible, while the expected first-order defect is electrophysiological and may remain buffered from a large nuclear mRNA response.

### Declared focal count table

The training count table is sparse and highly skewed:

- 1,674 training targets
- 1,205 have `n_degs = 0`
- median `n_degs = 0`
- 75th percentile `n_degs = 1`
- mean `n_degs = 14.05`, driven by a small high-count tail such as `Uba5 = 2677`

Hand-selected channel/excitability comparators were also mostly zero or singleton in `151 TH Prkcd Grin2c Glut`:

- `Kcnab2 = 1`
- direct Kv1 alpha-subunit comparators: `Kcna1 = 0`, `Kcna2 = 0`
- broader `Kcn*` training targets: 20 targets with counts `[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1]`, mean `0.3`
- other excitability families were similar: `Scn*` mean `1.0`, `Cacn*` mean `1.4`, `Hcn*` mean `0.5`, `Prkc*` mean `0.5`

### Declared Parquet rows

Querying the focal cell class in `training_de_all_cell_groups.parquet` confirmed that the nearest observed Kv beta example was self-only:

- `Kcnab2` had exactly one `pvals_adj < 0.05` row in `151 TH Prkcd Grin2c Glut`, and it was `names = Kcnab2`.
- `Kcna1` had zero significant focal rows.
- `Kcna2` had zero significant focal rows.

The other one-DEG potassium-channel responses I inspected, `Kcnc2`, `Kcnc3`, `Kcnq2`, and `Kcnq3`, were also self-transcript-only in the focal class. By contrast, the multi-gene channel/receptor outliers had different biology: `Cacna1g = 12` in this count table and `Grin1 = 89`.

### Same-experiment corpus interpretation

I used the packaged corpus only as an interpretation layer over the same Perturb-seq measurements, not as independent replication. It supported the raw-comparator readout:

- `Kcnab2:F001` summarizes a buffered Kv1 auxiliary-subunit response: no downstream FDR signal despite Kcnab2 self-transcript depletion in several recovered groups.
- `Kcnab2:F004` and `Kcna1:F002` place `Kcnab2`, `Kcna1`, and `Kcna2` in a Kv1/Kv-complex sector that was flat or near-flat at the neuronal nuclear RNA level.
- Broader potassium-channel claims report no robust shared voltage-gated-potassium response program in this assay.

## Synthesis

`Kcnab1` is well expressed in the focal thalamic neurons, so I did not force the prediction to zero. However, its biology is closest to `Kcnab2` and Kv1-complex loss: an auxiliary potassium-channel perturbation whose primary consequences should be gating/localization or electrophysiology, with substantial uncertainty about how much edited cells have depleted the pre-existing protein complex by P37-P44. The observed focal-class training behavior of this sector is overwhelmingly null or self-only, and the nearest beta-subunit training perturbation contributes a single target-transcript DEG rather than a downstream response.

Prediction: `1`.
