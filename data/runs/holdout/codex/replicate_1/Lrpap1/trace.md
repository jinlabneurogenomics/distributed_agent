# Lrpap1 direct n_degs forecast

## Requested quantity

The one-row holdout manifest names `Lrpap1`; the focal endpoint is the integer
count of measured genes with `pvals_adj < 0.05` in `151 TH Prkcd Grin2c Glut`.
The supplied `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` has 1,674
training perturbations and does not contain `Lrpap1`.

## Target biology used

The declared `Lrpap1` biology bundle says that the target is directly expressed
in the focal class: in matched non-target nuclei, `Lrpap1` had mean CP10K
1.0002, mean raw UMI 1.6396, and was detected in 17,528 of 23,679 nuclei
(`74.0%`).  Thus the perturbation is reachable in the requested thalamic
glutamatergic population.

The same card makes the functional-stock prior non-null but limited.  LRPAP1/RAP
is an ER-resident chaperone/escort for LDL-receptor-family clients, so an edit
at P16 should stop production of new RAP and should substantially reduce the
renewed mature client-receptor pool by P37-P44.  The supporting neural loss
evidence is germline/hippocampal rather than an induced postnatal thalamic
time-course, and RAP-null neural evidence reported impaired LRP maturation and
localization without a gross brain-architecture or cultured-neuron survival
phenotype.  I therefore treated `Lrpap1` as biologically engaged but not as an
obvious broad acute transcriptional stressor.

## Training measurements used

The full focal count table is strongly concentrated at zero:

| statistic | value |
|---|---:|
| training perturbations | 1,674 |
| `n_degs = 0` | 1,205 |
| `1 <= n_degs <= 4` | 337 |
| `n_degs >= 5` | 132 |
| median | 0 |
| 75th percentile | 1 |
| 90th percentile | 2 |

The most directly relevant receptor/adaptor perturbations in the same focal
class were almost all at the null floor:

| training target | `151 TH Prkcd Grin2c Glut` `n_degs` |
|---|---:|
| `Lrp1` | 0 |
| `Lrp2` | 0 |
| `Lrp4` | 0 |
| `Lrp5` | 0 |
| `Lrp6` | 4 |
| `Lrp8` | 0 |
| `Vldlr` | 0 |
| `Sorl1` | 0 |
| `Sort1` | 0 |
| `App` | 1 |
| `Apbb2` | 0 |
| `Appl1` | 0 |

Those 12 LDLR/APP/sorting-axis perturbations have median `n_degs = 0` and mean
`n_degs = 0.42`.  Direct Parquet inspection of the exact focal class confirmed
that the zeroes were complete FDR-null surfaces for the represented receptor
targets; for example `Lrp1`, `Lrp2`, `Vldlr`, `Sorl1`, and `Sort1` each had no
gene below FDR 0.05 among 17,259 measured rows.

ER quality-control comparisons put an upper bound on a stress interpretation:

| training target | `151 TH Prkcd Grin2c Glut` `n_degs` |
|---|---:|
| `Atf6` | 0 |
| `Edem3` | 0 |
| `Hspa5` | 5 |
| `Sec63` | 11 |

`Sec63` and `Hspa5` show that ER folding or ER-client stress can be recovered in
this thalamic class, but direct `Atf6` loss and `Edem3` loss were quiet.  Same
experiment corpus reports sharpened this boundary: `Hspa5` and `Sec63`
perturbations induce ER chaperone/ERAD or UPR-like transcription in vulnerable
neurons, whereas `Atf6`, `Edem3`, and `Lrp1` do not recapitulate that durable
ER-stress module under matched conditions.

## Synthesis

I expect most of the `Lrpap1` effect to be loss of mature LDL-receptor-family
client function, not a strong backlog of unfolded bulk ER cargo.  In the exact
requested class, direct loss of the principal represented clients and related
sorting receptors was nearly always FDR-null and even `Lrp1` was uncoupled from
the detectable UPR program.  The focal target expression is high enough that the
self transcript, or one weak client-homeostasis transcript, could pass the
Wilcoxon/BH threshold even if downstream biology is otherwise buffered.

Point forecast: `1` DEG.
