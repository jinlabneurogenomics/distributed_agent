# Question and interpretation

The task is to predict `n_degs` for each held-out perturbation in `151 TH Prkcd Grin2c Glut` neurons.  I interpreted `n_degs` exactly as the focal training CSV does: the count of measured genes in this cell group with Benjamini-Hochberg adjusted Wilcoxon `pvals_adj < 0.05`, including the perturbed target transcript itself if it crosses that threshold.

This run requested one held-out target:

```tsv
target_name
Kmt2e
```

`Kmt2e` was absent from both supplied training inputs, as expected.  I therefore estimated its response breadth by comparing focal-cell expression signatures and observed DEG counts of biologically related non-held-out perturbations.

# Sources used

- Supplied focal endpoint table: `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
- Supplied full differential-expression parquet: `training_de_all_cell_groups.parquet`.
- Internal same-experiment semantic corpus: Distributed Agents `perturbai-july-260713-sourceguard-1773-v1`.
  - `target_context(Kmt2e)` and `related_targets(Kmt2e)` had no record, so the corpus did not directly annotate this held-out target.
  - `target_context(Kmt2a)`, `target_context(Setd1a)`, `target_context(Chd8)`, `search_claims("H3K4 chromatin Kmt2 Setd1")`, and `inventory` over `Kmt2a`, `Kmt2c`, `Ash1l`, and `Setd5` supplied curated same-experiment claims and finding summaries for the relevant observed perturbations.
- Distributed Agents runtime profile tools over the focal parquet.
  - I filtered to `group_name == "151 TH Prkcd Grin2c Glut"`.
  - I counted `pvals_adj < 0.05` for selected H3K4/chromatin analogs to verify the CSV values against the parquet.
  - I compared signed `logfoldchanges` and FDR-positive gene-set intersections among a candidate cohort: `Kmt2a`, `Kmt2c`, `Setd1a`, `Setd5`, `Ash1l`, `Chd2`, `Chd4`, `Chd8`, `Arid1a`, and `Sin3a`.
  - I inspected both exact pairwise metrics and the numbers of positive and negative FDR hits per candidate.
- External literature from NCBI PubMed:
  - Zhang et al. 2017, DOI 10.1007/s00018-017-2470-8, PMID 28188343: review of MLL5/KMT2E structure and function, emphasizing that KMT2E is an atypical MLL/KMT2 member and appears to lack intrinsic histone methyltransferase activity toward histone substrates.
  - O'Donnell-Luria et al. 2019, DOI 10.1016/j.ajhg.2019.03.021, PMID 31079897: de novo heterozygous pathogenic `KMT2E` variants cause a neurodevelopmental disorder with intellectual disability, autism, macrocephaly, hypotonia, and seizures.
  - Velmans et al. 2021, DOI 10.1136/jmedgenet-2020-107470, PMID 34321323: an additional ODLURO cohort confirmed pathogenic mostly truncating `KMT2E` variants and high ASD prevalence.
  - Ding et al. 2015, DOI 10.1371/journal.pone.0145023, PMID 26678539: OGT and USP7 regulate MLL5/KMT2E protein stability in a nuclear complex.

# Dataset calibration

The focal training table is extremely zero-inflated: among 1,674 observed training perturbations, the median `n_degs` is 0, the 75th percentile is 1, and the 90th percentile is 2.  Very broad responses exist but are rare: the 95th percentile is 18 and only a small tail reaches hundreds or thousands of DEGs.

The focal parquet contained 17,259 measured genes per training perturbation.  `Kmt2e` itself was absent.  Selected focal analog counts were:

```tsv
target	n_degs	direction_of_fdr_hits
Setd1a	368	299 down, 69 up
Chd4	100	48 down, 52 up
Chd8	61	39 down, 22 up
Chd2	34	22 down, 12 up
Kmt2a	24	12 down, 12 up
Setd5	9	1 down, 8 up
Ogt	4	mixed sparse
Ash1l	1	1 down, self transcript only
Kmt2c	0	none in 151 TH
Kat6a	0	none in 151 TH
Kat6b	0	none in 151 TH
Chd7	0	none in 151 TH
Smarca4	0	none in 151 TH
```

`Setd1a` is therefore not a generic template for every H3K4-axis perturbation.  The internal Distributed Agents Kmt2a finding made this explicit: represented H3K4 writer relatives diverged, with `Setd1a` broad and largely non-overlapping, `Kmt2a` sparse, and `Kmt2c` nearly flat.  The high-confidence Distributed Agents claim over PHF/PHD, KDM/H3K4, REST-associated, SETBP1-associated, and adjacent chromatin regulators likewise stated that these postnatal neuronal signatures are target-specific rather than interchangeable by domain, pathway, or family membership.

# Target-specific reasoning

## Kmt2e

Biology.  KMT2E/MLL5 carries SET-domain homology and is grouped with KMT2/MLL proteins, making `Kmt2a`, `Kmt2c`, and `Setd1a` the most direct training comparators available in the held-in dataset.  However, the Zhang et al. review emphasizes that MLL5 is the atypical member of the family and appears not to behave like a canonical H3K4 histone methyltransferase on its own.  External genetics clearly keeps the target relevant to the nervous system: O'Donnell-Luria et al. and Velmans et al. show that heterozygous disruptive `KMT2E` variants cause ODLURO neurodevelopmental disorder with ASD and seizure susceptibility.  That human evidence supports a real neuronal/developmental role, but it is not age- or assay-matched to sparse acute P16 mouse CRISPR in postmitotic nuclei.

Most relevant training perturbations.

- `Kmt2a`, `n_degs = 24`: the nearest biochemical analog in the training set.  In the focal group it down-regulated a compact neuronal identity/connectivity arm with `Nr2f1`, `Pcdh7`, `Lhx9`, `Pcdh10`, `Camk2d`, `Grik2`, and `Map1b`, while also inducing a small compensatory arm including `Igfbp5`, `Tnr`, `Cx3cl1`, `Atxn2l`, `Luc7l`, and `Txndc5` in the Distributed Agents finding.  This argues that acute loss of an H3K4-family gene can give a modest nonzero thalamic response.
- `Kmt2c`, `n_degs = 0`: the clearest KMT-family counterexample.  In the focal group it had no adjusted DEGs, and same-experiment Distributed Agents findings characterized acute P16 `Kmt2c` loss as broadly buffered, with only one cortical `Prnp` hit across the whole measured surface.  This prevents assigning `Kmt2e` a positive count just because it carries a KMT2-family name.
- `Setd1a`, `n_degs = 368`: a canonical H3K4 writer that is much broader than `Kmt2a`.  Its 151 TH signature was mostly down-regulation of mitochondrial, GPI-anchor, ER/Golgi, UFMylation, glycoprotein-processing, and cilium/centrosome maintenance transcripts.  It provides an upper counterexample rather than a good point estimate because its focal DEG set shared only one FDR-positive gene with `Kmt2a`, and the corpus reports that `Kmt2a` did not phenocopy it.
- `Setd5`, `n_degs = 9`: another neurodevelopmental chromatin regulator with only a small focal state, mostly up-regulating `Rgs4`, `Adarb1`, `Prkcd`, and `Lrrc7`.  This is a useful magnitude analog for a disease-associated epigenetic regulator whose strongest germline or progenitor phenotypes are not necessarily reconstructed by P16 postmitotic editing.
- `Ash1l`, `n_degs = 1`, and `Ogt`, `n_degs = 4`: `Ash1l` was essentially self-only despite chromatin and developmental relevance.  `Ogt` is not a loss-of-KMT2E phenocopy, but Ding et al. show OGT can stabilize MLL5/KMT2E protein; the sparse `Ogt` count is consistent with the idea that a KMT2E-linked biochemical route need not yield a Setd1a-sized transcriptome in this focal group.
- `Chd2`, `Chd4`, and `Chd8`, with 34, 100, and 61 DEGs: these ASD/chromatin remodelers prove that 151 TH Prkcd Grin2c Glut can report dozens of DEGs for nuclear regulators.  They are indirect for `Kmt2e`; Distributed Agents CHD findings explicitly warn that represented CHD paralogs and ASD-associated chromatin genes are not interchangeable in this P16 neuronal assay.

The exact profile comparison supported using `Kmt2a`/`Setd5`/`Ogt` as low-count magnitude anchors rather than borrowing `Setd1a`: `Kmt2a` had no FDR-positive overlap with `Chd2`, `Chd4`, `Chd8`, or `Arid1a` in the focal group and shared only one FDR-positive gene with `Setd1a`; `Kmt2c`, `Ash1l`, and `Setd5` shared zero focal FDR-positive genes with the CHD comparators.  Broad subthreshold log-fold-change cosines were not treated as mechanistic phenocopies because the adjusted DEG sets remained absent or nearly disjoint.

Zero versus nonzero.  I predict a detectable but small focal response.  The external human genetics and the H3K4-family placement make a complete 0 less likely than for `Kmt2c`, `Kat6a`, `Kat6b`, `Chd7`, or `Smarca4`; the atypical KMT2E enzymology and the weak mature-neuron responses of `Kmt2c`, `Ash1l`, `Setd5`, and `Ogt` make the Setd1a/CHD range too high.  I put the point estimate below `Setd5` and above the `Ogt` sparse response:

```tsv
target_name	predicted_n_degs
Kmt2e	6
```

# Limits

The largest uncertainty is that the training set did not contain a direct MLL5/KMT2E protein-complex member such as USP7, and the Distributed Agents corpus had no Kmt2e-specific same-experiment report.  Human ODLURO genetics is strong evidence for organismal neurodevelopmental importance but weakly matched to a juvenile, sparse, acute mouse neuronal loss-of-function readout.  The H3K4-axis training targets themselves are explicitly non-interchangeable in this dataset, so the integer 6 is an extrapolation from low-count analogs rather than a signature-level interpolation from a true Kmt2e phenocopy.
