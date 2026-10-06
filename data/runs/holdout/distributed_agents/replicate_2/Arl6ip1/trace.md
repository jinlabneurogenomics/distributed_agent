# Arl6ip1 DEG-count prediction

## Question and resolved ambiguities

The requested held-out perturbation set contains one target:

```text
Arl6ip1
```

I interpreted the prediction target as the exact `n_degs` endpoint used in
`151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`: the number of measured
genes in `151 TH Prkcd Grin2c Glut` with `pvals_adj < 0.05` in the focal
Perturb-seq differential-expression table. I treated the target transcript
itself as eligible to contribute to `n_degs`, because the supplied training
counts match direct self-transcript calls: for example `Atl1`, `Reep1`,
`Reep2`, `Retreg1`, `Cpt1c`, `Klc2`, `Arl3`, and `Slc1a1` each have exactly
one DEG in the focal class and that DEG is the perturbed target's own mRNA.

I did not treat a zero as failed editing, and I did not use measured target
RNA reduction as a proxy for knockout strength. The endpoint is the assayed,
FDR-thresholded nuclear RNA footprint 3 to 4 weeks after sparse AAV CRISPR in
postnatal mouse neurons.

## Evidence used

- Held-out target manifest:
  `[local file: 016_Arl6ip1.csv]`.
- Focal-cell training DEG counts:
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
- Full training differential-expression parquet:
  `[local file: training_de_all_cell_groups.parquet]`.
- Distributed Agents same-experiment semantic corpus
  `perturbai-july-260713-sourceguard-1773-v1`, including the claims:
  - `claim:8d2c5d189191c9ea65cf`: represented ER-shaping, HSP, and long-axon
    transport perturbations do not form a shared acute neuronal nuclear
    transcriptomic module in this assay.
  - `claim:46c56a8a58ea8e01922e`: `Ddhd2` does not sit in a shared acute
    neuronal RNA response with represented lipid/lipophagy, autophagy, or HSP
    perturbations.
  - `claim:ffc790a19a9a59483519` and
    `claim:824e52fd6f0f48823f38`: HSPA5/ERAD-like transcription is detectable
    in `151 TH Prkcd Grin2c Glut` after selected perturbations such as
    `Hspa5`, `Manf`, and `Sec63`, but it is not a generic output of every
    ER-associated perturbation.
  - `claim:f6d22ea9448373eb8a02` and
    `claim:9ba3289b451540e57545`: represented autophagy and lysosomal
    perturbations are cell-context-restricted and are not generally
    interchangeable basal transcriptomic phenocopies.
- PubMed literature for ARL6IP1 biology:
  - Yamamoto et al., 2014, DOI `10.1042/BJ20131186`, showed that ARL6IP1 is
    an ER-membrane protein with reticulon-like short hairpin transmembrane
    domains, can bind atlastin, and can shape high-curvature ER tubules.
  - Fowler and O'Sullivan, 2016, DOI `10.1093/hmg/ddw139`, reported that loss
    of Drosophila Arl6IP1 disrupts smooth ER and mitochondrial organization at
    distal motor axons and produces progressive locomotor phenotypes.
  - Byrne et al., 2022, DOI `10.1186/s40478-022-01343-6`, connected Arl6IP1
    knockout in HSP models with axonal ER organization and lipid homeostasis.
  - Foronda et al., 2023, DOI `10.1038/s41586-023-06090-9`, found that
    ARL6IP1 interacts with FAM134B/RETREG1 and participates in ER-phagy
    clusters; Arl6ip1 disruption impaired ER-phagy flux and expanded ER sheets
    in sensory neurons.
  - Lim et al., 2023, DOI `10.1084/jem.20230367`, localized ARL6IP1 to
    mitochondria-associated ER membranes and linked ARL6IP1 loss to
    mitochondrial dysfunction and dysregulated autophagy in HSP models.
  - Akiduki and Ikemoto, 2008, DOI `10.1074/jbc.M801570200`, identified
    ARL6IP1 as an ARL6IP5/addicsin-associated protein that can indirectly
    regulate the EAAC1/SLC1A1 glutamate transporter in a heterologous system.

## Computations over the supplied data

I first read the focal-cell training count CSV and extracted exact observed
`n_degs` for biological analogs of ARL6IP1: ER-shaping/HSP genes, the
ARL6IP1-FAM134B/RETREG1 ER-phagy neighborhood, autophagy genes, MAM and
mitochondrial-stress comparators, and ER-stress controls.

I then used the run-local Distributed Agents `profile_neighbors` tool to compare each of
20 in-dataset analog anchors against all 1,674 eligible non-held-out profiles in
`151 TH Prkcd Grin2c Glut`, using all 17,259 measured log2 fold changes and
retaining top signed tails. This was a sanity check for hidden within-dataset
phenocopies; it did not identify a coherent high-DEG neighbor set for the
ER-shaping HSP anchors, and it kept `Hspa5`, `Sec63`, and `Opa1` separated as
detectable stress responses rather than same-pathway substitutes for ARL6IP1.

Finally, I filtered the large parquet to the focal cell group and the selected
analog targets:

```python
f = (
    (pc.field("group_name") == "151 TH Prkcd Grin2c Glut")
    & pc.field("gene_target").isin(candidate_targets)
)
```

For each analog I counted `pvals_adj < 0.05`, listed the significant measured
genes, and compared the top 50 positive and top 50 negative log-fold-change
tails among the closest ER-shaping/HSP perturbations. No pair among
`Atl1`, `Atl3`, `Reep1`, `Reep2`, `Spast`, `Bscl2`, `Cpt1c`, `Klc2`, `Ddhd2`,
and `Retreg1` shared an FDR-significant gene in the focal class; signed top-50
tail overlaps were small, typically 0 to 4 genes per tail with no meaningful
downstream overlap.

## Target-specific reasoning

ARL6IP1 is biologically closest to ER-shaping and hereditary-spastic-paraplegia
genes rather than to the strong transcriptional regulators in the training set.
It shapes ER membranes in a reticulon-like fashion, binds atlastin, and in
neuronal disease models affects axonal smooth ER, mitochondria-associated ER
membranes, lipid homeostasis, and ER-phagy. Those are compelling structural and
long-term maintenance phenotypes, but the exact assay here is a basal nuclear
RNA readout in recovered postnatal thalamic neurons, not an axon-morphology,
flux, or chronic degeneration assay.

The most relevant in-dataset HSP/ER-shaping comparators were transcriptionally
nearly flat in `151 TH Prkcd Grin2c Glut`:

| comparator | focal `n_degs` | focal significant genes | interpretation for Arl6ip1 |
| --- | ---: | --- | --- |
| `Atl1` | 1 | `Atl1` down | atlastin-family ER tubule GTPase and reported ARL6IP1 interactor class; self-transcript only |
| `Atl3` | 0 | none | closest represented atlastin paralog did not produce a focal DEG |
| `Reep1` | 1 | `Reep1` down | HSP ER-shaping hairpin protein; self-transcript only |
| `Reep2` | 1 | `Reep2` down | HSP ER-shaping REEP paralog; self-transcript only |
| `Spast` | 0 | none | canonical HSP ER/microtubule-severing comparator; no focal RNA response |
| `Bscl2` | 2 | `Bscl2`, `Hpf1` down | ER lipid-droplet/HSP comparator; only a two-gene effect |
| `Cpt1c` | 1 | `Cpt1c` down | ER-associated HSP/lipid comparator; self-transcript only |
| `Klc2` | 1 | `Klc2` down | axonal-transport comparator; self-transcript only |
| `Ddhd2` | 0 | none | lipid/lipophagy HSP comparator; no focal RNA response |
| `Retreg1` | 1 | `Retreg1` down | mouse FAM134B, the ARL6IP1 ER-phagy cluster partner; self-transcript only |

This panel argues strongly against borrowing a broad transcriptional response
from an ER-shaping disease phenotype. `Arl6ip1` should not phenocopy a high-DEG
stress or chromatin perturbation under these conditions.

I also used several counterexample panels. Core autophagy genes were flat or
nearly flat in the focal class: `Atg5`, `Becn1`, and `Atg16l1` had 0 DEGs, and
`Rb1cc1` had 4 DEGs. ER-proteostasis perturbations showed that the focal
neurons can reveal ER stress when the perturbation actually engages that state:
`Hspa5`, `Manf`, and `Sec63` had 5, 3, and 11 DEGs, respectively, with
`Hspa5`, `Pdia4`, `Pdia6`, `Hyou1`, `Canx`, or `Chac1` among their significant
features. However, `Atf6`, `Edem3`, `Lman2l`, `Mttp`, `Suco`, and `Ap4s1` were
0-DEG and `Bcap31` and `Amfr` were self-only or near self-only, matching the
Distributed Agents corpus claim that a BiP/ERAD module is recoverable but not generic to
all ER-associated loss. Mitochondrial morphology was similarly nontransferable:
`Opa1` had a clear 37-DEG ATF4/ISR-like amino-acid-stress signature in the
focal class, whereas `Mff` had 0. Although ARL6IP1 can affect
mitochondria-associated ER membranes, its closest ER-shaping and ER-phagy
comparators do not approach `Opa1`.

The remaining question is whether the point prediction should be 0 or 1. The
best external and within-dataset evidence both put the expected downstream
program at zero, but ARL6IP1 itself is a measured gene in the focal signature
matrix, and many of the closest small ER-shaping/HSP comparators have exactly
one DEG consisting of their own transcript. I therefore predict a single
FDR-significant gene, most likely `Arl6ip1` itself, with no broad downstream
RNA program.

## Prediction

`Arl6ip1`: predicted `n_degs = 1`

## Limits and extrapolation

There is no direct `Arl6ip1` perturbation profile in the supplied training
parquet or in the focal training-count CSV, and the selected Distributed Agents semantic
corpus had no direct `Arl6ip1` claim. The prediction therefore transfers from
mechanistically related ER-shaping and ER-phagy genes, none of which is a
perfect ARL6IP1 phenocopy. The strongest ARL6IP1 phenotypes in the literature
involve chronic HSP models, sensory neurons, motor axons, Drosophila systems,
ER-phagy flux, lipid droplets, and organelle morphology; these are poorly
matched to an acute, partial, postnatal, basal snRNA-seq endpoint in recovered
thalamic glutamatergic nuclei. Finally, the choice between 0 and 1 DEG hinges
on whether the specific four CRISPR guides drive an FDR-significant decrease
of nuclear `Arl6ip1` RNA, which cannot be inferred reliably from biology alone.
