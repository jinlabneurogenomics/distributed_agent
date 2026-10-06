# Reasoning trace

## Question and endpoint

The requested held-out perturbation is `Sdccag8`; it does not occur in the
training differential-expression parquet or in the focal training count table.
The endpoint to predict is the total number of measured genes with
Benjamini-Hochberg-adjusted Wilcoxon `pvals_adj < 0.05` in
`151 TH Prkcd Grin2c Glut` after the held-out CRISPR perturbation.

I treated the supplied focal count CSV as the direct observation of this
endpoint for non-held-out targets. I treated the all-cell-group parquet as the
direct source for exact focal rows and sample counts. The same-experiment report
corpus was used only as packaged interpretation of those measurements, not as an
independent replicate. External literature was used to decide which visible
perturbations are mechanistically appropriate analogs of `Sdccag8`.

## Sources used

- Differential-expression input:
  `training differential-expression dataset`.
- Direct focal endpoint input:
  `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
- Requested held-out list:
  `single-target request for Sdccag8`.
- Run-local task bindings, coverage, capability manifest, and measurement
  registry in `codex_runtime/pipeline`.
- Same-experiment corpus:
  `perturbai-july-260713-sourceguard-1773-v1`, including the filtered
  run-local target reports in `codex_runtime/protected_inputs/findings_reports.filtered.jsonl`.
- External literature from PubMed/NCBI E-utilities:
  Otto et al. 2010, DOI `10.1038/ng.662`, PubMed `20835237`;
  Airik et al. 2014, DOI `10.1681/ASN.2013050565`, PubMed `24722439`;
  Insolera et al. 2014, DOI `10.1016/j.neuron.2014.06.029`, PubMed `25088364`;
  Airik et al. 2016, DOI `10.1371/journal.pone.0156081`, PubMed `27224062`;
  Tsutsumi et al. 2022, DOI `10.1016/j.jbc.2022.101686`, PubMed `35131266`;
  Ren et al. 2022, DOI `10.24272/j.issn.2095-8137.2021.387`, PubMed `35503560`;
  Wingfield et al. 2018, DOI `10.1042/EBC20180030`, PubMed `30287585`;
  Nakayama and Katoh 2018, DOI `10.1093/jb/mvx087`, PubMed `29272450`.

No unavailable ranking workbench was used: this task asks for a scalar DEG
count, the request has no ranked or partially ranked supervision, and the run
manifest explicitly marked `dataset.perturbseq_features`,
`corpus.predictive_graph_review`, and `synthesis.ordering_validate` unavailable.

## Quantitative checks

I read the requested-target CSV and found exactly one held-out target:
`Sdccag8`.

I read the training count CSV to calibrate the focal endpoint. It contains
1,674 visible perturbations; 1,205 have `n_degs = 0`, 276 have `n_degs = 1`,
and 469 are nonzero. The endpoint in this cell group is therefore sparse and
zero-inflated.

I then filtered the differential-expression parquet to
`group_name == "151 TH Prkcd Grin2c Glut"` and to visible genes from the
ciliary/BBS/transition-zone/IFT neighborhood around `Sdccag8`. The focal
FDR<0.05 counts and matched perturbed nuclei were:

| training perturbation | focal `n_degs` | focal perturbed nuclei | expression-pattern evidence |
|---|---:|---:|---|
| `Alms1` | 0 | 110 | no focal FDR<0.05 row |
| `Armc9` | 0 | 196 | no focal FDR<0.05 row |
| `B9d1` | 0 | 180 | no focal FDR<0.05 row |
| `Bbs5` | 0 | 121 | no focal FDR<0.05 row; best row `Ptprn`, FDR 0.220 |
| `Cep112` | 0 | 106 | no focal FDR<0.05 row |
| `Cep120` | 0 | 184 | no focal FDR<0.05 row |
| `Cep290` | 0 | 99 | no focal FDR<0.05 row; best row `Opcml`, FDR 0.650 |
| `Dync2h1` | 0 | 98 | no focal FDR<0.05 row; best row `Gpbp1`, FDR 0.348 |
| `Dync2i1` | 0 | 229 | no focal FDR<0.05 row |
| `Ift43` | 0 | 328 | no focal FDR<0.05 row; best row `Celf3`, FDR 0.847 |
| `Ift81` | 0 | 152 | no focal FDR<0.05 row; best row `Atl3`, FDR 0.391 |
| `Ift88` | 0 | 143 | no focal FDR<0.05 row |
| `Kif3b` | 0 | 156 | no focal FDR<0.05 row |
| `Rpgrip1l` | 0 | 137 | no focal FDR<0.05 row; best row `Dennd4b`, FDR 0.184 |
| `Ttc21b` | 0 | 131 | no focal FDR<0.05 row; best row `Tm2d2`, FDR 0.459 |
| `Ttc8` | 1 | 180 | the sole focal FDR<0.05 row was on-target `Ttc8` itself; no downstream gene passed |

I also checked the focal training counts for other represented genes repeatedly
used in the same-experiment reports as ciliary/Hedgehog controls:
`Cspp1`, `Cplane1`, `Gli1`, `Gli2`, `Lztfl1`, `Ptch1`, `Ptch2`, `Rpgr`,
`Smo`, and `Tbc1d32` all had `n_degs = 0` in the focal count table.

These calculations were not sensitive to a generic nearest-neighbor heuristic.
They asked a targeted question: among perturbations that actually damage
centriolar, BBSome, IFT, dynein-2, transition-zone, kinesin-2, or ciliary
Hedgehog functions, is there an FDR<0.05 RNA response in the requested thalamic
postnatal neurons? For this held-out target, the answer in the supplied
training set was essentially no.

## Same-experiment report context

The July same-experiment corpus gave the same picture at the broader
FDR<0.10 downstream-gene level:

- `Alms1`, `Cep290`, `Dync2h1`, `Dync2i1`, `Ift43`, `Ift81`, and `Rpgrip1l`
  were reported as complete or nearly complete neuronal transcriptomic nulls.
- `Bbs5` had one downstream gene, `Sirt5`, but only in `046 CTX-CGE GABA`;
  the `151 TH Prkcd Grin2c Glut` slice had zero FDR<0.10 genes.
- `Ift88` had a single downstream `Pcsk1n` hit in `155 MB Glut`, not in the
  requested thalamic class.
- `B9d1` was the clearest ciliary-network counterexample, with a 25-gene
  response in `308 CB GABA`, but matched transition-zone/IFT/BBSome comparators
  including `Cep290`, `Rpgrip1l`, `Ift88`, `Dync2h1`, `Dync2i1`, `Kif3b`,
  `Ttc21b`, `Bbs5`, and `Smo` did not reproduce it.
- `Ttc8`/BBS8 was a useful on-target counterexample: its transcript was
  significantly depleted in the focal cell group, but no secondary mRNA program
  passed FDR.

`Sdccag8` also appeared as a downregulated transcript within broad `Setd1a`
and `Thap11` responses in the same corpus. I did not transfer those large
chromatin/transcription-factor signatures to `Sdccag8`, because in that causal
direction `Sdccag8` is a marker inside a much broader TF-controlled program.
The better intervention-level analogs are the represented ciliary knockouts
listed above.

## Target-specific reasoning

### `Sdccag8`

External mechanism:
`Sdccag8` is a real centrosome/cilium disease gene, also called `NPHP10` or
`BBS16`. Otto et al. 2010 identified truncating `SDCCAG8` mutations as a cause
of retinal-renal ciliopathy and showed SDCCAG8 localization at centrioles plus
direct interaction with OFD1. Airik et al. 2014 generated
`Sdccag8` gene-trap mice with retinal degeneration and nephronophthisis-like
renal disease. Airik et al. 2016 placed SDCCAG8 at the centrosome with OFD1,
AZI1, RABEP2, ERC1, and non-muscle myosins and showed that SDCCAG8 is required
for ciliogenesis and Hedgehog signaling in cultured cells. Tsutsumi et al. 2022
showed that the Sdccag8 C-terminal region is needed for centrosomal localization
and cilia formation, and Ren et al. 2022 showed that hypomorphic knock-in mouse
alleles impair cilia and recapitulate Bardet-Biedl-like retinal, renal,
polydactyly, infertility, and growth phenotypes. Insolera et al. 2014 further
links SDCCAG8 to PCM1, pericentriolar material recruitment, and embryonic
cortical neuronal migration.

Causal transfer model:

1. The Perturb-seq intervention would acutely disrupt `Sdccag8` in sparse
   postmitotic P16-to-P37/44 neurons.
2. The direct molecular consequence is expected to be impaired
   centrosome/centriolar-satellite and primary-cilium organization.
3. The affected pathway propagates through ciliary protein trafficking,
   transition-zone/IFT/BBSome function, and context-dependent Hedgehog or
   ciliary-GPCR signaling.
4. The measured endpoint is not ciliary trafficking, cilium length, Hedgehog
   ligand response, or neuronal migration; it is only resting nuclear RNA among
   recovered thalamic glutamatergic nuclei.
5. By P16, cortical migration and many patterning phenotypes described for
   SDCCAG8/ciliopathy loss-of-function are earlier-stage endpoints, while
   photoreceptor outer segments, kidney epithelium, sperm flagella, and glia are
   outside this NeuN-enriched whole-brain neuronal readout.

Appropriate within-dataset analogs and counterexamples:

- `Cep290`, `Rpgrip1l`, `B9d1`, `Tbc1d32`, and `Cplane1` are transition-zone or
  ciliopathy comparators. The directly closest visible thalamic results,
  `Cep290`, `Rpgrip1l`, and `B9d1`, were all `n_degs = 0`. `B9d1` proves the
  assay could detect a ciliary-network perturbation elsewhere, but its effect
  was in cerebellar GABA neurons and did not transfer to the focal thalamic
  class.
- `Ift43`, `Ift81`, `Ift88`, `Dync2h1`, `Dync2i1`, `Kif3b`, and `Ttc21b`
  sample IFT-A, IFT-B, dynein-2, and kinesin-2 trafficking. Every one was a
  focal zero at FDR<0.05 despite 98-328 recovered perturbed focal nuclei.
- `Bbs5` and `Ttc8` sample the BBSome branch of ciliary membrane cargo
  trafficking reviewed by Wingfield et al. 2018 and the IFT/BBSome trafficking
  machinery reviewed by Nakayama and Katoh 2018. `Bbs5` was a focal zero.
  `Ttc8` had one focal hit, but it was `Ttc8` itself, so it supports target RNA
  detection for BBS8 without a downstream survivor-state program.
- Hedgehog/ciliary output controls in the training set, including `Gli1`,
  `Gli2`, `Ptch1`, `Ptch2`, `Smo`, and `Lztfl1`, also had focal `n_degs = 0`.

Prediction:
I therefore predict `Sdccag8` will be a focal zero. The decisive evidence is
within-dataset: close ciliary perturbations are repeatedly FDR-flat in
`151 TH Prkcd Grin2c Glut`, and the only represented BBSome focal nonzero is an
on-target `Ttc8` self row. External literature supports assigning `Sdccag8` to
that ciliary/centrosomal intervention class, but it mostly increases confidence
that the visible ciliary analogs are mechanistically relevant; it does not by
itself predict a broad resting thalamic RNA response.

Final point estimate: `0`.

## Limits and uncertainty

- The prediction extrapolates from other ciliary genes because the Sdccag8
  expression signature and count were held out completely.
- The assay did not measure DNA indels, SDCCAG8 protein, cilium length, ciliary
  cargo localization, Hedgehog ligand response, photoreceptor and kidney
  phenotypes, or pre-assay survival.
- Many canonical SDCCAG8 phenotypes arise in retina, renal epithelium, sperm,
  or embryonic patterning contexts; those are imperfect matches to a sparse
  postnatal NeuN+ thalamic snRNA-seq endpoint.
- A singleton self-transcript event, like the one seen for `Ttc8`, is possible
  even without any downstream program. I did not add one for `Sdccag8` because
  the related focal ciliary targets mostly had flat or nonsignificant self
  rows, and self-mRNA depletion is not predictable from function alone in this
  CRISPR-indel assay.
- Same-experiment reports and Findings are curated views of the same parquet,
  not independent validation.
