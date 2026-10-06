# Tspan12 n_degs forecast

Endpoint: predict the held-out `n_degs` for `Tspan12` in `151 TH Prkcd Grin2c Glut`, where `n_degs` is the count of measured genes with BH-adjusted Wilcoxon `p < 0.05`.

Target prior from the declared biology-only bundle:

- The exact focal non-target expression measurement shows `Tspan12` is detectable but low in this assayed thalamic NeuN-positive population: mean raw UMI `0.323`, pseudobulk CPM `20.256`, and `25.905%` of 23,679 non-target nuclei expressing at least one UMI.
- The established molecular operation is a plasma-membrane Norrin/FZD4/LRP5/6 beta-catenin co-receptor function in retinal endothelial cells. The bundle adjudicates the best match for the thalamic neuronal assay as `mouse_non_neural_or_systemic`, with mouse loss phenotypes confined to retinal vasculature and blood-retina-barrier maintenance.
- The functional-stock card calls the 21-28 day post-edit harvest an early or partially depleted phase, because adult endothelial Tspan12 loss reaches full barrier dysfunction only over roughly 2-3 months; that timing is informative about slow TSPAN12-dependent function but not directly transferable to postmitotic thalamic neurons.

Training measurements used:

- The focal 151-class training table has 1,674 perturbations; 1,205 are exact zeros, the median is `0`, the 90th percentile is `2`, and 1,571 perturbations, `93.85%`, have `n_degs <= 10`.
- The closest Norrin receptor-side training perturbations in the count table were quiet: `Fzd4 = 0`, `Lrp5 = 0`, and `Lrp6 = 4`.
- The declared Parquet confirmed that `Fzd4` and `Lrp5` had no significant 151-class genes at BH-adjusted `p < 0.05`. `Lrp6` had four small hits, with maximum absolute log-fold-change `0.398`, consistent with a tiny rather than broad receptor-side footprint.
- `Ctnnb1 = 383` and `Tcf7l2 = 106` show that core beta-catenin/Wnt transcriptional perturbations can be visible in this class, but I did not treat them as close scale donors because TSPAN12 is ligand-specific and upstream, with its demonstrated cell-autonomous function outside neurons.

Synthesis:

Low in-assay `Tspan12` RNA argues that enough cells could be edited for a response, so I did not make an expression-absence call. The endpoint-scale evidence still points to a zero or very small footprint: the 151-class endpoint is strongly zero-inflated, the functional receptor-side genes nearest to TSPAN12 are 0/0/4 DEG perturbations, and the target-specific biology lacks a demonstrated thalamic neuronal requirement while suggesting delayed realization of the best-known endothelial function. I therefore choose the modal low-footprint value.

Predicted `n_degs`: `0`
