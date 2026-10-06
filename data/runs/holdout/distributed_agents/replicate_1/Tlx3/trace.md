# DEG-count prediction for `151 TH Prkcd Grin2c Glut`

## Question and endpoint

I interpreted the task as a scalar holdout prediction for the number of genes that
would pass Benjamini-Hochberg FDR 0.05 after acute AAV-CRISPR loss of `Tlx3` in
the `151 TH Prkcd Grin2c Glut` thalamic glutamatergic cell group.  The requested
row was fully held out, so the `Tlx3` DEG count and `Tlx3` perturbation signature
are absent from the supplied training-count CSV and the DE Parquet.  Counts from
the training CSV are direct observations of the requested endpoint for
non-held-out perturbations; Parquet signatures are direct observations for those
same training perturbations; external literature is only a prior on whether any
training perturbation is an appropriate surrogate.

The held-out manifest contained one target and no ranking semantics:

```tsv
target_name
Tlx3
```

## Sources used

- Declared input endpoint table:
  `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
- Declared input DE table:
  `training differential-expression dataset`.
- Run-local metadata: `task_bindings.json`, `coverage.json`,
  `measurement_registry.json`, and the PerturbAI atlas dataset portrait in
  `dataset_context.md`.
- Internal same-experiment semantic corpus:
  `perturbai-july-260713-sourceguard-1773-v1`; I used its bounded Findings and
  Evidence entries for the measured `Lbx1`, `Gata3`, and `Tcf7l2` training
  perturbations as packaged interpretation of the same PerturbAI experiment,
  not as independent replication.
- NCBI PubMed E-utilities literature searches, 2026-09-03, for the external
  mouse `Tlx3` developmental literature.

## Training-set calibration

The focal training table contains 1,674 non-held-out perturbations.  Its endpoint
distribution is very sparse: 1,205 perturbations have 0 DEGs, 469 have a
positive count, the median is 0, the mean is 14.05, and a small tail extends to
2,677 DEGs.  The background zero rate matters because a held-out developmental
transcription factor should not be predicted to give a broad signature unless
the experiment contains a close active analog.

I queried the Parquet only for the focal cell group and exact candidate
comparators, using DuckDB predicates equivalent to:

```sql
SELECT gene_target,
       any_value(n_pert_matched) AS n_pert_matched,
       any_value(n_ctrl_matched) AS n_ctrl_matched,
       count(*) AS measured_genes,
       sum(CASE WHEN pvals_adj < 0.05 THEN 1 ELSE 0 END) AS degs,
       min(pvals_adj) AS min_padj
FROM read_parquet('training_de_all_cell_groups.parquet')
WHERE group_name = '151 TH Prkcd Grin2c Glut'
  AND gene_target IN (...)
GROUP BY gene_target;
```

The screen did not include `Tlx1` or `Tlx2`, the two closest TLX-family analogs
to `Tlx3`, so there is no measured paralog perturbation to copy.  The represented
developmental transcription-factor neighborhood was mostly silent at FDR 0.05:

| training perturbation class | focal DEG counts |
|---|---|
| GATA family | `Gata1` 0, `Gata3` 0, `Gata4` 0, `Gata6` 0 |
| HOX family | `Hoxa1` 0, `Hoxa13` 0, `Hoxa3` 0, `Hoxb8` 0, `Hoxd10` 0, `Hoxd13` 0 |
| LIM/homeobox or dorsal/ventral fate factors | `Lbx1` 1, `Isl1` 0, `Lhx3` 0, `Lhx4` 0, `Lmx1b` 0 |
| PAX family | `Pax2` 0, `Pax3` 0, `Pax4` 0, `Pax6` 0, `Pax7` 0, `Pax8` 0 |
| Other represented neuronal TFs | `Dlx3` 0, `Dlx6` 0, `Foxp2` 0, `Otx2` 0, `Pou4f3` 0, `Sox2` 2, `Sox5` 2, `Zic1` 2 |

The closest biological comparators had these exact focal signatures:

- `Lbx1`: 177 perturbed nuclei versus 23,679 controls, 17,259 measured genes,
  exactly 1 DEG.  The only FDR 0.05 call was `Vps35l`, log2FC -0.610,
  FDR 0.043.  The July PerturbAI corpus summarizes this as a one-gene response
  in 151 and notes that represented developmental partners such as `Pax2`,
  `Pax8`, and `Phox2b` did not recreate a canonical embryonic Lbx1/Ptf1a/Pax
  dorsal-spinal module in the juvenile neuronal screen.
- `Gata3`: 220 perturbed nuclei versus 23,679 controls, 0 DEGs, minimum focal
  FDR 0.159.  In the same-experiment corpus, `Gata3` loss was almost completely
  buffered across the P16-to-P37/44 neuronal panel despite strong embryonic and
  peripheral sympathetic, raphe, and GABAergic literature priors.
- `Lmx1b`, `Pax2`, `Pax6`, `Isl1`, `Pou2f1`, `Tcf4`, `Lhx3`, `Lhx4`, `Hoxa1`,
  and `Hoxb8` each had 0 focal DEGs; their minimum adjusted p values ranged from
  0.143 to 1.000.  These are counterexamples to assigning a nonzero broad
  response solely because a gene is a developmental transcription factor.
- `Tcf7l2`: 111 perturbed nuclei versus 23,679 controls and 106 DEGs at FDR
  0.05, with top focal changes including `Ramp3` down, `Cck` up, `Spock3` down,
  `Kcnc2` down, and `Pcsk2` down.  I treated this as a counterexample rather
  than the scale estimate for `Tlx3`: the corpus shows `Tcf7l2` is a postnatal
  thalamic Wnt/TCF terminal-state regulator in this exact cell group, whereas
  the better `Tlx3` prior is dorsal-spinal glutamatergic selector activity.

As a falsification check, I searched the supplied Parquet for significant
`Tlx3` measured-gene rows across all visible perturbations.  No non-held-out
knockout moved `Tlx3` itself at FDR 0.10 in any cell group.  This is only
context--target-transcript rows are not engagement measurements in this
experiment--but it means the training signatures do not expose a visible
upstream regulator that would make `Tlx3` a shared active module member in 151.

## Target-specific reasoning

### `Tlx3`

External biology gives `Tlx3` a strong developmental role, but in a different
place and time from the held-out assay.  Cheng et al. 2004 showed that mouse
`Tlx3`/`Tlx1` act as postmitotic selector genes in the developing dorsal spinal
cord, promoting glutamatergic identity and repressing the GABAergic program;
`Tlx` mutants lost markers such as `Vglut2`/`Slc17a6` and derepressed `Pax2`,
`Gad1`, `Gad2`, and `Viaat`/`Slc32a1` (Nature Neuroscience 2004,
doi:10.1038/nn1221, PMID:15064766).  Monteiro et al. 2021 then used Tlx3
ChIP-seq and expression profiling in embryonic dorsal spinal cord and found
that TLX3 directly activates many dILB excitatory genes and directly represses
many alternative dILA inhibitory-fate genes (Frontiers in Cell and
Developmental Biology 2021, doi:10.3389/fcell.2021.642697, PMID:33996801).

The causal transfer chain from those papers to the held-out experiment is:
acute `Tlx3` loss at P16 -> loss of TLX3 selector binding -> possible erosion of
an excitatory dorsal-spinal fate program -> survival and recovery of infected
NeuN+ nuclei 3-4 weeks later -> Wilcoxon DE within broad atlas cell classes.
The chain is weak in the middle for `151 TH Prkcd Grin2c Glut`: the focal group
is thalamic, not dorsal spinal; it is juvenile and already postmitotic when
CRISPR is delivered; and the directly represented fate-regulator perturbations
with the same embryonic-selector flavor do not show a comparable thalamic
program.  `Lbx1` is the most relevant within-dataset analog because it belongs
to the same dorsal spinal developmental context, but it produced only the
isolated `Vps35l` hit in 151 rather than a neurotransmitter-fate or TLX-like
module.  `Gata3` is a second useful counterexample because its strong embryonic
neuronal and autonomic requirements failed to translate into an FDR-resolved
151 response.  `Tcf7l2` demonstrates that the 151 cell group can report a
postnatal thalamic transcription-factor phenotype when a factor has the correct
local terminal-state role, but that mechanism is Wnt/TCF and beta-catenin
linked rather than TLX-family linked.

I therefore predicted that acute `Tlx3` loss would sit below the FDR 0.05
counting threshold in recovered 151 nuclei.  A one-gene outcome like `Lbx1`
would also be compatible with the evidence, but the exact point estimate of 0
better matches the many zero DEG counts among represented homeobox/PAX/GATA
developmental regulators and the absence of any measured upstream perturbation
that significantly exposed `Tlx3` in the training DE surface.

Predicted count: **0 DEGs**.

## Limits

`Tlx3` itself is held out, so no expression pattern, recovered-nucleus count, or
gRNA performance statistic for `Tlx3` is present in the inputs.  The training
set lacks the closest TLX-family paralogs, `Tlx1` and `Tlx2`, so the prediction
extrapolates from broader developmental transcription-factor controls rather
than from an obligate family member.  The PubMed literature is embryonic and
dorsal-spinal, while the requested assay is sparse P16 CRISPR in juvenile
thalamic glutamatergic neurons; that difference is not by itself proof of a
null, but it is a candidate-specific reason to downgrade transfer because the
known TLX3 targets specify a lineage that the sampled 151 neurons have already
left.  Finally, the endpoint is a BH-thresholded count, so a prediction of zero
means no measured gene is expected to clear FDR 0.05; it does not exclude small
subthreshold changes or survivor-conditioned effects that the single-nucleus
DE test cannot see.
