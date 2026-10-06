## Question and resolved ambiguities

I interpreted the requested endpoint as one integer for each row of
`074_Fcgr2b.csv`: the number of measured genes with `pvals_adj < 0.05` after
acute AAV-CRISPR loss of that target in `151 TH Prkcd Grin2c Glut` nuclei.
The manifest for this run contains a single held-out target:

| target_name |
|---|
| Fcgr2b |

I treated the training CSV as the authoritative focal-cell endpoint for
non-held-out targets and the parquet as the source of per-gene expression
patterns for those same training perturbations. `Fcgr2b` itself was held out, so
no row with `gene_target == "Fcgr2b"` was used.

## Sources used

Internal and same-experiment sources:

- `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`
- `[local file: training_de_all_cell_groups.parquet]`
- Distributed Agents corpus MCP release `perturbai-july-260713-sourceguard-1773-v1`
  - `claim:8bd7e3c8a73422ba8b45`: represented microglial and neuroimmune receptor perturbations do not produce recurrent cell-autonomous neuronal nuclear programs in the NeuN-positive screen.
  - related claim searches covering flat TLR/CD14 innate-receptor, CD3/TCR/BCR-like immunoreceptor, IL-2 receptor, and TNFR-superfamily perturbations.

External mechanism literature:

- Nimmerjahn, Bruhns, Horiuchi, and Ravetch 2005, Immunity,
  DOI `10.1016/j.immuni.2005.05.010`, PMID `16039578`: murine
  FcgammaRIV/Fcgr4 is an activating IgG receptor in the Fc receptor locus with
  myeloid-lineage restriction.
- Nimmerjahn and Ravetch 2005, Science, DOI `10.1126/science.1118948`, PMID
  `16322460`: IgG subclass effector activity is set by the balance of activating
  and inhibitory Fc receptors.
- Xu et al. 2018, Protein and Peptide Letters,
  DOI `10.2174/0929866525666181026162216`, PMID `30370842`, and Roghanian et
  al. 2018, Journal of Leukocyte Biology, DOI `10.1002/JLB.2MIR0917-354R`, PMID
  `29406570`: FcgammaRIIB/CD32B is the sole inhibitory IgG Fc receptor and
  primarily regulates B-cell and myeloid innate/adaptive immune activation.
- Kam et al. 2013, Journal of Clinical Investigation,
  DOI `10.1172/JCI66827`, PMID `23921129`, and Gwon et al. 2018, Journal of
  Neuroscience, DOI `10.1523/JNEUROSCI.1996-17.2018`, PMID `30185465`: Fcgr2b
  has reported neuronal roles in amyloid-beta uptake and toxicity models, a
  stressed Alzheimer-like ligand context rather than the basal juvenile neuronal
  CRISPR context assayed here.

## Same-dataset computations

The focal training endpoint is highly zero-inflated: among 1,674 non-held-out
perturbations in `151 TH Prkcd Grin2c Glut`, 1,205 have `n_degs = 0`, 276 have
`n_degs = 1`, the median is `0`, the mean is `14.05`, and the maximum is `2677`.

To avoid substituting that background rate for target-specific evidence, I
first selected mechanistic analogs for `Fcgr2b`: the available Fc receptor
`Fcgr4`; myeloid and microglial receptors or lineage regulators
`Axl`, `Csf1r`, `Cx3cr1`, `Mertk`, `P2ry12`, `Spi1`, `Ccr2`, and `P2ry14`;
innate immune receptor comparators `Cd14`, `Cd36`, `Tlr2`, `Tlr3`, `Tlr4`,
`Tlr5`, `Tlr7`, and `Tlr8`; and lymphoid immunoreceptor counterexamples
`Cd247`, `Cd3d`, `Cd3e`, `Cd3g`, `Cd4`, `Cd79a`, `Cd79b`, `Cd80`, `Cd40`,
`Icos`, `Il2ra`, `Il2rb`, and `Il2rg`.

I then filtered the parquet to the focal cell group and those selected training
targets and recomputed `sum(pvals_adj < 0.05)` from the per-gene rows, also
checking the minimum adjusted p-value for each target:

```python
expr = (
    (pc.field("group_name") == "151 TH Prkcd Grin2c Glut")
    & pc.field("gene_target").isin(selected_targets)
)
table = dataset.to_table(columns=de_columns, filter=expr)
summary = (
    df.assign(sig=df.pvals_adj < 0.05)
      .groupby("gene_target")
      .agg(n_degs=("sig", "sum"), min_padj=("pvals_adj", "min"))
)
```

The resulting relevant focal counts were uniformly null:

| training target | relationship to Fcgr2b decision | observed focal n_degs | expression-pattern evidence |
|---|---|---:|---|
| `Fcgr4` | closest assayed Fc receptor; activating FcgammaRIV in myeloid Fc biology | 0 | 17,259 measured genes; 162 perturbed nuclei vs 23,679 controls; minimum BH-adjusted p-value `1.0`. Top nominal genes were `Myt1l`, `Grid2ip`, and `Ctnnbip1`, but all had `pvals_adj = 1.0`. |
| `Csf1r` | microglial CSF1R-axis receptor | 0 | minimum BH-adjusted p-value `1.0`; no FDR genes |
| `Cx3cr1` | homeostatic microglial chemokine receptor | 0 | minimum BH-adjusted p-value `1.0`; no FDR genes |
| `P2ry12` | homeostatic microglial purinergic receptor | 0 | minimum BH-adjusted p-value `1.0`; no FDR genes |
| `Axl` | TAM/phagocytic receptor comparator | 0 | minimum BH-adjusted p-value `0.362839`; no FDR genes |
| `Mertk` | TAM/phagocytic receptor comparator | 0 | minimum BH-adjusted p-value `0.888119`; no FDR genes |
| `Spi1` | myeloid-lineage transcription factor counterexample | 0 | minimum BH-adjusted p-value `1.0`; no FDR genes |
| `Cd14`, `Tlr2`, `Tlr3`, `Tlr4`, `Tlr5`, `Tlr7`, `Tlr8`, `Cd36` | basal TLR/CD14/innate immune comparators | all 0 | each had no focal FDR genes; all had minimum BH-adjusted p-value `1.0` in the extracted focal slice |
| `Cd247`, `Cd3d`, `Cd3e`, `Cd3g`, `Cd4`, `Cd79a`, `Cd79b`, `Cd80`, `Cd40`, `Icos`, `Il2ra`, `Il2rb`, `Il2rg` | lymphoid immunoreceptor and cytokine-receptor counterexamples | all 0 | each had no focal FDR genes, arguing against an unobserved generic immune-receptor RNA state in NeuN-positive nuclei |

## Target-specific prediction

### Fcgr2b

`Fcgr2b` encodes FcgammaRIIB/CD32B, the inhibitory IgG Fc receptor. Its canonical
function is to set immune-cell activation thresholds through the balance of
activating Fc receptors and the inhibitory Fcgr2b receptor, with ITIM/SHIP-linked
inhibitory signaling in B cells and myeloid cells. The strongest same-assay
training analog is `Fcgr4`, because it is another murine Fc receptor in the IgG
effector pathway and, unlike more distant cytokine or TLR comparators, is a
direct member of the Fc-receptor biology that `Fcgr2b` modulates. `Fcgr4`
perturbation gave `0` DEGs in the focal thalamic glutamatergic cell group, with
no near-threshold adjusted p-values.

The broader within-dataset evidence points the same way. Microglial and
myeloid-lineage receptors (`Csf1r`, `Cx3cr1`, `P2ry12`, `Axl`, `Mertk`) and the
lineage regulator `Spi1` were all FDR-flat in this focal group. The Distributed Agents
corpus distilled these and related surfaces into a high-confidence claim that
represented microglial and neuroimmune receptor perturbations do not produce
recurrent cell-autonomous neuronal nuclear RNA programs in this NeuN-positive
screen. Innate receptor comparators (`Cd14`, `Tlr2`, `Tlr3`, `Tlr4`, `Tlr5`,
`Tlr7`, `Tlr8`, `Cd36`) and BCR/TCR-like lymphoid immunoreceptors were also
flat in the same endpoint.

The external literature does not supply a reason to override that null. Fcgr2b
can participate in amyloid-beta uptake or Fc-mediated neurotoxicity models, but
those reports involve Alzheimer-like amyloid ligand exposure or disease states.
This experiment instead measured sparse, acute loss of function in basal
postnatal NeuN-positive nuclei without microglia enrichment, antibody immune
complex stimulation, amyloid-beta challenge, or an inflammatory ligand. Under
those conditions the closest same-dataset Fc-receptor perturbation and the
larger neuroimmune comparator panel both indicate no FDR-scale autonomous
neuronal response.

Prediction: `0` DEGs.

## Limits

The prediction is an extrapolation because no training signature exists for
`Fcgr2b` itself, and mouse `Fcgr4` is an activating myeloid Fc receptor whereas
`Fcgr2b` is inhibitory and may signal through different intracellular adaptors.
Key Fc-complex genes such as `Fcer1g`, `Fcgr1`, and `Fcgr3` were absent from the
focal training-count table, so the Fc-family comparison rests on `Fcgr4` plus
more distant immune-receptor panels. The assay also measured nuclear RNA after
sparse partial CRISPR loss in juvenile postmitotic neurons; it would not capture
Fcgr2b roles in B cells, macrophages, microglia, disease-associated amyloid
uptake, antibody-opsonized material, or protein-level receptor trafficking.
Those caveats weaken mechanistic completeness but do not point toward a positive
FDR-scale response in `151 TH Prkcd Grin2c Glut`.
