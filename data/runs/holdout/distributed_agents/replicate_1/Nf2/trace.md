# Nf2 DEG-count prediction for `151 TH Prkcd Grin2c Glut`

## Question and endpoint

The requested target set contains one held-out perturbation:

```tsv
target_name
Nf2
```

I interpreted the target as a mouse `Nf2` loss-of-function perturbation scored in
`151 TH Prkcd Grin2c Glut` thalamic glutamatergic neurons. The quantity to
predict is the assay-specific `n_degs`: the number of measured transcripts with
Benjamini-Hochberg-adjusted Wilcoxon `pvals_adj < 0.05` for that perturbation in
that focal cell group. Because held-out signatures are absent from both supplied
inputs, the endpoint is absent for `Nf2`; the training count CSV is a direct
measurement for other perturbations and the Parquet is a direct source for their
gene-by-gene focal and non-focal DE patterns.

I resolved one ambiguity explicitly: a count of 1 in the training file can be
driven entirely by the perturbed target's own transcript. I treated that as
evidence for a near-null downstream state, not as evidence for a broad response,
because the dataset portrait warns that target-RNA loss is not a quantitative
editing-efficiency or biological-effect metric.

## Sources used

- Direct dataset: `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
- Direct dataset: `training differential-expression dataset`.
- Requested-target manifest: `single-target request for Nf2`.
- Internal same-experiment corpus: `perturbai-july-260713-sourceguard-1773-v1`, used only for compact Tead1/Cdc42/Dlg4/Mark3/Taok1 report interpretations. I found no Nf2 target report or Nf2 comparator Finding in this corpus.
- External literature:
  - Lavado et al. 2013, DOI `10.1242/dev.096537`, PMID `23863479`: Nf2/Merlin constrains neural progenitor expansion by inhibiting Yap/Taz activity.
  - Cockburn et al. 2013, DOI `10.1016/j.cub.2013.05.044`, PMID `23791728`: Nf2 acts upstream of Lats1/2-dependent Yap phosphorylation in the early embryo.
  - Primi et al. 2021, DOI `10.1016/j.mbplus.2021.100074`, PMID `34337379`: Merlin is a FERM-family Lats-binding tumor suppressor that links cortical membrane/cytoskeleton organization with Hippo signaling.
  - Kim and Gumbiner 2019, DOI `10.1073/pnas.1819400116`, PMID `31043565`: Nf2/Merlin can regulate TEAD activity and palmitoylation in cell-contact/Hippo contexts.
  - Murakoshi et al. 2011, DOI `10.1038/nature09823`, PMID `21423166`: Cdc42/Rho actin signaling operates in dendritic-spine structural plasticity, supporting Cdc42/Rac1 as pathway-adjacent neuronal counterexamples rather than as Hippo-specific analogs.

## Dataset calibration

The focal endpoint CSV contains 1,674 training perturbations. Its distribution is
zero-heavy:

```text
zero DEG perturbations: 1205 / 1674 = 71.98%
median n_degs: 0
75th percentile: 1
90th percentile: 2
95th percentile: 18
maximum: 2677
```

I then selected biologically interpretable, visible perturbations around Nf2's
known axes: Hippo/Yap/TEAD signaling, polarity kinases, adherens/PSD scaffolds,
and Rho-family actin regulation. I recomputed the focal count from the Parquet by
filtering `group_name == "151 TH Prkcd Grin2c Glut"` and summing
`pvals_adj < 0.05` for each candidate; this matched the supplied endpoint CSV.

```tsv
training_target	focal_n_degs	all_neuronal_group_n_degs	why inspected
Tead1	0	0	visible YAP/TAZ transcription-factor output partner downstream of Hippo
Taok1	0	0	visible upstream Hippo/MARK-family kinase
Mark3	0	1	visible MARK/polarity kinase connected to Hippo and cytoskeleton regulation
Ctnna2	0	0	neuronal adherens-junction catenin
Ctnna3	0	0	adherens-junction catenin
Flnb	0	0	cortical actin scaffold
Rac1	0	1	Rho-family actin regulator
Cdc42	1	1	Rho-family actin regulator; the one focal FDR hit was Cdc42 itself
Dlg4	1	2	neuronal PSD scaffold counterexample; the one focal FDR hit was Dlg4 itself
```

The same-experiment corpus interpretations reinforced the raw counts: Tead1 was
FDR-flat across measured neuronal classes with no YAP/TEAD target module; Taok1
was flat across recovered neuronal groups; Mark3 showed only a restricted
one-gene off-focal response; Cdc42 had no robust downstream actin/Rho/synaptic
mRNA program despite significant self-transcript loss in the focal class; and
Dlg4 was globally close to transcriptionally flat even though Dlg4 RNA itself was
reduced.

I also inspected two tempting but weaker counterexamples:

```tsv
training_target	focal_n_degs	all_neuronal_group_n_degs	interpretation
Ctnnb1	383	393	large Wnt/adherens response, but beta-catenin loss is not the same acute intervention as Merlin loss
Tsc2	86	423	large mTOR response, but tumor-cell NF2-to-mTOR coupling is indirect and context dependent
```

These high-count perturbations show that the focal class had enough power to
detect broad responses, but I did not transfer their magnitudes to Nf2 because
neither is an obligate Nf2 effector in postmitotic thalamic glutamatergic neurons
3-4 weeks after sparse AAV CRISPR delivery.

## Target-specific reasoning

### Nf2

Nf2 encodes Merlin, a FERM-domain membrane/cytoskeletal tumor suppressor that can
promote LATS-dependent inhibition of YAP/TAZ and can also organize
contact-dependent TEAD regulation. In embryos and neural progenitor cells,
Nf2 loss can derepress Yap/Taz and alter proliferation or lineage allocation
(Cockburn et al. 2013; Lavado et al. 2013), so the strongest prior is a
developmental/proliferative Hippo role.

The requested experiment is different at every stage of that causal chain:

1. Intervention: partial, mosaic CRISPR loss of function started at P16.
2. Direct molecular consequence: reduced Merlin function in already specified
   postmitotic neurons, not in apical neural progenitors or dividing Schwann,
   epithelial, or tumor cells.
3. Propagation: any effect would have to pass through mature-neuron
   membrane/cytoskeletal or YAP/TEAD machinery.
4. Exposure and selection: the measured state is 3-4 weeks post-perturbation in
   recovered NeuN-positive nuclei.
5. Endpoint: FDR-significant nuclear RNA changes, not YAP localization,
   palmitoylation, proliferation, cell geometry, spine morphology, or survival.

Visible perturbations that probed the downstream transcriptional end of this
chain were silent. `Tead1` was `0` in the focal group and across the whole
measured neuronal panel, and the internal report specifically found no expected
YAP/TEAD or cortical Tead target module after Tead1 perturbation. Visible
upstream or polarity kinases (`Taok1`, `Mark3`) were also flat in the focal
group. Actin/synaptic counterexamples that should have revealed a durable
cytoskeletal RNA signature if this axis were broadly transcription-coupled in
mature neurons were at the null boundary: `Cdc42` and `Dlg4` each had only their
own transcript as a focal FDR hit, while `Rac1`, `Flnb`, `Ctnna2`, and `Ctnna3`
had no focal FDR hits.

This does not prove Merlin is biologically irrelevant in thalamic neurons. The
prediction is narrower: an acute P16 Nf2 perturbation is unlikely to create a
large enough recovered-nucleus RNA shift to pass BH FDR 0.05 in this focal cell
group. The developmental Nf2-Yap/Taz literature is displaced to embryonic or
progenitor contexts, and the cancer literature couples NF2 loss to YAP/TEAD, PAK,
and mTOR in proliferative Schwann, mesothelial, epithelial, or hepatic cells. I
therefore weighted the directly measured near-null Tead1/Taok1/Mark3/Cdc42/Dlg4
training analogs more heavily than those external proliferative models.

Predicted `Nf2` count: `0`.

## Limits and uncertainty

The prediction is extrapolative because no true Nf2 perturbation signature is
present in the supplied inputs and the internal same-experiment corpus has no Nf2
report. The most specific measured Hippo/YAP analog in the training set is
`Tead1`; core components such as `Lats1`, `Lats2`, `Sav1`, `Stk3`, `Stk4`,
`Yap1`, `Wwtr1`, `Amot`, `Msn`, and `Ezr` were not in the focal training-count
CSV, so the comparison misses several direct Merlin partners. A sparse CRISPR
screen can also miss phenotypes if Nf2 loss primarily affects neuronal position,
synaptic physiology, YAP phosphorylation/localization, or pre-assay survival
rather than steady-state nuclear mRNA in recovered cells. The final integer is
therefore a low-count prediction with substantial biological uncertainty, but
zero is the most likely FDR-count outcome given the training perturbations
available in this endpoint.
