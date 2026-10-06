# Reasoning trace

## Question and resolved ambiguities

The requested held-out target list contains one mouse perturbation:

```text
Trrap
```

For that target I predicted `n_degs`, the number of measured genes whose Wilcoxon
Benjamini-Hochberg adjusted p-value is below 0.05 in the focal
`151 TH Prkcd Grin2c Glut` population after acute postnatal AAV CRISPR loss of
function. The value is a point prediction for this assay-specific thresholded
RNA endpoint, not an estimate of TRRAP biochemical importance, editing success,
or viability.

`Trrap` is completely absent from both the differential-expression parquet and
the focal training-count CSV. I therefore treated all direct target counts and
signatures for `Trrap` as unknown, and only transferred evidence from observed
training perturbations and external TRRAP biology.

## Sources used

- Input endpoint table:
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`
- Input DE table:
  `[local file: training_de_all_cell_groups.parquet]`
- Requested-target manifest:
  `[local file: 249_Trrap.csv]`
- Distributed Agents same-experiment corpus, release
  `perturbai-july-260713-sourceguard-1773-v1`.
- Distributed Agents runtime profile-neighborhood/profile-compare tables computed over
  the focal `151 TH Prkcd Grin2c Glut` rows.
- PubMed literature on TRRAP as a SAGA / NuA4-TIP60 scaffold and MYC/E2F
  cofactor:
  - McMahon et al. 1998, DOI `10.1016/S0092-8674(00)81479-8`, PMID `9708738`.
  - Lang et al. 2001, DOI `10.1074/jbc.M102067200`, PMID `11418595`.
  - Lang and Hearing 2003, DOI `10.1038/sj.onc.1206376`, PMID `12743606`.
  - Elias-Villalobos et al. 2019, DOI `10.1042/BST20180496`, PMID `31769470`.
  - Yang et al. 2024, DOI `10.1126/science.adl5816`, PMID `39088653`.

The Distributed Agents corpus had no direct `Trrap` finding or claim, so I used it only
for same-experiment information about observed analogs such as `Atxn7`, `Myc`,
and `Mga`.

## Computational summary

The manifest has exactly one row, `Trrap`.

The focal training-count file has 1,674 assayed non-held-out targets. Its
endpoint distribution is very zero-heavy in this cell group:

- median `n_degs`: 0
- mean `n_degs`: 14.05
- nonzero targets: 469 / 1,674
- maximum: 2,677, from `Uba5`

I inspected the parquet metadata and found that the focal cell group is stored
in a compact row-group block. Filtering by
`group_name = '151 TH Prkcd Grin2c Glut'` gives 28,891,566 DE rows:

```sql
SELECT group_name,
       COUNT(*) AS rows,
       COUNT(DISTINCT gene_target) AS targets,
       COUNT(DISTINCT names) AS measured
FROM training_de_all_cell_groups
WHERE group_name = '151 TH Prkcd Grin2c Glut'
GROUP BY group_name;
```

This is exactly 1,674 perturbations x 17,259 measured genes. I then counted
`pvals_adj < 0.05` for biologically nominated analogs and counterexamples, and
computed score-vector Pearson/cosine comparisons among those anchors in the
same focal table.

## Target-specific reasoning

### Trrap

#### External biology

TRRAP is the large catalytically dead PIKK-family scaffold shared by SAGA /
GCN5/PCAF and NuA4/TIP60 HAT assemblies rather than a sequence-specific
transcription factor. It was originally isolated as a c-Myc and E2F cofactor
required for oncogenic transcriptional programs (McMahon et al. 1998), E2F
transactivation can recruit TRRAP and GCN5 HAT activity (Lang et al. 2001), and
human TRRAP was found in TIP60 and GCN5/PCAF HAT complexes (Lang and Hearing
2003). A review by Elias-Villalobos et al. 2019 places Tra1/TRRAP as a scaffold
that assembles and recruits SAGA and NuA4/TIP60 to chromatin. Recent
NuA4/TIP60 structural work showed that EP400 and TRRAP contact each other and
that loss of TRRAP can mislocalize the NuA4/TIP60 complex and redistribute
H2A.Z acetylation in human cells (Yang et al. 2024).

Those priors make SAGA/NuA4 subunits, HAT coactivators, and MYC/E2F-network
factors the most appropriate training analogs. They also warn against using
generic "chromatin regulator" counts without checking expression-pattern
evidence: a central TRRAP scaffold could matter in proliferating or
DNA-damaged cells while still being buffered at a basal mRNA endpoint in
settled juvenile neurons.

#### Relevant within-dataset perturbations

The closest direct SAGA/NuA4/TIP60 perturbation in the training endpoint is
`Atxn7`, a SAGA deubiquitinase-module subunit. It had 0 focal DEGs from 124
matched perturbed nuclei. The Distributed Agents same-experiment corpus describes
`Atxn7` as transcriptomically buffered across the postmitotic neuronal panel:
20 measured groups and 1,021 perturbed nuclei produced zero downstream genes at
FDR < 0.10. In the focal score space `Atxn7` also had only noise-scale
relationships to other nominated anchors:

- `Atxn7` vs `Myc`: Pearson 0.026, cosine 0.027, no shared FDR 0.05 genes.
- `Atxn7` vs `Mga`: Pearson 0.005, cosine 0.001, no shared FDR 0.05 genes.
- `Atxn7` vs `Crebbp`: Pearson 0.025, cosine 0.021, no shared FDR 0.05 genes.
- `Atxn7` vs `Yeats2`: Pearson 0.009, cosine 0.009, no shared FDR 0.05 genes.

Many stronger same-complex tests were unavailable: the focal training-count
file did not include `Kat5`, `Ep400`, `Ruvbl1`, `Ruvbl2`, `Dmap1`, `Ing3`,
`Brd8`, `Epc1`, `Epc2`, `Yeats4`, `Kat2a`, `Kat2b`, `Taf5l`, `Taf6l`,
`Supt3`, `Supt7l`, `Atxn7l3`, or `Usp22`.

The represented HAT/coactivator perturbations did not expose a hidden
TRRAP-like HAT-collapse response in this cell group:

| training perturbation | focal `n_degs` | focal matched perturbed nuclei | relevance |
|---|---:|---:|---|
| `Atxn7` | 0 | 124 | observed SAGA subunit |
| `Yeats2` | 0 | 99 | HAT-complex-adjacent YEATS protein |
| `Crebbp` | 8 | 61 | p300/CBP acetyltransferase coactivator paralog |
| `Ep300` | 0 | 155 | p300/CBP acetyltransferase coactivator paralog |
| `Kat6a` | 0 | 170 | MOZ/MORF acetyltransferase |
| `Kat6b` | 0 | 150 | MOZ/MORF acetyltransferase |
| `Brd1` | 4 | 178 | KAT6/BRPF-complex member |

The tiny `Crebbp` and `Brd1` signatures did not align with `Atxn7` or with each
other in a way that would justify lifting `Trrap` above the threshold. For
example, `Crebbp` vs `Ep300` had Pearson 0.090 but no shared FDR 0.05 genes,
and `Brd1` vs `Kat6a` had Pearson -0.004.

The observed transcription-factor side of TRRAP biology was also flat or
singleton-scale:

| training perturbation | focal `n_degs` | focal matched perturbed nuclei | relevance |
|---|---:|---:|---|
| `Myc` | 0 | 210 | direct TRRAP-interacting MYC family TF |
| `Mycn` | 0 | 320 | MYC family |
| `Mnt` | 0 | 226 | MAX-network repressor |
| `Mga` | 2 | 82 | MAX-network/PRC1.6 factor |
| `Mlxip` | 0 | 182 | MAX/Mondo-adjacent network factor |
| `E2f1` | 0 | 253 | E2F activator |
| `E2f5` | 0 | 117 | E2F family |
| `Tfdp1` | 2 | 203 | E2F/DP partner |
| `Tfdp2` | 0 | 184 | E2F/DP partner |
| `Trp53` | 0 | 251 | DNA-damage/apoptosis axis counterexample |
| `Cdkn2a` | 0 | 346 | cell-cycle checkpoint counterexample |

The Distributed Agents corpus independently summarized this part of the screen as
showing that represented MYC/MAX-network and E2F/Mondo/metabolic perturbations
do not form a shared postmitotic neuronal transcriptomic module. Its `Myc`
finding called acute `Myc` loss a pan-neuronal transcriptomic null in the
P16-to-P37/44 NeuN+ screen. `Mga` produced only two upregulated genes in this
focal group, `Obscn` and `Stag3`, and the corpus tied that to a small
MGA-specific derepression response rather than to a generic MYC/MAX/E2F state.
In my focal profile comparison, `Myc` vs `E2f1` had Pearson/cosine 0.007/0.007,
`Atxn7` vs `Myc` 0.026/0.027, and `Mga` vs `E2f1` 0.002/0.002, again with no
overlapping significant genes.

As counterexamples, the same focal endpoint is fully capable of detecting broad
chromatin and RNA-processing responses when the perturbation engages this
postmitotic state: `Sin3a` had 1,433 focal DEGs, `Brd4` had 311, `Smarcc2` had
185, and `Setdb1` had 22. I did not transfer those large counts to `Trrap`
because their observed signatures and mechanistic assignments are different:
`Setdb1` derepressed a local H3K9/protocadherin/HUSH-adjacent program, and the
Brd4 response was not a MYC-axis or p300/CBP/Mediator phenocopy in the
Distributed Agents corpus. These are evidence that the assay has power for chromatin
regulators, not positive evidence for a TRRAP-like module.

#### Zero/nonzero decision

The strongest positive external prior is that TRRAP is central to two HAT
complexes, so a full acute depletion in a sensitive context could be broad.
However, the assay is a partial CRISPR loss in settled P37-P44 NeuN+ nuclei,
not a proliferating MYC/E2F-driven cell or a degron-level removal of TRRAP.
Within this exact perturbation modality and focal cell class, the SAGA,
HAT/coactivator, MYC/MAX, and E2F-side anchors were observed as 0, 2, 4, or 8
DEG cases, and their weak whole-profile correlations argue against an
unobserved coherent HAT or MYC/E2F subthreshold module.

I therefore predicted a thresholded zero:

```text
Trrap -> 0
```

## Limits

This is an extrapolation from imperfect analogs. `Trrap` itself is more central
than `Atxn7`, `Kat6a`, `Kat6b`, `Crebbp`, or `Ep300`, and the most direct mouse
NuA4/TIP60 and SAGA subunits were not available as training perturbations. The
RNA endpoint also cannot measure histone acetylation, H2A.Z localization, DNA
repair defects, electrophysiology, or long-term survival. Finally, zero here
means no measured genes are expected to pass FDR 0.05 in this powered
Wilcoxon/snRNA-seq readout; it does not mean the edited neurons have no
TRRAP-dependent molecular changes.
