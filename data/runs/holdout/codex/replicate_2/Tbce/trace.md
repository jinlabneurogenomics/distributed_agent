# Trace

## Target and endpoint

- Target: `Tbce`
- Focal population: `151 TH Prkcd Grin2c Glut`
- Endpoint: `n_degs`, the count of measured genes with BH-adjusted Wilcoxon `pvals_adj < 0.05` in the focal population.
- Declared target biology came from `biology_bundles/Tbce.json`, checksum `490feb2093a4237c8902f4ff9c9c62a5bab515d2d0a69b1135e04932ee27ce84`. Its serving metadata reported `target_outcome_exposed=false` and `labeled_neighbors_exposed=false`.
- The 1,674-gene focal count table did not contain `Tbce`, so the target count was not read from the training table.

## Endpoint-blind Tbce prior

The canonical Tbce card made a nonzero thalamic response plausible:

- Exact focal expression was strong for this assay: `Tbce` was detected in `21,553 / 23,679` non-target cells in the focal class, or `91.02%`, with mean raw UMI `2.885` and mean CP10k `1.849`.
- TBCE acts in a renewable tubulin-folding/routing axis. The source card described TBCE as a tubulin-specific chaperone supporting alpha/beta tubulin heterodimer production and routing newly synthesized tubulin from neuronal Golgi regions into distal axons.
- The functional-stock adjudication called the operative stock `likely_substantially_depleted` by P37-P44 after a P16 edit, because the postnatal pmn mouse phenotype shows TBCE-dependent axonal microtubule loss beginning within roughly two weeks.
- I discounted that prior from a large response because the direct kinetic anchor is a lifelong destabilizing missense phenotype in motor and sensory pathways, not acute thalamic CRISPR loss; wild-type TBCE half-life was unresolved; and a related `Tbcel` gene leaves compensation unresolved rather than excluded.

## Training scale

The focal count table is very sparse overall:

- `1205 / 1674` training perturbations had `n_degs = 0`.
- Median `n_degs` was `0`, the 75th percentile was `1`, the 95th percentile was `18`, and the mean was pulled up to `14.05` by a long tail.

I used the FDR<0.05 focal counts from the declared count table and profile tables for the quantitative scale; the same-experiment Findings below were used only to interpret why the measured counts were or were not transferable.

The closest measured biological comparator was `Tbcd`:

- `Tbcd` is in the post-chaperonin tubulin-folding pathway and is the only direct tubulin-folding cofactor neighbor represented in the training table; `Tbca`, `Tbcb`, `Tbcc`, `Tbce`, and `Arl2` had no rows as training perturbations in the same parquet according to `Tbcd:E031`.
- In the focal class, `Tbcd` had exactly `12` FDR<0.05 genes: 9 up and 3 down in `17,259` measured features. The leading up features were `Tuba1a`, `Tuba1b`, `Ypel4`, `Nfil3`, `Kctd16`, `Satb1`, `Slc25a23`, `Mturn`, and `Jun`; the three down features were `Lrrc7`, `Ptprn2`, and `Samd5`.
- The corpus record `Tbcd:F002`, with evidence `Tbcd:E024` and `Tbcd:E025`, interprets the recurrent `Tbcd` response as alpha-tubulin mRNA feedback: `Tuba1a` was recurrent across all Tbcd responder groups and `Tuba1b` was up in the two strongest glutamatergic responders.
- `Tbcd:F006`, with evidence `Tbcd:E029`, `Tbcd:E030`, and `Tbcd:E031`, shows why I did not treat every tubulin or ARL2-adjacent perturbation as equivalent to Tbcd: direct `Tuba1a`, `Tuba4a`, and the indirect ARL2-axis proxy `Arl2bp` failed to phenocopy the 19 Tbcd FDR<0.10 gene-cell features.

The direct tubulin and sampled microtubule targets were mostly lower than `Tbcd`:

- `Tuba1a`: `7`
- `Tuba4a`: `2`
- `Tubb4b`: `1`
- `Tubb5`: `1`
- `Map1b`: `1`
- `Kif5a`: `1`
- `Stmn2`: `1`
- `Arl2bp`: `0`
- `Map6`: `0`
- `Spast`: `0`

This lower group pulled the expected Tbce value below broad stress perturbations but not to zero, because the target biology places TBCE with cofactor-mediated tubulin folding and axonal tubulin routing rather than with a single replaceable tubulin paralog.

## Profile boundaries

I compared `Tbcd`, direct tubulin genes, sampled microtubule targets, `Dctn1`, and the main empirical `Tbcd` neighbors in the declared Parquet filtered to `151 TH Prkcd Grin2c Glut`.

- `Tbcd` had near-zero focal whole-profile similarity to direct tubulin targets despite related genes: Pearson `0.0084` to `Tuba1a`, `0.0310` to `Tuba4a`, `0.0150` to `Tubb4b`, `0.0114` to `Tubb5`, and `-0.0047` to `Arl2bp`. None of those pairs shared a same-direction FDR<0.05 feature.
- `Dctn1` had `75` focal FDR<0.05 genes and a sterol/cholesterol response, anchored by `Dctn1:F001`; its cosine to `Tbcd` was only `0.0331`, with no same-direction significant overlap. I treated it as evidence that the assay can see cytoskeletal/transport perturbations, not as a Tbce count donor.
- The broad data-neighbor and proteasome contrasts were too large and mechanistically off-axis for direct scaling: `Grin1` had `89`, `Cic` had `576`, `Psmb4` had `742`, and `Psmc1` had `430` focal FDR<0.05 genes. `Tbcd:F005` specifically marks `Psmb4` and `Psmc1` as opposite for recurrent Tbcd tubulin features, so these were upper boundaries rather than analogues.

## Synthesis

The best endpoint-matched scale is `Tbcd = 12`: it is the only measured post-chaperonin tubulin-folding cofactor, it has the right narrow alpha-tubulin-feedback state, and the exact focal profile is modest rather than a broad proteostasis or sterol program. The main downward bearings are residual pre-edit TBCE protein/microtubule stock and quantitative transfer from pmn motor neurons to acute thalamic editing. The main upward bearings are high exact `Tbce` reach in the focal cells, continuous postmitotic tubulin-routing demand, and the card's `likely_substantially_depleted` stock call by harvest.

Those bearings land closest to the `Tbcd` focal count rather than to the flat tubulin-paralog boundary or to the broad `Dctn1`/proteasome states.

Predicted `n_degs`: `12`
