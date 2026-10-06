# Nf2 direct DEG-count forecast

Target: `Nf2`

Endpoint: `n_degs` in `151 TH Prkcd Grin2c Glut`, counted as all measured genes with Wilcoxon BH-adjusted `pvals_adj < 0.05`.

Prediction: `1`

## Evidence Used

- The declared one-row manifest and the canonical biology bundle both name `Nf2`; the served `biology` characterization view reported `target_outcome_exposed=false` and `labeled_neighbors_exposed=false`.
- Exact focal-population reach for `Nf2` is real but partial: in matched non-target `151 TH Prkcd Grin2c Glut` nuclei, Nf2 was detected in 13,221 of 23,679 cells, or 55.834%, with mean raw UMI 0.909 and mean log1p CP10k 0.371. I used this as population reach only, not as an editing-efficiency estimate.
- The biology card calls merlin a dynamic FERM/ERM membrane-cytoskeleton and signaling adaptor. Its functional-stock adjudication concluded `likely_substantially_depleted` by the P37-P44 harvest because P16 editing stops new merlin supply, merlin occupies dynamic membrane/cytoskeletal/junctional/cytoplasmic/nuclear pools, and the only direct turnover fact in the bundle was a 14.6 h wild-type merlin half-life in a pulse-chase transfer context. That supports realized loss in successfully edited Nf2-positive cells, with uncertainty from using a human meningioma kinetic measurement rather than juvenile thalamic neurons.
- The same card gave moderate support for postnatal neuronal observability: postnatal cerebellar conditional Nf2 loss alters synaptic-terminal organization and miniature excitatory currents. I treated that as a plausibility prior only because it is cerebellar, begins before the requested P16 edit, and has no clean 21-28 day latency measurement.
- The 1,674-row training count table for this exact cell group is zero-heavy: 469/1,674 targets are nonzero, the median is 0, the 75th percentile is 1, and the 90th percentile is 2. Thus a poorly matched target should stay near 0-1 unless there is stronger assay-matched evidence for a thalamic RNA state.

## Training Perturbations Interpreted

The nearest operation-level counts point to a very small Nf2 response:

| comparator set | observed `151 TH Prkcd Grin2c Glut n_degs` |
| --- | --- |
| ERM/cytoskeleton/Rho-PAK/spectrin-catenin genes | `Rdx=1`, `Cdc42=1`, `Rac1=0`, `Pak1=1`, `Pak2=0`, `Pak3=0`, `Limk1=0`, `Actg1=1`, `Add1=0`, `Add2=0`, `Add3=0`, `Ank1=0`, `Ank2=0`, `Sptan1=1`, `Sptb=0`, `Ctnnd2=1`, `Frmd5=0` |
| postsynaptic scaffolds | `Dlg4=1`, `Shank2=0`, `Shank3=2`, `Syngap1=0`, `Homer2=0` |
| Wnt/beta-catenin relatives and receptors | `Ctnnb1=383`, `Tcf7l2=106`, `Lrp6=4`, `Gsk3b=6`, but `Lrp5=0`, `Fzd2=0`, `Fzd4=0`, `Fzd6=0`, `Fzd9=0`, `Lgr4=0`, `Gpc6=0`, `Ctnna2=0`, `Ctnna3=0`, `Ctnnd2=1` |
| Hippo/YAP transcriptional branch | `Tead1=0` |

The direct membrane/cytoskeleton set had median 0 and a log1p-mean count of 0.277, and the postsynaptic-scaffold set had median 0 and a log1p-mean count of 0.431. The raw Parquet rows showed that several of the one-count entries were self-transcript-only contrasts in the focal class: for example `Rdx` had only `Rdx` significant, `Cdc42` had only `Cdc42`, `Actg1` had only `Actg1`, `Sptan1` had only `Sptan1`, `Ctnnd2` had only `Ctnnd2`, and `Dlg4` had only `Dlg4`. This is important because the requested `n_degs` includes the self transcript when it passes FDR.

I did not transfer the high `Ctnnb1`, `Tcf7l2`, or `Grin1` counts directly. In the same-experiment corpus, `Ctnnb1` and `Tcf7l2` were interpreted as a thalamic Wnt/terminal-state module with many excitability, adhesion, and extracellular-matrix genes, whereas the represented receptor-level Wnt perturbations were mostly flat and `Lrp6`/`Gsk3b` were small. `Grin1` marked an NMDA-receptor-loss state. These prove that the 151 class can mount large synaptic or Wnt transcriptional programs, but they are broader downstream states than acute loss of the merlin scaffold.

The Hippo branch did not supply a high-count lower bound: `Tead1` was flat in every measured neuronal class in the corpus, with no detectable YAP/TEAD target program. That makes canonical YAP/TEAD activation an unsafe reason to lift Nf2 toward the beta-catenin core counts.

## Synthesis

Nf2 has enough expression and protein turnover support that a recovered, edited, target-positive neuron could lose merlin by harvest, so I did not force the estimate to zero. The closest assay-matched membrane/cytoskeleton and postsynaptic perturbations, however, are overwhelmingly FDR-flat in the exact focal class despite significant self-transcript loss in several cases. The high Wnt/NMDAR anchors are better treated as upper contextual boundaries than as scale-matched donors.

I therefore forecast a sparse self-only or near-self-only signature and set the integer point at:

```tsv
target_name	predicted_n_degs
Nf2	1
```
