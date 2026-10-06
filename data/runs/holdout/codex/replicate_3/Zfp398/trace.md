# Direct forecast for Zfp398

## Target and admissible context

- Holdout target: `Zfp398`.
- Requested endpoint: `n_degs`, the number of genes in `151 TH Prkcd Grin2c Glut` with BH-adjusted Wilcoxon `p < 0.05`.
- The target was present in the one-row manifest and in the prediction-safe biology bundle, and absent from the 1,674-row training count table. I did not use a `Zfp398` Perturb-seq signature or target DEG count.
- The biology bundle reports exact focal-population reach for the target transcript: `Zfp398` was detectable in 17,892 of 23,679 non-target nuclei in the focal class, mean raw UMI 1.61, mean CP10K 1.03, pseudobulk CPM 100.89.
- Biologically, `Zfp398` is a KRAB/C2H2 nuclear DNA-binding transcription regulator. The card adjudicates its operative stock as a dynamic complex component and concludes low-confidence, partial `likely_substantially_depleted` stock by the P37-P44 harvest after P16 editing. The same bundle found no transferable postnatal thalamic-neuron loss phenotype, no target-specific turnover clock, and no close paralog with proven same-context compensation.

The expression and stock evidence make the perturbation plausible in this cell class, but they do not specify a downstream RNA program. I therefore treated them as evidence against a pure reach failure, not as evidence for a large response.

## Training measurements used

The declared `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` table contains 1,674 training perturbations for the exact focal class.

- 1,205/1,674 training targets were exact zeros.
- 1,481/1,674 had at most 1 DEG.
- The empirical median was 0, the 75th percentile was 1, the 90th percentile was 2, and the 95th percentile was 18.
- The mean was 14.05 only because of a small long tail; the maximum was 2,677.

Within represented `Zfp*` training perturbations, the matched counts were even more concentrated near zero:

- 25/30 had 0 DEGs.
- 27/30 had at most 1 DEG.
- The nonzero `Zfp*` counts were `Zfp148` 8, `Zfp236` 19, `Zfp423` 150, `Zfp612` 1, and `Zfp692` 1.
- The closest alphabetic measured neighbor I could inspect, `Zfp397`, had 0 DEGs at this FDR<0.05 endpoint.

Related local transcription-factor and partner checks were also mostly quiet in this class: `Ep300` 0, `Smad3` 0, all represented `Smad*` genes except `Smad2` at 1 were 0, and most `Klf*` and `Zbtb*` perturbations were 0 or 1. `Zbtb7a` was a major exception at 841 DEGs, but its count table behavior was not typical of this regulator cohort.

I queried the declared Parquet only for the focal class and the selected training regulators to verify that the count table rows reflected full focal-class profiles. Each selected node had 17,259 measured genes. The FDR<0.05 counts from the Parquet matched the table: `Zbtb7a` 841, `Zfp423` 150, `Klf9` 19, `Zfp236` 19, `Zfp148` 8, `Zfp612` 1, `Zfp692` 1, `Ep300` 0, `Smad3` 0, and `Zfp397` 0.

## Profile and corpus interpretation

I compared a 61-node matched cohort of observed zinc-finger, KLF, SMAD, ZBTB, and related transcriptional regulators using their `151 TH Prkcd Grin2c Glut` log-fold-change profiles. This same-Parquet profile comparison found:

- 45/61 cohort members with no FDR<0.05 features.
- 7/61 with 1-9 features.
- 2/61 with 10-49 features.
- 7/61 with at least 50 features.

The nonzero `Zfp` perturbations were not a coherent scale-bearing module for `Zfp398`. `Zfp423` shared only 1 positive and 1 negative significant feature with `Zfp236`, shared no significant features with `Zfp148`, and had no significant-feature intersection with one-gene `Zfp612` or `Zfp692`. `Zfp236` and `Zfp148` also shared no significant features. The inspected pairwise cosine/spearman values looked like weak whole-profile background similarity rather than a recurrent C2H2/KRAB signature.

The same-experiment corpus, which is an interpretation of the same Parquet rather than independent replication, supported the same boundary:

- `Zfp397` was transcriptionally silent across 22/23 measured neuronal groups and lacked a robust neighbor.
- A synthesized SCAN/C2H2/KRAB-associated claim states that the represented family members did not define an interchangeable shared neuronal transcriptomic regulon in the screen.
- `Zfp423`'s strong 151 signal was a target-specific thalamic subtype, neurotransmission, cell-surface, and ER/glycoprotein-processing response.
- `Zbtb7a`'s strong signal was a broad membrane-trafficking, lysosomal, neurosecretory, and synaptic-remodeling response.
- `Zfp236`'s smaller signal centered on Ogt/Eif4a2/Cpt1c and did not provide a general zinc-finger program.
- `Ep300` and `Smad3` were explicit same-assay transcriptional-regulator nulls, consistent with the idea that canonical developmental or non-neuronal transcription factors can be flat in postmitotic recovered neurons.

The corpus release often summarizes FDR<0.10 surfaces, so I used its Findings only qualitatively to interpret which training outliers carried target-specific programs; the requested numeric endpoint stayed the FDR<0.05 count from the declared training table.

## Forecast synthesis

Upward bearings:

- `Zfp398` is measurably expressed in the focal thalamic population.
- A disruptive P16 edit should cut off new supply of a dynamic nuclear regulator, and ordinary protein turnover over 21-28 days makes some functional depletion plausible.
- The biology bundle did not find a close same-context compensating paralog.

Downward bearings:

- The bundle found no direct mouse postnatal thalamic-neuron loss phenotype, no matched onset/stock kinetics, and no direct evidence for ongoing Zfp398 demand in this class.
- Most assayed zinc-finger transcription regulators in the exact focal count table were zero; 90% of represented `Zfp*` rows had at most one DEG.
- The large zinc-finger/ZBTB outliers mapped to specific programs that do not look transferable to an understudied KRAB/C2H2 regulator.
- `Zfp397`, the strongest measured flat family boundary, and the SCAN/C2H2/KRAB same-corpus claim argue against assigning a large response solely from zinc-finger identity.

Balancing those points, I expect target engagement but no detectable downstream program at FDR<0.05. The modal exact value in the local family and in the whole training set is 0; `Zfp398` has expression support but lacks the target-specific biology that separated `Zfp423`, `Zbtb7a`, or `Zfp236` from that mass of zeros.

Point prediction: `0`
