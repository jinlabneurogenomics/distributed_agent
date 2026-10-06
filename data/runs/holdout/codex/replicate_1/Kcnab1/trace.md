target: Kcnab1
cell group: 151 TH Prkcd Grin2c Glut
prediction: 1

Evidence used
-------------

- Declared holdout manifest: the one requested target is `Kcnab1`; the
  declared training count table contains 1,674 other targets and no `Kcnab1`
  row.
- Endpoint definition: `n_degs` is the focal-class count of measured genes with
  BH-adjusted Wilcoxon `p < 0.05` in the declared Perturb-seq differential
  expression table.
- Exact target reach from the canonical Kcnab1 biology bundle: in non-target
  `151 TH Prkcd Grin2c Glut` nuclei, `Kcnab1` is readily detected
  (`n_cells_expressing = 18,265 / 23,679`, `pct_cells_expressing = 77.1359`,
  `mean_raw_umi = 2.0391`, `mean_cp10k = 1.2436`). This establishes that a
  Kcnab1 self-transcript row should be observable in the focal population, but
  per the dataset portrait it is not a quantitative editing-efficiency measure.
- Functional biology from the same Kcnab1 bundle: Kcnab1/Kvbeta1 is a
  cytoplasmic auxiliary subunit of native Kv1-family potassium-channel
  complexes. A disruptive edit should stop new Kvbeta1 supply while leaving
  pre-existing Kv1-Kvbeta1 complexes functional until subunit or complex
  turnover. The bundle adjudicates functional stock by the P37-P44 harvest as
  indeterminate because mature-neuron antisense data show replaceable function
  but do not time the loss within the 21-28 day experimental window.
- Count-table scale in `151 TH Prkcd Grin2c Glut`: 1,205 / 1,674 training
  perturbations have `n_degs = 0`; 276 have `n_degs = 1`; the median is 0, the
  90th percentile is 2, the 95th percentile is 18, and the distribution has a
  long tail up to 2,677. Thus a value of 0 or 1 is much more typical than a
  broad response unless a target enters one of the rare high-burden programs.
- Biologically closest focal-class training perturbations:
  - `Kcna1`: `n_degs = 0`; raw focal Parquet top adjusted p-value was 0.3569.
  - `Kcna2`: `n_degs = 0`; raw focal Parquet top adjusted p-value was 1.
  - `Kcnab2`: `n_degs = 1`; the only significant focal row was the self
    transcript (`Kcnab2`, logFC -0.744, q = 4.379e-14), with the next rows at
    q = 0.3021.
- Same-experiment corpus context for those measured analogs, used as
  interpretation of the same Parquet rather than independent replication:
  Kcna1, Kcna2, and Kcnab2 are reported as electrophysiologically plausible
  Kv1/Kv-beta perturbations that are transcriptomically flat or nearly flat in
  the postnatal neuronal nuclear RNA readout. The Kcnab2 report specifically
  records no downstream FDR signal despite significant Kcnab2 RNA depletion in
  multiple groups; the Kcna1/Kcna2/Kcnab2 cross-perturbation reports argue
  against a robust shared Kv1 nuclear-mRNA program.
- Focal ion-channel context also favored singleton self-transcript signatures
  rather than high DEG burdens: in the selected channel genes queried from the
  focal Parquet, Kcnc2, Kcnc3, Kcnma1, Kcnq2, Kcnq3, Scn1a, Scn2a, Scn8a,
  Cacnb4, and Cacna2d1 each had exactly one FDR<0.05 row, which was the edited
  gene itself. Scn1b had two rows. Large focal responses among excitability
  genes existed but were exceptions, e.g. Atp1a3 and Grin1.

Reasoning
---------

The Kv1/Kv-beta neighborhood is the most relevant training evidence because the
Kcnab1 bundle places Kvbeta1 in native Kv1 complexes and names Kcna1/Kcna2 as
interacting alpha subunits and Kcnab2 as the closest represented beta-subunit
loss. These measured analogs argue strongly against a large downstream nuclear
RNA state in the focal thalamic glutamatergic class: Kcna1 and Kcna2 have zero
FDR<0.05 focal genes, and Kcnab2 contributes only its own knocked-down
transcript.

Kcnab1 is not an alpha-pore subunit, and the stock card leaves 21-28 day loss of
installed Kvbeta1 function unresolved, so I did not project a larger
activity/stress or channelopathy program from the adult hippocampal and
antisense literature. The exact focal expression reach does, however, make the
Kcnab1 self-transcript a plausible detectable row. I therefore forecast zero
downstream DE genes plus one self-transcript DE gene:

`predicted_n_degs = 1`
