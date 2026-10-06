# Held-out DEG-count prediction for `151 TH Prkcd Grin2c Glut`

## Question and interpretation

The held-out target list for this run contains exactly one perturbation, `Ddr2`. I interpreted the task as a point prediction of the number of genes that would pass `pvals_adj < 0.05` in the `151 TH Prkcd Grin2c Glut` focal cell group if `Ddr2` had been included in the same Perturb-seq experiment.

The endpoint is an assay-specific single-cell Wilcoxon/BH count, not a count of all real biological changes. Because this screen used sparse AAV CRISPR loss of function in postmitotic NeuN+ nuclei, I treated developmental germline phenotypes as evidence about pathway identity, but not as direct evidence that a juvenile thalamic glutamatergic nucleus should produce many DEGs after acute mosaic editing.

## Sources used

- `training_de_all_cell_groups.parquet`: per-gene log fold changes and Wilcoxon statistics for every non-held-out perturbation.
- `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`: observed `n_degs` for 1,674 non-held-out focal-cell perturbations.
- `053_Ddr2.csv`: held-out manifest; it contains only `Ddr2`.
- Distributed Agents corpus `perturbai-july-260713-sourceguard-1773-v1`. `Ddr2` itself had no frozen same-experiment Claim. The corpus did have a moderate Claim that represented integrin and laminin-receptor perturbations, including `Itga2` and `Itgb1`, did not produce a shared basal postmitotic neuronal adhesion or beta1/focal-adhesion transcriptional module.
- Distributed Agents runtime signed-profile comparison for focal-cell `logfoldchanges`, run against the 1,674 eligible observed perturbations for ECM/collagen and receptor-tyrosine-kinase anchors.
- PubMed literature on DDR2 biology:
  - Shrivastava et al. 1997, DOI `10.1016/S1097-2765(00)80004-0`, PMID 9659900: DDR1/DDR2 are non-integrin collagen receptor tyrosine kinases.
  - Xu et al. 2010, DOI `10.1016/j.matbio.2010.10.004`, PMID 21044884: DDR2 binds fibrillar collagen motifs in collagens II and III, while DDR1 has broader collagen-IV recognition.
  - Carafoli and Hohenester 2012, DOI `10.1016/j.bbapap.2012.10.014`, PMID 23128141: DDRs are slowly and persistently activated by triple-helical collagen.
  - Xu et al. 2004, DOI `10.1074/jbc.M411036200`, PMID 15509586: collagen-II/DDR2 signaling can induce `MMP13` in chondrocytes in osteoarthritis-like cartilage.
  - Ge et al. 2016, DOI `10.1002/jbmr.2893`, PMID 27341689; Mohamed et al. 2022, DOI `10.1038/s41413-021-00182-w`, PMID 35140200: DDR2 has strong skeletal-progenitor, osteoblast, and chondrocyte functions through MAPK/RUNX2 and related extracellular-matrix responses.
  - Min et al. 2023, DOI `10.1038/s41467-023-42626-3`, PMID 37919278: human tauopathy integrative data prioritized glial `DDR2`, consistent with DDR2 being most salient in non-neuronal or disease-remodeling compartments rather than basal postmitotic neurons.

## Dataset checks

I read the manifest and confirmed that the held-out target was `Ddr2` only. The focal-cell training endpoint was extremely zero-inflated:

| statistic | value |
| --- | ---: |
| training perturbations | 1,674 |
| mean `n_degs` | 14.1 |
| median | 0 |
| 75th percentile | 1 |
| 90th percentile | 2 |
| 95th percentile | 18 |

I then filtered the endpoint table for DDR2-relevant perturbations and verified the same calls directly in the focal-cell rows of the parquet:

```python
dataset.to_table(
    columns=["names", "gene_target", "logfoldchanges", "pvals_adj"],
    filter=(ds.field("group_name") == "151 TH Prkcd Grin2c Glut")
           & ds.field("gene_target").isin(anchors),
)
```

Each available anchor below had 17,259 measured genes in the focal cell group. The direct collagen/RTK anchors all had zero FDR-significant genes except `Ntrk2`, which had only 3:

| training target | focal `n_degs` | relevance to `Ddr2` |
| --- | ---: | --- |
| `Itga2` | 0 | alpha subunit of alpha2beta1, a collagen-binding integrin and the closest sampled non-DDR collagen receptor |
| `Itgb1` | 0 | beta1 chain used by many ECM integrins; a broad test of beta1/focal-adhesion matrix signaling |
| `Col2a1` | 0 | type-II fibrillar collagen, a canonical DDR2-activating cartilage ligand |
| `Col11a1` | 0 | cartilage fibrillar collagen family member; `Col11a1` mutant cartilage engages the DDR2/MMP13 OA axis |
| `Adam10` | 0 | membrane protease/adhesion counterexample, not a direct DDR2 paralog but an extracellular receptor-processing gene |
| `Met` | 0 | receptor tyrosine kinase using MAPK/PI3K-type signaling in other contexts |
| `Erbb4` | 0 | neuronal receptor tyrosine kinase counterexample |
| `Fgfr1`, `Fgfr2`, `Fgfr3` | 0, 0, 0 | receptor tyrosine kinases with developmental skeletal and neuronal roles |
| `Igf1r`, `Insr` | 0, 0 | growth-factor RTKs with broad PI3K/MAPK outputs |
| `Axl`, `Mertk` | 0, 0 | TAM RTK counterexamples, largely non-neuronal in basal brain |
| `Ntrk3` | 0 | neurotrophin RTK counterexample |
| `Ntrk2` | 3 | strongest RTK effect in this comparator set, but still at the one-to-few-DEG boundary |
| `Bmpr1a`, `Bmpr1b`, `Bmpr2`, `Acvr1`, `Tgfbr1`, `Tgfbr2` | all 0 | BMP/TGF-family receptor counterexamples; DDR2 can modulate BMP or TGF responses in bone/fibroblast settings, but those axes are quiet here |
| `Runx2`, `Gli1`, `Gli2`, `Mapk1` | all 0 | sampled transcriptional or MAPK nodes from the best-described skeletal DDR2 pathway |

The most direct missing comparators were `Ddr1`, `Src`, `Ptk2/FAK`, fibrillar collagen-I/III genes, and matrix metalloproteinases; they were not present in the focal training-count table, so I did not infer a signature from them. I also inspected focal signed-profile neighbors for the available anchors. The quiet ECM/RTK perturbations had no shared FDR-significant positive program, and their apparent high whole-profile similarity was driven mainly by shared extreme but nonsignificant log-fold changes on sparse features. I therefore used those profiles only as a warning not to overinterpret weak unsigned rank similarity.

## Target-specific reasoning

### `Ddr2`

`Ddr2` encodes discoidin domain receptor 2, a collagen-activated receptor tyrosine kinase. Its canonical ligands are fibrillar collagens, and its clearest transcriptional outputs occur when cells are physically embedded in or exposed to collagen-rich extracellular matrix: chondrocytes up-regulate `Mmp13` in osteoarthritis models, and skeletal progenitors/osteoblasts require DDR2 for RUNX2- and MAPK-linked differentiation. Those systems are collagen-rich and non-neuronal or progenitor-like.

That biology argues against transferring from the high-count neuronal transcription-factor perturbations in this assay. In the focal `151 TH Prkcd Grin2c Glut` training data, the actually sampled matrix-receptor genes were flat: `Itga2 = 0`, `Itgb1 = 0`, and the broader integrin/laminin-receptor corpus Claim reported no coherent basal neuronal adhesion module. The sampled collagen-matrix genes `Col2a1` and `Col11a1` were also `0`, and downstream skeletal pathway proxies `Runx2`, `Gli1`, `Gli2`, `Bmpr1a/Bmpr1b/Bmpr2`, `Acvr1`, `Tgfbr1/Tgfbr2`, and `Mapk1` were `0`. Broad RTK loss was likewise quiet, with `Met`, `Erbb4`, `Fgfr1/2/3`, `Igf1r`, `Insr`, `Axl`, `Mertk`, and `Ntrk3` all `0`; even the most neuronal RTK counterexample I checked, `Ntrk2`, only reached 3 DEGs.

The external literature leaves room for a `Ddr2` effect in brain disease or meningeal/glial compartments, but the screen is NeuN-enriched and depleted for the glial, fibroblast-like, skeletal, and cartilage states where DDR2 is most active. The perturbation is also acute and partial rather than a germline null, so the strong skeletal phenotypes of Ddr2 loss are poor quantitative guides for the postmitotic focal nuclei. With no direct `Ddr1` training perturbation and no DDR2-specific same-experiment claim, this is an extrapolation, but every available same-dataset analog near collagen receptors, beta1 integrins, BMP/TGF crosstalk, and generic RTKs points to the zero bin.

Prediction: `Ddr2` should produce no focal genes passing BH FDR 0.05, so `predicted_n_degs = 0`.

## Limits

- The training set lacks the best paralog/control, `Ddr1`, and lacks several immediate DDR2 signaling components such as `Ptk2`, `Src`, and canonical fibrillar collagen-I/III ligands.
- The parquet contains perturbation differential expression, not baseline receptor or ligand abundance, so I could not directly confirm the basal expression of `Ddr2` in the focal nuclei from these inputs.
- DDR2 can signal in glia, microglia, meninges, fibroblasts, and skeletal cells, and a whole-brain mosaic perturbation could in principle create indirect non-cell-autonomous effects. The focal assay, however, counted neuronal nuclei and the closest sampled ECM/RTK perturbations were all at zero or nearly zero.
- The numeric value is therefore driven mainly by within-dataset negative evidence plus the cell-context mismatch of known DDR2 biology; it is weaker than a prediction supported by a direct `Ddr1` or `Ddr2` signature.
