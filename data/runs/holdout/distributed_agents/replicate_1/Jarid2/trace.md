# Held-out DEG-count prediction for `151 TH Prkcd Grin2c Glut`

## Question and endpoint

The requested target list contains one perturbation, `Jarid2`, in its requested
CSV order. I interpreted the task as a scalar prediction of the number of
measured RNAs with `pvals_adj < 0.05` after acute AAV-CRISPR loss of `Jarid2`
in the `151 TH Prkcd Grin2c Glut` thalamic glutamatergic class. `Jarid2`
itself was held out, so neither its `151` signature nor its DEG count is present
in the parquet or in the training count CSV.

The predicted endpoint is directly observed for training perturbations only.
For `Jarid2`, no validated quantitative proxy is present: the prediction is a
biological transfer from visible training perturbations plus external knowledge
of JARID2/PRC2 function. I did not use target-transcript loss as an editing
efficiency score, because the dataset portrait notes that target mRNA reduction
is a poor measure of functional CRISPR engagement in this assay.

## Sources used

- Declared training DEG-count table:
  `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
- Declared differential-expression parquet:
  `training differential-expression dataset`.
- Run-local requested-target manifest:
  `single-target request for Jarid2`.
- PerturbAI same-experiment semantic corpus:
  `perturbai-july-260713-sourceguard-1773-v1`, release date 2026-09-01. I used
  its compact Findings for `Kdm6b`, `Kmt2a`, `Setd1a`, and `Phf12` as
  summaries of the same screen, not as independent replication.
- PubMed literature searches through NCBI E-utilities for the external
  JARID2/PRC2 mechanism.

External citations used for the JARID2 mechanism:

- Takeuchi et al. 1995, Genes & Development, PMID 7758946,
  DOI 10.1101/gad.9.10.1211: mouse `jumonji`/`Jarid2` is embryonic lethal when
  disrupted and is required for normal neural tube morphogenesis.
- Landeira et al. 2010, Nature Cell Biology, PMID 20473294,
  DOI 10.1038/ncb2065: JARID2 is a PRC2 component in embryonic stem cells,
  supports PRC1/PRC2 and RNA polymerase II recruitment to developmental
  regulators, and is required for efficient neural and mesodermal
  differentiation.
- Kasinath et al. 2018, Biochemistry, PMID 30451485,
  DOI 10.1021/acs.biochem.8b01064: PRC2 catalyzes H3K27 methylation and is the
  complex that establishes repressive H3K27me3 domains.
- Sanulli et al. 2015, Molecular Cell, PMID 25620564,
  DOI 10.1016/j.molcel.2014.12.020: JARID2 is a PRC2 cofactor whose PRC2-
  mediated methylation and recognition by EED fine-tune H3K27me3 deposition
  during differentiation.
- Glancy et al. 2023, Molecular Cell, PMID 37030288,
  DOI 10.1016/j.molcel.2023.03.018: JARID2-containing PRC2.2 has a subcomplex-
  specific role in recruiting CBX7-canonical PRC1 in pluripotent cells.

## Dataset calibration

The training-count file contained 1,674 visible perturbations. Its focal-cell
endpoint was extremely zero-heavy: 1,205 of 1,674 training targets had
`n_degs = 0`; the median was 0, the 75th percentile was 1, the 95th percentile
was 18, and a small tail of broad responses extended to 2,677 DEGs. Thus a
positive call for a held-out chromatin regulator needs either a close visible
analog or a reason to expect a strong postnatal survivor signature.

I queried the parquet by `group_name == "151 TH Prkcd Grin2c Glut"` and visible
candidate targets, then counted rows with `pvals_adj < 0.05`; this reproduces
the training CSV endpoint and exposes the leading genes and effect directions
for candidate analogs. I also counted FDR-significant rows for a few material
perturbations across all available cell groups to avoid over-reading one focal
number.

Direct PRC2 comparators were missing: `Eed`, `Ezh1`, `Ezh2`, `Suz12`, the PCL
accessory genes, and `Jarid2` were not visible training perturbations. The
closest axis-level visible comparison was the H3K27 demethylase `Kdm6b`.

| training target | `151` `n_degs` | relevant expression-pattern evidence | relationship to `Jarid2` |
|---|---:|---|---|
| `Kdm6b` | 0 | No `pvals_adj < 0.05` genes in `151`; scanning all available `Kdm6b` rows found 0 FDR-significant genes in every assayed cell group. The same-experiment `Kdm6b:F001-F003` Findings also report an all-neuronal FDR-null and absence of expected KDM6B-responsive inflammatory, activity-regulated, SVZ-neurogenic, and cerebellar-granule programs. | Best visible H3K27-axis comparator, but a counter-direction perturbation: KDM6B removes H3K27 methylation whereas PRC2/JARID2 supports it. Its null argues that basal post-P16 neurons can buffer H3K27 writer/eraser perturbation, but it is not a same-direction PRC2 loss. |
| `Kmt2a` | 24 | Sparse thalamic program: `Nr2f1`, `Pcdh7`, `Lhx9`, `Pcdh10`, `Camk2d`, and `Grik2` were decreased, with a small induced arm including `Igfbp5` and `Tnr`. Across all groups I counted only 29 FDR-significant genes, 24 of them in `151`. | Demonstrates that a developmental histone methyltransferase can be detectable yet very small in this postmitotic assay. It is an H3K4 activator, so the causal sign and genomic targets are not PRC2-like. |
| `Kdm5c` | 18 | Small focal signature headed by induced `Ptgds` and `Capn3`; no broad stress or Polycomb-like state was evident in the inspected top genes. | Another H3K4-axis chromatin enzyme with a weak count. Useful as a chromatin counterexample only. |
| `Chd4` | 100 | Moderate focal response headed by `Begain` induction and `Cpne7`/`Ramp3` repression. | NuRD remodeling/HDAC machinery can produce a larger chromatin-regulator response than `Kdm6b` or `Kmt2a`, but it is not a PRC2 component. |
| `Brd4` | 311 | Broad focal signature with strong mixed changes, including `Omg`, `Plch2`, `Rnf112`, `Irag1`, `Sparcl1`, and `Akap8l` decreases and `Pabpn1` induction. | A positive chromatin regulator counterexample. Its bromodomain/transcriptional elongation biology is mechanistically distant from PRC2 recruitment. |
| `Setd1a` | 368 | Large, mostly down-regulated focal signature. The same-experiment corpus summarizes recurrent nuclear-encoded mitochondrial, GPI-anchor, ER/Golgi, primary-cilium, and lysosomal down-modules; in `151`, the strongest genes included `Itfg1`, `Foxred1`, `Nprl3`, `Sfi1`, `Tafazzin`, `Pigq`, `Zcchc7`, and `Ufl1`. | Shows that the assay has ample power to detect a major postmitotic histone-writer phenotype, but SETD1A is an H3K4 COMPASS writer, not the repressive PRC2/JARID2 module. |
| `Phf12` | 403 | Large up-biased focal signature with `Ptcd3`, `Zdhhc4`, `Dhx38`, `Srsf11`, ER/Golgi, RNA-processing, mitochondrial, and secretory-proteostasis induction; the same-experiment corpus maps this away from SETD1A and toward RNA/proteostasis stress. | A chromatin-associated repressor whose count is high, but its Sin3/TLE/HDAC biology and induced RNA-processing state are not an appropriate PRC2 surrogate. |

## Target-specific reasoning

### `Jarid2`

Biologically, `Jarid2` loss should impair a branch of Polycomb repression rather
than copy the visible H3K4 writers or bromodomain/NuRD repressors. The causal
chain I used was:

`Jarid2` CRISPR loss -> reduced JARID2-containing PRC2 recruitment/allosteric
activity at some developmental Polycomb domains -> potential de-repression of
developmental genes or altered PRC1 recruitment -> transcriptional propagation
in recovered postnatal thalamic glutamatergic neurons -> Wilcoxon DEGs after
3-4 weeks.

The strongest external evidence lies in embryonic stem cells and early
development, where JARID2 is needed to prime PRC2-regulated developmental loci
and embryos lacking `jumonji` die by midgestation with neural-tube defects.
Those stages require active cell-fate transitions. The requested assay is
different: sparse partial CRISPR perturbation starts at P16, the profiled
nuclei are postmitotic neurons harvested at P37-P44, and the endpoint counts
basal survivor mRNA changes rather than chromatin occupancy or evoked
differentiation capacity.

Within the training data, the only visible H3K27 writer/eraser-axis
perturbation, `Kdm6b`, was FDR-null in `151` and in all other assayed neuronal
groups. That is not same-direction endpoint transfer: KDM6B demethylates
H3K27 while PRC2/JARID2 promotes H3K27 methylation, and `Kdm6a` could in
principle compensate for `Kdm6b`. It nevertheless says the basal postnatal
H3K27me3 balance was not a high-yield transcriptional vulnerability in this
screen. The weak `Kmt2a` and `Kdm5c` counts also show that some developmental
chromatin regulators with known neuronal roles produce only tens of focal DEGs
here. Conversely, `Setd1a`, `Phf12`, `Brd4`, and `Chd4` prove that `151` cells
would have produced hundreds of FDR-significant genes if `Jarid2` loss had
evoked a broad RNA-processing, organelle, or generic chromatin-stress program;
those visible high-count states are mechanistically too distant to justify
transferring their DEG burdens to JARID2.

I therefore predicted no FDR-significant genes for held-out `Jarid2` in the
focal class. The zero is driven primarily by the within-dataset `Kdm6b` null and
the zero-heavy training distribution, with external PRC2 biology used to avoid
promoting high-count but non-Polycomb chromatin analogs.

Predicted count: `Jarid2 = 0`.

## Limits and uncertainty

- No core PRC2 loss-of-function perturbation (`Eed`, `Suz12`, `Ezh1`, or
  `Ezh2`) was visible, so the prediction cannot be calibrated from a
  same-complex training signature.
- `Kdm6b` is an H3K27 counter-enzyme rather than a same-direction PRC2
  perturbation; its null supports pathway buffering in the assayed context but
  does not prove that decreasing PRC2 activity is null.
- The literature grounding for JARID2 is strongest in embryonic stem cells,
  embryogenesis, and differentiation. Transfer to juvenile postmitotic
  thalamic neurons is an extrapolation.
- `n_degs` is thresholded and power dependent. A prediction of 0 means no genes
  are expected to pass BH FDR 0.05, not that JARID2 is biologically irrelevant
  or that editing would fail.
