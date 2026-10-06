# Naa20 held-out DEG-count prediction

## Question

The held-out manifest for this run contained one requested perturbation:
`Naa20`. I interpreted the requested endpoint as the integer number of measured
genes with `pvals_adj < 0.05` for the acute CRISPR loss-of-function perturbation
of `Naa20` in the focal postnatal neuronal group `151 TH Prkcd Grin2c Glut`.

The held-out target is absent from both input training files, so I used the
training perturbations only as analogs and counterexamples. I treated `0` as a
real prediction of no FDR 0.05 genes, not as missing data.

## Sources

- Held-out manifest:
  `[local file: 142_Naa20.csv]`.
- Focal training count table:
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
- Differential-expression parquet:
  `[local file: training_de_all_cell_groups.parquet]`.
- Distributed Agents same-experiment corpus, release
  `perturbai-july-260713-sourceguard-1773-v1`, queried through
  `target_context` and `search_claims`.
- Distributed Agents run-local signed profile comparison over focal-cell log-fold-change
  vectors, using `gene_target` as the profiled node, `names` as the feature, and
  `pvals_adj < 0.05` as the significance threshold.
- External PubMed literature from NCBI PubMed E-utilities.

## Local computations

1. I read the requested-target CSV. It had exactly one row, `Naa20`.

2. I summarized the 1,674 non-held-out focal-cell DEG counts. Of these, 1,205
   were exact zeros and 469 were nonzero. The distribution was highly sparse:
   median 0, 75th percentile 1, 90th percentile 2, 95th percentile 18, 99th
   percentile 436, and maximum 2,677.

3. I searched the training count table for N-terminal acetyltransferase
   perturbations. The only `Naa*` training target in this endpoint was `Naa10`,
   with `n_degs = 0`; `Naa20`, its NatB partner `Naa25`, and the other Nat
   catalytic genes were not available as training perturbations.

4. I filtered the parquet to the focal cell group and to a small hand-selected
   set of analogs and counterexamples. The filter was:

   ```python
   f = (
       (pc.field("group_name") == "151 TH Prkcd Grin2c Glut")
       & pc.field("gene_target").isin(candidate_targets)
   )
   ```

   Each selected perturbation had 17,259 measured genes in this cell group.
   `Naa10` had 240 matched perturbed nuclei, 23,679 matched controls, and no
   gene passed either FDR 0.05 or FDR 0.10. As positive controls, the same
   focal assay recovered 742 FDR 0.05 genes for `Psmb4`, 430 for `Psmc1`, and 9
   for `Eef2`.

5. I computed signed log-fold-change profile comparisons among `Naa10` and
   focal protein-homeostasis or translation controls. `Naa10` again had
   `significant_feature_count = 0`; `Psmb4` had 357 positive and 385 negative
   FDR genes, `Psmc1` had 231 positive and 199 negative FDR genes, and `Eef2`
   had 6 positive and 3 negative FDR genes. The leading focal-cell whole-vector
   neighbors of `Naa10` within this hand-selected set were other flat or nearly
   flat perturbations, including `Gli2`, `Rorb`, `Eif2ak4`, `Eif4g1`, `Eif4h`,
   `Eif4a2`, and `Eif5a`; none of those are NatB mechanistic partners, so I
   used them only as evidence that `Naa10`'s rank pattern was a flat-profile
   artifact rather than a N-terminal-acetylation module.

## Training analogs and counterexamples for Naa20

| training target | focal `n_degs` | matched perturbed nuclei | why I considered it |
|---|---:|---:|---|
| `Naa10` | 0 | 240 | The only NAA-family training perturbation. It encodes the catalytic subunit of NatA, a different but closely related cotranslational N-terminal acetyltransferase. It is the most direct in-dataset analog for asking whether partial acute depletion of a core NAT enzyme creates a nuclear RNA response in settled neurons. |
| `Eif2ak4` | 0 | 194 | Translation/stress-sensing kinase counterexample; focal profile was flat. |
| `Eif5a` | 0 | 189 | Translation-related counterexample; no FDR 0.05 genes. |
| `Eif4a2` | 2 | 135 | Translation-initiation helicase; tiny response only. |
| `Eif4g1` | 1 | 143 | Translation-initiation scaffold; singleton response only. |
| `Eif4h` | 1 | 178 | Initiation factor cofactor; singleton response only. |
| `Hspa5` | 5 | 47 | Protein-folding/ER-stress chaperone; small but detectable focal response. |
| `Hspa8` | 9 | 97 | Hsc70 chaperone; small focal response. |
| `Ube2e2` | 0 | 124 | Ubiquitin-conjugating enzyme counterexample; flat in the focal count table. |
| `Ube3a` | 0 | 84 | Neuronal ubiquitin ligase counterexample; flat in the focal count table despite known neuronal importance. |
| `Eef2` | 9 | 87 | A translation elongation factor that the Distributed Agents `Naa10` report used as a protein-homeostasis/translation assay-positive contrast; in this exact focal cell group its response was present but still single-digit. |
| `Psmb4` | 742 | 62 | Direct 20S proteasome perturbation. It showed that broad protein-homeostasis secondary RNA programs are detectable in `151 TH Prkcd Grin2c Glut` cells when the perturbation hits proteasome function directly. It is a boundary, not a NatB analog. |
| `Psmc1` | 430 | 89 | Direct 19S proteasome perturbation. Like `Psmb4`, it bounds the prediction by showing assay detectability of broad proteasome-associated states. |
| `Mpc1`, `Rorb`, `Gli2`, `Diaph2` | 0, 0, 0, 0 | 199, 162, 205, 23 | These appeared in Distributed Agents' data-driven `Naa10` neighbor report, but the report itself classified the relationship as weak full-vector similarity among flat signatures rather than a NatA mechanism. I treated them as confirmation that the nearest `Naa10` neighbors were null-like profiles, not as biological analogs of `Naa20`. |

The Distributed Agents corpus had no direct `Naa20` node in the same-experiment
knowledge layer. For `Naa10`, however, it contained a high-confidence
same-experiment finding: P16 `Naa10` perturbation was a pan-neuronal FDR-level
transcriptomic null, with 2,123 total matched perturbed nuclei across 22
measured neuronal groups and no downstream genes at FDR 0.10. A companion
finding reported no compensatory NAT-family, integrated-stress, apoptotic, or
proteasome/ubiquitin rebound program after `Naa10` perturbation. The corpus also
contrasted `Naa10` against active proteostasis/translation controls
`Psmb4`, `Psmc1`, and `Eef2`, concluding that the experiment was capable of
detecting large secondary proteostasis responses even when `Naa10` was flat.

## External biology used for Naa20

`Naa20` encodes the catalytic subunit of NatB. NatB is a heterodimeric
N-terminal acetyltransferase containing catalytic NAA20 and auxiliary NAA25 and
preferentially acetylates nascent polypeptides whose initiator methionine is
followed by Asp, Glu, Asn, or Gln. Structural and biochemical work showed that
NAA25 scaffolds NAA20 and improves substrate affinity, while the NAA20 active
site confers the Met-Asp/Glu/Asn/Gln specificity (Hong et al. 2017,
DOI:10.1016/j.str.2017.03.003, PMID:28380339; Layer et al. 2021,
DOI:10.1038/s42003-020-01546-4, PMID:33398031). Quantitative N-terminomics
found large NatB substrate pools in yeast and human cells and linked human NatB
depletion to actomyosin and migration defects (Van Damme et al. 2012,
DOI:10.1073/pnas.1210303109, PMID:22814378).

There is real neurodevelopmental support for NatB importance: recessive human
NAA20 missense variants weaken NAA20-NAA25 complex formation and cause
developmental delay, intellectual disability, and microcephaly (Morrison et al.
2021, DOI:10.1038/s41436-021-01264-0, PMID:34230638), with later case work
expanding the phenotype to ataxia, brain malformations, and epilepsy
(D'Onofrio et al. 2023, DOI:10.1111/cge.14359, PMID:37191084). NatB can also
control specific neuronal proteins: in human induced neurons, NatB promoted
N-terminal acetylation of alpha-synuclein and protected cytosolic
alpha-synuclein from UBE2W-dependent proteasomal degradation (Santhosh Kumar et
al. 2024, DOI:10.1126/sciadv.adj4767, PMID:38335281).

These external facts make `Naa20` a plausible biochemical perturbation but do
not imply a large nuclear transcriptomic state in this assay. Most NatB
mechanisms are post-translational changes in substrate stability, localization,
or cytoskeletal behavior. The experiment perturbed postmitotic P16 neurons
acutely and mosaically, with partial target RNA knockdown on average, rather
than producing a germline NatB-null developmental state or assaying the
N-terminome. The direct within-dataset Nat analog, `Naa10`, showed that a broad
loss of cotranslational N-terminal acetylation can be transcriptionally buffered
under exactly these assay conditions.

## Naa20 decision

The closest same-assay analog, `Naa10`, was an exact focal zero and was reported
by the Distributed Agents corpus as a pan-neuronal null rather than merely a low-powered
single-cell-group miss. The nearby translation and chaperone perturbations were
also mostly 0 to 9 DEGs. I therefore expect acute `Naa20` perturbation in
`151 TH Prkcd Grin2c Glut` nuclei to be either silent or, at most, a
very small singleton-like response.

I set the point prediction to the modal and mechanistically favored value,
`0`, rather than to a small positive count, because there was no focal
NatB-specific training perturbation at all and because the assay did not show an
integrated stress, ubiquitin, proteasome, or compensatory NAT-family RNA program
after perturbing the analogous `Naa10` enzyme.

## Limits

- The training set did not contain `Naa20`, `Naa25`, or another true NatB
  subunit, so the prediction extrapolates from NatA and indirect
  proteostasis/translation controls.
- NatA and NatB have different substrate specificities; `Naa10` is a useful
  assay-context analog but not a NatB phenocopy.
- Germline human `NAA20` disease, plant and yeast NatB deletion, and strong
  knockdown in dividing mammalian cells are not the same as sparse juvenile
  mouse neuronal CRISPR loss-of-function.
- The assay measured nuclear mRNA, not N-terminal acetylation, alpha-synuclein
  abundance, actin/tropomyosin organization, protein turnover, electrophysiology,
  or viability. Any of those could change without producing an FDR 0.05 mRNA
  signature.
- The hidden held-out matched cell count is not in the supplied files. DEG
  counts are power-sensitive, so a larger or smaller realized `Naa20` cell count
  could move a borderline singleton response across the FDR threshold.
