# DEG-count prediction trace

## Question and endpoint

The run asks for one point prediction: the number of genes that would pass
Benjamini-Hochberg FDR < 0.05 after CRISPR loss of `Ust` in the focal
`151 TH Prkcd Grin2c Glut` neuronal group. `n_degs` is therefore an assay- and
power-dependent breadth of the snRNA-seq DE signature in recovered nuclei, not a
direct measurement of enzyme function, cell abundance, viability, or editing
efficiency. The held-out `Ust` perturbation is absent from the supplied Parquet
and from the focal training-count CSV, so the prediction must transfer from
visible perturbations and external gene-function knowledge.

## Sources used

- Declared focal training counts:
  `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
- Declared training differential-expression Parquet:
  `training differential-expression dataset`.
- Run-local requested-target manifest:
  `single-target request for Ust`.
- PerturbAI July same-experiment corpus release
  `perturbai-july-260713-sourceguard-1773-v1`, queried only for visible
  training perturbations and pathway interpretation.
- PubMed-indexed external literature:
  - Kobayashi et al., 1999, Journal of Biological Chemistry,
    DOI `10.1074/jbc.274.15.10474`, PMID `10187838`.
  - Nikolovska et al., 2015, Journal of Cell Science,
    DOI `10.1242/jcs.152660`, PMID `25480151`.
  - Nikolovska et al., 2017, PLoS ONE,
    DOI `10.1371/journal.pone.0170054`, PMID `28107390`.
  - Mikami and Kitagawa, 2013, Biochimica et Biophysica Acta,
    DOI `10.1016/j.bbagen.2013.06.006`, PMID `23774590`.
  - Habicher et al., 2022, PLoS Genetics,
    DOI `10.1371/journal.pgen.1010067`, PMID `35192612`.
  - Okada et al., 2010, Biochemical Journal,
    DOI `10.1042/BJ20100101`, PMID `20377530`.

## Quantitative analysis

The requested manifest contains exactly one held-out target:

| target_name |
|---|
| Ust |

I first read the focal training-count CSV to identify GAG, heparan-sulfate, and
proteoglycan perturbations present among the non-held-out targets. `Ust` itself
was not present. The focal training set contains 1674 visible targets, 1205 with
`n_degs = 0` and 469 with one or more FDR-significant genes, with a long
right tail up to 2677 DEGs. The visible genes nearest the relevant
glycosaminoglycan chemistry were all zero in the focal cell type:

| visible perturbation | biochemical relationship to UST or GAG biology | observed `151 TH Prkcd Grin2c Glut` `n_degs` |
|---|---|---:|
| `B3gat3` | glucuronyltransferase in the common proteoglycan linkage tetrasaccharide upstream of CS/DS and HS chain formation | 0 |
| `Xylt1` | xylose transferase that initiates the proteoglycan linkage region | 0 |
| `Rxylt1` | xylosyltransferase-like GAG-linker enzyme | 0 |
| `Ext1` | heparan-sulfate polymerase subunit, paired with EXT2 | 0 |
| `Ext2` | heparan-sulfate polymerase subunit, paired with EXT1 | 0 |
| `Glce` | glucuronyl C5-epimerase for HS uronic-acid modification | 0 |
| `Hs6st2` | HS 6-O-sulfotransferase, a sulfation enzyme downstream of polymerization | 0 |
| `Gpc6` | glypican HSPG core protein | 0 |
| `Cspg4` | chondroitin-sulfate proteoglycan core protein | 0 |

I then queried the declared Parquet in the focal cell type for those targets:

```sql
SELECT gene_target,
       count(*) AS rows,
       sum(pvals_adj < 0.05) AS n_fdr05,
       sum(pvals < 0.05) AS n_nom05,
       min(pvals_adj) AS min_padj,
       median(abs(logfoldchanges)) AS median_abs_lfc,
       any_value(n_pert_matched) AS n_pert,
       any_value(n_ctrl_matched) AS n_ctrl
FROM read_parquet(:training_de_all_cell_groups)
WHERE group_name = '151 TH Prkcd Grin2c Glut'
  AND gene_target IN (:analogs)
GROUP BY gene_target;
```

This verified that the zeros in the count CSV are exact for the Parquet rows:
all nine analogs had `n_fdr05 = 0` over 17,259 measured genes, with
127 to 255 matched perturbed nuclei against 23,679 matched controls in the focal
class. Their nominal counts were typical of flat signatures before
multiple-testing correction rather than broad subthreshold programs:

| perturbation | nominal `p < 0.05` genes | minimum adjusted p | median absolute log2FC | matched perturbed nuclei |
|---|---:|---:|---:|---:|
| `B3gat3` | 362 | 1.000 | 0.162 | 204 |
| `Cspg4` | 382 | 0.339 | 0.169 | 190 |
| `Ext1` | 329 | 1.000 | 0.148 | 238 |
| `Ext2` | 349 | 0.0559 | 0.153 | 213 |
| `Glce` | 363 | 0.162 | 0.187 | 155 |
| `Gpc6` | 380 | 1.000 | 0.145 | 255 |
| `Hs6st2` | 344 | 1.000 | 0.178 | 170 |
| `Rxylt1` | 268 | 1.000 | 0.198 | 127 |
| `Xylt1` | 339 | 1.000 | 0.155 | 217 |

As a local expression-pattern check, I also inspected the focal-cell rows for
`Ust`, `B3gat3`, `Ext1`, `Ext2`, `Glce`, `Hs6st2`, `Xylt1`, `Ndst1`,
`Ndst2`, `Hs2st1`, `Hs6st1`, and `Slc35b2` as measured genes under the same
analog perturbations. Those pathway transcripts were not coordinately changed:
every inspected row had adjusted p = 1 except for the `Ext2` self-transcript
under `Ext2` perturbation, which was reduced with nominal p = 0.000003 but only
reached adjusted p = 0.0559. In particular, the measured `Ust` transcript was
small and nonsignificant in the focal cell type under these perturbations:
log2FC ranged from -0.35 for `Xylt1` to +0.14 for `Ext2`, and every `Ust`
adjusted p-value was 1.

Finally, I checked the same visible pathway genes across all measured neuronal
classes. `Ext1`, `Glce`, and `Xylt1` were pan-neuronal nulls at FDR < 0.05;
`Hs6st2` had only a one-gene event outside the focal class; `B3gat3` had a
two-gene event in `059 CNU-LGE LSX GABA`; and `Ext2` had one-gene events in
`052 Pvalb Gaba` and `155 MB Glut`. None showed a hidden broad response in a
related thalamic class that would argue for a strong but missed `151` response.

The July same-experiment corpus gave the same interpretation for visible
training genes: `Ext1` produced no FDR-level downstream response in any
recovered neuronal class and did not activate FGF/ERK, Hedgehog, WNT, Slit/Robo,
or Eph reporters; `Glce` produced a zero-FDR cell-autonomous surface across all
22 recovered groups queried in that report; `Hs6st2` had no robust downstream
response in any measured group; and `Xylt1` produced a pan-neuronal null nuclear
transcriptome. For `B3gat3`, the corpus recorded a very restricted
`059 CNU-LGE LSX GABA` two-gene response and explicitly noted that acute
`B3gat3` loss did not feed back onto the common linker,
heparan-sulfate/chondroitin-sulfate enzyme set, proteoglycan core genes, or
canonical stress modules. These are same-experiment interpretations, not
independent replication, but they support reading the raw Parquet zeros as a
buffered GAG-pathway response rather than a single target-specific failure.

## Target-specific prediction

### Ust

`Ust` encodes uronyl 2-O-sulfotransferase. Kobayashi et al. cloned the human
enzyme and showed that it transfers sulfate to the 2-position of uronyl
residues, mostly in dermatan sulfate and more weakly in chondroitin sulfate,
with no detectable activity on desulfated N-resulfated heparin in their assay.
Mikami and Kitagawa summarize this class of chondroitin/dermatan-sulfate
biosynthetic enzymes as regulators of the structure of extracellular
proteoglycan chains rather than as direct nuclear transcriptional regulators.
Nikolovska et al. connected UST-dependent CS/DS 2-O-sulfation to FGF2 binding,
ERK activation, adhesion, and migration in CHO, 3T3, melanoma, and fibronectin
contexts. Habicher et al. found that zebrafish `ust` single mutants survived to
adulthood and argued that multiple CS/DS enzymes are buffered or redundant
unless combined.

The closest within-dataset analogs are not exact CS/DS 2-O-sulfotransferases:
several CS/DS sulfotransferases and epimerases were not visible training
perturbations. The visible set does, however, include enzymes whose loss should
perturb broader proteoglycan assembly (`Xylt1`, `B3gat3`, `Rxylt1`) or the more
developmentally central HS pathway (`Ext1`, `Ext2`, `Glce`, `Hs6st2`).
Okada et al. describe `Ext1`/`Ext2` as HS co-polymerases, and this HS chain
extension step is upstream of many growth-factor and axon-guidance interactions
that a postmitotic neuron could in principle sense through extracellular
ligands. If a partial, sparse P16 neuronal perturbation of HS/CS proteoglycan
chemistry readily triggered a broad autonomous DEG response in
`151 TH Prkcd Grin2c Glut`, these visible analogs would be the expected
positive controls. Instead, each had zero FDR-significant genes in the focal
group, and the focal pathway-transcript rows around `Ust` and the HS/CS genes
were flat.

The causal chain for transfer is:

`Ust` CRISPR loss -> reduced CS/DS uronyl 2-O-sulfation on a subset of
extracellular proteoglycan chains -> altered growth-factor/coreceptor or matrix
interactions outside the nucleus -> any signaling change in recovered thalamic
glutamatergic nuclei -> a Wilcoxon/FDR-significant snRNA-seq signature at
P37-P44.

The first two steps are well supported biochemically. The transfer weakens at
the signaling-to-transcription step: the screen directly shows that broader
visible GAG-linker, HS-polymerase, and HS-sulfation perturbations were buffered
in the same focal cell group, and the best external UST evidence emphasizes
matrix-rich developmental or motility contexts rather than a large acute
postmitotic neuronal RNA program. UST could still affect dendritic matrix,
synapses, or FGF responsiveness without generating FDR-significant nuclear
transcription in this sparse mosaic assay.

Prediction for `Ust`: **0 DEGs**. This is primarily a within-dataset prediction
from the flat `151 TH Prkcd Grin2c Glut` responses of `B3gat3`, `Xylt1`,
`Rxylt1`, `Ext1`, `Ext2`, `Glce`, `Hs6st2`, `Gpc6`, and `Cspg4`, with external
biochemical literature used to place `Ust` downstream of CS/DS sulfation rather
than among the screen's high-yield nuclear regulators.

## Limits

- The declared inputs contain no observed `Ust` perturbation; the requested
  endpoint is absent for `Ust`, so the final value is an extrapolated point
  prediction.
- The training set did not include the closest mouse CS/DS-modifying genes
  (`Chst3`, `Chst7`, `Chst11`, `Chst12`, `Chst13`, `Chst14`, `Chst15`, `Dse`,
  `Dsel`, `Csgalnact1`, `Csgalnact2`, `Chsy1`, and `Chpf` were absent), so the
  analog set leans toward common GAG-linker and HS biology.
- GAG enzymes act on extracellular polysaccharide fine structure. A loss of
  UST activity could cause biochemical or synaptic effects that are invisible
  to single-nucleus Wilcoxon DE at four weeks, especially if the affected
  process occurs during wiring, in glia/vascular matrix, or in unrecovered
  nuclei.
- The same-experiment corpus is a curated interpretation of the same July atlas
  measurements used in the Parquet; it helped interpret visible analogs but is
  not independent experimental validation.
- I did not use target mRNA loss as a measure of editing efficiency or as a
  reason to discard visible analogs.

## Final point estimate

| target_name | predicted_n_degs |
|---|---:|
| Ust | 0 |
