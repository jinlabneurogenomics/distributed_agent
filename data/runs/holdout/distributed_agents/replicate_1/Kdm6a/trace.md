# Trace

## Question and endpoint

The requested target set contains one held-out perturbation:

- `Kdm6a`

I interpreted the task as a point prediction of `n_degs` in `151 TH Prkcd Grin2c Glut`: the number of measured genes whose Wilcoxon Benjamini-Hochberg adjusted p value would be below 0.05 after acute P16 AAV CRISPR loss of `Kdm6a`, assayed by snRNA-seq at P37-P44 against matched non-targeting controls.

The endpoint is directly observed for the non-held-out training perturbations in `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`, but is absent for `Kdm6a`; the held-out `Kdm6a` expression signature is also absent from `training_de_all_cell_groups.parquet`. The prediction is therefore an extrapolation from visible perturbations plus external biology. I did not treat target-transcript fold change as editing efficiency, because the dataset context explicitly cautions that self-knockdown is uncorrelated with downstream response in this modality.

## Sources used

- Declared training DEG counts: `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
- Declared differential-expression parquet: `training differential-expression dataset`.
- Run-local requested-target manifest: `single-target request for Kdm6a`.
- PerturbAI July sourceguard same-experiment corpus, release `july_260713_sourceguard_1773_v1`, for compact Finding-level interpretations of the visible `Kdm6b`, `Kdm5c`, `Kmt2a`, and `Kmt2c` reports. This corpus is a curated representation of the same experiment, not independent replication.
- PubMed literature for target biology:
  - Tran, Broun & Ge 2020, DOI `10.1128/MCB.00341-20`, PMID `32817139`: KDM6A/UTX is an H3K27me2/3 demethylase, can work with MLL3/KMT2C and MLL4/KMT2D enhancer methyltransferase complexes, and has context-dependent catalytic and noncatalytic activities.
  - Shpargel et al. 2012, DOI `10.1371/journal.pgen.1002964`, PMID `23028370`: UTX/KDM6A and UTY can be redundant in mouse embryonic development even though UTY lacks in vivo H3K27 demethylase activity.
  - Shpargel et al. 2017, DOI `10.1073/pnas.1705011114`, PMID `29073101`: neural-crest deletion shows demethylase-independent KDM6A/UTY functions in Kabuki craniofacial phenotypes.
  - Lei & Jiao 2018, DOI `10.1016/j.stemcr.2018.02.008`, PMID `29551674`: embryonic cortical neural-stem-cell UTX loss perturbs proliferation/differentiation through PTEN signaling.
  - Koizumi et al. 2022, DOI `10.1096/fj.202201002RR`, PMID `36412518`: neural-stem/progenitor UTX loss impairs embryonic neural development, differentiation, and neonatal survival.

## Quantitative checks

I first summarized the visible endpoint distribution from the training count CSV. It has 1,674 visible perturbations in the focal cell group, with 1,205 zeros and only 469 nonzero counts; the median is 0, the 90th percentile is 2, the 95th percentile is 18, and the top responses are a small right tail (`Uba5` 2677, `Tpr` 1768, `Sin3a` 1433). This makes zero the prior for a held-out perturbation unless the visible neighborhood gives a stronger same-endpoint reason to call a response.

For expression-pattern evidence, I read the Parquet row groups whose `group_name` statistics overlapped `151 TH Prkcd Grin2c Glut` and then restricted to the chromatin and KDM6-related visible targets. This recovered the FDR 0.05 focal signatures and their signed log fold changes without scanning unrelated cell groups. The relevant focal counts were:

| visible perturbation | focal `n_degs` | relationship to `Kdm6a` |
|---|---:|---|
| `Kdm6b` | 0 | same KDM6 H3K27 demethylase subfamily; best visible paralog |
| `Kmt2c` | 0 | MLL3, the closest visible member of KDM6A-associated MLL3/MLL4 enhancer complexes |
| `Ep300` | 0 | enhancer/chromatin acetyltransferase; indirect counterexample |
| `Kat6a` | 0 | chromatin acetyltransferase; indirect counterexample |
| `Kat6b` | 0 | chromatin acetyltransferase; indirect counterexample |
| `Kdm5b` | 0 | H3K4 demethylase paralog of `Kdm5c`; indirect |
| `Ash1l` | 1 | histone methyltransferase; only the self transcript passed FDR |
| `Crebbp` | 8 | enhancer acetyltransferase with a small focal signature |
| `Setd5` | 9 | chromatin-associated NDD gene with a small focal signature |
| `Kdm5c` | 18 | X-linked H3K4 demethylase NDD gene; sparse derepression module |
| `Setdb1` | 22 | H3K9 methyltransferase; sparse chromatin signature |
| `Kmt2a` | 24 | MLL1 H3K4 writer; sparse and nonconvergent with `Kmt2c`/`Kdm5c` |
| `Chd8` | 61 | NDD chromatin remodeler; moderate but indirect |
| `Zmynd8` | 74 | RACK7 enhancer regulator that phenocopies part of `Kdm5c`, not KDM6A |
| `Smarcc2` | 185 | BAF-complex perturbation; broader thalamic signature, indirect |
| `Setd1a` | 368 | SET1-family H3K4 writer; broad and non-overlapping with KDM5C/KMT2A |
| `Phf12` | 403 | SIN3/HDAC-associated repressor; broad, indirect |
| `Sin3a` | 1433 | SIN3 corepressor; broad, indirect |

The direct `Kdm6b` evidence was the strongest same-family evidence. Its FDR 0.05 `151` count was exactly 0. The July same-experiment report summarized that acute postnatal `Kdm6b` loss was FDR-null across all recovered neuronal groups, despite prior developmental, activity-dependent, and inflammatory KDM6B biology. Its report also contrasted the null against visible chromatin perturbations such as `Setd1a`, `Smarcc2`, `Rora`, `Kmt2a`, `Setdb1`, `Kdm5c`, `Crebbp`, and `Setd5`, showing that the focal thalamic population and Wilcoxon pipeline were capable of detecting chromatin-regulator responses.

The MLL3/MLL4 enhancer-complex evidence also pointed low. External reviews place KDM6A in MLL3/KMT2C and MLL4/KMT2D enhancer complexes, so `Kmt2c` is the closest visible complex-side analog. `Kmt2c` had 0 DEGs in the focal group, and the same-experiment report described acute P16 `Kmt2c` loss as broadly buffered, with only one FDR 0.10 downstream gene across the measured groups and essentially no validated signature neighbor. `Kmt2d`, the other close writer partner and the gene more commonly paired with KDM6A in Kabuki syndrome, was not visible in the training set, so this is incomplete complex coverage.

The positive chromatin counterexamples were weaker analogs. `Kdm5c` had 18 focal FDR genes dominated by up-regulated `Ptgds`, `Capn3`, `Man2a2`, `Zfp532`, `Col9a3`, `Usp11`, `Zmynd8`, `Hexim2`, `Ank1`, `Msra`, `Dusp27`, `Catsperz`, and `Kcnk4`; the July report interpreted this as a narrow loss-of-repression module that was recapitulated by `Zmynd8` but not by `Kdm5b`, `Rest`, `Kmt2a`, or `Kmt2c`. Thus `Kdm5c` is informative that an X-linked intellectual-disability chromatin regulator can produce a small `151` response, but its H3K4-demethylase/RACK7 module is not a mechanistic reason to expect the H3K27 demethylase `Kdm6a` to share the same genes.

`Kmt2a` had 24 focal FDR genes, with down-regulated neuronal identity/connectivity genes such as `Nr2f1`, `Pcdh7`, `Lhx9`, `Camk2d`, `Pcdh10`, `Atp2c1`, and `Grik2`, and a separate induced module including `Igfbp5`, `Tnr`, `Cx3cl1`, `Atxn2l`, `Luc7l`, `Kalrn`, and `Txndc5`. The July report explicitly found that `Kmt2a` did not phenocopy `Kmt2c` or `Setd1a`, so I treated it as a sparse chromatin counterexample rather than as direct evidence that all MLL/COMPASS-related factors should get a nonzero call.

Finally, the extremes `Setd1a`, `Phf12`, and `Sin3a` show that some chromatin perturbations cause hundreds to thousands of focal DEGs. They are important assay positive controls, but they are not paralogs, not members of the KDM6 H3K27 demethylase family, and do not transfer through an obligate KDM6A complex. Broad chromatin identity alone would overpredict relative to the direct `Kdm6b` and `Kmt2c` nulls.

## Target-specific prediction

### `Kdm6a`

Biological model:

`Kdm6a` perturbation removes UTX function in sparsely edited postmitotic juvenile neurons. The direct molecular consequences are reduced KDM6A H3K27me2/3 demethylase activity and loss of KDM6A noncatalytic enhancer/coregulator functions. These can propagate through selected enhancer programs, often in cooperation with MLL3/MLL4 complexes, but the experiment observes only nuclei that survive 3-4 weeks after P16 AAV editing and have a stable `151 TH Prkcd Grin2c Glut` identity. Germline, embryonic progenitor, neural-crest, tumor, and injury functions do not automatically transfer through this chain because they act at different differentiation states or under inflammatory/proliferative stimuli.

Analog transfer:

- `Kdm6b` predicts the same histone-mark direction and is the best visible paralog. It had `n_degs = 0` in the exact focal endpoint and was null across every recovered neuronal group in the internal July corpus. This is a same-subfamily, same-assay argument that acute basal H3K27 demethylase loss can be buffered in these postmitotic neurons.
- `Kmt2c` tests the visible MLL3 side of the KDM6A enhancer complex. It had `n_degs = 0` in `151`, so the closest visible enhancer-partner perturbation also did not give a detectable focal response.
- `Ep300`, `Kat6a`, `Kat6b`, `Kdm5b`, and most other enhancer/chromatin analogs were also zero; `Crebbp`, `Setd5`, `Kdm5c`, `Setdb1`, and `Kmt2a` gave only 8-24 DEGs. These small positives leave room for a weak `Kdm6a` effect, but their expression modules were mechanistically different.
- `Setd1a`, `Phf12`, and `Sin3a` were large positive controls, not close transfer evidence.

The external prior says `Kdm6a` is biologically real in neural development: UTX controls embryonic neural stem/progenitor differentiation in mice, Utx-deficient neural progenitors show altered DNA-replication and differentiation programs, and KDM6A mutations cause Kabuki syndrome. Those studies mostly involve embryonic progenitors, neural crest, or chronic developmental deletion. Shpargel et al. also showed partial noncatalytic redundancy with `Uty`; because the perturbation targets `Kdm6a` but not `Uty` in mixed-sex postnatal neurons, male nuclei in particular could be partially buffered. None of the external studies demonstrate that losing `Kdm6a` after P16 in already specified thalamic glutamatergic neurons should induce a basal, cell-autonomous snRNA-seq signature over the 3-4 week assay window.

I therefore predict a true zero at the endpoint: a `Kdm6a` perturbation may have small sub-FDR chromatin effects or context-gated phenotypes, but the best visible same-subfamily and same-complex analogs both sit at zero in the focal Wilcoxon count, and positive chromatin controls do not provide a candidate-specific reason to override that.

Final point prediction:

- `Kdm6a`: `0`

## Limits

- The `Kdm6a` perturbation and all of its expression rows were held out, so no target-specific same-experiment DE vector was available.
- `Kdm6b` is a paralog and `Kmt2c` is a complex-side analog, but neither is a strict obligate surrogate for KDM6A. KDM6A can have demethylase-independent activities and can work with KMT2D, which was absent from the visible perturbation set.
- The sex mixture matters for an X-linked target. UTY can buffer some UTX/KDM6A functions in male mice, but the input does not provide sex-stratified DE for `151` cells; averaging sexes could hide a female-biased weak response.
- The prediction is specific to sparse P16 CRISPR loss in recovered postmitotic NeuN+ nuclei and to a basal snRNA-seq/Wilcoxon DEG-count endpoint. It should not be read as a prediction about embryonic Kdm6a deletion, neural-stem-cell differentiation, neural crest, glia, inflammation, viability before harvest, or stimulus responses.
- A point estimate of 0 means no measured gene is expected to pass BH FDR 0.05, not that KDM6A is biologically irrelevant in thalamic neurons.
