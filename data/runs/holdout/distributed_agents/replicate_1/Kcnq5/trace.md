# Held-out DEG-count prediction for `151 TH Prkcd Grin2c Glut`

## Question and endpoint

The requested held-out target is `Kcnq5`. I interpreted the task as a scalar point prediction for the number of rows that would have `pvals_adj < 0.05` if the acute AAV-CRISPR `Kcnq5` loss-of-function perturbation had been present in the `151 TH Prkcd Grin2c Glut` differential-expression table.

The endpoint is directly observed for non-held-out training perturbations in `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`; it is absent by construction for `Kcnq5`. I treated self-transcript rows the same way as the provided count file does: the `Kcnq2` and `Kcnq3` training counts are both 1, and direct focal Parquet queries show that these one-gene counts are their own target-transcript decreases. Downstream genes such as `Agap2` for `Kcnq2` were not counted unless they crossed the strict `pvals_adj < 0.05` threshold.

There was no ranked or partially ranked supervision. The requested-target CSV contained exactly:

```text
target_name
Kcnq5
```

## Sources used

- Declared focal training DEG counts, 1,674 non-held-out targets.
- Declared differential-expression Parquet, queried only for non-held-out perturbations and the focal group or close channel comparators. The relevant columns were `names`, `gene_target`, `group_name`, `logfoldchanges`, `pvals_adj`, `scores`, `n_pert_matched`, and `n_ctrl_matched`.
- The selected same-experiment semantic corpus, `perturbai-july-260713-sourceguard-1773-v1`, for packaged `Kcnq1`, `Kcnq2`, and `Kcnq3` July PerturbAI reports and their evidence tables. This corpus is a literature-grounded interpretation of the same Perturb-seq experiment, not independent replication.
- PubMed-indexed literature on Kv7/KCNQ channels:
  - Schroeder et al., 2000, J Biol Chem, DOI `10.1074/jbc.M003245200` showed that KCNQ5/Kv7.5 is broadly expressed in brain, mediates M-type currents, and can heteromerize with KCNQ3.
  - Schwake et al., 2006, J Neurosci, DOI `10.1523/JNEUROSCI.5017-05.2006` defined assembly determinants for KCNQ/Kv7 heteromerization and noted the physiological importance of KCNQ3 heteromers with KCNQ2 or KCNQ5.
  - Ekberg et al., 2007, J Biol Chem, DOI `10.1074/jbc.M609385200` studied KCNQ2/3 and KCNQ3/5 channels and their regulation by Nedd4-2.
  - Brown and Passmore, 2009, Br J Pharmacol, DOI `10.1111/j.1476-5381.2009.00111.x` reviewed neuronal KCNQ/Kv7 channels as M-current channels that regulate excitability.
  - Tzingounis et al., 2010, PNAS, DOI `10.1073/pnas.1004644107` found that KCNQ5 contributes to medium and slow afterhyperpolarization currents in hippocampal CA3 in a cell-type-specific fashion.
  - Soh et al., 2022, PNAS, DOI `10.1073/pnas.2117640119` showed that KCNQ2 and KCNQ5 can form native heteromeric brain channels independently of KCNQ3 and are compatible with KCNQ2/3/5 heteromers.

## Computational checks over the declared inputs

The focal training count distribution was highly zero-inflated:

- `n = 1674` training perturbations, all unique.
- `1205 / 1674` had `n_degs = 0`.
- Median `n_degs = 0`; 75th percentile `= 1`; 90th percentile `= 2`; 95th percentile `= 18`.
- The large focal responses were rare and were dominated by spliceosome, proteasome, RNA-processing, and transcriptional-regulatory targets such as `Uba5`, `Tpr`, `Sin3a`, `Rnpc3`, `Zbtb7a`, `U2af2`, and `Psmb4`.

I then enumerated screened ion-channel and receptor analogs and compared their focal `n_degs` to `Kcnq5`:

```text
Kcnq paralogs: Kcnq1=0, Kcnq2=1, Kcnq3=1
Voltage-gated K channels: Kcna1=0, Kcna2=0, Kcnb1=0, Kcnb2=0,
  Kcnc1=0, Kcnc2=1, Kcnc3=1, Kcnd3=0, Kcnh1=0, Kcnh5=0, Kcnab2=1, Kcnj6=0
HCN and sodium channels: Hcn1=0, Hcn2=1, Scn1a=1, Scn1b=2, Scn2a=1, Scn3a=0, Scn8a=1
NMDA/AMPA controls: Grin1=89, Grin2a=1, Grin2b=2, Grin2d=0, Grin3a=0, Gria1=0, Gria2=0, Gria3=0
```

For each close channel target I also re-counted the Parquet rows in `151 TH Prkcd Grin2c Glut` with `pvals_adj < 0.05` and `< 0.10`. The training CSV exactly matched the strict FDR 0.05 counts. In the two closest neuronal Kv7 perturbations:

- `Kcnq2`, 283 perturbed nuclei versus 23,679 controls, had `Kcnq2` itself as the only focal FDR<0.05 row: `logfoldchanges = -0.775903`, `pvals_adj = 2.12e-28`. Its nearest downstream focal feature was `Agap2`, `logfoldchanges = 0.283634`, `pvals_adj = 0.050867`, just outside the requested threshold.
- `Kcnq3`, 211 perturbed nuclei versus 23,679 controls, had `Kcnq3` itself as the only focal FDR<0.05 row: `logfoldchanges = -0.379112`, `pvals_adj = 0.007168`. `Agap2`, `Bdnf`, `Coq2`, `Gdpd1`, `Kcnq2`, and `Kcnq5` were all `pvals_adj = 1.0`.
- `Kcnq1`, a non-neuronal Kv7-family counterexample, had 280 perturbed nuclei and zero FDR<0.05 or FDR<0.10 rows in the focal group.

Across all cell groups, the represented Kv7 family also looked sparse rather than like a broad stress module. `Kcnq1` had zero FDR<0.05 or FDR<0.10 calls in all 23 represented groups. `Kcnq2` mostly reported its self-transcript; the same-experiment report found only three downstream FDR<0.10 rows across 23 groups: `Bdnf` in `005 L4-5 IT CTX Glut`, `Rogdi` in `008 L2-3 IT ENT PPP RSP Glut`, and `Agap2` in the focal `151` class. `Kcnq3` had only two downstream FDR<0.10 rows across 22 groups, `Coq2` in `027 NP-CT-L6b-OB Glut` and `Gdpd1` in `155 MB Glut`; it had no focal downstream FDR<0.10 gene.

Finally, I queried `Kcnq5` as a measured gene, never as a held-out perturbation. In the focal group it never passed `pvals_adj < 0.10` under any of the 1,674 training perturbations; its minimum adjusted p-value was 0.626. In `Kcnq2` and `Kcnq3` focal perturbations specifically, the `Kcnq5` rows were flat (`pvals_adj = 1.0` with Wilcoxon scores -0.304 and 0.254). That argues against assigning an extra Kv7-compensation DEG to `Kcnq5` perturbation.

## Target-specific transfer

### `Kcnq5`

`Kcnq5` encodes Kv7.5, a neuronal potassium-channel subunit that can carry M-type current and participate in KCNQ3/5, KCNQ2/5, and likely KCNQ2/3/5 assemblies. At the direct molecular level, acute CRISPR loss should impair an M-current/afterhyperpolarization conductance rather than remove a transcription factor, spliceosome component, proteasome subunit, or metabolic enzyme. The propagated phenotype should therefore be a change in intrinsic excitability, and the RNA-seq endpoint would only move if that electrical perturbation was strong and sustained enough in surviving P37-P44 focal thalamic glutamatergic neurons to entrain activity-regulated, stress, channel-compensatory, or homeostatic transcription.

The best within-dataset analogs point to an endpoint near the assay threshold:

- `Kcnq2` is a close neuronal Kv7 partner. It produced `n_degs = 1` in the focal group, but that one FDR<0.05 row was only `Kcnq2` self-knockdown. Its `Agap2` focal downstream increase had the right direction for a tiny nonzero signal but stopped at FDR 0.0509, and the same-experiment corpus notes that even `Kcnq2` had only three downstream FDR<0.10 calls across the whole 23-class surface.
- `Kcnq3` is also a direct neuronal Kv7 partner and KCNQ5 can heteromerize with it. It likewise produced `n_degs = 1` in the focal group, explained by its own self-transcript decrease, with no downstream focal gene even at FDR<0.10.
- `Kcnq1` is a Kv7-family counterexample rather than a true neuronal analog: it produced no focal response and no all-cell FDR<0.10 downstream response, consistent with the literature distinction between KCNQ1/KCNE cardiac/epithelial biology and neuronal Kv7.2/7.3/7.5 M-current channels.
- Other pore-forming channel perturbations in this same focal cell group were mostly null or one self-transcript event: `Hcn2`, `Kcnab2`, `Kcnc2`, `Kcnc3`, `Scn1a`, `Scn2a`, and `Scn8a` were each `n_degs = 1`, while `Hcn1`, `Kcna1`, `Kcna2`, `Kcnb1`, `Kcnb2`, `Kcnd3`, `Kcnh1`, `Kcnh5`, and `Kcnj6` were 0. This is an important counterweight to any generic "neuronal excitability gene" prior.

The zero/nonzero boundary is therefore whether `Kcnq5` itself is likely to be detectable as a down-regulated target transcript in this focal class. The literature prior is that KCNQ5 is expressed broadly in brain and overlaps substantially with KCNQ2/KCNQ3 expression, but the same-experiment focal Parquet shows that `Kcnq5` was not a stable downstream readout under other perturbations, including direct `Kcnq2` and `Kcnq3` losses. I therefore expect no broad downstream program but assign one DEG for the target transcript itself, matching the observed focal breadth of `Kcnq2` and `Kcnq3`.

Predicted `Kcnq5 n_degs`: `1`.

## Limits

The prediction is a one-step extrapolation because `Kcnq5` was completely held out as a perturbation. The training data directly calibrate only `Kcnq1`, `Kcnq2`, and `Kcnq3`; `Kcnq4` and `Kcne` accessory-subunit perturbations were absent. The assay measures nuclear RNA weeks after sparse postmitotic editing, not M-current, afterhyperpolarization current, spike threshold, or guide-level indels, so electrophysiological effects of Kv7.5 loss can be real while producing zero downstream FDR-significant RNAs. The exact distinction between 0 and 1 hinges on focal `Kcnq5` expression and the strength of its self-transcript reduction, which are not observable without the held-out `Kcnq5` rows. I did not use `Kcnq5` target rows, withheld DEG counts, any grader/evaluation labels, or reports for the held-out perturbation.
