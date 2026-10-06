# Task understanding

The held-out target in `183_Ppargc1b.csv` is `Ppargc1b`.  I interpreted the
requested endpoint as the exact focal-cell count used in the training CSV:

* cell group: `151 TH Prkcd Grin2c Glut`
* statistic: number of measured genes with `pvals_adj < 0.05`
* perturbation modality: acute mosaic AAV CRISPR-Cas9 loss of function
* required output: one non-negative integer point prediction

I did not treat germline knockout, Cre-lox knockout, knockdown, or
pharmacologic studies as numerically interchangeable with the AAV screen.  They
were useful only for deciding which training perturbations are mechanistically
close to `Ppargc1b`.

# Sources used

* Training DEG endpoint:
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`
* Training differential-expression parquet:
  `[local file: training_de_all_cell_groups.parquet]`
* Requested-target manifest:
  `[local file: 183_Ppargc1b.csv]`
* Run-local signed-profile comparison over the focal parquet rows, written to
  `ppargc1b_analog_profile_compare.json` and inspected through
  `ppargc1b_analog_profile_inspect.json`.
* Distributed Agents same-experiment corpus:
  `perturbai-july-260713-sourceguard-1773-v1`.  The corpus had no
  `Ppargc1b`-centered finding, but did contain a high-confidence
  ERR/PGC/PPAR/NRF claim over assayed neighbors of this held-out gene.
* PubMed literature:
  * Scarpulla 2008, *Physiological Reviews*, DOI
    `10.1152/physrev.00025.2007`, PMID `18391175`.
  * Scarpulla 2010, *Biochimica et Biophysica Acta*, DOI
    `10.1016/j.bbamcr.2010.09.019`, PMID `20933024`.
  * Sonoda et al. 2007, *Genes & Development*, DOI
    `10.1101/gad.1553007`, PMID `17671090`.
  * Camacho et al. 2012, *Experimental Neurology*, DOI
    `10.1016/j.expneurol.2012.06.031`, PMID `22771762`.

# Computational checks

I read the requested-target CSV and found exactly one row, `Ppargc1b`.  I then
filtered `training_de_all_cell_groups.parquet` to
`group_name == "151 TH Prkcd Grin2c Glut"` and recomputed

```
sum(pvals_adj < 0.05) by gene_target
```

over all focal rows.  The filtered focal matrix contained 28,891,566 rows, 1,674
training perturbations, and a median of 17,259 measured genes per perturbation.
The recomputed DEG counts matched all 1,674 rows of the focal training-count CSV.
The endpoint was sparse: 1,205 of 1,674 training perturbations had `n_degs = 0`,
the 75th percentile was 1 DEG, the 90th percentile was 2 DEGs, and the 95th
percentile was 18 DEGs.

For `Ppargc1b`, the assayed analogs that mattered most were:

| training perturbation | focal `n_degs` | `n_pert_matched` | why it was considered |
| --- | ---: | ---: | --- |
| `Ppargc1a` | 0 | 135 | closest PGC-1 coactivator paralog in the training set |
| `Ppara` | 0 | 158 | PPAR nuclear receptor partner class |
| `Ppard` | 0 | 315 | PPAR nuclear receptor partner class |
| `Pparg` | 0 | 109 | PPAR nuclear receptor partner class |
| `Esrra` | 57 | 275 | ERR-alpha is a PGC-1 coactivated mitochondrial/OXPHOS TF |
| `Esrrb` | 0 | 209 | ERR paralog; counterexample to broad ERR-family transfer |
| `Esrrg` | 0 | 183 | ERR paralog; counterexample to broad ERR-family transfer |
| `Nrf1` | 138 | 222 | NRF mitochondrial transcription factor downstream of the PGC-1 network |
| `Nfe2l1` | 0 | 157 | stress/respiratory regulator with NRF-family name but different biology |
| `Nfe2l2` | 0 | 207 | NRF2 oxidative-stress regulator; mostly flat in basal recovered neurons |
| `Creb1` | 10 | 126 | upstream activity-dependent regulator connected to PGC-1alpha induction |
| `Mef2a` | 4 | 138 | upstream activity/metabolic transcription factor; weak focal response |
| `Mef2c` | 1 | 223 | same MEF2 family, also weak in the focal group |

The nearest biological neighbor, `Ppargc1a`, had no significant genes at
FDR 0.05 in the requested cell group; its smallest adjusted p-value among focal
rows was `Bcan`, `pvals_adj = 0.189`.  `Ppara`, `Ppard`, and `Pparg` were also
0-DEG despite ordinary matched perturbed-cell counts for this screen.

The positive mitochondrial-axis examples were real but imperfect analogs:
`Esrra` loss produced 57 FDR<0.05 genes including down-regulated
`Gas6` (`logFC = -0.556`, `FDR = 1.56e-9`), `Bcan`
(`logFC = -0.937`, `FDR = 2.38e-6`), `Mdh1`
(`logFC = -0.250`, `FDR = 1.53e-4`), `Mpc1`
(`logFC = -0.252`, `FDR = 0.00763`), `Dlat`
(`logFC = -0.345`, `FDR = 0.0187`), and `Ndufs2`
(`logFC = -0.281`, `FDR = 0.0396`).  `Nrf1` loss produced 138 FDR<0.05 genes,
with top genes including `Snhg11` (`logFC = -0.355`, `FDR = 3.78e-20`),
`Rsrp1` (`logFC = -0.748`, `FDR = 5.42e-17`), `Nrsn2`
(`logFC = -0.821`, `FDR = 9.38e-13`), and the OXPHOS gene `Sdha`
(`logFC = -0.572`, `FDR = 9.16e-8`).  However, `Esrra` and `Nrf1`
shared only four significant genes at FDR 0.05 in this focal group, and only two
of those four (`Cntnap1`, `Tecr`) had the same sign.  Neither positive signature
overlapped significantly with the flat `Ppargc1a` profile.

This pattern agrees with Distributed Agents corpus claim
`claim:4a99ad45816a763032e0`: in juvenile neuronal nuclei, single-gene
perturbations of the represented ERR/PGC/PPAR/NRF mitochondrial network were
node-specific.  In particular, the corpus recorded the same-experiment contrast
that `Esrra` had a detectable partial oxidative-metabolism program in
`151 TH Prkcd Grin2c Glut`, whereas `Ppargc1a`, ESRR paralogs, PPAR neighbors,
and `Nrf1`-related perturbations were flat or divergent rather than
interchangeable.

# Target-specific prediction

## Ppargc1b

`Ppargc1b` encodes PGC-1beta, a non-DNA-binding transcriptional coactivator in
the PGC-1 family.  Public literature places PGC-1alpha, PGC-1beta, and PRC
upstream of transcription factors such as NRF1/NRF2 and ERR-alpha that regulate
nuclear respiratory-chain genes and the mitochondrial transcription/replication
apparatus (Scarpulla 2008; Scarpulla 2010).  PGC-1beta can be a functional
coactivator of ERR-alpha in a stimulated mammalian context: Sonoda et al. 2007
found that an interferon-gamma host-defense program in macrophages required an
ERR-alpha/PGC-1beta arm to induce mitochondrial respiratory-chain genes and
mitochondrial ROS.  PGC-1beta is also not irrelevant to brain physiology:
Camacho et al. 2012 reported that germline PGC-1beta knockout mice had altered
brain mitochondrial function and abnormal mTOR/ER-stress behavior in
hypothalamus and cortex under nutritional or pharmacologic stress.

Those external facts argue that `Ppargc1b` belongs in the same broad
mitochondrial coactivator network as `Ppargc1a`, `Esrra`, and `Nrf1`, but they
do not argue for a large acute AAV-CRISPR response in this particular neuronal
snRNA-seq endpoint.  The most direct measured paralog, `Ppargc1a`, had
`n_degs = 0` in `151 TH Prkcd Grin2c Glut` with 135 matched perturbed nuclei and
had zero FDR<0.10 downstream genes across the cell groups summarized by the
Distributed Agents Ppargc1a finding.  The assayed PPAR receptors that would receive PGC
coactivation were also 0 in the focal group.  `Esrra` and `Nrf1` showed that the
dataset can detect some mitochondrial transcription-factor perturbations, but
those genes bind DNA directly and produced distinct rather than shared
expression states; using their 57- and 138-DEG counts for a non-DNA-binding
PGC-1beta partial loss would overstate the within-dataset evidence.

I therefore predict that partial acute `Ppargc1b` loss will be buffered in the
basal recovered `151 TH Prkcd Grin2c Glut` nuclei, like the closest measured
PGC/PPAR-side perturbations, and will not put any measured gene below the
0.05 BH threshold.

Predicted `n_degs`: 0.

# Limits

This is an extrapolation because `Ppargc1b` itself was completely held out and
the Distributed Agents corpus release had no `Ppargc1b`-centered same-experiment finding.
The prediction is driven primarily by within-dataset behavior of measured
PGC/PPAR/ERR/NRF neighbors, especially the `Ppargc1a` zero, not by a measured
`Ppargc1b` expression signature.

The external literature for PGC-1beta comes from reviews, macrophages, germline
mouse brain phenotyping, and stress paradigms.  None of those exactly matches
sparse, juvenile, postmitotic, acute CRISPR with only partial average target
mRNA down-regulation.  Finally, zero in this screen is a statistical prediction:
it means no measured transcript is expected to pass FDR 0.05, not that
Ppargc1b has no mitochondrial role in neurons.
