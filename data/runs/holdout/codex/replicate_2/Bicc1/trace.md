target: Bicc1
cell class: 151 TH Prkcd Grin2c Glut
prediction: 1

I treated the held-out target as a low, but not impossible, responder.

Key target biology:

- The canonical Bicc1 biology bundle exposes focal expression but not the
  target endpoint. In the exact focal population, Bicc1 was detected in
  9519 / 23679 non-target nuclei, 40.200% of cells, with mean raw UMI 0.610,
  mean CP10K 0.380, and pseudobulk CPM 38.209.
- The molecular lesion is plausible over 21-28 days but delayed. Bicc1 is a
  cytoplasmic KH/SAM RNA-binding protein whose SAM-dependent polymers bind,
  localize, and silence mRNAs. A P16 CRISPR lesion stops new Bicc1 supply but
  does not immediately remove pre-existing RNA-bound polymers, and the card
  adjudicates the P37-P44 harvest state as only
  `partially_depleted_or_leading_edge`.
- Constitutive Bicc1 loss causes strong developmental renal/systemic disease,
  but that evidence was explicitly discounted for this endpoint because it
  does not establish an acute postnatal thalamic-neuron requirement.

Training evidence:

- The declared `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` table has
  1674 training targets; Bicc1 is absent. Counts are very sparse: 1205 / 1674
  have 0 DEGs, the median is 0, Q75 is 1, and Q90 is 2, with a heavy outlier
  tail.
- Species-safe analog nomination against the actual training universe found no
  exact Bicc1 paralog, narrow module, direct-interaction candidate, or
  reciprocal same-experiment corpus comparator. All 1184 available nominees
  came from `broad_functional_fallback` annotations, so none was strong enough
  to transfer as an equal-scale direct donor.
- The narrowest annotated mRNA-catabolic candidates were `Ski`, `Xrn1`, and
  `Reg1`, with observed focal counts 2, 20, and 0. I treated `Xrn1 = 20` as an
  upper local reference because Xrn1 is a core exonuclease, not a Bicc1-like
  adaptor/localizer.
- A hand-inspected cytoplasmic silencing / RNA-localization set was mostly
  quiet: `Ago1 = 1`, `Ago2 = 0`, `Tnrc6a = 0`, `Tnrc6b = 0`, `Cnot1 = 0`,
  `Eif4a2 = 2`, `Eif4h = 1`, `Fmr1 = 0`, `Fxr1 = 0`, `Dicer1 = 0`,
  `Syncrip = 0`, alongside `Ski = 2`, `Reg1 = 0`, and `Xrn1 = 20`.
  The central tendency of that operation-matched set is therefore at or just
  above zero.
- The high-count RNA genes in the broad RNA-binding annotation pool were
  mechanistically off-axis nuclear processing or broader transcriptional
  regulators: `U2af2 = 828`, `Hnrnpu = 733`, `Cdc40 = 624`,
  `Tardbp = 210`, `Hnrnpc = 122`; `Ctnnb1 = 383` was a broad Wnt/kidney
  boundary. The profile comparisons on the declared Parquet kept these
  outliers visible but did not justify pulling Bicc1 onto their scale.

Parquet profile check:

- I compared two focal-class signed-profile cohorts from
  `training_de_all_cell_groups.parquet`: the top 30 Bicc1 nominees and a
  19-node cytoplasmic-silencing set with the high outliers retained as
  boundaries.
- In the 30-node broad cohort, 19 / 30 nodes had no significant focal-class
  features, 3 had 1-9, 2 had 10-49, and 6 had at least 50.
- In the 19-node operation-focused cohort, 9 / 19 nodes had no significant
  focal-class features, 4 had 1-9, 1 had 10-49, and 5 had at least 50. The
  negative tails were shared more than positive tails
  (median top-tail overlap 0.264 vs 0.132), consistent with weak common
  direction across RNA perturbations, but the closest Ago/Tnrc/Cnot/Dicer/Fmr
  perturbations still did not cross the BH threshold in this cell class.

Synthesis:

Bicc1 is expressed in enough thalamic neurons that a nonzero survivor-state
signature is possible, and polymeric stock should at least partly turn over by
harvest. The same target biology also argues against a broad acute response:
the assay averages over Bicc1-low nuclei, the functional stock is not assured
to be fully cleared, and the severe mouse phenotype is developmental and
non-neural. Training analogs that most closely match cytoplasmic
post-transcriptional silencing sit at 0-2 DEGs, while the 20+ and 100+ count
examples come from more central mRNA decay, spliceosome, hnRNP, or Wnt
perturbations. I therefore forecast the held-out Bicc1 DEG count as a
low-single-digit value and rounded the point to 1.
