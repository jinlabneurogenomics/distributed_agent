# DEG-count prediction for `151 TH Prkcd Grin2c Glut`

## Question and endpoint

I interpreted the task as a scalar holdout prediction for the requested genetic perturbation in the manifest
`prepared/manifests/deg-count/the single-target request`.  That manifest contains one target:

| target_name |
|---|
| Pi4ka |

The predicted endpoint is `n_degs`, the number of measured genes with
Benjamini-Hochberg-adjusted Wilcoxon `pvals_adj < 0.05` in the `151 TH Prkcd Grin2c Glut`
cell group.  I did not exclude the perturbed transcript from the count, because the supplied
training file also counts it; for example, `Synj1` has `n_degs = 1` in the focal group and the
single passing row is `Synj1` itself.

## Sources used

- Declared input count table:
  `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
- Declared input DE Parquet:
  `training differential-expression dataset`.
- Run-local target manifest:
  `single-target request for Pi4ka`.
- The selected same-experiment semantic corpus, `perturbai-july-260713-sourceguard-1773-v1`;
  I used the July Findings ledger for the `Pi4kb`, `Synj1`, and `Ocrl` reports and the BioKG
  graph only to enumerate explicit `Pi4kb` report comparators.  These are interpreted as
  curated summaries of the same Perturb-seq experiment, not as independent measurements.
- External literature from PubMed:
  - Dornan et al. 2018, DOI `10.1016/j.jmb.2018.07.020`, for PI4KA/TTC7/FAM126 complex
    architecture.
  - Chung et al. 2015, DOI `10.15252/embr.201439151`, for EFR3/TTC7/TMEM150 control of
    mammalian plasma-membrane PI4KA recruitment.
  - Suresh et al. 2024, DOI `10.1126/sciadv.adp6660`, for direct recruitment of the
    PI4KA-TTC7B-FAM126A complex by EFR3.
  - Guo et al. 2022, DOI `10.1016/j.celrep.2022.110452`, for activity-dependent PI4KA
    function in dendritic plasma-membrane PI4P synthesis, AMPA-receptor trafficking, LTP,
    and memory.
  - Salter et al. 2021, DOI `10.1093/brain/awab313`, and Verdura et al. 2021, DOI
    `10.1093/brain/awab124`, for biallelic human PI4KA neurological and hypomyelinating
    disease.
  - Alvarez-Prats et al. 2018, DOI `10.1016/j.celrep.2018.05.019`, for the strong Schwann-cell
    myelination phenotype after Pi4ka loss.
  - Mizuike et al. 2023, DOI `10.1083/jcb.202111069`, for Golgi PI4KB production of a PI4P
    pool used in CERT-dependent ceramide trafficking.

## Dataset calculations

From the focal training count CSV:

- 1,674 training perturbations are represented, all unique.
- The distribution is strongly zero-inflated: median `0`, 75th percentile `1`, 90th
  percentile `2`, 95th percentile `18`, and 469/1,674 perturbations have a nonzero count.
- Directly relevant observed counts in `151 TH Prkcd Grin2c Glut` were:

| comparator | `n_degs` | interpretation |
|---|---:|---|
| `Pi4kb` | 1 | closest measured PI 4-kinase paralog, but Golgi rather than plasma-membrane biased |
| `Ocrl` | 0 | PI(4,5)P2 5-phosphatase / endocytic PI node, buffered here |
| `Inpp5k` | 0 | PI 5-phosphatase, buffered here |
| `Synj1` | 1 | the one DEG is the on-target `Synj1` transcript |
| `Itpr1`, `Plcb1`, `Ppip5k2`, `Pitpnm3`, `Pik3cb`, `Pik3r1`, `Pik3r2`, `Cert1`, `Ywhae` | 0 | PI/Ca2+/lipid-transfer adjacent nodes, all quiet |
| `Ywhag`, `Ywhaz`, `Dnm1` | 1 each | each singleton is the target transcript itself |
| `Ppp3ca`, `Ppp3r1` | 4, 9 | calcineurin subunits; small focal response but broad targets of calcineurin make these indirect PI4KA analogs |
| `Pitpna` | 21 | the largest PI-adjacent response; internal Pi4kb report says it did not converge on Pi4kb |
| `Cltc` | 3 | endocytic coat perturbation, still small in this focal group |
| `Rab7` | 501 | late endosome/lysosome perturbation, a strong counterexample for generic membrane stress but not the same PI4P-generating step |

I then queried the Parquet for the closest three measured targets in the focal group.  The
operation was:

1. filter rows to `group_name == "151 TH Prkcd Grin2c Glut"` and
   `gene_target in ("Pi4kb", "Ocrl", "Synj1")`;
2. count `pvals_adj < 0.05` and `pvals_adj < 0.10`;
3. rank each target's measured genes by adjusted P value.

The focal details were:

| comparator | focal FDR 0.05 genes | focal FDR 0.10 genes | top rows |
|---|---:|---:|---|
| `Pi4kb` | 1 | 2 | `Tmem50b`, log2FC `0.426`, `padj=0.028`; `Rnf145`, log2FC `0.538`, `padj=0.069` |
| `Ocrl` | 0 | 0 | best row `Nat8l`, log2FC `0.404`, `padj=0.200` |
| `Synj1` | 1 | 1 | `Synj1`, log2FC `-0.583`, `padj=3.1e-7`, with no downstream row below FDR 0.10 |

I also checked whether the core PI4KA plasma-membrane complex was directly represented in the
training table.  `Efr3a`, `Efr3b`, `Ttc7`, `Ttc7b`, `Fam126a`, `Fam126b`, `Tmem150a`,
`Tmem150b`, and `Tmem150c` were not observed as training perturbations, so the decisive
within-dataset analog is the type-III 4-kinase paralog `Pi4kb` rather than a same-complex
subunit.

The same-experiment `Pi4kb` report strengthened that quantitative reading without adding an
independent replicate: the July corpus describes Pi4kb as producing only a tiny PI4P-loss
surface, with a `Tmem50b`/`Rnf145` ER-Golgi/sterol-E3-ligase module in `151 TH Prkcd Grin2c
Glut`, only one additional FDR 0.10 event in `054 CNU-MGE GABA`, no robust transcriptome-wide
phenocopy, and no convergence with `Pitpna`, `Ocrl`, `Synj1`, `Itpr1`, `Plcb1`, `Inpp5k`,
`Ppip5k2`, `Pitpnm3`, `Pik3cb`, `Pik3r1`, `Pik3r2`, `Cert1`, `Ywhae`, `Ywhag`, or `Ywhaz`.

## Target-specific reasoning

### Pi4ka

The direct molecular consequence of a successful `Pi4ka` perturbation is loss of
PI4KIIIalpha-dependent PI4P production at the plasma membrane, with secondary pressure on
PI(4,5)P2 and PI(3,4,5)P3 pools.  PI4KA is assembled with TTC7 and FAM126 and recruited to the
plasma membrane by EFR3 proteins, whereas the closest observed kinase comparator, `Pi4kb`,
mostly supplies a Golgi PI4P pool that supports Golgi trafficking and lipid-transfer reactions.
That makes `Pi4kb` mechanistically close at the enzymatic step but imperfect in organelle
exposure.

I considered three possible directions for the endpoint:

- A broad nonzero response: this is supported by PI4KA's disease relevance and by hippocampal
  PI4KA requirements for activity-dependent AMPA-receptor trafficking and LTP.  I downweighted
  it because the experiment is an acute, sparse P16 loss-of-function screen in recovered basal
  neuronal nuclei; it does not assay evoked LTP, chronic biallelic developmental impairment,
  Schwann cells, oligodendrocyte myelination, intestinal epithelium, or immune cells.
- A strict zero: this is supported by the general zero inflation of this endpoint and by
  focal zeros for `Ocrl`, `Inpp5k`, `Itpr1`, `Plcb1`, `Ppip5k2`, `Pik3cb`, `Pik3r1`,
  `Pik3r2`, `Pitpnm3`, `Cert1`, and `Ywhae`.
- A tiny one-gene response: this is most consistent with the closest measured kinase.
  `Pi4kb` had exactly one FDR 0.05 gene in the focal cells and no broad FDR 0.10 response
  elsewhere; `Synj1`, `Dnm1`, `Ywhag`, and `Ywhaz` show that some lipid or synaptic
  perturbations only count the on-target transcript; and the whole training distribution
  places a one-gene response at the upper quartile, not as a large outlier.

I therefore predicted `Pi4ka = 1`.  The call is driven mainly by the within-dataset
`Pi4kb` focal count and the flat phosphoinositide-neighbor surface, with external biology used
to reject both of the stronger extrapolations: PI4KA is not a random quiet gene, but the known
PI4KA phenotypes largely occur in contexts or activity states that this assay would not be
expected to convert into hundreds of basal thalamic nuclear RNA changes.

## Limits

The prediction is extrapolative because the true PI4KA complex partners and EFR3/TTC7/FAM126
recruiters were absent as training perturbations.  The closest observed analog, `Pi4kb`, makes
the same lipid phosphorylation but in a different membrane compartment.  Conversely, PI4KA has
stronger documented central-neuronal physiology than PI4KB, so the true count could be a small
multi-gene response rather than a singleton if plasma-membrane PI4P depletion couples more
efficiently to thalamic transcription than the Golgi PI4KB perturbation did.  The endpoint also
counts the target transcript, but target-RNA loss is only partly predictable from guide identity
in this mosaic Cas9 assay.  Overall the evidence supports a very small response, with the
largest uncertainty being `0` versus a few DEGs rather than a high-burden response.
