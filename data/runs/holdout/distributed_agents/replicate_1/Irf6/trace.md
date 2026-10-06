# DEG-count prediction trace

## Question and endpoint

The task asks for a point prediction of the held-out `n_degs` endpoint for each requested perturbation in `151 TH Prkcd Grin2c Glut` cells. I treated `n_degs` as the count of measured genes with BH-adjusted Wilcoxon `pvals_adj < 0.05` in that focal thalamic glutamatergic group, with positive log fold change meaning higher expression in the CRISPR loss-of-function nuclei than in matched non-targeting controls.

The only requested held-out perturbation was:

| target_name |
| --- |
| `Irf6` |

I resolved the main ambiguity as follows: the task is a scalar count prediction, not a ranking. `Irf6` has no training signature or training `n_degs`, so the focal endpoint is absent for `Irf6` itself and must be inferred from visible focal-cell DEG counts, visible expression signatures of mechanistic analogs, and external knowledge about IRF6 function.

## Sources used

- Declared training endpoint: `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
- Declared DE table: `training differential-expression dataset`.
- Run-local requested targets: `single-target request for Irf6`.
- Run-local manifests: `task_bindings.json`, `coverage.json`, `capabilities.json`, `measurement_registry.json`.
- Same-experiment internal corpus: `perturbai-july-260713-sourceguard-1773-v1`, queried through `corpus.findings` for visible IRF, epithelial, and Notch-pathway analogs. This corpus is a packaged interpretation of the same Perturb-seq experiment, not independent replication.
- External literature from PubMed/NCBI E-utilities:
  - Thomason et al. 2010, JCI, DOI `10.1172/JCI40266`, PMID `20424327`: p63 transactivates `IRF6` through an upstream enhancer and genetically cooperates with `Irf6` during murine secondary-palate development.
  - Moretti et al. 2010, JCI, DOI `10.1172/JCI40267`, PMID `20424325`: the DeltaNp63-IRF6 feedback loop controls keratinocyte proliferation/differentiation and links p63- and IRF6-associated ectodermal dysplasia.
  - Alade et al. 2020, Molecular Genetics & Genomic Medicine, DOI `10.1002/mgg3.1355`, PMID `32558391`: pathogenic IRF6 variants are concentrated in its DNA- and protein-binding domains and underlie most Van der Woude syndrome cases.

## Computations over the supplied data

I read the focal training-count CSV to calibrate how sparse the endpoint is and to retrieve exact observed counts for biologically relevant visible perturbations. The focal training set contains 1,674 perturbations; 1,205 of 1,674, or 71.98%, had `n_degs = 0`, and 1,481 of 1,674, or 88.47%, had `n_degs <= 1`. The distribution was highly skewed: median `0`, 75th percentile `1`, 95th percentile `18`, and maximum `2,677`.

I queried the Parquet only for exact focal-cell rows around the analog set:

```sql
SELECT gene_target,
       COUNT(*) AS measured,
       SUM(CASE WHEN pvals_adj < 0.05 THEN 1 ELSE 0 END) AS n_sig,
       MAX(ABS(scores)) AS max_abs_score,
       ANY_VALUE(n_pert_matched) AS n_pert,
       ANY_VALUE(n_ctrl_matched) AS n_ctrl
FROM read_parquet('training_de_all_cell_groups.parquet')
WHERE group_name = '151 TH Prkcd Grin2c Glut'
  AND gene_target IN (...)
GROUP BY gene_target;
```

Each queried visible analog had 17,259 measured focal-cell genes and a large matched control pool of 23,679 nuclei. The exact focal `n_degs` values from the training CSV and Parquet were concordant:

| visible target | focal `n_degs` | relevance to `Irf6` |
| --- | ---: | --- |
| `Irf1` | 0 | IRF transcription-factor paralog; canonical interferon regulator |
| `Irf2` | 0 | IRF paralog and IFN/ISRE transcriptional brake |
| `Irf3` | 0 | IRF paralog in antiviral signaling |
| `Irf5` | 0 | IRF paralog in innate inflammatory signaling |
| `Irf8` | 0 | IRF paralog, strongest focal subthreshold row was `Panx2` only, `pvals_adj = 0.121` |
| `Irf9` | 0 | IRF paralog in interferon-stimulated transcription |
| `Trp63` | 0 | upstream p63-family regulator of `Irf6` in ectoderm/palate biology |
| `Grhl2` | 0 | epithelial-barrier transcription factor in a related keratinocyte/periderm regulatory state |
| `Ovol2` | 0 | GRHL2-adjacent epithelial/EMT regulator |
| `Notch1` | 0 | canonical developmental transcriptional pathway comparator |
| `Notch2` | 0 | Notch receptor comparator; canonical HES/HEY targets flat in this neuronal assay |
| `Notch4` | 0 | Notch receptor comparator |
| `Dlx3` | 0 | ectodermal developmental transcription-factor comparator |
| `Dlx6` | 0 | DLX-family developmental transcription-factor comparator |
| `Smad1` | 0 | TGF-beta/BMP transcriptional mediator comparator |
| `Smad2` | 1 | TGF-beta/BMP mediator; one-gene boundary case |
| `Smad3` | 0 | TGF-beta/BMP mediator comparator |
| `Smad4` | 0 | TGF-beta/BMP mediator comparator |

I also queried focal rows for epithelial and Notch-output genes under the best visible analog perturbations (`Grhl2`, `Trp63`, `Ovol2`, `Notch1`, `Notch2`, `Notch4`, and visible IRFs). `Irf6`, `Trp63`, `Grhl2`, `Ovol2`, `Hes1`, `Hes5`, `Hey1`, `Hey2`, `Dtx1`, `Cdh1`, `Cldn3`, `Cldn4`, `Cldn6`, `Cldn7`, `Epcam`, `Esrp1`, and `Pvr` had `pvals_adj = 1.0` across the focal analog rows where they were measured. These large pseudocount-driven log fold changes are the expected low-expression behavior described in the dataset portrait; the Wilcoxon scores and adjusted p-values, rather than the raw log fold changes, showed that the canonical epithelial program was not engaged in these thalamic neurons.

## Same-experiment corpus context

The internal July corpus independently summarized the visible low-count analogs across all neuronal groups:

- `Irf1`: basal `Irf1` loss did not derepress or collapse canonical IFN-stimulated, antigen-presentation, or inflammatory transcripts in any sampled postmitotic neuron group; represented IRF-family, IFN-receptor/STAT, and NF-kappaB-neighbor targets also failed to activate a coherent IFN/MHC module.
- `Irf2`: acute `Irf2` loss produced no FDR-significant basal neuronal response and no IFN/ISG derepression; IRF-family and IFN-receptor/STAT perturbations were nearly flat.
- `Grhl2`: the canonical GRHL2 apical-junction, epithelial-barrier, and EMT-suppression program was absent from every measured neuronal group, and Ovol2/Zeb pathway neighbors did not phenocopy it.
- `Trp63`: `Trp63` was summarized as a pan-measured neuronal transcriptional null in the acute P16-to-P37/44 CRISPR loss-of-function screen.
- `Notch2`: `Notch2` produced a whole-surface neuronal null, and canonical `Hes`/`Hey`/`Dtx1`/`Rbpj` Notch-output genes were measured but not regulated.

These report findings did not substitute for the focal count calculation; they helped interpret the visible zeros as pathway quiescence in postmitotic neurons rather than just single-target noise.

## Target-specific reasoning

### Irf6

`Irf6` encodes an IRF-family DNA-binding transcription factor, but the best-established IRF6 biology is epithelial and craniofacial rather than tonic postnatal neuronal interferon signaling. External evidence places IRF6 in the keratinocyte/periderm proliferation-to-differentiation switch: p63 directly activates `IRF6`, IRF6 feeds back on DeltaNp63 protein abundance, and IRF6/p63 perturbations disrupt ectodermal and secondary-palate development in mouse and human cells (Thomason et al. 2010, DOI `10.1172/JCI40266`; Moretti et al. 2010, DOI `10.1172/JCI40267`). Human pathogenic variants in `IRF6` cause Van der Woude / popliteal pterygium or orofacial cleft phenotypes, with many deleterious variants in the DNA-binding and protein-binding domains (Alade et al. 2020, DOI `10.1002/mgg3.1355`).

The causal transfer chain from those systems to the requested experiment is weak:

`Irf6` loss -> altered IRF6-dependent p63/keratinocyte differentiation program -> epithelial adhesion/periderm and palate morphogenesis -> embryonic tissue fusion and stratified-epithelial phenotypes -> fetal or neonatal tissue endpoint.

The requested experiment is:

`Irf6` CRISPR in sparse postmitotic P16 neurons -> any direct neuronal IRF6-dependent transcription -> propagation within thalamic glutamatergic cells that survive until P37-P44 -> Wilcoxon DE among recovered `151 TH Prkcd Grin2c Glut` nuclei.

The represented visible perturbations test the key links that could have made `Irf6` nonzero. First, all six measured immune IRF paralogs in the focal group, `Irf1`, `Irf2`, `Irf3`, `Irf5`, `Irf8`, and `Irf9`, had zero focal FDR 0.05 genes, so the dataset does not show a basal IRF-family transcriptional response in this cell type. The same-experiment `Irf1` and `Irf2` reports further found no coherent IFN/ISG/MHC module across related IFN-receptor, STAT, and NF-kappaB perturbations. This argues that IRF-family membership alone does not produce a broad focal signature under unchallenged neuronal conditions.

Second, the specific developmental circuit around IRF6 was also flat in the focal endpoint. The direct upstream analog `Trp63` had `0` focal DEGs, the epithelial factor `Grhl2` had `0`, the GRHL2-adjacent `Ovol2` perturbation had `0`, the ectodermal `Dlx3` and `Dlx6` perturbations had `0`, and the closest represented TGF-beta/BMP SMADs were zero or a singleton (`Smad1 = 0`, `Smad2 = 1`, `Smad3 = 0`, `Smad4 = 0`). The Parquet rows for `Irf6`, epithelial adhesion genes (`Cdh1`, `Cldn3`, `Cldn4`, `Cldn6`, `Cldn7`, `Epcam`, `Pvr`), and canonical Notch-output genes (`Hes1`, `Hes5`, `Hey1`, `Hey2`, `Dtx1`) were all nonsignificant at `pvals_adj = 1.0` under `Trp63`, `Grhl2`, `Ovol2`, and Notch-receptor knockouts in the focal thalamic group. Those are imperfect analogs, because none is the exact IRF6 knockout, but they sit closer to the known IRF6 epithelial state than generic transcriptome neighbors would.

Third, the only weak counterexample was `Stat1`, with `1` focal DEG that was `Stat1` itself. That self-row is not a biologically analogous downstream IRF6 program and does not outweigh six zero-count IRF paralogs plus zero-count p63/GRHL2/Ovol2/Notch comparators.

Given these observations, I predict that `Irf6` loss in recovered `151 TH Prkcd Grin2c Glut` nuclei is a focal zero. The prediction is driven primarily by within-dataset evidence from the visible analogs; the external literature explains why the strongest IRF6 phenotypes are expected to require embryonic ectodermal and epithelial contexts not represented in this NeuN-enriched, postnatal neuronal assay.

## Final prediction

| target_name | predicted_n_degs |
| --- | ---: |
| `Irf6` | 0 |

## Limits

- `Irf6` itself was deliberately absent from the training count CSV and Parquet, so the endpoint is not directly observed.
- No visible perturbation is an obligate IRF6 cofactor in the exact thalamic neuronal context. `Trp63` and `Grhl2` test the best-known epithelial developmental neighborhood, while IRF1/2/3/5/8/9 test broader IRF-family behavior.
- The experiment measures single time-point survivor-state nuclear RNA 3-4 weeks after mosaic CRISPR perturbation. It could miss earlier editing-dependent selection, transient immediate responses, or effects restricted to glia, epithelia, vasculature, embryonic palate, skin, and periderm.
- The one-gene distinction between a true `0` and a singleton is assay-threshold-limited. The training distribution, all direct analog counts, and the lack of subthreshold focal `Irf6`-module rows support `0`, but a one-DEG result would not be biologically surprising.
