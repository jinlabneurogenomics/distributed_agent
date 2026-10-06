# Direct Sdhb n_degs forecast for 151 TH Prkcd Grin2c Glut

## Target and endpoint

- Target from the one-row holdout manifest: `Sdhb`.
- Cell context: `151 TH Prkcd Grin2c Glut`.
- Endpoint: number of measured genes in that class with BH-adjusted Wilcoxon `pvals_adj < 0.05`.
- The declared `Sdhb` biology bundle was used as a biology-only prior; the held-out `Sdhb` perturbation signature and `Sdhb` endpoint were not queried or reconstructed.

## Sdhb biology prior

- The in-assay focal expression card reports detectable non-target `Sdhb` expression in 16,626 of 23,679 focal non-target nuclei, 70.214% expressing, mean log1p CP10K 0.535, and pseudobulk CPM 88.29. Thus the target transcript is observable in this 151 population.
- SDHB is the obligate iron-sulfur subunit of respiratory complex II. The functional-stock adjudication judged post-edit SDHB as `likely_substantially_depleted` by harvest: the thalamic protein half-life prior is about 12.82 days, so a P16 disruptive edit should erode most newly supplied functional stock across the P37-P44 harvest window.
- That supported real biological engagement, but not a high-count forecast by itself, because complex-II enzymatic activity, residual assembled protein, cellular survival, and absolute respiration were not measured in this snRNA-seq endpoint.

## Training counts in the exact focal class

The declared 151-count table contains 1,674 training perturbations. Its distribution is sparse:

- 1,205 / 1,674 have `n_degs = 0`.
- 1,481 / 1,674 have `n_degs <= 1`.
- median `n_degs = 0`; 75th percentile `= 1`.
- the mean is inflated to 14.05 by a small responder tail headed by `Uba5`, `Tpr`, `Sin3a`, `Rnpc3`, and other non-OXPHOS broad responders.

The biologically closest measured analog was `Sdha`, the catalytic partner in the same four-subunit complex-II assembly. In `151 TH Prkcd Grin2c Glut`, `Sdha` had `n_degs = 1`. Direct Parquet inspection showed that the FDR<0.05 call was the perturbed transcript itself:

```text
Sdha / Sdha: logFC -0.7809, score -8.2808, p_adj 2.11e-12
Sdha / Edem2: logFC -0.7681, score -4.4795, p_adj 0.0646
```

So the matched complex-II anchor had a formal 151 signal, but no downstream 151 gene crossed the requested 0.05 threshold.

A respiratory-chain / TCA / mitochondrial-import cohort drawn from the same count table was also uniformly tiny:

```text
Aco2 0; Cox5a 1; Cox8a 0; Dld 0; Dlst 0; Idh3a 1; Mdh2 1;
Ndufa10 1; Ndufa11 0; Ndufb10 1; Ndufs2 1; Ndufs4 0; Ndufv1 0;
Ndufv2 1; Sdha 1; Tomm40 1; Uqcrc2 1; Uqcrfs1 0; Uqcrq 1
```

Across these 19 observed structural/metabolic peers, the maximum focal count was 1, with 8 zeros and 11 ones. The one-count cases were usually self-transcript calls rather than broad stress modules.

## Same-experiment corpus and profile checks

Packaged same-experiment reports for the measured anchors matched the raw counts:

- `Sdha` was summarized as a broadly buffered neuronal RNA response across all 23 groups, with only `Ndrg4` in `012 MEA LA CA1 DG Glut` and `Edem2` in `151 TH Prkcd Grin2c Glut` below FDR 0.10, and without HIF, mitochondrial ISR/UPRmt, NRF2/redox, or broad ER/ISR induction.
- `Ndufs2`, `Ndufs4`, `Uqcrc2`, `Uqcrfs1`, `Cox*`, and `Tomm40` reports likewise described flat or singleton OXPHOS surfaces and near-zero convergence among respiratory-chain peers.
- `Opa1` and `Uba5` were useful positive contrasts: the same 151-cell assay produced 37 and 2,677 FDR<0.05 genes respectively, so the OXPHOS nulls are not just a generic inability to detect mitochondrial/proteostasis states in these nuclei. Their mechanisms are mitochondrial dynamics and UFMylation rather than structural complex-II loss, so they bounded sensitivity but were not averaged into the complex-II point.

A 20-node profile comparison in the exact 151 population gave the same separation. `Sdha` had 1 significant feature and near-zero whole-profile similarity to the buffered OXPHOS peers; `Opa1` had 37 significant features; `Uba5` had 2,677 and was strongly similar to its E2 `Ufc1`. This kept `Sdhb` closest to `Sdha` / structural ETC behavior, not the `Uba5` responder branch.

## Point estimate

The final point estimate is `1`.

Rationale: `Sdhb` is expressed and its protein stock should be substantially reduced by harvest, making a completely unavailable perturbation less likely than for very low-expression targets. But the best task-matched quantitative analog, `Sdha`, had only a self-transcript FDR<0.05 call in 151, and all 19 nearby structural ETC/TCA peers had 0 or 1 focal DEG. I therefore forecast the common buffered structural-respiratory outcome: at most a self/on-target call and no broad secondary mitochondrial-stress signature.
