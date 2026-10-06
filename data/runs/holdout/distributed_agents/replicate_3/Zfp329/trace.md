# Question and interpretation

The held-out target for this run is `Zfp329`.  I interpreted the task as a point
prediction of the number of genes that would satisfy `pvals_adj < 0.05` in the
`151 TH Prkcd Grin2c Glut` cell group after acute mosaic AAV-CRISPR loss of
`Zfp329`.

Ambiguities I resolved:

- I used only the supplied held-in differential-expression parquet and the
  focal-cell training counts for assay calibration.  `Zfp329` is absent from
  both as a perturbation target, so there is no direct expression signature to
  correlate.
- I treated zero as a real prediction of no measured focal-cell genes crossing
  the FDR 0.05 endpoint, not as failed editing or complete lack of biological
  function.
- I used same-experiment signatures from related zinc-finger and transcriptional
  regulators as analogs or counterexamples, and then used external annotation to
  decide whether those analogs were mechanistically close enough.

# Sources

- Input count endpoint:
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
- Input per-gene DE table:
  `[local file: training_de_all_cell_groups.parquet]`.
- Requested-target manifest:
  `[local file: 269_Zfp329.csv]`.
- Distributed Agents same-experiment corpus:
  `perturbai-july-260713-sourceguard-1773-v1`.
- NCBI Gene, Mus musculus `Zfp329`, GeneID `67230`, updated 2026-08-12.
  The entry maps the locus to Ensembl `ENSMUSG00000057894`, MGI `MGI:1921283`,
  and summarizes Alliance of Genome Resources July 2025 predictions of nuclear
  RNA-polymerase-II transcriptional regulation.
- UniProtKB/Swiss-Prot `ZN329_MOUSE`, accession `Q6GQR8`, entry version 165,
  annotation update 2026-09-02.  This entry annotates a 522-aa nuclear protein
  with 12 C2H2 zinc-finger repeats and the function comment "May be involved in
  transcriptional regulation".  Its cDNA evidence includes the FANTOM3
  transcriptome study, Carninci et al. 2005, PMID 16141072,
  DOI `10.1126/science.1112014`.
- PubMed searches for exact `Zfp329` and `ZNF329`.  I found no primary mouse
  `Zfp329` functional paper and did not use sparse human `ZNF329` disease
  association hits as mechanistic evidence for this neuronal perturbation.

# Computational calibration

I read the requested manifest and confirmed it contained exactly:

```tsv
target_name
Zfp329
```

I then filtered the parquet to `group_name == "151 TH Prkcd Grin2c Glut"` and
joined those signatures conceptually to the training-count CSV by
`gene_target`/`target_name`.  The focal count distribution was sparse:

- 1,674 held-in perturbations.
- 469/1,674 with at least one FDR-significant gene.
- 1,205/1,674, or 72.0%, with `n_degs == 0`.
- median 0, 75th percentile 1, 90th percentile 2, 95th percentile 18.
- a very long upper tail, led by `Uba5` 2677, `Tpr` 1768, `Sin3a` 1433,
  `Rnpc3` 868, and `Zbtb7a` 841.

For family-level calibration I enumerated all held-in perturbations whose names
start with `Zfp`, and also inspected nearby C2H2 classes such as `Zkscan*` and
`Klf*`.  Canonical held-in `Zfp` targets were mostly null: 24 of 29 had zero
DEGs.  The nonzero `Zfp` endpoint counts were:

| perturbation | training `n_degs` | strongest focal-cell rows |
| --- | ---: | --- |
| `Zfp423` | 150 | `Grid2ip` -1.27, q=3.1e-45; `Cd47` -0.99, q=1.3e-35; `Ntsr1` +5.14, q=5.9e-21 |
| `Zfp236` | 19 | `Ogt` -0.71, q=1.5e-38; `Eif4a2` -0.70, q=2.7e-19; `Gdi1` -0.40, q=1.9e-11 |
| `Zfp148` | 8 | `Ypel4` -0.54, q=0.0016; `Srrm2` -0.29, q=0.0016; `Plekhj1` +0.58, q=0.0025 |
| `Zfp612` | 1 | `Notum` +1.01, q=1.6e-07 |
| `Zfp692` | 1 | `Zfp692` +0.51, q=0.022 |

Representative null C2H2/Zfp-like perturbations included `Zfp1`, `Zfp106`,
`Zfp160`, `Zfp182`, `Zfp266`, `Zfp280c`, `Zfp280d`, `Zfp292`, `Zfp322a`,
`Zfp341`, `Zfp397`, `Zfp451`, `Zfp462`, `Zfp521`, `Zfp536`, `Zfp609`,
`Zfp644`, `Zfp654`, `Zfp664`, `Zfp804a`, `Zfp846`, `Zfp949`, `Zfp950`,
`Zfp961`, `Zkscan1`, and `Zkscan16`.  In these null examples the smallest
adjusted P values in the focal cell group were typically 1.0, 0.95, or similar,
not a collection of near-threshold hits that would argue for a low nonzero
prediction.

# Target-specific reasoning for Zfp329

`Zfp329` is an annotated but poorly characterized mouse protein-coding gene.
NCBI Gene and UniProtKB agree that it is a nuclear C2H2 zinc-finger protein
predicted to regulate RNA-polymerase-II transcription.  UniProtKB annotates 12
C2H2 zinc fingers and no more specific effector domain or curated neuronal
pathway.  The exact `Zfp329` symbol returned no mouse PubMed papers.  Thus the
external prior is "sequence-specific transcription factor candidate", not a
well established developmental determinant or a component of a chromatin/RNA
complex.

The most relevant direct analogs in the training table are the many
uncharacterized `Zfp*` and `Zkscan*` perturbations that were transcriptionally
silent in the same focal cell group.  `Zfp1`, `Zfp160`, `Zfp182`, `Zfp266`,
`Zfp322a`, `Zfp397`, `Zfp846`, `Zfp950`, `Zfp961`, `Zkscan1`, and `Zkscan16`
all had zero observed DEGs, and the 24/29 zero rate among canonical `Zfp`
targets is higher than the 72% global zero rate.  This is strong within-dataset
evidence that loss of an arbitrary C2H2 zinc-finger gene in postnatal
thalamic glutamatergic neurons usually falls below this assay's FDR 0.05
readout.

The nonzero `Zfp` counterexamples point away from assigning `Zfp329` a large
count:

- `Zfp423` was the largest `Zfp` responder at 150 DEGs, but the Distributed Agents
  corpus describes it as a specific thalamic subtype and surface/ECM program.
  The same corpus reports that obvious `Zfp423` relatives and partner pathways
  such as `Zfp521`, `Ebf1/2/3`, BMP `Smad` targets, retinoic-acid receptors,
  `Zic` genes, and `Chd4` did not phenocopy the matched `Zfp423` response.
  A broad developmental 30-zinc-finger cofactor therefore should not be used as
  a family-wide proxy for `Zfp329`.
- `Zfp236` had 19 DEGs dominated by `Ogt` and `Eif4a2` down-regulation.  The
  same-experiment corpus calls this a narrow postnatal neuronal program and
  notes that perturbing the major downstream genes `Ogt`, `Eif4a2`, `Cpt1c`,
  and `Gdi1` did not recreate the `Zfp236` signature.  I found no evidence that
  `Zfp329` participates in this O-GlcNAc/translation-like state.
- `Zfp148` had 8 DEGs in the count table.  The corpus reports a small
  thalamus-restricted signature with down-regulated splicing/nuclear-speckle
  and synaptic/secretory genes, and explicitly rejects a canonical p53/cell-cycle
  readout in postmitotic neurons.  `Zfp148` is an established GC-box binding
  regulator rather than a close mechanistic match to `Zfp329`.
- `Zfp612` and `Zfp692` each had exactly one DEG.  These are better evidence
  for singleton edge cases than for a reproducible multi-gene `Zfp329`
  response.

I also considered chromatin and C2H2 transcription-factor neighbors that are
not named `Zfp`.  `Klf9` had 19 DEGs, `Kmt2a` 24, `Setdb1` 22, and `Kdm5c` 18,
but other family members such as `Klf1`, `Klf11`, `Klf12`, `Klf13`, `Kdm4b`,
`Kdm4c`, `Kdm5b`, `Kdm6b`, and `Kmt2c` were zero.  Those counts imply that
postmitotic 151 TH Prkcd Grin2c Glut cells can detect a modest regulatory
phenotype when the target has the right role, but they do not lift the prior for
an uncharacterized C2H2 gene without a known thalamic program.

Combining these observations, I predict that `Zfp329` will be below the FDR
0.05 endpoint in the focal cell type.  I choose an exact point of **0 DEGs**:
the held-in family calibration has many clean zeros, the one-gene `Zfp612` and
`Zfp692` cases show only fragile singleton responses, and the larger `Zfp148`,
`Zfp236`, and `Zfp423` signatures have recognizable target-specific mechanisms
that should not be transferred to `Zfp329`.

# Limits

The main uncertainty is that `Zfp329` itself has almost no curated biology.
Database annotation tells me domain class and predicted nuclear DNA binding but
not its binding motif, its expression level in this thalamic subtype, or whether
it cooperates with an unavailable partner in juvenile neurons.  Because the
held-out `Zfp329` signature is completely absent, I could not check whether its
actual transcriptome resembles any measured training perturbation.  The
prediction is therefore a local extrapolation from weakly annotated C2H2/Zfp
neighbors and from the sparse global response distribution, not a direct
phenocopy assignment.
