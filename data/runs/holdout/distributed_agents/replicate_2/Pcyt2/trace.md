# DEG-count prediction trace

## Question and resolved ambiguity

The held-out manifest for this run contains one requested perturbation:
`Pcyt2`. I interpreted the endpoint as the exact training-table quantity:
the number of measured genes, including the targeted transcript if it is
detected, with `pvals_adj < 0.05` in `151 TH Prkcd Grin2c Glut` nuclei.
`Pcyt2` was absent from both supplied training files, so its own signature was
not available and was not used.

I treated `151 TH Prkcd Grin2c Glut` as a thalamic glutamatergic population
from the Allen taxonomy, not as dopaminergic TH cells. I also treated this as
an acute P16 AAV CRISPR loss-of-function readout in surviving postmitotic
neurons; germline and disease models were used only as gene-function priors.

## Sources

- The supplied
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`
  table for observed focal-cell DEG counts of all non-held-out perturbations.
- The supplied
  `[local file: training_de_all_cell_groups.parquet]`
  for focal differential-expression rows, top genes, FDR support, and
  pairwise profile similarity among selected lipid and sterol comparators.
- The Distributed Agents same-experiment semantic corpus
  `perturbai-july-260713-sourceguard-1773-v1`, queried for interpreted
  within-screen claims and findings around `Selenoi`, `Agps`, `Marchf6`,
  `Sptlc2`, `Stard7`, and `Acsl4`.
- PubMed through NCBI E-utilities for external mechanism. The main mechanism
  citations were:
  - Bladergroen and van Golde 1997, DOI `10.1016/s0005-2760(97)00113-6`:
    Pcyt2/ET converts phosphoethanolamine to CDP-ethanolamine and is distinct
    from phosphocholine cytidylyltransferase.
  - Bakovic, Fullerton, and Michel 2007, DOI `10.1139/o07-006`, and Pavlovic
    and Bakovic 2013, DOI `10.3390/ijms14022529`: Pcyt2 is the main
    regulatory enzyme of the mammalian CDP-ethanolamine Kennedy pathway for
    de novo phosphatidylethanolamine synthesis.
  - Singh et al. 2012, DOI `10.1194/jlr.M021881`: complete mouse Pcyt2
    deletion is embryonic-lethal and heterozygous deficiency causes systemic
    lipid-homeostasis phenotypes.
  - Vaz et al. 2019, DOI `10.1093/brain/awz291`: biallelic hypomorphic human
    PCYT2 variants cause a complex hereditary spastic paraplegia with
    developmental regression, epilepsy, and brain atrophy, and perturb
    ether-phospholipid metabolism.
  - Horibata et al. 2018, DOI `10.1194/jlr.P081620`: SELENOI/EPT1 transfers
    phosphoethanolamine from CDP-ethanolamine to lipid acceptors to make
    diacyl phosphatidylethanolamine and plasmenyl-phosphatidylethanolamine.
  - Fu et al. 2021, DOI `10.1038/s41586-021-03692-z`: the
    ETNK1-PCYT2-SELENOI CDP-ethanolamine pathway can control cell signaling
    through a PE-dependent, partly post-transcriptional mechanism in immune
    cells, illustrating that this pathway can be biologically potent without
    necessarily acting first through a broad mRNA program.

## Computational work over the training data

The focal count table had 1,674 non-held-out targets. Its distribution was
zero-heavy in this cell group: median `n_degs = 0`, third quartile `1`, 90th
percentile `2`, 95th percentile `18`, and a long right tail driven by a small
number of broad perturbations. That made the default expectation for a new
metabolic target zero or a singleton unless a direct measured neighbor argued
otherwise.

I first enumerated lipid and organelle-homeostasis genes present in the
training count table. The direct Kennedy-pathway genes closest to Pcyt2 were
mostly absent as perturbations: I did not find `Etnk1`, `Etnk2`, `Cept1`,
`Chpt1`, `Pcyt1a`, `Pcyt1b`, `Pisd`, `Ptdss1`, `Ptdss2`, or `Pemt`. The useful
remaining comparators were therefore the downstream CDP-ethanolamine
phosphotransferase `Selenoi`, ether-lipid enzymes such as `Agps` and `Far1`,
generic lipid-enzyme or lipid-transfer controls such as `Sptlc2`, `Acsl4`, and
`Stard7`, and sterol/SREBP controls such as `Marchf6`, `Srebf2`, and `Hmgcr`.

I then pulled only `151 TH Prkcd Grin2c Glut` rows for the selected cohort from
the parquet, avoiding a full materialization of the 7.8 GB file:

```python
filt = (pc.field("group_name") == "151 TH Prkcd Grin2c Glut") & \
       pc.field("gene_target").isin(candidates)
tab = dataset.to_table(
    columns=["names", "scores", "logfoldchanges", "pvals_adj",
             "group_name", "gene_target",
             "control_label", "n_pert_matched", "n_ctrl_matched"],
    filter=filt,
)
```

The focal parquet counts matched the provided count table for the selected
targets. I also compared the signed Wilcoxon-score profiles among the selected
targets with the Distributed Agents runtime profile comparison tool. The important
profile observations were:

- `Selenoi`: 5 focal DEGs. `Insig1`, `Msmo1`, and `Fdft1` were significant
  positive sterol genes; `Selenoi` itself and `Nos1ap` were significant
  negative calls. It had direct FDR-level positive overlap with `Marchf6` on
  `Insig1`, `Msmo1`, and `Fdft1`, and it was anti-oriented to the `Srebf2`
  loss profile on sterol genes.
- `Marchf6`: 14 focal DEGs. The strongest downstream genes were the same
  sterol/cholesterol-feedback axis: `Insig1`, `Dhcr24`, `Cyp51`, `Msmo1`,
  `Hmgcr`, `Fdft1`, `Hmgcs1`, `Ldlr`, `Fdps`, `Sqle`, and `Srebf2` were all
  up.
- `Srebf2`: 7 focal DEGs. `Srebf2` itself and cholesterol genes including
  `Dhcr24`, `Insig1`, `Hmgcs1`, `Msmo1`, `Cyp51`, and `Sqle` were down,
  confirming that the Marchf6/Selenoi direction is an induced SREBF2-like
  sterol-feedback module rather than random lipid-gene noise.
- `Agps`: 1 focal DEG at FDR 0.05, `Dhcr24` up; `Lmtk3` and `Cyp51` were
  directionally positive but above the cutoff.
- `Far1`: 2 focal DEGs, a `Far1` self-transcript decrease plus `Tial1` up, not
  the Selenoi/Marchf6 sterol program.
- `Sptlc2`: 1 focal DEG, `Sptlc2` itself; same-experiment corpus findings
  describe no downstream FDR<0.10 program in this focal group despite detectable
  target-mRNA loss.
- `Acsl4`: 1 focal DEG, `Acsl4` itself in 151; its restricted sterol signal was
  elsewhere rather than a focal-cell match.
- `Stard7`, `Hmgcr`, `Srebf1`, `Pex1`, and `Gpx4`: 0 focal DEGs.

## Target-specific reasoning

### Pcyt2

`Pcyt2` encodes CTP:phosphoethanolamine cytidylyltransferase, the enzyme that
activates phosphoethanolamine to CDP-ethanolamine in the Kennedy pathway. That
places it directly upstream of ethanolamine phosphotransferases that consume
CDP-ethanolamine to make diacyl PE and plasmenyl-PE. The best represented
downstream neighbor was `Selenoi`, whose product EPT1 carries out this terminal
CDP-ethanolamine transfer reaction and whose loss produced the most relevant
training signature: five focal DEGs with a compact SREBP2/cholesterol-feedback
shape. The external SELENOI and PCYT2 genetics both support treating this as a
real PE/plasmalogen route rather than a superficial lipid-family match:
Horibata et al. showed that SELENOI/EPT1 loss impairs production of
ethanolamine glycerophospholipids and plasmenyl-PE, and Vaz et al. showed that
hypomorphic PCYT2 variants disturb etherlipid metabolism in a neurodevelopmental
spastic paraplegia.

That direct-neighbor signal argues against a hard zero prediction. The
Selenoi focal signature was small but coherent: `Insig1`, `Msmo1`, and `Fdft1`
were all up at FDR<0.05, and the same positive coordinates were significant in
the broader `Marchf6` sterol rebound. `Srebf2` loss drove the same module in
the opposite direction. The Distributed Agents corpus explicitly summarized this as
Selenoi loss producing a compact FDR-corrected sterol-feedback signature only
in 151 TH Prkcd Grin2c Glut, and as lying in a recurrent ER/endolysosomal
cholesterol-homeostasis state with `Marchf6`, `Rab7`, `Mib1`, and `Dctn1`.
That is within-dataset evidence for a detectable, not merely theoretical,
lipid-feedback response in exactly the focal cell group.

Several counterexamples pull the expected count down. The represented lipid
space was mostly flat or sparse in this assay: `Stard7` had 0 focal DEGs,
`Sptlc2` had only its own transcript in the focal group, and the
peroxisomal/ether-lipid comparators `Agps` and `Far1` reached only 1 and 2
focal DEGs respectively. The corpus made the same point at screen scale:
represented sphingolipid-pathway and lipid-transfer perturbations did not form
a coherent multi-gene neuronal module, and `Agps`/`Far1`/peroxisome relatives
were not interchangeable phenocopies. Likewise, `Hmgcr` and `Srebf1` were flat
in the focal group, so simply touching lipid synthesis is not enough to produce
the Selenoi/Marchf6 sterol output. `Acsl4` and `Gpx4` also argue against a
large oxidative-stress or ferroptosis transcriptional burst after basal
phospholipid perturbation.

Balancing those pieces, I predict `Pcyt2` as a small nonzero responder, nearest
to `Selenoi` but not as broad as direct ER sterol-control perturbations such as
`Marchf6`, `Rab7`, or `Tsc2`. The point estimate I used is 4 DEGs: enough for a
Selenoi-like sterol-feedback call, possibly including `Pcyt2` itself if the
target transcript is depleted, but below the Marchf6/Srebf2 tier because no
training evidence showed that CDP-ethanolamine or plasmalogen perturbations
expand to dozens of focal DEGs in this acute postnatal neuronal assay.

## Limits

The largest uncertainty is that the exact enzymatic substitute for PCYT2 was
not in the training set. `Selenoi` is downstream of PCYT2 and consumes the
product of the PCYT2 reaction, but it is not identical: final PE synthesis can
involve different phosphotransferases, and PCYT2 lies upstream of both diacyl
and ether-linked PE branches. The comparison to `Agps` and `Far1` is also
imperfect because those enzymes act in peroxisomal ether-lipid synthesis rather
than in the cytosolic CDP-ethanolamine step.

The training assay measured nuclear RNA after sparse editing, not PE,
plasmalogen, diacylglycerol, or cholesterol flux. Literature showing that
PCYT2 is essential for organismal development or that SELENOI is required for
normal ether phospholipid homeostasis does not guarantee a broad RNA response
in surviving P37-P44 thalamic neurons. Conversely, a zero-DEG training target
could still have a strong lipid phenotype that is buffered, post-transcriptional,
or selected away before nuclei collection. Therefore the predicted count is an
extrapolation from a small number of lipid-feedback analogs rather than a
direct phenocopy measurement.
