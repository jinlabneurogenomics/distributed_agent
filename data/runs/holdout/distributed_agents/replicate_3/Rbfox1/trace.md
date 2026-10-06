# Rbfox1 held-out DEG-count prediction

## Question and interpretation

The requested held-out manifest contains one target, `Rbfox1`. I interpreted the endpoint as the exact training endpoint: the integer number of measured genes in `151 TH Prkcd Grin2c Glut` whose `pvals_adj` is below 0.05 in the Scanpy Wilcoxon comparison of sparse AAV-CRISPR perturbed nuclei against matched controls.

`Rbfox1` itself is absent from both supplied training inputs, so I did not use an Rbfox1 expression signature or a direct Rbfox1 count. I used focal-cell counts and focal-cell differential-expression profiles for non-held-out training perturbations as calibration evidence, and used external biology only to decide which training perturbations were plausible mechanistic analogs or counterexamples.

## Sources used

- `training_de_all_cell_groups.parquet`: focal `151 TH Prkcd Grin2c Glut` log2 fold-change vectors and FDR-significant gene sets for selected training comparators.
- `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`: observed focal `n_degs` for all 1,674 non-held-out training perturbations.
- `196_Rbfox1.csv`: the held-out target order; this run requested only `Rbfox1`.
- PerturbAI atlas dataset portrait in the run-local `codex_runtime/pipeline/dataset_context.md`, used for assay semantics and for the warning that the corpus is a same-experiment interpretation layer, not an independent replicate.
- PerturbAI July 260713 sourceguard-1773 corpus, accessed through the `findings-ledger-skill`, for same-experiment reports on `Hnrnpu`, `Hnrnpc`, `Tardbp`, and `Rnpc3`.
- Run-local Distributed Agents runtime profile-neighborhood tool, used to audit selected focal log-fold-change profiles.
- The bundled PerturbAI mouse gene-annotation and gene-analog-nomination stores, using GO, MSigDB/WikiPathways, functional-class annotations, and pinned STRING v12.0 physical interactions. These were used to nominate comparators, not to score the endpoint.
- NCBI/PubMed for Rbfox1 mechanism:
  - Gehman et al. 2011, *Nature Genetics*, DOI 10.1038/ng.841, PMID 21623373.
  - Weyn-Vanhentenryck et al. 2014, *Cell Reports*, DOI 10.1016/j.celrep.2014.02.005, PMID 24613350.
  - Lee et al. 2016, *Neuron*, DOI 10.1016/j.neuron.2015.11.025, PMID 26687839.

## Computational checks

The focal training endpoint is extremely zero-inflated: 1,205 of 1,674 training targets have `n_degs = 0`; the median is 0, the 75th percentile is 1, the 95th percentile is 18, and only 43 targets have 100 or more focal DEGs. This makes a zero prediction plausible by prior rate, but I did not use that rate alone.

I first nominated mechanistic comparators for absent `Rbfox1` with `gene-analog-nomination-skill` against the actual training universe. The highest-priority candidate pool had no exact paralog or exact complex member available. It was dominated by RNA-binding and splicing annotations, notably:

- GO:0000381, `regulation of alternative mRNA splicing, via spliceosome`;
- GO:0003730, `mRNA 3'-UTR binding`;
- GO:0043484, `regulation of RNA splicing`;
- `WP_MRNA_PROCESSING`;
- a pinned STRING v12.0 physical interaction between mouse Rbfox1 and Atxn2.

Then I extracted focal profiles for 36 candidate or counterexample perturbations nominated from those RNA-processing, hnRNP, Rett/MeCP2, and core-spliceosome neighborhoods. The extraction used predicate pushdown to avoid loading the full atlas:

```python
flt = (
    (pc.field("group_name") == "151 TH Prkcd Grin2c Glut")
    & pc.is_in(pc.field("gene_target"), value_set=pa.array(selected))
)
```

The filtered table contained 621,324 focal rows. Recounting `pvals_adj < 0.05` from those Parquet rows exactly matched every selected value in the training count CSV.

## Rbfox1-specific reasoning

### Available analogs and counterexamples

`Rbfox1` is an Rbfox/Fox-1-family RNA-binding protein that binds the UGCAUG motif and regulates neuronal alternative splicing. Brain Rbfox1 loss in mice changes splicing of synaptic and membrane-excitability transcripts and produces neuronal hyperexcitability; HITS-CLIP maps a broad Rbfox splicing-regulatory network linked to brain development and autism; cytoplasmic Rbfox1 also regulates synaptic/autism-related mRNAs. Those external papers make `Rbfox1` very plausible as a neuronal regulator, but the first paper also reported many splicing changes with few whole-transcript abundance changes. That distinction matters because this Perturb-seq endpoint is gene-level 3-prime snRNA-seq abundance, not junction-level splicing, intron retention, cytoplasmic translation, or mRNA localization.

The closest annotated training perturbations were mostly flat or weak in the focal cell group:

| comparator | focal n_degs | why it was considered | focal expression-pattern evidence |
|---|---:|---|---|
| `Tia1` | 0 | RNA-binding, mRNA 3'-UTR binding, and regulation of alternative splicing | no FDR<0.05 genes in `151 TH Prkcd Grin2c Glut` |
| `Fmr1` | 0 | neuronal RBP, mRNA 3'-UTR binding, alternative-splicing annotation | no focal FDR genes |
| `Fxr1` | 0 | FMRP-family 3'-UTR/mRNA-binding factor | no focal FDR genes |
| `Syncrip` | 0 | mRNA 3'-UTR/RNA-binding factor in the Rbfox1 nomination pool | no focal FDR genes |
| `Atxn2` | 8 | the only direct STRING v12.0 physical partner surfaced for Rbfox1 | only eight focal DEGs |
| `Hnrnpa2b1` | 11 | hnRNP-family RNA-binding comparator | only eleven focal DEGs; just 1 FDR gene overlapped `Tardbp` and 2 overlapped `Hnrnpc` |
| `Hnrnph2` | 4 | RNA-splicing regulator from the GO:0043484 nomination | only four focal DEGs |

These are not exact Rbfox1 phenocopies, but they are the strongest evidence that loss of a sequence-specific RBP can be invisible at a gene-abundance endpoint even in this high-yield thalamic glutamatergic class.

I also checked moderate RNA-processing positives:

| comparator | focal n_degs | evidence and interpretation |
|---|---:|---|
| `Hnrnpc` | 122 | The corpus reported an RNA-processing rewiring state after `Hnrnpc` loss and noted that `Hnrnpc` was only a weak, restricted branch relative to core spliceosome perturbations. In the focal Parquet, `Hnrnpc` and `Tardbp` shared only 15 significant genes despite whole-profile Pearson 0.667. |
| `Tardbp` | 210 | The corpus found a real but compact TDP-43 response whose strongest neighbors were spliceosome/proteostasis perturbations, not disease-family RBP comparators such as `Tia1`, `Atxn2`, or `Hnrnpa2b1`. This is a direct warning not to map every ALS/RBP-like gene onto the Tardbp count. |
| `Matr3` | 149 | Another RBP with a medium response; mechanistically less close to Rbfox1 than Atxn2/Tia1/Fmr1 because it was nominated through broad nucleic-acid/RNA-binding annotations. |
| `Snrnp70` | 213 | A major-spliceosome snRNP factor. Its count shows RNA-processing perturbations can be nonzero, but it is a core spliceosome component rather than a sequence-specific Rbfox-like regulator. |

Finally, I explicitly treated the broad core-spliceosome and RNA-processing stress programs as counterexamples rather than direct positive analogs:

| comparator | focal n_degs | evidence and reason for down-weighting |
|---|---:|---|
| `Rnpc3` | 868 | Minor-spliceosome factor. The corpus reported convergence with `Prpf6`, `Snrnp70`, `U2af2`, `Cdc40`, and `Hnrnpu`; in the focal profile it shared 194 FDR genes with `U2af2` and 174 with `Hnrnpu`. This is a broad spliceosome-stress state, not an Rbfox-like sequence-specific splicing regulator. |
| `U2af2` | 828 | Core 3-prime splice-site factor. It shared 171 focal FDR genes with `Hnrnpu` and 130 with `Cdc40`, again marking the broad spliceosome block. |
| `Prpf6` | 454 | U4/U6-U5 tri-snRNP factor; it shared 121 focal FDR genes with `U2af2`. |
| `Cdc40` | 624 | Activated-spliceosome factor in `WP_MRNA_PROCESSING`; strong but too core to use as a direct Rbfox1 analog. |
| `Hnrnpu` | 733 | hnRNP-family and RNA-processing perturbation. The same-experiment corpus specifically says measured hnRNP-family perturbations did not phenocopy `Hnrnpu`, even though `Hnrnpu` converged with spliceosome/RNA-processing targets. I therefore used it as evidence for the broad stress block, not as a direct Rbfox1 count donor. |

The Rett/MeCP2 WikiPathways nominations also failed specificity checks. `Rest` had 0 DEGs and `Mecp2` had 16, while `Sin3a` had 1,433; that spread is too large for the pathway membership to be quantitatively useful for `Rbfox1`.

### Decision

I predict `Rbfox1` will have no focal genes pass FDR 0.05.

The main within-dataset evidence for zero is that the most specific available mRNA-binding and alternative-splicing nominees were flat or nearly flat at the same gene-abundance endpoint: `Tia1`, `Fmr1`, `Fxr1`, and `Syncrip` all had 0; the direct STRING partner `Atxn2` had 8; `Hnrnpa2b1` had 11; `Hnrnph2` had 4. The nonzero RNA-processing perturbations in the 100 to 900 DEG range mostly reflect essential spliceosome components or broad Hnrnpu/Tardbp/Hnrnpc stress programs that the same-experiment corpus separated from generic RBP family membership. Because Rbfox1 is a sequence-specific Rbfox regulator rather than a core spliceosome factor, those broad programs are upper-bound counterexamples.

The external evidence strengthens the biological plausibility of `Rbfox1` perturbation in neurons but also points to splice-junction, isoform, and cytoplasmic mRNA regulation as the primary readouts. Those are exactly the modes that a 10x 3-prime, gene-level Wilcoxon test can miss. Combining those facts pushed the prediction from a small nonzero count down to zero:

```tsv
target_name	predicted_n_degs
Rbfox1	0
```

## Limits

- `Rbfox2` and `Rbfox3` were absent from the supplied focal training table, so there was no exact Rbfox-family calibration point.
- GO and WikiPathways memberships are broad for RNA-binding genes; several nominated targets were chromatin or Rett-related genes rather than mechanistic Rbfox1 phenocopies.
- The same-experiment corpus had no `Rbfox1` ledger records, so all same-experiment interpretation came from neighboring training perturbations.
- Whole-gene 3-prime snRNA-seq cannot directly see alternative exon inclusion, cryptic exons, intron retention, mRNA localization, or translation. This probably underestimates Rbfox1's real post-transcriptional effect.
- The final zero is therefore an endpoint-specific extrapolation: Rbfox1 is expected to be biologically active in neurons, but I predict that its acute sparse CRISPR perturbation will not create a reproducible enough whole-gene abundance footprint in recovered `151 TH Prkcd Grin2c Glut` nuclei to pass BH FDR 0.05.
