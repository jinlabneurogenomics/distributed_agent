# Med12 prediction trace

## Question and setup

The held-out manifest `[local file: 136_Med12.csv]` contains one requested target:

```tsv
Med12
```

The endpoint to predict is the number of measured genes with Benjamini-Hochberg-adjusted Wilcoxon `pvals_adj < 0.05` in `151 TH Prkcd Grin2c Glut` cells after acute sparse AAV-CRISPR loss of the target. I treated the supplied focal training-count CSV as the authoritative endpoint for non-held-out perturbations and the large parquet as the source of focal expression patterns. Target-transcript knockdown was not used as a weight, because in this assay the target mRNA row is not a quantitative editing-efficiency estimate.

The main ambiguity was how much to transfer from generic MED12 biology. MED12 is a central Mediator kinase-module scaffold and a Wnt/beta-catenin interface, but this readout is basal postnatal neuronal snRNA-seq, not embryonic progenitors, ligand-stimulated Wnt cells, or tumor cells. I therefore used external biology only to choose comparators, and then let observed 151-cell signatures set the count scale.

## Sources used

- `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`: 1,674 non-held-out focal counts. It is highly sparse in this cell group: 1,205 targets have 0 DEGs, 363 have 1-9, 63 have 10-99, and 43 have at least 100.
- `training_de_all_cell_groups.parquet`: filtered with DuckDB to `group_name = '151 TH Prkcd Grin2c Glut'` and the nominated Med12 comparators, retaining `gene_target`, `names`, `logfoldchanges`, `scores`, `pvals_adj`, `n_pert_matched`, and `n_ctrl_matched`. The non-obvious step was only the bounded parquet scan:

```sql
SELECT gene_target, names, logfoldchanges, scores, pvals_adj,
       n_pert_matched, n_ctrl_matched
FROM read_parquet('training_de_all_cell_groups.parquet')
WHERE group_name = '151 TH Prkcd Grin2c Glut'
  AND gene_target IN (
    'Med13','Med13l','Med15','Med23','Cdk8',
    'Ctnnb1','Tcf7l2','Brd4','Ep300','Crebbp'
  );
```

- Distributed Agents selected corpus `perturbai-july-260713-sourceguard-1773-v1`: I queried target-centered reports for `Med13`, `Med13l`, `Cdk8`, `Med15`, and `Med23`, plus an induced topology check over Mediator/Wnt/coactivator comparators. The corpus has no visible held-out Med12 report.
- Distributed Agents gene-analog nomination and annotation store: Med12 comparators were nominated from CORUM 5.0 native mouse complexes, CORUM 5.0 human complexes projected through one-to-one MGI homology downloaded 2026-09-13, GO/KEGG/MSigDB annotations, and STRING v12.0 mouse physical edges at combined score >= 700. These annotations were used as priors about which training genes to inspect, not as endpoint measurements.
- NCBI Entrez/PubMed literature:
  - Kim, Xu, Hecht and Boyer, 2006, J Biol Chem, "Mediator is a transducer of Wnt/beta-catenin signaling", DOI `10.1074/jbc.M602696200`, PMID `16565090`. This grounds the direct beta-catenin/MED12 interface.
  - Clark, Oldenbroek and Boyer, 2015, Crit Rev Biochem Mol Biol, "Mediator kinase module and human tumorigenesis", DOI `10.3109/10409238.2015.1064854`, PMID `26182352`. This grounds the MED12-MED13-CDK8-Cyclin C kinase-module organization.
  - Philibert and Madan, 2007, Pharmacogenomics, "Role of MED12 in transcription and human behavior", DOI `10.2217/14622416.8.8.909`, PMID `17716226`. This grounds MED12 as a neurodevelopmental transcription-regulator disease gene, while not treating germline human disease as an expected acute postnatal DEG count.

## Within-dataset calibration

The direct available Mediator neighborhood was small but internally informative:

| comparator | focal `n_degs` | reason for comparing with held-out `Med12` |
| --- | ---: | --- |
| `Med13` | 11 | Highest-priority available Med12 analog from the nomination step; scaffold component of the CDK8 kinase module and shared human CORUM ARC/ARC-L memberships with Med12. |
| `Cdk8` | 0 | Enzymatic kinase-module component; a strong boundary because it is biochemically close but completely FDR-flat in 151 cells. |
| `Med13l` | 1 | `Med13` paralog and kinase-module-family boundary; it reproduced only `Grm1` down-regulation at FDR 0.05 in 151 cells. |
| `Med15` | 19 | Broader Mediator subunit, shared projected ARC/ARC-L membership, and same-direction 151 thalamic module with `Med13`/`Med23`. |
| `Med23` | 13 | Broader Mediator tail subunit, native/projected complex analog, and same-direction 151 thalamic module with `Med13`/`Med15`. |

Exact focal counts from the parquet matched the training-count CSV: `Cdk8 = 0`, `Med13l = 1`, `Med13 = 11`, `Med23 = 13`, and `Med15 = 19`. The module was also directionally coherent. Five genes were significant and down-regulated under all three of `Med13`, `Med15`, and `Med23`: `Prkcd`, `Grm1`, `Pcp4`, `Plekhg1`, and `Atp2a2`. Seven more were shared by two of the three, again all in the same negative direction: `Atp2b1`, `Grin2b`, `Ildr2`, `Kcnc2`, `Lef1`, `Lrrtm1`, and `Ptpn3`. `Med13l` kept only the `Grm1` part of this response, and the same `Med13` responder genes had `pvals_adj = 1` under `Cdk8` with small mostly opposite log-fold changes. This makes `Med13`/`Med15`/`Med23` positive analogs and `Cdk8`/`Med13l` boundary cases rather than a single pooled family.

I also checked broader candidates nominated by known MED12 interfaces:

| comparator | focal `n_degs` | interpretation |
| --- | ---: | --- |
| `Ctnnb1` | 383 | Strong Wnt/beta-catenin effector; overlapped many of the Mediator down-genes but was far broader than `Med13`/`Med15`/`Med23`. |
| `Tcf7l2` | 106 | Same Wnt/TCF axis; again broader than the compact Mediator module. |
| `Brd4` | 311 | Broad transcriptional coactivator/elongation perturbation; the Distributed Agents corpus explicitly found represented Mediator and p300/CBP perturbations did not phenocopy `Brd4`. |
| `Ep300` | 0 | p300 coactivator control; flat in the focal endpoint. |
| `Crebbp` | 8 | CBP coactivator control; weak and not a focal Mediator phenocopy. |
| `Ncoa1`, `Ncoa3` | 0, 0 | Nuclear-receptor coactivator controls from the annotation neighborhood; both flat. |

The Wnt comparison matters because Kim et al. showed beta-catenin can physically and functionally target MED12. However, in the training data the directly perturbed Wnt effectors were much broader than any represented Mediator response: `Ctnnb1` had 383 DEGs and `Tcf7l2` had 106, compared with 11-19 for the convergent Mediator subunits. The selected corpus also reports that `Med13` and `Med23` recovered only a small Wnt/beta-catenin-sensitive thalamic subset rather than a full canonical Wnt program. I therefore used the Wnt nodes to support a nonzero call but not to predict a 100+ count.

## Target-specific decision for Med12

Med12 is most naturally bracketed by two facts from the same experiment. First, loss of available Mediator scaffolding/subunits was detectable in the focal thalamic group: `Med13`, `Med15`, and `Med23` all landed in a compact 10-20 DEG range and shared a down-regulated neuronal identity/synaptic/calcium-handling module. Second, the effect was selective even inside closely related biology: `Cdk8` was 0 and its Wilcoxon-score profile was not a phenocopy, while `Med13l` was almost flat except for `Grm1`.

For the zero/nonzero decision, I put the most weight on `Med13` as the direct kinase-module scaffold analog and on the `Med15`/`Med23` convergence showing that the same cell group can reveal a small Mediator-sensitive module. That argues against predicting 0. I discounted large generic transcription-regulator counts, including `Brd4`, `Ctnnb1`, and `Tcf7l2`, because their focal signatures are broader and were not reproduced by the core Mediator comparators. I also used `Cdk8 = 0` as a downward boundary because it shows that acute postnatal loss of a CDK8-module component need not have any FDR-significant nuclear RNA footprint.

The resulting point estimate is **12 DEGs**: essentially Med13/Med23 scale, slightly below `Med15`, and far below the broad Wnt/beta-catenin or BRD4 counts.

## Limits

This is extrapolation across Mediator subunits because `Med12`, `Med12l`, `Ccnc`, and `Cdk19` were unavailable as training perturbations in this run. Most external MED12 knowledge comes from human cells, tumor contexts, or developmental systems with active signaling; it only tells me that Wnt/beta-catenin and CDK8-module comparisons are relevant, not that the juvenile basal thalamic endpoint should be large. The assay is survivor-conditioned and lacks direct protein loss or DNA-indel measurements, so a small or zero DEG count would not prove weak editing or no biological role. Finally, the prediction is count-scale only: individual genes near the FDR threshold could move this low-teens estimate by several genes.
