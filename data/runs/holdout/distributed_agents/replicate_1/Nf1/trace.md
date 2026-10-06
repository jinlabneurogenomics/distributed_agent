# DEG-count prediction trace

## Question interpreted

The requested held-out perturbation is `Nf1`. I interpreted the readout as the
integer number of measured genes with `pvals_adj < 0.05` in the held-out `Nf1`
signature for `151 TH Prkcd Grin2c Glut` cells. This endpoint is an observed
single-nucleus Wilcoxon DEG burden in recovered NeuN+ nuclei after P16 sparse
AAV CRISPR loss of function and P37-P44 harvest. I did not treat it as a direct
measurement of editing rate, neurofibromin protein loss, Ras activity, cell
survival, firing, cell size, or biological importance.

The training count CSV counts every significant measured gene in this focal
cell class. Some comparator counts therefore include a significant target
self-transcript, as in `Ntrk2`, `Grin1`, `Gabrb2`, `Dlg4`, and `Camk2b`; the
held-out `Nf1` self-row was absent with the rest of the `Nf1` signature and was
not available for calibration.

## Sources used

- Declared input counts:
  `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
  This supplied the endpoint for 1,674 non-held-out perturbations.
- Declared differential-expression Parquet:
  `training differential-expression dataset`.
  I filtered it to `group_name == "151 TH Prkcd Grin2c Glut"` and candidate
  analogs/counterexamples, then inspected the genes, directions, adjusted
  p-values, and matched perturbed/control nucleus counts crossing `pvals_adj <
  0.05`.
- Requested-target manifest:
  `single-target request for Nf1`.
  It contained one target, `Nf1`, with no duplicate requested symbols and no
  overlap with the training endpoint CSV.
- Run-local metadata:
  `task_bindings.json`, `coverage.json`, `dataset_context.md`, and
  `capabilities.json`. These identified the focal cell label exactly and showed
  that rank-calibration and predictive graph-review tools were not authorized
  for this scalar-count task.
- Same-experiment semantic corpus:
  PerturbAI July `july_260713_sourceguard_1773_v1` reports and Finding ledgers,
  read through the bounded `read_reports.py` and `query_ledger.py` entrypoints.
  There was no packaged `Nf1` report. I used reports for measured analogs
  including `Tsc2`, `Depdc5`, `Braf`, `Raf1`, `Syngap1`, `Ntrk2`, and `Gabrb2`
  to avoid interpreting isolated DEGs without the corpus' same-assay
  comparison context.
- External literature, via PubMed:
  Scheffzek and Shivalingaiah 2019, DOI `10.1101/cshperspect.a031500`,
  PMID `30104198`; Bergoug et al. 2020, DOI `10.3390/cells9112365`,
  PMID `33121128`; Oliveira and Yasuda 2014, DOI
  `10.1523/JNEUROSCI.3096-13.2014`, PMID `24431436`; Hennig et al. 2016, DOI
  `10.1186/s12964-016-0128-z`, PMID `26861207`; Cui et al. 2021, DOI
  `10.1093/hmg/ddaa263`, PMID `33331896`; Dibble et al. 2012, DOI
  `10.1016/j.molcel.2012.06.009`, PMID `22795129`; Bar-Peled et al. 2013,
  DOI `10.1126/science.1232044`, PMID `23723238`.

## Computational checks over the declared inputs

I first read the requested manifest and the focal-cell training counts. The
manifest had exactly one row after the header:

```tsv
target_name
Nf1
```

The training count CSV had 1,674 unique `target_name` values. `Nf1` was absent,
as required. The focal readout was sparse:

```text
min = 0
median = 0
75th percentile = 1
90th percentile = 2
95th percentile = 18
99th percentile = 436.48
max = 2677
nonzero perturbations = 469 / 1674
```

I then filtered the Parquet to the focal cell group and biologically relevant
training perturbations, using exact `pvals_adj < 0.05` to match the requested
endpoint. The closest Ras/MAPK and mTOR comparison counts in `151 TH Prkcd
Grin2c Glut` were:

| training perturbation | `n_degs` | focal expression-pattern evidence |
|---|---:|---|
| `Spred1` | 0 | no focal FDR<0.05 genes; best adjusted p-value 0.638 |
| `Spred2` | 0 | no focal FDR<0.05 genes; all adjusted p-values 1.0 |
| `Rasa2` | 0 | no focal FDR<0.05 genes; best adjusted p-value 0.257 |
| `Syngap1` | 0 | no focal FDR<0.05 downstream genes; the self-transcript was subthreshold, logFC -0.343, FDR 0.117 |
| `Hras` | 0 | no focal FDR<0.05 genes; all adjusted p-values 1.0 |
| `Kras` | 0 | no focal FDR<0.05 genes; all adjusted p-values 1.0 |
| `Sos1` | 0 | no focal FDR<0.05 genes; only `Cul7` was near the cutoff, FDR 0.0778 |
| `Ptpn11` | 0 | no focal FDR<0.05 genes; all adjusted p-values 1.0 |
| `Raf1` | 0 | no focal FDR<0.05 genes; all adjusted p-values 1.0 |
| `Mapk1` | 0 | no focal FDR<0.05 genes; all adjusted p-values 1.0 |
| `Shoc2` | 1 | only `Vgf` was significant, logFC -0.660, FDR 0.00794 |
| `Braf` | 4 | `Vgf`, `Ptpn5`, `Atp2a2`, and `Unc13a` were all down |
| `Map2k1` | 4 | `Vgf`, `Ptpn5`, `Etv5`, and `Unc13a` were all down; it shared same-direction `Vgf`, `Ptpn5`, and `Unc13a` with `Braf` |
| `Ntrk2` | 3 | self `Ntrk2`, `Atp2a2`, and `Vgf` were down; the two downstream genes overlapped same-direction with `Braf` |
| `Mtor` | 2 | only `Rims3` up and `Tmed8` down were significant |
| `Depdc5` | 13 | sterol/PI3K state: `Ldlr`, `Insig1`, `Hmgcs1`, `Msmo1`, `Pik3r1`, and `Pik3r3` up, with `Rnpc3` and `Amy1` down |
| `Tsc2` | 86 | broader mTORC1-like sterol, lysosomal, and feedback state with `Cyp51`, `Pik3r3`, `Slc2a6`, `Hmgcr`, `Ldlr`, `Dusp1`, `Ddit4`, `Grn`, `Dpp7`, `Rragd`, and `Lamp2` among the significant genes |
| `Srebf2` | 7 | sterol genes including `Dhcr24`, `Insig1`, `Hmgcs1`, `Msmo1`, `Cyp51`, and `Sqle` went down, opposite to the `Depdc5`/`Tsc2` sterol arm |
| `Gabrb2` | 4 | self `Gabrb2` down, with `Nr4a1` and `Vgf` up |
| `Atp2b1` | 22 | activity/neuropeptide-like induction including `Fos`, `Nr4a1`, `Vgf`, `Cck`, `Opn3`, and `Gpr88` |

Two explicit focal overlaps mattered:

- `Tsc2` and `Depdc5` shared eight FDR<0.05 genes in the same direction
  (`Amy1`, `Ldlr`, `Msmo1`, `Pik3r1`, `Pik3r3`, `Rnpc3`, `Snhg11`,
  `Tubb3`), supporting a real but target-position-dependent mTORC1/sterol
  branch.
- `Braf` and `Map2k1` shared `Vgf`, `Ptpn5`, and `Unc13a` down in the same
  direction, and `Ntrk2` shared down-regulated `Vgf` and `Atp2a2` with `Braf`.
  These are loss-of-positive-signaling signatures, so their sign is the
  opposite biochemical prior for `Nf1` loss even though they mark a Ras/ERK
  responsive module.

## Target-specific biological reasoning

### `Nf1`

`Nf1` encodes neurofibromin, a Ras-specific GTPase-activating protein that
accelerates Ras-GTP hydrolysis. Loss of neurofibromin should therefore release,
not inhibit, Ras signaling. RasGAP mechanism and neurofibromin's central role
are reviewed by Scheffzek and Shivalingaiah 2019, and neurofibromin is also
linked to Akt/mTOR, ROCK/LIMK/cofilin, and cAMP/PKA pathways in the broader
cell literature (Bergoug et al. 2020). In neurons, Oliveira and Yasuda 2014
showed that neurofibromin supplies most Ras inactivation in CA1 dendritic
spines after synaptic stimulation and that neurofibromin loss can make Ras
activation sustained. Hennig et al. 2016 similarly placed neurofibromin in
feedback termination of growth-factor-induced Ras signals. A separate
Schwann-cell study showed cooperation among neurofibromin, Spred1, and merlin
in suppressing Ras-Erk output (Cui et al. 2021), reinforcing `Spred1` as a
reasonable, though not neuronal, same-direction suppressor comparator.

The nearest same-direction perturbations in the training screen were the Ras
negative regulators `Spred1`, `Spred2`, `Rasa2`, and `Syngap1`. All had zero
focal DEGs at FDR 0.05. `Syngap1` is a postsynaptic Ras/Rap GAP rather than the
same protein complex as NF1, but its internal report is relevant because it
tested the strongest "remove a neuronal RasGAP" precedent in this exact P16
CRISPR, P37-P44 snRNA-seq design: the perturbation had 0 downstream FDR<0.10
genes in every measured neuronal group and no robust full-surface signature
neighbor. That result is not proof that RasGAP loss is inert at the synapse; it
says that this nuclear RNA assay did not see a durable cell-autonomous
transcriptional response from the closest measured postsynaptic RasGAP loss.

The canonical positive Ras/ERK branch also argued for caution. `Braf` and
`Map2k1` loss produced a real but tiny all-down focal module (`Vgf`, `Ptpn5`,
`Unc13a`, plus `Atp2a2` or `Etv5`), and `Shoc2`, a RAF-activating scaffold,
only lowered `Vgf`. Loss of positive ERK components models the opposite
biochemical sign from `Nf1`: it should reduce, not increase, basal RAF/MEK/ERK
output. Therefore the expected `Nf1` transfer, if any, would be an induced ERK
or activity-like program, closer in sign to the `Gabrb2`/`Atp2b1` axis where
`Vgf`, `Nr4a1`, and `Fos` rose. That possible program exists in the focal
dataset, but `Gabrb2` had only four FDR<0.05 genes and its mechanism is
disinhibition of a GABA-A chloride channel, not direct Ras control.

The mTOR branch provided a second possible nonzero route. TSC1-TSC2-TBC1D7
normally acts as a Rheb GAP upstream of mTORC1 (Dibble et al. 2012), and GATOR1
containing DEPDC5/NPRL2/NPRL3 acts as a RagA/B GAP that suppresses
amino-acid-dependent mTORC1 signaling (Bar-Peled et al. 2013). In the focal
cell group, derepressing these two mTORC1 inputs by perturbing `Tsc2` or
`Depdc5` activated overlapping sterol/LDL genes, especially `Ldlr`, `Msmo1`,
`Pik3r1`, and `Pik3r3`. `Nf1` loss can signal into ERK and PI3K/Akt/mTOR, so
same-direction escape from a growth-control brake is plausible. The transfer is
imperfect, however: NF1 controls Ras-GTP, not the Rheb GAP or Rag GAP itself;
`Mtor`, `Rptor`, `Akt3`, `Spred1`, `Spred2`, `Rasa2`, `Hras`, and `Kras` did
not reproduce the focal `Tsc2`/`Depdc5` sterol state; and the internal `Tsc2`
and `Depdc5` reports both concluded that pathway position mattered strongly in
this postnatal neuronal assay.

The causal chain I used was:

`Nf1` CRISPR loss -> reduced neurofibromin RasGAP activity -> increased Ras-GTP
with possible ERK and PI3K/mTOR propagation -> cell-state changes only if the
151 thalamic neurons are exposed to a stimulus or basal input that requires
NF1 to terminate Ras -> survival/recovery of edited nuclei -> persistent
nuclear RNA differences detectable 3-4 weeks after P16 perturbation.

The weak link is the propagation/exposure step. External knowledge strongly
supports neurofibromin as an important Ras brake in neurons, but the same
dataset shows that several measured Ras suppressors and core Ras components
are transcriptionally flat in the exact target cell group. The external spine
work was rat hippocampal CA1 and used acute glutamate uncaging, not juvenile
mouse thalamic neurons in basal snRNA-seq. A stimulus-evoked or local dendritic
Ras effect could therefore fail to become a persistent nuclear DEG burden.

I therefore predicted a zero rather than a small nonzero count. The call is
driven mostly by within-dataset focal evidence from `Spred1`, `Spred2`,
`Rasa2`, `Syngap1`, `Hras`, and `Kras`; external NF1 biology was used to check
the sign of candidate transfers and keep `Tsc2`/`Depdc5`, `Braf`/`Map2k1`, and
activity-response comparators in the review rather than to override the closest
flat analogs.

## Limits and uncertainty

- The strongest uncertainty is that `Nf1` was not itself measured in the
  supplied Parquet. Neurofibromin can be a much stronger Ras-GAP than `Rasa2`
  or `Syngap1` in some neuronal compartments, so a small focal response is
  plausible even though the closest available analogs were flat.
- `Spred1` and `Spred2` are same-direction Ras-suppression comparators, but
  SPRED proteins recruit NF1 to activated Ras rather than serving as the GAP
  itself; their zero-DEG counts may reflect redundancy or low reliance on that
  recruitment route in `151 TH Prkcd Grin2c Glut`.
- `Tsc2` and `Depdc5` directly remove mTORC1 brakes, whereas `Nf1` is upstream
  of Ras and only indirectly reaches PI3K/mTOR or ERK-to-TSC signaling. I used
  their 86- and 13-DEG focal counts as upper-side counterexamples rather than
  as direct numeric phenocopies.
- `Braf`, `Map2k1`, `Ntrk2`, and `Shoc2` are loss-of-positive-signaling
  comparators. Their shared down-regulation of `Vgf`-centered genes shows that
  the focal cells can report a small RAF/MEK/TrkB program, but it does not
  establish that releasing Ras through `Nf1` loss will drive the same genes in
  reverse.
- The assay observes recovered NeuN+ nuclei weeks after sparse postnatal CRISPR
  perturbation. It could miss Ras, ERK, cAMP, spine, growth, or survival effects
  that are acute, local, protein-phosphorylation-based, stimulus-dependent, or
  carried by edited cells that did not survive or were not sampled.
