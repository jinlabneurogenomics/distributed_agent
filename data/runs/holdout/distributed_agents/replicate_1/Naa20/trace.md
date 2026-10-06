# DEG-count prediction for `151 TH Prkcd Grin2c Glut`

## Question and resolved ambiguities

The requested held-out perturbation is `Naa20`. I interpreted the endpoint as the integer `n_degs`: the count of measured genes in `151 TH Prkcd Grin2c Glut` nuclei with BH-adjusted Wilcoxon `pvals_adj < 0.05` after acute mosaic AAV-CRISPR loss of the target gene. The held-out `Naa20` expression signature itself is absent from the supplied Parquet and from the focal training-count CSV, so I did not use a same-target readout.

The endpoint is directly observed only for the 1,674 non-held-out perturbations in `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`. The all-cell Parquet is the corresponding measured-gene differential-expression surface for those same visible perturbations. Same-experiment reports in the internal `perturbai-july-260713-sourceguard-1773-v1` corpus were treated as curated summaries of those visible measurements, not as independent replication. External literature from NCBI PubMed was used only to decide whether a visible perturbation is a mechanistically suitable analog for `Naa20`.

## Quantitative checks

I read the held-out manifest at `single-target request for Naa20`; it contains exactly:

```tsv
target_name
Naa20
```

The focal training-count file has 1,674 perturbations. Its `n_degs` distribution is highly sparse: 1,205 perturbations have 0 focal DEGs, the median is 0, the mean is 14.05, and the maximum is 2,677 (`Uba5`). Thus the prior for an arbitrary held-out perturbation in this focal class is a zero-DEG call unless a close, visible loss-of-function analog argues otherwise.

I ran the declared Perturb-seq feature summarizer over the full 616,253,184-row training Parquet and materialized `workbench/features.parquet`. At target level, the only visible N-terminal-acetyltransferase-family member matching `^Naa|^Nat` was `Naa10`, with `n_fdr_005 = 0` and `n_fdr_010 = 0` across the full cached all-cell summary. I then filtered the declared Parquet to the exact focal class and selected visible comparators:

```python
ds.dataset(training_de_all_cell_groups.parquet, format="parquet").to_table(
    columns=["names", "gene_target", "logfoldchanges", "scores",
             "pvals", "pvals_adj", "n_pert_matched", "n_ctrl_matched"],
    filter=(
        (ds.field("group_name") == "151 TH Prkcd Grin2c Glut")
        & ds.field("gene_target").isin(["Naa10", "Hspa8", "Crebbp",
                                        "Ep300", "Eif5a"])
    ),
)
```

This yielded these focal analog/counterexample observations:

| visible perturbation | focal `n_degs` | matched perturbed nuclei | focal expression-pattern evidence | relevance to `Naa20` |
| --- | ---: | ---: | --- | --- |
| `Naa10` | 0 | 240 | no FDR < 0.05 gene in 17,259 focal measured genes; minimum adjusted p-value 1.0 | closest visible Nat-family perturbation, but it is NatA catalytic rather than NatB |
| `Eif5a` | 0 | 189 | no FDR < 0.05 gene; minimum adjusted p-value 0.0708 | abundant translation-related protein; weak counterexample showing translation-associated genes need not produce focal DEGs |
| `Hspa8` | 9 | 97 | small heat-shock/chaperone response headed by `Dnaja1`, `Hspa4l`, `Syt4`, `Hsp90aa1` | broader proteostasis counterexample, not NatB-specific |
| `Crebbp` | 8 | 61 | small chromatin/transcription response headed by `Stxbp2` | generic acetyltransferase counterexample; not an N-terminal acetyltransferase |
| `Ep300` | 0 | 155 | no FDR < 0.05 gene; minimum adjusted p-value 1.0 | paralog of `Crebbp`, useful only to show weak responses can occur even for canonical acetyltransferases |

The internal July corpus gave the same visible `Naa10` interpretation: `Naa10:F001` summarized postmitotic P16 `Naa10` perturbation as a pan-neuronal FDR-level null across 22 measured neuronal groups with 2,123 total matched perturbed nuclei and zero downstream genes at FDR < 0.10; `Naa10:F002` reported no Nat-family, integrated-stress, apoptosis, or proteasome/ubiquitin rebound program at FDR < 0.10; and `Naa10:F004` placed `Naa10` among flat full-vector neighbors rather than responsive proteostasis or translation targets.

## Target-specific biological reasoning

### `Naa20`

`Naa20` encodes the catalytic subunit of NatB. NatB is a two-subunit N-terminal acetyltransferase in which the NAA25 auxiliary subunit holds and stabilizes NAA20, and the NAA20 active site acetylates nascent proteins whose N termini fit the canonical NatB substrate class. This catalytic/auxiliary relationship is structural and direct: Hong et al. 2017 solved a NatB holoenzyme and showed how Naa25 positions Naa20 and how Naa20 residues determine NatB substrate specificity for Met-Asp/Glu/Asn/Gln peptides (DOI 10.1016/j.str.2017.03.003; PMID 28380339). Lasa et al. 2020 further showed that NAA20 N-terminal maturation is required for NAA25 interaction and NatB complex formation (DOI 10.1016/j.jmb.2020.09.010; PMID 32976911). Human recessive hypomorphic NAA20 variants impair NatB complex formation and catalytic activity and cause developmental delay, intellectual disability, and microcephaly, supporting a real neurodevelopmental role for NatB loss rather than a dispensable enzyme (Morrison et al. 2021, DOI 10.1038/s41436-021-01264-0; PMID 34230638).

The cleanest within-dataset analog would have been `Naa25`, because loss of either NAA20 or NAA25 should impair the same obligate NatB activity. `Naa25` was not in the visible focal training counts, and neither were `Naa15`, `Naa30`, `Naa35`, `Naa40`, `Naa50`, `Naa60`, `Metap1`, or `Metap2` under those symbols. The only visible Nat perturbation was `Naa10`. `Naa10` is a counterexample more than an anchor: it is the NatA catalytic subunit, acts with NAA15/HYPK, and acetylates a larger but different fraction of N termini than NatB. Human genetics nevertheless argues that NatA loss is at least as neurodevelopmentally consequential as NatB loss: Cheng et al. 2018 reported NAA15 truncating variants in intellectual disability, autism, and congenital anomalies (DOI 10.1016/j.ajhg.2018.03.004; PMID 29656860), while NAA10 variants cause Ogden/NAA10-related neurodevelopmental disease. In this Perturb-seq experiment, however, acute postnatal sparse `Naa10` perturbation was completely silent in the focal cell class and across all visible neuronal groups.

The causal transfer chain is therefore:

`Naa20` CRISPR loss -> reduced NatB catalytic capacity -> altered cotranslational N-terminal acetylation of the NatB substrate subset -> possible changes in substrate stability, localization, or interactions -> transcriptional adaptation in recovered postnatal thalamic glutamatergic neurons -> single-nucleus Wilcoxon DEG count.

The first two steps are well supported externally. The later steps are weak in this assay. NatB loss can matter over development, but the requested perturbation is a partial, mosaic, P16 neuronal loss measured 3-4 weeks later in recovered nuclei. The most relevant visible perturbation, `Naa10`, did not trigger any integrated-stress, NAT-compensation, proteasome, or apoptosis program, even though NatA dysfunction is externally neurodevelopmental. That within-experiment null makes a broad, FDR-detectable NatB survivor-state response unlikely unless `Naa20` has an idiosyncratic postnatal thalamic NatB substrate not tested by `Naa10`; I did not find visible training evidence for such a substrate-specific route.

I therefore predict `Naa20` as a zero-DEG perturbation in `151 TH Prkcd Grin2c Glut`. The call is driven mainly by the visible `Naa10` null and the zero-heavy training distribution, with external NatB/NatA literature used to judge that `Naa10` is related but imperfect rather than an exact same-complex proxy.

## Limits

The evidence is weak because `Naa25`, the obligate NatB partner, is not a visible training perturbation. `Naa10` is informative about the local assay's tolerance of N-terminal acetylation perturbation but it is not a NatB subunit and could miss NatB-specific substrates. Germline and patient evidence for NatB and NatA dysfunction supports organismal and developmental importance, but that does not directly establish an FDR-level transcriptional response after partial postnatal AAV-CRISPR editing of thalamic glutamatergic neurons. The prediction is therefore a low-response extrapolation, not a claim that NAA20 is biologically unimportant or that editing would fail.
