# DEG-count prediction for 151 TH Prkcd Grin2c Glut

## Question and endpoint

I interpreted the task as a scalar holdout prediction: for each requested held-out genetic perturbation, predict the integer number of rows in `151 TH Prkcd Grin2c Glut` whose Wilcoxon `pvals_adj` would be below 0.05 if that perturbation had not been held out. The requested target list contains one target, `Gad1`, and I preserved that order in `answer.txt`.

The `151 TH Prkcd Grin2c Glut` label was treated as thalamic glutamatergic neurons. I did not expand `TH` as tyrosine hydroxylase, and I counted `n_degs` exactly as an FDR < 0.05 endpoint, including the perturbed gene itself when present, because the training count CSV uses that convention.

## Sources used

- Declared training endpoint: `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
- Declared differential-expression parquet: `training differential-expression dataset`.
- Requested-target manifest: `single-target request for Gad1`.
- Distributed Agents same-experiment internal corpus `perturbai-july-260713-sourceguard-1773-v1`, used for compact interpreted reports and packaged Evidence/Reference records for `Gad2`, `Slc32a1`, `Slc6a1`, `Abat`, `Gabra1`, `Gabrb2`, and `Gabrg2`. This is a semantic representation of the same Perturb-seq experiment, not independent validation.
- External gene-function priors from PubMed and the report-packaged NCBI Gene/Reactome references.

External mechanism references I used:

- Erlander et al. 1991, PMID 2069816, doi:10.1016/0896-6273(91)90077-d: `Gad1`/GAD67 and `Gad2`/GAD65 are distinct glutamate decarboxylase genes whose enzymes differ in localization and cofactor handling.
- Bu et al. 1992, PMID 1549570, doi:10.1073/pnas.89.6.2115: both GAD65 and GAD67 cDNAs encode enzymatically active glutamate decarboxylases.
- Feldblum et al. 1993, PMID 8315667, doi:10.1002/jnr.490340612: GAD65 and GAD67 mRNAs have overlapping but different brain distributions, consistent with complementary GABA-synthetic roles.
- Asada et al. 1997, PMID 9177246, doi:10.1073/pnas.94.12.6496, cited in the internal `Gad2` report: germline Gad1/GAD67 knockout caused severe neonatal phenotypes and markedly reduced newborn cortical GABA.
- Kash et al. 1997, PMID 9391152, doi:10.1073/pnas.94.25.14060, cited in the internal `Gad2` report: germline Gad2/GAD65 knockout on C57BL/6 was viable but stress-seizure susceptible, contrasting with the basal GABA requirement of GAD67.
- Jin et al. 2003, PMID 12634427, doi:10.1073/pnas.0730698100, cited in the internal `Gad2` report: GAD65-containing complexes functionally couple GABA synthesis to vesicular GABA transport.
- McIntire et al. 1997, PMID 9349821, and Chaudhry et al. 1998, PMID 9822734, cited in the internal `Slc32a1` report: `Slc32a1`/VGAT marks the vesicular inhibitory amino-acid transporter in GABAergic and glycinergic terminals.
- Jensen et al. 2003, PMID 12815026, doi:10.1152/jn.00240.2003, cited in the internal `Slc6a1` report: GAT1 deficiency alters extracellular GABA and tonic/phasic inhibition.
- NCBI Gene `GAD2`, `SLC6A1`, and Reactome R-HSA-428625, cited in the internal reports, for the curated placement of GAD2 in GABA production, SLC6A1 in plasma-membrane GABA reuptake, and SLC32A1 in vesicular inhibitory amino-acid transport.

## Dataset calculations

I used DuckDB predicate scans over the parquet, always restricted either to the focal group or to a short hand-picked analog list, and the count CSV for the exact FDR < 0.05 training endpoint.

The target manifest contains exactly:

```tsv
target_name
Gad1
```

`Gad1` had zero rows as a `gene_target` in the parquet and zero rows in the training count CSV, confirming that this is a held-out prediction rather than a lookup.

The training `151 TH Prkcd Grin2c Glut` counts contain 1,674 targets. They are heavily zero-inflated: 1,205/1,674 were zero, the median was 0, the 75th percentile was 1, the 90th percentile was 2, and the largest response was 2,677 DEGs. The largest focal burdens were broad core-process perturbations such as `Uba5`, `Tpr`, `Sin3a`, `Rnpc3`, and `Zbtb7a`, not neurotransmitter synthesis or synaptic-vesicle perturbations.

For GABA/glutamate analogs in the focal class I counted FDR < 0.05 rows directly from the parquet and joined them against the CSV endpoint:

| training perturbation | focal n_degs | n_pert_matched | focal pattern relevant to Gad1 |
| --- | ---: | ---: | --- |
| `Gad2` | 0 | 178 | closest represented GABA-synthetic paralog; no FDR < 0.05 gene in `151 TH Prkcd Grin2c Glut`; its best focal p-values all adjusted to 1.0 |
| `Slc32a1` | 0 | 268 | vesicular inhibitory transmitter loading; zero focal DEGs despite the largest perturbed-cell count among the checked analogs |
| `Slc6a1` | 0 | 220 | GABA reuptake; zero focal DEGs |
| `Abat` | 0 | 188 | mitochondrial GABA catabolism; zero focal DEGs |
| `Gls` | 0 | 103 | glutamine-to-glutamate supply for neurotransmitter and metabolism; zero focal DEGs |
| `Gabra1` | 1 | 128 | GABA-A alpha subunit; only `Gabra1` itself passed FDR < 0.05 |
| `Gabrb2` | 4 | 140 | GABA-A beta2 subunit; small activity-like response with `Gabrb2`, `Nr4a1`, `Vgf`, and `Nalf1` at FDR < 0.05 |
| `Gabrb3` | 0 | 100 | GABA-A beta3 subunit; zero focal DEGs |
| `Gabrg2` | 1 | 166 | GABA-A gamma2 subunit; only `Gabrg2` itself passed FDR < 0.05 |
| `Glud1` | 1 | 153 | glutamate dehydrogenase; only the self transcript passed FDR < 0.05 |
| `Slc1a2` | 1 | 187 | glutamate transporter, mostly glial in native biology; only the self transcript passed FDR < 0.05 |

I also queried focal rows for expected GABA and activity markers. Under `Gad2`, `Slc32a1`, `Slc6a1`, and `Abat`, `Gad1`, `Gad2`, `Slc32a1`, `Slc6a1`, `Fos`, `Npas4`, `Nr4a1`, `Vgf`, `Bdnf`, `Arc`, `Egr1`, and `Homer2` all remained at FDR 1.0. The Gabrb2 rows are the important counterexample: in the same focal class `Gabrb2` induced `Nr4a1` logFC +0.804, FDR 0.000251 and `Vgf` logFC +0.573, FDR 0.00203, with `Fos`, `Npas4`, and `Homer2` just above 0.05. Thus the assay could report a weak disinhibition/activity state, but presynaptic GABA supply perturbations did not cross that threshold.

Across the rest of the atlas, the same GABA-axis perturbations were sparse rather than hidden focal negatives. The internal `Gad2` report records 0 downstream genes at FDR < 0.10 in all 22 `Gad2`-measured cell groups; the only visible signal was Gad2 self-transcript reduction in five GABAergic groups. Its whole-surface Wilcoxon-score neighbors were essentially uncorrelated, with absolute Pearson correlations <= 0.030, arguing against a coherent subthreshold Gad2 program. The `Slc32a1` report similarly records a downstream pan-null: 0 non-self genes at FDR < 0.10 in all 23 recovered groups even though `Slc32a1` itself was significantly reduced in several GABAergic groups. `Slc6a1` had only one downstream FDR < 0.10 row across 22 measured groups, `Yif1a` in 009 L2-3 IT PIR AON ENT Glut at FDR 0.0501, and the `Abat` surface had only a one-gene Pvalb-class response. Those corpus summaries were derived from the same parquet, but they supply a useful checked interpretation: presynaptic GABA synthesis, vesicle loading, reuptake, and catabolism were nearly all self-only or fully null at snRNA resolution.

## Gad1 prediction

`Gad1` encodes GAD67, the major basal glutamate decarboxylase for GABA synthesis, whereas `Gad2` encodes the GAD65 isoform enriched in regulated synaptic pools. The external prior therefore does not make `Gad2` a perfect equivalent: germline `Gad1` loss is more severe than germline `Gad2` loss. In a dense developmental or GABAergic-neuron experiment I would expect Gad1 to be at least as consequential as Gad2 for inhibitory transmitter supply.

The requested endpoint, however, is not GABA content, seizure tendency, vesicle filling, synaptic current, or developmental survival. It is the number of corrected nuclear DE rows 3-4 weeks after sparse P16 CRISPR in recovered `151 TH Prkcd Grin2c Glut` nuclei, a glutamatergic thalamic class. At the intervention stage, `Gad1` loss reduces capacity for GABA synthesis. The next direct molecular consequence is presynaptic GABA availability in cells that use the GABA pathway. Propagation to this readout would require a change in inhibitory chemistry to persist in assayed recovered nuclei and then become a soma-wide transcriptional program large enough for FDR correction. In the training data, that propagation step is the failing link: `Gad2`, `Slc32a1`, `Slc6a1`, and `Abat` all perturb adjacent GABA production/loading/clearance chemistry yet produce zero FDR < 0.05 genes in the focal class, and even in inhibitory classes `Gad2`, `Slc32a1`, and `Slc6a1` mostly show only their own transcript or a single isolated downstream row.

The receptor-subunit perturbations are biologically relevant counterexamples, not better Gad1 analogs. `Gabrb2` loss in 151 TH Prkcd Grin2c Glut creates a small immediate-early/neuropeptide response consistent with postsynaptic loss of inhibition and disinhibition-driven nuclear signaling. `Gabra1` and `Gabrg2` show that even receptor-subunit losses with strong self-transcript depletion can be self-only at this threshold. Gad1 is upstream of transmitter synthesis, held out from the perturbation universe, and likely mismatched to this glutamatergic focal group, so I did not transfer the 4-gene `Gabrb2` burden to it.

I therefore predict `Gad1` will be a focal-class null with:

```tsv
target_name	predicted_n_degs
Gad1	0
```

## Limits and uncertainty

This is an extrapolation from `Gad2` and neighboring GABA-axis perturbations because `Gad1` itself was completely held out. The most important imperfection is that GAD67 is the basal isoform and has a stronger germline knockout phenotype than GAD65, so a clean, dense `Gad1` knockout in GABAergic neurons could have a larger molecular consequence than `Gad2`. The task's mosaic postnatal snRNA endpoint and glutamatergic focal class make that external severity a poor predictor of a large corrected DEG count.

The prediction also cannot exclude an effect outside nuclear mRNA: GABA content, vesicle filling, phasic release, extracellular GABA, inhibitory postsynaptic currents, pre-assay cell selection, and glial responses were not directly measured. The zero means only that no measured nuclear gene is predicted to pass BH-adjusted Wilcoxon FDR < 0.05 in recovered `151 TH Prkcd Grin2c Glut` nuclei.
