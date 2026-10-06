# Smc3 DEG-count prediction trace

## Question and resolved ambiguities

The task is to predict, for each gene in `214_Smc3.csv`, the held-out
`n_degs` endpoint in `151 TH Prkcd Grin2c Glut`: the number of measured
genes with Benjamini-Hochberg-adjusted Wilcoxon `pvals_adj < 0.05` after an
acute AAV-PHP.eB CRISPR loss-of-function perturbation in juvenile/postnatal
mouse neurons.

The requested manifest contains one target, `Smc3`. `Smc3` was absent from both
the all-cell differential-expression parquet and the focal-cell training-count
CSV, so I treated the problem as a forward prediction from measured
non-held-out genes. Several same-experiment corpus findings summarize
FDR<0.10 analyses; I used those only as curated qualitative same-experiment
context and used the supplied FDR<0.05 count CSV as the numerical endpoint.

## Sources used

- `training_de_all_cell_groups.parquet`: focal-group log2 fold changes,
  adjusted p-values, matched perturbed-cell counts, and expression profiles for
  non-held-out perturbations.
- `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`: exact FDR<0.05 `n_degs`
  values for the non-held-out perturbations in the focal cell group.
- The selected Distributed Agents same-experiment corpus,
  `perturbai-july-260713-sourceguard-1773-v1`, especially the `Smc1a`,
  `Stag2`, `Ctcf`, `Hdac8`, `Pds5a`, and `Stag1` findings and the shared
  claim that `Smc1a` and `Stag2` share a restricted thalamic same-direction
  module not reproduced by `Stag1`, `Pds5a`, `Hdac8`, `Ncapd3`, `Prr12`,
  `Zfp609`, or `Smchd1`.
- Gene Ontology and Reactome functional/pathway annotations as external
  database priors for cohesin membership and the cohesin loading/release cycle.
- External literature:
  - Deardorff et al., 2012, Nature, DOI `10.1038/nature11316`,
    PMID `22885700`: cohesin contains SMC1, SMC3, RAD21, and a STAG subunit;
    HDAC8 is the vertebrate SMC3 deacetylase.
  - Guo et al., 2012, PNAS, DOI `10.1073/pnas.1219280110`,
    PMID `23204437`: CTCF/cohesin-mediated DNA looping is required for
    protocadherin promoter choice.
  - Merkenschlager and Odom, 2013, Cell, DOI `10.1016/j.cell.2013.02.029`,
    PMID `23498937`, and Seitan et al., 2013, Genome Research,
    DOI `10.1101/gr.161620.113`, PMID `24002784`: cohesin and CTCF form
    long-range chromatin interactions that support regulated transcription.
  - Yamada et al., 2019, Nature, DOI `10.1038/s41586-019-1190-7`,
    PMID `31068695`: adult mouse cerebellar granule-neuron cohesin knockout
    disrupts enhancer-promoter contacts, activity-dependent transcription, and
    motor learning.

## Computations over the supplied DE data

1. I read the manifest and confirmed the only requested target was `Smc3`.
2. I queried the focal training-count CSV for cohesin and chromosome-architecture
   comparators. The closest represented direct analogs were `Smc1a`, with
   24 DEGs at FDR<0.05, and `Stag2`, with 37. Nearby cohesin-cycle genes that
   were actually present, `Stag1`, `Pds5a`, and `Hdac8`, were all 0 at this
   FDR<0.05 endpoint. `Ctcf` was 270; broader chromatin regulators such as
   `Brd4`, `Yy1`, and `Smarcc2` were hundreds of DEGs and therefore useful
   counterexamples but not direct quantitative analogs.
3. I filtered the parquet to `group_name == "151 TH Prkcd Grin2c Glut"` for
   `Smc1a`, `Stag2`, `Stag1`, `Pds5a`, `Hdac8`, and `Ctcf` and checked both
   FDR-significant rows and matched sample sizes. `Smc1a` had 135 perturbed
   nuclei and 24 FDR<0.05 genes; `Stag2` had 193 perturbed nuclei and 37 genes;
   `Stag1`, `Pds5a`, and `Hdac8` had 126, 137, and 111 perturbed nuclei,
   respectively, with no FDR<0.05 genes. Thus the three nulls are not just
   tiny-n boundary cases relative to the active core-cohesin analogs.
4. I used the Distributed Agents `profile_compare` runtime on signed log2 fold-change
   vectors for the curated cohort
   `Smc1a, Stag2, Stag1, Pds5a, Hdac8, Ctcf, Yy1, Brd4, Smarcc2, Smarca4`.
   On the 17,259 measured genes in the focal group, `Smc1a` and `Stag2`
   shared 1 up-regulated and 8 down-regulated FDR<0.05 genes with no
   significant direction conflicts. The shared FDR<0.05 genes were `Inhbb`
   up and `Adamts2`, `Adamts19`, `Necab2`, `Ptprm`, `Sema5a`, `Smtn`,
   `Sox13`, and `Utp14b` down.
5. I also computed whole-profile Pearson and cosine similarity for `Smc1a` and
   `Stag2` against all 1,674 training targets. The nearest raw whole-vector
   neighbors were functionally mixed unrelated genes with Pearson correlations
   near 0.69, whereas `Smc1a` versus `Stag2` was 0.658 over all 17,259
   features. I therefore used all-gene correlation only as a weak sanity check;
   the decisive evidence was the shared significant cohesin module plus the
   known core-complex relationship.

## Target-specific reasoning

### Smc3

`Smc3` encodes one of the two SMC ATPase heads in the cohesin ring. SMC3 pairs
directly with SMC1A; RAD21 closes the ring, and STAG1/STAG2 are alternative
stromal antigen subunits. Because `Rad21`, `Nipbl`, `Mau2`, `Wapl`, `Pds5b`,
`Esco1`, and `Esco2` were not in the focal training-count CSV, the strongest
measured on-complex analogs were the core ring subunit `Smc1a` and the neuronal
SA2 subunit `Stag2`.

The direct focal evidence for a nonzero call is:

| training perturbation | focal `n_degs` | why it mattered |
| --- | ---: | --- |
| `Smc1a` | 24 | Obligate SMC3 partner in the cohesin ring; its 151 TH response was mostly down-regulation of neuronal adhesion, extracellular-matrix/guidance, and excitability genes. |
| `Stag2` | 37 | Direct cohesin SA2 subunit; it shared 9 FDR<0.05 genes with `Smc1a` in the same direction and the Distributed Agents corpus identified `Smc1a` as its strongest positive cohesin neighbor over the broader FDR<0.10 thalamic signature. |
| `Stag1` | 0 | Paralogous SA1 subunit. Its null focal response argues that all cohesin-associated targets are not interchangeable in this assay. |
| `Pds5a` | 0 | Cohesin residence/release regulator. The null focal response bounds the prediction downward for indirect cohesin-cycle perturbations, though it is less direct than SMC3 itself. |
| `Hdac8` | 0 | SMC3 deacetylase. Despite its biochemical connection to SMC3, its null response argues against using every cohesin regulator as a quantitative analog. |
| `Ctcf` | 270 | Cooperates with cohesin at loop anchors and Pcdh loci, but the same-experiment corpus found the Pcdh-heavy `Ctcf` output was not phenocopied by measured cohesin-machinery perturbations; it sets an upper counterexample rather than a target value. |

The external prior also favors a nonzero count. Core cohesin dosage is relevant
to transcriptional regulation outside mitosis: SMC1A/SMC3/RAD21/STAG form the
ring (Deardorff et al. 2012), cohesin and CTCF can wire promoters to distant
enhancers (Merkenschlager and Odom 2013; Seitan et al. 2013), CTCF/cohesin
looping is a known mechanism at neuronal protocadherin clusters (Guo et al.
2012), and depleting cohesin from postmitotic mouse granule neurons can alter
enhancer-promoter contacts and activity-dependent transcription (Yamada et al.
2019). The supplied screen nevertheless showed that acute P16 sparse CRISPR
does not turn every cohesin regulator into a broad transcriptomic responder;
the only clear measured cohesin-module counts at the requested FDR<0.05 cutoff
were the modest `Smc1a` and `Stag2` responses.

I therefore predicted `Smc3` as positive but modest, near the log-scale center
of `Smc1a` and `Stag2`: `exp((log(24 + 1) + log(37 + 1)) / 2) - 1 = 29.8`.
I rounded this to 30 DEGs rather than moving toward the 270-gene `Ctcf` state,
because CTCF had many additional Pcdh/endosomal genes that the core cohesin
perturbations did not recover, or to zero, because `Smc3` is the SMC1A partner
itself rather than an auxiliary loader, releaser, or deacetylase.

## Prediction

| target | predicted FDR<0.05 DEGs |
| --- | ---: |
| `Smc3` | 30 |

## Limits

This is an extrapolation from `Smc1a` and `Stag2`; `Smc3`, `Rad21`, `Nipbl`,
`Mau2`, `Wapl`, `Pds5b`, and the ESCO acetyltransferases were not measured as
training perturbations, so the prediction cannot be anchored to a complete
within-complex dose series. `Smc1a` and `Stag2` are X-linked whereas `Smc3` is
autosomal, and biallelic editing efficiency in sparse AAV CRISPR could change
the effective loss-of-function amplitude. The same-experiment corpus is a
curated interpretation of this dataset, not independent validation. Finally,
the endpoint is a survivor-conditioned single-nucleus mRNA count in one
thalamic glutamatergic group; it does not measure DNA looping, cohesin protein
loss, electrophysiology, absolute cell abundance, or perturbation severity
directly.
