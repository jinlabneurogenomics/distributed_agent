# Dalrd3 direct n_degs forecast

## Target and endpoint

- Target: `Dalrd3`
- Cell group: `151 TH Prkcd Grin2c Glut`
- Endpoint: measured genes with Wilcoxon `pvals_adj < 0.05`
- Forecast: `0`

## Evidence used

### Declared biology bundle for Dalrd3

The declared manifest and canonical biology bundle both identify the held-out perturbation as `Dalrd3`.

The exact focal-population expression measurement shows that `Dalrd3` is well represented in the matched non-target 151-class nuclei:

- `n_non_target_cells = 23679`
- `n_cells_expressing = 20282`
- `pct_cells_expressing = 85.65395498120698`
- `mean_log1p_cp10k = 0.7976864880141836`
- `pseudobulk_cpm = 142.63068767691584`

I therefore treated target presence in the assayed thalamic glutamatergic population as favorable rather than as a reason for a null call.

The bundle's functional-stock adjudication concluded `likely_substantially_depleted` by the P37-P44 harvest window: a P16 disruptive edit stops new DALRD3 production, residual DALRD3 and pre-existing m3C-modified tRNAs initially persist, generic mouse-brain protein and cultured-cell tRNA turnover both favor material replacement over 21-28 days, and no DALRD3-specific neuronal clearance time course was found.

The mechanism is narrow and partly post-transcriptional. DALRD3 is a METTL2 targeting factor for m3C32 modification on selected arginine tRNAs; loss nearly eliminates that mark on those tRNAs in human cells without lowering their steady-state abundance. The strongest organismal phenotype in the bundle is human germline developmental epileptic encephalopathy, while the bundle found no direct mouse postmitotic conditional-loss time course. I therefore treated `Dalrd3` as a real but uncertain acute postnatal neuronal perturbation whose main expected consequences could remain at tRNA, translation, protein, or developmental levels rather than necessarily becoming a bulk snRNA-seq state.

### Local 151-class training scale

The declared count table for `151 TH Prkcd Grin2c Glut` contains 1,674 training perturbations after removing the held-out target. The distribution is strongly zero-heavy:

- 1,205 / 1,674 targets have `n_degs = 0`.
- 276 have `n_degs = 1`.
- 31 have `n_degs = 2`.
- 59 have 3-10.
- 61 have 11-100.
- 42 have more than 100.
- The maximum is `Uba5 = 2677`.

Thus a positive molecular prior is not enough to move the prediction to a large footprint; even in this high-yield class, the median target has no BH-significant gene.

### Matched tRNA-modification comparators

Among training perturbations with the closest represented biology to `Dalrd3`, the exact 151-class counts were:

| training target | 151 `n_degs` | interpretation |
|---|---:|---|
| `Alkbh8` | 0 | tRNA wobble-uridine modification branch; measured null |
| `Nsun2` | 0 | tRNA methyltransferase with neurodevelopmental biology; measured null |
| `Trmt1` | 0 | tRNA m2,2G writer; measured null |
| `Elp2` | 150 | Elongator scaffold subunit; ISR/amino-acid program |
| `Elp1` | 645 | Elongator scaffold subunit; stronger same-branch ISR/UPR program |

I used the Parquet in the exact `151 TH Prkcd Grin2c Glut` context to compare these five training profiles. The matched profile table had 17,259 measured features per node and reproduced the same endpoint split under `pvals_adj < 0.05`: `Alkbh8`, `Nsun2`, and `Trmt1` each had 0 significant features; `Elp2` had 74 up and 76 down; `Elp1` had 340 up and 305 down.

The same-experiment Finding ledger is not an independent replicate of the Parquet, but it helped interpret that measured split. Packaged Findings for `Alkbh8`, `Nsun2`, and `Trmt1` describe these non-Elongator tRNA-modification perturbations as flat or nearly flat in the acute P16 neuronal screen and explicitly contrast them with the Elp1/Elp2 integrated-stress response. Packaged Findings for `Elp1` and `Elp2` attribute the large 151 signatures to the Elongator branch, with direct same-complex convergence and induction of ATF4/amino-acid and ER-quality-control genes.

## Reasoning

`Dalrd3` has better exact expression reach than a target-absence null, and the stock card supports substantial functional decline over the assay window. Those points argue against discounting it as unexpressed or impossible to perturb.

The expected downstream defect, however, is the loss of a targeting factor for m3C32 on two arginine tRNA species. That is narrower than Elongator's early wobble-U34 step and lacks a same-complex measured positive partner in the training table. The best represented non-Elongator tRNA-methylation comparators were all zero in the focal class, and corpus interpretations of those targets already treat the Elp1/Elp2 program as branch-specific rather than as a generic readout of any tRNA-writer knockout.

I therefore chose the floor of the local analog distribution. The forecast remains uncertain because no mouse postnatal Dalrd3 time course was available and survivor-conditioned snRNA-seq could miss protein-level or translational phenotypes, but the lightest task-matched synthesis points to no BH-significant 151-class mRNA genes.
