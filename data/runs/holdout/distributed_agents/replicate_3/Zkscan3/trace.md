# DEG-count prediction trace

## Question

The requested held-out target is `Zkscan3`. I interpreted the endpoint as the exact scalar used in the supplied training table: the number of measured genes in `151 TH Prkcd Grin2c Glut` nuclei whose Wilcoxon `pvals_adj` is below 0.05 after acute sparse AAV-CRISPR loss of the target gene.

I treated the held-out target as absent from both the parquet and the training-count CSV and preserved the order in `272_Zkscan3.csv`, which contains only:

```text
Zkscan3
```

## Sources used

- Same-experiment DE statistics: `[local file: training_de_all_cell_groups.parquet]`.
- Same-endpoint training counts for `151 TH Prkcd Grin2c Glut`: `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
- Requested-target manifest: `[local file: 272_Zkscan3.csv]`.
- Distributed Agents same-experiment corpus, release `perturbai-july-260713-sourceguard-1773-v1`, queried with `target_context`, `inventory`, and the calibration summary. This release had no `Zkscan3` claims, findings, or explicit references, but it did have findings for autophagy/lysosome comparators such as `Atg5`, `Becn1`, `Ctsb`, `Lamp2`, and `Tsc2`.
- Distributed Agents run-local profile tooling, used to compare signed `logfoldchanges` in the focal cell group across candidate observed perturbations.
- NCBI Gene, queried 2026-09-23 through E-utilities. Mouse `Zkscan3` resolved to Gene ID `72739`, official symbol `Zkscan3`, aliases `Skz1`, `Zfp306`, `Zfp307`, and description "zinc finger with KRAB and SCAN domains 3".
- UniProtKB, queried 2026-09-23. Mouse ZKSCAN3 primary reviewed entry `Q91VW9` annotates KRAB, SCAN, and C2H2 zinc-finger domain signatures and GO terms for DNA-binding transcription-factor/repressor activity, lysosome organization, and negative regulation of autophagy.
- Literature:
  - Chauhan et al. 2013, *Molecular Cell*, DOI `10.1016/j.molcel.2013.01.024`, PMID `23434374`: ZKSCAN3 represses an autophagy/lysosome-biogenesis transcriptional network, and ZKSCAN3 silencing induced autophagy and lysosome biogenesis in cultured cells.
  - Park et al. 2025, *Autophagy*, DOI `10.1080/15548627.2025.2569965`, PMID `41037798`: CRISPR ablation of `ZKSCAN3` in Huntington disease animal and human iPSC-derived neuronal models increased autophagy/lysosomal function and lowered mutant HTT burden.

## Computational calibration

The training endpoint contains 1,674 observed perturbations. Its distribution in the focal class is very zero-inflated: 1,205/1,674 targets have `n_degs = 0`, 363 have 1-9 DEGs, 63 have 10-99, and 43 have at least 100.

I filtered the parquet to `group_name == "151 TH Prkcd Grin2c Glut"` for biologically chosen comparators and checked both scalar counts and signed expression patterns. The `151` block has 17,259 measured genes per queried perturbation. I used `pvals_adj < 0.05` as the same significance rule as the target endpoint, and I compared full signed `logfoldchanges` plus the top signed tails for a candidate cohort of SCAN/C2H2 zinc fingers and autophagy/lysosome regulators.

Key observed focal counts were:

| comparator | focal `n_degs` | reason for considering it |
|---|---:|---|
| `Zkscan1` | 0 | SCAN/KRAB/C2H2 family member, closest available same-nomenclature analog |
| `Zkscan16` | 0 | SCAN/KRAB/C2H2 family member |
| `Zscan26` | 0 | SCAN/C2H2 zinc-finger family member |
| `Zfp1` | 0 | broader C2H2 zinc-finger counterexample |
| `Zfp692` | 1 | broader C2H2 zinc-finger weak responder |
| `Zfp148` | 8 | broader zinc-finger transcription-factor weak responder |
| `Zfp236` | 19 | broader zinc-finger transcription-factor modest responder |
| `Zfp423` | 150 | active zinc-finger counterexample, not a KRAB/SCAN autophagy repressor |
| `Atg5` | 0 | core autophagy conjugation machinery |
| `Atg16l1` | 0 | ATG5-ATG12-ATG16L1 complex component |
| `Becn1` | 0 | autophagy initiation regulator |
| `Lamp2` | 0 | lysosomal membrane protein |
| `Ctsb` | 1 | lysosomal protease |
| `Sqstm1` | 1 | autophagy adaptor/p62 |
| `Mtor` | 2 | nutrient-sensing kinase upstream of TFEB/CLEAR and autophagy |
| `Ppp3ca` | 4 | calcineurin catalytic subunit; calcineurin can activate TFEB |
| `Ppp3r1` | 9 | calcineurin regulatory subunit |
| `Tsc2` | 86 | mTORC1 brake; strong mTORC1/SREBP/lysosomal counterexample |
| `Ppargc1a` | 0 | mitochondrial/lysosomal transcriptional co-regulator |

The three most direct SCAN-family comparators, `Zkscan1`, `Zkscan16`, and `Zscan26`, had zero FDR-significant genes. Their minimum adjusted p-values in the focal parquet were all 1.0 despite 180, 247, and 246 matched perturbed nuclei, respectively, so their largest signed fold changes were the familiar sparse-gene, nonsignificant extremes rather than a coherent tail of corrected hits. A profile comparison of these three with the broader candidate cohort likewise found no FDR-significant overlap with the nonzero `Zfp*` or autophagy regulators; for example, `Zkscan1`, `Zkscan16`, and `Zscan26` each had `significant_feature_count = 0` in the inspection table.

The broader zinc-finger family showed why family membership alone is insufficient. Most `Zfp*` training targets were null in this cell group: among 33 `Zfp`/`Zkscan`/`Zscan`-style targets detected by name, 25 had zero DEGs and two had exactly one. The high-count zinc-finger targets were specific regulators with other biology: `Zfp423` produced 150 DEGs and, in the Distributed Agents corpus, a thalamic subtype/neurotransmission and cell-surface program; `Zbtb7a` produced 841 DEGs. Those are proof that the assay can detect a zinc-finger transcription-factor perturbation when a relevant neuronal program moves, but they are poor mechanistic analogs for `Zkscan3`.

The autophagy/lysosome evidence also favored a zero or near-zero response. Direct perturbation of core autophagy or lysosomal components was flat in this exact cell group (`Atg5`, `Atg16l1`, `Becn1`, `Lamp2`, `Ppargc1a`) or one-gene weak (`Ctsb`, `Sqstm1`). The same-experiment Distributed Agents corpus calls `Atg5`, `Becn1`, `Ctsb`, and `Lamp2` negative or pathway-uncoupled in basal neuronal CRISPR: for example, `Ctsb:F002` reports failure to induce a canonical lysosomal/autophagy/CLEAR or generic stress response, and `Lamp2:F002` reports no corrected lysosome, macroautophagy, proteasome, UPR/ISR, or redox program. `Tsc2` is a real mTORC1/sterol/endolysosomal responder in the same experiment, but loss of a TSC complex brake hyperactivates mTORC1 and is not expected to phenocopy partial loss of a KRAB/SCAN transcriptional repressor.

## Target-specific prediction

### `Zkscan3`

`Zkscan3` is a DNA-binding KRAB/SCAN/C2H2 zinc-finger transcription factor. The external literature makes the nonzero case biologically plausible: Chauhan et al. showed that ZKSCAN3 can repress a broad autophagy and lysosome-biogenesis gene set, and Park et al. showed functional autophagy/lysosomal consequences of direct `ZKSCAN3` editing in Huntington disease neuronal systems.

I nevertheless predict no corrected DEGs in this basal mouse thalamic glutamatergic assay. The decision is driven mainly by the within-dataset calibration:

- the three available SCAN-family analogs, `Zkscan1`, `Zkscan16`, and `Zscan26`, are all exact zeroes in the focal endpoint;
- most other C2H2 zinc-finger factors in the training panel are zeroes or one-gene weak responders unless they have a known, distinct postnatal neuronal/chromatin program;
- the observed autophagy/lysosome branch that ZKSCAN3 is reported to repress is transcriptionally buffered in this dataset under basal postnatal neuronal conditions;
- the one stronger pathway counterexample, `Tsc2`, represents mTORC1 pathway activation and sits too far upstream to justify assigning a medium response to `Zkscan3`.

The held-out acute AAV-CRISPR perturbation is also expected to be partial; this screen averaged only about 18% target mRNA down-regulation per gRNA. A modest knockdown of `Zkscan3` in wild-type postmitotic neurons is therefore less likely to derepress the >60-gene stress/autophagy program seen after ZKSCAN3 silencing or disease-context CRISPR in published cell models.

Prediction: **0 DEGs**.

## Limits

- There is no measured `Zkscan3` perturbation signature in the parquet and no `Zkscan3` entry in the same-experiment Distributed Agents corpus, so the final scalar is an extrapolation from related genes.
- `Zkscan1`, `Zkscan16`, and `Zscan26` share SCAN/C2H2 domain architecture but are not guaranteed to bind the same loci or repress the same autophagy genes as ZKSCAN3.
- The public ZKSCAN3 literature is strongest in cultured cancer cells or Huntington disease models with deeper ablation or disease stress; that may overstate the effect expected after partial sparse CRISPR in healthy juvenile mouse neurons.
- The DEG count is an assay- and power-dependent FDR endpoint. A predicted zero means I do not expect any gene to pass this particular FDR cutoff in `151 TH Prkcd Grin2c Glut`, not that ZKSCAN3 is biologically inert.
