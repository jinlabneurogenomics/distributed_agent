# Trpv4 direct n_degs forecast

## Endpoint

- Target manifest: `Trpv4`
- Cell class: `151 TH Prkcd Grin2c Glut`
- Endpoint: number of measured genes in the focal class with BH-adjusted Wilcoxon `pvals_adj < 0.05`
- I used the declared holdout manifest, target biology bundle, focal training count table, and declared training Parquet. I did not query a `Trpv4` differential-expression row or target outcome.

## Evidence Used

### Canonical Trpv4 biology bundle

The bundle identifies TRPV4 as a plasma-membrane, Ca2+-permeable nonselective TRP cation channel. The functional-stock adjudication says the channel is a dynamic membrane complex and that a disruptive edit at P16 should stop new functional TRPV4 synthesis; pre-existing channel stock is unlikely to persist through the 21-28 days to P37-P44 harvest.

That supports real loss of function in successfully edited Trpv4-expressing cells, but the exact in-assay focal reach is tiny:

| quantity | value |
|---|---:|
| focal non-target nuclei | 23679 |
| nuclei with any Trpv4 RNA | 167 |
| percent expressing | 0.705266% |
| mean raw UMI | 0.007475 |
| pseudobulk CPM | 0.468483 |
| mean log1p(CP10K) | 0.003355 |

The same bundle also keeps the strongest phenotype prior outside this focal context: adult Trpv4-null mice have an osmoregulatory/CNS-activation phenotype, but the evidence is germline, centered on circumventricular physiology rather than juvenile thalamic NeuN-positive nuclei, and published single-cell localization cited in the card was in a minority of adult hippocampal astrocytes. Since this assay enriches NeuN-positive nuclei and aggregates the thalamic class, a large focal transcriptional footprint would require either sparse high-impact Trpv4-positive neurons or a non-cell-autonomous state that is not established by the bundle.

### Focal training DEG-count table

The declared focal count table contains 1,674 non-Trpv4 training targets. Its empirical distribution is extremely zero-heavy:

| count range | training targets |
|---|---:|
| `n_degs = 0` | 1205 |
| `n_degs = 1-2` | 307 |
| `n_degs = 3-18` | 79 |
| `n_degs = 19-100` | 41 |
| `n_degs > 100` | 42 |

The median and 70th percentile are 0, the 80th percentile is 1, the 90th percentile is 2, the 95th percentile is 18, and the mean is pulled upward to 14.05 by a small heavy tail.

### Prechosen channel-family checks in the expression Parquet

Before inspecting their profiles, I selected the available TRP/PKD-style cation-channel perturbations in the focal training table as weak biological comparators. They are not exact TRPV4 analogues, but they test whether related ion-channel perturbations in this cell class generally look like broad high-yield transcriptional regulators.

Scanning the declared training Parquet only in `151 TH Prkcd Grin2c Glut` gave:

| training target | focal measured genes | focal genes with `pvals_adj < 0.05` |
|---|---:|---:|
| Pkd1 | 17259 | 0 |
| Trpa1 | 17259 | 0 |
| Trpm3 | 17259 | 0 |
| Trpm7 | 17259 | 0 |
| Trpv1 | 17259 | 0 |

`Trpv1` was the only TRPV-family paralog present in the focal count table, and it was also quiet.

## Synthesis

The CRISPR loss should clear functional TRPV4 channels in cells that actually depend on Trpv4, so I did not treat stock persistence as a reason for a failed perturbation. The dominant downward evidence is instead focal reach and endpoint coupling: Trpv4 RNA is detected in less than 1% of the matched non-target thalamic nuclei, while the assay aggregates the whole `151 TH Prkcd Grin2c Glut` population and measures survivor-conditioned nuclear RNA. A sparse channel loss could be biologically real yet still produce no BH-significant aggregate DE genes.

The count prior also favors zero for targets without broad expression or core transcriptional/proteostasis roles, and the available related channel perturbations were all exactly zero in the same focal context. I therefore used the modal and median focal value as the point forecast, with residual uncertainty mainly from possible RNA dropout or a sparse high-effect TRPV4-positive subpopulation.

Predicted `n_degs`: **0**
