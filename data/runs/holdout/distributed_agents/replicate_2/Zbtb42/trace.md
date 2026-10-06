# Prediction trace

## Question and resolved ambiguities

The held-out manifest contains one requested target:

```tsv
target_name
Zbtb42
```

I interpreted the requested endpoint as the exact training-count endpoint:
the number of measured genes in `151 TH Prkcd Grin2c Glut` with
`pvals_adj < 0.05` after a P16 AAV CRISPR-Cas9 loss-of-function perturbation,
assayed by P37-P44 single-nucleus RNA-seq and tested by Wilcoxon rank-sum
against the matched non-targeting controls. The held-out `Zbtb42` perturbation
has no row in the supplied differential-expression parquet and no row in the
focal-cell training-count CSV, so I treated any direct `Zbtb42` signature as
unavailable and transferred from measured non-held-out perturbations only.

I used zeros as legitimate point predictions for "no measured gene is expected
to pass BH FDR 0.05", not as a claim that the knockout is biologically inert.
I did not use target-transcript knockdown as an editing-efficiency filter; the
dataset description cautions that self-RNA change is not a quantitative proxy
for functional editing.

## Sources used

- Input count CSV:
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
- Input differential-expression parquet:
  `[local file: training_de_all_cell_groups.parquet]`.
- Distributed Agents same-experiment semantic corpus
  `perturbai-july-260713-sourceguard-1773-v1`.
  The corpus has no `Zbtb42` claims, findings, or related-target paths, but it
  has annotated ZBTB-family comparisons for the represented training targets.
- NCBI Gene ESummary for mouse `Zbtb42` Gene ID 382639, accessed
  2026-09-23; the summary was supplied by Alliance of Genome Resources,
  July 2025.
- PubMed literature searches for `ZBTB42`, `Zfp651`, BTB/POZ zinc-finger
  transcription factors, and lethal congenital contracture syndrome.
  Key external literature:
  - Devaney et al. 2010, Human Genetics, DOI `10.1007/s00439-010-0940-2`:
    experimentally characterized the two-exon human/mouse ZBTB42 transcript and
    protein, with strongest mouse signal in skeletal muscle and ovary and a
    nuclear pattern enriched near neuromuscular junctions.
  - Harmon et al. 2010, Human Genetics, DOI
    `10.1007/s00439-010-0891-7`: showed that SNPs in a small haplotype upstream
    of `AKT1`, overlapping the `ZBTB42` promoter/first exon region, modulate
    cis-regulatory activity in muscle, bone, and fat reporter contexts and
    alter `ZBTB42` allele-specific expression in human skeletal muscle.
  - Patel et al. 2014, Human Molecular Genetics, DOI
    `10.1093/hmg/ddu384`: associated homozygous human `ZBTB42` mutation with a
    lethal congenital contracture syndrome and showed that zebrafish `zbtb42`
    knockdown disrupts skeletal muscle/myofibrillar development.
  - Huynh and Bardwell 1998, Oncogene, DOI `10.1038/sj.onc.1202197`, and
    Ahmad et al. 1998, PNAS, DOI `10.1073/pnas.95.21.12123`: established that
    BTB/POZ domains can mediate dimerization and recruitment of corepressors
    such as N-CoR/SMRT for transcriptional repression.

## Computational steps

1. I read the manifest and confirmed it contains exactly one unique target,
   `Zbtb42`, and that it is absent from the training-count CSV.
2. I summarized all 1,674 training targets in the focal count CSV. The endpoint
   is very zero-heavy: 1,205 of 1,674 targets have `n_degs = 0`; the median is
   0, the 75th percentile is 1, the 90th percentile is 2, and the 95th
   percentile is 18.
3. I queried the parquet with DuckDB, filtering to
   `group_name = '151 TH Prkcd Grin2c Glut'`, and for each selected analog
   counted `pvals_adj < 0.05`.

The focal-cell count query was:

```sql
SELECT gene_target,
       COUNT(*) AS measured,
       SUM(pvals_adj < 0.05)::INTEGER AS n_sig,
       MIN(pvals_adj) AS min_q,
       ANY_VALUE(n_pert_matched) AS n_pert,
       ANY_VALUE(n_ctrl_matched) AS n_ctrl
FROM read_parquet('training_de_all_cell_groups.parquet')
WHERE group_name = '151 TH Prkcd Grin2c Glut'
  AND gene_target IN (...)
GROUP BY gene_target;
```

I also checked the top low-`q` genes for non-null analogs so that one
exceptional family member would not be mistaken for a common ZBTB-family state.

## Within-dataset analogs for Zbtb42

`Zbtb42` is annotated as a BTB/POZ C2H2 zinc-finger transcription factor, so the
most direct in-dataset comparators are represented `Zbtb*` and related
zinc-finger transcription-factor perturbations. In the focal cell group:

| training target | matched perturbed nuclei | focal `n_degs` | expression-pattern evidence |
| --- | ---: | ---: | --- |
| `Zbtb10` | 187 | 0 | No focal genes passed FDR 0.05; the minimum adjusted p-value was 1.0. |
| `Zbtb16` | 180 | 0 | No focal genes passed FDR 0.05; the minimum adjusted p-value was 1.0. |
| `Zbtb20` | 185 | 0 | No focal genes passed FDR 0.05; the minimum adjusted p-value was 0.710. |
| `Zbtb21` | 137 | 0 | No focal genes passed FDR 0.05; the minimum adjusted p-value was 1.0. |
| `Zbtb38` | 199 | 1 | One significant focal gene, `Msra`, was up-regulated, with log2FC 0.485 and q = 0.00448. |
| `Zbtb18` | 208 | 5 | A small 151-local signature: `Endou`, `Pxdn`, `Clstn2`, `Man2a2`, and the measured `Zbtb18` transcript were significant. |
| `Zbtb7a` | 282 | 841 | A broad outlier signature led by genes such as `Pnma3`, `Col9a3`, `Gpc1`, `Usp11`, and `Sema4a`, all with q < 1.1e-34. |

The same-experiment Distributed Agents corpus explicitly cautions against treating the
family label as predictive: high-confidence claim
`claim:6db8c668eadac106872d` states that shared BTB-ZF/ZBTB family membership
is insufficient to predict a common postmitotic neuronal transcriptomic
phenotype. Its Zbtb-centered findings separate the broad `Zbtb7a` program from
the sparse `Zbtb18`/`Zbtb38` effects and from the flat `Zbtb10`,
`Zbtb16`, `Zbtb20`, and `Zbtb21` surfaces. The `Zbtb18` corpus findings are
also a useful boundary: the focal `Zbtb18` program is only a small
`Endou`/`Pxdn`/`Clstn2`/`Man2a2` response, and the partial
`Zbtb18`-`Zbtb7a` overlap does not generalize to the represented family.

More diffuse zinc-finger controls supported the same prior. Of 30 `Zfp*`
training perturbations, 25 had `n_degs = 0` in this cell group; the few
nonzero exceptions were target-specific outliers such as `Zfp423` with 150
DEGs and `Zfp236` with 19. Nearby broad nuclear regulators showed that the
assay can see a transcription-factor response when one exists in these cells
-- for example `Thap11` had 478 focal DEGs -- but broad transcription-factor
detectability did not extend to most uncharacterized C2H2/BTB perturbations.

`Akt1` would have been an attractive negative/positive check because human
`ZBTB42` lies immediately upstream of `AKT1` and shares a metabolic-syndrome
association haplotype with it, but `Akt1` was not present as a focal training
target, so I did not use a direct in-dataset `Akt1` count.

## Target-specific biological rationale

### Zbtb42

External gene-function evidence puts `Zbtb42` in the broad class of nuclear
BTB zinc-finger transcriptional regulators: mouse NCBI Gene 382639 names it
`zinc finger and BTB domain containing 42`, and classic BTB/POZ studies show
that this domain family can dimerize and recruit chromatin corepressors. That
domain-level fact is weakly compatible with a transcriptional response after
loss of function, but it is not enough to infer a broad postnatal neuronal
state.

The target-specific literature is mostly outside the assayed population.
Devaney et al. found the strongest murine ZBTB42 expression in skeletal muscle
and ovary and observed ZBTB42-enriched nuclei at neuromuscular junctions in
muscle. Harmon et al. focused on muscle/bone/fat cis-regulatory activity near
`AKT1`, not on brain neurons. Patel et al. tied `ZBTB42` mutation to lethal
congenital contracture syndrome and found a zebrafish skeletal-muscle
development phenotype. These results argue that ZBTB42 can matter
developmentally, but they do not nominate a maintained transcriptional module
in NeuN-enriched juvenile thalamic glutamatergic neurons.

The within-dataset transfer therefore dominates the point estimate. The
measured `Zbtb*` perturbations are mostly FDR-null in
`151 TH Prkcd Grin2c Glut`, and the corpus-annotated family comparison shows
that the one large family member, `Zbtb7a`, is a target-specific outlier rather
than a generic ZBTB archetype. `Zbtb18` and `Zbtb38` provide a plausible upper
boundary for a weak ZBTB-family effect, but even those reached only five and
one significant genes, respectively, despite similar or larger matched
perturbed-cell counts. Because `Zbtb42` lacks a Zbtb7a-like neuronal mechanism
and its best external evidence points to muscle/NMJ biology, I predict that no
gene will cross BH FDR 0.05 in the focal cell group.

Predicted `n_degs`: 0.

## Limits and extrapolation

- The Distributed Agents corpus has no direct `Zbtb42` report, claim, or graph edge in
  the selected release; all corpus support is by analogy to represented
  ZBTB/BTB-ZF perturbations.
- None of `Zbtb10`, `Zbtb16`, `Zbtb18`, `Zbtb20`, `Zbtb21`, `Zbtb38`, or
  `Zbtb7a` is a proven one-to-one paralog or biochemical partner of `Zbtb42`.
  They calibrate a broad domain family, not a shared complex.
- The focal endpoint is sample-size and FDR dependent. A prediction of zero
  allows subthreshold changes, sparse rare-cell effects, protein-level effects,
  or developmental roles that would not be visible after mosaic P16 CRISPR in
  recovered P37-P44 NeuN-positive nuclei.
- Human LCCS and zebrafish muscle phenotypes involve development and skeletal
  muscle organization; transferring that absence of neuronal specificity to
  postmitotic mouse thalamic neurons is still an extrapolation.
