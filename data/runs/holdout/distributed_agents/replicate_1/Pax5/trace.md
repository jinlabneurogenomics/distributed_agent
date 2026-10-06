# DEG-count prediction trace

## Question and endpoint

The task asks for a point prediction of `n_degs` after each requested held-out CRISPR loss-of-function perturbation in `151 TH Prkcd Grin2c Glut` cells. I interpreted `n_degs` exactly as the focal training CSV defines it: the number of measured genes with Benjamini-Hochberg adjusted Wilcoxon `pvals_adj < 0.05` in the thalamic `151 TH Prkcd Grin2c Glut` class.

There was one requested target, `Pax5`. It is absent from the training count table and from the differential-expression Parquet as a `gene_target`, so the prediction is a transfer from non-held-out genes. The endpoint is directly observed for those training perturbations, but absent for `Pax5` itself.

## Sources used

- Declared training endpoint: `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
- Declared differential-expression table: `training differential-expression dataset`.
- Requested-target manifest: `single-target request for Pax5`.
- Run-local dataset metadata: `codex_runtime/pipeline/task_bindings.json`, `coverage.json`, `capabilities.json`, `measurement_registry.json`, and the PerturbAI atlas v5 dataset portrait.
- Same-experiment semantic corpus: `perturbai-july-260713-sourceguard-1773-v1`, queried through `corpus.findings` for `Pax2`, `Pax3`, `Pax4`, `Pax6`, `Pax8`, `Ebf1`, `Ebf2`, `Ebf3`, `Bcl11a`, `Bcl11b`, `Pou2f1`, and `Pou2f2`.
- External literature from PubMed for the B-lineage and midbrain/hindbrain developmental roles of Pax5 and its paired-box relatives.

I did not use the unavailable rank-calibration or predictive graph-review operations, because the manifest marks them as disallowed for scalar/count prediction tasks without ranked supervision.

## Quantitative calibration

The focal training set contained 1,674 non-held-out perturbations. Its DEG-count distribution was strongly zero-inflated:

| statistic | value |
|---|---:|
| targets with `n_degs = 0` | 1,205 / 1,674 |
| median `n_degs` | 0 |
| 75th percentile | 1 |
| 90th percentile | 2 |
| 95th percentile | 18 |
| 99th percentile | 436.48 |
| max | 2,677 |

I then checked training perturbations selected by `Pax5` biology rather than by file order.

### Paired-box / embryonic midbrain analogs

`Pax5` is a member of the Pax2/5/8 subfamily. Pax-2, Pax-5 and Pax-8 proteins can bind regulatory elements in the `En-2` enhancer during early mouse midbrain-hindbrain development, and `Pax-5` is induced in the isthmic organizer and can drive `En-2`, `Wnt-1`, `Fgf8`, and related embryonic organizer genes when ectopically expressed in embryonic chick neural tube (Song et al. 1996, PMID: 8625814, DOI: 10.1242/dev.122.2.627; Funahashi et al. 1999, PMID: 10445503, DOI: 10.1046/j.1440-169x.1999.00401.x). That made `Pax2`, `Pax8`, and the other represented Pax factors the most direct within-dataset developmental analogs, while `En1`, `En2`, and `Otx2` were stage/pathway counterexamples for the same embryonic organizer circuit.

Observed focal-cell training counts:

| training target | focal `n_degs` | why compared |
|---|---:|---|
| `Pax2` | 0 | Pax2/5/8 subfamily and embryonic midbrain-hindbrain organizer regulator |
| `Pax8` | 0 | Pax2/5/8 subfamily |
| `Pax6` | 0 | paired-box neurodevelopmental transcription factor |
| `Pax3` | 0 | paired-box neural-crest/neural-tube developmental regulator |
| `Pax4` | 0 | paired-box developmental regulator, pancreatic rather than neuronal |
| `Pax7` | 0 | paired-box neural/myogenic developmental regulator |
| `En1` | 0 | downstream midbrain-hindbrain/homeobox comparator for Pax2/5/8 biology |
| `En2` | 0 | downstream midbrain-hindbrain/homeobox comparator for Pax2/5/8 biology |
| `Otx2` | 0 | embryonic anterior neural patterning comparator |

All of those targets had `pvals_adj >= 0.05` for every one of the 17,259 focal DE rows. The selected same-experiment corpus reports reached the same interpretation over all sampled neuronal groups: acute postnatal `Pax2` perturbation was nearly globally flat and did not move canonical midbrain-hindbrain transcripts; `Pax6` was FDR-flat in 22 recovered NeuN+ classes; `Pax3`, `Pax4`, and other Pax paralogs were null or singleton-only across the assay. The `Pax2` report explicitly notes that Pax5 was not a perturbation target but that measured Pax2/Pax8/Pax6/En1/En2/Otx2/Gata3/Lbx1 comparators did not produce an interchangeable postnatal module.

This makes a `Pax5` focal response unlikely. The relevant intervention chain is:

`Pax5` CRISPR at P16 -> reduced Pax5 protein in neurons where Pax5 is active -> loss of paired-box transcriptional control -> possible movement of embryonic isthmic `En`/`Wnt`/`Fgf8` targets -> FDR-significant snRNA-seq DE in recovered P37-P44 `151 TH Prkcd Grin2c Glut` nuclei.

The supported break is at the second step. `Pax5`'s strong CNS role is embryonic midbrain-hindbrain organizer biology, whereas the assayed cells are postmitotic thalamic glutamatergic neurons perturbed after birth. The same experiment already perturbed nearby Pax-family developmental factors in the same postnatal setting and found no focal DE response.

### B-cell lineage analogs

`Pax5` is also B-cell-specific activator protein and a core B-lineage commitment factor: mouse `Pax-5` is expressed through B-cell development up to mature B cells, `Pax-5` loss arrests adult bone-marrow B lymphopoiesis at an early pro-B stage, reduces `CD19` and `Ig alpha`/`mb-1`, and blocks normal immunoglobulin heavy-chain recombination (Nutt et al. 1997, PMID: 9442394, DOI: 10.1016/S0171-2985(97)80043-5; Morrison et al. 1998, PMID: 9618759, DOI: 10.1006/smim.1998.0115). Single-cell and acute-degradation studies further place E2A/`Tcf3`, `Ebf1`, `Pax5`, Ikaros-family factors, and `Pou2f2`/Oct2 in early B-cell regulatory logic rather than in basal mature neurons (Zandi et al. 2012, PMID: 23019372, DOI: 10.1073/pnas.1210144109; Fedl et al. 2024, PMID: 39179932, DOI: 10.1038/s41590-024-01933-7).

Observed focal-cell training counts for represented B-lineage regulators and marker-like counterexamples were also near zero:

| training target | focal `n_degs` | why compared |
|---|---:|---|
| `Ebf1` | 0 | early B-cell factor acting near Pax5 in B lymphopoiesis |
| `Ebf2` | 0 | EBF paralog; no focal effect and only one FDR hit in all other groups queried |
| `Ebf3` | 0 | EBF paralog |
| `Tcf3` | 0 | E2A/TCF3, an upstream B-lineage transcription factor |
| `Pou2f1` | 0 | Oct/Pou transcription factor; Pou2 family comparator |
| `Pou2f2` | 0 | Oct2, a B-cell transcriptional regulator |
| `Spi1` | 0 | PU.1 lineage factor upstream of B-cell fate in hematopoiesis |
| `Cd79a` | 0 | B-cell receptor component downstream of Pax5 biology |
| `Cd79b` | 0 | B-cell receptor component downstream of Pax5 biology |
| `Irf8` | 0 | B-lymphoid regulator in the Pax5/Ebf1 network |
| `Ikzf3` | 0 | Ikaros-family B-lineage regulator |

In focal-cell Parquet rows for `Ebf1`, `Ebf2`, `Ebf3`, `Tcf3`, `Pou2f2`, and `Spi1`, the canonical B-cell sentinels I checked were all non-significant: `Cd19`, `Cd79a`, `Cd79b`, `Igll1`, `Rag1`, `Rag2`, and `Irf4` each had adjusted p-value 1.0 in these analog perturbations. Several have extreme log-fold values with FDR 1.0, consistent with the dataset portrait's warning that low-expression normalized log-fold changes are not robust signal.

This B-cell circuit therefore provides no positive mature-neuronal analog for `Pax5`. The experimental design also FACS-enriched NeuN+ nuclei and largely excluded immune and non-neuronal cells, so the major external `Pax5` program is outside the sampled tissue/cell lineage.

## Prediction for `Pax5`

The prediction is:

| target | predicted `n_degs` | rationale |
|---|---:|---|
| `Pax5` | 0 | `Pax5`'s strongest biology is B-cell commitment and embryonic isthmic organizer patterning. Both are displaced from P16-P37/P44 NeuN+ thalamic glutamatergic neurons. The direct in-dataset Pax2/Pax8/Pax6/Pax3/Pax4/Pax7 analogs all have `n_degs = 0` in the focal group; the B-lineage TF analogs `Ebf1`, `Ebf2`, `Ebf3`, `Tcf3`, `Pou2f1`, `Pou2f2`, `Spi1`, and `Ikzf3` are also zero; and same-experiment reports describe these family signatures as globally flat or near-null rather than as strong hidden modules. |

## Limits

This is still an extrapolation. `Pax5` itself was held out, its guide cutting, protein depletion, and expression signature are unobserved, and no training perturbation is an obligate same-complex phenocopy of Pax5. The closest training genes test paired-box developmental regulators and B-lineage transcription factors, not Pax5 protein directly. If `Pax5` had a rare thalamic function in a subtype diluted inside `151 TH Prkcd Grin2c Glut`, the coarse group-level Wilcoxon endpoint could miss it. Conversely, if CRISPR loss selected against a rare Pax5-dependent neuronal state before nuclei recovery, the survivor-conditioned DE surface could look flat. Within the declared data, however, the biologically matched evidence all falls on the zero side rather than on a low positive DEG count.
