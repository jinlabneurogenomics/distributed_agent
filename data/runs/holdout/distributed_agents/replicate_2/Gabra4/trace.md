# Gabra4 DEG-count prediction

## Question and resolved ambiguities

The held-out manifest contains one requested perturbation, `Gabra4`. I interpreted the requested endpoint as the exact screen endpoint in `151 TH Prkcd Grin2c Glut`: the count of measured genes whose Wilcoxon `pvals_adj` is below 0.05, with the perturbed target transcript itself included when it is significant. That inclusion is visible in the training counts: for example `Gabra1` has `n_degs = 1` and its only FDR < 0.05 row in the focal cell group is `names = Gabra1`.

The held-out `Gabra4` perturbation has no row in either the parquet or the count CSV, so I treated all `Gabra4` knockout outcomes as unknown and transferred from non-held-out receptor and ion-channel perturbations. `Gabra4` as a measured transcript was still available in other training signatures, and I used that only to confirm that the gene is detectable and thalamically regulated, not as a direct knockout signature.

## Sources

Internal experimental data:

- `[local file: training_de_all_cell_groups.parquet]`
- `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`
- `[local file: 085_Gabra4.csv]`

Internal knowledge layer:

- Distributed Agents PerturbAI atlas semantic corpus, release `perturbai-july-260713-sourceguard-1773-v1`
- Distributed Agents run-local `profile_neighbors`, applied to `Gabrd`, `Gabrb2`, `Gabra1`, and `Gabrg2` score profiles in `151 TH Prkcd Grin2c Glut`

External mechanism sources:

- NC-IUPHAR Guide to Pharmacology / GtoPdb v2021.3 classifies mammalian `GABA_A` receptors as pentameric ligand-gated anion channels and lists alpha4/beta2/delta and alpha4/beta3/delta among conclusively identified native extrasynaptic receptor subtypes; Belelli et al. 2021, DOI `10.2218/gtopdb/F72/2021.3`, PMID `35005623`.
- Mouse thalamic ventrobasal neurons express extrasynaptic alpha4/beta2/delta `GABA_A` receptors that mediate tonic inhibition; Jia et al. 2005, DOI `10.1152/jn.00421.2005`, PMID `16162835`.
- Alpha4-containing extrasynaptic receptors dynamically couple reticular-thalamic presynaptic firing to tonic/postsynaptic inhibition in somatosensory thalamus; Herd et al. 2013, DOI `10.1523/JNEUROSCI.1174-13.2013`, PMID `24027285`.
- Germline alpha4 loss in mouse thalamus markedly alters delta subunit localization and reduces neuropil delta labeling, supporting a close alpha4-delta partnership but also showing that much of the adaptation is receptor trafficking rather than necessarily a broad mRNA program; Peng et al. 2013, DOI `10.1007/s11064-013-1202-1`, PMID `24352815`.

## Computational steps

I first read the held-out manifest and found a single target, `Gabra4`. I then used the training count CSV to calibrate the endpoint distribution in the focal group: 1,205 of 1,674 training perturbations, or 72.0%, had zero DEGs; the median was 0, the 90th percentile was 2, and the 95th percentile was 18. This is a sparse endpoint with a long upper tail, so I focused on local biological analogs rather than using the mean count.

I queried the parquet with DuckDB for rows in:

```sql
WHERE group_name = '151 TH Prkcd Grin2c Glut'
  AND gene_target IN (...)
```

and, for each relevant target, counted `pvals_adj < 0.05` rows and inspected the top FDR-ranked genes. The relevant observed training perturbations were:

| target | focal `n_degs` | FDR < 0.05 genes in `151 TH Prkcd Grin2c Glut` | interpretation for `Gabra4` |
| --- | ---: | --- | --- |
| `Gabrd` | 2 | `Gabrd`, `Cttnbp2` | Closest assayed complex partner for alpha4/beta/delta extrasynaptic receptors. Its response was only target transcript plus one small downstream postsynaptic-scaffold readout, so delta-like tonic-inhibition loss did not make a broad state. |
| `Gabrb2` | 4 | `Gabrb2`, `Nr4a1`, `Vgf`, `Nalf1` | Upper-bound receptor-subunit counterexample. It induced a small activity/neuropeptide program, but it is a beta subunit used by many `GABA_A` assemblies, and the internal corpus reports that the `Gabrb2` state was not reproduced by `Gabrd`, alpha subunits, `Gabrr2`, or `Slc12a2`. |
| `Gabra1` | 1 | `Gabra1` | Alpha-subunit counterexample with strong self-transcript loss but no downstream FDR < 0.05 genes in this cell group. |
| `Gabrg2` | 1 | `Gabrg2` | Gamma2 subunit with self-only focal response; internal reports found sparse `Bdnf`/`Vgf` leakage in other glutamatergic groups but no focal activity program. |
| `Gabra2`, `Gabra3`, `Gabra5` | 0 each | none | Alpha paralog counterexamples; these are less direct than alpha4 for thalamic tonic receptors, and they show that alpha-family membership alone does not imply a response. |
| `Gabrb1`, `Gabrb3`, `Gabrg3`, `Gabrr2` | 0 each | none | Same receptor superfamily members that bounded the GABA receptor neighborhood at zero. |
| `Gad2`, `Slc32a1`, `Slc6a1`, `Gphn` | 0 each | none | GABA synthesis, vesicle loading, reuptake, and inhibitory postsynaptic scaffolding were transcriptionally silent in the focal endpoint, arguing against a generic GABAergic-loss signature. |
| `Cacna1g` | 12 | `Ptprn`, `Cacna1g`, `Stmn4`, `Cpne7`, `Ly6e`, `Jun`, `Zdhhc22`, `Iyd`, `Lrrc7`, `Serpine2`, `Notum`, `Irag1` | A thalamic excitability control with a larger but still modest footprint. `Gabra4` is not expected to exceed this because the closest GABA_A subunits were much smaller. |
| `Hcn2` | 1 | `Hcn2` | A second thalamic conductance counterexample showing that an electrophysiologically important channel can be self-only in this assay. |

I separately queried rows with `names = Gabra4` across all focal training perturbations. `Gabra4` was significantly decreased by several high-footprint regulatory perturbations, including `Ctnnb1`, `Rnpc3`, `Rab7`, `U2af2`, `Wac`, `Hnrnpu`, `Rora`, and `Psmb4`, which confirms that `Gabra4` mRNA is detectable in this cell group. Because those targets are global RNA-processing, Wnt/catenin, proteostasis, or transcriptional regulators with 278 to 868 focal DEGs, I used them only for detectability and not as `Gabra4` knockout analogs.

The run-local `profile_neighbors` analysis did not uncover a strong hidden receptor module. In the focal cell group, whole-score correlations among the best `Gabrd` neighbors were small: `Gabrb2` was the top Pearson neighbor at `r = 0.138`, while `Gabra1` ranked sixth at `r = 0.128`. The best `Gabrb2` whole-profile neighbor was `Gabra1` at `r = 0.155`; these are weak values driven by sparse self-target and tail overlaps, not by a shared high-confidence downstream program.

## Target-specific prediction

### `Gabra4`

`Gabra4` encodes the alpha4 `GABA_A` receptor subunit. External physiology makes it more specific than the generic alpha-subunit paralogs: thalamic relay neurons express extrasynaptic alpha4/beta2/delta receptors that mediate tonic inhibition, and alpha4 loss disrupts tonic alpha4/delta receptor function and delta-subunit surface localization. That makes `Gabrd` the closest observed training analog, with `Gabrb2` a plausible but broader upper bound.

The dataset-local evidence points to a very small nonzero count. `Gabrd`, the most direct delta partner, had exactly two focal DEGs: its own transcript and `Cttnbp2`. `Gabrb2` had four, including `Nr4a1` and `Vgf`, but the Distributed Agents corpus explicitly reports this as a beta2-selective thalamic activity response not reproduced by `Gabrd`, `Gabra3`, `Gabra2`, `Gabrr2`, or `Slc12a2`. `Gabra1` and `Gabrg2` each had only their self transcript in the focal group, and the remaining assayed `Gabr*` genes were zero. The internal corpus also reports that represented GABA receptor and inhibitory-synapse neighbors do not form a shared juvenile postmitotic nuclear-RNA module, and that single postnatal GABA_A subunit perturbations do not induce robust compensatory mRNA replacement of other subunits.

I therefore expect edited `Gabra4` nuclei to be detectable through the `Gabra4` transcript itself but not to pass the threshold for a multi-gene immediate-early or receptor-compensation program. I predict one FDR < 0.05 gene.

## Limits

This is an extrapolation because `Gabra4` and `Gabra6`, the alpha subunits most directly paired with `Gabrd`, were both held out or absent from the training perturbation universe visible here. Germline alpha4 knockout studies in thalamus are informative for receptor assembly and tonic inhibition, but they include developmental and circuit adaptation that the P16 mosaic CRISPR experiment intentionally avoids. The snRNA-seq endpoint also does not measure tonic current, phasic inhibition, delta trafficking, or receptor surface abundance, so a true alpha4 electrophysiological phenotype could be present with zero or one DEG. Finally, whether the self transcript crosses BH FDR 0.05 depends on guide efficacy and recovered-cell power; I treated `Gabra1`, `Gabrb2`, `Gabrd`, and `Gabrg2` self-significance as enough support for a small nonzero point estimate, but the difference between 0, 1, and 2 DEGs is the most uncertain part of this call.
