# Srrm2 n_degs forecast

## Requested endpoint

The held-out perturbation is `Srrm2` in `151 TH Prkcd Grin2c Glut`. The quantity to predict is the number of measured genes in that focal class with Wilcoxon BH-adjusted `p < 0.05`.

The expression signature and count for `Srrm2` were not used. I used the declared biology-only Srrm2 bundle, the `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` count table, the declared training parquet, and same-experiment corpus summaries for measured non-Srrm2 RNA-processing comparators.

## Target biology

The target bundle puts SRRM2 on a spliceosome/nuclear-speckle axis: cultured-cell data place SRRM2 in spliceosomes and show that its disordered regions cooperate with SON in nuclear-speckle organization, while SRRM2 loss changes cassette-exon inclusion. The functional-stock adjudication therefore treated SRRM2 as a dynamic complex component with ongoing renewal demand and concluded that an edit beginning at P16 should likely substantially deplete operative SRRM2 by P37-P44, although no matched neuronal SRRM2 protein half-life was available.

The exact focal-population reach argues against a pure expression blind spot: in non-target nuclei from `151 TH Prkcd Grin2c Glut`, `Srrm2` RNA was detected in 23,661 of 23,679 cells, with mean 8.09 CP10K and mean 12.47 raw UMI. That supports target presence but not editing efficiency or downstream magnitude.

Two features made me discount a very large core-spliceosome-sized forecast:

- SRRM2 biology is expected to affect splicing and nuclear organization first, whereas this endpoint is a 3-prime whole-gene abundance test; isoform changes can be invisible.
- Its strongest literature partner, `Son`, is a direct nuclear-speckle comparator and was flat in this focal count table.

## Training measurements used

The focal count table is highly zero-inflated: 1,205 of 1,674 training targets had `n_degs = 0`; the median was 0, the 75th percentile was 1, the 95th percentile was 18, and the 97.5th percentile was 100. Thus a modest-looking two-digit count is already high relative to the empirical background.

RNA-processing training perturbations separated into broad, weak, and null cases in the exact same class:

| comparator | focal n_degs | interpretation for Srrm2 |
| --- | ---: | --- |
| `U2af2` | 828 | core spliceosome/RNA-processing broad response |
| `Rnpc3` | 868 | core spliceosome broad response |
| `Hnrnpu` | 733 | broad RNP/RNA-processing response |
| `Prpf6` | 454 | spliceosome broad response despite only 72 matched perturbed cells |
| `Cdc40` | 624 | spliceosome broad response |
| `Thoc1` | 303 | TREX/export-linked broad response |
| `Snrnp70` | 213 | U1 snRNP response |
| `Tardbp` | 210 | RNA-binding response with only partial spliceosome convergence |
| `Hnrnpc` | 122 | hnRNP-family member with moderate response |
| `Hnrnpa2b1` | 11 | weak hnRNP/RBP response |
| `Hnrnph2` | 4 | weak hnRNP/RBP response |
| `Son` | 0 | closest speckle-core boundary case |
| `Ddx39b` | 0 | RNA export/splicing factor can be silent in this class |
| `Snrpb` | 0 | core spliceosomal family membership alone is insufficient |

The declared parquet confirmed these same focal counts and showed that self-transcript loss was not a reliable discriminator: `Prpf6` had hundreds of downstream DEGs without significant self-mRNA depletion in this class, whereas `Son`, `Ddx39b`, and `Snrpb` were flat.

## Corpus/profile interpretation

Same-experiment Findings over the measured comparator genes reported a real but selective RNA-biogenesis state: `Prpf6`, `U2af2`, `Snrnp70`, `Cdc40`, `Rnpc3`, `Hnrnpu`, `Thoc1`, and `Tpr` form a densely cross-referenced RNA-processing module in the release. A cohort profile over `Son`, `Prpf6`, `U2af2`, `Hnrnpu`, `Hnrnpc`, `Tardbp`, `Snrnp70`, `Rnpc3`, `Ddx39b`, `Snrpb`, `Hnrnpa2b1`, `Hnrnph2`, `Cdc40`, `Tpr`, and `Thoc1` also showed that the shared signature is stronger in the negative tail than the positive tail.

The same corpus explicitly warns against a generic RNA-processing transfer: `Son` did not phenocopy broad RNA-processing-factor loss, and `U2af2` did not simply phenocopy every RNA-binding or hnRNP perturbation. Those boundary observations matter more for `Srrm2` than the largest `U2af2`/`Rnpc3` counts, because SRRM2 is a nuclear-speckle scaffold and spliceosome-associated factor rather than a core snRNP or U2-recognition component.

## Numeric synthesis

I put the point above the global background because `Srrm2` is essentially ubiquitously expressed in the focal thalamic population, operative SRRM2 should be at least partly depleted by harvest, and the training data show that this cell class can mount RNA-processing responses. I kept it far below the 200-800 DEG core-spliceosome range because the most directly related observed perturbation, `Son`, was flat; SRRM2's best-established consequence is alternative splicing rather than gene-level abundance; and several measured RNA-processing perturbations were weak or null.

I therefore predict a small but nonzero response, just above the training 95th percentile:

`predicted_n_degs = 25`
