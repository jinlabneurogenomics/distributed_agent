# Ptcd3 prediction trace

## Question and resolved ambiguities

The requested readout is the integer number of genes with `pvals_adj < 0.05`
after each held-out perturbation in `151 TH Prkcd Grin2c Glut` cells.
The run manifest contains one held-out target:

```text
Ptcd3
```

`n_degs` in the supplied training count table includes the targeted transcript
itself if that row passes FDR. I therefore counted the `gene_target` row as part
of the endpoint when reviewing analogs. I treated the matched perturbation count
as power/context information only, not as a viability or editing-efficiency
readout.

The `Ptcd3` perturbation was absent from both training inputs as required. The
gene does appear as a measured transcript in other perturbation tables; I used
that only to verify that the symbol is in the measured gene universe, not as an
observation of the held-out `Ptcd3` knockout.

## Sources used

Direct training data:

- `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`
  for the exact `151 TH Prkcd Grin2c Glut` DEG counts of non-held-out
  perturbations.
- `[local file: training_de_all_cell_groups.parquet]`
  for focal-cell Wilcoxon scores, log2 fold changes, BH-adjusted p-values, and
  matched cell counts for mechanistic analogs.
- `[local file: 189_Ptcd3.csv]`
  for the requested target list.

Same-experiment interpretation:

- Distributed Agents corpus `perturbai-july-260713-sourceguard-1773-v1`, queried for
  `Ptcd3`, `Gfm2`, `Lrpprc`, `Rmnd1`, `Dap3`, and the phrases
  "mitochondrial translation" and "OXPHOS respiratory chain mitochondrial
  complex".

External biology:

- Davies et al. 2009, PMID 19427859, DOI `10.1016/j.febslet.2009.04.048`:
  PTCD3 is mitochondrial, associates with the mitochondrial small ribosomal
  subunit, and lowering PTCD3 in cultured cells reduced mitochondrial protein
  synthesis, respiration, and complex III/IV activity.
- Haque et al. 2011, PMID 22015679, DOI `10.1016/j.bbapap.2011.09.013`:
  PTCD3/MRPS39 is in the mammalian mitochondrial small subunit neighborhood
  contacted by mitochondrial IF3.
- Borna et al. 2019, PMID 30607703, DOI `10.1007/s10048-018-0561-9`, and
  Munoz-Pujol et al. 2022, PMID 36450274, DOI `10.1111/bpa.13134`:
  biallelic human PTCD3 variants cause a mitochondrial translation defect with
  combined oxidative-phosphorylation deficiency and Leigh/Leigh-like syndrome.
- Janer et al. 2012, PMID 23022098, DOI `10.1016/j.ajhg.2012.08.020`: RMND1
  loss causes multiple OXPHOS deficiencies and a mitochondrial translation
  defect, making `Rmnd1` a reasonable pathway comparator in the screen even
  though it is not a mitoribosomal protein.

## Computation over the input matrices

I loaded the focal-cell training counts and used Arrow predicate filtering of
the parquet with:

- `group_name == "151 TH Prkcd Grin2c Glut"`
- `gene_target` restricted to candidate mitochondrial translation or OXPHOS
  comparators.

For each comparator I counted rows with `pvals_adj < 0.05`, recorded the
matched perturbed and control nucleus counts, and inspected the top Wilcoxon
`scores` rather than using raw `logfoldchanges` for profile similarity. Several
nearly unexpressed genes have huge finite log2 fold changes with FDR 1.0, which
can make whole-vector logFC correlations look artificially high; Wilcoxon
scores gave the expected near-zero similarities among null profiles.

Overall focal-cell calibration from the training count table:

- 1,674 training perturbations were available.
- 1,205/1,674 had `n_degs = 0`.
- The median was 0, the 75th percentile was 1, the 90th percentile was 2, and
  only 43 perturbations were in the `>= 100` DEG class.

The relevant focal-cell counts were:

| target | `n_degs` in 151 | matched perturbed nuclei | focal-cell FDR pattern |
|---|---:|---:|---|
| `Gfm2` | 0 | 190 | no gene, including `Gfm2`, passed FDR |
| `Lrpprc` | 0 | 111 | best row was `Emc1`, FDR 0.174; `Lrpprc` self row was FDR 1.0 |
| `Rmnd1` | 0 | 175 | no significant rows |
| `Fars2` | 0 | 180 | no significant rows |
| `Lars2` | 0 | 256 | no significant rows |
| `Rars2` | 0 | 165 | no significant rows |
| `Dap3` | 1 | 223 | only `Dap3` itself passed, logFC -0.676, FDR 3.95e-6 |
| `Aimp1` | 0 | 199 | no significant rows; useful mostly as a negative RNA/translation-control neighbor, not as a direct mitochondrial comparator |
| `Ndufs2` | 1 | 197 | only `Ndufs2` itself passed |
| `Ndufa4` | 1 | 133 | only `Ndufa4` itself passed |
| `Sucla2` | 1 | 151 | only `Sucla2` itself passed |
| `Sod2` | 1 | 193 | only `Sod2` itself passed |
| `Coa8` | 0 | 194 | no significant rows |
| `Cox4i1` | 0 | 220 | no significant rows; self score -4.41 still FDR 0.176 |
| `Cox11` | 0 | 265 | no significant rows |
| `Opa1` | 37 | 195 | broad ATF4-like response, led by `Asns`, `Mars1`, `Chac1`, `Ddit3`, `Mthfd2`, `Slc7a5`, and the `Opa1` self row |

The score-based profile comparison among `Gfm2`, `Lrpprc`, `Rmnd1`, `Dap3`,
`Fars2`, `Lars2`, `Rars2`, `Opa1`, `Ndufs2`, `Coa8`, and `Cox4i1` supported the
same conclusion. Primary mitochondrial translation analogs had no shared FDR
features in the focal group, and pairwise whole-score correlations with each
other were tiny: for example `Gfm2` versus `Lars2`, `Rars2`, and `Opa1` had
Pearson correlations 0.021, 0.022, and 0.017. `Lrpprc` versus `Opa1` was only
0.046. The handful of positive/negative top-tail overlaps were all FDR 1.0
noise except where the `Opa1` stress program was present in `Opa1` alone.

The Distributed Agents same-experiment corpus agreed with that direct count-level
picture:

- It had no `Ptcd3` target report, so there was no direct held-out leakage or
  packaged hidden phenotype for `Ptcd3`.
- It summarized `Gfm2` as pan-surface downstream-null and explicitly contrasted
  it with the detectable `Opa1` ATF4/mitochondrial-stress program.
- It summarized `Lrpprc` as 0 downstream FDR<0.10 genes in 21 recovered
  neuronal groups, with mtDNA-coded mRNA and nuclear ISR/UPRmt marker programs
  absent.
- It summarized `Rmnd1` as 0 downstream FDR<0.10 genes in all 23 measured
  groups, again without ATF4/UPRmt induction.
- It summarized `Dap3` as downstream-null despite focal self-depletion and as
  failing to activate the `Opa1`-like `Asns`/`Ddit3`/`Chac1` stress module.
- Its higher-order mitochondrial-translation claim stated that represented
  mitochondrial aaRS and mitochondrial protein-synthesis perturbations
  (`Fars2`, `Gfm2`, `Lars2`, `Rars2`) were flat, singleton, or nonconvergent
  rather than forming a shared acute mitochondrial-stress module.

## Target-specific reasoning: `Ptcd3`

`Ptcd3` encodes PTCD3/MRPS39, a pentatricopeptide-repeat mitochondrial RNA
binding protein integrated into the small mitochondrial ribosomal subunit.
External work makes it a genuine mitochondrial translation gene: PTCD3
knockdown impairs mitochondrial protein synthesis and respiration in cultured
cells, and inherited PTCD3 deficiency produces combined OXPHOS defects with
Leigh-spectrum neurologic disease.

The relevant training analogs are therefore genes that perturb mitochondrial
translation or the immediate production of mtDNA-encoded OXPHOS proteins:

- `Dap3` is the closest represented structural analog because it is also a
  small-subunit mitoribosomal protein. In the focal group it gave `n_degs = 1`,
  and the one hit was `Dap3` itself. This is the strongest argument that a
  PTCD3 guide pool might produce a singleton self transcript if the mRNA is
  efficiently destabilized, but it is also a counterexample to any broad
  downstream mitochondrial-stress prediction.
- `Gfm2` acts at the mitochondrial ribosome during translation. It had
  `n_degs = 0` in the focal group, and the same-experiment corpus reported no
  robust downstream DE in 22 neuronal groups plus no `Opa1`-like ISR program.
  This is an appropriate process analog for a mitochondrial translation
  blockade that did not cross the snRNA-seq response threshold.
- `Fars2`, `Lars2`, and `Rars2` are mitochondrial aminoacyl-tRNA synthetases.
  Each had `n_degs = 0` in the focal group, and corpus summaries specifically
  rejected a shared acute mitochondrial protein-synthesis RNA module among the
  mt-aaRS comparators and `Gfm2`.
- `Rmnd1`, while not a ribosomal protein, is required for mitochondrial
  translation and OXPHOS complex assembly. It had `n_degs = 0` in the focal
  group and a pan-neuronal null in the corpus, so it supports the idea that
  severe textbook mitochondrial translation genes can be buffered in this
  acute P16 CRISPR neuronal assay.
- `Lrpprc` is a PPR-family mitochondrial RNA stabilizer upstream of
  mitochondrial translation. It had `n_degs = 0` in this focal cell group, and
  the expected mtDNA mRNA and ISR marker responses were absent in the
  same-experiment corpus. It is less structurally direct than `Dap3`, but it is
  a useful PTCD3-adjacent RNA-binding comparator because both couple
  mitochondrial transcripts to respiratory-chain biogenesis.

The important counterexample is `Opa1`: `Opa1` perturbation had 37 focal-cell
FDR<0.05 genes and a clear `Asns`/`Chac1`/`Ddit3`/`Mthfd2`/`Slc7a5` amino-acid
stress program. That response shows that `151 TH Prkcd Grin2c Glut` cells can
mount a mitochondrial-stress transcriptome under this assay, but the response
did not appear after `Dap3`, `Gfm2`, `Rmnd1`, `Lrpprc`, or mt-aaRS perturbations.
Core respiratory-chain genes gave the same boundary: several OXPHOS structural
targets had only self-transcript singletons, while `Coa8`, `Cox4i1`, `Cox11`,
and `Ndufv1` were zero.

I therefore predict that acute sparse `Ptcd3` loss will look like the buffered
mitochondrial translation/OXPHOS group rather than like `Opa1`. The main
remaining decision is whether to allocate one gene for a significant `Ptcd3`
self row. `Dap3`, `Ndufs2`, `Ndufa4`, `Sod2`, and `Sucla2` show that self-only
singletons happen, but six of the seven primary mitochondrial translation
analogs in the focal cell group were 0, including PPR/RNA and mt-aaRS
comparators. Because the training median for this local biological class is 0
and no downstream module is expected, I assign `Ptcd3` a point prediction of 0
rather than 1.

## Limits of the inference

There is no same-complex PTCD3 perturbation in the training table beyond the
partial `Dap3` mitoribosomal analogy; no exact PTCD paralog or GFM1/TUFM partner
was available as a direct comparator. The assay measures nuclear and a small
set of mitochondrial RNAs in surviving NeuN+ nuclei, not mitochondrial
translation rates, respiratory-chain activity, or pre-assay loss of vulnerable
edited neurons. Human PTCD3 disease and fibroblast knockdown literature come
from stronger, chronic, often biallelic defects, so they establish pathway
importance but overpredict the breadth of a 3-4 week sparse neuronal CRISPR
RNA signature. Finally, distinguishing 0 from a one-gene self-transcript hit is
guide- and expression-dependent; the predicted absence of a broad downstream
program is much more strongly supported than the exact integer at the 0/1
boundary.
