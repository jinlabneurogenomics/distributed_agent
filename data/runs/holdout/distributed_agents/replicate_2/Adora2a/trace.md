# Adora2a DEG-count prediction trace

## Question and resolved ambiguities

The requested manifest contains one held-out perturbation:

| target_name |
|---|
| Adora2a |

The quantity to predict is the number of measured genes with `pvals_adj < 0.05` after CRISPR loss of `Adora2a` in `151 TH Prkcd Grin2c Glut`, a thalamic glutamatergic cell group. The held-out target is absent from both the parquet `gene_target` column and the focal training-count CSV, so no `Adora2a` differential-expression row can be used directly.

The training endpoint counts all measured genes that pass the adjusted-p cutoff, including the perturbed transcript itself when that row is significant. I therefore did not strip self-target rows from training analogs. This matters for `Gnao1`, `Prkaca`, and `Prkar1a`: each has one DEG in the focal group, but the one significant row is the target transcript itself rather than a downstream response.

## Sources used

- Input endpoint table: `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
- Input DE parquet: `[local file: training_de_all_cell_groups.parquet]`.
- Held-out manifest: `[local file: 004_Adora2a.csv]`.
- Same-experiment semantic layer: Distributed Agents corpus release `perturbai-july-260713-sourceguard-1773-v1`, especially claims and findings around `Gnal`, `Gnas`, `Pde10a`, `Drd2`, `Drd4`, and `Drd5`. The Distributed Agents corpus is a packaged interpretation of the same Perturb-seq experiment, not independent replication of the parquet.
- External literature retrieved through NCBI PubMed:
  - Kaelin-Lang et al. 2000, DOI `10.1007/s007020070037`, PubMed `11041267`.
  - Fuxe et al. 2003, DOI `10.1212/01.wnl.0000095206.44418.5c`, PubMed `14663004`.
  - Farrell et al. 2012, DOI `10.1038/npp.2012.251`, PubMed `23303063`.
  - Wang and Zhou 2019, DOI `10.1016/j.neuropharm.2019.01.014`, PubMed `30659840`.
  - Ferre and Ciruela 2019, DOI `10.1089/caff.2019.0008`, PubMed `31559390`.

## Computation over the supplied dataset

I first summarized the 1,674 non-held-out focal-cell counts. The distribution is strongly zero-inflated:

| statistic | n_degs |
|---|---:|
| zero-count targets | 1,205 |
| nonzero targets | 469 |
| median | 0 |
| 75th percentile | 1 |
| 90th percentile | 2 |
| 95th percentile | 18 |
| maximum | 2,677 |

The largest responses in this cell group are from core or nuclear genes such as `Uba5`, `Tpr`, `Sin3a`, `Rnpc3`, `Zbtb7a`, `U2af2`, `Psmb4`, `Hnrnpu`, and `Yy1`, rather than from neuromodulatory GPCRs.

To keep the analog comparison matched to the requested endpoint, I row-filtered the parquet to `group_name == "151 TH Prkcd Grin2c Glut"` and to a manually selected set of represented `gene_target` values in the adenosine/dopamine/G-protein/cAMP/PKA/CREB neighborhood:

```python
filter = (
    pc.field("group_name") == "151 TH Prkcd Grin2c Glut"
) & pc.field("gene_target").isin(analogs)
```

This yielded 17,259 measured-gene rows per analog target in the focal group. I then counted rows with `pvals_adj < 0.05` and inspected the highest absolute Wilcoxon-score rows for the closest targets.

I also used a Distributed Agents runtime `profile_compare` on the same `151` rows for `Adcy1`, `Adcy3`, `Adcy5`, `Adk`, `Creb1`, `Crebbp`, `Drd2`, `Drd4`, `Drd5`, `Gnao1`, `Gnal`, `Gnas`, `Pde10a`, `Pde4b`, `Pde4d`, `Prkaca`, and `Prkar1a`. This computed signed Wilcoxon-score correlations over the complete focal-cell gene vectors. The profiles of the receptor/source-arm nodes were flat: within the inspected G-protein/cAMP receptor cohort, whole-profile cosine similarities were close to zero. For example, `Drd2` to `Adcy1/3/5`, `Drd4`, `Drd5`, `Gnao1`, `Pde4b`, `Prkaca`, and `Prkar1a` ranged from `-0.0128` to `0.0465`; `Gnal` to the same peer set ranged from `-0.0133` to `0.0264`; and even the largest focal-cohort similarities for `Gnas`, `Pde10a`, or `Creb1` were only about `0.052` to `0.065`. None shared adjusted-significant genes with these receptor/source-arm analogs in `151`.

## Target-specific biological comparison

### `Adora2a`

`Adora2a` encodes the adenosine A2A receptor, a Golf/Gs-coupled GPCR that stimulates cAMP production. The canonical neuronal setting for A2A receptor biology is not thalamic glutamatergic neurons but striatopallidal medium spiny neurons: Kaelin-Lang et al. found high A2A receptor gene expression only in medium-sized striatal cells across mouse, rat, cat, and human striatum; Farrell et al. used an `Adora2a` BAC to drive a Gs-DREADD selectively in striatopallidal MSNs; Wang and Zhou described A2A receptors as highly and selectively expressed in D2-MSNs and showed that A2A activation can inhibit Kir current and increase D2-MSN excitability; and Fuxe et al. plus Ferre and Ciruela reviewed the antagonistic A2A-D2 receptor complexes in striatopallidal neurons.

The most direct represented training comparators were therefore the D2-MSN dopamine/cAMP source arm and its immediate downstream effectors:

| analog | why it was compared | focal `n_degs` | focal expression-pattern evidence |
|---|---|---:|---|
| `Drd2` | best represented striatopallidal receptor comparator for `Adora2a` | 0 | no FDR<0.05 rows in 213 perturbed nuclei; top nominal rows such as `Zbtb7a`, `Impa1`, and `Fibp` had `pvals_adj = 1` |
| `Drd4`, `Drd5` | dopamine receptor family and Gs/Gi GPCR counterexamples | 0, 0 | no FDR<0.05 rows in 218 and 228 perturbed nuclei |
| `Gnal`, `Gnas` | Golf and Gs alpha subunits coupled to A2A-like GPCR/cAMP signaling | 0, 0 | no FDR<0.05 rows in 148 and 306 perturbed nuclei |
| `Adcy1`, `Adcy3`, `Adcy5` | membrane adenylyl cyclases downstream of stimulatory G proteins; `Adcy5` is the striatal AC subtype in the A2A/D2 pathway | 0, 0, 0 | no focal DEGs; the strongest `Adcy1` and `Adcy3` rows had adjusted p-values 0.139 and 0.112, and `Adcy5` had no row near FDR |
| `Pde10a`, `Pde4b`, `Pde4d`, `Pde1c` | cAMP/cyclic-nucleotide phosphodiesterase comparators | 0, 0, 0, 0 | no focal FDR<0.05 rows; `Pde10a`'s strongest focal row had `pvals_adj = 0.304` |
| `Prkaca`, `Prkar1a` | PKA catalytic and regulatory nodes downstream of cAMP | 1, 1 | the only focal DEGs were `Prkaca` and `Prkar1a` themselves, respectively |
| `Creb1`, `Crebbp` | distal CREB transcriptional machinery, used as positive counterexamples rather than receptor analogs | 10, 8 | `Creb1` induced `Crem` up plus nine additional rows; `Crebbp` produced eight rows. This shows that the focal cell type can register a CREB-axis perturbation when a nuclear transcriptional node is hit directly |
| `Adk` | purine/adenosine metabolism boundary comparator | 0 | no focal FDR<0.05 rows in 186 perturbed nuclei |

The same-experiment corpus reinforced this boundary. `Adora2a` itself had no target context in the selected Distributed Agents release, consistent with being held out. However, `Gnal:F002` reports that in the striatal/LGE GABA group the screen detected a compact `Pde10a` response with `Scg2` and `Crem` up-regulation, while `Gnal`, `Adcy5`, `Gnas`, `Drd2`, `Gnao1`, and `Pde4b` were flat in that same source-arm branch. `Pde10a:F003` explicitly contrasts `Pde10a` against represented PDE and dopamine/cAMP/PKA pathway perturbations, and notes that `Adora2a`, `Drd1`, `Pde1b`, `Pde2a`, and `Ppp1r1b` were absent from the parquet. `Gnas:F003` and the high-confidence corpus claim `claim:5778f7e46773642bd0bd` summarize the broader observation: represented dopamine/GPCR and cAMP-pathway perturbations do not collapse into one shared durable basal neuronal mRNA module in this assay.

Putting these together, the direct external prior predicts that the largest `Adora2a` cell-autonomous effect should land in striatal D2/striatopallidal neurons, if anywhere. The within-dataset prior says that even in cAMP-relevant represented nodes, tonic receptor-to-cyclase loss is usually buffered at a 3-4-week basal snRNA-seq endpoint, and in the exact requested thalamic group the relevant receptors, Golf/Gs proteins, adenylyl cyclases, PDEs, and PKA subunits had zero or self-only DEG counts. `Creb1` and `Crebbp` prevent overclaiming that the `151` group cannot respond at all; instead they show the response starts to become visible at a direct nuclear transcriptional node, not at the Adora2a-like receptor/source arm.

I therefore predict no measured genes passing FDR 0.05 for `Adora2a` in `151 TH Prkcd Grin2c Glut`.

## Limits and extrapolation

- The closest adenosine paralogs, `Adora1`, `Adora2b`, and `Adora3`, and some especially relevant striatal genes, including `Drd1`, `Pde1b`, `Pde2a`, and `Ppp1r1b`, were not available as training perturbations in this focal endpoint. The prediction has to extrapolate from dopamine receptors, G proteins, adenylyl cyclases, PDEs, PKA, and purine metabolism instead of from another A2A-family KO.
- The data are basal single-nucleus RNA 3-4 weeks after sparse mosaic CRISPR. They do not assay adenosine levels, acute cAMP, phospho-PKA, phospho-CREB, Kir current, receptor heteromers, or firing. A zero DEG count is compatible with strong acute electrophysiological biology in a responsive striatal neuron.
- The focal `151` class is thalamic and glutamatergic. Rare `Adora2a`-expressing thalamic or contaminating nuclei would be diluted in this broad class, and the Wilcoxon/BH endpoint is power-dependent.
- Self-transcript loss is not used as an editing-efficiency score. The forecast is zero because the receptor is off-canonical for this cell class and the represented cAMP source-arm perturbations were transcriptionally silent here, not because a weak `Adora2a` transcript would prove failed editing.
