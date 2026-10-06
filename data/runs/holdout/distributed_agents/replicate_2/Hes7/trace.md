# Question

Predict `n_degs` for the held-out target list in
`151 TH Prkcd Grin2c Glut` cells, where `n_degs` is the count of measured genes
with Benjamini-Hochberg adjusted Wilcoxon `pvals_adj < 0.05` after an acute
AAV CRISPR loss-of-function perturbation. The manifest for this run contains one
target, `Hes7`, and `Hes7` is absent from both the training DEG-count table and
the training DE parquet as a perturbation target.

I treated large log fold changes on genes with `pvals_adj = 1` as low-expression
pseudocount artifacts unless the Wilcoxon score also supported a change. Target
self-RNA was not used as a measure of editing.

# Sources

- Same-experiment raw DE table:
  `[local file: training_de_all_cell_groups.parquet]`.
- Focal-cell training endpoint:
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
- Requested-target manifest:
  `[local file: 104_Hes7.csv]`.
- Internal same-experiment semantic layer: Distributed Agents PerturbAI corpus release
  `perturbai-july-260713-sourceguard-1773-v1`.
- Internal observed-profile layer: Distributed Agents runtime profile comparison over
  `logfoldchanges` in `151 TH Prkcd Grin2c Glut`, using `pvals_adj < 0.05` as
  the activity threshold.
- External literature was retrieved from NCBI PubMed.

# Dataset Work

The requested manifest was:

```tsv
target_name
Hes7
```

The focal training table has 1,674 non-held-out perturbations. It is heavily
zero-inflated in this endpoint: 1,205/1,674 targets have zero DEGs, the median
is 0, the 75th percentile is 1, the 90th percentile is 2, and the top tail is
large, with a maximum of 2,677.

I queried the 616M-row parquet with DuckDB, restricted to:

```sql
WHERE group_name = '151 TH Prkcd Grin2c Glut'
  AND gene_target IN (<candidate analogs>)
  AND (pvals_adj < 0.05 OR names IN (<canonical Notch/HES outputs>))
```

The canonical genes `Hes1`, `Hes5`, `Hes7`, `Hey1`, `Hey2`, `Heyl`, `Dtx1`,
`Lfng`, `Mesp2`, and `Tbx6` were present in the DE table, so failures to move
them are measured negatives rather than missing features.

The candidate set and focal-cell DEG counts were:

| training perturbation | focal `n_degs` | expression evidence in `151 TH Prkcd Grin2c Glut` |
|---|---:|---|
| `Adam10` | 0 | Core Notch protease comparator. `Hes1`, `Hes5`, `Hes7`, `Hey1`, `Hey2`, `Heyl`, `Dtx1`, `Lfng`, `Dll1`, `Maml1`, `Rbpj`, `Ascl1`, `Neurog2`, `Neurod1`, and `Neurod2` all had `pvals_adj = 1`. |
| `Dll1` | 0 | Notch ligand. Same HES/HEY/RBPJ output genes all had `pvals_adj = 1`. |
| `Notch1` | 0 | Canonical receptor. Same output genes all had `pvals_adj = 1`. |
| `Notch2` | 0 | Canonical receptor. Same output genes all had `pvals_adj = 1`; the corpus also annotates a whole-surface neuronal null for `Notch2` and reports that `Hes1`, `Hes5`, `Hey1`, `Hey2`, `Heyl`, `Dtx1`, `Rbpj`, `Maml1`, `Ascl1`, `Neurog2`, `Neurod1`, and `Neurod2` all had FDR 1.0 in the full `Notch2` surface. |
| `Notch4` | 0 | Notch receptor. Same output genes all had `pvals_adj = 1`; the corpus reports that the sparse `Notch4` singleton responses elsewhere were uncoupled from a HES/HEY Notch program. |
| `Psen1` | 0 | Gamma-secretase/Notch cleavage comparator. Same output genes all had `pvals_adj = 1`; the corpus reports no FDR-supported downstream response in any recovered neuronal group. |
| `Fgfr1` | 0 | FGF input into the embryonic segmentation clock. The same HES/HEY/Notch-output genes all had `pvals_adj = 1`. |
| `Tbx6` | 0 | Presomitic-mesoderm activator of the `Hes7` enhancer. The same output genes all had `pvals_adj = 1`. |
| `Mesp2` | 1 | Direct somitogenesis neighbor downstream of the segmentation clock. Only `Arih2` passed FDR 0.05 in the focal group; canonical HES/HEY/Notch-output genes had `pvals_adj = 1`. |
| `Atoh1` | 0 | Neural bHLH developmental comparator. No focal response and no canonical HES/HEY/Notch-output movement. |
| `Mib1` | 27 | Notch-ligand E3 ligase, but its focal positive genes were sterol/cholesterol genes such as `Insig1`, `Fdft1`, `Dhcr24`, `Ldlr`, `Msmo1`, `Hmgcs1`, `Hmgcr`, `Cyp51`, and `Lss`; HES/HEY/RBPJ/Neurod outputs were all `pvals_adj = 1`. The corpus explicitly annotates the `Mib1` sterol response as uncoupled from canonical Notch transcription. |
| `Nr1d1` | 116 | Circadian nuclear receptor comparator checked because CLOCK/BMAL1 can interfere with embryonic `Hes7` oscillation in PSM organoids. Its top focal DEGs included `Erc2`, `Pdgfa`, `Tspan14`, `Cacna2d3`, `Pdzd2`, `Rasl11b`, and `Npas2`, not a Notch/HES module, so this was rejected as a mature-neuron circadian state rather than a `Hes7` analog. |
| `Nr1d2` | 1 | Same circadian counterexample class; not a presomitic `Hes7` analog. |
| `Clock` | 3 | Same circadian counterexample class; not a presomitic `Hes7` analog. |
| `Hesx1` | 0 | Name-neighbor only. `Hesx1` is a paired-like homeobox factor rather than a Hairy/enhancer-of-split bHLH repressor, so I used it only as a weak boundary. |

The Distributed Agents runtime profile comparison over these 14 measured candidate
profiles found no tight FDR-supported module: 10/14 profiles had no significant
features, the only 10-to-49 DEG member was `Mib1`, and the Notch/developmental
set shared essentially no significant-program overlap.

# Target-Specific Reasoning

## Hes7

`Hes7` is a bHLH-Orange transcriptional repressor and core segmentation-clock
component in the presomitic mesoderm, where delayed negative feedback by unstable
Hes7 protein periodically represses `Hes7` itself and `Lfng` to drive somite
timing (Bessho et al. 2003, PMID 12783854, DOI 10.1101/gad.1092303). Its
presomitic enhancer is activated by an E-box/T-box/RBPJ region integrating
mesogenin1, `Tbx6`, and Notch inputs and is repressed by Hes7 feedback
(Hayashi et al. 2018, PMID 29895619, DOI 10.1074/jbc.RA118.003728). FGF
signaling maintains Hes7 levels and proper oscillation in that embryonic
mesodermal circuit (Anderson et al. 2020, PMID 33210601, DOI
10.7554/eLife.55608). Human HES7 loss-of-function mutations cause
spondylocostal dysostosis, reinforcing the somitogenesis/Notch-pathway role
rather than a postnatal neuronal role (Sparrow et al. 2008, PMID 18775957, DOI
10.1093/hmg/ddn272).

Within the training data, the best same-pathway candidates were therefore
`Adam10`, `Dll1`, `Notch1`, `Notch2`, `Notch4`, and `Psen1`, all of which had
0 DEGs in the focal thalamic glutamatergic cell group. Their measured canonical
Notch outputs also stayed flat at FDR 1.0, including HES/HEY genes, `Dtx1`,
`Rbpj`, `Maml1`, `Ascl1`, and `Neurog2`. The closer embryonic segmentation
neighbors that happened to be assayed were likewise null or almost null in this
cell group: `Tbx6` and `Fgfr1` had 0 DEGs, and `Mesp2` had a single DEG
unconnected to the HES/Notch program.

I rejected `Mib1` as a quantitative analog despite its membership in Notch
ligand endocytosis because both the focal parquet and the same-experiment corpus
show that `Mib1` drove a sterol/SREBF2-like response, not HES/HEY or RBPJ output.
I also rejected circadian perturbations such as `Nr1d1` and `Clock`: they are
transcriptionally active in mature neurons, but the literature link is an
experimental interaction with the embryonic segmentation oscillator, not shared
postnatal thalamic `Hes7` biology.

Combining those observations, the assay-calibrated prior for an acute `Hes7`
perturbation in P37 recovered thalamic glutamatergic neurons is a null response.
The point prediction is:

```tsv
target_name	predicted_n_degs
Hes7	0
```

# Limits

- There is no direct `Hes7` perturbation signature in the training data or in the
  selected Distributed Agents corpus release.
- The training set lacked true HES bHLH paralogs such as `Hes1`, `Hes5`, `Hey1`,
  and `Hey2` as perturbation targets, so the closest measured perturbations were
  upstream receptors/ligands/proteases and embryonic PSM regulators.
- Some canonical output genes showed large absolute log fold changes with
  `pvals_adj = 1`; I treated those as low-expression artifacts, not as directional
  biological evidence.
- A rare one-DEG outcome like `Mesp2` is plausible in a noisy, sparse assay.
  However, the nearest measured Notch/segmentation perturbations concentrate at
  zero, so the integer point prediction is zero rather than one.
