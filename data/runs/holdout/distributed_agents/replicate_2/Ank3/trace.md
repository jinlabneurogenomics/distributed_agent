# Ank3 DEG-count prediction for 151 TH Prkcd Grin2c Glut

## Question and resolved ambiguities

The held-out readout is the number of measured genes with Scanpy/Wilcoxon
Benjamini-Hochberg-adjusted `pvals_adj < 0.05` after a single gene is perturbed
in `151 TH Prkcd Grin2c Glut` cells. The manifest for this run contains one
held-out target, `Ank3`.

I interpreted `n_degs` exactly as in the training-count CSV:

- the target transcript itself is counted if its own row is FDR-significant;
- the prediction must be an integer count for the focal cell group only;
- no direct `Ank3` DE rows can be used, because `Ank3` was held out from both
  the parquet and the focal-cell training counts.

## Sources used

- `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`
  for the observed `n_degs` endpoint in `151 TH Prkcd Grin2c Glut`.
- `[local file: training_de_all_cell_groups.parquet]`
  for per-gene Wilcoxon signed DE profiles of non-held-out perturbations.
- `[local file: 010_Ank3.csv]`
  for the requested held-out target.
- Distributed Agents same-experiment corpus
  `perturbai-july-260713-sourceguard-1773-v1`, especially target-scoped
  summaries for `Ank2`, `Sptan1`, `Nrcam`, `Scn2a`, and `Kcnq2`.
- Distributed Agents runtime profile tools:
  - `profile_neighbors` compared `Ank2`, `Sptan1`, `Nrcam`, `Kcnq2`, and
    `Scn2a` against all 1,674 measured training targets in the `151` signed
    Wilcoxon-score space.
  - `profile_compare` and `profile_inspect` compared a hand-selected
    19-perturbation ankyrin/spectrin, L1-family, NaV, and Kv7 cohort in the same
    focal cell group.
- NCBI PubMed literature retrieved for external AnkG biology.

External mechanism references:

- Leterrier et al. 2017, DOI `10.3389/fncel.2017.00006`: ankyrin-G membrane
  partners, including voltage-gated sodium channels and neurofascin-186, help
  establish and maintain the axon initial segment.
- Freal et al. 2019, DOI `10.1016/j.neuron.2019.07.029`: ankyrin-G, neurofascin,
  EB proteins, and TRIM46 participate in feedback-based AIS assembly.
- Yang et al. 2019, DOI `10.1073/pnas.1909989116`: giant ankyrin-G recruits
  beta4-spectrin through a regulated conformation needed for ordered AIS
  assembly.
- He et al. 2022, DOI `10.1016/j.jbc.2022.102272`: structural and cellular
  evidence for ankyrin-G binding to neurofascin at the AIS.
- Smith et al. 2014, DOI `10.1016/j.neuron.2014.10.010`: ankyrin-G also acts in
  glutamatergic spine nanodomains.
- Nelson et al. 2018, DOI `10.1038/s41380-018-0308-x`: an Ank3/GABARAP
  interaction regulates forebrain GABAergic circuitry in vivo.
- Stevens and Rasband 2022, DOI `10.1080/19336950.2022.2120467`: review of
  ankyrin-family scaffolds for ion channels and transporters.

## Dataset computations

The held-out manifest has exactly one row, `Ank3`. The focal training-count file
has 1,674 non-held-out targets. Its distribution is dominated by zeros:

- mean `n_degs`: 14.1, inflated by a few very broad responses;
- median `n_degs`: 0;
- 1,205 of 1,674 targets have `n_degs = 0`;
- 75th percentile: 1 DEG;
- 95th percentile: 18 DEGs.

I inspected the parquet metadata rather than materializing all 616,253,184 rows.
The file is row-grouped by cell group; `151 TH Prkcd Grin2c Glut` occupies row
groups 546 through 580. I read only those row groups and filtered to the
mechanistically relevant assayed perturbations. Each target had 17,259 measured
gene rows in this focal group.

The focal-cell analogs were almost all complete nulls or target-self singletons:

| training perturbation | `n_degs` in 151 | FDR 0.05 events in the focal parquet | interpretation for Ank3 |
|---|---:|---|---|
| `Ank2` | 0 | none | closest assayed ankyrin scaffold paralog; no target self-call and no downstream AIS/channel response |
| `Ank1` | 0 | none | ankyrin-family counterpoint; also null |
| `Sptan1` | 1 | only `Sptan1` down | alpha-II-spectrin, a cytoskeletal scaffold relative; self-only |
| `Sptb`, `Add1`, `Add2`, `Add3` | 0 each | none | spectrin/adducin membrane-skeleton neighbors; no shared response |
| `L1cam`, `Ncam1`, `Chl1` | 1 each | only self for each target | IgSF/adhesion neighbors of ankyrin-linked axonal biology; self-only |
| `Nrcam` | 2 | `Nrcam` down and `Letm2` up | L1-family AIS/node-associated CAM; only one downstream singleton |
| `Cntnap1`, `Cntnap2` | 1 each | only self for each target | paranodal/juxtaparanodal adhesion comparators; no broad axonal transcriptional module |
| `Scn1a`, `Scn2a`, `Scn8a` | 1 each | only self for each target | NaV alpha-subunits that bind AnkG at the AIS; no secondary channel/homeostatic program |
| `Scn1b` | 2 | `Scn1b` down and `Jun` up | NaV beta-subunit; singleton downstream response only |
| `Scn3a`, `Kcnq1` | 0 each | none | voltage-gated-channel counterexamples that are fully flat |
| `Kcnq2`, `Kcnq3` | 1 each | only self for each target | Kv7 AIS-channel partners; no focal downstream program at FDR 0.05 |

The same focal cell group is not globally incapable of responding to membrane or
ion-homeostasis lesions. For example, `Cacna1g` had 12 DEGs, `Atp1a3` had 80,
`Grin1` had 89, `Atp2a2` had 187, and `Rab7` had 501 in the same endpoint. The
flatness is specific to the directly relevant ankyrin, AIS-adhesion, and AIS
channel neighborhood rather than an artifact of `151` power.

The Distributed Agents runtime signed-profile comparison supported the thresholded
picture. In the exact focal group, `Ank2` and `Ank1` had zero significant
features; `Sptan1`, `Nrcam`, and `Kcnq2` had only one to two significant
features. Among inspected scaffold/channel pairs, whole-profile cosines were all
tiny: for example `Ank2` versus `Sptan1` was 0.026, `Ank2` versus `Nrcam` was
not strong enough to enter its first eight whole-profile local neighbors within
the 19-node cohort, `Ank2` versus `Scn2a` was -0.004, and `Kcnq2` versus
`Kcnq3` was only 0.044. None of these pairs shared an exact FDR 0.05 positive or
negative significant gene in `151`.

## Target-specific reasoning

### Ank3

`Ank3` encodes ankyrin-G, the canonical master scaffold of the axon initial
segment. AnkG concentrates NaV channels, Kv channels, neurofascin-family CAMs,
and beta4-spectrin in a periodic cytoskeletal membrane domain that controls
spike initiation and axonal polarity. AnkG is also reported outside the AIS in
glutamatergic spines and in GABAergic receptor regulation. Those facts make
`Ank3` biologically important, but most of the direct phenotypes are local
protein localization, membrane excitability, spine, or circuit phenotypes rather
than obvious soma-wide RNA programs.

The strongest in-dataset analog is `Ank2`. Distributed Agents corpus finding
`Ank2:F003` directly contrasted measured ankyrin/spectrin/adducin/L1CAM
structural comparators and found them "flat or sparse like Ank2"; the supporting
evidence reported `Ank2` itself as a 0-downstream-gene perturbation across all
23 recovered neuronal groups and noted that `Ank3`, `Sptbn1`, `Sptbn2`,
`Sptbn4`, and `Nfasc` were absent as perturbation targets. In the focal group
used for this prediction, `Ank2` had 0 DEGs despite 218 perturbed nuclei, and
`Ank1` also had 0. `Sptan1` had a single FDR event, its own transcript, whereas
`Sptb`, `Add1`, `Add2`, and `Add3` were all zero. This set argues against a
generic transcriptional consequence of disturbing the ankyrin/spectrin membrane
skeleton after sparse juvenile CRISPR.

The second bridge is the AnkG-associated AIS membrane neighborhood. AnkG binds
the same channel/CAM families represented by `L1cam`, `Nrcam`, `Scn1a`,
`Scn2a`, `Scn8a`, `Kcnq2`, and `Kcnq3`, but those perturbations in `151`
remained at self-only or one-downstream-gene scale. Distributed Agents corpus findings
for `Nrcam`, `Scn2a`, and `Kcnq2` all state the same limitation in the original
experiment: node/paranode adhesion genes, NaV subunits, and Kv7 subunits did not
collapse into shared postmitotic neuronal nuclear mRNA phenotypes. That matters
for `Ank3` because AIS disassembly could still alter NaV/Kv channel localization
without producing changes in channel mRNAs.

The nonzero counterexamples did not pull the estimate upward. `Cacna1g` is a
voltage-gated calcium-channel pore gene with 12 DEGs in `151`, and `Atp1a3` and
`Grin1` have much larger thalamic programs, so the assay can detect an
excitability or membrane-trafficking signature in this cell type. Those programs
are not seen in the ankyrin/spectrin, L1-CAM, NaV, or Kv7 perturbations that are
closer to AnkG.

Prediction: `Ank3` is more central to AIS integrity than `Ank1` or `Ank2`, so a
small self-transcript call is plausible. However, the closest observed ankyrin
paralogs were exact zeros in the requested endpoint, and the assayed direct
protein neighbors that did show nonzero counts mostly did so through their own
transcript rather than a downstream module. With no `Nfasc` or `Sptbn4` direct
readout and no evidence that the held-out `Ank3` guides would force an FDR 0.05
self decrease, the conservative point call is no FDR-significant genes.

`Ank3` predicted `n_degs`: **0**.

## Limits

- The direct `Ank3` expression signature and count were completely held out; the
  prediction is an extrapolation from `Ank1`, `Ank2`, AIS membrane partners, and
  structural scaffold neighbors.
- Two of the most exact AnkG partners, `Sptbn4` and `Nfasc`, were not assayed as
  training perturbations, and the corpus explicitly notes this gap.
- The experiment measures acute, sparse, postnatal CRISPR loss by snRNA-seq. It
  does not measure AnkG protein, AIS channel clustering, NaV/Kv current density,
  axonal polarity, synapse ultrastructure, or network synchrony.
- A target-self singleton depends on guide placement, indel spectrum,
  transcript architecture, and probe coverage. The training data showed both
  strong self calls in nearby genes and complete absence of a self call for
  `Ank1` and `Ank2`, so the zero-versus-one boundary is the main uncertainty.
- External Ank3 literature includes shRNA, culture, isoform-specific, germline,
  knock-in, and disease-variant systems. Those establish AnkG mechanism but are
  imperfect matches to mosaic P16 AAV-CRISPR in juvenile thalamic glutamatergic
  neurons.
