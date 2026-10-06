# Chchd10 direct n_degs forecast

## Target and endpoint

- Target manifest: one row, `Chchd10`.
- Focal population: `151 TH Prkcd Grin2c Glut`.
- Endpoint: number of measured genes with BH-adjusted Wilcoxon `pvals_adj < 0.05` in the focal population, including the self transcript if it passes.
- The declared training parquet has no `Chchd10` rows in `151 TH Prkcd Grin2c Glut`; the point below does not use the withheld target profile or target count.

## Evidence used

### Canonical Chchd10 biology bundle

The target is reachable in this class: non-target nuclei show `Chchd10` expression in 17,776 of 23,679 cells, or 75.07%, with mean log1p CP10K 0.623. This makes a self-transcript call technically plausible.

The functional-stock card argues that a disruptive P16 edit should have removed pre-edit CHCHD10 by P37-P44: CHCHD10 is modeled as a dynamic inner-mitochondrial-membrane/intermembrane-space component, and the direct half-life datum is about 4 hours in HEK293 cells. That supports real perturbation of Chchd10 protein stock over the 21-28 day window.

The same bundle also gives the main attenuation: CHCHD10 physically and functionally overlaps with CHCHD2, combined Chchd2/Chchd10 loss activates OMA1/OPA1-linked cristae stress, and effective Chchd10 single knockout mice had no gross early brain phenotype or selected forebrain/substantia-nigra mitochondrial defect. Those data are not a matched thalamic snRNA-seq null, but they make a large single-Chchd10 transcriptional state unlikely.

### Training count table in the exact focal class

The 1,674 observed training perturbations in `151 TH Prkcd Grin2c Glut` are concentrated at the floor:

- 1,205 of 1,674 have `n_degs = 0`.
- 276 have `n_degs = 1`.
- Median `n_degs` is 0; the 75th percentile is 1 and the 90th percentile is 2.
- The heavy tail starts well away from most targets: only 106 training perturbations have at least 10 DE genes.

So the class is high-yield globally, but most individual perturbations still resolve as 0 or 1.

### Mitochondrial comparators from the training table and parquet

The most direct measured paralog, `Chchd2`, has `n_degs = 1` in `151 TH Prkcd Grin2c Glut`. Querying the declared parquet shows that this sole significant feature is `Chchd2` itself; there are zero significant downstream genes.

Other represented mitochondrial/cristae/OXPHOS comparators also sit near zero in the focal count table:

- `Micos13`: 0
- `Yme1l1`: 0
- `Afg3l2`: 0
- `Mff`: 0
- `Clpp`: 0
- `Cox4i1`: 0
- `Snca`: 0
- `Park7`: 1, self only
- `Ndufs2`: 1, self only
- `Ndufs8`: 1, self only
- `Tomm40`: 1, self only
- `Uqcrq`: 1

`Opa1` is the informative larger exception, with `n_degs = 37` and 36 downstream genes in this class, including the amino-acid/ISR-like genes `Asns`, `Mars1`, `Chac1`, `Ddit3`, `Cars`, and `Mthfd2`. That shows the assay can detect a mitochondrial-stress state in the focal population when OPA1 disruption crosses the stress threshold.

### Same-experiment corpus interpretation

The packaged corpus is another representation of the same experiment, not independent replication. I used it to interpret the Chchd2/Opa1 contrast already visible in the parquet:

- `Chchd2:F001` records Chchd2 as a 23-cell-group transcriptional null for non-target genes.
- `Chchd2:F002` records the absence of the OMA1-DELE1-eIF2alpha mitochondrial ISR after Chchd2 loss, while the Opa1 perturbation induces that program.
- `Chchd2:F003` records that Chchd2 aligned with the buffered mitochondrial subset rather than with the Opa1 mtISR state.
- `Opa1:F006` records that represented OPA1-processing and fission comparators such as `Yme1l1`, `Afg3l2`, `Mff`, and `Clpp` did not phenocopy Opa1.

## Synthesis

I expect a Chchd10 edit to be biologically realized by harvest and to occur in cells with measurable target RNA, so a self-transcript FDR call is credible. I do not expect a robust downstream state: the Chchd10 card itself emphasizes CHCHD2 redundancy and mild effective single-gene loss, and the most relevant in-atlas perturbation, Chchd2, is self-only despite the assay's ability to see Opa1-induced mitochondrial ISR in the same class.

The resulting direct point forecast is therefore a self-only response:

`predicted_n_degs = 1`
