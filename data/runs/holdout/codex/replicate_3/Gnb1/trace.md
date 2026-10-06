# Gnb1 n_degs forecast

Predicted perturbation: `Gnb1` in `151 TH Prkcd Grin2c Glut`

Forecast: `1`

## Evidence used

### Target biology bundle

`Gnb1` is well reached in the focal thalamic class: the declared exact
non-target expression measurement reports 19,830 / 23,679 nuclei expressing
`Gnb1` in `151 TH Prkcd Grin2c Glut` (83.75%), mean raw UMI 2.219, mean
log1p(CP10K) 0.768, and pseudobulk CPM 139.1.

The canonical target card identifies GNB1/Gbeta1 as a conventional
heterotrimeric G-protein beta subunit that forms Gbeta-gamma dimers and
couples GPCRs to effectors. Its stock adjudication calls the operative entity a
dynamic complex component and concludes that productive P16 disruption should
stop new intact Gbeta1 supply and likely substantially deplete functional
Gbeta1 over the 21-28 day edit-to-harvest interval. The card also preserves the
main uncertainty: there is no target-specific Gbeta1 turnover measurement in
P16-P44 thalamic neurons, embryonic/neonatal complete-loss phenotypes do not
transfer directly to this postmitotic assay, and paralog or partner buffering
in juvenile thalamic neurons remains quantitatively unresolved.

### Focal count table

The declared `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` contains 1,674
training perturbations for this cell class. Its distribution is sparse and
highly right-skewed:

- 1,205 / 1,674 perturbations have `n_degs = 0`
- median `n_degs = 0`
- mean `n_degs = 14.05`
- 90th percentile `n_degs = 2`
- 95th percentile `n_degs = 18`
- maximum `n_degs = 2,677`, from `Uba5`

I treated the high tail as a poor quantitative prior for `Gnb1` because it is
dominated by core RNA-processing, transcriptional, proteasomal, and trafficking
hits such as `Uba5`, `Tpr`, `Sin3a`, `Rnpc3`, `Zbtb7a`, `U2af2`, `Psmb4`, and
`Hnrnpu`, not by GPCR transducers.

I then used a manually selected focal cohort of represented GPCR/G-protein,
cAMP/GIRK, and nearby Ca2+ signaling perturbations. Their exact focal counts
were:

| target | n_degs |
|---|---:|
| `Gnao1` | 1 |
| `Gnas` | 0 |
| `Gnal` | 0 |
| `Gnb5` | 0 |
| `Rgs6` | 0 |
| `Adcy1` | 0 |
| `Adcy3` | 0 |
| `Adcy5` | 0 |
| `Kcnj6` | 0 |
| `Prkaca` | 1 |
| `Prkar1a` | 1 |
| `Grm1` | 1 |
| `Grm7` | 1 |
| `Gpr158` | 1 |
| `Gabrb2` | 4 |
| `Cacna1g` | 12 |
| `Calm1` | 14 |

All 17 cohort members were measured over 17,259 genes in the focal Parquet
slice, with 88-306 matched perturbed nuclei against 23,679 matched controls.
The cohort mean was 2.12 DEGs, the median was 1, 8 / 17 were zero, and even the
largest Ca2+/calmodulin-adjacent members remained far outside the screen-wide
right tail.

### Profile and report evidence for the cohort

I compared the 17 selected training profiles in the same
`151 TH Prkcd Grin2c Glut` slice. The cohort diagnostic used all 136 pairwise
comparisons and found weak recurrence of top-ranked features:

- positive top-tail overlap coefficient mean 0.025, median 0.02
- negative top-tail overlap coefficient mean 0.033, median 0.02
- no nonzero significant-program overlap among the retained significant
  positive or negative programs

The same-experiment corpus was consistent with the raw profile check. `Gnao1`
is a singleton or near-null perturbation and did not phenocopy represented
Gi/o/cAMP relatives. `Gnas` likewise failed to induce a durable basal CREB or
immediate-early module and was near-zero correlated with cAMP-pathway
comparators. `Gnb5` produced no robust downstream transcriptional response in
any measured neuronal group, and its R7/GPCR/GIRK neighborhood was also nearly
silent. `Adcy5` and the represented membrane adenylyl cyclases were downstream
null across recovered groups. These reports are the same experiment as the
Parquet, so I used them as interpretation of the observed training surfaces,
not as an independent replicate.

## Synthesis

The Gnb1 bundle argues that a productive edit should remove an expressed,
nonredundant GPCR beta-subunit pool in many focal neurons by harvest, so I did
not collapse the forecast to a generic safe-target-like null. However, the
closest measured GPCR, G-protein, adenylyl-cyclase, GIRK, metabotropic-receptor,
and kinase nodes show that proximal signaling perturbations in this postnatal
basal snRNA-seq assay usually leave zero or a single FDR-significant gene, and
their full profiles do not form a coherent durable RNA module that `Gnb1`
should inherit.

I therefore forecast a near-null but not fully silent outcome: one
FDR-significant measured gene, representing either the on-target transcript
alone or an isolated singleton rather than a multi-gene downstream program.
