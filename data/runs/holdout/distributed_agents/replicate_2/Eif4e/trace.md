# DEG-count prediction for held-out `Eif4e`

## Question and interpretation

The requested target CSV contained one held-out perturbation, `Eif4e`. I
interpreted the endpoint as the exact training CSV definition: the number of
measured genes in `151 TH Prkcd Grin2c Glut` whose Benjamini-Hochberg adjusted
Wilcoxon p-value is below 0.05 after the `Eif4e` CRISPR perturbation. That count
includes the target transcript itself when its own row passes FDR. `Eif4e` was
absent from both the training count CSV and the DE parquet, so no row from the
held-out perturbation was used.

## Sources

Internal experiment and training surfaces:

- `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`, for exact `n_degs` counts in
  the focal cell group.
- `[local file: training_de_all_cell_groups.parquet]`, queried only for non-held-out
  perturbations in `151 TH Prkcd Grin2c Glut`.
- Distributed Agents same-experiment corpus
  `perturbai-july-260713-sourceguard-1773-v1`, used for curated
  same-screen findings around `Eif4a2`, `Eif4g1`, `Eif4h`, `Mtor`, `Tsc2`,
  `Fmr1`, and `Cyfip2`. This is a semantic layer over the supplied experiment,
  not independent replication.
- Distributed Agents runtime profile tools, used to compare signed
  `151 TH Prkcd Grin2c Glut` log-fold-change profiles for a hand-selected
  translation-control cohort.

External biological grounding came from PubMed-indexed literature:

- Sonenberg and Hinnebusch, 2009, DOI `10.1016/j.cell.2009.01.042`, PMID
  `19239892`: eIF4E is the mRNA-cap-binding subunit of the eIF4F initiation
  complex, binds eIF4G, and is inhibited by 4E-BP proteins downstream of mTOR.
- Napoli et al., 2008, DOI `10.1016/j.cell.2008.07.031`, PMID `18805096`:
  CYFIP1 can repress initiation by binding eIF4E as an FMRP-associated
  4E-BP-like factor at synapses.
- Gkogkas et al., 2012, DOI `10.1038/nature11628`, PMID `23172145`: loss of
  the eIF4E repressor 4E-BP2 or eIF4E overexpression increases neuroligin
  translation and produces autism-related synaptic and behavioral phenotypes in
  mice.
- Santini et al., 2012, DOI `10.1038/nature11782`, PMID `23263185`:
  transgenic eIF4E overexpression increases cap-dependent translation and
  produces autism-like synaptic and behavioral abnormalities reversible by the
  cap-dependent translation inhibitor 4EGI-1.

## Computation over the training data

I first calibrated the endpoint distribution from the 1674 training targets in
the focal class. It is very zero-heavy:

- `1205/1674 = 71.98%` had `n_degs == 0`.
- `363/1674 = 21.68%` had `1 <= n_degs < 10`.
- `63/1674 = 3.76%` had `10 <= n_degs < 100`.
- `43/1674 = 2.57%` had at least 100 DEGs.

I then searched the training count table for represented cap-initiation,
translation, FMRP/CYFIP, and mTOR-axis perturbations. For the focal cell group,
the relevant counts were:

| Perturbation | focal `n_degs` | relationship to `Eif4e` |
|---|---:|---|
| `Eif4a2` | 2 | eIF4F RNA helicase paralog represented in the screen |
| `Eif4g1` | 1 | eIF4F scaffold that binds eIF4E |
| `Eif4h` | 1 | eIF4A accessory factor for cap-dependent initiation |
| `Mtor` | 2 | upstream kinase regulating 4E-BP/eIF4E availability |
| `Rptor` | 0 | mTORC1 scaffold |
| `Fmr1` | 0 | translational repressor connected to eIF4E through CYFIP1 |
| `Cyfip1` | 0 | FMRP/eIF4E bridge and 4E-BP-like eIF4E binder |
| `Cyfip2` | 1 | CYFIP paralog; its one focal DEG was its own transcript |
| `Cnot1` | 0 | CCR4-NOT node linked to translation/RNA helicase biology |
| `Eif2ak4` | 0 | integrated-stress-response kinase |
| `Mcts1` | 0 | translation-reinitiation/recycling-associated factor |
| `Ddx3x` | 8 | translation/RNA helicase with a small focal response |
| `Eef2` | 9 | elongation factor with a small focal response |
| `Tsc2` | 86 | upstream mTORC1 brake; loss activates mTORC1 |

For exact same-cell-group expression evidence, I filtered the parquet with
DuckDB:

```sql
SELECT gene_target, names, logfoldchanges, scores, pvals_adj
FROM read_parquet('training_de_all_cell_groups.parquet')
WHERE group_name = '151 TH Prkcd Grin2c Glut'
  AND gene_target IN (...)
  AND pvals_adj < 0.05
ORDER BY gene_target, pvals_adj, names;
```

This showed that the low counts above were not hiding broad submodules:

- `Eif4a2` had two FDR-significant rows: `Eif4a2` itself
  logFC `-0.629`, FDR `1.23e-7`, and `Cadm4` logFC `-0.392`,
  FDR `0.0122`.
- `Eif4g1` had one FDR-significant row: `Eif4g1` itself, logFC `-0.764`,
  FDR `0.00702`.
- `Eif4h` had one FDR-significant row: `Hexim1`, logFC `0.744`,
  FDR `0.0208`; `Eif4h` itself did not pass FDR.
- `Mtor` had two FDR-significant rows: `Rims3`, logFC `0.300`,
  FDR `0.0185`, and `Tmed8`, logFC `-0.821`, FDR `0.0265`.
- `Fmr1`, `Cyfip1`, `Rptor`, and `Mcts1` had zero FDR-significant rows.

I also used the Distributed Agents runtime profile comparator on signed log-fold changes
in `151 TH Prkcd Grin2c Glut`, thresholding `pvals_adj < 0.05`, with the cohort
`Eif4a2`, `Eif4g1`, `Eif4h`, `Mtor`, `Rptor`, `Tsc2`, `Fmr1`, `Cyfip1`,
`Cyfip2`, `Eef2`, `Ddx3x`, and `Mcts1`. The focal eIF4F nodes each had only
`1_to_9_significant_features`; the profile inspection counted 2 significant
features for `Eif4a2`, 1 for `Eif4g1`, 1 for `Eif4h`, and 2 for `Mtor`, versus
86 for `Tsc2`. None of the significant features overlapped between
`Eif4a2`, `Eif4g1`, `Eif4h`, `Mtor`, and `Tsc2`, supporting the corpus
interpretation that these are singleton or near-singleton signatures rather
than one recurrent eIF4F/mTOR transcriptomic state.

## Same-experiment analogs and counterexamples

`Eif4a2`, `Eif4g1`, and `Eif4h` are the nearest represented loss-of-function
analogs because eIF4E, eIF4G, and eIF4A form the cap-dependent eIF4F complex,
with eIF4H acting on the eIF4A helicase branch. Their training endpoints in the
focal class were `2`, `1`, and `1`. Distributed Agents corpus findings made the same
point across the whole experiment: the `Eif4a2` report found that represented
CCR4-NOT/eIF4F/mTOR comparators, including `Cnot1`, `Ddx3x`, `Eif4g1`, `Eif4h`,
and `Mtor`, did not phenocopy its two responder signatures
(`Eif4a2:F005`); the `Eif4g1` report found that individually perturbed
`Eif4g1`, `Eif4a2`, `Eif4h`, `Mtor`, and `Rptor` were flat or extremely weak
whereas `Tsc2` was broad (`Eif4g1:F003`); and the `Eif4h` report found only
a weak rank-order relationship to `Eif4a2` rather than a robust shared
eIF4F state (`Eif4h:F005`).

The mTOR branch gives a directionally important counterexample. `Tsc2` loss,
which disinhibits mTORC1, caused 86 focal DEGs and a sterol/lysosomal
mTORC1-like program including `Cyp51`, `Ldlr`, `Hmgcr`, `Msmo1`, `Lamp2`,
`Dpp7`, and `Grn`. But `Mtor` loss caused only 2 focal DEGs and `Rptor` caused
0; the Distributed Agents Mtor/Tsc2 reports specifically describe Rptor, Akt3,
Pik3cb, Pik3r1, and Pik3r2 as failing to phenocopy `Mtor` or `Tsc2`
(`Mtor:F005`; `Tsc2:F007`). Therefore I treated `Tsc2` as evidence that
mTOR-axis transcription can be detected in this assay, but not as a quantitative
analog for `Eif4e`, which is a cap-binding loss perturbation, not loss of an
mTORC1 repressor.

The FMRP/CYFIP neighborhood also argues against a broad hidden response.
CYFIP1 is a biochemical eIF4E-binding FMRP partner, but the focal training
counts were 0 for `Fmr1`, 0 for `Cyfip1`, and 1 for `Cyfip2`; the only
`Cyfip2` focal FDR call was `Cyfip2` itself. The Distributed Agents corpus likewise
reported that represented FMRP/CYFIP/local-translation-associated perturbations
do not form a robust acute neuronal nuclear RNA module, and that `Fmr1` was
buffered even relative to `Tsc2` and `Mtor` (`Fmr1:F003`, `Fmr1:F004`,
`Cyfip2:F003`).

Finally, broad stress responders such as `Uba5` and `Ufc1` show the upper bound
for protein-homeostasis stress in this class: `Uba5` had 2677 DEGs and `Ufc1`
had 572. They are useful positive controls for detectability of
translation/ER-ribosome quality-control stress, but they are UFMylation factors,
not direct cap-binding factors, and the corpus reports for `Eif4g1`/`Eif4h`
did not treat them as close mechanistic phenocopies.

## Target-specific call for `Eif4e`

External biology made `Eif4e` a plausible weak responder rather than a
confident zero: eIF4E is the limiting cap-binding eIF4F subunit, 4E-BPs and
CYFIP1 regulate translation through direct eIF4E binding, and increasing eIF4E
or removing 4E-BP2 is sufficient to alter synaptic protein synthesis and mouse
behavior. However, those studies are largely protein-translation or gain-of-
function contexts. The held-out experiment asks about acute, sparse,
loss-of-function editing in already postmitotic juvenile neurons, assayed by
nuclear RNA-seq.

Within that exact assay, the observed loss-of-function nodes closest to eIF4E
were consistently singleton or near-singleton in `151 TH Prkcd Grin2c Glut`.
They did not turn on a recurrent ISR, UPR, ribosome, mTOR, or synaptic mRNA
program at FDR 0.05. I therefore predict a nonzero but minimal endpoint:
`Eif4e` is likely to yield one FDR-significant measured gene, most plausibly the
target transcript itself or one isolated downstream gene, with no broad
secondary transcriptional response.

Final point prediction for `Eif4e`: `1`.

## Limits and extrapolation

The main uncertainty is that no perfect analog was assayed: `Eif4e` itself,
`Eif4e2`, `Eif4e3`, `Eif4b`, `Eif4a1`, `Eif4g3`, `Eif4ebp1`, `Eif4ebp2`,
`Mknk1`, `Mknk2`, `Rheb`, and `Tsc1` were absent from the represented training
targets I could compare directly. The prediction therefore transfers from
nearby but imperfect eIF4F nodes.

The external eIF4E literature is also not endpoint-matched. eIF4E
overexpression and 4E-BP2 loss increase eIF4E-dependent translation, whereas
this task is sparse CRISPR loss of `Eif4e`; synaptic protein synthesis,
eIF4E phosphorylation, cell size, electrophysiology, and proteome-wide
translation were not measured. The single-nucleus endpoint can miss purely
local or translational effects. Conversely, a zero or singleton RNA signature
does not mean eIF4E is unimportant; it only means I expect few transcripts to
cross BH FDR 0.05 among recovered nuclei at this time point.
