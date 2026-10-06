# DEG-count prediction trace

## Question and resolved ambiguities

The requested endpoint is the number of measured genes with `pvals_adj < 0.05`
after each held-out perturbation in `151 TH Prkcd Grin2c Glut` cells.
The run manifest contains one target:

```text
Arnt2
```

`Arnt2` was not present as a perturbation in the differential-expression
parquet or in the focal training-count CSV, so there is no direct observed
`Arnt2` expression profile. A prediction of `0` means I expect no measured gene
to pass BH FDR 0.05 for `Arnt2` in this cell group; positive integers would be
raw counts of passing genes, not effect sizes.

## Sources used

- Input differential-expression dataset:
  `[local file: training_de_all_cell_groups.parquet]`.
- Input training endpoints:
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
- Held-out manifest:
  `[local file: 017_Arnt2.csv]`.
- Distributed Agents same-experiment corpus, release
  `perturbai-july-260713-sourceguard-1773-v1`; specifically, curated Claims and
  ledger Findings for `Arnt`, `Ahr`, `Hif1a`, `Bmal1`, and related bHLH-PAS
  perturbations.
- Distributed Agents runtime `profile_neighbors`, used to compare observed signed
  `logfoldchanges` in `151 TH Prkcd Grin2c Glut` for `Arnt`, `Ahr`, `Hif1a`,
  `Npas3`, `Bmal1`, and `Clock` against the complete 1,674-perturbation
  eligible training universe.
- PubMed literature retrieved through NCBI PubMed E-utilities:
  Hirose et al. 1996, DOI `10.1128/MCB.16.4.1706`, PMID `8657146`;
  Hosoya et al. 2001, DOI `10.1046/j.1365-2443.2001.00421.x`, PMID
  `11318878`; Keith et al. 2001, DOI `10.1073/pnas.121494298`, PMID
  `11381139`; Hao et al. 2013, DOI `10.1093/nar/gkt206`, PMID `23599003`;
  Sharma et al. 2019, DOI `10.1016/j.neuron.2019.02.007`, PMID `30846309`;
  Turer et al. 2018, DOI `10.1242/dmm.035451`, PMID `30563851`.

## Dataset computations

I first read the held-out manifest and found one target, `Arnt2`. The focal
training-count CSV contains 1,674 perturbations; 469 have a nonzero DEG count
and the observed range is 0 to 2,677 genes. I then filtered the parquet to
`group_name == "151 TH Prkcd Grin2c Glut"` and to bHLH-PAS or ARNT-axis
comparators selected before seeing any held-out `Arnt2` data:

```python
f = (
    pc.field("group_name") == "151 TH Prkcd Grin2c Glut"
) & pc.field("gene_target").isin(
    ["Arnt", "Ahr", "Ahrr", "Hif1a", "Npas3", "Bmal1", "Bmal2", "Clock"]
)
```

Each selected perturbation had 17,259 measured genes in the focal group and
23,679 matched controls. The observed focal DEG counts were:

| training target | matched perturbed nuclei | observed `n_degs` |
|---|---:|---:|
| `Arnt` | 209 | 0 |
| `Ahr` | 93 | 0 |
| `Ahrr` | 159 | 0 |
| `Hif1a` | 175 | 0 |
| `Npas3` | 198 | 0 |
| `Bmal2` | 182 | 0 |
| `Clock` | 162 | 3 |
| `Bmal1` | 152 | 103 |

The profile-neighbor calculation used signed `logfoldchanges` in the same focal
cell group, `names` as features, `gene_target` as profile IDs, `pvals_adj` as
the significance column, and the full training-count CSV as the eligible
perturbation universe. Its most important output was not a positive module but
the lack of one: `Arnt`, `Ahr`, `Hif1a`, and `Npas3` each had zero significant
features in this focal group, and their top whole-profile neighbors were almost
all 0-DEG or 1-DEG perturbations. For example, the top five whole-profile
Pearson neighbors were:

| anchor | top same-experiment neighbors in `151 TH Prkcd Grin2c Glut` |
|---|---|
| `Arnt` | `Sbf2` 0, `Zfpm2` 0, `Mt3` 1, `Ptprd` 0, `Kiz` 0 |
| `Ahr` | `Ptchd1` 0, `Dnajb6` 0, `Tnrc6a` 0, `Kdm4c` 0, `Taf1b` 0 |
| `Hif1a` | `Thrb` 0, `Zfp397` 0, `Tcf12` 0, `Fgfr3` 0, `Eif4g1` 1 |
| `Npas3` | `Nsd2` 0, `Ebf2` 0, `Kiz` 0, `Ppara` 0, `Tcf12` 0 |

In contrast, the same readout can detect a bHLH-PAS transcription-factor
module when it is tonically active: `Bmal1` loss produced 103 DEGs in the focal
cell group, led by circadian outputs `Dbp`, `Nr1d2`, and `Nr1d1`; `Clock` had a
narrow but concordant 3-DEG signature with `Dbp`, `Nr1d2`, and `Tef`
significant. This makes the flat ARNT/AHR/HIF branch unlikely to be a generic
failure to recover PAS-family factors.

## Target-specific reasoning

### `Arnt2`

`Arnt2` encodes a neuronal bHLH-PAS beta-class dimerization partner related to
`Arnt`. The closest represented paralog and HIF/AHR cofactor was `Arnt` itself,
and it had `n_degs = 0` in the focal cell group. The Distributed Agents corpus records
that `Arnt` was FDR-null across all 22 recovered neuronal groups and that
canonical AHR and HIF outputs were absent after `Arnt` perturbation. The focal
data match that curated result: `Ahr`, `Ahrr`, and `Hif1a` also all had
`n_degs = 0`.

Those are mechanistically appropriate analogs for only one part of ARNT2
biology. Hirose et al. showed that mouse ARNT2 is similar to ARNT and can
interact with AHR and mouse SIM in vitro, and Keith et al. showed that ARNT2
can form functional HIF complexes and overlaps genetically with `Arnt` during
early development. In this basal postnatal screen, however, the same-experiment
ARNT/AHR/HIF axis is silent: no AHR ligand, hypoxia, or ischemia was applied,
and the directly perturbed `Arnt`, `Ahr`, `Ahrr`, and `Hif1a` nodes have zero
focal DEGs. That makes an ARNT2 effect through tonic AHR or HIF signaling
unlikely.

The best-known ARNT2-specific role is developmental rather than an acute
maintenance function in juvenile glutamatergic thalamic neurons. Hosoya et al.
reported that germline `Arnt2` knockout mice lose hypothalamic PVN/SON
neurosecretory neurons and argued for ARNT2 as an obligatory SIM1 partner in
that developmental lineage; Turer et al. later found that a hypomorphic Arnt2
mutation impairs SIM1-dependent homeostatic feeding. `Sim1`, `Sim2`, and
`Npas4` were not available as training perturbations, so this piece is an
extrapolation from literature rather than a direct same-complex transfer.
Still, the experiment perturbs postmitotic P16 neurons sparsely and reads them
3-4 weeks later, not embryonic hypothalamic specification or a germline
homeostatic-feeding circuit. The Distributed Agents `Arnt` ledger makes the same
stage/lineage point for ARNT-family genes: the screen did not reproduce
embryonic placental `Arnt` requirements or ARNT2/SIM1 hypothalamic development
phenotypes in juvenile NeuN+ neuronal mRNA.

ARNT2 also has mature-neuron biology through NPAS4. Hao et al. described a
developmental switch toward Arnt2 expression in neuronal differentiation, and
Sharma et al. showed that ARNT2 can repress activity-dependent regulatory
elements via NCoR2 at baseline and recruit NPAS4 after heightened synaptic
activity. That could, in principle, make `Arnt2` more neuronal than `Arnt`.
But the focal assay is a steady-state, unstimulated snRNA-seq endpoint. The
available represented bHLH-PAS neighbor outside AHR/HIF, `Npas3`, was also
flat in this same cell group (`n_degs = 0`), while the detectable bHLH-PAS
module was the separate CLOCK/BMAL1 clock arm (`Bmal1 = 103`, `Clock = 3`,
`Bmal2 = 0`). I therefore used `Bmal1` and `Clock` as assay-positive
counterexamples rather than as quantitative analogs for `Arnt2`.

The zero/nonzero decision is therefore driven mainly by within-dataset evidence
from the flat ARNT/AHR/HIF/Npas3 branch, with external literature used to check
whether ARNT2 has a missing partner or stimulus that should override that
branch. The missing SIM1/SIM2/NPAS4 comparators and the activity-dependent
literature keep the prediction lower-confidence than the observed `Arnt`
endpoint, but not enough to move the expected BH-significant count above zero.
My point prediction for `Arnt2` is `0`.

## Limits

- `Arnt2` itself, `Sim1`, `Sim2`, and `Npas4` were held out or unavailable as
  training perturbations, so the ARNT2/SIM and ARNT2/NPAS4 arms could not be
  tested directly in the focal dataset.
- The expression-profile neighborhood of a 0-DEG anchor is inherently noisy;
  many whole-profile similarities among flat perturbations are driven by weak
  signs and extreme low-expression features rather than a crisp biological
  program. I used those neighborhoods only to confirm absence of a hidden broad
  module.
- ARNT2 can be important in embryonic hypothalamic development, hypoxic
  responses, homeostatic feeding, and stimulated NPAS4-dependent plasticity.
  The prediction only covers acute sparse CRISPR loss in basal juvenile
  NeuN-enriched neurons in the `151 TH Prkcd Grin2c Glut` aggregate.
- The screen reports nuclear RNA and an assay- and power-dependent FDR count.
  It may miss physiology, dendritic/synaptic effects, protein turnover,
  non-cell-autonomous glial effects, or a small number of weak direct targets
  that do not pass BH 0.05.
