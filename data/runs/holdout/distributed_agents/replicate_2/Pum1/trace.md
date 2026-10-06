# Pum1 DEG-count prediction

## Question and endpoint

I interpreted the task as a target-level prediction for the held-out perturbation `Pum1`: the number of measured genes that would have `pvals_adj < 0.05` in `151 TH Prkcd Grin2c Glut` nuclei after acute sparse AAV-CRISPR loss of function. The number is an assay-level response-breadth count, not a count of true PUM1 targets, a viability score, or a target-engagement estimate.

The manifest `[local file: 192_Pum1.csv]` contains one requested target:

```tsv
target_name
Pum1
```

`Pum1` and its closest paralog `Pum2` were absent from the focal training count CSV, and `Pum1` was absent from the supplied training parquet by design. The filtered same-experiment semantic corpus release `perturbai-july-260713-sourceguard-1773-v1` also had no `Pum1` or `Pum2` target report, so PUM-family reasoning is extrapolated from other measured RNA-regulatory perturbations plus external literature.

## Sources used

- Focal training endpoint: `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
- Full training differential-expression parquet: `[local file: training_de_all_cell_groups.parquet]`.
- Same-experiment interpreted semantic layer: Distributed Agents corpus release `perturbai-july-260713-sourceguard-1773-v1`, queried for `Fmr1`, `Ddx3x`, `Atxn2`, `Cnot1`, `Atxn1`, `Hnrnpu`, and `Tardbp`.
- Run-local profile analysis: `profile_neighbors` compared the focal 151-TH logFC profiles of `Fmr1`, `Ddx3x`, `Atxn2`, `Upf3b`, `Ago1`, `Ago2`, `Cnot1`, `Atxn1`, `Hnrnpc`, `Hnrnpu`, and `Tardbp` against all 1,674 eligible focal training nodes.
- External literature:
  - Gennarino et al. 2015, Cell, DOI `10.1016/j.cell.2015.02.012`, PMID `25768905`: Pum1 haploinsufficiency increases wild-type ATXN1 and causes SCA1-like neurodegeneration in mice.
  - Gennarino et al. 2018, Cell, DOI `10.1016/j.cell.2018.02.006`, PMID `29474920`: human PUM1 loss-of-function/decreased PUM1 dosage causes PADDAS/PRCA and increases known PUM1 targets in patient cells in a dosage-sensitive way.
  - Enwerem et al. 2021, RNA, DOI `10.1261/rna.078436.120`, PMID `33397688`: human PUM1 and PUM2 repress sequence-matched RNAs by recruiting CCR4-NOT deadenylation and decapping-dependent mRNA-decay machinery.
  - Dong et al. 2018, Oncotarget, DOI `10.18632/oncotarget.24345`, PMID `30181804`: mouse Pum2 knockout increases excitatory synaptic protein output, dendritic spines, and seizure susceptibility, with a GLUR2 effect that is primarily translational rather than a whole-mRNA abundance increase.

## Computational checks

The training endpoint has 1,674 biological perturbations. It is highly zero-inflated in this focal cell group: 1,205 targets have `n_degs = 0`, the median is 0, the 75th percentile is 1, the 95th percentile is 18, and the 99th percentile is about 436. Thus even 8 to 20 DEGs is above almost all training perturbations even though it is far below the spliceosome/proteostasis outliers.

I queried the parquet for the focal cell group and a mechanistic shortlist with a filter equivalent to:

```python
(field("group_name") == "151 TH Prkcd Grin2c Glut") &
field("gene_target").isin(shortlisted_targets)
```

and then counted `pvals_adj < 0.05` rows and inspected the leading significant genes. This confirmed the focal counts and showed that the relevant cytoplasmic RNA/translation comparators are sparse:

| training target | observed `n_degs` in 151 TH | focal expression-pattern evidence | relevance to `Pum1` |
|---|---:|---|---|
| `Fmr1` | 0 | No FDR<0.05 genes in the focal group. The corpus also reports a nearly flat FMRP/CYFIP/local-translation neighborhood in this assay. | Cytoplasmic neuronal translational repressor; supports the idea that loss of a famous local-translation RBP can be invisible to whole-gene snRNA-seq. |
| `Cnot1` | 0 | No focal DEGs. In the corpus, `Cnot1` had a sparse response outside 151 and did not phenocopy measured `Ago`/`Tnrc6`/`Xrn1` decay-route perturbations. | PUM1/PUM2 can recruit CCR4-NOT; the direct CNOT scaffold being quiet in 151 argues against a broad generic deadenylation-collapse response. |
| `Ago2`, `Dicer1`, `Tnrc6a`, `Tnrc6b`, `Tia1` | 0 each | Flat in 151. `Ago1` had only one focal DEG, `Kif13b`. | Other post-transcriptional silencing and stress-granule nodes are mostly zero in the same readout. |
| `Eif4g1`, `Eif4h`, `Eif4a2` | 1, 1, 2 | Singleton or two-gene signatures; `Eif4g1`'s only focal call was self, `Eif4h` induced `Hexim1`, and `Eif4a2` had self plus `Cadm4`. | Cap-dependent translation-initiation comparators; they set a very low baseline for translation machinery nodes. |
| `Upf3b` | 1 | One focal DEG, `Inpp5f`. | NMD/RNA-surveillance perturbation; another compact cytoplasmic RNA-regulatory footprint. |
| `Ddx3x` | 8 | Compact focal response with self-downregulation plus `Grin2b`, `Synpo2`, `Plekhg1`, `Tcea2`, and `Ccdc136` down and `Ypel3`/`Tmsb10` up. The corpus describes this as a narrow postnatal glutamatergic Ddx3x response rather than a broad translation-factor state. | Stronger cytoplasmic RBP/translation comparator whose count is a good upper end for the buffered local-translation class. |
| `Atxn2` | 8 | Compact focal response with `Coro6`, `Srsf11`, `Rsrp1`, and `Tspoap1` down and `Syt7`, `Crmp1`, `Sncb`, and `Cspg5` up. The corpus separates it from `Tardbp`/stress-granule/ALS family broad responses. | Cytoplasmic RBP/stress-granule disease gene; supports a small but real focal RNA-metabolism response. |
| `Xrn1` | 20 | Small 5-prime-to-3-prime decay response including `Psap`, `Enpp5`, `Rufy2`, and `Ap3m1` down and `Adgrb1`, `Gpatch8`, `Rap1gap2`, `Ppp1r9b`, `Rims2`, and `Shank1` up. | mRNA-decay enzyme; a plausible upper-side comparator because PUM1 also modulates mRNA stability, but XRN1 is a direct decay effector rather than a sequence-specific recruiter. |
| `Atxn1` | 187 | Strong thalamic transcription-factor-like response. The corpus reports sharp 151-TH convergence of `Atxn1` loss with `Cic` loss through the ATXN1-CIC repressor axis. | PUM1 directly represses ATXN1, but PUM1 loss should increase ATXN1 output rather than delete `Atxn1`; this is a pathway warning and upward-risk counterexample, not a same-direction phenocopy. |
| `Hnrnpc`, `Tardbp`, `Hnrnpu` | 122, 210, 733 | Large nuclear RBP signatures; `Hnrnpu` and `Tardbp` produce hundreds of focal DEGs with RNA-processing, proteostasis, ER/lysosomal, and secretory remodeling arms. | Demonstrates the assay can detect RNA-regulatory loss when the perturbation creates a nuclear stress/splicing state; these are too nuclear and broad to use as direct PUM1 analogs. |

For the run-local profile scan, the focal logFC neighbors of the weak RNA-regulatory anchors were themselves mostly zero- or one-DEG perturbations. For example, `Fmr1` had 0 significant features and nearest whole-profile neighbors with `n_degs` 0,0,0,0,0,1; `Ddx3x` had 8 significant features and nearest whole-profile neighbors with `n_degs` 0,0,0,0,0,0; `Cnot1` had 0 significant features and its nearest whole-profile neighbors included `Tia1` at 0 and other flat targets. I used that as evidence that these anchors do not sit in a hidden high-response expression module.

## Target-specific prediction for `Pum1`

`Pum1` encodes PUMILIO1, a sequence-specific PUF-family RNA-binding repressor. External literature makes it biologically non-null in neurons: PUM1 dosage controls ATXN1 abundance in mice, and reduced PUM1 causes human neurodevelopmental/ataxia/seizure syndromes. Enwerem et al. further show that PUM1/PUM2 can regulate transcript levels by direct CCR4-NOT recruitment, so PUM1 loss is not purely translational in all contexts.

The focal Perturb-seq calibration argues against a broad hundreds-of-DEGs signature, however. The closest measured post-transcriptional silencing nodes available in 151 TH are flat or tiny: `Cnot1`, `Ago2`, `Dicer1`, `Tnrc6a`, `Tnrc6b`, `Tia1`, and `Fmr1` all have 0 DEGs; `Ago1`, `Upf3b`, `Eif4g1`, and `Eif4h` have 1; `Eif4a2` has 2; and the stronger cytoplasmic RBP disease-gene examples `Ddx3x` and `Atxn2` each have 8. The clearest mRNA-decay enzyme, `Xrn1`, reaches 20, which I treated as an upper-side analog rather than the center because PUM1 selects a subset of targets and can be buffered by `Pum2`.

The direct `Atxn1` training count is much higher at 187, but it points in the wrong perturbational direction: PUM1 loss derepresses ATXN1 whereas the training perturbation removes `Atxn1`. It raises the chance that `Pum1` could trigger a detectable 151-TH response through ATXN1/CIC-sensitive genes, but it does not justify assigning an `Atxn1`-scale count. The very broad nuclear RBP counts for `Hnrnpu`, `Tardbp`, and `Hnrnpc` are even less direct because PUM1 is primarily a cytoplasmic sequence-specific repressor rather than a core spliceosome/hnRNP node.

Balancing those points, I predict a compact nonzero footprint about equal to the `Ddx3x`/`Atxn2` focal counts and below `Xrn1`: **8 DEGs**.

## Limits and uncertainty

This is an extrapolation without a same-experiment `Pum1` or `Pum2` signature. `Pum2`, the most direct paralog, is also absent from the training count table, as are several obvious CPEB/RBFOX/ELAVL/NOVA neuronal RNA-regulatory comparators. The focal endpoint is a whole-gene nuclear RNA Wilcoxon count, so ribosome occupancy, cytoplasmic localization, dendritic translation, ATXN1 or GLUR2 protein abundance, and seizure/excitability phenotypes could all change with few FDR-significant nuclear mRNAs. Conversely, PUM1 target derepression could be more mRNA-visible than `Fmr1` or `Pum2` biology, and the `Atxn1` axis could amplify a secondary response in 151-TH neurons. The exact point estimate should therefore be read as a low-count call, not as evidence that PUM1 is biologically inert.
