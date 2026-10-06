# GAPDH DEG-count prediction

## Question and interpretation

The requested held-out perturbation list contained one gene, `Gapdh`.  I interpreted
the task as a point prediction for the total number of genes with
`pvals_adj < 0.05` in the held-out `Gapdh` knockout in the focal
`151 TH Prkcd Grin2c Glut` class.  The count includes the perturbed gene's own
transcript if that transcript is measured and passes the same FDR threshold, as
it does for several training targets.

I treated `151 TH Prkcd Grin2c Glut` as the thalamic glutamatergic neuronal
group described in the dataset context.  I did not treat the absence of the
held-out `Gapdh` row from the parquet as a biological zero; the point estimate
below is transferred from non-held-out glycolysis perturbations and GAPDH
biology.

## Sources used

- Training endpoint counts:
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
- Training differential-expression parquet:
  `[local file: training_de_all_cell_groups.parquet]`.
- Same-experiment semantic layer: Distributed Agents corpus
  `perturbai-july-260713-sourceguard-1773-v1`.
- Distributed Agents runtime profile comparison over the focal cell group, using
  `logfoldchanges` keyed by `gene_target` and `names`.
- KEGG, genes/pathway records current 2026-09-23 and `mmu00010`
  Glycolysis/Gluconeogenesis record current 2026-09-17.  KEGG annotates mouse
  `Gapdh` as glyceraldehyde-3-phosphate dehydrogenase, EC 1.2.1.12, in
  glycolysis modules `M00001` and `M00002`, and lists `Gapdhs` as the
  testis-specific paralog in the same enzyme class.
- External literature on GAPDH's non-glycolytic stress functions, used only as
  weak prior knowledge: Nicholls et al. 2012, DOI 10.1111/j.1440-1681.2011.05599.x;
  Hildebrandt et al. 2015, DOI 10.1515/hsz-2014-0295; White and Garcin 2017,
  DOI 10.1007/978-3-319-46503-6_15.

## Computational steps over the training data

1. Read the requested-target CSV and confirmed it has exactly one row:
   `Gapdh`.
2. Read the focal training count table and summarized its calibration:
   1,674 non-held-out targets; 1,205 have 0 DEGs; 363 have 1-9; 63 have
   10-99; 43 have at least 100.  The median is 0 and the distribution is
   extremely right-skewed, so a generic essential-gene prior would overpredict
   unless same-pathway training perturbations justified a large footprint.
3. Searched KEGG `mmu00010` glycolysis genes against the training-count
   universe.  The represented central-carbon analogs closest to GAPDH in the
   training table were:

   | training perturbation | focal `n_degs` |
   | --- | ---: |
   | `Hk1` | 1 |
   | `Gpi1` | 1 |
   | `Pfkm` | 1 |
   | `Tpi1` | 1 |
   | `Eno1` | 0 |
   | `Slc2a1` | 0 |
   | `Pdha1` | 1 |
   | `Gfpt1` | 311 |
   | `Ogt` | 4 |

4. Pulled the exact focal DE rows for `Hk1`, `Gpi1`, `Pfkm`, `Tpi1`,
   `Eno1`, `Slc2a1`, `Pdha1`, `Gfpt1`, and `Ogt` from the 8.3 GB parquet with
   a `pyarrow.dataset` filter on `group_name` and `gene_target`, keeping
   `names`, `gene_target`, `logfoldchanges`, `pvals_adj`, `scores`,
   `n_pert_matched`, and `n_ctrl_matched`.

   The operation was:

   ```python
   flt = (
       (pc.field("group_name") == "151 TH Prkcd Grin2c Glut")
       & pc.field("gene_target").isin(analogs)
   )
   table = dataset.to_table(columns=columns, filter=flt)
   ```

5. Verified that the one-DEG counts for the central-glycolysis analogs are
   self-transcript-only effects in the focal group:

   | perturbation | significant focal genes | target self log2FC; FDR |
   | --- | --- | --- |
   | `Hk1` | `Hk1` only | -0.768; 9.86e-05 |
   | `Gpi1` | `Gpi1` only | -0.673; 2.14e-07 |
   | `Pfkm` | `Pfkm` only | -0.857; 6.42e-14 |
   | `Tpi1` | `Tpi1` only | -1.010; 6.23e-12 |
   | `Pdha1` | `Pdha1` only | -1.039; 1.31e-06 |
   | `Eno1` | none | `Eno1` was not a measured feature in this parquet |
   | `Slc2a1` | none | -0.701; FDR 1.0 |

6. Used `Gfpt1` as an internal counterexample showing that metabolic stress can
   be visible in this focal group when the perturbed node reaches a responsive
   branch.  `Gfpt1` has 311 focal DEGs despite only 120 matched perturbed
   nuclei; its significant genes include `Ogt` down and ER/ISR/amino-acid
   stress genes such as `Herpud1`, `Asns`, `Ddit3`, `Hspa5`, `Chac1`, `Atf4`,
   aminoacyl-tRNA synthetases, and serine/one-carbon genes.  This separates the
   flat single-gene central-glycolysis hits from a true broad response in the
   same assay and matched focal class.
7. Ran a Distributed Agents runtime `profile_compare` over
   `Hk1,Gpi1,Pfkm,Tpi1,Eno1,Slc2a1,Pdha1,Gfpt1,Ogt` in the focal cell group.
   It confirmed that the relevant central-glycolysis analogs have 0 or 1
   FDR-significant focal features while `Gfpt1` is the broad responder.  The
   high-magnitude log-fold-change tails for the one-DEG analogs were almost all
   non-significant low-expression artifacts (`pvals_adj` mostly 1.0), so I used
   them as a check against hidden significant overlap rather than as positive
   evidence for a downstream module.

## Same-experiment and biological reasoning for `Gapdh`

`Gapdh` is the sixth glycolytic enzyme, immediately downstream of aldolase/TPI
and upstream of PGK.  In mouse KEGG `mmu00010`, the only direct GAPDH paralog
with the same EC number is `Gapdhs`, annotated as testis-specific, not a
neuronal glycolytic backup enzyme.  GAPDH also has redox-, nuclear-, RNA-, and
apoptosis-related moonlighting roles (Nicholls et al. 2012; Hildebrandt et al.
2015; White and Garcin 2017), so it was not safe to assume that its knockout
would be completely equivalent to every glycolysis enzyme.

The strongest within-dataset evidence nevertheless comes from the central
glycolysis block:

- `Tpi1` is immediately upstream of GAPDH.  It had one DEG in the focal group,
  `Tpi1` itself.  Distributed Agents reports that `Tpi1` did not activate expected
  glycolytic-compensation, glyoxalase, ISR/UPR, or proteasome transcripts, and
  that the larger `Gfpt1`/O-GlcNAc and `Psmb4` stress signatures were not
  phenocopied by central glycolytic comparators.
- `Pfkm`, an upstream committed glycolytic enzyme, likewise had one focal DEG,
  `Pfkm` itself.  The Distributed Agents `Pfkm:F002` finding explicitly compared
  `Hk1`, `Eno1`, `Gpi1`, `Slc2a1`, and `Tpi1` and summarized those represented
  neighbors as flat or nearly flat rather than as missed copies of a glycolytic
  stress state.
- `Hk1` and `Gpi1` sit farther upstream at glucose phosphorylation and
  glucose-6-phosphate isomerization.  In this focal class each had exactly one
  DEG, again only the self transcript.  The same-experiment `Hk1` finding
  contrasts flat `Gpi1`/`Tpi1`/`Pfkm`/`Eno1`/`Slc2a1` surfaces with broader
  `Ogt` activity, and the `Gpi1` finding calls GPI1 loss an almost
  origin-centered neuronal transcriptional phenotype.
- `Eno1` was a useful null boundary: it had zero focal DEGs and no corrected
  response in any recovered neuronal group in the Distributed Agents corpus.  ENO2/ENO3
  were not perturbation targets, but their readout transcripts did not become
  significant after `Eno1` perturbation, supporting pre-existing or enzymatic
  rather than induced RNA compensation.
- `Slc2a1` is not a glycolytic enzyme, but it tests neuronal glucose entry.  It
  also had zero focal DEGs, and Distributed Agents reports no glucose-starvation,
  glycolytic, HIF, ATF4/ISR, autophagy, or UPR transcript program after
  `Slc2a1` perturbation in the experiment.
- `Gfpt1` is the main counterexample.  It diverts fructose-6-phosphate into
  hexosamine biosynthesis, and perturbing it was highly visible in the focal
  neurons, with 311 DEGs.  Because `Gfpt1` directly changed `Ogt` and induced
  ER/ISR genes whereas the single-node central-glycolysis perturbations did not,
  I treated it as evidence that the assay could see nutrient/proteostasis RNA
  stress but that `Gapdh` should be kept with the buffered core-glycolysis
  comparators, not predicted near 311.
- `Pdha1` is downstream of glycolysis at mitochondrial pyruvate entry and also
  had only its own transcript as a focal DEG.  This is a weaker analog because
  it is mitochondrial pyruvate oxidation rather than cytosolic glycolysis, but
  it reinforces that a central-carbon enzyme can be self-only rather than broad
  in these recovered postmitotic nuclei.

The Distributed Agents corpus had no direct `Gapdh` target context, as expected for a
held-out perturbation, but a lexical claim search recovered the internal claim
that single perturbations of represented central glycolysis genes are
transcriptionally buffered in postmitotic neurons.  The induced corpus topology
over `Eno1`, `Gpi1`, `Hk1`, `Pfkm`, `Slc2a1`, `Tpi1`, and `Pdha1` placed
`Eno1/Gpi1/Hk1/Pfkm/Slc2a1/Tpi1` in one connected glycolysis component via
explicit report references and shared claims; `Pdha1` was isolated, as expected
for a more distal pyruvate-dehydrogenase comparator.

## Target-specific point estimate

### `Gapdh`: predicted `n_degs = 1`

I predict a nonzero but self-only response.  The downstream component should be
zero or very close to zero because the best available same-assay perturbations
of central glycolysis, `Hk1`, `Gpi1`, `Pfkm`, `Tpi1`, `Eno1`, and the glucose
entry target `Slc2a1`, failed to produce a broad FDR<0.05 response in
`151 TH Prkcd Grin2c Glut`.  GAPDH's nuclear/redox moonlighting roles are real
external biology, but they are usually stress- or post-translational
modification-dependent; the pooled P16 CRISPR assay in healthy recovered
NeuN-positive nuclei gives more weight to the flat same-dataset glycolytic
knockouts than to extrapolation from oxidative-stress literature.

The one predicted DEG is `Gapdh` itself.  This part is less about GAPDH
pathway signaling than about observability: `Hk1`, `Gpi1`, `Pfkm`, `Tpi1`, and
`Pdha1` all produced significant self-transcript depletion and no downstream
DEGs in the focal class.  GAPDH is an abundantly expressed housekeeping
transcript and the gRNA set targeted `Gapdh` directly, so a modest
CRISPR/NMD-linked drop is likely to be detected even if the surviving neurons
do not mount a secondary stress program.  `Eno1` and `Slc2a1` warn that the
self row is not guaranteed for every glycolytic or glucose-related target, but
GAPDH's high basal abundance makes the self-only one-DEG outcome a better point
estimate than a strict zero.

## Limits and extrapolations

- This is an extrapolation from neighboring glycolysis genes; `Gapdh` itself
  was held out of both the raw DE rows and the focal count table.
- The parquet gives nuclear RNA from recovered NeuN-positive nuclei only.  It
  does not measure GAPDH protein, enzyme activity, NADH/NAD+, ATP, methylglyoxal
  or redox chemistry, indel rates, or loss of neurons before FACS recovery.
- Direct lower-glycolysis perturbations closest to GAPDH, including `Pgk1`,
  `Pgam1`, `Pkm`, `Ldha`, and the testis-specific `Gapdhs`, were not in the
  focal training-count table, so the nearest represented core enzymes are
  mostly upstream.
- The same-experiment corpus was preinterpreted from the same Perturb-seq
  experiment; it is useful for curated comparisons but is not independent
  replication.
- `Gfpt1` shows that a carbon-flux-related perturbation can generate hundreds
  of DEGs in this focal group.  I rejected it as the quantitative analog for
  GAPDH because it sits on the hexosamine/ER-glycosylation branch rather than
  the buffered Embden-Meyerhof core, but the exact point prediction would be
  wrong if GAPDH's moonlighting or redox roles were engaged more strongly than
  the assayed `Hk1`/`Gpi1`/`Pfkm`/`Tpi1` perturbations suggest.
