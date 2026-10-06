# Fcgr2b DEG-count prediction for `151 TH Prkcd Grin2c Glut`

## Question and endpoint

The task asks for a point prediction of `n_degs` for the held-out mouse perturbation
`Fcgr2b` in `151 TH Prkcd Grin2c Glut` cells.  I interpreted `n_degs` exactly as
the number of measured genes with `pvals_adj < 0.05` in the Wilcoxon
differential-expression table for that perturbation and focal neuronal group.
`Fcgr2b` was completely held out, so neither its DEG count nor its expression
signature is present in the training count CSV or the Parquet.

The requested endpoint is directly observed for non-held-out training
perturbations.  It is absent for `Fcgr2b`; the prediction must therefore
extrapolate from visible perturbations and gene-function knowledge.  I did not
use measured target-RNA fold change as evidence of guide success or failure,
because this Perturb-seq design frequently leaves the target transcript flat
even after functional coding-sequence disruption.

## Sources used

- Declared focal training counts:
  `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
- Declared raw DE table:
  `training differential-expression dataset`.
- Run-local requested-target manifest:
  `single-target request for Fcgr2b`.
- The `perturbai-july-260713-sourceguard-1773-v1` internal corpus, specifically
  report/Finding summaries for `Fcgr4`, `Cd14`, `Csf1r`, `Tlr4`, and `Ptprc`.
  This corpus is a same-experiment interpretation layer over the DE Parquet,
  not an independent replication.
- PubMed-indexed external literature for Fc-gamma receptor function:
  Espeli, Smith, and Clatworthy 2016, DOI `10.1111/imr.12368`,
  PMID `26683154`; Stopforth et al. 2018, DOI
  `10.4049/jimmunol.1700832`, PMID `29351998`; Chauhan et al. 2017,
  DOI `10.1038/srep41889`, PMID `28165503`; Choi et al. 2015, DOI
  `10.1016/j.nbd.2015.08.025`, PMID `26342897`; Nimmerjahn et al. 2010,
  DOI `10.1073/pnas.1014515107`, PMID `20974962`.

## Quantitative checks over the training data

The focal training-count CSV contains 1,674 non-held-out perturbations.  The
distribution in `151 TH Prkcd Grin2c Glut` is highly sparse:

| statistic | value |
|---|---:|
| median `n_degs` | 0 |
| mean `n_degs` | 14.05 |
| perturbations with `n_degs = 0` | 1,205 / 1,674 |
| perturbations with `n_degs > 0` | 469 / 1,674 |
| 90th percentile | 2 |
| 95th percentile | 18 |
| maximum | 2,677 |

I then queried the declared Parquet only in the focal cell group for visible
immune-receptor and Fc-receptor-adjacent comparators.  The relevant operation
was:

```sql
SELECT gene_target,
       COUNT(*) AS rows,
       COUNT(*) FILTER (WHERE pvals_adj < 0.05) AS n_sig_005,
       COUNT(*) FILTER (WHERE pvals_adj < 0.10) AS n_sig_010,
       MIN(pvals_adj) AS min_fdr,
       MIN(n_pert_matched) AS n_pert,
       MIN(n_ctrl_matched) AS n_ctrl
FROM read_parquet($declared_training_de)
WHERE group_name = '151 TH Prkcd Grin2c Glut'
  AND gene_target IN ($selected_visible_comparators)
GROUP BY gene_target;
```

Every returned target had 17,259 measured genes in the focal group.  The
training-count endpoint and the raw focal Parquet agreed for the closest
comparators:

| visible perturbation | focal `n_degs` at FDR 0.05 | raw focal FDR<0.10 genes | focal perturbed / control nuclei | why it is relevant to `Fcgr2b` |
|---|---:|---:|---:|---|
| `Fcgr4` | 0 | 0 | 162 / 23,679 | the only visible Fc-gamma receptor perturbation; like `Fcgr2b`, it should require Fc-receptor-expressing immune or activated microglial cells and Ig immune-complex engagement |
| `Cd14` | 0 | 0 | 180 / 23,679 | visible myeloid innate co-receptor; tests whether an immune receptor axis has tonic activity in recovered NeuN-positive neurons |
| `Csf1r` | 0 | 0 | 146 / 23,679 | visible microglial/myeloid receptor with strong CNS biology outside neurons |
| `Tlr4` | 0 | 0 | 113 / 23,679 | ligand/DAMP receptor coupled to NF-kappaB/IRF inflammatory transcription |
| `Tlr2` | 0 | 0 | 167 / 23,679 | TLR-family receptor and `Cd14` comparator |
| `Nfkb1` | 0 | 0 | 181 / 23,679 | downstream inflammatory transcription factor |
| `Chuk` | 0 | 0 | 156 / 23,679 | IKK/NF-kappaB pathway kinase |
| `Map3k7` | 0 | 0 | 160 / 23,679 | innate immune-to-NF-kappaB/MAPK pathway kinase |
| `Cx3cr1` | 0 | 0 | 258 / 23,679 | microglial homeostatic receptor comparator |
| `P2ry12` | 0 | 0 | 102 / 23,679 | microglial homeostatic receptor comparator |
| `Spi1` | 0 | 0 | 178 / 23,679 | PU.1, microglial/myeloid lineage transcription factor |
| `Irf8` | 0 | 0 | 203 / 23,679 | microglial/myeloid lineage transcription factor |
| `Ptprc` | 0 | 0 | 140 / 23,679 | CD45, pan-leukocyte signaling phosphatase excluded with immune cells |
| `Itgb2` | 0 | 0 | 189 / 23,679 | leukocyte integrin and `Cd14` comparator |

The visible B-cell/T-cell costimulatory and antigen-receptor genes I checked
were also flat in the training endpoint: `Cd40`, `Cd80`, `Cd79a`, `Cd79b`,
`Cd14`, `Cd247`, `Cd27`, `Cd3d`, `Cd3e`, `Cd3g`, `Cd4`, and `Cblb` all had
`n_degs = 0` in the training-count CSV.  `Cd47` and `Cd81` each had only one
FDR 0.05 gene, which I treated as a counterexample showing that a tiny isolated
hit can occur but as weak evidence for a broad immune-receptor program.

The internal corpus supplied the same qualitative view from report-level
analyses.  Its `Fcgr4` report says `Fcgr4` had no FDR<0.10 downstream gene in
22 measured NeuN-positive neuronal groups and no meaningful Pearson/cosine
signature neighbor; it also states that `Fcgr1`, held-out `Fcgr2b`, `Fcgr3`,
`Fcer1g`, `Syk`, `Lyn`, and `Hck` were absent as direct Fc-receptor pathway
target perturbations, with only the broad Src kinase `Fyn` visible and flat.
`Cd14`, `Csf1r`, `Tlr4`, and `Ptprc` reports likewise summarized pan-neuronal
or broad neuronal nulls and explicitly attributed them to displacement of the
canonical immune mechanisms into microglia, macrophages, or other
non-NeuN-positive lineages and ligand/challenge conditions.

## Fcgr2b target-specific reasoning

`Fcgr2b` encodes Fc-gamma receptor IIB/CD32B, the sole inhibitory IgG Fc
receptor.  Productive Fc-gamma receptor IIB signaling is receptor- and
ligand-state dependent: immune complexes cross-link the receptor, its ITIM
recruits SHIP-family phosphatases, and this dampens BCR, Toll-like receptor,
complement-receptor, myeloid, and other immune-cell activation outputs
(Espeli, Smith, and Clatworthy 2016; Stopforth et al. 2018).  In the CNS,
published Fcgr2b biology is also glial or inflammatory rather than basal
postmitotic-neuronal: murine cytomegalovirus infection increases inhibitory
Fc-gamma RIIB on microglia and Fcgr2b knockout delays M2-like polarization
(Chauhan et al. 2017), while aggregated alpha-synuclein binds microglial
Fc-gamma RIIB and triggers SHP-1 to inhibit phagocytosis (Choi et al. 2015).

The causal model for transferring the visible analogs is:

1. `Fcgr2b` CRISPR loss would remove an inhibitory Fc receptor.
2. A direct molecular consequence requires `Fcgr2b` expression in the perturbed
   cell plus receptor engagement by IgG immune complexes or a disease ligand.
3. Propagation would flow through ITIM/SHP or ITIM/SHIP signaling into immune
   activation, polarization, or phagocytic programs.
4. The Perturb-seq design instead delivered guides at P16 to sparse
   postmitotic cells and sorted NeuN-positive nuclei from unchallenged juvenile
   whole brain minus olfactory bulb and hindbrain.
5. Microglia, macrophages, B cells, other leukocytes, and ligand-rich infection
   or alpha-synuclein disease states were not assayed, so the expected pathway
   is cut off before the direct receptor-signaling step in the recovered
   `151 TH Prkcd Grin2c Glut` nuclei.

`Fcgr4` is the most informative same-family training perturbation even though
it is an activating rather than an inhibitory Fc receptor.  Fc-gamma RIV has
well-established IgG2a/IgG2b effector functions in vivo (Nimmerjahn et al.
2010), but in this experiment its loss produced zero FDR 0.05 DEGs in the focal
thalamic glutamatergic cells and zero robust hits across all tested neuronal
groups.  The sign of proximal signaling differs between activating Fc-gamma RIV
and inhibitory Fc-gamma RIIB, so I did not infer that an `Fcgr2b` knockout
would phenocopy `Fcgr4` in a macrophage or stimulated microglial experiment.
For this endpoint, however, both perturbations are expected to have the same
outcome: no measurable basal transcriptional response in recovered
NeuN-positive thalamic neurons, because the receptor-bearing immune cell and
immune-complex exposure are absent.

The broader immune/myeloid analogs support the same zero/nonzero call rather
than simply adding superficial pathway votes.  `Cd14`, `Tlr2`, `Tlr4`,
`Nfkb1`, `Chuk`, and `Map3k7` ask whether a TLR/NF-kappaB inflammatory circuit
has tonic neuron-autonomous transcriptional activity; all were FDR-null in the
focal group.  `Csf1r`, `Cx3cr1`, `P2ry12`, `Spi1`, and `Irf8` ask whether
microglial maintenance and myeloid identity genes reveal a latent neuronal
state in the same assay; all were FDR-null in the focal group.  `Ptprc` and
`Itgb2` ask whether leukocyte signaling components are active after NeuN
sorting; both were FDR-null.  No candidate-specific counterexample indicated
that `Fcgr2b`, unlike those receptors, should be expressed and tonically
signaling in `151 TH Prkcd Grin2c Glut` neurons.

I therefore predict a point count of **0 DEGs** for `Fcgr2b`.

## Limits

This is an extrapolation from lineage-matched nulls, not a direct `Fcgr2b`
measurement.  `Fcgr2b` itself, `Fcgr1`, `Fcgr3`, `Fcer1g`, `Syk`, `Lyn`, and
`Hck` were not visible as non-held-out Perturb-seq targets, so the dataset
cannot test a complete Fc-receptor signaling module.  The evidence also does
not imply that Fc-gamma RIIB is inert in brain disease: microglial infection,
alpha-synuclein, immune complexes, systemic autoimmunity, or B-cell/myeloid
contexts could all depend on `Fcgr2b` while this juvenile NeuN-positive
unstimulated thalamic-neuron readout remains zero.  Finally, focal perturbed
cell counts of roughly 100 to 250 nuclei for the key visible comparators give
finite power; they are adequate for broad survivor-state signatures but can
miss very small or highly transient effects.
