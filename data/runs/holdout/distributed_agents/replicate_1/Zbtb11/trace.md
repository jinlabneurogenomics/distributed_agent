# DEG-count prediction trace

## Question and resolved ambiguities

The requested endpoint is `n_degs` for held-out `Zbtb11` loss of function in
`151 TH Prkcd Grin2c Glut` thalamic glutamatergic neurons: the number of
measured genes with Wilcoxon Benjamini-Hochberg adjusted `pvals_adj < 0.05`.
`Zbtb11` was absent from both the training DE parquet and the focal
training-count CSV, so there is no directly observed Zbtb11 signature in the
declared Perturb-seq input.

I treated the count as an assay- and power-dependent recovered-cell
transcriptional footprint, not as a direct estimate of biological importance,
viability, or edit efficiency. I also treated broad ZBTB-family membership as a
weak prior only: ZBTB11 has a specific mitochondrial transcription role, so
unrelated ZBTB-domain repressors are counterexamples, not close quantitative
analogs.

## Sources used

- Declared focal endpoint table:
  `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
  It contained 1,674 visible training perturbations; 1,205 of them had zero
  DEGs in the focal class.
- Declared DE parquet:
  `training differential-expression dataset`.
  I queried rows with `group_name == "151 TH Prkcd Grin2c Glut"` for ZBTB
  family targets, mitochondrial/complex-I targets, and nuclear transcription
  regulators relevant to ZBTB11 biology.
- Internal same-experiment corpus: `perturbai-july-260713-sourceguard-1773-v1`.
  The run-local coverage summary and a bounded corpus story count had no
  Zbtb11, Zbtb7a, or Nrf1 Finding records, and a BioKG expansion for a Zbtb11
  target node returned no Finding-comparator rows. I therefore used the corpus
  only to check that it did not contain a packaged Zbtb11 same-experiment
  interpretation.
- External literature:
  - Fattahi et al. 2018, Human Molecular Genetics,
    doi:10.1093/hmg/ddy220, PMID:29893856.
  - Wilson et al. 2020, Nature Communications,
    doi:10.1038/s41467-020-19205-x, PMID:33122634.
  - Cao et al. 2023, Blood Advances,
    doi:10.1182/bloodadvances.2022009580, PMID:37567157.
  - Satou-Kobayashi et al. 2024, PLoS ONE,
    doi:10.1371/journal.pone.0293852, PMID:39083515.

## Computation over the training data

I first summarized the focal training-count CSV. The distribution is extremely
zero-heavy: median `n_degs = 0`, 75th percentile `= 1`, 90th percentile `= 2`,
95th percentile `= 18`, and only a small tail of regulators exceeded hundreds
of DEGs. I then queried the full DE parquet for focal-class rows from
biologically plausible Zbtb11 analogs to determine whether nonzero counts were
driven by coherent downstream expression changes or only by the perturbed
gene itself.

The biologically relevant focal-class observations were:

| Comparison class | Training perturbations and `n_degs` | Pattern in the focal DE rows |
| --- | --- | --- |
| ZBTB transcription-factor family | `Zbtb7a` 841; `Zbtb18` 5; `Zbtb38` 1; `Zbtb16` 0; `Zbtb10` 0; `Zbtb20` 0; `Zbtb21` 0 | The family did not have a shared small or large response. `Zbtb7a` was a large outlier, while four measured ZBTB knockouts were completely quiet and `Zbtb18`/`Zbtb38` were near the detection boundary. |
| Mitochondrial complex-I genes downstream of the ZBTB11/GABP program | 23 `Nduf*` targets: 14 zeros and 9 with exactly 1 DEG | The significant hits were usually the targeted subunit itself, e.g. `Ndufa10`, `Ndufa6`, `Ndufa4`, `Ndufb8`, `Ndufb11`, `Ndufb10`, `Ndufs8`, `Ndufs2`, `Ndufc2`, and `Ndufb9`; this argues that reducing one complex-I component rarely generated a broad survivor transcriptome in this cell group. |
| Other OXPHOS/mitochondrial executors | `Opa1` 37; `Cox5a` 1; `Uqcrc2` 1; `Uqcrq` 1; `Sdha` 1; `Cox11` 0; `Cox8a` 0; `Cox7b` 0; `Cox6a1` 0; `Cox4i1` 0; `Uqcrb` 0; `Lars2` 0; `Uqcrfs1` 0; `Uqcrh` 0 | `Opa1` showed a modest stress-like footprint including `Cdkn1a`, `Chac1`, `Asns`, `Ddit3`, and `mt-Co2`. The respiratory-chain genes themselves were otherwise null or single-hit targets. |
| NRF/mitochondrial transcriptional regulation | `Nrf1` 138; `Nfe2l1` 0; `Nfe2l2` 0; `Ppargc1a` 0; `Creb1` 10 | GABPA/GABPB1/GABPB2, the most direct ZBTB11 partners reported by Wilson et al., were not present in the training set. `Nrf1` is an imperfect analog: it is a mitochondrial and proteasome transcription regulator, but not the same obligate ZBTB11/GABP factor. |
| Nucleolar/RNA-processing analogs | `Nop56` 25; `Ddx3x` 8; `Las1l` 0; `Ddx39b` 0; `Wdr37` 0; `Wdr48` 0 | Fattahi et al. linked ZBTB11 localization to the nucleolus and rRNA-related pathways, but the closest measured ribosome/RNA-processing perturbations in this set were at most modest in this cell group. |
| Reported context-specific interactors or regulators | `Set` 0; `Otx2` 0 | SET-ZBTB11 is a lung-cancer metastasis axis and Otx2-Zbtb11 was shown in Xenopus anterior neuroectoderm, so these were negative contextual checks rather than direct neuronal analogs. |

## Target-specific rationale

### Zbtb11

`Zbtb11` encodes a zinc-finger/BTB transcription factor. Human biallelic
missense variants in its C2H2 zinc fingers cause intellectual disability and
mislocalize ZBTB11 away from the nucleolus; ENCODE ChIP-seq pathway analysis
in that study linked the bound genes to rRNA synthesis and ribosomal assembly
(Fattahi et al. 2018). Wilson et al. later found that Zbtb11 cooperates with
NRF-2/GABP at promoters and activates a subset of nuclear genes required for
complex-I and mitoribosome biogenesis; complete genetic inactivation in
cycling cultured cells caused severe complex-I assembly defects, impaired
respiration, mitochondrial depolarization, proliferation arrest, and cell
death. Cao et al. showed an essential, cell-intrinsic Zbtb11 requirement in
fetal hematopoietic stem/progenitor cells, again with oxidative
phosphorylation down-regulation. These external data make `Zbtb11` a real
regulatory gene, not an inert target.

The transfer chain to this exact readout is weak, however. The strongest
external phenotypes come from proliferating embryonic or hematopoietic cells,
whereas the experiment perturbed postmitotic neurons sparsely at P16 and read
out surviving NeuN+ nuclei 3-4 weeks later. A full knockout of a mitochondrial
biogenesis factor could reduce fitness or respiration without leaving many
recoverable nuclei with a large Wilcoxon DEG burden. In the declared training
data, individual perturbations of complex-I subunits downstream of the
ZBTB11/GABP program were almost all `0` or `1` DEG, and the positive `Nduf*`
cases were largely self-target calls. Other respiratory-chain perturbations
were similarly quiet. That argues against propagating Wilson et al.'s
complex-I mechanism into a broad focal-class transcriptome.

The transcription-factor analogs also did not support a large count.
`Zbtb7a`, `Yy1`, `Sin3a`, `Cic`, and `Thap11` demonstrate that some chromatin
or transcriptional regulators can produce hundreds of DEGs in this cell group,
but they are not obligate partners of ZBTB11 and their signatures are not
ZBTB11's NRF-2/GABP mitochondrial program. Among other ZBTB genes the observed
counts were `Zbtb18 = 5`, `Zbtb38 = 1`, and four zeros; that is a better
family-level estimate for an unsupported Zbtb11 prediction than the `Zbtb7a`
outlier. Direct reported interactors from non-neuronal or embryonic contexts
also failed to transfer: `Set` and `Otx2` both had zero DEGs in the focal
training table.

I therefore predicted no genes passing FDR 0.05 for `Zbtb11`. A small count
between one and about ten would also be biologically plausible, especially if
partial Zbtb11 editing perturbs mitoribosome targets in these thalamic neurons,
but the central mass of the focal training distribution and the measured
complex-I analogs both favor the zero side of that boundary.

## Final point prediction

| target_name | predicted_n_degs |
| --- | ---: |
| Zbtb11 | 0 |

## Limits

The main limitation is that no GABPA/GABPB perturbation was present in the
training endpoint table, so the most mechanistically direct ZBTB11 partner
could not be used as a within-dataset analog. The relevant ZBTB11 literature
used human cell lines, hematopoietic fetal mouse cells, or Xenopus
neuroectoderm; none measured acute mosaic loss in postnatal thalamic
glutamatergic neurons. The Perturb-seq dataset and its July 260713 corpus are
two representations of one experiment rather than independent replication, and
the corpus had no packaged Zbtb11 evidence. This prediction is therefore a
low-count extrapolation from downstream complex-I and RNA-processing
perturbations, not a direct measurement of `Zbtb11`.
