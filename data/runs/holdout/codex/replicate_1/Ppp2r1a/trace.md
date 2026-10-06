## Target and endpoint

- Target: `Ppp2r1a`, from the declared one-row holdout manifest.
- Endpoint: `n_degs` in `151 TH Prkcd Grin2c Glut`, defined as the number of measured genes with BH-adjusted Wilcoxon `p < 0.05`.
- The declared 151-class training count table contains 1,674 targets and does not contain `Ppp2r1a`.

## Target biology used

The canonical biology bundle supports a realized perturbation in the focal thalamic population:

- `Ppp2r1a` is readily measured in the exact non-target `151 TH Prkcd Grin2c Glut` population: 94.003% expressing nuclei, mean 4.400 raw UMI, mean log1p CP10K 1.194.
- Ppp2r1a encodes the A-alpha scaffold of PP2A holoenzymes. The bundle adjudicates this as a dynamic complex component whose A-alpha functional stock is likely substantially depleted by P37-P44 after a P16 edit.
- Functional observability is plausible but not a matched direct time course: postnatal forebrain excitatory-neuron loss produced phenotypes, while A-beta/Ppp2r1b can provide only partially characterized reserve.

I therefore did not treat the target as an unexpressed or uncleared-stock null, but the biology also does not require a broad transcriptional crisis in recovered nuclei.

## Training measurements used

The declared 151-class count table is extremely sparse:

- median `n_degs`: 0
- 75th percentile: 1
- 90th percentile: 2
- 95th percentile: 18
- 99th percentile: 430
- mean: 14.05, inflated by a small upper tail

The closest available PP2A/calcineurin phosphatase targets were all in the zero-to-single-digit regime:

| training target | relation used | n_degs |
|---|---|---:|
| `Ppp2r2b` | PP2A regulatory B subunit | 0 |
| `Ppp2r5d` | PP2A regulatory B subunit | 0 |
| `Ppp3ca` | calcineurin catalytic subunit | 4 |
| `Ppp3cc` | calcineurin catalytic subunit | 0 |
| `Ppp3r1` | calcineurin regulatory subunit | 9 |

I also checked adjacent neuronal signaling perturbations in the same class: `Akt3` 0, `Mtor` 2, `Tsc2` 86, `Set` 0, `Camk2a` 0, `Camk2b` 1, `Grin2a` 1, and `Grin2b` 2. A profile comparison over these 13 perturbations in the declared parquet found six with no significant features, six with 1-9 significant features, and only the broader growth regulator `Tsc2` above that band.

## Synthesis

The exact focal expression and short inferred A-alpha stock lifetime argue against forcing the PP2A B-subunit zeros onto `Ppp2r1a`: knocking out the scaffold should be more disruptive than knocking out one measured regulatory subunit. At the same time, the measured PP2A/calcineurin and synaptic-signaling neighborhood in `151 TH Prkcd Grin2c Glut` is consistently low, with the large signatures in this class concentrated in RNA-processing, protein-homeostasis, and other high-yield cellular targets rather than ordinary phosphorylation circuitry.

I therefore forecast a low nonzero response, inside the 1-9 DEG regime and below the 95th percentile of the training distribution:

`predicted_n_degs = 6`
