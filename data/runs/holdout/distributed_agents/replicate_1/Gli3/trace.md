# Held-out DEG-count prediction trace

## Question and endpoint

The requested prediction is the number of FDR-significant genes that an acute
AAV-PHP.eB CRISPR loss-of-function perturbation of each held-out target would
produce in the focal `151 TH Prkcd Grin2c Glut` thalamic glutamatergic class.
The endpoint is `n_degs`: the count of measured genes with Wilcoxon
Benjamini-Hochberg adjusted `pvals_adj < 0.05` in the focal class.

The requested-target manifest contains one held-out perturbation:

| target | predicted count |
|---|---:|
| Gli3 | 0 |

I treated `151 TH Prkcd Grin2c Glut` as an Allen taxonomy label for thalamic
glutamatergic neurons, with `TH` meaning thalamus, not tyrosine hydroxylase.
The held-out `Gli3` perturbation itself is absent from both supplied training
inputs, so all numerical evidence below comes from non-held-out perturbations.
The training DEG-count CSV is a direct observation of the endpoint for those
perturbations; the all-cell differential-expression Parquet is the underlying
same-experiment DE surface for inspecting their focal signatures. The selected
PerturbAI July same-experiment corpus was used only as curated interpretation
of those same training perturbations, not as independent replication.

## Sources

- Training endpoint:
  `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
- Training differential-expression rows:
  `training differential-expression dataset`.
- Requested held-out targets:
  `single-target request for Gli3`.
- Same-experiment internal corpus:
  `perturbai-july-260713-sourceguard-1773-v1`, queried through the run-declared
  `corpus.findings` ledger for `Gli1`, `Gli2`, `Smo`, `Gpr161`, and `Cdon`.
- External biology was checked with PubMed-indexed literature, especially:
  Persson et al. 2002, Genes & Development, DOI `10.1101/gad.243402`,
  PubMed `12435629`; Jacob and Briscoe 2003, EMBO Reports, DOI
  `10.1038/sj.embor.embor896`, PubMed `12897799`; Hwang and Mukhopadhyay
  2014, Birth Defects Research Part A, DOI `10.1002/bdra.23267`, PubMed
  `24917297`; Balaskas et al. 2012, Cell, DOI `10.1016/j.cell.2011.10.047`,
  PubMed `22265416`; Zhang et al. 2017, Molecular and Cellular Biology, DOI
  `10.1128/MCB.00421-16`, PubMed `27849569`; Shimada et al. 2019,
  Developmental Biology, DOI `10.1016/j.ydbio.2019.03.011`, PubMed `30914320`;
  Constable et al. 2020, Development, DOI `10.1242/dev.183301`, PubMed
  `31964774`.

## Computation over the supplied data

I first read the held-out manifest and confirmed that it contains only
`Gli3`, and read the focal training count table to identify Hedgehog/Gli
comparators that were assayed in the non-held-out set. The focal endpoint is
zero-inflated: among 1,674 training perturbations, 469 have nonzero `n_degs`,
the median is 0, the 75th percentile is 1, the 90th percentile is 2, and the
95th percentile is 18.

The direct Hedgehog pathway perturbations visible in the training endpoint all
had no focal response:

| training perturbation | focal `n_degs` | focal DE support |
|---|---:|---|
| Gli1 | 0 | 17,259 measured genes; minimum adjusted p = 1.0 |
| Gli2 | 0 | 17,259 measured genes; minimum adjusted p = 1.0 |
| Smo | 0 | 17,259 measured genes; minimum adjusted p = 1.0 |
| Ptch1 | 0 | 17,259 measured genes; minimum adjusted p = 1.0 |
| Ptch2 | 0 | 17,259 measured genes; minimum adjusted p = 1.0 |
| Gpr161 | 0 | 17,259 measured genes; minimum adjusted p = 1.0 |
| Cdon | 0 | 17,259 measured genes; minimum adjusted p = 1.0 |
| Ift88 | 0 | 17,259 measured genes; minimum adjusted p = 1.0 |

The Parquet rows behind these eight focal signatures were filtered to
`group_name == "151 TH Prkcd Grin2c Glut"` and the listed `gene_target` values,
then summarized by `gene_target`; no gene passed FDR 0.05 for any of them.
Their smallest nominal p-values were also modest after a 17,259-gene
multiple-test correction. For example, the smallest raw p-values were
`0.000396` for `Gli1`, `0.000249` for `Gli2`, `0.000468` for `Smo`,
`0.000562` for `Ptch1`, `0.000429` for `Ptch2`, `0.000476` for `Gpr161`,
`0.000114` for `Cdon`, and `0.000159` for `Ift88`; the adjusted values were
all 1.0. This made the local baseline for a core Hedgehog/Gli factor a true
near-origin signature rather than a borderline one- or two-gene effect.

As broader developmental transcription-factor counterexamples, `Zic1` produced
only 2 focal DEGs, while `Zic2`, `Zic3`, `Zic4`, `Sall1`, and `Sall4` produced
0 focal DEGs. Those genes are not direct functional substitutes for `Gli3`, but
they put the Hedgehog result in context: embryonic patterning factors need not
produce a large transcriptional footprint when hit sparsely at P16 in
postmitotic neurons.

## Target-specific reasoning

### Gli3

**Biological role.** `Gli3` encodes a bifunctional zinc-finger Hedgehog
effector. In the absence of Hedgehog pathway activation, ciliary/PKA-dependent
processing generates GLI3 repressor; after Smoothened activation, the balance
shifts toward GLI activator output from GLI2/GLI3 and transcriptional induction
of feedback genes such as `Gli1`, `Ptch1`, `Ptch2`, and `Hhip`. `Gli3`
repressor is central during embryonic neural-tube, forebrain, and limb
patterning (Persson et al. 2002; Jacob and Briscoe 2003), and ciliary
regulators such as `Gpr161`, `Smo`, `Sufu`, and `Inpp5e` act through the GLI
activator/repressor balance (Hwang and Mukhopadhyay 2014; Zhang et al. 2017;
Constable et al. 2020).

**Causal transfer model.** The requested intervention is P16 sparse mosaic
CRISPR indel formation in neurons, followed by 3-4 weeks of propagation and a
P37-P44 survivor-conditioned nuclear RNA readout. For `Gli3` to yield many
focal DEGs, loss of GLI3 protein in these postmitotic thalamic glutamatergic
neurons would need to remove a limiting GLI3 repressor state or blunt an
ongoing GLI3 activator state; the cell would then need an intact postnatal
Ptch/Smo/cilium/Sufu/Gli transcriptional circuit; the shifted GLI balance
would need to move many nuclear transcripts in recovered cells strongly enough
to pass BH correction.

The best same-experiment analogs probe several points in that chain:

- `Gpr161`, 0 focal DEGs, is a same-direction derepression analog in cilia:
  GPR161 raises ciliary cAMP and promotes GLI3 repressor processing. Its loss
  should relieve GLI repression in embryonic Hh-responsive cells, yet it
  produced no corrected focal genes and the curated PerturbAI report concluded
  that the expected `Gli1`/`Ptch`/`Hhip` induction was uncoupled in sampled
  postnatal neurons.
- `Ptch1` and `Ptch2`, each 0 focal DEGs, are also Hh-derepression analogs
  upstream of `Smo`; loss of a ligand receptor should de-repress Smoothened if
  the focal cells maintain an active canonical pathway. Their complete focal
  silence argues against a receptor-level Hedgehog feedback program.
- `Smo`, 0 focal DEGs, tests the opposite side of the pathway. SMO is the
  obligate canonical transducer downstream of Patched; if ongoing Hh input
  maintained a GLI transcriptional state in this focal class, acute `Smo` loss
  should decrease Hh-on feedback transcripts. The same-experiment `Smo` report
  instead found no canonical GLI target repression across recovered neuronal
  classes.
- `Gli1` and `Gli2`, each 0 focal DEGs, are the closest assayed GLI
  transcription-factor perturbations. `Gli1` is a Hh-induced amplifier and
  `Gli2` carries much of the initial activator burden in responsive cells.
  Neither produced any focal FDR 0.05 signature, and the `Gli2` report
  specifically found no movement of the Hh feedback reporters `Gli1`, `Ptch1`,
  `Ptch2`, or `Hhip`.
- `Cdon`, 0 focal DEGs, and `Ift88`, 0 focal DEGs, are less direct but useful
  counterpoints. `Cdon` is a Hh co-receptor used during ligand-dependent
  developmental signaling, and `Ift88` participates in ciliary trafficking
  required for vertebrate Hh transduction. Neither revealed a focal Hh-like
  response.

This chain points to a zero rather than a low positive prediction. The causal
break is not that `Gli3` is biologically irrelevant: GLI3 loss can strongly
alter embryonic morphogen interpretation. The break is that the susceptible
stage and cell state are absent from this experiment. `151 TH Prkcd Grin2c
Glut` is a recovered postmitotic neuronal class, the perturbation is acute and
mosaic after birth, and every represented direct Hh/Gli intervention in the
same focal class is at the FDR origin. A sparse single-gene or noise-level
signature remains possible, but the closest observed counts are all exactly
zero and none of their focal p-value distributions had a near-threshold BH
candidate.

**Prediction: `Gli3 -> 0` DEGs.** The prediction is driven primarily by the
within-dataset zeros for core Hedgehog/Gli comparators and supported by
external developmental Hh literature that places strong `Gli3` requirements in
embryonic progenitor patterning rather than acute transcriptional maintenance
of P16-perturbed thalamic neurons.

## Limits

The held-out `Gli3` signature and count are absent by construction. `Sufu`,
`Shh`, `Kif7`, `Boc`, and `Gas1` were also not focal training targets, so the
analogy uses the represented pathway nodes `Gli1`, `Gli2`, `Smo`, `Ptch1`,
`Ptch2`, `Gpr161`, `Cdon`, and `Ift88` rather than a complete Hh perturbation
panel. All same-experiment corpus records are interpretations of the same
Perturb-seq dataset, not external replication. The Parquet contains
differential-expression summaries, not raw UMI counts, indel genotypes, GLI3
protein, GLI3 repressor/activator isoforms, ciliary localization, or cells lost
before sorting; severe selection before nuclear recovery could therefore be
missed. The external literature is dominated by embryonic and progenitor
systems, so it supports the stage-specific causal boundary more strongly than
it provides a direct adult-thalamus measurement.
