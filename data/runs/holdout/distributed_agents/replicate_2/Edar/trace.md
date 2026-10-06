# Question

Predict the held-out value `n_degs` for each target in
`065_Edar.csv`, preserving requested order.  The endpoint is the number of
measured genes with Wilcoxon BH-adjusted `pvals_adj < 0.05` after sparse P16
CRISPR loss of the target in `151 TH Prkcd Grin2c Glut` neurons.  I treated a
zero as an expected lack of any FDR 0.05 DEG in the recovered thalamic
glutamatergic nuclei, not as a statement that EDAR is biologically unimportant
in all tissues.

The requested held-out list contains one target:

| target_name |
| --- |
| Edar |

# Sources Used

- Direct input tables:
  - `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`, for observed FDR 0.05
    DEG counts in the focal cell group for 1,674 non-held-out training targets.
  - `training_de_all_cell_groups.parquet`, for focal-cell adjusted p-values,
    signed Wilcoxon scores, log fold changes, and matched nucleus counts for
    mechanistically related training perturbations.
  - `065_Edar.csv`, for the requested held-out target and exact output order.
- Same-experiment internal knowledge layer: Distributed Agents corpus
  `perturbai-july-260713-sourceguard-1773-v1`.  `Edar` was not itself present
  in that corpus, consistent with the holdout, but claims and target-context
  records for `Eda`, `Cd40`, `Chuk`, `Traf3`, and `Tnfrsf1a` summarized
  within-experiment comparisons over the same Perturb-seq parquet.
- External biology and literature:
  - Headon and Overbeek 1999, DOI `10.1038/11943`, PubMed `10431242`:
    positional cloning of mouse `downless` as the TNF-receptor-family gene
    `Edar`, required for ectodermal placode derivatives.
  - Monreal et al. 1999, DOI `10.1038/11937`, PubMed `10431241`: human `EDAR`
    mutations cause autosomal hypohidrotic ectodermal dysplasia.
  - Headon et al. 2001, DOI `10.1038/414913a`, PubMed `11780064`: the
    `crinkled` locus encodes `Edaradd`, a death-domain adaptor that links EDAR
    to downstream signaling.
  - Morlon, Munnich, and Smahi 2005, DOI `10.1093/hmg/ddi405`, PubMed
    `16251197`: EDARADD recruits the TAB2/TRAF6/TAK1 complex to activate the
    IKK/NF-kappaB pathway downstream of EDAR.
  - Lindfors, Voutilainen, and Mikkola 2013, DOI `10.1007/s10911-013-9277-5`,
    PubMed `23591968`: the Eda/Edar/Edaradd pathway is summarized as a
    TNF-like ligand, TNFR-family receptor, and NF-kappaB-mediated
    transcriptional pathway in ectodermal appendage development.

# Computation Over the Input Data

I first read `065_Edar.csv`; it contains exactly `Edar`.

From the focal training-count CSV I computed the empirical calibration:

- Training targets: 1,674.
- Fraction with `n_degs == 0` in `151 TH Prkcd Grin2c Glut`: 0.7198.
- Median `n_degs`: 0.
- 75th percentile: 1.
- 90th percentile: 2.
- 95th percentile: 18.

I then pulled the focal-cell rows from `training_de_all_cell_groups.parquet`
for biologically nearby targets.  The direct EDAR ligand and every represented
EDAR-adjacent TNFR/NF-kappaB target had zero FDR 0.05 DEGs in the focal count
table:

| training target | relation to EDAR biology | focal `n_degs` | focal minimum `pvals_adj` |
| --- | --- | ---: | ---: |
| `Eda` | cognate TNF-family ligand for EDAR | 0 | 1.000000 |
| `Cd40` | TNFR-family receptor using TRAF/NF-kappaB signaling | 0 | 1.000000 |
| `Fas` | TNFR/death-receptor family counterexample | 0 | 1.000000 |
| `Tnfrsf1a` | TNFR1 comparator | 0 | 1.000000 |
| `Tnfrsf11a` | RANK/TNFRSF comparator | 0 | 1.000000 |
| `Tnfrsf13c` | TNFRSF/BAFFR comparator | 0 | 0.815593 |
| `Tnfrsf4` | TNFRSF/OX40 comparator | 0 | 1.000000 |
| `Tnfrsf9` | TNFRSF/CD137 comparator | 0 | 0.390980 |
| `Map3k7` | TAK1 kinase downstream of EDARADD/TAB2/TRAF6 | 0 | 1.000000 |
| `Chuk` | IKK-alpha kinase in NF-kappaB activation | 0 | 0.726612 |
| `Nfkb1` | NF-kappaB p105/p50 subunit | 0 | 1.000000 |
| `Traf3` | TRAF-family pathway comparator | 0 | 1.000000 |

As receptor-side innate/NF-kappaB counterexamples, the represented TLRs were
also null in the focal cell group: `Tlr2`, `Tlr3`, `Tlr4`, `Tlr5`, `Tlr7`, and
`Tlr8` each had `n_degs = 0`.  For `Eda`, the measured EDAR/NF-kappaB sentinel
genes that would be expected in an ectodermal placode program were present in
the table but far from significant in the focal cell group: `Edar`, `Dkk4`,
`Lrp4`, `Shh`, `Ccnd1`, `Nfkbia`, `Tnfaip3`, `Birc2`, `Birc3`, `Fos`, and
`Jun` all had adjusted p-values of 1.0.

The same-experiment Distributed Agents corpus agreed with the raw extraction:

- `Eda:F001` reported a pan-neuronal corrected-DE null for `Eda`, with 0
  downstream genes at FDR 0.10 in all 23 measured neuronal groups.
- `Eda:F003` contrasted `Eda` with `Nfkb1`, `Chuk`, `Map3k7`, and `Traf3` and
  reported absence of the embryonic EDA/EDAR/NF-kappaB placode program.
- `Eda:F004` found that detectable thalamic Wnt/beta-catenin responses through
  `Ctnnb1`, `Tcf7l2`, and `Lrp6` did not converge with `Eda`; this matters
  because Wnt and EDA/EDAR are developmentally linked in ectoderm, but the
  directly tested ligand did not phenocopy a neuronal Wnt response.
- Corpus claim `claim:778b2c45f226febe4372` summarized represented
  CD40/TNFR/TLR/IL-1-to-TAK1/IKK/NF-kappaB/JNK/p38 perturbations as broadly
  transcriptionally silent in unchallenged postnatal NeuN-positive neurons.
- Corpus claim `claim:c5ebf285abfd6f803965` summarized represented
  TNFR-superfamily, death-receptor, TRAF, NF-kappaB, and MAPK-adjacent
  perturbations as refractory to a shared basal immune-like or death-receptor
  neuronal transcriptomic module.

# Target-Specific Reasoning

## Edar

`Edar` encodes the receptor for EDA-A1.  In the canonical ectodermal pathway,
EDA binds EDAR, EDAR recruits the adaptor EDARADD, and EDARADD connects via
TAB2/TRAF6/TAK1 to IKK and NF-kappaB.  This pathway is genetically central to
hair follicles, teeth, sweat glands, and other ectodermal appendages:
loss-of-function mutations in mouse `Edar`/`Eda`/`Edaradd` or human `EDAR`
cause hypohidrotic ectodermal dysplasia rather than a primary postnatal
thalamic neuron syndrome.

The closest training perturbation was the cognate ligand `Eda`.  `Eda` had
`n_degs = 0` in `151 TH Prkcd Grin2c Glut`, and in the focal raw parquet every
gene in the `Eda` contrast had adjusted p-value 1.0; the cell group had 221
matched perturbed nuclei against 23,679 controls, so this was not just a
single-gene self-transcript dropout.  The internal `Eda` context extended the
negative result across all neuronal groups and specifically noted that expected
EDAR/NF-kappaB or placode-associated transcripts such as `Dkk4`, `Lrp4`,
`Shh`, `Ccnd1`, and `Edar` were not induced or repressed detectably.

The downstream receptor-to-NF-kappaB branch gave the same answer.  `Map3k7`,
`Chuk`, `Nfkb1`, and `Traf3` were all zero in the focal count table, and none
had a near-threshold focal minimum adjusted p-value.  The broader TNFR-family
counterexamples `Cd40`, `Fas`, `Tnfrsf1a`, `Tnfrsf11a`, `Tnfrsf13c`,
`Tnfrsf4`, and `Tnfrsf9` were also all zero.  Those are imperfect substitutes
for EDAR because many signal through different TRAF combinations and
cell-type-specific ligands, but their joint nulls are a strong within-dataset
boundary: basal, unchallenged NeuN-positive juvenile neurons did not show a
constitutive TNFR/TLR/IKK/NF-kappaB RNA program that would make an EDAR-family
receptor perturbation obvious.

I therefore predict no FDR 0.05 DEG for `Edar` in the focal cell group:

```tsv
target_name	predicted_n_degs
Edar	0
```

# Limits and Extrapolation

This is still an extrapolation from pathway neighbors because `Edar` itself was
held out and `Edaradd`, `Traf6`, `Tab2`, `Ikbkb`, `Ikbkg`, `Nfkb2`, `Rela`,
and `Relb` were absent as perturbation targets in the training count table.
The experiment is also a basal loss-of-function screen; it did not provide
ectodysplasin ligand, inflammatory stimulation, epithelial placodes, teeth,
skin, sweat glands, craniofacial tissue, or embryonic induction windows.  Thus
the zero prediction is scoped narrowly to recovered postnatal NeuN-positive
`151 TH Prkcd Grin2c Glut` nuclei 3-4 weeks after AAV CRISPR delivery.
