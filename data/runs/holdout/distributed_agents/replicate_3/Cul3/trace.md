# Cul3 prediction for `151 TH Prkcd Grin2c Glut`

## Question and resolved ambiguities

The requested held-out target list contains one gene, `Cul3`. The target was absent from both training inputs, so I treated its expression profile and exact DEG count as unavailable and transferred from non-held-out perturbations only. The endpoint I predicted is the assay-specific count of measured genes with `pvals_adj < 0.05` in the focal thalamic glutamatergic class, not viability, target editing, behavioral severity, or a generic measure of CUL3 biological importance.

I used the `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` endpoint file for exact focal-cell counts and re-read the parquet only for the same focal cell group when I needed signed expression details. For a focal group/target I counted:

```python
n_degs = (rows.pvals_adj < 0.05).sum()
```

Expression-pattern comparisons used the focal-cell `scores` vectors, because they preserve genome-wide signed Wilcoxon rank information even when a perturbation has no FDR-significant genes. The runtime comparison used top-200 positive and negative score tails plus full-vector Pearson/cosine similarities for the declared candidate set.

## Sources

Internal experiment/data sources:

- `[local file: training_de_all_cell_groups.parquet]`
- `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`
- `[local file: 048_Cul3.csv]`
- Distributed Agents corpus `perturbai-july-260713-sourceguard-1773-v1`. This release had no direct `Cul3` report (`target_found=false`), but it had curated same-experiment reports for the observed BTB/KCTD/KLHL and proteostasis comparator targets.
- Distributed Agents runtime profile artifacts generated in this run: `cul3_candidate_compare.json` and `cul3_candidate_cohort.json`.

External biological knowledge:

- NCBI PubMed records for CUL3/CRL3, KEAP1/NRF2, and CUL3/KCTD13/RhoA biology.
- Wang, Song and Ye 2020, PMID 31898230, DOI 10.1007/978-981-15-1025-0_13: CRL3 review summarizing CUL3 as the Cullin-RING scaffold used by many BTB substrate adaptors.
- Zhang et al. 2004, PMID 15572695, DOI 10.1128/MCB.24.24.10941-10953.2004: KEAP1 assembles with CUL3/RBX1 to ubiquitinate NRF2.
- Lin et al. 2015, PMID 25695269, DOI 10.1016/j.neuron.2015.01.010: neuropsychiatric 16p11.2 network analysis identifying a KCTD13-CUL3-RhoA axis.
- Escamilla et al. 2017, PMID 29088697, DOI 10.1038/nature24470: mouse Kctd13 deletion increases RhoA and reduces synaptic transmission.
- Amar et al. 2021, PMID 33727673, DOI 10.1038/s41380-021-01052-x: germline Cul3 haploinsufficiency affects brain development and cytoskeletal/RhoA signaling.

## Within-dataset calibration

The focal-cell training endpoint is strongly zero-inflated: among 1,674 observed perturbations, 1,205 had `n_degs = 0`, the median was 0, the 75th percentile was 1, and only a long tail reached hundreds or thousands of genes. This matters because a famous or pleiotropic gene should not be assigned a broad transcriptional footprint unless observed analogs in this same sparse P16 CRISPR/snRNA assay support that transfer.

I therefore separated three classes of observed perturbations.

Direct or near-direct CRL3 adaptor-side analogs, all weak in the focal class:

| observed perturbation | focal `n_degs` | focal pattern |
| --- | ---: | --- |
| `Btbd9` | 0 | no adjusted hits; strongest genes had `pvals_adj = 1` |
| `Kbtbd7` | 0 | no adjusted hits |
| `Klhl7` | 0 | no adjusted hits |
| `Klhl20` | 0 | no adjusted hits |
| `Kctd1` | 2 | `Resp18` up, `Cluap1` down |
| `Kctd8` | 0 | no adjusted hits |
| `Kctd16` | 0 | no adjusted hits |

These are not perfect CUL3 substitutes because CUL3 is the scaffold and each listed gene is only one substrate adaptor or KCTD-family relative. Still, they are the closest measured CRL3-adjacent losses in the training set. Distributed Agents corpus reports reinforced the focal counts: `Btbd9` was a true transcriptomic null across recovered neuronal classes, and its report explicitly found no basal ubiquitin, proteasome, autophagy, ISR, or UPR program and no phenocopy by `Kbtbd7`, `Klhl7`, or `Klhl20`; `Klhl7` was also flat across recovered groups; `Klhl20` produced only singleton hits outside the focal cell class and did not converge with autophagy/Rho/BTB relatives; `Kctd1` produced a tiny, cell-type-restricted response and did not phenocopy `Kctd8`/`Kctd16`; and `Kctd16`/`Kctd8` were flat on the GABA_B auxiliary axis. These same-experiment corpus findings argue that loss of one BTB/Kelch or KCTD adaptor usually does not collapse neurons into a common CRL3-loss nuclear RNA state.

The focal-cell expression profiles agreed with the count-level story. Over the focal `scores` vectors, BTB/KCTD/KLHL pairs had near-zero full-vector similarity and minimal top-tail overlap: examples include `Btbd9` versus `Klhl7`, cosine 0.011 and 2.5% positive/3.5% negative top-200 overlap; `Klhl7` versus `Klhl20`, cosine -0.015 and 2.0%/2.5% top-200 overlap; `Kctd1` versus `Kctd8`, cosine 0.021 and 2.0%/3.0% top-200 overlap; and `Kctd1` versus `Kctd16`, cosine 0.034 and 2.5%/1.5% overlap. The tiny observed `Kctd1` signature therefore did not nominate a reusable CRL3 adaptor module.

NRF2/redox branch counterexamples:

| observed perturbation | focal `n_degs` | interpretation |
| --- | ---: | --- |
| `Nfe2l2` | 0 | NRF2 loss was transcriptionally silent in basal focal cells |
| `Nfe2l1` | 0 | FDR-flat in the focal class, with only subthreshold proteostasis ranks |

KEAP1 was not present in the training targets, so the direct predicted CUL3 direction, NRF2 stabilization after losing the KEAP1-CUL3 ligase, could not be measured. The fact that `Nfe2l2` loss was flat does not rule out NRF2 gain after `Cul3` loss, but it makes a broad oxidative-stress program less compelled in unchallenged juvenile NeuN+ nuclei.

Proteostasis and endolysosomal counterexamples:

| observed perturbation | focal `n_degs` | expression evidence |
| --- | ---: | --- |
| `Psmb4` | 742 | broad proteasome signature |
| `Psmc1` | 430 | broad, highly correlated with `Psmb4`: Pearson 0.652, 215 shared same-direction FDR genes |
| `Uba5` | 2,677 | massive UFMylation/protein-homeostasis footprint |
| `Ufc1` | 572 | same UFMylation pathway; Pearson 0.751 with `Uba5` |
| `Gigyf2` | 17 | sparse ER/RNA-processing response, with `Xbp1` and `Selenok` up but not global proteotoxic stress |
| `Rab7` | 501 | broad endolysosomal signature |
| `Huwe1` | 158 | broader E3-ligase/RNA-stress signature than CRL3 adaptors |

These genes show that the focal cell class can produce large protein-quality-control, lysosomal, and ubiquitin-associated signatures when the perturbed node is limiting. They are important upper-bound counterexamples, not good quantitative analogs for `Cul3`: their score profiles formed a separate high-burden cluster, whereas all direct BTB/KCTD/KLHL adaptor perturbations remained flat to tiny. For example `Psmb4` versus `Psmc1` had cosine 0.659; `Uba5` versus `Ufc1` had cosine 0.761; but `Btbd9` versus `Psmb4`, `Kctd1` versus `Psmb4`, `Kctd8` versus `Psmb4`, and `Nfe2l2` versus `Psmb4` all had cosines within roughly -0.03 to 0.00.

Autophagy/Rho-adjacent counterexamples:

| observed perturbation | focal `n_degs` | reason for comparison |
| --- | ---: | --- |
| `Cdc42` | 1 | Rho-family cytoskeletal GTPase, but only self-target RNA passed FDR |
| `Becn1` | 0 | autophagy regulator |
| `Rb1cc1` | 4 | autophagy-initiation scaffold with a very small ER-chaperone/self signature |
| `Map1lc3a` | 1 | autophagy marker; only self-target RNA passed FDR |

Those genes bound the canonical KLHL20/autophagy/Rho substrate stories reported by the Distributed Agents corpus. In the same focal thalamic cells they again supported a small count rather than a broad transcriptional collapse.

## Cul3 target-specific rationale

`Cul3` differs from the observed adaptors because it is the core cullin scaffold for CRL3 ligases. Wang, Song and Ye 2020 note that mammalian CUL3 can be wired to many BTB substrate receptors, so losing the scaffold could accumulate weak defects from multiple adaptors even when `Btbd9`, `Klhl7`, `Klhl20`, `Kctd1`, `Kctd8`, and `Kctd16` single-gene losses were null or nearly null. The external literature gives two plausible neuron-relevant branches absent from the focal training set: the KCTD13-CUL3-RhoA axis implicated by Lin et al. 2015 and Escamilla et al. 2017, and a broader Cul3/RhoA cytoskeletal phenotype in the Amar et al. 2021 mouse haploinsufficiency study.

I did not let those developmental papers drive the count upward very far. They used germline or developmental contexts rather than this P16 sparse CRISPR perturbation, the relevant adaptor `Kctd13` and the direct CRL RING partner `Rbx1` were not training perturbations, and the measurable focal-cell Rho/autophagy comparators were all 0-4 DEGs. Likewise, the KEAP1-NRF2 branch is a real CUL3 mechanism according to Zhang et al. 2004, but the direct adaptor `Keap1` was absent and `Nfe2l2` was flat in basal focal cells.

I therefore predict `Cul3` as nonzero but small: larger than the one-adaptor KCTD/KLHL nulls because a scaffold perturbation can hit several branches at once, but far below `Gigyf2` and far, far below the proteasome/UFMylation counts that would require a coherent protein-quality-control response. The final point estimate is 6 DEGs.

## Limits

This is an extrapolation from partial pathway pieces rather than a direct paralog. No other cullin scaffold, no `Rbx1`, no `Keap1`, and no `Kctd13` training perturbation was available in the focal table, so the strongest external CUL3 mechanisms could not be profiled directly in-dataset. Acute postnatal CRISPR in surviving NeuN+ nuclei may miss protein-turnover, RhoA activity, dendritic, developmental, electrophysiological, glial, and circuit consequences of CUL3 loss. The broad proteostasis perturbations prove that the cell class can respond, but they are mechanistically downstream or parallel stress states rather than CUL3 phenocopies. Finally, `n_degs` is sensitive to recovered nuclei and FDR thresholding, so the difference between a strict null and a handful of genes is intrinsically less reliable than the distinction between a few genes and a several-hundred-gene proteotoxic program.
