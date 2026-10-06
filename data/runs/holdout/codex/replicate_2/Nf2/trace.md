# Direct forecast for 151 TH Prkcd Grin2c Glut

## Target

The declared one-row holdout target is `Nf2`.

## Evidence used

- Declared Nf2 biology bundle:
  - In the focal `151 TH Prkcd Grin2c Glut` control nuclei, `Nf2` is measurable: 13,221 of 23,679 nuclei express it, `pct_cells_expressing = 55.8343`, `mean_cp10k = 0.56585`, and `pseudobulk_cpm = 56.9459`.
  - The functional-stock adjudication says a P16 disruptive edit should stop new merlin production and that merlin's dynamic membrane/cytoskeletal/junctional/cytoplasmic/nuclear pools are likely substantially depleted by the P37-P44 harvest.
  - The postnatal mouse-neuron loss prior is real but displaced: conditional Nf2 loss perturbed cerebellar synaptic-terminal organization and excitatory currents, while timing and thalamic transfer remain unresolved.
- Declared 151 DEG-count training table:
  - `Nf2` is absent from the 1,674 exposed training targets.
  - The 151 count distribution is sparse: 1,205/1,674 training targets have `n_degs = 0`; 1,481/1,674 have `n_degs <= 1`; 1,571/1,674 have `n_degs <= 10`.
- Declared Parquet rows and packaged same-experiment Findings for Nf2-relevant training perturbations:
  - Closest membrane-cytoskeleton / Rho / ERM-side perturbations in 151 were flat or self-only: `Rac1 = 0`, `Tiam1 = 0`, `Baiap2 = 0`, `Arhgap32 = 0`, `Cdc42 = 1` with only the self transcript significant, and `Rdx = 1` with only the self transcript significant.
  - Hippo-output evidence did not support a broad TEAD-like transfer: `Tead1 = 0` in the 151 count table, and packaged Findings describe sparse P16 `Tead1` loss as FDR-flat across every measured neuronal class.
  - The represented Ras/ERK branch showed only a tiny 151 transcriptional module: `Braf = 4`, `Map2k1 = 4`, `Map2k2 = 0`, and `Mapk1 = 0`.
  - Larger thalamic programs exist but require different, more direct pathway lesions: `Ctnnb1 = 383`, `Tcf7l2 = 106`, and `Tsc2 = 86` in the FDR<0.05 151 training table.

## Reasoning

`Nf2` is a reachable target in this focal class: the RNA is present in over half of non-target 151 nuclei and the stock card argues that edited cells should lose merlin protein within the 21-28 day assay window. That rules out treating the perturbation as an expression or turnover null.

The expected cellular consequence, however, is not a direct acute transcriptional program. Merlin is a membrane-cytoskeleton and signaling adaptor. In the same 151 assay, the nearest represented structural/Rho/ERM genes were overwhelmingly quiet, and even the nearest ERM-family perturbation, `Rdx`, contributed only its own transcript to the count. The Hippo/TEAD and Rac/Tiam1/Baiap2/Arhgap32 surfaces were also flat. That makes the broad `Ctnnb1`/`Tcf7l2` Wnt terminal-state programs and the `Tsc2` mTOR program upper biological references rather than direct scale donors for Nf2.

I therefore placed Nf2 at the high end of the self-or-near-null group, above a hard zero because its focal expression and protein turnover make functional editing plausible, but below the small Braf/Map2k1/Lrp6/Gsk3b responses because the best-matched merlin-side pathways did not propagate into recurrent 151 RNA changes.

Point prediction: `1`.
