# Held-out DEG-count prediction for 151 TH Prkcd Grin2c Glut

## Question and resolution

The task asks for one integer prediction of `n_degs` for each gene in
`050_Dalrd3.csv`. Here `n_degs` is the number of measured genes whose
Benjamini-Hochberg-adjusted Wilcoxon p-value is below 0.05 for a CRISPR
loss-of-function perturbation in `151 TH Prkcd Grin2c Glut` nuclei.

The manifest contains exactly one requested target:

| target | decision |
| --- | --- |
| `Dalrd3` | predict no FDR-significant downstream genes: `0` |

I treated the endpoint as an assay-specific breadth statistic, not as a
measurement of whether DALRD3 is biologically important. Because `Dalrd3` was
held out, its own signature and DEG count were unavailable; I therefore
calibrated the call from same-cell training perturbations and then used
external gene-function evidence to decide which training targets were valid
analogs.

## Sources used

Primary screen data:

| file | use |
| --- | --- |
| `training_de_all_cell_groups.parquet` | focal-cell log fold changes, adjusted p-values, and matched cell counts for individual training perturbations |
| `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` | observed `n_degs` labels for the 1,674 non-held-out perturbations in the focal cell group |
| `050_Dalrd3.csv` | held-out target order |

Internal evidence:

- Distributed Agents corpus, release `perturbai-july-260713-sourceguard-1773-v1`.
- I queried `Dalrd3`, `Trmt1`, `Nsun2`, `Elp1`, and `Elp2`. The corpus had no
  direct `Dalrd3` findings, so it was used for same-experiment interpretation
  of the assayed tRNA-modification perturbations.

External biology:

- NCBI PubMed E-utilities, queried on 2026-09-23.
- Lentini et al. 2020, Nature Communications, DOI
  `10.1038/s41467-020-16321-6`, PMID `32427860`.
- Zhang et al. 2024, HGG Advances, DOI `10.1016/j.xhgg.2024.100377`, PMID
  `39482881`.

## Computation over the training data

I first read the requested-target CSV and confirmed that it contains only
`Dalrd3`. I then used the training count CSV to put any single prediction on
the right scale. In `151 TH Prkcd Grin2c Glut`, the training endpoint was
strongly zero-inflated: 1,205 of 1,674 targets had `n_degs = 0`; the median was
0, the 75th percentile was 1, the 90th percentile was 2, and only the upper tail
reached broad responses.

The full parquet has 616,253,184 rows, so I filtered by
`group_name = '151 TH Prkcd Grin2c Glut'` rather than materializing all cell
groups. The focal slice contains 28,891,566 rows:

| quantity | value |
| --- | ---: |
| training perturbations | 1,674 |
| measured genes per target | 17,259 |
| matched perturbed nuclei per target | 23 to 419 |
| matched controls | 23,679 |

I then extracted focal-cell counts and marker rows for tRNA-modification and
translation-stress comparators. The most informative local observations were:

| training target | focal `n_degs` | why it mattered |
| --- | ---: | --- |
| `Trmt1` | 0 | Cytosolic tRNA methyltransferase; closest assayed non-Elongator RNA-modification analog. Distributed Agents classifies it as nearly flat across the neuronal screen. |
| `Nsun2` | 0 | Cytosolic tRNA m5C methyltransferase with neurodevelopmental disease biology; Distributed Agents reports no BH-significant downstream mRNA program in any measured neuronal group. |
| `Alkbh8` | 0 | Wobble-uridine tRNA-modification enzyme downstream of Elongator chemistry; a useful negative tRNA-modification comparator. |
| `Cdkal1` | 0 | tRNA-modification disease relative; did not converge with Elongator or non-Elongator tRNA modifiers in this assay. |
| `Lars2`, `Fars2`, `Rars2` | 0 each | Mitochondrial aminoacyl-tRNA synthetases; indirect tRNA-homeostasis comparators showing that partial perturbation of related translation machinery need not create a 151-cell DEG response. |
| `Elp1` | 645 | Same-screen positive counterexample: an Elongator-complex perturbation that strongly activated an ATF4/amino-acid integrated-stress state in 151 cells. |
| `Elp2` | 150 | Same-complex `Elp1` phenocopy; reproduced the same stress module in the same direction but at lower breadth. |
| `Gfpt1`, `Atp2a2`, `Dhdds`, `Hspa5` | 311, 187, 116, 5 | Non-tRNA proteostasis/ER-stress comparators that share parts of the Elp1/Elp2 151 signature and mark the response as a detectable stress state rather than a hidden universal tRNA defect. |

The marker-level signature supported the same split. `Elp1` and `Elp2` induced
ATF4/amino-acid and ER-stress genes in the focal cell group, whereas the
non-Elongator tRNA comparators were flat on those same genes:

| target | `Asns` log2FC / q | `Chac1` log2FC / q | `Herpud1` log2FC / q | `Srsf5` log2FC / q |
| --- | ---: | ---: | ---: | ---: |
| `Elp1` | 1.456 / 1.50e-27 | 3.435 / 2.28e-28 | 0.982 / 4.76e-21 | -0.543 / 4.79e-14 |
| `Elp2` | 1.249 / 3.60e-16 | 2.858 / 7.45e-09 | 0.811 / 4.38e-13 | -0.299 / 2.60e-04 |
| `Trmt1` | -0.010 / 1 | -0.305 / 1 | 0.163 / 1 | -0.030 / 1 |
| `Nsun2` | 0.104 / 1 | 0.512 / 1 | -0.032 / 1 | 0.016 / 1 |
| `Alkbh8` | -0.100 / 1 | 0.215 / 1 | 0.202 / 1 | -0.047 / 1 |
| `Cdkal1` | 0.149 / 1 | -0.234 / 1 | 0.022 / 1 | -0.081 / 1 |
| `Lars2` | 0.116 / 1 | 0.132 / 1 | -0.038 / 1 | -0.009 / 1 |
| `Fars2` | 0.092 / 1 | -0.277 / 1 | 0.015 / 1 | 0.102 / 1 |
| `Rars2` | 0.115 / 1 | 0.038 / 1 | 0.034 / 1 | 0.000 / 1 |

This was the central within-dataset pattern used for `Dalrd3`: the experiment
can detect a tRNA-linked ISR/UPR transcriptional state when the disrupted
branch is Elongator, but multiple other RNA- and tRNA-modification perturbations
with plausible disease links had exactly zero focal DEGs.

## Target-specific reasoning

### Dalrd3

Known biology:

- DALRD3 is not a generic transcription factor or chromatin regulator; it is a
  DALR-domain tRNA-binding factor.
- Lentini et al. showed that human DALRD3 complexes with METTL2 to target a
  subset of arginine tRNAs for 3-methylcytosine, and that DALRD3-deficient
  cells have near-complete loss of the m3C mark on those tRNA-Arg species.
  The same paper connected a homozygous nonsense DALRD3 variant to
  developmental delay and early-onset epileptic encephalopathy.
- Zhang et al. reported a second epileptic-encephalopathy case, an R517C
  DALRD3 DALR-domain variant that reduced METTL2 association and substrate tRNA
  binding and impaired m3C formation.

Appropriate within-dataset analogs:

- No exact same-complex METTL2 perturbation is present in the training-count
  CSV. `Mettl2` is measured as an expression feature in the parquet but was not
  itself a 151-cell training target, so it could not be used as a direct
  perturbation analog.
- The closest functional comparators represented in the screen are
  `Trmt1`, `Nsun2`, `Alkbh8`, and `Cdkal1`: they all perturb tRNA nucleotide
  chemistry rather than a large RNA polymerase, spliceosome, proteasome, or
  chromatin complex. Each has 0 DEGs in the focal cell group.
- `Trmt1` and `Nsun2` were the strongest negative guideposts because the
  Distributed Agents same-screen corpus explicitly labels them as buffered/flat
  non-Elongator tRNA-modification perturbations. The corpus claim spanning
  `Alkbh8`, `Cdkal1`, `Nsun2`, and `Trmt1` states that single-gene perturbations
  of represented non-Elongator tRNA-modification enzymes are largely buffered
  or flat at the basal neuronal mRNA level in this screen.
- `Elp1` and `Elp2` are essential counterexamples, not close numeric templates.
  They show that an RNA-modification defect can yield a 151-cell ATF4,
  amino-acid, and proteostasis program, but Distributed Agents findings `Elp1:F003`,
  `Elp2:F003`, `Nsun2:F003`, and `Trmt1:F004` all separate that Elongator
  response from the flat `Alkbh8`/`Nsun2`/`Trmt1` branch.
- Mitochondrial aminoacyl-tRNA synthetase targets `Lars2`, `Fars2`, and
  `Rars2` are weaker mechanistic comparators, but their 0-DEG outcomes are
  consistent with the same point: partial loss of a tRNA-adjacent enzyme in this
  acute postnatal neuronal assay did not automatically activate the Elp1/Elp2
  stress module.

Zero/nonzero call:

I predict `Dalrd3` has zero focal-cell DEGs. A nonzero call would require
believing that loss of tRNA-Arg m3C crosses the same transcriptomic stress
threshold as Elongator-core loss. The training data argued the opposite:
non-Elongator tRNA writer perturbations had 0 DEGs and failed to up-regulate
`Asns`, `Chac1`, `Herpud1`, aminoacyl-tRNA synthetases, or amino-acid
transporters, all with adjusted p-values of 1 in the focal marker rows. DALRD3
also has a narrower substrate set than Elongator, and the experiment perturbs
sparsely at P16 with an average per-gRNA mRNA reduction of only about 18%, so a
post-transcriptional, substrate-specific m3C defect is unlikely to generate a
large nuclear mRNA response within 3 to 4 weeks.

The integer estimate is therefore exactly `0`, matching the flat non-Elongator
tRNA-modification comparators rather than the Elongator or ER-stress positives.

## Limits of the reasoning

- `Dalrd3` has no direct Distributed Agents corpus finding and no measured perturbation
  profile in the supplied training matrix.
- The most relevant enzymatic partner, `Mettl2`, was not an observed training
  perturbation in the focal count table, so there is no direct METTL2/DALRD3
  same-complex phenocopy to transfer.
- The parquet reports nuclear mRNA differential expression only. It does not
  measure DNA indels, DALRD3 protein, tRNA-Arg m3C, tRNA charging, translation
  pausing, seizure physiology, or developmental circuit phenotypes.
- `Trmt1`, `Nsun2`, `Alkbh8`, and `Cdkal1` are analogs because they alter tRNA
  chemistry, not because they share DALRD3 substrates or a protein complex.
- Disease genetics for DALRD3 are germline human loss-of-function contexts;
  this screen is mouse, sparse AAV-CRISPR, postmitotic, and postnatal. The
  prediction could therefore miss protein-level, developmental, or stressed
  states that do not become BH-significant snRNA-seq changes in this assay.
