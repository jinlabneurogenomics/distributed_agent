# Trace

## Question and endpoint

The held-out target for this run is `Agrn`. I interpreted the request as a
point prediction for the focal `151 TH Prkcd Grin2c Glut` endpoint:

`n_degs = count(measured genes with BH-adjusted Wilcoxon pvals_adj < 0.05)`

after sparse P16 AAV-CRISPR loss of the held-out gene, assayed in recovered
NeuN+ postnatal brain nuclei at P37-P44. `151 TH Prkcd Grin2c Glut` is the
thalamic glutamatergic class label, not a count and not tyrosine hydroxylase.
The requested `Agrn` rows were absent from both supplied inputs by design, so I
treated the training count CSV as the direct endpoint for retained analogs and
the Parquet signatures as direct same-experiment evidence for how those analogs
behaved. External biology was used only to decide which retained perturbations
were mechanistically close enough to be informative.

## Sources

- Declared endpoint table:
  `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`
- Declared differential-expression Parquet:
  `training differential-expression dataset`
- Requested-target manifest:
  `single-target request for Agrn`
- Internal same-experiment interpretation corpus: PerturbAI July release
  `perturbai-july-260713-sourceguard-1773-v1`, queried through the run-declared
  `corpus.findings`, `corpus.calibration`, and `corpus.graph` capabilities.
- External literature from PubMed for Agrn/LRP4/MuSK and CNS agrin function.
  I used these papers only as mechanistic priors:
  - Li, Xiong, and Mei 2017, DOI `10.1146/annurev-physiol-022516-034255`,
    PMID `29195055`
  - Herbst 2019, DOI `10.1016/j.neulet.2019.134676`, PMID `31811897`
  - Hoover et al. 2003, DOI `10.1083/jcb.200301013`, PMID `12796478`
  - Hilgenberg et al. 2006, DOI `10.1016/j.cell.2006.01.052`, PMID `16630822`
  - Li et al. 1999, DOI `10.1002/(sici)1097-4695(19990615)39:4<547::aid-neu8>3.0.co;2-c`,
    PMID `10380076`
  - Karakatsani et al. 2017, DOI `10.1242/dev.150110`, PMID `29061639`
  - Handara et al. 2018, DOI `10.1016/j.ydbio.2018.10.017`,
    PMID `30385274`

## Quantitative calibration

The training endpoint table has 1,674 non-held-out targets in the focal class.
It is strongly zero-inflated: 1,205 targets have `n_degs = 0`, the median is
0, the 75th percentile is 1, the 90th percentile is 2, and the high-count upper
tail is made of a small number of RNA-processing, proteasome, ubiquitin, and
core-transcription hits.

For the mechanistic analogs below, I queried the Parquet rows satisfying
`group_name == "151 TH Prkcd Grin2c Glut"` and `gene_target in (...)`, then
checked their retained endpoint counts, their `pvals_adj < 0.10` counts, their
number of nominal `pvals < 0.05` genes, and the top nominal genes. This was to
distinguish true sparse/null signatures from targets that barely missed the
0.05 FDR threshold.

| comparator | reason inspected | focal `n_degs` at FDR<0.05 | focal FDR<0.10 genes | focal expression evidence |
|---|---:|---:|---:|---|
| `Lrp4` | canonical agrin receptor and MuSK coreceptor at the neuromuscular junction | 0 | 0 | 381 nominal genes, maximum absolute score 3.32, all adjusted p-values 1 |
| `Musk` | kinase downstream of agrin-LRP4 in the canonical pathway | 0 | 0 | 310 nominal genes, maximum absolute score 3.58, all adjusted p-values 1 |
| `Chrna1`, `Chrnd`, `Chrne`, `Chrng` | AChR endplate branch downstream of agrin-LRP4-MuSK | 0 each | 0 each | all flat at FDR<0.10 |
| `Ache` | neuromuscular cholinergic endplate-associated comparator present in the screen | 1 | 1 | only the self transcript passed FDR<0.05 |
| `Dag1`, `Dmd`, `Snta1`, `Gpc6` | extracellular matrix, dystroglycan/dystrophin, or heparan-sulfate-proteoglycan-adjacent counterexamples | 0 each | 0 each | all flat at FDR<0.10 |
| `Nrxn1`, `Nrxn2`, `Nrxn3`, `Nlgn3`, `Lrrtm1`, `Grid1`, `Grid2` | neuronal synaptic adhesion or postsynaptic organizer counterexamples | 0 to 1 | 0 to 1 | only singleton or null focal FDR calls |
| `Atp1a3` | possible agrin interactor through alpha3 Na,K-ATPase in CNS neurons | 80 | 108 | a broad thalamic ion-pump/calcium/excitability state |

The internal PerturbAI July corpus agreed with these focal measurements and
added cross-cell context. Its `Lrp4` report called the perturbation globally
buffered: only 1 of 371,796 downstream Lrp4 tests reached FDR<0.10 anywhere,
and `Lrp4` did not engage the Lrp6/Ctnnb1 Wnt module in 151 thalamic cells.
Its `Musk` report found one weak FDR<0.10 gene in `027 NP-CT-L6b-OB Glut`, no
shared response with `Lrp4`, `Chrna1`, `Chrnd`, `Chrne`, or `Ache`, and no
broad neuronal transcriptional liability. A graph query for `Agrn` as an
explicit same-experiment reported comparator returned no rows, so there was no
hidden `Agrn`-centered comparator set in the July release.

## Agrn-specific causal transfer

Agrin is a large extracellular heparan-sulfate proteoglycan. At skeletal
neuromuscular junctions, motor-neuron agrin binds LRP4 and activates MuSK,
with DOK7 and rapsyn organizing acetylcholine receptor clusters; that pathway
is a highly established obligate endplate mechanism rather than a generic
neuron-nuclear RNA program. The retained perturbations that directly sample
the receptor branch most relevant to this mechanism, `Lrp4` and `Musk`, were
both complete focal nulls at FDR<0.05 and FDR<0.10. The retained AChR subunits
were also complete nulls, and `Ache` produced only its own transcript as a
singleton focal hit.

That makes the transfer chain weak for a nonzero thalamic DEG-count prediction:

1. `Agrn` CRISPR impairs an extracellular ligand.
2. In the canonical NMJ chain, the direct consequence must propagate through
   LRP4 and MuSK on a postsynaptic muscle endplate.
3. The requested experiment samples NeuN+ brain nuclei, not skeletal muscle or
   Schwann cells, and the focal 151 class is postmitotic thalamic glutamatergic
   neurons.
4. The exact neuronal Lrp4/Musk/AChR perturbations that remained in training
   did not produce the requested 151 DEG endpoint.

Agrin also has CNS biology, so I did not discard it as purely muscular.
Hoover et al. reported agrin-responsive signaling at CNS neuron synapses, and
Hilgenberg et al. identified alpha3 Na,K-ATPase/ATP1A3 as a neuronal agrin
binding partner whose activity can be modulated by agrin. However, direct
`Atp1a3` loss disrupts the Na,K pump itself and gave a large 151 response
(`n_degs = 80`), while loss of an extracellular agrin ligand would only affect
that pump through a context-dependent modulation step. Treating `Atp1a3` as a
same-outcome analog would transfer across the wrong intervention stage.

The CNS synaptogenesis prior is also mixed rather than strongly pro-DEG.
Karakatsani et al. and Handara et al. support roles for LRP4, agrin, and MuSK
in dendritogenesis and synapse organization in embryonic cortical cultures or
developing cortex, but Li et al. showed that functional glutamatergic and
GABAergic synapses can form between agrin-deficient cortical neurons. In the
present P16 mosaic, survivor-conditioned whole-brain snRNA-seq design, the
training `Nrxn`, `Nlgn3`, `Lrrtm1`, `Grid1/2`, `Dag1`, and `Dmd` perturbations
showed that synaptic adhesion or extracellular organization genes frequently
produce no broad nuclear RNA footprint even when their primary biology is
synaptic.

## Prediction

I predict `Agrn` will be below the FDR<0.05 detection threshold in
`151 TH Prkcd Grin2c Glut`: the closest retained canonical receptor-pathway
members, `Lrp4` and `Musk`, were focal zeros; represented endplate branch genes
were focal zeros; heparan-sulfate or dystroglycan/matrix-adjacent retained
genes were focal zeros; and the CNS literature does not establish an obligate
Agrn-to-nuclear-transcription chain in postnatal thalamic neurons. My point
estimate is therefore `0`.

## Limits

The prediction is an extrapolation because `Agrn` itself has no held-in
differential-expression rows or count. The most direct agrin effect could be
non-cell-autonomous, isoform-specific, extracellular, or electrophysiological;
those endpoints are mostly invisible to this single-nucleus RNA assay. The
canonical Agrn-LRP4-MuSK evidence comes largely from neuromuscular junctions,
which are not present in the NeuN+ screen, while the CNS agrin literature comes
from cultured embryonic neurons or non-thalamic systems. A small singleton
response is also plausible because several synaptic comparators produced one
FDR gene, but the best assay-matched evidence favors a zero-count point
prediction.
