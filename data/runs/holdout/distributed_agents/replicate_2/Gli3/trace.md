# Predicting the held-out `Gli3` DEG count

## Question and resolution of ambiguities

The requested held-out perturbation list for this run contains one target:
`Gli3`. I interpreted the task as asking for the number of measured genes with
`pvals_adj < 0.05` after `Gli3` CRISPR loss of function in
`151 TH Prkcd Grin2c Glut` neurons. The count is the same endpoint supplied in
`151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`; it includes any significant
measured row, including the target transcript itself if it were to pass FDR.

I treated `Gli3` as completely held out. Its own count and expression profile
were not used from the parquet or count CSV. The prediction is therefore a
transfer from measured Hedgehog/GLI/ciliary perturbations and from external
knowledge of GLI3 biology.

## Sources used

- Input training endpoint:
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`
- Input DE parquet:
  `[local file: training_de_all_cell_groups.parquet]`
- Held-out manifest:
  `[local file: 091_Gli3.csv]`
- Same-experiment semantic layer:
  Distributed Agents corpus release `perturbai-july-260713-sourceguard-1773-v1`
- Run-local Distributed Agents observed-profile tools for symmetric focal-cell
  comparison of GLI/Hedgehog/ciliary perturbations
- External mechanism references from Reactome and PubMed:
  - Reactome `R-HSA-5635851`, "GLI proteins bind promoters of Hh responsive genes to promote transcription"
  - Persson et al. 2002, DOI `10.1101/gad.243402`, PMID `12435629`
  - Bai, Stephen and Joyner 2004, DOI `10.1016/S1534-5807(03)00394-0`, PMID `14723851`
  - Rohatgi, Milenkovic and Scott 2007, DOI `10.1126/science.1139740`, PMID `17641202`
  - Bangs and Anderson 2017, DOI `10.1101/cshperspect.a028175`, PMID `27881449`
  - Briscoe and Therond 2013, DOI `10.1038/nrm3598`, PMID `23719536`

## Dataset computations

I first read the training-count CSV to calibrate the endpoint. The focal-cell
training set has 1,674 perturbations: 1,205 zeros, 363 weak responses with
1-9 DEGs, 63 medium responses with 10-99 DEGs, and 43 strong responses with at
least 100 DEGs. The distribution is therefore zero-heavy, but a zero prediction
for a held-out gene still has to be justified by pathway-matched perturbations
rather than by the global majority class.

I then scanned the focal slice of the parquet for represented GLI/Hedgehog,
primary-cilium, GLI-processing, and developmental transcription-factor
comparators. The non-obvious part was using a row filter so the 616M-row parquet
was restricted to the cell group and genes of interest:

```python
dset = ds.dataset(TRAINING_PARQUET, format="parquet")
filt = (
    (ds.field("group_name") == "151 TH Prkcd Grin2c Glut")
    & ds.field("gene_target").isin(analogs)
)
tab = dset.to_table(
    columns=[
        "gene_target", "names", "logfoldchanges",
        "pvals_adj", "pvals", "scores",
        "n_pert_matched", "n_ctrl_matched",
    ],
    filter=filt,
)
```

This returned 17,259 measured genes per represented analog in the focal group.
I counted rows at `pvals_adj < 0.05` to match the task endpoint and separately
looked at canonical Hh readouts: `Gli1`, `Gli2`, `Gli3`, `Ptch1`, `Ptch2`,
`Hhip`, `Smo`, `Gpr161`, `Shh`, `Mycn`, `Ccnd1`, `Ccnd2`, `Ccne1`, `Foxm1`,
`Atoh1`, `Nes`, `Hes1`, and `Hes5`.

The exact training counts in `151 TH Prkcd Grin2c Glut` were:

| analog | `n_degs` | relevance to `Gli3` |
|---|---:|---|
| `Gli1` | 0 | GLI-family transcription factor and Hh-induced amplifier |
| `Gli2` | 0 | closest represented GLI activator paralog |
| `Ptch1` | 0 | ligand receptor and negative regulator upstream of SMO |
| `Ptch2` | 0 | PTCH-family Hh receptor/regulator |
| `Smo` | 0 | obligate canonical Hh transducer |
| `Gpr161` | 0 | ciliary cAMP/PKA repressor of GLI activation |
| `Ift88` | 0 | IFT-B ciliary component needed for mammalian Hh signaling |
| `Ttc21b` | 0 | IFT-A/ciliary trafficking component |
| `Cep290` | 0 | transition-zone/ciliary disease component |
| `Rfx3` | 0 | cilia-related transcription factor |
| `Prkaca` | 1 | PKA catalytic subunit; the one focal DEG is not a GLI/Ptch/Hhip reporter |
| `Gsk3b` | 6 | GLI/Wnt-related kinase; no canonical Hh output in this group |
| `Ctnnb1` | 383 | positive counterexample showing that 151 TH neurons can mount a strong Wnt/developmental-TF response |
| `Foxa2` | 0 | embryonic Shh ventral-patterning factor |
| `Nkx2-1` | 0 | ventral forebrain Shh-patterning factor |
| `Pax6` | 0 | developmental neurogenic TF checked as a boundary |
| `Otx2` | 0 | developmental brain-patterning TF checked as a boundary |

The canonical Hh reporter check was uniformly negative for the pathway analogs
in the focal group. For example, after `Gli1`, `Gli2`, `Ptch1`, `Ptch2`,
`Smo`, `Gpr161`, `Ift88`, `Ttc21b`, and `Cep290` perturbation, every inspected
`Gli1`/`Gli2`/`Gli3`/`Ptch1`/`Ptch2`/`Hhip`/`Smo`/`Shh` marker row had
`pvals_adj = 1.0`. `Gsk3b` weakly changed a few genes but also left
`Axin2`, `Lef1`, `Gli1`, `Gli2`, `Gli3`, `Hhip`, `Ptch1`, `Ptch2`, and `Smo`
nonsignificant; `Ctnnb1`, in contrast, strongly repressed Wnt feedback genes
such as `Lef1` and `Axin2` and produced hundreds of focal DEGs. Thus the focal
cell group was capable of a broad developmental signaling response, but not
through the represented Hh/GLI branch.

The Distributed Agents corpus agreed with the raw focal-count check at the pathway
level. `Gli3` itself was absent from the same-experiment corpus, as expected
for a held-out target, but `Gli1`, `Gli2`, `Ptch1`, `Ptch2`, `Smo`, `Gpr161`,
`Ift88`, `Kif3b`, `Dync2h1`, and `Cdon` formed a dense related cohort. The
shared high-confidence claim in the corpus was that represented acute
perturbations of Hedgehog receptors, SMO, GLI factors, GPR161, ciliary
transduction components, and co-receptors repeatedly failed to recover a
coordinated `Gli`/`Ptch`/`Hhip` feedback or proliferative transcriptional output
in postnatal NeuN+ nuclei.

## Target-specific reasoning

### `Gli3`

`Gli3` encodes a bifunctional GLI transcription factor. In the absence of
Hedgehog signaling, ciliary and PKA-dependent processing favors GLI repressor
production; Hh/PTCH-SMO signaling shifts GLI proteins toward activator output.
GLI3 is especially important as a repressor in embryonic dorsal-ventral neural
patterning, and GLI2 plus GLI3 are jointly able to mediate mouse Hh target-gene
activation in ventral spinal cord patterning (Persson et al. 2002; Bai,
Stephen and Joyner 2004). Mammalian PTCH1 and SMO traffic through the primary
cilium during Hh signal transduction, and cilia organize GLI activator/repressor
processing (Rohatgi, Milenkovic and Scott 2007; Bangs and Anderson 2017).

Those mechanisms make `Gli1`, `Gli2`, `Ptch1`, `Ptch2`, `Smo`, `Gpr161`, and
IFT/ciliary genes the correct first analogs, but in this particular assay they
point toward zero in the focal group:

- `Gli2` is the closest measured GLI-family analog. It had `n_degs = 0` in
  `151 TH Prkcd Grin2c Glut`, and the corpus report for `Gli2` found no
  downstream FDR<0.10 genes in any recovered neuronal class. Its Hh feedback
  genes `Gli1`, `Ptch1`, `Ptch2`, and `Hhip` were explicitly checked and did
  not move.
- `Gli1` was also `n_degs = 0` in the focal group. The only FDR<0.10 corpus
  events for `Gli1` were singletons in other cell groups, not a GLI/Hedgehog
  program, and represented Hh/ciliary comparators did not phenocopy those
  singleton hits.
- `Ptch1`, `Ptch2`, `Smo`, and `Gpr161` all had `n_degs = 0` in the focal
  endpoint. These perturb both sides of the upstream switch: loss of PTCH or
  GPR161 should de-repress Hh/GLI if the pathway is tonically constrained,
  whereas loss of SMO should reduce GLI activator output if the pathway is
  active. Neither direction produced a focal transcriptome.
- `Ift88`, `Ttc21b`, `Cep290`, and `Rfx3` were also `n_degs = 0` in the focal
  endpoint, arguing that a generic primary-cilium or cilium-to-Hh RNA program
  was not exposed in these postnatal thalamic glutamatergic neurons.

Two boundary comparisons kept the zero call from becoming "all developmental
genes are silent":

- `Ctnnb1` had `n_degs = 383` in the same cell group and strongly changed Wnt
  feedback genes. Large effects from a postmitotic developmental signaling
  effector are therefore detectable in `151 TH Prkcd Grin2c Glut`.
- `Gsk3b` had a small positive focal endpoint, `n_degs = 6`, but it did not
  activate a Wnt/beta-catenin program or a GLI/Ptch/Hhip program. `Prkaca`,
  another GLI-processing node, had `n_degs = 1`, apparently just the
  perturbation target row and no downstream Hh reporters.

My zero/nonzero decision for `Gli3` is driven mainly by the within-dataset
pathway evidence: all direct GLI and PTCH-SMO-cilium analogs were zeros at the
task cutoff in the same focal cell group, and the canonical Hh reporter genes
were present but flat. External biology resolves why that transfer is
appropriate. The known high-impact GLI3 functions are embryonic morphogen and
progenitor-patterning functions; the experiment instead edits sparse
postmitotic NeuN+ neurons at P16 and reads nuclear RNA 3-4 weeks later. A
single acute `Gli3` loss in this mature neuronal context is therefore unlikely
to create a stable cell-autonomous `Gli1`/`Ptch`/`Hhip` transcriptional state.

The point prediction is **0 DEGs**.

## Limits

- There is no measured `Gli3` perturbation in the supplied training data or in
  the same-experiment corpus, so this is an extrapolation from `Gli1`/`Gli2`
  and upstream Hh/ciliary genes, not a target-specific observation.
- `Gli3` has strong repressor biology that is not identical to `Gli1` or
  `Gli2`; the best represented upstream perturbations can test whether the Hh
  circuit is active, but they cannot perfectly mimic direct GLI3 de-repression.
- The assay reports survivor-conditioned nuclear RNA after sparse CRISPR. It
  does not measure GLI3 protein processing, ciliary GLI localization, embryonic
  fate specification, morphologic cilia phenotypes, glial Hh responses, or
  proliferating neural stem and cerebellar granule precursor compartments.
- Extreme log-fold changes for lowly detected genes with `pvals_adj = 1.0`
  were not treated as real expression changes. I relied on the adjusted
  Wilcoxon endpoint, pathway reporter panels, and analog DEG counts instead.
