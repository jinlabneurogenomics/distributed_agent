# DEG-count prediction trace

## Question and endpoint

I interpreted the task as a point prediction of the held-out `151 TH Prkcd Grin2c Glut` endpoint for the requested perturbation `Irf7`. The endpoint is the assay-specific number of measured genes whose Wilcoxon Benjamini-Hochberg adjusted p value is below 0.05 in this focal thalamic glutamatergic neuronal class after acute sparse AAV-CRISPR loss of function.

The held-out `Irf7` perturbation itself is absent from both declared inputs, so there is no direct `n_degs` or expression signature for `Irf7`. The count below is an extrapolation from visible training perturbations and from external IRF7 biology, not a recovered measurement.

## Sources used

- Declared training counts: `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
- Declared differential-expression parquet: `training differential-expression dataset`; I queried only the `151 TH Prkcd Grin2c Glut` rows needed for inflammatory and interferon-pathway analogs.
- Requested-target manifest: `single-target request for Irf7`.
- Run-local July PerturbAI same-experiment corpus: release `perturbai-july-260713-sourceguard-1773-v1`. I used its compact report and Finding content as an interpretation layer over the same DE experiment, especially its summaries for `Irf1`, `Tlr7`, and interferon-pathway nulls. This corpus is not independent replication.
- PubMed for external biology. The key external prior is Honda et al. 2005, *Nature*, DOI `10.1038/nature03464`, PMID `15800576`, which established that IRF7 is essential for type-I-interferon induction downstream of both virus-activated and TLR/MyD88 pathways, with particularly strong biology in plasmacytoid dendritic cells and systemic antiviral responses.

## Dataset calculations

The focal-cell training endpoint is sparse. The training CSV contains 1,674 visible biological perturbations; 1,205 have `n_degs = 0`, the median is 0, the 90th percentile is 2, the 95th percentile is 18, and the maximum is 2,677. Thus a new target with no strong analog in a transcriptionally active pathway should default near zero unless the visible analogs argue otherwise.

For `Irf7`, I treated the following training perturbations as the most relevant within-dataset analogs:

| training perturbation | observed `151 TH Prkcd Grin2c Glut` `n_degs` | expression-pattern evidence in the focal class |
|---|---:|---|
| `Irf1` | 0 | no FDR 0.05 genes; the three smallest adjusted p values were all 1.0 |
| `Irf2` | 0 | no FDR 0.05 genes; all checked ISG/MHC/inflammatory sentinels had FDR 1.0 |
| `Irf3` | 0 | no FDR 0.05 genes; no corrected movement of `Irf7`, `Stat1`, `Isg15`, `Ifit1`, `Oas1a`, `Psmb9`, `B2m`, `H2-D1`, `Cxcl10`, `Il6`, `Fos`, or `Nfkbia` |
| `Irf5` | 0 | no FDR 0.05 genes; closest row was off-pathway `Tulp3`, FDR 0.789 |
| `Irf8` | 0 | no FDR 0.05 genes; closest row was off-pathway `Panx2`, FDR 0.121 |
| `Irf9` | 0 | no FDR 0.05 genes; no ISGF3/ISG program after loss of the canonical `Stat1`/`Stat2` partner |
| `Ifnar1` | 0 | no FDR 0.05 genes; no detectable loss of tonic type-I-IFN target genes |
| `Ifnar2` | 0 | no FDR 0.05 genes; no detectable loss of tonic type-I-IFN target genes |
| `Ifngr1` | 0 | no FDR 0.05 genes; raw movement of some antigen-presentation genes remained FDR 1.0 |
| `Ifngr2` | 0 | no FDR 0.05 genes; raw movement of `Stat1` and `Nlrc5` remained FDR 1.0 |
| `Stat1` | 1 | the only FDR 0.05 hit was the self transcript `Stat1`, not an interferon-stimulated secondary program |
| `Stat2` | 0 | no FDR 0.05 genes; no `Stat1`/`Stat2`/`Irf9` ISGF3 output |
| `Ifih1` | 0 | no MDA5/type-I-IFN output in the focal class |
| `Tlr3` | 0 | no endosomal TLR inflammatory or IFN output |
| `Tlr7` | 0 | no FDR 0.05 genes in the direct TLR7 comparator |
| `Tlr8` | 0 | no endosomal TLR inflammatory or IFN output |
| `Traf3` | 0 | no FDR 0.05 genes despite its role upstream of IRF3/IRF7 in innate signaling |
| `Nfkb1` | 0 | no FDR 0.05 genes; no NF-kappaB inflammatory program |
| `Rel` | 0 | no FDR 0.05 genes; no NF-kappaB-family inflammatory program |

The focal Parquet slice contained 431,475 rows for these 25 checked IRF/IFN/TLR/NF-kappaB analogs. All checked analogs had zero focal FDR 0.05 calls except `Stat1`, whose only call was `Stat1` itself at logFC -1.300 and FDR 0.027. Across the core sentinels `B2m`, `Cxcl10`, `Fos`, `H2-D1`, `Ifit1`, `Il6`, `Irf7`, `Isg15`, `Nfkbia`, `Oas1a`, `Psmb9`, and `Stat1`, every analog had adjusted p value 1.0 except the `Stat1` self row. The measured `Irf7` RNA was also FDR 1.0 in each analog, for example FDR 1.0 after `Irf1`, `Irf3`, `Irf9`, `Ifnar1`, `Ifnar2`, `Tlr7`, and `Traf3` perturbation.

This was the relevant operation over the Parquet: filter row groups to the focal `group_name`, restrict `gene_target` to mechanistic analogs, and inspect both their FDR<0.05 burdens and the expected interferon/inflammatory sentinel genes. I did not use the unavailable ranked-supervision `dataset.perturbseq_features` workbench, because this is a scalar count prediction with an unranked one-target manifest.

## Target-specific prediction

### `Irf7`

`Irf7` encodes the IRF7 transcription factor. Externally, it is a central inducible amplifier of type-I-interferon production: Honda et al. showed that Irf7-deficient mice and cells are defective for IFN-alpha/beta induction in antiviral and TLR/MyD88 settings. That mechanism predicts a broad RNA phenotype only if the assayed cell has active viral, TLR7/9, TLR3/MDA5/RIG-I, IFNAR/JAK-STAT, or related basal interferon drive.

The training experiment argues that those conditions were not present in `151 TH Prkcd Grin2c Glut` nuclei. The most direct transcription-factor analogs `Irf1`, `Irf2`, `Irf3`, `Irf5`, `Irf8`, and `Irf9` were all exact zeros in the focal training endpoint. The two type-I-IFN receptor chains, `Ifnar1` and `Ifnar2`, were exact zeros, and loss of the ISGF3 components did not uncover a tonic program: `Stat2` was zero and `Stat1` had only its self row. Pattern-recognition and upstream regulators also stayed flat: `Ifih1`, `Tlr3`, `Tlr7`, `Tlr8`, `Traf3`, `Nfkb1`, and `Rel` all had zero focal FDR 0.05 genes.

The same-experiment July corpus reaches the same interpretation for visible analogs rather than just reporting counts. Its `Irf1` report noted that 31 canonical IFN-stimulated, antigen-presentation, and inflammatory transcripts, including `Irf7`, `Isg15`, `Ifit1/2/3`, `Oasl1/2`, `Rsad2`, `Usp18`, `Stat1`, `Stat2`, `Tap1`, `Psmb8`, `Psmb9`, `B2m`, `H2-D1`, `H2-K1`, `Nlrc5`, `Cxcl10`, and `Il12b`, were absent from the `Irf1` DE surface. The `Tlr7` report likewise found no cytokine, chemokine, AP-1/NF-kappaB, MyD88-proximal, or IFN-stimulated output after TLR7 loss. These are exact same-assay observations, so they support a context gate: acute neuronal basal loss of an innate immune factor did not generate a sustained nuclear RNA phenotype in the sampled postnatal NeuN+ cells.

I therefore predict no FDR 0.05 DEGs for `Irf7`: the most appropriate within-dataset comparators are exact or near-exact zeros, and the external reason to expect a large IRF7 phenotype depends on infection, endosomal TLR ligand, IFN priming, or innate-immune/glial lineages that the focal NeuN+ thalamic glutamatergic assay did not supply. The main counterexample is only conceptual, not within-dataset: IRF7 loss can be profound in virus- or TLR-stimulated immune settings. I did not give that external immune prior enough weight to move the count above zero because the visible neuronal perturbations of upstream receptors and downstream IFN-receptor/STAT/IRF mediators all lacked the relevant sentinels.

Point prediction: `0`.

## Limits

- `Irf7` itself was held out; its guide recovery, matched perturbed-cell count, and signature in the focal class are unknown.
- DNA indels and protein loss were not measured. As in the source experiment, unchanged target RNA is not evidence against functional editing.
- The zero prediction is a prediction for a specific unstimulated, P16-to-P37/44, sparse NeuN+ snRNA-seq endpoint. It should not be transferred to plasmacytoid dendritic cells, macrophages, astrocytes, microglia, viral infection, TLR agonist exposure, or IFN-primed conditions.
- `n_degs` is power- and assay-dependent. A true but tiny `Irf7` effect in a rare neuronal substate could still produce zero BH-significant genes.
