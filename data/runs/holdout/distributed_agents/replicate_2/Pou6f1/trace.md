# Held-out question

The manifest for this run contains one held-out perturbation, `Pou6f1`. I
interpreted the requested endpoint as the integer count of focal
`151 TH Prkcd Grin2c Glut` rows with `pvals_adj < 0.05` that would have been
observed if `Pou6f1` had been included in the Perturb-seq training parquet.
`n_degs` is therefore an assay-specific response-breadth count, not a general
score of gene essentiality or developmental importance.

The main ambiguity was whether broad POU-domain family membership should make a
class-VI prediction nonzero. I resolved that by giving highest weight to
perturbations whose own acute P16 neuronal signatures were measured in the same
assay. In those data, class membership alone was not predictive of a shared
signature.

# Sources used

- `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`
  for the observed focal-cell `n_degs` of non-held-out perturbations.
- `[local file: training_de_all_cell_groups.parquet]`
  for focal-cell adjusted p-value surfaces, log fold changes, and matched-cell
  counts for selected analogs.
- Distributed Agents same-experiment corpus release
  `perturbai-july-260713-sourceguard-1773-v1`. The exact held-out target
  `Pou6f1` was not present as a target node, so I used target contexts and
  claims for measured POU perturbations, especially `Pou6f2`, `Pou3f3`,
  `Pou3f4`, `Pou2f1`, `Pou5f1`, and `Pou1f1`.
- PubMed via NCBI E-utilities for external biology. Most relevant were Andersen
  et al. 1993, PMID 7901208, defining Brn-5/POU6F1 as a divergent class-VI POU
  factor expressed in developing brain and adult layer-IV neocortex; Cui and
  Bulleit 1998, DOI 10.1002/(SICI)1097-4547(19980615)52:6<625::AID-JNR1>3.0.CO;2-A,
  showing Brn-5 expression in early terminally differentiating CNS neurons;
  Rhee et al. 1998, DOI 10.1074/jbc.273.51.34196, characterizing class-VI
  POU-domain DNA-binding behavior; Wu et al. 2001, DOI 10.1006/mcne.2000.0957,
  placing Brn-5 in myelinating Schwann cells; McClard et al. 2018,
  DOI 10.1523/JNEUROSCI.1641-17.2017, showing a CRHR1-dependent POU6F1 role in
  dendritic and synaptic development of adult-born olfactory-bulb neurons; and
  Toda et al. 2007, DOI 10.1016/j.mce.2007.09.002, showing mPOU/Brn-5 regulation
  of pituitary `Prl`/`Pou1f1`.

# Dataset checks

The focal training-count table contained 1,674 perturbations. The endpoint was
sparse: median `n_degs = 0`, 75th percentile `= 1`, 95th percentile `= 18`,
and only 469/1,674 training perturbations were nonzero in this cell group.

For the biologically selected comparator set, I filtered the parquet to
`group_name == "151 TH Prkcd Grin2c Glut"` and extracted rows for POU-family
genes and a few transcription-factor controls. I then recomputed, per
perturbation, `sum(pvals_adj < 0.05)` and the minimum adjusted p value. The
recomputed counts matched the focal count CSV.

Key focal-cell comparators:

| training perturbation | observed `n_degs` | minimum focal `pvals_adj` | matched perturbed nuclei | relevance |
|---|---:|---:|---:|---|
| `Pou6f2` | 0 | 1.000 | 182 | closest assayed class-VI POU-family member |
| `Pou1f1` | 0 | 1.000 | 208 | measured POU factor; pituitary POU network displaced from NeuN+ brain |
| `Pou2f1` | 0 | 0.369 | 173 | broadly expressed octamer POU factor, but flat in basal neurons |
| `Pou2f2` | 0 | 1.000 | 166 | class-II POU paralog/control |
| `Pou3f3` | 0 | 0.849 | 419 | neural POU-III factor; sparse pan-atlas phenotype in the corpus |
| `Pou3f4` | 0 | 0.759 | 220 | neural/otic POU-III factor; sparse pan-atlas phenotype in the corpus |
| `Pou4f3` | 0 | 1.000 | 241 | POU-IV factor; hair-cell lineage program absent in this neuronal assay |
| `Pou5f1` | 0 | 1.000 | 143 | POU factor/pluripotency control |
| `Isl1` | 0 | 0.143 | 208 | LIM-homeodomain developmental comparator |
| `Lhx3` | 0 | 0.686 | 355 | pituitary/motor-neuron LIM-homeodomain comparator |
| `Lhx4` | 0 | 1.000 | 191 | pituitary LIM-homeodomain comparator |

Positive transcription-factor counterexamples existed in the same focal cell
type: `Ctcf` had 270 DEGs, `Rora` had 278, `Tcf7l2` had 106, `Bmal1` had 103,
`Nr1d1` had 116, and `Klf9` had 19. Thus I did not interpret the POU-family
zeros as a blanket failure to detect transcription-factor perturbations in
`151 TH Prkcd Grin2c Glut`.

# Same-experiment corpus evidence

The Distributed Agents corpus had no `Pou6f1` target context, no `Pou6f1` claims, and no
explicit same-experiment references centered on the held-out target. It did,
however, contain directly relevant POU-neighborhood results:

- The `Pou6f2` context reported that `Pou6f2` produced no FDR<0.10 genes in any
  of 23 measured neuronal cell groups after P16 mosaic CRISPR, had no meaningful
  full-surface positive or negative target neighbor, and showed no shared
  acute POU-family signature with `Pou1f1`, `Pou2f1`, `Pou2f2`, `Pou3f3`,
  `Pou3f4`, `Pou4f3`, or `Pou5f1`.
- The corpus claim `claim:cdbc022fa93623830ad5` summarized POU-family-centered
  comparisons across `Pou1f1`, `Pou3f3`, `Pou3f4`, and `Pou6f2`: shared
  POU-homeodomain family membership was insufficient to generate an
  interchangeable acute neuronal CRISPR phenotype in the P16 assay.
- The `Pou3f3` and `Pou3f4` target contexts described only sparse,
  non-overlapping singleton effects across the broader atlas and no POU-III
  phenocopy. That makes neural POU annotations weak evidence for a positive
  focal thalamic count.
- The `Pou1f1`, `Pou2f1`, and `Pou5f1` contexts likewise treated their POU
  relatives as flat or nonconvergent in the postnatal NeuN-enriched assay,
  arguing against borrowing any large response from another POU class.

# Pou6f1 reasoning and prediction

`Pou6f1`/Brn-5 is a POU transcription factor, and the literature makes clear
that it is not biologically inert: it is expressed in developing and mature CNS
neurons, appears during terminal CNS neuronal differentiation, can regulate
pituitary `Prl`/`Pou1f1`, is controlled by neuregulin in myelinating Schwann
cells, and can mediate CRHR1-dependent dendritic/synaptic maturation of
adult-born olfactory-bulb neurons.

Those functions nevertheless map poorly onto the endpoint here. The experiment
edits already specified P16 NeuN+ brain neurons and scores them at P37-P44; the
focal group is a thalamic glutamatergic class; olfactory bulb was excluded; and
Schwann cells, pituitary lineages, embryonic neural progenitors, and injury
contexts were not sampled. In the same assay, the nearest measured class-VI POU
factor, `Pou6f2`, was completely flat in the focal group and flat across the
atlas in the corpus. All seven other POU perturbations measured in the focal
group also had `n_degs = 0`, and their adjusted-p-value surfaces were far from
the 0.05 threshold. Nearby developmental homeodomain comparators such as
`Isl1`, `Lhx3`, and `Lhx4` were also flat.

The key transfer is therefore negative and within-dataset driven: acute loss of
represented POU/homeodomain developmental transcription factors, including the
closest assayed `Pou6f2`, did not produce a broad postnatal focal thalamic RNA
response. External knowledge mainly determines which of those zeros are
mechanistically appropriate; it also warns that known `Pou6f1` roles are in
developmental, olfactory-bulb, peripheral-glial, pituitary, or injury settings
rather than in basal juvenile thalamic glutamatergic maintenance. I predict
that the held-out `Pou6f1` surface lands in the same null regime:
`predicted_n_degs = 0`.

# Limits

The prediction extrapolates across POU class VI because the exact held-out
`Pou6f1` perturbation was absent from the training parquet and from the
Distributed Agents corpus. `Pou6f2` is the closest assayed family member, but the corpus
itself emphasizes that POU factors are not interchangeable in this assay, so a
flat `Pou6f2` is a strong negative analog rather than a literal phenocopy.
This Perturb-seq screen also measured RNA at one postnatal time point with
mosaic AAV-CRISPR editing and did not measure indels or protein; it could miss
early developmental requirements, olfactory-bulb adult-born-neuron phenotypes,
non-neuronal Schwann-cell roles, or stress/injury-responsive targets. Finally,
a zero prediction means no gene is expected to cross BH FDR 0.05 in this
specific focal Wilcoxon test, not that `Pou6f1` lacks all neuronal function.
