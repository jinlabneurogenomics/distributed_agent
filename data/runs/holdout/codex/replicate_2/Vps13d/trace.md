# Vps13d forecast trace

## Target and endpoint

- Target: `Vps13d`
- Focal population: `151 TH Prkcd Grin2c Glut`
- Endpoint: measured genes with BH-adjusted Wilcoxon `pvals_adj < 0.05`
- Point forecast: `4`

## Evidence used

### Declared target biology

The declared biology bundle for `Vps13d` reports strong focal reach: the target
feature is available in `151 TH Prkcd Grin2c Glut`, with `Vps13d` detected in
20,815 of 23,679 non-target nuclei, 87.9049% of cells expressing, mean CP10K
1.6016, and mean raw UMI 2.5206.  This supported that a successfully edited
cell in the focal class should usually have target RNA present, while the
bundle explicitly cautions that expression is not an editing-efficiency
measurement.

The same bundle adjudicates Vps13d functional stock as
`likely_substantially_depleted` by the P37-P44 harvest.  The most relevant facts
were that VPS13D supports continuous mitochondrial fission/clearance and
peroxisome biogenesis at organelle contact sites, related Vps13 paralogs do not
replace those tested VPS13D functions, and postnatal mouse neuronal Vps13d loss
has mitochondrial pathology on a week-to-month scale.  That moved the forecast
above a strict zero.

The same biology is still only a partial, survivor-conditioned prior.  The
closest in vivo mouse phenotype was hippocampal/cortical rather than thalamic,
VPS13D protein kinetics in juvenile thalamic neurons are unresolved, and
pre-existing organelles can persist after editing.

### Same-experiment corpus context

The packaged same-experiment corpus had no direct `Vps13d` target report or
Finding, so I did not use any held-out Vps13d transcriptional outcome.

For represented family members, the corpus and the focal count table agreed on
a flat acute neuronal response: `Vps13a`, `Vps13b`, and `Vps13c` each had
0 genes at `pvals_adj < 0.05` in the 151-class count table, and corpus Findings
described Vps13a/Vps13b/Vps13c as transcriptionally flat across the recovered
postnatal neuronal panel.  A high-confidence corpus Claim states that acute
single-gene perturbation of represented VPS13 paralogs does not elicit a shared
basal neuronal transcriptomic module in this screen; its scope explicitly
excludes held-out `Vps13d`.

### Training count table

The declared 151-class training table contains 1,674 targets and is strongly
zero-heavy:

| summary | value |
| --- | ---: |
| minimum | 0 |
| median | 0 |
| 75th percentile | 1 |
| 90th percentile | 2 |
| 95th percentile | 18 |
| maximum | 2677 |
| zero-count targets | 1205 / 1674 |

Counts for hand-selected organelle comparators in the same table:

| group | training perturbations and `n_degs` |
| --- | --- |
| VPS13 paralogs | `Vps13a` 0; `Vps13b` 0; `Vps13c` 0 |
| autophagy / lysosome / mitophagy sparse or flat | `Atg5` 0; `Atg16l1` 0; `Lamp2` 0; `Mff` 0; `Rhot1` 0; `Snca` 0; `Atp13a2` 1; `Park7` 1; `Sqstm1` 1; `Pex14` 1; `Tomm40` 1 |
| focal endomembrane or mitochondrial positives | `Vps35` 17; `Vps54` 31; `Opa1` 37; `Rab7` 501 |

The broad training distribution put a random biological perturbation near 0 or
1; the high Vps13d expression and short-window functional-stock evidence argued
for increasing above that baseline, but the closest VPS13 and
mitophagy/peroxisome comparators argued against a large Opa1- or Rab7-like
signature.

### Parquet profile checks

I aggregated the declared `training_de_all_cell_groups.parquet` over the same
organelle cohort to verify that the 151-class calls were not hiding a broad
family pattern in other classes.  The pattern stayed sparse: all three
represented Vps13 paralogs had no 151-class DEGs, `Vps13c` had only one DEG
outside 151 among the queried groups, `Atp13a2`, `Park7`, `Sqstm1`, `Pex14`,
and `Tomm40` each had a single 151-class hit, and the only appreciable focal
endomembrane/mitochondrial counts were `Vps35`, `Vps54`, `Opa1`, and the much
larger, late-endosomal `Rab7`.

The run-local profile comparison artifact for the selected 18 analogs also
kept the large responders as boundaries rather than close numeric anchors:
9 of 18 selected analogs had no significant 151-class features, 5 had 1-9,
3 had 10-49, and only `Rab7` had at least 50.  The core inspection showed
`Opa1` had 37 significant focal features and `Rab7` had 501, while exact
FDR-significant intersections from `Opa1` or `Rab7` into Vps/endolysosomal
comparators were tiny.

## Synthesis

Vps13d is more likely to be realized by harvest than a generic silent
organelle gene because it is expressed in most 151-class nuclei and supports
renewable mitochondrial/peroxisomal pools.  I therefore did not leave the
forecast at the screen median of zero.

I also did not transfer `Rab7` or `Opa1` directly.  `Rab7` is a proximal late
endosome/lysosome perturbation with a sterol and lysosomal compensation program
that is much broader than Vps-family comparators.  `Opa1` crosses a
mitochondrial ATF4/ISR threshold, but represented mitochondrial fission,
electron-transport, mitophagy, peroxisomal, and VPS13 lipid-transfer targets
usually do not.  The expected survivor-conditioned Vps13d state is therefore a
small FDR footprint, plausibly just above the empirical 90th percentile of 2
but below the Vps35/Vps54/Opa1 17-37 range.

Balancing those anchors, I forecast `4` DEGs.
