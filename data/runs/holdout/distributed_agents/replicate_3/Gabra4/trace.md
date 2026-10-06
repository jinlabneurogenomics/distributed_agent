# Gabra4 held-out DEG-count prediction

## Question interpreted

The run asks for the number of genes that would pass `pvals_adj < 0.05` after an acute AAV-CRISPR loss-of-function perturbation of each held-out target in `151 TH Prkcd Grin2c Glut` nuclei.  The count is assay-specific and includes any measured transcript, including the targeted gene itself when its own RNA is significantly depleted.

The requested manifest contained one held-out target:

| target | prediction |
|---|---:|
| Gabra4 | 1 |

I treated `Gabra4` as completely unobserved: it was not used as a `gene_target` in the parquet or as a training endpoint.  The prediction is therefore transferred from represented GABA receptor perturbations and external knowledge of alpha4-containing GABA_A receptors.

## Sources used

- Input endpoint table: `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
- Input DE table: `training_de_all_cell_groups.parquet`.
- Held-out manifest: `085_Gabra4.csv`.
- Distributed Agents same-experiment corpus release `perturbai-july-260713-sourceguard-1773-v1`.
- Run-local Distributed Agents profile tools:
  - `profile_compare` over 17 represented GABA receptor or inhibitory-synapse nodes in the focal cell group.
  - `profile_cohort` on the same node set to check whether they form a shared significant transcriptional module.
- NCBI PubMed for external thalamic GABA_A receptor biology.
  - Jia, Pignataro and Harrison 2007, DOI `10.1016/j.alcohol.2007.03.010`, PMID `17521848`.
  - Peng, Zhang, Chandra, Homanics, Olsen and Houser 2013, DOI `10.1007/s11064-013-1202-1`, PMID `24352815`.

The Distributed Agents corpus had no direct target context for `Gabra4`, so it contributed only indirect same-experiment claims for represented GABA_A comparators such as `Gabrb2`, `Gabrd`, `Gabra1`, `Gabra3`, and `Gabrg2`.

## Computational checks

I first confirmed that `085_Gabra4.csv` contains only `Gabra4`.  I then read the training count table and extracted receptor and inhibitory-synapse perturbations available in the focal cell group.  The represented classical GABA_A receptor subunits had very sparse endpoints:

| represented perturbation | focal `n_degs` |
|---|---:|
| Gabra1 | 1 |
| Gabra2 | 0 |
| Gabra3 | 0 |
| Gabra5 | 0 |
| Gabrb1 | 0 |
| Gabrb2 | 4 |
| Gabrb3 | 0 |
| Gabrd | 2 |
| Gabrg2 | 1 |
| Gabrg3 | 0 |
| Gabrr2 | 0 |

Nearby GABA handling or inhibitory synapse genes were also mostly self-only or flat in the same endpoint: `Gabbr1 = 1`, `Gabbr2 = 1`, `Arhgef9 = 1`, `Gad2 = 0`, `Gphn = 0`, `Slc6a1 = 0`, `Slc32a1 = 0`, and `Zkscan1 = 0`.

To determine which of the nonzero counts were target self-depletion and which were secondary responses, I filtered the parquet to `151 TH Prkcd Grin2c Glut`, the represented GABA comparison set, and `pvals_adj < 0.05`:

```sql
select gene_target, names, logfoldchanges, scores, pvals_adj,
       n_pert_matched, n_ctrl_matched
from read_parquet('training_de_all_cell_groups.parquet')
where group_name = '151 TH Prkcd Grin2c Glut'
  and gene_target in (
      'Gabra1','Gabra2','Gabra3','Gabra5',
      'Gabrb1','Gabrb2','Gabrb3',
      'Gabrd','Gabrg2','Gabrg3','Gabrr2',
      'Gabbr1','Gabbr2','Slc6a1','Gad2','Gphn','Arhgef9'
  )
  and pvals_adj < 0.05
order by gene_target, pvals_adj;
```

That yielded:

| perturbation | FDR<0.05 rows in 151 TH |
|---|---|
| Arhgef9 | `Arhgef9` down |
| Gabbr1 | `Gabbr1` down |
| Gabbr2 | `Gabbr2` down |
| Gabra1 | `Gabra1` down |
| Gabrb2 | `Gabrb2` down; `Nr4a1` up; `Vgf` up; `Nalf1` down |
| Gabrd | `Gabrd` down; `Cttnbp2` up |
| Gabrg2 | `Gabrg2` down |

Thus the closest represented GABA_A receptors were not producing broad hidden responses.  `Gabrb2` had three downstream FDR<0.05 genes plus its own transcript; `Gabrd` had one downstream gene plus its own transcript; `Gabra1` and `Gabrg2` were self-only; six other classical or rho-family subunits had zero FDR<0.05 rows.

The run-local profile comparison over 17 receptor/synapse nodes independently supported this sparsity.  Ten of the 17 nodes had no significant features in `151 TH`; the other seven had only 1-9 significant features.  The profile-cohort significant-program overlap coefficient was zero for the evaluable pairwise comparisons, so there was no shared FDR-significant mRNA module that could be transferred wholesale from `Gabrb2` or `Gabrd` to `Gabra4`.

## Same-experiment corpus evidence

The internal corpus made three points that are directly relevant to `Gabra4`.

First, the high-confidence `Gabrb2`/`Gabrd`/`Gabra2`/`Gabra3` claim states that `Gabrb2` loss selectively induced an activity-associated response in `151 TH Prkcd Grin2c Glut`, whereas represented `Gabra3`, `Gabra2`, `Gabrd`, `Gabrr2`, and `Slc12a2` perturbations did not reproduce that multi-gene response.  The `Gabrb2` finding behind the claim described `Nr4a1`, `Vgf`, `Fos`, `Npas4`, and `Homer2` as a broader FDR<0.10 activity-associated response after strong `Gabrb2` self-reduction.  This made `Gabrb2` a useful positive control that the assay can detect disinhibition/activity-like nuclear genes after a GABA_A perturbation, but also a counterexample to treating every GABA_A subunit as equivalent.

Second, a separate high-confidence corpus claim over `Gabra1`, `Gabra3`, `Gabrb2`, `Gabrg2`, `Glra3`, and `Gphn` concluded that represented GABA receptor subunits and inhibitory-synapse neighbors do not form a shared postnatal neuronal nuclear-RNA perturbation module.  That matched the profile-cohort result and argues against using receptor family membership alone.

Third, the `Gabrd` context specifically reported a one-downstream-gene response in `151 TH`, with `Cttnbp2` up-regulated while `Gabrd` was strongly reduced, and contrasted it with the more activity-gene-biased `Gabrb2` and `Gabrg2` responses.  The corpus also noted that the `Cttnbp2` feature recurred after several non-GABA_A perturbations, so I did not treat it as an alpha4/delta-specific marker.

## External biology used

`Gabra4` encodes the GABA_A receptor alpha4 subunit.  In thalamic relay neurons, alpha4 combines prominently with beta2 and delta subunits to form extrasynaptic receptors mediating tonic inhibition; alpha1, alpha4, beta2, and delta are heavily expressed in thalamic relay nuclei, and alpha4 knockout abolishes thalamocortical tonic inhibition and gaboxadol sensitivity according to the review by Jia et al. 2007.

That biology makes `Gabrd` and `Gabrb2` the best available in-dataset mechanistic comparators, because alpha4/beta2/delta receptors sit on the tonic-inhibition branch rather than the synaptic alpha1/beta/gamma branch.  Peng et al. 2013 further showed in alpha4 knockout mice that delta-subunit localization and expression are altered in the thalamic ventrobasal nucleus, with loss of delta labeling in neuropil and retention near the endoplasmic reticulum, supporting a tight alpha4-delta partnership.

At the same time, Peng et al. measured receptor protein localization, and Jia et al. summarize electrophysiological tonic-current effects.  Those are exactly the phenotypes that can be missed by a 3-4 week sparse CRISPR snRNA readout.  Therefore the external literature raises confidence that `Gabra4` is expressed and functional in thalamic neurons, but it does not imply a broad mRNA response.

## Target-specific decision

`Gabra4` should be nonzero, but barely so.

The nonzero call is driven by expression and direct-target logic.  Alpha4-containing receptors are enriched in thalamic relay neurons, and every close represented receptor subunit that was both expressed enough and successfully depleted in the focal group contributed its own target row to `n_degs`: `Gabra1`, `Gabrb2`, `Gabrd`, and `Gabrg2` were all significantly down as measured transcripts.  `Gabra4` is at least as plausible as `Gabra1` or `Gabrd` to be detected in a thalamic group, so I expect the on-target `Gabra4` row itself to pass FDR.

The decision not to predict several downstream genes is driven by within-dataset evidence.  `Gabrd`, the most specific represented partner for alpha4-containing extrasynaptic receptors, had only one downstream FDR<0.05 transcript (`Cttnbp2`).  `Gabra1` and `Gabrg2` were self-only despite strong focal self-knockdown.  `Gabra2`, `Gabra3`, `Gabra5`, `Gabrb1`, `Gabrb3`, `Gabrg3`, and `Gabrr2` were flat.  The largest in-family focal count was `Gabrb2 = 4`, but the corpus and the FDR rows show that those extra hits were a small beta2-biased activity/neuropeptide response, not a generic alpha4/beta2/delta or receptor-subunit replacement module.

I therefore set `Gabra4` to 1: one expected self-depletion DEG and no confidently transferred secondary DEG.

## Limits

This is an extrapolation from related subunits, not a direct signature match.  The most exact same-complex alpha4 partner, `Gabrd`, was present, but `Gabra4` itself was held out and there was no represented `Gabra6`, `Gabre`, `Gabrg1`, `Gabrq`, or `Gabrp` perturbation to fully tile extrasynaptic receptor subclasses.

The readout is nuclear RNA, not indel rate, receptor assembly, surface receptor abundance, tonic current, sleep circuitry, seizure susceptibility, or behavior.  Alpha4 loss can alter delta-subunit trafficking at the protein level without inducing delta or beta subunit mRNA compensation, so a low DEG count should not be read as a low physiological effect.

Finally, the 151 TH cell group is broader than a purified thalamic nucleus.  If alpha4 biology is concentrated in a subcluster, sparse CRISPR plus the Wilcoxon group-level test could dilute a true electrophysiological effect below FDR 0.05.
