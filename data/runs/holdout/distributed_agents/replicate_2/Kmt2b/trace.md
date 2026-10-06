# Prediction trace for held-out `Kmt2b`

## Question and interpretation

The held-out manifest `[local file: 121_Kmt2b.csv]` contains one requested perturbation, `Kmt2b`. I interpreted the endpoint as the number of measured genes in `151 TH Prkcd Grin2c Glut` with `pvals_adj < 0.05` after acute P16 AAV-CRISPR loss of the target in recovered NeuN+ mouse nuclei.

The answer therefore must be a count of downstream DE genes for the held-out `Kmt2b` knockout in the focal thalamic glutamatergic class, not a p-value, probability, disease score, target-transcript knockdown, or germline phenotype. I treated zero as "no measured gene crosses FDR 0.05 in this exact assay"; a nonzero call is a prediction about assay-visible breadth, not about biological essentiality.

## Sources used

- Direct training endpoint: `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`, 1,674 non-held-out perturbations.
- Direct differential-expression data: `[local file: training_de_all_cell_groups.parquet]`. I queried `group_name == "151 TH Prkcd Grin2c Glut"` for candidate KMT2/H3K4/chromatin analogs and counted `pvals_adj < 0.05`.
- Distributed Agents same-experiment semantic corpus: `perturbai-july-260713-sourceguard-1773-v1`. I used `target_context`, `common_outbound_neighbors`, `profile_compare`, and `profile_cohort` outputs for report-authored cross-target contrasts and focal logFC profile similarities. This corpus is another derived view of the same experiment, not an independent replication.
- PubMed literature:
  - Zech et al. 2016, PMID 27839873, DOI `10.1016/j.ajhg.2016.10.010`: KMT2B haploinsufficiency causes early-onset generalized dystonia.
  - Meyer et al. 2016, PMID 27992417, DOI `10.1038/ng.3740`: heterozygous KMT2B/MLL4 variants cause complex childhood-onset dystonia responsive to DBS in some patients.
  - Zech, Lam and Winkelmann 2019, PMID 31768667, DOI `10.1007/s11910-019-1007-y`, and Cif et al. 2020, PMID 33150406, DOI `10.1093/brain/awaa304`: DYT-KMT2B is typically limb-onset childhood dystonia with neurodevelopmental and systemic features, usually from loss-of-function/haploinsufficiency.
  - Ladopoulos et al. 2013, PMID 23358417, DOI `10.1128/MCB.01721-12`: KMT2B, also named MLL2/WBP7 in mouse work, is an H3K4 methyltransferase needed to keep a CpG-island promoter active and unmethylated.
  - Hu et al. 2013, PMID 23934151, DOI `10.1038/nsmb.2653`, and Denissov et al. 2014, PMID 24423662, DOI `10.1242/dev.102681`: the Mll2/Kmt2b COMPASS branch deposits H3K4me3 at bivalent promoters in embryonic stem cells, while Mll1/Kmt2a can back up only some of that activity.
  - Hu et al. 2017, PMID 28157506, DOI `10.1016/j.molcel.2017.01.013`: Mll2/KMT2B-COMPASS H3K4me3 is required at a subset of developmental regulatory loci in primordial-germ-cell specification.
  - Kubo et al. 2024, PMID 38513661, DOI `10.1016/j.molcel.2024.02.030`: acute KMT2B depletion can reduce H3K4me1 at KMT2C/D-independent enhancers during ESC neural differentiation, tying KMT2B to a subset of enhancer-promoter contacts in a developmental model.

## Computation over the training dataset

I first confirmed that the held-out target does not appear in the training count file and scanned the focal-cell training counts for H3K4 and adjacent chromatin perturbations. The exact focal counts used below came from both the count CSV and a direct Parquet check:

```sql
select gene_target,
       sum(case when pvals_adj < 0.05 then 1 else 0 end) as n_sig
from read_parquet('training_de_all_cell_groups.parquet')
where group_name = '151 TH Prkcd Grin2c Glut'
  and gene_target in (...)
group by gene_target;
```

I then used Distributed Agents `profile_compare` in the same focal group with `entity_column=gene_target`, `feature_column=names`, `value_column=logfoldchanges`, and `pvals_adj < 0.05` as the significance definition for the cohort `Kmt2a`, `Kmt2c`, `Setd1a`, `Crebbp`, `Ep300`, `Setd2`, `Chd8`, and `Kat6b`. This measured whether candidate analogs merely had positively correlated whole-transcriptome logFC vectors or also shared the signed top/significant features that define a transferable module.

## Target-specific reasoning

### `Kmt2b`

`Kmt2b` is an H3K4 methyltransferase in the SET1/MLL or COMPASS family. The relevant external biology makes `Kmt2a` the closest assayed analog: mammalian KMT2A/MLL1 and KMT2B/MLL2 are sister promoter-oriented Trithorax/COMPASS methyltransferases, whereas KMT2C/KMT2D are the better-known enhancer H3K4me1 writers. KMT2B haploinsufficiency is a strong monogenic dystonia mechanism in humans, so I did not treat it as a random chromatin gene. At the same time, several of the sharpest KMT2B molecular phenotypes are in embryonic stem cells, bivalent developmental promoters, and differentiation systems. That is a partial mismatch to sparse P16 editing of already specified, postmitotic thalamic glutamatergic neurons.

Biologically relevant training perturbations:

| training perturbation | observed focal `n_degs` | role in the `Kmt2b` prediction |
|---|---:|---|
| `Kmt2a` | 24 | Closest measured paralog and best positive analog. Its 151 signature had 12 down and 12 up genes at FDR 0.05; the most significant down-regulated genes included `Nr2f1`, `Pcdh7`, `Lhx9`, the self target `Kmt2a`, `Camk2d`, `Usp43`, `Pcdh10`, and `Grik2`, while induced genes included `Igfbp5`, `Tnr`, `Cx3cl1`, `Atxn2l`, `Luc7l`, `Txndc5`, `Gabrd`, `Cry2`, `Acsl3`, and `Car4`. The Distributed Agents corpus described this as a sparse, glutamatergic-biased Kmt2a response with the 151 class carrying 25 of 30 downstream FDR<0.10 genes genome-wide. |
| `Kmt2c` | 0 | Same KMT2 family but a poorer mechanistic analog because it is in the MLL3/enhancer branch. It was completely flat in the focal 151 group and, according to the corpus, had only a single FDR<0.10 gene across its broader surface. This is a boundary against assigning a broad family-wide effect to every KMT2 enzyme. |
| `Setd1a` | 368 | Same H3K4/COMPASS axis and a strong positive control for the ability of 151 TH nuclei to report loss of an H3K4 writer. Its broad focal response was dominated by down-regulated mitochondrial, ER/Golgi, GPI-anchor, ciliary, lysosomal, and RNA-biogenesis genes. It is an upper-bound counterexample rather than a direct quantitative analog: corpus Finding `Setd1a:F010` reports that measured KMT2/chromatin-disorder comparators did not phenocopy Setd1a, and in the focal cohort `Kmt2a` and `Setd1a` shared only one significant up-regulated gene and no significant down-regulated genes. |
| `Crebbp` | 8 | Enhancer/chromatin neurodevelopmental regulator with a weak but nonzero response in the same cell group. It keeps the prediction in a weak-to-moderate band rather than forcing zero. |
| `Ep300` | 0 | Paralogue of `Crebbp` and an enhancer coactivator but flat in the focal cell group; a counterexample to simple coactivator or chromatin-label transfer. |
| `Setd2` | 1 | H3K36 methyltransferase, singleton focal response; useful as a boundary showing that many histone methyltransferases remain nearly silent in this P16 assay. |
| `Kat6b` | 0 | Histone acetyltransferase and neurodevelopmental-disease chromatin gene, completely flat despite 150 matched perturbed 151 nuclei. The corpus specifically contrasts this `Kat6b` null with measurable `Crebbp` and `Kmt2a` responses. |
| `Chd8` | 61 | Broader chromatin remodeler ASD gene. It demonstrates assay sensitivity to chromatin perturbation but is mechanistically farther from KMT2B; the corpus found CHD and other ASD chromatin genes did not phenocopy one another. |

The same-experiment corpus gave two particularly important guardrails. First, `Kmt2a:F005` states that Kmt2a did not phenocopy the represented H3K4 writer relatives: `Setd1a` was broad and largely non-overlapping, while `Kmt2c` was almost flat. Second, `Setd1a:F010` states that measured KMT2 and chromatin-disorder comparators did not collapse into the Setd1a state. The bounded focal profile cohort agreed with this: among the eight KMT2/H3K4/chromatin candidates, top-tail overlap was low overall, with median significant-program overlap coefficient 0 in both positive and negative directions. For example, the `Kmt2a` versus `Kmt2c` pair had zero significant-gene intersection, and `Kmt2a` versus `Setd1a` had a small same-direction whole-profile correlation but only 1 intersecting significant up gene and 0 intersecting significant down genes.

Those contrasts argue against a generic bulk heuristic such as "all H3K4 writers are strong" or "all developmental KMT2 genes are flat". I weighted `Kmt2a` most heavily because it is the assayed promoter-branch paralog and because its focal count of 24 is directly in the requested endpoint. I treated `Kmt2c`, `Ep300`, `Setd2`, and `Kat6b` as proof that developmental chromatin regulators can be buffered in this assay, pulling the point estimate below `Kmt2a`. I treated `Setd1a` as evidence for a true possible neuronal H3K4 effect but too broad and too divergent to transfer quantitatively.

My zero/nonzero decision was therefore nonzero: human KMT2B loss-of-function disease genetics, KMT2B/MLL2 promoter H3K4 function, and the modest but clear `Kmt2a` focal response make a complete FDR-level null less likely than the prior 72% zero rate. The approximate count is just under `Kmt2a`, not near `Setd1a`; I predict 18 focal FDR<0.05 genes.

## Limits and extrapolation

- `Kmt2b` itself was deliberately absent from both the Parquet and training-count CSV. No expression signature, DEG count, target down-regulation, or matched perturbed-cell count for `Kmt2b` was available.
- The closest same-complex subunits for a KMT2A/B complex, such as `Wdr5`, `Ash2l`, `Rbbp5`, `Dpy30`, `Men1`, `Hcfc1`, and `Psip1`, were not present as focal training perturbations, so the comparison is largely paralog and broader pathway transfer.
- Human DYT-KMT2B is a developmental haploinsufficiency syndrome. The requested experiment is acute, sparse CRISPR in postnatal neurons recovered 3-4 weeks later, so developmental disease importance can overstate basal snRNA-seq response breadth.
- H3K4me3/H3K4me1 chromatin papers are mostly from embryonic stem cells, primordial germ cells, oocytes, or cancer/developmental models, not from P16 thalamic glutamatergic neurons.
- The profile similarities over logFC can be inflated by shared background structure in genes that are not FDR-significant. I used signed significant-tail overlap and direct counts as the decisive evidence; those show the local chromatin regulators are mostly non-phenocopic.
