# Reasoning trace

## Question and endpoint

The task asks for the integer number of `151 TH Prkcd Grin2c Glut` differentially expressed measured genes expected after each requested held-out CRISPR loss-of-function perturbation. I interpreted `n_degs` exactly as in the training count file: the count of measured genes in the focal cell group whose Wilcoxon Benjamini-Hochberg adjusted p-value is below 0.05.

The requested manifest contains one held-out target, `Pik3ca`. `Pik3ca` is absent from the supplied focal training-count CSV, and the task states that its expression signature was withheld from the differential-expression parquet. The requested endpoint is therefore directly observed for visible training perturbations only and absent for `Pik3ca`; any `Pik3ca` prediction is an extrapolation from visible perturbations plus external knowledge of PI3K signaling. I used the same-experiment report corpus only for visible training analogs and did not use a same-experiment `Pik3ca` report.

## Sources used

- Declared focal endpoint table: `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
- Declared differential-expression parquet: `training differential-expression dataset`.
- Requested-target manifest: `single-target request for Pik3ca`.
- Internal same-experiment semantic corpus `perturbai-july-260713-sourceguard-1773-v1`, specifically Findings and bounded target reports for the visible analogs `Pik3cb`, `Pik3r1`, `Pik3r2`, `Akt3`, `Depdc5`, `Mtor`, `Rptor`, and `Tsc2`.
- External literature from PubMed: Engelman, Luo and Cantley 2006, Nature Reviews Genetics, DOI `10.1038/nrg1879`, PMID `16847462`; Inoki et al. 2002, Nature Cell Biology, DOI `10.1038/ncb839`, PMID `12172553`; Manning et al. 2002, Molecular Cell, DOI `10.1016/s1097-2765(02)00568-3`, PMID `12150915`; Bar-Peled et al. 2013, Science, DOI `10.1126/science.1232044`, PMID `23723238`; Hara et al. 2002, Cell, DOI `10.1016/s0092-8674(02)00833-4`, PMID `12150926`; Lee et al. 2012, Nature Genetics, DOI `10.1038/ng.2329`, PMID `22729223`; Roy et al. 2021, Frontiers in Molecular Neuroscience, DOI `10.3389/fnmol.2021.772847`, PMID `34899181`.

## Dataset calculations

I loaded the held-out manifest and the focal training count CSV with pandas, then used `pyarrow.dataset` filters to read only `151 TH Prkcd Grin2c Glut` rows for visible PI3K/AKT/mTOR comparator perturbations from the parquet:

```python
filt = (
    pc.field("group_name") == "151 TH Prkcd Grin2c Glut"
) & pc.field("gene_target").isin(targets)
table = dataset.to_table(
    columns=[
        "names", "gene_target", "logfoldchanges",
        "pvals_adj", "scores", "n_pert_matched", "n_ctrl_matched",
    ],
    filter=filt,
)
n_degs = rows[rows.pvals_adj < 0.05].groupby("gene_target").size()
```

The focal training endpoint is sparse: 1,205 of 1,674 visible training perturbations have `n_degs = 0`, the median is 0, the 75th percentile is 1, and the top count is 2,677. I used that only for calibration of scale; the target-specific estimate came from the PI3K neighborhood.

Relevant visible focal counts were:

| perturbation | focal `n_degs` | focal expression-pattern evidence |
|---|---:|---|
| `Pik3cb` | 0 | No measured gene passed FDR 0.05 in the focal group; every adjusted p-value was 1.0. The corpus reports that `Pik3cb` had no FDR 0.10 downstream response in any of its 22 recovered neuronal groups and was flat along with represented PI3K-core comparators. |
| `Pik3r1` | 0 | No focal FDR 0.05 hits; minimum adjusted p-value was 0.776. The corpus reports a pan-neuronal flat result and the same absence for `Pik3r2` and `Pik3cb`. |
| `Pik3r2` | 0 | No focal FDR 0.05 hits despite 260 matched perturbed focal nuclei; minimum adjusted p-value was 0.887. The corpus reports no downstream FDR 0.10 response in any recovered neuronal group. |
| `Akt3` | 0 | `Akt3` itself was the strongest focal row, but still above threshold at adjusted p = 0.064; all other focal rows had adjusted p = 1. The corpus separates this flat AKT node from detectable downstream TSC/mTOR outputs. |
| `Rptor` | 0 | No focal FDR 0.05 genes. This was a counterexample showing that loss of the positive mTORC1 scaffold did not simply mirror loss of mTORC1 inhibitors in this assay. |
| `Mtor` | 2 | A very small mixed focal signature: `Rims3` up and `Tmed8` down at FDR 0.05. The report layer describes the broader FDR 0.10 signature as only a few genes in `151` and `155 MB Glut`. |
| `Depdc5` | 13 | A moderate GATOR1-loss focal response with sterol/LDL genes up, including `Pik3r1`, `Ldlr`, `Pik3r3`, `Insig1`, `Hmgcs1`, `Cyp51`, and `Msmo1`, and a few RNA-processing or host genes down. |
| `Tsc2` | 86 | The clearest same-pathway response. Its significant focal genes included `Pik3r3`, `Cyp51`, `Slc2a6`, `Ldlr`, `Msmo1`, `Lamp2`, and other sterol/lysosomal/stress genes. |
| `Srebf2` | 7 | Downstream, branch-specific counterexample: the only two FDR 0.05 overlaps with `Tsc2`, `Cyp51` and `Msmo1`, moved in the opposite direction after `Srebf2` loss. |
| `Rab7` | 501 | A much broader lysosomal/sterol stress perturbation. It overlapped the `Tsc2` focal DEG set at 38 FDR 0.05 genes, 36 in the same direction, but it is not a receptor-proximal PI3K paralog and would overestimate single p110alpha loss. |

The exact focal overlap between the two mTORC1-brake perturbations supports a real but downstream branch: `Depdc5` and `Tsc2` shared 8 FDR 0.05 focal genes, all in the same direction (`Pik3r1`, `Ldlr`, `Pik3r3`, `Tubb3`, `Msmo1`, `Snhg11`, `Rnpc3`, `Amy1`). That module is expected for loss of GATOR1 or TSC inhibition, because Bar-Peled et al. showed that DEPDC5/NPRL2/NPRL3 form the GATOR1 GAP that represses Rag-dependent amino-acid input to mTORC1, while Inoki et al. and Manning et al. showed that AKT phosphorylation inhibits TSC2, relieving the TSC brake on mTOR signaling.

## Target-specific prediction

### `Pik3ca`

`Pik3ca` encodes p110alpha, a class IA PI3K catalytic subunit paired with p85-family regulatory subunits and positioned upstream of PIP3, AKT, TSC2, and mTORC1. Activating PI3K/AKT/mTOR mutations, including mosaic `PIK3CA` alleles, can drive developmental brain overgrowth and elevated S6 phosphorylation (Lee et al. 2012), and Pik3ca activation can cause neuronal hyperexcitability through PI3K/AKT signaling (Roy et al. 2021). Those disease alleles are gain-of-function and often developmental; they are the opposite biochemical sign from sparse postnatal CRISPR loss of function.

The most appropriate visible analogs are the upstream positive PI3K-side perturbations. `Pik3cb`, `Pik3r1`, and `Pik3r2` all had zero focal DEGs, and the internal reports found the same broad buffering at FDR 0.10 across recovered neuronal classes. `Akt3`, the represented neuronal AKT isoform downstream of p110, was also zero in the focal count. These are not perfect substitutes for p110alpha: p110alpha and p110beta are paralogous catalytic isoforms with different receptor and Ras coupling, and `Pik3r1`/`Pik3r2` perturb regulatory rather than catalytic subunits. They are nevertheless the within-dataset perturbations most likely to reveal whether one acute upstream class IA PI3K lesion produces a basal postnatal neuronal nuclear-RNA state. In this experiment, the answer for all represented upstream PI3K/AKT nodes was no.

The pathway counterexamples argue against blindly inheriting the `Tsc2` or `Depdc5` counts. `Tsc2` loss removes an mTORC1 brake and had 86 focal DEGs; `Depdc5` loss removes the GATOR1 amino-acid brake and had 13. Both should increase or de-repress mTORC1 output, which is directionally opposite to loss of the positive p110alpha input. `Mtor` loss, which should have a closer sign to losing upstream PI3K input for the mTORC1 arm, was only 2 DEGs, and loss of the obligate mTORC1 scaffold `Rptor` was 0 even though Hara et al. established Raptor as required for mTOR action. `Srebf2` loss confirmed that the sterol branch can move opposite the `Tsc2`/`Depdc5` state, but its count was only 7 and it tests one downstream transcription factor rather than the whole PI3K node. `Rab7` produced a 501-DEG lysosomal/sterol state and partially converged with `Tsc2`, but its late-endolysosomal biology is too broad to be a point estimate for receptor-proximal p110alpha.

The experimental causal transfer chain is therefore:

`Pik3ca` CRISPR loss -> reduced p110alpha-dependent PIP3/AKT signaling if p110alpha is limiting -> reduced AKT inhibition of TSC2 and potentially lower mTORC1 drive -> postnatal thalamic neurons have redundant or buffered upstream PI3K inputs under basal conditions -> the surviving nuclei sampled at P37-P44 are expected to show no FDR 0.05 steady-state nuclear RNA program.

This chain predicts a same endpoint direction as the flat `Pik3cb`/`Pik3r1`/`Pik3r2`/`Akt3` perturbations, an opposite direction from the positive `Tsc2` and `Depdc5` mTORC1-release signatures, and an indeterminate but weak relationship to the broad `Rab7` lysosomal state. I therefore predict no genes below BH FDR 0.05:

`Pik3ca -> 0`

## Limits and uncertainty

The main uncertainty is paralog specificity. p110alpha is not identical to p110beta, and the focal parquet could not test `Pik3ca`, `Pik3cd`, `Pten`, `Tsc1`, `Rheb`, or `Akt1`/`Akt2` directly. The visible p85 regulatory perturbations are same-complex context, not a catalytic p110alpha knockout. The assay also measured survivor-conditioned nuclear RNA, not PIP3, pAKT, pS6, protein synthesis, autophagic flux, morphology, excitability, cell size, or depletion before sorting. A real biochemical PI3K effect could therefore remain below the DEG-count endpoint. Despite those caveats, the nearest visible loss-of-function nodes on the positive PI3K side were all zero or nearly zero, while the larger same-pathway counts came from releasing mTORC1 inhibitors in the opposite biochemical direction, so the most calibrated point estimate for this scalar endpoint is 0.
