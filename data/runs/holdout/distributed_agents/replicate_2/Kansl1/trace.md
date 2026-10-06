# Kansl1 prediction trace

## Question and resolved ambiguities

The held-out manifest for this run contains one mouse target, `Kansl1`. I interpreted `n_degs` exactly as the requested endpoint: in `151 TH Prkcd Grin2c Glut`, count every measured gene whose Benjamini-Hochberg adjusted Wilcoxon P value is below 0.05 in the perturbed-vs-control contrast. I did not exclude the self transcript from the count, because the supplied training CSV also includes self rows when they pass the FDR cutoff; for example `Ogt` has four genes at FDR < 0.05 in the count CSV and its focal signature contains the significant `Ogt` self row plus three downstream rows.

The input parquet and the training count CSV are held-in data only. `Kansl1` is absent from both by design, so the calculation is a prospective transfer from assayed perturbations.

## Sources used

- `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`: the focal `151 TH Prkcd Grin2c Glut` count table with 1,674 held-in targets.
- `[local file: training_de_all_cell_groups.parquet]`: exact focal differential-expression rows for the same held-in targets.
- Distributed Agents PerturbAI atlas dataset context, `perturbai-atlas-v5`, and the Distributed Agents same-experiment semantic corpus release `perturbai-july-260713-sourceguard-1773-v1`, including the run-local protected Findings reports for `Brd4`, `Crebbp`, `Ep300`, `Kat6a`, `Kat6b`, `Kmt2a`, `Msl2`, `Ogt`, and `Setd1a`.
- Distributed Agents runtime profile-neighbor analysis of the focal-cell log-fold-change signatures for the chromatin anchors listed below.
- PubMed-indexed external literature on KANSL1 and the KAT8/NSL complex:
  - Dias et al. 2014, Genes & Development, DOI `10.1101/gad.240200.114`, PMID `24788516`.
  - Sheikh et al. 2019, EMBO Reports, DOI `10.15252/embr.201847630`, PMID `31267707`.
  - Gaub et al. 2020, Nature Communications, DOI `10.1038/s41467-020-16103-0`, PMID `32382029`.
  - Linda et al. 2021, Autophagy, DOI `10.1080/15548627.2021.1936777`, PMID `34286667`.
  - Li et al. 2022, Nature Communications, DOI `10.1038/s41467-022-28613-0`, PMID `35177641`.
  - Soutar et al. 2022, Brain, DOI `10.1093/brain/awac325`, PMID `36074904`.
  - Arbogast et al. 2017, PLoS Genetics, DOI `10.1371/journal.pgen.1006886`, PMID `28704368`.
  - Koolen et al. 2015, European Journal of Human Genetics, DOI `10.1038/ejhg.2015.178`, PMID `26306646`.

## Dataset computations

I first loaded the requested-target CSV and the focal training-count CSV. The request was a single target, `Kansl1`. The 1,674 training targets had a very sparse count distribution in `151`: median 0, 75th percentile 1, 90th percentile 2, 95th percentile 18, 97.5th percentile 100.5, and a maximum of 2,677. Thus even counts around 10-25 are already above most perturbations in this cell group.

I searched the training target list for direct NSL, KAT8/MSL, COMPASS/WDR5, HAT, and chromatin coactivator comparators. `Kansl2`, `Kansl3`, `Kat8`, `Mcrs1`, `Phf20`, `Wdr5`, `Hcfc1`, `Wdr82`, `Rbbp5`, `Ash2l`, and `Dpy30` were not held-in focal targets. The exact held-in comparators and their observed `n_degs` at FDR < 0.05 were:

| Comparator | Observed `151` `n_degs` | How I used it |
| --- | ---: | --- |
| `Ogt` | 4 | NSL-associated subunit and O-GlcNAc writer; the closest direct assayed NSL-adjacent perturbation, but focal response was tiny |
| `Msl2` | 0 | KAT8-containing MSL, not NSL; useful as a counterexample that KAT8-complex membership alone did not make an acute focal RNA phenotype |
| `Brd4` | 311 | NSL/BRD4 functional axis comparator; broad thalamic transcriptional response but not a core NSL subunit |
| `Setd1a` | 368 | WDR5/COMPASS H3K4 methyltransferase comparator; strong positive chromatin response, mechanistically indirect for KANSL1 |
| `Kmt2a` | 24 | WDR5/COMPASS H3K4 methyltransferase comparator; smaller thalamic neuronal identity/connectivity response |
| `Crebbp` | 8 | KAT3 histone-acetyltransferase coactivator; weak thalamic response |
| `Ep300` | 0 | CREBBP paralog; null counterexample |
| `Kat6a` | 0 | MYST-family HAT; null counterexample |
| `Kat6b` | 0 | KAT6 paralog; null counterexample |
| `Kmt2c` | 0 | KMT2 family counterexample |

I then queried the parquet directly with DuckDB for `group_name = '151 TH Prkcd Grin2c Glut'` and these anchors. Each anchor had 17,259 measured genes in the focal class. The exact focal FDR < 0.05 counts from the parquet matched the training CSV: `Brd4` 311, `Setd1a` 368, `Kmt2a` 24, `Crebbp` 8, `Ogt` 4, and `Msl2`/`Ep300`/`Kat6a`/`Kat6b` 0. Recovery in the same group was adequate for all of them: 61 perturbed nuclei for `Crebbp`, 71 for `Ogt`, 93 for `Brd4`, 111 for `Msl2`, 150 for `Kat6b`, 154 for `Setd1a`, 155 for `Ep300`, 161 for `Kmt2a`, and 170 for `Kat6a`, all versus 23,679 controls.

For expression-pattern context, I ran the Distributed Agents `profile_neighbors` tool on the focal log-fold-change vectors for `Brd4`, `Setd1a`, `Kmt2a`, `Crebbp`, `Ogt`, `Msl2`, `Ep300`, `Kat6a`, and `Kat6b`, using all 1,674 training targets as the eligible universe and signed tails of 300 genes, 1%, and 5%. This recovered no hidden direct `Kansl1` substitute. The null HAT anchors produced many rank-neighbor relationships driven by extreme but nonsignificant tails, so I treated those as evidence against a clean shared HAT signature rather than as positive `Kansl1` analogs. The only biologically relevant same-context relationship that touched a direct NSL-adjacent target was `Ogt` appearing as `Brd4`'s rank-3 neighbor by negative top-300 feature overlap, but `Ogt` itself had only four FDR < 0.05 genes in `151`, so that overlap was not strong enough to move `Kansl1` toward the 300-DEG BRD4 scale.

## Kansl1-specific biological reasoning

`Kansl1` encodes the KAT8 regulatory NSL complex subunit 1. The NSL complex contains KAT8/MOF and noncatalytic subunits including KANSL1, KANSL2, KANSL3, MCRS1, PHF20, WDR5, HCF1, and OGT; KANSL1 is a scaffold that can bind several subunits, and structural work showed that the KANSL1/WDR5/KANSL2 interaction is needed for proper NSL assembly and chromatin targeting. That direct-complex prior makes `Kansl1` more plausible as a transcriptional responder than unrelated metabolic targets or silent HAT paralogs. KANSL1 haploinsufficiency also causes Koolen-de Vries syndrome, and KdVS patient or engineered KANSL1-deficient human neurons show oxidative-stress/autophagy imbalance and excitatory synaptic defects. Mouse `Kansl1` heterozygosity or 17q21.31 syntenic deletion alters cognition, hippocampal synaptic transmission, and hippocampal expression programs. More directly, Li et al. linked Kansl1 haploinsufficiency in mice to defective autophagosome-lysosome fusion through transcriptional regulation of `Stx17`, while Soutar et al. placed KANSL1 and KAT8 in PINK1-dependent mitophagy regulation.

The key question is how much of that biology should be expected to surface as nuclear RNA DE after sparse P16 AAV CRISPR in already postmitotic neurons. The same-experiment answer from close held-in genes argues for a small response, not a BRD4/SETD1A-scale event:

- The direct assayed NSL-associated node `Ogt` produced only 4 focal DEGs at FDR < 0.05. In the full Distributed Agents report `Ogt` was broad in other neuronal classes, especially `155 MB Glut`, `191 MB P MY GABA`, and `066 CNU-HYa HY GABA`, and had an RNA-processing/proteostasis signature, but the requested thalamic class had only a self row plus three other significant genes. This is the strongest same-complex calibration point against a very large focal prediction.
- `Msl2` produced 0 focal DEGs and was null in every measured group in the Distributed Agents report. Because MSL2 belongs to the KAT8-containing MSL complex rather than the NSL complex, I used this only as a boundary: loss of one KAT8 complex subunit need not recapitulate NSL scaffold biology in this assay.
- `Brd4` is a plausible downstream-state analog because the NSL complex can enable BRD4 recruitment for active transcription through histone acetylation. `Brd4` had 311 focal DEGs and a 513-gene FDR < 0.10 thalamic program dominated by loss of neuronal process, adhesion, channel, and synaptic transcripts plus a smaller lysosomal/endosomal counter-program. I treated it as proof that a promoter acetylation/reader axis can be highly visible in `151`, but not as a direct magnitude analog: the same Distributed Agents report rejected `Ep300`, `Myc`, Mediator, and weak `Crebbp` signatures as BRD4 phenocopies.
- `Setd1a` had 368 focal DEGs and a strong mitochondrial, GPI-anchor, ER/Golgi, ciliary, and lysosomal/GATOR/autophagy program. That shows WDR5-linked promoter chromatin machinery can be very visible. But Dias et al. showed WDR5 recruitment into NSL and MLL/COMPASS complexes is mutually exclusive; in the dataset, `Setd1a` did not phenocopy `Kmt2a`, and `Kmt2a` itself had a much smaller 24-DEG focal program. I therefore used `Setd1a` as an upper-bound counterexample rather than as a direct estimate for `Kansl1`.
- `Crebbp` had 8 focal DEGs and `Ep300` had 0, despite strong KAT3 literature priors. `Kat6a` and `Kat6b` were both 0 in the focal class. These null and weak HATs are important because they show that postnatal, sparse CRISPR of a chromatin coactivator can be buffered, redundant, or displaced from its developmental phenotype.

I therefore called `Kansl1` nonzero because it is a direct NSL scaffold with documented transcriptional, autophagy, mitochondrial-quality-control, and synaptic consequences in neuronal disease models. I kept the magnitude in the weak-to-low-medium range because the closest held-in NSL-adjacent perturbation, `Ogt`, was only 4 DEGs in `151`, the KAT8/MSL comparator `Msl2` was null, direct KAT8/KANSL/MCRS1/WDR5 perturbations were missing, and most KANSL1 literature used constitutive haploinsufficiency, developmentally exposed cells, iPSC-derived neurons, or non-neuronal systems.

Final point prediction for `Kansl1`: **12 DEGs**.

## Limits

- No held-in perturbation was a direct `Kansl1` paralog or a core `Kansl2`, `Kansl3`, `Kat8`, `Mcrs1`, `Phf20`, `Wdr5`, or `Hcfc1` knockout, so the estimate relies on one NSL-associated target (`Ogt`), one KAT8/MSL boundary (`Msl2`), indirect BRD4 and WDR5/COMPASS biology, and general HAT counterexamples.
- The profile-neighbor search over focal log-fold-change vectors was useful mainly for detecting absence of a clean shared chromatin signature. Whole-profile similarities around null anchors can be driven by large, nonsignificant ranks, so I did not use them quantitatively.
- KANSL1 has strong developmental and haploinsufficiency priors, but this experiment is an acute, sparse, survivor-conditioned P16-to-P37/44 CRISPR assay in NeuN+ nuclei. It will miss embryonic requirements, non-neuronal effects, dosage phenotypes that require chronic 50% expression, and protein/autophagy changes that do not feed back onto nuclear RNA within 3-4 weeks.
- The 12-DEG prediction is an extrapolation between weak direct NSL-adjacent evidence and larger indirect chromatin examples. A zero or a `Kmt2a`-like count around 20 would not be surprising; a `Brd4`/`Setd1a`-scale response would require KANSL1 loss to engage the NSL-BRD4 promoter axis far more strongly in this thalamic class than the measured `Ogt` and MSL/KAT3/KAT6 comparators did.
