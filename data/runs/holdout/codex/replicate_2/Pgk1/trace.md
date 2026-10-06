# Pgk1 direct n_degs forecast

## Target and endpoint

- Target: `Pgk1`.
- Focal class: `151 TH Prkcd Grin2c Glut`.
- Endpoint: number of measured genes with BH-adjusted Wilcoxon `pvals_adj < 0.05` in the focal class.
- The declared focal-class training count table has 1,674 perturbations and excludes `Pgk1`; the declared all-cell expression parquet also has no `gene_target = 'Pgk1'` rows.

## Evidence used

### Target biology

The canonical biology bundle reports strong focal reach for `Pgk1` in matched non-target nuclei:

- `77.499%` of 23,679 non-target focal-class nuclei expressed `Pgk1`.
- Mean raw expression was `1.916` UMI and pseudobulk abundance was `120.067` CPM.

The same bundle characterizes PGK1 as a soluble cytosolic glycolytic enzyme that catalyzes the ATP-generating 1,3-bisphosphoglycerate to 3-phosphoglycerate step. Functional stock should plausibly clear within the P16-to-P37/P44 window because mouse PGK1 peptide half-lives in a non-neural assay were about 2.8-5.2 days, and `Pgk2` is testis-restricted rather than an established brain substitute. This supports real target engagement in recovered neurons, but it does not establish a large nuclear RNA response: the harvest is survivor-conditioned, neuronal Pgk1-loss latency is not directly known, and the assay does not measure glycolytic flux, ATP, metabolites, or dropout of strongly affected nuclei.

### Training count distribution

The focal count table is very zero-inflated:

- `1205/1674` training perturbations had `n_degs = 0`.
- `276/1674` had `n_degs = 1`.
- `1481/1674` therefore had either 0 or 1 DEG.
- The median was `0`, the 90th percentile was `2`, and the mean was inflated to `14.05` by a long tail headed by chromatin, RNA-processing, proteasome, and trafficking perturbations.

### Pgk1 analogs in the training table

A typed mouse analog nomination against the 1,674-gene training universe found `Pgk1` absent from the training universe and absent from the selected corpus ledger. The leading specific, narrow-module training comparators were central glycolysis and glycolysis/gluconeogenesis genes:

| comparator | focal `n_degs` | interpretation |
| --- | ---: | --- |
| `Tpi1` | 1 | significant row was only `Tpi1` itself |
| `Pfkm` | 1 | significant row was only `Pfkm` itself |
| `Hk1` | 1 | significant row was only `Hk1` itself |
| `Gpi1` | 1 | significant row was only `Gpi1` itself |
| `Eno1` | 0 | no focal significant genes |
| `Slc2a1` | 0 | no focal significant genes |

Adjacent narrow or hand-selected carbon/mitochondrial comparators were also mostly flat:

- `Pdha1`, `Dlat`, `Mdh2`, `Got1`, `Got2`, and `Ndufs2` each had 1 DEG, their own transcript where queried.
- `Dld`, `Mpc1`, `Aco2`, `Ogdh`, `Ndufv1`, and `Cox4i1` had 0.
- `Mdh1` was the clear local outlier at 29 DEGs.
- Across 29 screened `Nduf*`/`Cox*` respiratory-chain entries, the median focal count was 0 and the total was 12.

### Same-experiment corpus context for training analogs

The selected same-experiment corpus for `Tpi1`, a training perturbation, records a moderate-confidence cross-perturbation contrast in which represented glycolytic comparators `Hk1`, `Gpi1`, `Pfkm`, and `Eno1` were also mostly transcriptionally flat, while the HBP/O-GlcNAc branch and proteasome perturbation gave much broader responses in the same screen. A synthesized moderate-confidence claim over `Hk1`, `Pfkm`, and `Tpi1` states that single perturbations of represented central glycolysis genes are transcriptionally buffered in postmitotic neurons.

### Profile check in the expression parquet

A symmetric focal-class profile comparison over 19 observed metabolic genes found 9 nodes with no significant focal features, 9 with 1-9 significant features, and only `Mdh1` in the 10-49 bin. Inspection of `Tpi1`, `Pfkm`, `Hk1`, `Gpi1`, and `Eno1` against adjacent pyruvate/TCA/respiratory peers showed no shared BH-significant downstream feature among the central-glycolysis self-only or null signatures.

## Synthesis

Upward pressure comes from the Pgk1 bundle: Pgk1 is expressed in most focal control nuclei, PGK1 protein should plausibly be renewed within 21-28 days, and no neural Pgk2 redundancy is established.

Downward pressure is stronger for this specific endpoint. The nearest measured glycolysis perturbations in the same P16 CRISPR, P37/P44 survivor-conditioned neuronal RNA assay did not enter a broad glycolytic, ISR, or proteostasis program. Their focal `n_degs` values were 0 or 1, and the 1s were self-transcript calls rather than downstream transcriptional cascades. Adjacent mitochondrial and respiratory-chain donors were likewise near-null. The corpus interpretation of these training data explicitly separates buffered central glycolysis from large HBP/Ogt or proteasome responses, so a high-count forecast for Pgk1 would require assuming that PGK1 is a sharp exception among otherwise flat single glycolytic-enzyme perturbations.

I therefore predict a near-null focal response. Because Pgk1 is well expressed in the focal population and the four most local central-glycolysis donors with detectable focal calls each contributed exactly one self-transcript DEG, the point estimate is one rather than zero.

`predicted_n_degs = 1`
