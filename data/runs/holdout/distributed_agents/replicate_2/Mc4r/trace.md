# DEG-count prediction for the held-out target

## Question and setup

The requested target file contains one held-out perturbation:

```tsv
target_name
Mc4r
```

I interpreted the task as a point prediction of `n_degs`, the number of measured
mouse genes with Benjamini-Hochberg-adjusted Wilcoxon `pvals_adj < 0.05` after
acute mosaic CRISPR loss of the requested target in the focal neuronal group
`151 TH Prkcd Grin2c Glut`. I treated the endpoint as the assay-specific count
in this postnatal Perturb-seq screen, not as a measure of MC4R physiological
importance, editing efficiency, or the effect of germline Mc4r deletion.

The main ambiguity was that Mc4r itself has no held-out DE vector or DEG count in
the supplied training surfaces. I therefore used the training counts and focal
DE signatures of biologically related non-held-out targets to calibrate whether
a Mc4r knockout should be expected to cross the FDR threshold in this exact
cell group.

## Sources used

- Supplied endpoint table:
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
- Supplied all-cell differential-expression parquet:
  `[local file: training_de_all_cell_groups.parquet]`.
- Requested heldout manifest:
  `[local file: 135_Mc4r.csv]`.
- Distributed Agents same-experiment corpus release
  `perturbai-july-260713-sourceguard-1773-v1`, especially Mc1r, Mc2r, Agrp,
  Gnas, and Adcy3 findings and the melanocortin-system claim
  `claim:a37db0dd68ddbbfdd6ab`.
- PubMed literature searches through NCBI E-utilities for MC4R and
  melanocortin signaling.

Key external citations:

- Krashes, Lowell & Garfield, 2016, *Nature Neuroscience*,
  DOI `10.1038/nn.4202`, PMID `26814590`: review of MC4R-expressing central
  melanocortin circuits controlling feeding, energy expenditure, glucose
  homeostasis, and autonomic output.
- Farooqi et al., 2003, *New England Journal of Medicine*,
  DOI `10.1056/NEJMoa022050`, PMID `12646665`: human MC4R loss-of-function
  mutations cause a dosage-sensitive obesity/hyperphagia syndrome.
- Collet et al., 2017, *Molecular Metabolism*,
  DOI `10.1016/j.molmet.2017.06.015`, PMID `29031731`: POMC-derived peptides
  act through MC4R; an MC4R agonist requires MC4R signaling for weight-loss
  efficacy in rodents.
- Ghamari-Langroudi et al., 2015, *Nature*,
  DOI `10.1038/nature14051`, PMID `25600267`: in hypothalamic PVN neurons,
  MC4R can regulate neuronal firing through the Kir7.1 potassium channel in a
  Gs/cAMP-independent manner, with AgRP acting as a biased MC4R ligand.
- Higgins, Glendining & Jasoni, 2024, *Journal of Neuroendocrinology*,
  DOI `10.1111/jne.13366`, PMID `38279680`: developmental mouse PVN cells
  can co-express Leprb with Sim1, Pou3f2, Mc4r, and Bdnf, emphasizing that
  canonical Mc4r biology sits in hypothalamic melanocortin circuitry rather
  than generic thalamic glutamatergic neurons.

## Computations over the supplied data

The training DEG-count table had 1,674 non-held-out biological perturbations in
the focal cell group. It was strongly zero-inflated: 1,205 targets, or 72.0%,
had `n_degs = 0`; 363 had 1-9 DEGs; 63 had 10-99; and 43 had at least 100.
Thus a positive prediction needs target-specific evidence for a visible RNA
state, not just known disease biology.

The full parquet contains 616,253,184 rows. I used Parquet row-group metadata to
identify row groups 546-580 as containing `151 TH Prkcd Grin2c Glut`, then read
only `names`, `gene_target`, `scores`, `logfoldchanges`, `pvals_adj`,
`group_name`, `n_pert_matched`, and `n_ctrl_matched` for a curated Mc4r analog
set. The filter was simply:

```python
group_name == "151 TH Prkcd Grin2c Glut"
and gene_target in mc4r_analog_targets
```

I also ran a Distributed Agents runtime signed-profile comparison over the same 26
analogs in this matched context, using `logfoldchanges` as the signed value and
`pvals_adj < 0.05` as the significance definition. This was used to check
whether the low-count analogs hid a shared FDR-supported expression pattern.
They did not: 20/26 analogs had no significant genes, five had 1-9, one
(`Creb1`) had 10, and the sparse significant features were not recurrent across
the biologically relevant analogs.

## Mc4r-specific evidence

### Melanocortin-system analogs

The most direct represented melanocortin perturbations in the training data were
transcriptionally flat in the focal cell group:

| training target | focal `n_degs` | focal expression evidence |
|---|---:|---|
| `Mc1r` | 0 | no FDR-significant genes |
| `Mc2r` | 0 | no FDR-significant genes |
| `Agrp` | 0 | no FDR-significant genes |
| `Atrn` | 1 | only `Atrn` itself was significant: log2FC -0.685, adjusted p = 6.40e-05 |

The Distributed Agents corpus makes the same screen-local point at whole-experiment
scale: its melanocortin-system claim over `Agrp`, `Atrn`, `Mc1r`, and `Mc2r`
states that represented melanocortin receptor, peptide, and Atrn perturbations
independently showed flat or absent downstream RNA responses. The claim also
explicitly notes the limitation that `Mc4r`, `Mc3r`, `Pomc`, `Mrap`, and `Mrap2`
were absent as perturbation targets, so this is not a direct Mc4r measurement.

This is an imperfect but useful comparison. `Mc1r` and `Mc2r` are receptor
paralogs, not the central satiety receptor; `Agrp` is the endogenous MC3R/MC4R
antagonist/inverse agonist, not a postsynaptic receptor; and `Atrn` is an
accessory melanocortin factor. Still, all are closer to Mc4r biology than
unrelated high-DEG nuclear or proteostasis perturbations, and in the focal
thalamic class they all behaved like null/self-only events.

### Gs/cAMP and CREB pathway analogs

MC4R is classically a Gs-coupled GPCR, so I checked represented G-protein,
adenylyl-cyclase, PKA, Epac, PDE, and CREB-axis targets:

| training target | focal `n_degs` | focal expression evidence |
|---|---:|---|
| `Gnas` | 0 | no FDR-significant genes |
| `Adcy1` | 0 | no FDR-significant genes |
| `Adcy3` | 0 | no FDR-significant genes |
| `Adcy5` | 0 | no FDR-significant genes |
| `Prkaca` | 1 | only `Prkaca` itself significant: log2FC -0.940 |
| `Prkar1a` | 1 | only `Prkar1a` itself significant: log2FC -0.569 |
| `Rapgef2` | 0 | no FDR-significant genes |
| `Rapgef4` | 0 | no FDR-significant genes |
| `Pde4b` | 0 | no FDR-significant genes |
| `Pde4d` | 0 | no FDR-significant genes |
| `Gnal` | 0 | no FDR-significant genes |
| `Gnao1` | 1 | only `Gnao1` itself significant: log2FC -0.591 |
| `Creb1` | 10 | the small signature included `Crem` up-regulation |
| `Crebbp` | 8 | small signature, no overlap with the melanocortin or cAMP-effector nulls |

The direct nuclear CREB perturbations demonstrate that this cell group can
report a small transcription-factor response when the transcriptional node is
hit. However, the membrane and second-messenger nodes upstream of CREB were
zero or self-only. Distributed Agents corpus findings for `Gnas` and `Adcy3` summarize
the same pattern across the experiment: receptor/G-protein/adenylyl-cyclase/PKA
perturbations did not collapse into a shared durable basal cAMP or CREB mRNA
module 3-4 weeks after perturbation.

This makes a large focal `Mc4r` response unlikely. MC4R can change acute cAMP,
beta-arrestin, ERK, and Kir7.1-gated excitability, but those are ligand-gated or
post-translational effects; the training screen shows that removing individual
Gs/cAMP components rarely produced a chronic basal snRNA-seq footprint in the
same focal class.

### Feeding-GPCR and hypothalamic counterexamples

I also checked represented energy-balance or peptide-GPCR comparators that would
be plausible if sparse CRISPR loss of a feeding receptor generally produced a
detectable basal RNA feedback state:

| training target | focal `n_degs` |
|---|---:|
| `Lepr` | 0 |
| `Htr2c` | 0 |
| `Ghsr` | 0 |
| `Npy1r` | 0 |
| `Npy2r` | 0 |
| `Npy5r` | 0 |
| `Mchr1` | 0 |
| `Slc32a1` | 0 |
| `Stat3` | 0 |
| `Insr` | 0 |
| `Irs1` | 0 |
| `Ptpn1` | 0 |
| `Ptpn11` | 0 |

These are not Mc4r pathway members one-to-one, but they are useful
counterexamples: the assay did not turn known feeding, leptin, NPY, GABA, or
serotonin appetite biology into broad FDR-significant signatures in the
`151 TH Prkcd Grin2c Glut` class.

## Zero/nonzero decision

External biology says Mc4r is a high-confidence functional receptor in central
energy homeostasis: POMC-derived melanocortins activate it, AgRP antagonizes or
biases it, human MC4R loss causes obesity, and PVN hypothalamic MC4R neurons can
signal through cAMP and Kir7.1. Those facts make Mc4r important, but they do
not by themselves predict a many-gene steady-state nuclear RNA signature after
sparse postnatal knockout in a broad thalamic glutamatergic class.

The within-dataset evidence points the other way. The represented melanocortin
paralogs and peptide ligand were 0 in the focal class; the only melanocortin
accessory comparator had a self-only count of 1; the represented Gs/cAMP/PKA
effectors were 0 or self-only, with small effects only when directly perturbing
`Creb1` or `Crebbp`; and the feeding/neuropeptide GPCR comparators were also
0. Because `151 TH Prkcd Grin2c Glut` is thalamic rather than a purified
PVH/ARH MC4R ensemble, and because the endpoint is a basal 3-4 week snRNA-seq
readout rather than food intake, cAMP, pCREB, or membrane excitability, I
predict that Mc4r will behave like the null melanocortin/GPCR analogs.

Final point prediction for `Mc4r`: `0` DEGs.

## Limits

- There is no direct Mc4r perturbation profile in the supplied training parquet,
  training DEG-count CSV, or same-experiment Distributed Agents target records.
- The best represented melanocortin receptors are `Mc1r` and `Mc2r`, not
  `Mc4r`; `Mc1r` is more pigment/inflammatory and `Mc2r` is the ACTH receptor,
  so their null profiles are only indirect analogs.
- `Agrp` is presynaptic/ligand biology, while the held-out target is the
  postsynaptic receptor. A cell-autonomous receptor knockout in a rare
  Mc4r-positive population could have effects that an `Agrp` perturbation in
  broad NeuN+ classes misses.
- Baseline Mc4r expression in the exact `151 TH Prkcd Grin2c Glut` recovered
  nuclei was not provided, and the thalamic class label is coarser than the
  hypothalamic PVN/ARH MC4R circuits emphasized by the literature.
- The prediction extrapolates from lack of basal mRNA responses. It would not
  apply to germline Mc4r knockout, ligand stimulation, setmelanotide treatment,
  cAMP/pCREB/Kir7.1 assays, food-intake phenotypes, or subtype-resolved
  hypothalamic Mc4r neurons.
