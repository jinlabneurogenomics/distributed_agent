# Holdout DEG-count prediction for 151 TH Prkcd Grin2c Glut

## Question and endpoint

I interpreted the task as a scalar holdout prediction: for each requested genetic
perturbation, predict the integer number of genes that would pass
Benjamini-Hochberg FDR 0.05 in `151 TH Prkcd Grin2c Glut` after acute P16 AAV
CRISPR loss of function and P37-P44 single-nucleus RNA-seq. The requested
manifest contained one held-out target, `Tef`. Its own DEG count and differential
expression rows were absent from the supplied training files, so I treated the
training endpoint as directly observed for non-held-out perturbations and absent
for `Tef`.

`n_degs` is an assay- and power-dependent width of the recovered nuclear
transcriptional response. I counted the target transcript itself if it passed
FDR, because the training CSV is defined as all measured genes with
`pvals_adj < 0.05`; I did not use self-RNA depletion as evidence of editing
success or failure.

## Sources

- Declared differential-expression table:
  `training differential-expression dataset`.
- Declared focal training counts:
  `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
- Declared held-out manifest:
  `single-target request for Tef`.
- Run-local task bindings, compact coverage, measurement registry, and
  capability manifest in `codex_runtime/pipeline`.
- The internal same-experiment July PerturbAI sourceguard corpus release
  `perturbai-july-260713-sourceguard-1773-v1`, queried through its Findings
  ledger for `Bmal1`, `Clock`, `Nr1d1`, `Rora`, `Rorc`, and `Tef`.
- External PubMed-indexed literature:
  - Gachon et al. 2004, *Genes & Development*, DOI 10.1101/gad.301404, PMID
    15175240.
  - Takahashi 2016, *Nature Reviews Genetics*, DOI 10.1038/nrg.2016.150, PMID
    27990019.

## Quantitative calibration

The held-out target list contained only `Tef`. In the focal training CSV there
were 1,674 measured training targets. The response-breadth distribution was
zero-heavy: median 0, 75th percentile 1, 90th percentile 2, 95th percentile 18,
mean 14.1, and maximum 2,677.

The direct PAR bZIP paralogs `Dbp` and `Hlf` were not present as training
perturbations in this fold, so I could not use a one-hop paralog DEG count.
I therefore inspected the nearest represented clock and ROR/REV-ERB regulators
in the focal cell group by filtering the Parquet to
`group_name = '151 TH Prkcd Grin2c Glut'` and to ten biologically relevant
targets: `Bmal1`, `Bmal2`, `Clock`, `Cry1`, `Cry2`, `Nr1d1`, `Nr1d2`, `Rora`,
`Rorb`, and `Rorc`. That returned 172,590 raw measured-gene rows, exactly
17,259 genes for each target. Recounting `pvals_adj < 0.05` in these rows
matched the training CSV:

| training perturbation | focal n_degs | relevant 151 expression evidence |
| --- | ---: | --- |
| `Rora` | 278 | Broad down-dominant thalamic terminal/synaptic program, with `Prkcg`, `Adgrb1`, `Rasa4`, `Pcp4`, `Car4`, `Kcnc2`, `Erc2`, `Cry2`, and `Nr1d1` significant. |
| `Nr1d1` | 116 | REV-ERBalpha loss de-repressed an expected clock-output branch: `Dbp` +0.407 log2FC, `Nfil3` +0.752, `Ciart` +0.595, `Cry2` +0.375, `Npas2` +0.606; `Tef`, `Hlf`, and `Pdxk` were not FDR hits. |
| `Bmal1` | 103 | Positive clock-limb loss strongly decreased `Dbp`, `Nr1d2`, `Nr1d1`, and `Per3` and increased `Npas2` and `Cry1`, but measured `Tef` was not significant. |
| `Clock` | 3 | A very narrow activator-limb signature: `Dbp` -1.03, `Nr1d2` -0.378, and `Tef` -0.518 were the only FDR 0.05 hits. |
| `Cry2` | 3 | Tiny response: significant `Cry2`, `Nr1d1`, and `Dbp` decreases; `Tef` was not significant. |
| `Cry1` | 1 | Only `Per2` passed FDR 0.05. |
| `Nr1d2` | 1 | Only `Nr1d1` passed FDR 0.05. |
| `Rorb` | 0 | No focal DEGs. |
| `Rorc` | 0 | No focal DEGs. |
| `Bmal2` | 0 | No focal DEGs. |

Two corpus checks were useful. First, the same-experiment Findings for `Clock`
and `Bmal1` report that the expected CLOCK/BMAL1 E-box output was recovered:
`Clock` depressed the tiny `Nr1d2`/`Dbp`/`Tef` module, while `Bmal1` produced a
larger 151-dominant clock plus synaptic/adhesion response. Second, the Findings
for `Rora`, `Nr1d1`, and `Rorc` warn against family-name transfer: `Rora` and
`Nr1d1` are strong in 151, but `Nr1d2`, `Rorb`, `Rorc`, `Cry1`, and `Cry2` are
mostly buffered as single perturbations, and `Rora`'s broad thalamic program is
Rora-selective rather than a generic ROR or circadian signature. The corpus had
no `Tef` Finding, as expected for a held-out perturbation.

## Target-specific reasoning

### Tef

`Tef` encodes thyrotroph embryonic factor, one of the three mammalian PAR bZIP
transcription factors together with `Dbp` and `Hlf`. These are D-box-binding
clock-output activators, not the shared positive oscillator limb itself.
Gachon et al. showed that combined `Dbp`/`Hlf`/`Tef` loss in mouse causes severe
spontaneous and audiogenic epilepsy and identified brain `Pdxk` reduction as one
downstream consequence, supporting a neuronal role for the family. That study
also makes the redundancy problem explicit: the strong phenotype is from
removing all three PAR bZIP factors. Takahashi's review places this family below
the CLOCK/BMAL1 and REV-ERB/ROR loops, whose upstream perturbations can shift
`Dbp`, `Tef`, `Nr1d1`, `Nr1d2`, and related circadian transcripts.

The causal transfer model is:

`Tef` CRISPR loss -> reduced TEF D-box activation at susceptible output genes
-> compensation by remaining DBP/HLF and intact upstream clock feedback in most
postmitotic neurons -> little or no propagated shift in thalamic identity,
synaptic, or survival state -> recovered 151 nuclei have few FDR-level DEGs.

The within-dataset evidence fits that model. `Clock` perturbation proves that
`Tef` mRNA is a clock-responsive transcript in these thalamic cells because
`Tef` itself falls by -0.52 log2FC at FDR 0.00054, but `Clock` still produces
only three total FDR hits. That is the closest measured sign for `Tef` as a
downstream output. In contrast, `Bmal1` and `Nr1d1` broaden to 103 and 116 DEGs
because they perturb central feedback nodes and recruit `Erc2`/`Pdgfa`/adhesion
modules; a single `Tef` knockout should not phenocopy those feedback effects.
`Rora` is an even poorer count analog despite sharing clock-adjacent logic:
its 278 DEGs are dominated by a Rora-selective thalamic terminal program
(`Prkcg`, `Pcp4`, `Car4`, `Kcnc2`, `Adgrb1`) and ROR paralogs are flat
(`Rorb`, `Rorc`, `Bmal2`: 0). The low observed counts for `Clock`, `Cry1`,
`Cry2`, and `Nr1d2` also show that pathway membership alone is insufficient to
create a broad 151 response in this sparse acute CRISPR assay.

I therefore predicted a true null or noise-scale response rather than a
Rora/Nr1d1/Bmal1-sized program. I assigned `Tef` to 0 DEGs: nonzero is possible
from a self-transcript hit or a small `Dbp`/`Pdxk`/clock-output shift, but the
best point prediction is below the FDR detection boundary in this fold.

## Limits and uncertainty

- The ideal analogs, `Dbp` and `Hlf`, were not present as training
  perturbations, so the prediction extrapolates from upstream core-clock and
  ROR/REV-ERB perturbations.
- The clock genes were assayed at one terminal time window, not as a circadian
  time course. A small log-fold change can mix mean expression changes with
  phase effects.
- The Parquet and the July Findings corpus are representations of the same
  Perturb-seq experiment; their agreement calibrates interpretation but is not
  independent replication.
- Published PAR bZIP knockout phenotypes are stronger than this assay's acute,
  sparse, mosaic single-gene perturbation because they often remove multiple
  family members. I treated the cross-gene redundancy as a reason to downgrade
  single-`Tef` transfer.
- FDR-level zero is not a proof of no biology. It means the predicted response
  is too weak, too redundant, or too survivor-conditioned to yield a measured
  DEG at BH-adjusted Wilcoxon FDR 0.05 in this focal class.
