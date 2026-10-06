# Gata2 prediction reasoning

## Question and resolved ambiguities

The requested held-out target list in
`[local file: 088_Gata2.csv]`
contains one gene:

```tsv
target_name
Gata2
```

For that target I need to predict the held-out endpoint, `n_degs`, defined as the
number of measured genes with Benjamini-Hochberg-adjusted Wilcoxon `pvals_adj <
0.05` in the focal `151 TH Prkcd Grin2c Glut` group after postnatal AAV-CRISPR
loss of function. I treated this as an assay-calibrated response-breadth
prediction, not as a prediction of embryonic essentiality, raw target knockdown,
or the number of GATA2 binding targets. `Gata2` is absent from both the focal
training-count CSV and the DE parquet as a `gene_target`, as expected for this
held-out run.

## Sources used

- Training endpoint counts:
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
- Training differential expression:
  `[local file: training_de_all_cell_groups.parquet]`,
  filtered to `group_name == "151 TH Prkcd Grin2c Glut"`.
- Distributed Agents same-experiment corpus release
  `perturbai-july-260713-sourceguard-1773-v1`. `target_context(Gata2)`
  returned no curated `Gata2` finding, so I used corpus findings for observed
  relatives, especially `Gata3`, and an induced topology over
  `Gata1/Gata3/Gata4/Gata6/Zfpm2` and boundary comparator TFs.
- Distributed Agents runtime profile comparison
  `profiles/gata_family_compare.json`, which compared focal-cell signed
  `logfoldchanges` for observed GATA-family and developmental TF perturbations.
- PubMed via NCBI E-utilities, queried 2026-09-23, for external Gata2 biology.
  The key papers used were:
  - Tsai et al. 1994, Nature, DOI `10.1038/371221a0`, PMID `8078582`.
  - Nardelli et al. 1999, Developmental Biology, DOI
    `10.1006/dbio.1999.9278`, PMID `10357893`.
  - Nozawa et al. 2009, Genes to Cells, DOI
    `10.1111/j.1365-2443.2009.01289.x`, PMID `19371385`.
  - Kirjavainen et al. 2022, Development, DOI `10.1242/dev.200937`,
    PMID `35815619`.

## Computation over the training data

I first loaded the focal-cell rows from the parquet instead of the full 7.8 GB
file. The focal slice contains 28,891,566 rows: 17,259 measured genes for each
of 1,674 training perturbations. I then joined the requested focal targets with
the training-count CSV and explicitly inspected:

- the observed `n_degs` of biologically relevant training analogs;
- for each analog, the minimum focal-cell adjusted p-value and the counts of
  rows with `pvals_adj < 0.10` or `< 0.25`;
- the rows for marker or pathway transcripts likely to matter for the GATA2
  decision, including `Gata2`, `Gata3`, `Zfpm2`, `Nkx2-2`, `Skor2`, `Th`,
  `Slc17a6`, `Prkcd`, and `Grin2c`;
- signed full-profile and tail-overlap relationships among the observed
  GATA-family perturbations and a small set of hematopoietic and neuronal
  developmental TF counterexamples.

The operation was standard predicate filtering and grouping; conceptually:

```python
focal_de = read_parquet(
    training_de,
    columns=["names", "gene_target", "logfoldchanges", "pvals_adj",
             "n_pert_matched", "n_ctrl_matched"],
    filters=[("group_name", "=", "151 TH Prkcd Grin2c Glut")],
)
n_degs = focal_de.groupby("gene_target").pvals_adj.apply(lambda x: (x < 0.05).sum())
```

The focal count distribution is very zero-heavy: 1,205 of 1,674 training
perturbations have `n_degs = 0`; among the 469 nonzero perturbations, the median
count is only 1. A one-gene or two-gene call is therefore a plausible outcome in
this assay, but the GATA-specific data were even flatter than that.

## Relevant training perturbations

| training perturbation | focal `n_degs` | focal support and interpretation |
|---|---:|---|
| `Gata3` | 0 | Most relevant assayed paralog and known downstream/neural partner of GATA2. It had 220 perturbed nuclei, 23,679 controls, zero FDR<0.05 genes, zero genes at FDR<0.10, and only two rows below FDR<0.25 (`Hagh`, `Cttn`; both `pvals_adj = 0.159`). The same-experiment corpus reports that `Gata3` was almost completely buffered across the P16 postmitotic neuronal panel and that assayed GATA-family/neural comparators did not form a shared module. |
| `Gata1` | 0 | DNA-binding family member in the GATA1/2/3 hematopoietic subfamily. It had 223 perturbed nuclei and no focal adjusted p-values below 0.25; the minimum focal `pvals_adj` was 0.989. Useful mainly as a boundary: the erythroid/megakaryocytic GATA circuit is lineage-displaced in NeuN+ brain nuclei. |
| `Gata4` | 0 | GATA factor from a different developmental branch. It had 250 perturbed nuclei and a minimum focal `pvals_adj` of 1.0. It is not a close GATA2 analog for these neurons, but its complete focal flatness supports the absence of a generic GATA-family response. |
| `Gata6` | 0 | GATA4/5/6 branch factor. It had 330 perturbed nuclei and minimum focal `pvals_adj = 1.0`; again a weak mechanistic analog but a good negative family counterexample. |
| `Zfpm2` | 0 | FOG2/GATA cofactor family member and the most obvious assayed GATA-associated cofactor. It had 180 perturbed nuclei, no focal adjusted p-values below 0.25, and minimum `pvals_adj = 1.0`. The corpus connects `Zfpm2` with `Gata3` and `Gata6` in a same-screen claim that represented GATA-family and Zfpm2-associated perturbations do not form a shared postmitotic neuronal transcriptional module. |
| `Spi1`, `Klf1`, `Etv6` | 0, 0, 1 | Hematopoietic TF counterexamples to GATA2's canonical stem/progenitor role. `Spi1` and `Klf1` were fully flat in the focal group; `Etv6` had only one focal DEG, `Adora1`. These are not neuronal GATA2 partners, but they show that blood-development regulators do not create a broad response in this NeuN-enriched assay. |
| `Foxa2`, `Lmx1b`, `Sox2`, `Tcf7l2` | 0, 0, 2, 106 | Developmental-neuronal TF calibration set. `Foxa2` and `Lmx1b` were flat, `Sox2` had two focal DEGs, while `Tcf7l2` had a real postmitotic thalamic program. This argues that the assay can detect an active TF circuit in `151 TH Prkcd Grin2c Glut`; the GATA near-null is not just a blanket failure of TF CRISPR perturbations. |

The full-profile runtime comparison did not reveal a hidden GATA-like module:
`Gata1`, `Gata3`, `Gata4`, `Gata6`, and `Zfpm2` each had zero FDR-significant
features in the focal group. Apparent whole-profile correlations among these
near-null signatures were dominated by shared flatness and by very large
low-confidence log-fold changes with `pvals_adj = 1`, so I did not treat them as
positive expression-pattern phenocopies. The corpus topology over the nominated
training analogs recovered a connected GATA/Zfpm2 component
`Gata1/Gata3/Gata4/Gata6/Zfpm2`, but the associated same-experiment claim is
explicitly a negative one: represented GATA-family and Zfpm2-associated
perturbations did not converge in the postmitotic neuronal screen.

## Target-specific decision

### `Gata2`

External biology makes `Gata2` a real transcriptional regulator, but mostly in
contexts that the P16-to-P37/44 NeuN+ screen is not built to re-enter. Germline
mouse studies established an early hematopoietic stem/progenitor requirement
for GATA2 (Tsai et al. 1994). In the nervous system, GATA2 is expressed
embryonically in hindbrain and ventral neural-tube regions, acts upstream of
`Gata3` in early CNS development (Nardelli et al. 1999), is positively
autoregulated in embryonic mouse midbrain enhancers (Nozawa et al. 2009), and is
required with `Nkx2-2` for `Skor2` expression in a specific midbrain GABAergic
precursor subtype (Kirjavainen et al. 2022).

Those observations made `Gata3` the key in-dataset analog rather than generic
TFs. `Gata3` loss, however, had `n_degs = 0` in the held-out endpoint cell type;
its best two focal rows were only `Hagh` and `Cttn` at `pvals_adj = 0.159`.
Assayed GATA paralogs (`Gata1`, `Gata4`, `Gata6`) and the assayed GATA cofactor
`Zfpm2` were even flatter in the same focal cells. Expected midbrain-GATA
sentinel transcripts did not move reproducibly in these analogs: `Gata2`,
`Gata3`, `Nkx2-2`, `Skor2`, and the focal-cell identity markers `Th`,
`Slc17a6`, `Prkcd`, and `Grin2c` were not significantly changed after
`Gata3` perturbation, and the corresponding rows for `Gata1`, `Gata4`,
`Gata6`, and `Zfpm2` were also FDR-null.

The relevant developmental GATA2 literature is therefore better read as
evidence of a strong embryonic progenitor and GABAergic-lineage requirement than
as evidence for an acute adult-like glutamatergic TH/PRKCD maintenance circuit.
The focal group is glutamatergic and postmitotic, the perturbation is mosaic and
delivered after the main embryonic GATA2/GATA3/Nkx2-2/Skor2 decisions, and the
observed `Gata3`/`Zfpm2` results show that the represented GATA network is
buffered or absent in this transcriptional state.

I therefore predict no FDR<0.05 DE genes:

```tsv
target_name	predicted_n_degs
Gata2	0
```

## Limits of the prediction

- There is no measured `Gata2` perturbation signature in the supplied parquet
  and no curated `Gata2` target context in the Distributed Agents same-experiment corpus,
  so the call extrapolates from `Gata3`, other GATA paralogs, `Zfpm2`, and
  non-GATA developmental TF controls.
- `Gata3` is the closest observed paralog, but it is not identical to `Gata2`;
  GATA2 can act upstream of GATA3 during early CNS development, so a complete
  embryonic Gata2 knockout would not necessarily match an acute Gata3
  perturbation.
- The assay measures surviving, NeuN-enriched juvenile neurons after sparse
  viral CRISPR and does not test embryonic progenitors, rare midbrain GABAergic
  precursors, adrenal chromaffin cells, blood progenitors, glia, or viability
  effects before nuclei were sampled.
- The DE tables are single-nucleus Wilcoxon tests without indel genotyping or
  protein measurements. Flat downstream signatures do not prove absent editing;
  they only indicate that no measured transcript crossed the assay's adjusted
  p-value threshold.
