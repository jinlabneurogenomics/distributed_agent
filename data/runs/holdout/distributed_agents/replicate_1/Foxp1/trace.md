# DEG-count prediction trace

## Question interpreted

The requested scalar endpoint is the number of genes with Benjamini-Hochberg
adjusted Wilcoxon `pvals_adj < 0.05` after CRISPR loss of each held-out target
in the focal `151 TH Prkcd Grin2c Glut` cell group. The single requested
held-out perturbation in this run was:

```text
Foxp1
```

I treated `151 TH Prkcd Grin2c Glut` as the exact thalamic glutamatergic atlas
group. I did not treat the numeric prefix as a nucleus count, and I did not use
held-out `Foxp1` expression or DEG values because this target is absent from the
training parquet and the training DEG-count CSV. The prediction is therefore a
transfer from non-held-out perturbations plus prior knowledge about FOXP-family
biology.

The endpoint is directly observed for training targets in the supplied focal
cell group through `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
For held-out `Foxp1`, the same endpoint is absent by design; focal-cell
training counts and same-assay expression signatures are proxies for expected
response breadth.

## Sources used

- Declared differential-expression input:
  `training differential-expression dataset`.
  This supplied focal-cell Wilcoxon statistics, adjusted p-values, log2 fold
  changes, and matched recovered-cell counts for training perturbations.
- Declared training endpoint:
  `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
  This supplied exact `n_degs` counts for non-held-out targets in `151 TH Prkcd
  Grin2c Glut`.
- Declared requested-target manifest:
  `single-target request for Foxp1`.
- Run-local PerturbAI atlas dataset portrait, task bindings, compact coverage,
  and capability manifest under `codex_runtime/pipeline`.
- Internal same-experiment semantic corpus:
  `perturbai-july-260713-sourceguard-1773-v1`, queried only for visible
  training-target Findings around `Foxp2`, `Sox5`, `Tbr1`, `Rora`, and
  `Tcf7l2`. This corpus is a packaged interpretation of the same Perturb-seq
  experiment, not an independent replicate.
- External PubMed-indexed literature:
  Tamura et al. 2004, DOI `10.1016/j.neuroscience.2003.11.036`, PMID
  `14980377`; Hisaoka et al. 2009, DOI `10.1016/j.neuroscience.2009.12.055`,
  PMID `20040367`; Sin et al. 2014, DOI `10.1007/s12031-014-0359-7`, PMID
  `25027557`; Sollis et al. 2015, DOI `10.1093/hmg/ddv495`, PMID `26647308`;
  Lozano et al. 2015, DOI `10.1038/ejhg.2015.66`, PMID `25853299`;
  Khandelwal et al. 2024, DOI `10.1126/sciadv.adm7039`, PMID `38701209`.

## Quantitative checks

I first read the requested manifest and confirmed that it contained one target,
`Foxp1`. The focal training-count table contained 1,674 training targets and
had median `n_degs = 0`, maximum `n_degs = 2677`, and 28.0% nonzero targets.
`Foxp1` was absent from this table, as expected for a held-out target.

For biologically plausible analogs and counterexamples I pulled the `151 TH
Prkcd Grin2c Glut` rows from the parquet and recomputed significant genes as
`pvals_adj < 0.05`. The filtered query was equivalent to:

```python
filter = (
    pc.field("group_name") == "151 TH Prkcd Grin2c Glut"
) & pc.field("gene_target").isin(selected_training_targets)
```

This query also exposed the top adjusted p-values and matched recovered-cell
counts for each selected target so that a zero count could be distinguished
from a visibly underpowered comparison.

Observed focal counts for the main comparators were:

| training target | focal `n_degs` | matched perturbed nuclei in 151 | expression-pattern evidence in the focal rows |
| --- | ---: | ---: | --- |
| `Foxp2` | 0 | 245 | no gene passed FDR 0.05; the smallest adjusted p-values were all 1.0 |
| other represented FOX genes: `Foxa2`, `Foxc2`, `Foxe3`, `Foxi1`, `Foxj3`, `Foxk2`, `Foxl1`, `Foxl2`, `Foxn1`, `Foxp3` | 0 each | `Foxa2` inspected at 213 | all were zero in the endpoint table; `Foxa2` had no focal adjusted p-value below 1.0 among its strongest rows |
| `Tbr1` | 0 | 288 | no focal DEG; same-corpus report showed sparse Tbr1 effects in cortical glutamatergic groups, not thalamus |
| `Satb2` | 0 | 236 | no focal DEG despite good matched-cell recovery |
| `Bcl11b` | 0 | 206 | no focal DEG; strongest adjusted p-values were 1.0 |
| `Sox5` | 2 | 184 | a real but two-gene thalamic response, `Dgkh` and `Tnnt1`, not a broad developmental fate program |
| `Mef2c` | 1 | 223 | only the self transcript passed FDR 0.05 |
| `Tcf7l2` | 106 | 111 | a broad thalamic terminal-selector response with `Ramp3`, `Cck`, `Spock3`, `Kcnc2`, `Pcsk2`, and other strong hits |
| `Rora` | 278 | not in the focused parquet pull, but present in the training count table | same-corpus report described a broad down-dominant 151 thalamic program |

The positive `Tcf7l2`, `Rora`, `Chd8` with 61 DEGs, and `Setd5` with 9 DEGs
counterexamples show that this cell group and assay could produce a focal
transcriptional footprint for transcriptional/chromatin regulators. The
specific FOXP and cortical-projection-neuron neighborhood instead sat at zero
or at a two-gene sparse boundary.

## Same-experiment analog evidence

`Foxp2` was the closest training-set member of the FOXP subfamily. The July
PerturbAI corpus summarized `Foxp2` as having no FDR-supported downstream
transcriptomic response in any of 22 measured neuronal groups after P16 sparse
CRISPR loss of function. A second `Foxp2` Finding explicitly contrasted this
with prior FOXP biology: although FOXP2 directly regulates `CNTNAP2` and
FOXP1/FOXP2/FOXP4 dimers can regulate early neuronal-development targets,
neither the nominated `Cntnap2` axis nor early FOXP target genes were recovered
in this P16-to-P37/P44 snRNA-seq assay. A third `Foxp2` comparator Finding
noted that postnatal transcription-factor responsiveness was factor-specific:
`Tbr1` and `Mef2c` had real DE surfaces in some Foxp2-matched groups, while
`Foxp2`, `Bcl11b`, and `Satb2` were flat.

This matters for `Foxp1` because the direct intervention and molecular
consequence are analogous: both are sparse CRISPR loss of a FOXP forkhead
transcription factor in juvenile postmitotic neurons. The propagation step is
imperfect. FOXP1 is not simply FOXP2; FOXP1 has stronger evidence in striatal
projection neurons and is a distinct human neurodevelopmental-disease gene.
But the same-experiment `Foxp2` data are the only close FOXP-subfamily
perturbation and argue that disrupting this family in P16 postmitotic neurons
did not inevitably create a broad, recovered-cell RNA response.

`Sox5`, `Tbr1`, `Satb2`, and `Bcl11b` were used as projection-neuron
transcription-factor counterexamples rather than as direct biochemical
analogs. `Tbr1`, `Satb2`, and `Bcl11b` were all zero in the focal thalamic
group. `Sox5` had a two-gene 151 response, but the same-experiment corpus
separated that pair from the canonical embryonic cortical projection-neuron
program and noted no strong genome-wide phenocopy. These comparisons suggest
that many developmental transcription factors with clear embryonic or cortical
functions are buffered or temporally displaced when perturbed sparsely at P16.

`Rora` and `Tcf7l2` were important counterexamples. Both are thalamic
transcriptional regulators that were strongly visible in the same focal class:
`Rora` had 278 focal DEGs and the corpus described a broad, down-dominant
151-specific program; `Tcf7l2` had 106 focal DEGs and a thalamic
terminal-effector signature. Their presence prevents treating `Foxp1` as zero
solely because transcription factors are hard to detect. The decisive
difference is that the training set shows a maintained RORalpha/TCF7L2
terminal-selector requirement in this thalamic class, whereas the FOXP-related
and cortical projection-neuron analogs are flat.

## Biological transfer to Foxp1

Tamura et al. 2004 mapped `Foxp1` RNA in adult mouse CNS and found strongest
expression in striatum, with moderate cerebral cortex, CA1/CA2 hippocampus,
and several thalamic nuclei, and striatal signal in projection rather than
interneuron populations. Hisaoka et al. 2009 further placed FOXP1 and FOXP2 in
different postnatal/adult cortical projection-neuron populations, with FOXP1
in layers III-VIa and FOXP2 more restricted to layer VI DARPP-32-positive
neurons. Human genetics also supports real FOXP1 dosage sensitivity: Lozano et
al. 2015 and Sollis et al. 2015 reported de novo FOXP1 variants causing
intellectual disability, autism features, and speech/language impairment.
FOXP1 can heterodimerize with FOXP2 and FOXP4, and FOXP1/2/4 dimer combinations
can regulate FOXP2 target genes in cellular assays (Sin et al. 2014).

Those facts establish that `Foxp1` is not an implausible neuronal regulator.
They do not, however, establish a broad DEG count in recovered thalamic
Prkcd/Grin2c glutamatergic nuclei after acute juvenile mosaic CRISPR. The most
direct postnatal FOXP1 evidence with snRNA-seq, Khandelwal et al. 2024,
identified a postnatal FOXP1 requirement in striatal D2 spiny projection
neurons and candidate postsynaptic gene-expression changes; that is a
different GABAergic striatal context from the focal thalamic glutamatergic
class used here. Transfer therefore breaks mainly at the exposure and
cell-context step, not at the idea that FOXP1 can regulate neuronal genes.

For this focal class the same-assay evidence favors a null or near-null
response. If Foxp1 KO in 151 behaved like the closest represented FOXP member,
`Foxp2`, no measured genes would pass FDR 0.05. If it behaved like weak
projection-neuron TFs such as `Sox5` or `Mef2c`, it might yield a one- or
two-gene edge response. I assigned zero rather than a positive edge count
because every represented FOX-family perturbation in the focal endpoint was
zero, `Foxp2` was flat even outside 151, and the thalamus-active
`Tcf7l2`/`Rora` programs were mechanistically much closer to maintained
thalamic terminal identity than to FOXP1.

## Prediction

| target_name | predicted_n_degs |
| --- | ---: |
| `Foxp1` | 0 |

## Limits

This is an extrapolation from visible analogs, not a direct Foxp1 measurement.
The training set does not contain `Foxp4`, the other close FOXP-subfamily
member, and it lacks raw guide-level genotypes or protein measurements, so the
model cannot distinguish incomplete functional disruption from postnatal
buffering. The external literature is strongest for embryonic, cortical,
striatal, and disease contexts; several thalamic nuclei express `Foxp1`, but
the exact `151 TH Prkcd Grin2c Glut` population was not functionally tested in
those reports. Because the endpoint is a BH-thresholded count from recovered
nuclei, a prediction of 0 DEGs means no gene is expected to clear this assay's
FDR 0.05 threshold in 151, not that Foxp1 is biologically irrelevant.
