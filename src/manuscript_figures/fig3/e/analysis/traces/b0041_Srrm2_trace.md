# Question

I interpreted the task as a scalar holdout prediction for one perturbation,
`Srrm2`, in the focal `151 TH Prkcd Grin2c Glut` neuronal group.  The requested
endpoint is the held-out number of measured genes with `pvals_adj < 0.05` in
the same Wilcoxon differential-expression pipeline used for the visible
training targets.  The held-out perturbation has no focal signature or DEG
count in the supplied inputs, so the point estimate below transfers from
visible focal-cell perturbations and from prior biology of SRRM2.

I treated the supplied focal CSV as the direct endpoint for the 1,674 training
perturbations and the Parquet as direct evidence for their expression
signatures.  The endpoint for `Srrm2` itself is absent by construction.  The
PerturbAI July same-experiment corpus
`perturbai-july-260713-sourceguard-1773-v1` was used only as a packaged
interpretation layer over the same experiment, not as independent replication.
External mechanism came from PubMed-indexed literature.

# Quantitative checks

The requested-target CSV contains a single held-out row, in order:

```text
Srrm2
```

The focal training distribution is sparse and heavy-tailed:

```text
count = 1674 perturbations
mean n_degs = 14.05
median = 0
75th percentile = 1
90th percentile = 2
95th percentile = 18
99th percentile = 436
maximum = 2677
positive fraction = 0.280
```

I then queried
`training_de_all_cell_groups.parquet` for `151 TH Prkcd Grin2c Glut` rows only
and counted FDR-significant genes for spliceosome, RNA-processing, and
nuclear-transport perturbations that are plausible mechanistic analogs or
counterexamples for SRRM2.  Representative focal counts were:

```text
Rnpc3    868
U2af2    828
Hnrnpu   733
Cdc40    624
Tnpo3    618
Prpf6    454
Thoc1    303
Snrnp70  213
Tardbp   210
Matr3    149
Hnrnpc   122
Ddx39b     0
Rbm28      0
Snrpb      0
Son        0
```

The same query verified that the broad splicing/SR-import analogs alter
`Srrm2` itself as part of their focal whole-gene signatures:

```text
perturbation  Srrm2 log2FC  Srrm2 FDR
Rnpc3         -0.620        4.46e-14
Tnpo3         -0.536        1.69e-10
Cdc40         -0.448        1.27e-10
U2af2         -0.444        8.73e-17
Thoc1         -0.322        2.61e-06
Prpf6         -0.294        5.47e-03
Snrnp70       -0.132        3.64e-01
Hnrnpc        -0.032        1
Son           -0.027        1
```

These rows make `Srrm2` a recurrent member of the response to several
high-count spliceosome or SR-cargo perturbations, especially `Rnpc3`, `U2af2`,
`Cdc40`, `Tnpo3`, `Thoc1`, and `Prpf6`.  They also show the relevant
counterexamples: `Son`, the closest assayed nuclear-speckle scaffold, had no
FDR 0.05 focal genes, and generic RNA-binding or spliceosome labels were not
sufficient because `Snrpb`, `Ddx39b`, and `Rbm28` were flat.

# Same-experiment analogs

`Rnpc3` was the strongest focal RNA-splicing analog by count, with 868 DEGs.
The internal corpus report for `Rnpc3` states that RNA-splicing perturbations
converged with `Rnpc3`, with `Prpf6`, `Snrnp70`, `U2af2`, `Cdc40`, and
`Hnrnpu` sharing hundreds of same-direction RNPC3-coordinate DE events in the
large 151/155/191 responders.  The same report also noted that `Rnpc3` altered
RNA-processing and transcription/export genes and included `Srrm2` as one of
the down-regulated RNA-processing targets in the broad signatures.  This is a
strong within-dataset argument that perturbing a limiting spliceosome factor
can create hundreds of FDR 0.05 DEGs in this exact focal cell class.

`U2af2` had 828 focal DEGs.  Its corpus report described U2AF2 as a 3-prime
splice-site recognition factor and identified `Rsrp1`, `Srrm2`, `Luc7l2`,
`Srsf5`, and `Tial1` as repeatedly decreased abundance markers, with
`Prpf6`, `Cdc40`, and `Tpr` among its closest positive neighbors.  In the raw
focal rows, `U2af2` reduced `Srrm2` with log2FC -0.444 at FDR 8.7e-17.  This
is the most direct same-experiment expression-pattern evidence that SRRM2 lies
inside the RNA-splicing response axis that becomes broad in 151 TH Prkcd
Grin2c Glut cells.

`Cdc40`, `Prpf6`, `Tnpo3`, and `Thoc1` provide intermediate anchors rather
than exact biochemical phenocopies.  `Cdc40` is a PRP17 second-step splicing
factor and had 624 focal DEGs; `Prpf6` is a U5 tri-snRNP assembly factor and
had 454; `Tnpo3`, an import receptor for phosphorylated RS-domain splicing
factors, had 618; and `Thoc1`, a TREX mRNA-export factor, had 303.  The July
corpus connected these perturbations to a recurrent down-regulated
SR-splicing/RNA-processing arm that includes `Srrm2` and `Srsf5`, coupled to
stress and mature-neuronal gene changes.  These are appropriate partial
analogs because they interfere with RNP maturation upstream, downstream, or
adjacent to nuclear speckles, not merely because they share a GO label.

`Snrnp70`, `Tardbp`, `Matr3`, and `Hnrnpc` constrain the lower side of the
prediction.  They are bona fide RNA-processing perturbations but produced
substantially smaller focal counts, 213, 210, 149, and 122 respectively.
`Hnrnpc` was specifically described in the U2AF2 corpus report as
non-convergent with `U2af2` despite HNRNPC/U2AF competition at cryptic
3-prime splice sites.  This limits the transfer from "RNA binding" alone.

`Son` is the main counterexample.  External work places SON with SRRM2 at the
core of nuclear speckles, but the focal `Son` perturbation had zero FDR 0.05
DEGs and only one FDR 0.10 gene in another class in the packaged report.  I
therefore did not treat SRRM2 as guaranteed to match the 454 to 868 DEG core
spliceosome group.  I also did not treat the SON null as decisive for SRRM2:
Ilik et al. found that SON depletion only partially disassembles nuclear
speckles, whereas combined SON/SRRM2 depletion or SON depletion with SRRM2
intrinsically disordered regions removed almost dissolves them; Zhang et al.
later described SRRM2 and SON as non-redundant scaffold proteins that form
immiscible subphases and regulate separable alternative-splicing target sets.

# External mechanism

SRRM2 encodes the SRm300 component of the SRm160/300 splicing coactivator and
promotes interactions between pre-mRNA-bound splicing factors, snRNPs, and SR
proteins (Blencowe et al., 2000, doi:10.1017/S1355838200991982).  It is also a
core nuclear-speckle protein: the commonly used SC35 speckle antibody mainly
recognizes SRRM2, and SRRM2 with SON provides the major organizing scaffold for
nuclear speckles (Ilik et al., 2020, doi:10.7554/eLife.60579).  SRRM2 has
recently been shown to phase separate and drive nuclear-speckle
subcompartment assembly while regulating a distinct subset of alternative
splicing events from SON (Zhang et al., 2024,
doi:10.1016/j.celrep.2024.113827).  Independent human genetics identifies
heterozygous SRRM2 loss-of-function variants as a neurodevelopmental-disorder
mechanism, so the gene is not a dispensable housekeeping passenger in neurons
(Cuinat et al., 2022, doi:10.1016/j.gim.2022.04.011).  Nuclear ArgRS also
interacts with SRRM2 and changes in nuclear ArgRS/SRRM2 trafficking alter
splice-site usage under arginine-depletion inflammation (Cui et al., 2023,
doi:10.1038/s41556-023-01118-8), consistent with SRRM2 acting at the interface
of speckles, splicing, and nuclear RNA handling.

The causal transfer model I used was:

```text
Srrm2 CRISPR loss of function
-> impaired SRRM2 scaffold and SRm300-dependent speckle/spliceosome coupling
-> altered alternative splicing and nuclear-speckle organization
-> secondary RNA-processing, export, proteostasis, and mature-neuronal
   abundance changes in vulnerable recovered thalamic glutamatergic neurons
-> several hundred whole-gene DEGs in the FDR 0.05 Wilcoxon endpoint
```

This predicts the same broad direction as the `U2af2`, `Tnpo3`, `Cdc40`,
`Prpf6`, and `Rnpc3` anchors because each intervention can limit efficient
pre-mRNA maturation in the P16-to-P37/44 window.  The count is set below those
anchors because SRRM2 is a speckle scaffold with non-redundant, subset-specific
targets rather than a catalytic spliceosome subunit, because the gene-level
assay misses pure isoform changes, and because `Son` shows that a visible
speckle-factor perturbation can be nearly silent in this screen.

# Target-specific prediction

## Srrm2

Zero/nonzero decision: I predict a nonzero effect.  Within the focal training
data, all of `Rnpc3`, `U2af2`, `Cdc40`, `Tnpo3`, `Prpf6`, and `Thoc1` caused
hundreds of DEGs and significantly reduced measured `Srrm2`, so SRRM2 sits in
the same vulnerable RNA-maturation module rather than in the large zero class
of unrelated neurodevelopmental genes.  External biology also makes direct
SRRM2 loss endpoint-bearing for a transcriptional response because SRRM2 is a
spliceosome-associated nuclear-speckle scaffold, not just a downstream marker.

Approximate count: I place `Srrm2` below `Thoc1`/`Prpf6` and well below
`U2af2`/`Rnpc3`, but slightly above the weaker associated RNA-binding anchors
`Hnrnpc`, `Matr3`, `Tardbp`, and `Snrnp70`.  The point estimate is therefore
260 DEGs.

# Limits

No exact same-complex SRRM2 paralog was visible in the training-count file:
`Srrm1`, `Pnn`, `Bclaf1`, `Clk1-4`, and the canonical `Srsf` targets were not
present as perturbations.  `Son` is the closest measured speckle-core
comparison, but SRRM2 and SON are not interchangeable.  Conversely, `Rnpc3`,
`U2af2`, `Cdc40`, `Prpf6`, `Tnpo3`, and `Thoc1` perturb distinct spliceosome,
SR-import, or RNA-export stages, so their large DEG counts can only bound the
expected response, not dictate it.  The Parquet reports whole-gene nuclear RNA
abundance in recovered nuclei; it does not assay splice junctions, intron
retention, SRRM2 protein depletion, nuclear-speckle morphology, DNA indels, or
pre-assay loss of vulnerable cells.  The estimate is accordingly an
extrapolation from biologically adjacent perturbations in the same experiment.
