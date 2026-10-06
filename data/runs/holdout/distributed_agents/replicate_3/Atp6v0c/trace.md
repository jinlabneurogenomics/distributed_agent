# Held-out DEG-count prediction for `151 TH Prkcd Grin2c Glut`

## Question interpreted

The manifest for this run contains one fully held-out genetic perturbation:
`Atp6v0c`. I treated the requested endpoint as the assay-specific count of
mouse genes with Wilcoxon `pvals_adj < 0.05` in the supplied focal class,
including the self transcript if the perturbed gene itself crosses FDR. I did
not require a DEG to be downstream of the perturbation, because the training
CSV endpoint also counts self-transcript hits; for example, `Atp6v0a1` has
`n_degs = 1` in the focal class and the only significant row is `Atp6v0a1`
itself.

## Sources used

- `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`
  for exact training labels and exact focal-class `n_degs`.
- `[local file: training_de_all_cell_groups.parquet]`
  for focal-cell log-fold changes, BH-adjusted p-values, and matched nucleus
  counts of the V-ATPase and endolysosomal comparators.
- Distributed Agents runtime profile comparison over `151 TH Prkcd Grin2c Glut`
  log-fold-change vectors, restricted to the 1,674 training perturbations, to
  check whether direct V-ATPase comparators shared FDR-supported features with
  larger endolysosomal responses.
- Distributed Agents corpus release `perturbai-july-260713-sourceguard-1773-v1`, the
  same-experiment semantic layer. `Atp6v0c` itself was not present in the
  filtered corpus, but `Atp6v0a1`, `Atp6v1a`, `Rab7`, `Atp6ap2`, and related
  V-ATPase findings were present.
- External literature from PubMed:
  Forgac 2007, DOI `10.1038/nrm2272`, for the V-ATPase as a multisubunit
  rotary proton pump acidifying endomembrane compartments.
  Zoncu, Bar-Peled, Efeyan, Wang, Sancak and Sabatini 2011, DOI
  `10.1126/science.1207056`, for lysosomal V-ATPase coupling to
  Ragulator/Rag/mTORC1 amino-acid sensing.
  Xu et al. 2019, DOI `10.1016/j.cell.2019.06.007`, for an ATP6V0C-centered
  V-ATPase-ATG16L1 axis in autophagic recognition of damaged bacteria-containing
  vacuoles.
  Mattison et al. 2023, DOI `10.1093/brain/awac330`, and Zhao et al. 2023,
  DOI `10.1038/s10038-023-01145-1`, for human ATP6V0C variants that impair
  V-ATPase function and are associated with neurodevelopmental phenotypes and
  epilepsy.

## Computational checks

The Parquet has 712 row groups and is sorted by `group_name`. I used Parquet
row-group min/max statistics to read only the 35 row groups overlapping
`151 TH Prkcd Grin2c Glut`, then filtered to biologically nominated comparator
targets. For each comparator I counted rows with `pvals_adj < 0.05` to verify
the CSV count and inspected the significant genes. I also scanned the focal
block for V-ATPase measured genes to confirm that `Atp6v0c` is an assayed
transcript in this cell group.

The most relevant focal-class counts were:

| training perturbation | `n_degs` | focal-class evidence and interpretation |
|---|---:|---|
| `Atp6v0a1` | 1 | Closest measured V0 membrane-sector comparator. The only FDR gene was the self transcript, `Atp6v0a1` log2FC `-0.640`, adjusted `p = 4.52e-12`; the next best non-self row had adjusted `p = 0.125`. |
| `Atp6v1a` | 0 | Core catalytic V1 A subunit; no focal FDR genes. |
| `Atp6v1b2` | 0 | Core V1 B subunit; no focal FDR genes. |
| `Atp6v1e1` | 0 | Core V1 E subunit; no focal FDR genes. |
| `Atp6ap2` | 2 | V-ATPase accessory/assembly-associated factor; `Atp6ap2` self was down and `Atp6v0a1` was also down. This is a two-gene pump-related mini-signature, not a lysosomal-collapse program. |
| `Atp13a2` | 1 | Lysosomal P5B ATPase disease comparator; self only. |
| `Lamp2` | 0 | Lysosomal membrane comparator; no focal FDR genes. |
| `Atg5`, `Atg16l1`, `Becn1` | 0, 0, 0 | Core autophagy comparators; no focal FDR genes. |
| `Sqstm1`, `Map1lc3a` | 1, 1 | Each is self-only in the focal class. |
| `Vps41` | 0 | HOPS/Rab7-pathway comparator; no focal FDR genes. |
| `Vps35`, `Vps54` | 17, 31 | Retromer/GARP trafficking perturbations with modest nonzero signatures, but they do not phenocopy core V-ATPase loss. |
| `Tsc2`, `Mtor` | 86, 2 | mTOR-pathway comparators. `Tsc2` is a real positive sterol/lysosome-state control, whereas `Mtor` is nearly flat. |
| `Rab7` | 501 | Strong late-endosome/lysosome positive control. It induced `Atp6v1b2`, `Dpp7`, `Atp6v0b`, `Lamp2`, `Atp6ap1`, `Atp6v1a`, and a sterol/proteostasis stress arm, showing that this cell group can report endolysosomal injury when the perturbation reaches a nuclear stress threshold. |

The runtime profile comparison used the 17,259 measured focal features shared
across the selected nodes. Among the direct V-ATPase comparators,
`Atp6v0a1` had one significant feature, `Atp6ap2` had two, and `Atp6v1a`,
`Atp6v1b2`, and `Atp6v1e1` had none; none of those FDR features intersected
the hundreds of significant `Rab7` features or the 86 `Tsc2` features. I
therefore treated all-gene logFC cosine similarity among these mostly flat
profiles as background structure, not as evidence for a hidden broad V-ATPase
module.

## Internal same-experiment evidence

The Distributed Agents corpus strongly cautions against transferring the large `Rab7`
response to every V-ATPase subunit:

- `Atp6v0a1:F003` reports that represented V-ATPase relatives and lysosomal
  disease comparators failed to generate a robust neuronal snRNA signature.
  In the focal class this is the self-only `Atp6v0a1` result above.
- Claim `claim:d08f04d8507bae4de40b` summarizes the represented V-ATPase
  subunits, regulators, accessory factors and lysosomal comparators as
  subunit-specific, sparse, divergent, or flat; same-pump membership was
  insufficient to produce a shared postnatal neuronal module.
- Claim `claim:2aa16e813622a843c706` similarly states that shared
  endomembrane-acidification annotation was not enough to make NHE, CLC, and
  V-ATPase perturbations converge in this P16 postmitotic neuronal assay.
- `Rab7:F002` and `Rab7:F009` provide the key counterweight: `Rab7` loss
  induced a recurrent late-endosomal/lysosomal compensation state, but measured
  HOPS, retromer, WASH, V-ATPase, `Lamp2`, `Gaa`, `Grn`, and `Becn1`
  comparators mostly failed to phenocopy it at FDR level. That makes `Rab7`
  a positive detection control, not a quantitative proxy for `Atp6v0c`.

## Target-specific prediction

### `Atp6v0c`

`Atp6v0c` encodes the small proteolipid c subunit of the V0 membrane sector.
The c-ring is required for V-ATPase proton translocation, so a complete
ATP6V0C loss is expected to perturb lysosomal, endosomal, and synaptic-vesicle
acidification. External evidence makes this a biologically real neuronal
gene: human heterozygous ATP6V0C variants can impair V-ATPase function and
are associated with neurodevelopmental epilepsy phenotypes, and V-ATPase
activity participates in lysosomal mTORC1 signaling and, through ATP6V0C, in
ATG16L1-mediated xenophagy.

The dataset-local evidence argues that this biology should not be converted
into a large focal `n_degs`:

- the closest V0 comparator, `Atp6v0a1`, had exactly one FDR gene in
  `151 TH Prkcd Grin2c Glut`, and it was only the edited transcript;
- the other represented core pump subunits had `n_degs` of `0`, `0`, and `0`;
- the accessory factor `Atp6ap2` gave only a two-gene V-ATPase mini-signature;
- autophagy and lysosomal-membrane controls were zero or self-only;
- the broad `Rab7` and moderate `Tsc2` responses show that the assay can
  detect endolysosomal/sterol/proteostasis compensation, but the corpus and the
  focal rows both reject them as direct quantitative phenocopies of core
  V-ATPase loss.

The one reason to predict a nonzero count rather than `0` is the endpoint's
inclusion of self-DE. `Atp6v0c` was present as a measured transcript in the
focal Parquet and was FDR-significant under 14 other training perturbations,
including induction after `Rab7`. Given the strong self-DE of `Atp6v0a1` and
`Atp6ap2` in the same focal class, the best point estimate is a self-only
signature with no secondary BH-significant genes.

Predicted `n_degs`: `1`.

## Limits and uncertainty

This is an extrapolation from neighboring V-ATPase subunits because `Atp6v0c`
was absent from both the training DE table and the filtered Distributed Agents corpus.
`ATP6V0C` is not just another isoform of `Atp6v0a1`: it is part of the
rotating c-ring and may be less redundant, while `Atp6v0a1` is an a-subunit
isoform. A severe biallelic `Atp6v0c` lesion could deplete edited neurons
before harvest, or guide cuts in this short hydrophobic coding region could
destroy protein without much nonsense-mediated decay; either case would make
the recovered nuclear RNA count lower than the biochemical importance of the
gene. Conversely, if the four gRNAs happened to create a strong target-RNA
knockdown, the self transcript alone could cross FDR even with no downstream
program. Because the endpoint is a hard BH count near zero, the main
uncertainty is therefore `0` versus `1`, not whether `Atp6v0c` should look like
the 501-DEG `Rab7` response.
