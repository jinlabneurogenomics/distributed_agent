# Pdss1 DEG-count prediction trace

## Question and interpretation

The run manifest contains one held-out target:

```text
Pdss1
```

I interpreted the task as a point prediction for `n_degs`, the number of measured genes with `pvals_adj < 0.05` after acute AAV/CRISPR loss of the target in `151 TH Prkcd Grin2c Glut` nuclei. The count includes the target transcript itself if the target row passes the same FDR threshold; this is visible in the training set for focal-cell mitochondrial genes such as `Uqcrc2`, `Ndufs2`, `Ndufa10`, `Ndufb8`, `Sdha`, `Cyc1`, and `Tomm40`, whose one focal-cell hit is their own mRNA.

`Pdss1` was absent from the training count CSV, and the prediction below therefore transfers from non-held-out perturbations.

## Sources used

- Input training endpoint: `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
- Input differential-expression matrix: `[local file: training_de_all_cell_groups.parquet]`.
- Requested-target manifest: `[local file: 173_Pdss1.csv]`.
- Same-experiment internal corpus: Distributed Agents corpus release `perturbai-july-260713-sourceguard-1773-v1`.
- Same-experiment runtime profile-neighborhood check written to `profile_neighbors_coq5_uqcrc2_opa1.json`.
- External mechanism literature from PubMed:
  - Saiki et al. 2005, FEBS Journal, DOI `10.1111/j.1742-4658.2005.04956.x`, PMID `16262699`.
  - Nguyen et al. 2014, BBA Molecular and Cell Biology of Lipids, DOI `10.1016/j.bbalip.2014.08.007`, PMID `25152161`.
  - Doimo et al. 2014, Molecular Syndromology, DOI `10.1159/000362826`, PMID `25126048`.
  - Kawamukai 2015, Bioscience, Biotechnology, and Biochemistry, DOI `10.1080/09168451.2015.1065172`, PMID `26183239`.
  - Yen et al. 2020, BBA Bioenergetics, DOI `10.1016/j.bbabio.2020.148192`, PMID `32194061`.
  - Jurkute et al. 2022, NPJ Genomic Medicine, DOI `10.1038/s41525-022-00330-z`, PMID `36266294`.

## Dataset calibration

The focal-cell training endpoint has 1674 non-held-out perturbations. The endpoint is extremely zero-inflated:

- median `n_degs`: 0
- 75th percentile: 1
- 90th percentile: 2
- nonzero perturbations: 469/1674

This makes the zero/nonzero decision the main step; a pathway member needs strong same-experiment support before I should assign even a small positive integer.

I queried the focal-cell counts for direct CoQ and oxidative-phosphorylation comparators. The only represented direct CoQ-biosynthesis target was `Coq5`, and it was exactly null:

| comparator class | focal-cell training targets and `n_degs` |
| --- | --- |
| CoQ biosynthesis | `Coq5` 0 |
| Complex III / ubiquinol-cytochrome c oxidoreductase | `Uqcrb` 0, `Uqcrc2` 1, `Uqcrfs1` 0, `Uqcrh` 0, `Uqcrq` 1, `Cyc1` 1 |
| Complex I examples | `Ndufs4` 0, `Ndufv1` 0, `Ndufs2` 1, `Ndufa10` 1, `Ndufb8` 1 |
| Other mitochondrial controls | `Sdha` 1, `Tomm40` 1, `Timmdc1` 0, `Clpp` 0, `Lonp1` 0, `Opa1` 37 |

I then filtered the parquet to `group_name == "151 TH Prkcd Grin2c Glut"` for these comparators and counted `pvals_adj < 0.05`. This reproduced the CSV counts and showed that the one-gene Complex-I/III/TOMM/SDH calls were target-self rows or private singletons, not a mitochondrial stress module. For the closest same-pathway comparator, `Coq5`, the focal-cell details were:

- 200 perturbed nuclei and 23679 matched control nuclei.
- `n_degs = 0`.
- `Coq5` self row `logfoldchanges = -0.473`, `pvals_adj = 1.0`.
- No focal-cell ATF4/ISR or mitochondrial-UPR sentinel passed FDR; `Asns`, `Atf4`, `Atf5`, `Chac1`, `Clpp`, `Ddit3`, `Herpud1`, `Hspd1`, `Lonp1`, `Mthfd2`, `Shmt2`, `Slc7a5`, `mt-Co2`, `mt-Cytb`, `mt-Nd1`, and `mt-Nd5` all had `pvals_adj = 1.0`.

`Opa1` was an important counterexample. In the same focal group it produced `n_degs = 37`, including strong ATF4/ISR-like and respiratory rows: `Asns`, `Chac1`, `Ddit3`, `Mthfd2`, `Slc7a5`, `Herpud1`, and `mt-Co2` all passed FDR<0.05. So the expected mitochondrial-stress transcriptome is detectable by this Wilcoxon/snRNA workflow when an acute neuronal perturbation crosses the response threshold.

The Distributed Agents corpus supported the same calibration on the full same-experiment surface:

- `Coq5:F001`: `Coq5` had zero downstream genes at FDR<0.10 in all 22 measured neuronal groups, not just in the focal group.
- `Coq5:F002`: representative mitochondrial ISR/UPR genes were absent after `Coq5`; `Atf4`, `Ddit3`, `Trib3`, `Herpud1`, `Asns`, `Shmt2`, `Aldh1l2`, `Mthfd2`, `Lonp1`, `Hspd1`, `Hspa5`, and `Clpp` each had minimum FDR 1.0 across the measured `Coq5` groups.
- `Coq5:F003`: the direct respiratory and mitochondrial-proteostasis comparators represented in the parquet did not phenocopy `Coq5`; score-space Pearson correlations to `Coq5` in matched groups were near zero for `Uqcrfs1`, `Uqcrc2`, `Cyc1`, `Uqcrb`, `Ndufs2`, `Ndufc2`, `Clpp`, and `Lonp1`.
- `Uqcrc2` and `Ndufs4` corpus claims generalized this: represented nuclear Complex-III and Complex-I structural/assembly targets were largely transcriptionally buffered in neuronal nuclei, with weak or absent private responses rather than a shared acute OXPHOS-stress signature.

I also ran a local Distributed Agents runtime `profile_neighbors` check for `Coq5`, `Uqcrc2`, and `Opa1` in the focal group against all 1674 eligible training targets. `Coq5` had zero significant features in this exact context. Whole-logFC null-vector correlations were not used as positive evidence, because the nearest neighbors of a no-FDR signature are dominated by low-information signed noise.

## Pdss1 target reasoning

`Pdss1` encodes the mammalian long-chain trans-prenyl diphosphate synthase catalytic subunit. Saiki et al. showed that the mouse and human enzymes that set the ubiquinone side-chain length are heterotetramers of a Dps1/Pdss1-like and a Dlp1/Pdss2-like subunit; the mouse pair produces Q9 and the human pair produces Q10. This places `Pdss1` at the first committed polyprenyl-tail step of coenzyme Q biosynthesis.

The nearest observed perturbation is therefore `Coq5`, not a generic mitochondrial gene. `Coq5` catalyzes a C-methyltransferase step in CoQ biosynthesis and can assemble with the mitochondrial CoQ biosynthetic complex, as shown in yeast and human complementation/biochemistry by Barkovich et al. 1997 and Nguyen et al. 2014. Yen et al. 2020 further showed that human PDSS/COQ proteins influence CoQ10 abundance and the stability of other CoQ proteins. Human genetics also shows that defects in both PDSS/COQ genes can cause primary CoQ10 deficiency with neurologic or retinal phenotypes (Doimo et al. 2014; Jurkute et al. 2022).

Those external facts say `Pdss1` is a real CoQ gene, but they do not override the in-dataset null. In this assay:

- the only direct CoQ-biosynthetic target, `Coq5`, had `n_degs = 0` in the focal cell group;
- `Coq5` was null across essentially the whole neuronal panel, not just in one undersampled group;
- focal-cell Complex-I/Complex-III genes downstream of ubiquinone also sat at 0-1 DEGs, with their few hits dominated by on-target transcript decreases;
- focal-cell `Coq5`, `Uqcr*`, `Cyc1`, `Nduf*`, and `Sdha` perturbations did not induce the `Asns`/`Chac1`/`Ddit3`/`Slc7a5` stress state seen after `Opa1`.

I considered whether `Pdss1` could be stronger than `Coq5` because the prenyltransferase step sits at the entrance to the CoQ pathway and because PDSS1/PDSS2 can affect stability of a CoQ-synthome subcomplex. That is plausible biochemically, but the experiment is sparse, postmitotic, 3-4 weeks long, and uses gRNAs that on average only partially depress target mRNA. Under exactly those conditions, perturbing the later CoQ methyltransferase and perturbing direct ubiquinone-consuming respiratory complexes both failed to produce a corrected focal-cell RNA state. The more specific transfer is therefore the `Coq5`/OXPHOS buffered class, not the rare `Opa1` branch that affects mitochondrial inner-membrane architecture and crosses into an ATF4-like stress response.

## Prediction

`Pdss1`: predict no measured gene crossing FDR 0.05 in `151 TH Prkcd Grin2c Glut`.

Point prediction: **0**

## Limits

This is an extrapolation from adjacent genes, because `Pdss1`, `Pdss2`, `Coq2`, `Coq3`, `Coq4`, `Coq6`, `Coq7`, `Coq8a/b`, `Coq9`, and `Coq10a/b` were not available as focal-cell training perturbations. The CoQ analog is a single represented gene, `Coq5`; if `Pdss1` loss depletes CoQ faster than `Coq5` loss, or perturbs a PDSS-specific protein-stability branch not reached by `Coq5`, the zero call could be too low. The parquet also reports RNA effects only: it has no indel, protein, CoQ pool, oxygen-consumption, ROS, survival, or mitochondrial morphology readouts. I therefore use `n_degs = 0` only as a prediction that no single-nucleus RNA rows will pass the stated Wilcoxon FDR cutoff, not as a prediction that acute `Pdss1` editing is biologically inert.
