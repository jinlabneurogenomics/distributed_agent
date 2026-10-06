# Prediction trace

## Question and interpretation

The requested held-out perturbation is `Ndufs3`.  I interpreted the endpoint as the integer `n_degs` for the single focal group, `151 TH Prkcd Grin2c Glut`, counting every measured row with `pvals_adj < 0.05` in the same differential-expression table that generated the training CSV.  The on-target transcript is therefore part of the count when it survives BH correction; the focal counts for many measured `Nduf*` targets are single self-transcript calls.

The final prediction is:

| target_name | predicted_n_degs |
|---|---:|
| Ndufs3 | 1 |

## Sources used

- Input endpoint table: `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
- Input DE table: `[local file: training_de_all_cell_groups.parquet]`.
- Requested manifest: `[local file: 147_Ndufs3.csv]`.
- Distributed Agents same-experiment corpus: release `perturbai-july-260713-sourceguard-1773-v1`.
  - There was no direct `Ndufs3` record, consistent with this target being held out.
  - The central family-level claim was `claim:46019c530f79c38141a7`: represented nuclear Complex I subunit and assembly-factor perturbations are broadly buffered in this postnatal neuronal CRISPR/snRNA-seq assay and fail to form a shared acute OXPHOS-stress module.
  - Key target findings were `Ndufs2:F004`, `Ndufs4:F001/F002/F003/F004`, and `Ndufs8:F001/F003/F004`.
- Distributed Agents runtime profile tools:
  - `profile_compare` over the 23 focal-cell `Nduf*`/`Ndufaf*` training signatures.
  - `profile_inspect` for the `Ndufs2`, `Ndufs4`, `Ndufs7`, `Ndufs8`, and `Ndufv1` focal profiles versus proximal `Nduf`/`Ndufaf` peers.
- PubMed literature:
  - Benit et al. 2004, DOI `10.1136/jmg.2003.014316`, PMID `14729820`: pathogenic human `NDUFS3` mutations cause Complex I deficiency with Leigh or Leigh-like neurologic disease.
  - D'Angelo et al. 2021, DOI `10.1016/j.celrep.2021.109002`, PMID `33882309`: `NDUFS3` is a non-catalytic core Complex I subunit whose depletion affects Complex I disassembly and maturation; complete ablation still left small amounts of functional Complex I in mammalian cells.
  - Quintana et al. 2010, DOI `10.1073/pnas.1006214107`, PMID `20534480`: brain `Ndufs4` loss in mice causes progressive encephalopathy resembling Leigh syndrome.
  - van de Wal et al. 2022, DOI `10.1093/brain/awab426`, PMID `34849584`: review of human NDUFS4 Complex I disease and the severe phenotypes of `Ndufs4` knockout mouse models.

## Computations over the input data

1. I read the requested-target CSV and found exactly one held-out target, `Ndufs3`.

2. I summarized focal `n_degs` for all training targets whose names contain `Nduf`, and then separated the direct Complex I structural/assembly set:

| training target | focal n_degs |
|---|---:|
| Ndufa10 | 1 |
| Ndufa11 | 0 |
| Ndufa12 | 0 |
| Ndufa4 | 1 |
| Ndufa6 | 1 |
| Ndufa8 | 0 |
| Ndufa9 | 0 |
| Ndufaf2 | 0 |
| Ndufaf4 | 0 |
| Ndufaf5 | 0 |
| Ndufb10 | 1 |
| Ndufb11 | 1 |
| Ndufb3 | 0 |
| Ndufb7 | 0 |
| Ndufb8 | 1 |
| Ndufb9 | 1 |
| Ndufc2 | 1 |
| Ndufs2 | 1 |
| Ndufs4 | 0 |
| Ndufs7 | 0 |
| Ndufs8 | 1 |
| Ndufv1 | 0 |
| Ndufv2 | 1 |

The class is sharply bounded in this focal cell type: 12/23 had zero DEGs and 11/23 had one DEG; none produced a multi-gene response.

3. I filtered the parquet to `group_name == "151 TH Prkcd Grin2c Glut"` and the Complex I comparators to see whether the singletons were pathway genes or just self-depletion.  The most relevant Q/N-module comparators were:

| target | n_pert | focal n_degs | self log2FC | self p_adj | FDR<0.05 gene |
|---|---:|---:|---:|---:|---|
| Ndufs2 | 197 | 1 | -0.728 | 8.26e-12 | `Ndufs2` |
| Ndufs4 | 103 | 0 | -0.623 | 0.502 | none |
| Ndufs7 | 263 | 0 | -0.344 | 1.0 | none |
| Ndufs8 | 285 | 1 | -0.650 | 3.06e-08 | `Ndufs8` |
| Ndufv1 | 223 | 0 | -0.292 | 1.0 | none |
| Ndufv2 | 93 | 1 | -0.291 | 1.0 | `Cdc40` |

This argues that a nonzero NDUF endpoint generally means "the target mRNA crossed FDR" or an isolated singleton, not activation of a coherent respiratory-chain program.

4. I tested the expected mitochondrial stress axis by examining `Asns`, `Atf4`, `Chac1`, `Ddit3`, `Herpud1`, `Slc7a5`, `Mthfd2`, `Lonp1`, selected Complex I transcripts, and mitochondrial RNAs in `Ndufs2`, `Ndufs4`, `Ndufs7`, `Ndufs8`, `Ndufv1`, `Ndufv2`, `Opa1`, and `Elp1`.

   `Ndufs2`, `Ndufs4`, `Ndufs7`, `Ndufs8`, `Ndufv1`, and `Ndufv2` left the stress markers at `pvals_adj = 1.0` in this focal group.  As same-assay positive controls, `Opa1` had 37 focal DEGs and induced `Asns`, `Chac1`, `Ddit3`, `Mthfd2`, `Slc7a5`, and `Herpud1`, while `Elp1` had 645 focal DEGs with a strong ISR-like amino-acid response.  Thus the focal readout can see ISR/stress programs, but acute NDUF subunit perturbation did not engage one.

5. I computed a Distributed Agents focal profile comparison across the 23 measured `Nduf*`/`Ndufaf*` training signatures using all 17,259 focal features per target.  The comparison had no missing profiles and classified 12 targets as `no_significant_features` and 11 as `1_to_9_significant_features`.  Inspection of the NDUFS anchors showed:

| anchor | significant focal features in profile |
|---|---:|
| Ndufs2 | 1 |
| Ndufs4 | 0 |
| Ndufs7 | 0 |
| Ndufs8 | 1 |
| Ndufv1 | 0 |

The inspected NDUFS-vs-NDUF/NDUFAF pairs had zero intersections of FDR-significant features despite positive all-feature correlations driven by weak global structure, so I treated them as a shared near-null cohort, not as a set of reproducible downstream genes.

## Target-specific reasoning

### `Ndufs3`

`Ndufs3` encodes a nuclear core subunit of respiratory Complex I.  Human `NDUFS3` variants can cause Complex I deficiency and Leigh syndrome (Benit et al. 2004), and NDUFS3 depletion changes Complex I disassembly and ND4-module maturation in mammalian cells (D'Angelo et al. 2021).  Those facts make `Ndufs3` a mechanistically real Complex I perturbation, but the correct training evidence is the same-experiment sparse postnatal CRISPR screen rather than complete germline or cultured-cell loss.

The most biologically relevant training perturbations are the other nuclear core Complex I genes:

- `Ndufs2`: 1 focal DEG, the `Ndufs2` self transcript.
- `Ndufs4`: 0 focal DEGs, despite being a severe Leigh-model gene in complete neural loss.
- `Ndufs7`: 0 focal DEGs.
- `Ndufs8`: 1 focal DEG, the `Ndufs8` self transcript.
- `Ndufv1`: 0 focal DEGs.
- `Ndufv2`: 1 focal DEG, an isolated `Cdc40` call while the `Ndufv2` self transcript was not significant.

The broader NDUFA/NDUFB/NDUFC/NDUFAF panel supplied counterexamples to any rule that "Complex I subunit" implies a stress response.  All 23 focal Complex I relatives were either 0 or 1, and the Distributed Agents corpus found that represented NDUF and NDUFAF perturbations were broadly buffered rather than converging on an acute OXPHOS-stress module.  The same assay had strong responses for `Opa1` and `Elp1`, so the zero/one NDUF counts are not just an inability of snRNA-seq to detect nuclear stress when it exists.

I therefore predicted `Ndufs3` to be nonzero but minimal: one FDR gene.  The nonzero part is a narrow on-target prediction, by analogy to `Ndufs2`, `Ndufs8`, `Ndufa10`, `Ndufb10`, `Ndufb8`, `Ndufb9`, and `Ndufc2`, where CRISPR knockdown of a moderately expressed nuclear OXPHOS transcript often made that transcript itself the only focal DEG.  The approximate count is capped at one because same-Q-module and same-N-module comparators did not show any reproducible downstream stress signature, no NDUF family member in this focal cell type exceeded one DEG, and the corpus found no hidden same-complex transcriptional module.

## Limits

This is mainly an extrapolation from sibling Complex I perturbations; `Ndufs3` itself was held out and absent from the Distributed Agents corpus and training parquet as a `gene_target`.  The 0-versus-1 distinction depends on guide efficiency, mRNA expression, and whether the target transcript crosses FDR in this one cell type, none of which can be measured for `Ndufs3` from the released training inputs.  The data also do not measure DNA indels, NDUFS3 protein, Complex I enzymatic activity, ATP, NADH/NAD+, ROS, or survival bias in unrecovered neurons.  Complete Complex I loss is biologically severe, as shown by human `NDUFS3` disease and `Ndufs4` mouse models, but the prediction is specific to the acute, mosaic, P16-to-P37/44 neuronal snRNA-seq assay.
