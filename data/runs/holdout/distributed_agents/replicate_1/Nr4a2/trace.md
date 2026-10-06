# DEG-count prediction for held-out Nr4a2

## Question and endpoint

The requested held-out perturbation was `Nr4a2`. I interpreted the task as a point prediction of the exact assay endpoint used in the training table: the number of measured genes in `151 TH Prkcd Grin2c Glut` with Benjamini-Hochberg adjusted Wilcoxon `pvals_adj < 0.05`, after acute AAV CRISPR-Cas9 loss of function in juvenile postmitotic mouse neurons.

`151 TH Prkcd Grin2c Glut` was treated as the exact focal thalamic glutamatergic class; `TH` in this atlas label is thalamus, not tyrosine hydroxylase. I did not use self-target transcript loss as an editing-efficiency score, because the dataset portrait notes that nuclear target RNA reduction is not correlated with downstream response size in this CRISPR mosaic assay.

## Sources used

- Declared focal training counts: `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
- Declared DE Parquet: `training differential-expression dataset`.
- Requested-target manifest: `single-target request for Nr4a2`.
- Internal same-experiment semantic corpus: `perturbai-july-260713-sourceguard-1773-v1`, Findings ledger queried for `Nr4a1`, `Nr4a3`, `Esrra`, and `Rora`.
- External literature via NCBI PubMed E-utilities:
  - Zetterstrom et al. 1997, Science, DOI `10.1126/science.276.5310.248`, PMID `9092472`: Nurr1/Nr4a2 is required for generation of midbrain dopaminergic neurons.
  - Hawk et al. 2012, Journal of Clinical Investigation, DOI `10.1172/JCI64145`, PMID `22996661`: all three Nr4a genes are CREB-regulated, learning-induced orphan nuclear receptors whose combined NR4A function supports long-term memory enhancement by HDAC inhibitors.
  - Bridi and Abel 2013, Neurobiology of Learning and Memory, DOI `10.1016/j.nlm.2013.06.020`, PMID `23835142`: dominant-negative NR4A signaling impairs hippocampal transcription-dependent LTP.
  - Catala-Solsona et al. 2023, Journal of Neuroscience, DOI `10.1523/JNEUROSCI.1341-22.2023`, PMID `36931707`: neuronal activity induces Nr4a2 through an iGluR/Ca2+/CREB/CRTC1 pathway and Nr4a2 activation affects hippocampal BDNF, AMPAR expression, and LTD.

## Training-set calibration

The focal endpoint is highly zero-inflated: among 1,674 non-held-out perturbations, 1,205 had `n_degs = 0`; the median was 0, the 75th percentile was 1, the 90th percentile was 2, the 95th percentile was 18, and only the upper tail reached hundreds or thousands of DEGs. I therefore treated zero as the default for a target unless a within-dataset analog or target-specific biology supported a standing basal program in the focal thalamic class.

I queried the Parquet directly with `gene_target` filters, counted `pvals_adj < 0.05` per target and cell group, and inspected the lowest adjusted p-values in the exact focal group for the relevant comparators. That avoided using all-cell averages, which would mix the requested endpoint with non-focal populations.

## Target-specific reasoning

### Nr4a2

**Closest in-dataset paralogs**

| training perturbation | focal `n_degs` | focal matched perturbed nuclei | expression-pattern evidence |
|---|---:|---:|---|
| `Nr4a1` | 0 | 200 | No FDR-significant genes in `151 TH Prkcd Grin2c Glut`; no DEG in any of the 23 measured neuronal groups for this target. In the focal group, `Nr4a1`, `Nr4a2`, and `Nr4a3` transcript rows all had `pvals_adj = 1.0`. The internal Findings ledger reported that the nearest signed-score neighbors of the flat `Nr4a1` surface had only tiny cosines and did not represent biological convergence. |
| `Nr4a3` | 0 | 218 | No FDR-significant genes in the focal group; only two focal rows were even subthreshold at `pvals_adj < 0.25` (`Kcnj9`, 0.166; `Edem3`, 0.218). `Nr4a1`, `Nr4a2`, and `Nr4a3` transcript rows all had `pvals_adj = 1.0`. Across the atlas, the same-experiment report found only a single weak pineal-class FDR<0.10 `Xpo6` hit, not a shared NR4A program. |

This is the strongest quantitative evidence. `Nr4a1`, `Nr4a2`, and `Nr4a3` are the NR4A orphan nuclear receptor family; Hawk et al. showed that all three are learning-induced CREB-regulated nuclear receptors, and hippocampal plasticity studies place NR4A activity downstream of neuronal stimulation. If a single basal NR4A loss were sufficient to create a broad juvenile resting neuronal transcriptome, one of `Nr4a1` or `Nr4a3` should have produced at least a small focal footprint. They did not, despite 200 and 218 matched focal perturbed nuclei, respectively.

**Activity-dependent pathway analogs and counterexamples**

| training perturbation | focal `n_degs` | relevance |
|---|---:|---|
| `Creb1` | 10 | Upstream activity-regulated transcriptional node. It produced a small focal signature centered on `Crem`, not a broad NR4A-like or BDNF/AMPAR program. |
| `Crebbp` | 8 | CREB coactivator relevant to NR4A induction in memory studies; its focal signature was small and distinct. |
| `Fosl2` | 0 | Immediate-early/AP-1 neighbor mentioned in hippocampal NR4A output literature, but flat in the focal endpoint. |
| `Jund` | 0 | AP-1 immediate-early neighbor; focal null, with only one DEG each in `145 MH-LH TH Glut` and `155 MB Glut`. |
| `Egr2` | 0 | Immediate-early transcription factor; null across the focal group and the queried atlas groups. |

These comparators argue that the assay can detect a small activity-transcription factor footprint (`Creb1`, `Crebbp`) but that basal single-gene perturbation of the NR4A/AP-1/EGR part of the network is usually silent in this thalamic class. External hippocampal work, especially the activity-dependent Nr4a2 iGluR/Ca2+/CREB/CRTC1 result from Catala-Solsona et al. 2023, supports a stimulus-coupled model rather than a constitutive thalamic maintenance model in unstimulated juvenile nuclei.

**Nuclear receptor and RXR pathway counterexamples**

| training perturbation | focal `n_degs` | relevance |
|---|---:|---|
| `Rxra`, `Rxrb`, `Rxrg` | 0, 0, 0 | NR4A-family receptors can signal with RXR in some contexts, but perturbing each RXR target was focal-null here. |
| `Ncoa1`, `Ncoa3` | 0, 0 | Nuclear-receptor coactivator controls; no focal response. |
| `Rarb` | 0 | Retinoic-acid receptor family counterexample with adequate focal recovery. |
| `Esrrb`, `Esrrg` | 0, 0 | Related orphan nuclear receptors did not produce focal DEGs. |
| `Rora` | 278 | A positive thalamic nuclear-receptor control: `Rora` loss down-regulated a broad thalamic Prkcd/Grin2c program, including `Prkcg`, `Rasa4`, `Pcp4`, `Car4`, `Nr1d1`, `Prkcd`, `Grin2c`, `Slc1a6`, `Tcf7l2`, and `Foxp2` in the same-experiment Finding summary. |
| `Esrra` | 57 | A second positive nuclear-receptor control with a focal oxidative-metabolism/ion-handling signature; this was restricted to `151 TH Prkcd Grin2c Glut`. |

`Rora` and `Esrra` are important counterexamples rather than analogs for the final estimate. They show that the focal class has enough power to recover a maintained nuclear-receptor program, but their expression states are ROR-alpha thalamic terminal identity and ERR-alpha oxidative metabolism, respectively, not NR4A activity-response biology. The RXR and coactivator nulls also argue against assigning `Nr4a2` a positive count on the basis of generic nuclear-receptor family membership.

**Biological rationale and final point**

`Nr4a2` differs from the two measured paralogs by its classic Nurr1 requirement in dopaminergic neuron development and maintenance, as shown by loss of midbrain dopaminergic neurons in germline Nurr1-deficient mice. That function is a candidate-specific reason to expect an effect in a dopaminergic class, not in the requested `151 TH Prkcd Grin2c Glut` class. The assay did include a sparse `215 MB Dopa` class for some training targets, but the requested endpoint is thalamic glutamatergic neurons. The task asks for the FDR-gated breadth among surviving focal nuclei after acute P16 CRISPR loss, not for an embryonic dopaminergic differentiation phenotype or a hippocampal learning/stimulation assay.

Putting those pieces together, I predicted `Nr4a2` to follow the two closest NR4A paralogs and the RXR/NCOA/immediate-early nulls in this exact endpoint. The point estimate is `0` DEGs.

## Limits and extrapolation

`Nr4a2` itself was completely held out, so no same-experiment `Nr4a2` expression signature or count was available. The prediction transfers from `Nr4a1` and `Nr4a3`; that transfer is imperfect because Nurr1 has dopaminergic functions that are not shared equally by the full family. The external NR4A literature is dominated by dopaminergic development, hippocampal plasticity, stimulation, stress, or disease contexts, while the Perturb-seq measurement is basal, acute, partial mosaic loss in juvenile postmitotic neurons. Severe survivor-conditioned selection could in principle remove an early `Nr4a2`-sensitive subpopulation and leave a quiet recovered signature, but the training analogs provide no target-specific reason to expect that in thalamic Prkcd/Grin2c glutamatergic cells. I therefore used a hard zero rather than a small positive integer.
