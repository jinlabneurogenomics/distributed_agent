# Direct forecast trace

## Target and endpoint

- Target: `Ndufs3`
- Focal population: `151 TH Prkcd Grin2c Glut`
- Endpoint: `n_degs`, the number of measured genes in this population with BH-adjusted Wilcoxon `p < 0.05`
- Point forecast: `1`

The holdout manifest contains only `Ndufs3`. I treated the focal count table and the Parquet as the declared training measurement surface; `Ndufs3` was absent from the training count table, and I did not use a held-out `Ndufs3` DE profile or count.

## Biology prior for `Ndufs3`

The canonical biology bundle makes `Ndufs3` a strong-expressed but temporally buffered target in the requested assay:

- Exact non-target expression in `151 TH Prkcd Grin2c Glut`: `Ndufs3` was detected in 22,000 of 23,679 non-target nuclei, or 92.9%, with mean raw UMI 3.38 and mean log1p CP10K 1.045. This makes the target transcript observable in the focal population, while not itself proving functional editing.
- Functional operation: NDUFS3 is a nuclear-encoded core Q-module component of respiratory complex I, and the relevant functional pool is installed respiratory complex I rather than free transcript.
- Stock timing: the closest postnatal-neuronal conditional model retained near-control NDUFS3 at one month and declined later, whereas faster HEK293 exchange and mouse-heart turnover only established renewal potential. The bundle therefore adjudicated P16-to-P37/P44 loss as `partially_depleted_or_leading_edge`.
- Redundancy: no close mouse paralog or normal substitute for NDUFS3 in complex I was found, but the timing evidence argues against complete clearance of pre-existing complex-I stock by the 21-28 day harvest window.

I read this as high opportunity for a detectable self-transcript decrease but weak support for a broad downstream complex-I crisis in recovered thalamic nuclei.

## Training perturbations that set the numeric scale

The visible Complex-I subunit and assembly-factor perturbations in the focal training table were nearly all 0 or 1:

```text
Ndufs2   1
Ndufs7   0
Ndufs8   1
Ndufa9   0
Ndufa10  1
Ndufa11  0
Ndufa12  0
Ndufa6   1
Ndufa8   0
Ndufs4   0
Ndufv1   0
Ndufv2   1
Ndufaf2  0
Ndufaf4  0
Ndufaf5  0
Timmdc1  0
```

That 16-target NDUF/NDUFAF/Timmdc1 cohort has 11 zeros, 5 ones, and mean focal `n_degs = 0.31`. The nearest core Complex-I set was similarly sparse: `Ndufs2 = 1`, `Ndufs7 = 0`, `Ndufs8 = 1`, `Ndufa9 = 0`, `Ndufs4 = 0`, `Ndufv1 = 0`, and `Ndufv2 = 1`.

Exact Parquet rows showed that the 1-count structural-subunit hits were mostly self-transcript calls rather than a downstream stress program. In the focal class, the sole significant row for `Ndufs2` was `Ndufs2` itself (`logFC = -0.728`, `padj = 8.3e-12`), the sole significant row for `Ndufs8` was `Ndufs8` itself (`logFC = -0.650`, `padj = 3.1e-08`), and the same self-only pattern held for `Ndufa10`, `Ndufa6`, and the broader respiratory comparators `Cox5a`, `Ndufa4`, `Mdh2`, `Sdha`, and `Uqcrc2`. `Ndufs7`, `Ndufa9`, `Ndufs4`, `Ndufv1`, and multiple NDUFAF assembly factors had no focal FDR-significant gene.

I treated `Opa1`, `Nrf1`, and `Esrra` as positive respiratory or mitochondrial-stress controls rather than scale donors for `Ndufs3`: they had focal counts of 37, 138, and 57 respectively, but they are regulatory or mitochondrial-dynamics perturbations with broad downstream programs not reproduced by acute core NDUF perturbations.

## Same-experiment corpus and profile checks

The selected corpus had no packaged `Ndufs3` Finding or explicit report edge, so I used it only for the visible Complex-I analogues. The Ndufs2/Ndufs8/Ndufa9 report layer and the higher-order Complex-I Claim consistently described represented nuclear Complex-I subunits and NDUFAF factors as transcriptionally buffered in juvenile postnatal neurons, without a shared acute OXPHOS-stress module. This is a semantic view of the same experiment, not independent replication of the Parquet counts.

A run-local profile comparison among 29 respiratory-chain and mitochondrial controls reinforced that interpretation. Within the 16-member NDUF/NDUFAF/Timmdc1 cohort, 120 of 120 pairwise comparisons were available, the median top-tail overlap coefficient was only `0.01` in both directions, and significant-program overlap was effectively absent. Pairwise score correlations between `Ndufs2`, `Ndufs7`, `Ndufs8`, `Ndufa9` and other NDUF/NDUFAF/respiratory peers were near zero with no shared significant genes; comparisons against `Opa1` and `Nrf1` likewise did not share the large stress signatures with the core Complex-I nodes.

## Synthesis

The all-training base rate in this focal class is zero-heavy: 1,205 of 1,674 visible perturbations are zero and 1,546 are five or fewer. The target-specific prior nevertheless lifts `Ndufs3` above a pure zero forecast because the exact focal population expresses `Ndufs3` robustly and its closest measured Q-module peers, `Ndufs2` and `Ndufs8`, each produced one focal call corresponding to their own transcript.

I did not project the broader `Opa1`/`Nrf1` mitochondrial stress scale onto `Ndufs3`, because the visible nuclear Complex-I structural and assembly perturbations were buffered, mutually nonconvergent, and frequently self-only. The delayed installed-stock biology further argues that a P16 `Ndufs3` edit should often remain below the threshold for a large survivor nuclear-RNA response by P37-P44. The best integer forecast is therefore a near-null, self-only outcome:

```text
predicted_n_degs = 1
```
