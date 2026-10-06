# DEG-count prediction trace

## Question

The held-out manifest contains one requested perturbation, `Tubb4a`.  I interpreted the endpoint as the exact focal-cell response-breadth measurement in `151 TH Prkcd Grin2c Glut`: the number of measured genes whose Wilcoxon BH-adjusted p-value is `< 0.05` for a sparse postnatal AAV-CRISPR loss-of-function of the requested target.  The `Tubb4a` perturbation is absent from both supplied training files, so its count has to be inferred from non-held-out Perturb-seq perturbations plus gene-function knowledge.

Two small ambiguities I resolved:

- The count includes the perturbed target transcript when that transcript itself passes FDR.  This is clear from the focal training rows for the assayed tubulin genes: `Tubb4b` and `Tubb5` each have exactly one DEG in the endpoint file, and in the DE parquet that significant row is `Tubb4b` or `Tubb5`, respectively.
- A zero prediction should mean no measured row, including self, crosses FDR 0.05.  I therefore separated the probability of a target-transcript row from the probability of a downstream cytoskeletal state.

## Sources

- Primary input parquet: `training_de_all_cell_groups.parquet`; I used focal-cell rows for all assayed tubulin, microtubule-associated, kinesin, dynein, and cytoskeletal comparators.
- Primary endpoint CSV: `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`; this gave the observed focal counts for 1,674 non-held-out targets.
- Held-out manifest: `254_Tubb4a.csv`; this contained only `Tubb4a`.
- Internal same-experiment semantic layer: Distributed Agents corpus release `perturbai-july-260713-sourceguard-1773-v1`; there was no `Tubb4a` target-context card in this release, but there were target cards and synthesized claims for `Tuba1a`, `Tuba4a`, `Tubb4b`, and `Tubb5`.
- Internal Distributed Agents profile-neighbor runtime over the focal DE profiles.  I generated `profile_neighbors_tubulin.json` for `Tuba1a`, `Tuba4a`, `Tubb4b`, `Tubb5`, `Map1b`, `Mapt`, `Kif1a`, and `Kif5a` against the full 1,674-target training universe.
- PubMed literature for TUBB4A disease and tubulin autoregulation: Simons et al. 2013, DOI `10.1016/j.ajhg.2013.03.018`, PMID `23582646`; Hamilton et al. 2014, DOI `10.1093/brain/awu110`, PMID `24785942`; Krajka et al. 2022, DOI `10.1126/sciadv.abj9229`, PMID `35275727`; Lin et al. 2019, DOI `10.1126/science.aaz4352`, PMID `31727855`; Hopfler et al. 2023, DOI `10.1016/j.molcel.2023.05.020`, PMID `37295431`.

## Computational checks over the training data

The focal training-count distribution is heavily zero-inflated: among 1,674 training perturbations, 1,205 had `0` DEGs, 363 had `1-9`, 63 had `10-89`, and only 43 had `>=100`.  Tubulin and cytoskeletal genes fell into the weak or null bins:

| training target | focal n_degs | focal DE pattern most relevant to Tubb4a |
|---|---:|---|
| `Tuba1a` | 7 | `Tuba1a` down plus six alpha/beta tubulin paralogs up: `Tubb3`, `Tubb2a`, `Tuba4a`, `Tubb4a`, `Tubb4b`, `Tubb5` |
| `Tuba4a` | 2 | `Tuba4a` down and `Mast1` up |
| `Tubb4b` | 1 | `Tubb4b` down only |
| `Tubb5` | 1 | `Tubb5` down only |
| `Map1b` | 1 | essentially self only |
| `Mapt` | 1 | essentially self only |
| `Stmn2` | 1 | self down; `Tuba1a` was subthreshold |
| `Mapre2` | 1 | essentially self only |
| `Kif1a`, `Kif5a`, `Kif5c`, `Kif21a` | 1 each | mostly self or singletons |
| `Kif1b`, `Kif2a`, `Kif3b`, `Map6`, `Spast`, `Actn4` | 0 | no FDR 0.05 focal response |

For the directly assayed tubulin genes in `151 TH Prkcd Grin2c Glut`, I also inspected the ranked focal DE rows.  `Tuba1a` had 121 matched perturbed nuclei and 23,679 controls and gave the only multi-tubulin response: the target was down with `log2FC = -0.967`, `p_adj = 2.8e-20`; `Tubb4a` itself was up as a downstream gene with `log2FC = 0.506`, `p_adj = 2.9e-5`.  `Tuba4a`, `Tubb4b`, and `Tubb5` had comparable matched perturbed counts of 199, 171, and 186 and their target rows were also strongly reduced, but they did not induce significant `Tubb4a`, `Tubb3`, `Tubb2a`, `Tuba1a`, or other beta-tubulin replacement rows.

I computed focal whole-transcriptome log-fold-change neighbor lists for the four direct tubulin anchors after collapsing duplicate `(measured gene, target)` coordinates by their mean only for the correlation matrix.  This check was a falsification step rather than a source of candidate analogs: sparse tubulin profiles had very high raw correlations with many unrelated zero-DEG targets, reflecting broad shared structure in log-fold-change ranks.  I therefore did not use raw whole-profile correlation to move the prediction away from the FDR-supported tubulin rows and the corpus-curated residual contrasts.

## Same-experiment biological analogs

The most important positive analog for a tubulin response was `Tuba1a`, because it proved that the P16-to-P37/P44 NeuN+ snRNA-seq design can detect tubulin dosage feedback in this same thalamic glutamatergic class.  `Tuba1a` loss up-regulated both alpha- and beta-tubulin paralog transcripts, including `Tubb4a`.

The stronger quantitative analogs for `Tubb4a` were the assayed beta-tubulin genes:

- `Tubb4b`, focal `n_degs = 1`: in the focal parquet the only significant row was `Tubb4b` itself (`log2FC = -0.597`, `p_adj = 1.1e-7`).  The Distributed Agents `Tubb4b` report states that `Tubb4b` loss was buffered across recovered neuronal groups and produced zero non-self FDR<0.10 genes in every group; it also specifically contrasts `Tubb4b` against `Tuba1a`, `Tuba4a`, `Tubb5`, `Stmn2`, `Mapt`, `Map1b`, `Map6`, `Mapre2`, `Kif5a`, `Kif5c`, and `Dctn1`, with no coherent microtubule phenocopy.
- `Tubb5`, focal `n_degs = 1`: again the focal FDR 0.05 signal was just `Tubb5` self-depletion (`log2FC = -1.478`, `p_adj = 7.7e-23`).  The Distributed Agents `Tubb5` card notes that even strong measured `Tubb5` transcript loss did not bring in tubulin-paralog compensation, p53 targets, ISR/UPR genes, or a stable beta-tubulin downstream mRNA program.
- `Tuba4a`, focal `n_degs = 2`: this was useful as an alpha-tubulin counterexample.  It had self-depletion plus one `Mast1` singleton in the focal class, not the six-gene `Tuba1a` paralog feedback module.
- `Map1b`, `Mapt`, `Stmn2`, `Mapre2`, `Kif1a`, `Kif5a`, `Kif5c`, and several null kinesin/MAP/dynein perturbations were negative boundaries.  The broad microtubule cytoskeleton is not transcribed as one shared stress module in these postmitotic recovered nuclei.

The corpus-level synthesized claims reinforce the same direction: in release `perturbai-july-260713-sourceguard-1773-v1`, `Tuba1a` loss is annotated as uniquely eliciting alpha/beta-tubulin mRNA up-regulation among the represented tubulin and microtubule-related perturbations; `Tuba4a`, `Tubb4b`, and `Tubb5` do not phenocopy it.

## Target-specific rationale for Tubb4a

`Tubb4a` encodes beta-tubulin 4A, a microtubule heterodimer subunit.  Dominant human TUBB4A variants cause a continuum from DYT-TUBB4A dystonia to hypomyelination with atrophy of the basal ganglia and cerebellum; the recurrent H-ABC variants alter alpha/beta tubulin dimerization, microtubule polymerization, or microtubule integration in disease-relevant cellular assays.  That external evidence argues that TUBB4A is a real neuronal/oligodendroglial microtubule disease gene, not a passenger.

The external disease literature does not argue for a large focal count in this experiment, however.  H-ABC and DYT-TUBB4A are dominated by heterozygous missense mechanisms; Krajka et al. 2022 showed distinct pathogenic effects of H-ABC- versus dystonia-causing variants on microtubule polymerization/integration, while this screen uses acute sparse CRISPR loss-of-function in juvenile postmitotic mouse neurons.  The NeuN+ focal population also excludes or strongly undersamples oligodendrocytes, a major compartment for hypomyelinating TUBB4A biology.

Mechanistically, the one part of the external biology that could have expanded the response was general tubulin autoregulation: excess soluble tubulin can trigger TTC5-dependent co-translational tubulin mRNA decay, with SCAPER/CCR4-NOT recruitment downstream of TTC5.  The same-experiment rows show this does not translate into a generic FDR-scale RNA replacement module after every tubulin loss.  The postnatal `Tubb4b` and `Tubb5` knockouts were buffered, and the Distributed Agents corpus explicitly separates them from `Tuba1a`.

My zero/nonzero decision is therefore:

- Nonzero rather than zero because `Tubb4a` was measurably expressed in the focal class and was itself a significant downstream row after `Tuba1a` loss; every directly assayed tubulin training target had a significant self-transcript row in `151 TH Prkcd Grin2c Glut`.
- Approximately one rather than seven or higher because the closest beta-tubulin loss-of-function analogs, `Tubb4b` and `Tubb5`, each stopped at one focal DEG and lacked FDR-significant alpha/beta-tubulin compensation.  I expect `Tubb4a` loss to look like these buffered beta-tubulin perturbations more than like the `Tuba1a` exception.

The resulting point prediction is `1` DEG.

## Limits

This is still an extrapolation.  The most direct beta-tubulin paralogs `Tubb2a`, `Tubb2b`, `Tubb3`, and the held-out `Tubb4a` itself were not present as perturbations in the training endpoint, and the Distributed Agents corpus had no `Tubb4a` card.  The prediction also assumes that the CRISPR guides for `Tubb4a` would give enough transcript-level reduction for the self row to pass FDR, as happened for `Tuba1a`, `Tuba4a`, `Tubb4b`, and `Tubb5`; target mRNA loss is not a general measure of editing efficiency in this assay.  Finally, transcript counts in recovered thalamic glutamatergic nuclei cannot rule out later axonal, microtubule-polymer, oligodendrocyte, or dominant-missense phenotypes that would not appear as a broad nuclear RNA state here.
