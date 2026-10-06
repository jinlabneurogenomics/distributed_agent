# Gpr12 direct DEG-count forecast

Target and endpoint:

- Target: `Gpr12`, the only row in `[local file: Gpr12.csv]`.
- Endpoint: `n_degs` in `151 TH Prkcd Grin2c Glut`, counted as measured genes with BH-adjusted Wilcoxon `p < 0.05`.
- Declared measurement inputs used: the focal-class training counts in `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`, the declared training DE parquet `[local file: training_de_all_cell_groups.parquet]`, and the target-only biology bundle `[local file: Gpr12.json]`.

Evidence that determined the number:

- `Gpr12` is expressed in the focal non-target nuclei rather than being absent from this population: `77.524%` of `151 TH Prkcd Grin2c Glut` non-target nuclei express it, with mean `1.134` CP10K and pseudobulk `113.799` CPM in the exact target-measurement card.
- The curated target biology supports a plausible postmitotic thalamic role but leaves within-window functional loss unresolved. GPR12 is a constitutively active Gs-coupled membrane receptor; adult mediodorsal-thalamus AAV RNAi caused a functional phenotype, but the supporting protein reduction was assayed at an eight-week histology point and no GPR12 clearance curve or half-life establishes depletion by the P37-P44 harvest after P16 editing.
- The focal count table is zero-heavy even in this high-yield class: among 1,674 training targets, 1,205 have `n_degs = 0`, 276 have `n_degs = 1`, and the 75th percentile is 1 DEG.
- Curated GPCR/cAMP perturbations in the same count table are much quieter than the whole-table right tail:
  - `functional_class=gpcr`: 95 training targets, median `0`, mean `0.11`, 10 nonzero, maximum `1`.
  - `GO:0007189`, adenylate-cyclase-activating GPCR signaling: 35 training targets, median `0`, mean `0.11`, 4 nonzero, maximum `1`.
  - `GO:0007186`, GPCR signaling: 114 training targets, median `0`, mean `0.11`, 12 nonzero, maximum `1`.
  - `WP_GPCRS_CLASS_A_RHODOPSINLIKE`: 49 training targets, median `0`, mean `0.04`, 2 nonzero, maximum `1`.
- Directly inspected focal-class count labels for nearby receptor/Gs/cAMP nodes were similarly sparse: `Gnas`, `Adcy1`, `Adcy3`, and `Adcy5` were `0`; `Prkaca`, `Prkar1a`, `Gpr158`, and `Gprasp2` were `1`; and only the nuclear transcriptional node `Creb1` rose to `10`.
- The declared DE parquet showed that the one-DEG calls in this small receptor/cAMP group can be self-transcript singleton profiles rather than broad downstream programs: `Gpr158`, `Gprasp2`, `Prkaca`, and `Prkar1a` each had a significant focal self-target row and `n_degs = 1`.
- A symmetric profile comparison over `Adcy1`, `Adcy3`, `Adcy5`, `Creb1`, `Gnas`, `Gpr156`, `Gpr158`, `Gpr161`, `Gpr179`, `Gpr45`, `Gprasp2`, `Gprc5b`, `Prkaca`, and `Prkar1a` found 9/14 nodes with no FDR-0.05 features, 4/14 with 1-9 features, and one modest 10-49-feature node. The cohort diagnostic was cohesive mainly as a weak or near-null signed DE surface, not as a recurrent high-response GPCR module.
- Same-experiment corpus context for `Gnas` reinforced the direct table evidence without adding independent replication: `Gnas:F003` reports nonconvergence of Gnas with Gnal, Adcy5, Pde10a, PKA, Epac, and CREB-axis perturbations, and the associated Claim states that represented dopamine/GPCR and cAMP-pathway perturbations do not collapse into one durable basal neuronal mRNA module in this assay.

Synthesis:

The upward evidence is real but small: `Gpr12` has focal expression reach and an adult thalamic loss phenotype, so it is not in the same category as a completely absent receptor. The exact profile scale from biologically adjacent training perturbations is nevertheless a singleton scale: Gs, adenylate cyclases, PKA subunits, and GPCRs in the focal class are overwhelmingly `0` or `1`, and their observed DE profiles do not expose a multi-gene basal cAMP module. The target card's unresolved 21-28 day receptor clearance and possible spatial dilution inside the aggregated thalamic class further argue against borrowing the `Creb1` or unrelated chromatin/proteostasis tail. Because `Gpr12` is well detected in the focal nuclei, I placed it at the top of the local GPCR/proximal-signaling range and predicted one significant gene, most plausibly a self-transcript or trace singleton rather than a broad downstream response.

Predicted `n_degs`: `1`
