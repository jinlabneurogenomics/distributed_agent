# Pafah1b1 DEG-count prediction

## Question and resolved ambiguities

The manifest for this run contains one held-out perturbation, `Pafah1b1`. I interpreted the task as a point prediction for the number of measured genes with `pvals_adj < 0.05` after acute AAV-PHP.eB CRISPR loss of `Pafah1b1` in the focal recovered neuronal group, `151 TH Prkcd Grin2c Glut`. I treated `151` as the thalamic glutamatergic Allen-taxonomy class identifier, not as a nucleus count.

The count is the exact assay endpoint in the training CSV, so the main calibration was from the 1,674 non-held-out perturbations in that file and the matching focal rows of the all-cell differential-expression parquet. External biology was used only to choose which training perturbations are appropriate mechanistic analogs or counterexamples.

## Sources used

- Training endpoint table: `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
- Training DE table: `[local file: training_de_all_cell_groups.parquet]`, filtered to `group_name = '151 TH Prkcd Grin2c Glut'`.
- Requested-target manifest: `[local file: 165_Pafah1b1.csv]`.
- Distributed Agents same-experiment corpus: `perturbai-july-260713-sourceguard-1773-v1`, queried with `story_count`, `search_claims`, `shared_claim_context`, and `expand_candidate_set`.
- Distributed Agents runtime expression-profile tool: `profile_neighbors`, run on the focal-cell parquet slice using signed `logfoldchanges`, `pvals_adj < 0.05`, and the 1,674 training targets as the eligible universe.
- External literature from PubMed:
  - Hirotsune et al. 1998, Nature Genetics, DOI `10.1038/1221`, PMID `9697693`.
  - Elshenawy et al. 2020, Nature Cell Biology, DOI `10.1038/s41556-020-0501-4`, PMID `32341547`.
  - Zhao et al. 2023, Nature Communications, DOI `10.1038/s41467-023-42907-x`, PMID `37940657`.
  - Singh et al. 2024, Science, DOI `10.1126/science.adk8544`, PMID `38547289`.
  - Moon and Wynshaw-Boris 2013, WIREs Developmental Biology, DOI `10.1002/wdev.67`, PMID `23495356`.
  - Pramparo et al. 2011, PLoS Genetics, DOI `10.1371/journal.pgen.1001331`, PMID `21423666`.

## Computational checks

The focal training table has 1,674 perturbations. Its response distribution is very zero-heavy: 1,205/1,674 targets have `n_degs = 0`, 363 are weak with 1-9 DEGs, 63 are medium with 10-89 DEGs, and only 43 have at least 100 DEGs. Thus a held-out target needs a close in-dataset reason to be moved away from zero.

I filtered the parquet to `151 TH Prkcd Grin2c Glut` and counted significant genes per training perturbation as:

```sql
select gene_target, count(*) filter (where pvals_adj < 0.05) as n_degs
from read_parquet($training_de)
where group_name = '151 TH Prkcd Grin2c Glut'
group by gene_target;
```

That slice contains 17,259 measured genes for each of 1,674 training targets, for 28,891,566 rows. The counts recomputed from the parquet matched the endpoint CSV for the inspected analogs.

I then seeded a signed focal expression-neighborhood run with `Dctn1`, `Ywhae`, `Map1b`, `Tuba1a`, `Tubb5`, `Cdc42`, `Dab1`, and `Reln`. The key observation was not that any whole-profile neighbor of `Dctn1` is a better biological surrogate for `Pafah1b1`, but that the `Dctn1` state is dominated by a sterol/cholesterol regulon while tubulin, kinesin, 14-3-3, and Reelin-pathway perturbations sit near the null endpoint.

## Target-specific reasoning

### `Pafah1b1`

`Pafah1b1` encodes LIS1, a dosage-sensitive dynein regulator. Heterozygous or hypomorphic mouse `Pafah1b1` alleles cause cell-autonomous neuronal migration defects, and human PAFAH1B1/LIS1 haploinsufficiency is a canonical cause of type I lissencephaly (Hirotsune et al. 1998; Moon and Wynshaw-Boris 2013). Biochemically, LIS1 is in the cytoplasmic dynein pathway: it promotes assembly of active dynein-dynactin-adaptor complexes, Nde1/Ndel1 modulate LIS1 recruitment and release, and a recent dynein-dynactin structure places LIS1 against dynactin p150/DCTN1 during efficient complex formation (Elshenawy et al. 2020; Zhao et al. 2023; Singh et al. 2024).

The best same-experiment analog is therefore `Dctn1`, the only clear dynein-1/dynactin structural target represented in the focal training endpoint. `Dctn1` has `75` DEGs, with 182 matched perturbed nuclei. Its leading significant changes include up-regulation of `Insig1`, `Msmo1`, `Hmgcs1`, `Cyp51`, `Hmgcr`, `Fdft1`, `Fasn`, `Sqle`, `Dhcr24`, `Stard4`, `Mvd`, `Lss`, `Dhcr7`, `Sc5d`, `Nsdhl`, `Ldlr`, `Fdps`, and `Idi1`, a coherent cholesterol-biosynthesis and uptake response, while the edited transcript itself is down (`Dctn1` log2FC `-0.59`, adjusted p `3.3e-11`). The Distributed Agents corpus independently summarized that same in-experiment surface in high-confidence claims: `Dctn1` elicits an SREBF2-like sterol/cholesterol biosynthesis module; that module is recurrent with `Mib1`, `Marchf6`, `Htt`, and `Selenoi`; and it is not a generic effect of every sampled cytoskeletal or trafficking perturbation.

The cholesterol-module neighborhood provides calibration but not a simple average. In this focal group, related recurrent sterol-output perturbations span `Mib1 = 27`, `Marchf6 = 14`, `Srebf2 = 7`, `Selenoi = 5`, and `Htt = 3`, with broader endolysosomal outliers such as `Rab7 = 501` and `Tsc2 = 86`. Since `Pafah1b1` is upstream of dynein/dynactin activation rather than a sterol regulator itself, these counts support a nonzero call but do not justify a `Rab7`-scale broad response.

Several counterexamples kept the estimate below the direct `Dctn1` count. First, same-screen tubulin and microtubule-neighborhood perturbations did not form a generic high-DEG state: `Map6 = 0`, `Nin = 0`, `Kif5a = 1`, `Map1b = 1`, `Mapt = 1`, `Tubb4b = 1`, `Tubb5 = 1`, `Tuba4a = 2`, and `Tuba1a = 7`. The corpus specifically notes that `Tuba1a` is read out mainly as tubulin-isotype dosage compensation, not as a DCTN1-like sterol response. Second, the 17p13.3/neuronal-migration branches adjacent to LIS1 are transcriptionally quiet under this P16 mosaic readout: `Ywhae = 0`, `Ywhag = 1`, `Ywhaz = 1`, `Reln = 0`, `Dab1 = 0`, `Lrp8 = 0`, `Vldlr = 0`, and `Fyn = 0`. The Distributed Agents Reelin claim likewise states that represented `Reln`/`Dab1`/`Vldlr`/`Lrp8` signaling is buffered in this postmitotic nuclear RNA assay. These are useful boundaries because classic embryonic neuronal-migration severity alone would overpredict many flat P16 perturbations.

I therefore predicted a medium response: high enough to reflect LIS1's close mechanistic position next to dynein-dynactin and the visible `Dctn1` sterol module, but lower than `Dctn1` because acute partial loss of a regulatory cofactor may leave more residual dynein transport than loss of the p150 dynactin scaffold in recovered postmitotic neurons.

Prediction: `48` DEGs.

## Limits

The closest measured analog, `Dctn1`, is a dynactin subunit, not `Pafah1b1` itself, and no `Dync1h1`, `Nde1`, `Ndel1`, `Pafah1b2`, or `Pafah1b3` training perturbation was available in the focal endpoint table. The predicted value is therefore an extrapolation from one direct dynein/dynactin component plus negative boundaries around less direct cytoskeletal and neuronal-migration pathways. The public literature is mostly developmental genetics or purified dynein biochemistry; those facts identify mechanism but do not determine the breadth of a sparse P16 AAV CRISPR snRNA-seq signature. Finally, `n_degs` is power- and survivor-conditioned, so this count should be read as a prediction of measured FDR hits among recovered thalamic neurons, not as a quantitative prediction of LIS1 biology, target engagement, or cell loss.
