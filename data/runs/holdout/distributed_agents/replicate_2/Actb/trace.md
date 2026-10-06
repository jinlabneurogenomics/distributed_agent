# Reasoning trace

## Question interpreted

The requested endpoint is the integer `n_degs` that would have been observed for
each held-out perturbation in `151 TH Prkcd Grin2c Glut` neurons, where a DEG is
one measured output gene with `pvals_adj < 0.05` in the Wilcoxon DE table.

This run has one held-out target:

```text
Actb
```

I treated the focal DE matrix as having the same measured feature universe as
the hidden `Actb` signature. That matters here because `Actb` is a held-out
perturbation target but was not present as a measured output gene in a focal
training signature, while `Actg1`, `Cdc42`, `Pak1`, and several other actin
neighbors scored as one-DEG perturbations only because their own transcript was
significantly depleted.

## Sources used

- Requested target manifest:
  `[local file: 003_Actb.csv]`
- Focal-cell training endpoint counts:
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`
- Full training DE parquet:
  `[local file: training_de_all_cell_groups.parquet]`
- Distributed Agents same-experiment corpus MCP,
  release `perturbai-july-260713-sourceguard-1773-v1`
  - `target_context(Actg1)`, especially `Actg1:F001` and `Actg1:F005`
  - `target_context(Cdc42)`, `target_context(Rac1)`, `target_context(Cyfip1)`,
    `target_context(Cyfip2)`, `target_context(Actn4)`,
    `target_context(Tpm3)`
  - `search_claims` for cytoskeletal and Rac/Cdc42 claims
  - `resolve_evidence(Actg1:F005)`, `resolve_evidence(Cdc42:F003)`,
    `resolve_evidence(Actn4:F004)`
- PubMed via `mcp__bioeval_literature` for outside gene-function priors:
  - Perrin and Ervasti 2010, `The actin gene family: function follows
    isoform`, doi:10.1002/cm.20475, PMID:20737541.
  - Bunnell et al. 2011, `Beta-Actin specifically controls cell growth,
    migration, and the G-actin pool`, doi:10.1091/mbc.E11-06-0582,
    PMID:21900491.
  - Riviere et al. 2012, `De novo mutations in the actin genes ACTB and ACTG1
    cause Baraitser-Winter syndrome`, doi:10.1038/ng.1091, PMID:22366783.
  - Miralles et al. 2003, `Actin dynamics control SRF activity by regulation of
    its coactivator MAL`, doi:10.1016/S0092-8674(03)00278-2,
    PMID:12732141.
  - Govek et al. 2005, review of neuronal Rho GTPase biology,
    doi:10.1101/gad.1256405, cited by the Distributed Agents Cdc42 evidence.
  - Reactome pathway `Activation of WASP and N-WASP by CDC42`,
    `R-HSA-442586`, cited by the Distributed Agents Cdc42 evidence.

The Distributed Agents corpus includes cross-cell-group FDR<0.10 findings. I used those
as same-experiment biological context and checked the exact focal-cell,
FDR<0.05 counts directly from the supplied CSV/parquet before assigning the
point prediction.

## Computational checks

The focal training count table contains 1,674 non-held-out perturbations:
1,205 have zero DEGs, the median count is 0, the 75th percentile is 1, the 95th
percentile is 18, and the maximum is 2,677. Thus the assay can detect very
broad effects, but the common outcome is no FDR<0.05 feature.

I loaded the focal rows for a curated set of actin, Rho/WAVE, PAK/LIMK,
MRTF, myosin, tropomyosin, and actin-crosslinking training targets and counted
`pvals_adj < 0.05` directly. The operation was:

```python
df = dataset.to_table(
    columns=["names", "gene_target", "scores", "logfoldchanges", "pvals_adj"],
    filter=(
        pc.field("group_name") == "151 TH Prkcd Grin2c Glut"
    ) & pc.field("gene_target").isin(selected_actin_targets),
).to_pandas()

n_degs = df.groupby("gene_target").pvals_adj.apply(lambda s: (s < 0.05).sum())
scores = df.pivot(index="names", columns="gene_target", values="scores")
actg1_r = scores["Actg1"].corr(scores[g])
```

I also read the 17,259 measured genes for the `Actg1` focal signature and
verified that `Actb` was absent while nearby actin-pathway transcripts such as
`Actg1`, `Actr2`, `Actr3`, `Arpc1a`, `Cfl1`, `Dstn`, `Pfn1`, `Pfn2`, `Rhoa`,
`Srf`, and `Mrtfb` were present. Therefore an `Actb` perturbation cannot be
credited with the one self-transcript DEG that would otherwise be the most
likely event.

## Same-assay analogs and counterexamples for Actb

| training target(s) | focal `n_degs` | focal signature evidence | relevance to `Actb` |
| --- | ---: | --- | --- |
| `Actg1` | 1 | The only FDR<0.05 gene was `Actg1` itself, logFC -0.824, adjusted p = 9.85e-16. No downstream gene passed FDR in this focal group. | Closest usable paralog of cytoplasmic beta-actin. Its near-null surface is the strongest same-assay argument against a broad nuclear transcriptome after perturbing a single cytoplasmic actin isoform. |
| `Cdc42`, `Rac1` | 1, 0 | `Cdc42` had exactly one focal DEG, its own transcript; `Rac1` had none. Actg1-vs-Cdc42 and Actg1-vs-Rac1 focal Wilcoxon-score correlations were -0.010 and -0.008. | Rho-family GTPases are canonical upstream organizers of WASP/WAVE, Arp2/3, PAK/LIMK, cofilin, and dendritic actin. Their focal signatures were self-only or flat. |
| `Cyfip1`, `Cyfip2`, `Baiap2`, `Washc4` | 0, 1, 0, 0 | `Cyfip2` was self-only; the others were FDR-null. `Cyfip2` had essentially no focal correlation with `Actg1`, r = 0.001. | These touch the WAVE regulatory complex or adjacent Arp2/3 actin remodeling. They are good counterexamples to the idea that WRC/branched-actin disruption gives a shared RNA state in this assay. |
| `Pak1`, `Pak2`, `Pak3`, `Limk1`, `Cfl2` | 1, 0, 0, 0, 0 | `Pak1` was self-only; PAK/LIMK/cofilin perturbations had no non-self focal FDR calls. | The Rac/Cdc42 to PAK/LIMK/cofilin arm did not project onto sustained nuclear mRNA in the focal cell group. |
| `Mrtfa` | 0 | No focal FDR calls; weak target-transcript trend was upward rather than knockdown-like, and its Actg1 score correlation was -0.017. | MRTF/SRF is the obvious transcriptional sensor of actin polymerization, but isolated `Mrtfa` perturbation did not resemble `Actg1` or create a focal SRF-response signature. |
| `Tpm1`, `Tpm3` | 0, 0 | Both tropomyosin perturbations were focal nulls. Distributed Agents `Tpm3:F002` further reported no `Tpm1`, `Tpm2`, or `Tpm4` transcript rebound after `Tpm3` perturbation. | Tests whether loss of an actin-filament component drives a generic actin-damage or paralog-compensation mRNA program. It did not. |
| `Actn4`, `Flnb` | 0, 0 | Both were FDR-null in the focal cell type; Actg1-vs-Actn4 and Actg1-vs-Flnb score correlations were 0.017 and 0.006. | Actin crosslinking and filamin-family structural neighbors were quiet, supporting a structural/local rather than nuclear-RNA response. |
| `Fmn2`, `Diaph2`, `Myo5a`, `Myo6`, `Myo9a` | 0, 0, 1, 0, 0 | `Myo5a` was self-only; formins and myosins otherwise lacked downstream focal DE. The largest absolute `Actg1` correlation in the curated focal set was only `Myo5a` r = 0.056. | Formin-mediated linear actin assembly and actin motors are pathway-adjacent but poor phenotype matches; their near-null profiles bound the possibility of a broad actomyosin stress response. |

The Distributed Agents corpus generalizes these focal observations across all recovered
cell groups. `Actg1:F005` compared 20 represented actin-network targets,
including `Cdc42`, `Rac1`, `Cyfip1`, `Cyfip2`, `Limk1`, `Pak1-3`, `Diaph2`,
`Fmn2`, `Mrtfa`, myosins, tropomyosins, and `Washc4`; it found that these
targets did not phenocopy the two weak `Actg1` responder classes. The high
confidence Rac/Cdc42 cytoskeleton claim `claim:1aeabad1e41e30f971bc` similarly
states that represented Rac/Cdc42-linked actin-cytoskeleton signaling
perturbations are transcriptionally buffered in juvenile neurons rather than
forming a recurrent shared nuclear mRNA module. The moderate `Actn4:F004`
finding reached the same boundary from another structural actin node.

## Biology-to-count reasoning for Actb

`ACTB` and `ACTG1` encode the two ubiquitous cytoplasmic actin isoforms. They
are extremely close biochemically but are not perfectly interchangeable: mouse
`Actb` loss is embryonically lethal and changes growth, migration, the G-actin
pool, and gene expression in fibroblasts, whereas human ACTB/ACTG1 developmental
actinopathies are dominated by de novo missense mechanisms rather than simple
postnatal loss of function (Perrin and Ervasti 2010; Bunnell et al. 2011;
Riviere et al. 2012). Actin dynamics can signal to SRF through MAL/MRTF, and
CDC42/RAC1 can signal to WASP/WAVE, Arp2/3, PAK, LIMK, and cofilin, so a broad
actin-stress or cytoskeletal-compensation RNA program was a plausible outside
prior (Miralles et al. 2003; Govek et al. 2005; Reactome R-HSA-442586).

The same-assay evidence argues that this prior does not transfer to the basal
P16-to-P37/P44 sparse neuronal snRNA-seq endpoint:

- In the focal cell group, no represented actin-network perturbation produced a
  non-self DEG at FDR<0.05.
- The nearest paralog `Actg1` had exactly one focal FDR call, and that was
  target-transcript depletion.
- `Actb` itself was not in the measured output feature universe, so a comparable
  on-target RNA decrease would not increase `n_degs`.
- Rho/WAVE, PAK/LIMK/cofilin, MRTF, tropomyosin, formin, myosin, alpha-actinin,
  and filamin comparators were flat or self-only and had near-zero score-vector
  correlations to `Actg1`.
- The same-experiment Distributed Agents corpus found no hidden pan-neuronal actin,
  Rac/Cdc42, CYFIP/WRC, or tropomyosin module across the broader screen.

I therefore predict that acute sparse `Actb` loss would not place any measured
gene below FDR 0.05 in `151 TH Prkcd Grin2c Glut` cells.

## Limits

This is an extrapolation because the true `Actb` perturbation signature was
fully held out and the closest beta/gamma-actin compensation test is exactly
what the holdout removes. The prediction also assumes that the hidden `Actb`
DE calculation used the same measured-gene filtering as the visible focal
signatures. The screen measured surviving NeuN-positive nuclei at the soma and
did not assay indels, ACTB protein, F-actin architecture, local translation,
endocytosis, spine morphology, electrophysiology, or cell abundance. `Actb`
could easily have a structural or viability effect that is invisible to
`n_degs`; I am only predicting the FDR<0.05 breadth of the nuclear RNA readout.
