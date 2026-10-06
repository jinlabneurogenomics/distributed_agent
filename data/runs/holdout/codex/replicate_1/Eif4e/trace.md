## Target and endpoint

- Target: `Eif4e`
- Population: `151 TH Prkcd Grin2c Glut`
- Endpoint: number of measured genes with BH-adjusted Wilcoxon `p < 0.05`

## Evidence used

The one-row holdout manifest declares only `Eif4e`. The focal count table is the
training table for `151 TH Prkcd Grin2c Glut`; it has 1,674 observed training
perturbations and does not supply the held-out Eif4e count.

The biology-only Eif4e bundle supports target reach and perturbation realization
but not a large transcriptional response:

- Eif4e is expressed in the focal non-target nuclei: 20,346 of 23,679 nuclei,
  85.92%, with mean `log1p(CP10K)` 0.810.
- The disruptive edit should stop synthesis of new canonical eIF4E. Existing
  eIF4E protein is not directly inactivated, but the curated half-life proxy is
  roughly 11-13 hours, far shorter than the 21-28 days between P16 editing and
  P37-P44 harvest, so pre-edit stock should mostly clear in edited neurons.
- The same bundle leaves postnatal thalamic requirement and redundancy
  uncertain: germline complete loss is embryonic lethal, half dose is tolerated,
  and Eif4e2/Eif4e1b paralogy is not a same-context compensation test.

The matched training table argues for a near-null focal-class mRNA footprint for
local translation-initiation perturbations:

| training target | biological relation used here | n_degs |
| --- | --- | ---: |
| `Eif4g1` | eIF4F cap-dependent initiation scaffold | 1 |
| `Eif4a2` | eIF4F RNA helicase paralog | 2 |
| `Eif4h` | eIF4A accessory initiation factor | 1 |
| `Eif5a` | translation factor | 0 |
| `Eif2ak4` | translation-initiation stress kinase | 0 |
| `Mtor` | upstream growth/translation regulator | 2 |
| `Rptor` | mTORC1 scaffold, upstream of eIF4E control | 0 |
| `Fmr1` | translational repression/regulatory comparator | 0 |
| `Cyfip1` | translational repression/regulatory comparator | 0 |
| `Cyfip2` | translational repression/regulatory comparator | 1 |
| `Ddx3x` | eIF4F-associated RNA helicase/regulator | 8 |

I treated `Tsc2 = 86` separately because Tsc2 loss releases mTORC1 signaling and
is directionally closer to eIF4E-pathway activation than to loss of the cap
binding subunit. It shows that the focal thalamic population can report a
translation-pathway perturbation when it enters a broad downstream state, but it
is a poor scale donor for Eif4e loss.

A direct Parquet check in `151 TH Prkcd Grin2c Glut` confirmed that those low
counts are not masking broad significant signatures. Each queried training
target had 17,259 measured genes in this population; the significant rows were
only the self transcript for `Eif4g1`, the self transcript plus `Cadm4` for
`Eif4a2`, one non-self gene for `Eif4h`, none for `Eif5a`, none for `Eif2ak4`,
none for `Rptor`, two non-self genes for `Mtor`, one self gene for `Cyfip2`,
none for `Cyfip1` or `Fmr1`, and eight genes for `Ddx3x`.

For scale, the full focal training distribution is highly zero-inflated:
1,205/1,674 perturbations have `n_degs = 0`, 1,512/1,674 have `n_degs <= 2`,
and only 106/1,674 have `n_degs >= 10`; the arithmetic mean is 14.05 because a
small tail reaches hundreds to thousands of DEGs. The close Eif4e analogs sit
in the modal near-zero region rather than the tail.

## Synthesis

Eif4e should be engaged in many focal neurons and the perturbation has enough
time to deplete a soluble eIF4E pool. That makes a strict technical null less
plausible than for a non-expressed or very persistent target. At the same time,
the closest observed perturbations on the cap-dependent translation axis
(`Eif4g1`, `Eif4a2`, `Eif4h`, `Mtor`, `Rptor`) produced 0-2 significant genes in
the exact same cell class, and broader translational repressors were similarly
quiet. The best point is therefore not a tail response like `Tsc2`, but a
single-gene, self-or-near-self level response.

Predicted `n_degs`: 1
