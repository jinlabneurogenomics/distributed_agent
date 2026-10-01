# S5B — flags by DEG footprint

The left view is the 100%-stacked composition by nonzero target-DEG bin; the
right view is the conditional KDE of `log10(total DEG + 1)` within each flag.
The archived aggregate bin table and both source figures are retained here.

`prepare_notebook_input.py` materializes the KDE's two required row-level
columns from the archived workbook and target-footprint table.  This keeps the
notebook input compact while preserving the exact 5,125 populated-flag rows.

Archived source:
`manuscript/_archive_260924/fig2/_debug/current_flag_distributions/`.
