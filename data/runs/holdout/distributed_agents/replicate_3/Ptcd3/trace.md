# Ptcd3 DEG-count prediction

## Question interpreted

The task is to predict `n_degs` for the held-out perturbation `Ptcd3` in
`151 TH Prkcd Grin2c Glut` nuclei. I treated the count exactly as defined in the
training CSV: the number of measured genes, including the edited gene itself if
it is measured, with Wilcoxon Benjamini-Hochberg adjusted `pvals_adj < 0.05`.
The requested manifest contained one target, `Ptcd3`, and `Ptcd3` was absent
from both the focal training-count CSV and the differential-expression parquet.

The main ambiguity I resolved is that mitochondrial translation is a strong
essential process in other settings, but this endpoint is a survivor-conditioned
single-nucleus transcriptional breadth endpoint after acute sparse AAV-CRISPR in
postnatal neurons. I therefore calibrated the prediction from same-assay
Perturb-seq behavior of mitochondrial translation, mitoribosome, mitochondrial
RNA, OXPHOS, and stress-response analogs rather than from viability or human
disease severity.

## Sources used

- `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`,
  the direct training endpoint for 1,674 non-held-out targets in the focal cell
  group.
- `[local file: training_de_all_cell_groups.parquet]`,
  filtered to `group_name == "151 TH Prkcd Grin2c Glut"` for selected analog
  perturbations.
- `gene-annotation-skill`, using the deterministic PerturbAI closed-universe
  annotation store with GO, Reactome, KEGG, MSigDB, native CORUM,
  one-to-one human CORUM projection, and pinned STRING v12.0 physical
  interactions.
- `gene-analog-nomination-skill`, run with the 1,674 focal training genes as the
  explicit training universe. This selected training-available `Ptcd3` analogs
  before I looked at DEG counts.
- Distributed Agents selected same-experiment corpus
  `perturbai-july-260713-sourceguard-1773-v1`, especially the induced topology
  and full Finding cards for `Dap3`, `Gfm2`, `Lars2`, `Rars2`, `Lrpprc`, and
  `Opa1`.
- Reactome mouse pathway records `R-MMU-5368287.1`, Mitochondrial translation,
  and `R-MMU-5419276.1`, Mitochondrial translation termination.
- QuickGO term `GO:0032543`, mitochondrial translation.
- NCBI Gene record 69956 for mouse `Ptcd3`.
- STRING physical evidence as bundled in the local annotation store,
  pinned to STRING v12.0; the relevant record was the high-confidence
  `Ptcd3`-`Dap3` physical interaction.
- Literature for PTCD3 biology: Davies et al. 2009,
  "Pentatricopeptide repeat domain protein 3 associates with the mitochondrial
  small ribosomal subunit and regulates translation",
  DOI 10.1016/j.febslet.2009.04.048, PMID 19427859; Borna et al. 2019,
  "Mitochondrial ribosomal protein PTCD3 mutations cause oxidative
  phosphorylation defects with Leigh syndrome",
  DOI 10.1007/s10048-018-0561-9, PMID 30607703.

## Computational steps

1. I read the held-out manifest and confirmed that the only requested row is
   `Ptcd3`.

2. I summarized the focal training counts. They are highly zero-inflated:
   1,205 of 1,674 training targets have `n_degs == 0`; 363 have 1 to 9; 63 have
   10 to 99; and only 43 have at least 100. The median is 0.

3. I nominated analogs for `Ptcd3` with the gene-analog nomination skill rather
   than by string matching symbols. `Ptcd3` was placed in Reactome
   mitochondrial translation and termination, GO mitochondrial translation,
   GO ribosomal small-subunit binding, and the pinned STRING physical network.
   The most specific training-available nominees were:

   - `Gfm2`, shared Reactome mitochondrial translation and termination;
   - `Lars2` and `Rars2`, shared GO mitochondrial translation;
   - `Dap3`, high-confidence STRING v12.0 physical interaction with `Ptcd3` and
     projected mitochondrial ribosome CORUM membership.

   The nominator also surfaced mitochondrial neighbors such as `Lrpprc`,
   `Fars2`, `Rmnd1`, `Slc25a46`, `Ndufs4`, and `Opa1` through graph-supported
   mitochondrial-translation communities; I kept these as looser analogs or
   counterexamples.

4. I scanned only the focal row groups of the 8 GB parquet. Row-group statistics
   limited the scan to row groups whose `group_name` range included
   `151 TH Prkcd Grin2c Glut`; each decoded row group was filtered to the focal
   group and a 30-gene comparator set. The retained table had 517,770 rows,
   exactly 17,259 measured genes for each of 30 selected perturbations. I then
   recomputed per-target `sum(pvals_adj < 0.05)`, minimum adjusted p-value,
   leading genes by adjusted p-value, and Spearman correlations of signed
   Wilcoxon scores among the most direct profiles.

5. I inspected Distributed Agents corpus topology over `Dap3`, `Gfm2`, `Lars2`, `Rars2`,
   `Lrpprc`, `Opa1`, `Ndufs4`, `Fars2`, `Rmnd1`, and `Slc25a46`. `Ptcd3`
   itself was absent from this selected corpus release, so the corpus could not
   provide a direct held-out profile. The analog cohort was, however, connected
   by explicit same-experiment Finding references. The relevant Finding cards
   report that `Gfm2`, `Lars2`, `Rars2`, `Dap3`, and `Lrpprc` were flat or weak
   in mitochondrial-translation/OXPHOS comparisons, whereas `Opa1` was an
   ISR-like mitochondrial-stress positive control.

## Ptcd3-specific analog evidence

| training perturbation | focal `n_degs` | why compared with `Ptcd3` | focal expression-pattern evidence |
| --- | ---: | --- | --- |
| `Gfm2` | 0 | Most specific curated training analog: it shares Reactome `R-MMU-5368287.1` Mitochondrial translation and `R-MMU-5419276.1` Mitochondrial translation termination with `Ptcd3`. | No FDR genes; the best nominal genes all had adjusted `pvals_adj == 1`. Spearman score correlation with the already flat `Dap3`, `Lars2`, and `Rars2` signatures was only 0.025, 0.019, and 0.025, respectively. Distributed Agents `Gfm2:F003` says represented core OXPHOS/mitochondrial-translation perturbations were flat or weak compared with `Opa1`. |
| `Lars2` | 0 | GO `GO:0032543` mitochondrial-translation member and mitochondrial leucyl-tRNA synthetase, testing whether mitochondrial tRNA charging caused a similar state. | No FDR genes; minimum adjusted p-value 0.9517. Distributed Agents `Lars2:F004` explicitly grouped `Fars2`, `Gfm2`, and `Rars2` as also flat or nearly flat in this screen. |
| `Rars2` | 0 | GO mitochondrial-translation member and mitochondrial arginyl-tRNA synthetase. | No FDR genes; minimum adjusted p-value 1.0. Distributed Agents `Rars2:F003` says the literature-obvious mitochondrial-translation relatives `Fars2`, `Lars2`, and `Gfm2` did not phenocopy the sparse `Rars2` surface. |
| `Dap3` | 1 | Closest available mitoribosome-protein comparator; it had a STRING v12.0 high-confidence physical edge to `Ptcd3` in the local annotation store and projected human CORUM 28S/55S mitochondrial ribosome membership. | The only FDR gene was `Dap3` itself, down in its own perturbation (`logfoldchanges = -0.676`, `pvals_adj = 3.95e-06`); the next genes had `pvals_adj == 1`. Distributed Agents `Dap3:F002` reports no detectable `Asns`, `Ddit3`, `Chac1`, `Slc7a5`, `Shmt2`, `Herpud1`, `mt-Co2`, or `mt-Cytb` stress program after `Dap3`. |
| `Lrpprc` | 0 | Mitochondrial RNA stabilizer with GO regulation of mitochondrial translation, used as a mitochondrial RNA-expression neighbor rather than a mitoribosome subunit. | No FDR genes; minimum adjusted p-value 0.1744. Distributed Agents `Lrpprc:F003` reports no meaningful cross-perturbation neighbor and divergence from textbook mitochondrial comparators in this neuronal screen. |
| `Fars2` | 0 | Mitochondrial aminoacyl-tRNA synthetase in the same weak core mitochondrial-protein-synthesis community. | No FDR genes; all leading genes had adjusted p-value 1.0. The Distributed Agents topology placed it in a fully connected weak mitochondrial-translation set with `Gfm2`, `Lars2`, `Lrpprc`, `Rars2`, and `Rmnd1`. |
| `Rmnd1` | 0 | Mitochondrial translation-support factor surfaced by the same community as `Gfm2` and `Lrpprc`. | No FDR genes; all leading genes had adjusted p-value 1.0. It did not provide a hidden strong stress state. |
| `Slc25a46` | 1 | Mitochondrial dynamics/import stress counterexample linked to the `Gfm2`/`Opa1` corpus neighborhood, not a direct translation factor. | The only FDR gene was `Slc25a46` itself. |
| `Opa1` | 37 | Positive control for a mitochondrial perturbation that is visibly detected in `151 TH Prkcd Grin2c Glut`; mechanistically a cristae/fusion GTPase rather than a mitochondrial translation component. | `Opa1` up-regulated an ISR/amino-acid program headed by `Asns`, `Mars1`, `Chac1`, and `Ddit3` and gave 37 FDR genes in the focal group. This shows mitochondrial stress can be recovered in the assay but argues against transferring a broad `Opa1` count to `Ptcd3`. |
| `Ndufs4`, `Uqcrfs1`, `Uqcrb`, `Uqcrc2`, `Uqcrh`, `Uqcrq`, `Cyc1`, `Ndufa4`, `Ndufb7` | 0 or 1 | OXPHOS and complex III/I comparators downstream of mitochondrial translation. | These were flat or self-target-only near-zero profiles: `Ndufs4`, `Uqcrfs1`, `Uqcrb`, `Uqcrh`, and `Ndufb7` had 0; `Cyc1`, `Uqcrc2`, and `Ndufa4` had 1, driven by their own transcript; `Uqcrq` had 1 unrelated leading gene. |
| `Afg3l2`, `Clpp`, `Clpx`, `Lonp1`, `Yme1l1` | 0 | Mitochondrial proteostasis counterexamples; `Clpp` also shares a Perrault-spectrum disease lane with mitochondrial translation genes. | Every focal profile had 0 FDR genes, so mitochondrial organelle membership or severe organismal phenotypes were not sufficient for a response in this endpoint. |

I also checked broad candidates that the nominator found through non-specific
translation or ribosomal-small-subunit annotations. `Ddx3x` had 8 DEGs,
`Hspa5` had 5, `Mcts1` had 0, while proteasome factors `Psmb4` and `Psmc1`
had 742 and 430 DEGs. These were rejected as quantitative analogs because they
reflect cytosolic translation, ER stress, or proteasome biology rather than
the mitochondrial small ribosome.

## Biological rationale and prediction

`Ptcd3` encodes a pentatricopeptide-repeat protein associated with the
mitochondrial small ribosomal subunit and required for mitochondrial translation
in the Davies et al. 2009 cell-biological study. Reactome places mouse `Ptcd3`
in mitochondrial translation and termination, and severe human PTCD3 mutations
can cause oxidative-phosphorylation defects with Leigh syndrome
(Borna et al. 2019). This external biology makes a mitochondrial-translation
response mechanistically plausible.

The same-experiment evidence points the other way for this endpoint. The three
specific training-available mitochondrial-translation analogs with endpoint
counts, `Gfm2`, `Lars2`, and `Rars2`, all had `n_degs = 0` in
`151 TH Prkcd Grin2c Glut`. The nearest mitoribosomal protein comparator,
`Dap3`, had `n_degs = 1`, and that one gene was the edited transcript itself;
its downstream profile was FDR-null. Neighboring mitochondrial RNA,
OXPHOS, and proteostasis perturbations were also almost all 0 or 1. Finally,
`Opa1` proves that an ISR-like mitochondrial stress program is detectable in
this cell type, but direct mitoribosome and mitochondrial-translation
perturbations did not activate that program.

I therefore predict that acute sparse `Ptcd3` editing will be buffered or
survivor-conditioned below the FDR threshold in this cell group. I chose
`0` rather than `1` because `Dap3`, `Tomm40`, `Cyc1`, `Uqcrc2`, and `Ndufa4`
show that single-DEG mitochondrial profiles often consist only of a target RNA
self-effect, and target-transcript loss is not reliably transferable across
perturbations in this assay.

Predicted `Ptcd3 n_degs`: **0**.

## Limits

- No `Ptcd3` DE profile or Distributed Agents Finding existed in the training parquet or
  the selected same-experiment corpus, so the prediction extrapolates from
  adjacent mitochondrial-translation genes rather than from a paralog or a
  second PTCD-family member.
- `Gfm2`, `Lars2`, and `Rars2` share the mitochondrial protein-synthesis axis
  but are not structural 28S small-subunit PPR proteins. `Dap3` is structural
  but did not have the same GO mitochondrial-translation annotation as `Ptcd3`
  in the curated store. The analog set is therefore mechanistically close but
  imperfect.
- Complete PTCD3 loss is expected to impair oxidative phosphorylation. The
  experiment instead used partial, mosaic postnatal CRISPR in recovered neuronal
  nuclei, so strong organismal or biochemical phenotypes need not appear as many
  FDR-significant snRNA-seq genes.
- The zero prediction is most confident for downstream stress genes. The final
  count could be 1 if the `Ptcd3` transcript itself happened to pass FDR in its
  own contrast; the training data did not justify assigning that self-effect as
  the point estimate.
