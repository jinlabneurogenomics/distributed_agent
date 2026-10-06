# Reasoning trace

## Question and resolved ambiguities

The task is to predict the held-out endpoint for every target in
`090_Gbf1.csv`, preserving manifest order. The manifest contains one requested
target, `Gbf1`.

I interpreted `n_degs` as the exact number of measured genes in `151 TH Prkcd
Grin2c Glut` whose Scanpy Wilcoxon Benjamini-Hochberg adjusted p-value was
below 0.05 for that perturbation in the original experiment. `Gbf1` was absent
from the supplied training signatures and from the supplied training count CSV,
so I used only non-held-out perturbations as within-dataset evidence. The
prediction is an assay-scale count, not a claim about complete loss of GBF1
protein, viability, secretion, or Golgi morphology.

## Sources used

- Supplied endpoint counts:
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`
- Supplied per-gene DE signatures:
  `[local file: training_de_all_cell_groups.parquet]`
- Requested-target manifest:
  `[local file: 090_Gbf1.csv]`
- Distributed Agents same-experiment corpus:
  `perturbai-july-260713-sourceguard-1773-v1`
- Distributed Agents runtime profile-neighbor comparison over the focal cell group,
  written to `gbf1_traffic_profile_neighbors.json`
- External mechanism literature from PubMed:
  - Garcia-Mata et al. 2003, PMID: 12808027, DOI: 10.1091/mbc.e02-11-0730
  - Zhao et al. 2006, PMID: 16926190, DOI: 10.1242/jcs.03173
  - Szul et al. 2007, PMID: 17956946, DOI: 10.1242/jcs.010769
  - Manolea et al. 2007, PMID: 18003980, DOI: 10.1091/mbc.e07-04-0394
  - Jackson 2014, PMID: 25610717, DOI: 10.4161/21592780.2014.943616
  - Kaczmarek et al. 2017, PMID: 28985001, DOI: 10.1111/boc.201700042
  - Sager et al. 2021, PMID: 33405949, DOI: 10.1091/mbc.E20-09-0587

## Computational steps

1. Read `090_Gbf1.csv`; it contains only `Gbf1`.
2. Read the focal training-count CSV and summarized the 1,674 available
   endpoints. The distribution is very sparse: 1,205 targets have 0 DEGs, 1,481
   have 0 or 1, and only 59 have 50 or more.
3. Selected same-pathway or counterexample targets from the training counts:
   COPI and ER-Golgi targets (`Copa`, `Copg1`, `Stx5a`, `Trip11`, `Tmem165`),
   COPII/ER-exit targets (`Sec23a`, `Sar1b`, `Tfg`), COG/GARP/retrograde
   targets (`Cog4`, `Cog5`, `Vps53`, `Vps54`, `Vps35`), and ER-stress positive
   comparators (`Sec63`, `Atp2a2`, `Dhdds`, `Gfpt1`, `Hspa5`, `Manf`). The
   focal counts were:

   | target | n_degs |
   | --- | ---: |
   | Copa | 0 |
   | Copg1 | 1 |
   | Stx5a | 0 |
   | Trip11 | 0 |
   | Tmem165 | 0 |
   | Sec23a | 0 |
   | Sar1b | 0 |
   | Tfg | 0 |
   | Cog4 | 0 |
   | Cog5 | 0 |
   | Vps53 | 0 |
   | Vps54 | 31 |
   | Vps35 | 17 |
   | Caml | 28 |
   | Pitpna | 21 |
   | Sec63 | 11 |
   | Hspa5 | 5 |
   | Manf | 3 |
   | Atp2a2 | 187 |
   | Dhdds | 116 |
   | Gfpt1 | 311 |
   | Rab7 | 501 |

4. Used Parquet row-group statistics to read only the focal `151 TH Prkcd
   Grin2c Glut` row groups and the selected targets above, then listed each
   FDR-significant gene. The extracted significant rows matched the count CSV:
   for example `Copg1` and `Stx16` each had only the perturbed transcript as a
   hit, `Sec63` had 11 DEGs headed by the ER-stress genes `Hspa5`, `Canx`,
   `Hyou1`, and `Chac1`, while `Atp2a2`, `Dhdds`, and `Gfpt1` showed broader
   UPR/ISR-like programs containing `Ddit3`, `Xbp1`, `Herpud1`, `Hspa5`,
   `Chac1`, aminoacyl-tRNA synthetases, and one-carbon or amino-acid stress
   genes.
5. Ran Distributed Agents `profile_neighbors` on the same focal signatures with the
   ER-Golgi and trafficking analogs as anchors. This produced a lossless
   per-anchor profile-neighborhood artifact for all 1,674 training endpoints.
   I treated unthresholded logFC neighborhoods cautiously because the closest
   COPI/COPII/Golgi anchors were FDR-flat; their top whole-profile neighbors
   were not biologically coherent ER-Golgi genes and did not justify inventing
   a broad secretory-pathway module.

## Target-specific reasoning

### Gbf1

GBF1 is a cis-Golgi and vesicular-tubular-cluster ARF guanine-nucleotide
exchange factor. Cell-biological perturbations place it upstream of ARF1/ARF4
activation and COPI recruitment at the ER-Golgi interface: GBF1 recruitment is
needed for COPI association with pre-Golgi intermediates, anti-GBF1 antibodies
or GBF1 depletion disperse COPI, and GBF1 is the cis-Golgi ARF-GEF separated
from BIG1/BIG2 function at the trans-Golgi network. Those roles were defined by
Garcia-Mata et al. 2003, Zhao et al. 2006, Szul et al. 2007, and Manolea et al.
2007; Jackson 2014, Kaczmarek et al. 2017, and Sager et al. 2021 summarize the
ARF1/COPI GEF-effector model and dynamic GBF1-mediated ARF1 activation.

The direct within-assay analogs were much more informative than the generic
"Golgi essential gene" label. `Copa` and `Copg1`, two assayed COPI coatomer
subunits downstream of GBF1/ARF1, produced 0 and 1 DEGs in the focal neurons.
The one `Copg1` hit was `Copg1` itself, not an ER-stress or secretory-pathway
response. Other cis-Golgi or ER-Golgi comparators were also flat: `Stx5a`,
`Trip11`, `Tmem165`, `Cog4`, and `Cog5` were all 0, and the COPII/ER-exit
targets `Sec23a`, `Sar1b`, and `Tfg` were 0. The same-experiment Distributed Agents
corpus explicitly summarizes this pattern in two relevant claims:

- Represented ER-Golgi trafficking and Golgi glycosylation-homeostasis
  perturbations do not form a shared broad secretory-pathway transcriptional
  module in postmitotic neurons (`Cog4`, `Copa`, `Copg1`, `Stx5a`, `Tmem165`,
  `Trip11`; moderate-confidence claim).
- Represented COPII initiation or ER-exit nodes `Tfg`, `Sec23a`, and `Sar1b`
  are transcriptionally buffered in this neuronal assay, unlike the smaller
  ER-stress response after `Sec63` perturbation.

The main positive counterexamples were useful but less direct. `Sec63` had 11
DEGs and was a local ER-client-handling/UPR hit; `Atp2a2`, `Dhdds`, `Hspa5`,
and `Gfpt1` recovered much broader ER quality-control or ISR states. GBF1 can
block or slow trafficking when acutely inhibited in cell culture, but the
training data show that the juvenile sparse CRISPR snRNA-seq assay does not
convert every early secretory defect into a durable `Hspa5`/`Ddit3`/`Chac1`
program. `Vps54`, `Vps35`, `Caml`, and `Pitpna` gave small 17 to 31 DEG
responses, but these signatures centered on GARP/retromer, CAML, or PITP
biology rather than on a shared COPI-collapse module; the corpus also notes
that Golgi and retrograde trafficking perturbations do not collapse into a
generic neuronal stress state.

My zero/nonzero decision is therefore weakly nonzero but at singleton scale. I
expect GBF1 loss to be at least as central as a single COPI subunit and
`Gbf1` itself is in the measured gene set, so one FDR hit from the target RNA
or a single immediate trafficking-stress transcript is plausible. I do not
expect the perturbation to cross into the 10 to 50 DEG GARP/retromer range, and
I definitely do not expect the 100+ DEG ER-stress/ISR programs seen after
`Atp2a2`, `Dhdds`, or `Gfpt1`.

Predicted `n_degs` for `Gbf1`: 1.

## Limits and extrapolation

`Gbf1` itself is held out, and no represented training perturbation is a true
GBF1 paralog or the exact upstream ARF-GEF node. COPI subunits are the closest
downstream biochemical analogs, but knocking out a coatomer subunit is not the
same as partial GBF1 loss: GBF1 can have COPI-independent ARF functions, and
direct GBF1 inhibition in proliferating cultured cells can have sharper effects
than sparse postnatal AAV-CRISPR editing in neurons. Conversely, complete GBF1
loss could be poorly tolerated and therefore depleted from the assayed nuclei,
which would flatten the transcriptomic endpoint rather than broaden it. The
prediction is consequently an extrapolation from several near-zero ER-Golgi
neighbors and small trafficking counterexamples, with the exact distinction
between 0 and 1 DEGs driven mostly by whether `Gbf1` target-RNA depletion
itself clears FDR in this cell group.
