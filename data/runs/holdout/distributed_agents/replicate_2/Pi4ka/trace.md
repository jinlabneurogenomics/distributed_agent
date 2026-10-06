# Reasoning trace

## Question and interpretation

The held-out target manifest for this run contains one requested perturbation:
`Pi4ka`. I interpreted the endpoint as the exact same scalar in
`151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`: the number of measured
genes in `151 TH Prkcd Grin2c Glut` whose Wilcoxon Benjamini-Hochberg adjusted
`pvals_adj` is below 0.05. I counted the target transcript itself when it was
significant in training, because the supplied `n_degs` values do so: for
example, `Synj1` and `Dgke` each have `n_degs=1` in this cell group and the only
FDR<0.05 row is the perturbed transcript.

The prediction is therefore a point estimate of the hidden PI4KA CRISPR
signature in the same acute, sparse, P16-to-P37/P44 neuronal Perturb-seq assay,
not an estimate of full-germline Pi4ka essentiality, cell survival, or lipid
turnover.

## Sources

- Supplied focal training counts:
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
- Supplied all-cell differential-expression parquet:
  `[local file: training_de_all_cell_groups.parquet]`.
- Supplied held-out manifest:
  `[local file: 177_Pi4ka.csv]`.
- Distributed Agents same-experiment corpus `perturbai-july-260713-sourceguard-1773-v1`,
  especially the target reports for `Pi4kb`, `Pitpna`, `Synj1`, `Ocrl`,
  `Pik3cb`, and `Pik3r1`.
- Distributed Agents runtime profile comparison over the eight represented focal-cell
  phosphoinositide candidates `Pi4kb`, `Pitpna`, `Ocrl`, `Synj1`, `Pik3cb`,
  `Pik3r1`, `Inpp5k`, and `Pitpnm3`.
- PubMed-indexed external biology for PI4KA/PI4P mechanisms:
  - Balla 2013, `Phosphoinositides: tiny lipids with giant impact on cell
    regulation`, DOI `10.1152/physrev.00028.2012`, PMID `23899561`.
  - Boura and Nencka 2015, `Phosphatidylinositol 4-kinases: Function,
    structure, and inhibition`, DOI `10.1016/j.yexcr.2015.03.028`, PMID
    `26183104`.
  - Nakatsu et al. 2012, `PtdIns4P synthesis by PI4KIIIalpha at the plasma
    membrane and its impact on plasma membrane identity`, DOI
    `10.1083/jcb.201206095`, PMID `23229899`.
  - Baskin et al. 2015, `The leukodystrophy protein FAM126A (hyccin) regulates
    PtdIns(4)P synthesis at the plasma membrane`, DOI `10.1038/ncb3271`, PMID
    `26571211`.
  - Salter et al. 2021, `Biallelic PI4KA variants cause neurological,
    intestinal and immunological disease`, DOI `10.1093/brain/awab313`, PMID
    `34415310`.

## Computational calibration

I first checked the focal training-count distribution. It is highly zero
inflated: among 1,674 non-held-out targets, 1,205 had `n_degs=0`, 276 had
`n_degs=1`, 87 had `n_degs=2..9`, 47 had `n_degs=10..49`, and 59 had at least
50. Thus a single lipid-signaling gene needs strong matched analog evidence to
be moved from an assay-floor prediction into the broad-response tail.

I then intersected the focal training count table with hand-nominated
phosphoinositide and PI4P/PIP2 pathway genes. The represented PI-relevant
targets and observed focal counts were:

| training target | focal `n_degs` | relevance to `Pi4ka` |
| --- | ---: | --- |
| `Pi4kb` | 1 | Type III PI 4-kinase paralog; Golgi rather than plasma-membrane PI4P producer. |
| `Pitpna` | 21 | Phosphatidylinositol transfer protein that can feed PI4P/PIP2 synthesis, but not a PI4K paralog. |
| `Synj1` | 1 | PI(4,5)P2/PI phosphatase for synaptic vesicle uncoating. |
| `Dgke` | 1 | PI-cycle diacylglycerol kinase; singleton was only self-transcript knockdown. |
| `Ocrl` | 0 | PI(4,5)P2/PI4P 5-phosphatase in endocytic/Golgi compartments. |
| `Inpp5k` | 0 | ER-associated inositol 5-phosphatase. |
| `Pitpnm3` | 0 | PITPNM/RdgB-family lipid-transfer protein, more distant than PITPNA. |
| `Pik3cb` | 0 | Class IA PI3K catalytic subunit, PIP3 rather than PI4P synthesis. |
| `Pik3r1` | 0 | Class IA PI3K regulatory subunit. |
| `Pik3r2` | 0 | Class IA PI3K regulatory subunit. |
| `Plcb1` | 0 | PI(4,5)P2-consuming PLC-beta. |

For the closest rows I read the `151 TH Prkcd Grin2c Glut` slice of the
parquet directly. The effective focal sample sizes and FDR<0.05 observations
were:

- `Pi4kb`, 162 perturbed nuclei: one FDR<0.05 gene, `Tmem50b` up
  with logFC `0.426`, FDR `0.028`; `Rnf145` was suggestive but did not pass the
  endpoint cutoff, logFC `0.538`, FDR `0.069`; the `Pi4kb` self row was not
  significant, logFC `-0.316`, FDR `1`.
- `Pitpna`, 189 perturbed nuclei: 21 FDR<0.05 genes. Besides `Pitpna` itself
  being reduced, logFC `-0.788`, FDR `2.48e-16`, the signature contained
  down-regulated `Prkcg`, `Atp2a2`, `Gabra4`, `Ankfy1`, and `Cpne7` and
  up-regulated `Rreb1`, `Scg2`, `Kctd16`, and `Stmn4`, consistent with a small
  synaptic/Ca2+/secretory/cytoskeletal response rather than a pure PI4K
  signature.
- `Synj1`, 90 perturbed nuclei: one FDR<0.05 gene, `Synj1` itself
  down-regulated, logFC `-0.583`, FDR `3.11e-07`; there was no downstream
  response in the focal cell group.
- `Dgke`, 225 perturbed nuclei: one FDR<0.05 gene, `Dgke` itself
  down-regulated, logFC `-0.586`, FDR `5.97e-08`.
- `Ocrl`, `Inpp5k`, `Pitpnm3`, `Pik3cb`, `Pik3r1`, and `Plcb1` had no focal
  FDR<0.05 rows.

I also asked the Distributed Agents runtime to compare the eight represented
phosphoinositide candidates in the focal cell group with `pvals_adj<0.05` as
the significant-feature threshold. Across the 28 candidate pairs there was no
same-direction overlap of FDR-significant genes in either the positive or
negative programs. `Pi4kb` and `Pitpna` were explicitly connected in the
same-experiment corpus, but reciprocally as non-convergent comparators: the
`Pi4kb:F005` finding reports that measured phosphoinositide and PI4KB-adjacent
targets did not converge on `Pi4kb`, while `Pitpna:F008` reports that measured
PI-transfer, PI4P-turnover, PLC, and PKC perturbations did not phenocopy
`Pitpna`.

## Target-specific reasoning

### `Pi4ka`

External mechanism. PI4KA/PI4KIIIalpha is the plasma-membrane type III
phosphatidylinositol 4-kinase that makes a major PM PI4P pool; this PI4P both
contributes to membrane identity and feeds PI(4,5)P2 synthesis. PI4Ks are central
enzymes for Golgi/TGN and plasma-membrane PI4P metabolism (Balla 2013; Boura
and Nencka 2015), and PI4KA is recruited to the plasma membrane by an EFR3,
TTC7, and FAM126 complex (Nakatsu et al. 2012; Baskin et al. 2015). Human
biallelic PI4KA variants can cause neurological, intestinal, and immunological
disease through impaired PI4KIIIalpha-TTC7-FAM126 function (Salter et al.
2021). This made a true nonzero neuronal effect more plausible than for a
random target.

Within-dataset analogs. The best measured enzymatic analog, `Pi4kb`, was tiny
rather than broad in the focal cell group: only `Tmem50b` crossed FDR<0.05, and
`Rnf145` sat just above threshold. The best measured phosphatidylinositol
supply analog, `Pitpna`, did produce 21 focal DEGs, but the same-experiment
Distributed Agents report showed that it did not phenocopy `Pi4kb`, `Ocrl`, `Synj1`,
`Plcb1`, `Prkca`, `Prkcg`, or `Pitpnm3`; its 151-cell response looks like a
PITPNA-specific mixed synaptic/Ca2+/secretory/cytoskeletal adjustment, not a
generic consequence of reducing any node in the PI4P/PIP2 cycle. Downstream or
parallel lipid-signaling perturbations supplied mostly counterexamples:
`Synj1` and `Dgke` had only self-transcript singletons, while `Ocrl`, `Inpp5k`,
`Pitpnm3`, `Pik3cb`, `Pik3r1`, `Pik3r2`, and `Plcb1` were zero in the focal
count table.

Decision. I predict a nonzero but assay-floor focal response. The nonzero call
comes more from external PI4KA biology and the fact that both `Pi4kb` and
`Pitpna` were detectable in `151 TH Prkcd Grin2c Glut` than from any strong
shared expression module. The magnitude is pulled down by the focal training
data: the represented pathway members do not share a significant transcriptomic
program at FDR<0.05, the PI4KB paralog produced just one significant gene, and
most phosphoinositide/endocytic relatives were flat under the same sparse
postnatal CRISPR regime. I therefore placed `Pi4ka` nearest to a `Pi4kb`-like
singleton rather than to the 21-gene `Pitpna` state.

Point prediction: `Pi4ka = 1`.

## Limits and extrapolations

- The most direct PI4KA plasma-membrane complex partners, `Efr3a`, `Efr3b`,
  `Ttc7a`, `Ttc7b`, `Fam126a`, and `Fam126b`, were not represented in the focal
  training table, so no same-complex perturbation calibrated the expected DEG
  count.
- Other very direct lipid enzymes, including `Pi4k2a`, `Pi4k2b`, `Pip5k1a`,
  `Pip5k1b`, `Pip5k1c`, and `Pten`, were also absent as measured training
  perturbations.
- The parquet measures nuclear RNA, not PI4P, PI(4,5)P2, DAG/IP3, synaptic
  vesicle recycling, membrane identity, or protein localization. A real PI4KA
  phenotype could therefore be post-transcriptional and still score as zero or
  one DEG here.
- Literature disease contexts for PI4KA and the FAM126/TTC7/EFR3 complex
  involve development, oligodendrocytes, intestine, and immune cells as well as
  neurons. Those settings are only partially sampled by this NeuN-enriched
  juvenile mosaic assay.
- The point estimate assumes partial acute loss is buffered similarly to the
  represented phosphoinositide single-gene perturbations. If PI4KA protein loss
  were unusually efficient in this guide set, or if `151 TH Prkcd Grin2c Glut`
  cells are specifically dependent on plasma-membrane PI4P, the hidden count
  could move toward the `Pitpna` range.
