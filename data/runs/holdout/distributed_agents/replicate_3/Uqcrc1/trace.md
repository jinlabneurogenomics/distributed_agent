# Uqcrc1 prediction trace

## Question interpreted

The held-out manifest for this run contains one requested perturbation:
`Uqcrc1`. I interpreted the requested endpoint as the literal focal-cell count in
the training CSV: the number of measured genes, including the target transcript
itself when present, with `pvals_adj < 0.05` in `151 TH Prkcd Grin2c Glut`.
`Uqcrc1` is absent as a `gene_target` from the supplied differential-expression
parquet and absent from the focal training count table, so the estimate must be
transferred from non-held-out perturbations.

## Sources used

- `training_de_all_cell_groups.parquet`, filtered to
  `group_name == "151 TH Prkcd Grin2c Glut"`, for signed Wilcoxon scores,
  log2 fold changes, adjusted p-values, and perturbed/control nucleus counts.
- `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`, containing exact
  observed `n_degs` for the 1,674 available training perturbations in the focal
  cell group.
- The requested-target manifest `257_Uqcrc1.csv`.
- The Distributed Agents same-experiment semantic corpus
  `perturbai-july-260713-sourceguard-1773-v1`. `Uqcrc1` itself was not present
  in that corpus, so I used target cards and claims for observed complex-III and
  mitochondrial comparators: `Uqcrc2`, `Uqcrfs1`, `Uqcrb`, `Uqcrh`, `Uqcrq`,
  `Cyc1`, `Ndufs2`, and `Opa1`.
- The Distributed Agents runtime profile-comparison tool, run on the focal group with
  `scores` as the signed profile value and `pvals_adj < 0.05` as the
  significance flag.
- The local Distributed Agents gene-annotation skill over curated GO, Reactome, KEGG,
  MSigDB, and CORUM memberships in the PerturbAI closed gene universe.
- External mechanism anchors: MitoCarta3.0 places UQCRC1/UQCRC2/UQCRFS1/CYC1
  in the mitochondrial complex III/OXPHOS system (Rath et al., 2021,
  DOI 10.1093/nar/gkaa1011, PMID 33174596), and the cytochrome bc1 structural
  work establishes core 1/core 2, Rieske, cytochrome c1, and small UQCR
  subunits as members of the 11-subunit mitochondrial complex III (Iwata et al.,
  1998, PMID 9651245). Reactome/GO/CORUM memberships were taken from the local
  Distributed Agents gene-annotation store.

## Computational checks

1. I loaded the focal training count table. It contains 1,674 non-held-out
   perturbations. Counts were extremely sparse overall: median 0, third
   quartile 1, 90th percentile 2, 95th percentile 18, and maximum 2,677 DEGs.

2. I filtered the parquet to the focal group and to complex-III or adjacent
   OXPHOS perturbations, then counted rows with `pvals_adj < 0.05` and inspected
   exact significant genes and canonical mitochondrial-stress sentinels.

3. For the directly represented GO respiratory-chain complex III targets,
   focal `n_degs` values were:

   | Perturbation | focal `n_degs` | focal FDR 0.05 gene(s) |
   | --- | ---: | --- |
   | `Cyc1` | 1 | `Cyc1` self transcript |
   | `Uqcrb` | 0 | none |
   | `Uqcrc2` | 1 | `Uqcrc2` self transcript |
   | `Uqcrfs1` | 0 | none; the self transcript was down but not FDR 0.05 (`p_adj=0.199`) |
   | `Uqcrh` | 0 | none |
   | `Uqcrq` | 1 | private `Gpr180` decrease, not the self transcript |

   The Reactome complex III assembly set additionally nominates `Ttc19` as an
   assembly/turnover comparator; in the focal group it also had exactly one DEG,
   its own self transcript.

4. Canonical ISR/mitochondrial-stress genes did not pass FDR for the observed
   complex-III targets in the focal group. For `Uqcrc2`, `Uqcrfs1`, `Uqcrb`,
   `Uqcrh`, and `Uqcrq`, sentinel rows such as `Asns`, `Ddit3`, `Chac1`,
   `Slc7a5`, and `Mthfd2` all had `pvals_adj = 1.0`.

5. I computed whole-focal signed-score similarities among the complex-III
   comparators and `Opa1`. All relevant similarities were noise-scale. In the
   runtime profile projection over 17,259 shared measured genes, `Uqcrc2` had
   Pearson/cosine 0.008/0.007 to `Cyc1`, -0.012/-0.009 to `Uqcrfs1`,
   0.011/0.009 to `Uqcrb`, -0.012/-0.018 to `Uqcrh`, -0.010/-0.013 to `Uqcrq`,
   and -0.033/-0.038 to `Opa1`. None of the complex-III pairs shared
   same-direction FDR 0.05 features.

6. I used `Opa1` as a counterexample for detectability rather than as a direct
   mechanistic analog. `Opa1` had 37 focal DEGs, including `Asns`, `Mars1`,
   `Chac1`, `Ddit3`, `Mthfd2`, `Slc7a5`, and other ATF4/ISR-like amino-acid and
   one-carbon genes. The absence of those genes from `Uqcr*` perturbations
   therefore reflects buffering or thresholding of structural respiratory-chain
   subunits in this assay, not a universal inability of the snRNA-seq/Wilcoxon
   pipeline to see mitochondrial stress.

## Target-specific rationale

### `Uqcrc1`

`Uqcrc1` encodes a core protein of mitochondrial complex III. The curated
closed-universe annotations place `Uqcrc1`, `Uqcrc2`, `Uqcrfs1`, `Uqcrq`, and
`Cyc1` together in GO respiratory-chain complex III, KEGG oxidative
phosphorylation, Reactome respiratory electron transport, Reactome complex III
assembly, and CORUM cytochrome bc1 complex sets. Among represented targets,
`Uqcrc2` is the best direct analog because it is the other matrix-facing core
subunit of the same complex; `Cyc1`, `Uqcrfs1`, `Uqcrb`, `Uqcrh`, and `Uqcrq`
are same-enzyme structural comparators, and `Ttc19` is a turnover/assembly
comparator.

The key within-dataset evidence points to a singleton-scale response:

- The focal structural complex-III counts were 1, 0, 1, 0, 0, and 1 for
  `Cyc1`, `Uqcrb`, `Uqcrc2`, `Uqcrfs1`, `Uqcrh`, and `Uqcrq`.
- The one `Uqcrc2` DEG in the focal group was `Uqcrc2` itself, with log2FC
  -0.576 and `p_adj=0.002997`; no downstream complex-III, ISR, UPRmt, redox, or
  mitophagy feature accompanied it.
- `Cyc1` and `Ttc19` likewise reached FDR only on their own transcripts in this
  focal group.
- `Uqcrq` was a useful counterexample against a generic complex-III downstream
  count: its single focal hit was `Gpr180`, and `Uqcrc2`, `Uqcrfs1`, `Uqcrb`,
  `Uqcrh`, and `Cyc1` did not reproduce that event.
- The Distributed Agents corpus summarized the same represented complex-III neighborhood
  with the high-confidence claim that structural complex-III perturbations were
  largely transcriptionally buffered and failed to induce a shared complex-III
  depletion RNA signature. The Uqcrb, Uqcrc2, Uqcrfs1, Uqcrh, Uqcrq, and Cyc1
  Findings all stress that singleton events were target-private rather than a
  recurring complex-level transcriptome.

I therefore did not extrapolate the broad `Opa1` mitochondrial-stress state to
`Uqcrc1`; `Opa1` is an internal positive control showing that the assay could
detect ATF4/ISR-like mitochondrial stress when a perturbation crossed that
threshold. I also did not give much quantitative weight to broader complex-I or
complex-IV subunits except as a boundary, because they are less direct
biochemically and in this dataset mostly reinforced the same sparse
respiratory-chain pattern with 0 or 1 focal DEGs.

The predicted count is **1**. The one-gene call is driven mostly by the
within-dataset `Uqcrc2`/`Cyc1`/`Ttc19` self-transcript observations plus the
fact that `Uqcrc1` is measured in the focal parquet; the absence of a predicted
second or larger block is driven by the observed lack of shared downstream
complex-III or ISR features.

## Limits and uncertainty

- `Uqcrc1` itself was held out from both supplied expression signatures and the
  same-experiment Distributed Agents target corpus, so there is no direct measured
  `Uqcrc1` perturbation signature in any evidence I used.
- A count of zero is plausible: several same-complex structural perturbations
  had no focal FDR 0.05 genes, and self-transcript detection is guide-, allele-,
  expression-, and nucleus-count-dependent.
- Conversely, a count above one is possible if the hidden `Uqcrc1` guides
  happened to create an idiosyncratic private event like `Uqcrq -> Gpr180`, but
  the training signatures did not support a recurrent downstream complex-III
  state to copy.
- All comparisons are transcriptional and survivor-conditioned. They do not
  measure complex-III protein, bc1 activity, oxygen consumption, ROS, cell loss,
  or DNA indel fractions; the prediction is only for the assay-specific
  FDR-count endpoint in recovered `151 TH Prkcd Grin2c Glut` nuclei.
- External knowledge establishes same-complex membership and respiratory-chain
  function, but the point estimate is dominated by the within-dataset finding
  that acute sparse postnatal CRISPR of structural OXPHOS subunits was usually
  buffered at the nuclear RNA level.
