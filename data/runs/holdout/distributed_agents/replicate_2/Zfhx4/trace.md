# DEG-count prediction for `151 TH Prkcd Grin2c Glut`

## Question and resolved ambiguities

The held-out manifest `[local file: 268_Zfhx4.csv]` contains one requested perturbation:

```text
Zfhx4
```

I interpreted `n_degs` as the number of measured genes in the held-out `Zfhx4` knockout with Benjamini-Hochberg adjusted Wilcoxon `pvals_adj < 0.05` in `151 TH Prkcd Grin2c Glut` nuclei, using the same effect convention as the training parquet: positive log fold change is knockout versus matched non-targeting control. Because `Zfhx4` was absent from both supplied training inputs, I did not use any `Zfhx4` differential-expression row or DEG count from this screen.

## Sources used

- Training endpoint CSV: `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
- Differential-expression parquet: `[local file: training_de_all_cell_groups.parquet]`.
- Internal same-experiment corpus: Distributed Agents PerturbAI corpus release `perturbai-july-260713-sourceguard-1773-v1`. This release had no `Zfhx4` Finding or Claim, so it was used for same-screen comparator interpretation rather than for the held-out target itself.
- NCBI PubMed literature:
  - Kostich and Sanes, 1995, DOI `10.1002/aja.1002020206`, PMID `7537552`.
  - Chudnovsky et al., 2014, DOI `10.1016/j.celrep.2013.12.032`, PMID `24440720`.
  - Zhang et al., 2021, DOI `10.1093/jmcb/mjaa081`, PMID `33475140`.
  - Perez Baca et al., 2025, DOI `10.1016/j.ajhg.2025.04.008`, PMID `40367947`.

## Computations over the supplied data

The training count table contains 1,674 focal-cell perturbations. It is highly zero-inflated:

| class | count |
|---|---:|
| `n_degs == 0` | 1,205 |
| `1 <= n_degs < 10` | 363 |
| `10 <= n_degs < 100` | 63 |
| `n_degs >= 100` | 43 |

The median was 0, the 75th percentile was 1, the 90th percentile was 2, and the 95th percentile was 18. That distribution makes zero the baseline prediction unless the held-out gene has a mechanistically specific reason to look like one of the rare broad responders.

I then read the focal cell class from the parquet with PyArrow predicate pushdown on `group_name == "151 TH Prkcd Grin2c Glut"` and `gene_target` restricted to biologically plausible comparators. The focal class occupied row groups 546 to 580, 29,926,757 rows before target filtering. For the 35 comparator targets below, 604,065 rows were read, corresponding to 17,259 measured genes per perturbation. For each comparator I counted genes with `pvals_adj < 0.05` and checked the lowest-FDR genes and the matched nucleus counts.

The most relevant exact and near-exact training comparators were:

| comparator | why compared | observed focal `n_degs` | focal signature evidence |
|---|---|---:|---|
| `Zfhx2` | closest represented ZFHX family member | 0 | 203 perturbed and 23,679 control nuclei; no gene had focal FDR < 0.05 and the top focal adjusted p-values were all 1. The Distributed Agents corpus also reports that a model-wide `Zfhx2` Wilcoxon-score neighbor search found only near-zero correlations and only a single weak downstream hit in another cell group. |
| `Zfp423` | large zinc-finger transcription factor with a real thalamic response, useful as a counterexample showing that the assay could detect a developmental TF when active | 150 | 160 perturbed nuclei; the top focal genes included `Grid2ip` down, `Cd47` down, `Ntsr1` up, `Kcnab3` up, `Syt13` down, and `Grin2c` down. The same-experiment corpus describes this as a cell-surface/extracellular-matrix and thalamic subtype program and notes that known or obvious `Zfp423` relatives did not phenocopy it. |
| `Chd4` | ZFHX4 has been reported to interact with CHD4/NuRD in glioblastoma tumor-initiating cells and neural precursors | 100 | 163 perturbed nuclei; the top focal genes included `Begain` up, `Cpne7` down, `Zfp467` up, `Ramp3` down, `Pygm` up, and `Sorbs1` down. However, the same-experiment corpus reports that measured NuRD-related perturbations did not phenocopy `Chd4`. |
| `Gatad2b` | NuRD-associated subunit/control for the CHD4 analogy | 1 | Only `Gatad2b` itself was significant in the focal group. The corpus specifically notes that `Gatad2b` had zero downstream FDR genes in 151 despite a self-transcript drop under the FDR < 0.10 analysis used there. |
| `Mbd2` and `Mbd5` | methyl-CpG/NuRD-adjacent chromatin controls | 0, 0 | Both had no focal FDR < 0.05 gene. Distributed Agents Claims state that represented NuRD/MBD-adjacent chromatin perturbations are target-selective rather than one generic NuRD loss signature. |
| `Mecp2` | methyl-CpG reader and NuRD/NCoR-adjacent disease regulator | 16 | Detectable but small focal signature, with `Nap1l5` up and `Ache` down among the strongest genes; this again argues for target-selective chromatin effects rather than transferring the `Chd4` count to `Zfhx4`. |

I also used a broader panel of postnatal developmental and neuronal transcription-factor perturbations as calibration. In the exact focal class, `Bcl11a`, `Bcl11b`, `Satb2`, `Tbr1`, `Neurod2`, `Tcf4`, `Tcf12`, `Tcf20`, `Nfia`, `Nfib`, `Nfix`, `Sox11`, `Zeb2`, `Tead1`, and `Cux1` all had 0 DEGs; `Cux2` and `Mef2c` each had 1; `Sox5` had 2; `Mef2a` had 4; and `Zeb1` had 15. The corpus summarizes the same pattern for several families: many embryonic identity or homeobox transcription-factor perturbations were flat or singleton-only in the P16/P37 postmitotic neuronal assay, whereas the exceptions were target-specific. `Rora` with 278 DEGs and `Tcf7l2` with 106 DEGs are important thalamic TF counterexamples, but their curated signatures are thalamic terminal excitability, subtype, or Wnt-linked programs; I found no evidence that `Zfhx4` belongs to either module.

## Biological rationale for `Zfhx4`

`Zfhx4` is a zinc-finger homeobox transcription factor with a real developmental nervous-system role. Kostich and Sanes cloned `zfh-4` and found high embryonic expression in brain and muscle, regionally enriched in midbrain and hindbrain and declining toward adulthood (Kostich and Sanes 1995, DOI `10.1002/aja.1002020206`, PMID `7537552`). Germline mouse `Zfhx4` ablation causes early postnatal lethality through a brainstem respiratory-center defect, with loss of `Phox2b` and Math1/Atoh1 in the retrotrapezoid nucleus; ChIP-seq supported `Phox2b` as a direct Zfhx4 target in that developmental brainstem context (Zhang et al. 2021, DOI `10.1093/jmcb/mjaa081`, PMID `33475140`). Human loss-of-function variants cause a neurodevelopmental disorder, and neural-progenitor CUT&RUN shows ZFHX4 binding near genes involved in embryonic, neuronal, and axonal development (Perez Baca et al. 2025, DOI `10.1016/j.ajhg.2025.04.008`, PMID `40367947`). ZFHX4 can also interact with CHD4 and overlap CHD4 genomic binding in glioblastoma tumor-initiating cells (Chudnovsky et al. 2014, DOI `10.1016/j.celrep.2013.12.032`, PMID `24440720`).

Those papers make `Zfhx4` a plausible regulator, but they point mainly to embryonic neural progenitors, hindbrain/brainstem respiratory neurons, zebrafish craniofacial patterning, dopaminergic differentiation, or glioblastoma stem-like cells. The requested assay perturbs sparse postmitotic neurons starting at P16 and reads out recovered NeuN-positive nuclei in a juvenile thalamic glutamatergic class, not the developmental brainstem or a proliferating precursor population.

The best within-dataset anchor is therefore `Zfhx2`: the same broad ZFHX family was represented and was completely flat in the target focal class. The positive ZFHX4-CHD4 literature is too context-specific to promote `Zfhx4` toward `Chd4`'s 100-DEG focal count because the internal screen shows that even assayed NuRD/MBD-adjacent perturbations split sharply: `Chd4` is a selective 151 responder, while `Gatad2b`, `Mbd2`, and `Mbd5` are null or essentially self-only. The broad developmental-TF panel gives the same calibration, with most postnatal identity TFs producing zero or near-zero focal counts unless they map onto a specific active thalamic maintenance program. I therefore predict no FDR 0.05 DEG for `Zfhx4` in `151 TH Prkcd Grin2c Glut`.

## Final point estimate

| target | predicted `n_degs` |
|---|---:|
| `Zfhx4` | 0 |

## Limits

The prediction is an extrapolation: `Zfhx4` itself is absent from the training parquet, the Distributed Agents release has no `Zfhx4` Finding or Claim, and the public ZFHX4 literature is mostly outside P16-to-P37 thalamic glutamatergic neurons. `Zfhx2` is the closest represented family member, but ZFHX proteins need not be interchangeable. Conversely, `Chd4` is a real internal responder and ZFHX4 has a reported CHD4 interaction in GBM and neural precursor systems, so a small-to-medium thalamic effect cannot be excluded. The zero call is driven by focal training calibration and by the lineage-window mismatch of known `Zfhx4` biology, not by evidence that the gene is biologically unimportant.
