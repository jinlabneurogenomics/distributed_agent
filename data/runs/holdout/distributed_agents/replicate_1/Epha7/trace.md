# Prediction trace

## Question and endpoint

I interpreted the task as a scalar holdout prediction for one perturbation,
`Epha7`, in `151 TH Prkcd Grin2c Glut` cells. The requested output is the
integer number of measured genes whose Wilcoxon `pvals_adj` would be below 0.05
for the held-out `Epha7` CRISPR perturbation. I treated the endpoint as directly
observed for the 1,674 supplied non-held-out training perturbations and absent
for `Epha7`; no `Epha7` perturbation rows occur in the declared Parquet or the
training-count CSV.

Two points constrained the prediction. First, `n_degs` includes the target
transcript if that row passes FDR, as illustrated by `Epha4` below. Second,
self-transcript loss in this Perturb-seq design is not a quantitative measure of
editing success or biological strength, so a self-only signature is weak
evidence for the count and is not evidence for a broad downstream transcriptional
state.

## Sources used

- Declared focal training counts:
  `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
- Declared differential-expression table:
  `training differential-expression dataset`.
- Run-local manifest of requested genes:
  `single-target request for Epha7`.
- Run-local task bindings, compact coverage, capability manifest, and
  measurement registry under `codex_runtime/pipeline/`.
- Internal same-experiment corpus:
  `perturbai-july-260713-sourceguard-1773-v1`. I queried its story inventory for
  visible Eph-family analogs and found no packaged Findings for `Epha2`,
  `Epha3`, `Epha4`, `Epha5`, `Epha10`, `Ephb1`, `Ephb2`, or `Ephb4` in this
  filtered release, so no same-experiment report text entered the endpoint
  decision.
- PubMed for external mechanism checks:
  Lisabeth, Falivelli and Pasquale 2013, DOI 10.1101/cshperspect.a009159;
  Rashid et al. 2005, DOI 10.1016/j.neuron.2005.05.030;
  Torii, Rakic and Levitt 2013, DOI 10.1002/cne.23195;
  Leonard et al. 2020, DOI 10.1371/journal.pone.0231561.

## Dataset calibration

I used the focal training-count CSV to calibrate the response-breadth scale.
The focal class is highly zero-inflated: among 1,674 training targets, 1,205
had `n_degs = 0`; the median was 0, the 75th percentile was 1, the 90th
percentile was 2, the 95th percentile was 18, and the mean was 14.1 only
because a small number of targets such as `Uba5`, `Tpr`, and `Sin3a` produced
hundreds to thousands of DEGs.

I then queried the Parquet for the closest visible Eph receptors in the same
cell class. The exact SQL operation was:

```sql
SELECT gene_target,
       COUNT(*) AS measured,
       SUM(CASE WHEN pvals_adj < 0.05 THEN 1 ELSE 0 END) AS n_degs,
       MIN(pvals_adj) AS min_padj
FROM parquet_scan($training_de)
WHERE group_name = '151 TH Prkcd Grin2c Glut'
  AND gene_target IN
      ('Epha2','Epha3','Epha4','Epha5','Epha10','Ephb1','Ephb2','Ephb4')
GROUP BY gene_target;
```

All eight visible Eph receptors had 17,259 measured-gene rows in the focal
cell group. Their observed focal counts were:

| target | focal `n_degs` | expression-pattern evidence |
| --- | ---: | --- |
| `Epha10` | 0 | no FDR-significant measured gene; self row `Epha10`, logFC -0.368, padj 1 |
| `Epha2` | 0 | no FDR-significant measured gene; self row `Epha2`, logFC +0.842, padj 1 |
| `Epha3` | 0 | no FDR-significant measured gene; self row `Epha3`, logFC -0.005, padj 1 |
| `Epha4` | 1 | the only FDR-significant gene was the perturbed transcript itself, `Epha4`, logFC -1.027, padj 7.9e-32 |
| `Epha5` | 0 | no FDR-significant measured gene; self row `Epha5`, logFC -0.149, padj 1 |
| `Ephb1` | 0 | no FDR-significant measured gene; self row `Ephb1`, logFC +0.214, padj 1 |
| `Ephb2` | 0 | no FDR-significant measured gene; self row `Ephb2`, logFC -0.412, padj 1 |
| `Ephb4` | 0 | no FDR-significant measured gene; self row `Ephb4`, logFC +0.451, padj 1 |

The near-null behavior was not specific to one EphA paralog. In the declared
training counts, Eph/ephrin-proximal Rho/MAPK and axon-guidance perturbations
were also at the assay floor in the focal class: `Fyn` 0, `Mapk1` 0, `Mapk9`
0, `Rac1` 0, `Pak1` 1, `Pak2` 0, `Pak3` 0, `Mtor` 2, `Plxna1` 0, `Plxna2` 1,
`Plxna4` 0, `Sema4d` 0, `Sema5a` 1, `Sema6a` 0, `Slit2` 0, `Robo1` 1, `Robo2`
0, `Dcc` 0, `Unc5c` 1, and `Unc5d` 0. I used these as negative
counterexamples for the idea that perturbing a membrane guidance cue or its
small-GTPase/MAPK effector layer generally creates a broad recovered-cell DEG
state in this focal population.

## Target-specific reasoning

### `Epha7`

`Epha7` is an EphA receptor tyrosine kinase. Eph receptors bind
membrane-tethered ephrins and signal through contact-dependent bidirectional
pathways that converge on cytoskeletal and Ras/Rho-family effectors rather than
on a constitutive transcription-factor complex; this signaling mode is
summarized by Lisabeth et al. 2013. `Epha7` itself has strong nervous-system
developmental roles: EphA7 mutant mice have disrupted retinocollicular
topographic maps, reported by Rashid et al. 2005; EphA7/ephrin-A signaling
helps set corticothalamic projection maps in mouse, reported by Torii et al.
2013; and EphA7 isoforms can regulate cortical dendritic growth and spine
formation with an mTOR-sensitive dendritic-branching component, reported by
Leonard et al. 2020.

The within-dataset transfer model is therefore:

1. Intervention: sparse postnatal CRISPR loss of `Epha7`.
2. Direct molecular consequence: reduced functional EphA7 receptor in the
   edited neuron, with uncertain visibility through nuclear `Epha7` mRNA.
3. Propagation: altered ephrin-A/EphA contact signaling to cytoskeletal and
   local growth/spine pathways, not an obligate stoichiometric loss of a
   transcriptional complex.
4. Exposure and timing: AAV was delivered at P16 and nuclei were harvested at
   P37 to P44. Major mouse retinocollicular and corticothalamic topographic
   mapping roles of EphA7 are prenatal or early postnatal; Torii et al. place
   corticothalamic map establishment by the second postnatal week, before this
   screen's perturbation has had much time to act.
5. Sampling: the measured endpoint is a survivor-conditioned nuclear RNA state
   in recovered `151 TH Prkcd Grin2c Glut` nuclei, not neurite targeting or
   synaptic morphology.

`Epha4` was the closest visible EphA receptor analog in the focal dataset and
produced a count of 1, but that one gene was `Epha4` itself; it had no detected
downstream FDR-significant genes. `Epha2`, `Epha3`, `Epha5`, and `Epha10`
likewise produced no focal DEGs. The B-class Eph receptors in the screen
(`Ephb1`, `Ephb2`, `Ephb4`) were less direct paralogs but were useful
counterexamples because they share contact-dependent Eph/ephrin signaling and
also produced zero focal DEGs. Perturbations of candidate downstream or
parallel axon-guidance nodes were not broad either: for example `Fyn`, `Rac1`,
`Mapk1`, `Mapk9`, `Plxna1`, `Plxna4`, `Sema6a`, `Slit2`, `Robo2`, `Dcc`, and
`Unc5d` all had zero focal DEGs.

I therefore predict no gene crossing FDR 0.05 for the held-out `Epha7`
perturbation. The call is driven mainly by the focal training data: seven of
eight visible Eph receptor analogs were exactly zero and the eighth was
self-transcript only. External biology makes a high count less likely because
the best-established `Epha7` neural phenotypes are wiring or dendrite phenotypes
whose strongest windows and readouts are not the P37 to P44 nuclear
transcriptome of sparse postmitotic thalamic glutamatergic knockouts.

## Limits

`Epha7` itself was held out, so no same-target expression signature or observed
focal count was available. EphA receptors are paralogous but not obligate
complex partners; transfer from `Epha4` or `Epha5` could fail if `Epha7` is more
highly expressed or has unique thalamic partners in `151 TH Prkcd Grin2c Glut`
cells. The prediction also does not rule out a real anatomical, axon-targeting,
or spine phenotype, because those endpoints are absent from the declared inputs
and can occur with little change in survivor nuclear RNA. Finally, a self-row
effect is possible for `Epha7`, as seen for `Epha4`; I left the integer
prediction at zero because most related receptors did not even show their own
target transcript as an FDR-significant row in the focal class.

