# Task interpretation

The held-out target list contains one perturbation, `Slc12a5`.  The quantity to
predict is the number of measured genes with `pvals_adj < 0.05` in the held-out
`Slc12a5` CRISPR loss-of-function profile for `151 TH Prkcd Grin2c Glut`.  By
construction the `Slc12a5` perturbation itself is absent from both the
differential-expression parquet and the focal-cell training count CSV, so the
prediction has to be transferred from non-held-out targets.

I treated a direct FDR hit on the perturbed gene's own RNA as part of
`n_degs`, because the training endpoint is literally the count of all measured
genes passing FDR, and many ion-channel and receptor perturbations in the focal
cell group have exactly this pattern: the target transcript itself is the only
DEG.

# Sources used

- `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]` for observed `n_degs` in the focal cell group.
- `[local file: training_de_all_cell_groups.parquet]` for focal-cell effect sizes and adjusted P values of mechanistic analogs.
- Distributed Agents same-experiment corpus, release `perturbai-july-260713-sourceguard-1773-v1`, via `target_context` and `candidate_set_topology`.  `Slc12a5` was absent from this frozen corpus; `Slc12a2` was present and had curated negative findings.
- Distributed Agents runtime profile comparison `profile_compare_chloride.json`, computed from the DE parquet for a caller-declared cohort of chloride transport, GABA receptor, sodium-channel, potassium-channel, and NMDAR perturbations in `151 TH Prkcd Grin2c Glut`.
- PubMed literature for KCC2 biology: Rivera et al. 1999, DOI `10.1038/16697`, PMID `9930699`; Huebner et al. 2001, DOI `10.1016/s0896-6273(01)00297-5`, PMID `11395011`; Blaesse et al. 2009, DOI `10.1016/j.neuron.2009.03.003`, PMID `19323993`; Kaila et al. 2014, DOI `10.1038/nrn3819`, PMID `25234263`; Gauvain et al. 2011, DOI `10.1073/pnas.1107893108`, PMID `21878564`.

# Computation over the supplied data

I first used the count CSV to calibrate response breadth.  The focal-cell
training set has 1,674 perturbations; 72.0% have exactly zero DEGs, the median
is 0, the 75th percentile is 1, the 95th percentile is 18, and the maximum is
2,677.  In other words, a biologically real ion-transport or synaptic
perturbation has to overcome a strong empirical prior toward a null or
near-null nuclear RNA profile.

I queried the parquet with DuckDB using
`group_name = '151 TH Prkcd Grin2c Glut'`, then inspected mechanistic analogs.
Each observed analog had 17,259 measured genes in the focal cell group and
roughly 90 to 283 matched perturbed nuclei against 23,679 matched controls,
depending on target, so the flat calls below are not explained by a total lack
of matched cells.

I also checked the measured `Slc12a5` feature across the 1,674 non-held-out
focal-cell profiles.  Its log-fold changes are finite and small, with median
absolute log2FC 0.050 and 99th percentile 0.232; five broad perturbations
changed it at FDR 0.05.  That makes `Slc12a5` look like a detectable neuronal
transcript in this cell group, unlike `Slc12a2`, whose own transcript was not
detectably reduced after `Slc12a2` perturbation.

# Slc12a5-specific reasoning

`Slc12a5` encodes KCC2, the neuron-enriched K-Cl cotransporter that extrudes
chloride and helps make GABA_A and glycine receptor currents hyperpolarizing in
mature neurons.  Rivera et al. 1999 showed that KCC2 induction is coupled to the
developmental GABA polarity switch, Huebner et al. 2001 showed that full KCC2
loss disrupts early synaptic inhibition in knockout mice, and Blaesse et al.
2009 and Kaila et al. 2014 summarize KCC2/NKCC1/WNK-SPAK regulation as a core
chloride-homeostasis axis.  KCC2 also has transporter-independent synaptic
roles, including actin/dendritic-spine effects described by Gauvain et al.
2011.  None of those mechanisms implies that acute, partial, mosaic P16 editing
must produce a large basal snRNA-seq response 3 to 4 weeks later.

The closest direct cation-chloride cotransporter in the training set was
`Slc12a2`/NKCC1.  It had `n_degs = 0` in `151 TH Prkcd Grin2c Glut`, and its own
RNA was only log2FC -0.147 with adjusted P = 1.0.  The Distributed Agents corpus further
curates `Slc12a2` as pan-neuronally FDR-null in this screen and reports no
shared FDR-level transcriptional convergence among represented WNK/SPAK/CCC
pathway members.  The focal-cell counts agree: `Wnk1` 0, `Stk39` 0, `Strada` 0,
`Prkca` 0, and `Wnk3` only 1.  This is the strongest within-dataset evidence
that cation-chloride physiology is largely buffered, post-translational, or
invisible to this RNA endpoint.

I used represented chloride and bicarbonate transporters as additional
boundaries.  `Slc4a7` had 0 DEGs; `Clcn3` had 0; `Clcn4` had 1, consisting of a
strong self-transcript hit (`Clcn4` log2FC -0.802, adjusted P
`6.72e-11`) without a broader downstream program.  This pattern again favors a
count near zero, while showing that a high-confidence self RNA decrease can
produce a one-gene endpoint.

GABA_A receptor perturbations are the most relevant downstream chloride-channel
counterexamples.  `Gabra1` had 1 DEG, its own transcript; `Gabra2`, `Gabra3`,
`Gabra5`, `Gabrb1`, `Gabrb3`, `Gabrg3`, and `Gabrr2` were zero; `Gabrd` had 2;
and `Gabrb2` had 4.  The only `Gabrb2` downstream genes at FDR were a small
activity-like set (`Nr4a1` up, `Vgf` up, `Nalf1` down) in addition to `Gabrb2`
itself.  The Distributed Agents corpus explicitly notes that `Slc12a2` did not
phenocopy these small GABA_A receptor activity signatures.  If removing a
major postsynaptic GABA_A subunit usually produces zero to four DEGs, reducing
the chloride gradient through KCC2 is unlikely to produce hundreds.

Other electrical-excitability genes in the same cell group were also tiny:
`Kcnq1` 0, `Kcnq2` 1, `Kcnq3` 1, `Kcnb1` 0, `Scn1a` 1, `Scn1b` 2, `Scn2a` 1,
and `Scn8a` 1.  Those direct channel losses can strongly affect firing yet,
in this assay, were mostly counted only through self-transcript knockdown.

The main nonzero counterexample was the NMDAR obligate subunit `Grin1`, which
had 89 DEGs in the focal group, with `Grin1` itself down and additional
synaptic/activity genes such as `Scg2`, `Stmn4`, `Kctd16`, and `Gpm6a`
up-regulated.  I did not transfer that larger value to `Slc12a5`, because
`Grin2a` and `Grin2b` had only 1 and 2 DEGs respectively in the same focal
group, and the Distributed Agents corpus reports that represented NMDAR subunits did not
phenocopy each other in this postnatal CRISPR transcriptome.  A broad response
therefore looks like a `Grin1`-specific exception, not the generic result of
altered inhibition or excitation.

I predict a very small nonzero response, `n_degs = 1`.  The zero-response
argument is strong for downstream genes: the best transporter and WNK/SPAK
analogs are flat, GABA_A receptor perturbations are narrow, and K+/Na+ channel
perturbations rarely exceed their own knocked-down transcript.  I still chose
one rather than zero because `Slc12a5` is a robustly detectable mature-neuron
transcript in this focal group, so an on-target CRISPR-induced RNA decrease is
more plausible for KCC2 than it was for the low-response `Slc12a2` profile.

# Limits

The direct KCC family members `Slc12a4`, `Slc12a6`, and `Slc12a7` were not in
the training perturbation universe, so `Slc12a2` is a mechanistic analog but
not a paralog with identical direction of chloride flux or adult neuronal
expression.  `Oxsr1` was also absent, and the WNK/SPAK evidence is restricted
to `Wnk1`, `Wnk3`, `Stk39`, `Strada`, and `Prkca`.

The assay measures nuclear RNA after sparse AAV CRISPR, not chloride reversal
potential, surface KCC2, phosphorylation, seizure susceptibility, dendritic
spine morphology, or the survival phenotypes seen in stronger KCC2 models.
Thus, the prediction extrapolates from transcriptomic analogs and is compatible
with substantial electrophysiological effects that leave few or no FDR-level
RNAs.  The largest uncertainty is guide/on-target behavior for `Slc12a5`
itself: if the KCC2 transcript does not pass FDR in the held-out profile, the
same reasoning would have yielded a pure zero.
