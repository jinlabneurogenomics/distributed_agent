# Direct n_degs forecast for Twist1 in 151 TH Prkcd Grin2c Glut

## Declared target

- Holdout manifest: `[local file: Twist1.csv]`
- Target: `Twist1`
- Endpoint: number of measured genes in `151 TH Prkcd Grin2c Glut` with BH-adjusted Wilcoxon `pvals_adj < 0.05`

I did not query a held-out `Twist1` differential-expression profile, a `Twist1`
DEG count, or any target-outcome artifact. The direct target evidence came from
the declared outcome-excluded Twist1 biology bundle at
`[local file: Twist1.json]`,
sha256 `4821be30f92b2e279ee2aef8b287a7ef3bb3e22a8c8d822c30e43fe4af8de43d`.

## Evidence used

### Target biology

- Twist1 is a soluble nuclear bHLH transcription factor. If it is present in a
  successfully edited neuron, the P16 to P37-P44 window is long enough for old
  Twist1 protein and reversible DNA-binding occupancy to clear after new
  functional supply stops.
- The direct functional-loss phenotype in the target bundle is embryonic and
  developmental. The bundle found no matched postnatal thalamic-neuron loss
  experiment over a 21-28 day interval, so there is no positive matched-context
  reason to expect a broad adult thalamic neuronal response.
- Exact in-assay non-target expression for the focal class was extremely sparse:
  104 of 23,679 matched non-target `151 TH Prkcd Grin2c Glut` nuclei expressed
  Twist1, or 0.43920773681321%, with mean raw UMI 0.005405633683854893 and
  pseudobulk CPM 0.3387902320116766.

### Training counts

The declared training count table
`[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`
contains 1,674 measured training perturbations for the same endpoint.

- 1,205 / 1,674 perturbations, 71.98%, have `n_degs = 0`.
- The median is 0, the 75th percentile is 1, the 90th percentile is 2, the 95th
  percentile is 18, and only 78 training perturbations exceed 20 DEGs.

The closest training genes I used as qualitative scale checks were the available
Twist1 paralog or bHLH/neurogenic TF-like perturbations in the count table:

```text
Atoh1    0
Gata3    0
Neurod1  0
Neurod2  0
Tcf12    0
Tcf3     0
Tcf4     0
Twist2   0
```

I then queried the declared training Parquet
`[local file: training_de_all_cell_groups.parquet]`
for only those eight perturbations in `151 TH Prkcd Grin2c Glut`. Each had
17,259 measured-gene rows and zero rows with `pvals_adj < 0.05`, confirming the
matched-context CSV counts.

## Reasoning

Twist1 has a real molecular operation, and the experimental window should be
long enough to remove its short-lived functional stock in any cell that depends
on continuous Twist1 synthesis. The endpoint, however, is an aggregate
single-nucleus RNA state across recovered postnatal thalamic neurons. The
critical quantitative bearing is that baseline Twist1 RNA is nearly absent from
that exact focal population. Even a complete loss in the rare target-positive
subfraction would be heavily diluted in the aggregate Wilcoxon contrast.

The training table shows that a zero-DEG result is the local default for this
cell class. More specifically, available Twist2 and related bHLH or E-protein
perturbations do not generate any FDR-significant genes in the same class, so
the presence of a developmental bHLH transcription-factor annotation is not by
itself enough to push the expected count above the 0/1 boundary.

Counterevidence exists only as uncertainty: Twist1 could have an unmeasured
rare postnatal neuronal role, and survivor conditioning could hide cells lost
before recovery. Those possibilities do not imply FDR-significant aggregate
survivor-state DEGs in `151 TH Prkcd Grin2c Glut`. I therefore put the integer
point estimate at the modal and biologically supported floor.

Predicted `n_degs`: 0
