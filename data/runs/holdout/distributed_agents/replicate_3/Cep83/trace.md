# Question

The held-out manifest for this run contains one target, `Cep83`. I interpreted the
task as a point prediction for the exact focal endpoint used in
the focal training count CSV: the number of measured
genes with `pvals_adj < 0.05` in `151 TH Prkcd Grin2c Glut` after acute postnatal
AAV-CRISPR perturbation.

The main ambiguity I resolved was how to treat genes in the same organelle when
their measured transcriptome was nearly null. For `Cep83`, the relevant biology is
not a generic centrosome label but its position at the root of centriole distal
appendages, upstream of membrane docking and cilium initiation. I therefore gave
most weight to represented distal-appendage and core ciliogenesis genes, then used
the broader IFT/BBS/transition-zone/Hedgehog set as counterevidence against a
large hidden ciliary RNA state.

# Sources

Internal data and corpus:

- Input focal DEG-count table:
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`
- Input DE parquet:
  `[local file: training_de_all_cell_groups.parquet]`
- Held-out manifest:
  `[local file: 036_Cep83.csv]`
- Distributed Agents same-experiment corpus
  `perturbai-july-260713-sourceguard-1773-v1`

External mechanism:

- Tanos et al., 2013, PMID 23348840, DOI `10.1101/gad.207043.112`: CEP83/CCDC41
  is a distal-appendage component that recruits SCLT1 and CEP89, with SCLT1
  mediating later recruitment of FBF1 and CEP164; CEP83 loss blocks
  centriole-to-membrane docking and prevents TTBK2 recruitment and CP110 removal.
- Joo et al., 2013, PMID 23530209, DOI `10.1073/pnas.1220927110`: CCDC41/CEP83 is
  required for ciliary-vesicle docking to the mother centriole and collaborates
  with IFT20 at the onset of ciliogenesis.
- Failler et al., 2014, PMID 24882706, DOI `10.1016/j.ajhg.2014.05.002`: human
  biallelic `CEP83` mutations cause an infantile nephronophthisis ciliopathy with
  ciliary defects in patient fibroblasts and renal tubular cells.
- Yang et al., 2018, PMID 29789620, DOI `10.1038/s41467-018-04469-1`: CEP83 sits
  at the root of the distal-appendage blade, with SCLT1 and CEP164 extending the
  distal-appendage backbone.
- Lo et al., 2019, PMID 31455668, DOI `10.1083/jcb.201811142`: CEP164-dependent
  recruitment of TTBK2 leads to CEP83 phosphorylation, which supports early
  ciliary-vesicle docking and CP110 removal.
- Kumar et al., 2021, PMID 34241634, DOI `10.1083/jcb.202011133`: the CEP90/MNR
  distal-centriole module recruits CEP83 to root distal-appendage formation.
- Kanie et al., 2025, PMID 39882846, DOI `10.7554/eLife.85999`: CRISPR knockout
  of distal-appendage genes separates a core CEP83-SCLT1 and CEP164-TTBK2 module
  that is critical for distal-appendage assembly and four early steps of
  ciliation.

# Same-experiment computation

I filtered the parquet to `group_name == "151 TH Prkcd Grin2c Glut"` and counted
`pvals_adj < 0.05` for ciliary and Hedgehog perturbations represented in training.
Each selected profile had 17,259 measured genes and shared the same 23,679
matched control nuclei in the focal group.

I also computed pairwise signed log-fold-change comparisons over a 29-gene
ciliary/Hedgehog cohort with Distributed Agents Runtime `profile_compare`. I inspected:

- per-perturbation activity, to verify how many genes were FDR significant in
  the focal cell group;
- pairwise significant intersections, to test whether nominally similar flat
  profiles shared any FDR-supported genes;
- top whole-profile and tail neighbors among all 1,674 training perturbations,
  to make sure the comparison was not dominated by unrelated zero-DEG signatures.

The endpoint distribution in the training count table was heavily zero inflated:
1,205 of 1,674 training perturbations had `n_degs = 0`, the median was 0, the
75th percentile was 1, and the 90th percentile was 2. Large focal-cell responses
were still detectable in this assay, for example `Uba5 = 2677`, `Tpr = 1768`,
`Sin3a = 1433`, and `Psmb4 = 742`, so zero calls for ciliary genes are not just a
failure of the focal group or Wilcoxon pipeline.

# Cep83 evidence and analogs

`Cep83` itself is absent from both inputs as required. The closest direct
training analog is `Sclt1`, because SCLT1 is recruited downstream of CEP83 at the
distal appendage and forms the proximal CEP83-SCLT1 assembly module. `Sclt1` had
`0` DEGs in `151 TH Prkcd Grin2c Glut` despite 122 perturbed nuclei. Its own
transcript was nominally reduced but not FDR significant
(`Sclt1` log2FC -0.397, raw `p = 0.017`, adjusted `p = 1`), so the most direct
available distal-appendage perturbation did not even contribute a self-hit to the
endpoint. In the Distributed Agents corpus, the `Sclt1:F002` finding says that the Sclt1
DE surface did not recover a Hedgehog, cilium-gene, UPR, or ISR transcriptional
program and that represented ciliary comparators were flat or single-gene-only in
the same neuronal groups.

`Kiz`, another distal-appendage-associated training perturbation, was also flat
in the focal endpoint: `0` DEGs with 169 perturbed nuclei. It is less proximal to
CEP83 than SCLT1, but Kanie et al. place KIZ in the distal-appendage assembly
neighborhood, and the same-screen `Kiz:F002` Distributed Agents finding explicitly used
`Sclt1`, `Cep290`, IFT, BBS, and Hedgehog genes as ciliary comparators and found
no shared neuronal signature.

The represented downstream structural-cilium genes all pointed in the same
direction:

| training perturbation | focal `n_degs` | focal perturbed nuclei | relevance to `Cep83` |
| --- | ---: | ---: | --- |
| `Sclt1` | 0 | 122 | direct distal-appendage module recruited by CEP83 |
| `Kiz` | 0 | 169 | distal-appendage/ciliary assembly neighbor |
| `Cep290` | 0 | 99 | transition-zone ciliopathy gene downstream of appendage docking |
| `Ift88` | 0 | 143 | IFT-B cilium assembly/maintenance component |
| `Ift81` | 0 | 152 | IFT-B component |
| `Ift43` | 0 | 328 | IFT-A component |
| `Dync2h1` | 0 | 98 | dynein-2 retrograde IFT motor subunit |
| `Dync2i1` | 0 | 229 | dynein-2 intermediate chain |
| `Bbs5` | 0 | 121 | BBSome ciliary-cargo trafficking component |
| `Rpgrip1l` | 0 | 137 | transition-zone ciliopathy gene |
| `Kif3b` | 0 | 156 | kinesin-2 anterograde IFT motor subunit |
| `Ttc21b` | 0 | 131 | IFT-A/retrograde trafficking component |
| `Smo` | 0 | 284 | cilium-localized Hedgehog transducer |
| `Ptch1` | 0 | 159 | Hedgehog receptor |
| `Gli1` | 0 | 234 | Hedgehog transcriptional effector |
| `Gli2` | 0 | 205 | Hedgehog transcriptional effector |

Two related ciliary perturbations had a singleton in this focal group, but both
singletons were self-transcript hits: `Arl3` had `1` DEG, `Arl3` itself
(`log2FC -0.418`, adjusted `p = 0.018`), and `Ttc8` had `1` DEG, `Ttc8` itself
(`log2FC -0.663`, adjusted `p = 3.07e-05`). Those are useful boundary cases:
they show that this focal group can sometimes count a target knockdown without
inducing a secondary ciliary transcriptional state, but they do not argue for a
multi-gene `Cep83` response.

The expression-pattern comparison supported using the FDR counts rather than
inferring a hidden shared module from weak tails. Among `Sclt1`, `Cep290`,
`Ift88`, `Dync2h1`, `Dync2i1`, `Bbs5`, `Alms1`, `Arl3`, `Ttc8`, and `Ift43`,
no inspected pair shared a significant positive or negative feature in the focal
group. The whole-logFC vectors of these flat perturbations could be correlated,
but their largest tail genes had `pvals_adj = 1` and were sparse-expression
artifacts. The all-training nearest neighbors of `Sclt1` by whole-profile
correlation were unrelated perturbations such as `Cdc42`, `Lrp6`, `Thrb`,
`Il1rapl2`, and `Arhgef9`, reinforcing that a near-null ciliary profile should
be calibrated from FDR-supported biology, not from all-gene tail ranks.

# Prediction for Cep83

The external biology says `Cep83` is an essential, very early cilium-initiation
factor: losing it should impair membrane docking and primary-cilium assembly.
However, the held-out endpoint is not cilium assembly; it is basal nuclear RNA
after partial, mosaic, acute P16 loss in postmitotic NeuN+ neurons. The best
same-experiment proxy for an early distal-appendage defect, `Sclt1`, was exactly
zero in the focal cell group, and the broader represented ciliary transport,
BBSome, transition-zone, and Hedgehog perturbations were also zero except for
self-transcript singletons in `Arl3` and `Ttc8`. The Distributed Agents corpus summarizes
that pattern as a high-confidence absence of a coherent shared ciliary
transcriptional module in postnatal NeuN+ snRNA-seq.

I therefore predict that `Cep83` will be fully FDR-silent in this focal group:
`predicted_n_degs = 0`.

# Limits

The prediction is an extrapolation because `Cep83`, `Cep164`, `Cep89`, `Fbf1`,
`Ttbk2`, and `C2cd3` were not direct training perturbations; `Sclt1` and `Kiz`
are close but imperfect substitutes. The screen measured nuclear RNA only, so a
zero count is compatible with strong ciliary structural defects, mislocalized
ciliary GPCRs, defective Hedgehog responsiveness under ligand stimulation, or
cell-type- and developmental-stage-specific phenotypes outside sampled NeuN+
postnatal neurons. The endpoint can also count the target transcript itself, as
seen for `Arl3` and `Ttc8`, and there is no direct measurement here of `Cep83`
self-knockdown strength in the held-out perturbation. I assigned zero rather
than one because the direct distal-appendage analog `Sclt1` and most structural
cilium genes failed to pass focal FDR even for their own RNAs.
