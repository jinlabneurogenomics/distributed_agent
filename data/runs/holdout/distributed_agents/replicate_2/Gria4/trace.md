# Gria4 DEG-count prediction trace

## Question and readout

The manifest for this run, `098_Gria4.csv`, contains one held-out target:
`Gria4`. I interpreted the requested point prediction as the number of
measured genes with `pvals_adj < 0.05` after acute AAV-CRISPR perturbation of
`Gria4` in `151 TH Prkcd Grin2c Glut` cells. `Gria4` itself was absent as a
perturbation target from both the DE parquet and the focal training-count CSV,
so there is no direct Gria4 expression signature to query. Rows where `names ==
Gria4` in other perturbations were usable as readouts of the Gria4 transcript.

I treated `n_degs` as an assay-specific breadth endpoint, not as a direct proxy
for electrophysiological severity. In particular, the perturbations are sparse
postnatal CRISPR indel perturbations with modest measured RNA knockdown, so the
absence of target-RNA DE is not by itself evidence that editing failed.

## Evidence sources

- `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`
  for observed focal-cell `n_degs` in 1,674 held-in perturbations.
- `[local file: training_de_all_cell_groups.parquet]`
  for focal per-gene log fold-changes and FDRs for biologically related
  held-in perturbations.
- Distributed Agents same-experiment corpus MCP, release
  `perturbai-july-260713-sourceguard-1773-v1`. I used the frozen claims and
  findings ledgers, especially the high-confidence AMPAR buffering claim
  `claim:a9367c3aeaad95bfae9c` and target-specific findings for `Gria1`,
  `Gria2`, `Cacng2`, and `Cacng3`.
- Distributed Agents runtime profile comparison tools for signed log-fold-change profile
  checks among AMPAR, TARP/scaffold, NMDAR, kainate/delta receptor, CaMKII, and
  thalamic-channel comparator perturbations in the focal cell group.
- External literature retrieved with PubMed:
  - Diering and Huganir, 2018, Neuron, DOI
    `10.1016/j.neuron.2018.10.018`, PMID `30359599`: AMPARs are tetramers of
    GluA1-GluA4 plus auxiliary/interacting proteins; synaptic plasticity is
    dominated by receptor composition, trafficking, and post-translational
    regulation.
  - Beyer et al., 2008, Human Molecular Genetics, DOI `10.1093/hmg/ddn064`,
    PMID `18316356`: hypomorphic and null `Gria4` alleles cause absence
    seizures in mice and alter reticular-thalamic AMPAR function; `Gria3` loss
    is not equivalent.
  - Paz et al., 2011, Nature Neuroscience, DOI `10.1038/nn.2896`, PMID
    `21857658`: `Gria4-/-` mice have a specific reduction of cortico-reticular
    thalamic synaptic strength in a circuit model of absence epilepsy.
  - Chen et al., 2000, Nature, DOI `10.1038/35050030`, PMID `11140673`, and
    Tomita et al., 2005, Nature, DOI `10.1038/nature03624`, PMID `15858532`:
    stargazin/CACNG2 couples AMPARs to synaptic targeting and gating.
  - Menuz et al., 2008, Journal of Neuroscience, DOI
    `10.1523/JNEUROSCI.1319-08.2008`, PMID `18753375`: gamma-2/gamma-3 TARP
    redundancy can preserve AMPAR function after loss of either one alone.
  - Xia et al., 1996, Journal of Neuroscience, DOI
    `10.1523/JNEUROSCI.16-17-05425.1996`, PMID `8757255`: NMDA-receptor
    calcium influx can drive MAPK/ERK-dependent immediate-early transcription,
    a reason to keep NMDAR and AMPAR perturbations mechanistically distinct.

## Computation on the supplied DE data

The training endpoint is sparse: 469 of 1,674 held-in perturbations are
nonzero in the focal cell group; the median count is 0, the 75th percentile is
1, the 95th percentile is 18, and the large tail is driven by broad nuclear
regulators such as `Uba5`, `Tpr`, `Sin3a`, spliceosome, proteasome, and
transcriptional regulators.

To inspect the local evidence around `Gria4`, I pulled all focal-cell rows from
the parquet for 27 prespecified ionotropic glutamate receptor, AMPAR
trafficking/scaffold, CaMKII/RapGEF/PSD, and thalamic excitability comparators:

```sql
SELECT gene_target, names, logfoldchanges, pvals, pvals_adj, scores,
       n_pert_matched, n_ctrl_matched
FROM read_parquet('training_de_all_cell_groups.parquet')
WHERE group_name = '151 TH Prkcd Grin2c Glut'
  AND gene_target IN (<Gria/TARP/NMDAR/PSD/thalamic candidates>)
```

This yielded 465,993 rows: 27 perturbations times 17,259 measured genes. For
each target I recomputed `sum(pvals_adj < 0.05)` and checked that it matched
the training-count CSV. Matched perturbed-nucleus counts were 94-283 for this
candidate set, with 23,679 controls.

Key focal counts were:

| training perturbation | focal `n_degs` | expression-pattern evidence |
| --- | ---: | --- |
| `Gria1` | 0 | No FDR<0.05 genes; best adjusted p-value was 0.246. The measured `Gria1`, `Gria2`, `Gria3`, `Gria4`, `Arc`, `Bdnf`, `Fos`, `Egr1`, `Egr3`, `Npas4`, and `Homer1` rows all had q=1. |
| `Gria2` | 0 | No FDR<0.05 genes; every adjusted p-value in the focal surface was 1. AMPAR subunit and activity-response transcripts were also q=1. |
| `Gria3` | 0 | No FDR<0.05 genes; best adjusted p-value was 0.971, including nonsignificant `Gria3` target RNA. |
| `Cacng2` | 0 | No FDR<0.05 genes; all adjusted p-values were 1. `Gria1-4`, `Cacng3`, `Arc`, `Bdnf`, `Fos`, `Egr1`, `Egr3`, `Npas4`, `Vgf`, and `Homer1` were not detectably altered. |
| `Cacng3` | 0 | No FDR<0.05 genes; all adjusted p-values were 1, matching the pan-null same-experiment corpus finding for this TARP. |
| `Dlg4` | 1 | The singleton was `Dlg4` itself with q=1.15e-8; the next ranked gene had q=0.738. This argues for perturbation engagement without a broad PSD-95 downstream state. |
| `Ica1` | 0 | AMPAR-trafficking claim member; no focal FDR<0.05 genes. |
| `Rnf220` | 0 | AMPAR-trafficking claim member; no focal FDR<0.05 genes. |
| `Camk2a` | 0 | Downstream calcium/PSD effector; no focal response. |
| `Camk2b` | 1 | Near-null downstream calcium/PSD effector. |
| `Magi2`, `Rapgef2`, `Rapgef4`, `Syngap1`, `Homer2` | 0 each | PSD/Ras-Rap and scaffold neighbors were flat in the focal group. |
| `Dlgap4` | 2 | Near-null scaffold response. |
| `Grid1`, `Grid2`, `Grik1`, `Grik3`, `Grik4`, `Grik5` | 0-1 | Other ionotropic glutamate receptor families did not show a broad AMPAR-like response. |
| `Grin1` | 89 | Positive receptor counterexample: q=3.31e-53 for `Grin1`, with activity/synaptic genes such as `Scg2`, `Stmn4`, `Kctd16`, and `Gpm6a` also passing FDR. |
| `Grin2a`, `Grin2b`, `Grin2d` | 1, 2, 0 | NMDAR subunit effects were stronger than AMPARs only for some subunits; `Grin2b` had a strong self-RNA hit plus `Pianp`. |
| `Cacna1g` | 12 | T-type calcium channel positive control in the same thalamic group; top hits included `Ptprn`, `Cacna1g`, `Stmn4`, and `Cpne7`. |

I also compared signed log-fold-change profiles for these 27 targets. `Gria1`,
`Gria2`, and `Gria3` each had 17,259 measured features and zero significant
features. Their whole-profile Pearson/cosine values against TARPs, PSD genes,
and NMDAR genes were all similar and weakly informative because the surfaces
were flat; for example, the top Gria1 Pearson neighbor in this candidate set
was `Camk2b`, with `Cacng2` second and `Rapgef4` third. Thus the profile
analysis did not reveal a hidden AMPAR transcriptional module that would raise
the Gria4 estimate above zero.

## Gria4-specific transfer

`Gria4` encodes GluA4, one of the four AMPA receptor pore-forming subunits.
Mechanistically it is closest to the held-in `Gria1`, `Gria2`, and `Gria3`
perturbations: all are AMPAR core subunits, and the external AMPAR literature
places GluA1-GluA4 in the same receptor-code/trafficking axis. In this assay
and this focal cell group, all three held-in AMPAR pore paralogs had `n_degs =
0`; their top FDRs were far from significance and neither AMPAR-subunit
replacement nor immediate-early activity genes were induced.

The TARP/scaffold comparators make the same zero call more secure. `Cacng2`
and `Cacng3`, which regulate AMPAR trafficking and gating, were both perfectly
flat in the focal FDR<0.05 table. `Dlg4` had only its own target transcript as
a DEG. The Distributed Agents corpus summarized this pattern across the whole
same-experiment dataset as a high-confidence statement that represented AMPAR
core and AMPAR-trafficking/scaffold perturbations are transcriptionally
buffered in basal juvenile neurons rather than forming an interchangeable
AMPAR-loss nuclear RNA program.

The strongest counterargument is that Gria4 is especially important in
thalamic circuitry: germline or hypomorphic `Gria4` mutants have absence
seizures and altered cortico-reticular thalamic transmission. I did not let
that override the held-in AMPAR data for two reasons. First, those phenotypes
are network/electrophysiological phenotypes, especially in inhibitory
reticular-thalamic neurons, while `151 TH Prkcd Grin2c Glut` is a
glutamatergic focal group assayed by nuclear RNA after sparse P16 editing.
Second, the dataset could detect nuclear responses to ion-channel perturbation
in this thalamic population when the biology coupled to RNA: `Grin1` had 89
DEGs and `Cacna1g` had 12. The silent AMPAR/TARP/PSD entries therefore point
to a post-transcriptional or buffered AMPAR phenotype, not a global blind spot
for receptors.

## Prediction

For `Gria4`, I predict `0` DEGs in `151 TH Prkcd Grin2c Glut`.

The prediction is driven primarily by within-dataset evidence from held-in
AMPAR core paralogs and AMPAR-trafficking/scaffold genes, with the external
literature used to decide that those are the right analogs and that NMDAR or
T-type channel positives are mechanistic boundaries rather than better
matches.

## Limits

- `Gria4` itself was held out, so this is a paralog/pathway extrapolation, not
  a nearest-neighbor estimate from a Gria4 signature.
- Gria4 has thalamic and absence-epilepsy biology that is not shared
  identically by `Gria1-3`; the screen may miss circuit-level reticular
  thalamic effects, electrophysiological defects, receptor trafficking, or
  AMPAR protein loss.
- The perturbation is acute, sparse, postnatal, and assayed 3-4 weeks after
  AAV delivery. Germline compensation, developmental deletion, pharmacology,
  double-TARP loss, or complete protein ablation could produce a different RNA
  phenotype.
- The focal endpoint is FDR<0.05 in a single cell group. A few weak nominal
  changes could exist below power, but the held-in AMPAR subunits and TARPs
  argue against a robust count above the FDR threshold.
