# Reasoning trace

## Question and resolved ambiguities

The requested held-out perturbation set contains one target, `Dcx`, and the
quantity to predict is the integer number of measured genes with
`pvals_adj < 0.05` in `151 TH Prkcd Grin2c Glut` nuclei after the held-out gene
was perturbed. `TH` was interpreted using the dataset portrait as thalamus, not
tyrosine hydroxylase, so the focal group is a mature thalamic glutamatergic
class marked by `Prkcd` and `Grin2c`.

I treated `n_degs` as the same thresholded endpoint in
`151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`; it includes the target
transcript when the self-transcript is significant, as seen for `Map1b`,
`Stmn2`, `Kif5a`, `Kif5c`, `Tuba1a`, and `Tuba4a`. I did not use weak
self-target knockdown as a proxy for editing efficiency, because the PerturbAI
dataset notes that transcript loss is not correlated with downstream response
in this CRISPR design.

## Sources used

- The supplied training-count endpoint:
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
- The supplied per-gene DE parquet:
  `[local file: training_de_all_cell_groups.parquet]`.
- The requested-target manifest:
  `[local file: 052_Dcx.csv]`.
- The run-local PerturbAI atlas v5 dataset portrait in
  `codex_runtime/pipeline/dataset_context.md`.
- The Distributed Agents same-experiment semantic corpus,
  `perturbai-july-260713-sourceguard-1773-v1`; notably `Dcx` itself was absent
  from this filtered corpus, while related training targets such as `Map1b`,
  `Map6`, `Tuba1a`, `Dpysl5`, and `Dst` had curated same-experiment findings.
- PubMed-indexed literature on DCX biology and the DCX/DCLK family:
  des Portes et al. 1998, Cell, doi:10.1016/S0092-8674(00)80898-3,
  PMID:9489699; Gleeson et al. 1998, Cell,
  doi:10.1016/S0092-8674(00)80899-5, PMID:9489700; Francis et al. 1999,
  Neuron, doi:10.1016/S0896-6273(00)80777-1, PMID:10399932; Gleeson et al.
  1999, Neuron, doi:10.1016/S0896-6273(00)80778-3, PMID:10399933; Brown et al.
  2003, J Comp Neurol, doi:10.1002/cne.10874, PMID:14574675;
  Couillard-Despres et al. 2005, Eur J Neurosci,
  doi:10.1111/j.1460-9568.2004.03813.x, PMID:15654838; Deuel et al. 2006,
  Neuron, doi:10.1016/j.neuron.2005.10.038, PMID:16387638; Koizumi et al.
  2006, Neuron, doi:10.1016/j.neuron.2005.10.040, PMID:16387639; Tanaka et al.
  2006, Cereb Cortex, doi:10.1093/cercor/bhk005, PMID:16766710.

## Dataset computations

1. Parsed `052_Dcx.csv` and confirmed the only requested target was `Dcx`.
2. Loaded the 1,674 focal-cell training counts. The endpoint was extremely
   zero-inflated: 1,205/1,674 training perturbations had `n_degs = 0`,
   1,481/1,674 had `n_degs <= 1`, 1,512/1,674 had `n_degs <= 2`, and only
   58/1,674 exceeded 50 DEGs.
3. Queried the parquet for
   `group_name == "151 TH Prkcd Grin2c Glut"` and candidate `gene_target`
   values from DCX-neighbor biology: structural and microtubule-associated
   genes, tubulin genes, kinesin/dynactin genes, Reelin/migration genes, and
   semaphorin/CRMP pathway genes. For each, I inspected the exact significant
   rows at FDR 0.05 and joined those observations to the training `n_degs`.
4. Queried `names == "Dcx"` in the focal class across all 1,674 training
   perturbations. `Dcx` itself was significantly changed only by broad
   high-response perturbations `Qrich1` and `Rora`; the nearby cytoskeletal and
   migration perturbations did not form a `Dcx`-regulating module.
5. Ran a run-local `profile_compare`/`profile_cohort` over a 14-target analog
   cohort (`Map1b`, `Map6`, `Tuba1a`, `Stmn2`, `Dctn1`, `Kif2a`, `Kif5a`,
   `Kif5c`, `Tuba4a`, `Reln`, `Dab1`, `Vldlr`, `Nrp1`, `Arx`) using focal
   Wilcoxon `scores`, `pvals_adj`, and all measured genes. Seven of the
   fourteen analogs had no significant feature, six had only 1-9, only `Dctn1`
   had at least 50, and pairwise whole-profile Pearson/cosine similarities
   were near zero with no FDR-level shared program.

## Target-specific reasoning: Dcx

`Dcx` encodes Doublecortin, a neuronal doublecortin-domain microtubule-binding
protein. Human loss-of-function mutations cause X-linked lissencephaly and
subcortical band heterotopia by disturbing neuronal migration during cortical
development, and the protein binds and stabilizes microtubules in migrating
neurons (des Portes 1998; Gleeson 1998; Francis 1999; Gleeson 1999). In mouse,
single `Dcx` loss is partly buffered by the related doublecortin-like kinase
family: `Dcx/Dclk1` double mutants have severe hippocampal, cortical layering,
commissural, and axon-outgrowth defects, while single mutants are much milder
in several structures (Deuel 2006; Koizumi 2006; Tanaka 2006). Adult and
postnatal `Dcx` expression is best established in newly generated neuroblasts
of the dentate gyrus and SVZ/rostral migratory stream, with expression falling
as neurons mature (Brown 2003; Couillard-Despres 2005). Those facts make `Dcx`
an early wiring/cytoskeletal target whose canonical readouts are migration,
axon growth, and microtubule organization rather than a constitutive nuclear
RNA regulator of already specified thalamic relay neurons.

The nearest direct paralogs, `Dclk1` and `Dclk2`, were not present as training
perturbations, so the prediction had to use less perfect pathway analogs. The
most relevant structural microtubule and neuronal MAP perturbations were
silent or self-only in the focal class:

| training perturbation | focal `n_degs` | focal expression-pattern evidence | relevance for `Dcx` |
| --- | ---: | --- | --- |
| `Map1b` | 1 | only `Map1b` itself crossed FDR 0.05; Distributed Agents `Map1b:F001-F006` report a self-only, nonconvergent surface and no MAP/tubulin compensation module | MAP1B is a neuronal microtubule-associated protein tied to axon growth and migration; its flatness supports buffering of structural MAP loss at the nuclear RNA level |
| `Map6` | 0 | no focal FDR genes; Distributed Agents `Map6:F001-F005` report a complete downstream null across all recovered neuronal groups and no phenocopy of microtubule-track or motor perturbations | another structural microtubule-stabilizing MAP with strong non-RNA synaptic literature but no postnatal snRNA response |
| `Mapt`, `Map1lc3a`, `Mapre2` | 1, 1, 1 | each had only a singleton in the focal count table; the Map1b/Map6/Mapre2/Mapt corpus findings describe near-zero correlations among MAP/EB-family comparators | family membership alone did not generate a common MAP loss transcriptome |
| `Stmn2` | 1 | only `Stmn2` itself was significant; `Dcx`, `Dclk1`, `Dclk2`, `Map1b`, `Map6`, and `Reln` were all FDR-negative downstream | a growth-cone and microtubule-dynamics gene gave a self-only state, not a DCX-like developmental program |
| `Kif2a`, `Kif5a`, `Kif5c`, `Kif1a` | 0, 1, 1, 1 | `Kif5a` and `Kif5c` were self-only; `Kif2a` was zero | microtubule motors did not evoke a shared migration/transport nuclear state |
| `Tuba1a`, `Tuba4a`, `Tubb4b`, `Tubb5` | 7, 2, 1, 1 | `Tuba1a` was a narrow tubulin-isotype dosage-compensation exception; it up-regulated `Tubb3`, `Tubb2a`, `Tuba4a`, `Tubb4a`, `Tubb4b`, and `Tubb5` after `Tuba1a` transcript loss | shows the assay can see a tubulin response, but the response is specific to loss of a core alpha-tubulin isotype and not copied by MAP perturbations |
| `Dctn1` | 75 | clear induction of a sterol/SREBP-like program (`Insig1`, `Msmo1`, `Hmgcs1`, `Cyp51`, `Hmgcr`, `Fdft1`, `Fasn`, `Sqle`, `Ldlr`, and others) | the main counterexample: cytoskeletal trafficking disruption can be visible in this class, but its lipid-response program is not a plausible DCX phenotype |

The developmental migration pathways adjacent to DCX also pointed toward a
zero. `Reln`, `Dab1`, `Vldlr`, `Nrp1`, `Nrp2`, `Sema4d`, `Sema5a`, `Sema6a`,
`Plxna1`, `Plxna2`, `Plxna4`, `Plxnd1`, and `Dpysl5` were all represented by
zero- or one-DEG focal counts except `Gsk3b` with 6. Distributed Agents `Dpysl5:F001-F004`
and the semaphorin/plexin claim context explicitly report that represented
semaphorin, plexin, neuropilin, CRMP/DPYSL5, GSK3B/Fyn, and microtubule
comparators do not converge into an interchangeable acute postnatal neuronal
mRNA module. That is an imperfect proxy because `Cdk5`, `Nde1`, `Ndel1`, and
`Pafah1b1/Lis1` were not available as focal training perturbations, but the
available pathway surface gives no reason to lift `Dcx` above the sparse
baseline.

`Dcx` appeared as a measured gene in the focal DE matrix, so it was not absent
from the assay's vocabulary. Across the 1,674 non-held-out perturbations,
however, only `Qrich1` and `Rora` changed `Dcx` itself at FDR 0.05 in this cell
class (`Qrich1`: `Dcx` log2FC -0.965, FDR 0.0021, 75 focal DEGs; `Rora`: log2FC
0.652, FDR 0.0136, 278 focal DEGs). These are broad transcriptional or RNA-state
perturbations, not mechanistic analogs of a microtubule-stabilizing
developmental MAP. The direct analog queries showed that `Dcx`, `Dclk1`, and
`Dclk2` were all FDR-negative downstream of `Map1b`, `Map6`, `Tuba1a`, `Stmn2`,
`Dctn1`, `Kif2a`, `Kif5a`, `Kif5c`, `Tuba4a`, `Reln`, `Dab1`, `Vldlr`, `Nrp1`,
`Arx`, `Mapt`, `Map1lc3a`, `Mapre2`, `Tubb5`, `Tubb4b`, `Dpysl5`, `Gsk3b`, and
`Fyn`.

The resulting zero/nonzero decision is therefore a zero. If the perturbation
were in embryonic cortex or newborn dentate/SVZ neurons, or if the endpoint were
neuronal migration, commissural axon growth, or microtubule/vesicle imaging,
`Dcx` would be biologically strong. In this specific experiment the edit is
delivered at P16 and read out at P37-P44 in recovered NeuN-positive thalamic
glutamatergic nuclei, and the training set repeatedly shows that acute loss of
structural microtubule and migration machinery is either silent or restricted to
self-transcript/tubulin-isotype events. A self-only hit is also less likely for
`Dcx` than for `Map1b` or `Stmn2`, because `Dcx` is not a high constitutive MAP
in mature thalamic relay neurons. I therefore predict no measured gene passing
FDR 0.05:

`Dcx`: predicted `n_degs = 0`.

## Limits

- `Dclk1` and `Dclk2`, the cleanest mouse DCX-family paralogs, were not
  training perturbations in the focal-count CSV; the prediction extrapolates
  from broader microtubule, MAP, kinesin/dynactin, Reelin, semaphorin, and CRMP
  targets.
- The parquet contains differential statistics, not baseline UMI distributions
  or protein/indel measurements, so the chance of a `Dcx` self-transcript call
  has to be inferred indirectly.
- The focal snRNA endpoint cannot see the classic DCX phenotypes: altered
  embryonic neuronal migration, hippocampal lamination, axonal tracts, dendrite
  growth, and synaptic-vesicle transport are outside the readout.
- `Dctn1` and `Tuba1a` prove that the thalamic class can respond to selected
  cytoskeletal perturbations, but neither is mechanistically equivalent to
  postnatal `Dcx` loss; they serve mostly as assay-detectability boundaries.
