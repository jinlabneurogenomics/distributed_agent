# Held-out DEG-count prediction for 151 TH Prkcd Grin2c Glut

## Question and endpoint

The task asks for a point prediction of `n_degs` for the held-out `Chchd10`
perturbation in the thalamic glutamatergic class `151 TH Prkcd Grin2c Glut`.
I treated `n_degs` exactly as in the training count CSV: the number of measured
genes with a Benjamini-Hochberg-adjusted Wilcoxon `pvals_adj < 0.05` in the
focal cell class. The held-out `Chchd10` perturbation has no direct rows in the
DE parquet and no direct count in the training count CSV, so all expression
evidence below is transfer from non-held-out perturbations in the same screen.

The input endpoint is directly observed for training genes in
`151 TH Prkcd Grin2c Glut`, but absent for `Chchd10`. I therefore used the
training endpoint as the quantitative anchor and same-experiment DE signatures
as mechanistic checks. The internal July PerturbAI corpus was used only as a
bounded, same-experiment interpretation layer over the same parquet, not as
independent replication.

## Sources

- Training count CSV:
  `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
- Training DE parquet:
  `training differential-expression dataset`.
- Requested-target CSV:
  `single-target request for Chchd10`,
  which contains only `Chchd10`.
- Run-local measurement registry and dataset portrait in `codex_runtime/pipeline`.
- Internal same-experiment corpus:
  `perturbai-july-260713-sourceguard-1773-v1`, especially packaged reports for
  `Chchd2`, `Opa1`, and `Micos13`.
- External mechanism priors from PubMed literature: Burstein et al. 2018,
  DOI `10.1093/hmg/ddx397`; Huang et al. 2018, DOI `10.1093/hmg/ddy270`;
  Zhou et al. 2019, DOI `10.1093/hmg/ddy413`; Liu et al. 2020,
  DOI `10.1093/hmg/ddaa077`; Ruan et al. 2022,
  DOI `10.1038/s41419-022-04602-5`; Guo et al. 2020,
  PMID `32132707`; Quiros et al. 2017, PMID `28566324`.

## Quantitative calibration

The focal training file contains 1,674 non-held-out perturbations. It is a
sparse endpoint:

- 1,205/1,674 had `n_degs = 0`.
- 276/1,674 had `n_degs = 1`.
- 1,481/1,674, or 88.5%, had at most one DEG.
- The median was 0, the 75th percentile was 1, the 95th percentile was 18, and
  the maximum was 2,677.

I queried the focal class of the parquet for CHCHD/MICOS/cristae, OXPHOS,
mitochondrial-import, and Parkinson/ALS-adjacent training perturbations and
counted `pvals_adj < 0.05` rows per perturbation. The relevant focal counts
were:

| training perturbation | focal `n_degs` | focal expression-pattern evidence |
|---|---:|---|
| `Chchd2` | 1 | The only significant focal row was the on-target `Chchd2` transcript, log2FC -0.880, q = 3.18e-28. `Asns`, `Ddit3`, `Chac1`, `Cars`, `Mars1`, `Mthfd2`, `Shmt2`, and `Slc7a5` were all q = 1.0. |
| `Opa1` | 37 | A clear ISR/amino-acid response: `Asns`, `Mars1`, `Chac1`, `Ddit3`, `Cars`, `Mthfd2`, and `Slc7a5` were significant with positive log2FCs. |
| `Micos13` | 0 | No focal FDR<0.05 genes; the same Opa1 ISR sentinel genes were q = 1.0. |
| `Yme1l1` | 0 | No focal FDR<0.05 genes; same ISR sentinels were q = 1.0. |
| `Afg3l2` | 0 | No focal FDR<0.05 genes. |
| `Clpp` | 0 | No focal FDR<0.05 genes. |
| `Mff` | 0 | No focal FDR<0.05 genes. |
| `Micu1` | 0 | No focal FDR<0.05 genes. |
| `Tomm40` | 1 | The one call was self transcript only. |
| `Ndufs2` | 1 | The one call was self transcript only. |
| `Slc25a4` | 1 | The one call was self transcript only. |
| `Slc25a46` | 1 | The one call was self transcript only. |
| `Park7` | 1 | The one call was self transcript only. |
| `Uqcrq` | 1 | One non-OXPHOS singleton, `Gpr180`; no focal ISR. |
| `Cox4i1` | 0 | No focal FDR<0.05 genes despite nominal self knockdown. |
| `Snca` | 0 | No focal FDR<0.05 genes. |

The parquet query was a single focal-class aggregation:

```sql
SELECT gene_target,
       count(*) FILTER (WHERE pvals_adj < 0.05) AS deg05,
       count(*) FILTER (WHERE pvals_adj < 0.10) AS deg10,
       min(pvals_adj) AS min_padj,
       arg_min(names, pvals_adj) AS min_gene
FROM read_parquet(:training_de)
WHERE group_name = '151 TH Prkcd Grin2c Glut'
  AND gene_target IN (:mitochondrial_analogs)
GROUP BY gene_target;
```

The same-experiment corpus also reports that `Chchd2` produced a 23-cell-group
transcriptional null once its own transcript was excluded: every assayed
neuronal group had zero downstream genes at FDR<0.10, although `Chchd2` mRNA
was reduced in every group and was significant in 9/23 groups, including the
focal class. That argues the near-null surface was not simply a complete
absence of on-target engagement. In the same corpus, `Opa1` is the adjacent
mitochondrial perturbation that activated an OMA1/DELE1/HRI/eIF2alpha-ATF4-like
program; OPA1-processing and cristae comparators such as `Yme1l1`, `Afg3l2`,
`Mff`, `Clpp`, and `Micos13` did not phenocopy `Opa1` in this acute postnatal
neuronal screen.

## Target-specific biological transfer

### Chchd10

`Chchd10` encodes a small mitochondrial intermembrane-space protein and is the
closest paralog and binding partner of `Chchd2`. Burstein et al. 2018 showed
that CHCHD10 resides in the intermembrane space, interacts with CHCHD2, and
that homozygous CHCHD10 knockout mice were viable and lacked gross brain,
heart, or skeletal-muscle bioenergetic or mitochondrial-ultrastructural
phenotypes, whereas mutant CHCHD10 proteins impaired mitochondrial energy
metabolism. Huang et al. 2018 found that CHCHD2 and CHCHD10 form heterodimers
and are partially redundant. Liu et al. 2020 placed combined CHCHD2/CHCHD10
loss upstream of OMA1-mediated long-OPA1 cleavage, cristae disruption, and a
mitochondrial integrated stress response in double-knockout mice. Ruan et al.
2022 similarly placed CHCHD2/CHCHD10 upstream of OMA1, OPA1 processing,
DELE1 cleavage, and eIF2alpha-linked mtISR, with a stronger basal ISR after
double CHCHD2/CHCHD10 knockdown than after either single perturbation. Zhou et
al. 2019 linked PD-associated CHCHD2 alleles to CHCHD10 and MICOS disruption.

The causal transfer chain is therefore:

1. Acute sparse CRISPR loss reduces CHCHD10 function in recovered postmitotic
   neurons.
2. The direct molecular consequence is a partial defect in the
   CHCHD2/CHCHD10 intermembrane-space complex.
3. Propagation to a broad nuclear RNA program would require that single
   CHCHD10 loss overcome CHCHD2 compensation enough to activate OMA1/OPA1 and
   the OMA1-DELE1-HRI/ATF4 mitochondrial ISR.
4. The measured endpoint is the survivor-conditioned snRNA-seq differential
   expression 3-4 weeks after P16 viral CRISPR.

Within this screen, the limiting steps are step 2 to step 3. The best direct
analog is `Chchd2`, not `Opa1`: it perturbs the same two-protein module and
gave a one-DEG focal footprint consisting only of its own transcript, with no
focal induction of `Asns`, `Ddit3`, `Chac1`, `Cars`, `Mars1`, `Mthfd2`, or
`Slc7a5`. This matches the external loss-of-function literature in which
single CHCHD2 or CHCHD10 loss is buffered, while double loss or disease-mutant
proteotoxic CHCHD10 alleles can cross into OMA1/OPA1/cristae pathology.

`Opa1` is an informative positive counterexample rather than a count template:
it is downstream in the cristae-stress axis and, when directly perturbed,
generated 37 focal DEGs and the expected ATF4/amino-acid program. If
`Chchd10` single loss strongly activated OPA1 cleavage in these neurons, an
`Opa1`-like nonzero count would be plausible; the represented single-gene
perturbations around the same pathway show that this is not the default.
`Micos13`, `Yme1l1`, `Afg3l2`, `Mff`, and `Clpp` further show that cristae or
OPA1-adjacent annotations alone do not imply a focal ISR under this assay.

I predict a tiny nonzero count, `1`, because the closest observed analog,
`Chchd2`, had exactly one focal DEG and the broad downstream program was
buffered. The most likely one DEG is the knocked-out `Chchd10` transcript
itself, but this is weaker than the downstream null call: target-transcript
loss is variable in this mosaic nuclear-RNA screen, and `Chchd10` expression
or guide visibility in `151 TH Prkcd Grin2c Glut` could make the realized count
0. I did not add any OPA1/ATF4 genes because the single-loss causal chain is
not expected to pass the compensation threshold in the focal survivor nuclei.

## Limits and extrapolation

- The endpoint for `Chchd10` is absent from the declared inputs; the prediction
  is transfer, not a direct measurement.
- The CHCHD2 report is same-experiment evidence over the training parquet and
  is not an independent experiment.
- `Chchd2` is the closest available perturbation but not identical to
  `Chchd10`; the two paralogs can have asymmetric and tissue-specific biology.
- The predicted count depends partly on whether `Chchd10` self mRNA is
  observed as an FDR-significant row. Self-knockdown is assay-visible for
  `Chchd2`, `Tomm40`, `Ndufs2`, and several other near-null mitochondrial
  perturbations, but the dataset portrait warns that self-transcript reduction
  is not a reliable editing-efficiency measurement.
- The literature establishes severe phenotypes for CHCHD10 missense mutants
  and CHCHD2/CHCHD10 double loss. Those are not the same intervention as a
  sparse juvenile `Chchd10` CRISPR loss-of-function perturbation by itself.
