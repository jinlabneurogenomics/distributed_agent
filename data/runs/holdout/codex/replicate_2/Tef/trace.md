# Direct Tef DEG-count prediction

## Target and endpoint

- Target: `Tef`.
- Endpoint: `n_degs`, the number of measured genes in `151 TH Prkcd Grin2c Glut` with BH-adjusted Wilcoxon `p < 0.05`.
- Point prediction: `0`.

## Evidence used

### Biology-only Tef bundle

- Exact focal reach is not limiting. In the target expression card, `Tef` is available in the focal population and is detected in 20,305 of 23,679 non-target thalamic glutamatergic nuclei, or 85.751%, with mean raw UMI 2.414 and mean log1p CP10K 0.819.
- The functional-stock adjudication says TEF is a renewed soluble nuclear PAR-bZIP transcription factor and is likely substantially depleted 21-28 days after P16 CRISPR disruption. A quiet profile therefore would not be explained by a durable pre-edit protein stock alone.
- The same bundle also marks observability as strongly buffered: the postnatal neural phenotype is from combined germline loss of `Tef`, `Dbp`, and `Hlf`, while retained Tef-bearing genotypes in that family avoided the generalized seizure phenotype. Thus there is direct mouse-brain evidence for PAR-BZIP family redundancy, but not for an acute `Tef`-single-loss thalamic phenotype.

### Held-in focal count table

- `Tef` is absent from the declared `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`; no target outcome was used.
- The focal-class training endpoint is heavily concentrated at very small counts:

| count bin | held-in targets |
| --- | ---: |
| `n_degs = 0` | 1205 / 1674 |
| `n_degs <= 1` | 1481 / 1674 |
| `n_degs <= 2` | 1512 / 1674 |
| `n_degs >= 10` | 106 / 1674 |

- The closest named family members in the Tef card, `Dbp` and `Hlf`, are not held-in perturbations in either the count table or the declared training Parquet, so there is no measured PAR-BZIP single-perturbation profile to transfer.
- Held-in circadian/nuclear-receptor transcriptional regulators were heterogeneous in the same count table: `Rorb` = 0, `Rorc` = 0, `Cry1` = 1, `Nr1d2` = 1, `Clock` = 3, `Cry2` = 3, `Nr1d1` = 116, and `Rora` = 278. A symmetric `151 TH Prkcd Grin2c Glut` profile comparison of these eight observed targets gave two null nodes, four 1-9 DEG nodes, and two broad responders, so shared circadian or transcription-factor annotation did not define a uniform large-DEG response state.

## Synthesis

The Tef perturbation should be expressed and functionally realized by harvest, which argues against treating it as a technical dropout. However, the biological prior is a buffered Tef-only transcription-factor loss, the direct PAR-BZIP comparators are unmeasured, and the task-matched training distribution puts the empirical mode and median at zero with 88.5% of held-in targets at zero or one DEG. I therefore used the low-count part of the distribution, not the heavy positive tail, and chose the modal sparse outcome:

`predicted_n_degs = 0`
