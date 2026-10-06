# Plxnc1 DEG-count prediction

## Question and resolved ambiguities

The requested held-out perturbation set contains one target, `Plxnc1`, and the
task asks for a point prediction of `n_degs` in `151 TH Prkcd Grin2c Glut`.
I treated `n_degs` exactly as defined by the supplied endpoint table: the
number of measured genes in the focal cell group with `pvals_adj < 0.05` after
Benjamini-Hochberg correction of Scanpy Wilcoxon tests. That count includes the
target transcript itself when it passes FDR, as seen for focal `Plxna2`,
`Sema5a`, and `Robo1`.

The requested endpoint is directly observed for the non-held-out perturbations
in `151 TH Prkcd Grin2c Glut` by
`151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`; it is absent for `Plxnc1`.
The full Parquet is a direct differential-expression surface for the same
non-held-out perturbations and was used to inspect focal expression patterns for
biological analogs. The same-experiment July 260713 sourceguard corpus supplied
packaged interpretation for visible analog genes; it is another representation
of the same Perturb-seq experiment, not independent replication.

The held-out gene was a scalar-count prediction target, not ranked supervision,
so the rank-calibration and predictive graph-review operations were not
available or applicable.

## Sources

- Declared focal training counts:
  `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
- Declared DE Parquet:
  `training differential-expression dataset`.
- Requested-target manifest:
  `single-target request for Plxnc1`.
- Same-experiment internal corpus:
  `perturbai-july-260713-sourceguard-1773-v1`, especially the Nrp1, Nrp2,
  Plxna1, Plxna2, Plxna4, Plxnd1, Sema4d, Sema5a, and Sema6a Finding reports.
- External literature from PubMed:
  Alto and Terman 2017, DOI 10.1007/978-1-4939-6448-2_1 / PMID 27787839;
  Scott et al. 2008, DOI 10.1038/jid.2008.329 / PMID 18987670;
  Chabrat et al. 2017, DOI 10.1038/s41467-017-01042-0 / PMID 29038581;
  Inoue et al. 2021, DOI 10.7554/eLife.65078 / PMID 33780330;
  Konig et al. 2014, DOI 10.1002/eji.201343968 / PMID 24890788.

## Dataset calculations

I first read the training count CSV to calibrate the response-breadth scale for
the focal cell group. It contains 1,674 visible perturbations. The distribution
is zero-heavy: 1,205 perturbations have `n_degs = 0`, the median is 0, the
75th percentile is 1, the 90th percentile is 2, and the 95th percentile is 18.

I then selected mechanistically nearby perturbations from the training endpoint
table and queried their focal rows from the Parquet. The selected targets were
Plexin/semaphorin pathway genes and immediate comparators that were present in
the focal training universe. Their observed focal counts were:

| training perturbation | focal `n_degs` |
| --- | ---: |
| `Plxna1` | 0 |
| `Plxna2` | 1 |
| `Plxna4` | 0 |
| `Plxnd1` | 0 |
| `Nrp1` | 0 |
| `Nrp2` | 0 |
| `Sema4d` | 0 |
| `Sema5a` | 1 |
| `Sema6a` | 0 |
| `Itgb1` | 0 |
| `Kdr` | 0 |
| `Flt4` | 0 |
| `Fyn` | 0 |
| `Rac1` | 0 |
| `Dpysl5` | 0 |
| `Gria1` | 0 |
| `Gria2` | 0 |
| `Gria3` | 0 |
| `Robo1` | 1 |
| `Robo2` | 0 |
| `Robo4` | 0 |

For the principal semaphorin/plexin analogs I verified that the focal counts
came from null or self-only signatures rather than broad downstream phenotypes:

| perturbation | focal perturbed/control nuclei | focal FDR<0.05 pattern |
| --- | --- | --- |
| `Plxna1` | 229 / 23,679 | 0 genes; minimum adjusted p-value 1 |
| `Plxna2` | 246 / 23,679 | 1 gene, the self transcript `Plxna2`, logFC -0.596, FDR 0.024 |
| `Plxna4` | 184 / 23,679 | 0 genes; minimum adjusted p-value 1 |
| `Plxnd1` | 279 / 23,679 | 0 genes; minimum adjusted p-value 1 |
| `Nrp1` | 182 / 23,679 | 0 genes; minimum adjusted p-value 1 |
| `Nrp2` | 115 / 23,679 | 0 genes at FDR<0.05; the nearest call was `Lrp1` up, logFC 0.367, FDR 0.069 |
| `Sema4d` | 165 / 23,679 | 0 genes at FDR<0.05; nearest adjusted p-value 0.189 |
| `Sema5a` | 258 / 23,679 | 1 gene, the self transcript `Sema5a`, logFC -0.915, FDR 3.94e-9 |
| `Sema6a` | 219 / 23,679 | 0 genes; minimum adjusted p-value 1 |

The July corpus gave the same local message across the full neuronal surface:
these receptor and ligand perturbations occasionally produced a singleton in
another neuronal class, such as Plxna1-Kif21a in CA3/CA2/DG glutamatergic
neurons, Plxna4-Zfp384 in MEA/LA/CA1/DG glutamatergic neurons,
Sema4d-Ablim1 in Pvalb GABA neurons, Sema5a-Ndufa11 in CNU-MGE GABA neurons,
or Sema6a-Camk2n1 in MB/P/MY GABA neurons, but those singletons did not align
with one another or with the `151 TH Prkcd Grin2c Glut` state. Whole-surface
score-vector comparisons reported in the corpus were near zero for represented
semaphorin relatives, rejecting a hidden shared mRNA program behind the focal
zeros.

## Plxnc1 rationale

`Plxnc1` encodes Plexin-C1, a receptor for Semaphorin-7A. Semaphorins signal
mainly through plexin receptor complexes to small-GTPase, actin, microtubule,
and adhesion machinery rather than through an obligatory nuclear
transcriptional cascade (Alto and Terman 2017). Plexin-C1 has clear
Sema7A-coupled biology outside the exact focal-cell readout: Scott et al. 2008
placed cofilin and LIMK downstream of Sema7A/Plexin-C1 in melanocytes; Chabrat
et al. 2017 showed that Otx2 and Lmx1a/b control Plxnc1 and that
Sema7a/Plxnc1 interactions help segregate developing mesodiencephalic
dopaminergic axons; Inoue et al. 2021 showed that neonatal olfactory
Sema7A/PlxnC1 signaling drives mitral/tufted-cell dendrite selection; and
Konig et al. 2014 implicated hematopoietic Plexin-C1 in leukocyte recruitment
during acute inflammation. Those priors support a real receptor function but
mostly at developmental wiring, local cytoskeletal, olfactory-bulb, immune, or
non-neuronal stages that are displaced from sparse P16 CRISPR perturbation and
snRNA-seq of recovered thalamic glutamatergic nuclei.

I therefore used visible same-experiment semaphorin receptors and ligands as
the primary quantitative analogs for the requested endpoint. In the causal
chain, perturbing a plexin changes a receptor for extracellular guidance cues;
the direct molecular consequence is loss of ligand-gated plexin signaling; the
expected propagation is local Ras/Rap/Rho/cofilin, adhesion, and cytoskeletal
remodeling; those processes may affect axon or dendrite geometry before or
outside the P16 to P37-44 window; the endpoint samples nuclear RNA in recovered
NeuN-positive focal thalamic nuclei. For `Plxnc1`, that chain predicts no
strong same-direction transfer from the dramatic high-DEG training perturbations
such as proteostasis, splicing, or core chromatin genes, because those
perturbations damage cell-intrinsic housekeeping systems. The appropriate
analogs are `Plxna1`, `Plxna2`, `Plxna4`, `Plxnd1`, `Nrp1`, `Nrp2`, `Sema4d`,
`Sema5a`, and `Sema6a`, all of which were flat or self-only in the focal cell
group.

The strongest counterexample to a strict zero is `Nrp2`: it is another
semaphorin co-receptor and had an `Lrp1` up-regulation just above the requested
threshold in `151 TH Prkcd Grin2c Glut`. I did not transfer that to a positive
`Plxnc1` count because the event was a single FDR 0.069 marker after `Nrp2`
loss, not an FDR<0.05 event in the training endpoint, and Plxnc1 is not an
obligate subunit of the Nrp2/Sema3F holoreceptor. `Plxna2` and `Sema5a` are
also apparent one-count positives, but each focal count was only the targeted
transcript itself; the July report for `Sema5a` explicitly notes that a clean
`Sema5a` self-transcript decrease occurred in this focal group without any
downstream FDR<0.10 response. Those cases argue against predicting a broad
downstream count for another semaphorin-family target merely because it may be
edited.

The point prediction is therefore `0`: no measured gene, including `Plxnc1`
itself, is expected to survive FDR<0.05 in `151 TH Prkcd Grin2c Glut` after
acute sparse postnatal `Plxnc1` loss.

## Limits and uncertainty

This is an extrapolation because both `Plxnc1` and the exact `Sema7a` ligand
axis were held out or absent from the visible focal perturbation table. A narrow
thalamic subtype could respond even if the broad `151` class and all represented
semaphorin relatives look flat, and snRNA-seq would miss axonal geometry,
dendrite selection, cofilin phosphorylation, receptor trafficking, and immune
or glial phenotypes unless they secondarily change nuclear RNA in recovered
neurons. The focal analog counts were, however, internally consistent: several
closer pathway members had 110 to 279 perturbed focal nuclei and still produced
0 downstream genes at FDR<0.05, making a zero count more likely than a rare
singleton or multi-gene response for `Plxnc1`.
