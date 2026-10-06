# Tfap2a prediction trace

## Question interpreted

The held-out manifest for this run contains one requested perturbation:

| target_name |
| --- |
| Tfap2a |

For that target I predicted the number of genes that would pass `pvals_adj < 0.05` in the focal cell group, `151 TH Prkcd Grin2c Glut`, after sparse P16 AAV-CRISPR loss of function and P37-P44 snRNA-seq. I treated the endpoint as an assay-calibrated response breadth, not as a direct measure of editing efficiency, target-gene essentiality, or developmental importance.

There is no row for `Tfap2a` in the focal training-count CSV, and the held-out design states that its per-gene DE signature is absent from the parquet, so every estimate below is transfer from non-held-out genes.

## Sources

Internal data and corpus:

- `[local file: training_de_all_cell_groups.parquet]`
- `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`
- `[local file: 236_Tfap2a.csv]`
- Distributed Agents corpus MCP, release `perturbai-july-260713-sourceguard-1773-v1`, especially target-centered and claim-level summaries for `Tfap4`, `Tcf12`, retinoid/RAR/RXR perturbations, Wnt/beta-catenin perturbations, and midbrain-dopaminergic developmental regulator perturbations.

External literature:

- Hilger-Eversheim et al. 2000, review of AP-2 transcription-factor functions in vertebrate development, apoptosis, and cell-cycle control; DOI `10.1016/s0378-1119(00)00454-6`; PMID `11137286`.
- Brewer et al. 2004, neural-crest-specific `Tcfap2a` deletion in mouse showing that AP-2alpha directs several neural-crest developmental outputs; DOI `10.1016/j.ydbio.2003.10.039`; PMID `14975722`.
- Brewer et al. 2002, AP-2alpha requirement for mouse cardiac outflow-tract morphogenesis; DOI `10.1016/s0925-4773(01)00579-2`; PMID `11744375`.
- Zhao et al. 2001 and Feng and Williams 2003 for AP-2delta/AP-2epsilon cloning and the shared AP-2 DNA-binding/dimerization family architecture; DOIs `10.1074/jbc.M106284200` and `10.1016/s1044-7431(03)00209-4`; PMIDs `11522791` and `14572467`.

## Dataset computations

I used the focal training-count table to calibrate the breadth endpoint and the parquet to verify candidate analog signatures in the same cell group. The focal training table contains 1,674 assayed non-held-out perturbations:

| quantity | value |
| --- | ---: |
| zero-DEG perturbations | 1,205 |
| nonzero perturbations | 469 |
| median `n_degs` | 0 |
| 75th percentile | 1 |
| 90th percentile | 2 |
| 95th percentile | 18 |
| 99th percentile | 436.5 |
| maximum | 2,677 |

The parquet is row-grouped by `group_name`, so exact focal summaries were computed by scanning only `group_name = '151 TH Prkcd Grin2c Glut'` and aggregating per `gene_target`:

```sql
SELECT
  gene_target,
  count(*) FILTER (WHERE pvals_adj < 0.05) AS n_degs,
  min(pvals_adj) AS min_padj,
  max(abs(scores)) AS max_abs_score,
  avg(n_pert_matched) AS n_pert,
  avg(n_ctrl_matched) AS n_ctrl
FROM parquet_scan('training_de_all_cell_groups.parquet')
WHERE group_name = '151 TH Prkcd Grin2c Glut'
  AND gene_target IN (...)
GROUP BY gene_target;
```

Direct AP-2 paralogs were the largest missing within-dataset comparator: `Tfap2b`, `Tfap2c`, `Tfap2d`, and `Tfap2e` were not non-held-out perturbation targets in the focal CSV. The only `Tfap*` target present was `Tfap4`, which is AP4, a bHLH-LZ factor and not an AP-2 paralog.

## Target-specific reasoning

### Tfap2a

`Tfap2a` encodes AP-2alpha, a sequence-specific AP-2-family transcription factor with a shared AP-2 DNA-binding/dimerization domain. Mouse and zebrafish loss-of-function studies place AP-2alpha in embryonic neural crest, craniofacial, outflow-tract, ectodermal, pigment, and sensory-organ development. Those data make `Tfap2a` biologically important, but they do not by themselves imply that postmitotic juvenile thalamic glutamatergic neurons remain dependent on AP-2alpha for a broad nuclear-RNA maintenance program.

The same-assay perturbations I considered were:

| comparison set | training targets in `151 TH Prkcd Grin2c Glut` | observed `n_degs` | how I used them |
| --- | --- | ---: | --- |
| AP4 / E-protein / proneural developmental TF neighborhood | `Tfap4`, `Tcf3`, `Tcf4`, `Tcf12`, `Atoh1`, `Neurod1`, `Neurod2`, `Ptf1a` | all `0` | These are not AP-2 paralogs, but they test the broader idea that developmental DNA-binding factors re-engage large acute programs after P16 neuronal CRISPR. They did not. In the parquet, `Tfap4`, `Tcf12`, `Tcf4`, `Atoh1`, `Neurod1`, `Neurod2`, and `Ptf1a` all had zero FDR<0.05 genes in the focal group; `Tfap4`, `Tcf12`, `Tcf4`, `Atoh1`, and `Neurod1` had `min_padj = 1.0`. The Distributed Agents corpus also reports that `Tfap4` had no FDR<0.10 downstream genes in any of 23 postnatal NeuN+ neuronal groups and that `Tcf12` was pan-neuronal-null across its measured groups. |
| Retinoid/RAR/RXR axis | `Rarb`, `Rarg`, `Rxra`, `Rxrb`, `Rxrg` | all `0` | AP-2alpha participates in embryonic regulatory networks that intersect retinoid patterning, so I checked whether the represented retinoic-acid nuclear receptors gave a basal thalamic response. They did not. This agrees with the Distributed Agents claim that represented retinoid/RAR/RXR and lipid nuclear-receptor single-gene perturbations are flat, singleton, sparse, or nonconvergent rather than a shared acute postmitotic-neuronal receptor module. |
| Other neuronal developmental identity regulators | `Pitx3`, `Lmx1b`, `Nr4a1`, `Nr4a3` | all `0` | AP-2 factors have published developmental expression in neural tissues, and there are late catecholaminergic reports, but the focal group is thalamic glutamatergic, not the `215 MB Dopa` class. In the focal group, the tested dopaminergic and NR4A-family developmental or activity-regulated TFs were flat. The corpus similarly reports that represented midbrain dopaminergic developmental regulators did not form a shared acute postnatal dopamine-identity mRNA module, and that single `Nr4a1` or `Nr4a3` loss is largely buffered at baseline. |
| Canonical Wnt/beta-catenin counterexamples | `Ctnnb1`, `Tcf7l2`, `Lrp6`, `Gsk3b` versus `Fzd2`, `Fzd4`, `Fzd6`, `Fzd9`, `Lrp5`, `Ror1`, `Ror2`, `Ryk`, `Macf1`, `Kremen1`, `Zic2`, `Peg3`, `Antxr1` | `Ctnnb1 = 383`, `Tcf7l2 = 106`, `Lrp6 = 4`, `Gsk3b = 6`; most receptor-adjacent genes `0` | This was the main positive counterexample. The assay can detect a thalamic Wnt/TCF-like state after direct `Ctnnb1` and `Tcf7l2` perturbation, including a significant `Lef1` change after `Ctnnb1` loss. However, even within Wnt biology the response is selective: single Frizzleds, `Lrp5`, `Ror1`, `Ror2`, `Ryk`, `Macf1`, `Kremen1`, and `Zic2` were zero in the focal count table. Thus embryonic Wnt/AP-2 developmental proximity is too indirect to map `Tfap2a` to the broad `Ctnnb1` or `Tcf7l2` response. |

These comparisons put `Tfap2a` closest to a set of developmental transcription factors and retinoid receptors that are silent in the postnatal focal neurons, rather than to the broad chromatin, stress, proteostasis, or Ctnnb1/Tcf7l2 branches that yield hundreds of focal DEGs. Because the training distribution itself is heavily zero-inflated and the direct mechanistic analogs available in the dataset have zero FDR<0.05 genes, I predict no detected downstream DEGs for `Tfap2a` in `151 TH Prkcd Grin2c Glut`.

Final point prediction: `Tfap2a -> 0`.

## Limits

The closest missing evidence is a same-assay AP-2 paralog: none of `Tfap2b`, `Tfap2c`, `Tfap2d`, or `Tfap2e` was a training perturbation. `Tfap4` shares a name prefix but is mechanistically AP4/bHLH-LZ, so it is only a broad developmental-TF negative analog, not a paralog control.

The public `Tfap2a` literature is dominated by germline, embryonic, lineage-specific, or non-neuronal contexts. Those studies support a strong developmental AP-2alpha role, especially in neural crest and craniofacial lineages, but extrapolation to sparse acute P16 loss in surviving NeuN+ thalamic neurons is weak.

The parquet does not provide raw basal `Tfap2a` expression or AP-2alpha chromatin occupancy in the focal cells. A prediction of zero means no gene is expected to pass the Wilcoxon BH FDR threshold in this assay; it does not exclude sub-FDR expression shifts, protein-level effects, altered physiology, or a response in olfactory bulb, hindbrain, neural crest derivatives, or other unsampled cell classes.

