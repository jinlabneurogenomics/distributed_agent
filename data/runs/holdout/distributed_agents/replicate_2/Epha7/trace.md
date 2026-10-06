# Question and setup

I interpreted the task as a point prediction of the held-out endpoint
`n_degs` for each manifest target in the exact focal class
`151 TH Prkcd Grin2c Glut`: the number of measured genes, including the
targeted transcript when present, with Benjamini-Hochberg adjusted Wilcoxon
`pvals_adj < 0.05` after acute P16 CRISPR loss of function and P37-P44
single-nucleus RNA-seq. The run manifest contained a single target, `Epha7`,
so no ordering ambiguity remained beyond preserving that one row in
`answer.txt`.

The key ambiguity I resolved was how to treat canonical Eph receptor biology.
`Epha7` is a real neural EphA receptor, but the readout here is a sparse,
postmitotic, survivor-conditioned nuclear RNA signature, not embryonic axon
routing, local cytoskeletal signaling, receptor phosphorylation, spine
morphology, or electrophysiology. I therefore used Eph-family biology to pick
within-dataset analogs, and then let the observed focal DEG counts decide
whether that biology was visible as many DE genes in this assay.

# Sources

Internal, same-experiment sources:

- `[local file: 071_Epha7.csv]`
  named the requested target, `Epha7`.
- `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`
  provided the focal training `n_degs` for 1,674 non-held-out targets.
- `[local file: training_de_all_cell_groups.parquet]`
  provided per-gene log2 fold changes, Wilcoxon scores, FDR values, and matched
  nucleus counts for the non-held-out signatures.
- Distributed Agents selected same-experiment corpus
  `perturbai-july-260713-sourceguard-1773-v1`.
  `target_context(Epha7)` had no direct Epha7 records, so I used target
  contexts for `Epha4`, `Epha5`, and `Ephb2` plus `search_claims` for
  Eph/axon-guidance statements.
- Distributed Agents runtime `profile_neighbors` computed signed
  `logfoldchanges` neighbors in `151 TH Prkcd Grin2c Glut` for `Epha4`,
  `Epha5`, `Epha2`, and `Ephb2` against the full 1,674-target training
  universe.

External biological sources:

- Flanagan and Vanderhaeghen 1998, DOI `10.1146/annurev.neuro.21.1.309`,
  PMID 9530499: Eph receptors/ephrins as membrane-bound positional labels for
  neural topographic maps, pathway choice, and cell migration.
- Bevins, Lemke and Reber 2011, DOI `10.1523/JNEUROSCI.1652-11.2011`,
  PMID 21753007: mouse EphA4/EphA5/EphA6 and an ectopic EphA3 can act
  approximately interchangeably in the retinal EphA gradient for
  retinocollicular mapping.
- Clifford et al. 2014, DOI `10.1073/pnas.1323793111`, PMID 24707048:
  EphA7 signaling constrains cortical dendritic elaboration and contributes to
  spine/synaptic maturation, via local dendritic and synaptic mechanisms.
- Leonard et al. 2020, DOI `10.1371/journal.pone.0231561`, PMID 33275600:
  full-length and truncated EphA7 isoforms are dynamically expressed during
  cortical development and have different effects on dendrites and spines.
- Levy et al. 2021, DOI `10.1111/cge.14017`, PMID 34176129: human `EPHA7`
  haploinsufficiency is associated with variable neurodevelopmental phenotypes,
  supporting developmental relevance but not an acute thalamic soma-RNA
  response.

# Computation

I first calibrated the endpoint distribution in the focal training CSV. It is
zero inflated: 1,205/1,674 targets had `n_degs = 0`, 363 had 1-9 DEGs, 63 had
10-99, and 43 had at least 100. The mean count was 14.1, but the median was 0
and the 75th percentile was 1, so a nonzero prediction for `Epha7` needed
specific support.

I then selected biologically relevant Eph, axon-guidance, and proximal signaling
targets from the training set. In the CSV, the focal Eph counts were:

| training target | focal `n_degs` |
| --- | ---: |
| `Epha2` | 0 |
| `Epha3` | 0 |
| `Epha4` | 1 |
| `Epha5` | 0 |
| `Epha10` | 0 |
| `Ephb1` | 0 |
| `Ephb2` | 0 |
| `Ephb4` | 0 |

I queried only the focal parquet rows for those targets and a small set of
axon-guidance comparators:

```python
filt = (
    (pc.field("group_name") == "151 TH Prkcd Grin2c Glut")
    & pc.field("gene_target").isin(targets)
)
```

That slice had 17,259 measured genes per queried target. It exactly reproduced
the CSV counts. Among the Eph receptors, only `Epha4` had an FDR-significant
gene, and that lone gene was the self-target transcript `Epha4`:
`log2FC = -1.0266`, `pvals_adj = 7.88e-32`. The best non-self rows for
`Epha4`, `Epha5`, `Epha2`, `Epha3`, `Epha10`, `Ephb1`, `Ephb2`, and `Ephb4`
all had `pvals_adj = 1.0` except for two nominal `Epha10` genes with
`pvals_adj = 0.603`, so there was not an almost-significant Eph family program
just below the threshold.

I also checked self-transcript behavior because a one-count prediction could be
caused by `Epha7` mRNA depletion alone. In this focal class, 319/1,642 training
targets with a self row had a significant self transcript. The adjacent
receptors were mixed: `Epha4` was strongly self-depleted, but `Epha5`,
`Epha2`, `Epha3`, `Epha10`, `Ephb1`, `Ephb2`, and `Ephb4` all had FDR 1.0 for
their own transcripts. `Epha7` itself was a measured gene in the focal
signature matrix, but it was not altered by the represented Eph knockouts:
`Epha7` under `Epha4`, `Epha5`, `Epha2`, `Epha3`, `Ephb1`, `Ephb2`, and
`Ephb4` all had FDR 1.0.

For broader counterexamples, the training counts for related guidance or
receptor targets were mostly flat: `Dcc`, `Nrp1`, `Nrp2`, `Ntrk1`, `Ntrk3`,
`Robo2`, `Robo4`, `Rtn4r`, `Sema4d`, `Sema6a`, `Slit2`, and `Unc5d` had 0
DEGs in the focal class. `Robo1`, `Sema5a`, and `Unc5c` had exactly one DEG
each, again their own transcripts; `Ntrk2` had 3, comprising `Ntrk2`, `Atp2a2`,
and `Vgf`. Eph-proximal cytoskeletal/signaling comparators were also
effectively null in the focal class: `Fyn`, `Rac1`, `Kalrn`, `Tiam1`, `Limk1`,
`Chn1`, `Rasa2`, `Sos1`, `Adam10`, `Mapk1`, `Mapk9`, and `Ptpn11` had 0;
`Cdc42` and `Pak1` had 1 each, and `Pak2`/`Pak3` had 0.

The profile-neighbor check did not uncover a hidden Eph module. Pairwise
Spearman correlations among the eight Eph receptor `logfoldchanges` vectors in
the focal class were low, 0.207-0.262. In the Distributed Agents runtime
`profile_neighbors` artifact, anchoring on `Epha4`, `Epha5`, `Epha2`, and
`Ephb2` mostly returned unrelated zero- or one-DEG targets as nearest
neighbors. The only Eph-family neighbor in the top whole-profile neighbors was
`Ephb4`, rank 12 for `Epha4`, and `Ephb4` itself had 0 focal DEGs.

# Target-specific reasoning

## Epha7

Biological role. `Epha7` encodes an EphA receptor tyrosine kinase. Eph/ephrin
signaling is a canonical membrane contact system for developmental axon
guidance and topographic mapping rather than a transcription factor cascade
inside the soma (Flanagan and Vanderhaeghen 1998). EphA receptors can be
partially interchangeable in some guidance settings: EphA4, EphA5, EphA6, and
an ectopic EphA3 contribute similarly to the mouse retinal EphA gradient in the
Bevins/Reber genetic tests (Bevins et al. 2011). EphA7 itself has documented
roles in cortical dendritic and spine development, with full-length and
truncated isoforms modulating dendritic elaboration and synaptic maturation
(Clifford et al. 2014; Leonard et al. 2020), and human dosage evidence links
`EPHA7` deletions to neurodevelopmental phenotypes with variable expressivity
(Levy et al. 2021).

Most appropriate in-dataset analogs.

- `Epha5`, focal `n_degs = 0`: the closest same-family A-class comparator in
  the training endpoint. The Distributed Agents corpus reported that `Epha5` was
  mostly flat and that its one all-atlas downstream event in a limbic/mixed
  glutamatergic group did not converge with `Epha2`, `Epha3`, `Epha4`,
  `Epha10`, `Ephb1`, `Ephb2`, or `Ephb4`.
- `Epha4`, focal `n_degs = 1`: the strongest Eph focal analog, but its sole
  focal FDR hit was the `Epha4` self transcript; there was no downstream
  `151 TH Prkcd Grin2c Glut` program. Corpus finding `Epha4:F004` described
  represented Eph receptors and Rho/Pak actin nodes as not phenocopying
  `Epha4`.
- `Epha2`, `Epha3`, `Epha10`, `Ephb1`, `Ephb2`, `Ephb4`, focal `n_degs = 0`
  for each: useful as boundaries against a generic Eph-family response.
  Corpus claim `claim:2d52a03dd54eace8a29f` summarized the same-experiment
  Eph evidence as flat, singleton-only, or non-overlapping rather than a
  common Eph-family nuclear transcriptomic program in postnatal neurons.
- `Fyn`, `Rac1`, `Cdc42`, `Pak1`, `Pak2`, `Pak3`, `Kalrn`, and `Tiam1`,
  focal `n_degs = 0-1`: these lie on Eph/Rac/PAK actin or spine-signaling
  branches. They did not create a recurrent focal mRNA module, matching the
  corpus interpretation that the represented Rac/Cdc42-linked actin
  perturbations are transcriptionally buffered in juvenile neurons.
- `Dcc`, `Slit2`, `Robo1/2/4`, `Unc5c/d`, `Nrp1/2`, and semaphorin-family
  targets: these are mechanistic counterexamples from other axon-guidance
  pathways. Most were zero in this exact focal class, and the few nonzeros
  were self-only singleton hits. Corpus search found a high-confidence
  axon-guidance claim stating that represented DCC/UNC5/DSCAM and Slit/Robo
  perturbations did not produce a convergent robust neuronal soma
  transcriptomic module in this assay.

Decision. The within-dataset evidence is the driver. Seven of eight represented
Eph receptors were focal zeros and the eighth, `Epha4`, contributed only its
own transcript. The same-experiment semantic corpus independently summarizes
the broader Eph neighborhood as non-convergent in this postnatal snRNA-seq
assay. External biology makes `Epha7` plausible for wiring and synaptic
phenotypes, but those are localized/developmental outputs and the acute P16
mosaic loss experiment did not turn close Eph or guidance receptors into broad
thalamic soma RNA signatures. I therefore predict that `Epha7` will also be
below the focal FDR threshold and assign `predicted_n_degs = 0`.

# Limits

- `Epha7` was completely held out, and the Distributed Agents corpus had no direct
  `Epha7` finding. The prediction is extrapolated from represented Eph family
  members, especially `Epha5` and `Epha4`.
- Ephrin-A ligands and `Epha6` were not present as training perturbations, so
  ligand-side and exact EphA6/EphA7 comparisons could not be tested.
- A zero prediction is about FDR-significant nuclear mRNA in recovered
  `151 TH Prkcd Grin2c Glut` nuclei. It does not imply failed editing, no
  EphA7 protein phenotype, no dendritic/spine effect, and no developmental
  consequence in embryonic or cortical settings.
- The self-transcript component is uncertain. Some focal one-DEG receptor
  responses were only self-depletion events. `Epha7` could score a single
  self hit if its guides drive strong nonsense-mediated decay in this cell
  group, but the adjacent Eph receptor evidence did not justify making that
  the point estimate.
