# Zbtb24 DEG-count prediction

## Question and endpoint alignment

I interpreted the task as a scalar prediction for one held-out perturbation,
`Zbtb24`, in `151 TH Prkcd Grin2c Glut` thalamic glutamatergic neurons.
The requested endpoint is:

`n_degs = count(measured genes with pvals_adj < 0.05)`

using the supplied Wilcoxon/BH differential-expression contrasts of perturbed
versus matched non-targeting controls. The held-out `Zbtb24` perturbation was
absent both as a `gene_target` in
`training_de_all_cell_groups.parquet` and as a `target_name` in
`151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`, so the endpoint is absent
for `Zbtb24` itself. The training CSV is direct endpoint evidence for visible
perturbations in the focal cell class; the parquet is direct per-gene DE
evidence for those same visible perturbations. The July
`perturbai-july-260713-sourceguard-1773-v1` same-experiment Findings ledger was
used only as a packaged interpretation of this experiment, not as independent
replication.

The main ambiguity I resolved was how far to transfer from other zinc-finger
BTB-domain genes. I did not treat all `Zbtb*` knockouts as equivalent. ZBTB24
is a DNA-binding activator of the ICF-syndrome `CDCA7` gene and acts upstream
of the CDCA7/HELLS heterochromatin and DNA-methylation pathway, whereas the
large in-dataset `Zbtb7a` response has a different LRF/glycolysis and
endomembrane profile.

## Sources

- Declared training endpoint CSV:
  `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`
- Declared DE parquet:
  `training differential-expression dataset`
- Requested held-out CSV:
  `single-target request for Zbtb24`
- Same-experiment internal corpus:
  July Findings ledger, release `perturbai-july-260713-sourceguard-1773-v1`,
  queried through `corpus.findings` and `corpus.calibration`.
- External mechanism papers:
  de Greef et al. 2011, doi:10.1016/j.ajhg.2011.04.018, PMID:21596365;
  Wu et al. 2016, doi:10.1093/hmg/ddw243, PMID:27466202;
  Aktar et al. 2019, doi:10.1111/gtc.12723, PMID:31561277;
  Hardikar et al. 2020, doi:10.1007/s13238-019-00682-w, PMID:31970665;
  Unoki et al. 2020, doi:10.1038/s41598-020-74636-2, PMID:33082427;
  Lavery et al. 2020, doi:10.7554/eLife.52981, PMID:32159514.

## Quantitative calibration

The focal training count table contains 1,674 visible biological perturbations.
The endpoint is zero-inflated: 1,205 perturbations, 72.0%, had
`n_degs = 0`; the median was 0; the 75th percentile was 1; the 90th percentile
was 2; the 95th percentile was 18; and the maximum was 2,677. Thus any
positive prediction above a few genes requires either a close measured analog
or a strong reason to extrapolate to one of the rare broad-response classes.

I then filtered the declared parquet to
`group_name == "151 TH Prkcd Grin2c Glut"` and visible perturbations that were
mechanistically plausible comparators: all visible `Zbtb*` targets, DNA
methylation/readers, and selected chromatin regulators. Counts below are the
direct focal-cell FDR<0.05 counts from the training CSV, and top marker
directions are from the focal-cell parquet:

| training perturbation | focal `n_degs` | focal expression pattern relevant to `Zbtb24` |
| --- | ---: | --- |
| `Zbtb16` | 0 | no FDR<0.05 genes |
| `Zbtb20` | 0 | no FDR<0.05 genes |
| `Zbtb10` | 0 | no FDR<0.05 genes |
| `Zbtb21` | 0 | no FDR<0.05 genes |
| `Zbtb38` | 1 | only `Msra` up |
| `Zbtb18` | 5 | a small up-only `Endou`, `Pxdn`, `Clstn2`, `Man2a2`, `Zbtb18` signature |
| `Zbtb7a` | 841 | broad, mixed response with `Pnma3`, `Col9a3`, `Gpc1`, `Usp11`, `Sema4a`, `Fhl1`, `Vgf`, and trafficking/neurosecretory genes |
| `Dnmt3a` | 0 | no FDR<0.05 genes |
| `Mbd2` | 0 | no FDR<0.05 genes |
| `Mbd5` | 0 | no FDR<0.05 genes |
| `Mecp2` | 16 | small mixed channel/adhesion signature led by `Nap1l5`, `Ache`, `Focad`, `Tnr`, `Ptprm`, `Fxyd7` |

As counterexamples showing that the focal cell group can detect nuclear
chromatin perturbations, `Chd4`, `Chd8`, `Kmt2a`, `Setdb1`, and `Setd1a`
produced 100, 61, 24, 22, and 368 focal DEGs, respectively. Their signatures
were not close endpoint analogs. `Setd1a` mainly lowered mitochondrial,
GPI-anchor, ER/Golgi, ciliary, and lysosomal transcripts; `Chd4` mixed
thalamic channel, extracellular-matrix, adhesion, and metabolic genes; and
`Zbtb7a` was dominated by endomembrane/lysosomal and peptidergic components.
The FDR<0.05 overlap between `Zbtb18` and `Zbtb7a` was only 3 genes, while
`Zbtb18` overlapped neither `Setd1a` nor `Mecp2`, and `Dnmt3a` overlapped none
of these because it was flat. The same-experiment Findings ledger makes the
same point for the represented analogs: `Zbtb7a` and `Zbtb18` partially
converged on `Pxdn`, `Clstn2`, and `Man2a2`, but `Zbtb7a` had a much broader
surface; `Zbtb16` and `Zbtb20` were flat; and acute P16 `Dnmt3a` loss had no
downstream FDR response in measured neuronal classes.

The parquet read used direct Arrow filtering rather than materializing the
whole 616M-row file:

```python
expr = (
    ds.field("group_name") == "151 TH Prkcd Grin2c Glut"
) & ds.field("gene_target").isin(targets)
table = dataset.to_table(
    columns=["names", "scores", "logfoldchanges", "pvals_adj",
             "gene_target", "n_pert_matched", "n_ctrl_matched"],
    filter=expr,
)
```

## Target-specific prediction

### `Zbtb24`

`Zbtb24` is predicted to have `0` FDR<0.05 genes.

External biology gives `Zbtb24` a real chromatin role rather than a generic
null prior. Recessive `ZBTB24` mutations cause ICF type 2 with juxtacentromeric
hypomethylation, showing that ZBTB24 is tied to heterochromatin methylation
(de Greef et al. 2011). Mechanistically, ZBTB24 directly activates `CDCA7`;
loss of Zbtb24 in mouse embryonic stem cells down-regulates `Cdca7`, and
human/mouse ZBTB24 zinc-finger motifs are required for `CDCA7` promoter
activation (Wu et al. 2016; Aktar et al. 2019). CDCA7 in turn works with the
SNF2-like remodeler HELLS to support DNA methylation at heterochromatic repeat
classes and to suppress DNA:RNA hybrid-associated damage at pericentromeric
repeats (Hardikar et al. 2020; Unoki et al. 2020).

The causal chain for transfer to this P16 mosaic Perturb-seq endpoint is:

`Zbtb24` loss -> less CDCA7 activity -> weaker CDCA7/HELLS remodeling at
selected heterochromatic repeats -> altered methylation/repeat regulation or
repair stress -> any neuron-autonomous survivor-state RNA response at P37-44.

The weakest links are in the last two steps. The strongest published ZBTB24
phenotypes are developmental, lymphoid, embryonic-stem-cell, or repeat
methylation phenotypes, not an immediate broad mRNA program in postmitotic
thalamic neurons. The screen perturbation is sparse acute CRISPR delivered at
P16 and read 3-4 weeks later, with only partial average target-RNA reduction;
it cannot be assumed to erase pre-existing methylation. The most relevant
visible methylation writer, `Dnmt3a`, had zero focal DEGs and zero downstream
FDR<0.10 genes across the July same-experiment reports, despite conditional
`Dnmt3a` loss being able to reshape neuronal non-CG methylation when imposed
early and densely (Lavery et al. 2020). The represented methylation readers
`Mbd2` and `Mbd5` were also flat in the focal count table. That makes the
DNMT/methylation arm a same-experiment counterexample to extrapolating from an
essential developmental methylation factor to a visible acute RNA response.

The visible ZBTB family was not a positive reason to inflate the count.
`Zbtb16`, `Zbtb20`, `Zbtb10`, and `Zbtb21` were exactly zero in the focal
class; `Zbtb38` had one DEG; and `Zbtb18` had only five. `Zbtb7a` was a
counterexample with 841 DEGs, but its focal program contained glycolytic,
lysosomal, GPCR-sorting, synaptic, and peptidergic genes and was dataset-nearest
to UFMylation/proteostasis perturbations rather than to other ZBTB factors.
Because ZBTB24 is tied instead to a CDCA7/HELLS pericentromeric-methylation
axis, `Zbtb7a` is evidence that thalamic neurons can respond strongly to a
particular BTB zinc-finger loss, not evidence that `Zbtb24` should have a broad
response.

I therefore anchored the point estimate at the modal and mechanistically
supported outcome, `0`, rather than at the sparse `Zbtb18` value of 5 or the
chromatin-factor upper tail. The decision is driven mainly by within-dataset
endpoint evidence: the closest visible ZBTB and methylation analogs are zero
or single-digit perturbations. External ZBTB24/CDCA7/HELLS knowledge was used
to choose those analogs and to reject transfer from the broad but biologically
distant `Zbtb7a`, `Setd1a`, and `Chd4` responses.

## Limits

This is an extrapolation. `CDCA7`, `HELLS`, `UHRF1`, `DNMT1`, `PARP1`,
`XRCC4`, and `LIG4` were not visible in the focal training count table, so the
closest biochemical branch of the ZBTB24 pathway was only indirectly tested by
`Dnmt3a` and methyl-CpG readers. The parquet has no raw indel calls, direct DNA
methylation, pericentromeric repeat RNA quantification optimized for repetitive
sequence mapping, repair-stress assays, or pre-assay survival denominators.
A quiet recovered signature could miss early death or subtle heterochromatin
changes. Conversely, the single-cell Wilcoxon endpoint is power-sensitive; a
small `Zbtb24` response of a few genes would be easy to miss with this
target-analog transfer. The integer 0 should therefore be read as a prediction
that no gene crosses the assay's whole-transcriptome FDR 0.05 threshold, not
as a claim that ZBTB24 is irrelevant in neurons.
