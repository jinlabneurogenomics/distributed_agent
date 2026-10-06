# Pi4ka held-out DEG-count prediction

## Question and interpretation

The manifest `[local file: 177_Pi4ka.csv]` contains one requested held-out perturbation:

| target_name |
|---|
| Pi4ka |

I interpreted `predicted_n_degs` as the number of measured genes in `151 TH Prkcd Grin2c Glut` with Benjamini-Hochberg-adjusted Wilcoxon `pvals_adj < 0.05` after acute AAV-PHP.eB CRISPR loss of the requested gene. `Pi4ka` was absent from the supplied training endpoint and from `gene_target` in the differential-expression parquet, so the prediction had to be transferred from non-held-out perturbations. Zero would mean that no measured gene, including the perturbed transcript itself, is predicted to cross the FDR cutoff.

There was no ambiguity in target order because the manifest had a single row. The main biological ambiguity is that `Pi4ka` is the closest mammalian type-III PI 4-kinase paralog of assayed `Pi4kb`, but the two enzymes maintain different PI4P pools: PI4KA/PI4KIIIalpha is the dominant plasma-membrane PI4P kinase, whereas PI4KB/PI4KIIIbeta is more Golgi-centered. I therefore treated `Pi4kb` as the primary in-dataset analog for expected response scale, not as a phenocopy with the same downstream genes.

## Sources used

- Supplied endpoint CSV: `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
- Supplied DE parquet: `[local file: training_de_all_cell_groups.parquet]`.
- Run-local Distributed Agents same-experiment corpus, release `perturbai-july-260713-sourceguard-1773-v1`, especially the target contexts for `Pi4kb`, `Pitpna`, `Synj1`, and `Dgke`.
- Distributed Agents run-local profile analysis over focal `151 TH Prkcd Grin2c Glut` Wilcoxon score vectors for phosphoinositide-adjacent training perturbations.
- PubMed-indexed literature on PI4K localization and neuronal PI4KA biology:
  - Balla et al. 2005, DOI `10.1091/mbc.e04-07-0578`, PMID `15635101`.
  - Balla et al. 2007, DOI `10.1091/mbc.e07-07-0713`, PMID `18077555`.
  - Nakatsu et al. 2012, DOI `10.1083/jcb.201206095`, PMID `23229899`.
  - Chung et al. 2015, DOI `10.15252/embr.201439151`, PMID `25608530`.
  - Alvarez-Prats et al. 2018, DOI `10.1016/j.celrep.2018.05.019`, PMID `29874576`.
  - Guo et al. 2022, DOI `10.1016/j.celrep.2022.110452`, PMID `35235793`.
  - Suresh et al. 2024, DOI `10.1126/sciadv.adp6660`, PMID `39705356`.

## Computation over the training data

I first checked the focal endpoint distribution. Among 1,674 non-held-out perturbations in the `151 TH Prkcd Grin2c Glut` count CSV, the response was very sparse: the median was 0 DEGs, the 75th percentile was 1 DEG, only 469/1,674 perturbations were nonzero, and the 95th percentile was 18 DEGs. Thus a count near 1 is still an explicit nonzero call in this assay, not an arbitrary rounding of a broad response.

I then filtered the DE parquet to `group_name == "151 TH Prkcd Grin2c Glut"` and to represented phosphoinositide, PI signaling, or lipid-transfer perturbations:

| training perturbation | focal `n_degs` | focal DE evidence |
|---|---:|---|
| `Pi4kb` | 1 | One FDR<0.05 gene: `Tmem50b` up, Wilcoxon score 4.79, logFC 0.43, adjusted p = 0.028. `Rnf145` was the next ranked focal gene and was suggestive but subthreshold, adjusted p = 0.069. |
| `Pitpna` | 21 | 7 up and 14 down FDR<0.05 genes; the strongest was the target transcript itself, `Pitpna` down with adjusted p = 2.48e-16, and downstream genes included `Prkcg`, `Atp2a2`, `Gabra4`, `Rreb1`, `Scg2`, and `Pip5kl1`. |
| `Synj1` | 1 | Only the target transcript was FDR<0.05, `Synj1` down, adjusted p = 3.11e-07; the focal surface had no downstream FDR-scale module. |
| `Dgke` | 1 | Only the target transcript was FDR<0.05, `Dgke` down, adjusted p = 5.97e-08; no downstream gene crossed FDR<0.10. |
| `Pik3cb` | 0 | No FDR<0.05 or FDR<0.10 focal genes. |
| `Pik3r1` | 0 | No FDR<0.05 or FDR<0.10 focal genes. |
| `Pik3r2` | 0 | No FDR<0.05 or FDR<0.10 focal genes. |
| `Plcb1` | 0 | No FDR<0.05 or FDR<0.10 focal genes. |
| `Inpp5k` | 0 | No FDR<0.05 or FDR<0.10 focal genes. |
| `Ppip5k2` | 0 | No FDR<0.05 or FDR<0.10 focal genes. |
| `Pitpnm3` | 0 | No FDR<0.05 or FDR<0.10 focal genes. |

To check whether the obvious pathway neighbors had hidden whole-signature similarity, I computed pairwise comparisons over all measured focal genes among:

`Pi4kb, Pitpna, Synj1, Dgke, Pik3cb, Pik3r1, Pik3r2, Plcb1, Inpp5k, Ppip5k2, Pitpnm3`

using signed Wilcoxon `scores`. The exact Pi4kb-centered score-vector similarities were noise-scale:

| pair | Pearson | cosine | shared FDR<0.05 genes |
|---|---:|---:|---:|
| `Pi4kb` vs `Pitpna` | 0.0117 | 0.0107 | 0 |
| `Pi4kb` vs `Synj1` | -0.0009 | -0.0011 | 0 |
| `Pi4kb` vs `Dgke` | -0.0263 | -0.0263 | 0 |
| `Pi4kb` vs `Pik3cb` | -0.0302 | -0.0294 | 0 |
| `Pi4kb` vs `Pik3r1` | -0.0176 | -0.0159 | 0 |
| `Pi4kb` vs `Pik3r2` | 0.0185 | 0.0179 | 0 |
| `Pi4kb` vs `Plcb1` | 0.0214 | 0.0206 | 0 |
| `Pi4kb` vs `Inpp5k` | 0.0339 | 0.0337 | 0 |
| `Pi4kb` vs `Ppip5k2` | 0.0101 | 0.0091 | 0 |
| `Pi4kb` vs `Pitpnm3` | 0.0309 | 0.0307 | 0 |

These values match the Distributed Agents same-experiment corpus summary for `Pi4kb`: only three FDR<0.10 gene-cell events were detected experiment-wide for `Pi4kb`; the focal effect was the tiny `Tmem50b`/`Rnf145` ER/Golgi/sterol-ligase candidate module; and same-dataset phosphoinositide relatives, including `Pitpna`, `Synj1`, `Plcb1`, `Inpp5k`, `Ppip5k2`, `Pitpnm3`, and PI3K subunits, did not converge with `Pi4kb`.

The same corpus also made two important counterpoints. First, `Pitpna` produced a real 21-DEG response in this focal cell group, showing that phosphoinositide-related perturbations can be transcriptional here. Second, the `Pitpna` response was not a generic PI/PLC/PKC response: `Pitpnm3`, `Pi4kb`, `Synj1`, `Plcb1`, `Prkca`, and `Prkcg` did not reproduce its FDR genes in matched responder groups. The `Synj1` and `Dgke` corpus contexts likewise described singleton/self or downstream-null phenotypes with near-zero whole-profile neighbors despite strong canonical lipid or vesicle biology. I therefore did not pool the full 21 `Pitpna` DEGs into the `Pi4ka` estimate.

## Target-specific biological transfer

### Pi4ka

`Pi4ka` encodes PI4KIIIalpha, a type-III phosphatidylinositol 4-kinase. External cell-biological work makes it a mechanistically serious neuronal gene: PI4KIIIalpha is required for dynamic resynthesis of plasma-membrane PI4P/PI(4,5)P2 after PLC-linked receptor activation (Balla et al. 2005; Balla et al. 2007), is recruited to the plasma membrane by the EFR3/TTC7/FAM126 complex (Nakatsu et al. 2012; Chung et al. 2015; Suresh et al. 2024), and acute PI4KIIIalpha inhibition or silencing in rodent hippocampal neurons impairs activity-dependent PI4P synthesis, AMPA-receptor surface delivery, LTP, and memory (Guo et al. 2022). Conditional `Pi4ka` loss in Schwann cells also causes major membrane and actin phenotypes during myelination (Alvarez-Prats et al. 2018), although that PNS glial context is outside the NeuN-enriched central-neuron assay here.

The best in-dataset analog is `Pi4kb`, because it is the other type-III PI4K represented in the focal training data. Its observed focal count was 1 rather than 0, so the closest paralog argues against forcing `Pi4ka` all the way to a definite zero. The only FDR<0.05 `Pi4kb` gene was `Tmem50b`, with `Rnf145` just below FDR<0.10, and the same-experiment corpus interpreted this as a small ER/Golgi/sterol quality-control echo rather than a global PI4P or organelle-stress program. PI4KA is not the same enzyme: the literature places PI4KA primarily at the plasma membrane and PI4KB primarily at Golgi-associated PI4P production, so I would not expect the exact `Tmem50b`/`Rnf145` pair to transfer feature-by-feature. Still, both kinases sit upstream of PI4P pools, and the fact that the PI4KB paralog was barely nonzero is the most direct assay-calibrated evidence for a tiny PI4KA RNA footprint.

`Pitpna` is a counterexample to complete buffering of lipid-transfer biology in this focal cell type, but it is also a counterexample to broad family pooling. Its 21-DEG response involved the target itself plus synaptic/Ca2+/cytoskeletal genes such as `Prkcg`, `Atp2a2`, `Gabra4`, `Scg2`, and `Pip5kl1`, and it was essentially uncorrelated with `Pi4kb` over the focal score vector. `Synj1`, `Dgke`, `Plcb1`, `Inpp5k`, `Ppip5k2`, and the PI3K subunits were flat or self-only. Those training data argue that the basal postnatal snRNA-seq assay often does not turn phosphoinositide or vesicle physiology into a broad nuclear transcriptional program, especially under mosaic AAV CRISPR where the average target mRNA decrease per gRNA is modest.

I therefore made a **nonzero but singleton-scale** prediction for `Pi4ka`. The nonzero side is driven by external PI4KA plasma-membrane/neuronal essentiality plus the same-enzyme-class `Pi4kb` singleton. The magnitude is held to 1 DEG because the focal training data show no shared broad phosphoinositide kinase/turnover module, `Pi4kb` itself had only one FDR<0.05 gene, and nearby PI/PLC/PI3K perturbations were zero or singleton-only. A prediction of 0 would underweight PI4KA's direct PI(4,5)P2-replenishment and activity-dependent dendritic role; a Pitpna-like double-digit count would overread one lipid-transfer perturbation that the same dataset explicitly separates from `Pi4kb` and other PI-cycle genes.

## Final point prediction

| target_name | predicted_n_degs |
|---|---:|
| Pi4ka | 1 |

## Limits

- `Pi4ka` itself was completely held out, so no focal `Pi4ka` self-knockdown statistic or whole-signature neighbor could be measured.
- PI4KA and PI4KB act on different PI4P pools and use different recruitment complexes; `Pi4kb` is the closest assayed enzyme but an imperfect paralogic proxy.
- The PI4KA plasma-membrane complex genes most likely to be precise comparators, such as `Efr3a`, `Efr3b`, `Ttc7a`, `Ttc7b`, `Fam126a`, and `Fam126b`, were not available as non-held-out focal perturbations in the endpoint CSV.
- snRNA-seq at basal state cannot see PI4P, PI(4,5)P2, AMPAR trafficking, evoked LTP, or protein relocalization directly. A true electrophysiological PI4KA phenotype could therefore coexist with zero or one FDR-level nuclear RNA changes.
- The prediction assumes that a sparse P16 AAV CRISPR perturbation in surviving NeuN+ nuclei behaves more like partial acute loss than like complete germline or cell-type-specific deletion. Strong effects in Schwann cells or after hippocampal activity stimulation are informative about function but not directly quantitative for this focal thalamic-like glutamatergic population.
