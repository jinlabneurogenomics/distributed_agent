# GNS forecast trace

## Target and endpoint

- Target: `Gns`
- Focal population: `151 TH Prkcd Grin2c Glut`
- Endpoint: `n_degs`, the count of measured genes in this class with BH-adjusted Wilcoxon `p < 0.05`
- Point forecast: **1**

## Evidence used

### Declared GNS biology bundle

The canonical target bundle says `Gns` is an expressed feature in the requested
population: mean CP10K 1.0636, mean raw UMI 1.7302, and 18,103 / 23,679
non-target nuclei expressing it, or 76.45%. That makes a target-transcript call
technically possible, while not saying whether the edit will visibly lower
nuclear `Gns` RNA.

Functionally, GNS is a soluble lysosomal N-acetylglucosamine-6-sulfatase used in
heparan-sulfate and keratan-sulfate degradation. The bundle adjudicates the
operative stock as a continuously renewed soluble lysosomal enzyme and concludes
that pre-edit GNS activity is likely substantially depleted by the 21-28 day
harvest window. The most direct clock is a 1.1 day recombinant human GNS
activity half-life in neonatal knockout mouse brain, with the caveat that this
was exogenous enzyme in P2 whole brain rather than endogenous juvenile thalamic
neurons.

The observability prior is positive but slower and less matched than the assay:
constitutive `Gns` knockout mice develop glycosaminoglycan storage and
neuroinflammatory pathology including ventral posterior thalamus, but the first
detailed histology in the cited mouse study was at 12 weeks. That is later than
the P37-P44 Perturb-seq harvest and includes glial readouts that are largely
outside the NeuN-enriched screen.

### Training perturbations selected

I used the gene-annotation store to choose a biochemical rather than
symbol-string neighborhood.

- The exact GNS catabolic sets were singleton or effectively singleton in the
  perturbed training universe: KEGG `mmu00531` glycosaminoglycan degradation and
  GO `GO:0030200` heparan-sulfate proteoglycan catabolic process returned only
  `Gns` among perturbation targets.
- The broader Reactome glycosaminoglycan-metabolism set had seven measured
  non-GNS training targets in the focal count table:
  `B3gat3`, `Cspg4`, `Ext1`, `Ext2`, `Gpc6`, `Hs6st2`, and `Xylt1`. All seven
  had `n_degs = 0`.
- KEGG lysosome had 18 represented non-GNS training targets in the focal count
  table. Eleven had zero DEGs; the median was 0 and the mean was 0.5. The largest
  was `Cltc` with only 3 DEGs.

The nearest soluble lysosomal hydrolase / cargo / M6P-trafficking examples were
also flat or self-only in `151 TH Prkcd Grin2c Glut`:

| target | training `n_degs` | significant rows in the focal Parquet |
| --- | ---: | --- |
| `Asah1` | 0 | none |
| `Gnptab` | 0 | none |
| `Gnptg` | 0 | none |
| `Manba` | 0 | none |
| `Ctsb` | 1 | `Ctsb` self row only |
| `Gaa` | 1 | `Gaa` self row only |
| `Ppt1` | 1 | `Ppt1` self row only |
| `Psap` | 1 | `Psap` self row only |

The broad lysosome/endolysosome responders were qualitatively different
operations. `Rab7` had 501 DEGs and the packaged report interprets it as a
late-endosomal/lysosomal trafficking perturbation with V-ATPase, `Lamp2`,
hydrolase, sterol, ISR/UPR, proteasome, and synaptic remodeling arms. `Tsc2` had
86 focal DEGs and is an mTORC1 metabolic/endolysosomal state. I treated these as
proof that the assay can detect a large lysosomal/sterol stress program in this
cell class, not as scale donors for a single cross-correctable lumenal hydrolase.

The same-experiment report/Claim layer supported that interpretation of the
training rows. It groups `Gnptab`, `Gnptg`, `Manba`, `Ppt1`, and `Psap` into the
Claim that represented soluble hydrolase and M6P-pathway perturbations are
largely buffered in the acute sparse neuronal mRNA endpoint rather than
converging on a broad storage-stress module. Separate `Gaa`, `Ctsb`, `Ppt1`,
`Psap`, `Manba`, `Gnptab`, and `Gnptg` Findings call out absence of
TFEB/CLEAR, autophagy, lysosomal, UPR/ISR, or broad downstream RNA responses.
These reports are a semantic layer over the same Parquet, so I used them as
training-profile interpretation rather than independent replication.

### Count-table scale

The focal count table is extremely zero-heavy: among 1,674 training
perturbations, 1,205 were zero, 1,481 were at most one DEG, 1,512 were at most
two, and 1,546 were at most five. Thus a flat or self-only lysosomal hydrolase is
also aligned with the dominant empirical scale of this cell class.

## Synthesis

`Gns` has enough focal expression and a short enough soluble-enzyme lifetime that
the perturbation is biologically reachable by P37-P44. The reason I did not map
that reach to a broad DEG count is that the closest measured class is repeatedly
silent in this exact screen: multiple soluble lysosomal enzymes and M6P-related
targets produced no downstream DEGs, and GAA/PSAP-like cross-correctable enzymes
can be buffered in a sparse mosaic tissue by enzyme uptake from unedited
neighbors. The congenital GNS thalamic phenotype is real, but its measured
12-week mixed-cell pathology is a poor magnitude guide for a 3-4 week
neuron-only nuclear RNA endpoint.

I therefore forecast **zero downstream genes** and assign the single DEG to the
possibility of an on-target `Gns` transcript row, since `Gns` is a measured,
well-detected feature in the focal population and the nearest self-only soluble
hydrolases in the training table land at `n_degs = 1`.
