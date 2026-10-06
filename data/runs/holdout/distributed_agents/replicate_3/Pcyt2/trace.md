# Question and resolved ambiguities

The requested held-out perturbation for this run was `Pcyt2`. I interpreted
`n_degs` as the number of measured genes in `151 TH Prkcd Grin2c Glut` nuclei
with Scanpy Wilcoxon Benjamini-Hochberg adjusted `pvals_adj < 0.05`, using the
same focal-cell endpoint reported in
`151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.

`Pcyt2` was absent from both supplied training tables, so I did not try to use a
Pcyt2 expression vector. The prediction below transfers from same-assay training
perturbations and from the known CDP-ethanolamine/Kennedy-pathway position of
PCYT2.

# Sources used

- Differential-expression parquet:
  `[local file: training_de_all_cell_groups.parquet]`.
  I filtered it to `group_name == "151 TH Prkcd Grin2c Glut"` and inspected
  focal-cell log2 fold changes, adjusted P values, and matched nucleus counts
  for lipid and sterol perturbations.
- Focal training counts:
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
  This gave the calibrated endpoint for 1,674 non-held-out perturbations.
- Requested-target manifest:
  `[local file: 169_Pcyt2.csv]`.
- Distributed Agents corpus MCP, release
  `perturbai-july-260713-sourceguard-1773-v1`. `target_context(Pcyt2)` had no
  direct Pcyt2-centered claims, but `target_context(Selenoi)` and claim search
  contained same-experiment summaries around the SELENOI sterol response,
  SREBF2 directionality, and ether-lipid/sterol counterexamples.
- Distributed Agents runtime profile comparison. I compared `Selenoi`, sterol-feedback
  genes, and lipid-metabolism counterexamples with
  `profile_compare(..., context={"group_name":"151 TH Prkcd Grin2c Glut"})`,
  using `gene_target` as the entity, `names` as the feature, `logfoldchanges`
  as the signed value, and `pvals_adj < 0.05` as the significance flag.
- PubMed literature:
  Horibata and Hirabayashi 2006, DOI `10.1194/jlr.C600019-JLR200`,
  PMID 17132865; Fullerton et al. 2007, DOI `10.1128/MCB.01527-06`,
  PMID 17325045; Bakovic et al. 2007, DOI `10.1139/o07-006`,
  PMID 17612623; Ahmed et al. 2017, DOI `10.1093/brain/aww318`,
  PMID 28052917; Vaz et al. 2019, DOI `10.1093/brain/awz291`,
  PMID 31637422; Nunes et al. 2022, DOI `10.1016/j.abb.2022.109376`,
  PMID 36007576.

# Same-assay calibration

The focal-cell endpoint is sparse. Among the 1,674 training perturbations,
1,205 had 0 DEGs, 276 had exactly 1 DEG, 65 had 2 to 5, and only 78 had more
than 20. The median was 0, the mean was 14.05 because a small number of broad
stress/regulatory perturbations had hundreds of DEGs, and the 95th percentile
was only 18.

For the parquet calculations I selected only the focal cell group and then
looked up lipid-metabolism genes present in the training target universe:

```sql
SELECT gene_target, names, logfoldchanges, pvals_adj,
       n_pert_matched, n_ctrl_matched
FROM training_de_all_cell_groups
WHERE group_name = '151 TH Prkcd Grin2c Glut'
  AND gene_target IN (...)
ORDER BY gene_target, pvals_adj ASC, abs(logfoldchanges) DESC;
```

I also compared the selected cohort with the Distributed Agents runtime profile tools to
ask whether their signed expression tails were similar. Those profile metrics
were used only as diagnostics, because no `Pcyt2` expression profile is
available.

# Pcyt2 reasoning

## Directly related training perturbations

`Selenoi` is the closest measured analog. PCYT2 converts phosphoethanolamine to
CDP-ethanolamine, the committed cytidylyltransferase step of the
CDP-ethanolamine Kennedy branch that supplies phosphatidylethanolamine and
plasmalogen precursors (Bakovic et al. 2007). SELENOI/EPT1 is a downstream
CDP-ethanolamine:diacylglycerol ethanolaminephosphotransferase that consumes
CDP-ethanolamine to make PE in the same branch; it is CDP-ethanolamine specific
and expressed in brain (Horibata and Hirabayashi 2006), and SELENOI loss has
human and mouse CNS phenotypes through PE/plasmenyl-PE deficiency (Ahmed et al.
2017; Nunes et al. 2022).

In the focal cell group, `Selenoi` had `n_degs = 5` with 172 matched perturbed
nuclei. Its five FDR-significant genes were:

| Perturbation | DEG count | Significant features |
| --- | ---: | --- |
| `Selenoi` | 5 | `Insig1` up, `Msmo1` up, `Selenoi` down, `Fdft1` up, `Nos1ap` down |

Distributed Agents corpus finding `Selenoi:F001` summarizes this as a compact sterol
feedback signature in `151 TH Prkcd Grin2c Glut`; `Selenoi:F002` notes that
`Mib1`, `Dctn1`, `Marchf6`, and `Rab7` re-induced the same sterol genes in the
dataset; and `Selenoi:F005` reports that the SELENOI response lacked a broader
UPR, ISR, autophagy/lysosome, or redox tail. Those points argue that a
Kennedy-branch hit is visible in this assay, but only as a small lipid-feedback
state rather than a large pan-stress response.

## Directional and negative counterexamples

The Selenoi sterol genes are in the SREBF2 cholesterol-biosynthesis regulon:
`Srebf2` itself had `n_degs = 7` in the focal cell group, down-regulating
`Srebf2`, `Dhcr24`, `Insig1`, `Hmgcs1`, `Msmo1`, `Cyp51`, and `Sqle`. That is
the opposite direction from SELENOI loss for `Insig1` and `Msmo1`, matching
Distributed Agents corpus findings `Selenoi:F003` and claim
`claim:1aaa975607fdcf65be70`. I therefore used `Srebf2` to verify the axis, not
as a positive analog for the direction of Pcyt2 loss.

Broader lipid targets were mostly flat or nearly flat in the same endpoint:

| Perturbation | Focal `n_degs` | Interpretation for Pcyt2 |
| --- | ---: | --- |
| `Agps` | 1 | Plasmalogen synthesis neighbor with only a small `Dhcr24` response; supports weak lipid feedback rather than a large ether-lipid program. |
| `Far1` | 2 | Peroxisomal ether-lipid entry enzyme; did not phenocopy `Selenoi`. |
| `Hmgcr` | 0 | Direct sterol enzyme; flat despite SREBF2-module readability. |
| `Srebf1` | 0 | Lipogenic SREBP paralog; flat, so the cholesterol signal is not generic SREBP/lipid perturbation. |
| `Sptlc2` | 1 | Sphingolipid de novo synthesis; essentially self-transcript only. |
| `Tecr` | 1 | Fatty-acid elongation/reduction; essentially self-transcript only. |
| `Abhd12` | 1 | Lipid hydrolase; self-transcript only. |
| `Acsl4` | 1 | Fatty-acyl-CoA ligase; self-transcript only. |
| `Bscl2` | 2 | ER lipid-droplet/lipid-metabolism protein; only two DEGs. |
| `Pld3` | 1 | PLD-family lysosomal nuclease; self-transcript only and not a Kennedy-pathway analog. |
| `Pi4kb` | 1 | Phosphoinositide kinase; not a PE-biosynthesis analog. |

These counterexamples keep the Pcyt2 estimate close to SELENOI's five-gene
scale. The runtime profile comparison similarly showed no coherent, high-DEG
lipid cohort surrounding `Selenoi`: the SELENOI significant set did not overlap
significantly with the formal significant sets of `Agps`, `Far1`, `Hmgcr`,
`Sptlc2`, `Tecr`, `Acsl4`, or `Pld3`, even when whole-profile correlations were
positive because most genes are near-null in the same direction.

## Zero vs nonzero call

PCYT2 is a nonredundant enzyme for the CDP-ethanolamine branch in animals and
complete mouse `Pcyt2` deletion is embryonic lethal, whereas heterozygotes
retain partial PE synthesis and maintain total phospholipid content (Fullerton
et al. 2007; Bakovic et al. 2007). Human hypomorphic `PCYT2` variants perturb
ether-lipid biosynthesis and cause complex hereditary spastic paraplegia with
developmental delay, epilepsy, and progressive cerebral/cerebellar atrophy
(Vaz et al. 2019). Those data say that loss of PCYT2 can matter to nervous
system lipid homeostasis, but they do not imply that a 3 to 4 week partial
CRISPR knockdown in a sparse postmitotic neuronal population should create a
broad nuclear RNA phenotype.

The exact same-assay downstream analog, `Selenoi`, is the decisive nonzero
evidence. It shows that the focal thalamic neurons can register a
CDP-ethanolamine terminal-step perturbation as a few DEGs, specifically
sterol-homeostasis genes plus the target transcript. At the same time, direct
sterol genes and neighboring ether-lipid enzymes were flat to very weak, so I
do not extrapolate to tens of DEGs.

My point estimate for `Pcyt2` is therefore **5 DEGs**: nonzero, on the same
order as the SELENOI Kennedy-branch signature, with enough room for PCYT2's
upstream/nonredundant step to match SELENOI rather than collapse to the
single-self-DEG pattern.

# Limits

- There is no Pcyt2-centered Distributed Agents corpus neighborhood and no held-out
  Pcyt2 expression profile in the input parquet, so the prediction is an
  extrapolation from `Selenoi`.
- `Selenoi` is downstream of PCYT2 but is not the same enzyme: CEPT1 can also
  transfer phosphoethanolamine to DAG, and PCYT2 affects the CDP-ethanolamine
  pool upstream of both PE and plasmalogen terminal reactions.
- The published PCYT2 and SELENOI disease/knockout phenotypes are germline or
  strong tissue-specific losses, whereas the experiment used acute AAV CRISPR
  with modest average target-RNA depletion in juvenile postmitotic neurons.
- Lipids, PE abundance, plasmalogens, and SREBP2 activity were not measured in
  the input; the sterol module is inferred from nuclear mRNA only.
- Most lipid-metabolism perturbations in training were very sparse in this
  assay. A prediction of 5 rather than 0 is driven mainly by the exact
  CDP-ethanolamine analog `Selenoi`, not by a broad family-wide rule.
