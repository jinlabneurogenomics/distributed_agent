# Col25a1 direct n_degs forecast

## Target and endpoint

- Target: `Col25a1`.
- Cell class: `151 TH Prkcd Grin2c Glut`.
- Endpoint: the integer count of measured genes with BH-adjusted Wilcoxon `pvals_adj < 0.05` in the focal class.
- Declared target biology came from the prediction-safe `Col25a1` biology bundle; the bundle exposed no target outcome or labeled-neighbor outcomes.

## Biology used

The exact focal-population expression record reports that `Col25a1` is detectable in this class: 12,027 of 23,679 matched non-target nuclei expressed the feature, `pct_cells_expressing = 50.7918`, `mean_log1p_cp10k = 0.43945`, and `pseudobulk_cpm = 84.417`. This makes an RNA consequence in the 151 thalamic class observable in principle.

The functional-stock card lowers the expected response amplitude. COL25A1 has a membrane precursor and a furin-released extracellular ectodomain, so a P16 edit should block new supply but should not synchronously remove pre-existing shed extracellular protein. The card adjudicates the P37-P44 functional stock as `partially_depleted_or_leading_edge`, with target-specific membrane and extracellular half-lives unresolved. Its direct expression evidence is P25 thalamic-neuron expression, but it discounts the global developmental motor-neuron knockout phenotype because that timing and cell type do not anchor an acute postnatal thalamic-neuron loss experiment.

## Training measurements used

The declared 151-class count table contains 1,674 training perturbations. Its distribution is highly zero-inflated:

- median `n_degs`: 0
- 1,205 / 1,674 perturbations: 0 DEGs
- 75th percentile: 1
- 90th percentile: 2
- 95th percentile: 18
- maximum: 2,677

I then chose the visible training perturbations closest to the biology of a neuronal extracellular collagen or adhesion molecule: `Col11a1`, `Col2a1`, nine integrin genes, `Adam10`, `Adamts17`, `Adam22`, `Pcdh19`, `Cntnap1`, `Cntnap2`, `Dscam`, `Lrrtm1`, `Lrrtm3`, `Lrrtm4`, `Nrxn1`, `Nrxn2`, `Nrxn3`, `Nlgn3`, `Ncam1`, `Dag1`, and `Reln`. In the declared count table for the exact requested cell class, that 28-target cohort had 21 zeros, 7 ones, and no value above 1; its mean was 0.25 and median was 0.

The focal Parquet confirmed that the 1-DEG analogs were still almost entirely self-transcript calls, not broad downstream programs. At `pvals_adj < 0.05` in `151 TH Prkcd Grin2c Glut`, `Adam22`, `Cntnap1`, `Cntnap2`, `Ncam1`, `Nlgn3`, and `Nrxn1` called only the corresponding target transcript; `Lrrtm1` called one non-self feature, `R3hdm2`. `Col11a1`, `Col2a1`, `Adam10`, `Itgb1`, `Dag1`, `Reln`, `Nrxn2`, `Nrxn3`, and the other queried integrin/adhesion perturbations had zero significant rows in this class.

I also compared the same 28 nodes over their full signed 151-class Wilcoxon-score profiles. All 28 profiles were present; 21/28 had no significant feature and 7/28 landed in the `1_to_9_significant_features` activity bin. The whole selected cohort had very little directional recurrence: mean top-tail overlap coefficient was 0.01296 for positive tails and 0.01392 for negative tails, and the material collagen/adhesion pairs had no shared significant positive or negative features. As concrete checks, the `Col11a1` versus `Col2a1` Pearson correlation was 0.0326, and `Col11a1` against the inspected one-hit adhesion nodes ranged from about -0.0069 to 0.0325 by Pearson.

The same-experiment Finding ledger for safe training comparators gave the same qualitative boundary rather than independent validation: `Col11a1` was interpreted as having no downstream FDR<0.10 neuronal response in any measured group, `Col2a1` as near-flat across postnatal NeuN-enriched neurons, and `Cadm2`/`Cntnap1`/`Nrxn1` reports repeatedly described synaptic or axonal adhesion perturbations as buffered, isolated, or non-convergent in this snRNA-seq readout.

## Synthesis

`Col25a1` has better focal expression support than the two collagen training perturbations, so a self-transcript-sized call is plausible. The evidence does not support moving into the long right tail: COL25A1 loss by harvest is partial/uncertain because of the shed extracellular pool, no direct postnatal thalamic loss phenotype is known, and the nearest visible training perturbations in collagen/ECM, integrin, and neuronal adhesion biology are 0-1 DEG events with no hidden shared score-profile program.

I therefore treated the target as below the already-small class median for biologically generic targets and near the 0/1 analog boundary. Because the strongest same-biology evidence is the zero-valued collagen pair plus the 21/28 zero-valued broader ECM/adhesion cohort, I used the modal analog outcome as the integer point forecast:

`predicted_n_degs = 0`
