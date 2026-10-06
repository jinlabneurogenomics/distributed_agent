# DEG-count prediction trace

## Question and endpoint

The task asks for a point prediction of `n_degs` for each held-out genetic perturbation in `151 TH Prkcd Grin2c Glut` thalamic glutamatergic neurons. I treated `n_degs` as the exact training endpoint: the number of measured genes in the focal cell class with `pvals_adj < 0.05` after Wilcoxon testing and BH correction. The requested perturbation, `Pafah1b1`, is absent from both visible inputs, so its count is absent from the declared data and has to be transferred from visible perturbations.

The endpoint is a directly observed count for visible training perturbations and is absent for `Pafah1b1`. The expression signatures of visible analogs are directly observed; their relationship to `Pafah1b1` is a biological transfer, not direct replication.

## Sources used

- Declared Perturb-seq DE parquet, `training differential-expression dataset`, for focal-cell differential-expression rows and significant-gene counts.
- Declared training-count CSV, `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`, for exact `pvals_adj < 0.05` DEG counts of visible perturbations.
- Requested-target CSV, `single-target request for Pafah1b1`, for the one requested target and its required output order.
- Run-local dataset portrait, task bindings, compact coverage, and measurement registry, which define the focal cell class, the readout, and the fact that same-experiment corpus reports are interpretations of the same Perturb-seq experiment.
- The July PerturbAI same-experiment Findings corpus, release `perturbai-july-260713-sourceguard-1773-v1`, queried through `corpus.findings`, `corpus.calibration`, and `corpus.report_evidence`, for bounded interpreted summaries of the visible `Dctn1`, `Reln`, and `Dab1` perturbations.
- External literature from PubMed and the packaged Dctn1 report references:
  - Hirotsune et al. 1998, Nat Genet, doi:10.1038/1221, PMID:9697693.
  - Gambello et al. 2003, J Neurosci, doi:10.1523/JNEUROSCI.23-05-01719.2003, PMID:12629176.
  - Tai et al. 2002, J Cell Biol, doi:10.1083/jcb.200109046, PMID:11889140.
  - Yamada et al. 2009, EMBO J, doi:10.1038/emboj.2009.378, PMID:20019668.
  - Pandey and Smith 2011, J Neurosci, doi:10.1523/JNEUROSCI.4108-11.2011, PMID:22114287.
  - Moughamian and Holzbaur 2012, Neuron, doi:10.1016/j.neuron.2012.02.025, PMID:22542186.

## Computation over visible data

I used the training-count CSV for the focal endpoint and filtered the parquet to `group_name = '151 TH Prkcd Grin2c Glut'` for the specific visible analogs. The non-obvious checks were:

```sql
SELECT gene_target,
       sum(CASE WHEN pvals_adj < 0.05 THEN 1 ELSE 0 END) AS n_sig_151
FROM read_parquet($training_de)
WHERE group_name = '151 TH Prkcd Grin2c Glut'
  AND gene_target IN ('Dctn1','Reln','Dab1','Dync2h1','Dync2i1',
                      'Map1b','Mapt','Map6','Map2k1')
GROUP BY gene_target;
```

and a second focal query that read the `Dctn1` significant genes and selected marker genes from the candidate comparators. These checks confirmed that:

- The requested list contains only `Pafah1b1`, and `Pafah1b1` is not a visible training target.
- `Pafah1b2`, `Pafah1b3`, `Nde1`, `Ndel1`, `Nudc`, `Dync1h1`, `Dync1i1`, `Dync1i2`, `Dync1li1`, and `Dync1li2` are also absent as visible perturbations.
- The exact focal `FDR < 0.05` training counts for the visible anchors were: `Dctn1` 75, `Mib1` 27, `Rab7` 501, `Tsc2` 86, `Vps35` 17, `Marchf6` 14, `Srebf2` 7, `Htt` 3, `Reln` 0, `Dab1` 0, `Vldlr` 0, `Lrp8` 0, `Fyn` 0, `Gsk3b` 6, `Dync2h1` 0, `Dync2i1` 0, `Map1b` 1, `Mapt` 1, `Map6` 0, `Kif2a` 0, `Tuba1a` 7, `Tuba4a` 2, and `Tubb5` 1.
- `Dctn1` had 182 matched perturbed nuclei versus 23,679 controls in the focal cell class and produced 75 focal `FDR < 0.05` genes. The leading positive genes were sterol/lipid-feedback genes: `Insig1` logFC 1.16, `Msmo1` 1.10, `Hmgcs1` 0.86, `Cyp51` 0.74, `Hmgcr` 0.78, `Fdft1` 1.14, `Fasn` 0.87, `Sqle` 0.98, `Dhcr24` 0.73, `Ldlr` 1.46, and `Fdps` 1.00. The response also downregulated neuronal or cytoskeletal genes such as `Plekhg1`, `Kcnc2`, `Stmn4`, `Syt11`, `Grin2b`, `Jun`, and `Jund`.
- Focal `Dctn1` sterol genes moved in the same direction under visible endolysosomal or lipid-feedback perturbations and in the opposite direction under `Srebf2`. For example, `Mib1`, `Rab7`, `Marchf6`, `Htt`, and `Tsc2` all increased `Insig1`, `Msmo1`, `Hmgcs1`, `Hmgcr`, `Fdft1`, `Ldlr`, `Sqle`, and `Dhcr24`, whereas `Srebf2` decreased those genes. The July Dctn1 report summarized the same state as a recurrent SREBF2-like cholesterol-biosynthesis and uptake module with broader fatty-acid/lipid remodeling and a limited lysosome/autophagy/proteostasis echo.

## Target-specific prediction

### Pafah1b1

The closest perturbation chain I used was:

`Pafah1b1/LIS1 loss -> impaired LIS1 regulation of cytoplasmic dynein and dynactin -> perturbed retrograde organelle and vesicle transport, including lysosomal/autophagosomal traffic -> sterol and membrane-lipid feedback in recovered neurons -> focal snRNA differential-expression breadth`.

`Dctn1` is the best visible within-dataset analog. DCTN1 is a structural dynactin subunit required for dynein-dependent retrograde vesicle/organelle transport, and LIS1 physically and functionally regulates the dynein-dynactin motor system. Tai et al. showed LIS1 association with dynein and dynactin; Moughamian and Holzbaur showed that dynactin initiates retrograde transport from distal axons; Yamada et al. placed LIS1 in dynein/dynactin transport by kinesin-1; and Pandey and Smith showed a mature-neuron Lis1/Ndel1/dynein switch for acidic-organelle transport in adult axons. In the same experiment, `Dctn1` caused 75 focal DEGs at `FDR < 0.05`, and its report records a sterol/lipid response concentrated in 151 and several caudal/hypothalamic groups. That makes `Dctn1` endpoint-bearing evidence for a nonzero `Pafah1b1` response, because both perturbations are expected to impair the same limiting cytoplasmic dynein transport machinery rather than merely sharing a broad pathway label.

The count should be below `Dctn1`, not at or above it. `Dctn1` directly damages dynactin, whereas `Pafah1b1` is a dynein regulator with timing- and cargo-dependent effects. The strongest Pafah1b1 biology in mouse is embryonic and dose-sensitive: Hirotsune et al. and Gambello et al. showed that reduced Pafah1b1 disrupts neuronal migration, progenitor nuclear migration, and survival during cortical development. In this Perturb-seq assay the intervention starts at P16 and the readout is 3-4 weeks later in recovered postmitotic neurons, so the embryonic migration and progenitor-survival pieces of the Pafah1b1 phenotype are mostly outside the assayed causal window. The visible Reelin-core developmental-migration branch supports this caution: `Reln`, `Dab1`, `Vldlr`, `Lrp8`, and `Fyn` all had 0 focal DEGs, and the July `Reln`/`Dab1` reports showed that the Reelin adaptor/receptor perturbations were flat or nearly flat after juvenile sparse CRISPR despite their strong developmental positioning phenotypes. Visible generic microtubule genes were also far weaker than `Dctn1`: `Map1b` 1, `Mapt` 1, `Map6` 0, `Kif2a` 0, `Tuba1a` 7, `Tuba4a` 2, and `Tubb5` 1 focal DEGs. Those are counterexamples to predicting a large footprint from lissencephaly, migration, or microtubule membership alone.

I therefore predicted a moderate, nonzero focal footprint: enough to recover part of the `Dctn1`/SREBF2 lipid-feedback state through dynein-organelle transport failure, but attenuated because LIS1 loss is an upstream regulatory perturbation in mature recovered neurons rather than direct loss of the dynactin scaffold. The point estimate is 40 DEGs, roughly half of the visible `Dctn1` count and above the sparse `Htt`/`Srebf2`/`Vps35` comparators, but below `Tsc2` and far below the broad `Rab7` state whose lysosomal cholesterol role is more direct.

## Limits

The main uncertainty is that no close LIS1-complex or cytoplasmic-dynein-chain perturbation was visible: `Pafah1b2`, `Pafah1b3`, `Nde1`, `Ndel1`, `Nudc`, `Dync1h1`, `Dync1i1`, `Dync1i2`, `Dync1li1`, and `Dync1li2` were all absent from the focal training-count table. `Dctn1` is a mechanistically close transport analog but not an obligate member of a LIS1 stoichiometric complex, so the DEG breadth has to be extrapolated. The same-experiment corpus summarizes many Dctn1 effects at `FDR < 0.10`, while the requested count uses `FDR < 0.05`; I used the raw parquet and the focal training CSV for the exact endpoint and the corpus only for bounded interpretation. Finally, the literature most strongly establishes Pafah1b1 function during embryonic neuronal migration, but the requested experiment perturbs sparse juvenile postmitotic neurons and measures only survivor nuclear RNA, so morphology, axonal transport, selection before recovery, and local organelle defects could be present without a proportional DEG count.
