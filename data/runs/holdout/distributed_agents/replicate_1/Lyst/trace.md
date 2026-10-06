# DEG-count prediction for Lyst in 151 TH Prkcd Grin2c Glut

## Question and endpoint

The held-out readout is the integer number of measured genes with `pvals_adj < 0.05` after acute mosaic CRISPR loss of each requested target in `151 TH Prkcd Grin2c Glut` thalamic glutamatergic neurons.  The requested CSV contains one held-out perturbation, `Lyst`, and its own DEG count/signature is absent from the supplied training inputs, so the estimate has to be transferred from non-held-out perturbations.

I treated the training count CSV as the direct endpoint for represented perturbations, and the parquet as the direct source for the focal-cell expression patterns behind those counts.  Packaged July PerturbAI Findings/Evidence are same-experiment interpretations of the same parquet, not independent validation.  LYST biology from PubMed and curated database-style report references was used only to choose relevant in-dataset analogs and counterexamples.

## Sources used

- `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`: exact `n_degs` endpoint for the 1,674 non-held-out training targets.
- `training differential-expression dataset`: focal-cell differential-expression rows for lysosome-, AP-3/BLOC-, BEACH-domain, Rab, VPS, and autophagy analogs.
- Internal PerturbAI July release `perturbai-july-260713-sourceguard-1773-v1`: bounded `corpus.findings` and `corpus.report_evidence` records for `Ap3b1`, `Dtnbp1`, `Rab27a`, `Lrba`, `Nbea`, `Lamp2`, `Atg5`, `Atg16l1`, `Becn1`, and `Rab7`.
- External mechanism references:
  - Cullinane, Schaffer & Huizing 2013, Traffic, doi:10.1111/tra.12069: review of LYST, LRBA, NBEA, WDFY3 and other BEACH-domain membrane trafficking proteins.
  - Rudelius et al. 2006, Acta Neuropathologica, doi:10.1007/s00401-006-0092-6, PMID 16791600: murine `Lyst` missense allele causing giant lysosomes and progressive Purkinje-cell degeneration.
  - Greene et al. 2025, Communications Biology, doi:10.1038/s42003-025-08482-1, PMID 40681653: CRISPR `Lyst`-null mouse recapitulating Chediak-Higashi syndrome with age-progressive neurodegeneration.
  - Ji et al. 2022, PLoS ONE, doi:10.1371/journal.pone.0254469, PMID 35239671: `Lyst` deficiency in retinal pigment epithelium causing phagosome accumulation, cathepsin/MMP increases, and oxidative stress.
  - Wang et al. 2000, Journal of Neuroscience, doi:10.1523/JNEUROSCI.20-23-08551.2000, PMID 11102458: NBEA is a neuronal BEACH-WD40 homolog of beige/LYST with post-Golgi membrane localization.
  - Larimore et al. 2011, Molecular Biology of the Cell, doi:10.1091/mbc.E11-07-0592, PMID 21998198: BLOC-1/dysbindin and AP-3 cooperate in neuronal cargo sorting from the soma to synapses.

## Computations over the training data

I first summarized the direct focal-cell endpoint.  The training distribution is highly zero-inflated: 1,205 of 1,674 training perturbations have `n_degs = 0`, the median is 0, the 75th percentile is 1, the 90th percentile is 2, and the 95th percentile is 18.  Thus a prediction of one or a few DEGs is already above most perturbations; I did not round every biologically plausible gene to a positive count.

I then selected represented perturbations that could distinguish several causal positions:

- lysosome-related-organelle cargo routing close to Chediak-Higashi/Hermansky-Pudlak biology: `Ap3b1`, `Dtnbp1`, `Rab27a`
- BEACH-domain or large endomembrane scaffolds: `Nbea`, `Lrba`, `Wdfy3`
- autophagy or lysosomal membrane/hydrolase genes: `Atg5`, `Atg16l1`, `Becn1`, `Lamp2`, `Ctsb`
- late-endosome, HOPS, GARP, retromer, and VPS-family counterexamples: `Rab7`, `Vps35`, `Vps41`, `Vps53`, `Vps54`, `Vps13a`, `Vps13b`, `Vps13c`
- mTOR/lysosome-stress positive controls: `Tsc2`

For those targets I filtered the parquet to `group_name == "151 TH Prkcd Grin2c Glut"` and counted rows with `pvals_adj < 0.05`, checking the result against the training CSV.  The exact focal counts were:

| perturbation | focal `n_degs` | relevance to LYST prediction |
| --- | ---: | --- |
| `Ap3b1` | 0 | AP-3 beta3A lysosome-related-organelle/synaptic-vesicle cargo adaptor; a close functional neighbor of BLOC/HPS trafficking. |
| `Dtnbp1` | 0 | BLOC-1/dysbindin, cooperating with AP-3 in endosomal cargo sorting to neuronal processes. |
| `Rab27a` | 0 | regulated secretory lysosome/exocytosis Rab and Griscelli/Chediak-Higashi-like disease-space comparator. |
| `Lrba` | 0 | BEACH-domain endomembrane scaffold, broad family comparator for LYST. |
| `Nbea` | 0 | neuronal BEACH-WD40 homolog of beige/LYST and synaptic receptor-trafficking scaffold. |
| `Lamp2` | 0 | lysosomal membrane/autophagy endpoint; nearest focal rows were just below significance (`Lamp2` FDR 0.0537 and `Ppm1g` FDR 0.0545). |
| `Atg5`, `Atg16l1`, `Becn1` | 0, 0, 0 | core or initiation autophagy genes, all buffered in the focal class. |
| `Vps13a`, `Vps13b`, `Vps13c`, `Vps35l`, `Vps41`, `Vps53` | all 0 | vacuolar/endosome trafficking perturbations that did not cross the focal FDR threshold. |
| `Wdfy3` | 17 | BEACH/FYVE autophagy adaptor; the main BEACH counterexample but developmentally distinct from LYST. |
| `Vps35`, `Vps54` | 17, 31 | retromer and GARP/EARP genes with small positive focal responses. |
| `Tsc2` | 86 | mTORC1 regulator showing that lysosome-adjacent metabolic biology can be detected but is not an LYST analog. |
| `Rab7` | 501 | late-endosomal/lysosomal Rab, the strong positive counterexample with V-ATPase, hydrolase, sterol, ISR/UPR, and proteasome mRNA induction. |

The same-experiment corpus refined these focal counts with all-cell-group pattern checks.  `Ap3b1` had no downstream FDR<0.10 genes in 18 measured neuronal groups, and `Dtnbp1` and `Slc32a1` were also flat in the Ap3b1-matched groups.  `Dtnbp1` had no BH-corrected downstream transcriptional response in any of 23 recovered neuronal groups.  `Rab27a` had 0 downstream FDR<0.10 genes across all 21 recovered NeuN+ groups, while `Rab7` and `Stxbp1` produced lysosomal or synaptic responses in the same screen.  `Nbea` was FDR<0.10 pan-null across 21 groups, and its BEACH comparators split into flat `Lrba` and low-count `Wdfy3`.  `Lrba` was also a near-pan-neuronal transcriptional null and had near-zero score cosines to `Wdfy3`, `Nbea`, `Becn1`, `Atg5`, `Atg16l1`, and `Map1lc3a`.  `Rab7` was the opposite: in the same release it induced recurrent late-endosomal/lysosomal compensation and stress modules, but HOPS/retromer/WASH comparators were weak or partial FDR phenocopies, so physical pathway adjacency alone clearly did not transfer the 501-DEG `Rab7` response.

## Lyst-specific reasoning

`Lyst` encodes the lysosomal trafficking regulator, a BEACH-WD40 protein whose loss causes Chediak-Higashi/beige giant lysosome-related organelles.  Germline or complete loss can be neurologically important: Lyst-mutant mice can show progressive Purkinje-cell degeneration and a newer `Lyst`-null C57BL/6 model develops later neurodegeneration with inflammatory lipid/transcript changes.  Those sources establish that the gene is real neuronal disease biology, not that an acute P16 sparse CRISPR perturbation in recovered juvenile thalamic nuclei should produce a broad 3-4 week nuclear-RNA response.  The Ji et al. retinal study also points to large secondary effects in a professional phagocytic epithelium; that phagosome/cathepsin/MMP stress chain is not the primary physiology of the NeuN+ thalamic glutamatergic cells assayed here.

The causal transfer I used was:

`Lyst` loss -> abnormal lysosome-related-organelle size/fission and cargo handling -> possible altered endolysosomal, secretory, or autophagy flux -> possible stress or compensation if the defect reaches a limiting pathway in juvenile thalamic neurons -> surviving, recovered NeuN+ nuclei -> Wilcoxon DEGs.

The represented perturbations argue that this chain usually stops before the nuclear DEG endpoint for cargo-routing and BEACH-domain factors.  `Ap3b1` and `Dtnbp1` perturb the AP-3/BLOC route that is mechanistically close to Hermansky-Pudlak and lysosome-related-organelle cargo sorting; both were exact focal zeros and had broad same-experiment null surfaces.  `Rab27a`, another lysosome-related-organelle/regulated secretion disease comparator, was an exact focal zero in 135 perturbed cells with no corrected response across 21 neuronal groups.  `Nbea` and `Lrba`, the available BEACH-domain comparators, were exact focal zeros and pan- or near-pan-neuronal nulls.  `Lamp2`, `Atg5`, `Atg16l1`, and `Becn1` further show that even established lysosomal/autophagy biochemical lesions often did not propagate to FDR<0.05 mRNA changes in `151 TH Prkcd Grin2c Glut`.

I treated `Rab7`, `Vps35`, `Vps54`, `Wdfy3`, and `Tsc2` as counterexamples rather than primary analogs.  `Rab7` is a limiting late-endosome Rab; the exact focal count was 501, and its signature contained a large V-ATPase/hydrolase/sterol/ISR response.  LYST is upstream and more specialized in organelle-size regulation, and the same release already showed that even direct Rab7 pathway neighbors such as `Vps41`, `Vps35`, and WASH/V-ATPase/lysosomal comparators mostly fail to phenocopy `Rab7` at FDR level.  `Vps35` and `Vps54` had only 17 and 31 focal DEGs; they represent retrieval/tethering perturbations with detectable but still small effects.  `Wdfy3` is the only positive BEACH/FYVE scaffold in this focal cell class, but its same-experiment comparison to `Lrba` and `Nbea` showed divergence, and WDFY3/ALFY is an autophagy adaptor with developmental connectivity biology rather than a Chediak-Higashi lysosomal-size regulator.

Therefore the best transfer is from the zero AP-3/BLOC/RAB27A/NBEA/LRBA set rather than from `Rab7`.  Because the endpoint distribution puts zero at the median and the nearest direct analogs are all zero, I predicted no BH-significant genes for `Lyst` in this focal class.

## Prediction

`Lyst`: predicted `n_degs = 0`.

## Limits and uncertainty

The requested `Lyst` perturbation itself is completely held out, so there is no direct focal signature to correlate.  None of the AP-3 subunits closest to neuronal AP-3 beta3A besides `Ap3b1`, and none of `Hps1-6`, were represented in the training endpoint table.  The assay measures nuclear RNA in surviving, class-assigned NeuN+ nuclei; it can miss organelle morphology, protein sorting, lysosomal fission, vesicle release, and slowly accumulating degeneration.  Complete or germline `Lyst` loss in specialized secretory/phagocytic cells or aged cerebellum is a stronger perturbation in a different context.  Those caveats make a one- to few-DEG `Lyst` response plausible, especially because `Lamp2` had two genes just under the focal FDR cutoff, but the exact nearest training outcomes favor the integer zero prediction.
