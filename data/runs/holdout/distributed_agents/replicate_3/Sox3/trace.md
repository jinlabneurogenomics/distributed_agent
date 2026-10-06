# Predicting held-out DEG counts for 151 TH Prkcd Grin2c Glut

## Question

The manifest for this run contains one held-out perturbation:

| target_name |
|---|
| Sox3 |

I interpreted the endpoint as the integer number of measured genes in `151 TH Prkcd Grin2c Glut` whose Wilcoxon `pvals_adj` would be below 0.05 after acute sparse AAV-CRISPR loss of `Sox3`. `Sox3` was held out completely, so I did not have its signature or true DEG count in either supplied input.

The main ambiguity was how literally to transfer embryonic SOXB1 biology to this assay. I resolved this in favor of the assay context: the data are P16-edited, NeuN-enriched, mostly postmitotic juvenile neurons, not embryonic ventricular-zone progenitors or adult neurogenic zones.

## Sources used

- `training_de_all_cell_groups.parquet`: per-gene differential-expression rows for non-held-out perturbations.
- `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`: observed FDR 0.05 DEG counts for the 1,674 training targets in the focal cell group.
- `219_Sox3.csv`: the requested held-out target list.
- Distributed Agents same-experiment corpus, release `perturbai-july-260713-sourceguard-1773-v1`.
  - I used the Sox-family claim that measured SOX perturbations did not define a generic postnatal neuronal SOX transcriptomic response.
  - I used the `Sox2`, `Sox5`, `Sox10`, and `Sox11` target findings to separate closest or named SOX-family analogs from lineage-mismatched counterexamples.
- Distributed Agents runtime observed-profile analysis over the focal `group_name` to compare the assayed Sox-family signed log-fold-change profiles and their nearest observed neighbors.
- PubMed literature for SOXB1/SOX3 biology:
  - Graham et al. 2003, Neuron, DOI `10.1016/s0896-6273(03)00497-5`, PMID `12948443`: SOXB1 factors, including SOX1/SOX2/SOX3, maintain neural progenitor identity.
  - Wang et al. 2006, Journal of Comparative Neurology, DOI `10.1002/cne.20984`, PMID `16680766`: Sox3 labels neonatal/adult forebrain germinative-zone progenitors and some postmitotic neuronal populations.
  - McAninch and Thomas 2014, PLoS One, DOI `10.1371/journal.pone.0113361`, PMID `25409526`: endogenous SOX3 binds thousands of neural-progenitor regulatory sites and overlaps SOXB1 developmental enhancer biology.
  - Rogers et al. 2014, PLoS One, DOI `10.1371/journal.pone.0095356`, PMID `24751947`: `Dbx1` is a direct SOX3 target in embryonic neural progenitors.
  - Mercurio et al. 2019, iScience, DOI `10.1016/j.isci.2019.04.030`, PMID `31082736`: Sox2, the closest assayed SOXB1 analog, has a postmitotic thalamic role in retina-thalamus-cortex connectivity.

## Dataset checks and calibration

The requested CSV contained only `Sox3`. The focal training endpoint contained 1,674 measured non-held-out targets; 469 had at least one FDR 0.05 DEG in `151 TH Prkcd Grin2c Glut`, the median count was 0, the 75th percentile was 1, the 90th percentile was 2, and the maximum was 2,677. This means that one or two passing genes is already a real, non-null but very sparse response in this cell group.

I read the focal rows of the parquet and confirmed that there were 1,674 targets by 17,259 measured genes. I then pulled the assayed Sox-family DEG counts and the exact significant genes:

| training perturbation | focal `n_degs` | FDR 0.05 genes in 151 TH Prkcd Grin2c Glut | interpretation for Sox3 |
|---|---:|---|---|
| Sox2 | 2 | `Tnnt1` down, logFC -1.006, FDR 0.000003; `Stam` down, logFC -0.567, FDR 0.0147 | Closest represented SOXB1-family analog. It supports at most a tiny effect in postmitotic thalamic neurons. |
| Sox5 | 2 | `Dgkh` up, logFC +0.387, FDR 0.000537; `Tnnt1` up, logFC +0.566, FDR 0.0284 | A SoxD counterexample: it shares `Tnnt1` with `Sox2` but in the opposite direction, so SOX-family membership alone is not predictive. |
| Sox4 | 0 | none | SOXC relative; no focal response. |
| Sox11 | 0 | none | SOXC/immature-neuron factor; Distributed Agents reports no robust FDR response in any recovered neuronal group. |
| Sox9 | 0 | none | SoxE/glial-lineage member; no focal neuronal response. |
| Sox10 | 0 | none | SoxE oligodendrocyte/neural-crest regulator; Distributed Agents reports a pan-neuronal transcriptional null. |
| Sox17 | 0 | none | SoxF vascular/endodermal/Wnt-associated member; no focal neuronal response. |
| Sox18 | 0 | none | SoxF vascular/endothelial member; no focal neuronal response. |

The Distributed Agents corpus claim over `Sox2`, `Sox5`, and `Sox17` states that measured SOX-family perturbations do not form a generic neuronal SOX module in this P16 NeuN+ assay; the limited thalamic effects are target-specific and can invert shared genes such as `Tnnt1`. That matches the direct focal counts above.

I also compared focal signed profiles for `Sox2`, `Sox4`, `Sox5`, `Sox9`, `Sox10`, `Sox11`, `Sox17`, and `Sox18` with the Distributed Agents runtime. `Sox2` and `Sox5` were the only assayed Sox nodes with 1 to 9 significant features; the other six had none. Full-profile correlations were not treated as strong biological evidence because the FDR-level signatures were near-null, and the top-tail overlap was small; the important FDR fact was that `Sox2` and `Sox5` had no same-direction significant overlap and one significant sign conflict on `Tnnt1`.

To check whether the focal cell group was simply unable to call broad transcriptional responses, I inspected high-count focal perturbations. The same training endpoint contains broad responses for, among others, `Uba5` with 2,677 DEGs, `Tpr` with 1,768, `Sin3a` with 1,433, `Brd4` with 311, `Rora` with 278, `Tcf7l2` with 106, and `Zfp423` with 150. Thus the sparse Sox-family counts are target-specific rather than a global lack of statistical power in `151 TH Prkcd Grin2c Glut`.

## Target-specific reasoning

### Sox3

**Closest within-dataset analog.** `Sox2` is the closest assayed perturbation because `Sox1`, `Sox2`, and `Sox3` are SOXB1 transcription factors with redundant neural-progenitor activity. In the focal dataset `Sox2` produced exactly two FDR 0.05 genes, `Tnnt1` and `Stam`, both down-regulated. This shows that a SOXB1 factor can be detectable in `151 TH Prkcd Grin2c Glut`, but the measured response was extremely narrow. The Distributed Agents `Sox2` finding also reports that this two-gene thalamic response did not recover canonical SOX2 neural-stem, pluripotency, proliferation, Notch/Hes, or previously published dLGN `Efna5`/serotonin-transporter outputs.

**Sox-family counterexamples.** `Sox5` is less homologous, as a SoxD rather than SOXB1 factor, but it provides a useful in-cell-group control: it also had two focal DEGs yet sent `Tnnt1` in the opposite direction from `Sox2`, with `Dgkh` as a private second hit. `Sox4`, `Sox9`, `Sox10`, `Sox11`, `Sox17`, and `Sox18` all had zero focal DEGs. The SoxE and SoxF nulls are lineage-mismatch counterexamples rather than close paralogs; the SOXC nulls argue more generally that many developmental SOX programs are not reopened by single acute loss in P16 NeuN+ nuclei.

**Developmental pathway comparators.** Focal `n_degs` was 0 for represented stem-cell or SOXB1-adjacent comparators including `Pax6`, `Notch1`, `Notch2`, `Myc`, `Mycn`, `Pou5f1`, `Rest`, `Ep300`, `Chd7`, and `Smarca4`. This does not directly model SOX3, but it argues against a broad neural-progenitor, Notch/Hes, OSKM-like, or CHD7/SOX2 stem-cell module being assay-visible in this postmitotic focal population.

**External prior.** Public literature gives SOX3 strong neural-progenitor biology: SOXB1 factors maintain panneural progenitor identity (Graham et al. 2003), SOX3 binds many conserved enhancers near neurodevelopmental genes in neural progenitors (McAninch and Thomas 2014), and `Dbx1` is one direct SOX3 target in embryonic spinal-cord progenitors (Rogers et al. 2014). Wang et al. 2006 also found Sox3 in neonatal/adult germinative zones and in some postmitotic neurons. However, those settings are embryonic or neurogenic progenitor compartments and selected mature neurons; they are not evidence that `Sox3` acutely maintains a broad RNA program in juvenile thalamic `Prkcd`/`Grin2c` glutamatergic nuclei. By contrast, `Sox2` has a more explicit postmitotic thalamic-neuron role in Mercurio et al. 2019 and still produced only two focal DEGs in the supplied experiment.

**Prediction.** I predict no gene will pass FDR 0.05 after held-out `Sox3` perturbation in `151 TH Prkcd Grin2c Glut`: `predicted_n_degs = 0`. A one- or two-gene singleton response analogous to `Sox2` is plausible, but the evidence for it is weaker for `Sox3` than for `Sox2`, and the majority of assayed Sox-family/developmental comparators were focal nulls.

## Limits

- `Sox3` itself was absent from the Distributed Agents corpus and from the training DEG parquet as a perturbation target, and the exact SOXB1 paralogs `Sox1` and `Sox3` were both missing as training perturbations. The prediction therefore extrapolates from `Sox2`, which is close but not interchangeable.
- The experiment measures nuclear RNA 3 to 4 weeks after sparse P16 editing. It cannot directly score early developmental fate choices, axon targeting, survival before harvest, protein loss, or rare Sox3-positive cells diluted within the broad `151 TH Prkcd Grin2c Glut` class.
- Near-null signatures produce noisy whole-transcriptome correlations, especially among lowly expressed genes with extreme log-fold-change estimates but adjusted p-values of 1.0. I therefore weighted FDR-level DEG counts and biologically motivated comparisons more heavily than all-gene Pearson/cosine similarities.
- A prediction of zero means no measured gene is expected to survive BH correction at 0.05 in this assay. It is not a claim that SOX3 is biologically unimportant or that CRISPR editing would fail.
