# Direct forecast trace

Target and endpoint:

- Target: `Actb`, from the one-row `Actb.csv` holdout manifest.
- Population: `151 TH Prkcd Grin2c Glut`.
- Endpoint: `n_degs`, the number of measured genes with BH-adjusted Wilcoxon `p < 0.05`.

Allowed biology-only Actb bundle:

- The bundle did not expose the target outcome or labeled neighbor outcomes.
- In the requested focal population, the exact in-assay Actb expression feature is unavailable: `feature_available=false`, `feature_status=not_in_expression_matrix`, while the perturbation contrast itself is available. This means an Actb self-transcript change cannot contribute to `n_degs`.
- The functional-stock card argues that a disruptive Actb edit should stop new beta-actin synthesis and that beta-actin-specific stock is likely substantially depleted within the 21-28 day P16-to-P37/P44 window.
- That loss is buffered: direct CNS Actb knockout evidence reports increased gamma-actin/other isoactin compensation and largely preserved total actin, with incomplete but real residual phenotype.
- The strongest neural phenotype evidence is developmental Nestin-Cre CNS deletion, not a P16 thalamic neuron loss-of-function experiment. The postnatal endpoint coupling and the fraction of the aggregated thalamic population that would mount a visible response therefore remain unresolved.

Training count table:

- The matched `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` table contains 1,674 observed training perturbations.
- The distribution is extremely sparse: median `n_degs=0`; 1,205/1,674 rows are zero; 276/1,674 have exactly one DEG; only 193/1,674 have at least two DEGs.
- High responses exist in this class, but they are outliers: the mean is 14.05 because of a small upper tail, while the 75th percentile is 1 DEG.

Task-matched training perturbations from the Parquet:

- The Actb bundle specifically names `Actg1` as the compensating cytoplasmic actin isoform. `Actg1` is an observed training target in the requested class with `n_degs=1`.
- Querying the declared training Parquet for `Actg1` in `151 TH Prkcd Grin2c Glut` showed 17,259 measured rows, 227 matched perturbed nuclei, and exactly one BH-significant feature: `Actg1` itself (`logfoldchanges=-0.824166`, `pvals_adj=9.85e-16`). There were no significant downstream measured genes.
- Weaker cytoskeletal comparators were also quiet in the same Parquet context: `Actn4` had 0 significant rows with 199 matched perturbed nuclei, and `Cfl2` had 0 significant rows with 112 matched perturbed nuclei.
- A manual intersection of common actin-regulatory genes with the count table found only a few present targets in this training slice: `Actg1=1`, `Actn4=0`, `Cfl2=0`, `Cdc42=1`, and `Rac1=0`.

Observed-profile context:

- A `profile_neighbors` scan used `Actg1`, `Actn4`, and `Cfl2` as anchors, all constrained to `151 TH Prkcd Grin2c Glut`, against the 1,674 eligible training targets.
- For `Actg1`, the best whole-profile neighbors were only moderately related (`Vezf1`, `Kat6a`, `Lamp2`, `Adar`, `Rapgef4`; Pearson about 0.703-0.708). Positive top-200 overlap never exceeded 14%, and negative top-200 overlap never exceeded 30.5%.
- The top whole-profile and signed-tail neighbors of `Actg1` were themselves almost all zero/one-count perturbations in the count table: for example, the main whole-profile neighbors were `Vezf1=6`, `Kat6a=0`, `Lamp2=0`, `Adar=0`, `Rapgef4=0`, `Trip11=0`, and `Dennd5a=0`.
- Thus the measured profile neighborhood around the best actin-family anchor looked like sparse background variation, not a coherent high-DEG response state.

Synthesis:

- The strongest matched quantitative datum is `Actg1`, which produced only a self-transcript DEG and no downstream program. Actb itself is not a measured feature, so the direct self-DEG route available to `Actg1` is absent for the held-out target.
- Actb loss should be biologically realized by harvest, but isoactin compensation, survivor conditioning, the developmental/non-thalamic nature of the phenotype evidence, and the lack of a matched high-response cytoskeletal cohort all push against projecting a broad transcriptional footprint.
- I therefore forecast that Actb will behave like a buffered cytoskeletal perturbation with no BH-significant downstream genes in the aggregated thalamic survivor population.

Point forecast:

- `predicted_n_degs = 0`
