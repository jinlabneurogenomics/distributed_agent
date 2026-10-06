# DEG-count prediction for held-out Tbk1

## Question and resolved ambiguities

The requested held-out target list in
`[local file: 234_Tbk1.csv]`
contains one perturbation, `Tbk1`. I interpreted the endpoint as the integer
number of measured genes in `151 TH Prkcd Grin2c Glut` with `pvals_adj < 0.05`
after acute AAV CRISPR loss of `Tbk1`, using the same Wilcoxon/FDR pipeline as
the supplied training table. The DEG count includes any measured gene passing
the threshold, including the target transcript if it passes; I did not require
a downstream-only event.

I treated the held-out `Tbk1` rows as unavailable for quantitative fitting, as
specified. Self-transcript loss in the training parquet was considered only as
QC context, not as evidence for a larger or smaller downstream biological
response.

## Sources used

Input tables:

- `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`, the direct endpoint for
  1,674 non-held-out perturbations in the focal cell group.
- `training_de_all_cell_groups.parquet`, filtered to `group_name == "151 TH
  Prkcd Grin2c Glut"` for focal signatures and for exact adjusted p-values of
  candidate analogs.
- `234_Tbk1.csv`, the ordered list of held-out targets for this run.

Same-experiment internal evidence:

- Distributed Agents PerturbAI semantic corpus
  `perturbai-july-260713-sourceguard-1773-v1`. I used it for curated
  same-experiment findings on the observed responses of `Chuk`, `Irf3`,
  `Nfkb1`, `Map3k7`, `Traf3`, `Atg5`, `Atg16l1`, and `Sqstm1`, and for
  outbound comparator discovery among their curated findings.

External biological evidence:

- NCBI PubMed literature searches/fetches on 2026-09-23 for TBK1 immune,
  STING-IRF3, mitophagy, and ALS/FTD biology.
- Freischmidt et al. 2015, PMID:25803835, DOI:10.1038/nn.4000, establishing
  TBK1 loss of function and optineurin-binding defects as causes of familial
  ALS/FTD.
- Tanaka and Chen 2012, PMID:22394562, DOI:10.1126/scisignal.2002521, showing
  that STING scaffolds IRF3 phosphorylation by TBK1 in cytosolic-DNA signaling.
- Zhang et al. 2019, PMID:30842653, DOI:10.1038/s41586-019-1000-2, defining
  the structural basis for STING recruitment/activation of TBK1.
- Vargas et al. 2019, PMID:30853401, DOI:10.1016/j.molcel.2019.02.010, showing
  that the NDP52 selective-autophagy receptor uses TBK1 to localize/activate
  the ULK1 complex on cargo.
- Nguyen et al. 2023, PMID:37207627, DOI:10.1016/j.molcel.2023.04.021,
  showing that OPTN can initiate PINK1/Parkin mitophagy through TBK1 and class
  III PI3K complex I.
- Xu et al. 2018, PMID:30146158, DOI:10.1016/j.cell.2018.07.041, showing that
  partial Tbk1 loss can interact with aging and reduced TAK1 to promote
  RIPK1-driven ALS/FTD-like neurodegeneration.
- Brenner et al. 2024, PMID:38517332, DOI:10.1084/jem.20221190, separating a
  TBK1-OPTN interaction defect from overt RIPK/TNF-alpha inflammation in mice
  and supporting an autophagolysosomal neuronal disease mechanism.

## Computational steps

1. Read `234_Tbk1.csv`; it had exactly one requested row, `Tbk1`.
2. Read the focal training-count CSV to check which TBK1 pathway genes were in
   training and what their observed endpoint was.
3. Queried the same-experiment Distributed Agents corpus. There was no direct `Tbk1`
   finding, but there were curated reports for the relevant in-training
   innate-immune, NF-kappaB, TAK1, and autophagy genes.
4. Ran a predicate-filtered parquet scan over `training_de_all_cell_groups`
   for the focal cell group and a hand-curated set of TBK1-adjacent genes and
   corpus-nominated comparators:

```python
flt = (
    (ds.field("group_name") == "151 TH Prkcd Grin2c Glut")
    & ds.field("gene_target").isin(candidate_genes)
)
table = dataset.to_table(
    columns=["names", "gene_target", "logfoldchanges", "pvals_adj", "scores"],
    filter=flt,
)
```

The filtered scan retrieved 414,216 rows, corresponding to the 24 selected
training perturbations in the focal cell group. I recomputed each selected
target's focal `n_degs` as `sum(pvals_adj < 0.05)` and inspected its smallest
adjusted p-values to see whether apparent nulls had marginal pathway features.

## Mechanistic analogs and same-experiment evidence

`Tbk1` encodes an IKK-family serine/threonine kinase with two relevant modules:

- innate-immune signaling, especially cGAS/STING and other adaptors that
  activate TBK1 to phosphorylate IRF3 and support NF-kappaB outputs;
- selective autophagy/mitophagy, where TBK1 phosphorylates or scaffolds cargo
  receptors such as OPTN and NDP52 to recruit autophagosome-initiation
  machinery.

The training set did not contain `Optn`, `Tank`, `Tbk1bp1/Sintbad`, `Azi2`,
`Ikbkb`, `Ikbke`, `Ikbkg`, `Mb21d1`, `Sting1/Tmem173`, `Calcoco2/Ndp52`,
`Tax1bp1`, `Nbr1`, `Prkn`, `Pink1`, `Ulk1`, or `Ulk2`, so the closest possible
observed analogs were pathway neighbors rather than exact TBK1 complex
partners.

Core TBK1-adjacent genes present in training were almost completely silent in
`151 TH Prkcd Grin2c Glut`:

| training perturbation | focal n_degs | focal matched perturbed nuclei | focal evidence and interpretation |
|---|---:|---:|---|
| `Chuk` | 0 | 156 | Same IKK/NF-kappaB family output boundary. Smallest focal padj was 0.727, and the corpus reports no FDR<0.10 downstream response in any of 22 measured neuronal groups plus absent canonical NF-kappaB feedback/inflammatory/survival transcripts. |
| `Nfkb1` | 0 | 181 | Canonical NF-kappaB transcriptional output. Smallest focal padj was 1.0; the corpus reports 0 downstream FDR<0.10 genes across 22 recovered neuronal cell groups and no cytokine/chemokine/survival-output program. |
| `Rel` | 0 | 205 | NF-kappaB-family comparator nominated through `Chuk`, `Map3k7`, `Nfkb1`, `Sqstm1`, and `Traf3`; it had no focal FDR<0.05 genes. This supported the idea that basal NF-kappaB perturbation did not resolve transcriptionally in these juvenile neurons. |
| `Irf3` | 0 | 165 | Direct TBK1 substrate in STING signaling. Smallest focal padj was 1.0; corpus summaries call `Irf3` transcriptionally buffered across basal postnatal NeuN+ classes and report that canonical IRF3-pathway perturbations did not phenocopy an interferon response. |
| `Traf3` | 0 | 211 | Adaptor upstream of TBK1 and IRF3/NF-kappaB. Smallest focal padj was 1.0; the corpus reports a pan-neuronal FDR null at FDR<0.10 and no interferon-stimulated, immediate NF-kappaB/MAPK, oxidative-stress, or apoptosis transcripts. |
| `Map3k7` | 0 | 160 | TAK1 is a TLR/IL-1/TNF-to-NF-kappaB/JNK/p38 hub and a relevant counterpoint to TBK1-RIPK1 inflammatory biology. It had focal minimum padj 1.0, and the corpus reports no FDR-resolved cell-autonomous transcriptional program in 22 measured juvenile NeuN+ groups. |
| `Atg5` | 0 | 114 | Core macroautophagy factor. Minimum focal padj was 0.105 and no gene crossed 0.05; the corpus reports only a two-gene effect in `155 MB Glut` and no canonical autophagy, lysosome, p62, proteasome-rebound, or UPR/ISR program after `Atg5` perturbation. |
| `Atg16l1` | 0 | 93 | LC3-conjugation machinery partner to `Atg5`. All focal padj were 1.0; the corpus reports no robust downstream transcriptome in any recovered neuronal class and no autophagy-lysosomal, UPR/ISR, or inflammasome aftershock. |
| `Sqstm1` | 1 | 259 | TBK1 substrate/adaptor-side selective-autophagy comparator. Its only focal FDR<0.05 gene was its self-transcript, `Sqstm1` padj 7.93e-4; the nearest downstream candidate was `Sfxn5`, but padj was 0.092. The corpus reports a very sparse surface with one FDR<0.10 gene in each of only three groups and no canonical p62-adjacent NRF2/redox, lysosomal-autophagy, proteasome, UPR, or ISR response. |

I also checked every Distributed Agents common-outbound comparator emitted for two or
more of these core sources:

| comparator | focal n_degs | use in reasoning |
|---|---:|---|
| `Becn1` | 0 | Kept as another autophagy-initiation boundary. |
| `Rb1cc1` | 4 | Kept as the FIP200/ULK-complex edge of selective autophagy; the effect was still tiny. |
| `Mtor` | 2 | Kept as an autophagy-regulatory counterpoint; tiny focal response. |
| `Rptor` | 0 | Kept as an mTORC1 counterpoint; null. |
| `Tlr2` | 0 | Kept as an upstream inflammatory-receptor counterpoint; null. |
| `Tlr3` | 0 | Kept as an upstream TRIF/TBK1 counterpoint; null. |
| `Tlr4` | 0 | Kept as an upstream TLR/NF-kappaB counterpoint; null. |
| `Tlr7` | 0 | Kept as an upstream TLR/IRF counterpoint; null. |
| `Tnfrsf1a` | 0 | Kept as a TNF/NF-kappaB/RIPK1 counterpoint; null. |
| `Ctsb` | 1 | Kept as lysosomal boundary evidence; tiny. |
| `Fbxo11` | 1 | Rejected as a mechanistic analog because it entered through weak flat-state neighbors, not a TBK1 pathway relationship. |
| `Rel` | 0 | Kept as an NF-kappaB-family output comparator; null. |
| `Psmb4` | 742 | Rejected as a TBK1 analog; its large burden reflects proteasome stress, a distinct perturbation class that the corpus used as a divergent counterexample for low-response autophagy/NF-kappaB genes. |
| `Psmc1` | 430 | Rejected for the same reason as `Psmb4`. |
| `Uba5` | 2677 | Rejected as a UFMylation/protein-homeostasis responder, not a TBK1-like innate/autophagy receptor signal. |
| `Ufc1` | 572 | Rejected as another UFMylation counterexample. |

## Target-specific prediction

### `Tbk1`

The zero/nonzero decision is driven mainly by within-dataset evidence. In the
focal thalamic glutamatergic class, every measured NF-kappaB/IRF/TLR/TNF/TAK1
analog was FDR-null, and the selective-autophagy genes that are closest to
TBK1's OPTN/NDP52/p62 biology were also null or self-only. This was not because
the focal class lacked power globally: high-burden counterexamples such as
`Uba5` with 2,677 DEGs, `Psmb4` with 742, `Ufc1` with 572, and `Psmc1` with 430
were all visible in the same `151 TH Prkcd Grin2c Glut` readout. Those
counterexamples represent ER/protein-homeostasis or proteasome programs rather
than TBK1 signaling and therefore argue against borrowing a large count from a
generic stress signature.

External biology cuts in the same direction for this acute juvenile neuronal
assay. TBK1 is very important when STING/TLR/RIG-I-like receptors are engaged,
and STING can recruit TBK1 to scaffold IRF3 phosphorylation (Tanaka and Chen
2012; Zhang et al. 2019). However, the experiment sampled basal NeuN+ nuclei,
not virally stimulated or glial inflammatory states, and the present training
perturbations around `Irf3`, `Traf3`, `Tlr2`, `Tlr3`, `Tlr4`, `Tlr7`, `Chuk`,
`Rel`, and `Nfkb1` show that this axis was not producing a detectable
cell-autonomous transcriptional program. TBK1 also promotes selective
autophagy/mitophagy through OPTN and NDP52 (Vargas et al. 2019; Nguyen et al.
2023), but the screen's `Atg5`, `Atg16l1`, `Becn1`, `Rb1cc1`, and `Sqstm1`
boundaries show that partial acute disruption of this machinery in recovered
juvenile neurons rarely yielded FDR-significant nuclear mRNA changes. The
ALS/FTD genetics and mouse work establish that TBK1 insufficiency can matter in
neurons (Freischmidt et al. 2015; Xu et al. 2018; Brenner et al. 2024), but
those phenotypes depend on aging, chronic autophagolysosomal burden, myeloid
inflammation, or a specific OPTN-binding variant rather than a 3 to 4 week
basal thalamic neuron assay.

The most likely endpoint is therefore a focal null. I predict `Tbk1` will have
0 genes crossing BH FDR 0.05 in `151 TH Prkcd Grin2c Glut`.

## Limits

- `Tbk1` itself and its closest adaptors, especially `Optn`, `Calcoco2/Ndp52`,
  `Tbk1bp1/SINTBAD`, `Azi2/NAP1`, `Tank`, `Sting1`, and `Mb21d1/cGAS`, were not
  measured as training perturbations here. The prediction transfers through
  pathway neighbors rather than through an exact in-complex analog.
- TBK1 is a kinase with stimulus-gated substrates. A null after loss of `Irf3`,
  `Traf3`, or basal TLR receptors does not prove that an activated STING/TBK1
  pathway would be silent after infection, DNA damage, or inflammation.
- NeuN+ FACS largely removes microglia and astrocytes, both central to much of
  the published TBK1/STING neuroinflammation literature.
- A zero DEG-count prediction does not mean Tbk1 is biologically irrelevant or
  unedited. It only says that this sparse acute CRISPR perturbation is expected
  not to push any measured nuclear transcript past FDR 0.05 in recovered `151
  TH Prkcd Grin2c Glut` nuclei.
