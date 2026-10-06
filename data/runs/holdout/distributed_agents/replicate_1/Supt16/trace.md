# Supt16 DEG-count prediction

## Question and resolved ambiguities

The requested endpoint is the integer number of focal-cell genes with
Benjamini-Hochberg adjusted Wilcoxon `pvals_adj < 0.05` after perturbing the
held-out gene in `151 TH Prkcd Grin2c Glut` neurons.  The one requested target
was `Supt16`; I treated that as the mouse gene symbol in the manifest and as the
ortholog of mammalian `SUPT16H`, the SPT16 subunit of the FACT histone
chaperone.  I did not interpret the count as viability, editing efficiency, or
absolute biological importance; it is an assay-specific count of FDR-significant
snRNA abundance changes among recovered nuclei.

## Sources used

- Declared PerturbAI differential-expression parquet:
  `training differential-expression dataset`.
- Declared training endpoint CSV:
  `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
- Declared requested-target CSV:
  `single-target request for Supt16`.
- The same-experiment semantic corpus `perturbai-july-260713-sourceguard-1773-v1`,
  especially report Findings for `Brd4`, `Setd1a`, `Smarcc2`, `Chd4`, `Chd8`,
  `Chd2`, `Cdk13`, and `Med15`.  I used those as compact descriptions of the
  parquet signatures from the same experiment, not as independent replication.
- PubMed-indexed external FACT literature: Belotserkovskaya et al. 2003,
  DOI `10.1126/science.1085703`; Winkler et al. 2011,
  DOI `10.1074/jbc.M111.301465`; Li et al. 2007,
  DOI `10.1074/jbc.M603822200`; Safina et al. 2013,
  DOI `10.4161/cc.25452`; Wang et al. 2021,
  DOI `10.1080/15384101.2021.1881726`.

## Dataset calculations

The training table contained 1,674 held-in biological perturbations for the
focal cell group: 1,205 had `n_degs = 0`, 469 had a nonzero response, the median
was 0, the 95th percentile was 18, and the largest focal responses were very
skewed (`Uba5` 2677, `Tpr` 1768, `Sin3a` 1433).

I then scanned the declared parquet only for `151 TH Prkcd Grin2c Glut` rows
from a small set of chromatin, RNAPII, Mediator, and BAF/NuRD comparators:

```sql
SELECT names, gene_target, scores, logfoldchanges, pvals_adj,
       n_pert_matched, n_ctrl_matched
FROM training_de_all_cell_groups
WHERE group_name = '151 TH Prkcd Grin2c Glut'
  AND gene_target IN (<selected chromatin/RNAPII targets>);
```

Those parquet counts reproduced the endpoint CSV exactly for the selected
targets.  The most relevant focal counts were:

| Training perturbation | 151 FDR<0.05 DEGs | Relevance to Supt16 |
| --- | ---: | --- |
| `Brd4` | 311 | Acetyl-chromatin reader that supports Pol II elongation; broadest RNAPII/chromatin training analog. |
| `Setd1a` | 368 | COMPASS/H3K4 methyltransferase; a high-count active chromatin counterpoint but not an elongation chaperone. |
| `Smarcc2` | 185 | BAF scaffold; showed that acute disruption of some chromatin complexes can produce a clear thalamic signature. |
| `Chd4` | 100 | NuRD ATPase; postmitotic thalamic chromatin-remodeling response but mechanistically distant from FACT. |
| `Chd8` | 61 | Chromatin/elongation-linked ASD gene with a restricted subcortical response. |
| `Cdk13` | 56 | RNAPII Ser2/splicing-linked kinase; a closer cotranscriptional analog than BAF/NuRD. |
| `Chd2` | 34 | ATP-dependent chromatin remodeler with a small but real 151 response. |
| `Med15`, `Med23`, `Med13` | 19, 13, 11 | Pol-II Mediator subunits that produced selective, low-count thalamic responses. |
| `Smarce1`, `Arid1a`, `Arid2` | 11, 22, 56 | BAF-family members with partial `Smarcc2` convergence. |
| `Setd2`, `Med13l`, `Smarca2`, `Smarcd1`, `Gatad2b` | 1 each | Same broad functional neighborhoods but essentially silent in 151. |
| `Smarca4`, `Smarcc1`, `Mbd2`, `Kat6a`, `Kat6b` | 0 each | Counterexamples showing that chromatin-complex membership alone did not imply a count above zero. |

The exact expression-pattern evidence also argued against treating all active
chromatin perturbations as one class.  `Smarcc2` and `Smarce1` were coherent
BAF comparators: 9 of the 11 `Smarce1` FDR hits were also significant for
`Smarcc2`, all in the same direction, and both repressed `Ptpn3`, `Reep2`,
`Prkcd`, `Abhd12b`, and `Begain`.  In contrast, active CHD and BAF targets
overlapped only partially: `Chd4` shared only 12 focal FDR genes with `Smarcc2`
and split them evenly by direction, and `Chd2` shared only 7 with `Smarcc2`.
The same-experiment corpus similarly reported that CHD paralogs, BAF/PBAF
subunits, and NuRD-associated genes did not cleanly phenocopy one another in
this P16-to-P37/44 thalamic assay.  Thus `Brd4` and `Setd1a` set an upper range
for visible core transcription/chromatin perturbations, but their hundreds of
DEGs are not a generic expectation for `Supt16`.

The parquet also included measured `Supt16` and `Ssrp1` transcript rows for all
1,674 held-in 151 perturbations.  Only `Tpr` drove `Supt16` itself below
FDR 0.05, and `Ssrp1` never passed FDR 0.05 as a measured gene in this focal
group.  I therefore did not use FACT-subunit RNA recurrence as evidence for a
large response.

## Supt16 target-specific reasoning

`Supt16` encodes the large SPT16 subunit of FACT, a conserved
`SUPT16H`/`SSRP1` histone chaperone.  FACT binds histones and nucleosomes and
can both disassemble and reassemble H2A-H2B/H3-H4-containing nucleosomes during
chromatin transcription; purified FACT was required for efficient RNA
polymerase II passage through nucleosomes in the classic in-vitro system
reported by Belotserkovskaya et al. 2003, and FACT has high-affinity histone,
DNA, and nucleosome contacts in the biochemical work of Winkler et al. 2011.
The mammalian knockdown experiment of Li et al. 2007 found surprisingly subtle
global mRNA changes after depletion of either SSRP1 or Spt16 in H1299 cells:
about 170 of 8,308 assayed transcripts crossed a 1.5-fold threshold and only
about 1.3% of genes changed by more than 1.2-fold in both subunit knockdowns.
Safina et al. 2013 further reported that SPT16/SSRP1 protein abundance falls on
differentiation or senescence, consistent with FACT being less dominant outside
proliferating states.  Wang et al. 2021 summarized the same core model: FACT is
a true chromatin regulator used in transcription, replication, and repair, not
a sequence-specific neuronal identity factor.

That biology made a zero prediction too conservative: the target is a direct
component of chromatin transcription machinery, and the focal thalamic group was
where this dataset most often revealed chromatin/RNAPII maintenance programs.
However, three parts of the same-experiment calibration kept the prediction
small.

First, the closest held-in RNAPII analogs were modest.  `Cdk13` produced 56
focal DEGs and its same-experiment report tied that response to
chromatin-coupled RNA processing rather than to a global Pol-II collapse.
Mediator subunits were lower still: `Med15`, `Med23`, and `Med13` had only
19, 13, and 11 focal DEGs despite being Pol-II coactivator machinery.
Second, no exact FACT partner was available: `Ssrp1` was not a training
perturbation, so there was no same-complex endpoint anchor analogous to the
informative `Smarcc2`/`Smarce1` pair.  Third, related chromatin complexes showed
large allele-, subunit-, and context-dependence.  `Brd4`, `Setd1a`, `Smarcc2`,
and `Chd4` prove that the assay could observe broad chromatin responses, but
`Smarca4`, `Smarcc1`, `Mbd2`, `Kat6a`, and `Kat6b` were null in the same
focal-cell endpoint.

I therefore placed `Supt16` just below the low Mediator/BAF positive
comparators rather than near the high-count chromatin regulators.  The point
prediction is nonzero because FACT directly supports nucleosomal transcription;
it is only 16 DEGs because differentiated postmitotic neurons should be less
dependent on replication-coupled FACT functions, the H1299 Spt16/SSRP1
transcriptional effect was sparse even after knockdown, and the exact PerturbAI
training surface gives many chromatin-complex counterexamples with zero or
near-zero focal FDR counts.

## Limits

The largest limitation is the absence of an `Ssrp1` held-in perturbation; the
prediction is transferred from general chromatin and RNAPII examples rather
than from the obligate FACT partner.  FACT has replication and DNA-repair roles
that are prominent in proliferating cells, but the requested assay sampled
postmitotic NeuN-positive nuclei 3-4 weeks after P16 AAV CRISPR, so those
priors only weakly constrain this endpoint.  The external SPT16/SSRP1
knockdown data came from human cancer cells, not mouse thalamic neurons, and
used RNAi rather than sparse Cas9 loss of function.  Finally, the endpoint is
FDR-thresholded; a prediction of 16 means I expect a weak visible
transcriptional footprint, not that exactly sixteen genes have a deterministic
biological state change.
