# Srsf1 direct n_degs forecast

## Target biology used

- Target and held-out endpoint: `Srsf1` in `151 TH Prkcd Grin2c Glut`; `Srsf1` is absent from the declared 151-class training count table.
- Exact focal-population reach from the declared biology bundle: `Srsf1` RNA was detected in 21,599 of 23,679 non-target nuclei in this class, 91.2158% expressing, with mean CP10K 2.0226 and mean raw UMI 3.2389. This supports broad accessibility of the perturbation in the assayed thalamic glutamatergic population, while the bundle explicitly warns that self-transcript abundance is not an editing-efficiency readout.
- The same bundle adjudicates SRSF1 stock as `likely_substantially_depleted` by the P37-P44 harvest after a P16 disruptive edit: the active nuclear and shuttling pools are continuously renewed RNA-processing protein pools rather than stable pre-installed structures. The four-day developmental cortical knockdown datum only supports rapid realizability, not direct P16 postmitotic thalamic severity.
- Functional interpretation: SRSF1 is an SR-family pre-mRNA splicing and post-splicing export/translation factor. SRSF2-related overlap and the lack of a direct postnatal thalamic loss experiment leave compensation and exact severity unresolved, and a whole-gene snRNA-seq DEG count will miss isoform-only defects.

## Training scale in 151 TH Prkcd Grin2c Glut

The declared count table has 1,674 observed training perturbations for this cell class. It is zero-heavy, with 1,205 zeros, median 0, 75th percentile 1, 90th percentile 2, 95th percentile 18, and 99th percentile 454; only 43 targets had at least 100 DEGs, 29 had at least 200, 19 had at least 400, and 12 had at least 600.

Observed RNA-processing and spliceosome counts formed the relevant high-effect tail:

| target | n_degs |
| --- | ---: |
| Rnpc3 | 868 |
| U2af2 | 828 |
| Hnrnpu | 733 |
| Cdc40 | 624 |
| Tnpo3 | 618 |
| Prpf6 | 454 |
| Thoc1 | 303 |
| Snrnp70 | 213 |
| Tardbp | 210 |
| Matr3 | 149 |
| Hnrnpc | 122 |

Matched negative/boundary points from the same family were also important: `Hnrnpa2b1` had 11, `Ddx3x` 8, `Hnrnph2` 4, `Hnrnpdl` 1, and `Ddx39b`, `Rbm28`, and `Snrpb` had 0 in the same endpoint.

## Same-experiment semantic/profile evidence

- Same-experiment Findings, used only as interpreted summaries of the training experiment, place `U2af2`, `Cdc40`, `Prpf6`, `Rnpc3`, and `Snrnp70` in a recurrent RNA-processing/spliceosome response in the thalamic and midbrain responder groups. Material records were `U2af2:F005` and `U2af2:F006`, `Cdc40:F002` and `Cdc40:F008`, and `Prpf6:F003`.
- Those Findings also show selectivity: `Cdc40:F008` explicitly contrasts convergence among `Prpf6`, `U2af2`, and `Snrnp70` with flat `Snrpb`, while `U2af2:F006` notes weak or nonconvergent `Hnrnpc`, `Hnrnpa2b1`, `Hnrnph2`, `Ddx39b`, and `Rbm28`. I therefore did not treat all spliceosome-annotated genes as interchangeable.
- I compared 18 observed RNA-processing/RNP perturbations in the declared Parquet filtered to `151 TH Prkcd Grin2c Glut` (`workbench/rna_processing_profile_compare.json`). All 18 profiles were available; 11 had at least 50 significant genes, 3 had 10 or fewer significant genes, 1 had 10-49, and 3 had none. The five focal high-confidence RNA-processing nodes had the expected significant-feature counts: `U2af2` 828, `Cdc40` 624, `Prpf6` 454, `Hnrnpu` 733, and `Snrnp70` 213.
- The profile comparison supported a broad same-direction RNA-processing stress geometry, but it was not used as a monotone count predictor. Whole-profile similarity connected high-count and null nodes, so I used it only to confirm that the high-count spliceosome/RNP perturbations occupy a related state and that nulls such as `Snrpb` remain real boundaries.

## Synthesis

`Srsf1` has high focal expression and a dynamic protein product expected to be functionally depleted over the 21-28 day window, so a null forecast would be too low. Its biology is closest to a single SR-family splicing regulator, not to pan-SR import (`Tnpo3`) or core U2/U5/PRP17 machinery (`U2af2`, `Prpf6`, `Cdc40`, `Rnpc3`), whose observed DEG counts span 454-868 in this cell class. The gene-level endpoint, unresolved SRSF paralog buffering, and survivor conditioning pull the forecast below that core-spliceosome block, while its essential RNA-processing role and stronger target reach put it above the nearly flat hnRNP/Sm boundaries.

I therefore placed `Srsf1` near the lower edge of the strong RNA-processing tail, close to `Snrnp70` and `Tardbp` and above `Matr3`/`Hnrnpc`: **220 DEGs**.
