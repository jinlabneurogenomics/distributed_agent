# Predicting held-out DEG counts for `151 TH Prkcd Grin2c Glut`

## Question interpreted

The manifest for this run contains one held-out target:

```text
Gli3
```

For that gene I need to predict the hidden endpoint
`n_degs = count(pvals_adj < 0.05)` in the focal `151 TH Prkcd Grin2c Glut`
cell group. I treated the supplied counts CSV as the authoritative endpoint for
training targets and used the parquet only for non-held-out expression profiles.
`Gli3` itself is absent from both inputs, so the prediction must be transferred
from measured perturbations of paralogs and pathway neighbors.

The main ambiguity is that `Gli3` is a powerful embryonic Hedgehog effector, but
the assay perturbed sparse postmitotic neuronal nuclei at P16 and read out RNA
3-4 weeks later. I therefore prioritized same-assay perturbations of the
Hedgehog/GLI/ciliary pathway over germline embryonic phenotypes.

## Sources used

- `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`: training endpoint counts
  for 1,674 non-held-out perturbations in the focal cell group.
- `training_de_all_cell_groups.parquet`: focal-cell signed DE rows for measured
  Hedgehog, GLI, ciliary, and developmental comparator targets.
- Distributed Agents same-experiment corpus
  `perturbai-july-260713-sourceguard-1773-v1`: target contexts for `Gli1`,
  `Gli2`, `Ptch1`, `Smo`, and `Cdon`. `Gli3` was not present in that corpus
  release.
- PubMed literature on GLI3 and Hedgehog signaling:
  - Wang, Fallon and Beachy 2000, Cell, DOI `10.1016/s0092-8674(00)80678-9`,
    PMID `10693759`: Hedgehog-regulated GLI3 processing generates a potent
    repressor form.
  - Huangfu and Anderson 2005, PNAS, DOI `10.1073/pnas.0505328102`, PMID
    `16061793`: mouse cilia are required downstream of Smo for both GLI
    activator function and proteolytic Gli3 repressor formation.
  - Kise et al. 2009, BBRC, DOI `10.1016/j.bbrc.2009.07.087`, PMID
    `19622347`: SUFU recruits GSK3beta for efficient GLI3 processing.
  - Tole, Ragsdale and Grove 2000, Developmental Biology, DOI
    `10.1006/dbio.1999.9509`, PMID `10625551`: `Gli3` loss disrupts dorsal
    telencephalic patterning and derepresses ventral identity.
  - Rallu et al. 2002, Development, DOI `10.1242/dev.129.21.4963`, PMID
    `12397105`: Shh and Gli3 have reciprocal roles in embryonic telencephalic
    patterning.
  - Rash and Grove 2007, Journal of Neuroscience, DOI
    `10.1523/JNEUROSCI.3204-07.2007`, PMID `17959802`: GLI3 repression and
    FGF signaling shape dorsal telencephalic development.
  - Haddad-Tovolli et al. 2012, Frontiers in Neuroscience, DOI
    `10.3389/fnins.2012.00027`, PMID `22371696`: Gli activator and Gli
    repressor functions participate in mouse thalamic nuclear development.

## Computation over the training data

I loaded the requested-target manifest and confirmed that only `Gli3` needed a
prediction. The focal training-count distribution was highly zero-inflated:
median `0`, 75th percentile `1`, 95th percentile `18`, mean `14.05`, and max
`2677` DEGs. Thus a nonzero point estimate should only be used when there is
specific evidence for a recurrent response, not just because the gene has an
important developmental function.

I then filtered the parquet to the focal cell group and to a curated list of
Hedgehog/GLI/ciliary/developmental comparators:

```python
filt = (
    ds.field("group_name") == "151 TH Prkcd Grin2c Glut"
) & ds.field("gene_target").isin(targets)
```

For each comparator I counted genes with `pvals_adj < 0.10`, raw nominal hits,
matched perturbed/control nuclei, and canonical Hedgehog reporter rows
(`Gli1`, `Gli2`, `Gli3`, `Ptch1`, `Ptch2`, `Hhip`, `Shh`, `Smo`, `Rnf220`).
The direct GLI/PTCH/SMO/CDON comparators all had 0 genes even at FDR 0.10 and
none moved the expected feedback reporters at adjusted significance.

| training target | relationship to `Gli3` | n_pert / n_ctrl | observed `n_degs`, FDR 0.05 |
| --- | --- | ---: | ---: |
| `Gli1` | GLI-family Hh effector and GLI target | 234 / 23679 | 0 |
| `Gli2` | closest GLI activator paralog tested | 205 / 23679 | 0 |
| `Ptch1` | Hh receptor and canonical GLI feedback gene | 159 / 23679 | 0 |
| `Ptch2` | Hh receptor family member | 192 / 23679 | 0 |
| `Smo` | obligatory canonical signal transducer upstream of GLI proteins | 284 / 23679 | 0 |
| `Cdon` | Hh coreceptor | 190 / 23679 | 0 |
| `Gpr161` | ciliary negative regulator of Hh signaling | 187 / 23679 | 0 |
| `Ift88` | ciliogenesis / GLI processing machinery | 143 / 23679 | 0 |
| `Kif3b` | anterograde IFT motor subunit | 156 / 23679 | 0 |
| `Dync2h1` | retrograde IFT dynein-2 motor heavy chain | 98 / 23679 | 0 |
| `Dync2i1` | dynein-2 intermediate chain | 229 / 23679 | 0 |
| `Ift43` | IFT-A component | 328 / 23679 | 0 |
| `Ift81` | IFT-B component | 152 / 23679 | 0 |
| `Ttc21b` | IFT-A / retrograde trafficking | 131 / 23679 | 0 |
| `Dzip1` | basal-body/cilium Hh component | 141 / 23679 | 0 |
| `Tbc1d32` | ciliogenesis/Hh component | 186 / 23679 | 0 |
| `Prkaca` | PKA catalytic subunit that promotes GLI3 repressor processing | 192 / 23679 | 1 |
| `Ttc8` | BBSome ciliary trafficking component | 180 / 23679 | 1 |
| `Ctnnb1` | Wnt/beta-catenin counterexample in the same thalamic group | 171 / 23679 | 383 |
| `Tcf7l2` | thalamic Wnt/TCF counterexample | 111 / 23679 | 106 |

The `Prkaca` and `Ttc8` positives were essentially single-target self effects
in this cell group: the FDR-passing rows were `Prkaca` under `Prkaca` and
`Ttc8` under `Ttc8`, respectively, with no canonical Hh feedback ensemble.

Canonical Hh reporter rows were flat in the most relevant direct perturbations:

- `Gli2` KO: `Gli1`, `Gli3`, `Hhip`, `Ptch1`, `Ptch2`, `Shh`, and `Smo` all
  had `pvals_adj = 1.0`.
- `Ptch1` KO: `Gli1`, `Gli2`, `Gli3`, `Hhip`, `Ptch1`, `Ptch2`, `Shh`, and
  `Smo` all had `pvals_adj = 1.0`.
- `Smo` KO: the same reporter panel had `pvals_adj = 1.0`.
- `Cdon`, `Ift88`, `Kif3b`, `Dync2h1`, `Dzip1`, and `Tbc1d32` likewise left
  GLI/PTCH/HHIP reporters nonsignificant.

The same-experiment Distributed Agents corpus independently summarized this as a
high-confidence pathway claim: across represented Hh receptors, `Smo`, GLI
factors, `Gpr161`, ciliary transduction components, and the `Cdon` coreceptor,
acute single-node perturbation did not recover a coordinated
`Gli`/`Ptch`/`Hhip` feedback or proliferative transcriptional output in
postnatal neuronal nuclei. This claim was anchored or supported by the `Gli2`,
`Ptch1`, `Smo`, `Gli1`, and `Cdon` target contexts I queried.

## Target-specific prediction

### `Gli3`

`Gli3` encodes a GLI zinc-finger transcription factor whose full-length and
processed repressor forms are controlled by the Hedgehog/PTCH-SMO/cilium/SUFU
machinery. In embryos, GLI3 repressor is a major antagonist of Shh signaling;
loss of `Gli3` causes strong dorsal telencephalic, ventral telencephalic, limb,
and thalamic patterning phenotypes. Those facts make `Gli3` biologically close
to the assayed `Gli1`, `Gli2`, `Ptch1`, `Ptch2`, `Smo`, `Gpr161`, `Cdon`,
`Ift88`, `Kif3b`, `Dync2h1`, `Dync2i1`, `Dzip1`, and `Tbc1d32` perturbations.

The within-dataset transfer was uniformly weak for an acute postnatal neuronal
effect:

- `Gli1` and `Gli2`, the direct GLI-family paralogs in training, each had
  `0` DEGs in `151 TH Prkcd Grin2c Glut`.
- Direct upstream Hh components also had `0`: `Ptch1`, `Ptch2`, `Smo`, `Cdon`,
  and `Gpr161`.
- Ciliary genes that should affect the same GLI activator/repressor balance in
  canonical Hh-responsive cells also had `0` in this cell group, including
  `Ift88`, `Kif3b`, `Dync2h1`, `Dync2i1`, `Ift43`, `Ift81`, `Ttc21b`, `Dzip1`,
  and `Tbc1d32`.
- The critical pathway sentinels `Gli1`, `Ptch1`, `Ptch2`, and `Hhip` stayed
  nonsignificant after GLI, PTCH, SMO, CDON, and IFT perturbations, so there is
  no sign of a buffered-but-coherent subthreshold Hh feedback program in the
  focal cells.
- The zero is pathway-specific rather than a blanket failure of the focal group:
  `Ctnnb1` and `Tcf7l2` produced 383 and 106 DEGs, respectively, in the same
  endpoint table.

I therefore predicted `0` for `Gli3`. The most likely state is that the P16
AAV-CRISPR perturbation occurs after the embryonic GLI3-dependent patterning
window and in a thalamic glutamatergic population where the canonical Hh
transcriptional circuit is not detectably active cell-autonomously.

## Limits

This is still an extrapolation. `Gli3` itself, `Sufu`, `Shh`, `Boc`, `Gas1`,
`Kif7`, and `Hhip` were not training perturbations in the focal table, so the
prediction depends on `Gli1`/`Gli2` and upstream PTCH/SMO/cilium proxies.
`Gli3` repressor loss is not directionally identical to `Gli2` activator loss
or `Smo` loss, and GLI3 has Shh-independent developmental roles. The snRNA-seq
readout also does not measure indels, GLI3 protein processing, or ciliary
localization. The claim is only that an acute mosaic partial loss in P16
postmitotic NeuN+ neurons is unlikely to yield any genes below BH FDR 0.05 in
this focal group.
