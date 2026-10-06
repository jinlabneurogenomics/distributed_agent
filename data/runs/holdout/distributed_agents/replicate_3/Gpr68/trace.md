# Prediction task

The held-out target list for this run contains one perturbation, `Gpr68`. I
interpreted the requested endpoint as the exact focal-class count of genes with
`pvals_adj < 0.05` in `151 TH Prkcd Grin2c Glut` after sparse postnatal CRISPR
loss of the target, with the count including a possible self-target transcript
if the perturbed gene itself passed FDR.

The main ambiguity I resolved was how to use receptor family information for an
orphan/proton-sensing GPCR. I did not treat "GPCR" membership alone as an
analog. GPR68 is a proton-sensing OGR1-family receptor whose acid response
couples to Gq/11 and inositol-phosphate/Ca2+ signaling, so I emphasized
training perturbations in the assayed Gq/PLC/PKC and neuromodulatory receptor
lanes rather than all receptor-like genes.

# Sources

- Direct training counts:
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
- Direct DE profiles:
  `[local file: training_de_all_cell_groups.parquet]`,
  filtered to `group_name == "151 TH Prkcd Grin2c Glut"`.
- Distributed Agents same-experiment corpus release
  `perturbai-july-260713-sourceguard-1773-v1`.
  This release had no target-scoped record for `Gpr68`; I used it for
  same-experiment claims about represented GPCR and second-messenger targets,
  especially:
  - `claim:9f69c85a0a28574c603c`: represented neuromodulatory GPCR,
    Gq/PLC/Ca2+/PKC/MAPK, cAMP/GIRK, and related effector perturbations
    generally fail to form a shared basal neuronal nuclear-transcriptome module.
  - `claim:e7bcf5f67cb9b3fcf6d2`: represented serotonin receptor hits are
    sparse and receptor/cell-context specific rather than a family-level or
    G-protein/PLC-level output.
  - `claim:5778f7e46773642bd0bd`: represented dopamine/GPCR and cAMP-pathway
    perturbations do not collapse into one shared durable basal neuronal mRNA
    module.
  - `claim:944ca6185dd70e5a895c`: represented Gbeta5/R7-adjacent GPCR/RGS/GIRK
    targets are largely uncoupled from a common downstream transcriptomic
    program.
- External receptor biology: Ludwig et al., 2003, "Proton-sensing
  G-protein-coupled receptors", Nature, DOI `10.1038/nature01905`, PMID
  `12955148`. This study established OGR1/GPR68 as a proton-sensing GPCR and
  linked acid activation of OGR1 to Gq/11-dependent inositol-phosphate/Ca2+
  signaling.

# Computation

I first loaded the 1,674 non-held-out focal-class DEG counts to calibrate the
scale of this endpoint. The distribution is extremely zero-heavy:

- 1,205 / 1,674 training perturbations have `n_degs = 0`.
- The median is 0, the 75th percentile is 1, the 90th percentile is 2, the 95th
  percentile is 18, and the maximum is 2,677.

I then made a focal-class profile comparison over 22 training perturbations that
were mechanistically plausible analogs or counterexamples for a GPCR signal:

```text
Gpr158, Gpr161, Gpr179, Gprc5b,
Chrm3, Htr2a, Htr2b, Htr2c, Grm5,
Gnas, Gnao1, Gnb5, Plcb1, Prkca, Prkcg,
Adrb2, Adrb3, Cnr1, Glp1r, Npsr1, Pth1r, Sstr5
```

For these 22 targets I filtered the Parquet to the focal cell group and directly
recounted `pvals_adj < 0.05` over the 17,259 measured genes per target. This
reproduced the relevant entries of the training-count CSV and separated
self-target singleton hits from downstream signatures:

| training target | focal `n_degs` | FDR genes, if any |
| --- | ---: | --- |
| `Gpr158` | 1 | `Gpr158` |
| `Gpr161` | 0 | none |
| `Gpr179` | 0 | none |
| `Gprc5b` | 0 | none |
| `Chrm3` | 0 | none |
| `Htr2a` | 0 | none |
| `Htr2b` | 0 | none |
| `Htr2c` | 0 | none |
| `Grm5` | 0 | none |
| `Gnas` | 0 | none |
| `Gnao1` | 1 | `Gnao1` |
| `Gnb5` | 0 | none |
| `Plcb1` | 0 | none |
| `Prkca` | 0 | none |
| `Prkcg` | 1 | `Prkcg` |
| `Adrb2` | 0 | none |
| `Adrb3` | 0 | none |
| `Cnr1` | 1 | `Srcap` |
| `Glp1r` | 0 | none |
| `Npsr1` | 0 | none |
| `Pth1r` | 0 | none |
| `Sstr5` | 0 | none |

The runtime profile comparison over the same 22 profiles found 18 with no
significant feature and 4 in the `1_to_9_significant_features` bin. In the 50
projected pairs involving `Gpr158`, `Gpr161`, `Gpr179`, `Htr2a`, and `Chrm3`
against G-protein/PLC/PKC and Gq-like receptor peers, no pair shared a
positive or negative FDR-significant gene. Whole-profile Pearson correlations
across all 231 GPCR/cofactor pairs had a tight background-like distribution
(mean 0.669, standard deviation 0.016; 5th to 95th percentile 0.640 to 0.692),
so I did not interpret raw log-fold-change correlation alone as evidence for a
biological shared module.

# Target-specific reasoning

## Gpr68

External mechanism:

`Gpr68`, also known as `Ogr1`, is not just a generic adhesion or sensory-family
gene; it encodes a proton-sensing GPCR whose acid-evoked signaling can proceed
through Gq/11 to inositol phosphate and intracellular Ca2+ mobilization
(Ludwig et al. 2003, DOI `10.1038/nature01905`, PMID `12955148`). That makes
`Plcb1`, `Prkca`, and `Prkcg` mechanistically closer than unrelated GPCRs, and
Gq-linked receptors such as `Chrm3`, `Htr2a`, `Htr2b`, `Htr2c`, and `Grm5`
useful counterexamples for whether a persistent Gq/PLC transcriptional program
is visible in this assay.

Training perturbations compared:

- `Plcb1`, the most direct represented PLC effector in the same broad pathway,
  had 0 focal DEGs. The Distributed Agents corpus also records that sparse postnatal
  `Plcb1` loss did not produce a sustained activity-regulated immediate-early
  state and that metabotropic glutamate receptor/PLC/IP3/PKC perturbations did
  not form a robust shared basal module.
- `Prkca` and `Prkcg`, downstream PKC genes, had 0 and 1 focal DEG,
  respectively; the lone `Prkcg` hit was `Prkcg` itself, so this did not
  provide evidence for a propagated GPR68-like downstream response.
- `Gnas`, `Gnao1`, and `Gnb5` had 0, 1, and 0 focal DEGs. As with `Prkcg`, the
  `Gnao1` singleton was the targeted transcript itself. These were treated as
  second-messenger counterexamples rather than close GPR68 analogs because the
  canonical GPR68 acid response is Gq/11-linked, not a simple Gs or Gi/o
  perturbation.
- `Chrm3`, `Htr2a`, `Htr2b`, `Htr2c`, and `Grm5` are represented
  neuromodulatory/classical GPCR routes into Gq/PLC signaling. All five had
  zero focal DEGs, and the same-experiment corpus specifically cautioned that
  represented serotonin, metabotropic glutamate, muscarinic, and PLC-adjacent
  perturbations were flat or receptor-specific rather than a shared basal
  Gq/PLC module.
- Other focal GPCR counterexamples were also flat: `Adrb2`, `Adrb3`, `Glp1r`,
  `Pth1r`, `Npsr1`, and `Sstr5` each had 0 focal DEGs. `Cnr1` had a single
  non-self hit, `Srcap`, but did not define a broad response.
- Training orphan/ciliary GPCR-family members were not close paralogs of GPR68,
  but they gave a family-level null check: `Gpr161`, `Gpr179`, and `Gprc5b`
  each had 0 focal DEGs and `Gpr158` had one self-target DEG.

Zero/nonzero decision:

The within-dataset evidence points to a zero or at most singleton outcome.
There is no GPR68 vector in the same experiment, no assayed GPR68-specific
partner, and no proton-sensing GPCR family member among the non-held-out
training perturbations. However, every available Gq/PLC/PKC receptor or
proximal effector analog in the focal group was an FDR null except for
self-target singleton cases. Because the readout was a single unstimulated
basal snRNA-seq endpoint 3-4 weeks after perturbation, an acid-evoked
GPR68/Ca2+ biochemical function is not by itself expected to become a durable
multi-gene nuclear RNA signature.

I therefore predicted `Gpr68` as a focal-class null and assigned
`predicted_n_degs = 0`.

# Limits

- The key extrapolation is that no non-held-out training perturbation is a true
  proton-sensing OGR1-family paralog of `Gpr68`; `Gpr4`, `Gpr65`, and `Gpr132`
  were absent from the focal training-count table.
- Gq/PLC/PKC genes and other Gq-coupled receptors are biochemical analogs, not
  genetic paralogs, and they may be expressed or wired differently in
  `151 TH Prkcd Grin2c Glut` neurons.
- The assay measured basal recovered nuclei and did not impose extracellular
  acidification, ligand stimulation, calcium imaging, membrane excitability
  measurements, or protein-localization readouts. A genuine GPR68 proton
  response could therefore be missed by this endpoint.
- The few singleton GPCR/cofactor DEG counts show that target-transcript loss
  can occasionally push `n_degs` from 0 to 1. The supplied experimental
  calibration warns that self-transcript knockdown is not a reliable editing
  or activity proxy, so I did not add one DEG to the prediction solely for a
  possible `Gpr68` self hit.
- Whole-profile log-fold-change correlations in this sparse low-count cohort
  had a common positive background across almost every pair. I used absence of
  FDR-supported overlap and the exact DEG counts as the quantitative anchors,
  not the absolute Pearson value as a stand-alone biological similarity score.
