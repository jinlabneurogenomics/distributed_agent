# DEG-count prediction for held-out `Srrm2`

## Question and resolved ambiguities

I interpreted the task as a one-target scalar prediction: predict the number of measured genes in `151 TH Prkcd Grin2c Glut` whose perturbed-vs-control Wilcoxon test will have BH-adjusted `pvals_adj < 0.05` after acute postnatal CRISPR loss of `Srrm2`.  The requested manifest contains only:

```tsv
target_name
Srrm2
```

I treated the supplied per-gene parquet and the focal-cell training count CSV as the quantitative evidence.  `Srrm2` itself is absent from both training inputs, so the count cannot be read directly; I used measured training perturbations as analogs and used external biology only to decide which analogs are relevant.

Important endpoint choices:

- The target value is a gene-level abundance DEG count, not an alternative-splicing count.  This matters because `Srrm2` is first a splicing and nuclear-speckle factor, so a primary isoform defect may leave few total nuclear mRNAs significant.
- Target-transcript fold change was not used as an editing-efficiency filter.  It was used only as a downstream-feature observation when `Srrm2` itself appeared as a measured gene in other perturbations.
- I predicted a weak nonzero response, far below the hundreds-DEG spliceosome-core responses, rather than treating every spliceosome-associated annotation as interchangeable.

## Sources used

- `training_de_all_cell_groups.parquet`: row-level perturbation differential expression.  I filtered it to `group_name == "151 TH Prkcd Grin2c Glut"` and to RNA-processing candidate targets.
- `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`: exact focal-cell observed `n_degs` for training targets.
- Distributed Agents same-experiment corpus `perturbai-july-260713-sourceguard-1773-v1`: retrieved claims and findings around the Prpf6/Rnpc3/U2af2 RNA-processing module and the Son boundary.
- Distributed Agents local mouse gene-annotation store: `genes.parquet`, `gene_membership.parquet`, and `gene_relationships.parquet`; 18,123 genes, 464,095 memberships, 51,743 typed relationships.  `Srrm2` annotations came from GO, Reactome, CORUM 5.0 projected by MGI 1:1 orthology downloaded 2026-09-13, and STRING physical v12.0.
- Distributed Agents runtime profile tools: symmetric profile comparison and cohort diagnostics over selected focal-cell training signatures.
- External literature from PubMed:
- Ilik et al. 2020, DOI `10.7554/eLife.60579`, PMID `33095160`: SON and SRRM2 form the major nuclear-speckle organizing core; SRRM2 is the main SC35-antibody target.
- Zhang et al. 2024, DOI `10.1016/j.celrep.2024.113827`, PMID `38381607`: SRRM2 phase separation drives nuclear-speckle subcompartments and SRRM2/SON regulate partly distinct splicing target sets.
- Cuinat et al. 2022, DOI `10.1016/j.gim.2022.04.011`, PMID `35567594`: heterozygous human `SRRM2` loss-of-function variants cause a neurodevelopmental disorder.
- Tanaka et al. 2018, DOI `10.1038/s41380-018-0253-8`, PMID `30283027`: neuronal SRRM2 deficiency perturbs splicing of synapse-related genes in Alzheimer's-disease models.

## Computation over the input data

I first confirmed that the training count table has 1,674 non-held-out targets and that the distribution is highly sparse in this focal cell group:

- 1,205 / 1,674 targets have `n_degs = 0`.
- 363 have 1-9 DEGs.
- 63 have 10-99 DEGs.
- 43 have at least 100 DEGs.

I then pulled every focal-cell row for candidate RNA-processing perturbations and counted `pvals_adj < 0.05`, reproducing the training CSV exactly for these genes.  The strongest relevant counts were:

```tsv
target	n_degs
Rnpc3	868
U2af2	828
Hnrnpu	733
Cdc40	624
Tnpo3	618
Prpf6	454
Thoc1	303
Snrnp70	213
Tardbp	210
Hnrnpc	122
Hnrnpa2b1	11
Hnrnph2	4
Ascc3	18
Ctnnbl1	1
Rp9	4
Snrpn	1
Ylpm1	1
Son	0
Snrpb	0
Ddx39b	0
```

I also inspected `Srrm2` as a measured downstream transcript in these same perturbations.  It was significantly decreased by several broad RNA-processing perturbations: `U2af2` logFC -0.444, FDR `8.7e-17`; `Rnpc3` -0.620, FDR `4.5e-14`; `Cdc40` -0.448, FDR `1.3e-10`; `Tnpo3` -0.536, FDR `1.7e-10`; `Tpr` -0.602, FDR `7.3e-10`; `Ascc3` -0.408, FDR `7.6e-08`; `Thoc1` -0.322, FDR `2.6e-06`; and `Prpf6` -0.294, FDR `5.5e-03`.  It was not changed by `Son`, `Snrpb`, `Ddx39b`, `Snrpn`, `Ctnnbl1`, `Ylpm1`, or `Hnrnpc` in this cell group.

The runtime profile comparison was run on 22 selected RNA-processing and boundary nodes in `151 TH Prkcd Grin2c Glut`.  It compared all 231 node pairs on `logfoldchanges`, using `pvals_adj < 0.05` to label significant features.  This confirmed that the high-count spliceosome factors are partly co-directional, particularly for negative programs, while zero-count genes can still show moderate weak whole-profile correlations and should not be promoted by Pearson correlation alone.

## Candidate analogs and target-specific reasoning

### Broad spliceosome/RNA-processing responders: informative upper bounds

`Srrm2` was annotated to CORUM 5.0 spliceosome A/C/E complexes and the SRm160/300 complex by 1:1 human-to-mouse orthology.  The local annotation nominator ranked the training-available spliceosome factors `U2af2`, `Snrpb`, `Snrnp70`, `Prpf6`, and `Cdc40` as the most specific candidates.  STRING physical v12.0 also linked mouse `Srrm2` to `Cdc40`, `Prpf6`, `Ddx39b`, and `Snrpb`.

The same-experiment corpus strongly supports a real measured RNA-processing module among some of these nodes.  In the Distributed Agents Claim `claim:c85727b65aed9288f022`, the screen found that a subset of `Prpf6`/`Rnpc3`-adjacent RNA-splicing perturbations produced a shared same-direction neuronal DE module, but that this was not generic to every spliceosome-associated target.  The material findings reported that:

- `Prpf6` converged with `Cdc40`, `U2af2`, `Snrnp70`, and `Rnpc3`, with hundreds of shared same-direction FDR genes concentrated in `151 TH Prkcd Grin2c Glut` and `155 MB Glut`.
- `Rnpc3` converged with `Prpf6`, `Snrnp70`, `U2af2`, `Cdc40`, and `Hnrnpu`.
- `U2af2` had broad same-direction neighbors including `Prpf6`, `Cdc40`, `Tpr`, `Psmc1`, and `Psmb4`.

Those observations justify a nonzero prior for `Srrm2`: independent RNA-processing perturbations in the same focal cell type can yield hundreds of DEGs.  They are poor direct scale donors, though.  `U2af2`, `Rnpc3`, `Cdc40`, and `Prpf6` are required at recognition or catalytic spliceosome steps, whereas SRRM2 is an SR-related speckle scaffold and splicing regulator.  The screen itself shows that exact or adjacent complex membership does not guarantee a broad signature.

### Direct boundaries: `Son`, `Snrpb`, `Ddx39b`, and `Ctnnbl1`

The strongest biological counterexample is `Son`.  SON and SRRM2 are the literature-obvious nuclear-speckle core pair, yet in the focal cell group `Son` had 0 DEGs from 51 perturbed and 23,679 control nuclei.  The same-experiment corpus explicitly used `Son` as a boundary: the Distributed Agents `Son:F003` finding says `Son` did not phenocopy broad RNA-processing-factor loss, even though `Prpf6`, `U2af2`, `Hnrnpu`, `Snrnp70`, and `Tardbp` were far broader in the same P16 NeuN+ assay.  It also noted that `Srrm2` was not available as a perturbation comparator and that the measured `Srrm2` transcript was FDR-flat in all `Son` cell groups.

Other annotation-near but quiet spliceosome targets provide the same warning:

- `Snrpb`: direct CORUM spliceosome and STRING SRRM2 candidate; `n_degs = 0`.
- `Ddx39b`: STRING physical SRRM2 candidate and E-complex spliceosome annotation; `n_degs = 0` in `151 TH`.
- `Ctnnbl1`: spliceosome A-complex / Prp19-adjacent annotation; `n_degs = 1`.
- `Snrpn`: broad spliceosome-related annotation; `n_degs = 1`.

These are not all mechanistic phenocopies of SRRM2, but they are crucial negative controls because they show that the gene-level snRNA response is not guaranteed for every nuclear RNP or spliceosome-associated perturbation.

### Why the final prediction is weak but nonzero

I predict `Srrm2` will be much weaker than `U2af2`, `Rnpc3`, `Cdc40`, `Prpf6`, or `Snrnp70`, and also below the 122-DEG `Hnrnpc` response.  The downward evidence is strong: SRRM2 is scaffold-like, the endpoint ignores isoform defects, the acute postmitotic screen can buffer closely related factors, and the direct SON partner is completely flat in this focal group.

I did not set the count to zero for three reasons:

1. `Srrm2` is not just a generic speckle marker.  Ilik et al. showed that SRRM2 is a major nuclear-speckle organizer and the main SC35 target; Zhang et al. showed that SRRM2 drives speckle subcompartmentalization and has target subsets distinct from SON.  Thus the SON zero is a real boundary but not a proof of SRRM2 silence.
2. The best local exact-complex analog with an SRm160/300 link, `Snrnp70`, produced 213 DEGs, and the direct STRING/CORUM neighbors `Cdc40` and `Prpf6` produced 624 and 454.
3. `Srrm2` itself was repeatedly down-regulated as a measured transcript in the `U2af2`/`Rnpc3`/`Cdc40`/`Tnpo3` broad RNA-processing states, which places it inside the responsive arm of the measured program even though perturbing upstream spliceosome-core genes is expected to be more severe.

Putting those together, I used the zero-count `Son`/`Snrpb`/`Ddx39b` cases as the strongest scale boundaries and `Hnrnpa2b1` 11, `Hnrnph2` 4, `Rp9` 4, and `Ascc3` 18 as approximate weak/low-medium comparators.  I chose a point estimate of **8 DEGs**: weakly nonzero, close to the observed weak RNA-binding factors, and far below the core spliceosome wave.

## Limits of the reasoning

- The key close partner, `Srrm1`, was not in the training count table, so I could not measure the SRm160 side of the SRm160/300 complex.
- `Son` had only 51 perturbed nuclei in the focal group; its zero response is informative because other low-count perturbations such as `Prpf6` and `Psmb4` were broad, but it is still a low-power boundary.
- CORUM spliceosome memberships for SRRM2 are projected from human to mouse and include large assembly-state complexes.  They nominate candidates but overstate direct functional substitutability.
- The Wilcoxon gene-level endpoint can miss the primary biology of a splicing factor.  SRRM2 loss may alter retained introns, exon choice, or speckle architecture without pushing many total transcript abundances below FDR 0.05.
- Human SRRM2 haploinsufficiency and AD-model SRRM2 deficiency establish neuronal relevance, but they occur in different allelic, developmental, and disease contexts from P16-to-P37/44 mosaic CRISPR in thalamic glutamatergic neurons.
