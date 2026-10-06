# Nr4a2 direct n_degs forecast

## Target and endpoint

- Target: `Nr4a2`.
- Cell group: `151 TH Prkcd Grin2c Glut`.
- Endpoint: number of measured genes in that cell group with BH-adjusted Wilcoxon `pvals_adj < 0.05`.
- Outcome blindness: the held-out `Nr4a2` DE rows and held-out `n_degs` were absent from the declared count table and training Parquet. I used the declared `Nr4a2` biology bundle, the training count table, and selected training rows from the expression Parquet, but not a same-experiment `Nr4a2` profile or count.

## Evidence used

### Canonical Nr4a2 biology

The outcome-excluded `Nr4a2` bundle supports functional realization but only narrow reach in the requested population.

- NR4A2 is a nuclear DNA-binding transcriptional regulator.
- A successful disruptive edit is expected to deplete functional nuclear NR4A2 before the P37-P44 harvest: the bundle adjudicates the functional stock as `likely_substantially_depleted`, based on short receptor turnover and direct mature-neuron loss within one week in a conditional mouse model.
- Postnatal neuronal loss can matter quickly, but the strongest source evidence is in midbrain dopamine neurons and developmental habenula, not the broad thalamic `151 TH Prkcd Grin2c Glut` population.
- The exact non-target expression reach in the focal population is low: 1,584 of 23,679 non-target nuclei express `Nr4a2`, or 6.689%, with mean raw UMI 0.089 and pseudobulk 5.61 CPM. This supersedes the qualitative regional-thalamus expression prior for the requested cell group.

### Training count table

The focal training endpoint is zero-inflated:

- 1,674 training targets are present.
- 1,205/1,674 are zero.
- Distribution of `n_degs`: median 0, 75th percentile 1, 90th percentile 2, 95th percentile 18, mean 14.05.

The closest measured nuclear-receptor family members are silent in this cell group:

- `Nr4a1`: 0 DEGs.
- `Nr4a3`: 0 DEGs.

Broader nuclear-receptor and transcription-factor strata are also mostly silent:

- Reactome nuclear receptor transcription pathway: 41 training targets, 34 zeros, median 0, 90th percentile 3.
- WikiPathways nuclear receptors: 33 training targets, 27 zeros, median 0, 90th percentile 2.8.
- Functional-class transcription factors: 344 training targets, 284 zeros, median 0, 90th percentile 2.

There are real nonzero nuclear-receptor examples, especially `Rora` with 278, `Nr1d1` with 116, and `Esrra` with 57 DEGs. I treated these as upper-context examples rather than direct scale donors because the bundle makes `Nr4a2` a restricted thalamic target in this class, not a broadly expressed ROR/REV-ERB/ESRR-like regulator.

### Training Parquet spot checks

The zero counts for the NR4A paralogs reflect observed DE contrasts, not missing data:

- `Nr4a1`: 17,259 measured genes in `151 TH Prkcd Grin2c Glut`, 200 matched perturbed nuclei, 23,679 matched controls, 0 genes at FDR 0.05.
- `Nr4a3`: 17,259 measured genes, 218 matched perturbed nuclei, 23,679 matched controls, 0 genes at FDR 0.05.

The nonzero receptors show clear low-q tails in the same Parquet slice, confirming that the focal group and the Parquet rows are capable of detecting receptor effects when they are broad enough:

- `Nr1d1`: 116 genes at FDR 0.05.
- `Esrra`: 57 genes at FDR 0.05.
- `Rora`: 278 genes at FDR 0.05.

## Synthesis

I put high weight on the exact low expression reach and on the two zero NR4A paralog training outcomes. The biology card argues that edited, `Nr4a2`-expressing neurons should lose NR4A2 function within the assay window, so I did not treat this as a stock-persistence null. The limiting factor is instead dilution and specificity: only a small minority of the broad thalamic class expresses detectable `Nr4a2`, and the best functional evidence points to dopamine/habenular programs rather than the aggregate `151 TH Prkcd Grin2c Glut` population.

Given the training table's heavy mass at zero, the mostly silent nuclear-receptor stratum, and the silence of `Nr4a1`/`Nr4a3`, the most likely BH-significant footprint for held-out `Nr4a2` is no detected genes rather than a small but nonzero tail. My point prediction is therefore:

`predicted_n_degs = 0`
