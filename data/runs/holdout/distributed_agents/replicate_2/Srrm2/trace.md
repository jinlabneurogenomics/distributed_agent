# DEG-count prediction for held-out Srrm2

## Question and resolved ambiguities

The task is to predict the held-out integer `n_degs` for perturbing `Srrm2` in `151 TH Prkcd Grin2c Glut` neurons.  I interpreted `n_degs` exactly as in the supplied training endpoint: the number of measured genes in the focal cell group with Wilcoxon Benjamini-Hochberg `pvals_adj < 0.05`, using the perturbed-vs-control direction in the parquet.  The held-out target CSV contains a single requested target, `Srrm2`; it is absent from both the training-count CSV and from `gene_target` in the differential-expression parquet.

I treated the same-experiment differential-expression parquet and the focal-cell training DEG counts as the only quantitative endpoint evidence.  External gene-function sources were used only to choose and interpret biologically fair analogs.

## Sources used

- `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`: observed `n_degs` for the 1,674 non-held-out training perturbations in the focal cell group.
- `[local file: training_de_all_cell_groups.parquet]`: per-gene log-fold changes and FDRs for training perturbations.  I filtered this to `group_name = '151 TH Prkcd Grin2c Glut'` and to mechanistic RNA-processing comparators of `Srrm2`.
- Distributed Agents corpus `perturbai-july-260713-sourceguard-1773-v1`: same-experiment semantic reports for training targets.  `target_context(Srrm2)` returned no direct finding, consistent with the target being held out, but the reports for `Son`, `U2af2`, `Prpf6`, `Cdc40`, `Snrnp70`, and `Tnpo3` gave interpreted same-experiment comparator evidence.
- Distributed Agents gene-analog nomination and gene-annotation stores over the PerturbAI closed gene universe, including projected human CORUM 5.0 complexes through one-to-one MGI orthology downloaded 2026-09-13, Reactome mouse pathway membership, GO annotations, and pinned STRING v12.0 physical interactions.
- Reactome pathway labels from the annotation store and Reactome ContentService for `SRRM2`.
- PubMed literature:
  - Blencowe et al. 2000, PMID 10668804: identified the 300-kDa SRm160/300 subunit and described the SRm160/300 splicing coactivator.
  - Ilik et al. 2020, DOI `10.7554/eLife.60579`, PMID 33095160: showed that SON and SRRM2 organize nuclear speckles.
  - Zhang et al. 2024, DOI `10.1016/j.celrep.2024.113827`, PMID 38381607: showed that SRRM2 phase separation helps assemble nuclear-speckle subcompartments.
  - Maertens et al. 2014, DOI `10.1073/pnas.1320755111`, PMID 24449914: resolved the structural basis of TNPO3-mediated nuclear import of phosphorylated SR splicing factors.
  - Bertram et al. 2017, DOI `10.1038/nature21079`, PMID 28076346: placed PRPF6 and CDC40/PRP17 in spliceosome remodeling around catalytic step 2.

## Computational evidence

The training endpoint was extremely zero-inflated: 1,205/1,674 training targets, or 71.98%, had zero focal-cell DEGs; the median was zero, the 75th percentile was one, and only 43 targets had at least 100 DEGs.  Thus a nonzero prediction for `Srrm2` needs specific RNA-processing evidence rather than a generic prior.

The analog-nomination run for held-out `Srrm2` nominated spliceosome and RNA-processing factors, headed by projected CORUM co-members `U2af2`, `Snrpb`, `Snrnp70`, `Prpf6`, and `Cdc40`.  It also recovered `Ddx39b` through projected spliceosome E-complex membership plus a pinned STRING v12.0 physical edge to SRRM2, and broad hnRNP/RNA-binding comparators such as `Hnrnpa2b1`, `Hnrnpu`, `Hnrnpc`, and `Rnpc3`.

For a bounded quantitative review I scanned the parquet in the focal cell group for these available analogs:

```sql
select gene_target, names, logfoldchanges, pvals_adj, scores
from read_parquet(training_de_all_cell_groups)
where group_name = '151 TH Prkcd Grin2c Glut'
  and gene_target in (...Srrm2 analog cohort...);
```

The focal DEG counts of the main mechanistic comparators were:

| comparator | focal `n_degs` | relevance to Srrm2 |
| --- | ---: | --- |
| `U2af2` | 828 | Projected A/E-spliceosome co-complex with SRRM2; broad same-experiment U2AF2 state repeatedly down-regulated `Srrm2`, `Rsrp1`, `Luc7l2`, and other RNA-processing transcripts. |
| `Cdc40` | 624 | Projected C-complex co-member and STRING physical interactor; the same-experiment report places `Cdc40` with `Prpf6`, `U2af2`, and `Snrnp70` but not `Snrpb`.  In 151 TH, `Srrm2` itself was a top Cdc40-down gene. |
| `Tnpo3` | 618 | Not a spliceosome subunit, but imports phosphorylated RS/SR cargos; its report describes a canonical down module led by `Srrm2`, `Srsf5`, `Srsf1`, `Srsf7`, `Srsf2`, `Akap8l`, `Clk1`, and `Cstf2`. |
| `Prpf6` | 454 | Projected A/C/E-spliceosome co-member and STRING physical interactor; same-experiment reports show broad spliceosome stress shared with `U2af2`, `Cdc40`, `Snrnp70`, and `Rnpc3`. |
| `Snrnp70` | 213 | Direct projected SRm160/300 complex member with SRRM2 and direct U1 factor; broad enough to establish that the SRm160/300 neighborhood can be visible, but weaker than core U2/U5/C-complex perturbations. |
| `Rnpc3` | 868 | Minor-spliceosome factor, not a direct SRRM2 complex member; a strong positive comparator for RNA-processing stress, but mechanistically less direct. |
| `Hnrnpu` | 733 | Broad RNA-binding/nuclear RNP perturbation with strong 151 response; useful as evidence that hnRNP stress can be broad, but not a direct Srrm2 substitute. |
| `Hnrnpc` | 122 | Weaker hnRNP branch that only partly overlapped the broad spliceosome signatures. |
| `Hnrnpa2b1` | 11 | Projected spliceosome complex member with only a small focal response, arguing against blindly averaging all complex annotations upward. |
| `Ctnnbl1` | 1 | PRP19/A-spliceosome-associated projected member; same-experiment reports call it buffered relative to core `Prpf6`, `Rnpc3`, `U2af2`, `Snrnp70`, `Cdc40`, and `Hnrnpu`. |
| `Snrpb` | 0 | Projected SRRM2/SNRNP70 spliceosome member and STRING physical interactor; flat in the focal cell group and explicitly a boundary to generic snRNP transfer. |
| `Ddx39b` | 0 | Projected E-complex/STRING comparator with no focal DEGs; its strongest same-experiment response is in 191 MB P MY GABA, so it is a context counterexample. |
| `Son` | 0 | The most important nuclear-speckle scaffold counterexample; the same-experiment corpus states that `Son` did not phenocopy broad RNA-processing-factor loss and explicitly notes that `Srrm2` was the strongest literature-obvious missing speckle-core partner. |
| `Cstf2` | 0 | `Cstf2` is downstream of `Tnpo3` and `Prpf6` but itself flat, bounding the significance of individual RNA-processing marker changes. |

Within the 15-gene inspected analog cohort, the strong focal signatures shared many same-direction FDR genes: for example, `U2af2` vs `Rnpc3` shared 157 significant genes in the same direction, `Cdc40` vs `Tpr` shared 201, `Prpf6` vs `Rnpc3` shared 118, and `Rnpc3` vs `Snrnp70` shared 79.  By contrast, `Son`, `Snrpb`, and `Ddx39b` had zero significant features in this cell group, so every same-direction FDR intersection with the broad spliceosome module was zero.  I therefore interpreted `Srrm2` as likely to have a true RNA-processing response, but as lower than the catalytic/core-spliceosome targets `Rnpc3`, `U2af2`, `Cdc40`, and `Prpf6`.

## Target-specific prediction

`Srrm2` encodes SRm300, a large SR-related nuclear-speckle/spliceosome protein.  The curated annotation layer links SRRM2 to `Snrnp70` in the exact projected human CORUM SRm160/300 complex and to `U2af2`, `Snrpb`, `Snrnp70`, `Prpf6`, and `Cdc40` in projected spliceosome A/E/C-complexes.  It also carries narrower physical evidence to `Prpf6`, `Cdc40`, `Ddx39b`, and `Snrpb` through the pinned STRING physical network.  Those links make a zero call too conservative: the same 151 TH dataset shows that multiple hits to this RNA-maturation axis produce hundreds of DEGs, and three independent broad signatures, `U2af2`, `Cdc40`, and `Tnpo3`, directly push `Srrm2` downward as part of their RNA-processing remodeling state.

The downward adjustment is also important.  The best available speckle-core comparator, `Son`, had 0 DEGs in 151 TH and only a minimal single-gene response elsewhere in the same-experiment report.  Two very close projected or physical spliceosome members, `Snrpb` and `Ddx39b`, were also 0 in this focal group, and `Ctnnbl1` and `Hnrnpa2b1` were only 1 and 11.  These are not nulls from unrelated pathways; they show that scaffold or particle membership was not enough to guarantee the broad `U2af2`/`Rnpc3`/`Cdc40` response in the P16 acute neuronal assay.

Balancing those two sides, I called `Srrm2` positive but attenuated relative to core spliceosome loss.  `Snrnp70` at 213 DEGs is the most direct observed SRm160/300 anchor, `Hnrnpc` at 122 represents a weaker spliceosome-adjacent branch, and `Prpf6`/`Cdc40`/`U2af2` set an upper range of roughly 450-830 for stronger catalytic spliceosome hits.  I placed `Srrm2` just above `Snrnp70`, at 220 DEGs.

## Limits and extrapolation

This is an extrapolation from analogs because `Srrm2` itself was deliberately held out, and the same-experiment corpus has no `Srrm2` report.  The predicted magnitude depends on whether postnatal sparse CRISPR creates enough functional SRRM2 loss in this giant low-complexity protein to disrupt nuclear speckles; guide indel state and SRRM2 protein are unobserved.  The assay is 3-prime nuclear RNA and reports whole-gene abundance, not splice junctions, intron retention, nuclear-speckle morphology, or protein localization, so a zero or weak DEG count would not exclude a primary splicing defect.  Finally, all training analogs are imperfect: `U2af2`, `Prpf6`, `Cdc40`, `Snrnp70`, and `Rnpc3` perturb catalytic spliceosome or snRNP functions, while `Son` is the closest speckle scaffold but was nearly silent in this readout.

