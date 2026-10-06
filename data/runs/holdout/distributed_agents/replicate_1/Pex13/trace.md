# DEG-count prediction trace

## Question and endpoint

The requested prediction is the integer number of genes expected to pass
Benjamini-Hochberg FDR 0.05 after acute AAV-CRISPR loss of each held-out target
in `151 TH Prkcd Grin2c Glut` neurons. The single held-out target in this run is
`Pex13`. I treated the requested count as the exact focal-cell `n_degs` endpoint
in the supplied training CSV: all measured genes with `pvals_adj < 0.05`,
including the perturbed transcript itself if it is called significant.

The `Pex13` signature and count are absent by construction. The directly
observed sources are the training DEG-count CSV and the
`training_de_all_cell_groups.parquet` differential-expression table. External
peroxisome biology is therefore a prior for choosing legitimate training
analogs, not an independent measurement of this Perturb-seq endpoint.

## Sources used

- Declared Perturb-seq Parquet:
  `training differential-expression dataset`.
- Focal-cell training DEG counts:
  `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
- Requested held-out manifest:
  `single-target request for Pex13`.
- Run-local dataset portrait, task bindings, measurement registry, compact
  coverage, and capability manifest.
- Internal same-experiment semantic corpus: PerturbAI July
  `july_260713_sourceguard_1773_v1` Findings/Evidence/Reference ledgers,
  queried for `Pex1`, `Pex14`, `Abcd3`, `Acbd5`, and `Hsd17b4`.
- External mechanism references:
  Reactome, Peroxisomal protein import, `R-HSA-9033241`;
  Braverman et al., GeneReviews Zellweger Spectrum Disorder, updated 2020;
  Bjorkman, Gould and Crane 2002, DOI `10.1006/geno.2002.6697`;
  Liu, Ma and Subramani 2012, DOI `10.1016/j.ceb.2012.05.003`;
  Berger et al. 2016, PMID `26686055`;
  Abe et al. 2018, PMID `30519675`;
  Law et al. 2017, DOI `10.1080/15548627.2017.1291470`;
  Gao, Skowyra, Feng and Rapoport 2022, DOI
  `10.1126/science.adf3971`;
  Demers et al. 2023, DOI `10.1080/15548627.2022.2160566`;
  Ravindran et al. 2023, DOI `10.1038/s41586-023-06044-1`;
  Gaussmann et al. 2024, DOI `10.1038/s41467-024-47605-w`.

## Computation over the declared data

The endpoint distribution in the supplied focal training count table is heavily
zero-inflated:

| quantity | value |
|---|---:|
| training targets | 1674 |
| targets with `n_degs == 0` | 1205 |
| fraction nonzero | 0.280 |
| median | 0 |
| 75th percentile | 1 |
| 90th percentile | 2 |
| 95th percentile | 18 |
| median among nonzero targets | 1 |

I then selected represented peroxisome biogenesis and peroxisome-linked
training perturbations by gene function and read their focal `n_degs` from the
training CSV:

| training perturbation | relationship to `Pex13` | focal `n_degs` |
|---|---|---:|
| `Pex14` | PEX5 docking/importomer partner with PEX13 | 1 |
| `Pex1` | AAA ATPase for PEX5 recycling, same matrix-protein import cycle but farther from the docking pore | 0 |
| `Abcd3` | peroxisomal fatty-acid transporter, downstream metabolic arm | 0 |
| `Acbd5` | peroxisome-ER tether and VLCFA-handling factor | 0 |
| `Hsd17b4` | peroxisomal beta-oxidation enzyme | 0 |
| `Mff` | peroxisome/mitochondrial fission factor | 0 |
| `Agps` | ether-lipid synthesis, indirect peroxisome metabolic comparator | 1 |
| `Far1` | ether-lipid synthesis, indirect peroxisome metabolic comparator | 2 |

I queried the Parquet for these targets in `151 TH Prkcd Grin2c Glut` and
counted `pvals_adj < 0.05` as a check against the training CSV. The only
significant rows in this set were:

| perturbation | significant focal row | log2 fold-change | adjusted p |
|---|---|---:|---:|
| `Pex14` | `Pex14` | -0.907 | 3.74e-7 |
| `Agps` | `Dhcr24` | 0.660 | 0.00192 |
| `Far1` | `Far1` | -0.438 | 0.00313 |
| `Far1` | `Tial1` | 0.247 | 0.0243 |

Thus `Pex14`, the nearest measured pore/docking comparator for `Pex13`, had no
significant downstream focal gene; its singleton FDR 0.05 call was the
`Pex14` transcript. `Pex1` had no focal FDR 0.05 gene. Score-vector Pearson
correlations across all measured focal genes were also at the noise floor for
the peroxisome set: `Pex1` versus `Pex14` was 0.013, `Pex14` versus `Abcd3` was
0.092, `Pex14` versus `Acbd5` was 0.095, and `Pex14` versus `Hsd17b4` was
0.030. I used Wilcoxon `scores` rather than log-fold-change vectors for this
check because extreme pseudocount-driven log-fold changes among genes with no
statistical support create a shared floor that is not biological.

The internal PerturbAI Findings/Evidence corpus provided the same-experiment
interpretation of these Parquet surfaces. It reported that acute `Pex1`
perturbation failed to induce peroxisome-import, lipid/redox, pexophagy,
autophagy, integrated-stress-response, or UPR transcripts across measured
neuronal classes; a prespecified 49-gene program covering those pathways
yielded 0/1029 rows at FDR 0.10. For `Pex14`, a 45-gene panel spanning
peroxisome biogenesis, lipid metabolism, redox, ISR, autophagy/lysosome, and
BDNF-TrkB transcripts yielded 0/1035 non-`Pex14` gene-by-cell-group rows at
FDR 0.10. The corpus also reported that `Abcd3`, `Acbd5`, and `Hsd17b4`
perturbations were flat across recovered neuronal groups and did not expose a
hidden common peroxisome RNA module.

## Target-specific reasoning

### `Pex13`

`Pex13` is a peroxisomal membrane factor in the PEX5/PEX7 matrix-protein import
machinery. Mouse Pex13 encodes a peroxisomal SH3-containing membrane protein
closely homologous to human PEX13 (Bjorkman, Gould and Crane 2002), and
Reactome places PEX13 and PEX14 at the peroxisomal cargo docking/import pore,
with PEX5/PEX7 receptors upstream and PEX1/PEX6/PEX26 recycling ubiquitinated
PEX5 downstream. Biochemical work supports a direct PEX13 relationship to
PEX5-cargo and PEX14: PEX13 forms the YG-domain selective phase used by PEX5
for folded protein import (Gao et al. 2022), PEX13/PEX5 and PEX14 can assemble
dynamic import condensates (Ravindran et al. 2023), and the PEX13 SH3 domain
uses diaromatic motifs to modulate PEX5 and PEX14 binding (Gaussmann et al.
2024). PEX13 also has a quality-control role: loss of PEX13 can accumulate
ubiquitinated PEX5, increase peroxisome-dependent ROS, and promote pexophagy in
cultured cells and zebrafish (Demers et al. 2023).

The causal chain expected from acute `Pex13` CRISPR in recovered thalamic
glutamatergic neurons is:

`Pex13` editing -> impaired peroxisomal matrix import at the PEX5/PEX14 docking
channel and potentially altered Ub-PEX5/pexophagy balance -> peroxisomal lipid,
redox, and organelle-turnover changes -> possible nuclear lipid-stress,
oxidative-stress, BDNF-TrkB, ISR/UPR, autophagy, or lysosomal transcription ->
survival and recovery of edited neurons -> Wilcoxon DEG count.

Two represented perturbations test the import part of that chain. `Pex14`
occupies the same docking/importomer step as `Pex13`; if partial postmitotic
loss of the import pore triggered a broad nuclear peroxisome stress program,
`Pex14` was the best available positive analog. Its focal `n_degs` was only
one, and the only FDR 0.05 focal row was `Pex14` itself. The same-experiment
corpus showed no downstream peroxisome/import, lipid, redox, ISR, autophagy, or
BDNF-TrkB module after `Pex14` in any measured neuronal group. `Pex1` is
mechanistically farther from `Pex13` but still in the PEX import cycle through
AAA-complex extraction of ubiquitinated PEX5. It had `n_degs = 0` in the focal
group and only two isolated singleton FDR 0.10 calls in other neuronal classes;
the expected 49-gene peroxisome/stress panel was completely FDR-flat.

The represented metabolic and organelle comparators were counterexamples to a
generic "peroxisome genes are transcriptomically broad" rule. `Abcd3`,
`Acbd5`, `Hsd17b4`, and `Mff` each had `n_degs = 0` in the focal group, while
`Agps` and `Far1` had only one and two focal hits. `Agps` affected `Dhcr24`;
`Far1` affected `Far1` and `Tial1`. Those singleton patterns do not resemble a
shared import-defect state and do not support inflating `Pex13` above the
`Pex14`/`Pex1` floor.

External biology says that severe congenital PEX defects are important in brain
development and peroxisome biogenesis disease: Zellweger spectrum disorders are
caused by biallelic PEX defects (Braverman et al. 2020, GeneReviews), and a
Pex14-defective mouse can disrupt cortical/cerebellar development with altered
BDNF-TrkB signaling (Abe et al. 2018). I did not treat those effects as a
large-DEG prior here because they occur in lifelong, developmental, or
non-sparse peroxisome deficiency, whereas the requested assay edits sparse
postmitotic NeuN-positive neurons from P16 to P37-P44 and observes only nuclear
RNA in recovered cells. Within that exact assay, the best import analog
`Pex14` did not turn the BDNF-TrkB or stress prior into detectable downstream
DE.

I therefore predict a transcriptional null for `Pex13` in `151 TH Prkcd Grin2c
Glut`, with zero genes passing FDR 0.05. The point prediction is driven mostly
by within-dataset evidence from `Pex14` and `Pex1`, with external literature
used to justify that these are true core-import analogs rather than superficial
gene-family matches.

## Limits and uncertainty

The largest ambiguity is the self-transcript contribution. `Pex14` had one
focal DEG only because its own mRNA was significantly depleted, while `Pex1`
did not show a significant self-transcript. The held-out `Pex13` self row is
unobserved, so the predicted difference between 0 and 1 could hinge on
`Pex13` transcript abundance, guide editing outcomes, nonsense-mediated decay,
and the number of recovered edited nuclei rather than on a downstream
peroxisome program.

The Parquet measures nuclear RNA after 3-4 weeks in recovered nuclei. It cannot
directly assess PEX13 protein, peroxisomal catalase import, PTS1/PTS2 cargo
mislocalization, ubiquitinated PEX5, peroxisome number, VLCFA/plasmalogen
metabolites, ROS, or selection before nuclei were recovered. Thus the zero
prediction is a prediction about FDR-significant snRNA-seq genes in this focal
class, not a claim that `Pex13` editing is biochemically inert.

Finally, most exact PEX13-neighborhood perturbations, including `Pex5`,
`Pex6`, `Pex10`, `Pex12`, `Pex26`, and the withheld `Pex13` itself, were not
available as focal training counts. The prediction extrapolates from the
observed `Pex14` docking factor and the farther `Pex1` AAA factor, and that
could miss a PEX13-specific pexophagy or PEX5-ubiquitination response.

## Final point prediction

| target | predicted `n_degs` |
|---|---:|
| `Pex13` | 0 |
