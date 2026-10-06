# Held-out prediction for Epha6 in 151 TH Prkcd Grin2c Glut

## Question and endpoint

The held-out target file for this run contains one mouse gene, `Epha6`. I interpreted the task as a point prediction of:

`n_degs = count(names with pvals_adj < 0.05)`

for the missing `Epha6` perturbation in the focal thalamic glutamatergic cell group, `151 TH Prkcd Grin2c Glut`. The count includes the perturbed gene's own transcript when that self row is significant; for example, the observed `Epha4` count of 1 in this same cell group is just `Epha4` itself.

The main ambiguity I resolved was how to treat biologically important but mostly morphologic Eph/ephrin signaling. I treated the direct endpoint as a durable single-nucleus RNA response 3-4 weeks after sparse postnatal CRISPR editing, not as axon guidance, kinase activity, cell adhesion, or a phosphoproteomic readout.

## Sources used

- Input training counts: `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
- Input DE parquet: `[local file: training_de_all_cell_groups.parquet]`.
- Requested-target manifest: `[local file: 070_Epha6.csv]`.
- Distributed Agents same-experiment corpus, release `perturbai-july-260713-sourceguard-1773-v1`, including the Epha/Ephb reports and the higher-order claim that single represented Eph receptors in postnatal neurons do not produce a common Eph-family nuclear transcriptomic program.
- Distributed Agents runtime profile-neighbor computation over the focal-cell log-fold-change vectors for `Epha2`, `Epha3`, `Epha4`, `Epha5`, `Epha10`, `Ephb1`, `Ephb2`, and `Ephb4`.
- PubMed literature on Eph/ephrin contact-dependent RTK biology and the sparse direct literature around `EPHA6`.

External mechanism citations:

- Egea and Klein 2007, Trends in Cell Biology, DOI `10.1016/j.tcb.2007.03.004`, PMID `17420126`: Eph/ephrin signaling is membrane-tethered, bidirectional, contact-dependent axon-guidance signaling with Rho-family cytoskeletal outputs.
- Gucciardo, Sugiyama and Lehti 2014, Cellular and Molecular Life Sciences, DOI `10.1007/s00018-014-1633-0`, PMID `24794629`: Eph receptors are the largest RTK family and their outputs are highly context-dependent because they integrate ephrin reverse signaling, clustering, proteolysis, ligand-independent crosstalk, and adhesion.
- Marcelli, Boisset and Schorderet 2014, PLoS One, DOI `10.1371/journal.pone.0100096`, PMID `24945320`: `EPHA6` is an HMX1-regulated retinal developmental target, consistent with an axon-guidance/developmental receptor rather than a known thalamic transcriptional regulator.

## What I computed from the supplied data

I first verified that the manifest contains only `Epha6` and that `Epha6` is absent from the 1,674-row focal-cell training-count table. The focal training distribution is extremely zero-inflated:

- 1,205 / 1,674 training perturbations had `n_degs = 0`.
- 469 / 1,674 had any DEG.
- The median was 0 and the 75th percentile was 1.
- Only 106 / 1,674 had 10 or more DEGs.

I then filtered the parquet to `group_name == "151 TH Prkcd Grin2c Glut"` and queried mechanistic comparators. The key focal-cell Eph-family counts were:

| training target | focal `n_degs` | focal FDR < 0.05 rows |
|---|---:|---|
| `Epha10` | 0 | none |
| `Epha2` | 0 | none |
| `Epha3` | 0 | none |
| `Epha4` | 1 | `Epha4` self only, logFC -1.027, FDR 7.88e-32 |
| `Epha5` | 0 | none |
| `Ephb1` | 0 | none |
| `Ephb2` | 0 | none |
| `Ephb4` | 0 | none |

The actual focal parquet slice for those targets had one significant row total across the eight receptors, and that row was the `Epha4` self-transcript. Thus no represented Eph receptor caused a corrected downstream gene in the held-out cell group.

I also checked represented receptor-tyrosine-kinase, axon-guidance, and proximal cytoskeletal nodes connected to the Eph reports by the corpus:

| related target or boundary | focal `n_degs` | use in the prediction |
|---|---:|---|
| `Cdc42` | 1 | kept as a proximal Eph/Rho cytoskeletal counterexample; self/singleton scale |
| `Rac1` | 0 | kept as a proximal Eph/Rho counterexample |
| `Pak1` | 1 | kept as a Rac/Cdc42-PAK branch counterexample; self/singleton scale |
| `Pak2` | 0 | kept as a Rac/Cdc42-PAK branch counterexample |
| `Pak3` | 0 | kept as a Rac/Cdc42-PAK branch counterexample |
| `Fyn` | 0 | kept as an Eph/NMDAR and RTK-signaling boundary |
| `Mapk1` | 0 | kept as a MAPK boundary |
| `Mapk9` | 0 | kept as a MAPK boundary |
| `Rasa2` | 0 | kept as a RasGAP boundary |
| `Adam10` | 0 | kept as an Eph/ephrin-processing boundary |
| `Pik3r1`, `Pik3r2`, `Pik3cb`, `Sos1` | 0 each | rejected as weaker generic RTK nodes after their zeros agreed with the closer Eph-family zeros |
| `Dcc`, `Robo2`, `Slit2`, `Nrp1`, `Nrp2`, `Plxna1`, `Plxna4`, `Unc5d` | 0 each | kept as axon-guidance receptor counterexamples |
| `Robo1`, `Sema5a`, `Plxna2`, `Unc5c` | 1 each | kept as self-only or singleton-scale axon-guidance counterexamples |
| `Grin2a`, `Grin2b` | 1 and 2 | rejected as NMDAR-channel perturbations rather than EphA paralogs; useful mainly because even the stronger synaptic/NMDAR branch is tiny in this cell at FDR 0.05 |
| `Fbxo11` | 1 | rejected as a graph-neighbor noise/boundary node, not an EphA6 mechanism |

For an unbiased profile audit, I compared each represented Eph receptor against all 1,674 eligible training targets using the focal-cell `logfoldchanges` vector. The direct EphA anchors had no strong or high-count neighbor in this cell group:

- `Epha2` nearest whole-profile neighbors included `Gabrr2`, `Meis2`, `Cnr1`, `Nfib`, and `Il17rd`; their focal counts were 0, 0, 1, 0, and 0.
- `Epha3` nearest neighbors included `Smarcc1`, `Vezf1`, `Prdm2`, `Zfp292`, and `Dpm1`; their counts were 0, 6, 0, 0, and 0.
- `Epha4` nearest neighbors included `Hsd17b4`, `Manba`, `Smarcad1`, `Flnb`, and `Trip11`; all had 0 focal DEGs.
- `Epha5` nearest neighbors included `Slit2`, `Herc2`, `Med13`, `Bach2`, and `Acvr1`; their counts were 0, 0, 11, 0, and 0.
- `Epha10` nearest neighbors included `Gphn`, `Spata7`, `Suclg1`, `Gabrr2`, and `Lrrtm3`; all had 0 focal DEGs.

The weak profile neighbors did not nominate a second high-breadth state for `Epha6`.

## Target-specific reasoning

`Epha6` encodes an A-class Eph receptor. The most relevant training analogs are therefore A-class Eph receptors, followed by B-class Eph receptors and their cytoskeletal/RTK branches.

The direct A-class evidence argues for zero. In the focal cell group, `Epha2`, `Epha3`, `Epha5`, and `Epha10` each had `n_degs = 0`. `Epha4` had `n_degs = 1`, but the only FDR < 0.05 row was its own transcript; after excluding self, it also had no downstream response in `151 TH Prkcd Grin2c Glut`. Because the held-out endpoint includes self rows, `Epha4` leaves open the possibility that `Epha6` could score as exactly 1 by self-depletion. I did not transfer that one self row directly, however, because four of five A-class receptors were zero in the same cell type and the same dataset repeatedly shows that target mRNA loss is a noisy property of the guide/transcript combination rather than a mechanistic Eph response.

The broader Eph family is also flat in the focal cell group. `Ephb1`, `Ephb2`, and `Ephb4` all had `n_degs = 0`. The Distributed Agents corpus reports for `Epha2`, `Epha3`, `Epha4`, `Epha5`, `Epha10`, `Ephb1`, and `Ephb2` further show that the few Eph effects seen elsewhere are receptor-private singletons in other cell groups, not a shared Eph receptor module. The release-level claim states that represented Eph receptor perturbations in postnatal neurons were flat, singleton-only, or non-overlapping rather than one common Eph-family nuclear transcriptomic program. That matters for `Epha6` because a generic family-transfer rule would predict poorly here.

The downstream pathway controls point the same way. Eph/ephrin signaling canonically acts through membrane contact, receptor clustering, Rho-family cytoskeletal remodeling, and sometimes RTK/MAPK or NMDAR crosstalk. But `Cdc42`, `Rac1`, `Pak1`, `Pak2`, `Pak3`, `Fyn`, `Mapk1`, `Mapk9`, `Rasa2`, `Adam10`, `Sos1`, and PI3K subunits were all zero or singletons in the focal endpoint. Axon-guidance receptor comparators such as `Dcc`, `Robo1`, `Robo2`, `Slit2`, `Nrp1`, `Nrp2`, `Sema5a`, `Sema6a`, and `Plxna*` were likewise zero or one. This is the expected behavior for a receptor/cytoskeletal guidance pathway in a postmitotic P16-to-P37/44 snRNA assay: the biology can be real while its first-order readout is adhesion, shape, phosphorylation, or wiring rather than many BH-significant nuclear RNAs.

External literature did not override the within-dataset zeros. The direct `EPHA6` literature I found is developmental retinal regulation and cancer/stem-cell work; I did not find evidence that loss of EphA6 in juvenile thalamic glutamatergic neurons uniquely triggers a broad activity, stress, or fate transcriptional program. The Eph/ephrin reviews support a local contact-dependent, bidirectional, cytoskeletal signaling prior, which makes `Epha6` more like `Epha4`/`Epha5`/Rho-PAK controls than like broad chromatin, proteasome, or splicing perturbations in the training set.

## Prediction

I predict `0` DEGs for `Epha6` in `151 TH Prkcd Grin2c Glut`.

Mechanistically, this is strongest as a prediction of no corrected downstream program. The self-transcript contribution is the weaker part of the zero/nonzero decision: `Epha6` is a measured gene in the focal DE universe and could in principle score a self row if its transcript were sufficiently depleted. Still, the nearest empirical A-class receptors put the focal self-plus-downstream endpoint at 0, 0, 0, 1, and 0, and the lone `1` is not a family-shared signature. The calibrated point prediction is therefore zero rather than a one-gene self-only effect.

## Limits

- `Epha6` itself was completely held out as a perturbation, so no within-dataset guide-level indel, self-knockdown, or expression signature exists.
- The closest represented paralogs are other EphA receptors, but `Epha7` was not available as a training perturbation and Eph receptors can have ligand-, region-, and subclass-specific phenotypes.
- The assay cannot measure EphA6 phosphorylation, receptor clustering, growth-cone collapse, spine structure, axon pathfinding, or ephrin reverse signaling.
- The perturbation begins at P16 in sparse postmitotic neurons; strong embryonic or retinal EphA6 wiring biology could already be over, diluted across mature thalamic subclasses, or expressed as anatomy rather than a nuclear RNA state.
- The point prediction is an assay-calibrated integer under FDR 0.05, not a claim that EphA6 has no neuronal function.
