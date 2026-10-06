# Question and resolved scope

The requested held-out perturbation set contains one mouse target, `Gpr12`, from
`095_Gpr12.csv`. I interpreted the requested endpoint as the integer number of
measured genes with `pvals_adj < 0.05` in the `151 TH Prkcd Grin2c Glut`
cell group after acute AAV-CRISPR loss of `Gpr12`, with the target transcript
itself counted if it would pass the same FDR threshold. `Gpr12` is absent from
both the supplied training differential-expression parquet as a `gene_target`
and from the focal-cell training DEG-count CSV, but it is present as a measured
`names` gene in the focal-cell signatures.

# Sources used

Internal and same-experiment data:

* `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`
* `[local file: training_de_all_cell_groups.parquet]`
* Distributed Agents corpus MCP release `perturbai-july-260713-sourceguard-1773-v1`;
  `target_context`, `story_count`, and pathway/evidence ledger queries returned
  no `Gpr12` claims, findings, explicit references, or pathway records, so the
  corpus did not supply a same-experiment mechanistic neighbor for this target.
* Distributed Agents runtime `profile_compare`, used on a declared cohort of observed
  GPCR, Gs/cAMP, and CREB-pathway perturbations in the focal group.

External biology:

* PubMed literature searches through NCBI PubMed E-utilities.
* Hsiao et al. 2020, Cell, DOI `10.1016/j.cell.2020.09.011`, PMID `32997977`:
  identified thalamic `Gpr12` as sufficient to modulate working-memory
  performance and thalamo-prefrontal synchrony.
* Li et al. 2022, Science Bulletin, DOI `10.1016/j.scib.2022.12.023`, PMID
  `36593162`: solved the active `GPR12`-Gs structure and described `GPR12` as a
  highly constitutively active Gs-coupled receptor that increases cAMP.
* Brown, Laun and Song 2017, Biochemical and Biophysical Research
  Communications, DOI `10.1016/j.bbrc.2017.09.001`, PMID `28888984`: measured
  `GPR12` as a constitutively active Gs receptor whose cAMP output can be
  inverse-agonized by cannabidiol.
* Morales, Isawi and Reggio 2018, Drug Metabolism Reviews, DOI
  `10.1080/03602532.2018.1428616`, PMID `29390908`: reviewed the related
  orphan class-A receptors `GPR3`, `GPR6`, and `GPR12`, their brain-biased
  expression, and their constitutive adenylyl-cyclase/cAMP activity.
* Bjursell et al. 2006, BBRC, DOI `10.1016/j.bbrc.2006.07.090`, PMID
  `16887097`, and Frank et al. 2012, PLoS One, DOI
  `10.1371/journal.pone.0042395`, PMID `22879962`: reported that whole-body
  `Gpr12` loss in mice produces modest, strain-sensitive metabolic and
  behavioral phenotypes rather than a severe neuronal viability phenotype.

# Same-experiment computations

I first read the held-out manifest and confirmed that the run asks only for
`Gpr12`. I then used the focal-cell training count CSV to calibrate the endpoint
scale. Among 1,674 observed training perturbations, the focal response is very
sparse: 469 are nonzero, the median is 0 DEGs, the 75th percentile is 1 DEG,
the 95th percentile is 18 DEGs, and the maximum is 2,677 DEGs. This makes a
zero or target-only call the default expectation for receptor perturbations
unless a strong within-assay analog shows broad secondary expression changes.

Over the parquet I selected only
`group_name == "151 TH Prkcd Grin2c Glut"` and relevant observed `gene_target`
values, retaining `gene_target`, `names`, `logfoldchanges`, and `pvals_adj`.
Each observed perturbation in this group had 17,259 measured genes. I also
checked target self-rows by filtering focal rows to `names in training_targets`
and then retaining `gene_target == names`; 1,642 observed targets had a
self-row, 319 self-transcripts were significant, and 237 of the 276 training
perturbations with exactly one DEG were target-self-only hits.

The relevant in-panel analogs and counterexamples were:

| training perturbation | n_degs in 151 TH Prkcd Grin2c Glut | focal expression-pattern evidence | interpretation for Gpr12 |
| --- | ---: | --- | --- |
| `Gpr158` | 1 | the only significant feature was its own transcript, `Gpr158`, log2FC -0.991, adjusted p `3.39e-26` | A brain GPCR can produce a target-only one-DEG result with no secondary program. |
| `Gpr156`, `Gpr161`, `Gpr179`, `Gpr45`, `Gprc5b` | 0 each | no significant focal DEGs | Nearby receptor annotations alone are not enough to imply a detectable response. |
| `Gprasp2` | 1 | the single DEG was its own transcript, log2FC -0.491, adjusted p `0.0071` | GPCR accessory/sorting biology was target-only in this assay. |
| `Gnas`, `Gnal`, `Adcy1`, `Adcy3`, `Adcy5`, `Pde1c`, `Pde4b`, `Pde4d`, `Pde10a` | 0 each | no significant focal DEGs for the Gs alpha or adenylyl-cyclase/phosphodiesterase targets | Direct perturbation of the bulk Gs/cAMP machinery did not create a detectable focal transcriptional program. |
| `Prkaca`, `Prkar1a` | 1 each | each had a single significant self-transcript; `Prkaca` log2FC -0.940, adjusted p `7.91e-22`; `Prkar1a` log2FC -0.569, adjusted p `0.00138` | Even core PKA subunits stayed target-only rather than broad in this cell type. |
| `Htr4`, `Htr6`, `Htr7`, `Drd5`, `Crhr1` | 0 each | no significant focal DEGs | Other neuronal Gs-coupled receptors in the library were silent by this endpoint. |
| `Cnr1`, `S1pr2`, `Sphk1` | 1, 0, 0 | `Cnr1` had one off-target-looking significant gene and the sphingolipid receptor/synthesis nodes had no significant DEGs | GPR12's cannabinoid/lysophospholipid neighborhood did not show broad transferable responses. |
| `Creb1`, `Crebbp` | 10, 8 | low but real DEG counts at a downstream transcription factor/coactivator layer; the two did not share significant genes with each other in the GPCR/cAMP profile comparison | These are downstream transcriptional regulators, not appropriate breadth templates for knocking out one upstream orphan receptor. |

The Distributed Agents runtime comparison of 23 observed GPCR/cAMP/CREB candidates in
the same focal group agreed with the manual counts: 16/23 had no significant
features, 6/23 had 1-9, and only `Creb1` reached the 10-49 bin. Whole-profile
correlations among these mostly flat signatures were dominated by assay-wide
background structure and the pairs shared essentially no significant
same-direction gene programs; I therefore used the comparison chiefly as a
falsification check for a coherent cAMP-response module, not as a weighted
average.

# Target-specific prediction

`Gpr12` is a constitutively active orphan class-A GPCR that couples to Gs and
elevates cAMP, and the closest paralogous receptors, `Gpr3` and `Gpr6`, are
absent from the observed perturbation set. The specific thalamic connection
matters because Hsiao et al. found that `Gpr12` can modify thalamus-dependent
short-term-memory circuitry, and this requested readout is a thalamic
glutamatergic group. At the same time, the training data argue strongly against
a large downstream program from partial acute loss: all three adenylyl cyclase
perturbations, `Gnas`, several Gs-coupled neurotransmitter receptors, and four
PDE perturbations produced 0 DEGs in the same cells, while `Prkaca` and
`Prkar1a` were target-only. Germline mouse studies also do not make `Gpr12`
look like an essential postmitotic-neuron survival gene.

I therefore predicted that the loss of `Gpr12` would not pass the FDR threshold
for a broad cAMP/CREB or stress program. The point estimate is still nonzero:
`Gpr12` is measured in `151 TH Prkcd Grin2c Glut`, `Gpr158` and several other
neuronal signaling genes in the training set landed exactly at one DEG because
their own transcript was significantly reduced, and the biology gives a better
case for `Gpr12` being expressed in thalamic neurons than for the receptors
whose focal signatures were completely empty. The resulting prediction is
`predicted_n_degs = 1`.

# Limits

This is an extrapolation because the best paralogs, `Gpr3` and `Gpr6`, were not
observed perturbations, the Distributed Agents corpus release had no `Gpr12` findings,
and the external `GPR12` literature uses overexpression, ligands, germline
mutants, or circuit-level behavioral assays rather than sparse juvenile
AAV-CRISPR in `151 TH Prkcd Grin2c Glut` nuclei. The distinction between 0 and
1 is also assay-power-sensitive: it depends on whether the four `Gpr12` guides
drive enough target-RNA depletion in this focal group for `Gpr12` itself to
cross Benjamini-Hochberg FDR 0.05. I see little evidence for more than a
target-only hit, but the exact integer is weakly constrained.
