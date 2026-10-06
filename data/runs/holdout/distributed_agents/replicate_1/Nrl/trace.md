# DEG-count prediction trace

## Question and endpoint

The task is to predict, for each completely held-out perturbation, the number of genes that would pass Benjamini-Hochberg adjusted Wilcoxon `pvals_adj < 0.05` in the focal `151 TH Prkcd Grin2c Glut` population. The only requested target in this run is `Nrl`.

I treated the requested value as the same focal-cell `n_degs` count supplied for non-held-out training targets. A prediction of `0` means that no measured transcript is expected to pass FDR 0.05 after sparse postnatal CRISPR loss of `Nrl` in recovered `151` nuclei. The held-out `Nrl` rows themselves are absent from both supplied inputs by construction, so the prediction has to transfer from biologically related training perturbations.

Endpoint alignment:

- Direct for training perturbations: the CSV `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` reports the exact focal-cell DEG count for 1,674 non-held-out perturbations.
- Direct for analog expression signatures: the Parquet `training differential-expression dataset` reports the measured-gene DE rows for those same non-held-out perturbations.
- Absent for `Nrl`: neither an `Nrl` perturbation count nor an `Nrl` perturbation signature is present in the supplied inputs.
- Transfer evidence for the prediction: `Crx`, `Nr2e3`, `Otx2`, `Rorb`, `Thrb`, retinal sentinel genes, and Maf-family factors were represented among training perturbations or measured genes and show whether the rod/cone transcriptional program appears in the recovered postnatal brain neurons.

## Sources used

- Declared training DEG-count CSV for exact observed `n_degs` values in `151 TH Prkcd Grin2c Glut`.
- Declared all-cell-group DE Parquet for focal signatures of retinal/photoreceptor and nuclear-receptor analogs.
- The run-local task bindings, measurement registry, coverage summary, and capability manifest in `codex_runtime/pipeline`.
- PerturbAI July same-experiment corpus release `perturbai-july-260713-sourceguard-1773-v1`, queried only for report-level interpretation around visible training analogs. Its Finding/Claim graph was used once to locate that `Nr2e3` report text explicitly compared against `Nrl`; relation presence and multiplicity were not used as scores.
- PubMed literature for external mechanism priors:
  - Swaroop et al. 1992, PNAS, DOI `10.1073/pnas.89.1.266`, PMID `1729696`: identified neural retina leucine zipper as a conserved retina-enriched Maf-like basic leucine zipper gene.
  - Mears et al. 2001, Nature Genetics, DOI `10.1038/ng774`, PMID `11694879`: showed that mouse `Nrl` loss eliminates rods and converts the retinal rod program toward S-cone-like photoreceptors.
  - Oh et al. 2008, Brain Research, DOI `10.1016/j.brainres.2008.01.028`, PMID `18294621`: placed `Nr2e3` downstream of NRL and CRX in the mammalian retinal rod-versus-cone hierarchy.
  - Cheng et al. 2004, Human Molecular Genetics, DOI `10.1093/hmg/ddh173`, PMID `15190009`: reported that NR2E3 cooperates with NRL and CRX on rod phototransduction promoters.
  - Cheng et al. 2006, Human Molecular Genetics, DOI `10.1093/hmg/ddl185`, PMID `16868010`: showed in vivo that NR2E3 suppresses cone genes and activates a subset of rod genes in photoreceptor precursors.

## Dataset calculations

I first read the held-out manifest and confirmed that this run contains a single requested target, `Nrl`, in unranked file order:

```text
target_name
Nrl
```

The focal training CSV contains 1,674 non-held-out perturbations. Its `n_degs` distribution is heavily zero-inflated: 1,205/1,674 training targets have `n_degs = 0`, the median is 0, the mean is 14.05, and the maximum is 2,677.

I then queried exact `151 TH Prkcd Grin2c Glut` counts for biologically relevant targets:

| training perturbation | observed `151` `n_degs` | relationship to `Nrl` |
|---|---:|---|
| `Crx` | 0 | CRX cooperates with NRL in rod photoreceptor transcription. |
| `Nr2e3` | 0 | Direct NRL/CRX target in the rod-vs-cone hierarchy. |
| `Otx2` | 0 | Upstream retinal/pineal homeobox regulator in the same developmental lineage network. |
| `Rorb` | 0 | Photoreceptor-lineage nuclear receptor and rod/cone developmental comparator. |
| `Thrb` | 0 | Cone-subtype retinal nuclear-receptor comparator. |
| `Neurod1` | 0 | Retinal-neurogenic transcription-factor comparator, but broader and less direct than CRX/NR2E3. |
| `Maf` | 0 | Maf-family bZIP comparator. |
| `Mafa` | 0 | Maf-family bZIP comparator. |
| `Mafb` | 0 | Maf-family bZIP comparator. |
| `Mafg` | 1 | Maf-family bZIP comparator with a single accepted focal DEG. |
| `Rho` | 0 | Rod phototransduction output. |
| `Opn1sw` | 0 | Cone output/sentinel. |
| `Esrrb` | 0 | Retinal nuclear receptor. |
| `Rax` | 0 | Eye/retinal developmental comparator. |
| `Rxrg` | 0 | Retinoid receptor comparator. |
| `Nr2e1` | 0 | NR2-family comparator. |
| `Rora` | 278 | Counterexample: a CNS-active ROR-family factor with a strong `151` thalamic signature. |
| `Nr1d1` | 116 | Counterexample: a REV-ERB clock repressor with a strong `151` thalamic signature. |

For the closest retinal transcription factors, the focal Parquet signatures were not hidden subthreshold programs. In class `151`, the smallest adjusted p-values for the direct analogs were:

- `Crx`: all adjusted p-values were 1.0 among the top Wilcoxon-ranked rows; 160 perturbed cells.
- `Nr2e3`: no gene approached FDR 0.05; the strongest listed negative row was `Fip1l1`, FDR 0.830, and top positive rows were FDR 1.0; 279 perturbed cells.
- `Otx2`: the best rows were `Cnih3` and `Rbm17`, FDR 0.885; most rows were FDR 1.0; 162 perturbed cells.
- `Rorb`: all displayed top rows had FDR 1.0; 162 perturbed cells.
- `Thrb`: all displayed top rows had FDR 1.0; 137 perturbed cells.
- `Neurod1`: all displayed top rows had FDR 1.0; 304 perturbed cells.
- `Maf`, `Mafa`, and `Mafb`: all displayed top rows had FDR 1.0; `Mafg` had exactly one accepted DEG, `Lamp2`, with FDR 0.0476.

By contrast, the same focal class had interpretable high-count transcription-factor responses for unrelated but context-relevant regulators: `Rora` had 278 DEGs at FDR 0.05 in the training CSV, headed in the Parquet by down-regulation of `Prkcg`, `Adgrb1`, `Rasa4`, `Tnnt1`, `Plekhd1`, `Elmod1`, `Atp6ap2`, and `Pcp4`; `Nr1d1` had 116 DEGs, headed by up-regulation of `Erc2`, `Pdgfa`, `Tspan14`, `Cacna2d3`, `Pdzd2`, `Rasl11b`, and `Npas2`. This makes the `Crx`/`Nr2e3`/`Otx2` nulls more specific than a statement that all transcription factors are invisible in this cell type.

Finally, I checked retinal sentinel measured genes in the `151` rows. `Nrl`, `Crx`, `Nr2e3`, `Otx2`, `Rho`, `Gnat1`, `Pde6b`, `Opn1sw`, `Opn1mw`, and `Rcvrn` all had adjusted p-values of 1.0 after `Crx`, `Nr2e3`, `Otx2`, `Rorb`, `Thrb`, `Neurod1`, Maf-family, `Rora`, or `Nr1d1` perturbation in the focal class. The packaged July `Nr2e3` report reached the same conclusion across cell groups: retinal rod/cone sentinels including `Nrl`, `Crx`, `Rorb`, `Rho`, `Opn1sw`, `Opn1mw`, `Gnat1`, `Arr3`, and `Pde6b` had minimum FDR 1.0 across tested brain groups after `Nr2e3` perturbation.

## Target-specific prediction: `Nrl`

`Nrl` encodes a Maf-family bZIP transcription factor whose established loss-of-function biology is in rod photoreceptors. NRL acts with CRX to activate rod genes, activates `Nr2e3`, and through NR2E3 helps suppress cone genes. Germline retinal loss therefore causes a very large rod-to-S-cone fate switch, not a generic neuronal stress response.

The transfer chain for this task is:

1. Intervention: sparse AAV CRISPR loss of one endogenous gene at P16.
2. Direct consequence: reduced NRL protein in cells that normally depend on `Nrl`.
3. Propagation: loss of NRL/CRX/NR2E3 rod transcriptional regulation.
4. Exposure and selection: only postmitotic, NeuN-enriched whole-brain nuclei, harvested at P37-44.
5. Measured endpoint: single-nucleus DE among recovered `151 TH Prkcd Grin2c Glut` neurons.

In true rod photoreceptors, steps 2 and 3 should be strongly endpoint-bearing: `Nrl` loss moves rod and S-cone transcripts, and the requested snRNA-seq endpoint would be an appropriate RNA readout. The chain breaks at exposure. The dataset did not include retina, and the focal `151` thalamic glutamatergic neurons do not represent the rod/pineal lineage where NRL, CRX, and NR2E3 form an active regulatory module. The July corpus reports that `Crx` and `Nr2e3` were complete or near-complete FDR-level nulls across recovered brain groups and that their phototransduction sentinels remained at FDR 1.0. The direct focal training counts agree: `Crx = 0`, `Nr2e3 = 0`, `Otx2 = 0`, `Rorb = 0`, `Thrb = 0`, `Rho = 0`, and `Opn1sw = 0`.

The appropriate counterexamples do not argue for promoting `Nrl`. `Rora` and `Nr1d1` show that nuclear receptors and clock-linked transcription factors can make a strong `151` signature when the thalamic cells contain a compatible regulatory program. `Mafg` shows that a Maf-family perturbation can produce an isolated one-gene speckle, but `Maf`, `Mafa`, and `Mafb` were all zero, and generic bZIP family membership is too broad to transfer a rod-specific NRL phenotype into thalamic glutamatergic neurons.

I therefore predict no accepted DEGs for held-out `Nrl` in `151 TH Prkcd Grin2c Glut`: the prediction is driven mainly by within-dataset nulls for retinal transcriptional analogs, with the external literature explaining why those are the correct analogs and why a retinally dramatic perturbation should be quiet in the assayed cell class.

## Limits and uncertainty

- This is an extrapolation because `Nrl` itself is held out; the actual `Nrl` guide recovery, indel rate, and signature are absent.
- A zero in the focal class is not evidence that `Nrl` is biologically unimportant. It is a prediction for a sparse postnatal brain-neuron assay that omitted retinal photoreceptors.
- The CRISPR design measured survivor-conditioned nuclear RNA, not DNA editing, rod survival, visual function, protein abundance, or retinal morphology.
- Some coarse atlas groups, especially pineal-containing `217 P MY Pineal Glut`, may dilute rare relevant cells. That does not materially change the `151` prediction because the requested cells are thalamic glutamatergic neurons.
- The training data contain many zero counts, so a null prior exists even before biology. I did not use that zero inflation alone; the point estimate is based on specific nulls for `Crx`, `Nr2e3`, `Otx2`, and other rod/cone network members.
