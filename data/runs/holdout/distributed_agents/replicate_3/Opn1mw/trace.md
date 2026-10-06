# DEG-count prediction for `151 TH Prkcd Grin2c Glut`

## Question and scope

I interpreted the task as predicting the held-out endpoint `n_degs` for each target
listed in `163_Opn1mw.csv`, where `n_degs` is the number of measured genes in
`151 TH Prkcd Grin2c Glut` cells with Wilcoxon Benjamini-Hochberg adjusted
`pvals_adj < 0.05`.  The manifest contains one target:

| target_name |
| --- |
| Opn1mw |

I treated the endpoint as an assay-, cell-type-, and power-dependent count, not
as a generic estimate of gene essentiality or importance.  The prediction is for
acute mosaic P16 AAV-CRISPR loss of function in NeuN+ postnatal brain nuclei;
retina, olfactory bulb, hindbrain, and non-neuronal tissues are outside the
measured population.

## Sources used

- Input manifest:
  `[local file: 163_Opn1mw.csv]`.
- Training endpoint table:
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
- Differential-expression parquet:
  `[local file: training_de_all_cell_groups.parquet]`.
- Distributed Agents same-experiment corpus, release
  `perturbai-july-260713-sourceguard-1773-v1`, searched for retinal,
  photoreceptor, and ciliary perturbation claims.
- Distributed Agents runtime `profile_neighbors`, used to compare retinal/photoreceptor
  training signatures in the focal cell group.
- External literature from PubMed:
  - Fujieda et al. 2008, DOI `10.1111/j.1471-4159.2008.05739.x`, PMID
    `19014374`.
  - Daniele et al. 2011, DOI `10.1016/j.visres.2010.12.017`, PMID `21219924`.
  - Merbs et al. 2012, DOI `10.1371/journal.pone.0032602`, PMID `22403679`.
  - Aavani et al. 2017, DOI `10.1016/j.gep.2017.03.001`, PMID `28288836`.
  - Ma et al. 2022, DOI `10.1089/hum.2021.298`, PMID `35272502`.

## Dataset checks and calibration

I first verified that `Opn1mw` appears exactly once in the held-out manifest and
is absent from the training count CSV, so no observed held-out `n_degs` was
available to leak into the prediction.

The focal training count CSV contained 1,674 non-held-out targets.  Its response
distribution was heavily concentrated at zero:

| statistic | value |
| --- | ---: |
| targets | 1,674 |
| targets with 0 DEGs | 1,205 |
| median `n_degs` | 0 |
| 75th percentile | 1 |
| 90th percentile | 2 |
| 95th percentile | 18 |
| maximum | 2,677 |

This establishes that zero-DEG calls are routine in this cell group, while the
rare broad responses are driven by targets with strong neuronal regulatory,
protein-homeostasis, or RNA-processing phenotypes.

I then filtered the DE parquet to `group_name == "151 TH Prkcd Grin2c Glut"` and
to photoreceptor, retinal, and phototransduction-related training targets.  For
each target I counted rows with `pvals_adj < 0.05` and compared those counts to
the endpoint CSV.

| training target | focal `n_degs` | pattern in the DE parquet | interpretation for `Opn1mw` |
| --- | ---: | --- | --- |
| `Opn1sw` | 0 | no FDR-significant genes among 17,259 measured genes; best unadjusted hits were unrelated low-rank genes such as `Ccdc28b`, `Ppil2`, and `R3hdm1` | closest in-dataset analog: the other mouse cone opsin did not create a thalamic neuronal state |
| `Rho` | 0 | no FDR-significant genes; lowest adjusted p-value was 0.661 | rod visual opsin, useful as a terminal photopigment countercheck |
| `Crx` | 0 | no FDR-significant genes; lowest adjusted p-value was 1.0 | photoreceptor transcription factor upstream of opsin programs did not elicit a retina-like program |
| `Gucy2e` | 0 | no FDR-significant genes despite 383 matched perturbed nuclei | retinal phototransduction effector, much more directly signaling-associated than `Opn1mw`, was flat in this brain cell type |
| `Nr2e3`, `Rorb`, `Rxrg`, `Thrb` | 0, 0, 0, 0 | no FDR-significant genes for any of these retinal-lineage or photoreceptor-associated factors in the focal group | loss of represented upstream retinal regulators was silent in this assay context |
| `Cep290`, `Iqcb1`, `Rpgr`, `Rpgrip1l`, `Spata7` | all 0 | flat focal DEG counts | retinal/ciliopathy genes did not form a shared brain-neuron transcriptional phenocopy |
| `Arl3` | 1 | the only FDR-significant row was `Arl3` itself | an on-target RNA decrease, not a propagated photoreceptor response |
| `Rora` | 278 | broad neuronal transcriptional response | counterexample; ROR-alpha regulates cone genes in retina, but is also a broad neuronal nuclear receptor, so its focal phenotype is not transferable to a terminal opsin |

A second DE-parquet check asked whether canonical phototransduction transcripts
were ever significantly altered in the focal group by any training perturbation.
`Opn1mw` itself was a measured row for every one of the 1,674 training targets
and never reached FDR 0.05; its best adjusted p-value was 0.83595.  The same
was true for measured `Opn1sw`, `Rho`, `Gnat1`, `Gnat2`, `Gucy2e`, `Pde6b`,
`Pde6c`, `Cnga3`, `Cngb3`, `Arr3`, `Crx`, `Nrl`, and `Nr2e3`, all of which had
minimum adjusted p-values above 0.05 across the training set.  Thus the focal
cell group did not show an inducible cone/rod phototransduction RNA module.

The Distributed Agents same-experiment corpus independently matched this view.  A
moderate-confidence claim for `Crx` and `Opn1sw` states that represented
photoreceptor-lineage perturbations fail to produce a shared photoreceptor-like
transcriptional program in the assayed postnatal brain-neuron groups.  A second
retinal/ciliary-gate claim spanning `Arl3`, `Cep290`, `Iqcb1`, `Rpgr`,
`Rpgrip1l`, and `Spata7` states that represented retinal/ciliary-gate disease
relationships were not reflected as shared basal transcriptomic phenocopies in
postnatal NeuN+ brain neurons.

I also ran Distributed Agents `profile_neighbors` on the focal log-fold-change profiles
for `Opn1sw`, `Rho`, `Crx`, and `Gucy2e`, with the retinal/ciliary targets above
as the eligible universe.  The returned topology consisted mostly of weak
tail-overlap and whole-profile similarities among profiles that had zero
adjusted hits.  I therefore interpreted the shared structure as a consequence
of very flat signatures rather than as an active photoreceptor module.

## Target-specific reasoning

### `Opn1mw`

`Opn1mw` encodes the mouse middle-wavelength-sensitive cone opsin, a
photopigment of retinal cone photoreceptors.  Mouse cones express the
short-wave opsin `Opn1sw` and the middle-wave opsin `Opn1mw` in retinal
counter-gradients (Daniele et al. 2011), and Opn1mw/Opn1sw expression is part
of the postnatal photoreceptor differentiation program rather than a generic
brain-neuron program (Aavani et al. 2017).  The locus behaves like a
retina-specific photoreceptor gene with cell-type-restricted epigenetic
regulation (Merbs et al. 2012).  Retinal ROR-alpha and CRX can regulate cone
opsin transcription in the mouse retina (Fujieda et al. 2008), and germline
retinal `Opn1mw`/`Opn1sw` loss affects cone structure and visual function
(Ma et al. 2022), but those phenotypes occur in cone outer segments, not in
thalamic glutamatergic neurons.

The most appropriate in-dataset comparator is `Opn1sw`: it is the paralogous
cone opsin and had 0 DEGs in `151 TH Prkcd Grin2c Glut`.  `Rho`, a rod opsin,
also had 0 DEGs.  Stronger upstream or pathway perturbations that should have
been more capable of exposing a photoreceptor program if one existed in these
cells, including `Crx`, `Rorb`, `Rxrg`, `Thrb`, `Nr2e3`, and `Gucy2e`, likewise
had 0 DEGs.  The retinal/ciliary genes were flat except for `Arl3`, where the
single significant feature was the targeted transcript itself.  `Rora` is not a
good analog despite its retinal role, because it has broad neuronal nuclear
receptor functions and was the only member of this comparison set to show a
large focal transcriptional phenotype.

I therefore predict that acute sparse `Opn1mw` loss will be transcriptionally
silent at the FDR 0.05 threshold in the focal thalamic cell group.

Prediction: `0` DEGs.

## Limits and caveats

- The held-out `Opn1mw` perturbation has no observed focal signature in the
  supplied files, so the prediction is an extrapolation from `Opn1sw`, `Rho`,
  retinal regulators, and retinal/ciliary genes that were assayed.
- The endpoint is a nuclear RNA count.  A zero prediction means no genes are
  expected to pass this particular Wilcoxon/BH threshold; it does not prove that
  the edited cells have no protein-level or rare-cell effect.
- The training perturbations use modest acute AAV-CRISPR knockdown in juvenile
  brain.  Germline retinal double-knockout phenotypes, subretinal AAV rescue
  phenotypes, and mature cone outer-segment biology are informative for gene
  function but imperfect transfer evidence for the focal brain cell type.
- `Opn1mw` was detectable as a measured feature in the DE tables, but the DE
  parquet does not by itself establish high expression or productive editing in
  `151 TH Prkcd Grin2c Glut`.
