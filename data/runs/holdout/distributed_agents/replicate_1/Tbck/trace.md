# DEG-count prediction trace

## Question and endpoint

The requested prediction is the number of genes that would pass
Benjamini-Hochberg-adjusted Wilcoxon `pvals_adj < 0.05` after each held-out
CRISPR loss-of-function perturbation in `151 TH Prkcd Grin2c Glut` cells.
The run's requested-target CSV contained one target, `Tbck`. I treated the
file order as required output order only; there was no ranked supervision in
this task.

The requested endpoint is directly observed for the non-held-out perturbations
in
`../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
`Tbck` itself was absent from both the training counts and the
`training_de_all_cell_groups.parquet` signatures, so every `Tbck` prediction
below is extrapolation from represented perturbations rather than a query of a
held-out signature.

## Sources used

- Declared input DEG-count CSV: 1,674 non-held-out focal-cell perturbations,
  with `n_degs` ranging from 0 to 2,677; median 0, 75th percentile 1, 90th
  percentile 2, 95th percentile 18.
- Declared input differential-expression Parquet: focal-cell signatures for
  mTOR, autophagy, endolysosomal, and TBC-domain training targets were queried
  with PyArrow and filtered to `group_name == "151 TH Prkcd Grin2c Glut"`.
  I recomputed FDR<0.05 gene sets and overlaps directly from `pvals_adj`.
- Same-experiment PerturbAI July 260713 SourceGuard v1 corpus: bounded reports
  and packaged evidence for the non-held-out `Tsc2`, `Depdc5`, `Mtor`,
  `Rptor`, and `Rab7` perturbations. These reports are curated views of the
  same Parquet experiment, not independent replication.
- PubMed literature for TBCK and mTOR biology:
  - Liu, Yan, and Zhou 2013, PLoS One, doi:10.1371/journal.pone.0071349,
    PMID:23977024.
  - Ortiz-Gonzalez et al. 2018, Annals of Neurology,
    doi:10.1002/ana.25130, PMID:29283439.
  - Beck-Wodl et al. 2018, Acta Neuropathologica Communications,
    doi:10.1186/s40478-018-0646-6, PMID:30591081.
  - Bar-Peled et al. 2013, Science, doi:10.1126/science.1232044,
    PMID:23723238.
  - Dibble et al. 2012, Molecular Cell, doi:10.1016/j.molcel.2012.06.009,
    PMID:22795129.
  - Saxton and Sabatini 2017, Cell, doi:10.1016/j.cell.2017.02.004,
    PMID:28283069.

## Computation over the supplied signatures

I first used the training count CSV to place candidate analogs in the observed
focal endpoint. The represented genes closest to a TBCK prior were sparse:

| training perturbation | mechanistic relationship to `Tbck` | focal `n_degs` |
|---|---|---:|
| `Rptor` | core mTORC1 scaffold, direct loss lowers mTORC1 output | 0 |
| `Atg5` | canonical autophagy gene | 0 |
| `Mtor` | mTOR kinase, direct loss lowers mTORC1 and mTORC2 output | 2 |
| `Depdc5` | GATOR1 negative regulator of Rag/mTORC1; opposite sign from mTORC1 loss | 13 |
| `Tsc2` | TSC-complex negative regulator of Rheb/mTORC1; opposite sign from mTORC1 loss | 86 |
| `Rab7` | late-endosome/autophagosome-lysosome regulator with a much more direct endolysosomal block | 501 |
| `Vps35`, `Vps54` | retromer/GARP trafficking comparators, partial and indirect | 17, 31 |
| `Tbcd` | TBC-name counterexample, tubulin folding rather than TBCK/mTOR biology | 12 |

The focal Parquet rows then tested whether those counts belonged to a coherent
shared signature. At FDR<0.05, `Tsc2` had 86 DEGs, `Depdc5` had 13, and all
8 genes shared between the two were same-sign, including the PI3K/sterol genes
`Pik3r3`, `Pik3r1`, `Ldlr`, `Insig1`, and `Hmgcs1`. This matches the corpus
interpretation that `Depdc5` loss weakly phenocopied the mTORC1
de-repression state of `Tsc2` in 151 cells. `Rab7` shared 38 FDR<0.05 genes
with `Tsc2`, 36 in the same direction, and 5 genes with `Depdc5`, all in the
same direction, showing a sterol/lysosomal stress module that is visible in the
focal group.

In contrast, the same-sign direct mTORC1-loss analogs did not carry that
program. `Mtor` had only two focal DEGs, `Rims3` and `Tmed8`, and shared no
FDR<0.05 genes with `Tsc2`, `Depdc5`, or `Rab7`; `Rptor` and `Atg5` had no
FDR<0.05 genes at all. The same-experiment `Mtor` and `Rptor` reports reached
the same conclusion at the looser FDR<0.10 threshold: expected TFEB/autophagy,
SREBP/sterol, integrated-stress, and translation-initiation sentinels were
absent or below threshold after direct mTORC1 disruption, whereas `Tsc2`,
`Depdc5`, and `Rab7` induced a visible sterol/lysosomal branch.

## Target-specific reasoning

### `Tbck`

`Tbck` encodes TBC1-domain-containing kinase. TBCK depletion was reported to
reduce the protein levels of mTOR-complex components and suppress mTOR
signaling in cultured cells (Liu et al. 2013). Homozygous human TBCK
loss-of-function causes a severe pediatric encephaloneuronopathy with aberrant
autophagy; patient-derived TBCK-null fibroblasts showed LC3-positive
autophagosome accumulation and biochemical abnormalities partially improved by
the mTORC1 activator leucine (Ortiz-Gonzalez et al. 2018). Neuropathology in
TBCK deficiency also linked the disorder to neuronal lipofuscin storage and
autophagosomal-lysosomal dysfunction (Beck-Wodl et al. 2018).

Those external data make a TBCK effect biologically plausible, but they point
most directly to lowered or dysregulated mTORC1/autophagy rather than to the
Rag/Rheb de-repression produced by `Depdc5` or `Tsc2` loss. The causal chain I
used was:

`Tbck` CRISPR loss in postmitotic P16 thalamic glutamatergic neurons ->
partial TBCK protein disruption, with no guaranteed nuclear mRNA loss ->
possible mTORC1 lowering and altered autophagy/lysosomal flux ->
protein, phosphorylation, vesicle, and storage phenotypes that may need strong
or chronic loss ->
only recovered NeuN+ nuclei sampled at P37-P44 ->
single-nucleus relative RNA DEGs at FDR<0.05.

The best same-direction within-dataset anchors were therefore `Mtor`,
`Rptor`, and `Atg5`, not `Tsc2` and `Depdc5`. `Mtor` had 188 perturbed nuclei
in the focal cell group and only 2 FDR<0.05 genes. `Rptor` was even more
powered with 235 perturbed nuclei and had 0 DEGs. `Atg5` had 114 perturbed
nuclei and 0 DEGs. These are imperfect because TBCK may act through additional
lysosomal trafficking steps, but they show that partial acute loss of a core
mTORC1/autophagy component usually failed to produce a broad FDR-significant
nuclear response in the exact focal endpoint.

The stronger counterexamples had candidate-specific causal breaks:

- `Tsc2`: 86 DEGs in the focal count endpoint. TSC2 is a Rheb GAP within the
  TSC1-TSC2-TBC1D7 complex, so its loss activates mTORC1 rather than lowering
  it (Dibble et al. 2012). Its 151 signature shared all 8 overlapping
  FDR<0.05 genes with `Depdc5` in the same direction, consistent with
  mTORC1 de-repression, but the sign is opposite the published TBCK-depletion
  effect.
- `Depdc5`: 13 focal DEGs. GATOR1 loss removes a RagA/RagB GAP and makes
  mTORC1 resistant to amino-acid deprivation (Bar-Peled et al. 2013), again
  an mTORC1-up state rather than the lowered mTORC1 state expected for TBCK
  loss.
- `Rab7`: 501 focal DEGs. `Rab7` shares the endolysosomal compartment and
  overlaps the `Tsc2`/`Depdc5` sterol-lysosome expression axis in this
  dataset, but Rab7 directly controls late endosome and autophagosome-lysosome
  traffic. Its large survivor-state RNA program is not evidence that every
  upstream autophagy regulator, especially a less direct TBCK perturbation,
  will cross FDR in the same way.
- `Vps35` and `Vps54`: 17 and 31 focal DEGs. These are trafficking
  counterexamples that show modest focal responses are possible, but retromer
  or GARP disruption is not an obligate same-function perturbation for TBCK.

On balance, the direct mTORC1-loss and autophagy anchors predict no robust
focal transcriptomic footprint for `Tbck`; the `Tsc2`/`Depdc5` and `Rab7`
responses argue only that opposite-sign or more direct lysosomal perturbations
are detectable. I therefore predict that `Tbck` produces zero FDR<0.05 genes
in `151 TH Prkcd Grin2c Glut`.

## Limits

The prediction is extrapolative because no `Tbck` signature is present in the
training Parquet, and the closest same-complex or pathway genes `Tbc1d7`,
`Tsc1`, `Rheb`, `Nprl2`, and `Nprl3` were also not represented as training
perturbations. TBCK biology is not a pure `Mtor` or `Rptor` knockout, and a
vesicle-fusion defect downstream of TBCK could in principle resemble the large
`Rab7` state. However, the published TBCK evidence comes mostly from complete
human loss or non-neuronal fibroblast systems, while the requested experiment
uses sparse, acute, partial, postnatal AAV CRISPR loss and observes only
recovered neuronal nuclei. The zero prediction should therefore be read as a
prediction about this FDR-thresholded nuclear RNA endpoint, not about a lack of
TBCK function in neurons or a lack of lysosomal pathology after stronger loss.
