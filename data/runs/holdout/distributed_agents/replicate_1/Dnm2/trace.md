# Question and endpoint

The task is to predict `n_degs` for each requested held-out perturbation in the
`151 TH Prkcd Grin2c Glut` class.  I interpreted `n_degs` as the number of
measured genes, including the perturbed target itself when measured, with
Benjamini-Hochberg-adjusted Wilcoxon `pvals_adj < 0.05` in perturbed versus
matched control nuclei.  The sole requested held-out target was `Dnm2`.  `Dnm2`
is absent from the 1,674-row focal training-count CSV; no Dnm2 expression
signature is available in the training differential-expression parquet.

This readout is directly observed for the training perturbations and absent for
`Dnm2`.  I therefore used the focal-cell DEG counts as direct calibration data,
queried the declared Parquet for mechanistically related visible perturbations,
and used biological knowledge only to decide which visible membrane-trafficking
perturbations were appropriate analogs or counterexamples.

# Sources used

- Declared focal training counts:
  `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
- Declared differential-expression parquet:
  `training differential-expression dataset`.
- Requested-target manifest:
  `single-target request for Dnm2`.
- Run-local dataset portrait, task bindings, coverage, and measurement registry.
- The internal PerturbAI July 260713 sourceguard 1773 v1 Findings/Reports corpus,
  only as same-experiment interpretation of visible training perturbations.
- NCBI PubMed literature searches for dynamin/clathrin biology.

The ranking workbench and predictive graph-review capabilities were not used
because this is a scalar held-out count prediction for an unranked singleton,
not a top-k ranking with ranked or partially ranked gene supervision.

# Dataset calculations

I first summarized the focal training-count distribution.  It was extremely
sparse: 1,205/1,674 visible targets had `n_degs = 0`, 1,481/1,674 had
`n_degs <= 1`, 1,512/1,674 had `n_degs <= 2`, and 1,527/1,674 had
`n_degs <= 3`.  The median and 75th percentile were 0 and 1, respectively,
whereas rare large responses raised the mean to 14.1.

I then queried the Parquet with filters on `group_name = '151 TH Prkcd Grin2c Glut'`
and selected training perturbations from dynamin, clathrin/endocytic, and
synaptic-vesicle traffic.  The exact 5% FDR rows in the focal class were:

| training perturbation | focal `n_degs` | FDR-significant genes in `151 TH Prkcd Grin2c Glut` |
| --- | ---: | --- |
| `Dnm1` | 1 | `Dnm1` only, logFC -0.712, q = 4.09e-25 |
| `Bin1` | 1 | `Bin1` only, logFC -0.331, q = 2.89e-6 |
| `Cltc` | 3 | `Rbms1`, `Ero1b`, `Gabra4`, all q = 0.042 |
| `Stxbp1` | 1 | `Stxbp1` only, logFC -0.663, q = 9.38e-19 |
| `Synj1` | 1 | `Synj1` only, logFC -0.583, q = 3.11e-7 |
| `Syn1` | 1 | `Syn1` only, logFC -0.834, q = 1.59e-24 |
| `Vamp1` | 1 | `Vamp1` only, logFC -0.465, q = 1.87e-3 |
| `Nsf` | 0 | none; best adjusted q was 0.835 |
| `Syn2` | 0 | none; self q = 0.425 |
| `Syt2` | 0 | none; best adjusted q was 1 |
| `Unc13a` | 0 | none; self q = 0.666 |

The broader all-cell query gave the same pattern.  Dnm1 had significant target
RNA reduction in 9 neuronal groups but zero downstream DEGs at both 5% and 10%
FDR in every group.  Bin1 had target-only hits in the 054, 151, and 191 groups
and only two weak downstream singleton hits across the whole 23-group surface
at 10% FDR.  Cltc was the stronger counterexample: it produced downstream
responses in selected neuronal groups, including 3 downstream genes in 151 and
41 DEGs in 155 MB Glut, but the internal Cltc report showed that its global
profile was proteostasis/stress-like rather than a clean phenocopy of dynamin,
Synj1, Hspa8, Bin1, or Nsf.

# Biological transfer to Dnm2

`Dnm2` encodes dynamin-2, a large GTPase that can perform membrane fission in
clathrin-mediated endocytosis.  Dynamin proteins are legitimate biological
neighbors of clathrin, endophilin/amphiphysin, and synaptojanin in synaptic
vesicle endocytosis: Brodin, Low and Shupliakov 2000 (PMID 10851177,
DOI 10.1016/s0959-4388(00)00097-0) reviewed these as sequential components of
clathrin-mediated vesicle recycling.  Dynamin-1 and dynamin-2 can be partly
redundant for endocytic vesicle fission but differ in membrane-domain
targeting in non-neuronal model cells, as shown by Altschuler et al. 1998
(PMID 9864361, DOI 10.1083/jcb.143.7.1871).  In an in vivo central synapse,
single conditional deletion of Dnm1, Dnm2, or Dnm3 did not disrupt calyx of
Held development, whereas combined Dnm1/Dnm3 loss and further Dnm2 loss
created stronger developmental phenotypes (Fan, Funk and Lou 2016,
PMID 27251629, DOI 10.1523/JNEUROSCI.3804-15.2016).

That causal chain argues against a broad response-breadth prediction for an
acute sparse Dnm2 loss in recovered juvenile thalamic neurons:

1. Intervention: CRISPR loss of Dnm2 was expected to reduce dynamin-2 function
   in a sparse, mosaic subset of postmitotic neurons.
2. Direct consequence: endocytic fission capacity could be partially impaired,
   but the relevant synaptic-vesicle function is shared with Dnm1/Dnm3 and is
   not an obligate Dnm2-only step in central neurons.
3. Propagation: if Dnm2 behaved like Dnm1, Synj1, Bin1, or Stxbp1 in this
   dataset, the focal secondary nuclear transcriptome would remain buffered.
   A Cltc-like response is possible for a sufficiently central coat defect,
   but Cltc is upstream/core clathrin coat loss, not a specific dynamin-2
   isoform loss, and Cltc itself yielded only three 5% FDR genes in the focal
   class.
4. Exposure and selection: the snRNA-seq endpoint is survivor-conditioned; a
   membrane-traffic or myelination phenotype, such as the peripheral
   Schwann-cell/neuronal endocytosis defect described for DNM2 neuropathy
   mutants by Sidiropoulos et al. 2012 (PMID 22451505, DOI 10.1093/brain/aws061),
   would not necessarily appear as a broad nuclear DEG count in recovered
   thalamic glutamatergic nuclei.
5. Measured endpoint: the close focal analogs Dnm1, Bin1, Synj1, and Stxbp1
   crossed FDR only through their own transcripts, and several trafficking
   genes crossed no genes at all.

The resulting prediction is `1`, driven mostly by the within-dataset
observation that the nearest endocytic/synaptic perturbations are
target-transcript-only or downstream-null in `151 TH Prkcd Grin2c Glut`.
External biology supports treating Dnm1, Synj1, Bin1 and Cltc as relevant but
imperfect comparators; it does not provide evidence that acute Dnm2 loss should
be a large outlier from the buffered dynamin/accessory-endocytosis branch.
Because `n_degs` includes self-transcript hits, and Dnm2 is a broadly expressed
dynamin isoform, I allowed one significant gene rather than zero.

# Limits

The largest uncertainty is the held-out self transcript.  The training endpoint
counts the target RNA itself, and self-significance varies across genes with
guide activity, expression, recovered perturbed-cell count, and nuclear
transcript behavior; Dnm2's own focal log fold change and q-value are absent.
The second uncertainty is isoform specificity.  Dnm2 is ubiquitous and can act
outside the synaptic-vesicle pool, whereas the visible closest paralog is Dnm1,
not Dnm3, and no AP-2 or endophilin perturbation was available as a perfect
focal analog.  Finally, all same-experiment reports are derived from the same
Parquet-scale PerturbAI experiment, so they helped interpret analogs but did
not constitute independent replication.
