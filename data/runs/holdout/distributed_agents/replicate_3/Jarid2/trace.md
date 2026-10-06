# Prediction trace

## Question and resolved ambiguities

The requested held-out perturbation set contains a single mouse target, `Jarid2`.
I treated the endpoint as the exact focal-cell count of measured genes with
Benjamini-Hochberg adjusted Wilcoxon `pvals_adj < 0.05` in
`151 TH Prkcd Grin2c Glut`, where the cell label denotes a thalamic
glutamatergic class. A prediction of `0` means that I expect no measured
transcript, excluding no special self-transcript rule, to cross that corrected
threshold in this class.

The held-out `Jarid2` row was absent from both the differential-expression
parquet and the supplied training count CSV, so all quantitative calibration
came from non-held-out targets.

## Sources

- Supplied training endpoint:
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
  It contains 1,674 non-held-out targets; 1,205 had `n_degs = 0`, 363 had
  `1-9`, 63 had `10-89`, and 43 had at least `100` DEGs in the focal class.
- Supplied differential-expression table:
  `[local file: training_de_all_cell_groups.parquet]`.
  I filtered it to `151 TH Prkcd Grin2c Glut` and a curated comparator set,
  then counted rows with `pvals_adj < 0.05` and inspected the leading
  significant rows.
- Distributed Agents same-experiment semantic corpus
  `perturbai-july-260713-sourceguard-1773-v1`. The corpus did not expose
  target-scoped `Jarid2` findings, so I used it only for same-experiment
  interpretations of training comparators such as `Kdm6b`, `Bap1`, `Yy1`, and
  `Setd1a`.
- Public literature from PubMed for the external PRC2/JARID2 mechanism:
  Pasini et al. 2010, DOI `10.1038/nature08788`, PMID `20075857`; Kaneko et
  al. 2013, DOI `10.1016/j.molcel.2013.11.012`, PMID `24374312`; Sanulli et
  al. 2015, DOI `10.1016/j.molcel.2014.12.020`, PMID `25620564`; Cooper et
  al. 2016, DOI `10.1038/ncomms13661`, PMID `27892467`; Petracovici and
  Bonasio 2021, DOI `10.1016/j.molcel.2021.03.038`, PMID `33887196`; Thomas et
  al. 2023, DOI `10.1126/sciadv.adg9832`, PMID `37556531`; Palomer et al.
  2016, DOI `10.1038/ncomms11081`, PMID `27010597`.

## Computation over the supplied data

I first verified that the manifest has only `Jarid2`, and that canonical PRC2
subunits or cofactors were unavailable as direct training perturbations in the
focal endpoint table: `Eed`, `Ezh1`, `Ezh2`, `Suz12`, `Rbbp4`, `Rbbp7`,
`Aebp2`, `Mtf2`, `Phf1`, `Phf19`, `Epop`, `Ring1`, and `Rnf2` were not present
as training `target_name` values. The relevant parquet scans used Arrow dataset
filters of the following form:

```python
flt = (
    (pc.field("group_name") == "151 TH Prkcd Grin2c Glut")
    & pc.field("gene_target").isin(candidate_targets)
    & (pc.field("pvals_adj") < 0.05)
)
```

For whole-profile comparison of selected chromatin perturbations, I used
Distributed Agents runtime `profile_compare` on `logfoldchanges` vectors in the focal
cell group, with `pvals_adj` as the significance column, against the 1,674
eligible training targets. This was diagnostic rather than predictive by
itself because `Jarid2` has no held-out expression vector.

## Training comparators

The most direct textbook PRC2 analogs were missing, so the useful evidence was
mostly boundary evidence.

| training target | focal `n_degs` | why it mattered |
| --- | ---: | --- |
| `Kdm6b` | 0 | Encodes the H3K27me3 demethylase JMJD3 and is an enzymatic antagonist of the H3K27 methylation written by PRC2. Palomer et al. showed KDM6B/JMJD3 and H3K27 demethylation can regulate neuronal activity-dependent derepression at `Bdnf`. In this screen, however, `Kdm6b` had no focal DEGs; the Distributed Agents corpus also summarized it as FDR-null in every recovered neuronal group and explicitly noted that this null occurred despite `Setd1a`, `Smarcc2`, `Rora`, `Kmt2a`, `Setdb1`, `Kdm5c`, `Crebbp`, and `Setd5` being detectable in the same thalamic group. |
| `Bap1` | 16 | Polycomb-repressive deubiquitinase catalytic subunit; BAP1/ASXL1 removes H2AK119ub, the PRC1 mark that JARID2 can bind to help PRC2 localize, as described for PR-DUB by Thomas et al. 2023 and for JARID2-H2AK119ub crosstalk by Cooper et al. 2016. Its effect was real but small in the focal group; leading DEGs included `Scg2`, `Serpine2`, `Cnot9`, and `Coro6`. Corpus finding `Bap1:F006` further reported that represented PR-DUB relatives such as `Asxl3`, `Foxk2`, and `Ogt` did not phenocopy acute `Bap1` loss in matched neuronal groups. |
| `Yy1` | 720 | YY1 is a DNA-binding factor that can recruit or cooperate with Polycomb at some mammalian loci, and Boyd et al. 2015 linked YY1/JARID2/EZH2 at the `CIITA` promoter. In the training data it was broad, with 277 up and 443 down focal DEGs; Distributed Agents finding `Yy1:F003` specifically observed mixed rewiring of Polycomb/chromatin transcripts rather than uniform PRC shutdown. That makes `Yy1` a poor count analog for `Jarid2`: its 720-gene footprint is dominated by YY1's wider transcriptional and RNA-processing roles. |
| `Dnmt3a` | 0 | Another chromatin repressor with developmental roles, included as a negative chromatin boundary. Its focal absence argues that not every developmental epigenetic regulator yields a corrected postmitotic signature after sparse P16 CRISPR loss. |
| `Setd1a` | 368 | H3K4 methyltransferase with a large focal response. It was used as a positive chromatin control: the assay readily sees some writer complexes in this exact cell class. Distributed Agents `Setd1a` findings placed its state in a mitochondrial / organelle-maintenance / RNA-biogenesis program rather than a generic Polycomb state. |
| `Kmt2a`, `Setdb1` | 24, 22 | Active but small-to-medium chromatin-writer boundaries. `Kmt2a` self-target and `Setdb1`/`Tasor`/`Atf7ip` rows showed that focal signatures can be narrow even for nuclear chromatin regulators. |
| `Chd4`, `Chd8`, `Smarcc2`, `Brd4`, `Phf12` | 100, 61, 185, 311, 403 | Broad chromatin/remodeling controls. They establish that a strong chromatin phenotype was observable in `151 TH Prkcd Grin2c Glut`, but they are not mechanistically close to PRC2. Their log-fold-change profiles also did not define a clean Polycomb module with `Kdm6b` or `Bap1`. |
| `Smarca4`, `Ep300`, `Kat6a`, `Kat6b`, `Mbd2`, `Phf6`, `Phf8`, `Kdm4b`, `Kdm4c`, `Kdm5b`, `Kmt2c` | 0 | Additional null chromatin or chromatin-adjacent perturbations. These are counterexamples to predicting a nonzero value merely because `Jarid2` is a chromatin regulator or disease/development gene. |

I also checked whether the comparator perturbations changed endogenous `Jarid2`
or PRC2 core transcripts in the focal cell group. None of `Kdm6b`, `Bap1`,
`Setd1a`, `Kmt2a`, `Setdb1`, `Smarcc2`, `Smarce1`, `Arid1a`, `Smarca4`,
`Dnmt3a`, `Chd4`, `Chd8`, or `Brd4` significantly moved `Jarid2`, `Eed`,
`Ezh1`, `Ezh2`, or `Suz12` at FDR 0.05. `Yy1` induced `Eed` nominally
(`log2FC = 0.353`, `pvals_adj = 0.0218`) and changed `Ring1`, but left
`Jarid2` itself just above threshold (`log2FC = -0.230`, `pvals_adj = 0.0586`);
this supports the corpus interpretation that the `Yy1` signature touches
Polycomb transcripts without being a simple PRC2 knockdown phenocopy.

## `Jarid2` rationale

External biology makes `Jarid2` a real PRC2 regulator rather than an arbitrary
JmjC-domain gene. Pasini et al. 2010 showed that JARID2 forms a stable complex
with PRC2, occupies most mapped PRC2 target genes in mouse embryonic stem
cells, and is needed for normal PRC2 binding and H3K27me3 at target genes.
Kaneko et al. 2013 showed that lncRNAs can facilitate JARID2-PRC2 recruitment
to chromatin. Sanulli et al. 2015 showed that PRC2 methylates JARID2 and that
EED recognizes methylated JARID2 to allosterically tune PRC2 activity. Cooper
et al. 2016 showed that JARID2 binds H2AK119ub to mediate crosstalk from PRC1
to PRC2. Petracovici and Bonasio 2021 further separated `JARID2`-sensitive
PRC2.2 establishment of new Polycomb repression from MTF2/PRC2.1 maintenance
during embryonic-stem-cell-to-neural-progenitor differentiation.

Those papers make the predicted direction non-null in embryonic or actively
differentiating contexts, but this experiment perturbs sparse postmitotic
NeuN+ neurons at P16 and profiles surviving nuclei 3-4 weeks later. In that
setting, the dataset-visible analogs point the other way. `Kdm6b`, the closest
available H3K27me3 turnover antagonist, was completely flat in the focal class
and across the broader atlas according to the Distributed Agents corpus. The
Polycomb-adjacent PR-DUB node `Bap1` had only 16 focal DEGs, and its own
same-experiment report argued that PR-DUB biochemical relatives were
non-phenocopied after acute neuronal perturbation. The one very broad
Polycomb-linked training factor, `Yy1`, had a mixed posterior chromatin/RNA
processing signature that does not behave like an isolated PRC2.2 defect.

I therefore expect `Jarid2` loss to be buffered in this postnatal thalamic
readout: established H3K27me3 domains can be maintained without an acute
JARID2-dependent de novo recruitment step, other PRC2 cofactors and PRC1 marks
can partially compensate, and a non-catalytic accessory-subunit perturbation is
less likely to cross hundreds of single-nucleus Wilcoxon tests than loss of
global transcription/chromatin regulators such as `Yy1` or `Setd1a`. The
closest class is `n_degs = 0`, so the point prediction is:

| target | predicted focal `n_degs` |
| --- | ---: |
| `Jarid2` | 0 |

## Limits

This prediction is an extrapolation because the decisive PRC2 comparators
`Eed`, `Ezh2`, `Suz12`, `Rbbp4`, `Rbbp7`, `Aebp2`, `Mtf2`, `Phf1`, and
`Phf19` were not in the training target universe. `Kdm6b` is an H3K27me3
antagonist, not a PRC2.2 subunit; `Bap1` works on H2AK119ub rather than
H3K27me3; and `Yy1` has extensive PRC2-independent transcriptional biology.
The public JARID2 literature is strongest in embryonic stem cells, neural
progenitor differentiation, X inactivation, and non-neuronal systems, so it
does not cleanly quantify acute partial CRISPR loss in surviving juvenile
postmitotic thalamic neurons. A small one- to ten-gene `Jarid2` response would
therefore be plausible, but the training evidence did not justify moving the
point estimate above zero.
