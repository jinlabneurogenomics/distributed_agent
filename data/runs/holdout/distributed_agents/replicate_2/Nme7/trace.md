# Nme7 held-out DEG-count prediction

## Question and resolved ambiguity

The held-out target list contains one perturbation:

| target_name |
|---|
| Nme7 |

I interpreted the task as a point prediction for the hidden number of genes with `pvals_adj < 0.05` in `151 TH Prkcd Grin2c Glut` after acute AAV CRISPR loss of mouse `Nme7`. The hidden row is absent from both supplied inputs, so the prediction has to be transferred from non-held-out perturbations in the same Perturb-seq screen and from target biology.

Two biological annotations for NME7 are plausible a priori:

- NME7 is a centrosomal/gamma-tubulin and ciliary microtubule protein.
- NME7 has also been reported to activate Wnt/beta-catenin signaling through GSK3B Ser9 phosphorylation in hepatocellular carcinoma models.

I treated the first as the primary analogy for this P16 to P37/P44 NeuN+ neuronal assay. The Wnt observation is real but is a cancer and pathway-potentiation context; it is a weaker reason to expect an acute postmitotic neuronal RNA response from a partial CRISPR loss of `Nme7`.

## Sources used

- `[local file: 154_Nme7.csv]` for the exact requested target order.
- `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]` for focal-cell observed training counts.
- `[local file: training_de_all_cell_groups.parquet]` for focal-cell Wilcoxon score/logFC/q-value surfaces of mechanistic comparators.
- Distributed Agents same-experiment corpus `perturbai-july-260713-sourceguard-1773-v1`.
  - `Nme7` itself was not represented in the corpus.
  - `claim:78305cab7c1c7b98458d` summarizes a high-confidence same-experiment claim that represented ciliary trafficking and signaling perturbations in postnatal NeuN+ neurons were buffered at the basal nuclear-RNA level rather than forming a coherent ciliary transcriptional module.
  - `Ift88:F003` specifically compares IFT-B, IFT-A, dynein-2, BBSome, `Cep290`, `Smo`, `Ptch1`, `Ptch2`, `Gli1`, and `Gli2` and finds shared absence of robust DE.
  - `Ttc8:F001` through `Ttc8:F003`, `Arl3:F001` through `Arl3:F003`, and `Rfx3:F001` through `Rfx3:F004` independently report near-null or singleton-only ciliary comparator surfaces in this same screen.
- UniProtKB release 2026_03 and Gene Ontology release 2026-07-26 for curated mouse/human protein function and ciliary annotations.
- External literature:
  - Liu, Choi and Qi, 2014, DOI `10.1091/mbc.E13-06-0339`, PMID `24807905`: human NME7 is a functional gamma-tubulin ring complex component that promotes centrosome-based microtubule nucleation.
  - Ren et al., 2021, DOI `10.1158/0008-5472.CAN-21-1020`, PMID `34764205`: NME7 kinase activity can activate Wnt/beta-catenin signaling through GSK3B phosphorylation in hepatocellular carcinoma.
  - Ji et al., 2025, DOI `10.26508/lsa.202402933`, PMID `39824631`: NME7 localizes to centrosomes/basal bodies and is required for primary-cilium assembly, ciliary microtubule stability, ciliary Smoothened accumulation, and Hedgehog signaling.

## Computation over the training data

The focal count table had 1,674 training perturbations. It was extremely zero-inflated in this cell group: 1,205 of 1,674 targets had `n_degs = 0`, the median was `0`, the 75th percentile was `1`, and the 95th percentile was `18`.

No `Nme1` through `Nme9` family perturbation was present in the training table, so same-family NME paralogs could not be used. I therefore looked for primary-cilium, IFT, BBSome, dynein-2, transition-zone, basal-body/Hedgehog, and Wnt/GSK3/beta-catenin targets in the training count table, then pulled their focal DE rows from the parquet:

```python
flt = (
    (ds.field("group_name") == "151 TH Prkcd Grin2c Glut")
    & ds.field("gene_target").isin(ciliary_or_wnt_targets)
)
```

For each comparator I counted `pvals_adj < 0.05`, recorded the minimum BH-adjusted p-value, inspected top Wilcoxon-score rows, and pivoted the ciliary/Hedgehog targets by measured gene to compute pairwise Spearman correlations among Wilcoxon score vectors. The selected ciliary/Hedgehog set had 17,259 measured genes per perturbation. Across 210 pairwise correlations among 21 ciliary/Hedgehog score vectors, the median Spearman rho was `0.011` and the largest absolute value was only `0.104`; this is expression-pattern evidence against a hidden shared ciliary RNA module.

## Nme7-specific analogs and counterexamples

| training target | focal n_degs | expression-pattern evidence in `151 TH Prkcd Grin2c Glut` | relevance to `Nme7` |
|---|---:|---|---|
| `Ift43` | 0 | 0/17,259 genes at FDR 0.05; minimum q `0.847` | IFT-A/ciliary trafficking comparator for a primary-cilium defect. |
| `Ift81` | 0 | 0 significant genes; minimum q `0.391` | IFT-B comparator for cilium assembly/anterograde transport. |
| `Ift88` | 0 | 0 significant genes; minimum q `1.0` | Canonical IFT-B comparator; Distributed Agents `Ift88:F003` reports that IFT, dynein-2, Cep290, BBSome, Ptch/Gli, and Smo perturbations were zero or singleton-only rather than a robust ciliary RNA program. |
| `Kif3b` | 0 | 0 significant genes; minimum q `1.0` | Kinesin-2/anterograde ciliary transport comparator. |
| `Dync2h1` | 0 | 0 significant genes; minimum q `0.348` | Dynein-2 heavy chain, a retrograde IFT comparator. |
| `Dync2i1` | 0 | 0 significant genes; minimum q `1.0` | Dynein-2 intermediate chain/WDR60 comparator. |
| `Bbs5` | 0 | 0 significant genes; minimum q `0.220` | BBSome/ciliary cargo trafficking comparator; Distributed Agents `Ttc8:F003` and `Bbs5:F003` both reject a robust shared BBSome/IFT neuronal signature. |
| `Cep290` | 0 | 0 significant genes; minimum q `0.650` | Transition-zone/ciliopathy comparator. |
| `Cep120` | 0 | 0 significant genes; minimum q `1.0` | Centriole/centrosome and ciliogenesis comparator. |
| `Rpgrip1l` | 0 | 0 significant genes; minimum q `0.184` | Transition-zone/Joubert-Meckel ciliary-gate comparator. |
| `Ttc21b` | 0 | 0 significant genes; minimum q `0.459` | IFT-A/retrograde-transport ciliopathy comparator. |
| `Cplane1` | 0 | 0 significant genes; minimum q `1.0` | Ciliogenesis/transition-zone assembly comparator. |
| `Dzip1` | 0 | 0 significant genes; minimum q `1.0` | Basal-body/Hedgehog ciliary assembly comparator. |
| `Rfx3` | 0 | 0 significant genes; minimum q `1.0` | RFX ciliogenic transcription-factor comparator; the corpus reports no FDR<0.10 downstream response in any recovered postmitotic neuronal cell group and no down-regulated ciliary target panel. |
| `Smo`, `Ptch1`, `Ptch2`, `Gli1`, `Gli2` | each 0 | all had 0 significant focal genes; minimum q values were all `1.0` | Direct Hedgehog pathway controls. They are relevant because Ji et al. place NME7 upstream of ciliary Smoothened/Hedgehog function, but the pathway is transcriptionally quiescent in this assay. |
| `Ttc8` | 1 | one significant gene, the `Ttc8` self transcript; minimum q `3.1e-05` | BBS8/BBSome comparator showing that even a visibly knocked-down ciliary transcript did not produce downstream FDR genes in this cell group. |
| `Arl3` | 1 | one significant gene, the `Arl3` self transcript; minimum q `0.018` | Ciliary lipidated-cargo comparator; Distributed Agents `Arl3:F003` reports ciliary comparators were orthogonal or flat. |
| `Gsk3b` | 6 | small nonzero surface | Counterexample for the Wnt/GSK3 axis. It is a central multifunctional kinase rather than a ciliary microtubule protein. |
| `Lrp6` | 4; `Fzd2`, `Fzd4`, `Fzd6`, `Fzd9` each 0 | proximal Wnt receptor perturbations were zero to small | Counterexamples to a strong Wnt-receptor-like prediction. |
| `Ctnnb1` | 383; `Tcf7l2` 106 | broad focal signatures | These show Wnt/beta-catenin effectors can be detected, but direct beta-catenin or TCF perturbation is not a close mechanistic phenocopy of partial `Nme7` loss in postnatal neurons. |

## Prediction rationale

The held-out target `Nme7` was predicted as `0` rather than a small positive value. The decisive evidence is internal:

- The closest represented machinery to NME7's best-established neuronal-cell role - primary-cilium assembly/stability and gamma-tubulin/centrosome function - was repeatedly FDR-null in exactly the focal cell group.
- The null was not a single low-powered comparator: IFT-A/IFT-B, kinesin-2, dynein-2, BBSome, transition-zone, basal-body, and Hedgehog transducer/effectors were all measured and had no focal downstream genes at FDR 0.05.
- Whole-score signatures among those comparators were essentially orthogonal, so there was no weak coherent ciliary module just below the FDR surface to extrapolate from.
- The one-DEG ciliary cases, `Ttc8` and `Arl3`, were self-transcript events. They set a plausible upper edge for target-RNA detection, but they do not imply that `Nme7` itself must clear BH correction: target mRNA knockdown in this platform averages only about 18% per guide, and several ciliary targets with visible negative self logFCs, such as `Cplane1` and `Dzip1`, were still nonsignificant.

External biology points the same way for this specific readout. NME7 can be important for centrosome-associated microtubule nucleation and primary cilia, but this screen samples postmitotic NeuN+ brain nuclei at basal state; it does not challenge Hedgehog signaling, image cilia, assay ciliary protein localization, or sample ependymal/airway multiciliated cells. The Wnt/beta-catenin report keeps `0` from being a no-information default, but it is less matched than the ciliary training set: Ren et al. studied hepatocellular carcinoma growth and one-carbon metabolism, whereas proximal Wnt receptor targets in the focal table were zero to small and NME7 is not a direct beta-catenin/TCF transcriptional effector.

## Final point estimate

| target_name | predicted_n_degs |
|---|---:|
| Nme7 | 0 |

## Limits and extrapolation

- `Nme7` had no same-experiment corpus entry and no NME paralog perturbations were available, so the estimate is a pathway transfer rather than a paralog transfer.
- The most informative comparators are primary-cilium/IFT/Hedgehog genes, not direct physical partners of mouse NME7.
- FDR-null snRNA-seq does not prove that cilia were normal: ciliary length, ciliary cargo, Smoothened localization, gamma-tubulin ring activity, and protein loss were not measured.
- The acute mosaic CRISPR design can leave residual mRNA and protein, so a structural ciliary protein may produce a smaller molecular effect than a germline or conditional knockout.
- A one-gene self-transcript hit remains possible for `Nme7`; I assigned `0` because the direct target transcript effect is variable and the pathway evidence argues against any downstream genes crossing FDR 0.05.
