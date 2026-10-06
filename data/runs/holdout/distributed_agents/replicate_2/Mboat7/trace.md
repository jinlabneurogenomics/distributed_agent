# Trace

## Question and resolved ambiguities

The held-out target list for this run is the single perturbation `Mboat7`. I
interpreted the task as asking for the `151 TH Prkcd Grin2c Glut` endpoint used
in the supplied training CSV: the number of measured genes with
Benjamini-Hochberg-adjusted Wilcoxon `pvals_adj < 0.05`.

The count is assay-calibrated and can include the knocked-out target transcript
itself when that transcript is measured and passes FDR. I used the training
count CSV as the scalar ground truth and used the parquet only to inspect focal
cell expression signatures and individual genes supporting each scalar count.

## Sources

Internal experiment sources:

- `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`, the focal training
  `n_degs` table for 1,674 non-held-out perturbations.
- `training_de_all_cell_groups.parquet`, filtered primarily to
  `group_name == "151 TH Prkcd Grin2c Glut"`.
- `133_Mboat7.csv`, which contains exactly one requested target, `Mboat7`.
- Distributed Agents corpus release `perturbai-july-260713-sourceguard-1773-v1`.
  `Mboat7` had no direct corpus card, so I used corpus findings for represented
  phosphatidylinositol, phosphoinositide, arachidonoyl, and membrane-lipid
  comparators such as `Acsl4`, `Dgke`, `Pi4kb`, `Synj1`, and `Inpp5k`.
- Distributed Agents runtime profile tools over the focal parquet, with
  `logfoldchanges` as the signed profile value, `pvals_adj` as the significance
  field, and the 1,674 training genes as the eligible universe.

External biological sources:

- Gijon et al. 2008, JBC, PMID:18772128, DOI:10.1074/jbc.M806194200:
  MBOAT7/LPIAT1 is a lysophosphatidylinositol acyltransferase with strong
  arachidonoyl-CoA preference.
- Lee et al. 2012, Molecular Biology of the Cell, PMID:23097495,
  DOI:10.1091/mbc.E12-09-0673: LPIAT1/MBOAT7 maintains arachidonic-acid
  content in phosphatidylinositol and PI phosphates and is required for mouse
  cortical lamination.
- Anderson et al. 2013, PLoS ONE, PMID:23472195,
  DOI:10.1371/journal.pone.0058425: LPIAT1 knockout reduces C38:4 PtdIns and
  PtdInsP2 and increases lyso-PtdIns in mouse brain and liver.
- Johansen et al. 2016, American Journal of Human Genetics, PMID:27616480,
  DOI:10.1016/j.ajhg.2016.07.019: biallelic inactivating `MBOAT7` variants
  cause intellectual disability with epilepsy and autistic features.
- Caddeo et al. 2021, BBA Molecular and Cell Biology of Lipids,
  PMID:33513444, DOI:10.1016/j.bbalip.2021.158891: human MBOAT7 transfers
  polyunsaturated fatty acids preferentially to lysophosphatidylinositol and
  requires its catalytic residues for acyltransferase activity.
- Tang et al. 2025, Science Translational Medicine, PMID:39742503,
  DOI:10.1126/scitranslmed.adp5247: Mboat7 loss in developmental models alters
  the PI-associated glycerolipidome, increases lysophosphatidylinositol, and
  links the migration phenotype to mTOR signaling.
- Epand et al. 2016, Frontiers in Cell and Developmental Biology,
  PMID:27803897, DOI:10.3389/fcell.2016.00112; Lung et al. 2009, JBC,
  PMID:19744926, DOI:10.1074/jbc.M109.050617: DGKepsilon/DGKE is selective for
  arachidonoyl-containing DAG species in the phosphatidylinositol cycle.

## Dataset computations

1. I read `133_Mboat7.csv` and confirmed the only held-out target was
   `Mboat7`.
2. I read the focal training count CSV and summarized the scalar endpoint. The
   distribution is sparse: 1,205/1,674 targets have `n_degs = 0`, 363 have
   1-9, 63 have 10-99, and 43 have at least 100. The median is 0 and the 75th
   percentile is 1.
3. I searched the training universe for phosphatidylinositol, PI-phosphate,
   DAG/PLC, arachidonoyl, endocytic phosphatase, and related lipid genes. The
   represented focal counts were:

   | analog | focal n_degs | why inspected |
   | --- | ---: | --- |
   | `Acsl4` | 1 | arachidonoyl-CoA synthetase; supplies 20:4-CoA that MBOAT7 uses |
   | `Dgke` | 1 | DGKepsilon acts on stearoyl-arachidonoyl DAG in the PI cycle |
   | `Abhd12` | 1 | arachidonoyl/endocannabinoid/lysophospholipid enzyme; weaker pathway match |
   | `Pi4kb` | 1 | PI 4-kinase feeding PI4P and downstream PIPs |
   | `Synj1` | 1 | PI(4,5)P2 phosphatase in synaptic-vesicle endocytosis |
   | `Pld3` | 1 | lexical phospholipase hit but not a mechanistic PI-remodeling comparator |
   | `Inpp5k` | 0 | inositol polyphosphate 5-phosphatase |
   | `Ocrl` | 0 | PI(4,5)P2 5-phosphatase |
   | `Plcb1` | 0 | PI(4,5)P2 phospholipase C beta |
   | `Pik3cb` | 0 | class I PI3K catalytic subunit |
   | `Pik3r1` | 0 | PI3K regulatory subunit |
   | `Pik3r2` | 0 | PI3K regulatory subunit |
   | `Ppip5k2` | 0 | inositol pyrophosphate kinase/phosphatase |

4. I filtered the parquet to the focal cell group and the most relevant lipid
   analogs, then counted rows with `pvals_adj < 0.05`. `Acsl4`, `Dgke`,
   `Abhd12`, and `Synj1` were singleton self-transcript hits in this cell group:
   `Acsl4` log2FC = -0.995, adjusted p = 3.83e-16; `Dgke` log2FC = -0.586,
   adjusted p = 5.97e-08; `Abhd12` log2FC = -0.846, adjusted p = 3.40e-22;
   `Synj1` log2FC = -0.583, adjusted p = 3.11e-07. Their next-best focal genes
   were not significant.
5. `Pi4kb` was the one phosphoinositide analog with a non-self focal downstream
   hit: `Tmem50b`, log2FC = 0.426, adjusted p = 0.028; `Rnf145` was next, at
   adjusted p = 0.069. The same-experiment corpus interprets this as a tiny
   endomembrane/sterol-E3 compensation pair, not a broad PI4P or stress
   signature.
6. I ran focal `profile_neighbors` and `profile_compare` on `Acsl4`, `Dgke`,
   `Pik3cb`, `Pik3r1`, `Pik3r2`, `Inpp5k`, `Ppip5k2`, and `Abhd12`, comparing
   signed `logfoldchanges` over measured genes against the 1,674 eligible
   training targets. Five of the eight anchors were entirely FDR-silent and
   three had only 1-9 significant rows. The nearest-neighbor lists put `Pi4kb`
   among the top whole-logFC neighbors of both `Acsl4` and `Dgke`, which was a
   useful prompt to inspect `Pi4kb`, but the FDR-level evidence remained in the
   zero/singleton regime. Because flat logFC profiles can share pseudocount
   artifacts, I used these neighbor lists for discovery only, not as a
   quantitative weight.
7. I also checked that `Mboat7` is a measured gene in the focal profiles for all
   1,674 training perturbations. Thus a held-out `Mboat7` profile could score
   as `n_degs = 1` through its own mRNA depletion, as many nearby training
   perturbations do.

## Mboat7-specific reasoning

MBOAT7/LPIAT1 is the direct acyltransferase that reacylates lyso-PI with
arachidonoyl-CoA. It sits on the Lands-cycle side of the same arachidonoyl-PI
chemistry touched by `Acsl4`, which makes the acyl-CoA substrate, and `Dgke`,
which phosphorylates arachidonoyl-containing DAG in the PI turnover cycle.
Germline or developmental Mboat7/Lpiat1 loss is clearly not benign: mouse
Lpiat1 deficiency depletes 20:4-containing PI/PIP species and disrupts cortical
lamination, and human biallelic `MBOAT7` variants cause a recessive
neurodevelopmental syndrome with intellectual disability, seizures, and autistic
features.

Those external facts raise the prior that a complete developmental knockout can
matter for neurons, but they do not imply a broad acute nuclear RNA signature
in this experiment. The assay edited sparse postmitotic P16 neurons, sampled
surviving NeuN-positive nuclei three to four weeks later, and did not measure
PI species, lyso-PI accumulation, mTOR activity, endocannabinoids, calcium
oscillation, synaptic physiology, migration, or cortical layering. The closest
within-dataset chemistry therefore carries more weight for `n_degs` than the
severity of a germline brain phenotype.

The key internal analogs all point to a tiny response:

- `Acsl4` is the most relevant substrate-side comparator. Its focal count was
  exactly 1, entirely `Acsl4` self-transcript depletion. The corpus further
  records that basal `Acsl4` loss did not phenocopy GPX4/NRF2/iron-uptake
  ferroptosis-axis perturbations and that its screen-visible response was
  largely isolated.
- `Dgke` is the PI-cycle DAG comparator. Its focal count was exactly 1, also a
  self-transcript hit. The corpus calls `Dgke` a buffered RNA phenotype with no
  robust steady-state downstream output across recovered neuronal classes, and
  notes that represented PI-cycle/DAG/PKC comparators such as `Plcb1` and
  `Prkca` did not phenocopy it.
- `Pi4kb` is not an acyl-chain remodeler, but it is the represented PI kinase
  nearest to production of PI4P and downstream PIPs. In the focal group it had
  one FDR<0.05 gene, `Tmem50b`; `Rnf145` just missed the cutoff. This is the
  only plausible non-self positive counterexample, and it is still a singleton,
  not a medium-width response.
- `Synj1`, `Ocrl`, `Inpp5k`, `Plcb1`, `Pik3cb`, `Pik3r1`, `Pik3r2`, and
  `Ppip5k2` bound the phosphoinositide pathway on the other side. In the focal
  endpoint, `Synj1` had only its own transcript and the rest had zero genes.
  Same-experiment claims for `Synj1`/`Ocrl`/`Inpp5k` explicitly warn that
  represented membrane-associated phosphoinositide and endocytic genes did not
  collapse into a shared neuronal RNA module in this assay.
- `Abhd12` is a weaker arachidonoyl-lipid comparator and also had only a
  self-transcript singleton. I treated it as supportive of "lipid enzymes can
  be edited yet RNA-flat" rather than as a direct MBOAT7 analog.

Putting those together, I expect acute `Mboat7` loss to alter local PI
remodeling, but the represented PI and arachidonoyl-lipid perturbations almost
never drove more than one FDR<0.05 gene in `151 TH Prkcd Grin2c Glut`.
Because `Mboat7` is itself measured and because the nearest enzyme comparators
often entered the endpoint solely through self-transcript depletion, the better
point prediction is a singleton rather than a hard zero.

Prediction: `Mboat7`, `predicted_n_degs = 1`.

## Limits and extrapolations

- `Mboat7` itself was held out and had no direct Distributed Agents corpus context in
  release `perturbai-july-260713-sourceguard-1773-v1`.
- No close MBOAT-family paralog or ACBD3/Rab11/ARF PI4KB recruiter was present
  as a focal training perturbation, so the comparison relies on pathway-neighbor
  genes rather than a one-complex phenocopy.
- The predicted singleton depends on the target transcript passing FDR. Several
  analogs did so, but measured mRNA depletion is not guaranteed for every AAV
  CRISPR target and is not a quantitative readout of indel burden.
- Published Lpiat1/Mboat7 knockout phenotypes are often germline or
  developmental and include migration and lipidomic effects outside this
  postmitotic snRNA endpoint. They justify biochemical relevance, but the final
  scalar is driven mainly by within-experiment lipid-gene flatness.
- The parquet reports nuclear RNA only. A prediction of one DEG does not imply
  absence of altered PI/PIP species, lyso-PI, calcium signaling, mTOR signaling,
  synaptic transmission, survival selection, or morphology.
