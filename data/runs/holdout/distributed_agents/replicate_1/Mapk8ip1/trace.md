# DEG-count prediction trace

## Question and endpoint

The task asks for one point prediction for each requested held-out perturbation in `151 TH Prkcd Grin2c Glut` neurons. In this run the requested CSV contains exactly one target:

```text
Mapk8ip1
```

I interpreted `predicted_n_degs` as the integer number of measured genes, including the target transcript if it passes correction, whose Wilcoxon Benjamini-Hochberg adjusted p-value would be below 0.05 for acute AAV-CRISPR loss of `Mapk8ip1` in the recovered `151 TH Prkcd Grin2c Glut` nuclei. `Mapk8ip1` was held out completely, so neither its focal-cell DEG count nor its expression signature was present in the supplied Parquet or the focal training-count CSV.

The requested endpoint is directly observed for the 1,674 non-held-out training perturbations. It is absent only for the held-out target being predicted. Matched-nucleus recovery, target-transcript log-fold change, and other genes' changes in `Mapk8ip1` RNA are context, not direct evidence for the held-out endpoint.

## Sources used

- Declared focal training endpoint: `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
- Declared differential-expression Parquet: `training differential-expression dataset`.
- Run-local task manifest: `single-target request for Mapk8ip1`.
- Run-local dataset portrait, task bindings, coverage, capability, and measurement-registry JSON under `codex_runtime/pipeline`.
- Same-experiment interpreted corpus: `perturbai-july-260713-sourceguard-1773-v1`, used only to understand visible `Map2k1`, `Mapk1`, `Mapk9`, `Mapkbp1`, `Kif5a`, `Kif5c`, `Klc1`, `Klc2`, and `App` signatures. This is a semantic layer over the same Perturb-seq experiment, not independent replication.
- PubMed literature for `Mapk8ip1/JIP1` biology:
  - Whitmarsh et al. 2001, "Requirement of the JIP1 scaffold protein for stress-induced JNK activation", PMID 11562351, DOI 10.1101/gad.922801.
  - Verhey et al. 2001, "Cargo of kinesin identified as JIP scaffolding proteins and associated signaling molecules", PMID 11238452, DOI 10.1083/jcb.152.5.959.
  - Matsuda et al. 2003, "Amyloid beta protein precursor (AbetaPP), but not AbetaPP-like protein 2, is bridged to the kinesin light chain by the scaffold protein JNK-interacting protein 1", PMID 12893827, DOI 10.1074/jbc.M304379200.
  - Morel et al. 2018, "JIP1-Mediated JNK Activation Negatively Regulates Synaptic Plasticity and Spatial Memory", PMID 29540552, DOI 10.1523/JNEUROSCI.1913-17.2018.
  - Chiba et al. 2014, "Quantitative analysis of APP axonal transport in neurons: role of JIP1 in enhanced APP anterograde transport", PMID 25165140, DOI 10.1091/mbc.E14-06-1111.

## Dataset calculations

I treated the focal training-count CSV as the authoritative scalar endpoint for visible perturbations and used the Parquet only to inspect signatures and DEG identities for biologically relevant comparators.

Basic calibration from the focal training counts:

- 1,674 visible biological perturbations had focal `n_degs`.
- 469/1,674 were nonzero.
- The distribution was highly skewed: median 0, 75th percentile 1, 90th percentile 2, 95th percentile 18, mean 14.1, maximum 2,677.
- Thus a target with pathway neighbors at 0 or 1 DEG belongs near the assay floor, not near the high-response tail.

I queried the declared Parquet for the focal cell group and for JNK/MAPK and kinesin/APP analogs, counting rows satisfying `pvals_adj < 0.05` and listing the significant measured genes. The biologically relevant visible focal counts were:

| training perturbation | focal `n_degs` | focal significant genes at FDR < 0.05 |
| --- | ---: | --- |
| `Mapk9` | 0 | none |
| `Mapk1` | 0 | none |
| `Mapkbp1` | 0 | none |
| `Map3k7` | 0 | none |
| `Map2k2` | 0 | none |
| `Map2k6` | 0 | none |
| `Jund` | 0 | none |
| `Map2k1` | 4 | `Vgf`, `Ptpn5`, `Etv5`, `Unc13a`, all down |
| `App` | 1 | `App` only |
| `Klc1` | 1 | `Klc1` only |
| `Klc2` | 1 | `Klc2` only |
| `Kif1a` | 1 | `Kif1a` only |
| `Kif5a` | 1 | `Kif5a` only |
| `Kif5c` | 1 | `Kif5c` only |
| `Kifbp` | 2 | `Kifbp`, `Srebf2` |
| `Kif1b`, `Kif11`, `Kif2a`, `Kif3b`, `Dync2h1`, `Dync2i1` | 0 | none |

Across all neuronal groups, the same analogs were sparse rather than broadly reactive: `Mapk9` had zero downstream DEGs at the corpus' FDR < 0.10 threshold; `Mapk1` had only a self-transcript call in `155 MB Glut`; `Kif5c` had no downstream FDR < 0.10 genes despite self-transcript changes; `Kif5a` had self-transcript calls in a few groups and no downstream FDR < 0.10 genes; and `App` produced its own transcript decrease without an APP-processing or AICD-responsive downstream program. The `Map2k1` report resolved its four focal DEGs as a small ERK-linked neuropeptide/synaptic module anchored by `Vgf`, `Ptpn5`, `Etv5`, and `Unc13a`, which is mechanistically upstream of ERK rather than a JIP1/JNK module.

## Target-specific reasoning

### Mapk8ip1

`Mapk8ip1` encodes JIP1, a scaffold that binds JNK-pathway kinases and is required for stress-induced JNK activation in hippocampal neurons in the setting of excitotoxic or anoxic stress. JIP1 also binds kinesin light chain through its C terminus and can bridge APP to kinesin-1, and JIP1-deficient neurons have reduced fast APP anterograde transport. A point mutation that disrupts JIP1-mediated JNK activation changes hippocampal NMDAR currents and NMDAR-mediated gene expression in mice.

Those mechanisms make `Mapk8ip1` a plausible neuronal signaling and transport gene, but the causal chain to the requested endpoint is weak:

```text
AAV-CRISPR Mapk8ip1 loss
-> reduced JIP1 scaffold function
-> altered stress-evoked JNK assembly and APP/kinesin cargo handling
-> possible changes in plasticity or transport programs
-> survivor-conditioned nuclear RNA in thalamic glutamatergic neurons 3-4 weeks later
-> Wilcoxon FDR < 0.05 DEG count
```

The represented training perturbations probe both major branches of that chain. The JNK side was locally silent: `Mapk9` had 0 focal DEGs and the corpus found no corrected AP-1, immediate-early, apoptosis, or FoxO/autophagy program anywhere in its measured surface; `Mapkbp1`, `Map3k7`, `Map2k2`, `Map2k6`, and `Jund` were also zero in the focal class. The ERK kinase `Mapk1` was focal-cell zero; the only nonzero MAPK neighbor, `Map2k1`, caused a four-gene ERK-output signature, which is a counterexample showing that this cell type can detect a small MAPK transcriptional program but not a direct analog for JIP1/JNK loss.

The transport side also argues against a broad DEG response. `App`, `Klc1`, `Klc2`, `Kif1a`, `Kif5a`, and `Kif5c` were one-gene calls in the focal class, and in each of those cases the sole FDR < 0.05 gene was the perturbed transcript itself. `Kifbp` was only 2 DEGs. Same-experiment reports for `Kif5a`, `Kif5c`, and `Klc1/Klc2` found no convergent broad kinesin or APP/JNK transcriptome, and the `App` report found no FDR-supported downstream APP-processing response.

Putting those together, the within-dataset evidence dominates the prediction: the closest visible genetic perturbations to JIP1's JNK scaffold role and its kinesin/APP cargo role are at 0, 1, or 2 focal DEGs. Because target-transcript drop is not a reliable editing or effect-size readout in this assay and `Mapk9`/`Mapk1` themselves did not yield focal self-transcript calls, I did not add a forced self-DEG for held-out `Mapk8ip1`. I therefore predict no gene will cross FDR 0.05:

```text
Mapk8ip1 predicted_n_degs = 0
```

## Limits and uncertainty

This prediction is an extrapolation because no `Mapk8ip1`, `Mapk8ip2`, or `Mapk8ip3` perturbation is visible in the training focal-count table. The PubMed support comes mostly from hippocampal neurons, cultured cells, whole-animal mutants, or transport biochemistry rather than acute mosaic P16 CRISPR in thalamic glutamatergic nuclei. JIP1's scaffold effect can be conditional on stress or synaptic activation, and a quiescent snRNA-seq snapshot of recovered nuclei can miss earlier selection, localized axonal transport defects, phosphorylation changes, and subcellular phenotypes. The point estimate is therefore a low-response prediction, not evidence that `Mapk8ip1` is biologically irrelevant.
