# Gpr12 direct `n_degs` forecast

## Target and endpoint

- Target: `Gpr12`
- Population: `151 TH Prkcd Grin2c Glut`
- Endpoint: number of measured genes with BH-adjusted Wilcoxon `pvals_adj < 0.05`
- Prediction: `0`

## Evidence used

The declared biology bundle gives good reach for the target transcript in the focal population: `Gpr12` is detected in 18,357 of 23,679 non-target nuclei, 77.52%, with mean 1.134 cp10k and pseudobulk 113.8 cpm. This makes the receptor present enough for a perturbation to be observable if loss of GPR12 creates a strong recovered-nucleus transcriptional state.

The same biology bundle makes the expected perturbation weaker and less endpoint-coupled than the expression level alone would suggest. GPR12 is a constitutively active Gs/cAMP seven-transmembrane receptor, so editing stops new intact receptor supply but does not instantly inactivate membrane receptor already present at P16. Adult mediodorsal-thalamus AAV RNAi supports a postmitotic thalamic function, but only with later validation than the P37-P44 Perturb-seq harvest, no measured receptor half-life in this context, and no direct evidence that juvenile Gpr12 loss drives a large nuclear RNA program.

The focal training count table is highly zero-heavy:

- 1,205 / 1,674 training perturbations, 71.98%, have `n_degs = 0`.
- The median is 0 and the 75th percentile is 1.
- Only 103 / 1,674, 6.15%, exceed 10 DEGs.

I therefore treated broad genome-scale large-footprint genes as a poor quantitative prior for this receptor and looked at G-protein receptor / cAMP / PKA pathway perturbations in the same count table and Parquet. Among 44 training targets with names beginning `Gpr`, `Adcy`, `Pde`, `Prka`, `Creb`, `Drd`, `Htr`, `Chrm`, `Grm`, or `Gna`, 35 had zero DEGs. Excluding the two more nuclear transcriptional targets `Creb1` and `Crebbp`, 35 of 42 had zero DEGs; the seven nonzero receptor or second-messenger cases were all exactly one DEG.

The Parquet showed that those seven one-DEG cases were self-target-only calls:

| training target | focal-population DEGs at FDR < 0.05 |
| --- | --- |
| `Gnao1` | `Gnao1` only |
| `Gpr158` | `Gpr158` only |
| `Gprasp2` | `Gprasp2` only |
| `Grm1` | `Grm1` only |
| `Grm7` | `Grm7` only |
| `Prkaca` | `Prkaca` only |
| `Prkar1a` | `Prkar1a` only |

The screened Gs/cAMP signal generators closest to a constitutive GPR12 receptor were quieter still: `Gnas`, `Gnal`, `Adcy1`, `Adcy3`, `Adcy5`, `Pde4b`, and `Pde4d` all had `n_degs = 0`.

## Synthesis

`Gpr12` has enough in-assay expression and external thalamic functional evidence that I would not call it biologically inert. For this endpoint, though, the most relevant measured perturbations say that upstream receptors and cAMP-pathway components almost always have no downstream FDR-significant RNA footprint in recovered `151 TH Prkcd Grin2c Glut` nuclei, and their rare one-DEG outcomes were isolated self-transcript calls rather than pathway-wide responses. The uncertain 21-28 day loss of pre-existing GPR12 receptor further discounts a large recovered-cell transcriptional response.

I therefore put the forecast at the mass point favored by the direct pathway comparators and the global zero-heavy training distribution: **0 DEGs**.
