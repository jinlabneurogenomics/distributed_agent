# Prediction trace

## Question and endpoint

The run asks for a point prediction of `n_degs` for each gene in
`103_Hdac4.csv` after that perturbation was fully held out from the supplied
DE parquet and the focal-cell training count table. The only requested target
is `Hdac4`.

I interpreted `n_degs` exactly as in the training CSV: in
`151 TH Prkcd Grin2c Glut` nuclei, count every measured gene with
Benjamini-Hochberg adjusted Wilcoxon `pvals_adj < 0.05`, including the target
transcript itself if it passes the threshold. Zero means that no measured gene,
self or downstream, is expected to pass FDR 0.05 in this assay.

The focal cell label is the thalamic glutamatergic Allen class
`151 TH Prkcd Grin2c Glut`; `TH` is thalamus, not tyrosine hydroxylase.

## Sources

- Training endpoint table:
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
  It contained 1,674 non-held-out targets. In this focal cell group, 1,205
  targets had 0 DEGs, 363 had 1-9, 63 had 10-89, and 43 had at least 100;
  the median was 0, the 75th percentile was 1, and the 95th percentile was 18.
- Training per-gene DE parquet:
  `[local file: training_de_all_cell_groups.parquet]`.
  I extracted the `151 TH Prkcd Grin2c Glut` rows for HDAC4-relevant pathway
  and chromatin comparators and verified their FDR<0.05 gene counts from the
  actual per-gene rows.
- Distributed Agents corpus release
  `perturbai-july-260713-sourceguard-1773-v1`, which is an internal semantic
  layer over this same Perturb-seq experiment. I used it for curated
  same-experiment findings around `Hdac5`, `Mef2c`, and calcium/MEF2
  comparators. It had no direct `Hdac4` target context, consistent with the
  held-out design.
- PubMed literature retrieved via the BioEval literature tool:
  Sando et al. 2012, Cell, DOI `10.1016/j.cell.2012.09.037`,
  PMID `23141539`; Kim et al. 2012, Journal of Neuroscience,
  DOI `10.1523/JNEUROSCI.2089-12.2012`, PMID `22875922`; Vega et al. 2004,
  Cell, DOI `10.1016/j.cell.2004.10.024`, PMID `15537544`.
- Literature references packaged in the Distributed Agents corpus for `Hdac5` and
  `Mef2c`: McKinsey et al. 2000, PNAS, DOI `10.1073/pnas.260501497`,
  PMID `11114197`; Hudson et al. 2015, Journal of Biological Chemistry,
  DOI `10.1074/jbc.M115.661058`; Assali et al. 2019, Current Opinion in
  Neurobiology, DOI `10.1016/j.conb.2019.04.008`; Akhtar et al. 2012,
  PLOS ONE, DOI `10.1371/journal.pone.0034863`.

## Computation over the training matrix

I first used the provided focal count CSV to put `Hdac4` on the observed assay
scale. The requested gene was absent, as required. Nearby targets showed:

| Training target | Focal `n_degs` | Why I used it |
| --- | ---: | --- |
| `Hdac5` | 0 | closest represented class-IIa HDAC paralog and signal-responsive MEF2 corepressor |
| `Hdac8` | 0 | only other represented HDAC-family perturbation in this run's training counts |
| `Mef2a` | 4 | HDAC4/5 repress MEF2-dependent transcription |
| `Mef2c` | 1 | MEF2 paralog with known postnatal neuronal effects |
| `Mef2d` | 0 | MEF2 paralog and a negative family counterexample |
| `Ppp3ca` | 4 | calcineurin catalytic subunit upstream of MEF2/class-IIa HDAC biology |
| `Ppp3r1` | 9 | calcineurin regulatory subunit; strongest calcineurin-axis count here |
| `Ppp3cc` | 0 | calcineurin catalytic subunit counterexample |
| `Camk2a` | 0 | CaMK pathway branch that regulates class-IIa HDAC localization |
| `Camk2b` | 1 | CaMKII paralog, self-only in this focal slice |
| `Camk2g` | 0 | CaMKII paralog counterexample |
| `Calm1` | 14 | strongest calmodulin locus in the focal group |
| `Calm2` | 0 | identical calmodulin protein from a buffered locus |
| `Calm3` | 1 | self-only calmodulin locus |
| `Ywhae` | 0 | 14-3-3 branch relevant to phosphorylated class-IIa HDAC export |
| `Ywhag` | 1 | self-only 14-3-3 family member |
| `Ywhaz` | 1 | self-only 14-3-3 family member |
| `Prkaca` | 1 | PKA/HDAC5 pathway comparator named by the internal Hdac5 finding |
| `Creb1` | 10 | activity-regulated transcription factor, weakly but detectably active |
| `Crebbp` | 8 | CREB/MEF2 coactivator, weak rather than broad in this focal group |
| `Ep300` | 0 | paralogous acetyltransferase counterexample |
| `Sin3a` | 1433 | broad chromatin-corepressor positive control, but mechanistically distant from class-IIa HDAC signaling |
| `Chd4` | 100 | chromatin-remodeling positive control showing the cell group can give chromatin DE |
| `Chd8` | 61 | chromatin positive control |
| `Smarcc2` | 185 | BAF-complex positive control in the same cell group |

For the main comparators I then filtered the full parquet to
`group_name == "151 TH Prkcd Grin2c Glut"` and counted rows with
`pvals_adj < 0.05`, keeping `names`, `gene_target`, `logfoldchanges`,
`pvals_adj`, `n_pert_matched`, and `n_ctrl_matched`. The focal slice had
17,259 tested genes per comparator. This confirmed, for example, that `Hdac5`
had 289 perturbed matched nuclei versus 23,679 matched controls but no FDR<0.05
genes; `Mef2c` had only its own transcript significant at FDR 0.05; `Camk2b`,
`Calm3`, `Ywhag`, and `Ywhaz` were also self-only one-gene effects.

The corpus also summarized the all-cell pattern for `Hdac5`: it produced only
one FDR<0.10 gene in the entire curated surface, `Chd5` up in
`012 MEA LA CA1 DG Glut`, and it did not induce canonical activity/MEF2 targets
such as `Npas4`, `Bdnf`, `Arc`, `Fos`, `Scn4b`, or `Tacr1`. Its curated
comparison against `Mef2a`, `Mef2c`, `Mef2d`, `Camk2a`, `Camk2g`, and `Prkaca`
found no phenocopy. The same corpus explicitly noted that `Hdac3`, `Hdac4`,
`Hdac7`, `Hdac9`, `Ncor1`, `Ncor2`, and `Chd5` were absent as represented
training perturbations, so the direct class-IIa/NCoR neighborhood was only
partially sampled.

## Hdac4-specific reasoning

HDAC4 is a class-IIa histone deacetylase. Like HDAC5, it is best understood as
a signal-regulated transcriptional corepressor that gates MEF2-dependent
programs rather than as a high-activity autonomous histone deacetylase.
Class-IIa HDACs have weak intrinsic catalytic activity and recruit repression
machinery through SMRT/NCoR-related complexes; CaMK-dependent phosphorylation
and 14-3-3 binding regulate class-IIa HDAC nuclear export
(McKinsey et al. 2000; Hudson et al. 2015). HDAC4 is absolutely capable of
affecting cells: germline Hdac4 loss derepresses RUNX2-dependent chondrocyte
hypertrophy in mice (Vega et al. 2004), and neuronal Hdac4 manipulations alter
synaptic plasticity and memory while NMDA receptor activity negatively
regulates HDAC4 nuclear chromatin association (Sando et al. 2012; Kim et al.
2012).

Those external facts argue that `Hdac4` is biologically meaningful, but they
do not argue for a broad basal FDR footprint in the postnatal sparse CRISPR
atlas. The nearest same-experiment readouts all sat at the floor:

- `Hdac5`, the closest represented class-IIa analog, was exactly 0 in
  `151 TH Prkcd Grin2c Glut` despite a strong matched-cell count.
- The only other represented HDAC target, `Hdac8`, was also 0 in the focal
  cell group.
- `Mef2a`, `Mef2c`, and `Mef2d`, which should be the cleanest downstream
  transcription-factor analogs if `Hdac4` loss were simply MEF2 derepression,
  had only 4, 1, and 0 FDR<0.05 genes in the focal cell group.
- Calcineurin and calcium/CaM/CaMK/14-3-3 nodes were sparse:
  `Ppp3ca` 4, `Ppp3r1` 9, `Ppp3cc` 0, `Camk2a` 0, `Camk2b` 1,
  `Camk2g` 0, `Calm1` 14, `Calm2` 0, `Calm3` 1, `Ywhae` 0, `Ywhag` 1,
  and `Ywhaz` 1.

The broad `Sin3a` count of 1433 and other chromatin counts such as `Chd4` 100,
`Chd8` 61, and `Smarcc2` 185 are important counterexamples: this thalamic
class can produce large FDR surfaces after chromatin perturbation. I did not
propagate those broad counts to `Hdac4`, because `Sin3a` is a scaffold-like
corepressor with many DNA-binding partners, and the internal corpus already
showed that represented Sin3/HDAC and MeCP2/NCoR-adjacent genes do not collapse
to one interchangeable neuronal state. The HDAC4-proximal evidence is the
sparse class-IIa/MEF2/calcium branch, not the broad SIN3A branch.

My zero/nonzero decision therefore came down to whether HDAC4 should depart
from HDAC5. HDAC4 has stronger published neuronal LOF phenotypes than HDAC5,
so a self-only or a few-gene focal response is plausible. However, this
endpoint is strict FDR<0.05 in recovered P37-P44 nuclei after partial mosaic
editing, under unstimulated basal conditions. Directly measured HDAC5 had no
focal target-gene FDR hit, MEF2C had only a self hit, and the corpus found the
canonical HDAC5 activity/MEF2 program absent. I therefore predict that acute
`Hdac4` loss is also below the FDR threshold in this exact `151` readout.

Point prediction: `Hdac4 = 0`.

## Limits

This is an extrapolation because `Hdac4`, the closest class-IIa paralogs
`Hdac7` and `Hdac9`, the catalytic complex member `Hdac3`, and the corepressor
genes `Ncor1` and `Ncor2` were not present in the training perturbations.
The `Hdac5` comparison is the key within-dataset anchor, but HDAC4 and HDAC5
are not interchangeable proteins. The assay also measured basal nuclear RNA in
surviving postmitotic nuclei; it did not assay depolarization, NMDA receptor
stimulation, learning, synaptic physiology, skeletal RUNX2 biology, or HDAC4
subcellular localization. A small self-transcript hit would be well within the
uncertainty of this prediction, but the mechanistic and same-experiment balance
favored zero rather than a weak nonzero count.
