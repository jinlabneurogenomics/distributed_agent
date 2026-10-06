# Prediction trace

## Question and resolved ambiguities

The held-out readout is the number of measured genes in `151 TH Prkcd Grin2c Glut` with Wilcoxon Benjamini-Hochberg adjusted `pvals_adj < 0.05` after acute mosaic AAV-CRISPR loss of each requested gene. The manifest for this run contains one held-out perturbation:

- `Zfp799`

I treated the input parquet and training count CSV as the calibration data and did not assume that a target transcript must decrease detectably for the perturbation to have worked, because this is an indel-based sparse Cas9 experiment and the task explicitly warns that weak self-RNA change is not evidence of failed editing.

## Sources used

- `training_de_all_cell_groups.parquet`: filtered to `group_name == "151 TH Prkcd Grin2c Glut"` and to candidate held-in perturbations to inspect focal-cell log fold changes, FDR values, and DEG counts.
- `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`: 1,674 held-in perturbations with the observed focal-cell `n_degs`.
- `271_Zfp799.csv`: the requested target list; it contains only `Zfp799`.
- Distributed Agents same-experiment corpus, release `perturbai-july-260713-sourceguard-1773-v1`: queried for `Zfp799`, `Zfp1`, `Zfp846`, `Zfp950`, `Setdb1`, and `Zbtb7a`.
- Distributed Agents local mouse gene-annotation cache: `genes.parquet`, `gene_membership.parquet`, and `gene_relationships.parquet`, with 18,123 genes, 464,095 gene-membership rows, and 51,743 pairwise rows.
- Distributed Agents run-local observed-profile tools: compared the held-in Zfp/KRAB candidates with broad transcriptional and chromatin counterexamples in the focal cell group.
- NCBI Gene Entrez record `240064`, updated 2026-09-10, and its Alliance of Genome Resources summary from June 2026, for `Zfp799` identity, protein-coding status, predicted nuclear Pol II transcription-factor function, and orthology to human `ZNF878`.
- UniProtKB release `2026_03`, release date 2026-09-02, for domain annotations. The mouse `Zfp799` entries include InterPro `IPR001909`/Pfam `PF01352` for a KRAB box and Pfam `PF00096` for C2H2 zinc fingers.
- Public literature on KRAB-ZFP biology:
  - Rowe et al. 2013, `Development`, DOI `10.1242/dev.087585`, PMID `23293284`: KRAB-ZFP/KAP1/ESET-SETDB1 requirements for de novo ERV methylation.
  - Imbeault, Helleboid and Trono 2017, `Nature`, DOI `10.1038/nature21683`, PMID `28273063`: mammalian KRAB-ZFPs as a large, rapidly evolving transposable-element regulatory family.
  - Helleboid et al. 2019, `EMBO Journal`, DOI `10.15252/embj.2018101220`, PMID `31403225`: many KZFPs recruit KAP1, while some have diverged toward other partners and functions.
  - Sun et al. 2019, `Journal of Molecular Biology`, DOI `10.1016/j.jmb.2019.05.002`, PMID `31078555`: TRIM28/KAP1 is the canonical corepressor recruited by KRAB-ZFPs and recruits SETDB1, HP1, and NuRD-related silencing effectors.

## Computations over the training data

I first read the focal-cell training count CSV and computed the response-class distribution. The training endpoint is very sparse: 1,205 of 1,674 held-in perturbations have `0` DEGs, 363 have `1-9`, 63 have `10-99`, and 43 have at least `100`; the median is `0` and the 75th percentile is `1`.

I then queried the local annotation cache for `Zfp799`. It is represented as a perturbation target and measured gene, has 11 broad memberships, and has no cached pairwise relationship rows. Because no pairwise partner was available, I computed a set-overlap screen between `Zfp799`'s memberships and every held-in perturbation's memberships, then inspected held-in zinc-finger genes with matching KRAB/C2H2-like annotations and their actual focal-cell `n_degs`.

The closest annotation neighbors among measured held-in perturbations were:

| Held-in analog | Shared Zfp799 memberships | Focal `n_degs` | Focal expression evidence |
|---|---:|---:|---|
| `Zfp961` | 10 | 0 | no FDR-significant feature |
| `Zfp612` | 9 | 1 | one positive FDR hit, `Notum`; otherwise flat |
| `Zfp664` | 8 | 0 | no FDR-significant feature |
| `Zfp1` | 9 | 0 | no FDR-significant feature in 151; same-experiment corpus reports zero FDR<0.10 genes across all neuronal groups |
| `Zfp949` | 7 | 0 | no FDR-significant feature |
| `Zfp846` | 8 | 0 | no FDR-significant feature in 151; corpus reports one narrow non-151 singleton and no robust convergent neighbor |
| `Zkscan16` | 8 | 0 | no FDR-significant feature |
| `Zfp266` | 7 | 0 | no FDR-significant feature |
| `Zkscan1` | 8 | 0 | no FDR-significant feature |
| `Zfp160` | 9 | 0 | no FDR-significant feature |

These 10 nearest annotation neighbors have a mean of `0.1` focal DEGs, a median of `0`, and 9 of 10 are exactly zero.

As counterexamples, I looked at other held-in zinc-finger and chromatin regulators that can respond in this same cell class:

| Counterexample | Focal `n_degs` | Why I did not project it to `Zfp799` |
|---|---:|---|
| `Zfp423` | 150 | It is a zinc-finger transcription factor but its annotation points to Notch/BMP/adipogenic and developmental programs, not KRAB/C2H2 retroelement repression. Its focal top genes (`Grid2ip`, `Cd47`, `Ntsr1`, `Kcnab3`, `Syt13`) do not match a KRAB-ZFP repressive-axis state. |
| `Zfp236` | 19 | It is a Pol II DNA-binding TF with far fewer shared `Zfp799` memberships; its nonzero count shows that some Zfp genes are detectable, but it is a weaker mechanistic analog than the KRAB/C2H2-like genes above. |
| `Zfp148` | 8 | A general zinc-finger repressor with small nonzero output; not a KRAB-family analog and much weaker than the strong TF outliers. |
| `Setdb1` | 22 | A downstream H3K9 methyltransferase used by KRAB/KAP1 silencing complexes. It is useful as an assay-capacity comparator but is broader and enzymatic; its 151 program up-regulated `Tasor`, `Atf7ip`, `Abhd12b`, and a Pcdh/HUSH-biased module rather than phenocopying individual KRAB-ZFPs. |
| `Zbtb7a` | 841 | A broad BTB/POZ transcription-factor perturbation with a trafficking, lysosomal, and neurosecretory state (`Pnma3`, `Col9a3`, `Gpc1`, `Usp11`, `Sema4a` among the top focal hits); it is a positive control for a strong neuronal TF response but mechanistically far from `Zfp799`. |

I also built a run-local profile comparison over `Zfp961`, `Zfp612`, `Zfp664`, `Zfp1`, `Zfp949`, `Zfp846`, `Zkscan16`, `Zfp266`, `Zkscan1`, `Zfp160`, `Zfp423`, `Setdb1`, and `Zbtb7a` in `151 TH Prkcd Grin2c Glut`, using `logfoldchanges` as the signed value and `pvals_adj < 0.05` as the significant-feature threshold. Nine of these 13 nodes had no significant feature in the focal group; only `Zfp612`, `Setdb1`, `Zfp423`, and `Zbtb7a` were nonzero. All inspected pairs between the flat close Zfp nodes and `Setdb1`, `Zfp423`, or `Zbtb7a` had zero intersecting FDR-significant positive features and zero intersecting FDR-significant negative features. Whole-profile correlations among flat signatures were not used to transfer a nonzero count because they were driven by subthreshold rank structure and by large log fold changes on genes with `pvals_adj = 1`.

## Same-experiment corpus evidence

The Distributed Agents corpus has no `Zfp799` finding, claim, or first-hop edge, so there is no direct same-experiment report for this held-out target.

It does have useful KRAB-ZFP boundary evidence around `Setdb1`, `Zfp1`, `Zfp846`, and `Zfp950`. The synthesized claim `claim:340c7e3bcac13675d574` states that the individual KRAB/C2H2 perturbations `Zfp1`, `Zfp950`, and `Zfp846` are not rate-limiting for the `Setdb1`-sensitive neuronal repressive response detected in this assay. A second high-confidence claim, `claim:68384b3b4cce631738fa`, states that the `Setdb1`-sensitive protocadherin/`Atf7ip`/`Tasor` neuronal response is detectable but is not reproduced by assayed KRAB-ZFPs, `Smchd1`, `Dnmt3a`, or other nearby heterochromatin perturbations. In the individual finding cards:

- `Zfp1:F001` reports no downstream gene-level DE genes at FDR<0.10 in any of the 23 recovered neuronal cell groups after the same P16-to-P37/44 mosaic CRISPR loss of function.
- `Zfp1:F002` reports divergence from `Setdb1`: `Setdb1` had 45 FDR<0.10 genes across 9 of 22 measured groups whereas matched `Zfp1` vectors had zero, with `Setdb1`-`Zfp1` score correlation only 0.005.
- `Zfp846:F003` reports that `Zfp846` does not phenocopy the detectable SETDB1/KRAB-adjacent repressive program, even though `SETDB1` is a core enzyme recruited by KRAB-ZFP systems.
- `Zfp950:F003` reports the same boundary for another KRAB/C2H2 zinc-finger gene.

This directly addresses the main positive hypothesis for `Zfp799`: even when a held-in target has KRAB/C2H2 architecture, individual DNA-binding KRAB-ZFP losses were usually silent in postnatal NeuN+ neurons rather than scaling up to the `Setdb1` response.

## Target-specific prediction

### `Zfp799`

`Zfp799` is predicted by NCBI/Alliance to be a nuclear Pol II transcriptional regulator and, by UniProtKB 2026_03 domain calls, contains a KRAB box and C2H2 zinc-finger architecture. The external biology therefore puts it in the KZFP family that can recruit TRIM28/KAP1 and SETDB1-associated H3K9 machinery to selected repeat-derived or promoter targets. That is a real route to transcriptional repression in principle: KRAB-ZFPs target KAP1/ESET-SETDB1 to ERV or transposable-element loci in embryonic contexts, and many mammalian KZFPs are repeat-targeting repressors.

For this endpoint, however, the transfer signal comes mainly from the dataset and goes the other way. The closest held-in KRAB/C2H2-like transcription factors are overwhelmingly flat in `151 TH Prkcd Grin2c Glut`: `Zfp961` 0, `Zfp612` 1, `Zfp664` 0, `Zfp1` 0, `Zfp949` 0, `Zfp846` 0, `Zkscan16` 0, `Zfp266` 0, `Zkscan1` 0, `Zfp160` 0, and `Zfp950` 0. Their profiles do not share FDR-level genes with the stronger `Setdb1`, `Zfp423`, or `Zbtb7a` responses. The same-experiment corpus further shows that measured KRAB/C2H2 factors `Zfp1`, `Zfp846`, and `Zfp950` specifically failed to reproduce the `Setdb1` Pcdh/HUSH/`Atf7ip`/`Tasor` program despite the screen being able to detect a modest `Setdb1` signature.

The broad responders are therefore assay-capacity controls rather than donors for `Zfp799`: `Setdb1` perturbs a catalytic node used by many silencing complexes, while `Zbtb7a` and `Zfp423` are distinct transcription factors with strong but different neuronal states. I do not see evidence that a single, lightly annotated KRAB DNA-binding factor such as `Zfp799` is rate-limiting in juvenile thalamic glutamatergic neurons under the mosaic partial-loss regime. I therefore predict no FDR-significant annotated gene-level response:

- predicted `Zfp799 n_degs = 0`

## Limits

The main limitation is the absence of any direct `Zfp799` corpus claim, measured `Zfp799` perturbation profile, or public functional study that maps its DNA targets in mouse neurons. `Zfp799` could repress a small private target set not shared with `Zfp1`, `Zfp846`, `Zfp950`, or the other KRAB-like analogs. The parquet also measures coding-gene nuclear RNA, not repeat-family RNA or H3K9me3, so a genuine repeat or chromatin effect could be invisible to the requested endpoint. TRIM28/KAP1 and the HUSH subunits were not themselves represented as held-in focal counts, so `Setdb1` is an indirect corepressor comparator. Finally, the perturbation is acute, mosaic, and partial; the prediction is not meant to describe a germline `Zfp799` knockout or an embryonic floor-plate phenotype.
