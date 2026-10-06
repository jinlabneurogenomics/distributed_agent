# Exoc6b DEG-count prediction

## Question interpreted

The requested target list contains one held-out mouse perturbation:

```tsv
target_name
Exoc6b
```

The endpoint to predict is `n_degs`, the number of measured genes whose Wilcoxon
Benjamini-Hochberg adjusted p-value is below 0.05 in `151 TH Prkcd Grin2c
Glut` nuclei after acute AAV CRISPR loss of the target. I treated this as the
same endpoint tabulated in
`151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`; if the target transcript
itself passed FDR in a training perturbation, the training `n_degs` includes it.

I resolved two ambiguities explicitly:

- `151 TH Prkcd Grin2c Glut` is the focal thalamic glutamatergic cell group,
  not a nucleus count.
- A predicted zero means no measured transcript, including `Exoc6b`, is
  expected to pass adjusted `p < 0.05`. It does not mean the edit is expected to
  be biologically inert or that exocyst protein function is dispensable.

## Sources used

- The held-out manifest
  `[local file: 073_Exoc6b.csv]`.
- The focal training count table
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
  It contains 1,674 non-held-out perturbations in the focal cell group: 1,205
  have `n_degs = 0`, 469 are nonzero, the median is 0, the 75th percentile is 1,
  the 90th percentile is 2, and the 95th percentile is 18.
- The differential-expression parquet
  `[local file: training_de_all_cell_groups.parquet]`.
  I used it to recover focal-cell signatures for mechanistic analogs rather
  than relying only on the pre-counted endpoint.
- The same-experiment Distributed Agents semantic corpus
  `perturbai-july-260713-sourceguard-1773-v1`. The target `Exoc6b` and the
  word `exocyst` were not represented by direct corpus Findings or Claims, so I
  used the corpus only for related vesicle, synapse, AMPAR/NMDAR, Rho/Ral, and
  endomembrane counterexamples.
- NCBI PubMed, via PubMed E-utilities, for external EXOC6B and exocyst
  literature.

Key external literature used:

- Brymora et al. 2001 showed that the brain exocyst binds active RalA and
  identified a second mammalian Sec15 homolog. DOI `10.1074/jbc.C100320200`,
  PMID `11406615`.
- Murthy et al. 2003 found that Drosophila `sec5` mutants disrupt neurite
  outgrowth and neuromuscular-junction growth but spare synaptic-vesicle
  fusion. DOI `10.1016/s0896-6273(03)00031-x`, PMID `12575951`.
- Riefler et al. 2003 and Sans et al. 2003 connected Sec8/exocyst to PSD-95 or
  SAP102/NMDA-receptor trafficking. DOI `10.1042/BJ20021838`, PMID `12675619`;
  DOI `10.1038/ncb990`, PMID `12738960`.
- Mehta et al. 2005 showed a Sec15 requirement for neuronal targeting of a
  subset of exocyst components in Drosophila. DOI
  `10.1016/j.neuron.2005.02.029`, PMID `15848801`.
- Gerges et al. 2006 separated Sec8- and Exo70-dependent steps in AMPA-receptor
  targeting and synaptic insertion. DOI `10.1038/sj.emboj.7601065`, PMID
  `16601687`.
- Martin-Urdiroz et al. 2016 reviewed the exocyst as an octameric tethering
  complex for exocytosis, polarity, signaling, and cilium-related biology. DOI
  `10.3389/fcell.2016.00024`, PMID `27148529`.
- Koon et al. 2018 and Lira et al. 2018 showed Exo70 roles in synaptic growth,
  dendritic arborization, synapse density, and vesicle recycling. DOI
  `10.1523/JNEUROSCI.0620-18.2018`, PMID `30209205`; DOI
  `10.1007/s12035-018-1378-0`, PMID `30374940`.
- Fruhmesser et al. 2013, Evers et al. 2014, Girisha et al. 2015, and
  Simsek-Kiper et al. 2022 linked human EXOC6B disruption to
  neurodevelopmental or skeletal disease phenotypes, and Simsek-Kiper et al.
  also provided fibroblast evidence for impaired primary ciliogenesis. DOI
  `10.1038/ejhg.2013.18`, PMID `23422942`; DOI `10.1002/ajmg.a.36770`, PMID
  `25256811`; DOI `10.1038/ejhg.2015.261`, PMID `26669664`; DOI
  `10.1002/humu.24478`, PMID `36150098`.

## Computational checks on the training data

I first read the focal training-count CSV to establish the endpoint scale and to
query genes in candidate pathways. I then inspected the Parquet metadata and
found that row groups are partitioned by `group_name`, so the focal cell group
could be pulled without scanning the whole table.

For candidate perturbations, I filtered the Parquet to the focal group and to
the nominated training genes:

```python
filt = (
    (pc.field("group_name") == "151 TH Prkcd Grin2c Glut")
    & pc.field("gene_target").isin(candidate_targets)
)
```

I counted `pvals_adj < 0.05` for each target, recorded matched perturbed and
control nucleus counts, and inspected the significant genes. This was important
because several `n_degs = 1` training perturbations only recovered the target
transcript itself:

- `Cdc42`: 1 DEG, only `Cdc42`, log2FC `-0.593`, FDR `8.62e-05`.
- `Cplx1`: 1 DEG, only `Cplx1`, log2FC `-0.863`, FDR `4.29e-24`.
- `Dnm1`: 1 DEG, only `Dnm1`, log2FC `-0.712`, FDR `4.09e-25`.
- `Stxbp1`: 1 DEG, only `Stxbp1`, log2FC `-0.663`, FDR `9.38e-19`.
- `Syp`: 1 DEG, only `Syp`, log2FC `-1.776`, FDR `7.95e-66`.
- `Syn1`: 1 DEG, only `Syn1`, log2FC `-0.834`, FDR `1.59e-24`.
- `Vamp1`: 1 DEG, only `Vamp1`, log2FC `-0.465`, FDR `1.87e-03`.

I also ran a profile comparison in the same focal group over `Rala`, `Cdc42`,
Rab-cycle genes, SNARE/presynaptic genes, `Cltc`, `Vps35`, and `Rab7`.
The run-local Distributed Agents profile artifact reported 6 of these selected nodes
with no significant features, 6 with 1-9 significant features, 1 with 10-49,
and only `Rab7` with at least 50. Pairwise comparisons between the key anchors
and the Rab/SNARE/presynaptic peers had no same-direction FDR-significant
feature intersections; `Rab7` was the only broad-expression outlier and was not
matched by the more proximal Rab-cycle or release perturbations.

## Target-specific reasoning

### Exoc6b

`Exoc6b` encodes a Sec15-family subunit of the octameric exocyst complex, which
tethers post-Golgi and recycling-endosome vesicles to selected plasma-membrane
sites. The closest literature links are to targeted membrane addition and
receptor/cargo delivery, not to a canonical transcription factor or a stress
response pathway. RalA is an established brain exocyst interactor, Sec8 and
Exo70 participate in glutamate-receptor trafficking, and Drosophila Sec5,
Sec15, and Exo70 perturbations affect neurite targeting or synaptic growth.

The focal training set had no direct `Exoc1`-`Exoc8` structural subunits, so
the evidence came from indirect analogs and counterexamples:

| Training perturbations | Focal `n_degs` | Expression-pattern evidence | Relevance |
| --- | ---: | --- | --- |
| `Rala`, `Cdc42` | `0`, `1` | `Rala` had no FDR-significant gene; `Cdc42` had only self-target `Cdc42` down. The same-experiment corpus reported that represented RHO/formin and Rho-family cytoskeletal perturbations, including `Rala` or `Cdc42` as comparators, did not form convergent neuronal snRNA-seq modules (`claim:41f9ace68f95c8cfa7fa`, `claim:767b4eb73b8456c34ded`, `claim:1aeabad1e41e30f971bc`). | These are the most proximal measured small-GTPase connections to exocyst/polarity biology. Their focal profiles argue that perturbing an exocyst regulatory neighborhood does not usually cross the FDR threshold in these thalamic neurons. |
| `Rab18`, `Rab27a`, `Rab3gap1`, `Rab3gap2` | all `0` | No focal DEGs. The corpus summarized Rab3/Rab18/Rab27/RAB3GAP relatives as flat, sparse, or non-overlapping rather than pathway-interchangeable (`claim:d28c08c3dc2e0831c`). | These are not the direct Rab8/Rab11 exocyst axis, but they bound the idea that Rab/vesicle-cycle annotation alone should create a nuclear RNA response. |
| `Cplx1`, `Cplx2`, `Stxbp1`, `Stx1b`, `Vamp1`, `Syp`, `Syn1`, `Dnm1`, `Bsn`, `Pclo`, `Unc13a`, `Unc13b`, `Unc13c` | mostly `0` or self-only `1` | `Cplx1`, `Stxbp1`, `Vamp1`, `Syp`, `Syn1`, and `Dnm1` were self-only in 151 TH; `Cplx2`, `Stx1b`, `Bsn`, `Pclo`, and the three `Unc13` genes were zero. Corpus claims found that presynaptic vesicle-cycle, active-zone, SNARE-cycle, complexin, synapsin, dynamin, and related release perturbations generally lacked broad steady-state neuronal RNA modules (`claim:dca6b049615a34cf831d`, `claim:c289360a665b7efbd17d`, `claim:e1dee3db28d664657805`, `claim:f48dd8852b94eb3b98e0`). | Exoc6b should influence constitutive polarized cargo delivery more than fast synaptic vesicle fusion, but these genes show that even severe synaptic machinery perturbations are often transcriptionally buffered in the assay endpoint. |
| `Gria1`, `Gria2`, `Gria3`, `Cacng2`, `Cacng3`, `Iqsec1`, `Iqsec2`, `Dlg4`, `Grin2b` | `0`, `0`, `0`, `0`, `0`, `0`, `0`, `1`, `2` | AMPAR/TARP/IQSEC genes were zero; `Dlg4` was self-only; `Grin2b` produced `Grin2b` plus `Pianp`. Corpus claims reported that represented AMPAR-core and AMPAR-trafficking/scaffold perturbations were buffered and that IQSEC/PSD-associated perturbations did not form a generic NMDAR/PSD transcriptomic program (`claim:a9367c3aeaad95bfae9c`, `claim:c0a95241aec700bec1c8`). | Sec8/Exo70 literature connects the exocyst to AMPAR and NMDAR receptor delivery, but same-assay receptor/scaffold perturbations near that phenotype were near-null at the nuclear RNA level. |
| `Trappc6b`, `Trappc9`, `Trappc10`; `Cog4`, `Cog5`, `Copa`, `Copg1`, `Stx5a`, `Tmem165`, `Trip11` | TRAPP all `0`; Golgi/COPI mostly `0`, `Copg1 = 1` self-only | Corpus claims found TRAPP II-related responses sparse and subunit-specific, and ER-Golgi/COPI/COG/SNARE/glycosylation perturbations did not produce a shared broad secretory-pathway module (`claim:d83b18fc04f647406a6b`, `claim:6a94b158a9de9a66a6c3`). | These are broad secretory or Golgi-traffic controls. They argue against assigning a large count solely because EXOC6B is a vesicle-tethering factor. |
| `Cltc`, `Vps35`, `Rab7` | `3`, `17`, `501` | `Cltc` had three focal DEGs: `Gabra4`, `Rbms1`, `Ero1b`. `Vps35` had a modest retromer signature including `Atp2a2`, `Brsk1`, `Grin2b`, and `Vps35`. `Rab7` had a large late-endosomal/lysosomal/sterol response led by genes such as `Atp6v1b2`, `Ptgds`, `Dpp7`, `Scpep1`, `Dusp1`, and `Insig1`. Corpus claims used these as detectable trafficking boundaries and showed that related Retriever/Commander/WASH or adjacent endolysosomal targets were flat or nonconvergent (`claim:a251c65f7a3f32088f68`, `claim:726468d7afc216bc3be2`, `claim:491c5c6eb002662cbefd`). | These prevent the trivial conclusion that trafficking genes are invisible in 151 TH, but their lysosomal or retromer stress programs are not close analogs of Sec15B-dependent exocyst tethering. |

Zero versus nonzero:

The external biology makes `Exoc6b` a plausible neuronal trafficking and
developmental gene, so I did not treat it as a random unexpressed or irrelevant
target. However, the endpoint is an acute postnatal soma/nuclear RNA response.
The most relevant measured neighborhood, `Rala` plus nearby small GTPases and
presynaptic or receptor-trafficking genes, sits at zero or self-only counts in
151 TH. Larger in-dataset trafficking responses were branch-specific
late-endosomal or retromer states and should not be transferred to the exocyst
only from the word "trafficking".

I therefore predict that acute sparse `Exoc6b` loss will be transcriptionally
buffered in the recovered `151 TH Prkcd Grin2c Glut` nuclei and that no
measured gene will pass FDR 0.05.

Predicted `n_degs`: `0`.

## Limits

- There is no direct Exoc6b same-experiment Finding, no direct held-out
  Exoc6b signature, and no represented exocyst structural subunit in the
  training-count table. The prediction extrapolates from regulators and
  neighboring vesicle-trafficking pathways.
- The exocyst literature measures receptor localization, vesicle tethering,
  synapse morphology, cilia, and development in Drosophila, cultured neurons,
  fibroblasts, chondrocytes, or human genetics. Those phenotypes can be strong
  while remaining invisible to 3-4-week post-perturbation single-nucleus RNA in
  sparse surviving mouse thalamic neurons.
- Several useful exocyst interactors, especially Rab8 and Rab11 family members
  and other mammalian exocyst subunits, were not in the focal training endpoint
  table, so the absence of a direct paralog or complex-mate response weakens
  the comparison.
- The focal `n_degs` endpoint is power-dependent. Some training analogs had
  substantially different recovered perturbed nuclei, such as `Cltc` with 32
  and `Rala` with 199, and Exoc6b's held-out perturbed count is unknown.
- Self-target transcript loss was not used as a proxy for editing efficiency or
  for downstream impact. For this prediction, self-only singleton responses in
  analogs were interpreted as closer to downstream-zero than as evidence for a
  broad state.
