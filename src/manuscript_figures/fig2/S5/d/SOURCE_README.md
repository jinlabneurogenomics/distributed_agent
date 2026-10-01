# S5D — literature-flag heatmap variants

The retained upper heatmap combines load-bearing, evidence-only, and
non-admissible findings, restricted to target × cell-class blocks with at least
one local DEG.  The retained lower heatmap uses load-bearing findings only and
includes every explicit canonical cell-class mention, regardless of local DEG
support.

The three copied generators define the target order, placement filters, and
decisiveness rule (`Disagree > Agree > Inferred > No Literature > Unassessed`).
`deg_universe_cells.csv` supplies the DEG-sorted target order and local-DEG
universe; `phenotype_findings_by_perturbation_deg_ordered.csv` is the reader
view from which both matrices and the finding-tier density curves are rebuilt.

Archived source:
`manuscript/_archive_260924/fig2/_debug/meaningful_biology_pipeline/steps/06_two_corpus_union/run/`.
