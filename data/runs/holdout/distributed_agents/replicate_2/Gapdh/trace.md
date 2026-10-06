# DEG-count prediction trace

## Question and resolved ambiguities

The held-out manifest `087_Gapdh.csv` contains one requested target:
`Gapdh`. I interpreted the task as asking for a point prediction of
`n_degs` in the focal `151 TH Prkcd Grin2c Glut` cell group. `n_degs` is the
number of measured genes with
Benjamini-Hochberg-adjusted Wilcoxon `pvals_adj < 0.05`, so a one-gene
response can be only the knocked-out transcript if that transcript is in the
feature set.

For `Gapdh` the target transcript itself is not represented among the 17,259
measured `names` in the focal differential-expression surfaces I checked. Thus
the prediction cannot rely on a direct self-depletion row passing FDR, unlike
several assayed glycolysis genes.

## Sources

I used:

- The held-out manifest:
  `[local file: 087_Gapdh.csv]`.
- The focal-cell training endpoint:
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
- The per-gene differential-expression parquet:
  `[local file: training_de_all_cell_groups.parquet]`.
- The Distributed Agents corpus MCP, release
  `perturbai-july-260713-sourceguard-1773-v1`. Gapdh itself had no release
  findings or claims. A lexical search for glycolysis returned same-experiment
  claims that Hk1/Pfkm/Tpi1 and Eno1 were buffered or flat central-glycolysis
  perturbations in postmitotic neuronal CRISPR surfaces.
- Distributed Agents runtime profile tools comparing focal-cell
  `logfoldchanges` profiles with `pvals_adj < 0.05` used only to count and
  compare observed signatures; the generated local artifacts were
  `gapdh_glycolysis_profile_compare.json` and
  `gapdh_anchor_neighbors.json`.
- External pathway and mechanistic facts: KEGG Glycolysis/Gluconeogenesis
  pathway `mmu00010`, via KEGG as described by Kanehisa et al. 2023,
  DOI 10.1093/nar/gkac963, PMID 36300620; the GAPDH multifunctionality review
  by Sirover 2011, DOI 10.1016/j.bbagen.2011.05.010, PMID 21640161; and the
  NO/Siah1 apoptotic GAPDH mechanism of Hara et al. 2005,
  DOI 10.1038/ncb1268, PMID 15951807.

## Computations over the training data

1. I loaded the focal training CSV and summarized the endpoint distribution:
   1,674 non-held-out perturbations; 1,205 were exactly zero; 469 were positive;
   median 0; 75th percentile 1; mean 14.05; maximum 2,677. This establishes
   that weak effects usually resolve to zero or one DEG in this assay.

2. I queried the focal rows of the parquet for glycolysis and energy-metabolism
   neighbors and counted `pvals_adj < 0.05` per `gene_target`. The central
   glycolysis neighbors were flat or self-only:

   | training target | focal `n_degs` | useful DE evidence |
   | --- | ---: | --- |
   | `Hk1` | 1 | only `Hk1` itself was significant; `logFC=-0.768`, `padj=9.86e-05`, `n_pert=148` |
   | `Gpi1` | 1 | only `Gpi1` itself was significant; `logFC=-0.673`, `padj=2.14e-07`, `n_pert=173` |
   | `Pfkm` | 1 | only `Pfkm` itself was significant; `logFC=-0.857`, `padj=6.42e-14`, `n_pert=176` |
   | `Tpi1` | 1 | only `Tpi1` itself was significant; `logFC=-1.010`, `padj=6.23e-12`, `n_pert=248` |
   | `Eno1` | 0 | no measured gene crossed FDR 0.05, `n_pert=228` |
   | `Slc2a1` | 0 | no measured gene crossed FDR 0.05 despite `n_pert=325` |

   The checked stress markers also stayed flat in these glycolysis/glucose-entry
   perturbations: `Asns`, `Ddit3`, `Hspa5`, and `Ogt` all had adjusted
   p-values of 1.0 in Hk1, Pfkm, Tpi1, Eno1, and Slc2a1, and none was
   significant in Gpi1. That argues against a hidden unfolded-protein response,
   integrated-stress response, or O-GlcNAc feedback state downstream of acute
   basal glycolysis loss in these neurons.

3. I checked nearby central-energy targets as weaker analogs. `Pdha1`,
   `Idh3a`, and `Mdh2` each had `n_degs=1`, again only their own transcript;
   oxidative-phosphorylation components including `Cox4i1`, `Ndufs4`, and
   `Uqcrb` had `n_degs=0`. `Mdh1` was the only small central-carbon exception I
   looked at, with `n_degs=29`; its hits (`Cars`, `Gls`, `Ncdn`, `Atp2a2`, ...)
   looked like a modest malate/aspartate-shuttle or TCA-adjacent response, not
   a recurrent glycolysis response.

4. I included `Gfpt1` as a mechanistic counterexample. `Gfpt1` uses
   fructose-6-phosphate to enter the hexosamine biosynthetic pathway rather
   than performing basal cytosolic ATP production. In the same focal group it
   had `n_degs=311` with clear downstream ER and ISR markers: `Ogt` down
   (`padj=8.10e-17`), and `Herpud1`, `Asns`, `Ddit3`, `Hspa5`, `Chac1`,
   `Shmt2`, `Pdia6`, `Hsp90b1`, `Xbp1`, and `Sdf2l1` up. That positive control
   shows that this cell group and sample sizes can detect a metabolic
   perturbation when it creates a transcriptionally visible glycosylation or ER
   stress state; the flat Hk1/Gpi1/Pfkm/Tpi1/Eno1 results are therefore not a
   generic inability to call any metabolic signature.

5. I used Distributed Agents runtime profile comparison on
   `Hk1,Gpi1,Pfkm,Tpi1,Eno1,Slc2a1,Gfpt1` with focal `logfoldchanges`. Hk1,
   Gpi1, Pfkm, and Tpi1 each had exactly one significant feature; Eno1 and
   Slc2a1 had none; Gfpt1 had 311. The profile scan against all 1,674 training
   nodes did not turn the central glycolysis anchors into a coherent hidden
   module: nearest whole-profile neighbors of the flat anchors were unrelated
   genes with low top-tail overlap and no matching significant glycolytic/ISR
   program.

## Target-specific reasoning

### Gapdh

`Gapdh` encodes glyceraldehyde-3-phosphate dehydrogenase, which KEGG places in
the core glycolytic step immediately after triose-phosphate isomerase and before
phosphoglycerate kinase. That makes `Tpi1`, `Gpi1`, `Pfkm`, `Hk1`, `Eno1`, and
`Slc2a1` the most direct training perturbations in this CRISPR screen: they are
the assayed glucose-entry and cytosolic glycolysis genes in the same basal
energy-production pathway. In `151 TH Prkcd Grin2c Glut`, all were zero or
one-DEG responses, and all of the one-DEG responses were the guide target RNA
itself rather than a downstream compensation program.

GAPDH does have important noncanonical stress biology. In particular, Hara et
al. showed that S-nitrosylated GAPDH can bind Siah1, translocate to the nucleus,
and promote apoptosis after NO/glutamate stress, and Sirover reviewed GAPDH as
a regulated moonlighting protein. I did not convert those facts into a broad
DEG prediction because this experiment is an acute, sparse postnatal CRISPR
loss-of-function in otherwise basal NeuN-positive nuclei, not glutamate or NO
challenge, germline removal, or a selection assay for neuronal viability.
Within the training data, perturbing the upstream glycolysis pathway also did
not induce `Ddit3`, `Asns`, `Hspa5`, `Xbp1`, or Hif1a/Myc-like metabolic
rewiring, while the HBP branch gene `Gfpt1` clearly did. `Gapdh` is therefore
closer to the buffered central-glycolysis anchors than to `Gfpt1`, `Dhdds`, or
`Atp2a2`.

The decisive assay-level detail is that `Gapdh` itself was absent from the
measured focal feature rows I inspected. If it behaved like Hk1, Gpi1, Pfkm, or
Tpi1, the only expected FDR-significant row would be the direct target
transcript, but such a row could not contribute to `n_degs` here. I therefore
predict no downstream genes passing FDR 0.05.

Prediction for `Gapdh`: `0`.

## Limits

This is an extrapolation because the held-out Gapdh expression profile and its
cell counts are not present in the inputs, and the Distributed Agents corpus release has
no Gapdh-specific same-experiment finding. Gapdh is also not a perfect copy of
Hk1, Gpi1, Pfkm, Tpi1, or Eno1: its NAD-binding catalytic step and its
NO/Siah1-linked moonlighting functions could in principle produce effects that
other glycolysis knockouts do not. The estimate assumes the AAV CRISPR
perturbation achieves a mild mRNA/protein reduction comparable to the assayed
central glycolysis guides and that severely Gapdh-edited neurons, if any, do not
survive as a distinct stress-enriched nucleus population at harvest.
