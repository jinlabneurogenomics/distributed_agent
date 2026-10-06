# Reasoning trace

## Question and endpoint

The requested endpoint is the FDR-significant differential-expression burden for each held-out perturbation in the `151 TH Prkcd Grin2c Glut` focal cell group. I interpreted `predicted_n_degs` as a single non-negative integer estimate of the number of measured genes with `pvals_adj < 0.05` after acute AAV-CRISPR loss of function, harvested in recovered P37-P44 NeuN+ nuclei.

The only requested held-out target was:

| target_name | requested order |
|---|---:|
| Usp9x | 1 |

`Usp9x` was held out completely. The declared training Parquet contains 0 rows for `Usp9x`, and it was not present in the focal-cell training count table. I also checked that the closest obvious family labels `Usp9y` and `Usp24` were not represented as `gene_target` perturbations, while `Usp48` and `Zbtb38` were represented.

## Sources used

- Declared differential-expression dataset: `training differential-expression dataset`.
- Declared focal-cell training endpoint: `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
- Declared requested-target manifest: `single-target request for Usp9x`.
- Run-local dataset portrait, task bindings, capability manifest, coverage, and measurement registry.
- Internal same-experiment semantic corpus: `perturbai-july-260713-sourceguard-1773-v1`, queried through `corpus.calibration`, `corpus.findings`, `corpus.graph`, and `corpus.report_evidence`.
- PubMed and packaged references for external mechanism:
  - Xu et al. 2005, Journal of Neuroscience Research, PMID:15723417, DOI:10.1002/jnr.20429, showing spatially and temporally patterned `Usp9x` expression in mouse hippocampus around postnatal maturation and motivating a role in synaptic development.
  - Reijnders et al. 2016, American Journal of Human Genetics, PMID:26833328, DOI:10.1016/j.ajhg.2015.12.015, establishing de novo human USP9X loss-of-function variants as a cause of female-restricted syndromic intellectual disability and congenital malformations.
  - Miotto et al. 2018, Nucleic Acids Research, PMID:29490077, DOI:10.1093/nar/gky149, showing that USP9X interacts with, deubiquitinates, and stabilizes ZBTB38 and that the USP9X/ZBTB38 axis limits oxidative stress.
  - Giles and Grill 2020, Neural Development, PMID:32336296, DOI:10.1186/s13064-020-00143-9, a review of HUWE1 nervous-system biology used only to interpret why the represented HECT ligase `Huwe1` is an imperfect comparator.

The Parquet and the internal corpus are different representations of the same Perturb-seq experiment, not independent measurements. I used the Parquet and focal count CSV for exact `n_degs`; the same-experiment corpus was used for compactly finding and interpreting analogs already observed in the training universe.

## Computation over the declared data

For the focal cell group I counted, for every represented training perturbation, how many measured genes had `pvals_adj < 0.05`; these counts matched the supplied training CSV definition. I then queried the focal DE rows for the mechanistically relevant represented targets and also counted their FDR<0.10 shoulder to distinguish hard zeros from borderline one- or two-gene responses.

The relevant focal training counts were:

| represented target | focal FDR<0.05 DEGs | focal FDR<0.10 DEGs | matched perturbed nuclei | relationship to Usp9x |
|---|---:|---:|---:|---|
| Zbtb38 | 1 | 2 | 199 | direct downstream stability substrate of USP9X protein in an oxidative-stress axis |
| Usp48 | 10 | 12 | 172 | another USP deubiquitinase with a small 151-specific neuronal response, not a paralog |
| Ddx3x | 8 | 10 | 138 | X-linked neurodevelopmental comparator with a mild thalamic response |
| Kdm5c | 18 | 18 | 184 | X-linked neurodevelopmental comparator with a mild thalamic response |
| Ube3a | 0 | 0 | 84 | brain-relevant ubiquitin ligase counterexample |
| Huwe1 | 158 | 225 | 105 | X-linked HECT E3 ligase with a much broader but target-specific RNA/mitochondrial response |
| Uba5 | 2677 | 3225 | 245 | global UFMylation counterexample, much broader than a substrate-specific DUB |
| Psmb4 | 742 | 1102 | 62 | core proteasome counterexample |
| Psmc1 | 430 | 656 | 89 | core proteasome counterexample |

The focal training endpoint was very zero-inflated overall: among 1,674 training perturbations, the median was 0 DEGs, the 75th percentile was 1 DEG, and only 469 perturbations were nonzero. The 95th percentile was 18 DEGs; `Uba5`, the strongest focal perturbation, had 2,677 DEGs.

The exact focal signature evidence for the closest small comparators was:

- `Zbtb38`: `Msra` was up-regulated and FDR-significant, log2FC 0.485 and FDR 0.00448; `Abhd12b` was also up, log2FC 0.817, just outside 0.05 at FDR 0.0941. The internal Zbtb38 report explicitly links this tiny two-gene FDR<0.10 response to the Miotto et al. USP9X/ZBTB38 oxidative-stress axis.
- `Usp48`: 10 FDR<0.05 and 12 FDR<0.10 focal hits, headed by `Abhd12b` up, log2FC 1.476 and FDR 8.4e-10; `Cyp46a1` down, log2FC -0.270 and FDR 1.4e-6; then `Resp18`, `Galk2`, `Msrb2`, `Tmem181a`, `Syne1`, `Bcan`, `Lrp10`, and `Macf1` at FDR<0.05. The internal Usp48 report called this a compact Abhd12b/Cyp46a1/Msrb2/Bcan module restricted to `151 TH Prkcd Grin2c Glut`.
- `Ddx3x`: 8 FDR<0.05 and 10 FDR<0.10 focal hits, including self-downregulation plus `Ypel3`, `Grin2b`, `Synpo2`, `Plekhg1`, `Tmsb10`, `Tcea2`, and `Ccdc136`. This shows that a severe X-linked neurodevelopmental gene can give only a single-digit response in the assay.
- `Kdm5c`: 18 focal hits, including `Ptgds`, `Capn3`, `Man2a2`, `Zfp532`, `Col9a3`, `Usp11`, `Zmynd8`, `Hexim2`, `Ank1`, and `Msra`. This is another low-double-digit X-linked comparator, and the weak overlap through `Msra` is more consistent with a small redox/homeostatic class than with a large shared USP9X program.
- `Huwe1`: 158 focal hits and 225 at FDR<0.10, with a recurrent RNA-processing and mitochondrial/redox upshift led by genes such as `Rsrp1`, `Tcea2`, `Dusp11`, `Aifm3`, `Srrm1`, `Txnl1`, `Cox7b2`, `Glrx2`, and `Tspan17`. The internal Huwe1 report also showed that `Ube3a`, `Hectd4`, `Herc2`, `Ubr1`, `Trp53`, `Myc`, and `Mycn` did not reproduce this signature, so `Huwe1` is a target-specific counterexample rather than a basis for inflating every ubiquitin-linked neurodevelopmental gene.

## Usp9x prediction

`Usp9x` is an X-linked ubiquitin-specific peptidase. Complete germline or developmental loss has strong biological consequences, and human haploinsufficiency causes a syndromic neurodevelopmental disorder, but the requested experiment is a sparse P16-to-P37/44 CRISPR perturbation in postmitotic neurons. The within-dataset examples therefore matter more than the existence of a developmental disease phenotype: `Ddx3x` and `Kdm5c` are disease genes yet landed at 8-18 DEGs in the focal group; `Ube3a`, also a brain-relevant ubiquitin-system gene, was 0.

The most candidate-specific causal chain is:

`Usp9x` loss of deubiquitinase activity -> destabilization of ZBTB38 protein -> weaker ZBTB38-dependent buffering of basal or induced oxidative stress -> small compensatory increases in oxidative repair or lipid/redox genes in recovered 151 thalamic neurons -> one to several measured FDR hits.

This chain is endpoint-bearing because the same experiment directly measured `Zbtb38` loss and found a small focal response containing `Msra` and borderline `Abhd12b`; the external Miotto et al. result supplies the mechanistic sign by placing USP9X upstream as a stabilizer of ZBTB38 protein. I expect the endpoint to move in the same direction as `Zbtb38` loss, but only partially. USP9X has many substrates and cell-biological roles, the Miotto work was in human non-neuronal cells, and the CRISPR screen measures steady-state nuclear RNA in surviving neurons, so the ZBTB38 axis is a validated mechanistic prior rather than a one-to-one count transfer.

I did not use `Uba5`, `Psmb4`, or `Psmc1` as positive analogs despite their large focal DEG counts. UBA5 controls UFMylation and the proteasome subunits control core proteasome function; those are much more global bottlenecks than a substrate-specific deubiquitinase and are expected to drive broad secondary stress states that `Usp9x` loss need not reproduce. I also kept `Huwe1` as an upper counterexample rather than as the point estimate, because its focal RNA-processing/mitochondrial module was explicitly not a generic HECT or ubiquitin-ligase signature in the training data.

Balancing the direct but tiny `Zbtb38` response, the small `Usp48` response, and the 8-18 DEG counts of `Ddx3x`/`Kdm5c`, I predicted that `Usp9x` will be nonzero but remain in the single digits. The final point estimate is:

| target_name | predicted_n_degs |
|---|---:|
| Usp9x | 5 |

## Limits and uncertainty

This estimate is an extrapolation. The screen does not contain `Usp9y` or `Usp24`, so I could not use a true USP9 paralog. The `Zbtb38` transfer goes through post-translational stabilization, not a stable obligate complex, and it was reported by Miotto et al. in human cells outside the postnatal thalamic neuron context. `Usp48` is the only represented USP-family target with a small positive focal signature, but its known Hedgehog, NF-kB, and H2A/BRCA1 biology is not USP9X biology. The focal endpoint is also discrete and zero-inflated; a perturbation with a real but weak state can easily cross the 0.05 FDR threshold for zero, one, or a handful of genes depending on matched-cell recovery and guide performance.
