Task: From the differential-expression dataset and training DEG counts, predict
the number of differentially expressed genes caused by each requested held-out
genetic perturbation in `151 TH Prkcd Grin2c Glut` cells.

What you are predicting (the held-out readout):
For each perturbation, `n_degs` is the number of measured genes with a
Benjamini–Hochberg-adjusted Wilcoxon p-value below 0.05 in `151 TH Prkcd Grin2c
Glut` cells. The requested perturbations were held out from the supplied
Perturb-seq differential-expression dataset completely. Their DEG counts and
expression signatures are not present in either input.

You must transfer information from the expression signatures and DEG counts of
the ~1,700 non-held-out perturbations, together with your knowledge of what each
held-out gene does. Useful evidence may include perturbations of paralogs,
members of the same complex or pathway, upstream or downstream regulators, and
other perturbations producing biologically analogous transcriptional states.

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

A CSV file at {{training_counts_path}} contains the observed endpoint for the
non-held-out training perturbations in the focal cell group. Columns:
  - target_name: perturbed mouse gene
  - n_degs: number of genes with pvals_adj < 0.05 in `151 TH Prkcd Grin2c Glut`

A CSV file at {{target_list_path}} contains exactly one column, `target_name`.
These are the held-out perturbations to predict in this run. None appears as a
`gene_target` in the differential-expression parquet or as a `target_name` in
the training-count CSV.

The input differential-expression signatures and training counts are central
evidence, not merely format references. Analyze the non-held-out perturbations
to identify within-dataset analogs and calibrate the expected response breadth
of each held-out target. External biological knowledge should help determine
which within-dataset comparisons are mechanistically appropriate; superficial
signature frequency or gene-family membership alone is not sufficient.

Experimental Context:
- Species/strain: Mouse, C57BL/6J × Cas9 transgenic, mixed sexes.
- Age window: AAV-PHP.eB delivered retro-orbitally at post-natal day 16; brains harvested at post-natal day 37–44 (3–4 weeks post-perturbation). Postmitotic, postnatal, juvenile-to-young-adult brain.
- Perturbation modality: Acute, mosaic, sparse CRISPR-Cas9 loss-of-function via AAV-PHP.eB delivery of pooled gRNAs (4 gRNAs/gene). NOT germline KO, NOT conditional Cre-lox KO, NOT siRNA/shRNA knockdown, NOT pharmacological inhibition. Average on-target downregulation ~18% per gRNA at the mRNA level.
- Tissue scope: Whole brain minus olfactory bulb and hindbrain; NeuN+ neuronal nuclei FACS-enriched. Non-neuronal cell types (astrocytes, microglia, oligodendrocytes, vascular) are largely absent or under-sampled.
- Focal cell group: `151 TH Prkcd Grin2c Glut`, selected because it had the strongest perturbation responses in this experiment.
- Readout: snRNA-seq (10x Flex V2). DEGs computed via Wilcoxon rank-sum test (Scanpy `rank_genes_groups`) at the single-nucleus level against pooled non-targeting controls, with Benjamini-Hochberg correction.
- Effect direction convention: `logfoldchanges` is perturbed vs. non-targeting control (positive = up in knockout).
- `n_degs` is an assay- and power-dependent response-breadth endpoint. It is not a direct measurement of biological importance, editing efficiency, viability, or effect magnitude. Weak or unchanged target RNA does not by itself imply failed editing.

Required Outputs:
You MUST create the following two output files in the working run directory.

1. Reasoning trace (`./trace.md`)

Describe how you arrived at each prediction in enough detail that a reviewer
can follow your reasoning. Include:
- The question as you understood it and any ambiguities you resolved.
- What sources you drew on (the input DE dataset, training DEG counts, specific external databases by name, literature, prior knowledge). Name any internal database or corpus used.
- The key reasoning steps. For computational steps over the parquet, describe what was computed and why; include code only where the operation is non-obvious.
- For every requested held-out target, the biologically relevant training perturbations you compared it with, their observed DEG counts and expression-pattern evidence, and why those are appropriate analogs or counterexamples.
- The biological rationale for the zero/nonzero decision and approximate DEG count for every held-out target. Distinguish predictions driven by within-dataset evidence from predictions driven by external gene-function knowledge.
- Citations for biological mechanisms and external knowledge (author + year with DOI/PubMed ID, or named database with version).
- An explicit statement of the limits of your reasoning: where the evidence is weak, where the comparison is imperfect, and where the prediction is extrapolation.

Develop the target-specific reasoning before finalizing the predicted counts.
Do not assign predictions using one generic bulk heuristic and then retrofit
generic rationales, including when many targets are requested in one run.

2. Final answer (`./answer.txt`)

The final answer MUST contain a single fenced code block tagged `tsv` with a
header and exactly one data row for every target in the requested-target CSV,
in this exact format:

```tsv
target_name	predicted_n_degs
ExampleGeneA	0
ExampleGeneB	37
```

Rules for the table:
- `target_name` must be a value in the requested-target CSV, written exactly as it appears there.
- `predicted_n_degs` must be one non-negative integer point prediction. Zero means no gene is predicted to pass FDR 0.05; any positive integer means an effect is predicted.
- Include every requested target exactly once and no other targets. Preserve requested-target order.
- Tab-separated, with no duplicate targets, ranges, uncertainty intervals, or alternative point estimates.
- Do not add prose outside the single fenced block in `answer.txt`.
