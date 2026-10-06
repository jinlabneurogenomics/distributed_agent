# Ap3b2 held-out DEG-count prediction

## Question and interpretation

The held-out manifest `014_Ap3b2.csv` contains one requested perturbation:
`Ap3b2`. I interpreted the requested endpoint as the exact training-count
definition: for `151 TH Prkcd Grin2c Glut`, predict the integer number
of measured genes with Wilcoxon Benjamini-Hochberg `pvals_adj < 0.05` after
acute sparse AAV-CRISPR loss of the target gene.

I treated the readout as an assay-specific nuclear RNA breadth measurement, not
as a direct statement about whether AP3B2 is important for synaptic-vesicle
protein sorting, electrophysiology, or mouse behavior.

## Sources used

- The held-out target manifest:
  `[local file: 014_Ap3b2.csv]`.
- The focal endpoint file:
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
- The same-experiment DE parquet:
  `[local file: training_de_all_cell_groups.parquet]`.
- Distributed Agents internal corpus release
  `perturbai-july-260713-sourceguard-1773-v1`; I used `target_context`
  and `search_claims` for same-assay claims about represented AP-3/BLOC,
  lysosome-fusion, clathrin/adaptor, and presynaptic-vesicle perturbations.
- Distributed Agents runtime profile-neighbor analysis over the focal DE table, used as
  a falsification check on residual expression-pattern similarity for
  `Ap3b1`, `Dtnbp1`, `Rab7`, and `Cltc`.
- PubMed literature:
  - Faundez and Kelly 2000, PMID:10930456, DOI:10.1091/mbc.11.8.2591.
    AP-3 coats participate in endosomal synaptic-vesicle biogenesis.
  - Seong et al. 2004, PMID:15537701, DOI:10.1091/mbc.e04-10-0892.
    beta3A/AP-3A and beta3B/AP-3B mouse deficiencies have divergent neuronal
    phenotypes; beta3B loss perturbs selected synaptic-vesicle cargoes such as
    ZnT3 and ClC-3.
  - Newell-Litwa et al. 2009, PMID:19144828,
    DOI:10.1091/mbc.e08-05-0456. AP-3 and BLOC-1 act from early endosomes to
    tune synaptic-vesicle protein cargo; Ap3b2 knockout reduced selected
    synaptic-vesicle proteins whereas Ap3b1 and BLOC-1 mutants changed cargo in
    the opposite direction for some proteins.
  - Evstratova et al. 2014, PMID:25410111, DOI:10.1038/ncomms6530.
    AP-3B/AP3B2 loss attenuates AP-3-dependent vesicles and asynchronous
    neurotransmitter release.

## Computation over the supplied data

I first joined the exact focal `n_degs` counts for selected mechanistic
neighbors to focal DE rows from the parquet. To avoid scanning all cell types
repeatedly, I predicate-filtered the parquet to
`group_name == "151 TH Prkcd Grin2c Glut"` and retained `gene_target`, `names`,
`logfoldchanges`, `pvals_adj`, `n_pert_matched`, and `n_ctrl_matched`. This
focal slice contained 28,891,566 rows, representing 1,674 training perturbations
and 17,259 measured genes.

The overall response scale in this cell type was sparse:

| statistic over 1,674 training targets | `n_degs` |
| --- | ---: |
| median | 0 |
| 75th percentile | 1 |
| 90th percentile | 2 |
| 95th percentile | 18 |
| maximum | 2677 |

For the biologically relevant AP-3/BLOC and vesicle/endosome comparators in
the focal cell group:

| training target | focal `n_degs` | focal perturbed nuclei | focal expression evidence |
| --- | ---: | ---: | --- |
| `Ap3b1` | 0 | 85 | all 17,259 tested genes had `pvals_adj = 1`; its own measured transcript had log2FC -0.166, `pvals_adj = 1` |
| `Dtnbp1` | 0 | 220 | all tested genes had `pvals_adj = 1`; its own transcript had log2FC -0.295, `pvals_adj = 1` |
| `Slc32a1` | 0 | 268 | all tested genes had `pvals_adj = 1` |
| `Becn1` | 0 | 177 | all tested genes had `pvals_adj = 1` |
| `Vps41` | 0 | 159 | minimum `pvals_adj = 0.204` |
| `Atp6v1a` | 0 | 76 | minimum `pvals_adj = 0.855` |
| `Rab27a` | 0 | 135 | minimum `pvals_adj = 0.950` |
| `Dnm1` | 1 | 194 | the single FDR hit was `Dnm1` itself |
| `Synj1` | 1 | 90 | the single FDR hit was `Synj1` itself |
| `Sv2a` | 1 | 231 | the single FDR hit was `Sv2a` itself |
| `Syp` | 1 | 197 | the single FDR hit was `Syp` itself |
| `Vamp1` | 1 | 230 | the single FDR hit was `Vamp1` itself |
| `Stxbp1` | 1 | 189 | the single FDR hit was `Stxbp1` itself |
| `Cltc` | 3 | 32 | sparse non-AP-3 clathrin response |
| `Vps35` | 17 | 133 | sparse retromer response |
| `Rab7` | 501 | 215 | broad lysosome/late-endosome response including `Lamp1`, `Lamp2`, `Mcoln1`, `Ctsd`, and V-ATPase genes |

The direct AP-3B subunits `Ap3d1`, `Ap3m2`, and `Ap3s2` and most BLOC-1/HPS
subunits were not present in the training-count target universe. The closest
available target was therefore `Ap3b1`, encoding the beta3A subunit of the
ubiquitous AP-3A complex, and the closest BLOC-side target was
`Dtnbp1`/dysbindin.

I also ran a same-cell profile-neighbor query for `Ap3b1`, `Dtnbp1`, `Rab7`,
and `Cltc`. The AP-3/BLOC anchors had zero FDR-significant genes, so their
nearest whole-profile neighbors were driven by non-significant rank tails and
shared placeholder-like extreme log fold changes rather than shared significant
biology. I used this as a guard against overinterpreting random nominal
`Ap3b1` or `Dtnbp1` ranks; no focal AP-3/BLOC expression-pattern module was
evident.

## Ap3b2-specific reasoning

`Ap3b2` encodes beta3B, the neuronal beta subunit of AP-3B. AP-3B is a real and
fairly direct synaptic-vesicle biogenesis complex: beta3B-containing AP-3 coats
are recruited to neuronal/endocrine endosomes, Ap3b2 knockout changes the
synaptic-vesicle abundance of selected cargoes, and AP-3B loss changes
asynchronous release in neurons. Those papers argue that `Ap3b2` knockout
should have a vesicle-sorting phenotype.

The prediction is about nuclear mRNA breadth after sparse P16 editing, though,
and the same experiment argues that this kind of vesicle-sorting defect is
usually transcriptomically silent:

- The one represented AP-3 subunit, `Ap3b1`, gave 0 focal DEGs and no FDR<0.10
  genes in any of its 18 recovered neuronal groups in the Distributed Agents corpus.
  `Ap3b1` is not identical to `Ap3b2`: beta3A and beta3B can have divergent
  cargo effects. Still, it is the strongest same-adaptor proxy and shows that
  AP-3 cargo-routing changes do not automatically induce a soma RNA stress
  state in this assay.
- `Dtnbp1`, a BLOC-1/AP-3-adjacent endosomal trafficking gene, also gave 0
  focal DEGs; the Distributed Agents corpus specifically synthesized `Ap3b1` and
  `Dtnbp1` as a represented AP-3/BLOC-related buffered outcome. The corpus
  caveat is material: most BLOC-1 genes and `Ap3b2` itself were untested.
- Direct synaptic-vesicle machinery genes were mostly zero or self-only in the
  focal count table: `Dnm1`, `Synj1`, `Sv2a`, `Syp`, `Vamp1`, and `Stxbp1`
  each had only 1 focal DEG, and for these examples the one hit was the
  perturbed transcript itself. This bounds the expectation for AP-3B: strong
  vesicle-cycle physiology is not enough to produce a broad steady-state
  snRNA-seq response.
- `Rab7` was a useful counterexample, not an analog. Its 501 focal DEGs show
  that the cell group can mount a broad endolysosomal/lysosomal RNA state when
  late endosome-lysosome traffic is severely disturbed. `Ap3b1`, `Becn1`,
  `Vps41`, and `Atp6v1a` did not reproduce that state in this focal group, so
  an AP-3 cargo-selection perturbation should not be promoted to a Rab7-scale
  prediction.
- `Cltc` and `Vps35` showed that clathrin/retromer perturbations can produce a
  few to tens of DEGs, but their focal signatures do not make a generic
  adaptor-tier module: the corpus reports represented AP-family perturbations
  as target-specific rather than a shared AP/clathrin transcriptional program.

I therefore predict that `Ap3b2` will be nonzero biologically but zero by this
FDR-gated nuclear RNA endpoint. I also predict that its own transcript will not
be a reliable singleton DEG: it is a lower-abundance adaptor subunit, whereas
the clear one-hit examples above were abundant vesicle genes or their direct
target transcripts.

## Final point prediction

| held-out target | predicted `n_degs` |
| --- | ---: |
| `Ap3b2` | 0 |

## Limits and uncertainty

This is an extrapolation because `Ap3b2`, `Ap3d1`, `Ap3m2`, and `Ap3s2` were
all absent as training perturbations. `Ap3b2` is the neuronal AP-3 beta subunit,
and AP-3B cargo phenotypes are not necessarily interchangeable with the
ubiquitous `Ap3b1`/AP-3A complex; in fact, Seong et al. and Newell-Litwa et al.
show divergent cargo effects for the two AP-3 isoforms. The available same-
experiment evidence is consequently strongest for "AP-3/BLOC cargo perturbation
need not produce broad nuclear RNA DE" and weaker for the exact `Ap3b2` effect.

The focal `Ap3b1` perturbation also had only 85 matched perturbed nuclei, so
its all-zero result is less powered than `Dtnbp1` or `Rab7`. The model is not
making a negative statement about AP-3B-mediated sorting, ZnT3/ClC-3 vesicle
content, asynchronous release, or seizure susceptibility; those phenotypes
could be present without any genes passing `pvals_adj < 0.05` in this
single-nucleus mRNA comparison.
