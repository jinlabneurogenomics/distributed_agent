# Lmx1a prediction trace

## Question and interpretation

The requested held-out target for this run is `Lmx1a`. I interpreted the task as a point prediction for the number of genes that would pass `pvals_adj < 0.05` after acute AAV-PHP.eB CRISPR loss-of-function of `Lmx1a` in the focal `151 TH Prkcd Grin2c Glut` group. The count is the screen-specific Wilcoxon/BH endpoint, not an estimate of developmental importance, editing efficiency, cell loss, or dopamine physiology.

`Lmx1a` is absent from both the perturbation column of the training parquet and the focal training-count table, so every comparison below is a transfer from measured training perturbations plus external knowledge about the Lmx1a/Lmx1b midbrain dopaminergic network.

## Sources used

- Held-out manifest: `127_Lmx1a.csv`, confirming that the only requested target is `Lmx1a`.
- Focal endpoint table: `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`, used as the calibrated `n_degs` endpoint for measured perturbations in `151 TH Prkcd Grin2c Glut`.
- Differential-expression parquet: `training_de_all_cell_groups.parquet`, used to check adjusted p-value spectra, matched cell counts, and movement of Lmx1a-associated marker genes for biologically plausible analogs.
- Distributed Agents same-experiment corpus, release `perturbai-july-260713-sourceguard-1773-v1`. `Lmx1a` itself had no target-centered corpus entry, but target contexts for `Lmx1b`, `Pitx3`, `Otx2`, `Foxa2`, and `En1` summarized the measured lack of an acute postnatal mDA-development module among represented Lmx/Otx/En/Foxa/Pitx regulators.
- PubMed literature for external mechanism:
  - Andersson et al. 2006, DOI `10.1016/j.cell.2005.10.037`, PMID `16439212`: Lmx1a and Msx1 act as intrinsic determinants in embryonic midbrain dopamine-neuron differentiation.
  - Nakatani et al. 2009, DOI `10.1016/j.ydbio.2009.12.017`, PMID `20035737`: Lmx1a/Lmx1b cooperate with Foxa2 in mesencephalic floor-plate and dopaminergic specification.
  - Chung et al. 2009, DOI `10.1016/j.stem.2009.09.015`, PMID `19951692`: Wnt1-Lmx1a autoregulation links Wnt signaling to Otx2, Nurr1/Nr4a2, and Pitx3 during mDA differentiation.
  - Yan et al. 2011, DOI `10.1523/JNEUROSCI.1077-11.2011`, PMID `21880902`: Lmx1a and Lmx1b have cooperative, partially redundant roles in mDA progenitor proliferation, specification, and differentiation.
  - Chung et al. 2012, DOI `10.1111/j.1471-4159.2012.07779.x`, PMID `22564125`: Lmx1a can directly regulate dopamine-transporter expression during dopaminergic maturation.
  - Doucet-Beaupre et al. 2016, DOI `10.1073/pnas.1520387113`, PMID `27407143`: combined Lmx1a/Lmx1b loss in adult mDA neurons affects mitochondrial function and survival.
  - Zou et al. 2008, DOI `10.1016/j.brainresbull.2008.12.001`, PMID `19111912`: Lmx1a expression persists postnatally in selected CNS regions, including VTA/SNpc tyrosine hydroxylase-positive neurons.

## Dataset computations

I first read the focal training-count CSV and queried measured Lmx/mDA pathway genes. The direct focal `n_degs` values were:

| training target | focal `n_degs` | reason for comparison |
| --- | ---: | --- |
| `Lmx1b` | 0 | closest paralog and partial functional substitute for `Lmx1a` |
| `Foxa2` | 0 | floor-plate and SHH-linked cofactor upstream of Lmx1a/Lmx1b programs |
| `Pitx3` | 0 | downstream mDA terminal-differentiation homeobox TF |
| `Otx2` | 0 | upstream/anterior determinant that induces Lmx1a in the embryonic midbrain floor plate |
| `En1` | 0 | dopaminergic survival/developmental TF in the same literature network |
| `En2` | 0 | Engrailed paralog and negative control for generic En homeobox behavior |
| `Msx2` | 0 | represented Msx-family developmental comparator; `Msx1` was not a training target |
| `Nr4a1`, `Nr4a3` | 0, 0 | represented NR4A comparators; `Nr4a2/Nurr1` was not a training target |
| `Ctnnb1` | 383 | active upstream Wnt/beta-catenin counterexample, not a close Lmx1a analog |

I then filtered the 616,253,184-row parquet to `group_name == "151 TH Prkcd Grin2c Glut"` and the analog targets above. For each target I counted `pvals_adj < 0.05`, `pvals_adj < 0.10`, and raw `pvals < 0.05`, and inspected the leading nominal rows. Every close transcription-factor analog was FDR-flat in the focal group:

| training target | perturbed nuclei | min focal `pvals_adj` | focal FDR 0.05 genes | focal FDR 0.10 genes |
| --- | ---: | ---: | ---: | ---: |
| `Lmx1b` | 271 | 1.000 | 0 | 0 |
| `Foxa2` | 213 | 1.000 | 0 | 0 |
| `Pitx3` | 184 | 0.751 | 0 | 0 |
| `Otx2` | 162 | 0.885 | 0 | 0 |
| `En1` | 242 | 1.000 | 0 | 0 |
| `En2` | 257 | 1.000 | 0 | 0 |
| `Msx2` | 254 | 1.000 | 0 | 0 |
| `Nr4a3` | 218 | 0.166 | 0 | 0 |
| `Ctnnb1` | 171 | `3.55e-25` | 383 | 477 |

The focal rows include 17,259 measured genes per target against 23,679 matched controls, so the zeroes were not due to missing measured features. The leading nominal rows for `Lmx1b`, `Foxa2`, `En1`, `En2`, and `Msx2` all had BH-adjusted p-values equal to 1.0; `Pitx3` and `Otx2` had only shallow subthreshold minima.

I also explicitly inspected canonical Lmx/mDA marker rows (`Lmx1a`, `Lmx1b`, `Foxa1`, `Foxa2`, `Pitx3`, `Otx2`, `En1`, `En2`, `Msx1`, `Msx2`, `Nr4a1`, `Nr4a2`, `Nr4a3`, `Wnt1`, `Th`, `Slc6a3`, `Ddc`, `Aldh1a1`, `Onecut1/2`, `Neurog1/2`, `Slitrk2/5`) after `Lmx1b`, `Foxa2`, `Pitx3`, `Otx2`, `En1`, `En2`, `Msx2`, `Nr4a1`, `Nr4a3`, and `Ctnnb1` perturbation in the focal group. With the exception of the expected `Ctnnb1` self-row, none of these marker rows passed FDR correction; nearly all adjusted p-values were 1.0. Thus, the measured analog perturbations did not hide a coordinated collapse of dopamine-synthesis or Lmx1a-network transcripts in this `TH`/`Prkcd`/`Grin2c` glutamatergic population.

Finally, I used the Distributed Agents runtime profile comparison on `Lmx1b`, `Foxa2`, `Pitx3`, `Otx2`, `En1`, `En2`, `Msx2`, `Nr4a3`, and `Ctnnb1` in the same focal group, with signed `logfoldchanges`, `pvals_adj < 0.05`, and top-500 signed tails. The runtime reported `no_significant_features` for eight of the nine analogs; only `Ctnnb1` had at least 50 significant features. This is the profile-level version of the count evidence: the developmentally specific TF nodes are inactive, while a broad Wnt effector can be strongly active in the same cell group.

## Target-specific reasoning

### `Lmx1a`

External biology makes `Lmx1a` a compelling dopaminergic-development gene, but the closest in-dataset evidence points to a focal zero.

The best measured analog is `Lmx1b`: it is the Lmx1a paralog, cooperates with Lmx1a during mDA progenitor development, and can buffer Lmx1a in embryonic dosage experiments. In the focal cell group `Lmx1b` had `n_degs = 0`, 0 genes at FDR 0.10, and a minimum adjusted p-value of 1.0. The same-experiment Distributed Agents corpus also reported that acute `Lmx1b` CRISPR was pan-taxonomy flat, including no FDR 0.10 genes in 23 recovered neuronal groups. That makes `Lmx1b` strong evidence against a robust cell-autonomous Lmx-family transcriptome in the P16-to-P37/P44 sparse screen.

The next mechanistic comparators, `Foxa2`, `Pitx3`, `Otx2`, `En1`, and `En2`, are also zero in `151 TH Prkcd Grin2c Glut`. `Foxa2` is upstream/cooperative with Lmx1a/Lmx1b in floor-plate and dopaminergic specification, `Pitx3` is a late dopamine-neuron identity and maintenance factor downstream of the Lmx1a/Nr4a2 axis, `Otx2` is an upstream anterior/floor-plate determinant, and `En1/En2` are mDA developmental and survival homeobox genes. If P16 mosaic knockout of a single developmental TF in this focal thalamic/hypothalamic glutamatergic group reliably triggered a dopamine-identity or floor-plate-like RNA program, at least one of these measured nodes should have produced a nonzero signature. Instead all were 0 by the exact endpoint, all were 0 even at FDR 0.10, and the corpus claim for represented mDA developmental regulators summarized the broader lack of an acute shared mDA-identity module.

`Ctnnb1` is the important counterexample rather than the anchor. It is upstream in Wnt/beta-catenin signaling and had 383 focal DEGs, proving that the focal group and Wilcoxon design can return a large response when the perturbation controls an active pathway. But beta-catenin has broader Wnt and adhesion functions than Lmx1a, and the Ctnnb1 focal signature did not significantly move `Lmx1a`, `Pitx3`, `Th`, `Slc6a3`, `Ddc`, or the Lmx/Foxa/Otx marker set. I therefore did not transfer the `Ctnnb1` count to `Lmx1a`.

Putting those together, the expected response breadth for a held-out acute `Lmx1a` perturbation in `151 TH Prkcd Grin2c Glut` is below the FDR 0.05 detection threshold. The specific point prediction is `0` DEGs.

## Limits and extrapolation

- There is no direct `Lmx1a` perturbation signature in the supplied training data, and the Distributed Agents same-experiment corpus had no `Lmx1a` target-centered entry, so the call is an extrapolation from `Lmx1b` and nearby regulators.
- Most public `Lmx1a` mechanisms are embryonic, midbrain dopaminergic, or combined/adult `Lmx1a`/`Lmx1b` conditional loss. The benchmark perturbation is a single-gene, sparse, postnatal P16 CRISPR loss-of-function with modest average mRNA downregulation.
- `151 TH Prkcd Grin2c Glut` is not a purified SNc/VTA `MB Dopa` group. A zero here does not argue that Lmx1a is unimportant for embryonic mDA specification, adult dopamine-neuron survival, DAT expression, axonal pathology, or dopamine release.
- Zero DEG analogs can arise from redundancy, low target expression in the focal neurons, low power for a given target, or biology that changes cell abundance or protein function without a robust nuclear mRNA signature. The supplied endpoint observes only per-gene snRNA-seq differential expression among recovered NeuN-positive nuclei.
