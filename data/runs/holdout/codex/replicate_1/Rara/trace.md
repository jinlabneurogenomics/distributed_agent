# Direct DEG-count forecast for Rara

## Target and endpoint

- Target: `Rara`.
- Cell class: `151 TH Prkcd Grin2c Glut`, i.e. thalamic glutamatergic neurons.
- Endpoint: number of measured genes in this class with BH-adjusted Wilcoxon `pvals_adj < 0.05`.

## Evidence used

- The declared biology bundle for `Rara` reported exact in-assay non-target expression in the focal class: mean expression 0.0887 cp10k, 0.0647 mean log1p(cp10k), 3,451 total target UMIs across 23,679 non-target nuclei, and 2,949 expressing nuclei, or 12.45% of the focal class. This is real but low target reach, and because the class is aggregated across thalamic neuronal populations it makes any cell-autonomous response easy to dilute.
- The same bundle supported a plausible functional perturbation if an edit lands in a `Rara`-dependent neuron: RARalpha is a dynamically renewed receptor protein with nuclear RXR/RAR transcriptional and dendritic translational-control pools, and the 21-28 day edit-to-harvest interval is long relative to measured RARalpha turnover. This argued against treating the perturbation as an editing/stock null.
- The visible `151 TH Prkcd Grin2c Glut` training count table is extremely zero-heavy: 1,205 of 1,674 visible targets had `n_degs = 0`, the median was 0, the 75th percentile was 1, and the 90th percentile was 2.
- The closest same-cell-class training analogs from the RAR/RXR/retinoid lane were all silent: `Rarb = 0`, `Rarg = 0`, `Rxra = 0`, `Rxrb = 0`, `Rxrg = 0`, and `Stra6 = 0`.
- A profile comparison over 20 visible retinoid and nuclear-receptor perturbations in the declared Parquet showed the same split: 13/20 had no significant features, 4/20 had only 1-9, and 3/20 had at least 50. The broad responders were `Rora`, `Nr1d1`, and `Esrra`, not RAR/RXR-family perturbations.

## Forecast rationale

`Rara` should be biologically engaged within the experimental window, so a nonzero signature is possible. The decisive downward evidence is that the exact focal expression is sparse and low, the direct retinoic-acid receptor family and RXR partners were all zero in the same training endpoint, and most visible ligand-responsive nuclear receptors were also at 0 or a few DEGs. The active nuclear-receptor cases in this thalamic class appear to be target-specific programs rather than evidence for a generic nuclear-receptor-scale DEG burden.

I therefore placed `Rara` at the floor of the visible count distribution and predict no BH-significant DEGs in `151 TH Prkcd Grin2c Glut`.

Predicted `n_degs`: 0
