# Prediction trace for held-out Zbtb24

## Question and resolved ambiguities

The requested endpoint is a point prediction for the number of genes with
Benjamini-Hochberg-adjusted Wilcoxon `pvals_adj < 0.05` after knocking out the
held-out target in `151 TH Prkcd Grin2c Glut` nuclei.  The manifest for this
run contains one held-out target:

```tsv
target_name
Zbtb24
```

I treated the target as the mouse gene symbol `Zbtb24` exactly as written in the
manifest.  Because the held-out perturbation was absent as a `gene_target`, I
did not use any direct `Zbtb24` knockout row.  I used the raw parquet only for
non-held-out perturbations and computed all focal counts with the requested
FDR threshold of 0.05; some same-experiment corpus summaries use FDR 0.10 for
broader biological reports, so the exact counts below come from the training
count CSV or my direct `pvals_adj < 0.05` tabulation.

## Sources used

- Input endpoint table:
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
  This supplied the observed `n_degs` for the 1,674 non-held-out perturbations
  in the focal cell group.
- Input DE parquet:
  `[local file: training_de_all_cell_groups.parquet]`.
  I filtered this table to `group_name == "151 TH Prkcd Grin2c Glut"` to inspect
  focal signatures, significant genes, matched cell counts, and overlaps among
  candidate analogs.
- Requested-target manifest:
  `[local file: 265_Zbtb24.csv]`.
- Same-experiment internal corpus:
  Distributed Agents corpus release `perturbai-july-260713-sourceguard-1773-v1`.  This
  supplied curated interpretations of training perturbations and graph links
  among ZBTB-family, methylation-reader/writer, heterochromatin, and
  chromatin-remodeling perturbations.  Zbtb24 itself was not represented in this
  corpus release.
- PubMed literature for external biology:
  de Greef et al. 2011, DOI `10.1016/j.ajhg.2011.04.018`, PMID `21596365`;
  Wu et al. 2016, DOI `10.1093/hmg/ddw243`, PMID `27466202`;
  van den Boogaard et al. 2017, DOI `10.1111/cge.12979`, PMID `28128455`;
  Velasco et al. 2018, DOI `10.1093/hmg/ddy130`, PMID `29659838`;
  Unoki et al. 2018, DOI `10.1172/JCI99751`, PMID `30307408`;
  Ren et al. 2019, DOI `10.1093/nar/gkz557`, PMID `31226215`;
  Hardikar et al. 2020, DOI `10.1007/s13238-019-00682-w`, PMID `31970665`;
  Unoki et al. 2020, DOI `10.1038/s41598-020-74636-2`, PMID `33082427`.

## Computational checks

I loaded the focal training-count CSV and used it to calibrate the scale:

- 1,205 of 1,674 training targets were zero in `151 TH Prkcd Grin2c Glut`
  at FDR 0.05.
- 363 targets had 1-9 DEGs.
- 63 targets had 10-99 DEGs.
- 43 targets had at least 100 DEGs.
- The distribution was very skewed: median 0, 75th percentile 1, 95th
  percentile 18, maximum 2,677.

For candidate analogs, I filtered the parquet to the focal group and recomputed
`sum(pvals_adj < 0.05)` per `gene_target`.  I also inspected the top genes in
each signature and compared FDR-level overlap, because broad whole-transcriptome
correlations were moderately positive even between near-null signatures and
therefore were too weak to serve as a mechanistic match by themselves.

The direct ICF-axis genes `Cdca7`, `Hells`, and `Dnmt3b` were present as
measured transcripts in the focal matrix but were not present as perturbation
targets in the training endpoint table.  Thus the training set lacked the
ideal ICF3, ICF4, and DNMT3B analog knockouts.

## Zbtb24 biology relevant to the held-out perturbation

ZBTB24 is a BTB/C2H2 zinc-finger transcription factor.  Biallelic loss-of-function
or zinc-finger variants in human `ZBTB24` cause ICF2 syndrome, one of the four
known ICF genotypes together with `DNMT3B`, `CDCA7`, and `HELLS`
(de Greef et al. 2011; van den Boogaard et al. 2017).  Wu et al. showed that
functional mouse Zbtb24 is required early in development and that ZBTB24 directly
activates `Cdca7`; `Cdca7` was the top down-regulated gene in Zbtb24-mutant
mouse embryonic stem cells and was rescued by ectopic ZBTB24 (Wu et al. 2016).
Ren et al. then defined a ZBTB24 DNA-binding consensus, confirmed binding at the
`Cdca7` promoter, and showed that ICF-associated zinc-finger mutations disrupt
specific DNA binding and fail to induce Cdca7 (Ren et al. 2019).

The best current pathway model is therefore not that ZBTB24 is an isolated
postmitotic neuronal fate factor.  It is an upstream transcriptional activator
for the CDCA7-HELLS chromatin-remodeling arm that helps methylate pericentromeric
satellite repeats and a subset of CpG-poor heterochromatin loci.  Comparative
ICF patient methylomes linked `ZBTB24`, `CDCA7`, and `HELLS`, and separated that
axis from ICF1/DNMT3B at subtelomeric and methylome features (Velasco et al.
2018).  Hardikar et al. reported that the ZBTB24-CDCA7 axis regulates HELLS
enrichment at centromeric satellite repeats (Hardikar et al. 2020).  CDCA7 and
HELLS also contribute to classical nonhomologous end joining and suppression of
DNA:RNA hybrid-associated damage at pericentromeric repeats in ICF cell models
(Unoki et al. 2018; Unoki et al. 2020).  Much of this literature is in stem,
fibroblast, lymphoblastoid, or immune cells, which is an imperfect match to an
acute P16 CRISPR loss-of-function perturbation in recovered postmitotic neurons.

## Within-dataset analogs and counterexamples

### ZBTB-family perturbations

The represented ZBTB-family members in the focal training data were mostly null
or very weak:

| target | focal n_degs | focal evidence |
| --- | ---: | --- |
| `Zbtb10` | 0 | no FDR 0.05 genes among 187 matched perturbed nuclei |
| `Zbtb16` | 0 | no FDR 0.05 genes among 180 matched perturbed nuclei |
| `Zbtb18` | 5 | small positive signature: `Endou`, `Pxdn`, `Clstn2`, `Man2a2`, and self-transcript `Zbtb18` |
| `Zbtb20` | 0 | no FDR 0.05 genes among 185 matched perturbed nuclei |
| `Zbtb21` | 0 | no FDR 0.05 genes among 137 matched perturbed nuclei |
| `Zbtb38` | 1 | single FDR gene, `Msra` |
| `Zbtb7a` | 841 | a broad endomembrane/proteostasis-like transcriptional state |

The Distributed Agents corpus contains a high-confidence ZBTB-family claim stating that
shared BTB-ZF/ZBTB membership was insufficient to predict a common postmitotic
neuronal transcriptomic phenotype in this experiment.  It specifically contrasts
flat `Zbtb10`, `Zbtb16`, `Zbtb20`, and `Zbtb21` with sparse `Zbtb18`/`Zbtb38`
effects and the broad but biologically distinct `Zbtb7a` signature.  This is
important for `Zbtb24`: the family comparison says that ZBTB domain architecture
alone should not pull the estimate upward.

`Zbtb7a` is the main counterexample.  Its 841-DEG focal signature proves that
some ZBTB transcription factors are strongly visible in these nuclei, but it is
not a close ICF-pathway analog.  The same-experiment `Zbtb7a` reports place its
nearest FDR-backed neighbors near UFMylation/proteostasis perturbations such as
`Uba5` and `Ufc1`, not near other ZBTB paralogs.  I therefore treated it as a
detectability control and outlier rather than as a predictor for `Zbtb24`.

### DNA-methylation and heterochromatin perturbations

The training set did not include `Cdca7`, `Hells`, `Dnmt3b`, `Dnmt1`, `Uhrf1`,
or `Uhrf2`.  I therefore used less direct methylation and repressive-chromatin
analogs:

| target | focal n_degs | relationship to Zbtb24 |
| --- | ---: | --- |
| `Dnmt3a` | 0 | de novo DNA methyltransferase/mCH writer; direct DNMT3B was not assayed |
| `Smchd1` | 0 | heterochromatin and long-range repressive regulator |
| `Lrrfip1` | 0 | represented Zbtb7a/heterochromatin-neighborhood counterexample, but no focal output |
| `Atrx` | 8 | H3.3/heterochromatin remodeler; sparse focal signature with `Resp18`, `Csf2ra`, `Cyp46a1`, `Pigk`, `Pnpla6`, `Begain`, `Ablim1`, `Pxdn` |
| `Mecp2` | 16 | methyl-CpG reader; modest thalamic signature, biologically nonidentical to methylation establishment |
| `Setdb1` | 22 | H3K9 methyltransferase; narrow HUSH/protocadherin response |
| `Chd4` | 100 | NuRD ATPase; broader local chromatin response |
| `Ctcf` | 270 | genome architecture/protocadherin regulator; broad counterexample |

The same-experiment corpus sharpened this comparison.  Its `Dnmt3a` reports show
that acute P16 `Dnmt3a` loss was completely flat across measured neuronal groups
and did not phenocopy `Mecp2`; this fits the idea that losing a cumulative DNA
methylation writer for only 3-4 weeks is buffered in recovered postmitotic
neurons.  `Setdb1` was detectable but narrow and specifically induced HUSH and
gamma-protocadherin transcripts, and the corpus explicitly notes that this was
not reproduced by neighboring `Dnmt3a` or `Smchd1` perturbations.  `Atrx` also
had a restricted state and did not overlap Setdb1 or Mecp2 at FDR level.  These
training perturbations argue for a small or zero coding-gene signature for a
Zbtb24-axis perturbation unless the exact CDCA7/HELLS branch has an acute
neuron-specific transcriptional role not captured by the represented analogs.

The medium and large chromatin perturbations, especially `Chd4`, `Ctcf`,
`Zbtb7a`, and `Sin3a` in the broader training table, are useful negative
controls against a purely technical null call: `151 TH Prkcd Grin2c Glut` can
emit 100 to 1,000+ FDR genes for nuclear regulatory perturbations.  They are not
strong mechanistic templates for `Zbtb24`, whose canonical downstream biology is
the CDCA7-HELLS heterochromatin/ICF axis rather than NuRD failure, CTCF loop
maintenance, or the Zbtb7a neuronal endomembrane state.

## Zero/nonzero decision for Zbtb24

I assigned `Zbtb24` to the null class for this focal endpoint.

The evidence driving that decision is mostly within-dataset evidence, with
external biology used to choose the analogs:

- The direct ICF pathway was under-represented in the training perturbations:
  no `Cdca7`, `Hells`, or `Dnmt3b` knockout was available, so there was no
  positive same-complex signature to transfer.
- Five of seven represented ZBTB-family perturbations had zero or one DEG in
  the focal endpoint, and `Zbtb18` had only five.  The single very broad family
  outlier, `Zbtb7a`, was biologically divergent in the internal corpus.
- The closest represented methylation/heterochromatin analogs were zero to
  weak: `Dnmt3a` 0, `Smchd1` 0, `Atrx` 8, `Mecp2` 16, and `Setdb1` 22.  Their
  significant genes were largely non-overlapping, so there was no repeated
  ICF-like expression pattern pointing to a definite nonzero Zbtb24 signature.
- The strongest external functions for ZBTB24 are DNA methylation maintenance
  at repeats through CDCA7/HELLS and cell proliferation or immune-cell ICF
  phenotypes.  Those mechanisms are plausible but not obviously rate-limiting
  for a sparse, acute, postmitotic neuronal CRISPR perturbation harvested
  3-4 weeks later.

I considered a weak nonzero estimate of 1-5 because ZBTB24 is an authentic
transcription factor and because ZBTB-family members such as `Zbtb18` and
`Zbtb38` showed sparse focal markers.  I left the prediction at zero because
the Zbtb24-specific CDCA7/HELLS biology looked more developmentally and
heterochromatically buffered than those sparse fate-factor readouts, and
because the training prior is very sparse: roughly 72% of biological targets in
this same focal endpoint were exact zeroes at FDR 0.05.

## Limits and extrapolations

- This is extrapolation.  `Zbtb24`, `Cdca7`, `Hells`, and `Dnmt3b` perturbations
  were absent from the supplied training endpoint, so the most direct analogs
  could not be measured.
- ICF patient, stem-cell, fibroblast, and lymphoid models may not transfer to
  sparse CRISPR loss of function in postmitotic thalamic glutamatergic neurons.
- The assay measured nuclear coding-gene RNA in recovered nuclei.  It did not
  measure pericentromeric repeats, DNA methylation, HELLS recruitment, genome
  instability, DNA indels, or pre-capture viability.
- A zero DEG prediction is not a claim that Zbtb24 editing would be absent or
  biologically irrelevant; it means I expect no measured coding gene to pass the
  stringent FDR 0.05 Wilcoxon threshold in this exact cell group and assay.
- Some analogs had fewer matched perturbed nuclei than the ZBTB-family rows
  (`Atrx` 98, `Setdb1` 113, `Ctcf` 129), so their exact counts include power
  effects.  Nonetheless, the same focal group detected medium and strong
  chromatin signatures at comparable cell counts.

## Final point prediction

`Zbtb24`: `0` differentially expressed genes.
