## Question and interpretation

The requested held-out target list contained one perturbation:

- `Mapk8ip1`

I interpreted `n_degs` exactly as the endpoint in `151 TH Prkcd Grin2c Glut`: the number of measured genes, including the perturbed target transcript if it was measured, with `pvals_adj < 0.05` for the Wilcoxon perturbation-vs-control contrast. `Mapk8ip1` was absent as a perturbation from both supplied training files, so I treated all `Mapk8ip1` rows in the parquet as ordinary measured-gene rows under other perturbations, not as a hidden `Mapk8ip1` perturbation signature.

## Sources

- Differential-expression matrix: `[local file: training_de_all_cell_groups.parquet]`
- Focal-cell training counts: `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`
- Requested targets: `[local file: 131_Mapk8ip1.csv]`
- Distributed Agents corpus MCP, release `perturbai-july-260713-sourceguard-1773-v1`. The target-scoped corpus had no `Mapk8ip1` node, but had useful stress-MAPK and kinesin/transport claims for `Mapk9`, `Map2k6`, `Kif5a`, `Kif5c`, `Klc1`, `App`, and `Dctn1`.
- Distributed Agents runtime `profile_neighbors`, used as a focal-cell signature-neighborhood QC on selected JNK, kinesin, APP, and dynactin anchors against the full 1,674-target eligible universe.
- External PubMed literature on JIP1/MAPK8IP1 JNK scaffolding and APP/kinesin transport.

## Computational evidence from the supplied data

I first loaded the training-count CSV for the focal cell group. It contains 1,674 non-held-out targets. The endpoint is very sparse in this population:

- 1,205 / 1,674 targets have `n_degs = 0`.
- The median is 0 and the 75th percentile is 1.
- Only 5% of training targets exceed 18 DEGs.

I then scanned the parquet only for `group_name == "151 TH Prkcd Grin2c Glut"` and for a hand-curated set of biologically relevant comparators. This gave the observed focal-cell counts and the actual significant rows for the JIP1-adjacent perturbations.

### JNK / stress-MAPK comparators

The closest assayed JNK core target was `Mapk9`, because `Mapk8`, `Mapk10`, `Map2k7`, `Map2k4`, `Mapk8ip2`, and `Mapk8ip3` were not present as perturbation targets.

| training target | focal `n_degs` | focal expression-pattern evidence |
| --- | ---: | --- |
| `Mapk9` | 0 | no FDR<0.05 genes; the `Mapk9` self row was only nominal, logFC -0.347, BH FDR 1.0 |
| `Map2k6` | 0 | no FDR<0.05 genes |
| `Map3k7` | 0 | no FDR<0.05 genes |
| `Mapk1` | 0 | no FDR<0.05 genes |
| `Map2k2` | 0 | no FDR<0.05 genes |
| `Map2k1` | 4 | a small ERK/MEK1-specific program, not a JNK scaffold-like response: `Vgf`, `Ptpn5`, `Etv5`, `Unc13a` |
| `Jund` | 0 | no FDR<0.05 genes |

This block argues that basal loss of one stress-MAPK/JNK-adjacent signaling node usually does not create a large soma-detectable nuclear RNA program in this assay. That interpretation is also the Distributed Agents corpus claim `claim:73be997a6a0b095c36d2`, which summarizes `Map2k6`, `Mapk9`, and `Taok1` evidence as absent or nonconvergent basal stress-MAPK responses.

### Kinesin-1, APP-transport, and cargo-adaptor comparators

`Mapk8ip1`/JIP1 is also a kinesin-1 and APP cargo adaptor. The assayed transport-side neighbors were essentially self-only or silent in the focal population:

| training target | focal `n_degs` | focal expression-pattern evidence |
| --- | ---: | --- |
| `App` | 1 | the only FDR<0.05 row was the `App` self row, logFC -1.420 |
| `Kif5a` | 1 | the only FDR<0.05 row was the `Kif5a` self row, logFC -0.445 |
| `Kif5c` | 1 | the only FDR<0.05 row was the `Kif5c` self row, logFC -0.528 |
| `Kif1a` | 1 | the only FDR<0.05 row was the `Kif1a` self row, logFC -0.561 |
| `Klc1` | 1 | the only FDR<0.05 row was the `Klc1` self row, logFC -0.525 |
| `Klc2` | 1 | the only FDR<0.05 row was the `Klc2` self row, logFC -0.467 |
| `Trak1` | 0 | no FDR<0.05 genes |
| `Rhot1` | 0 | no FDR<0.05 genes |
| `Atcay` | 1 | the only FDR<0.05 row was the `Atcay` self row, logFC -0.515 |
| `Psen1` | 0 | no FDR<0.05 genes |
| `Adam10` | 0 | no FDR<0.05 genes |
| `Sorl1` | 0 | no FDR<0.05 genes |

The Distributed Agents corpus makes the same distinction: claims `claim:064f16f0e8bfd08f9b64` and `claim:e899855f793ac6e6001e` state that represented kinesin-1, KIF1/Rab3/exocytosis, Miro/TRAK, and related transport genes do not form a common soma-detectable neuronal nuclear transcriptional module, with sparse target-specific exceptions. The `App` target context also explicitly records that `App` loss depleted `App` mRNA without producing downstream FDR-supported DEGs in recovered neuronal classes, and that APP-processing targets were transcriptionally uncoupled from a shared juvenile neuronal RNA response.

### Counterexamples that show transport genes can be detected

The decision is not that all transport genes are invisible. I used the following focal-cell positives as counterexamples:

| training target | focal `n_degs` | focal expression-pattern evidence |
| --- | ---: | --- |
| `Dctn1` | 75 | strong up-regulation of SREBF2/sterol genes such as `Insig1`, `Msmo1`, `Hmgcs1`, `Cyp51`, `Hmgcr`, `Fdft1`, `Sqle`, plus `Dctn1` self-depletion |
| `Rab7` | 501 | a broad endolysosomal/vATPase/sterol response including `Atp6v1b2`, `Ptgds`, `Dpp7`, `Scpep1`, `Dusp1`, `Insig1`, `Atp6v0b`, `Lamp2`, `Mcoln1`, `Grn` |
| `Mib1` | 27 | sterol/cholesterol program overlapping `Dctn1`: `Insig1`, `Dhcr24`, `Fdft1`, `Ldlr`, `Msmo1`, `Hmgcs1`, `Hmgcr`, `Cyp51` |
| `Tsc2` | 86 | mixed lysosome/mTOR/sterol response including `Cyp51`, `Pik3r3`, `Ptgds`, `Dusp1`, `Hmgcr`, `Ldlr` |
| `Srebf2` | 7 | self-depletion plus down-regulation of the same cholesterol genes that `Dctn1` and `Mib1` induce |

These are imperfect mechanistic analogs for JIP1. Distributed Agents `Dctn1` claims tie the `Dctn1` response to dynactin/endolysosomal SREBF2-like cholesterol feedback, and explicitly record that canonical kinesins such as `Kif5a`, `Kif5c`, `Kif1a`, and `Kifbp` did not robustly phenocopy `Dctn1`. I therefore used `Dctn1`, `Rab7`, `Mib1`, `Tsc2`, and `Srebf2` to confirm that the focal cell group can mount a sterol/endolysosomal transport-stress state, but not as high-count predictors for `Mapk8ip1`.

### Target self-row calibration

Among the 1,642 training targets that were also measured genes in this focal cell group, 319 had their own transcript pass FDR 0.05. Many one-DEG perturbations were exactly this: the target transcript itself crossed FDR and no downstream genes did. The `App`, `Kif5a`, `Kif5c`, `Kif1a`, `Klc1`, `Klc2`, and `Atcay` analogs above all fall in that class.

`Mapk8ip1` itself was a measured feature in the focal parquet. Across the 1,674 non-held-out perturbations, its median absolute logFC was small, but broad perturbations such as `Uba5`, `Zbtb7a`, `Cic`, `Atxn1`, and `Ufc1` significantly up-regulated `Mapk8ip1`. That tells me the gene was detectable enough in this cell group that an on-target mRNA row could plausibly be counted. The prediction of one DEG is therefore a self-row call, not a prediction of a downstream module.

## External biological rationale

MAPK8IP1/JIP1 is not itself a transcription factor. It is a scaffold for the MLK -> MKK7 -> JNK cascade: Yasuda et al. 1999 showed that JIP1/JIP2 assemble MLK, MKK7, and JNK pathway components into scaffolded MAPK modules (DOI: 10.1128/MCB.19.10.7245; PMID: 10490659), and Willoughby et al. 2003 showed that JIP1 can also recruit the JNK phosphatase MKP7 to modulate JNK signaling (DOI: 10.1074/jbc.M207324200; PMID: 12524447). Separately, JIP1 links APP-containing vesicles to kinesin-1/dynein transport: Horiuchi et al. 2007 connected the JIP1 ortholog APLIP1 to DLK/MKK7/JNK control of kinesin-cargo dissociation in axons (DOI: 10.1016/j.cub.2007.06.062; PMID: 17658258), Fu and Holzbaur 2013 showed that mammalian JIP1 coordinates APP axonal transport directionality by regulating kinesin and dynactin/dynein engagement (DOI: 10.1083/jcb.201302078; PMID: 23897889), and Chiba et al. 2014 showed that JIP1b-KLC1 interactions are required for efficient fast anterograde APP transport in neurons (DOI: 10.1091/mbc.E14-06-1111; PMID: 25165140).

Those mechanisms are strong priors for altered JNK phosphorylation or cargo movement, but weak priors for a broad change in steady-state nuclear mRNA in unstimulated postnatal neurons. The actual training perturbations nearest those two biochemical roles, especially `Mapk9`, `Map2k6`, `App`, `Kif5a`, `Kif5c`, `Klc1`, `Klc2`, `Trak1`, and `Rhot1`, were zero or self-only in `151 TH Prkcd Grin2c Glut`.

## Target-specific prediction

| target | prediction | reasoning |
| --- | ---: | --- |
| `Mapk8ip1` | 1 | The downstream prediction is effectively zero: represented JNK/stress-MAPK nodes were silent, and kinesin-1/APP transport analogs were silent or self-only. `Dctn1` and `Rab7` prove that this cell group can report a transport-adjacent sterol/endolysosomal stress module, but Distributed Agents evidence shows that module does not extend to canonical kinesin-1 perturbations. I assigned a point estimate of 1 because the endpoint includes the target transcript and the closest expressed scaffold/transport genes in this focal group often contributed exactly one DEG, their own depleted mRNA. |

## Limits

The main limitation is the lack of exact same-branch perturbations: `Mapk8`, `Mapk10`, `Map2k7`, `Map2k4`, `Mapk8ip2`, and `Mapk8ip3` were unassayed as training targets. The Distributed Agents corpus also had no `Mapk8ip1` node, so its claims constrain JNK and kinesin biology through neighboring measured genes rather than through a direct JIP1 finding. The perturbation screen measures nuclear RNA 3-4 weeks after sparse juvenile CRISPR; it is poorly aligned to the local axonal transport, cargo-directionality, phospho-JNK, and stress- or injury-evoked phenotypes for which JIP1 is best known. Finally, the difference between predicting 0 and 1 is dominated by whether the `Mapk8ip1` self-transcript row passes BH correction, and target self-detection is variable in this assay.
