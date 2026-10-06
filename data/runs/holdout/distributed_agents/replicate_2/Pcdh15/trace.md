# Prediction trace

## Question and endpoint

The held-out manifest contains one requested perturbation, `Pcdh15`. I interpreted the endpoint as:

- focal cell group: `151 TH Prkcd Grin2c Glut`
- perturbation: acute, sparse AAV-CRISPR loss of the named mouse gene at P16, assayed 3-4 weeks later by snRNA-seq
- scalar to predict: the total number of measured genes with `pvals_adj < 0.05` in the Wilcoxon DE table for that target and cell group
- the count includes the self-target transcript if that row passes FDR

`Pcdh15` is absent from both the focal training-count CSV and the all-cell DE parquet as a `gene_target`, so no held-out `Pcdh15` DEG count or expression signature was used.

## Sources used

- `[local file: 168_Pcdh15.csv]` for the requested target and row order.
- `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]` for exact observed focal-cell DEG counts of the 1,674 non-held-out perturbations.
- `[local file: training_de_all_cell_groups.parquet]` for focal-cell per-gene log-fold changes and FDR values.
- The internal Distributed Agents same-experiment corpus, release `perturbai-july-260713-sourceguard-1773-v1`, for packaged findings over this PerturbAI atlas.
- NCBI PubMed literature for external PCDH15 mechanism:
  - Ahmed et al. 2001, DOI `10.1086/321277`, PMID `11398101`
  - Webb et al. 2011, DOI `10.1242/dev.060061`, PMID `21427143`
  - Pepermans and Petit 2015, DOI `10.1016/j.heares.2015.05.005`, PMID `26049141`
  - Choudhary et al. 2020, DOI `10.1073/pnas.1920444117`, PMID `32963095`
  - Zhen et al. 2022, DOI `10.1038/s42003-022-03470-1`, PMID `35637313`
  - Mori et al. 2024, DOI `10.1038/s41398-024-02952-6`, PMID `38806495`

## Dataset operations

I read the training-count CSV directly and used the all-cell parquet only after filtering to the focal class and curated candidate targets. The parquet is row-grouped by `group_name`, so the expensive 616,253,184-row table did not need to be materialized.

The focal training endpoint was very sparse:

```text
0 DEGs      1205 targets
1 DEG        276 targets
2-9 DEGs      87 targets
10-99 DEGs    63 targets
100+ DEGs     43 targets
```

The relevant focal training counts were:

```text
Pcdh19 0
Adgrv1 0
Dscam 0
Cadm2 1
Cntnap1 1
Cntnap2 1
Nrxn1 1
Nrxn2 0
Nrxn3 0
Nlgn3 1
Adam22 1
Dlg4 1
Shank2 0
Shank3 2
Syngap1 0
Cacng2 0
Myo5a 1
Myo6 0
Myo9a 0
Grin1 89
Grin2a 1
Grin2b 2
Grin2d 0
Grin3a 0
Ctnna2 0
Ctnnb1 383
Ctnnd2 1
```

I also checked canonical PCDH15/tip-link and Usher genes against the training endpoint. `Cdh23`, `Ush1c`, `Ush1g`, `Ush2a`, `Whrn`, `Clrn1`, `Myo7a`, `Myo3a`, `Myo3b`, `Tmc1`, `Tmc2`, `Lhfpl5`, `Tmie`, and `Tomt` were not in this training split; `Adgrv1`, an Usher-2 ankle-link gene, was present with 0 focal DEGs.

For expression-pattern evidence, I extracted these genes from the parquet with the equivalent of:

```python
ds.field("group_name") == "151 TH Prkcd Grin2c Glut"
& ds.field("gene_target").isin(curated_targets)
```

and compared whole log-fold-change profiles over the 17,259 measured genes. I also wrote a Distributed Agents runtime comparison for 26 focal profiles to `pcdh15_profile_compare.json` and a bounded inspection to `pcdh15_profile_inspect.json`. The important outcome was that the curated adhesion/synapse set was null to weak at FDR:

- `Pcdh19`, `Adgrv1`, and `Dscam`: 0 significant genes in the focal class.
- `Cadm2`, `Cntnap1`, `Cntnap2`, `Nrxn1`, `Nlgn3`, `Adam22`, `Dlg4`, and `Myo5a`: exactly one significant gene, and in each case the one gene was the targeted transcript itself.
- `Shank3`: two significant genes, `Shank3` itself and `Uba5`.

Whole-vector Pearson correlations among these quiet profiles were modestly positive, commonly about `0.65-0.70`, but there was no shared significant feature intersection because most comparators had no downstream FDR-significant feature to intersect.

## Target-specific reasoning

### `Pcdh15`

**Closest observed analogs.** The cleanest in-dataset cadherin-family comparator was `Pcdh19`. It is not the PCDH15 tip-link partner, but it is a non-clustered protocadherin/cadherin superfamily membrane protein with a neurodevelopmental disease literature, so it is more relevant than a random high-count transcription factor. `Pcdh19` had `n_degs = 0` in `151 TH Prkcd Grin2c Glut` with 137 matched perturbed nuclei and 23,679 matched controls. The Distributed Agents corpus summarizes it as producing no robust downstream transcriptional response in any recovered neuronal supergroup, and specifically notes that expected Wnt/beta-catenin, GABA-A receptor, immediate-early, and synaptic-adhesion programs were not recovered. I treated this as the strongest within-dataset reason not to assign a medium or strong PCDH15 response.

`Adgrv1` was the best sensory/Usher-family counterexample that was present in training. It is an adhesion GPCR mutated in Usher syndrome type 2 and participates in sensory-cell ankle-link biology rather than the PCDH15-CDH23 tip link, so the comparison is imperfect. Still, it asks whether an inner-ear/retina adhesion molecule with long extracellular cadherin-like domains generates a broad autonomous neuronal transcriptome in this screen. It did not: `Adgrv1` had `n_degs = 0` in the focal class with 225 matched perturbed nuclei, and the Distributed Agents corpus reports no FDR-significant downstream transcriptional response across 22 recovered postmitotic neuronal groups.

`Dscam`, `Cadm2`, `Cntnap1`, `Cntnap2`, `Nrxn1`, `Nrxn2`, `Nrxn3`, `Nlgn3`, `Adam22`, `Dlg4`, `Shank2`, `Shank3`, `Syngap1`, and `Cacng2` were broad neuronal cell-adhesion, synaptic adhesion, or postsynaptic-density comparators. They are functional counterexamples rather than direct biochemical analogs of PCDH15. In `151 TH Prkcd Grin2c Glut`, this group stayed at 0, 1, or 2 DEGs, and almost all of the one-DEG cases were self-transcript calls only. The same-experiment corpus made the same qualitative point for `Cadm2`, `Dscam`, `Nrxn1`, and `Nlgn3`: they were buffered or sparse and lacked robust signature neighbors. That makes a large PCDH15 downstream signature unlikely.

I considered two nonzero counterexamples. `Grin1` had 89 focal DEGs, but that perturbation removes an obligate NMDA-receptor subunit and is much closer to a core excitability perturbation than to a stereociliary adhesion protein. `Ctnnb1` had 383 focal DEGs, but beta-catenin is a Wnt/transcriptional hub; the `Pcdh19` same-experiment finding is a useful boundary because a protocadherin perturbation did not phenocopy beta-catenin or Wnt targets in this postnatal neuronal assay.

**External biology.** PCDH15 is best established as an atypical cadherin in mechanosensory hair cells. Mutations in human `PCDH15` cause Usher syndrome type 1F, and mouse `Pcdh15` mutants have deafness and vestibular phenotypes (Ahmed et al. 2001, DOI `10.1086/321277`, PMID `11398101`). In mature hair cells, PCDH15 forms the lower part of the tip link with CDH23, and in developing hair cells particular PCDH15 isoforms contribute to kinociliary links and hair-bundle polarity (Webb et al. 2011, DOI `10.1242/dev.060061`, PMID `21427143`; Pepermans and Petit 2015, DOI `10.1016/j.heares.2015.05.005`, PMID `26049141`; Choudhary et al. 2020, DOI `10.1073/pnas.1920444117`, PMID `32963095`). Those mechanisms nominate `Cdh23`, `Lhfpl5`, Usher scaffolds, and myosins as partners, but almost all of those genes were absent from the training endpoint and the biology is specialized to hair cells or retina, neither of which is in the NeuN-positive whole-brain snRNA-seq input.

PCDH15 has CNS reports, including OPC proliferation and motility after knockdown (Zhen et al. 2022, DOI `10.1038/s42003-022-03470-1`, PMID `35637313`) and behavioral/c-Fos changes in constitutive `Pcdh15`-deficient mice (Mori et al. 2024, DOI `10.1038/s41398-024-02952-6`, PMID `38806495`). I did not treat either as a strong reason to increase the `151 TH Prkcd Grin2c Glut` count: the OPC work is outside the NeuN-positive neuronal sampling frame, and the behavioral/c-Fos study used germline deletion and whole-animal circuit state rather than sparse acute P16 loss in postmitotic neurons.

**Prediction.** The within-dataset evidence puts the closest observable cadherin, Usher, and synaptic-adhesion perturbations at zero or self-only one-DEG responses. The external PCDH15 literature points mainly to sensory epithelia and glia-lineage functions that are poorly represented in this assay. I therefore predicted `Pcdh15` to be below the FDR threshold in the focal class:

```text
Pcdh15 -> 0 DEGs
```

## Limits

- The internal corpus had no target card, findings, or claims for held-out `Pcdh15`; all same-experiment transfer is through imperfect observed analogs.
- The most direct molecular partner, `Cdh23`, and most Usher/tip-link components were absent from the training DEG-count table, leaving `Adgrv1` as a related but not equivalent sensory-adhesion comparator.
- A zero prediction does not mean PCDH15 is biologically unimportant. The endpoint is an assay- and power-dependent number of FDR-significant nuclear-RNA changes among recovered cells.
- PCDH15 could have an effect in hair cells, retina, OPCs, or a small neuronal subtype that this NeuN-positive whole-brain perturb-seq design would not read out well.
- Acute mosaic P16 CRISPR loss need not match constitutive mouse knockout or human recessive disease phenotypes, especially for adhesion molecules whose critical functions can occur during early morphogenesis.
