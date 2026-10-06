# Satb1 DEG-count prediction

## Question interpreted

The requested held-out target list is `[local file: 201_Satb1.csv]`; it contains one target, `Satb1`. I interpreted the task as predicting one integer:

`n_degs = #{measured genes with BH-adjusted Wilcoxon pvals_adj < 0.05 after Satb1 perturbation in 151 TH Prkcd Grin2c Glut cells}`.

The `Satb1` rows were completely absent from the supplied training count CSV and from the training differential-expression Parquet as perturbations, so I did not treat any row in either input as a measured `Satb1` endpoint. `logfoldchanges` were interpreted as perturbed versus matched non-targeting control.

## Sources used

- Supplied focal-cell training counts:
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`
- Supplied same-experiment differential-expression table:
  `[local file: training_de_all_cell_groups.parquet]`
- Supplied held-out manifest:
  `[local file: 201_Satb1.csv]`
- Distributed Agents same-experiment semantic corpus, release `perturbai-july-260713-sourceguard-1773-v1`.
  I queried its `related_targets` index for `Satb1`; this release returned no target-gene links for `Satb1`, so it did not provide a target-specific analog and I treated the absence as missing annotation rather than as evidence for no biology.
- Distributed Agents runtime profile tools over the supplied Parquet. I used `profile_compare` and `profile_inspect` to compare focal-cell expression profiles among a small, predeclared set of plausible `Satb1` comparators: `Satb2`, `Bcl11a`, `Bcl11b`, `Zbtb18`, `Sox5`, `Smarcc2`, `Chd4`, and `Ctcf`.
- PubMed literature retrieved through the BioEval literature tools.

## Computational calibration

I first read the held-out manifest and verified that `Satb1` is absent from the training counts. The count table has 1,674 non-held-out targets in `151 TH Prkcd Grin2c Glut`, of which 1,205 have zero DEGs at FDR 0.05 and 469 have a nonzero count. The response distribution is highly skewed:

| statistic | n_degs |
| --- | ---: |
| mean | 14.05 |
| median | 0 |
| 75th percentile | 1 |
| 90th percentile | 2 |
| 95th percentile | 18 |
| 99th percentile | 436.5 |
| maximum | 2677 |

The largest focal responses were from broad core regulators or toxicity/stress-like hits, for example `Uba5` 2677, `Tpr` 1768, `Sin3a` 1433, `Yy1` 720, `Cic` 576, `Ctcf` 270, and `Smarcc2` 185 DEGs. I therefore treated the baseline expectation for an unmeasured target as zero or very small unless there was target-specific reason to expect a broad, assay-visible state.

For selected analogs, I scanned only the focal row groups and selected `gene_target` values from the Parquet rather than loading the full 616M-row table. The essential operation was:

```python
import pyarrow.dataset as ds
import pyarrow.compute as pc

dset = ds.dataset(
    "[local file: Inputs]"
    "training_de_all_cell_groups.parquet",
    format="parquet",
)
fil = (
    (pc.field("group_name") == "151 TH Prkcd Grin2c Glut")
    & pc.field("gene_target").isin(targets)
)
table = dset.to_table(
    columns=["names", "gene_target", "logfoldchanges", "pvals", "pvals_adj",
             "n_pert_matched", "n_ctrl_matched"],
    filter=fil,
)
```

This retrieved exact per-gene focal signatures for the analog panel and their FDR 0.05 DEG counts.

## Relevant training perturbations

The most direct analog is `Satb2`, the paralog of `Satb1` and another AT-rich DNA-binding chromatin regulator. `Satb2` produced **0** focal DEGs among 236 matched perturbed nuclei; the smallest adjusted p-value in the focal signature was 1.0. That is strong within-dataset evidence against assuming that every SATB-family loss of function produces a broad state in this thalamic group.

Several developmental projection-neuron or neuronal-identity TFs were similarly flat in the focal cell group:

| training target | focal n_degs | focal matched perturbed nuclei | focal signature detail |
| --- | ---: | ---: | --- |
| `Satb2` | 0 | 236 | no FDR 0.05 genes; min FDR 1.0 |
| `Bcl11a` | 0 | 203 | no FDR 0.05 genes; min FDR 1.0 |
| `Bcl11b` | 0 | 206 | no FDR 0.05 genes; min FDR 1.0 |
| `Tbr1` | 0 | 288 | no FDR 0.05 genes; min FDR 0.944 |
| `Foxp2` | 0 | 245 | no FDR 0.05 genes; min FDR 1.0 |
| `Cux2` | 1 | 238 | only `Cux2` itself, logFC -0.428, FDR 0.0147 |
| `Ski` | 2 | 335 | `Cck` and `L1cam` significant |
| `Sox5` | 2 | 184 | `Dgkh` and `Tnnt1` significant |
| `Zbtb18` | 5 | 208 | `Endou`, `Pxdn`, `Clstn2`, `Man2a2`, and `Zbtb18` significant |
| `Mef2c` | 1 | 223 | only `Mef2c` itself, logFC -0.391, FDR 0.0283 |

These genes are not perfect biochemical partners for `Satb1`, but they are appropriate assay-scale comparators: they are neuronal transcription factors with strong developmental literature, yet the acute P16-to-P37/44 CRISPR assay in a broad postmitotic thalamic glutamatergic group saw no or very narrow focal transcriptional responses.

I also considered chromatin-regulator counterexamples:

| training target | focal n_degs | focal signature detail |
| --- | ---: | --- |
| `Chd4` | 100 | broad NuRD/remodeling response; top hits included `Begain`, `Cpne7`, `Zfp467`, `Ramp3` |
| `Smarcc2` | 185 | broad SWI/SNF response; top hits included `Ptpn3`, `Reep2`, `Tiam1`, `Prkcd` |
| `Ctcf` | 270 | broad genome-architecture response; top hits included `Dennd6b`, `Zcwpw2`, `Abhd14b`, `Wls` |

These establish that 151 TH Prkcd Grin2c Glut had the power to recover tens to hundreds of DEGs for some chromatin perturbations. I treated them as upper-bound counterexamples rather than close analogs: CTCF and SWI/SNF/NuRD perturbations globally change genome insulation or remodeler complexes, whereas SATB1 is a sequence-specific nuclear matrix/chromatin organizer with more lineage- and state-specific targets.

The Distributed Agents profile comparison agreed with that count-level picture. In a comparison among `Satb2`, `Bcl11a`, `Bcl11b`, `Zbtb18`, `Sox5`, `Smarcc2`, `Chd4`, and `Ctcf`, the three closest SATB/BCL11-family candidates had **no significant focal features**, `Sox5` and `Zbtb18` had **1-9 significant features**, and the broader chromatin regulators had **>=50 significant features**. Some whole-vector correlations between quiet and broad targets were numerically high because many rare measured genes share extreme but nonsignificant rank-tail values; the absence of FDR-significant feature overlap made those correlations weak evidence. I therefore used the profile comparison mainly to mark the boundary between the quiet developmental-TF group and the broad chromatin-regulator group.

## Biological rationale for Satb1

`Satb1` encodes a special AT-rich sequence-binding protein that can organize chromatin and tune transcription. External data support the idea that it is a real neuronal regulator:

- Balamotis et al. 2011 found SATB1 in mature mouse cortical neurons; Satb1-null postnatal cortical pyramidal neurons had reduced dendritic spine density and altered temporal induction of immediate-early genes including `Fos`, `Fosb`, `Egr1`, `Egr2`, `Arc`, and `Bdnf` (DOI: 10.1128/MCB.05917-11; PMID: 22064485).
- Denaxa et al. 2012 and Close et al. 2012 showed that SATB1 supports maturation, connectivity, and survival of MGE-derived cortical interneuron subtypes downstream of LHX6 or neuronal activity (DOI: 10.1016/j.celrep.2012.10.003, PMID: 23142661; DOI: 10.1523/JNEUROSCI.3583-12.2012, PMID: 23223290).
- Huang et al. 2011 mapped SATB1 protein in the adult mouse CNS. It was abundant in deep neocortical layers and several midbrain nuclei and present in smaller populations of centrolateral and parafascicular thalamic neurons, so `Satb1` is not an obviously irrelevant gene for thalamic neurons (DOI: 10.1016/j.neures.2011.05.015; PMID: 21658419).
- den Hoed et al. 2021 showed that human SATB1 dysfunction causes neurodevelopmental disorders through mechanism-specific transcriptional effects, reinforcing that the gene can be dosage sensitive in the nervous system but also that mechanism and cellular context matter (DOI: 10.1016/j.ajhg.2021.01.007; PMID: 33513338).
- Turovsky et al. 2021 reported that loss of Satb1 or Satb2 in cultured cortical neurons changes glutamate-receptor and GABA(A)-receptor gene regulation and calcium signaling, linking the two paralogs functionally but in an in-vitro cortical setting rather than in postnatal thalamus (DOI: 10.3390/ijms22115968; PMID: 34073140).

Those papers argue against treating `Satb1` as inert in all neurons. They do not, however, specifically predict a large steady-state nuclear RNA program in juvenile thalamic `Prkcd`/`Grin2c` glutamatergic neurons after a sparse acute CRISPR perturbation. Much of the decisive `Satb1` biology is cortical, interneuron, dopaminergic, developmental, or activity-dependent; the assay here is a basal recovered-nucleus snapshot in broad postnatal thalamic glutamatergic cells.

The closest within-dataset evidence points lower. `Satb2` itself was completely flat in the same focal group; `Bcl11a`, `Bcl11b`, `Tbr1`, and `Foxp2` were flat; `Sox5`, `Zbtb18`, `Cux2`, `Ski`, and `Mef2c` were only 1-5 DEGs. I considered whether the thalamic expression noted by Huang et al. should lift `Satb1` above these analogs, but without a thalamic SATB1-specific pathway or a broad chromatin-remodeler mechanism, the most defensible point estimate is no genes crossing BH FDR 0.05.

## Prediction

| target | predicted n_degs | reasoning |
| --- | ---: | --- |
| `Satb1` | 0 | `Satb1` is a neuronal chromatin-associated TF with credible effects in cortex, interneurons, dopamine neurons, and neurodevelopmental disease, but the closest focal training analog, `Satb2`, had 0 DEGs, several related neurodevelopmental TFs had 0 DEGs, the weakly active comparators were only 1-5 DEGs, and the high-count chromatin regulators were mechanistically broader counterexamples. |

## Limits

- `Satb1` has no held-out signature in the supplied table, so the prediction cannot use a measured `Satb1` vector or direct nearest neighbors.
- The Distributed Agents semantic corpus did not expose `Satb1` links in this release. Candidate selection therefore relied on external gene-function knowledge plus exact training counts rather than on a preinterpreted same-experiment `Satb1` report.
- SATB1 thalamic expression is anatomically suggestive but not mapped exactly onto the Allen-style `151 TH Prkcd Grin2c Glut` bin, which is broad and may pool multiple thalamic nuclei.
- Germline/null and conditional literature usually removes `Satb1` earlier or in cortical interneuron/projection-neuron contexts; this screen perturbed sparsely at P16 and measured survivor nuclei three to four weeks later.
- A true `Satb1` effect of one to a few DEGs is quite plausible in this count regime. I rounded that weak expectation down to 0 because the matched focal training paralog and several neuronal TF analogs were exact zeros at the same FDR threshold.
