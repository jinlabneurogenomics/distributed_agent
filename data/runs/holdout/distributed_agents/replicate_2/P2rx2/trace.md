# Question and endpoint

The requested held-out perturbation list contains a single target, `P2rx2`. I
interpreted the endpoint as the exact count of measured genes in `151 TH Prkcd
Grin2c Glut` with `pvals_adj < 0.05` after the P2rx2 CRISPR perturbation,
counting the self-target transcript if it passed the same threshold. The
target was completely held out as a perturbation, so the P2rx2 knockout
signature itself was not available; the prediction has to come from non-held-out
DE signatures/counts plus P2X2 biology.

# Sources used

- Differential-expression parquet:
  `[local file: training_de_all_cell_groups.parquet]`
- Focal training endpoint:
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`
- Held-out manifest:
  `[local file: 164_P2rx2.csv]`
- Same-experiment semantic layer: Distributed Agents corpus
  `perturbai-july-260713-sourceguard-1773-v1`.
- PubMed literature on P2X2/P2RX2 receptor biology.

The Distributed Agents corpus had no target card for `P2rx2` itself, which is consistent
with its held-out status. I therefore used it only for training-gene
neighborhoods such as `P2ry12`, GABA_A/GlyR receptors, glutamate/calcium
channel comparators, and channelopathy genes.

# Dataset computations

I read the focal training count table and used it to calibrate the response
scale in the same cell group:

- 1,674 non-held-out perturbations were present.
- 1,205/1,674 had `n_degs = 0`.
- The median was 0, the 75th percentile was 1, the 90th percentile was 2, and
  the 95th percentile was 18.
- The extreme large signatures were regulators/proteostasis genes, for example
  `Uba5` 2,677, `Tpr` 1,768, `Sin3a` 1,433, and `Rnpc3` 868.

I then scanned the focal `151 TH Prkcd Grin2c Glut` rows of the parquet for a
hand-curated receptor/channel panel containing purinergic receptors,
ligand-gated channels, voltage-gated channels, glutamate receptors, and
calcium-release pathway members. For each training perturbation in that panel I
counted `pvals_adj < 0.05` and inspected the leading adjusted p-values. This
recomputed the same FDR 0.05 endpoint used in the CSV and exposed whether a
one-gene count was just the self-transcript or a broader downstream pattern.

Important focal-cell observations:

- Direct purinergic training targets were flat:
  `P2ry12` had 0 DEGs and no gene with adjusted p below 1 in this focal group;
  `P2ry14` also had 0 DEGs and no gene with adjusted p below 1.
- Closest ligand-gated cation-channel analogs were also mostly flat:
  `Htr3a` 0, `Htr3b` 0, `Chrna7` 0, `Chrnb2` 1, and `Chrna4` 2.
- Inhibitory ligand-gated receptor training targets were sparse:
  `Gabra2` 0, `Gabra3` 0, `Gabrb2` 4, `Gabrd` 2, `Gabrr2` 0,
  `Glra1` 0, `Glra2` 0, `Glra3` 0, and `Glrb` 1. The nonzero cases were
  singletons or a very small `Gabrb2` activity-gene response, not a generic
  ligand-gated-receptor module.
- Ionotropic glutamate receptors were not automatically large: `Gria1`,
  `Gria2`, `Gria3`, `Grin2d`, and `Grin3a` were 0; `Grin2a` was 1 and
  `Grin2b` was 2. The main counterexample was `Grin1` with 89 DEGs, led by
  `Grin1` self-reduction plus `Scg2`, `Stmn4`, `Kctd16`, and other
  NMDA-linked downstream genes.
- Voltage-gated channel comparators were likewise near zero in this focal
  class: `Cacna1a` 0, `Cacna1d` 0, `Cacna1e` 0, `Scn1a` 1, `Scn2a` 1,
  `Scn8a` 1, and `Kcna1` 0. `Cacna1g`, a thalamic T-type calcium-channel
  subunit, was a small outlier at 12.
- `P2rx2` was present as a measured gene in this focal-group universe, but
  across all 1,674 training perturbations its best adjusted p-value as an
  output gene was only 0.906. That does not measure P2rx2 loss directly, but it
  argues that `P2rx2` is not a recurrent marker of the strong transcriptional
  states seen in this group.

# Same-experiment corpus context

The internal corpus reinforced the same boundary conditions:

- The P2ry12-centered corpus card reported that represented
  microglia-lineage purinergic and neuroimmune receptors were flat in the
  NeuN-positive neuronal screen; specifically, `P2ry14`, `Cx3cr1`, `Csf1r`,
  `Ccr2`, `Axl`, and `Mertk` did not form a neuronal downstream RNA module.
  This is only a weak analog for P2X2 because `P2ry12`/`P2ry14` are
  metabotropic and lineage-displaced, while P2X2 is an ionotropic neuronal
  channel.
- The GABA_A corpus claim showed that `Gabrb2` can produce a small
  151-TH activity-associated response, but that related subunits such as
  `Gabra3`, `Gabra2`, `Gabrd`, and `Gabrr2` do not reproduce it. At the exact
  FDR 0.05 endpoint those counts were 0 to 4, which bounds a possible
  ligand-gated-channel response near zero unless the target is an obligatory
  subunit in the sampled circuit.
- The glycinergic receptor claim reported flat, singleton, or non-overlapping
  RNA surfaces for `Glra1`, `Glra2`, `Glra3`, `Glrb`, `Gphn`, and `Slc6a5`.
- Calcium/channelopathy claims reported that `Cacna1a`, `Scn1a`, `Atp1a2`,
  `Itpr1`, `Ryr2`, and `Ryr3` were buffered at the basal postmitotic neuronal
  snRNA level. This makes the absence of broad downstream RNA output after a
  channel perturbation a recurrent observation in this assay, not a surprise.

# External P2rx2 biology

P2X receptors are trimeric ATP-gated cation channels; mutational and structural
work on P2X2 places ATP binding at intersubunit pockets that gate the pore
(Jiang et al., 2011, DOI 10.1073/pnas.1102170108, PMID 21576497).
P2X2 is expressed in selected central and peripheral neurons, with rat CNS
expression described in thalamic as well as sensory, autonomic, brainstem, and
cerebellar regions (Kanjhan et al., 1999, PMID 10213185). Its strongest
knockout phenotypes in mouse point to sensory/autonomic ATP signaling:
P2rx2-null and P2rx2/P2rx3 double-null mice have impaired ATP responses in
sensory and sympathetic ganglia, attenuated pain-related behavior, and reduced
bladder reflexes, while broad CNS behavioral tests in P2rx2-null mice were
normal (Cockayne et al., 2005, DOI 10.1113/jphysiol.2005.088435, PMID
15961431). A later behavioral study likewise found P2X2 dispensable for many
baseline CNS behaviors but necessary for ATP modulation of passive coping
through medial prefrontal cortex infusion (Kong et al., 2020, DOI
10.1111/gbb.12691, PMID 32761745).

That biology makes P2X2 a plausible acute excitability or sensory-signaling
node, but not a known core transcription factor, proteostasis node, or
obligatory thalamic receptor subunit. The experiment was also a basal juvenile
NeuN-positive whole-brain assay, not ATP stimulation, electrophysiology, taste,
cochlea, bladder, or peripheral sensory ganglion physiology.

# Target-specific prediction

## P2rx2

Biologically relevant in-dataset analogs:

- `P2ry12` 0 and `P2ry14` 0: only purinergic perturbations in the focal
  training table. They are weak mechanistic analogs because they are P2Y GPCRs
  and microglia-associated rather than P2X ligand-gated cation channels, but
  they show that purinergic receptor symbols did not create a hidden neuronal
  RNA program in this screen.
- `Htr3a` 0, `Htr3b` 0, `Chrna7` 0, `Chrna4` 2, `Chrnb2` 1: neuronal
  ligand-gated cation-channel comparators. These are closer in receptor logic
  than P2Y receptors and were mostly FDR-flat in the same cell group.
- `Gabra2` 0, `Gabra3` 0, `Gabrb2` 4, `Gabrd` 2, `Gabrr2` 0,
  `Glra1`/`Glra2`/`Glra3` 0 and `Glrb` 1: same-assay ligand-gated
  inhibitory-receptor controls. The small `Gabrb2` counterexample proves that
  receptor perturbations can echo into activity genes when the circuit crosses
  threshold, but the effect was only four genes at FDR 0.05 and did not
  generalize across related subunits.
- `Grin1` 89 and `Cacna1g` 12: counterexamples that a channel can have a
  measurable focal effect. I downweighted them for P2rx2 because `Grin1` is
  the obligatory NMDA receptor subunit and `Cacna1g` is a thalamic T-type
  calcium channel, whereas P2X2 is ATP-gated and context/stimulus dependent.

I therefore predict no gene will clear FDR 0.05. The estimate is mainly driven
by the same-dataset count distribution and the receptor/channel analog panel;
external P2X2 literature was used to avoid overinterpreting the P2Y nulls as
true paralog evidence.

Prediction: `P2rx2 = 0`.

# Limits

The central uncertainty is that no P2X-family perturbation was present in the
training panel; `P2ry12` and `P2ry14` are purinergic only at a high level.
Adult rat P2X2 expression and mouse sensory/autonomic knockout phenotypes do
not resolve whether P2rx2 transcript is efficiently edited and detected in the
held-out `151 TH Prkcd Grin2c Glut` nuclei. A self-target-only hit could move
the true endpoint from 0 to 1 even without downstream biology. The corpus cards
often reason at FDR 0.10, so I used them as qualitative mechanism/boundary
evidence and used the CSV/parquet FDR 0.05 counts for the point estimate.
