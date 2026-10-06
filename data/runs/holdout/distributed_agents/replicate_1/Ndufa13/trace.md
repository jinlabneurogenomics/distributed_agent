# Ndufa13 held-out DEG-count prediction

## Question and endpoint

The requested prediction is the withheld `n_degs` value for one genetic perturbation, `Ndufa13`, in the focal `151 TH Prkcd Grin2c Glut` neuronal group. I interpret `n_degs` as the number of measured nuclear transcripts, including the perturbed target transcript itself, with Scanpy Wilcoxon Benjamini-Hochberg adjusted `pvals_adj < 0.05` in perturbed versus matched non-targeting-control nuclei.

`Ndufa13` was completely held out: it was absent from both `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` and from `training_de_all_cell_groups.parquet` as a `gene_target`. Its transcript was nevertheless in the measured-gene space; there was an `Ndufa13` row for each of the 1,674 visible training perturbations in the focal cell group. Thus a withheld `Ndufa13` perturbation could score either because its own RNA passed FDR or because downstream RNAs responded.

## Sources used

- Declared DE input parquet: `training differential-expression dataset`.
- Declared focal training counts: `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
- Requested-target manifest: `single-target request for Ndufa13`.
- Run-local dataset portrait, bindings, coverage, and measurement registry under `codex_runtime/pipeline`.
- Same-experiment July 260713 SourceGuard 1773 v1 report corpus for visible Complex I analogs, inspected only as packaged interpretation of the same Perturb-seq experiment, not as independent replication.
- External references from PubMed and MitoCarta3.0: Rath et al. 2021, MitoCarta3.0, DOI 10.1093/nar/gkaa1011, PMID 33174596; Huang et al. 2004 on GRIM-19/NDUFA13 as an essential Complex I component, DOI 10.1128/MCB.24.19.8447-8456.2004, PMID 15367666; Hwang et al. 2019 on GRIM-19 protein in adult mouse brain neurons, DOI 10.1007/s10571-019-00689-1, PMID 31111264; Gonzalez-Quintana et al. 2020 on biallelic NDUFA13 variants causing isolated Complex I/OXPHOS deficiency, DOI 10.3390/genes11080855, PMID 32722639; Tammineni et al. 2012 on a GRIM-19 function in STAT3 mitochondrial import, DOI 10.1074/jbc.M112.378984, PMID 23271731.

## Within-dataset calculation

I loaded the focal training-count CSV to calibrate the count scale and used `pyarrow.dataset` to filter the large parquet to rows with:

```python
(group_name == "151 TH Prkcd Grin2c Glut")
& gene_target in visible Complex I / OXPHOS analogs
```

For each analog I counted rows with `pvals_adj < 0.05`, identified whether the significant row was the perturbed transcript itself, and read the self-target log-fold change and FDR when that transcript was measured.

Visible structural Complex I subunits in the focal training set were all at the null/singleton boundary:

| analog set | targets | zeros | ones | median `n_degs` | max |
|---|---:|---:|---:|---:|---:|
| Structural `Nduf` subunits: `Ndufa10`, `Ndufa11`, `Ndufa12`, `Ndufa6`, `Ndufa8`, `Ndufa9`, `Ndufb10`, `Ndufb11`, `Ndufb3`, `Ndufb7`, `Ndufb8`, `Ndufb9`, `Ndufc2`, `Ndufs2`, `Ndufs4`, `Ndufs7`, `Ndufs8`, `Ndufv1`, `Ndufv2` | 19 | 9 | 10 | 1 | 1 |
| Structural subunits plus assembly factors `Ndufaf2`, `Ndufaf4`, `Ndufaf5` | 22 | 12 | 10 | 0 | 1 |

The focal expression evidence was singleton-like rather than module-like. `Ndufa10`, `Ndufa6`, `Ndufb10`, `Ndufb11`, `Ndufb8`, `Ndufb9`, `Ndufc2`, `Ndufs2`, and `Ndufs8` each had exactly one significant focal row and that row was the target transcript itself. `Ndufv2` also had one DEG, `Cdc40`, while its own transcript was not significant. The remaining visible structural Complex I perturbations had 0 focal DEGs. The three visible Complex I assembly-factor perturbations, `Ndufaf2`, `Ndufaf4`, and `Ndufaf5`, also had 0 focal DEGs. Other OXPHOS controls showed the same near-null scale: `Cox5a`, `Cyc1`, `Sdha`, `Uqcrc2`, and `Tomm40` each had one focal DEG, usually their own transcript, while many Complex III/IV perturbations were zero.

The July same-experiment reports for `Ndufa10`, `Ndufb10`, `Ndufs2`, and `Ndufs8` supported the same interpretation across all assayed cell groups: visible nuclear-encoded Complex I perturbations were not producing a shared ATF4/ATF5 mitochondrial ISR, UPRmt, redox, mitophagy, or OXPHOS module in the recovered neurons. The rare downstream FDR events outside the self-transcript were isolated genes in isolated cell groups rather than a reproducible Complex I response.

## Target-specific reasoning

### Ndufa13

`Ndufa13` encodes GRIM-19/NADH:ubiquinone oxidoreductase subunit A13, a nuclear-encoded accessory subunit of mitochondrial respiratory-chain Complex I. MitoCarta3.0 annotates it as a mitochondrial protein in the respiratory-chain/OXPHOS pathway, and Huang et al. showed that GRIM-19 localizes to Complex I and that complete mouse loss disrupts Complex I assembly and electron-transfer activity with embryonic lethality. Human biallelic NDUFA13 variants can produce isolated Complex I deficiency, reduced NDUFA13 protein and respirasomes in fibroblasts, and Leigh-spectrum neurodevelopmental disease. Hwang et al. found GRIM-19 broadly but heterogeneously expressed in adult mouse brain, predominantly in neurons. These external data make visible Complex I subunit perturbations the appropriate in-dataset analogs and argue against treating `Ndufa13` as a biologically irrelevant or unexpressed target.

The causal chain for this experiment is:

CRISPR indels in `Ndufa13` -> reduced GRIM-19 protein in a subset of edited postmitotic neurons -> impaired Complex I assembly or activity if residual protein and pre-existing assembled enzyme fall below threshold -> possible ATP/redox/mitochondrial stress signaling in surviving neurons -> recovery of those nuclei in `151 TH Prkcd Grin2c Glut` -> Wilcoxon DE calls after BH correction.

The visible Complex I data show that this chain usually stopped at or before a broad nuclear stress response. Even core or assembly-relevant Complex I targets such as `Ndufs2`, `Ndufs4`, `Ndufs7`, `Ndufs8`, `Ndufv1`, `Ndufv2`, `Ndufa10`, and `Ndufb10` produced only 0 or 1 focal DEGs. Where focal hits were present they were mostly direct self-transcript depletion, not recurrent secondary mitochondrial transcripts. That is the closest assay-matched evidence for an acute, sparse P16 CRISPR perturbation of `Ndufa13`: loss of an individual nuclear Complex I subunit is an obligate-complex lesion in principle, but the observed survivor-conditioned snRNA readout is strongly buffered.

I therefore predict a nonzero but minimal focal count:

- **Zero/nonzero decision:** weakly nonzero. A true large downstream signature is not supported by the training Complex I panel. However, `Ndufa13` is an expressed structural Complex I subunit rather than a low-visibility assembly factor, and 10/19 visible structural Complex I subunits had exactly one focal DEG.
- **Approximate count:** 1 DEG. The best analog counts are bounded at 0 or 1; choosing 1 places `Ndufa13` with the self-transcript-positive structural subunits (`Ndufa10`, `Ndufa6`, `Ndufb10`, `Ndufb11`, `Ndufb8`, `Ndufb9`, `Ndufc2`, `Ndufs2`, `Ndufs8`) rather than with the zero assembly factors.
- **Counterexamples:** `Ndufa11`, `Ndufa12`, `Ndufa8`, `Ndufa9`, `Ndufb3`, `Ndufb7`, `Ndufs4`, `Ndufs7`, and `Ndufv1` were equally plausible Complex I comparators and had 0 focal DEGs, so the sign of the singleton call is uncertain. The one non-self hit in `Ndufv2` (`Cdc40`) was not mechanistically recurrent and does not argue for a larger `Ndufa13` count.
- **External biology not over-weighted:** GRIM-19 also interacts with STAT3 and can affect apoptosis or inflammatory pathways in tumor, macrophage, and cardiac settings. Those studies establish additional molecular roles, but they do not put an FDR-level STAT3, apoptosis, or inflammatory program into postnatal thalamic glutamatergic neurons after mosaic CRISPR. They were not used to inflate the count.

## Limits

This is a one-gene extrapolation from analogs rather than a direct `Ndufa13` measurement. The nearest Complex I analogs split almost evenly between 0 and 1 DEG in the focal group, so the integer boundary is intrinsically unstable. The prediction mainly distinguishes "none or singleton" from "broad response"; it is much better supported against a large count than against zero. Because the input parquet lacks raw guide identities, indel rates, per-nucleus expression, and the actual recovered `Ndufa13` nuclei, I cannot tell whether `Ndufa13` would cross FDR through stronger self-transcript depletion, weaker self-transcript depletion, or a rare non-self singleton. Finally, the same-experiment corpus is a curated interpretation of this same screen and was used only to confirm that visible Complex I reports did not hide a broad downstream mitochondrial-stress program; it is not independent biological replication.
