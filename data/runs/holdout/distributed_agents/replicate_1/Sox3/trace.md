# Sox3 held-out DEG-count prediction

## Question interpreted

The requested file contains one held-out perturbation, `Sox3`. I interpreted the
task as predicting a single non-negative integer: the number of measured genes
expected to pass Benjamini-Hochberg FDR 0.05 after acute AAV-CRISPR loss of
`Sox3` in the focal `151 TH Prkcd Grin2c Glut` neuronal group. The held-out
`Sox3` perturbation itself is absent from the supplied differential-expression
Parquet and from the focal-cell training count CSV, so I used only non-held-out
perturbations in those inputs as experimental analogs.

Important ambiguities I resolved:

- `TH` in the cell label means thalamus, not tyrosine hydroxylase.
- `n_degs` is an assay-specific FDR-significant transcript count in recovered
  nuclei, not an editing-efficiency, survival, or biological-importance score.
- On-target transcript depletion was not used as a quantitative edit-strength
  filter; in this indel-based atlas it is expected to be a weak QC readout.

## Sources used

- The declared focal training-count table,
  `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
- The declared differential-expression table,
  `training differential-expression dataset`.
- The same-experiment internal report corpus
  `perturbai-july-260713-sourceguard-1773-v1`, especially bounded `Sox2`,
  `Sox5`, `Sox4`, and `Sox11` Findings and the direct-evidence index for
  SOX-family comparisons. This corpus is another representation of the same
  Perturb-seq experiment, so I used it for compact interpretation of training
  analogs, not as independent replication.
- External PubMed literature on SOXB1/SOX3 function:
  Graham et al. 2003, Neuron, doi:10.1016/s0896-6273(03)00497-5, PMID
  12948443; Wang et al. 2006, Journal of Comparative Neurology,
  doi:10.1002/cne.20984, PMID 16680766; Archer et al. 2010, Developmental
  Biology, doi:10.1016/j.ydbio.2010.12.013, PMID 21147085; Rogers et al. 2014,
  PLoS ONE, doi:10.1371/journal.pone.0095356, PMID 24751947; McAninch and
  Thomas 2014, PLoS ONE, doi:10.1371/journal.pone.0113361, PMID 25409526.

## Quantitative calibration from the supplied training data

The focal count CSV has 1,674 non-held-out perturbations. Its empirical
distribution is strongly zero-inflated: 1,205 targets, 72%, have `n_degs = 0`;
the median is 0, the 75th percentile is 1, the 90th percentile is 2, the 95th
percentile is 18, and the maximum is 2,677. A held-out developmental
transcription factor therefore needs close, endpoint-bearing evidence before it
should be placed far above zero.

I then filtered the Parquet to `group_name == "151 TH Prkcd Grin2c Glut"` for
training SOX genes and relevant developmental comparators, counted rows with
`pvals_adj < 0.05`, and inspected the significant genes plus the largest
absolute Wilcoxon scores. The relevant focal-cell results were:

| training perturbation | focal `n_degs` | focal significant genes and pattern |
| --- | ---: | --- |
| `Sox2` | 2 | `Tnnt1` down, logFC -1.006, FDR 2.77e-6; `Stam` down, logFC -0.567, FDR 0.0147 |
| `Sox5` | 2 | `Dgkh` up, logFC +0.387, FDR 5.37e-4; `Tnnt1` up, logFC +0.566, FDR 0.0284 |
| `Sox4` | 0 | no focal gene passed FDR 0.05; strongest nominal rows all had adjusted P = 1 |
| `Sox11` | 0 | no focal gene passed FDR 0.05; best adjusted P = 0.577 |
| `Sox9`, `Sox10`, `Sox17`, `Sox18` | 0 each | no focal gene passed FDR 0.05; strongest nominal rows all had adjusted P = 1 |
| `Pax6`, `Neurod1`, `Neurod2`, `Notch1`, `Notch2`, `Rest`, `Pou5f1` | 0 each | no focal gene passed FDR 0.05 |
| `Tcf7l2` | 106 | broad focal thalamic response; useful as a power counterexample, but mechanistically distant |
| `Rora` | 278 | broad focal thalamic response; also distant from SOXB1 biology |

A broader scan over the same analog set across all assayed cell groups found
that the SOX effects were not hidden elsewhere in the atlas: `Sox2` and `Sox5`
had FDR<0.05 hits only in `151 TH Prkcd Grin2c Glut`; `Sox4`, `Sox9`,
`Sox10`, `Sox11`, `Sox17`, `Sox18`, `Pax6`, `Neurod1`, `Neurod2`, `Notch2`,
and `Rest` had no FDR<0.05 hits in any scanned group; the only positives among
the broader comparators were `Notch1` with one cortical hit, `Tcf7l2` with 106
focal hits and one olfactory/entorhinal hit, and `Rora` with 278 focal hits.

## Target-specific reasoning

### Sox3

`Sox3` is a SOXB1 HMG-box transcription factor, so the most appropriate
training analog is `Sox2`, the in-screen SOXB1 paralog. External work places
`Sox1`, `Sox2`, and `Sox3` in a partially redundant neural-progenitor module:
SOXB1 activity maintains vertebrate neural progenitor identity and can repress
neuronal differentiation (Graham et al. 2003; Archer et al. 2010). SOX3 binds
conserved neural-progenitor enhancers and developmental regulators, including
the directly validated target `Dbx1`, in embryonic neural progenitor contexts
(Rogers et al. 2014; McAninch and Thomas 2014). Wang et al. 2006 also found
that Sox3 protein persists in neonatal/adult germinative zones and in some
postmitotic neuronal populations, so a low-level neuronal role is plausible.

That prior transfers only weakly to this endpoint. The experiment perturbs
already postmitotic P16 thalamic neurons, not embryonic ventricular-zone neural
progenitors or adult SVZ/dentate precursors. In the same Perturb-seq atlas,
acute `Sox2` loss, despite being the closest SOXB1 comparator, produced only
two focal DEGs and the internal July report specifically noted that the
canonical Sox2 neural-stem, pluripotency, proliferation, Notch/Hes, and
published thalamic retina-thalamus-cortex outputs were not recovered. The
`Sox2` footprint itself was a tiny two-gene survivor-state signature
(`Tnnt1`, `Stam`) and not phenocopied by assayed Notch, REST, Pax6, chromatin,
or other SOX perturbations. The farther SOXD/SOXC analogs also argue against a
large generic SOX response: `Sox5` had only two focal genes and `Sox4`/`Sox11`
were completely buffered across recovered neuronal classes.

My causal model is therefore:

1. Acute mosaic CRISPR disrupts `Sox3` in postmitotic thalamic neurons.
2. The direct molecular consequence is loss of a SOXB1 transcription factor,
   but most established SOX3 targets are progenitor enhancers that should be
   closed, redundant, or no longer limiting in this P37-P44 neuronal context.
3. Any remaining propagation through thalamic neuronal maintenance programs is
   expected to be comparable to, and probably weaker than, the two-gene `Sox2`
   response because there is no supplied evidence for a Sox3-specific dLGN-like
   program in this focal group.
4. The recovered snRNA-seq endpoint is therefore likely at the stochastic
   boundary where zero to a few genes pass FDR 0.05.

I predicted a tiny nonzero effect, `1`, rather than a broad SOX developmental
program. The nonzero call is driven mainly by `Sox2 = 2` as a close in-dataset
SOXB1 analog and by external evidence that SOX3 can retain neuronal expression.
The attenuation from 2 to 1 reflects that the direct SOX3 literature is
strongest in progenitors, not juvenile thalamic neurons, and that most assayed
developmental TF analogs were exactly zero in this assay.

## Limits and extrapolations

The input contains no `Sox3` perturbation rows, so there is no direct
same-experiment signature for `Sox3`; the prediction is an extrapolation from
training perturbations. `Sox2` is mechanistically close but not equivalent:
SOXB1 factors are overlapping rather than identical, and `Sox2` has a published
postmitotic thalamic role that may not transfer to `Sox3`. The opposite
directions of the shared `Tnnt1` hit under `Sox2` and `Sox5` also show that
even very small SOX-family signatures in this focal class are not a coherent
family module. Finally, with 173-324 perturbed focal nuclei for the assayed SOX
comparators and an FDR threshold over about 17,000 genes, moving a count from 0
to 1 or 2 can depend on power and multiple-testing boundary behavior rather
than on a categorical biological difference.
