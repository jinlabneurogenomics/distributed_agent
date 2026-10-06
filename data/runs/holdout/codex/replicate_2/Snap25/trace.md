# Snap25 direct n_degs forecast

Target and endpoint: `Snap25` in `151 TH Prkcd Grin2c Glut`; `n_degs` is the count of measured genes with BH-adjusted Wilcoxon `pvals_adj < 0.05` in that target x class contrast.

## Blind inputs used

- The one-row holdout manifest names `Snap25`, and the training count table for `151 TH Prkcd Grin2c Glut` does not contain `Snap25`.
- A direct Parquet check found 0 rows with `gene_target = 'Snap25'`; the held-out target signature was therefore not queried or reconstructed.
- The selected same-experiment corpus has no `Snap25` Findings or Claims in this release, so same-target outcome text was not available.
- The Snap25 biology bundle reports strong exact baseline reach in the focal population: 23,673 / 23,679 non-target cells expressing `Snap25`, `mean_raw_umi = 35.03`, `mean_log1p_cp10k = 3.064`, `sd_log1p_cp10k = 0.329`, and 2,195 pseudobulk cpm.

## Snap25 biology

The biology-only characterization identifies SNAP-25 as a presynaptic Q-SNARE that supplies two helices to the syntaxin/synaptobrevin fusion complex. Loss of the protein should cripple fast calcium-triggered evoked synaptic vesicle release. The bundle also adjudicates the functional protein stock as `likely_substantially_depleted` by the P37-P44 harvest after P16 editing: pre-existing SNAP-25 is not directly destroyed by the edit, but published neuronal turnover and the 21-28 day interval imply many replacement cycles before harvest.

That made complete biological non-engagement unlikely in thalamic neurons. At the same time, the operation is fast vesicle fusion at terminals, and the readout is survivor-conditioned nuclear RNA. A strong electrophysiological lesion therefore does not require a broad steady-state somatic DEG program.

## Training measurements that anchored scale

The declared count table is extremely sparse in this focal class: among 1,674 training targets, 1,205 have `n_degs = 0`, 276 have `n_degs = 1`, and only 193 have more than one DEG.

I used represented presynaptic vesicle/SNARE-cycle perturbations as the closest measured biological comparators:

| target | 151 TH n_degs |
| --- | ---: |
| Cplx1 | 1 |
| Cplx2 | 0 |
| Stx1b | 0 |
| Stxbp1 | 1 |
| Vamp1 | 1 |
| Syt2 | 0 |
| Unc13a | 0 |
| Unc13b | 0 |
| Unc13c | 0 |
| Nsf | 0 |
| Napb | 0 |
| Syn1 | 1 |
| Syn2 | 0 |
| Syp | 1 |
| Sv2a | 1 |

The cohort mean was 0.4 DEGs, and no member of this core release cohort exceeded one DEG in the exact held-out cell class.

A targeted Parquet read showed that the one-gene calls in this presynaptic cohort were target-transcript events rather than a common downstream program:

| target | significant 151 feature |
| --- | --- |
| Cplx1 | Cplx1 |
| Stxbp1 | Stxbp1 |
| Vamp1 | Vamp1 |
| Syn1 | Syn1 |
| Syp | Syp |
| Sv2a | Sv2a |

`Stx1b`, `Cplx2`, `Syt2`, `Unc13a`, `Unc13b`, `Unc13c`, `Nsf`, `Napb`, and `Syn2` had no BH 0.05 feature in the focal class. Broader channel/excitability comparators were also at the self-hit floor in this class: `Cacnb4`, `Scn1a`, `Scn2a`, and `Kcnq2` each had only the perturbed transcript significant.

Packaged same-experiment Findings were concordant with the exact Parquet rows:

- `Stx1b` had a pan-measured neuronal transcriptomic null at FDR < 0.10, and its ranked profile had no meaningful presynaptic-pathway neighbor.
- `Cplx1`, `Cplx2`, `Unc13a`, and `Vamp1` reports all described sparse, buffered, or non-convergent vesicle-release signatures rather than a reproducible release-machinery DEG module.
- `Stxbp1` was explicitly called out as the exception: it generated a broader nuclear RNA response elsewhere, but canonical release-machinery perturbations such as `Stx1b`, `Vamp1`, `Cplx1`, `Cplx2`, `Unc13a/b/c`, and `Syt2` largely failed to phenocopy it despite acting in the same vesicle-fusion pathway.

Finally, I ran a matched `151 TH Prkcd Grin2c Glut` profile comparison over the 15 presynaptic comparators above. Across all 105 pairwise comparisons, the mean overlap among the top signed tails was only 0.0266 for positive features and 0.0277 for negative features. No leading feature from any comparator was present in the top tail of all other presynaptic peers, and the cohort had zero positive significant-program overlaps. That argues against assigning Snap25 a multi-gene downstream module merely because it is a core SNARE target.

## Point prediction

The best decomposition for Snap25 in this focal class is:

- downstream thalamic nuclear-RNA response: expected 0 genes, because the matched core exocytosis perturbations are null or self-only in this endpoint;
- Snap25 self-transcript: expected 1 gene, because Snap25 is nearly universally and highly expressed in the exact class, so even a modest allele/NMD-associated mRNA drop should be powered at BH 0.05.

The main downward risk is an edit that disrupts SNAP-25 protein without reducing nuclear `Snap25` mRNA enough to beat the whole-transcriptome BH correction, as happened for some other release genes. The main upward risk is Snap25-specific axonal pathology or survivor stress that is stronger than `Stx1b`/`Cplx1` and absent from the measured comparators. The presynaptic training data made the broad-response alternative less likely than the self-only alternative.

Predicted `n_degs`: **1**
