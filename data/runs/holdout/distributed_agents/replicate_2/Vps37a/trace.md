# Question and interpretation

The run asks for the held-out value of `n_degs` for the requested perturbation in
`151 TH Prkcd Grin2c Glut` neurons. I interpreted `n_degs` exactly as the number
of measured genes with `pvals_adj < 0.05` in the focal cell group in the
Perturb-seq differential-expression table. The target `Vps37a` was held out, so
neither its focal-cell DEG count nor any of its expression vectors were used.

The main ambiguity is whether a visible endolysosomal phenotype after one loss
of function should be transferred to every other endosomal gene. I resolved that
using the in-dataset signatures themselves: positive endolysosomal examples were
treated as evidence that the assay can detect such stress, while the many
nearby zero examples were treated as strong evidence against a generic
"trafficking gene equals nonzero" rule.

# Sources used

- Input endpoint table:
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
- Input DE table:
  `[local file: training_de_all_cell_groups.parquet]`.
- Requested-target manifest:
  `[local file: 262_Vps37a.csv]`.
- Distributed Agents same-experiment semantic corpus
  `perturbai-july-260713-sourceguard-1773-v1`, queried for same-assay claims
  about endolysosomal, retromer, lysosomal, and autophagy perturbations.
- Distributed Agents profile runtime, run locally on the supplied focal-cell DE rows, to
  compare the signed `logfoldchanges` vectors of observed endolysosomal and
  autophagy genes.
- External literature from PubMed:
  - Bache et al. 2004, Molecular Biology of the Cell,
    DOI: `10.1091/mbc.e04-03-0250`, PMID: `15240819`.
  - Stuchell et al. 2004, Journal of Biological Chemistry,
    DOI: `10.1074/jbc.M405226200`, PMID: `15218037`.
  - Eastman et al. 2004, Journal of Biological Chemistry,
    DOI: `10.1074/jbc.M410384200`, PMID: `15509564`.

# Dataset calibration

The manifest contains a single requested target, `Vps37a`. The focal training
endpoint has 1674 non-held-out perturbations; 469 are nonzero and the median is
0, so a zero prediction is common in this assay rather than an exceptional
claim. The distribution is very skewed: the 75th percentile is 1 DEG, the 95th
percentile is 18 DEGs, and rare very broad responses reach hundreds to thousands
of DEGs.

I searched the training counts for ESCRT, endosomal, retromer/GARP,
autophagy, and lysosomal disease genes, then verified the exact focal-cell
significant counts from the Parquet with `pvals_adj < 0.05`. The closest
observed analogs and bounds were:

| training perturbation | `151 TH Prkcd Grin2c Glut` DEGs | relevance to `Vps37a` |
|---|---:|---|
| `Chmp4b` | 0 | Same broad ESCRT pathway, but ESCRT-III rather than ESCRT-I; also one member of a paralogous CHMP4 family. |
| `Atg5` | 0 | Core macroautophagy machinery; tests whether autophagy-lysosome disruption alone gives a focal RNA state. |
| `Atg16l1` | 0 | LC3-lipidation/autophagy machinery; a second null autophagy comparator. |
| `Lamp2` | 0 | Lysosomal membrane protein; another nearby lysosome/autophagy counterexample. |
| `Tmem106b` | 1 | Lysosomal trafficking disease gene, with only its self-transcript significant. |
| `Snx10` | 0 | Sorting nexin/endosomal trafficking counterexample. |
| `Vps35l` | 0 | Retriever/Commander-retromer-related trafficking branch. |
| `Vps53` | 0 | GARP/EARP subunit; paired with the positive `Vps54` result to show subunit-specificity. |
| `Vps54` | 31 | Modest Golgi/endosome retrograde trafficking response. |
| `Vps35` | 17 | Modest retromer response and a positive endosomal-recycling bound. |
| `Vps41` | 0 | HOPS/late endosome-lysosome fusion branch; near the `Rab7` biology but null here. |
| `Rab7` | 501 | Strong upper-bound late-endosomal/lysosomal response. |
| `Abca7` | 0 | Endolysosomal/lipid trafficking comparator from the Distributed Agents Rab7 claim. |
| `Ocrl` | 0 | Phosphoinositide/endolysosomal comparator from the Distributed Agents Rab7 claim. |

The focal-cell DE rows show that the nonzero anchors were branch-specific rather
than one shared endosomal module. `Rab7` had 501 significant genes, including
early lysosomal/V-ATPase and sterol-associated changes such as `Atp6v1b2`,
`Dpp7`, `Insig1`, `Atp6v0b`, and `Ptgds`. `Vps35` had 17 significant genes and
`Vps54` had 31, but the `Vps35` and `Vps54` significant sets overlapped on only
one gene, `Atp2a2`, in the focal cell group. `Rab7` overlapped `Vps35` on nine
significant genes and `Vps54` on thirteen, still far from a direct phenocopy.

I also ran profile comparisons over complete 17,259-gene signed
`logfoldchanges` vectors in the focal group using `gene_target` as the entity
and `names` as the feature. The local Distributed Agents artifacts were:

- `profile_neighbors_endolysosomal.json`: independent neighborhoods of `Rab7`,
  `Vps35`, `Vps54`, `Atg5`, `Tmem106b`, and `Chmp4b` against all 1674 focal
  training targets.
- `profile_compare_endolysosomal.json` and
  `profile_inspect_endolysosomal.json`: exact pairwise comparisons among
  `Rab7`, `Vps35`, `Vps54`, `Vps35l`, `Vps41`, `Vps53`, `Atg5`, `Atg16l1`,
  `Chmp4b`, `Tmem106b`, `Lamp2`, `Snx10`, `Abca7`, and `Ocrl`.

Those comparisons confirmed the count-based picture. Whole-profile correlations
among the null and positive endolysosomal candidates are inflated by weak
background structure, but the significant programs do not line up into a common
ESCRT/lysosome signature. The Distributed Agents corpus made the same point in words:
its curated claims state that `Vps35` is a modest, branch-specific thalamic
response not phenocopied by represented Retriever/Commander or WASH-associated
perturbations; that `Rab7` induces a selective late-endosomal/lysosomal
compensation program weakly shared by `Vps41` but absent after `Ocrl`, `Abca7`,
or `Gdi1`; and that represented autophagy and lysosome perturbations are not
transcriptomically interchangeable in this postnatal neuronal screen.

# Target-specific reasoning

## Vps37a

External function: `Vps37a`, also called `Hcrp1` in older mammalian literature,
encodes a VPS37-family subunit of ESCRT-I. Bache et al. showed that hVPS37A
interacts with TSG101, VPS28, and HRS, cofractionates with the ESCRT-I complex,
localizes to LAMP1-positive endosomes, and is required for efficient EGF
receptor degradation. Stuchell et al. and Eastman et al. established the broader
mammalian VPS37A-D family as alternative ESCRT-I components that link TSG101 and
VPS28 to the class-E VPS pathway and to ESCRT-dependent membrane budding.

Within-dataset analogs:

- No direct ESCRT-I subunit was available in the focal training set: `Tsg101`,
  `Vps28`, `Vps37b`, `Vps37c`, `Vps37d`, `Mvb12a`, `Mvb12b`, and `Ubap1` were
  absent from the training-count CSV.
- The same ESCRT pathway was represented by `Chmp4b`, but `Chmp4b` loss had 0
  focal DEGs. This is not a perfect analog because CHMP4B acts downstream in
  ESCRT-III and, like VPS37A, has paralogs, but it argues that this assay does
  not inevitably turn ESCRT disruption into a BH-significant nuclear RNA state.
- Related autophagy/lysosome genes were also flat: `Atg5` 0, `Atg16l1` 0,
  `Lamp2` 0, `Snx10` 0, `Abca7` 0, `Ocrl` 0, `Vps41` 0, `Vps35l` 0, and
  `Vps53` 0. `Tmem106b` had only 1 DEG, its self-transcript.
- `Rab7` 501, `Vps35` 17, and `Vps54` 31 show that focal thalamic neurons can
  produce detectable signatures after selected endolysosomal or retrograde
  trafficking perturbations. I used them as positive controls and upper bounds,
  not as close quantitative predictors: `Rab7` is a central late-endosomal
  GTPase, while `Vps35` retromer and `Vps54` GARP are different trafficking
  branches and were themselves only modest and mutually nonconvergent in their
  significant genes.

Prediction logic: the balance of evidence favors either no FDR-significant
genes or a very small footprint for partial acute `Vps37a` loss in recovered
postmitotic thalamic neurons. The external ESCRT-I biology makes a true
cell-biological effect plausible, but the endpoint here is a sparse
single-nucleus RNA breadth count under mosaic CRISPR, and the observed training
data show that several lysosomal/autophagy/ESCRT-adjacent perturbations with
credible biology sit at zero. Because `Vps37a` is one VPS37 isoform rather than
the invariant TSG101/VPS28 core, and because EGFR/TNFR1-like receptor
down-regulation is not an obvious dominant basal program in these neurons, I
predict that it will fall below the BH 0.05 threshold in this focal cell group.

Final point prediction: `0`.

# Limits

The strongest limitation is the absence of any observed ESCRT-I training
subunit, so the prediction extrapolates from ESCRT-III, autophagy, retromer,
GARP, and late-endosomal genes rather than from an exact complex member.
`Chmp4b` is useful but not definitive, because CHMP4A/CHMP4C could compensate
and ESCRT-III is not the same biochemical step as ESCRT-I. The positive `Rab7`,
`Vps35`, and `Vps54` anchors prove detectability of some trafficking stresses
but also show substantial branch-specificity, making a numerical transfer to
`Vps37a` uncertain. Finally, literature on VPS37A is mostly from dividing
cancer or cultured cells and receptor-degradation assays; it establishes
mechanism but not the size of a nuclear RNA response in sparsely edited
juvenile mouse thalamic neurons.
