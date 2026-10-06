# Srsf1 n_degs forecast

## Target and endpoint

- Target manifest: `[local file: Srsf1.csv]`
- Target: `Srsf1`
- Focal population: `151 TH Prkcd Grin2c Glut`
- Endpoint: count of measured genes with Wilcoxon BH-adjusted `pvals_adj < 0.05`
- Point prediction: `180`

The Srsf1 target profile and Srsf1 count were not queried or used. The declared Parquet, count table, target biology bundle, and same-experiment corpus ledgers were treated as different representations or annotations of one Perturb-seq experiment, not as independent replications.

## Declared Srsf1 biology

Source: declared `Srsf1.json` biology bundle, also served by `characterization_bundle(target="Srsf1", view="biology")`.

- Exact focal-population expression is strong enough for editing to matter: in non-target nuclei from `151 TH Prkcd Grin2c Glut`, `Srsf1` is detected in 21,599 of 23,679 nuclei, or 91.215845%, with mean log1p CP10K 1.00193 and mean raw UMI 3.23886.
- The curated functional-stock call is `likely_substantially_depleted`: a P16 disruptive edit stops new SRSF1 synthesis, SRSF1 acts through renewable nuclear and cytoplasmic RNA-processing pools, and the P37-P44 harvest is 21-28 days after editing.
- The postnatal thalamic loss phenotype is not directly established. The closest in-vivo Srsf1 loss experiment is embryonic cortical shRNA, while the postnatal Srsf1 nuclear-retention allele preserves nuclear splicing and is not a NeuN-positive thalamic-neuron null.
- SRSF2 is a close related SR factor with overlapping binding in mouse fibroblasts, but full compensation after Srsf1 loss in thalamic neurons is untested.

Interpretation: Srsf1 is not a likely unreachable target in this focal population, but single SR-factor loss should be shrunk below multi-component spliceosome or SR-import failures because gene-level abundance, rather than alternative splicing, is the scored endpoint and related SR factors may buffer part of the response.

## Training measurements used

Primary count source: `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.

The focal count table contains 1,674 training targets; 1,205 are zero, 363 are 1-9, 63 are 10-99, 40 are 100-999, and only 3 are at least 1000 DEGs. Thus the RNA-processing comparators below all sit in the high-response tail except the deliberately included lower boundaries.

Biologically selected RNA-processing donors in `151 TH Prkcd Grin2c Glut`:

| training target | n_degs |
|---|---:|
| Rnpc3 | 868 |
| U2af2 | 828 |
| Hnrnpu | 733 |
| Cdc40 | 624 |
| Tnpo3 | 618 |
| Prpf6 | 454 |
| Snrnp70 | 213 |
| Hnrnpc | 122 |
| Hnrnpa2b1 | 11 |
| Ddx39b | 0 |

Exact Parquet checks for the same nodes in `151 TH Prkcd Grin2c Glut` recovered 17,259 measured genes per node and reproduced the same BH<0.05 counts: `Tnpo3` 618, `U2af2` 828, `Rnpc3` 868, `Prpf6` 454, `Cdc40` 624, `Hnrnpu` 733, `Hnrnpc` 122, `Snrnp70` 213, `Hnrnpa2b1` 11, and `Ddx39b` 0.

## Same-experiment profile context

Profile comparison artifacts:

- `workbench/rna_processing_profile_compare.json`
- `workbench/rna_processing_profile_inspect_core.json`
- `workbench/rna_processing_profile_cohort.json`

Those artifacts compared only the ten observed training nodes listed above, using `logfoldchanges` over the declared training Parquet filtered to `151 TH Prkcd Grin2c Glut`.

The profile comparison supported three scale anchors:

- The high core/RNA-trafficking anchors are not isolated outliers. `Tnpo3`, `U2af2`, `Rnpc3`, `Prpf6`, and `Cdc40` all have at least 454 focal BH<0.05 genes and positive pairwise whole-profile cosine similarity to the hnRNP/spliceosome peers.
- `Tnpo3` is mechanistically the closest training donor because it imports RS-domain splicing cargos and its canonical response down-regulates SR-splicing/RNA-processing transcripts including `Srsf1`, `Srsf2`, `Srsf5`, `Srsf7`, `Srrm2`, `Akap8l`, `Clk1`, and `Cstf2` in the same-experiment Finding `Tnpo3:F002`. It is still an upper-side donor because losing the transporter perturbs multiple SR proteins rather than only SRSF1.
- Single RBP/export boundaries were much lower in this exact focal group: `Hnrnpc` had 122 DEGs, `Hnrnpa2b1` had 11, and `Ddx39b` had 0. This argued against copying the 454-868 counts of core spliceosome factors directly onto Srsf1.

Packaged Findings from the same release gave the same boundaries: `Prpf6`, `Rnpc3`, `Snrnp70`, `Tnpo3`, and `U2af2` are a selective RNA-splicing/RNA-processing module in thalamic/midbrain responders, but this response is not generic to every RNA-processing, Sm-related, or transport perturbation. In particular, `Tnpo3:F004` supports convergence with spliceosome/RNA-processing targets rather than broad nuclear-transport perturbations, and `U2af2:F006` notes that several matched RNA-processing comparators were flat or weak.

## Synthesis

I treated `Tnpo3` at 618 as the best mechanistic high-side donor but discounted it because a Tnpo3 edit disrupts SR-protein import as a class. I treated the core spliceosome donors `U2af2`, `Rnpc3`, `Prpf6`, and `Cdc40` as evidence that perturbing repeatedly used RNA-processing machinery can produce hundreds of DEGs in this focal population, but they are broader than loss of one sequence-specific SR factor. `Snrnp70` at 213 and `Hnrnpc` at 122 were the closest scale anchors for a single RNA-binding/splicing factor that is active but not a whole-spliceosome choke point.

The final integer, 180, is therefore just below `Snrnp70` and well below the Tnpo3/core-spliceosome range, while remaining above `Hnrnpc` because Srsf1 is highly expressed in the focal thalamic nuclei, is expected to lose functional stock by harvest, and is directly tied to the SR-processing module perturbed by Tnpo3.
