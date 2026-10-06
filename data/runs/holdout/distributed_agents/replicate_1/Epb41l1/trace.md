# Reasoning trace

## Question and endpoint

I predicted the held-out `n_degs` value for `Epb41l1` in `151 TH Prkcd Grin2c Glut` cells.  I treated `n_degs` exactly as the task defined it: the number of measured genes with Benjamini-Hochberg-adjusted Wilcoxon `pvals_adj < 0.05` for the acute AAV CRISPR loss-of-function perturbation in the focal thalamic glutamatergic class.  The requested target list contained one unranked target, `Epb41l1`; it was absent from the focal training-count CSV and had zero `gene_target='Epb41l1'` rows in the supplied training parquet, so its own held-out signature was not used.

I resolved the main ambiguity as whether a self-transcript-only effect should count.  The supplied `n_degs` endpoint counts any measured gene crossing FDR 0.05, including the perturbed transcript when it is detected, but measured target-mRNA loss is not an editing-efficiency or downstream-effect score in this atlas.  I therefore used self-transcript events in analogs only to calibrate whether a one-gene count is plausible, not as evidence for a broad biological transcriptional program.

## Sources used

- Declared Perturb-seq DE parquet: `training differential-expression dataset`.
- Declared focal training DEG counts: `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
- Declared requested-target CSV: `single-target request for Epb41l1`.
- Run-local task metadata: `task_bindings.json`, `coverage.json`, `measurement_registry.json`, and the PerturbAI atlas v5 dataset portrait.
- Same-experiment July 260713 sourceguard 1773 v1 BioKG/corpus: I queried `Epb41l1` as a target and found no packaged target-comparator Findings for it, so corpus topology did not order or score this prediction.
- External mechanism literature from PubMed:
  - Peters et al. 1998, `10.1006/geno.1998.5537`, established conserved vertebrate protein 4.1 paralogs and the mouse `Epb41l1`/4.1N identity.
  - Biederer and Sudhof 2001, `10.1074/jbc.M105287200`, showed that CASK binds a brain-enriched protein 4.1 isoform and can assemble actin/spectrin structure at neurexin cytoplasmic tails.
  - Maximov et al. 2003, `10.1016/s1044-7431(02)00027-1`, mapped an interaction between neuronal 4.1N and the type-1 IP3 receptor in synaptic preparations.
  - Baines et al. 2013, `10.1016/j.bbamem.2013.05.030`, reviewed 4.1 proteins as membrane-protein organization hubs overlapping with ankyrin and spectrin-based scaffolds.
  - Wang et al. 2020, `10.1038/s41598-020-73795-6`, reported partial lethality and hypothalamus/pituitary/reproductive phenotypes in constitutive 4.1N-null mice.
  - Pushkin et al. 2023, `10.1523/JNEUROSCI.0185-23.2023`, found that reducing 4.1N reduces glutamatergic synapse function in rat dentate granule neurons but not CA1 pyramidal neurons.
  - Bonnet et al. 2023, `10.7554/eLife.85609`, placed 4.1N in GluA1 AMPA-receptor intracellular transport and export.

## Computations

I used the training count CSV to inspect the focal `n_degs` values for protein 4.1/cortical membrane cytoskeleton, ankyrin/spectrin, and postsynaptic/neurexin-neuroligin genes that had been assayed as non-held-out perturbations.  I then queried the full parquet only within `group_name='151 TH Prkcd Grin2c Glut'` for those targets to count FDR 0.05 and FDR 0.10 rows and list the significant measured genes.

The count distribution in the focal training CSV was sparse: 1,205 of 1,674 training targets had `n_degs=0`; 1,512 of 1,674 were between 0 and 2 DEGs.  The high-count end was dominated by genes such as `Uba5` at 2,677, `Tpr` at 1,768, `Sin3a` at 1,433, spliceosomal/RNA-processing factors, proteasome factors, chromatin regulators, and other core regulators, not by synaptic membrane-cytoskeleton adaptors.

Relevant focal training perturbations:

| Training perturbations | Observed `n_degs` in `151 TH Prkcd Grin2c Glut` | Focal expression-pattern evidence |
| --- | ---: | --- |
| `Dlg4`, `Caskin1`, `Nrxn1`, `Sptan1`, `Rdx` | 1, 1, 1, 1, 1 | Each had only its own transcript as an FDR 0.05 DEG in the focal parquet: `Dlg4` log2FC -0.44, `Caskin1` -0.56, `Nrxn1` -0.52, `Sptan1` -0.53, `Rdx` -0.61. |
| `Dlgap4`, `Shank3` | 2, 2 | Small non-self tails rather than broad states: `Dlgap4` had self plus `Vgf` at FDR 0.05 and a few FDR 0.10 rows; `Shank3` had self plus `Uba5`. |
| `Shank2`, `Bsn`, `Syngap1`, `Tanc2`, `Tspoap1` | all 0 | Postsynaptic/scaffold counterexamples with no focal FDR 0.05 genes. |
| `Add1`, `Add2`, `Add3`, `Ank1`, `Ank2`, `Sptb` | all 0 | Membrane-cytoskeleton and spectrin-linkage counterexamples; these are the closest training measurements to a protein 4.1 structural role and produced no focal DEGs. |
| `Actg1`, `Ank`, `Sptan1`, `Rdx` | all 1 | Actin/spectrin/membrane-associated perturbations with only single-gene signals. |
| `Gria1`, `Gria2`, `Gria3`, `Grik1`, `Grik3`, `Grik4`, `Grm8`, `Itpr1`, `Chrna7`, `Slc12a2` | 0 except `Grik5` and `Grm7` at 1 | Candidate membrane proteins or pathways connected to 4.1N in the literature were essentially null when directly perturbed. `Cask`, `Slc12a5`, `Ip6k2`, `Gria4`, and `Grik2` were not training targets in the focal count CSV. |
| `Camk2a`, `Camk2b`, `Camk2g`, `Calm1`, `Calm2`, `Calm3`, `Ywhae`, `Ywhag`, `Ywhaz` | mostly 0 or 1; `Calm1` was 14 | Calcium/calmodulin and 14-3-3 interactors were checked as broad signaling counterexamples. Only `Calm1` gave a modest multi-gene footprint, which I did not transfer to `Epb41l1` because calmodulin is a generic calcium sensor rather than an obligate 4.1N effector. |

## Target-specific prediction

### `Epb41l1`

`Epb41l1` encodes neuronal protein 4.1N, a FERM/spectrin-actin/C-terminal domain adaptor that links selected receptors and channels to cortical actin and spectrin.  The external literature supports a local synaptic and membrane-trafficking role: protein 4.1 proteins form a conserved family that organizes membrane proteins (Peters et al. 1998; Baines et al. 2013); 4.1N can connect with CASK/neurexin, IP3R1, and AMPA receptor trafficking machinery (Biederer and Sudhof 2001; Maximov et al. 2003; Bonnet et al. 2023); and 4.1N loss can have neuronal consequences that are strongly cell-type-dependent (Pushkin et al. 2023).  Constitutive mouse 4.1N loss has systemic developmental phenotypes (Wang et al. 2020), but those are weaker priors for the present experiment because this screen is sparse, postnatal, acute, neuronal CRISPR loss-of-function and reads out surviving nuclei rather than embryonic development or endocrine organ structure.

The within-dataset analogs point to a very small focal response.  Perturbing the spectrin/ankyrin/adducin membrane skeleton around a 4.1 protein did not yield broad transcriptional changes: `Add1`, `Add2`, `Add3`, `Ank1`, `Ank2`, and `Sptb` each had 0 DEGs, while `Sptan1` and `Rdx` each had one self-transcript DEG.  Postsynaptic scaffolds and neurexin-neuroligin-associated genes also sat on the zero/one boundary: `Dlg4`, `Nrxn1`, and `Caskin1` had one DEG each, `Dlgap4` and `Shank3` had two each, and `Shank2`, `Bsn`, `Syngap1`, `Tanc2`, and `Tspoap1` were 0.  Directly assayed receptor or calcium-signaling partners mentioned in the 4.1N literature, including `Gria1`, `Itpr1`, `Chrna7`, `Grm8`, and `Slc12a2`, were also 0; the AMPAR, IP3R1, and neurexin mechanisms therefore look more like local channel/receptor localization than the sort of nuclear stress or fate-like program that created hundreds of DEGs for `Uba5`, `Sin3a`, `U2af2`, `Psmb4`, or `Cic`.

My causal model for transfer is: acute `Epb41l1` editing should reduce 4.1N protein in some exposed thalamic glutamatergic neurons; the most direct molecular consequence is weaker anchoring or trafficking of a subset of synaptic membrane proteins through 4.1N's FERM and C-terminal interactions; downstream effects are expected at receptor localization, AMPA/IP3R/calcium signaling, and cortical actin-spectrin organization; cells that survive and retain the `151 TH Prkcd Grin2c Glut` class are sampled for nuclear RNA after 3 to 4 weeks.  The same direction of endpoint transfer is strong for genes that impair the same membrane-cytoskeleton or synaptic scaffold function, and those genes are empirically null or self-only in the training data.  Broad pathway co-membership with calcium signaling is too generic, and constitutive reproductive or survival phenotypes do not establish a matching thalamic nuclear DE signature.

I therefore predict no appreciable downstream transcriptional footprint and place the count at the self-only boundary.  Because many close scaffold analogs had exactly one focal DEG corresponding to the edited transcript itself, the point estimate is `1` rather than a high single-digit or larger response.

## Limits

The prediction is an extrapolation from related cytoskeletal and synaptic perturbations; neither `Epb41l1`, its closest paralogs `Epb41l2`/`Epb41l3`, nor the direct interactor `Cask` were present as training `gene_target` values in the focal count CSV.  The training analogs show that this biological neighborhood is usually quiet at FDR 0.05, but they cannot tell whether the held-out `Epb41l1` guide pool will make the `Epb41l1` transcript itself significant.  Published 4.1N mechanisms come mostly from hippocampal, cerebellar, epithelial, biochemical, or constitutive-null contexts; they support membrane-synapse function, not a calibrated DEG count in postnatal thalamic glutamatergic neurons.  Finally, absence of a large recovered-cell expression state would not rule out changes in synaptic physiology, receptor trafficking, or earlier selection effects that the declared `n_degs` endpoint does not directly observe.
