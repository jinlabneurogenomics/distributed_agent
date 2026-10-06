# Reasoning trace

## Question

The held-out endpoint is the number of genes with `pvals_adj < 0.05` after
knocking out the requested gene in `151 TH Prkcd Grin2c Glut` cells. The only
requested target in
`[local file: 168_Pcdh15.csv]`
was `Pcdh15`. I therefore made one point prediction:

- `0` means no measured gene, including the `Pcdh15` transcript itself, is
  expected to pass the Wilcoxon BH FDR cutoff.
- A value of `1` would usually mean a self-transcript-only response in this
  neighborhood of genes, because most structurally related training
  perturbations had no significant downstream genes.

The endpoint is an assay-specific response breadth, not a measure of editing
success or biological essentiality, so I treated target-RNA depletion and
downstream transcriptional remodeling separately.

## Sources used

- `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`: observed FDR<0.05 DEG
  counts for all non-held-out training perturbations in the focal cell group.
- `training_de_all_cell_groups.parquet`: focal-cell per-gene DE rows for the
  nearest represented adhesion and synaptic-recognition perturbations.
- Distributed Agents corpus release
  `perturbai-july-260713-sourceguard-1773-v1`: same-experiment, perturbation
  centered findings for `Pcdh19`, `Ncam1`, `Dscam`, `Nrxn1`, and `Cntnap2`.
  This release had no direct `Pcdh15` claim or finding.
- Distributed Agents runtime profile-neighbor analysis over the focal-cell
  `logfoldchanges`, comparing each selected adhesion anchor with all 1,674
  eligible training perturbations across the 17,259 focal-cell measured genes.
- PubMed literature for public `PCDH15` biology:
  - Ahmed et al. 2001, PMID 11398101, DOI 10.1086/321277: mutations in
    `PCDH15` cause Usher syndrome type 1F and the mouse ortholog is the
    Ames-waltzer deafness/vestibular gene.
  - Kazmierczak et al. 2007, PMID 17805295, DOI 10.1038/nature06091: CDH23
    and PCDH15 interact in trans to form inner-ear hair-cell tip links.
  - Dionne et al. 2018, PMID 30057206, DOI 10.1016/j.neuron.2018.07.006:
    PCDH15 forms a specialized cis-dimeric extracellular architecture needed
    for hair-cell mechanotransduction.
  - Webb et al. 2011, PMID 21427143, DOI 10.1242/dev.060061, and Cosgrove and
    Zallocchi 2013, PMID 24239741, DOI 10.1016/j.biocel.2013.11.001:
    PCDH15 isoforms and Usher-protein complexes act at hair-cell bundle links
    and photoreceptor specializations.
  - Mori et al. 2024, PMID 38806495, DOI 10.1038/s41398-024-02952-6:
    germline mouse `Pcdh15` deficiency can affect locomotor/body-temperature
    behaviors and brain c-Fos patterns, showing that the gene is not
    absolutely sensory-only, but those phenotypes were assayed after organismal
    deletion rather than sparse P16 postmitotic neuronal editing.

## Dataset computations

I first calibrated the focal-cell endpoint distribution from the training count
CSV. Among 1,674 training targets, 1,205 had `0` DEGs, 469 had any nonzero
response, the median was `0`, the 75th percentile was `1`, the 90th percentile
was `2`, the 95th percentile was `18`, and the maximum was `2,677`.

I then queried the focal rows of the parquet for structurally or
synaptically-related training targets:

```python
filt = (
    ds.field("group_name") == "151 TH Prkcd Grin2c Glut"
) & pc.field("gene_target").isin(anchors)
table = dataset.to_table(
    columns=["gene_target", "names", "logfoldchanges", "pvals_adj"],
    filter=filt,
)
```

This pulled 207,108 DE rows for 12 anchors, corresponding to 17,259 measured
genes per anchor. I also ran the Distributed Agents profile-neighbor tool on the same
focal-cell `logfoldchanges`, with the 1,674 training targets as the eligible
node universe, to ask whether any of these anchors had a hidden all-gene
neighbor with a broader response.

### Focal-cell adhesion and synaptic-recognition anchors

| training perturbation | focal `n_degs` | exact focal evidence |
|---|---:|---|
| `Pcdh19` | 0 | Only `Pcdh*` training target. The self row was down but entirely nonsignificant: `log2FC = -0.448`, `pvals_adj = 1.0`. The Distributed Agents corpus reported no downstream DE anywhere for `Pcdh19` and no robust cadherin/Wnt/GABA/synaptic signature. Its top focal all-logFC neighbors were also null or one-DEG targets: `Pi4kb` 1, `Tcf12` 0, `Adgrl2` 1, `Nrg1` 0, `Il17rd` 0. |
| `Dscam` | 0 | A large IgSF adhesion/axon-guidance gene. The focal self row was subthreshold, `log2FC = -0.419`, `pvals_adj = 0.0897`, and no gene passed FDR 0.05. Distributed Agents findings describe `Dscam` as globally buffered across 21 recovered neuronal groups despite a self-transcript drop in this same 151 group. |
| `Ncam1` | 1 | FDR support was self-transcript only in this cell group: `Ncam1`, `log2FC = -0.746`, `pvals_adj = 3.00e-10`. Distributed Agents reported no FDR<0.10 downstream gene for `Ncam1` in any measured group, despite negative self-transcript movement. |
| `Cntnap1` | 1 | Self-transcript-only in the focal group: `Cntnap1`, `log2FC = -0.822`, `pvals_adj = 1.09e-11`. |
| `Cntnap2` | 1 | Self-transcript-only in the focal group: `Cntnap2`, `log2FC = -1.087`, `pvals_adj = 7.90e-06`. Distributed Agents findings showed no convergence with the related `Cntnap1`/Kv1 juxtaparanodal complex. |
| `Nrxn1` | 1 | Self-transcript-only in the focal group: `Nrxn1`, `log2FC = -0.518`, `pvals_adj = 2.67e-23`. Distributed Agents described `Nrxn1` as a sparse, transcriptomically isolated presynaptic adhesion perturbation. |
| `Nrxn2` | 0 | Self row `log2FC = -0.129`, `pvals_adj = 1.0`; no focal DEGs. |
| `Nrxn3` | 0 | No self row was present among the 17,259 focal features and no focal DEGs were called. |
| `Nlgn3` | 1 | Self-transcript-only in the focal group: `Nlgn3`, `log2FC = -0.896`, `pvals_adj = 4.79e-11`. |
| `Lrrtm1` | 1 | One non-self hit, `R3hdm2` up with FDR 0.0269; the `Lrrtm1` self row was not significant (`pvals_adj = 1.0`). |
| `Lrrtm3` | 0 | Self row `log2FC = -0.320`, `pvals_adj = 1.0`; no focal DEGs. |
| `Lrrtm4` | 0 | Self row `log2FC = -0.070`, `pvals_adj = 1.0`; no focal DEGs. |

Two controls against over-generalizing this table mattered:

- The same gene family is a better guide than generic adhesion. `Ncam1`,
  `Cntnap1`, `Cntnap2`, `Nrxn1`, and `Nlgn3` reached `1` because their own
  transcripts were well detected and depleted; they did not reveal a shared
  secondary adhesion program. `Pcdh19`, the only observed protocadherin target,
  did not even pass the self-transcript threshold in this cell group.
- The focal `Pcdh19` whole-logFC neighbor set did not nominate a high-DEG
  phenocopy. Top Pearson neighbors had focal counts of `0` or `1`, and
  Distributed Agents' same-experiment `Pcdh19` review rejected hidden cadherin,
  Wnt/beta-catenin, GABA receptor, or epilepsy modules after centering the
  all-group logFC surface.

## Target-specific reasoning

### `Pcdh15`

`Pcdh15` is a protocadherin-family adhesion molecule, but its best-established
loss-of-function biology is not a broadly expressed brain nuclear-RNA program.
Human `PCDH15` mutations cause Usher syndrome type 1F, and mouse `Pcdh15` was
identified as the Ames-waltzer deafness/vestibular gene (Ahmed et al. 2001).
In the inner ear, PCDH15 and CDH23 are the lower and upper components of the
hair-cell tip link, and PCDH15 dimerization and cytoplasmic-domain isoforms are
specialized for the mechanical apparatus of stereocilia (Kazmierczak et al.
2007; Webb et al. 2011; Dionne et al. 2018). Usher complexes also function in
photoreceptor calyceal/synaptic compartments (Cosgrove and Zallocchi 2013).

Those mechanisms make `Pcdh15` a plausible sensory-cell structural gene, but
they are weak priors for a persistent somatic transcriptome in the requested
assay: sparse AAV CRISPR starting at P16 in NeuN+ whole-brain neurons, harvested
3-4 weeks later. The germline `Pcdh15` mouse study by Mori et al. 2024 argues
that the gene can influence brain circuits, yet that is a systemic developmental
knockout with circuit and c-Fos readouts, not a single-cell nuclear RNA
phenotype in already specified thalamic glutamatergic neurons.

The within-dataset evidence points to a zero rather than to a broad nonzero
count:

- The only training protocadherin perturbation, `Pcdh19`, had `0` DEGs in
  `151 TH Prkcd Grin2c Glut`. Its own mRNA was weakly lower but not close to
  significant (`log2FC -0.448`, FDR `1.0`), so another non-clustered
  protocadherin was not guaranteed even a self-only count.
- Multiple training membrane-adhesion perturbations that are more canonical in
  CNS synaptic organization, including `Dscam`, `Nrxn2`, `Nrxn3`, `Lrrtm3`,
  and `Lrrtm4`, were exactly `0`; `Ncam1`, `Nrxn1`, `Cntnap1`, `Cntnap2`, and
  `Nlgn3` were `1` only because the target transcript itself was significant.
- Same-experiment Distributed Agents corpus findings for `Pcdh19`, `Dscam`, `Ncam1`,
  `Nrxn1`, and `Cntnap2` repeatedly found that postnatal sparse perturbation of
  adhesion, IgSF-CAM, neurexin/neuroligin, and CASPR/Kv-related structural
  genes does not collapse into a shared adjusted nuclear-mRNA module.
- Focal all-gene profile-neighboring of `Pcdh19` and the other adhesion anchors
  did not replace these biological priors with a stronger high-DEG analog:
  nearby signatures were mostly zero/one-DEG perturbations, and the leading
  shared features for the flat anchors were not themselves FDR-supported.

I therefore predicted that `Pcdh15` will look most like the zero-count
protocadherin and buffered adhesion targets rather than like a self-transcript
only hit. The point prediction is `0`.

## Limits

The largest uncertainty is whether the `Pcdh15` guide pool happened to lower
the `Pcdh15` transcript strongly enough in this focal cell group to create a
single self DEG. The training data show both sides of that boundary:
`Ncam1`, `Nrxn1`, `Cntnap1`, `Cntnap2`, and `Nlgn3` were self-only positives,
whereas `Pcdh19`, `Dscam`, `Nrxn2`, `Lrrtm1`, `Lrrtm3`, and `Lrrtm4` had
nonsignificant self rows. I put `Pcdh15` with the latter group because its
known biology is hair-cell/photoreceptor-specialized and the observed
protocadherin perturbation, `Pcdh19`, was not self-significant here.

This prediction also extrapolates across nonidentical molecules. The closest
mechanistic `Pcdh15` partners, such as `Cdh23`, `Ush1c`, `Ush1g`, `Myo7a`,
`Clrn1`, `Lhfpl5`, `Tmc1`, and `Tmc2`, were present as measured features but
not as represented training perturbations in the focal count CSV, so I could
not directly test an Usher/tip-link perturbation neighborhood. The assay does
not measure tip-link assembly, hair-cell mechanotransduction, photoreceptor
outer-segment morphology, synaptic localization, axonal wiring, or behavior,
and a true local protein phenotype could be completely RNA-silent at the
single-nucleus FDR threshold.
