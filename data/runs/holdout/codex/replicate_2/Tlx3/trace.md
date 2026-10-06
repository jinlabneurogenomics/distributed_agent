# Tlx3 direct n_degs forecast

target_name: Tlx3
focal_population: 151 TH Prkcd Grin2c Glut
predicted_n_degs: 0

## Evidence used

### Declared Tlx3 biology bundle

The canonical Tlx3 bundle places the perturbation on a real neural regulator:
TLX3 is a nuclear homeodomain transcription factor with mouse loss and
misexpression evidence for developmental glutamatergic/sensory-neuron fate
control. The target-specific evidence did not, however, establish an acute
postnatal thalamic maintenance role. Its strong phenotypes were embryonic,
perinatal, brainstem, spinal-cord, cerebellar, or DRG lineage phenotypes rather
than a P16 loss in mature thalamic neurons.

The functional-stock adjudication was therefore indeterminate for harvest at
P37-P44: editing should stop new TLX3 synthesis, but it need not immediately
remove pre-existing TF protein or already established chromatin/regulatory
state, and no TLX3 protein half-life, chromatin residence time, or matched
postmitotic-neuron clearance clock was found.

The exact focal expression reach was the decisive downward bearing. In matched
non-target nuclei from `151 TH Prkcd Grin2c Glut`, only 44 of 23,679 cells
expressed `Tlx3`, for 0.1858186579% expressing cells, mean raw UMI
0.0018581866, mean cp10k 0.0012665925, and pseudobulk CPM 0.1164591423. That
is far below the reach expected for a broad aggregated response in this
coarse thalamic class.

### Focal training count table

The declared training table for `151 TH Prkcd Grin2c Glut` contained 1,674
training perturbations. Its endpoint distribution was highly sparse:

- 1,205 / 1,674 training targets had `n_degs = 0`.
- 469 / 1,674 had any focal DEG.
- 106 / 1,674 had at least 10 DEGs.
- 43 / 1,674 had at least 100 DEGs.
- 3 / 1,674 had at least 1,000 DEGs.
- The median was 0, the 75th percentile was 1, the 90th percentile was 2, the
  95th percentile was 18, the 99th percentile was 454, and the maximum was
  2,677.

The largest focal responses were broad core chromatin, RNA-processing,
proteostasis, and trafficking perturbations, for example `Uba5` 2,677, `Tpr`
1,768, `Sin3a` 1,433, `Rnpc3` 868, `Zbtb7a` 841, `U2af2` 828, `Psmb4` 742, and
`Hnrnpu` 733. Tlx3's biology and exact focal expression did not align with this
rare high-burden class.

### Training perturbations interpreted

I used the count table and the focal Parquet rows for neural/developmental TF
perturbations represented in training. Most analogous developmental regulators
were silent in `151 TH Prkcd Grin2c Glut`:

- `Pax6`: 0
- `Otx2`: 0
- `En1`: 0
- `En2`: 0
- `Foxp2`: 0
- `Neurod1`: 0
- `Rorb`: 0
- `Nfia`: 0
- `Nfib`: 0
- `Nfix`: 0
- `Zic2`: 0
- `Zic3`: 0
- `Zic4`: 0

The Parquet-confirmed nonzero TF examples from the checked set were small
except for `Rora`: `Sox2` had 2 DEGs, `Zic1` had 2 DEGs, and `Rora` had 278
DEGs. Packaged Rora findings interpret that exception as a maintained RORalpha
requirement in this same thalamic Prkcd/Grin2c class and show that even
closely related `Rorb` and `Rorc` did not phenocopy it. Packaged Pax6 findings
made the opposite point for a famous neural homeodomain developmental TF:
acute post-P16 Pax6 loss was transcriptionally silent across recovered
NeuN-positive neuronal groups despite measurable developmental pathway members
elsewhere.

## Synthesis

The training distribution alone puts most non-core targets at zero or a
singleton-level focal count. Tlx3 has a strong developmental prior, but the
declared biology bundle leaves acute postnatal thalamic dependence unresolved,
and the exact focal reach shows that the target transcript was almost absent
from the assayed non-target population. In the represented training data,
developmental transcription factors with mismatched postnatal context mostly
landed at zero, while the broad Rora exception reflected a specific maintained
thalamic requirement that is not established for Tlx3.

I therefore treated a one- or two-gene response as possible but less likely
than no BH-significant measured genes, and I placed the point forecast at the
modal and median local outcome:

predicted_n_degs = 0
