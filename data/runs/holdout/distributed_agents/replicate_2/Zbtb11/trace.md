# Prediction trace

## Question and resolved ambiguities

I needed to predict the held-out `n_degs` endpoint for the requested target in
`151 TH Prkcd Grin2c Glut` neurons: the number of measured genes with
Benjamini-Hochberg-adjusted Wilcoxon `pvals_adj < 0.05` after acute sparse
P16 CRISPR loss of function.

The manifest `[local file: 264_Zbtb11.csv]`
contains one held-out target, `Zbtb11`.  I treated `n_degs` as an
assay-calibrated focal-cell response-breadth endpoint, not as a direct measure
of editing efficiency, viability, or target-gene importance.

## Sources used

- `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`
  for exact focal training DEG counts.
- `[local file: training_de_all_cell_groups.parquet]`
  for exact focal signatures of candidate analogs.  I used the parquet row
  group metadata to read only the row groups containing `151 TH Prkcd Grin2c
  Glut` and then filtered to candidate perturbations.
- Distributed Agents same-experiment corpus
  `perturbai-july-260713-sourceguard-1773-v1`, queried with `target_context`
  for `Zbtb11`, `Nrf1`, `Nop56`, `Otx2`, and `Set`, and with lexical Claim
  search for mitochondrial and ribosome-biogenesis modules.
- Distributed Agents runtime profile comparison over a candidate focal-signature file
  written to `workbench/zbtb11_candidate_151_de.tsv`.
- PubMed literature for ZBTB11 biology:
  - Keightley et al. 2017, DOI `10.1038/ncomms14911`, PMID 28382966.
  - Fattahi et al. 2018, DOI `10.1093/hmg/ddy220`, PMID 29893856.
  - Wilson et al. 2020, DOI `10.1038/s41467-020-19205-x`, PMID 33122634.
  - Garipler et al. 2022, DOI `10.1016/j.celrep.2022.110524`, PMID 35294876.
  - Sumathipala et al. 2022, DOI `10.1093/brain/awac034`, PMID 35104841.
  - Xu et al. 2024, DOI `10.1038/s41467-024-45585-5`, PMID 38355937.
  - Satou-Kobayashi et al. 2024, DOI `10.1371/journal.pone.0293852`,
    PMID 39083515.

The selected Distributed Agents corpus has no target-scoped `Zbtb11` Finding or
explicit-reference neighborhood, so same-experiment reasoning had to be
transferred from measured training perturbations with mechanistic links to
ZBTB11.

## Computational checks over the training data

The focal training endpoint contains 1,674 non-held-out targets.  It is
strongly zero-inflated: 1,205 targets have `n_degs = 0`, 363 have 1-9 DEGs,
63 have 10-99 DEGs, and 43 have at least 100 DEGs.

For focal signature inspection I read parquet row groups 546-580, filtered to
`group_name == "151 TH Prkcd Grin2c Glut"`, and retained 63 candidate targets
covering mitochondrial transcriptional regulators, respiratory-chain
structural or assembly factors, nucleolar/RNA-biogenesis factors, known
ZBTB11 interactors, and ZBTB paralogs.  Recounting `pvals_adj < 0.05` in that
filtered table reproduced the training CSV counts exactly for every retained
target used below.

I then compared the signed Wilcoxon-score vectors with Distributed Agents
`profile_compare`; the useful pairwise facts were:

- `Nrf1` had 138 focal DEGs, with 23 positive and 115 negative.
- `Nop56` had 25 focal DEGs, with 10 positive and 15 negative.
- `Opa1` had 37 focal DEGs, with an ATF4/amino-acid-stress signature.
- `Esrra` had 57 focal DEGs.
- `Nop56` was close to the UFMylation/stalled-ribosome training responses
  (`Uba5`, Pearson 0.391; `Ufc1`, Pearson 0.333) but not to the direct
  respiratory-chain examples.
- Direct respiratory-chain examples were transcriptionally near-null in the
  focal group: `Ndufs2`, `Cox5a`, and `Sdha` each had exactly one significant
  negative self-transcript; `Ndufv1` and `Ndufaf5` had zero.

## Target-specific biological transfer

### `Zbtb11`

ZBTB11 is a BTB/C2H2 zinc-finger transcription factor.  Human biallelic
variants cause a neurodevelopmental syndrome; Fattahi et al. linked pathogenic
zinc-finger alleles to abnormal nucleolar localization and ENCODE ChIP
pathway enrichment for rRNA synthesis, ribosomal assembly, RNA modification,
and stress-sensing pathways.  Wilson et al. gave the closest mechanistic
handle for this prediction: Zbtb11 cooperates with NRF-2/GABP to activate a
subset of nuclear genes for complex-I and mitoribosome biogenesis, and loss of
Zbtb11 impairs complex-I assembly and mitochondrial respiration.  Sumathipala
et al. found wild-type ZBTB11 bound promoters enriched for mitochondrial and
RNA-processing functions and showed that pathogenic variants act as loss of
function.  Garipler et al. extended ZBTB11 biology to proximal repression of
pro-differentiation genes together with ZFP131 in embryonic stem cells.

The best measured training analog is therefore not the broad ZBTB family as a
symbol class, but the small intersection of nuclear mitochondrial control and
RNA/nucleolar production:

- `Nrf1`, `n_degs = 138`, is the strongest relevant within-dataset positive
  comparator.  It is a nuclear respiratory regulator and the same-experiment
  corpus reports a recurrent but noncanonical neuronal Nrf1 core, strongest in
  `151 TH Prkcd Grin2c Glut`, with down-regulation of genes such as `Snhg11`,
  `Rsrp1`, `Nrsn2`, `Kifc2`, `Haghl`, and `Sdha` rather than a concerted
  canonical mitochondrial collapse.  This shows that this focal thalamic class
  can report loss of a nuclear mitochondrial transcriptional regulator, but
  the corpus also explicitly separates `Nrf1` from `Esrra`, `Ppargc1a`, and
  the ESRR paralogs, so I used 138 as an upper benchmark rather than a direct
  phenocopy.
- `Esrra`, `n_degs = 57`, is another positive nuclear oxidative-metabolism
  regulator in 151, but its overlap with `Nrf1` is weak in the corpus and in
  the focal profile comparison, consistent with node-specific mitochondrial
  transcription-factor outputs.
- `Nop56`, `n_degs = 25`, is the clearest measured nucleolar/rRNA-processing
  comparator.  Its focal signature down-regulates RNA-processing and splicing
  genes including `Rsrp1`, `Ddx17`, `Srsf5`, `Srsf11`, and `Ddx5`.  The
  same-experiment corpus places it near `Uba5`/`Ufc1` rather than near a broad
  same-complex snoRNP phenocopy and notes that NOP56 did not trigger a broad
  p53/UPR/autophagy stress transcriptome in surviving neurons.
- `Opa1`, `n_degs = 37`, is not a ZBTB11 pathway member, but it is a useful
  positive mitochondrial-stress benchmark because it gives a compact neuronal
  ISR-like response (`Asns`, `Mars1`, `Chac1`, `Ddit3`) rather than the huge
  UFMylation or proteasome signatures.
- Direct downstream respiratory-chain perturbations argue against expecting a
  broad signature from ZBTB11 solely because it touches complex-I genes.  In
  the focal counts, represented `Nduf*` targets were all 0-1 DEG
  (`Ndufs2 = 1`, `Ndufv1 = 0`, `Ndufaf5 = 0`), represented cytochrome-c
  oxidase genes were 0-1 DEG (`Cox5a = 1`, `Cox11 = 0`), and `Sdha = 1`.
  Runtime profile correlations between these structural targets and `Nrf1`,
  `Nop56`, or `Opa1` were near zero.
- The literature-specific ZBTB11 partners were useful mostly as boundaries.
  `Otx2` is a Zbtb11 partner in Xenopus anterior neuroectoderm patterning
  (Satou-Kobayashi et al.), but `Otx2` itself had `n_degs = 0` and the
  Distributed Agents corpus reports no robust P16 postnatal neuronal response for Otx2
  or its developmental relatives in the assayed groups.  SET was reported as a
  lung-cancer ZBTB11 cofactor by Xu et al.; in this neuronal screen `Set = 0`
  and `Setbp1 = 0`, and the corpus describes Set as having no strong coherent
  neuronal neighbor.  `Zfp131`, the ESC partner from Garipler et al., and
  `Gabpa`/`Gabpb`, the direct NRF-2/GABP factors from Wilson et al., were not
  present as focal training targets.
- ZBTB paralogs were poor positive analogs.  `Zbtb7a` had a very broad
  response (`841` DEGs) but is a different BTB transcription factor with a
  distinct 151 signature; `Zbtb18` had only 5 DEGs, and the other measured
  ZBTB targets were mostly null.

I therefore predict a nonzero but not large focal response.  The direct
complex-I and cytochrome-c oxidase targets put a hard lower-bound warning on
mitochondrial structural biology; the active transcription-factor comparators
show that nuclear regulation can be visible; and the NOP56/OPA1 scale is a
better quantitative compromise for ZBTB11's expected RNA/mitochondrial
survivor-state response than either the 0-1 DEG structural genes or the
hundreds-to-thousands of DEG proteostasis and unrelated ZBTB7A responses.

**Point prediction: `Zbtb11 -> 37` DEGs.**

## Limits

There is no measured Zbtb11 signature or same-experiment corpus report for
Zbtb11 in the model-visible inputs.  The closest direct biochemical partners,
`Gabpa`, `Gabpb`, `Zfp131`, and `Acsf3`, were absent as focal training
perturbations, so every same-experiment comparison is one or more mechanistic
steps away.  Most ZBTB11 literature uses proliferating cells, fibroblasts,
embryonic patterning systems, cancer cells, or germline human genetics rather
than acute partial CRISPR loss in recovered postmitotic mouse neurons.  The
focal endpoint also censors cells that failed to survive, be captured, or keep
their class identity 3-4 weeks after editing, and it counts only BH-significant
nuclear-RNA effects, so a true mitochondrial or ribosome-biogenesis defect
could remain below this transcriptional threshold.
