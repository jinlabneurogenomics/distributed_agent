# Rhobtb2 DEG-count forecast

## Target and endpoint

- Target: `Rhobtb2`
- Population: `151 TH Prkcd Grin2c Glut`
- Endpoint: `n_degs`, measured genes with BH-adjusted Wilcoxon `pvals_adj < 0.05`
- Point forecast: `1`

## Evidence used

The declared `Rhobtb2` biology bundle supports assay reach but only a moderate
response prior. In the exact held-out thalamic population, Rhobtb2 was detected
in 16,698 of 23,679 non-target nuclei, with 70.52% of nuclei expressing it and
mean expression of 0.876 CP10K. Functional-stock adjudication concludes that a
P16 edit should likely substantially deplete the renewable RhoBTB2 protein by
P37-P44 because it is a dynamic CUL3-associated substrate adaptor under
ubiquitin-proteasome turnover. The same bundle leaves important endpoint
uncertainty: the mouse neural phenotype evidence is constitutive/developmental,
there is no matched postnatal thalamic loss timecourse, and Rhobtb1/Rhobtb3
paralogy is not a same-context compensation test.

The declared thalamic training count table is sparse. Among 1,674 observed
training targets, 1,205 had 0 DEGs and 276 had exactly 1 DEG; the median was 0,
the 75th percentile was 1, the 90th percentile was 2, and the mean was pulled to
14.05 by a small heavy tail. This makes a low integer the default unless a
target has a close training analogue with a large signature.

No exact Rhobtb paralogue, `Cul3`, or `Msi2` perturbation was available in the
declared count table. Curated gene-analogue nomination for `Rhobtb2` against the
training universe found no exact-complex/paralogue or direct-interaction
candidate and only four narrow Reactome Rhobtb-cycle candidates:

| training target | typed relation | 151 TH `n_degs` | interpretation |
|---|---:|---:|---|
| `Hsp90ab1` | narrow module | 1 | single significant gene was `Hsp90ab1` itself |
| `Myo6` | narrow module | 0 | no significant thalamic genes |
| `Ddx39b` | narrow module | 0 | no significant thalamic genes |
| `Hnrnpc` | narrow module | 122 | outlier RNA-binding/splicing perturbation, not a CUL3-adaptor analogue |

The more operation-like CUL3 or ubiquitin-ligase adaptor fallbacks were also at
the floor in the same declared inputs. `Klhl20`, `Klhl7`, and `Kbtbd7` each had
0 DEGs; `Lztr1`, `Fbxo11`, and `Fbxw7` each had 1 DEG. The leading Rho/GTPase
or cytoskeleton fallbacks were similarly quiet: `Rac1`, `Hras`, and `Arhgap18`
had 0, while `Cdc42` had 1.

I used filtered rows from `training_de_all_cell_groups.parquet` only for the
same population to verify that these low counts were true 151-TH signatures and
not count-table artifacts. The singletons for `Hsp90ab1`, `Lztr1`, and `Cdc42`
were self-transcript calls; the singletons for `Fbxo11` and `Fbxw7` were isolated
downstream calls. `Hnrnpc` was the lone high-DEG member of the narrow nominee
set and carried a broad RNA-processing profile, so it was treated as an upper
boundary rather than a scale estimate for RhoBTB2.

## Synthesis

The forecast should sit above the global zero mode because `Rhobtb2` has strong
focal expression and its protein stock is likely to turn over within the
21-28-day post-edit window. But there is no direct thalamic RhoBTB2 substrate
programme, no measured exact paralogue, and the available CUL3-adaptor/Rho
comparators are almost all null or one-gene calls in this same endpoint. I
therefore predict a singleton detectable call rather than a multi-gene
signature:

`predicted_n_degs = 1`
