# Cntn1 DEG-count prediction

## Question and resolved ambiguities

The requested held-out target was exactly:

| target_name |
|---|
| Cntn1 |

I interpreted `predicted_n_degs` as the assay endpoint in `151 TH Prkcd Grin2c Glut`: the number of measured genes with `pvals_adj < 0.05` in the hidden `Cntn1` perturbation signature.  The target itself is part of the count when its own mRNA is significantly decreased; this is true of the training table, where the one-gene signatures for `Cntnap1`, `Cntnap2`, `L1cam`, and `Chl1` in this focal class are all self-transcript losses.

## Sources used

Internal data and same-experiment evidence:

- `[local file: training_de_all_cell_groups.parquet]`
- `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`
- `[local file: 043_Cntn1.csv]`
- Distributed Agents same-experiment corpus release `perturbai-july-260713-sourceguard-1773-v1`, especially the Cntnap1, Cntnap2, L1cam, Nrcam, and Chl1 finding cards.
- Distributed Agents runtime profile comparison over the focal-cell score vectors for `Cntnap1`, `Cntnap2`, `L1cam`, `Chl1`, `Nrcam`, and `Ank2`.

External biology:

- NCBI PubMed searches for Contactin-1/F3, Caspr/Cntnap1, Neurofascin/NF155, and paranodal junctions.
- Rios et al. 2000, DOI `10.1523/JNEUROSCI.20-22-08354.2000`, PMID `11069942`: Contactin colocalizes with Caspr and forms a cis complex targeted to paranodal junctions.
- Charles et al. 2002, DOI `10.1016/S0960-9822(01)00680-7`, PMID `11839274`: glial NF155/Neurofascin binds the axonal paranodin/Caspr-Contactin complex.
- Falk et al. 2002, DOI `10.1016/S0248-4900(02)00006-0`, PMID `12500940`: Contactin/F3 is a GPI-anchored Ig-family neuronal adhesion molecule with roles in axogenesis, axon-glia contact, paranodes, and nodes of Ranvier.
- Gollan et al. 2003, DOI `10.1083/jcb.200309147`, PMID `14676309`: Caspr regulates Contactin processing and the glycoform presented at the cell surface.
- Pillai et al. 2007, DOI `10.1002/jnr.21374`, PMID `17549747`: Caspr mutants reinforce the essential axoglial-junction role of the Caspr/Contactin complex while noting that some Contactin functions can be independent of Caspr.

## Computational calibration

I filtered the DE parquet to `group_name = '151 TH Prkcd Grin2c Glut'` and used the training counts to calibrate the endpoint scale.

The focal cell group contains 28,891,566 DE rows: 1,674 non-held-out perturbations by 17,259 measured genes.  The endpoint was very sparse:

| quantity | value |
|---|---:|
| training perturbations | 1,674 |
| perturbations with `n_degs > 0` | 469 |
| median `n_degs` | 0 |
| 75th percentile | 1 |
| 90th percentile | 2 |
| 95th percentile | 18 |
| max | 2,677 |

I then pulled all focal-cell FDR rows for the closest adhesion and axonal-domain analogs.  Exact focal endpoint counts for the relevant training perturbations were:

| target | focal `n_degs` | focal FDR<0.05 genes |
|---|---:|---|
| Cntnap1 | 1 | `Cntnap1` down |
| Cntnap2 | 1 | `Cntnap2` down |
| L1cam | 1 | `L1cam` down |
| Chl1 | 1 | `Chl1` down |
| Nrcam | 2 | `Nrcam` down; `Letm2` up |
| Ncam1 | 1 | singleton |
| Kcna1 | 0 | none |
| Kcna2 | 0 | none |
| Kcnab2 | 1 | singleton |
| Ank1 | 0 | none |
| Ank2 | 0 | none |
| Nrp1 | 0 | none |
| Nrp2 | 0 | none |
| Dscam | 0 | none |
| Nrxn1 | 1 | singleton |
| Nrxn2 | 0 | none |
| Nrxn3 | 0 | none |

For the direct focal-cell analogs, the exact significant rows were:

| perturbation | gene | log2FC | FDR |
|---|---|---:|---:|
| Cntnap1 | Cntnap1 | -0.822 | 1.09e-11 |
| Cntnap2 | Cntnap2 | -1.087 | 7.90e-06 |
| L1cam | L1cam | -0.749 | 1.44e-24 |
| Chl1 | Chl1 | -0.958 | 2.71e-02 |
| Nrcam | Nrcam | -0.650 | 2.94e-15 |
| Nrcam | Letm2 | +0.459 | 4.90e-02 |

This argues that the right local scale for an Ig-superfamily axon-adhesion perturbation in the focal thalamic class is 0-2 genes, often exactly the target mRNA.

I also compared the full focal-cell Wilcoxon-score profiles for `Cntnap1`, `Cntnap2`, `L1cam`, `Chl1`, `Nrcam`, and `Ank2`.  All six profiles had 0-2 significant genes.  Among the most relevant five, whole-profile Pearson/cosine similarities were tiny; for example `Cntnap1` versus `Nrcam` was the largest Pearson neighborhood edge at only `r = 0.022`, `Cntnap1` versus `Cntnap2` was `r = 0.005`, and `Cntnap2` versus `Nrcam` was `r = -0.007`.  The positive and negative top-tail overlaps were similarly near background.  I therefore treated those genes as response-breadth analogs but did not pool their individual nominal features into a predicted downstream Cntn1 program.

## Target-specific reasoning

### Cntn1

**Mechanistic match to training perturbations.**  `Cntn1` encodes Contactin-1/F3, a neuronal GPI-anchored Ig-family cell-adhesion protein.  Its closest represented training neighbor is `Cntnap1`: Contactin-1 and Caspr1/Cntnap1 form the axonal cis complex that localizes to paranodal junctions during myelination (Rios et al. 2000), and glial NF155/Neurofascin binds this axonal Caspr-Contactin complex at the axoglial junction (Charles et al. 2002).  This makes `Cntnap1` a stronger mechanistic analog than generic Contactin-family frequency would be.

The focal `Cntnap1` perturbation had only one DEG, its own transcript.  The same pattern held for several other membrane adhesion or axon-domain genes in the same exact focal readout: `Cntnap2`, `L1cam`, and `Chl1` each had one DEG, again the target transcript; `Nrcam` had the target plus a marginal `Letm2` increase; `Ncam1`, `Nrxn1`, and `Kcnab2` were singleton responses; and `Kcna1`, `Kcna2`, `Ank1`, `Ank2`, `Nrp1`, `Nrp2`, `Nrxn2`, `Nrxn3`, and `Dscam` were zero.

**Same-experiment corpus evidence.**  The Distributed Agents corpus made the same distinction between strong structural priors and weak snRNA-seq consequences.  Its `Cntnap1:F001` finding summarized a pan-surface transcriptionally buffered phenotype with zero downstream genes at FDR<0.10 in every recovered group, and `Cntnap1:F002` reported that `Cntnap2`, `Kcna1`, `Kcna2`, `Kcnab2`, `Nrcam`, `Nrxn1`, and `Ank2` did not phenocopy `Cntnap1`.  The `Cntnap2:F003` finding likewise showed no transcriptional convergence among the CASPR/Kv1 neighborhood.  `L1cam:F003`, `Nrcam:F004`, `Nrcam:F006`, and `Chl1:F002` generalized that represented L1/NCAM/Ig-superfamily, neuropilin/semaphorin, ankyrin, and node/paranode comparators were flat, singleton-only, or mutually nonconvergent in the postnatal nuclear RNA assay.

**Zero/nonzero call.**  I predict a nonzero but singleton effect.  The external biology says Cntn1 loss should primarily perturb an axonal adhesion/paranodal protein complex, not a nuclear transcription factor, ribosome/spliceosome/proteasome process, or other class that created hundreds of DEGs in the training table.  The within-dataset evidence says the best represented analogs of this local membrane biology were buffered in exactly this endpoint.  I nevertheless keep the count at `1` rather than `0` because the directly comparable training genes frequently gave a significant self-decrease in `151 TH Prkcd Grin2c Glut`: `Cntnap1`, `Cntnap2`, `L1cam`, `Chl1`, and `Nrcam` all did.  `Cntn1` itself is among the measured genes in the focal parquet, so a self row is available to be counted.

The point prediction is therefore:

| target | predicted `n_degs` |
|---|---:|
| Cntn1 | 1 |

## Limits

- No `Cntn1` perturbation rows were present in the supplied DE parquet or the Distributed Agents same-experiment corpus, so all reasoning transfers from analogs.
- `Cntn1` is not identical to `Cntnap1`: Contactin-1 has L1-family and extracellular-matrix interactions and some Caspr-independent functions, so a perfect phenocopy is not guaranteed.
- `Cntn2`, `Nfasc`, oligodendrocyte NF155 perturbation, and combined paranodal loss were not directly represented as focal training perturbations.
- The experiment assayed NeuN+ neuronal nuclei 3-4 weeks after sparse postnatal AAV CRISPR.  It did not measure Contactin-1 protein, Caspr surface trafficking, paranodal ultrastructure, myelination, or conduction, and non-neuronal glial compartments were largely absent.
- The predicted singleton depends on target-RNA knockdown passing FDR.  Cntnap/L1/Nrcam/Chl1 make that plausible, but mRNA destabilization depends on guide placement, residual isoforms, and nuclear capture of a GPI-anchored axonal adhesion transcript.
