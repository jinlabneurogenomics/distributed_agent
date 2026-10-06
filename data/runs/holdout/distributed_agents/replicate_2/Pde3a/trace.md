# Question

The requested held-out perturbation is `Pde3a`; it appears in
`170_Pde3a.csv` and is absent from both supplied training files as a
perturbation target. The prediction is the number of genes with
Benjamini-Hochberg adjusted Wilcoxon `pvals_adj < 0.05` in the focal
`151 TH Prkcd Grin2c Glut` group after sparse postnatal CRISPR loss of
`Pde3a`.

I treated the endpoint as an assay-specific count of significant
single-nucleus RNA changes, not as a generic score of PDE3A biological
importance. In particular, weak target-RNA depletion or no target self-hit in
this screen does not prove no editing; it is still informative because the
same Wilcoxon/FDR endpoint is what must be predicted.

# Sources

- Held-out manifest:
  `[local file: 170_Pde3a.csv]`.
- Training endpoint:
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
- Training DE parquet:
  `[local file: training_de_all_cell_groups.parquet]`.
- Internal Distributed Agents same-experiment corpus release
  `perturbai-july-260713-sourceguard-1773-v1`, especially the target contexts
  for `Pde10a`, `Pde4b`, `Pde4d`, and `Prkaca` and the claim
  `claim:cc64bcf75ba1dfa29fce` that represented PDE-family perturbations were
  transcriptomically non-interchangeable in basal postnatal neuronal RNA
  readouts.
- Run-local Distributed Agents focal profile comparison
  `pde3a_camp_profile_compare.json` and inspection
  `pde3a_pde_profile_inspect.json`, computed from signed `logfoldchanges`
  after filtering the parquet to `group_name == "151 TH Prkcd Grin2c Glut"`.
- PubMed literature:
  Kelly et al. 2013, rodent brain PDE expression, DOI
  `10.1016/j.cellsig.2013.10.007`, PMID `24184653`;
  Degerman et al. 1997, PDE3 structure/localization/regulation, DOI
  `10.1074/jbc.272.11.6823`, PMID `9102399`;
  Wechsler et al. 2002, cardiac PDE3A isoforms and compartmentalization, DOI
  `10.1074/jbc.M203647200`, PMID `12154085`;
  Begum et al. 2011, `Pde3a` in vascular smooth-muscle growth and oocyte
  meiotic control, DOI `10.1016/j.coph.2011.10.006`, PMID `22051884`;
  Ercu et al. 2020, `PDE3A` gain-of-function in vascular smooth muscle causing
  hypertension with brachydactyly, DOI `10.1161/CIRCULATIONAHA.119.043061`,
  PMID `32524868`.

# Computation

The manifest has one row:

| target_name |
| --- |
| `Pde3a` |

I used the focal training-count CSV to get the observed FDR<0.05 counts for
all non-held-out perturbations. The count distribution is strongly zero
inflated: 1,205/1,674 training perturbations are zero, the median is 0, the
75th percentile is 1, and the 95th percentile is 18.

I then selected biologically relevant PDE and cyclic-nucleotide training
targets and queried the parquet only in the focal cell group. The profile
comparison used `gene_target` as the profile entity, `names` as the measured
gene, `logfoldchanges` as the signed value, and `pvals_adj < 0.05` as the
significance flag.

The observed focal DEG counts for the hand-selected analogs were:

| training target | focal n_degs | reason for comparison to `Pde3a` |
| --- | ---: | --- |
| `Pde1c` | 0 | Ca2+/calmodulin-regulated cyclic-nucleotide PDE in the same broader enzyme family |
| `Pde4b` | 0 | cAMP-specific PDE with detectable but tiny PDE-family responses elsewhere |
| `Pde4d` | 0 | cAMP-specific PDE; the internal corpus reports complete downstream buffering across recovered neuronal groups |
| `Pde10a` | 0 | striatal cyclic-nucleotide PDE that can make a compact `Scg2`/`Crem` signature outside this focal TH group |
| `Adcy1` | 0 | cAMP source enzyme upstream of PKA/CREB |
| `Adcy3` | 0 | cAMP source enzyme upstream of PKA/CREB |
| `Adcy5` | 0 | cAMP source enzyme, dopamine-linked in striatal contexts |
| `Gnas` | 0 | Gs alpha, upstream of adenylyl cyclase |
| `Gnal` | 0 | Golf alpha, upstream of adenylyl cyclase in striatal neurons |
| `Rapgef4` | 0 | EPAC2, cAMP effector |
| `Prkaca` | 1 | PKA catalytic alpha; its only focal hit was own-transcript depletion |
| `Prkar1a` | 1 | PKA regulatory RI-alpha; its focal hit was own-transcript depletion |
| `Creb1` | 10 | distal CREB transcription factor; positive control for a small CRE-family response in this group |
| `Crebbp` | 8 | CREB/CBP transcriptional coactivator and nuclear counterexample |

For the PDE-family rows in the focal group, all four assayed PDE perturbations
had zero significant features in the run-local profile table. Their smallest
parquet adjusted p-values were nonsignificant:

- `Pde1c`: `Amy1` and `Atp6v0a1`, both `pvals_adj = 0.180`.
- `Pde4b`: `Anp32a`, `pvals_adj = 0.922`.
- `Pde4d`: every measured gene `pvals_adj = 1.0`.
- `Pde10a`: `Smpd4`, `pvals_adj = 0.304`.

I also explicitly checked cAMP/CREB and immediate-early readouts under these
training perturbations. In `Pde1c`, `Pde4b`, `Pde4d`, and `Pde10a`, the
candidate reporters `Crem`, `Scg2`, `Fos`, `Fosb`, `Jun`, `Egr1`, `Nr4a1`,
`Arc`, `Bdnf`, `Map2k2`, and `Snx14` all had `pvals_adj = 1.0`. That argues
that the focal PDE zeroes are not concealing a borderline CREB-like signature.
By contrast, direct `Creb1` perturbation made `Crem` the strongest focal hit
with log2FC 1.09 and adjusted p-value `3.8e-7`; the focal assay could register
a small CRE-family module when the nuclear transcriptional node itself was
perturbed.

# Target-Specific Reasoning

## `Pde3a`

`Pde3a` encodes a cGMP-inhibited cyclic-nucleotide phosphodiesterase that
hydrolyzes cAMP/cGMP in local compartments. The strongest established genetic
and physiological roles are outside this NeuN-enriched thalamic glutamatergic
readout: cardiovascular/smooth-muscle and platelet cAMP regulation, oocyte
meiotic arrest, and vascular smooth-muscle proliferation. Degerman et al.
1997 and Wechsler et al. 2002 describe PDE3/PDE3A as spatially localized
cyclic-nucleotide hydrolysis rather than as a constitutive pan-nuclear
transcriptional regulator, Begum et al. 2011 places `Pde3a` loss in vascular
smooth-muscle and oocyte cell-cycle phenotypes, and Ercu et al. 2020 shows
that disease mutations act through vascular smooth muscle. Kelly et al. 2013
mapped brain PDE isoforms and found that PDE isoforms have distinct brain
distributions; `Pde3a` and `Pde3b` were not among the PDE isoforms showing
age-related changes in the sampled hippocampus, cortex, striatum, and
cerebellum.

The within-dataset analogs push the prediction to zero. The nearest measured
PDE-family comparators `Pde1c`, `Pde4b`, `Pde4d`, and `Pde10a` all had
`n_degs = 0` in `151 TH Prkcd Grin2c Glut`, with 155-211 matched perturbed
nuclei each against 23,679 matched controls. The same focal group was also
flat for the upstream and downstream cAMP nodes `Adcy1`, `Adcy3`, `Adcy5`,
`Gnas`, `Gnal`, and `Rapgef4`. `Prkaca` and `Prkar1a` were one-gene cases
driven by self-depletion, not by `Crem`/immediate-early induction.

The internal Distributed Agents corpus was useful mainly as a boundary check across the
larger same-experiment surface. It reports that `Pde4d` was buffered across
recovered neuronal groups, that `Pde4b` produced only two robust downstream
hits outside this focal group, and that `Pde10a` produced a narrow
`Scg2`/`Crem` response in striatal/LGE GABA neurons but did not phenocopy
`Pde1c`, `Pde4b`, or `Pde4d`. That argues against simply transferring the
PDE10A striatal signature to a held-out thalamic `Pde3a` perturbation.

Given these observations, I expect sparse P16 `Pde3a` CRISPR loss in the focal
NeuN-positive TH glutamatergic group to be buffered at the basal snRNA-seq
endpoint. The best point prediction is therefore no genes passing FDR 0.05:
`predicted_n_degs = 0`.

# Limits

- There is no measured `Pde3a` perturbation signature in the supplied inputs;
  the prediction is extrapolated from other PDEs and from cAMP-pathway nodes.
- The comparator set is incomplete: `Pde1b`, `Pde2a`, `Pde3b`, `Pde4a`, and
  `Pde4c` were not focal training targets, so possible `Pde3a`-specific
  thalamic regulation by those paralog families is untested.
- The DE parquet contains perturbed-vs-control differential statistics, not
  baseline `Pde3a` expression in unperturbed `151 TH Prkcd Grin2c Glut`
  neurons.
- The result should not be read as evidence that PDE3A is biologically inert.
  It only predicts that a partial, mosaic, postnatal, unstimulated neuronal
  loss-of-function perturbation will not create a stable nuclear-RNA program
  large enough to pass this screen's Wilcoxon/BH threshold.
