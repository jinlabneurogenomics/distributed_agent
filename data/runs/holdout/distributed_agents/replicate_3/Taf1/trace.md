# Taf1 DEG-count prediction

## Question interpreted

The requested held-out perturbation list contains one gene, `Taf1`. The task is to predict the number of genes that would pass `pvals_adj < 0.05` after `Taf1` CRISPR loss of function in `151 TH Prkcd Grin2c Glut` neurons. I treated the endpoint as the exact focal-cell `n_degs` count used in the training CSV, not as a genome-wide biological essentiality score. I also treated absent held-out signatures as intentionally hidden: no `Taf1` row from the DE parquet or training-count CSV was used.

## Sources used

- Training endpoint: `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
- Per-gene DE statistics: `[local file: training_de_all_cell_groups.parquet]`, filtered to `group_name == "151 TH Prkcd Grin2c Glut"` for selected observed comparator targets.
- Requested target manifest: `[local file: 231_Taf1.csv]`.
- Distributed Agents selected same-experiment semantic layer: `perturbai-july-260713-sourceguard-1773-v1`. `Taf1` itself had no Claim, Finding, or explicit relation in this release.
- Distributed Agents gene-annotation and analog-nomination stores over the PerturbAI closed mouse gene universe: native CORUM 5.0, one-to-one human CORUM projection through MGI homology downloaded 2026-09-13, KEGG mouse pathway annotations, Reactome mouse event annotations, GO annotations, and STRING v12.0 high-confidence physical interactions.
- Runtime profile comparison over focal-cell log fold changes for a Taf1-centered comparator cohort.
- External mechanistic priors came from the above curated databases: native mouse CORUM 5.0 placed Taf1 in TFIID complex records; Reactome placed Taf1 in `R-MMU-75953.1` RNA Polymerase II Transcription Initiation, `R-MMU-73779.1` RNA Polymerase II Transcription Pre-Initiation And Promoter Opening, and related Pol II promoter-clearance events; KEGG placed Taf1 in `mmu03022` Basal transcription factors; GO annotated Taf1 with histone acetyltransferase, protein kinase, histone-reader, TBP-class binding, and Pol II initiation activities.

## Computational steps

1. Loaded the manifest and confirmed that `Taf1` is the only requested held-out target.
2. Loaded the focal-cell training-count CSV. It contains 1,674 observed perturbations. The endpoint is sparse: 1,205 perturbations have `n_degs == 0`; the median is 0; the 75th percentile is 1; the 95th percentile is 18; and the 99th percentile is about 436.
3. Queried deterministic annotations for Taf1. The exact native mouse TFIID CORUM record `496` contains no non-held-out training target, so there was no same-complex training knockout. In the closed target universe, Reactome `R-MMU-75953` contains only `Gtf2h5` and held-out `Taf1`; KEGG `mmu03022` contains `Gtf2h5`, `Gtf2i`, `Gtf2ird1`, and held-out `Taf1`.
4. Ran Distributed Agents analog nomination against the actual 1,674-gene training universe. This prioritized `Gtf2h5` as the most direct basal-transcription comparator, then broader chromatin and coactivator genes such as `Ep300`, `Crebbp`, `Brd4`, and `Yy1`. The nominated candidate set did not contain a training-available exact TFIID subunit.
5. Filtered the 7.8 GB parquet only by focal cell group and selected comparator `gene_target` values. The saved run-local tables `taf1_comparator_focal_de.tsv` and `taf1_expanded_focal_de.tsv` contain the measured genes, focal log2 fold changes, and focal adjusted p-values for those observed training perturbations.
6. Ran a symmetric runtime profile comparison using focal `logfoldchanges` with `pvals_adj < 0.05` as the significance threshold and the top 200 signed features per tail for pairwise overlap. This compared nearby basal-transcription, Mediator, chromatin, proteasome, endolysosomal, and spliceosome perturbations in the same cell class as the requested endpoint.
7. Expanded the `Gtf2h5`/`Gtf2i`/`Gtf2ird1`/`Med15`/`Med23` cohort through the Distributed Agents same-experiment corpus and reviewed every returned candidate. `Med13`, `Med13l`, and `Cdk8` were kept as module-supporting Mediator controls. `Psmc1`, `Psmb4`, `Rab7`, and `Rnpc3` were kept only as high-count boundaries because their broad focal signatures are not Pol II initiation or TFIID-like mechanisms.

## Target-specific reasoning

### Taf1

**Primary local analogs**

| training target | focal `n_degs` | why it matters |
| --- | ---: | --- |
| `Gtf2h5` | 0 | The only non-held-out perturbation sharing the Reactome mouse RNA polymerase II initiation events with held-out `Taf1`; also in KEGG basal transcription. This is the closest training-available Pol II initiation comparator. |
| `Gtf2i` | 10 | KEGG basal-transcription member in the training universe, but biologically TFII-I rather than a canonical TFIID subunit. |
| `Gtf2ird1` | 4 | KEGG basal-transcription/GTF2I-family comparator with weak positive focal response. |
| `Med15` | 19 | Mediator tail subunit, adjacent to initiation but not TFIID. Its significant genes in the focal class were all downregulated. |
| `Med23` | 13 | Mediator tail subunit that shared a small downregulated thalamic module with `Med15`; all 13 focal DEGs were downregulated. |
| `Med13` | 11 | Mediator kinase-module support for a small transcription-regulatory footprint. |
| `Med13l` | 1 | Paralogous Mediator kinase-module boundary with only one focal DEG. |
| `Cdk8` | 0 | Another Mediator kinase-module boundary; same broad transcriptional neighborhood, no focal DEGs. |

`Gtf2h5`, the mechanistically closest observed Pol II initiation neighbor, had no significant focal genes. `Gtf2i` had 10 DEGs, 8 up and 2 down; `Gtf2ird1` had 4, all up. The Mediator subunits had small counts, ranging from 0 to 19, and the Med15/Med23/Med13 signatures were dominated by a small set of downregulated neuronal genes such as `Prkcd`, `Grm1`, `Pcp4`, `Plekhg1`, `Atp2a2`, and `Atp2b1`. In the profile comparison, `Gtf2h5` was closest to `Med23`, `Gtf2i`, `Med13`, and `Med15` by whole-profile Pearson correlation, but the top-tail overlaps were still small: for `Gtf2h5` versus `Med23`, Pearson was 0.695 with 49/200 negative-tail and 11/200 positive-tail overlaps; for `Gtf2h5` versus `Gtf2i`, Pearson was 0.693 with 44/200 negative-tail and 17/200 positive-tail overlaps. The small overlaps argue that these are calibration points for response breadth, not interchangeable expression states.

**Counterexamples and boundaries**

| training target | focal `n_degs` | interpretation |
| --- | ---: | --- |
| `Taf1b` | 0 | A Pol I SL1-associated TAF-like gene, not the large Pol II TFIID `Taf1`; useful only as a broad transcription boundary. |
| `Ep300` | 0 | HAT/coactivator neighbor from Taf1 GO molecular-function overlap but outside TFIID. |
| `Crebbp` | 8 | HAT/coactivator analog with a small positive focal response. |
| `Brd4` | 311 | Bromodomain/chromatin reader with a broad signature, but BET biology and P-TEFb coupling make it a poor TFIID quantitative proxy. |
| `Brd1` | 4 | Bromodomain chromatin boundary with little response. |
| `Rest` | 0 | Sequence-specific transcriptional repressor in the nominated Rett/chromatin neighborhood; no focal DEGs. |
| `Mecp2` | 16 | Rett-pathway/chromatin comparator with a small focal response. |
| `Chd8` | 61 | Chromatin remodeler directly connected to Taf1 through a STRING v12.0 physical edge in the annotation store, but more chromatin-remodeling than basal-initiation-like. |
| `Kmt2a` | 24 | MLL1/chromatin boundary; Taf1 and Kmt2a share MLL1 complex annotations but have different primary complexes. |
| `Yy1` | 720 | Ubiquitous DNA-binding chromatin regulator; a high-count counterexample showing that a nuclear transcription annotation can have a much broader state than Taf1's closest initiation factors. |
| `Sin3a` | 1433 | Large chromatin-corepressor state, far broader than the basal-transcription and Mediator neighbors. |
| `Psmc1` | 430 | Proteasome ATPase recovered by Gtf2h5/Med15/Med23 report comparators through shared modules; treated as a proteostasis boundary. |
| `Psmb4` | 742 | Proteasome beta subunit with the same broad-stress caveat as Psmc1. |
| `Rab7` | 501 | Endolysosomal response neighbor in the corpus-expanded set, not a TFIID mechanism. |
| `Rnpc3` | 868 | Minor spliceosome response neighbor, too broad and mechanistically distant for Taf1 transfer. |

The broad chromatin and proteostasis genes demonstrate that focal `151 TH Prkcd Grin2c Glut` neurons can show hundreds to thousands of DEGs after perturbing nuclear or housekeeping machinery. I did not transfer those large counts to `Taf1` because the high-count cases are driven by BET-chromatin, Sin3 corepressor, proteasome, endolysosomal, or spliceosome biology rather than the TFIID/Pol II preinitiation complex.

## Final prediction logic

The prediction is a small nonzero response. The zero side is supported by the closest observed Reactome Pol II initiation comparator, `Gtf2h5` with 0 DEGs, by `Taf1b` and `Ep300` with 0, and by the focal endpoint's zero-heavy training distribution. The nonzero side is supported by Taf1's central curated role in the TFIID complex and Pol II promoter opening and by nearby GTF2I/Mediator/chromatin coactivator perturbations that consistently have small positive counts (`Gtf2ird1` 4, `Crebbp` 8, `Gtf2i` 10, `Med13` 11, `Med23` 13, `Med15` 19).

I assigned `Taf1` a point prediction of **8 DEGs**. That keeps the estimate near the GTF2I/CREBBP/Mediator small-response band rather than the focal median of 0, while strongly discounting broad BRD4/YY1/SIN3A/proteasome signatures.

## Limits and extrapolation

- No exact TFIID subunit other than held-out `Taf1` was available as a training perturbation, so the most direct evidence is from TFIIH/GTF2I and Mediator, not from TAF2-15, TBP, or a Taf1 paralog.
- `Gtf2h5` is a TFIIH initiation factor, not a structural TFIID subunit. Its zero count could reflect subunit-specific dispensability, target engagement, or survivor-conditioned sampling rather than what Taf1 would do.
- `Gtf2i` and `Gtf2ird1` are KEGG basal-transcription members in the training universe but have Williams-locus, TFII-I-family biology that is not equivalent to canonical TFIID.
- The parquet signatures are powered by recovered nuclei. A severe Taf1 knockout could remove cells or leave only weakly affected survivors, so a small DEG count is compatible with an important cellular role.
- The profile correlations among candidate signatures are whole-vector correlations over many nonsignificant genes; the FDR-significant overlaps are very small for low-count perturbations. I therefore used them only to identify boundaries and local neighborhoods, not as a quantitative formula.
- External database memberships are curated priors and do not measure this screen's endpoint. They nominated the relevant comparator set; the final numeric prediction was calibrated primarily from observed focal DEG counts.
