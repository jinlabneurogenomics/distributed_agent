# Zfp799 held-out DEG-count prediction

## Question and endpoint

The requested held-out target was `Zfp799`. I interpreted the task as a point
prediction of the number of protein-coding measured genes that would pass
Benjamini-Hochberg adjusted Wilcoxon `pvals_adj < 0.05` in `151 TH Prkcd
Grin2c Glut` nuclei after P16-to-P37/P44 sparse AAV-CRISPR loss of function.
`n_degs` is therefore an assay- and power-dependent focal-cell transcriptional
response breadth, not a measure of target importance, viability, editing rate,
or direct repeat derepression.

`Zfp799` is absent from both supplied training files, so the prediction has to
transfer from non-held-out perturbations and from external function annotations.
No ranking supervision was supplied, and the requested output is not an
ordering, so I did not use the ranking-only `dataset.perturbseq_features`,
`synthesis.ordering_validate`, or predictive graph-review operations.

## Sources used

- Declared endpoint table:
  `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
- Declared differential-expression parquet:
  `training differential-expression dataset`.
- Run-local target manifest:
  `single-target request for Zfp799`.
- Run-local `task_bindings.json`, `coverage.json`, `capabilities.json`, and
  `dataset_context.md`.
- The internal same-experiment corpus
  `perturbai-july-260713-sourceguard-1773-v1`, using bounded Finding and
  Evidence/Reference entries for visible KRAB/C2H2 and SCAN/C2H2 perturbations.
  This is a semantic layer over the same Perturb-seq experiment, not
  independent replication.
- NCBI Gene and the Alliance of Genome Resources Jul 2025 gene summary for
  mouse `Zfp799`.
- PubMed and same-corpus reference records for KRAB-ZFP biology: Ecco, Imbeault
  and Trono 2017, doi:10.1242/dev.132605; Kauzlaric et al. 2017, PMID
  28334004, doi:10.1371/journal.pone.0173746; Wolf et al. 2020, PMID 32479262,
  doi:10.7554/eLife.56337; Yang et al. 2022, PMID 35259018,
  doi:10.1073/pnas.2119415119.

## Computational checks

The held-out CSV contained exactly one row, `Zfp799`; the focal-cell training
count file contained 1,674 unique non-held-out targets. The endpoint
distribution was strongly zero-inflated:

- 1,205 of 1,674 training targets had `n_degs = 0` in `151 TH Prkcd Grin2c Glut`.
- The median count was 0, the 75th percentile was 1, the 90th percentile was 2,
  and the right tail contained broad perturbations such as `Uba5` with 2,677
  DEGs and `Tpr` with 1,768 DEGs.
- Among the 30 visible `Zfp*` training perturbations in the endpoint table, 23
  were zero in the focal cell group. The large `Zfp423` count, 150 DEGs, is a
  counterexample showing that some zinc-finger transcription factors can be
  detected, but `Zfp423` is a developmental regulator rather than a
  sequence-specific KAP1/KRAB analog of `Zfp799`.

I then filtered the parquet to `group_name == "151 TH Prkcd Grin2c Glut"` and
to represented C2H2/KRAB, SCAN/KRAB, and broad chromatin comparator targets.
The focal-cell FDR<0.05 counts were:

| target | focal `n_degs` | interpretation |
| --- | ---: | --- |
| `Zfp1` | 0 | KRAB/C2H2 singleton, no corrected focal-cell response |
| `Zfp160` | 0 | KRAB/C2H2 singleton, no corrected focal-cell response |
| `Zfp182` | 0 | KRAB/C2H2 singleton, no corrected focal-cell response |
| `Zfp266` | 0 | zinc-finger target, no corrected focal-cell response |
| `Zfp612` | 1 | KRAB/C2H2 singleton; only `Notum` significant in the focal group |
| `Zfp846` | 0 | KRAB/C2H2 singleton, no corrected focal-cell response |
| `Zfp949` | 0 | KRAB/C2H2 singleton, no corrected focal-cell response |
| `Zfp950` | 0 | KRAB/C2H2 singleton, no corrected focal-cell response |
| `Zfp961` | 0 | KRAB/C2H2 ERV repressor, no corrected focal-cell response |
| `Zkscan1` | 0 | SCAN/KRAB C2H2 target, no corrected focal-cell response |
| `Zkscan16` | 0 | SCAN/KRAB C2H2 target, no corrected focal-cell response |
| `Zscan26` | 0 | SCAN C2H2 target, no corrected focal-cell response |
| `Setdb1` | 22 | broad KAP1/H3K9 effector, indirect positive comparator |
| `Chd4` | 100 | broad NuRD remodeler, indirect positive comparator |
| `Dnmt3a` | 0 | DNA methylation comparator, no focal-cell response |
| `Gatad2b` | 1 | NuRD subunit; only self-transcript significant |

For the same visible targets, I also counted significant rows across all
cell groups at FDR<0.05 and FDR<0.10. `Zfp1`, `Zfp160`, `Zfp949`, `Zfp950`,
and `Zkscan1` were zero across all recovered groups even at FDR<0.10. `Zfp182`,
`Zfp266`, `Zfp846`, `Zfp961`, `Zkscan16`, and `Zscan26` only had isolated
one- or two-gene responses in non-focal cell groups or singletons. `Zfp612` was
the closest weak positive focal-cell analog, with 1 FDR<0.05 gene in `151` and
2 in `110 CNU-HYa HY MM Glut`.

The relevant parquet operation was a direct filtered count, conceptually:

```python
dataset = pyarrow.dataset.dataset(training_parquet, format="parquet")
focal = pc.field("group_name") == "151 TH Prkcd Grin2c Glut"
same_family = pc.field("gene_target").isin(selected_zfp_and_corepressor_targets)
table = dataset.to_table(
    columns=["names", "gene_target", "pvals_adj"],
    filter=focal & same_family,
)
n_degs = table.to_pandas().assign(sig=lambda x: x.pvals_adj < 0.05) \
    .groupby("gene_target").sig.sum()
```

## Biological transfer to Zfp799

NCBI Gene identifies mouse `Zfp799` as `zinc finger protein 799` on chromosome
17, orthologous to human `ZNF878`, predicted by Alliance of Genome Resources
Jul 2025 to encode a nuclear, RNA-polymerase-II regulatory DNA-binding
transcription factor and reported as expressed in embryonic/floor-plate
structures. I found no PubMed record directly establishing a postnatal thalamic
or `151 TH Prkcd Grin2c Glut` function for `Zfp799`/`ZNF878`.

The causal model I used was:

1. P16 AAV-CRISPR produces mosaic loss of Zfp799 protein in postmitotic neurons.
2. If ZFP799 is a limiting C2H2/KRAB repressor in these neurons, its direct
   target promoters or transposable-element-derived enhancers would lose
   repression, generally through less KAP1/TRIM28, SETDB1/H3K9, NuRD/HDAC, or
   DNA-methylation-associated repression.
3. Direct local derepression would have to propagate to enough stable
   protein-coding nuclear RNAs in recovered `151` cells to pass single-nucleus
   Wilcoxon FDR.
4. Strong cell stress, antiviral, or cell-state effects in surviving neurons
   would broaden that coding-gene signature; weak locus-specific repeat effects
   or embryonic-only targets would not.

The external KRAB-ZFP literature supports step 2 as a plausible mechanism in
general: KRAB zinc fingers commonly recruit KAP1/TRIM28 and downstream SETDB1,
HP1, NuRD, and DNA methylation machinery to repress transposable-element-linked
regulatory loci, but murine KZFPs are rapidly duplicated, sequence-specific,
and often redundant or context-specific (Ecco et al. 2017; Kauzlaric et al.
2017; Wolf et al. 2020). The direct mouse `Zfp961` literature is an instructive
counterexample: ZFP961 binds PBS-Lys ERV sequences and can associate with KAP1
and SETDB1 in cell systems (Yang et al. 2022), yet `Zfp961` perturbation gave
0 focal DEGs in this P16-to-P37/P44 neuronal screen.

The internal same-experiment corpus reinforced that transfer. For visible
KRAB-family singletons, its packaged evidence reported that `Zfp1`, `Zfp160`,
`Zfp182`, `Zfp949`, and `Zfp950` did not phenocopy the represented
`Setdb1` response; `Zfp612` was sparse and orthogonal to `Setdb1`, `Chd4`, and
`Gatad2b`; `Zkscan1` and `Zkscan16` did not converge with `Zscan26` or with
the `Setdb1`/`Chd4` surfaces. In focal cells, `Setdb1` induced a modest module
including `Tasor`, `Atf7ip`, and protocadherin-gamma genes, and `Chd4` induced
a larger 100-DEG state; the sequence-specific zinc fingers above either did
not change those genes at all or produced only singletons. Thus the broad
chromatin-effectors show that this cell group can respond to perturbing
KAP1-adjacent repression machinery, but they are not direct count analogs for
an uncharacterized sequence-specific `Zfp799` loss.

For `Zfp799`, the same-intervention direction expected from `Zfp1`, `Zfp160`,
`Zfp182`, `Zfp949`, `Zfp950`, `Zfp961`, `Zkscan1`, `Zkscan16`, and `Zscan26`
is same-outcome or indeterminate and near-null: those are individual
DNA-binding zinc-finger perturbations with focal counts of 0, not indirect
coregulators. `Zfp612` is the main focal weak-positive challenge, but its one
`151` hit was `Notum` and the same-experiment report found the Zfp612 surface
orthogonal to KRAB/NuRD and SCAN-family comparators, so it does not justify
raising an otherwise orphan `Zfp799` above zero. `Setdb1` and `Chd4` have
larger counts in the same cell group, but transfer through them would require
ZFP799 to be a limiting feeder into the same effector complexes at loci whose
RNA changes are visible in postnatal thalamic neurons; there is no
Zfp799-specific evidence for that link, and several represented C2H2/KRAB
genes argue against such a generic transfer.

## Prediction

I predict `Zfp799` will produce no measured genes at FDR<0.05 in
`151 TH Prkcd Grin2c Glut`: the point prediction is `0` DEGs. This is driven
mainly by within-dataset evidence from multiple visible C2H2/KRAB singletons
with zero focal signatures, plus external annotation of `Zfp799` only as a
predicted, poorly characterized nuclear DNA-binding transcriptional regulator.

## Limits

The inference is weakly extrapolative because `Zfp799` itself is absent and I
did not find a published direct paralog, binding motif, or ERV-family target
that would make another perturbation an obligate same-endpoint analog. The
training parquet does not measure repeat RNAs, H3K9me3, DNA methylation,
chromatin occupancy, or indel formation, so a repeat-family derepression event
could be invisible to protein-coding snRNA-seq. The experiment is also limited
to recovered postnatal NeuN-positive nuclei; an embryonic floor-plate function,
a non-neuronal role, a transient early response before P37/P44, or a
selection effect in edited cells could be missed. Those caveats make small
nonzero counts plausible, but the best focal-cell calibration still centers on
zero.
