# Reasoning trace

## Question and resolved endpoint

The requested endpoint is a point prediction of `n_degs` for each held-out
genetic perturbation in `151 TH Prkcd Grin2c Glut`, where `n_degs` means the
number of measured genes whose Wilcoxon Benjamini-Hochberg adjusted p value is
below 0.05 in perturbed versus matched control nuclei. In this run the requested
CSV contains one target, `Tspan12`. `Tspan12` is absent as a `gene_target` in
the supplied differential-expression Parquet and absent from the focal training
count table, so the exact endpoint is not directly observed and has to be
transferred from non-held-out perturbations.

I treated the DEG-count training CSV as the direct endpoint for visible
perturbations and the Parquet as the expression-signature substrate. I did not
use target self-RNA loss as an editing-efficiency filter, because the atlas
metadata explicitly warns that self transcript loss is not a quantitative
measure of functional knockout strength in this pooled mosaic CRISPR design.

## Sources

- Declared Perturb-seq inputs:
  `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`
  and
  `training differential-expression dataset`.
- Run-local metadata: `task_bindings.json`, `coverage.json`,
  `capabilities.json`, and `measurement_registry.json` under
  `codex_runtime/pipeline`.
- Internal same-experiment corpus:
  `perturbai-july-260713-sourceguard-1773-v1`, queried through
  `corpus.findings`, `corpus.calibration`, and `corpus.report_evidence`.
  This corpus is packaged interpretation of the same screen, not independent
  replication.
- External biology: PubMed-indexed Norrin/FZD4/LRP5/LRP6/TSPAN12 papers,
  especially Ye et al. 2009, DOI 10.1016/j.cell.2009.07.047; Junge et al.
  2009, PMID 19837033, DOI 10.1016/j.cell.2009.07.048; Zhang et al. 2018,
  PMID 30354230, DOI 10.1161/ATVBAHA.118.311689; Panagiotou et al. 2017,
  PMID 28575650, DOI 10.1016/j.ajhg.2017.05.001; MacDonald and He 2012,
  PMID 23209147, DOI 10.1101/cshperspect.a007880; and Ren et al. 2021,
  PMID 34026761, DOI 10.3389/fcell.2021.670960.

## Quantitative checks

The focal training table contained 1,674 non-held-out perturbations; 1,205 had
zero DEGs and the median `n_degs` was 0, showing that a null point estimate is
common in this assay/cell-group combination. I then filtered the Parquet to
`group_name == "151 TH Prkcd Grin2c Glut"` and to candidate analog targets, and
counted `pvals_adj < 0.05` among the 17,259 measured genes for each target.

The relevant training perturbations and exact focal DEG counts were:

| perturbation | observed `n_degs` in 151 | expression evidence and role |
| --- | ---: | --- |
| `Fzd4` | 0 | Closest represented receptor for TSPAN12 biology. The focal profile had 188 perturbed nuclei, no FDR 0.05 DEG, and no movement of canonical Wnt feedback genes (`Axin2` logFC 0.187, `Lef1` 0.069, both FDR 1). The same-experiment FZD4 report also found 0 downstream FDR 0.10 genes in all 22 measured neuronal groups. |
| `Lrp5` | 0 | Norrin/FZD4 co-receptor and an FEVR gene. It had 0 focal DEGs and no `Axin2`/`Lef1` response (`Axin2` logFC 0.325 FDR 1; `Lef1` 0.030 FDR 1). |
| `Lrp6` | 4 | Canonical Wnt co-receptor and a positive control for receptor-level Wnt input in the cell group. It yielded only a small 151 response: `Nrbp2`, `Nsmf`, and `Atrnl1` down and `Chgb` up at FDR 0.05; `Axin2` was down but missed this task's cutoff. |
| `Ctnnb1` | 383 | Intracellular beta-catenin effector. It was a broad downstream counterexample with depressed `Axin2`, `Lef1`, `Vangl1`, `Wnt9b`, and many thalamic excitability/adhesion genes, demonstrating that the focal cell group can report beta-catenin/TCF loss when the perturbation hits a postmitotic neuronal effector. |
| `Tcf7l2` | 106 | Downstream transcription factor in the thalamic beta-catenin program. It confirms that parts of the pathway are transcriptionally visible, but its broad response is not expected from a ligand-selective endothelial Norrin co-receptor. |
| `Fzd2`, `Fzd6`, `Fzd9` | 0, 0, 0 | Frizzled receptor paralogs represented in training. None produced any focal DEG or any canonical Wnt feedback response. |
| `Ror1`, `Ror2`, `Ryk` | 0, 0, 0 | Alternative Wnt receptors checked in the same focal query. They were all flat, arguing against receptor-family membership alone as a predictor of a broad thalamic signature. |
| `Tspan7`, `Cd81` | 1, 1 | The available tetraspanin-family perturbations were essentially buffered in 151, each with only its own transcript significant. `Tspan7` also lacked a broad response across the same-experiment corpus despite known neuronal AMPAR/PICK1 biology. |

## Biological transfer to `Tspan12`

TSPAN12 is not a general Wnt receptor subunit. It is a ligand-selective
tetraspanin enhancer of Norrin-induced FZD4/beta-catenin signaling: Junge et al.
showed that Tspan12 loss phenocopies Norrin/Fzd4/Lrp5 retinal vascular defects
and that TSPAN12 potentiates Norrin-FZD4 signaling rather than Wnt3A signaling.
Ye et al. identified the Norrin-FZD4-LRP5 endothelial genetic program required
for retinal vascularization, and Zhang et al. localized an adult retinal
TSPAN12 requirement to endothelial blood-retina barrier maintenance. The
intervention chain for the screen is therefore:

`Tspan12` CRISPR in a recovered NeuN+ thalamic neuron -> loss of a
Norrin-specific FZD4/LRP5/6 co-receptor, if the complex is expressed in that
neuron -> altered beta-catenin/TCF transcription -> focal snRNA DEGs.

The weak link is the middle of that chain. The experiment largely excludes the
endothelial cells in which the Norrin/FZD4/TSPAN12 pathway is best established,
and the actual receptor-level analogs that are present in neurons do not
produce a focal response: `Fzd4`, the receptor that TSPAN12 potentiates, is
flat in `151 TH Prkcd Grin2c Glut`; `Lrp5`, the Norrin pathway co-receptor most
closely tied to retinal vascularization and FEVR, is flat; and the single
`Lrp6` edge response is much smaller than downstream `Ctnnb1` or `Tcf7l2`.
The reported FZD4 corpus finding explicitly checked the same branch and found
that `Fzd4`, `Fzd2`, `Fzd6`, `Fzd9`, and `Lrp5` did not converge with the
detectable `Ctnnb1`/`Lrp6` thalamic state.

I therefore used `Fzd4=0` and `Lrp5=0` as the highest-weight within-dataset
analogs, with `Lrp6=4` as an upper receptor-level counterexample and
`Ctnnb1=383`/`Tcf7l2=106` as evidence that the downstream beta-catenin machinery
is visible only when it is directly engaged. TSPAN12 acts upstream of FZD4 in a
more specialized ligand context than LRP6, so it should not exceed LRP6 in this
postnatal neuronal assay and is expected to behave like the null FZD4/Norrin
receptor surface.

Predicted `Tspan12` count: 0 DEGs.

## Limits

The prediction is extrapolative because `Tspan12` and `Ndp` were not available
as perturbation targets in the training Parquet. The Parquet proves that
`Tspan12` transcript itself was in the measured-gene universe for the analog
queries, but it does not provide raw single-nucleus expression or protein
abundance of TSPAN12, Norrin, FZD4, or LRP5 in `151 TH Prkcd Grin2c Glut`.
The closest biology comes from retinal and vascular endothelial systems rather
than juvenile thalamic neurons. That context mismatch lowers confidence but,
because the represented neuronal `Fzd4` and `Lrp5` perturbations were directly
observed and flat, it points toward a focal zero rather than toward a hidden
broad neuronal DEG response.
