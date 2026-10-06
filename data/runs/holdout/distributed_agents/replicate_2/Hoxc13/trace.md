# Hoxc13 DEG-count prediction

## Question and scope

The requested manifest contains one held-out target:

```tsv
target_name
Hoxc13
```

I interpreted the requested value as the assay endpoint `n_degs`: the number of
measured genes with Benjamini-Hochberg adjusted Wilcoxon `pvals_adj < 0.05` in
the `151 TH Prkcd Grin2c Glut` cell group after acute AAV CRISPR loss of the
target. `Hoxc13` itself was fully held out, so neither its signature nor its
observed count is available in the training CSV or the parquet.

I treated a prediction of zero as "no assayed transcript crosses FDR 0.05", not
as a statement that Hoxc13 is biologically irrelevant in every tissue or that
editing would necessarily fail.

## Sources

- Local training endpoint:
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`
- Local differential-expression parquet:
  `[local file: training_de_all_cell_groups.parquet]`
- Requested-target manifest:
  `[local file: 107_Hoxc13.csv]`
- Distributed Agents same-experiment corpus MCP, release
  `perturbai-july-260713-sourceguard-1773-v1`. The corpus returned no
  target-centered claims, findings, or explicit references for `Hoxc13`, so the
  target-specific mechanism below comes from the local DEG data plus literature.
- PubMed literature on HOXC13/Hoxc13:
  - Godwin and Capecchi, 1998, `Genes & Development`, DOI
    `10.1101/gad.12.1.11`, PMID `9420327`.
  - Jave-Suarez et al., 2001, `Journal of Biological Chemistry`, DOI
    `10.1074/jbc.M101616200`, PMID `11714694`.
  - Qiu et al., 2015, `Cell and Tissue Research`, DOI
    `10.1007/s00441-015-2312-7`, PMID `26553656`.
  - Han et al., 2017, `Human Molecular Genetics`, DOI
    `10.1093/hmg/ddw378`, PMID `28011715`.

## Training-data calibration

The focal training endpoint is sparse. In the 1,674 non-held-out perturbations,
the median count is 0, only 469 perturbations are nonzero, the 90th percentile
is 2, and the very broad responses are concentrated in core RNA processing,
proteasome, transport, and chromatin genes such as `Uba5` at 2,677 DEGs, `Tpr`
at 1,768, and `Sin3a` at 1,433.

I then queried development/homeobox-family counterexamples in the count table.
The assayed Hox genes in this focal cell type were uniformly null:

| training target | relationship to Hoxc13 | observed `n_degs` |
| --- | --- | ---: |
| `Hoxa13` | paralogous-group 13 Hox transcription factor | 0 |
| `Hoxd13` | paralogous-group 13 Hox transcription factor | 0 |
| `Hoxa1` | Hox transcription factor, anterior/hindbrain patterning | 0 |
| `Hoxa3` | Hox transcription factor, pharyngeal/hindbrain patterning | 0 |
| `Hoxb8` | Hox transcription factor | 0 |
| `Hoxd10` | Hox transcription factor | 0 |
| `Foxn1` | epithelial Hoxc13-regulated gene in the pig skin KO model | 0 |

Several broader developmental transcription-factor families gave the same
calibration: the inspected `Pax2/Pax3/Pax4/Pax6/Pax7/Pax8`, `Dlx3/Dlx6`,
`Msx2`, `Lhx3/Lhx4`, `Gli1/Gli2/Glis2/Glis3`, and most `Fox` perturbations also
had 0 DEGs. That argues that an anatomically mismatched developmental TF should
not be assigned a nonzero count merely because it is a DNA-binding regulator.

For the Hox comparators I also inspected the differential-expression signatures
in the parquet for `151 TH Prkcd Grin2c Glut`. The parquet is sorted by
cell-group row groups; I used Parquet metadata to localize the six Hox targets
to six focal row groups, read only
`group_name`, `gene_target`, `names`, `logfoldchanges`, `pvals_adj`,
`n_pert_matched`, and `n_ctrl_matched`, and filtered to the focal group plus
`Hoxa1/Hoxa3/Hoxa13/Hoxb8/Hoxd10/Hoxd13`.

Each Hox comparator had 17,259 measured genes and 23,679 matched controls.
Matched perturbed-nucleus counts were 136 to 286:

| training target | `n_pert_matched` | min adjusted p-value | genes with `pvals_adj < 0.05` |
| --- | ---: | ---: | ---: |
| `Hoxa1` | 196 | 1.0000 | 0 |
| `Hoxa3` | 228 | 1.0000 | 0 |
| `Hoxa13` | 232 | 1.0000 | 0 |
| `Hoxb8` | 286 | 0.8797 | 0 |
| `Hoxd10` | 136 | 1.0000 | 0 |
| `Hoxd13` | 278 | 1.0000 | 0 |

The null counts were therefore flat signature calls rather than near misses.

## Hoxc13-specific reasoning

HOXC13 is a homeobox transcription factor with a strong, specialized external
epithelial program rather than a known postnatal forebrain or thalamic neuronal
program. Godwin and Capecchi generated Hoxc13 mutant mice and found Hoxc13
expression in nails, tail, vibrissae, filiform papillae, and hair follicles,
with homozygotes showing brittle hair and alopecia in the domains where the
gene is expressed. Jave-Suarez et al. showed that HOXC13 binds and activates
human hair-keratin promoters, consistent with direct control of trichocyte
differentiation genes. Qiu et al. further placed Hoxc13 in the murine hair
cycle, where perturbing it in skin alters anagen/catagen behavior and
TGF-beta1/SMAD2 signaling. Han et al. generated Hoxc13 knockout pigs and found
hair-follicle defects with decreased expression of Hoxc13-regulated epithelial
genes including `Foxn1`, `Krt85`, and `Krt35`.

Those functions are real but poorly matched to this experiment: postnatal,
NeuN-enriched brain nuclei from whole brain excluding hindbrain, and a
`151 TH Prkcd Grin2c Glut` neuronal cluster. The six observed Hox-family
perturbations in the same cell group, including the paralogous-group 13 members
`Hoxa13` and `Hoxd13`, all had zero DEGs and essentially no adjusted-p-value
support. `Foxn1`, a downstream epithelial target in Hoxc13 skin biology, was
also a zero-count training perturbation. I therefore used these local nulls as
the main calibration and the skin/hair literature as the mechanism explaining
why Hoxc13 should not be expected to drive a broad acute transcriptomic response
in this TH/Prkcd glutamatergic population.

I predict `Hoxc13 = 0` DEGs.

## Limits

The best within-dataset analogs are imperfect. `Hoxa13` and `Hoxd13` share the
paralogous Hox group with `Hoxc13`, and the other Hox genes are useful
homeobox-family controls, but none is a true Hoxc13 perturbation or an assayed
hair-follicle keratin program. The external Hoxc13 loss-of-function literature
mostly uses germline or epithelial systems, not sparse P16-to-P37 neuronal AAV
editing, so it is extrapolated here only to tissue specificity and likely lack
of activity in the focal neuronal state. Finally, a very subtle Hoxc13-dependent
effect, or an effect in a rare off-targeted epithelial/non-neuronal contaminant,
could exist below this Wilcoxon/FDR endpoint; the prediction is that no measured
gene will pass the experiment's adjusted-p-value threshold.
