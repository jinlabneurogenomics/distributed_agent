# Fzd3 held-out DEG-count prediction

## Question and resolved ambiguities

The requested manifest contains one held-out perturbation, `Fzd3`. I interpreted the
task as a point prediction for the number of genes with `pvals_adj < 0.05` after
acute AAV CRISPR loss of `Fzd3` in the `151 TH Prkcd Grin2c Glut` cell group.

The endpoint is the assay-specific Wilcoxon/BH count, not a score for organismal
importance. I therefore treated developmental wiring phenotypes of `Fzd3` as
evidence about pathway membership, but not as direct evidence that a 3-4 week,
P16-onset, sparse postmitotic knockout must yield a broad nuclear RNA response.
I also counted self-target down-regulation as eligible when it appeared in the
training DE table, because `n_degs` is defined over all measured genes.

## Sources used

- Input endpoint table:
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
- Input DE parquet:
  `[local file: training_de_all_cell_groups.parquet]`.
- Requested-target manifest:
  `[local file: 084_Fzd3.csv]`.
- Distributed Agents corpus MCP, release `perturbai-july-260713-sourceguard-1773-v1`.
  `Fzd3` itself had no frozen target context, but corpus claims and findings for
  `Fzd2`, `Fzd6`, `Celsr2`, `Lrp6`, `Fzd4`, and `Fzd9` were used as same-assay
  summaries of represented Wnt/Frizzled/PCP perturbations.
- PubMed literature on FZD3 biology, particularly:
  Wang et al. 2002, DOI `10.1523/JNEUROSCI.22-19-08563.2002`, PMID `12351730`;
  Wang et al. 2006, DOI `10.1523/JNEUROSCI.3221-05.2006`, PMID `16407530`;
  Tissir and Goffinet 2006, DOI `10.1111/j.1460-9568.2006.04596.x`,
  PMID `16487141`; Fenstermaker et al. 2010,
  DOI `10.1523/JNEUROSCI.4508-10.2010`, PMID `21106844`; Shafer et al. 2011,
  DOI `10.1016/j.devcel.2011.01.002`, PMID `21316586`; Hua et al. 2014,
  DOI `10.1073/pnas.1406399111`, PMID `24799694`; Hua, Chang, Wang et al. 2014,
  DOI `10.1242/dev.110189`, PMID `25294940`.

## Computational checks over the training data

1. Loaded the manifest and verified that the held-out target list is exactly:

   ```text
   Fzd3
   ```

2. Read the 1,674-row training count table for `151 TH Prkcd Grin2c Glut`.
   The focal endpoint is very sparse: 1,205 of 1,674 training perturbations have
   `n_degs = 0`; only 45 have 11-50 DEGs and only 42 have more than 50 DEGs.

3. Queried the focal-cell DE rows in the parquet for a Wnt/PCP receptor-side
   cohort: Frizzled receptors, Celsr/Ror/Ryk/Prickle receptor or PCP relatives,
   the weak canonical co-receptor `Lrp6`, and the strong downstream beta-catenin
   control `Ctnnb1`. The focal-cell observed counts were:

   | perturbation | `n_degs` in 151 | why it was considered |
   |---|---:|---|
   | `Fzd2` | 0 | Frizzled paralog in training |
   | `Fzd4` | 0 | Frizzled paralog in training |
   | `Fzd6` | 0 | Frizzled paralog and FZD3 redundancy partner in PCP contexts |
   | `Fzd9` | 0 | Frizzled paralog in training |
   | `Celsr2` | 1 | Celsr/PCP cadherin branch adjacent to FZD3-CELSR signaling |
   | `Prickle1` | 0 | core PCP effector side of the FZD/CELSR/VANGL pathway |
   | `Ror1` | 0 | Wnt5a/noncanonical Wnt receptor comparator |
   | `Ror2` | 0 | Wnt5a/noncanonical Wnt receptor comparator |
   | `Ryk` | 0 | Wnt receptor comparator |
   | `Lrp6` | 4 | canonical Wnt co-receptor, weakly active in the same cell group |
   | `Ctnnb1` | 383 | downstream beta-catenin positive control |

   The direct self-RNA rows also argued against a hidden Frizzled knockdown
   module in the represented paralogs: in `151`, the `Fzd2`, `Fzd4`, `Fzd6`, and
   `Fzd9` self rows all had `pvals_adj = 1.0` and were not DE. `Celsr2`'s only
   focal DEG was `Celsr2` itself (`log2FC = -0.883`, `q = 1.49e-19`), so its
   one-gene count did not mark a downstream PCP transcriptome.

4. Ran the Distributed Agents runtime profile comparison on
   `Fzd2/Fzd4/Fzd6/Fzd9/Celsr2/Prickle1/Ror1/Ror2/Ryk/Lrp6/Ctnnb1` within
   `151 TH Prkcd Grin2c Glut`, using `logfoldchanges` as the signed vector and
   `pvals_adj < 0.05` as the significance call. The four observed Frizzled
   paralogs all had zero significant features; `Prickle1`, `Ror1`, `Ror2`, and
   `Ryk` also had zero; `Celsr2` had one; `Lrp6` had four; and `Ctnnb1` had 383.
   Whole-profile correlations among the flat receptor-side perturbations were
   modest and dominated by nonsignificant signed tails, with no shared
   FDR-significant module. In contrast, `Ctnnb1` provides a boundary condition:
   the same assay and same cell group can recover a Wnt/beta-catenin state, so
   the receptor-layer zeros are not merely because Wnt genes are invisible in
   the focal population.

## Biological interpretation for `Fzd3`

`Fzd3` encodes a Frizzled Wnt receptor with a well-established role in planar
cell polarity-like axon guidance. Germline `Fzd3` loss disrupts major embryonic
forebrain tracts including the thalamocortical and corticothalamic tracts,
anterior commissure, nigrostriatal tract, and variably the corpus callosum
(Wang et al. 2002; Wang et al. 2006). Conditional work showed that `Fzd3` is
required in multiple territories and as early as E11.5 for several tract-routing
events (Hua et al. 2014). `Fzd3`, `Celsr3`, and `Vangl2` participate in Wnt/PCP
growth-cone signaling in monoaminergic and commissural axon guidance
(Fenstermaker et al. 2010; Shafer et al. 2011), and `Fzd3` can partially share
FZD6's tissue-polarity logic in other developmental PCP settings (Hua, Chang,
Wang et al. 2014).

Those mechanisms are a reason not to compare `Fzd3` to arbitrary Wnt genes, but
they point mainly to embryonic axon orientation, growth-cone polarity, receptor
localization, and cytoskeletal outputs. The present experiment perturbs sparse
postmitotic neurons at P16 and reads nuclear RNA at P37-P44. That design should
miss many FZD3 phenotypes that are non-cell-autonomous, embryonic, axonal, or
post-translational. The best represented in-dataset analogs therefore are not
the broad downstream `Ctnnb1` transcriptional state but the other acute
single-receptor Wnt/PCP perturbations.

All of those receptor-side analogs were flat or nearly flat in the focal group.
`Fzd2`, `Fzd4`, `Fzd6`, and `Fzd9` each had `n_degs = 0`; `Prickle1`, `Ror1`,
`Ror2`, and `Ryk` also had `n_degs = 0`; `Celsr2` had a single self-only hit; and
`Lrp6` had only four DEGs while marking a selective beta-catenin branch rather
than a PCP/FZD3 branch. The Distributed Agents corpus made the same same-assay point in
its Wnt/Frizzled claim: represented single perturbations of Wnt receptor-layer
and PCP-associated genes are "largely transcriptionally buffered, sparse, or
nonconvergent" in postnatal neuronal nuclear-RNA readouts, while the `Lrp6` and
`Ctnnb1` findings show that canonical Wnt output is detectable but branch
specific.

Based on that evidence, I predict that `Fzd3` loss will behave like the other
single Frizzled/PCP receptor perturbations and not generate an FDR 0.05
downstream signature in `151 TH Prkcd Grin2c Glut`.

## Final target-specific call

| held-out target | prediction | rationale |
|---|---:|---|
| `Fzd3` | 0 | Developmentally essential FZD3/PCP receptor, but its closest measured single-receptor analogs in the postnatal snRNA perturbation data were `Fzd2`, `Fzd4`, `Fzd6`, `Fzd9`, `Prickle1`, `Ror1`, `Ror2`, and `Ryk`, all with zero focal DEGs. The only nearby nonzero receptor-side counts, `Celsr2 = 1` and `Lrp6 = 4`, were respectively self-only or a weak canonical co-receptor state rather than a convergent FZD3-like PCP module. |

## Limits

The main uncertainty is that the direct PCP partners most specific to FZD3
biology were missing from training: `Celsr3`, `Vangl1/2`, `Dvl1/2/3`,
`Prickle2`, several Wnt ligands, `Wls`, and `Porcn` were not observed
perturbations in the supplied count table. `Fzd3` may also be expressed more
strongly than the represented Frizzled paralogs in the focal thalamic cells,
which could have yielded a one-gene self call even without downstream biology.
Conversely, the literature phenotypes are dominated by germline or embryonic
conditional deletions and can overstate the expected transcriptional footprint
of a sparse P16 perturbation. The zero prediction is therefore mostly
within-dataset interpolation from receptor-layer nulls, with external FZD3
biology used to choose the appropriate analogs and to downweight the downstream
`Ctnnb1` counterexample.
