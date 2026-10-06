# Mitf DEG-count prediction trace

## Question understood

The held-out target list for this run contains one mouse gene, `Mitf`.  I need
to predict the number of genes that would pass FDR 0.05 after an acute mosaic
CRISPR loss-of-function perturbation of `Mitf` in `151 TH Prkcd Grin2c Glut`
neurons.  `Mitf` was held out from both supplied same-experiment inputs, so I
treated the focal training counts and signatures of related observed
perturbations as the calibration set and used external biology only to decide
which training genes were mechanistically interpretable.

Two ambiguities I resolved:

- The endpoint is the count of `pvals_adj < 0.05` rows in the focal cell group,
  not the magnitude of the `Mitf` guide's own RNA knockdown.
- A 0 prediction means no measured gene is expected to pass the
  Benjamini-Hochberg threshold in this assay; it does not claim that MITF has no
  biology in any cell type.

## Sources used

- Input differential-expression parquet:
  `[local file: training_de_all_cell_groups.parquet]`
- Focal training DEG counts:
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`
- Requested-target manifest:
  `[local file: 138_Mitf.csv]`
- Distributed Agents corpus MCP, release
  `perturbai-july-260713-sourceguard-1773-v1`: queried for `Mitf` target
  context and Mitf-centered claims.  The corpus returned no same-experiment
  claims, findings, or explicit references for `Mitf`.
- Distributed Agents Runtime profile analysis:
  `profile_compare` on selected observed focal signatures, with
  `gene_target` as the entity, measured `names` as features, `logfoldchanges`
  as signed values, and `pvals_adj < 0.05` as the significance mask.
- PubMed literature for MITF and MiT/TFE biology:
  - Cheli, Ohanna, Ballotti, and Bertolotto 2009, PMID 19995375,
    DOI 10.1111/j.1755-148X.2009.00653.x: MITF target genes in melanocytes,
    osteoclasts, and mast cells.
  - Hershey and Fisher 2004, PMID 15050900,
    DOI 10.1016/j.bone.2003.08.014: MITF and TFE3 as bHLH-Zip factors with
    essential osteoclast functions.
  - Martina, Diab, Li, and Puertollano 2014, PMID 24477476,
    DOI 10.1007/s00018-014-1565-8: MiT/TFE family members MITF, TFEB, TFE3,
    and TFEC in organelle biogenesis, nutrient sensing, and energy homeostasis.
  - Roczniak-Ferguson et al. 2012, PMID 22692423,
    DOI 10.1126/scisignal.2002790: mTORC1 phosphorylation controls TFEB and
    related MITF/TFE3 cytosolic retention and lysosomal stress responses.
  - Wan, Hu, and He 2011, PMID 21519923,
    DOI 10.1007/s11010-011-0823-4: SOX10, PAX3, CREB, STAT3/PIAS3, LEF1, and
    FOXD3 regulation of melanocytic MITF.
  - Shibahara et al. 2001, PMID 11764295,
    DOI 10.1046/j.0022-202x.2001.00010.x: MITF isoforms and melanocyte-lineage
    promoter regulation by PAX3, SOX10, CREB, and Wnt/LEF1.

## Same-assay calibration

The requested manifest is:

| target | requested? |
|---|---:|
| Mitf | yes |

The focal training-count table has 1,674 observed perturbations.  It is very
sparse in this cell group:

| statistic | value |
|---|---:|
| median `n_degs` | 0 |
| 75th percentile | 1 |
| mean | 14.05 |
| maximum | 2,677 |
| zero-count perturbations | 1,205 / 1,674 |

I then checked the training genes closest to MITF biology.  The direct MiT/TFE
paralogs `Tfe3`, `Tfeb`, and `Tfec` were absent from the training-count table,
as was the held-out `Mitf`, so no direct paralog knockout was available.  The
nearest observed one-step regulators and pathway controls in
`151 TH Prkcd Grin2c Glut` were:

| training perturbation | observed `n_degs` | relation to Mitf |
|---|---:|---|
| `Pax3` | 0 | melanocyte MITF promoter activator |
| `Sox10` | 0 | melanocyte MITF promoter activator |
| `Creb1` | 10 | cAMP-responsive activator of MITF expression in melanocytes |
| `Kit` | 0 | receptor upstream of melanocytic MAPK/MITF signaling |
| `Braf` | 4 | MAPK-pathway regulator of MITF phosphorylation/activity |
| `Raf1` | 0 | MAPK-pathway RAF paralog |
| `Mapk1` | 0 | ERK2/MAPK arm that can regulate MITF post-translationally |
| `Stat3` | 0 | reported MITF interactor/regulator in mast-cell literature |
| `Mtor` | 2 | kinase that controls TFEB/TFE3/MITF cytosolic retention |
| `Rptor` | 0 | mTORC1 scaffold |
| `Tsc2` | 86 | mTORC1 negative regulator; boundary, not MITF-loss analog |
| `Atg5` | 0 | autophagy component upstream of MiT/TFE activation in some stress states |
| `Atg16l1` | 0 | autophagy/noncanonical autophagy component |
| `Lamp2` | 0 | lysosomal membrane gene and MiT/TFE target readout |
| `Ctsb` | 1 | lysosomal cathepsin; self row was the only focal DEG |
| `Rab27a` | 0 | melanosome and exocytic trafficking GTPase |
| `Rab7` | 501 | broad late-endosome/lysosome trafficking boundary case |

For the selected profile cohort containing melanocytic MITF regulators,
MAPK/mTOR/lysosome genes, and bHLH transcription-factor controls, Distributed Agents
Runtime found all 19 requested training profiles and assigned response breadths
of 13 profiles with no significant features, 3 with 1-9 significant features,
1 with 10-49, and only 2 with at least 50.  `Pax3` and `Sox10`, the most
recognizable melanocyte MITF transcriptional inputs present in training, had
zero significant genes in the focal signature.  `Braf` had four significant
genes (`Atp2a2`, `Ptpn5`, `Vgf`, `Unc13a`), `Mtor` had two (`Rims3`, `Tmed8`),
and `Creb1` had ten, a small and idiosyncratic response that included its own
row and the CREB-family transcript `Crem`.

I also scanned all 1,674 focal signatures for measured MITF/MiT-TFE and
lysosomal readout genes:

| measured feature | signatures where feature was FDR-significant |
|---|---:|
| `Mitf` | 0 |
| `Tfe3` | 1 |
| `Tfeb` | 1 |
| `Tfec` | 0 |
| `Tyr` | 0 |
| `Dct` | 0 |
| `Tyrp1` | 0 |
| `Lamp1` | 4 |
| `Lamp2` | 7 |
| `Mcoln1` | 2 |

`Tfe3` and `Tfeb` only appeared as significant downstream features in broad
stress signatures (`Psmb4` and `Zbtb7a` respectively), not in a coherent
MiT/TFE pathway module.  The canonical melanocyte pigment genes were never
significant features in the focal cell type.

## Target-specific rationale

### Mitf

MITF is a MiT/TFE bHLH-Zip transcription factor.  The strongest established
loss-of-function phenotypes and direct transcriptional programs are in
melanocytes, retinal pigment epithelium, mast cells, and osteoclasts, where
MITF regulates lineage and effector genes such as pigmentation and osteoclast
functional targets.  It is also related to TFEB/TFE3/TFEC-dependent lysosomal
and autophagy gene regulation, especially in nutrient or lysosomal stress
contexts.  Those facts made me look for three classes of analogs in the
training data.

First, direct family analogs would have been `Tfe3`, `Tfeb`, and `Tfec`.
None was observed as a perturbation in the focal training set, so I did not
extrapolate from a same-family knockout count.  I did check whether their
transcripts or `Mitf` itself behaved as downstream focal readouts; `Mitf` and
`Tfec` were never FDR-significant in any of the 1,674 observed signatures,
whereas `Tfe3` and `Tfeb` were each hit once under unrelated high-response
perturbations.  This is weak evidence, but it argues against an active focal
MiT/TFE module being repeatedly engaged in the training experiment.

Second, the melanocytic MITF regulator lane was nearly all zero.  `Pax3` and
`Sox10` each produced 0 DEGs, `Kit` produced 0, and `Stat3` produced 0.
`Creb1` was not zero but had only 10 DEGs out of 17,259 tested genes.  Because
PAX3/SOX10/CREB/c-KIT biology is cell-type-specific and centered on melanocyte
MITF promoters or MITF phosphorylation, the zero responses of `Pax3`, `Sox10`,
and `Kit` in thalamic glutamatergic neurons are more relevant than CREB's small
generic transcriptional effect.

Third, the lysosomal and mTOR counterexamples did not support a high count for
`Mitf`.  `Mtor` loss caused only 2 DEGs and `Rptor`, `Atg5`, `Atg16l1`,
`Lamp2`, and `Rab27a` all caused 0.  `Rab7` caused a clear broad lysosomal
state with 501 DEGs, including `Atp6v1b2`, `Lamp2`, `Mcoln1`, `Sqstm1`,
`Flcn`, `Grn`, and multiple cholesterol/sterol genes, and `Tsc2` caused a
smaller mTORC1/metabolic state with 86 DEGs.  I treated these as boundaries:
they show that this cell type can respond to strong endolysosomal disruption,
but `Rab7` controls late endosomal trafficking directly and `Tsc2` loss
activates mTORC1 rather than removing a MiT/TFE transcription factor.  They are
therefore not clean analogs for a single, sparsely perturbed `Mitf` knockout in
a neuronal cell type.

Putting those lanes together, the within-dataset evidence is dominated by
zero-count perturbations at the closest observed melanocyte MITF inputs and by
zero-to-two counts at the closest mTORC1/lysosome nodes.  The nonzero
counterexamples reflect broad vesicle trafficking or mTORC1 imbalance rather
than MITF loss.  Given the focal cell group's high zero rate and the absence of
training perturbations for the other MiT/TFE transcription factors, I predict
that held-out `Mitf` will not cross the FDR 0.05 threshold for any measured
gene in this assay.

Prediction: `Mitf` -> `0`.

## Limits

- The best direct analogs, `Tfe3`, `Tfeb`, and `Tfec`, were absent from the
  training perturbation universe, so the prediction is one-step extrapolation
  from regulators and adjacent pathways.
- MITF can regulate autophagy and lysosome genes in stressed cultured cells and
  other lineages; a thalamic glutamatergic neuron AAV-CRISPR assay may not
  expose that state.
- The experiment is sparse and mosaic, with modest average target RNA
  downregulation.  A true weak `Mitf` effect could exist below Wilcoxon/BH
  detection even if the correct point prediction for this endpoint is zero.
- Raw all-gene signature correlations among very small-response perturbations
  were dominated by nonsignificant background features, so I used FDR-passing
  genes and mechanistic direction as the primary evidence.
