# Reasoning Trace

## Question

The manifest for this run contains one held-out perturbation, `Fzd3`. I interpreted the task as a point prediction of the number of measured genes with `pvals_adj < 0.05` after acute AAV-CRISPR loss of `Fzd3` in `151 TH Prkcd Grin2c Glut` neurons. I used the supplied training counts as the authoritative endpoint for non-held-out targets and the parquet rows as the expression-pattern evidence. I did not treat the corpus' occasional FDR < 0.10 summaries as endpoint counts; where a corpus card used the looser threshold, I rechecked the focal 5% FDR counts in the supplied files.

There are two relevant ambiguities that I resolved explicitly:

- The endpoint counts every measured transcript passing BH-adjusted Wilcoxon `pvals_adj < 0.05`, including self-transcripts if they pass. Mechanistically, though, a target's own mRNA fold change is only weak QC context in this assay, so I did not infer success or failure of `Fzd3` editing from expected `Fzd3` RNA loss.
- `Fzd3` was absent from both supplied inputs and absent from the selected Distributed Agents target context, so the prediction is extrapolation from measured Wnt/Frizzled/PCP perturbations rather than a lookup of an observed Fzd3 signature.

## Sources

- `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`
  - 1,674 focal-cell training endpoints.
  - Median `n_degs = 0`; 75th percentile `= 1`; 469/1,674 targets were positive; the high tail was dominated by broad essential regulators such as `Uba5`, `Tpr`, `Sin3a`, `Rnpc3`, `Zbtb7a`, spliceosome/proteasome/chromatin genes.
- `[local file: training_de_all_cell_groups.parquet]`
  - I extracted `151 TH Prkcd Grin2c Glut` rows for biologically relevant Wnt/Frizzled/PCP analogs and counted `pvals_adj < 0.05`.
  - The parquet is grouped by cell class; row-group metadata showed `151 TH Prkcd Grin2c Glut` at row groups 546-580, so the focused check was:

```python
pf = pyarrow.parquet.ParquetFile(training_parquet)
tbl = pf.read_row_groups(
    list(range(546, 581)),
    columns=["names", "logfoldchanges", "pvals_adj", "gene_target", "group_name"],
)
df = tbl.to_pandas()
df = df[
    df.group_name.eq("151 TH Prkcd Grin2c Glut")
    & df.gene_target.isin(wnt_pcp_targets)
]
```

- Selected Distributed Agents corpus release `perturbai-july-260713-sourceguard-1773-v1`
  - `Fzd3` had no target-scoped findings or claims.
  - I used the Wnt/Frizzled claims `claim:a8a38aa8426e4484d967`, `claim:d382bec180acf42c53fa`, `claim:91053558b1caee68fc9f`, `claim:cb8e8097cf4d28ac97a3`, and `claim:29928d1e672b55ba31dd` to identify same-experiment Wnt receptor and downstream comparator sets and to check whether the null Frizzled calls had already been falsified by signature-neighbor analysis.
- Public literature via NCBI PubMed/BioEval literature:
  - Wang et al. 2002, Journal of Neuroscience, PMID 12351730, DOI 10.1523/JNEUROSCI.22-19-08563.2002: germline mouse `Fz3` deletion disrupts the thalamocortical, corticothalamic, nigrostriatal, and anterior commissure tracts.
  - Hua et al. 2014, PNAS, PMID 24799694, DOI 10.1073/pnas.1406399111: conditional mouse deletion showed that proper corticothalamic and thalamocortical routing requires early `Fz3` function and that the affected tract pattern resembles `Celsr3`.
  - Hua et al. 2014, Development, PMID 25294940, DOI 10.1242/dev.110189: `Fz3` and `Fz6` are partially interchangeable in mammalian tissue-polarity signaling; `Fz6` partly rescued `Fz3` axon growth/guidance defects, supporting `Fzd6` as the closest measured Frizzled comparator.
  - Onishi et al. 2020, PNAS, PMID 32641508, DOI 10.1073/pnas.1921878117: LRRK1/2 regulate axon guidance through Frizzled3 phosphorylation and growth-cone communication, reinforcing that important FZD3 biology can be post-translational and morphologic rather than a durable cell-body nuclear-RNA state.

## Within-dataset analogs

I treated measured Wnt receptors and PCP-associated genes as the direct analog set, and downstream beta-catenin/TCF perturbations as positive controls for Wnt transcriptional detectability in the same focal neurons.

`Fzd2`, `Fzd4`, `Fzd6`, and `Fzd9` were the most literal receptor-family comparators. All four had `n_degs = 0` in the focal 5% FDR training file. Their focal top adjusted p-values were not borderline signals except for weak nonshared noise (`Fzd9` top q = 0.357; `Fzd6` top q = 0.875; `Fzd2` and `Fzd4` top q = 1.0), and canonical Wnt feedback genes were not significant after these perturbations. In the Distributed Agents corpus, `Fzd2:F003`, `Fzd6:F003`, and `Fzd9:F003` anchor the same result at the screen level: represented single-Frizzled perturbations shared a lack of downstream neuronal FDR support and did not form a hidden Wnt/PCP mRNA module. `Fzd6` is the best paralogous counterfactual for `Fzd3` because of the Fz3/Fz6 partial rescue data above, and it was a complete transcriptional null in every recovered neuronal group in the internal corpus.

`Lrp6`, `Lrp5`, `Ctnnb1`, `Tcf7l2`, `Gsk3b`, and `Csnk2b` bounded the canonical Wnt branch. The 5% FDR counts in the focal endpoint were:

| target | focal `n_degs` |
| --- | ---: |
| `Lrp5` | 0 |
| `Lrp6` | 4 |
| `Ctnnb1` | 383 |
| `Tcf7l2` | 106 |
| `Gsk3b` | 6 |
| `Csnk2b` | 25 |

`Ctnnb1` loss strongly down-regulated canonical feedback/readout transcripts such as `Axin2`, `Lef1`, `Notum`, `Wnt9b`, and `Vangl1`; `Tcf7l2` gave a smaller but still clear 106-gene focal response. `Lrp6` was the only upstream receptor/co-receptor that touched this branch at 5% FDR, and even it had only four genes (`Chgb`, `Nrbp2`, `Nsmf`, `Atrnl1`) while `Axin2` was just below the threshold at q = 0.073. The Distributed Agents Ctnnb1/Lrp6 claims conclude that the detectable 151 thalamic Wnt/catenin state links `Lrp6` with `Ctnnb1/Tcf7l2` rather than broadly extending to `Lrp5`, single Frizzleds, ROR/RYK receptors, `Lgr4`, or catenin scaffolds. That makes a `Ctnnb1`-sized prediction for `Fzd3` biologically inappropriate.

The noncanonical/PCP receptor layer also favored zero. `Ror1`, `Ror2`, `Ryk`, `Prickle1`, `Kremen1`, `Macf1`, `Antxr1`, `Antxr2`, `Lrp4`, `Eda`, and `Zic2` each had `n_degs = 0` in the focal 5% FDR file. `Celsr2` and `Peg3` each had one significant gene, but in both cases the hit was the perturbed gene itself (`Celsr2` or `Peg3`), not a downstream Wnt/PCP module. The Distributed Agents Wnt receptor-layer claim explicitly notes that obvious unmeasured tests such as `Fzd3`, `Vangl1/2`, `Celsr3`, and `Dvl1/2/3` were absent, but the represented receptor perturbations were flat, sparse, or nonconvergent.

## Target-specific prediction

### `Fzd3`

Public mouse genetics establishes `Fzd3` as a real axon-guidance and planar-cell-polarity receptor: germline and conditional loss perturb forebrain axon tracts, including thalamocortical/corticothalamic routing, and the phenotype overlaps `Celsr3`. That prior makes `Fzd3` more neurodevelopmentally relevant than `Fzd4` or `Fzd9`.

The same prior does not, however, imply a broad RNA signature after this perturbation. The strongest `Fzd3` requirements in the literature are embryonic wiring events beginning around E11.5, whereas the experiment edited sparse, postmitotic, postnatal NeuN+ neurons at P16 and measured survivor nuclear RNA at P37-P44. FZD3 also signals through PCP/growth-cone polarity, intercellular Vangl interactions, and phosphorylation-dependent localization, so a correct protein-level or morphologic effect could be invisible to a cell-body snRNA-seq Wilcoxon test.

In the training data, every measured single Frizzled receptor in the focal group was exactly zero at FDR < 0.05 (`Fzd2 = 0`, `Fzd4 = 0`, `Fzd6 = 0`, `Fzd9 = 0`). The closest functional analog, `Fzd6`, was also a corpus-wide negative transcriptional control despite its known tissue-polarity roles. The assay could detect Wnt transcription where the intracellular effector branch was rate-limiting (`Ctnnb1 = 383`, `Tcf7l2 = 106`), but that branch was not engaged by the Frizzled or ROR/RYK receptor-level perturbations. Even `Lrp6`, the upstream node that did converge with `Ctnnb1`, produced only four genes at the requested 5% FDR.

I therefore predict no FDR-significant genes for `Fzd3` in `151 TH Prkcd Grin2c Glut`: `predicted_n_degs = 0`.

## Limits

- `Fzd3` itself was held out, so there was no `Fzd3` self-transcript, DEG burden, or all-gene score vector to inspect.
- The strongest developmental partners of FZD3/PCP signaling were incompletely sampled. `Celsr3`, `Vangl1`, `Vangl2`, `Dvl1`, `Dvl2`, `Dvl3`, several Wnt ligands, and `Fzd5/Fzd7` were missing from the training target set.
- The observed zeroes for `Fzd2/Fzd4/Fzd6/Fzd9` are powerful receptor-layer evidence but imperfect analogs: `Fzd3` has a much stronger CNS axon-tract phenotype than several of them.
- A one-gene result caused solely by detectable target-transcript depletion is plausible for any CRISPR target in this endpoint. The closest Frizzled perturbations did not show that at 5% FDR, so I did not add a self-hit to the point prediction.
- The endpoint is power- and survivor-conditioned. A real effect on axon maintenance, synapse location, planar polarity, or neighboring cells would not necessarily yield a durable nuclear RNA signature in recovered thalamic neuronal nuclei.
