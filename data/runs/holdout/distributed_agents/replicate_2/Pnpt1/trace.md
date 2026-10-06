# Pnpt1 DEG-count prediction for `151 TH Prkcd Grin2c Glut`

## Question and interpretation

The held-out manifest contains one target:

| requested target | prediction needed |
|---|---|
| `Pnpt1` | number of measured genes with `pvals_adj < 0.05` after `Pnpt1` perturbation in `151 TH Prkcd Grin2c Glut` |

I treated the requested endpoint as the exact training CSV endpoint: a count of
Scanpy/Wilcoxon focal-cell-group DE rows with Benjamini-Hochberg adjusted
`pvals_adj < 0.05`. `Pnpt1` is absent from both the training endpoint and the
DE parquet as a perturbation, so its own DEG count and signature were not used.
The prediction is a point estimate for this acute AAV-CRISPR, postnatal,
NeuN-enriched snRNA-seq assay, not an estimate of full genetic null severity.

## Sources used

- Input endpoint table:
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
- Input DE parquet:
  `[local file: training_de_all_cell_groups.parquet]`.
- Requested-target manifest:
  `[local file: 180_Pnpt1.csv]`.
- Distributed Agents corpus, release `perturbai-july-260713-sourceguard-1773-v1`, queried for same-experiment Claims/Findings about `Lrpprc`, `Slc25a26`, mitochondrial aminoacyl-tRNA synthetases, OXPHOS genes, and `Opa1`.
- Distributed Agents runtime observed-profile comparison, run locally on the focal `151 TH Prkcd Grin2c Glut` log-fold-change vectors for selected mitochondrial comparators.
- External literature from PubMed:
  - Wang et al. 2009, JBC, DOI `10.1074/jbc.M109.009605`, PMID `19509288`: human SUV3 and PNPase form a mitochondrial RNA-degradosome complex that degrades structured/double-stranded RNA.
  - Dhir et al. 2018, Nature, DOI `10.1038/s41586-018-0363-0`, PMID `30046113`: loss of PNPase/SUV3 permits mitochondrial dsRNA accumulation and escape that activates an MDA5-driven type-I-interferon program; PNPT1 hypomorphic patient cells show mt-dsRNA and interferon-stimulated-gene activation.
  - Santonoceto et al. 2024, Human Molecular Genetics, DOI `10.1093/hmg/ddae043`, PMID `38779774`: review identifying the SUV3/PNPase degradosome as the best characterized human mitochondrial RNA decay machinery, especially for antisense RNA.
  - Sato et al. 2017, Clinical Genetics, DOI `10.1111/cge.13068`, PMID `28594066`: biallelic PNPT1 mutations can cause delayed myelination and mitochondrial dysfunction.
  - Sasarman et al. 2010, MBoC, DOI `10.1091/mbc.e10-01-0047`, PMID `20200222`, and Chujo et al. 2012, NAR, DOI `10.1093/nar/gks506`, PMID `22661577`: LRPPRC/SLIRP stabilizes mitochondrial mRNAs and interfaces with PNPase/SUV3-mediated mitochondrial mRNA decay.
  - Agrimi et al. 2004, Biochemical Journal, DOI `10.1042/BJ20031664`, PMID `14674884`, and Monne et al. 2022, IUBMB Life, DOI `10.1002/iub.2658`, PMID `35730628`: SLC25A26/SAMC imports S-adenosylmethionine into mitochondria for methylation reactions including mitochondrial RNA and translation-related chemistry.

## Computational checks

I first summarized the focal training endpoint. The 1,674 non-held-out
perturbations are highly zero inflated:

| statistic | `n_degs` |
|---|---:|
| mean | 14.05 |
| median | 0 |
| 75th percentile | 1 |
| 90th percentile | 2 |
| 95th percentile | 18 |
| 99th percentile | 436 |
| maximum | 2677 |

The largest focal responses were not generic mitochondrial RNA perturbations:
`Uba5` had 2677 DEGs, `Tpr` 1768, `Sin3a` 1433, `Rnpc3` 868,
`Zbtb7a` 841, `U2af2` 828, `Psmb4` 742, `Hnrnpu` 733, and `Yy1` 720.

The DE parquet has 616,253,184 rows over 712 row groups, so I used parquet
metadata to locate the row groups spanning the focal group, then filtered only
those row groups for biologically selected analogs. In outline:

```python
for i in range(546, 581):
    table = pq.ParquetFile(path).read_row_group(
        i,
        columns=[
            "group_name", "gene_target", "names", "logfoldchanges",
            "pvals", "pvals_adj", "scores",
            "n_pert_matched", "n_ctrl_matched",
        ],
    )
    mask = (
        pc.equal(table["group_name"], "151 TH Prkcd Grin2c Glut")
        & pc.is_in(table["gene_target"], value_set=selected_targets)
    )
```

This recovered 17,259 measured features per selected target. I also ran
`profile_compare` on focal log-fold-change vectors for `Lrpprc`, `Slc25a26`,
`Fars2`, `Rars2`, and `Opa1`, with `pvals_adj < 0.05` as the significance
threshold. Four of these five nodes had no significant focal features; `Opa1`
had 37. Tail-overlap similarity among the flat mitochondrial genes was weak
and insensitive to mechanism: top-100 positive-tail overlaps among the selected
anchors were only 3 to 11 genes and top-100 negative-tail overlaps only 2 to
14 genes. I therefore used the profile analysis mainly to confirm absence of a
shared focal expression module, not to average weak whole-profile correlations.

## Pnpt1 analogs in the focal training data

| training perturbation | focal `n_degs` | focal nuclei, pert/control | expression evidence and use |
|---|---:|---:|---|
| `Lrpprc` | 0 | 111 / 23679 | Nearest mitochondrial RNA-handling analog in the training set. It stabilizes mature mitochondrial mRNAs through the LRPPRC/SLIRP complex, which is functionally adjacent to PNPase/SUV3 RNA decay. Its own transcript was reduced, but not enough to pass focal FDR: log2FC -0.355, adjusted p = 1.0. Distributed Agents also reports a high-confidence pan-neuronal null for `Lrpprc`: 0 FDR<0.10 downstream genes in all 21 recovered neuronal groups and no expected mtDNA-mRNA or ATF4/UPR-mt stress program. |
| `Slc25a26` | 0 | 177 / 23679 | Mitochondrial SAM carrier; not the same complex as PNPase, but relevant to mitochondrial RNA methylation and mitochondrial translation chemistry. It had no focal DEG and no self-transcript reduction. Distributed Agents reports no FDR<0.10 downstream transcriptomic response in any of 22 recovered neuronal groups and specifically no Opa1/Lonp1-like ISR/UPR-mt program. |
| `Fars2` | 0 | 180 / 23679 | Mitochondrial phenylalanyl-tRNA synthetase; tests whether perturbing mitochondrial translation through mt-aaRS genes is enough to elicit a nuclear stress response in this assay. It was flat. |
| `Rars2` | 0 | 165 / 23679 | Mitochondrial arginyl-tRNA synthetase; another mt-aaRS comparator. It was flat in the focal group. |
| `Lars2` | 0 | 256 / 23679 | Mitochondrial leucyl-tRNA synthetase. It was flat in the focal group. |
| `Gfm2` | 0 | 190 / 23679 | Mitochondrial translation factor and OXPHOS/translation comparator in the Distributed Agents corpus. It was flat in the focal group. |
| `Aimp1` | 0 | 199 / 23679 | Aminoacyl-tRNA synthetase-associated disease gene but not a mitochondrial degradosome component. Included as a counterexample: Distributed Agents finds no convergence with represented mt-aaRS genes. It was flat. |
| `Dap3` | 1 | 223 / 23679 | Mitoribosomal small-subunit protein. The only focal DEG was `Dap3` itself; it did not show a broad secondary program. |
| `Ndufs2`, `Ndufv1`, `Ndufa4`, `Ndufa10`, `Sod2`, `Sucla2` | `Ndufs2` 1; `Ndufv1` 0; `Ndufa4` 1; `Ndufa10` 1; `Sod2` 1; `Sucla2` 1 | 114-223 / 23679 | Core mitochondrial/OXPHOS and matrix controls. The nonzero cases were self-transcript calls only; they did not cross into an ISR or interferon state. Distributed Agents Claim `claim:30ab45a3b952026ae47a` likewise marks represented OXPHOS comparators as below the Opa1-like response threshold. |
| `Opa1` | 37 | 195 / 23679 | Positive mitochondrial-stress benchmark rather than a Pnpt1 same-pathway analog. It significantly induced `Asns`, `Mars1`, `Chac1`, `Ddit3`, `Slc7a5`, `Mthfd2`, `Cars`, `Aars`, and other amino-acid/ATF4-like stress genes in the focal group, showing that this cell type and Wilcoxon workflow can detect a mitochondrial retrograde stress program when it is engaged. |
| `Lonp1`, `Clpp`, `Clpx`, `Afg3l2`, `Yme1l1` | 0 | 106-270 / 23679 | Mitochondrial proteostasis comparators. They were flat in the focal group and helped bound against a generic same-organelle effect. |

## Target-specific reasoning

`Pnpt1` encodes PNPase, a core mitochondrial RNA-degradosome nuclease. In
human biochemical work, PNPase cooperates with the SUV3 helicase to degrade
double-stranded/structured mitochondrial RNA. Severe PNPase or SUV3 loss can
therefore cause mitochondrial dsRNA accumulation; Dhir et al. showed that this
dsRNA can escape to the cytoplasm and trigger MDA5/MAVS/type-I-interferon
signaling, and hypomorphic human PNPT1 variants can present with mitochondrial
and neurodevelopmental disease.

That external mechanism makes a nonzero Pnpt1 response biologically plausible
under strong loss of function. However, the within-dataset evidence argues that
the acute P16 AAV CRISPR perturbation in juvenile, postmitotic, NeuN-enriched
neurons usually does not convert partial single-gene mitochondrial RNA or
translation lesions into a broad nuclear RNA state. The closest training gene,
`Lrpprc`, sits on the opposite side of PNPase/SUV3 mt-mRNA turnover and had 0
focal DEGs. `Slc25a26`, the mt-aaRS genes `Fars2`, `Rars2`, `Lars2`, and the
translation factor `Gfm2` were also 0 in the same focal group. Distributed Agents
same-experiment Claims support this as a repeated postmitotic-neuron pattern:
`Lrpprc` and `Rmnd1` do not recruit the expected mitochondrial ATF4/UPR-mt-like
program; represented mt-aaRS/mitochondrial-protein-synthesis perturbations are
flat, singleton, or nonconvergent; and many OXPHOS comparators sit below the
`Opa1` stress threshold.

I did not treat `Opa1` as the best quantitative neighbor for Pnpt1. `Opa1`
loss alters inner-membrane fusion/cristae organization and mtDNA maintenance,
and in this dataset it is an assay-positive mitochondrial architecture stressor
with a clear 37-DEG ATF4-like program. PNPase loss is instead a mitochondrial
RNA-decay lesion whose expected severe phenotype includes mitochondrial
antisense/dsRNA buildup and innate immune activation. The training genes that
best approximate mitochondrial RNA metabolism stayed at 0, and there was no
training perturbation of the actual SUV3/PNPase complex to justify borrowing
the larger `Opa1` count.

The one remaining route to a small positive count is the target RNA itself:
several near-null mitochondrial perturbations in the focal set have one DEG
that is simply the targeted transcript. This was inconsistent even among
highly expressed nuclear mitochondrial genes: `Dap3`, `Ndufs2`, `Ndufa4`,
`Ndufa10`, `Sod2`, and `Sucla2` passed, while `Lrpprc`, `Lonp1`, `Gfm2`,
`Ndufv1`, `Afg3l2`, `Yme1l1`, `Fars2`, and `Slc25a26` did not. With no direct
Pnpt1 self-knockdown row and no evidence for a secondary response, I assigned
the modal same-pathway count rather than a self-only count.

**Prediction:** `Pnpt1` -> `0` DEGs.

## Limits

- `Pnpt1` itself, its RNA-degradosome partner `Supv3l1`/SUV3, `Mtpap`, and most
  mitochondrial RNA-processing factors were absent as training perturbations,
  so this is an extrapolation from adjacent mitochondrial RNA stability,
  mitochondrial SAM import, and mitochondrial translation genes.
- `Lrpprc` is not a Pnpt1 phenocopy. It stabilizes sense mitochondrial mRNAs
  and can suppress PNPase-mediated decay, whereas PNPT1/PNPase degrades
  antisense/structured RNA and can gate mt-dsRNA escape. The predicted null
  assumes the partial neuronal CRISPR perturbation does not reach the severe
  dsRNA/MDA5 regime described in fibroblasts and patient cells.
- The assay is snRNA-seq. It does not measure mitochondrial RNA poly(A) tails,
  dsRNA, RNA import, mitochondrial translation, membrane potential, interferon
  protein secretion, or selective loss of edited nuclei.
- The point estimate is deliberately for the focal `151 TH Prkcd Grin2c Glut`
  cell group. Other groups, stronger editing, full nulls, glia, or chronic
  germline PNPT1 disease could have nonzero mitochondrial or interferon
  phenotypes even if this focal endpoint remains zero.
