# DEG-count prediction trace

## Question and endpoint

I predicted the held-out `n_degs` for `Ap2s1` in `151 TH Prkcd Grin2c Glut`, where `n_degs` means the number of measured focal-cell genes with Benjamini-Hochberg adjusted Wilcoxon `pvals_adj < 0.05`.

I treated the supplied focal-cell DEG-count CSV as the directly observed endpoint for non-held-out training perturbations. I treated `training differential-expression dataset` as direct differential-expression evidence for the same training perturbations and the same screen. Because `Ap2s1` was fully held out, its expression signature and count are absent from those inputs; the prediction is a transfer from assayed analogs plus external AP-2 biology, not a lookup.

## Sources

- Direct training endpoint: `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
- Direct expression summaries: `training differential-expression dataset`, filtered to `group_name = '151 TH Prkcd Grin2c Glut'` for the focal comparison.
- Requested target list: `single-target request for Ap2s1`; it contained exactly one requested target, `Ap2s1`.
- Same-experiment interpretation layer: PerturbAI July 260713 sourceguard 1773 v1 Findings ledger, queried through the run-declared `corpus.findings` capability for `Cltc`, `Dnm1`, `Synj1`, `Ap1b1`, `Ap1s2`, `Ap3b1`, and `Ap4s1`. This was used only as packaged interpretation of the same Perturb-seq experiment, not as independent replication.
- External biology: PubMed literature on AP-2 and clathrin-mediated endocytosis, specifically McMahon and Boucrot 2011, DOI 10.1038/nrm3151, PMID 21779028; Mettlen et al. 2018, DOI 10.1146/annurev-biochem-062917-012644, PMID 29661000; Beacham et al. 2019, DOI 10.1111/tra.12677, PMID 31313456; Kim and Ryan 2009, DOI 10.1523/JNEUROSCI.5639-08.2009, PMID 19321783; Nesbit et al. 2012, DOI 10.1038/ng.2492, PMID 23222959; Gorvin et al. 2017, DOI 10.1002/jbm4.10001, PMID 29479578; and Candiello et al. 2017, DOI 10.1038/s41598-017-16055-4, PMID 29150658.

## Quantitative calibration

The focal-cell training set had 1,674 perturbations. It was highly zero-inflated:

- 1,205/1,674 perturbations had `n_degs = 0`.
- 469/1,674 had any focal DEG.
- 1,527/1,674 had `n_degs <= 3`.
- The median was 0, the 90th percentile was 2, the 95th percentile was 18, and the maximum was 2,677.

I then queried the focal-cell Parquet rows for biologically relevant trafficking, AP-family, clathrin, and synaptic-vesicle perturbations. The non-obvious computation was:

```sql
SELECT gene_target,
       count(*) AS n_rows,
       sum(CAST(pvals_adj < 0.05 AS INTEGER)) AS n_sig,
       min(pvals_adj) AS min_padj,
       avg(n_pert_matched) AS mean_n_pert,
       avg(n_ctrl_matched) AS mean_n_ctrl
FROM read_parquet('training_de_all_cell_groups.parquet')
WHERE group_name = '151 TH Prkcd Grin2c Glut'
  AND gene_target IN (...)
GROUP BY gene_target;
```

The closest represented AP-family and endocytic comparators were all at the null boundary:

| training target | observed focal `n_degs` | focal expression-pattern evidence |
|---|---:|---|
| `Ap1b1` | 1 | The only FDR 0.05 hit was `Ap1b1` itself, log2FC -0.537, q = 3.99e-4. |
| `Ap1s2` | 0 | No FDR 0.05 gene; smallest q = 0.394. |
| `Ap3b1` | 0 | No FDR 0.05 gene; smallest q = 1.0. |
| `Ap4s1` | 0 | No FDR 0.05 gene; smallest q = 1.0. |
| `Cltc` | 3 | Three modest downstream FDR hits, `Rbms1`, `Ero1b`, and `Gabra4`, each q = 0.042, in only 32 matched perturbed nuclei. |
| `Dnm1` | 1 | The only FDR hit was `Dnm1` itself, q = 4.09e-25; no downstream FDR gene. |
| `Synj1` | 1 | The only FDR hit was `Synj1` itself, q = 3.11e-7; no downstream FDR gene. |
| `Stxbp1` | 1 | The only FDR hit was `Stxbp1` itself, q = 9.38e-19; no downstream FDR gene. |
| `Syp` | 1 | The only FDR hit was `Syp` itself, q = 7.95e-66; no downstream FDR gene. |
| `Nsf` | 0 | No FDR 0.05 gene; smallest q = 0.835. |
| `Cplx1` | 1 | The only FDR hit was `Cplx1` itself, q = 4.29e-24; no downstream FDR gene. |
| `Cplx2` | 0 | No FDR 0.05 gene. |

These are not equally close analogs. `Ap1b1`, `Ap1s2`, `Ap3b1`, and `Ap4s1` are AP adaptor subunits in related coat/cargo complexes. `Cltc` is the common clathrin heavy chain used downstream of AP-2 and other adaptors, so it is a broad coat counterexample showing that a trafficking lesion can sometimes be read out by this assay. `Dnm1` and `Synj1` are later synaptic-vesicle fission and uncoating factors and therefore test whether membrane-recycling defects in general triggered a focal nuclear state. `Rab7` was a poor positive analog despite a high focal count of 501, because RAB7 lies at late endosome/lysosome fusion rather than AP-2 cargo selection at the plasma membrane; its large lysosomal response should not be transferred to a specific AP-2 sigma loss.

To check whether the AP/clathrin comparators shared a weak focal transcriptional state below FDR, I correlated their genome-wide focal Wilcoxon score vectors. Pairwise Pearson correlations among `Ap1b1`, `Ap1s2`, `Ap3b1`, `Ap4s1`, `Cltc`, `Dnm1`, and `Synj1` ranged from -0.036 to 0.027. Thus there was no reusable AP-adaptor or clathrin-endocytosis expression program that would support a nonzero `Ap2s1` estimate beyond isolated self-transcript hits.

## Target-specific reasoning

### Ap2s1

`Ap2s1` encodes the sigma subunit of the heterotetrameric AP-2 adaptor. AP-2 is a central plasma-membrane clathrin adaptor that links cargo signals to clathrin-coated pit assembly and is especially relevant to receptor internalization and synaptic-vesicle protein retrieval (McMahon and Boucrot 2011; Mettlen et al. 2018; Beacham et al. 2019). Human AP2S1 Arg15 mutations impair dileucine-motif cargo recognition and CaSR endocytosis in familial hypocalciuric hypercalcemia type 3 (Nesbit et al. 2012), and mouse homozygous Ap2s1 loss-of-function is embryonic lethal whereas a heterozygous splice-loss allele is haplosufficient for viability and serum/urine mineral traits (Gorvin et al. 2017).

That external biology establishes that AP2S1 is a real obligate AP-2 component, but it does not imply a broad postmitotic thalamic nuclear response after sparse, partial P16 CRISPR loss. The most direct causal model here is:

`Ap2s1` editing -> impaired AP-2 cargo recognition or AP-2 complex function at the plasma membrane -> altered receptor and synaptic-vesicle protein endocytosis, with partial compensation by AP-1 and other adaptors in neurons -> survivor-conditioned nuclear RNA sampling after 3-4 weeks.

The comparator data mostly acted at the first two molecular stages and showed a causal break before the last measured stage. `Cltc` loss, which removes the broader coat scaffold shared by AP-2-dependent and AP-2-independent traffic, produced only three focal FDR 0.05 genes. `Ap1b1`, `Ap1s2`, `Ap3b1`, and `Ap4s1` loss did not produce a focal AP-family downstream program. `Dnm1` and `Synj1` are essential or important for activity-dependent synaptic-vesicle endocytosis, but their perturbations reached FDR only for their own transcripts in this focal population. Kim and Ryan 2009 found that synaptic vesicle proteins could still be endocytosed in primary neurons after near-complete AP-2 complex knockdown, with AP-1 appearing to substitute partly for AP-2, which is a concrete candidate-specific bypass mechanism for why AP-2 sigma loss need not produce a large basal mRNA phenotype. Candiello et al. 2017 similarly place AP-1/AP-2 balance at the synaptic vesicle coated-vesicle stage rather than making AP-2 sigma loss equivalent to loss of all clathrin traffic.

The zero/nonzero decision is therefore driven mostly by within-dataset evidence: every represented AP adaptor complex subunit was zero or self-only in `151 TH Prkcd Grin2c Glut`, clathrin itself was small, and the focal score vectors had no hidden AP-family convergence. External AP-2 literature raised `Ap2s1` above an arbitrary uncharacterized gene but also supplied redundancy and cargo-specificity reasons to keep it at the null boundary. I predict that an `Ap2s1` knockout in this acute mosaic assay would not push any measured gene below FDR 0.05 in the focal group.

## Limits and uncertainty

The main limitation is that no same-complex AP-2 alpha, beta, or mu subunit was represented as a training perturbation in the focal-count CSV, so `Ap2s1` is inferred from neighboring adaptor complexes and the shared clathrin/synaptic-vesicle machinery rather than from an assayed AP-2 subunit. The screen measures nuclear RNA in recovered NeuN-positive nuclei; it does not measure clathrin-coated pits, receptor uptake, synaptic vesicle recycling, electrophysiology, pre-assay survival, DNA indels, or AP2S1 protein. A true AP2S1 protein phenotype could therefore be present yet transcriptionally silent. The count is also sensitive to target-transcript expression and guide-induced nonsense-mediated decay; the closest one-DEG training perturbations were often self-transcript calls, and there is no direct held-out `Ap2s1` self row to calibrate whether that single gene would pass FDR. Those uncertainties could move the correct integer from 0 to a handful of DEGs, but the training evidence did not support a broad response.
