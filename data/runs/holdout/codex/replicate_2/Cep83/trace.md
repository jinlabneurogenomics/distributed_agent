target: Cep83
cell group: 151 TH Prkcd Grin2c Glut
prediction: 0

## Endpoint and allowed measurements

The requested endpoint is the count of measured genes with BH-adjusted
Wilcoxon p < 0.05 in the 151 TH Prkcd Grin2c Glut contrast. The declared
holdout manifest contains one target, Cep83. The target response profile and
target n_degs were not used; the endpoint evidence below comes from the
training count table, training parquet rows for non-Cep83 perturbations, the
Cep83 biology-only bundle, and same-experiment corpus summaries.

## Cep83 prior

The Cep83 bundle supports reach in the focal population but not a strong
acute-stock-loss prior:

- Cep83 is measured in this population in non-target cells
  (`14148 / 23679`, 59.75% expressing; mean raw UMI 1.06; pseudobulk CPM
  66.15), so a transcriptional response is not excluded by target absence.
- CEP83 is a proximal mother-centriole distal-appendage organizer needed for
  recruitment of downstream appendage proteins and cilium initiation.
- By the P16 edit, basal-body distal appendages and primary cilia should
  already be installed in postmitotic neurons. The functional-stock
  adjudication therefore marks new Cep83 supply as stopped by an edit while
  pre-existing appendage/cilium stock may initially persist.
- Postmitotic forebrain Cep83 deletion can remove primary cilia in vivo, so the
  operation is biologically material, but the bundle found no timed 21-28 day
  CEP83/appendage/cilium clearance measurement that transfers to the P16 to
  P37-P44 thalamic assay window. Functional stock at harvest is therefore
  indeterminate rather than confidently depleted.

## Training-count evidence

The declared 151 TH Prkcd Grin2c Glut training table is sparse overall:

- 1674 training targets.
- 1205 have n_degs = 0.
- median = 0; 75th percentile = 1; 90th percentile = 2; 95th percentile = 18.

I treated the ciliary assembly / transport / signaling genes present in the
training table as the most relevant measured comparators, because they hit the
same primary-cilium apparatus that Cep83 acts upstream of. Their exact
151-counts were:

```tsv
target_name	n_degs
Adcy3	0
Alms1	0
Arl2bp	0
Arl3	1
Armc9	0
B9d1	0
Bbs5	0
Cep112	0
Cep120	0
Cep290	0
Cplane1	0
Dync2h1	0
Dync2i1	0
Gli1	0
Gli2	0
Htr6	0
Ift43	0
Ift81	0
Ift88	0
Kif3b	0
Kiz	0
Rpgrip1l	0
Sclt1	0
Smo	0
Ttc21b	0
Ttc8	1
```

The row-level parquet for 18 manually selected ciliary/Hedgehog comparators in
the same cell group gave the same picture. Sclt1, the closest available
distal-appendage comparator, had 0 FDR<0.05 genes. Core ciliary comparators
Cep290, Cplane1, Dync2h1, Dync2i1, Ift43, Ift81, Ift88, Kif3b, Rpgrip1l,
Ttc21b, B9d1, Bbs5, Adcy3, and Smo also had 0. The only significant rows in
that focused parquet slice were the target transcripts of Arl3 and Ttc8
themselves; they did not show a multi-gene downstream state in this population.

## Same-experiment corpus evidence

The packaged findings for measured ciliary genes agreed with the direct count
inspection. I used these only as same-experiment interpretation, not as
independent replication:

- Arl3:F003 reports that represented ciliopathy comparators did not phenocopy
  Arl3 in the postnatal neuronal snRNA readout.
- Cep290:F003 reports absence of expected ciliary GPCR, BBSome/IFT, and
  Hedgehog-effector transcription after Cep290 and near-absence when the
  pathway components themselves were perturbed.
- Cplane1:F001-F003 report no downstream FDR<0.10 DE across 22 neuronal groups
  and no convergence among represented ciliary, Joubert, Hedgehog, or PCP
  neighbors.
- Dync2h1:F001-F004 and Kif3b:F001-F005 report pan-neuronal transcriptomic
  nulls or near-nulls and failure to recover a Hedgehog/Gli or transport
  module.
- Ift88:F003-F005 and Sclt1:F002-F003 report that cilium-related perturbations
  mainly converge by being transcriptionally buffered, without a robust shared
  IFT-B, Hedgehog, UPR, ISR, or cilium-gene program.

## Synthesis

Cep83 is not a generic non-expressed target: the focal neurons contain Cep83
RNA, and the protein is functionally important for primary cilia in neural
systems. The stronger determinant for this endpoint is that the Perturb-seq
assay starts after cilia assembly, samples survivor nuclei 21-28 days later,
and shows almost no BH-significant 151 TH Prkcd Grin2c Glut response for many
measured perturbations that attack ciliary transport, transition-zone
integrity, BBSome/IFT biology, Hedgehog transduction, or a distal-appendage
partner. The two ciliary one-count cases in this cell group were target-mRNA
events rather than a downstream program, and self-transcript loss is too noisy
to justify adding a DEG for Cep83.

I therefore put Cep83 at the modal, ciliary-comparator-supported quiet outcome
and forecast:

```tsv
target_name	predicted_n_degs
Cep83	0
```
