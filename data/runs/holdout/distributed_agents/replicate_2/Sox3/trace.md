# Sox3 held-out DEG-count prediction

## Question and endpoint

The requested manifest has one held-out perturbation, `Sox3`. I interpreted the
task as a point prediction of the hidden focal-cell endpoint:

`n_degs = count(pvals_adj < 0.05)` among measured genes in
`151 TH Prkcd Grin2c Glut` after acute AAV CRISPR loss of the target at P16 and
snRNA-seq at P37-P44.

I used the FDR 0.05 counts in
`151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` as the exact calibration
target. The Distributed Agents same-experiment corpus often summarizes Findings at
FDR<0.10, so I used those summaries qualitatively and always checked the exact
FDR<0.05 counts for the final numerical comparison. A DuckDB scan confirmed
that `Sox3` had zero rows in the supplied differential-expression parquet, as
expected for a held-out target.

## Sources used

- Training count CSV:
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`
- Differential-expression parquet:
  `[local file: training_de_all_cell_groups.parquet]`
- Manifest:
  `[local file: 219_Sox3.csv]`
- Run-local Distributed Agents profile tools over the focal `group_name`.
- Distributed Agents corpus release `perturbai-july-260713-sourceguard-1773-v1`, especially the `Sox2`, `Sox5`, and `Sox17` Findings and the moderate-confidence measured-SOX Claim that SOX-family perturbations did not form a generic postnatal neuronal SOX program.
- PubMed-indexed SOXB1 literature: Graham et al. 2003, PMID 12948443, DOI `10.1016/S0896-6273(03)00497-5`; Bylund et al. 2003, PMID 14517545, DOI `10.1038/nn1131`; Rizzoti et al. 2004, PMID 14981518, DOI `10.1038/ng1309`; Rogers et al. 2014, PMID 24751947, DOI `10.1371/journal.pone.0095356`; McAninch and Thomas 2014, PMID 25409526, DOI `10.1371/journal.pone.0113361`.

## Computations over the supplied data

1. Read the manifest and verified that the only requested target is `Sox3`.
2. Loaded the focal-cell training counts, which contain 1,674 non-held-out
   targets. The endpoint is very sparse: median `n_degs` is 0, the 75th
   percentile is 1, and the 90th percentile is 2.
3. Pulled all measured SOX targets in the focal count table:

   | target | focal n_degs |
   |---|---:|
   | Sox2 | 2 |
   | Sox4 | 0 |
   | Sox5 | 2 |
   | Sox9 | 0 |
   | Sox10 | 0 |
   | Sox11 | 0 |
   | Sox17 | 0 |
   | Sox18 | 0 |

4. Queried the parquet directly for focal FDR<0.05 SOX genes:

   ```sql
   SELECT gene_target, names, logfoldchanges, pvals_adj
   FROM read_parquet(...)
   WHERE group_name = '151 TH Prkcd Grin2c Glut'
     AND gene_target IN ('Sox2','Sox4','Sox5','Sox9',
                         'Sox10','Sox11','Sox17','Sox18')
     AND pvals_adj < 0.05
   ORDER BY gene_target, pvals_adj, names;
   ```

   Exact significant genes:

   | target | significant genes in 151 TH Prkcd Grin2c Glut |
   |---|---|
   | Sox2 | `Tnnt1`, logFC -1.006, q 2.77e-6; `Stam`, logFC -0.567, q 0.0147 |
   | Sox5 | `Dgkh`, logFC +0.387, q 5.37e-4; `Tnnt1`, logFC +0.566, q 0.0284 |
   | Sox4/Sox9/Sox10/Sox11/Sox17/Sox18 | none |

5. Ran score-vector `profile_compare` on the eight observed SOX targets in the
   same focal cell group. This used the signed Wilcoxon `scores` column as the
   all-gene expression signature and `pvals_adj < 0.05` only to annotate
   significant rows. The comparison classified two SOX perturbations as
   `1_to_9_significant_features` and six as `no_significant_features`.
   Pairwise score correlations among the inspected SOX targets were tiny
   rather than module-like: Pearson values for `Sox2` versus `Sox11`,
   `Sox17`, and `Sox18` were 0.025, 0.003, and 0.027, respectively; `Sox5`
   versus the same three were 0.059, 0.005, and 0.048. The only FDR-level
   recurrent gene among the observed SOX perturbations was `Tnnt1`, and it
   moved down after `Sox2` loss but up after `Sox5` loss.
6. Queried focal counts for SOX2-related and progenitor-stage counterexamples:

   | target set | focal counts |
   |---|---|
   | SOX2/pluripotency/Notch/chromatin comparators | `Chd7` 0, `Ep300` 0, `Myc` 0, `Mycn` 0, `Notch1` 0, `Notch2` 0, `Pax6` 0, `Pou5f1` 0, `Rest` 0, `Smarca4` 0, `Crebbp` 8 |
   | forebrain or progenitor transcription factors | `Bbx` 0, `Hesx1` 0, `Nfia` 0, `Nfib` 0, `Nfix` 0, `Nr2e1` 0, `Otx2` 0, `Pax6` 0, `Six3` 0, `Tcf4` 0, `Zic2` 0, `Zic3` 0, `Zic1` 2 |
   | Wnt/HMG counterexample | `Tcf7l2` 106 |

   `Tcf7l2` is useful as a counterexample: the 151 thalamic class can show a
   Wnt/HMG transcriptional response, so the flat SOX and progenitor factors are
   not merely an inability of this cell group to pass FDR.

## Biological interpretation for Sox3

`Sox3` is a SOXB1 transcription factor, closest to `Sox1` and `Sox2`. SOXB1
factors are classic neural-progenitor maintenance genes: SOX2 is sufficient and
necessary to maintain progenitor properties, and SOX1 can rescue blocked SOX2
signaling in chick neural progenitors (Graham et al. 2003); SOX1-3 factors
counteract proneural bHLH-driven differentiation (Bylund et al. 2003). SOX3
has many conserved embryonic neural-progenitor enhancer targets (McAninch and
Thomas 2014), and embryonic Sox3-null profiling found a limited set of genes,
including `Dbx1`, that were sensitive to Sox3 loss despite SOXB1 redundancy
(Rogers et al. 2014). Mouse Sox3 loss also perturbs formation of the
hypothalamo-pituitary axis through the ventral diencephalon (Rizzoti et al.
2004).

Those data make `Sox2` the best available training analog, but they also define
the main mismatch: the experiment knocked out genes acutely at P16 in recovered
NeuN-positive postmitotic neurons. It did not assay embryonic ventricular-zone
progenitors, Rathke's pouch, pituitary endocrine cells, or vascular/glial
populations. In the measured P16-to-P37 neuronal setting, the direct SOX2
analog was only a two-gene `Tnnt1/Stam` down response, and it did not recover a
stem-cell, Notch/Hes, proliferation, or published dorsal-LGN Sox2 program in
the Distributed Agents corpus. The Distributed Agents `Sox2:F005` Finding also reported that
measured SOX-family, OSKM/pluripotency, REST, Notch, `Ep300`, `Chd7`, and
`Smarca4` perturbations did not phenocopy `Sox2`; the exact focal count table
matches that qualitative statement.

`Sox5` is a useful non-SOXB1 counterexample. It had the same observed focal
count as `Sox2`, but its two hits were `Dgkh` and upregulated `Tnnt1`, so the
only overlapping SOX-family FDR gene inverted direction. `Sox4`, `Sox9`,
`Sox10`, `Sox11`, `Sox17`, and `Sox18` were all zero in the focal count table.
The Distributed Agents SOX-family Claim explicitly summarized this as a small,
restricted, target-specific set of SOX effects rather than a common neuronal
SOX transcriptomic response.

## Sox3 point prediction

I predict that acute `Sox3` perturbation in `151 TH Prkcd Grin2c Glut` will be
at the FDR floor:

- Primary in-dataset analog: `Sox2`, `n_degs = 2`, because it is the closest
  represented SOXB1 factor. It supports, at most, a tiny response.
- Counterexamples: other SOX targets in the focal group were either zero or a
  target-specific two-gene `Sox5` response with opposite `Tnnt1` direction;
  `Chd7`, `Ep300`, `Smarca4`, `Rest`, `Notch1`, `Notch2`, `Pax6`, `Pou5f1`,
  `Myc`, `Mycn`, and most forebrain/progenitor transcription factors were also
  zero.
- External prior: SOX3 biology is strongest in embryonic neural progenitors and
  hypothalamo-pituitary development. That is mechanistically relevant to
  `Sox2` but stage-mismatched to a sparse CRISPR perturbation in juvenile
  postmitotic thalamic glutamatergic neurons.

Because the biologically nearest measured signature has only two genes, because
six of eight measured SOX targets were exactly zero at FDR<0.05 in this cell
group, and because the SOX3-specific literature points mostly outside the
sampled P16 NeuN-positive neuronal compartment, I round the expected tiny
0-2-gene response down to a point prediction of `0`.

## Limits of the reasoning

The largest uncertainty is the missing direct paralog evidence: `Sox1` was not
represented in the training data and `Sox3` itself is held out, so `Sox2` is the
only true SOXB1 measurement. The external Sox3 evidence comes from embryonic,
germline, or cultured neural-progenitor systems, not acute P16 mosaic loss in
surviving thalamic neurons. The broad `151 TH Prkcd Grin2c Glut` class could
dilute a Sox3-sensitive subpopulation. Finally, the endpoint is a statistical
threshold count; for a two-gene-scale perturbation, sampling and power could
move one marginal gene across FDR 0.05 even if the underlying effect is
biologically similar.
