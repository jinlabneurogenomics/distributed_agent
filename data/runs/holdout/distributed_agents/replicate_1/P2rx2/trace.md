# Question and endpoint

The task is to predict the held-out `n_degs` count for each requested knockout in `151 TH Prkcd Grin2c Glut` thalamic glutamatergic neurons.  I treated `n_degs` as the exact focal-cell endpoint supplied in the training CSV: the number of measured genes with Scanpy Wilcoxon Benjamini-Hochberg-adjusted `pvals_adj < 0.05`, not a direct measure of viability, editing rate, biological importance, or absolute RNA output.

This run has one held-out target, `P2rx2`.  It is absent as a `gene_target` in the differential-expression Parquet and absent from the focal training-count CSV, so its focal DEG count is a true prediction.

# Sources used

- Declared input table `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`, with 1,674 non-held-out focal perturbations and their observed `n_degs`.
- Declared differential-expression Parquet `training differential-expression dataset`, queried only for the focal cell group and P2/purinergic, glutamate-receptor, nicotinic-receptor, and calcium/pump channel comparators.
- The run-local dataset portrait, task bindings, coverage summary, and measurement registry under `codex_runtime/pipeline`.
- The July PerturbAI same-experiment corpus, release `perturbai-july-260713-sourceguard-1773-v1`, queried through `corpus.findings` for `P2ry12`, `P2ry14`, `Grin1`, and `Cacna1g` compact Findings.  These reports are interpretations of the same experiment, not independent replication.
- External mechanism checks:
  - Mouse Genome Informatics / Alliance orthology and nomenclature: `P2rx2` encodes purinergic receptor P2X, ligand-gated ion channel, 2, the mouse ortholog of P2RX2.
  - North 2002, *Physiological Reviews*, DOI `10.1152/physrev.00015.2002`, PMID `12270951`: P2X receptors are extracellular ATP-gated trimeric cation channels; P2X2 can form homomeric channels and P2X2/3 heteromers.
  - Burnstock 2000, *British Journal of Anaesthesia*, DOI `10.1093/oxfordjournals.bja.a013473`, PMID `10823099`, and North 2003, *Journal of Physiology*, DOI `10.1113/jphysiol.2003.048587`, PMID `12832496`: P2X2/3 biology is strongest in primary sensory purinergic signaling and pain/taste/visceral afferent contexts, with P2X3-dominated sensory-neuron channels.
  - Jarlebark et al. 2002, *NeuroReport*, DOI `10.1097/00001756-200210280-00030`, PMID `12395104`: P2X2-containing ATP-gated channels are functional in mouse cochlear sensory and supporting cells.
  - Haynes et al. 2006, *Nature Neuroscience*, DOI `10.1038/nn1805`, PMID `17115040`: P2Y12 is a homeostatic microglial ADP/ATP receptor required for nucleotide-directed microglial process extension after injury, explaining why the P2Y training receptors are imperfect neuronal comparators.

# Quantitative calibration

The held-in focal endpoint was extremely sparse.  Across the 1,674 visible perturbations, the median count was `0`, the 75th percentile was `1`, the 90th percentile was `2`, and the 95th percentile was `18`; only a small upper tail of housekeeping and RNA-processing genes produced hundreds to thousands of DEGs.  That distribution makes zero the default for a target unless an expressed, cell-autonomous function or a close training analog argues otherwise.

There were no non-held-out `P2rx*` targets in the training-count table.  The only P2 purinergic receptors in the training table were:

| training perturbation | focal `n_degs` | relationship to `P2rx2` |
| --- | ---: | --- |
| `P2ry12` | 0 | P2-family nucleotide receptor, but Gi-coupled GPCR and homeostatic microglial marker rather than a P2X cation channel |
| `P2ry14` | 0 | P2-family UDP-sugar GPCR, mostly immune/glial/inflammatory rather than a constitutive thalamic neuronal channel |

The compact same-experiment corpus agrees with the raw focal counts: `P2ry14` produced no FDR<0.10 downstream genes in any of 22 NeuN-enriched neuronal groups, while `P2ry12` had only a near-threshold singleton in `054 CNU-MGE GABA` and no robust neuronal module.  I therefore used them as lineage/context counterexamples only, not as close molecular phenocopies of a P2X2 ATP channel.

I compared `P2rx2` with represented ion-channel knockouts in the focal training table:

| training perturbation | focal `n_degs` | focal expression-pattern note |
| --- | ---: | --- |
| `Chrna1` | 0 | no detectable nicotinic-channel footprint |
| `Chrna2` | 0 | no detectable nicotinic-channel footprint |
| `Chrna3` | 0 | no detectable nicotinic-channel footprint |
| `Chrna4` | 2 | only `Chrna4` and `Cyp46a1` significant |
| `Chrna6` | 0 | no detectable nicotinic-channel footprint |
| `Chrna7` | 0 | no detectable nicotinic-channel footprint |
| `Chrnb1` | 0 | no detectable nicotinic-channel footprint |
| `Chrnb2` | 1 | only the target transcript significant |
| `Chrnb3` | 0 | no detectable nicotinic-channel footprint |
| `Grin2a` | 1 | mostly self-target effect |
| `Grin2b` | 2 | self-target plus one additional gene |
| `Grin2d` | 0 | no focal FDR<0.05 footprint |
| `Grin3a` | 0 | no focal FDR<0.05 footprint |
| `Cacna1g` | 12 | a true but narrow thalamic Cav3.1 state |
| `Grin1` | 89 | obligatory NMDAR subunit with a clear 151 TH synaptic/plasticity response |
| `Atp1a3` | 80 | Na/K pump perturbation with a broader excitability/homeostasis response |
| `Atp2a2` | 187 | ER calcium pump perturbation with a stress-linked footprint |

`Grin1`, `Cacna1g`, `Atp1a3`, and `Atp2a2` show that the assay can see focal thalamic neuronal consequences of some channel and ion-homeostasis genes when the perturbed gene is limiting in this cell group.  They are counterexamples, not direct `P2rx2` analogs: NMDAR and T-type calcium-channel activity are core excitability signals in these thalamic neurons, whereas P2X2 is an ATP-gated purinergic receptor whose best established roles are in sensory afferents and ligand-evoked paracrine signaling.

I also queried the Parquet for P2 receptor transcripts as measured genes in the focal group across all 1,674 visible perturbations.  `P2rx2` was never significant (`min pvals_adj = 0.906`), and most other `P2rx`/`P2ry` measured genes were also inert except for occasional `P2rx4` or `P2rx7` changes inside very strong unrelated signatures such as `Zbtb7a`, `Yy1`, and `Uba5`.  Because differential-expression rows do not contain baseline expression, I used this only as weak evidence that `P2rx2` is not part of the recurrent 151 TH response modules.

# Target-specific prediction

## P2rx2

**Intervention.** Acute mosaic CRISPR loss of `P2rx2` should reduce functional P2X2 ATP-gated receptor subunits in successfully edited postmitotic neurons, but the readout samples surviving NeuN-positive nuclei and does not assay ATP-evoked currents.

**Direct molecular consequence.** P2X2 is a trimeric ligand-gated cation-channel subunit.  It can form homomeric P2X2 channels or heteromeric P2X2/3 channels after extracellular ATP binding; it is not a transcription factor, spliceosome factor, ubiquitin/proteasome component, or obligate component of the NMDA/Cav3.1 machinery.

**Propagation to this focal population.** There is no represented P2X paralog in training, so I could not transfer from a direct paralogous P2X knockout.  The two represented purinergic GPCR knockouts, `P2ry12` and `P2ry14`, were both zero in the exact focal endpoint and the July same-experiment corpus interpreted them as flat in NeuN-enriched neuronal cells because their canonical biology is microglial, immune, or ligand/injury dependent.  Those are not mechanistically equivalent to `P2rx2`, but they support a broader point: purinergic receptors do not create detectable basal neuronal DEG footprints in this assay merely by belonging to the P2 family.

The stronger ion-channel training counterexamples also argue against a large count.  `Grin1` had 89 DEGs because every conventional NMDA receptor requires GluN1 and the focal signature carried coordinated synaptic and plasticity genes.  `Cacna1g` had 12 DEGs because Cav3.1 is a thalamic low-voltage calcium channel.  By contrast, most ligand-gated subunit knockouts were at 0 to 2 DEGs: `Chrna1/2/3/6/7`, `Chrnb1`, `Chrnb3`, `Gria1/2/3`, `Grin2d`, and `Grin3a` were zero, `Chrnb2` and `Grin2a` were one, and `Chrna4` and `Grin2b` were two.  `P2rx2` is expected to behave more like these nonlimiting receptor-subunit knockouts than like `Grin1`: P2X2 is ligand gated and sensory-purinergic, and broad P2X membership gives no reason to expect tonic NMDAR-like synaptic remodeling in `151 TH Prkcd Grin2c Glut`.

**Exposure, selection, and measured endpoint.** The experiment occurred without an explicit ATP injury challenge, taste/cochlear/visceral sensory stimulation, or microglial sampling.  The focal class is thalamic glutamatergic, not cochlear, vagal, dorsal-root, nodose, trigeminal, or microglial.  A severe early selection effect could be missed by survivor-conditioned snRNA-seq, but the known P2X2 mechanism does not supply a strong candidate-specific reason for loss of these sparse thalamic neurons.

**Prediction.** I therefore predict that `P2rx2` will not produce a BH FDR<0.05 focal DEG in the held-out data.  I considered assigning a small positive value by analogy to `Chrna4`, `Chrnb2`, or `Grin2b`, but their one-to-two-gene counts were driven partly by significant self-target rows or receptor subunits with clearer CNS synaptic expression.  The nearest purinergic training counts are zero, and the ligand-gated receptor-subunit background is dominated by zeros, so the point prediction is:

`P2rx2	0`

# Limits and uncertainty

The largest weakness is absence of a non-held-out `P2rx1`, `P2rx3`, `P2rx4`, `P2rx5`, `P2rx6`, or `P2rx7` knockout in the training endpoint table; all P2X-to-P2X transfer is therefore external.  The P2Y receptors are nucleotide-responsive but molecularly different GPCRs and are mostly glial or immune, so they are lineage/context controls, not redundant receptor subunits.  The Parquet DE rows also do not provide baseline `P2rx2` expression in the focal cell group, and lack of recurrent `P2rx2` differential expression is only indirect support.  Finally, the predicted zero is an FDR-count prediction for recovered nuclei at this sample size; a non-transcriptional ATP current, an effect in rare sensory neurons, or an injury-dependent P2X2 phenotype could exist while still yielding `0` DEGs in `151 TH Prkcd Grin2c Glut`.
