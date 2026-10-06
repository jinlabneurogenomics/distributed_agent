## Question

The requested held-out target list contains one gene:

- `Naa15`

For this gene I needed to predict the number of genes that would pass
Benjamini-Hochberg FDR < 0.05 in `151 TH Prkcd Grin2c Glut` nuclei after acute,
sparse, AAV-CRISPR loss of function. `Naa15` is not present as a training
perturbation, so I treated its expression signature and DEG count as absent and
borrowed evidence only from non-held-out perturbations plus external NatA
biology.

## Sources Used

- Focal training DEG counts:
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`
- Training differential-expression parquet:
  `[local file: training_de_all_cell_groups.parquet]`
- Requested manifest:
  `[local file: 141_Naa15.csv]`
- Distributed Agents same-experiment corpus:
  `perturbai-july-260713-sourceguard-1773-v1`
- Distributed Agents runtime profile-neighbor analysis over the focal-cell log2 fold
  change vectors
- PubMed searches for external literature on `NAA15`, `NAA10`, and the NatA
  N-terminal acetyltransferase complex

## Dataset Calibration

The focal training endpoint is zero-inflated: across 1,674 non-held-out
perturbations the median `n_degs` is 0, the 75th percentile is 1, the 95th
percentile is 18, and the upper 1% contains the broad responses. The largest
focal responses were `Uba5` 2677, `Tpr` 1768, `Sin3a` 1433, `Rnpc3` 868,
`Zbtb7a` 841, `U2af2` 828, `Psmb4` 742, and `Hnrnpu` 733 DEGs.

Within that calibration, the key NatA-related or protein-homeostasis-adjacent
training counts were:

| perturbation | focal `n_degs` | use in the `Naa15` prediction |
|---|---:|---|
| `Naa10` | 0 | Core catalytic NatA subunit and the closest mechanistic analog present in training. |
| `Psmb4` | 742 | Positive counterexample; proteasome disruption produced a large detectable RNA state. |
| `Psmc1` | 430 | Positive counterexample; independent proteasome perturbation. |
| `Ufc1` | 572 | Positive counterexample for perturbed proteostasis-like chemistry. |
| `Uba5` | 2677 | Positive counterexample for UFMylation/proteostasis stress. |
| `Eef2` | 9 | Translation perturbation with a small but nonzero focal response. |
| `Hspa5` | 5 | ER/chaperone stress perturbation with only a very small focal response. |
| `Hspa8` | 9 | Chaperone perturbation with only a very small focal response. |
| `Vcp` | 2 | Protein-quality-control perturbation with a near-null focal response. |
| `Copg1` | 1 | One of the weak/flat profile neighbors of `Naa10`; not NatA-specific. |
| `Mpc1`, `Rorb`, `Gli2`, `Diaph2` | 0 each | Flat-signature neighbors noted by the Distributed Agents corpus as nonmechanistic. |

For the focal profile-vector check I compared `Naa10` against every eligible
training perturbation in `151 TH Prkcd Grin2c Glut`, using `logfoldchanges` as
the signed profile, `names` as features, and `pvals_adj < 0.05` as the
significance call. `Naa10` had 0 significant focal features. Its nearest
whole-vector Pearson/cosine neighbors were mostly flat 0- or 1-DEG profiles:
`Abca1`, `Copg1`, `Hcn2`, `Pde10a`, `Sall1`, `Vldlr`, `Dennd5a`, `Arih1`,
`Lamp2`, and `Bmpr1a`. This was useful as a negative control but not as a
NatA-specific module, because those neighbors share a low-information vector
shape rather than NatA biology.

The same-experiment Distributed Agents corpus was stronger and more explicit for this
point. It had no `Naa15` target-context card, consistent with `Naa15` being held
out. For `Naa10`, it reported a pan-neuronal FDR-level transcriptomic null:
across 22 measured neuronal groups and 2,123 matched perturbed nuclei, `Naa10`
produced zero downstream genes at FDR < 0.10. The corpus also reported that
`Naa10` lacked compensatory NAT-family, integrated-stress, apoptosis, and
proteasome/ubiquitin rebound programs, while `Psmb4`, `Psmc1`, and `Eef2`
produced 1,119-14,008 FDR < 0.10 downstream genes across matched groups.

## External Biology

`Naa15` encodes the large auxiliary subunit of NatA, the complex in which
`NAA10` supplies the main catalytic N-terminal acetyltransferase activity.
Crystal and biochemical work shows that NAA15 binds NAA10 and HYPK in the human
NatA complex and positions/regulates the cotranslational acetylation machinery
at the ribosomal exit tunnel (Gottlieb and Marmorstein 2018,
doi:10.1016/j.str.2018.04.003; Weyer et al. 2017,
doi:10.1038/ncomms15726). NAA10 disease mutations can disrupt interaction with
NAA15 and NAA50 and change the N-terminal acetylome (Myklebust et al. 2014,
doi:10.1093/hmg/ddu611). Human loss-of-function `NAA15` variants cause a
dominant neurodevelopmental syndrome with intellectual disability, speech and
motor delay, autism-spectrum features, and congenital anomalies, supporting
NatA haploinsufficiency as biologically real in development (Cheng et al. 2018,
doi:10.1016/j.ajhg.2018.03.004). The mouse gene was originally described as the
NMDA-receptor-regulated developmental brain gene `Narg1`, homologous to yeast
N-terminal acetyltransferase machinery and highly expressed in neonatal
proliferative/migratory regions (Sugiura et al. 2001,
doi:10.1074/jbc.M100011200).

These facts make `Naa15` a strong NatA biochemistry gene, but they do not imply
a broad acute nuclear transcriptomic response in postmitotic juvenile neurons.
NatA loss primarily perturbs protein N-termini and downstream protein stability,
localization, folding, or interactions; it need not immediately alter thousands
of mRNAs. The direct experimental analog, `Naa10`, is the catalytic partner of
`Naa15`, was present in training, and was transcriptomically silent in the focal
cell group and across all measured neuronal groups.

## Target-Specific Reasoning

### Naa15

The most relevant in-dataset perturbation is `Naa10`, not the high-count
proteasome or UFMylation hits. `Naa10` and `Naa15` form the core NatA complex,
so an acute CRISPR loss of either subunit should be much more mechanistically
similar to one another than to `Psmb4`, `Psmc1`, `Uba5`, or `Ufc1`. In the focal
training endpoint `Naa10` had `n_degs = 0`, and the Distributed Agents corpus extended
that observation to a 22-neuronal-group null at FDR < 0.10. It also documented
the absence of a secondary integrated-stress, apoptotic, NAT-family, or
proteasome/ubiquitin rebound program after `Naa10` perturbation.

The positive counterexamples argue that this zero is not simply because the
assay could never detect a protein-homeostasis response. In the same focal
cell group, proteasome perturbations were large (`Psmb4` 742 DEGs and `Psmc1`
430 DEGs), UFMylation was very large (`Uba5` 2677 and `Ufc1` 572), and `Eef2`
gave a small but real 9-DEG translation-associated response. If NatA loss in
this postnatal mosaic experiment created a broad proteotoxic or translational
stress state, the endpoint should have had the dynamic range to see it.

The weakest part of the comparison is that `Naa15` is the NatA ribosome-adapter
subunit rather than the NAA10 catalytic enzyme, so complete loss of NAA15 can
reduce complex stability or ribosome recruitment in ways not identical to
partial NAA10 loss. Human `NAA15` haploinsufficiency is also developmental, and
the strongest external phenotypes come from germline or constitutive variant
carriers, not from sparse P16-P37/44 neuronal CRISPR. Still, the task endpoint
is assay- and time-dependent RNA breadth, and the direct training evidence says
that a core NatA lesion was buffered at the FDR level in this experiment.

I therefore predict no FDR < 0.05 DEGs for `Naa15`.

## Prediction

| target_name | predicted_n_degs |
|---|---:|
| `Naa15` | 0 |

## Limits

- `Naa15` itself was not measured as a perturbation, so the prediction is an
  extrapolation from `Naa10`.
- No other NatA/NatE subunit such as `Naa16` or `Naa50` was available with a
  focal training count, leaving one true complex-level analog.
- The null call is specific to acute, mosaic, postnatal neuronal CRISPR and a
  Wilcoxon/FDR RNA endpoint. It does not claim that NAA15 protein function,
  N-terminal acetylation, neuronal morphology, or long-term viability are
  unchanged.
- The available expression signatures are mostly downstream nuclear mRNA
  measurements; they cannot directly measure the N-terminal acetylome that is
  expected to be the primary biochemical output of NatA perturbation.
