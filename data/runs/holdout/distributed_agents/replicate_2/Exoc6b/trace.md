# Held-out target

The task asks for the number of genes that would be significant at
Benjamini-Hochberg adjusted Wilcoxon `pvals_adj < 0.05` in
`151 TH Prkcd Grin2c Glut` nuclei after the held-out CRISPR perturbation.  The
manifest contains one target:

```tsv
target_name
Exoc6b
```

I treated `n_degs` as self-inclusive, matching the training CSV: if the target
transcript itself was the only corrected hit, the training endpoint is 1.
`Exoc6b` was absent from both supplied training tables, as expected for a
held-out target.

# Sources

Internal same-experiment sources:

- `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`: exact focal-cell DEG
  counts for 1,674 non-held-out perturbations.
- `training_de_all_cell_groups.parquet`: per-gene log2 fold changes and
  adjusted p-values.  I filtered this to `group_name ==
  "151 TH Prkcd Grin2c Glut"` for mechanistically related perturbations.
- Distributed Agents corpus release `perturbai-july-260713-sourceguard-1773-v1`, the
  curated semantic layer over the same PerturbAI experiment.  This release had
  no `Exoc6b` Finding or Claim, but had useful negative and contrast Findings
  for `Rala`, `Rab27a`, `Stx1b`, `Stxbp1`, `Rab7`, and `Vps35`.
- A bounded Distributed Agents runtime comparison,
  `profile_neighbors_151_exoc6b_analogs.json`, comparing focal-cell log-fold
  change profiles among 31 vesicle, exocytic, endocytic, Rab, adaptor, and ER
  trafficking perturbations.

External mechanism sources:

- The exocyst is an octameric vesicle-tethering complex that directs
  post-Golgi and recycling-endosome carriers to restricted plasma-membrane
  sites; see Martin-Urdiroz et al. 2016, DOI
  `10.3389/fcell.2016.00024`, PMID `27148529`.
- The Sec15/EXOC6 subunit is a mammalian Rab11 effector at recycling
  endosomes; see Zhang et al. 2004, DOI `10.1074/jbc.M402264200`,
  PMID `15292201`.
- RalA binds brain exocyst complexes in a GTP-dependent manner; see Brymora
  et al. 2001, DOI `10.1074/jbc.C100320200`, PMID `11406615`.  RalA also
  promotes exocyst-dependent GTP-triggered exocytosis in PC12 cells; see Wang
  et al. 2004, DOI `10.1074/jbc.M400522200`, PMID `14978027`.
- Exocyst components contribute to neuronal membrane growth and glutamate
  receptor delivery rather than simply catalyzing fast synaptic vesicle fusion:
  Sec5 loss blocked membrane addition but left transmitter release intact in
  Drosophila neurons, Murthy et al. 2003, DOI
  `10.1016/s0896-6273(03)00031-x`, PMID `12575951`; Sec8/SAP102 and Exo70
  studies connected exocyst subunits to NMDA and AMPA receptor trafficking,
  Sans et al. 2003, DOI `10.1038/ncb990`, PMID `12738960`, and Gerges et al.
  2006, DOI `10.1038/sj.emboj.7601065`, PMID `16601687`; Lira et al. 2020,
  DOI `10.3390/cells9112402`, PMID `33153008`, reviews the exocyst in
  glutamatergic receptor trafficking.
- Human `EXOC6B` disruption has been reported with developmental delay,
  epilepsy, and intellectual disability, and biallelic loss-of-function causes
  spondylo-epi-metaphyseal dysplasia with impaired ciliogenesis:
  Fruhmesser et al. 2013, DOI `10.1038/ejhg.2013.18`, PMID `23422942`;
  Evers et al. 2014, DOI `10.1002/ajmg.a.36770`, PMID `25256811`; Girisha
  et al. 2015, DOI `10.1038/ejhg.2015.261`, PMID `26669664`;
  Simsek-Kiper et al. 2022, DOI `10.1002/humu.24478`, PMID `36150098`.

# Computation over the training tables

I first read the 1,674-row focal count CSV to calibrate this endpoint.  The
distribution is sparse: the median is 0, the 75th percentile is 1, the 90th
percentile is 2, and only 469 of 1,674 training perturbations are nonzero.
This makes the distinction between "biologically important" and "visible as a
broad steady-state nuclear RNA response" central.

I then filtered the parquet to the focal cell group for a curated analog panel:
`Rala`, `Cdc42`, `Rac1`, `Rab7`, `Vps35`, `Rab18`, `Rab27a`, `Rab3gap1`,
`Rab3gap2`, `Stx1b`, `Stxbp1`, `Vamp1`, `Cplx1`, `Cplx2`, `Unc13a`,
`Unc13b`, `Unc13c`, `Syn1`, `Syn2`, `Cltc`, `Sec23a`, `Sec63`, `Trappc6b`,
`Trappc9`, `Trappc10`, `Ap1b1`, `Ap3b1`, `Ap4s1`, `Tbc1d24`, `Vps13a`, and
`Vps13c`.  These genes bracket Exoc6b by direct exocyst regulation, Rabs,
SNARE/synaptic-vesicle machinery, endosomal sorting, Golgi traffic, and
secretory stress.  The exact `pvals_adj < 0.05` counts from the filtered
parquet matched the training CSV.

Measured focal-cell evidence for the main comparisons:

| Perturbation | focal `n_degs` | expression evidence in `151 TH Prkcd Grin2c Glut` | relationship to `Exoc6b` |
|---|---:|---|---|
| `Rala` | 0 | Minimum adjusted p-value was 0.975; the Distributed Agents corpus reports no downstream FDR<0.10 genes in any recovered neuronal class and no coherent Ral-like nearest-neighbor module. | Best measured exocyst regulator. A complete null for acute `Rala` argues against a broad Ral/exocyst transcriptional program in this assay. |
| `Cdc42` | 1 | The only FDR<0.05 gene was the target transcript, `Cdc42`; all non-self genes had adjusted p = 1. | Rho-family polarity regulator that can interface with exocyst-directed growth. Its focal response was self-only. |
| `Rac1` | 0 | No corrected genes; minimum adjusted p = 1. | Actin/polarity GTPase counterexample, less direct than RalA. |
| `Rab27a` | 0 | No corrected genes in the focal group; the Distributed Agents corpus calls Rab27a a corrected transcriptomic null across 21 recovered neuronal groups. | Secretory Rab counterexample; loss of a vesicle-targeting Rab did not create a somatic RNA program. |
| `Rab18`, `Rab3gap1`, `Rab3gap2` | 0, 0, 0 | All were focal nulls, with minimum adjusted p-values 0.912, 1, and 0.830. | Rab-cycle relatives; useful boundary showing that nearby vesicle regulators were usually buffered or invisible transcriptionally. |
| `Stx1b` | 0 | No FDR<0.05 focal genes and a Distributed Agents Finding of a pan-measured neuronal null at FDR<0.10. | Canonical vesicle-fusion component; argues that impaired exocytosis per se does not guarantee a detectable nuclear response. |
| `Vamp1`, `Cplx1`, `Syn1` | 1, 1, 1 | Each singleton was the perturbed transcript itself; non-self adjusted p-values were 1.0, 0.766, and 1.0. | Presynaptic vesicle machinery and vesicle reserve proteins; their downstream programs were effectively null in the focal class. |
| `Cplx2`, `Unc13a`, `Unc13b`, `Unc13c`, `Syn2` | 0 each | No focal FDR<0.05 genes. | Additional fast-release comparators. |
| `Stxbp1` | 1 | The only focal FDR<0.05 hit was `Stxbp1` itself; the best non-self adjusted p was 0.527. The same-experiment corpus reports broader Stxbp1 effects in other classes, but also that canonical release genes did not phenocopy Stxbp1. | Counterexample: a release regulator can be visible in the screen, but that visibility is not shared by most SNARE-cycle members and is not present downstream in this focal class. |
| `Cltc` | 3 | Three focal genes passed FDR<0.05: `Gabra4`, `Rbms1`, and `Ero1b`, with only 32 matched perturbed nuclei. | Endocytic vesicle coat; a detectable but tiny and low-power focal response, not a broad membrane-trafficking state. |
| `Vps35` | 17 | Top focal hits included `Atp2a2`, `Brsk1`, `Grin2b`, `Ccdc136`, `Vps35`, `Pik3r2`, `Kifc2`, and `Coch`. | Retromer/endosomal trafficking positive comparator. It shows that the focal class can report some trafficking defects, but the response was modest and mechanistically downstream of late endosomal sorting rather than exocyst tethering. |
| `Rab7` | 501 | The focal signature was dominated by V-ATPase/lysosomal and stress genes such as `Atp6v1b2`, `Dpp7`, `Atp6v0b`, `Lamp2`, `Sqstm1`, and `Ctsd`, with down-regulation of receptor/ion-channel genes such as `Grin2b` and `Gabra4`. | Strong counterexample. Acute loss of the core late-endosomal GTPase produced a broad lysosomal compensation state that is much more severe than expected for partial Exoc6b loss. |
| `Sec23a` | 0 | No corrected focal genes; the self row had adjusted p = 0.873. | ER-to-Golgi vesicle formation control. |
| `Sec63` | 11 | Focal hits included ER stress/chaperone genes `Hspa5`, `Canx`, `Hyou1`, and `Chac1`. | ER import/stress comparator. It demonstrates an ER stress readout, but that mechanism is not the primary exocyst defect. |
| `Trappc6b`, `Trappc9`, `Trappc10`, `Ap1b1`, `Ap3b1`, `Ap4s1`, `Tbc1d24`, `Vps13a`, `Vps13c` | 0, 0, 0, 1, 0, 0, 0, 0, 0 | `Ap1b1` was self-only; the others had no FDR<0.05 focal hits. | Further Golgi/adaptor/lipid-transfer trafficking boundaries. |

The runtime log-fold-change profile comparison among these 31 genes did not
rescue a coherent exocyst-like signature: `Rala`, `Rab27a`, `Stx1b`, `Syn1`,
and the Rab3GAP/TRAPP/adaptor targets all had zero or self-only significant
programs.  Whole-profile correlations were not treated as positive biological
evidence because they were driven largely by shared extreme, non-significant
tails with adjusted p = 1.0.

# Target-specific reasoning for `Exoc6b`

`Exoc6b` encodes a Sec15-family exocyst subunit, so the most direct prior is a
defect in tethering Rab11/recycling-endosome cargoes to a cortical exocyst
assembly site, with possible consequences for membrane addition, postsynaptic
glutamate-receptor delivery, and ciliary trafficking.  Those mechanisms are
real, but three aspects make a broad `151 TH Prkcd Grin2c Glut` nuclear RNA
footprint unlikely here.

First, the nearest measured exocyst regulator, `Rala`, was a complete
transcriptional null in the same PerturbAI assay.  The curated Distributed Agents
Finding for `Rala` also notes that canonical RalBP1/exocyst, PAR-polarity,
AMPAR-trafficking, PLD1, and mTOR sentinels were not corrected-DE.  Thus the
training data give direct evidence that perturbing an exocyst-engaging GTPase
does not automatically produce a focal somatic expression program.

Second, the neuronal vesicle and secretory comparators were much closer to zero
than to the endolysosomal stress outlier.  `Stx1b`, `Cplx2`, `Unc13a/b/c`,
`Syn2`, `Rab27a`, `Rab18`, `Rab3gap1`, `Rab3gap2`, `Sec23a`, `Trappc6b`,
`Trappc9`, and `Trappc10` were all focal nulls; `Vamp1`, `Cplx1`, `Syn1`, and
`Ap1b1` only reached significance on the target transcript.  `Stxbp1` was also
self-only in the focal cell group.  These results make a 10 to 100 DEG
prediction for another exocytic tethering gene hard to justify.

Third, the positive trafficking counterexamples seem mechanistically too far
from `Exoc6b` to use quantitatively.  `Rab7` loss caused a 501-gene lysosomal,
autophagy, lipid, and proteostatic response, and `Sec63` loss caused a clear ER
stress program; `Exoc6b` is downstream at the plasma-membrane tethering step and
has an `Exoc6` paralog.  `Vps35` gave a more modest 17-gene endosomal/receptor
state, which is the closest positive comparator, but retromer loss is expected
to disturb endosome retrieval and receptor sorting more globally than partial
loss of one Sec15 paralog.

The human `EXOC6B` developmental and ciliogenesis literature increases
confidence that the gene matters for morphogenesis, but it comes mostly from
germline or patient cell contexts.  The current experiment is sparse,
postnatal, acute CRISPR in recovered NeuN+ nuclei, where developmental
ciliogenesis and skeletal extracellular-matrix programs should be weakly
sampled.  I therefore predict no measured gene, including `Exoc6b` itself, will
clear adjusted p < 0.05 in the focal cell class.

Final point prediction: `0`.

# Limits

- There is no measured same-complex exocyst knockout in the focal training
  table, and the selected Distributed Agents corpus has no `Exoc6b` Finding.  The
  prediction is an extrapolation from regulators and adjacent trafficking
  modules rather than a direct paralog/complex phenocopy.
- Several analogs are imperfect.  `Rab7`, `Vps35`, and `Sec63` report
  endosomal or ER stress; `Stx1b`/`Cplx1`/`Unc13*` report fast synaptic release;
  `Rala` is an upstream GTPase with multiple effectors.  None is a clean acute
  `Exoc6b` substitute.
- A singleton outcome driven by an `Exoc6b` self-transcript hit remains
  plausible because the endpoint counts self rows.  I did not use target RNA
  knockdown as an editing-efficiency proxy; the prediction of zero is instead
  based on the weak downstream responses of measured trafficking neighbors and
  the likelihood that `Exoc6b` is not a strong self hit.
- The assay is nuclear RNA from recovered neurons.  A real Exoc6b defect in
  vesicle tethering, receptor surface delivery, neurite growth, cilia, or
  synaptic physiology could occur with no stable transcriptional consequence
  detectable by this endpoint.
