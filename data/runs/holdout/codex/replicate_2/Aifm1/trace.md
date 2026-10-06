# Direct Aifm1 forecast

## Target and endpoint

- Holdout target: `Aifm1`.
- Cell class: `151 TH Prkcd Grin2c Glut`.
- Endpoint: number of measured genes with BH-adjusted Wilcoxon `pvals_adj < 0.05`.
- `Aifm1` is absent from the declared focal training count table, which contains 1,674 other targets.

## Biology and expression evidence

The biology-only Aifm1 bundle supports real target reach but does not support a large acute survivor transcriptome as the default outcome.

- Focal expression is present and measurable: in matched non-target nuclei for `151 TH Prkcd Grin2c Glut`, `Aifm1` was detected in 15,067 of 23,679 nuclei, 63.63%, with pseudobulk CPM 70.76 and mean raw UMI 1.129.
- AIFM1 has a baseline mitochondrial pool that supports respiratory-chain complex-I biogenesis or maintenance; the apoptotic death-effector role is separable and should not be assumed without an added stress trigger.
- A null-like P16 edit is expected to stop new AIFM1 supply while mature AIFM1 and dependent respiratory material decay over time. The functional-stock card therefore calls the P37-P44 stock likely substantially depleted, but with only partial evidence because the direct 1-18 day depletion measurement is from proliferating fibroblasts and the closest neural phenotype is delayed and outside the assayed thalamic population.
- The exact expression reach argues against a target-absent null, while the postmitotic timing and survivor-conditioned nuclear RNA readout make a broad stress or death program uncertain.

## Training measurements used for scale

The focal training table is sparse:

- 1,205 of 1,674 targets had 0 DEGs.
- 1,481 of 1,674 had at most 1 DEG.
- Median count was 0; the 90th percentile was 2; the mean was 14.05 because a small number of targets had very large signatures.

The most direct local comparators were respiratory-complex subunits or assembly factors, because AIFM1 maintains complex-I/respiratory-complex function rather than acting as a broad transcriptional regulator.

In `151 TH Prkcd Grin2c Glut`, the 35 represented `Nduf*`, `Cox*`, `Uqcr*`, and `Sdha` training perturbations all had only 0 or 1 DEG:

- 0-DEG examples included `Ndufs4`, `Ndufs7`, `Ndufv1`, `Ndufa9`, `Ndufaf2`, `Ndufaf4`, `Ndufaf5`, `Cox4i1`, `Cox6a1`, `Cox11`, `Uqcrb`, `Uqcrfs1`, and `Uqcrh`.
- 1-DEG examples included `Ndufs2`, `Ndufs8`, `Ndufv2`, `Ndufa10`, `Ndufa4`, `Ndufa6`, `Ndufb10`, `Ndufb11`, `Ndufb8`, `Ndufb9`, `Ndufc2`, `Sdha`, `Uqcrc2`, and `Uqcrq`.
- In the full Parquet, this same comparator class was quiet outside the focal group too: `Ndufs4` had 0 DEGs across 20 recovered groups, and `Ndufs2` had only 7 DEGs total across 22 groups with a maximum of 3 in any one group.

The packaged corpus interpretation was consistent with those direct counts: `Ndufs2` was described as almost completely buffered and failing to activate an OPA1-like ATF4/ISR program, while `Ndufs4` was described as silent across its recovered neuronal groups and part of a broader complex-I class dominated by on-target mRNA decreases with little downstream transcription.

I treated `Opa1` and `Nrf1` as upward references rather than direct donors. They had larger focal counts, 37 and 138 respectively, and corpus findings describe `Opa1` as entering an ATF4/ISR-like amino-acid stress program and `Nrf1` as mixing a smaller mitochondrial strand with RNA-processing, DNA-maintenance, vesicle, and endolysosomal features. Those programs are biologically farther from AIFM1's complex-maintenance operation than the near-null `Nduf*`/COX/UQCR training set.

## Synthesis

AIFM1 is expressed in the assayed thalamic class and its functional stock should be at least partly realized by harvest, so I did not use a strict target-absent or failed-stock zero. But the closest measured respiratory-complex perturbations were at the assay floor in this same focal class, and the stronger mitochondrial stress examples required OPA1 morphology or NRF1 transcriptional-regulatory biology rather than isolated complex-I maintenance.

I therefore forecast an essentially floor-level response, allowing one BH-significant gene for the target transcript itself or a single immediate downstream transcript but not a resolved mitochondrial ISR module.

Point prediction: `1`.
