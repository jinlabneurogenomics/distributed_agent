# Reasoning trace

## Question and resolved ambiguities

The held-out readout is the number of measured genes with `pvals_adj < 0.05`
after CRISPR loss of the requested target in `151 TH Prkcd Grin2c Glut` cells.
`151` is the thalamic glutamatergic Allen-taxonomy class named in the prompt,
not a nucleus count. The manifest for this run contains one held-out target:
`Ptpa`.

I treated the requested value as a point prediction for the exact assay-specific
DEG count, not as a judgment of whether PTPA is important, whether editing would
work, or whether PP2A phosphatase activity would change. This distinction
matters for `Ptpa` because PP2A activation is primarily a phosphoprotein and
holoenzyme-maturation process, whereas the endpoint is a basal single-nucleus
RNA Wilcoxon count in recovered postnatal neurons.

## Sources

- Input parquet:
  `[local file: training_de_all_cell_groups.parquet]`.
- Focal-cell training counts:
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
- Requested-target manifest:
  `[local file: 191_Ptpa.csv]`.
- Distributed Agents corpus `perturbai-july-260713-sourceguard-1773-v1`, queried for
  `Ptpa`, `Ppp2r2b`, `Ppp2r5d`, `Ptpn1`, and `Set`.
- Distributed Agents runtime profile-neighbor and profile-compare artifacts:
  `ptpa_pp2a_profile_neighbors.json`,
  `ptpa_candidate_profile_compare.json`, and
  `ptpa_candidate_profile_inspect.json`.
- External PubMed searches for `PTPA` / `PPP2R4` / PP2A biology.

The Distributed Agents corpus had no curated same-experiment finding for held-out
`Ptpa`, so the within-dataset part of the prediction came from held-in PP2A and
PTPA-adjacent perturbations.

## Dataset calibration

The focal training table has 1,674 held-in targets. The endpoint is sparse:
1,205 / 1,674 targets, or 71.98%, have `n_degs = 0`; the median is 0 and the
75th percentile is only 1. Counts above 10 are already uncommon.

I searched the 1,674 training targets for PP2A/phosphatase and nearby signaling
genes. The only represented PP2A regulatory-subunit targets were `Ppp2r2b` and
`Ppp2r5d`, and both had zero focal DEGs. Other exact catalytic, scaffold,
methylation, and PTPA-chaperone partners such as `Ppp2ca`, `Ppp2cb`,
`Ppp2r1a`, `Ppp2r1b`, `Lcmt1`, `Ppme1`, `Igbp1`, and `Tiprl` were not in the
training-count table.

For the biologically relevant held-in genes that were present, the focal counts
were:

| target | role as analog or counterexample | observed `n_degs` in `151 TH` |
|---|---|---:|
| `Ppp2r2b` | PP2A B55beta regulatory subunit | 0 |
| `Ppp2r5d` | PP2A B56delta regulatory subunit | 0 |
| `Set` | endogenous PP2A inhibitor | 0 |
| `Ptpn1` | PTP1B; reported mediator of PTPA effects on PP2A Tyr307 in a tau/AD cell model | 0 |
| `Setbp1` | SET-binding protein, indirect SET/PP2A comparator | 0 |
| `Ppm1g` | phosphatase comparator with a reported B56delta-related complex in other systems | 3 |
| `Mtor` | downstream mTOR-axis counterexample | 2 |
| `Rptor` | mTORC1 scaffold counterexample | 0 |
| `Tsc2` | mTORC1 brake; shows the assay can detect a downstream mTOR-like state | 86 |
| `Akt3` | PI3K/AKT branch comparator | 0 |
| `Gsk3b` | kinase linked to PP2A/tau/Wnt signaling | 6 |
| `Mapt` | tau itself | 1 |
| `App` | APP/tau-neurodegeneration comparator | 1 |
| `Ctnnb1` | strong Wnt/beta-catenin counterexample | 383 |

I then queried the parquet for those targets in exactly
`151 TH Prkcd Grin2c Glut`. This recomputed the endpoint from row-level
`pvals_adj` and checked whether any zero-count analog had near-threshold genes:

- `Ppp2r2b`: 17,259 measured genes, 151 perturbed nuclei versus 23,679 controls,
  `0` genes at FDR 0.05, minimum adjusted p-value 0.3617.
- `Ppp2r5d`: 17,259 measured genes, 141 perturbed nuclei, `0` FDR genes,
  minimum adjusted p-value 0.4050.
- `Ptpn1`: 17,259 measured genes, 208 perturbed nuclei, `0` FDR genes,
  minimum adjusted p-value 1.0.
- `Set`: 17,259 measured genes, 163 perturbed nuclei, `0` FDR genes, minimum
  adjusted p-value 0.6570.
- `Ppm1g`: `3` FDR genes, with `Col4a2` and `Col4a1` down and `H2ac25` up.
  This is a weak phosphatase response, not a PP2A core phenocopy.
- `Tsc2`: `86` FDR genes, showing that this cell group can report a robust
  sustained kinase/phosphatase-pathway perturbation when the hit is at a
  transcriptionally visible downstream node.
- `Ctnnb1`: `383` FDR genes, a positive counterexample for Wnt output. I did
  not transfer this large value to `Ptpa`: PP2A can modulate beta-catenin
  phosphorylation in some contexts, but PTPA partial loss is not equivalent to
  direct beta-catenin loss in juvenile postmitotic thalamic neurons.

The Distributed Agents corpus made the same local point from the broader same-experiment
semantic layer. It reports that:

- `Ppp2r2b` produced no FDR<0.10 downstream transcriptional response in any of
  the measured neuronal groups, and did not converge with `Ppp2r5d`.
- `Ppp2r5d` produced only a very sparse response outside this focal cell group
  and no broad mTOR, tau-kinase, APP/tau, Wnt, ISR, UPR, autophagy,
  proteasome, or apoptotic transcriptome.
- `Set` caused only a single resolved downstream change in another cell group
  and was disjoint from `Ppp2r2b`/`Ppp2r5d`.
- `Ptpn1` had only two isolated downstream genes across the screen and no basal
  leptin/insulin/JAK-STAT, BDNF-TrkB, or ER-stress RNA program.

Finally, I used the Distributed Agents runtime to compare held-in focal signatures.
`Ppp2r2b`, `Ppp2r5d`, `Ptpn1`, and `Set` each had
`significant_feature_count = 0`; `Ppm1g` had three. None of these weak/zero
phosphatase anchors shared a significant positive or negative focal DEG with
`Mtor`, `Tsc2`, `Gsk3b`, `Mapt`, `App`, or `Ctnnb1`. A whole-logFC neighbor
scan of the null anchors returned unrelated mostly-zero targets as nearest
neighbors, so I treated those raw vector correlations as null-background
diagnostics rather than as mechanistic analogs.

## Biological interpretation for `Ptpa`

`Ptpa` encodes the PP2A phosphatase activator PTPA, called `PPP2R4` in human
literature. PTPA binds the PP2A catalytic subunit and acts as an ATP-dependent
activation chaperone that helps generate active PP2A; structural and biochemical
work showed contacts around the PP2A active site and metal-loading/ATP-hydrolysis
requirements for activation (Jordens et al., 2005,
doi:10.1074/jbc.M507760200; Guo et al., 2013,
doi:10.1038/cr.2013.138). PTPA can therefore be more upstream of total PP2A
holoenzyme biogenesis than a single B subunit.

There is real external evidence that losing PTPA can matter. `Ppp2r4`
gene-trapped mice with residual PTPA had reduced PP2A activity and increased
tumor susceptibility (Sents et al., 2017, doi:10.1158/0008-5472.CAN-16-2911),
and PPP2R4 dysfunction accelerated KRAS-driven lung tumorigenesis (Meeusen et
al., 2021, doi:10.1016/j.canlet.2021.06.022). Neuronal/cell-line papers linked
PTPA to PP2A Tyr307, PTP1B, tau phosphorylation, and mitochondrial apoptosis
(Luo et al., 2013, doi:10.1016/j.bbamcr.2013.02.005; Luo et al., 2014,
doi:10.1111/jnc.12761). Human recessive PTPA/PPP2R4 variants have been reported
in early-onset parkinsonism with intellectual disability and impaired PP2A
activation (Fevga et al., 2023, doi:10.1093/brain/awac326; Li et al., 2023,
doi:10.1002/mds.29411).

Those mechanisms raise the prior above a totally inert gene, but they do not
outweigh the focal Perturb-seq calibration:

- PTPA biology is largely phosphoproteomic, holoenzyme-assembly, and chronic
  stress/disease biology; this endpoint is a 3-4 week basal nuclear RNA readout.
- The observed perturbation is sparse AAV CRISPR in recovered postmitotic
  nuclei. It is not a full germline knockout or a homozygous human missense
  disease state.
- `Ppp2r2b` and `Ppp2r5d`, the two PP2A regulatory subunits actually measured
  in training, were completely flat in the focal cell group despite reasonable
  matched perturbed-nucleus counts.
- `Set` and `Ptpn1`, the most directly represented SET/PP2A and PTPA-PTP1B
  comparators, were also completely flat in this same cell group.
- Strong downstream states can be detected in `151 TH` for some nodes
  (`Tsc2`, `Ctnnb1`), so the PP2A-adjacent zeros are not explained by a global
  inability of this cell group to produce DEGs.

I therefore predict `Ptpa` will be FDR-null rather than weakly positive in
`151 TH Prkcd Grin2c Glut`.

## Limits and extrapolation

The comparison is imperfect. PTPA is an activation chaperone for PP2A catalytic
subunits, not just another substrate-selecting B subunit; the screen did not
include `Ppp2ca`, `Ppp2cb`, `Ppp2r1a`, `Lcmt1`, or `Ppme1`, and it did not
measure PP2A catalytic activity, C-subunit methylation, tau phosphorylation,
Drp1 phosphorylation, mitochondrial morphology, apoptosis, or parkinsonism-like
physiology. PTPA could alter those outputs without crossing a single-nucleus
FDR threshold in basal recovered thalamic glutamatergic nuclei.

The point estimate is consequently a local endpoint prediction, driven most
strongly by the within-dataset PP2A/SET/PTP1B nulls. The external literature
prevents interpreting the prediction as "PTPA is irrelevant"; it only says that
a broad acute RNA signature is unlikely under this assay and cell-group
condition.

Final point prediction: `Ptpa = 0`.
