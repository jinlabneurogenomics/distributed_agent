# Direct Fth1 forecast

## Target and endpoint

- Target: `Fth1`
- Focal population: `151 TH Prkcd Grin2c Glut`
- Endpoint: `n_degs`, the count of measured genes with BH-adjusted Wilcoxon `p < 0.05`
- Prediction: `0`

The one-row holdout manifest names `Fth1`. The declared training Parquet contains no
`gene_target = 'Fth1'` rows, and I did not use a target expression signature or target
DEG count.

## Biology bearing

The canonical `Fth1` biology bundle supports target reach but not a high-burden
neuronal stress response:

- FTH1 is the ferroxidase subunit of the assembled 24-subunit ferritin iron-storage
  shell, so a successful disruptive edit is expected to stop production of new
  functional FTH1.
- Pre-existing ferritin particles and stored iron are already installed at P16; the
  bundle nevertheless judged substantial FTH1 functional-stock decline plausible by the
  P37-P44 harvest because ferritin is a renewable lysosomal substrate.
- Exact in-assay reach is present but modest: in non-target `151 TH Prkcd Grin2c Glut`
  nuclei, `Fth1` is detected in 17,566 of 23,679 nuclei, with mean CP10K 1.0016 and
  mean raw UMI 1.6569.
- The prior neural phenotypes transfer weakly to this endpoint: the closest postnatal
  loss-of-function evidence is oligodendroglial rather than NeuN-positive thalamic
  neuronal, FTL1-containing ferritin shells could buffer partial heavy-chain loss, and
  survivor conditioning is unresolved.

That makes within-window engagement plausible, but it keeps the assay projection closer
to a low iron/redox response than to the large unfolded-protein, proteasome, or RNA-
processing signatures in this cell class.

## Training measurements used

The focal count table contains 1,674 training perturbations. Its median `n_degs` is 0,
the 75th percentile is 1, and only 469 / 1,674 perturbations are nonzero in this class.

Curated iron-homeostasis and ferroptosis sets from the deterministic annotation store
were almost entirely flat in the focal count table:

- WikiPathways `WP_IRON_HOMEOSTASIS`: `Hjv` 0, `Il6ra` 0, `Ireb2` 1
- KEGG ferroptosis: `Acsl4` 1, `Atg5` 0, `Gclc` 0, `Gclm` 1, `Gpx4` 0,
  `Map1lc3a` 1, `Prnp` 1, `Tfrc` 0, `Trp53` 0
- GO intracellular iron-ion homeostasis: `Abcb7` 0, `Acvr2b` 0, `Atp13a2` 1,
  `Atp6v1a` 0, `Bmpr1a` 0, `Hif1a` 0, `Hjv` 0, `Ireb2` 1, `Mecr` 0, `Neo1` 0,
  `Smad1` 0, `Smad4` 0, `Smad9` 0, `Tfrc` 0
- Reactome iron uptake and transport: `Atp6v0a1` 1, `Atp6v1a` 0, `Atp6v1b2` 0,
  `Atp6v1e1` 0, `Flvcr1` 0, `Ireb2` 1, `Slc22a17` 1, `Tfrc` 0

Several direct or stress-adjacent comparators had ordinary recovered perturbed-cell
counts in `151 TH Prkcd Grin2c Glut` yet remained quiet in the Parquet:

| target | `n_degs` | matched perturbed nuclei |
|---|---:|---:|
| `Tfrc` | 0 | 123 |
| `Ireb2` | 1 | 206 |
| `Gpx4` | 0 | 143 |
| `Nfe2l2` | 0 | 207 |
| `Abcb7` | 0 | 120 |
| `Aco2` | 0 | 154 |
| `Nfs1` | 0 | 181 |
| `Atf6` | 0 | 177 |
| `Park7` | 1 | 221 |

The only stronger stress reference I retained was `Hspa5`, an ER-folding/UPR
perturbation with 5 focal DEGs at FDR < 0.05 from only 47 matched perturbed nuclei.
It shows that this thalamic class can report a small stress module, but its proximal
operation is ER chaperoning rather than ferritin iron storage.

## Profile and corpus checks

An observed-profile comparison of 21 training perturbations from iron-homeostasis,
ferroptosis, antioxidant, HIF, and iron-transport annotations found 14 nodes with no
FDR < 0.05 features and 7 nodes with only 1-9 features. Across all 210 cohort pairs,
the median positive and negative top-tail overlaps were both 0.025, and the cohort had
no positive significant-program overlap and zero negative significant-program overlap.
The focal `Tfrc`, `Ireb2`, `Gpx4`, `Nfe2l2`, and `Hif1a` profiles had either zero or one
significant features and only near-zero pairwise cosines to other curated peers.

Same-experiment corpus Findings for the training anchors gave the same interpretation
without serving as independent replication: `Gpx4` was pan-null across recovered
neuronal groups with no ferroptosis/NRF2/glutathione/iron/ISR induction; `Nfe2l2` was
flat across its measured neuronal groups; `Abcb7`, `Aco2`, and `Nfs1` lacked the
expected Fe-S, mitochondrial, OXPHOS, iron-heme, and secondary stress programs; and
`Ireb2` had only a single robust focal event rather than an iron-homeostatic mRNA
program.

## Synthesis

`Fth1` expression in the focal population and likely ferritin-particle renewal argue
against treating the edit as biologically unreachable. The magnitude-bearing training
evidence points the other way for this endpoint: perturbing measured iron uptake,
iron sensing, Fe-S/mitochondrial, ferroptosis, and NRF2 nodes produced zero or one
focal DEG, and their signed profiles did not assemble into a recurrent multi-gene
program. Given FTH1's residual installed ferritin stock, possible FTL1 buffering, low
neuronal demand relative to oligodendroglia, and the silent measured iron/redox
comparators, the best integer point is a flat recovered-nucleus signature.
