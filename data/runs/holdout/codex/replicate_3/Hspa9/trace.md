# Hspa9 direct n_degs forecast

Endpoint: number of `151 TH Prkcd Grin2c Glut` measured genes with Wilcoxon
BH-adjusted `p < 0.05`.

Target: `Hspa9`.

I used the declared one-row holdout manifest, the declared Hspa9 biology bundle,
the training count table
`151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`, and the matching training
DE Parquet. The count table and Parquet are two views of the same experiment;
I used the Parquet only to verify the 151-class rows behind selected training
perturbations and to inspect near-threshold support.

## Target biology

The Hspa9 biology bundle identifies HSPA9 as the mitochondrial HSP70
motor/chaperone for import, folding/assembly, quality control, and
iron-sulfur-cluster machinery. The functional-stock adjudication was only
partial: loss of new synthesis should matter because HSPA9 is a renewed
mitochondrial factor and a CLPP/CLPX-dependent degradation substrate, but
pre-existing imported protein is expected to keep functioning after an edit and
no juvenile-thalamus half-life pins down clearance within the 21-28 day
P16-to-harvest window. The same bundle also gives exact focal expression reach:
in non-target `151 TH Prkcd Grin2c Glut` nuclei, Hspa9 was detected in
10,522/23,679 nuclei, 44.44%, with mean raw UMI 0.654 and mean CP10K 0.393.

## Training measurements

The 151-class training table contained 1,674 observed perturbations. Its DEG
burden was very sparse: 1,205 had `n_degs = 0`, the median was 0, the 75th
percentile was 1, the 90th percentile was 2, and the 95th percentile was 18.
Only the extreme tail reached hundreds to thousands of DEGs.

I emphasized training perturbations that stress mitochondrial matrix import,
mitochondrial protein quality control, Fe-S/respiratory machinery, or a nearby
compartmental chaperone system:

| training target | reason for comparison | `n_degs` in 151 TH Prkcd Grin2c Glut |
| --- | --- | ---: |
| `Dnajc19` | inner-membrane co-chaperone coupled to the HSPA9 import motor | 0 |
| `Clpp` | mitochondrial ClpXP protease partner regulating HSPA9 turnover | 0 |
| `Clpx` | mitochondrial ClpXP unfoldase partner | 0 |
| `Lonp1` | mitochondrial matrix protease/proteostasis factor | 0 |
| `Nfs1` | Fe-S biogenesis axis downstream of HSPA9-supported machinery | 0 |
| `Timmdc1` | mitochondrial respiratory-complex assembly | 0 |
| `Tomm40` | mitochondrial protein import channel | 1 |
| `Afg3l2` | mitochondrial AAA protease | 0 |
| `Yme1l1` | mitochondrial inner-membrane AAA protease | 0 |
| `Mff` | mitochondrial fission boundary | 0 |
| `Park7` | mitochondrial stress boundary; only its self transcript was significant | 1 |
| `Opa1` | stronger mitochondrial-dynamics boundary with an ISR-like signature | 37 |
| `Hspa5` | ER HSP70 boundary | 5 |
| `Hspa8` | cytosolic constitutive HSP70 boundary | 9 |
| `Hsp90ab1` | broad cytosolic chaperone boundary; only self was significant | 1 |

For the core mitochondrial import/proteostasis group, the Parquet showed no
FDR 0.10 near-misses for `Dnajc19`, `Clpp`, `Clpx`, `Lonp1`, `Nfs1`,
`Timmdc1`, `Afg3l2`, or `Yme1l1`; the best adjusted p-value across those zero
targets was still 0.233 for `Nfs1`. `Tomm40`, `Park7`, and `Hsp90ab1` each had
a single significant self transcript, while the positive HSP-family boundaries
remained single-digit. `Opa1` was the main non-zero mitochondrial boundary,
but its 37-gene amino-acid/ISR-like response reflects inner-membrane dynamics
rather than the HSPA9 import motor itself.

## Point forecast

The nearest measured mitochondrial dependencies argue for an endpoint close to
zero in this recovered thalamic population. Hspa9 is more central than the
silent ClpXP and import-adaptor peers, and its transcript is detectable in the
focal class, so I do not want to force an exact zero. The partial functional
stock, postmitotic survivor-conditioned assay, lack of high-count mitochondrial
training analogs, and only low single-digit HSP70-family boundaries together
put the best point at an isolated-signature result:

`predicted_n_degs = 1`
