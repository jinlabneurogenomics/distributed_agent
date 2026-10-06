# Predicting held-out DEG counts for 151 TH Prkcd Grin2c Glut

## Question and resolved ambiguities

The manifest for this run contains one held-out perturbation, `Foxp1`. I interpreted the requested value as the integer number of measured genes that would have `pvals_adj < 0.05` if `Foxp1` had been assayed in `151 TH Prkcd Grin2c Glut` cells under the same P16 sparse AAV-CRISPR design. A prediction of `0` means that no measured gene is expected to pass that FDR threshold in the focal group, not that FOXP1 is biologically irrelevant or that editing failed.

`Foxp1` was not present in the parquet as a `gene_target` and was not present in the focal training-count CSV, so I treated all direct expression data for `Foxp1` as held out. I used the supplied non-held-out perturbations to choose analogs and used external biology only to decide which measured perturbations were mechanistically close enough to matter.

## Sources

- Raw differential-expression parquet: `[local file: training_de_all_cell_groups.parquet]`.
- Focal endpoint counts: `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
- Held-out target manifest: `[local file: 081_Foxp1.csv]`.
- Distributed Agents same-experiment corpus, release `perturbai-july-260713-sourceguard-1773-v1`, queried with `target_context` and `compare_targets` for `Foxp2`, `Foxa2`, `Bcl11b`, and `Satb2`.
- Distributed Agents runtime `profile_neighbors`, run on focal-cell `scores` profiles for `Foxp2`, `Foxp3`, and `Foxa2`; the resulting artifact is `fox_profile_neighbors.json`.
- PubMed literature:
  - Li et al. 2004, `Molecular and Cellular Biology`, DOI `10.1128/MCB.24.2.809-822.2004`: FOXP1, FOXP2, and FOXP4 homo- and heterodimerize through the leucine zipper and require dimerization for DNA binding.
  - Sin et al. 2014, `Journal of Molecular Neuroscience`, DOI `10.1007/s12031-014-0359-7`: FOXP1/2/4 dimers differentially regulate nominated FOXP2 target genes.
  - Estruch et al. 2018, `Human Molecular Genetics`, DOI `10.1093/hmg/ddy035`: FOXP proteins interact with neurodevelopmental transcription factors including SATB2 and SOX5.
  - Ferland et al. 2003, `Journal of Comparative Neurology`, DOI `10.1002/cne.10654`: Foxp1 and Foxp2 are expressed from development into adulthood in mouse brain, including basal ganglia and thalamus.
  - Hisaoka et al. 2009, `Neuroscience`, DOI `10.1016/j.neuroscience.2009.12.055`: Foxp1 and Foxp2 mark different subpopulations of mouse cortical projection neurons.
  - Fong et al. 2018, `Neuroscience`, DOI `10.1016/j.neuroscience.2018.07.017`: adult mouse Foxp1 and Foxp2 are expressed in partially overlapping striatal spiny projection neuron populations.
  - Precious et al. 2016, `Experimental Neurology`, DOI `10.1016/j.expneurol.2016.05.002`: FoxP1 marks medium spiny neurons from precursors to maturity and is required for DARPP-32-positive MSN differentiation in vitro.
  - Khandelwal et al. 2024, `Science Advances`, DOI `10.1126/sciadv.adm7039`: postnatal FOXP1 controls glutamatergic inputs and snRNA-seq programs in D2 striatal projection neurons, with rescue by postnatal reinstatement.
  - Ahmed et al. 2024, `Cell Reports`, DOI `10.1016/j.celrep.2024.114257`: FOXP1 and FOXP2 have compensatory functions in D1 striatal projection neurons; combined loss has stronger electrophysiological, behavioral, and transcriptional effects than either single loss.

## Computations over the supplied data

1. I loaded the held-out manifest and confirmed that only `Foxp1` was requested.
2. I summarized the focal training endpoint over 1,674 measured targets. The distribution is strongly zero-inflated: 1,205 targets had `n_degs = 0`, the median was 0, the 75th percentile was 1, only 132 targets had at least 5 DEGs, and 43 targets had at least 100 DEGs. A small positive prediction should therefore require specific evidence; most perturbations in this exact cell group are FDR-flat.
3. I filtered the parquet to `group_name == "151 TH Prkcd Grin2c Glut"`, giving 1,674 targets by 17,259 measured genes. I used this slice to inspect focal adjusted p-values and Wilcoxon scores for biologically nominated analogs, rather than relying only on the precomputed count CSV.
4. I queried the focal counts for represented FOX-family and neuronal-fate targets. All represented same-family perturbations were zero in the focal group:

| perturbations | focal `n_degs` | interpretation for `Foxp1` |
| --- | ---: | --- |
| `Foxp2` | 0 | Closest measured FOXP paralog; strong negative analog. |
| `Foxp3` | 0 | FOXP subfamily but non-neuronal Treg-biased; weak negative analog. |
| `Foxa2`, `Foxc2`, `Foxe3`, `Foxi1`, `Foxj3`, `Foxk2`, `Foxl1`, `Foxl2`, `Foxn1` | 0 each | Forkhead-family counterexamples; most are not close paralogs, but they show that a forkhead DNA-binding domain alone does not imply a thalamic response. |

5. I inspected the focal `Foxp2`, `Foxp3`, and `Foxa2` score profiles with `profile_neighbors`, using all 1,674 training targets as the eligible universe and retaining full profiles plus top 500 positive and negative Wilcoxon-score tails. `Foxp2` had zero significant positive or negative genes; its strongest whole-profile neighbor was only `Cic` with Pearson `r = 0.118` and cosine `0.119`. `Foxp3` and `Foxa2` were even flatter by this diagnostic, with best whole-profile correlations below `0.07`. The nominal top-tail overlaps were also composed of adjusted p-values of 1.0 for the FOXP/forkhead anchors. I therefore did not treat algorithmic neighbors such as `Cic`, `Ufc1`, `Ctnnb1`, or `Kcnq1` as mechanistic analogs.
6. I contrasted those zeros with focal targets that clearly respond in the same cell group. `Rora` had 278 DEGs, `Tcf7l2` had 106, `Prox1` had 50, `Chd4` had 100, `Stag2` had 37, and `Ctnnb1` had 383. Thus `151 TH Prkcd Grin2c Glut` cells are not globally unable to produce FDR-significant responses; the zeros for `Foxp2`, other `Fox*` targets, and striatal/cortical developmental factors are target-specific.

## Foxp1-specific reasoning

### Relevant measured analogs and counterexamples

`Foxp2` is the best measured analog. FOXP1, FOXP2, and FOXP4 are the neural members of a dimerizing FOXP subfamily: Li et al. 2004 showed homo- and heterodimerization, and Sin et al. 2014 showed that different FOXP1/2/4 dimer combinations can change transcription of nominated FOXP2 targets. Ferland et al. 2003 and Hisaoka et al. 2009 place both Foxp1 and Foxp2 in postmitotic projection-neuron populations, and Fong et al. 2018 showed partially overlapping expression in adult striatal SPNs. In the supplied focal group, however, `Foxp2` had `n_degs = 0`; its eight strongest nominal positive rows all had `pvals_adj = 1.0`. The Distributed Agents same-experiment corpus further reports that `Foxp2` produced no FDR<0.10 downstream response in any of 22 measured neuronal groups and that the expected CNTNAP2/FOXP target axis was not recovered. The direct paralog therefore points to a focal prediction of zero for `Foxp1`.

The remaining measured FOXP/forkhead perturbations also argue against a generic FOX response. `Foxp3`, the only other FOXP target in the focal count table, had `n_degs = 0`; FOXP3 is not a good neural paralog of FOXP1, but its flat profile rejects any broad FOXP-domain stress response. `Foxa2`, `Foxc2`, `Foxe3`, `Foxi1`, `Foxj3`, `Foxk2`, `Foxl1`, `Foxl2`, and `Foxn1` each had `n_degs = 0`. The forkhead counterexamples are distant, so I used them only as weak negative context.

The best striatal-development comparators were also flat in `151`. `Bcl11b`, `Ebf1`, `Isl1`, `Zfp521`, `Rarb`, `Meis1`, and `Meis2` all had `n_degs = 0` in the focal cell group. Precious et al. 2016 and Fong et al. 2018 make `Foxp1` an MSN-lineage gene, and Khandelwal et al. 2024 and Ahmed et al. 2024 show that FOXP1 can have postnatal SPN functions under dense, cell-type-directed perturbation. But those are GABAergic striatal projection-neuron settings. The focal readout here is a thalamic glutamatergic group, and the represented LGE/MSN regulators do not elicit a thalamic FOXP-like or striatal identity response.

The cortical projection-neuron factors served as timing and assay counterexamples. `Satb2`, `Bcl11b`, and `Tbr1` each had `n_degs = 0` in the focal thalamic group, and `Sox5` and `Mef2c` had only 2 and 1 focal DEGs, respectively. The Distributed Agents corpus reports that `Bcl11b` had no FDR<0.10 genes across 23 groups and `Satb2` had no downstream FDR<0.10 genes across recovered neuronal groups, while `Tbr1` and `Mef2c` could still show responses in cortical contexts. This is the pattern expected if many embryonic projection-neuron identity regulators are buffered after a sparse P16 perturbation instead of acutely reopening a fate program.

Finally, robust focal thalamic responders were poor positive analogs. `Rora`, `Tcf7l2`, `Prox1`, `Ctnnb1`, `Chd4`, and `Stag2` prove that this cell group can respond, but their biology and signatures point to Wnt/thalamic identity, chromatin remodeling, or cohesin/NuRD effects rather than FOXP1/FOXP2 transcriptional maintenance. In the `Foxp2` focal profile, `Ctnnb1` and `Rora` appeared only as weak nominal neighbors: Pearson `r = 0.096` and `0.084`, respectively, with no shared significant FOXP2 genes because `Foxp2` itself had none.

### Zero versus nonzero decision

The main external reason to expect an effect is that FOXP1 is a real postmitotic neuronal transcription factor, is expressed in thalamus/striatum/cortex, dimerizes with FOXP2 and FOXP4, and has postnatal functions in striatal projection neurons. The main within-dataset reason to reject a focal positive call is stronger for this endpoint: the closest measured paralog `Foxp2` was exactly zero in `151`, every represented same-family `Fox*` target was exactly zero, and the relevant striatal/cortical developmental comparators were zero or nearly zero in the requested thalamic class. The few robust `151` responders were biologically off-axis. I therefore predict that `Foxp1` loss would be FDR-flat in `151 TH Prkcd Grin2c Glut`, with an endpoint at the exact zero mode of its measured analogs rather than a tiny one- or two-gene count.

## Limits and extrapolation

This prediction extrapolates from paralogs and pathway neighbors because `Foxp1` itself was completely held out and `Foxp4` was not a represented training perturbation. The RNA readout provides no DNA indel or FOXP1 protein measurement, and sparse AAV-CRISPR with modest average target-mRNA downregulation could understate a dense conditional knockout phenotype. The focal `151 TH Prkcd Grin2c Glut` label is also a coarse thalamic glutamatergic class; a rare FOXP1-positive subtype could be diluted below FDR even if it were affected. Conversely, the conditional and rescue literature that demonstrates FOXP1 function is mostly embryonic or striatal SPN-specific, so it should not be mapped one-to-one onto an acute, mosaic, postnatal thalamic knockout.

The point prediction is therefore high-confidence for the binary zero/nonzero call relative to the supplied endpoint distribution, but it remains a one-target extrapolation from `Foxp2` and related transcription-factor nulls, not a direct measurement of FOXP1 editing or a claim that FOXP1 has no roles elsewhere.
