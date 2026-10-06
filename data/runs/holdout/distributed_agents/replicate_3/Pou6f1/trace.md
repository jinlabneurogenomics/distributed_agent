# Pou6f1 DEG-count prediction

## Question and resolved ambiguities

The held-out manifest for this run contains a single requested target:

```tsv
target_name
Pou6f1
```

I interpreted `predicted_n_degs` as the held-out endpoint for acute AAV CRISPR loss of `Pou6f1` in `151 TH Prkcd Grin2c Glut`: the integer count of measured genes with Wilcoxon Benjamini-Hochberg `pvals_adj < 0.05` in this focal cell group. I used the count CSV as the calibrated endpoint and the parquet as the expression-signature evidence. The Distributed Agents corpus sometimes summarizes target behavior at FDR 0.10 across cell groups; I used those summaries qualitatively, while keeping the final count on the required FDR 0.05 endpoint.

## Sources used

Internal experiment:

- `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`
- `[local file: training_de_all_cell_groups.parquet]`

Local corpus and runtime tools:

- Distributed Agents corpus release `perturbai-july-260713-sourceguard-1773-v1`
- Distributed Agents runtime profile comparison over focal-cell log fold-change vectors for the represented POU-family perturbations

External biological evidence:

- NCBI Gene for mouse `Pou6f1` and `Pou6f2` POU class-6 homeobox identities, queried 2026-09-23
- PubMed via `bioeval_literature`
- Andersen et al., 1993, PMID: 7901208: Brn-5/POU6F1 is a divergent POU-domain transcription factor that founded POU class VI and is enriched in developing and adult brain
- Cui and Bulleit, 1998, DOI: `10.1002/(SICI)1097-4547(19980615)52:6<625::AID-JNR1>3.0.CO;2-A`, PMID: 9669311: Brn-5/POU6F1 expression marks postmitotic CNS neurons during terminal differentiation
- McClard et al., 2018, DOI: `10.1523/JNEUROSCI.1641-17.2017`, PMID: 29305536: in adult-born olfactory-bulb granule neurons, CRHR1 activity regulates `Pou6f1`; cell-type-specific `Pou6f1` loss reduces dendritic complexity and synaptic connectivity
- Wang et al., 2025, DOI: `10.1016/j.nbd.2025.107080`, PMID: 40912411: POU6F1 overexpression in injured spinal motor-neuron circuits activates JNK/c-Jun/GAP43/BDNF-associated neurite-growth signaling

## Dataset calculations

I loaded the focal-cell training count table and filtered it for POU-family, pathway, and positive-control transcription-factor perturbations. I also queried the parquet directly in DuckDB for the same targets:

```sql
SELECT gene_target,
       SUM(pvals_adj < 0.05)::INT AS n_fdr05,
       SUM(pvals_adj < 0.10)::INT AS n_fdr10,
       MIN(pvals_adj) AS min_padj,
       AVG(n_pert_matched) AS n_pert,
       AVG(n_ctrl_matched) AS n_ctrl
FROM parquet_scan('training_de_all_cell_groups.parquet')
WHERE group_name = '151 TH Prkcd Grin2c Glut'
  AND gene_target IN (...)
GROUP BY 1;
```

The focal subset contains 28,891,566 parquet rows, 1,674 training perturbations, and 17,259 measured genes. In the exact `n_degs` training endpoint, 469 of 1,674 targets are nonzero; the median is 0, the 75th percentile is 1, the 95th percentile is 18, and the largest responses are broad perturbations such as `Uba5` 2677, `Tpr` 1768, `Sin3a` 1433, and `Cic` 576. This cell group is therefore not globally unable to respond.

The key focal-cell analogs were:

| training perturbation | focal `n_degs` | direct focal expression-pattern evidence | interpretation for `Pou6f1` |
|---|---:|---|---|
| `Pou6f2` | 0 | 0 genes at FDR 0.05, 0 at FDR 0.10, minimum adjusted p = 1.0 across 17,259 focal rows | Closest represented class-VI POU comparator; argues strongly against a broad generic POU6/class-VI maintenance program in this focal cell type |
| `Pou2f1` | 0 | 0 at FDR 0.05/0.10, minimum adjusted p = 0.369 | Ubiquitous Oct1/POU factor; showed no basal focal response |
| `Pou2f2` | 0 | 0 at FDR 0.05/0.10, minimum adjusted p = 1.0 | Oct2/POU factor; flat |
| `Pou3f3` | 0 | 0 at FDR 0.05/0.10, minimum adjusted p = 0.849 | Neural POU3 factor; flat in the focal group despite known developmental roles |
| `Pou3f4` | 0 | 0 at FDR 0.05/0.10, minimum adjusted p = 0.759 | Neural/otic POU3 factor; flat in the focal group |
| `Pou1f1` | 0 | 0 at FDR 0.05/0.10, minimum adjusted p = 1.0 | Pituitary POU factor; expected tissue is absent from NeuN+ brain |
| `Pou4f3` | 0 | 0 at FDR 0.05/0.10, minimum adjusted p = 1.0 | Hair-cell/POU4 factor; flat |
| `Pou5f1` | 0 | 0 at FDR 0.05/0.10, minimum adjusted p = 1.0 | Pluripotency POU factor; flat |
| `Hdx` | 0 | 0 at FDR 0.05/0.10, minimum adjusted p = 1.0 | atypical homeobox/POU-class comparator in the corpus; flat |
| `Crhr1` | 0 | 0 at FDR 0.05/0.10, minimum adjusted p = 0.861 | direct receptor upstream of the olfactory-bulb CRH to POU6F1 plasticity model; no matching basal focal signature |
| `Creb1` | 10 | sparse DE, dominated by `Crem` and a few non-module genes | CRHR1/CREB adjacency can be detected weakly, but did not produce a broad program |
| `Ntrk2` | 3 | `Ntrk2`, `Atp2a2`, and `Vgf` only | BDNF/TrkB adjacency gave a small self/sentinel response |
| `Mapk9`, `Jund` | 0, 0 | both 0 at FDR 0.05/0.10 | JNK/AP-1 relatives of the injury literature were flat |
| `Klf7`, `Sox11` | 1, 0 | one `Tuba1a` hit for `Klf7`; none for `Sox11` | neurite-growth developmental TF comparators were absent or singleton-level |
| `Rora`, `Ctnnb1`, `Tcf7l2`, `Cic`, `Atxn1` | 278, 383, 106, 576, 187 | hundreds of focal DE genes for several unrelated TF or regulator perturbations | positive controls showing this focal group would have reported a strong postnatal transcription-factor effect if one were present |

For the eight represented POU perturbations I also computed pairwise focal logFC profile correlations with Distributed Agents runtime. Every represented POU node had `response_activity_status = no_significant_features` in the focal group. `Pou6f2` had zero significant features and no significant-feature overlap with `Pou1f1`, `Pou2f1`, `Pou2f2`, `Pou3f3`, `Pou3f4`, `Pou4f3`, or `Pou5f1`; high-ranking absolute logFC rows all had adjusted p-values of 1.0, a sparse-data artifact rather than coherent POU biology.

## Corpus evidence

The exact held-out target `Pou6f1` was not present in the Distributed Agents corpus, so there were no same-experiment claims or findings for it.

The represented POU neighborhood did have same-experiment corpus evidence. The most relevant claim was:

- `claim:cdbc022fa93623830ad5`, confidence `moderate`: "Shared POU-homeodomain family membership is insufficient to generate an interchangeable acute neuronal CRISPR transcriptional phenotype in this P16 assay."

That claim was anchored by `Pou6f2:F003`, which directly contrasted `Pou6f2` with `Pou1f1`, `Pou2f1`, `Pou2f2`, `Pou3f3`, `Pou3f4`, `Pou4f3`, and `Pou5f1` and reported no generic acute POU-family response in P16 brain neurons. `Pou6f2:F001` further reported no FDR<0.10 downstream genes in any of the measured neuronal cell groups for `Pou6f2`. `Pou3f3:F004` and `Pou3f4:F005` showed that even closer neural POU3 relatives did not phenocopy one another or an expected embryonic POU/Eph axis in matched P16 neuronal cell groups.

## Target-specific reasoning

### Pou6f1

`Pou6f1`, also called Brn-5, is a POU class-VI transcription factor. Andersen et al. identified it as a divergent class-VI POU-domain factor with high embryonic brain and adult brain expression, and Cui and Bulleit found that its CNS expression appears in postmitotic rather than proliferating neurons. Those facts make it a biologically plausible perturbation in a neuronal CRISPR atlas and make `Pou6f2` the single most relevant represented family comparator.

The experiment, however, calibrates `Pou6f1` toward no focal response:

- The exact class-VI comparator `Pou6f2` had `n_degs = 0` in `151 TH Prkcd Grin2c Glut`, no genes at even FDR 0.10 in that group, and Distributed Agents corpus evidence of no FDR<0.10 downstream genes in any of 23 measured neuronal groups.
- All seven other represented POU-domain factors in the count table were also zero in the focal group: `Pou1f1`, `Pou2f1`, `Pou2f2`, `Pou3f3`, `Pou3f4`, `Pou4f3`, `Pou5f1`, and `Pou6f2`. Their direct focal signatures were not near-threshold versions of a hidden response; six of eight had minimum adjusted p-values of 0.76 to 1.0.
- The same-experiment corpus explicitly found nonconvergence rather than a common POU response among represented POU factors in the P16 neuronal assay.
- `Hdx`, an atypical homeobox comparator that corpus findings contrasted with POU factors, was also zero.

The main external reason not to call `Pou6f1` an automatic null is McClard et al.'s adult olfactory-bulb result: `Pou6f1` acts downstream of CRHR1 and is needed for dendritic branching and synaptic connectivity in adult-born CRHR1+ granule neurons. That system is a neuropeptide-dependent plasticity context, and the olfactory bulb was explicitly omitted from this Perturb-seq tissue. In the focal `151 TH Prkcd Grin2c Glut` group, the closest measured CRH/CREB/BDNF pathway handles were absent or sparse: `Crhr1` had 0 DEGs, `Ntrk2` had 3, `Mapk9` and `Jund` had 0, and `Creb1` had only 10. Wang et al.'s later spinal-injury work similarly points to a JNK/c-Jun/GAP43/BDNF neurite-growth program under overexpression/injury, not to a broad basal requirement in uninjured postnatal forebrain/midbrain neurons.

Finally, the zero call is not because transcription factors cannot score in this endpoint. The same focal group had hundreds of DEGs for `Cic`, `Ctnnb1`, `Rora`, `Tcf7l2`, and `Atxn1`. I therefore treated the POU-family flatness as local evidence against a `Pou6f1` state shift rather than a failure of the cell group or statistical test.

**Prediction:** `0` DEGs. A value of 1 to 3 would be plausible if `Pou6f1` behaved like the weakest plasticity-neighbor perturbations (`Ntrk2` or `Klf7`), but the exact class-VI comparator and every measured POU family member were zero; I therefore expect no measured gene to pass BH FDR 0.05.

## Limits

- `Pou6f1` itself was completely held out from both supplied input files and absent from the Distributed Agents corpus, so this is an extrapolation from `Pou6f2` and other POU-family perturbations.
- The strongest published `Pou6f1` neuronal loss-of-function evidence is in adult-born olfactory-bulb granule neurons. The Perturb-seq experiment excluded olfactory bulb and sampled NeuN+ neurons perturbed at P16, so the decisive in vivo `Pou6f1` context was not tested.
- The focal DE parquet reports perturbation log-fold changes, not baseline expression or DNA editing. Weak self-downregulation of a target RNA in a row was not interpreted as failed editing.
- `Pou6f2` is the closest represented comparator but is not interchangeable with `Pou6f1`. Class-VI relatedness supports a zero prediction only together with the broader flat POU neighborhood and the weak CRH/BDNF/JNK-adjacent training signatures.
