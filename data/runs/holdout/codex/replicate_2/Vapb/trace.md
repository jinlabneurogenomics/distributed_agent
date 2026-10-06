# Vapb n_degs prediction trace

## Target and endpoint

- Target manifest: `Vapb`
- Focal population: `151 TH Prkcd Grin2c Glut`
- Endpoint: number of measured genes with BH-adjusted Wilcoxon `p < 0.05`

## Biology prior used

The declared Vapb biology bundle supports target reach but not a large
transcriptional state.

- Vapb is expressed in the exact focal population: 18,327/23,679
  non-target nuclei, or 77.40%, with mean 1.078 CP10K and mean 1.73 raw UMI.
- VAPB is an ER membrane adaptor for FFAT/contact-site partners and also
  supports HCN1/HCN2 surface abundance/native HCN current in thalamic neurons.
- The operative stock should be mostly depleted by the P37-P44 harvest after
  P16 editing: existing ER-localized protein persists initially, but the only
  target-specific chase measured a wild-type VAPB half-time near 17 hours in
  cultured cells, far shorter than the 21-28 day experimental window.
- Single Vapb loss can matter despite Vapa: Vapa overlaps with Vapb in mouse
  brain, but Vapb-null ventrobasal thalamic neurons still have reduced native
  Ih current.

Those facts favor a real perturbation in these nuclei. They do not by
themselves imply many BH-significant RNA changes, because the strongest
same-region phenotype is channel trafficking/electrophysiology rather than an
acute transcription-factor, spliceosome, proteasome, or cell-stress program.

The selected same-experiment corpus release had no Vapb Finding, Claim, or
explicit comparator edge, so the forecast did not use any packaged Vapb
endpoint profile.

## Training measurements used

The declared count table contains 1,674 training perturbations in
`151 TH Prkcd Grin2c Glut`; Vapb is absent. Counts are sparse and heavy-tailed:

- median: 0
- 75th percentile: 1
- 90th percentile: 2
- 95th percentile: 18
- mean: 14.05, driven by a small high-burden tail
- 469/1,674 training perturbations have at least one DEG

Typed annotation over the actual training universe nominated one very close
available partner:

| training perturbation | relation to VAPB | `n_degs` |
| --- | --- | ---: |
| `Acbd5` | strict one-to-one mouse projection of human CORUM ACBD5-VAPB complex, plus STRING physical VAPB interaction | 0 |

Direct Parquet reads for selected Vapb-relevant candidates in the same focal
population gave the following exact endpoint counts:

| training perturbation | reason for inspection | `n_degs` |
| --- | --- | ---: |
| `Acbd5` | exact ACBD5-VAPB complex partner | 0 |
| `Cert1` | VAP FFAT ceramide-transport partner biology | 0 |
| `Hcn1` | thalamic HCN functional arm | 0 |
| `Hcn2` | thalamic HCN functional arm | 1 |
| `Atl1` | ER membrane-shaping/contact-site neighborhood | 1 |
| `Atl3` | ER membrane-shaping/contact-site neighborhood | 0 |
| `Spast` | ER-shaping microtubule neighborhood | 0 |
| `Reep1` | ER-shaping neighborhood | 1 |
| `Reep2` | ER-shaping neighborhood | 1 |
| `Vcp` | ERAD/proteostasis neighbor | 2 |
| `Amfr` | ERAD membrane E3 neighbor | 1 |
| `Atf6` | ER-stress transcriptional effector | 0 |
| `Hspa5` | ER unfolded-protein-response marker/chaperone | 5 |
| `Sec23a` | ER-to-Golgi vesicle traffic | 0 |
| `Vps35` | broader endosomal trafficking | 17 |
| `Vps54` | broader vesicle traffic | 31 |
| `Atp2a2` | ER calcium pump, broader ER stress state | 187 |

For the most target-proximal quiet rows, the Parquet confirmed that the nulls
were not hiding borderline multi-gene programs: `Acbd5` had no q < 0.05 rows
across 17,259 measured genes, and its smallest adjusted p-values were 0.46,
0.51, and 0.91; `Cert1` had no q < 0.05 rows, with its own transcript at
q = 0.25; `Hcn1` had no q < 0.05 rows; `Hcn2`, `Atl1`, `Reep1`, and `Reep2`
each had exactly one significant row and that row was the targeted transcript.

I treated `Atp2a2` and the higher vesicle-trafficking counts as upper-scope
context rather than direct scale donors: perturbing a major ER calcium pump or
endosomal trafficking machinery can induce a stress/transport state that is
much broader than losing a single VAPB adaptor. The exact ACBD5-VAPB partner,
HCN channels, atlastins, REEPs, Spast, Cert1, and Sec23a were therefore more
decisive for the expected endpoint scale.

## Point synthesis

The forecast is just above zero. Vapb is well expressed and its protein pool
should be depleted by harvest, so I did not collapse to a guaranteed null.
However, the best matched training perturbations in this thalamic class are
zero or self-only, and the known VAPB phenotype in thalamus is a channel
trafficking/electrophysiology defect rather than a broad RNA program. I
therefore expect a target-transcript-only or nearly null detected signature and
use:

```text
predicted_n_degs = 1
```
