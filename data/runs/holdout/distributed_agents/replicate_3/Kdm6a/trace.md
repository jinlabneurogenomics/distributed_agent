# Kdm6a DEG-count prediction

## Question and ambiguity resolution

The requested held-out target set contains exactly one perturbation, `Kdm6a`. I
interpreted the endpoint as the integer number of measured genes with
`pvals_adj < 0.05` in the held-out `Kdm6a` row of the focal
`151 TH Prkcd Grin2c Glut` differential-expression table.

I treated the experiment as an acute, sparse, AAV-delivered CRISPR-Cas9
loss-of-function perturbation in postmitotic P16-to-P37/P44 NeuN+ brain nuclei.
I did not use germline, embryonic, Cre-lox, shRNA, or drug phenotypes as direct
quantitative substitutes; those data only informed whether an in-dataset
perturbation was mechanistically close enough to be an analog.

## Sources used

- Input training endpoint:
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
- Input differential-expression parquet:
  `[local file: training_de_all_cell_groups.parquet]`.
- Held-out manifest:
  `[local file: 119_Kdm6a.csv]`.
- Distributed Agents corpus MCP, release
  `perturbai-july-260713-sourceguard-1773-v1`, especially the curated `Kdm6b`
  and `Kmt2c` findings summarizing their flat thalamic and midbrain signatures.
- PubMed-indexed literature on KDM6A/UTX biology: Tran, Broun and Ge 2020,
  PMID:32817139, DOI:10.1128/MCB.00341-20; Wang et al. 2017,
  PMID:28732206, DOI:10.1016/j.molcel.2017.06.028; Shpargel et al. 2017,
  PMID:29073101, DOI:10.1073/pnas.1705011114; Koizumi et al. 2022,
  PMID:36412518, DOI:10.1096/fj.202201002RR.

## Computational use of the input data

I first read the manifest and confirmed that the only requested target is
`Kdm6a`. I then summarized the 1,674 training counts in the focal cell group:
the median training perturbation has 0 DEGs, the 75th percentile has 1 DEG, the
95th percentile has 18 DEGs, and a small tail of generic strong perturbations
runs into hundreds or thousands of DEGs.

To avoid reasoning only from the count table, I filtered the parquet to
`group_name == "151 TH Prkcd Grin2c Glut"` and to chromatin perturbations
related to KDM6A. For each candidate analog I counted focal genes with
`pvals_adj < 0.05` and inspected the leading adjusted p-values. The core focal
comparisons were:

| training target | focal n_degs | matched perturbed nuclei | relationship to KDM6A | focal expression-pattern evidence |
|---|---:|---:|---|---|
| `Kdm6b` | 0 | 203 | closest measured H3K27me2/3 demethylase paralog | No focal FDR genes; all inspected high-rank rows had `pvals_adj = 1`. |
| `Kmt2c` | 0 | 55 | MLL3/COMPASS-family enhancer partner of UTX/KDM6A | No focal FDR genes; all inspected high-rank rows had `pvals_adj = 1`. |
| `Ep300` | 0 | 155 | p300 enhancer acetyltransferase recruited by the UTX-MLL4 enhancer module | No focal FDR genes. |
| `Kat6a` | 0 | 170 | enhancer-linked histone acetyltransferase and chromatin NDD gene | No focal FDR genes. |
| `Kat6b` | 0 | 150 | paralog of `Kat6a` and enhancer/chromatin NDD gene | No focal FDR genes. |
| `Crebbp` | 8 | 61 | CBP paralog of p300; enhancer coactivator | A very sparse signature, led by `Stxbp2`, `Rtn4rl1`, `Ccdc141`, `Cfap298`, `Rbfox2`, `Dgkz`, `Stmn4`, and `Leng8`. |
| `Kmt2a` | 24 | 161 | SET1/MLL H3K4 methyltransferase family member, but not the MLL3/4 UTX complex | Sparse focal response led by `Nr2f1`, `Pcdh7`, `Lhx9`, `Kmt2a`, `Camk2d`, and `Usp43`. |
| `Kdm5c` | 18 | 184 | H3K4 demethylase, same broad histone-methylation class but not an H3K27 eraser | Sparse, non-KDM6-like response led by `Ptgds`, `Capn3`, `Man2a2`, `Zfp532`, and `Col9a3`. |
| `Setd1a` | 368 | 154 | SET1 H3K4 writer counterexample | Broad response showing the focal cell type can report chromatin perturbations. |
| `Brd4` | 311 | 93 | acetyl-lysine reader counterexample | Broad response unrelated to the KDM6A/KDM6B nulls. |
| `Sin3a` | 1433 | 176 | HDAC-corepressor counterexample | Very broad response unrelated to the KDM6A/KDM6B nulls. |
| `Smarcc2` | 185 | 162 | SWI/SNF subunit counterexample | Broad response unrelated to the KDM6A/KDM6B nulls. |

The Distributed Agents corpus independently encoded the same useful contrast: `Kdm6b`
was FDR-flat in the focal thalamic group while `Setd1a`, `Smarcc2`, `Rora`,
`Kmt2a`, `Setdb1`, `Kdm5c`, `Crebbp`, and `Setd5` were detectable there, and
`Kmt2c` was flat in matched thalamic and midbrain groups while several H3K4 and
chromatin-neurodevelopmental comparators responded. That argues against a
generic assay failure for chromatin genes and instead supports selective
buffering of the represented H3K27/MLL3/4/enhancer branch.

## Target-specific biological reasoning

### `Kdm6a`

KDM6A/UTX is an X-linked KDM6-family H3K27me2/3 demethylase. It can also act
through demethylase-independent scaffolding: UTX physically associates with the
MLL3/MLL4 COMPASS-like enhancer machinery, and Wang et al. showed that a
UTX-MLL4-p300 module couples H3K4me1 and H3K27ac during enhancer activation.
Embryonic and lineage-specification data make KDM6A biologically important:
neural crest deletion caused Kabuki-like craniofacial phenotypes in Shpargel et
al., and neural stem/progenitor deletion impaired neurogenesis and postnatal
survival in Koizumi et al.

Those phenotypes are not a direct match to this readout. The Perturb-seq
experiment edited differentiated, NeuN+ neurons after P16, excluded most
microglia, astrocytes, and oligodendrocytes, and measured cell-autonomous
snRNA-seq after only partial AAV-CRISPR loss. In exactly that context, the
closest training perturbation, `Kdm6b`, had 0 focal DEGs from 203 perturbed
nuclei and was described by the Distributed Agents corpus as FDR-null across every
recovered neuronal group. The best represented same-enhancer branch target,
`Kmt2c`, was also 0 in the focal group and almost completely flat across its
measured neuronal surface in the corpus. `Ep300`, `Kat6a`, and `Kat6b` were
likewise focal-null, while `Crebbp`, `Kmt2a`, and `Kdm5c` were only
single-digit to low-double-digit responders.

I therefore predict no corrected DE genes for acute `Kdm6a` loss in
`151 TH Prkcd Grin2c Glut`. The zero/nonzero decision is driven
primarily by the within-dataset `Kdm6b` and `Kmt2c` nulls. The external biology
helps explain why those are appropriate analogs - H3K27 demethylation and
MLL3/4 enhancer regulation - and also why developmental disease phenotypes
should not be extrapolated into a broad postmitotic maintenance signature.

Predicted `n_degs`: **0**.

## Limits and weak points

- The exact target, `Kdm6a`, was absent from both input training files; the
  prediction is extrapolated from related genes.
- The closest same-complex member in human enhancer biology, `Kmt2d`/MLL4, was
  not present as a training perturbation for this comparison.
- Direct Polycomb counter-perturbations (`Ezh1`, `Ezh2`, `Eed`, `Suz12`) were
  not represented in the analog set I could compare.
- `Kdm6a` and `Kdm6b` are paralogs but not interchangeable; KDM6A has
  noncatalytic UTX/MLL3/4 scaffolding activities, and some literature reports
  functions that are demethylase-independent.
- The assay did not measure DNA indels or KDM6A protein depletion. It also mixed
  sexes, which could matter for the X-linked `Kdm6a` locus and for escape from X
  inactivation.
- `Kmt2c` had only 55 matched perturbed nuclei in the focal cell group, so its
  focal null has less power than the `Kdm6b` null.
