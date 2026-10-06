# Direct Hdac4 DEG-count forecast

## Target and endpoint

- **Target:** `Hdac4` from the one-row holdout manifest.
- **Endpoint:** `n_degs` in `151 TH Prkcd Grin2c Glut`, defined as the number of measured genes with BH-adjusted Wilcoxon `pvals_adj < 0.05`.
- **Declared focal population:** thalamic Prkcd/Grin2c glutamatergic neurons.

The biology bundle resolves this packet to the ID-defined mouse **HDAC5** perturbation, not to official mouse `Hdac4`. The exact in-assay reach is not the limiting factor: in non-target nuclei from `151 TH Prkcd Grin2c Glut`, the target transcript was detected in 18,962 of 23,679 nuclei, or 80.079%, with mean 1.208 CP10K and mean 1.894 raw UMI.

## Biology prior

HDAC5 is a signal-responsive class IIa corepressor component that associates with SMRT/N-CoR-HDAC3 assemblies and regulated MEF2 repression. A P16 CRISPR edit should stop new HDAC5 production, but it need not acutely disable pre-existing HDAC5 protein. The bundle found no endogenous postmitotic thalamic-neuron half-life or complex-residence measurement that resolves whether operative HDAC5 stock is materially gone after 21-28 days.

The main downward biological bearings were:

- the characterized functional stock at harvest was **indeterminate**, not confidently depleted;
- available HDAC5 phenotypes are stimulus- or region-dependent rather than a constitutive thalamic-neuron requirement;
- HDAC4/HDAC5 compensation is directly plausible from forebrain excitatory-neuron evidence, with no matched thalamic test excluding it.

The main upward bearing was strong measured focal expression plus a dynamic transcriptional-corepressor role. That argued against predicting a structural zero from absence of target RNA, but not against a postnatal basal null.

## Training perturbations used

I used the declared `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` count table and the training-only Parquet filtered to the focal cell class. The full focal count table is highly zero-inflated:

- 1,674 training perturbations
- median `n_degs = 0`
- 75th percentile `= 1`
- 90th percentile `= 2`
- 95th percentile `= 18`
- mean `= 14.05`, inflated by a small heavy tail
- 469/1,674 targets had any focal FDR<0.05 DEG, and only 103/1,674 exceeded 10

I then looked at measured perturbations closest to the target's biology:

| training target | focal FDR<0.05 DEGs | interpretation |
| --- | ---: | --- |
| `Hdac5` | 0 | closest assayed class-IIa HDAC/corepressor row; no focal response |
| `Mef2a` | 4 | tiny focal MEF2-family response |
| `Mef2c` | 1 | essentially buffered in this thalamic class despite cortical IT activity elsewhere |
| `Mef2d` | 0 | pan-recovered-neuron null in the same screen corpus |
| `Sin3a` | 1433 | broad chromatin-corepressor/stress boundary, not a close scale donor |

The Parquet confirmed that `Hdac5` had no FDR<0.05 features in the focal class, `Mef2a` had four, and `Mef2c` had one. Across all measured cell groups, `Hdac5` had only two singleton FDR<0.05 calls outside the focal class, whereas `Sin3a` produced the broad response expected for a highly active chromatin-stress boundary.

## Same-experiment corpus context

The packaged Finding ledger is another representation of the same experiment, so I used it only to interpret the training rows above.

Its `Hdac5` report described a single-gene `012 MEA LA CA1 DG Glut` Chd5 response, absence of the canonical activity/MEF2 target program after Hdac5 loss, non-phenocopy by represented MEF2/CaMK/PKA pathway perturbations, and no meaningful convergent or inverse whole-signature neighbor. That made the `Hdac5` training row a strong low anchor for the HDAC5 packet.

The MEF2 ledger entries also favored a small or zero focal count: `Mef2d` was a pan-neuronal basal transcriptional null, `Mef2a` was real but tiny and thalamus-restricted, and the thalamic `Mef2c` response was limited rather than a transfer of the larger cortical IT response. The `Sin3a` ledger showed that a chromatin perturbation can be very visible in the focal class, but through ER protein-quality-control, RNA-processing, lipid/redox, lysosomal, and ciliary branches that are much broader than the HDAC5/MEF2 state and therefore set an assay-visibility boundary rather than a numeric expectation for Hdac4.

## Profile check

I compared the focal signed Wilcoxon profiles for `Hdac5`, `Mef2a`, `Mef2c`, `Mef2d`, and `Sin3a`. The profile table reproduced the count contrast:

- `Hdac5`: 0 significant focal features
- `Mef2a`: 4 significant focal features
- `Mef2c`: 1 significant focal feature
- `Mef2d`: 0 significant focal features
- `Sin3a`: 1,433 significant focal features

`Hdac5` did not form a strong profile with the MEF2 rows in this focal class. Its whole-profile cosine values to `Mef2c`, `Mef2d`, `Sin3a`, and `Mef2a` were 0.004, 0.004, 0.009, and -0.013, respectively. This supported treating the nearby HDAC5/MEF2 training rows as separate sparse/buffered examples rather than averaging them into a hidden larger module.

## Synthesis

The target is expressed in the assayed nuclei, so a nonzero result is biologically reachable. But the operative biology is buffered and stimulus-gated, the closest assayed HDAC5 perturbation is focal-zero and nearly pan-zero, and the represented MEF2 neighbors are focal-zero to focal-tiny rather than broad responders. The large `Sin3a` response shows that the thalamic population and Wilcoxon pipeline can detect a chromatin-corepressor perturbation, but its scale is tied to a different broad SIN3A/proteostasis state.

I therefore put the point estimate at the bottom of the plausible HDAC5/MEF2 range rather than at the `Mef2a` count of 4 or at the heavy-tailed chromatin-regulator scale.

**Predicted `n_degs`: 0**
