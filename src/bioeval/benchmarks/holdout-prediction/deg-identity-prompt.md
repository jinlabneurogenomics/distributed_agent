Task: From the differential-expression dataset, predict the identities of the
25 most strongly up-regulated and 25 most strongly down-regulated genes caused
by each requested held-out genetic perturbation in `151 TH Prkcd Grin2c Glut`
cells.

What you are predicting (the held-out readout):
Each requested perturbation has a strong response in the focal cell group,
defined as at least 50 genes with a Benjamini–Hochberg-adjusted Wilcoxon p-value
below 0.05. For each target, you must predict its top 25 up-regulated genes and
top 25 down-regulated genes. The held-out reference rankings are based on the
signed Scanpy Wilcoxon `scores`: decreasing score for up-regulated genes and
increasing score for down-regulated genes. The reference lists are the first 25
genes of the appropriate sign in those full rankings, whether or not every gene
passes FDR 0.05. The perturbed target gene itself remains eligible if it appears
in the ranked results.

The requested perturbations were held out from the supplied Perturb-seq
differential-expression dataset completely. Their expression signatures are
not present in the input. You must transfer information from the full
expression signatures of the ~1,700 non-held-out perturbations plus your
knowledge of what each held-out gene does. Useful evidence may include
perturbations of paralogs, members of the same molecular complex or pathway,
upstream or downstream regulators, and perturbations producing biologically
analogous transcriptional programs in this experiment.

Input Datasets:
A parquet file at {{training_de_path}} contains per-gene differential-expression
statistics for all non-held-out perturbations. Each row is one (gene, cell type,
perturbation) combination. Columns:

- names: gene symbol (mouse) — the gene whose expression is measured
- group_name: cell type label (Allen brain-atlas taxonomy naming)
- gene_target: perturbation (gene knocked out)
- logfoldchanges: log2 fold change of `names` in perturbed vs matched control cells
- pvals, pvals_adj: raw and BH-adjusted Wilcoxon p-values
- scores
- control_label: the matched non-targeting / safe-targeting control group
- n_pert_matched, n_ctrl_matched: matched perturbed and control nucleus counts

A CSV file at {{training_counts_path}} contains `target_name` and `n_degs` for
the non-held-out training perturbations in `151 TH Prkcd Grin2c Glut`, where
`n_degs` is the number of genes with pvals_adj < 0.05. Use it to identify and
calibrate strong-response training perturbations; use the full DE parquet to
inspect their actual signatures.

A CSV file at {{target_list_path}} contains exactly one column, `target_name`.
These are the strong-response held-out perturbations to predict in this run.
None appears as a `gene_target` in the differential-expression parquet or as a
`target_name` in the training-count CSV.

The input differential-expression dataset is central evidence. Analyze it to
identify mechanistically appropriate perturbation analogs, shared programs,
directional relationships, and response signatures that could transfer to each
held-out target. External knowledge should guide those comparisons and supply
target-specific mechanisms; it should not replace analysis of the supplied
Perturb-seq data.

Experimental Context:

- Species/strain: Mouse, C57BL/6J × Cas9 transgenic, mixed sexes.
- Age window: AAV-PHP.eB delivered retro-orbitally at post-natal day 16; brains harvested at post-natal day 37–44 (3–4 weeks post-perturbation). Postmitotic, postnatal, juvenile-to-young-adult brain.
- Perturbation modality: Acute, mosaic, sparse CRISPR-Cas9 loss-of-function via AAV-PHP.eB delivery of pooled gRNAs (4 gRNAs/gene). NOT germline KO, NOT conditional Cre-lox KO, NOT siRNA/shRNA knockdown, NOT pharmacological inhibition. Average on-target downregulation ~18% per gRNA at the mRNA level.
- Tissue scope: Whole brain minus olfactory bulb and hindbrain; NeuN+ neuronal nuclei FACS-enriched. Non-neuronal cell types (astrocytes, microglia, oligodendrocytes, vascular) are largely absent or under-sampled.
- Focal cell group: `151 TH Prkcd Grin2c Glut`, selected because it had the strongest perturbation responses in this experiment.
- Readout: snRNA-seq (10x Flex V2). DEGs computed via Wilcoxon rank-sum test (Scanpy `rank_genes_groups`) at the single-nucleus level against pooled non-targeting controls, with Benjamini-Hochberg correction.
- Effect direction convention: positive `scores` and `logfoldchanges` are up in the knockout; negative values are down in the knockout.
- Target transcript behavior alone is not a reliable engagement measure.

Required Outputs:
You MUST create the following two output files in the working run directory.

1. Reasoning trace (`./trace.md`)

Describe how you arrived at each predicted signature in enough detail that a
reviewer can follow your reasoning. Include:

- The question as you understood it and any ambiguities you resolved.
- What sources you drew on (the input DE dataset, training DEG counts, specific external databases by name, literature, prior knowledge). Name any internal database or corpus used.
- The key reasoning steps. For computational steps over the parquet, describe what was computed and why; include code only where the operation is non-obvious.
- For every requested held-out target, the biologically relevant training perturbations and signatures you compared it with, including the measured genes, directions, cell context, and why those comparisons are appropriate.
- The biological rationale for the predicted up- and down-regulated programs and key genes for every target. Distinguish predictions driven by within-dataset expression evidence from predictions driven by external gene-function knowledge.
- Direction checks: explain why the principal genes or programs should increase versus decrease after acute target loss rather than merely being associated with the target.
- Citations for biological mechanisms and external knowledge (author + year with DOI/PubMed ID, or named database with version).
- An explicit statement of the limits of your reasoning: where evidence is weak, where analogs may not transfer, and where the prediction is extrapolation.

Develop each target-specific biological model before finalizing its gene lists.
Do not copy one nearest profile, generic stress signature, or globally frequent
set of DE genes across targets and then retrofit generic rationales, including
when many targets are requested in one run.

2. Final answer (`./answer.txt`)

The final answer MUST contain a single fenced code block tagged `tsv` with a
header and exactly 50 data rows per requested target, in this exact format:

```tsv
target_name direction rank gene_name
ExampleTargetA up 1 ExampleGeneA
ExampleTargetA up 2 ExampleGeneB
ExampleTargetA down 1 ExampleGeneC
```

Rules for the table:

- `target_name` must be a value in the requested-target CSV, written exactly as it appears there.
- `direction` must be exactly `up` or `down`.
- For every target, include exactly 25 `up` rows and 25 `down` rows. Within each target and direction, ranks must be the integers 1–25 exactly once; rank 1 is the strongest prediction.
- `gene_name` must be a measured gene appearing in the input parquet's `names` column, written exactly as it appears there.
- A gene may appear at most once within a target and direction. Include every requested target and no other targets.
- Sort rows by requested-target order, then `up` before `down`, then ascending rank.
- Tab-separated. Do not add prose outside the single fenced block in `answer.txt`.
