# Rb1 DEG-count prediction

## Question and resolved ambiguities

The requested held-out target set contains exactly one perturbation, `Rb1`. I
interpreted `n_degs` as the count of measured genes in `151 TH Prkcd Grin2c
Glut` with `pvals_adj < 0.05` for that target's CRISPR perturbation, using the
same Wilcoxon/BH endpoint as
`151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`. A value of `0` therefore
means that no assayed transcript is predicted to pass the exact FDR 0.05
threshold in this cell group; it is not a prediction of no edited alleles or no
biological role for pRB.

`151 TH Prkcd Grin2c Glut` is the thalamic glutamatergic focal group named in
the task, not a TH/dopaminergic population.

## Sources used

- Endpoint counts:
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`,
  1,674 non-held-out training perturbations.
- Differential-expression parquet:
  `[local file: training_de_all_cell_groups.parquet]`.
  I filtered this table to `group_name == "151 TH Prkcd Grin2c Glut"` and a
  hand-selected RB/E2F/MYC/p53 analog cohort, giving 189,849 rows: 11
  perturbations x 17,259 measured genes.
- Requested-target manifest:
  `[local file: 195_Rb1.csv]`.
- Same-experiment semantic layer: Distributed Agents corpus release
  `perturbai-july-260713-sourceguard-1773-v1`, queried with `target_context`
  for `E2f1`, `E2f5`, `Tfdp1`, `Tfdp2`, `Cdkn2a`, `Trp53`, `Myc`, `Mycn`,
  `Mnt`, and `Mga`, and with claim searches for E2F/cell-cycle/RB biology.
  This corpus is a curated layer over the same Perturb-seq experiment; I used
  the raw CSV/parquet for exact FDR 0.05 counts because some curated findings
  discuss FDR 0.10.
- Run-local profile analysis:
  `profile_rb1_e2f_cellcycle_compare.json` was generated from the parquet for
  `151 TH Prkcd Grin2c Glut` using `logfoldchanges` by measured gene and
  `pvals_adj < 0.05` as the significance call. I inspected the
  E2F/DP/CDKN2A/p53/MYC/MGA cohort for significant-feature counts and shared
  significant features.
- External literature:
  canonical RB/E2F and DREAM biology from Giacinti and Giordano 2006
  (doi:10.1038/sj.onc.1209615), Litovchick et al. 2007
  (doi:10.1016/j.molcel.2007.04.015), and Schade et al. 2019
  (doi:10.1038/s41388-019-0767-9); Rb/E2F neuronal apoptosis and cell-cycle
  re-entry from Liu and Greene 2001 (doi:10.1007/s004410100396), Hou et al.
  2000 (doi:10.1046/j.1471-4159.2000.0750091.x), Trinh et al. 2001
  (doi:10.1006/mcne.2000.0928), Futatsugi et al. 2012
  (doi:10.4161/cc.20009), and the direct acute postmitotic-neuron Rb
  inactivation study Andrusiak et al. 2012
  (doi:10.1523/JNEUROSCI.1912-12.2012).

## Computation over the training endpoint and parquet

The focal training counts are heavily zero-inflated: 1,205/1,674 training
targets are zero in `151 TH Prkcd Grin2c Glut`; the median is 0, the mean is
14.05, and the maximum is 2,677. The most biologically relevant RB-pathway
training targets in this cell group have the following exact FDR 0.05 counts:

| training target | focal `n_degs` | interpretation for `Rb1` |
|---|---:|---|
| `E2f1` | 0 | direct activating E2F; no canonical E2F/apoptotic output |
| `E2f5` | 0 | E2F/DREAM-side family member; no derepression signature |
| `Tfdp1` | 2 | DP partner; only `Cntrob` and `Dcaf15`, both up |
| `Tfdp2` | 0 | DP paralog; FDR-null |
| `Cdkn2a` | 0 | upstream inhibitor of CDK4/6/RB and p53-side `p19Arf` locus; FDR-null |
| `Trp53` | 0 | apoptosis/DNA-damage arm often coupled to aberrant E2F; FDR-null |
| `Myc` | 0 | proliferative growth program comparator; FDR-null |
| `Mycn` | 0 | MYC-family comparator in the focal thalamic group; FDR-null |
| `Mnt` | 0 | MAX-network repressor; FDR-null in the focal group |
| `Mlxip` | 0 | Mondo/MYC-adjacent comparator; FDR-null |
| `Mga` | 2 | PRC1.6/MAX-network target; only `Obscn` and `Stag3` in this group |

I then read the focal parquet rows for these 11 targets. The only genes passing
FDR 0.05 in this cohort were:

- `Mga`: `Obscn` up, `p_adj = 1.73e-8`; `Stag3` up, `p_adj = 4.83e-5`.
- `Tfdp1`: `Cntrob` up, `p_adj = 0.0114`; `Dcaf15` up, `p_adj = 0.0346`.

These were not broad E2F G1/S or apoptotic programs. A direct panel of
cell-cycle and apoptosis sentinels, including `Ccna2`, `Ccnb1`, `Ccnd1`,
`Ccne1`, `Ccne2`, `Cdc6`, `Cdc25a`, `Cdk1`, `Cdk2`, `Cdkn1a`, `Cdkn1b`,
`Mcm2`-`Mcm7`, `Pcna`, `Pola1`, `Rrm1`, `Rrm2`, `Apaf1`, `Bax`, and `Casp3`,
had `pvals_adj == 1.0` across the E2F/DP/MYC/MGA/p53/CDKN2A rows I queried in
the focal group. Matched perturbed nuclei for these exact analogs ranged from
82 for `Mga` to 346 for `Cdkn2a`, with 23,679 matched controls, so the direct
comparators had enough recovered cells to detect very large programs in this
high-yield class but still could miss a rare or strongly survivor-filtered
state.

The run-local profile comparison used whole log-fold-change vectors for the
same focal group. It reported no FDR-significant features for 9/11 analogs;
only `Tfdp1` and `Mga` had `1_to_9_significant_features`. No inspected pair
between `Tfdp1` and `E2f1`/`E2f5`/`Tfdp2`/`Cdkn2a`/`Trp53`/`Myc`/`Mycn`/`Mnt`
shared a positive significant gene, so the two-gene `Tfdp1` escape is not a
recurrent RB/E2F-family module.

## Target-specific reasoning

### Rb1

**Biology.** `Rb1` encodes the retinoblastoma pocket protein pRB, which binds
E2F transcription factors and represses G1/S transcription until cyclin/CDK
phosphorylation releases E2F activity; p107/`Rbl1` and p130/`Rbl2` provide
related pocket-protein repression, including p130/E2F4-containing DREAM
repression of cell-cycle genes in quiescence. That creates a clear external
prior that deleting `Rb1` could derepress E2F targets such as `Mcm`, `Pcna`,
`Cdc6`, cyclins, and nucleotide-synthesis genes. In neurons, the same axis is
often coupled to an abortive cell-cycle/apoptosis response: E2F1 overexpression
can kill cortical neurons (Hou et al. 2000), K+ withdrawal in cerebellar
granule neurons engages Rb/E2F regulation (Trinh et al. 2001), elevated Cdk5
can phosphorylate Rb and activate E2F in neurons (Futatsugi et al. 2012), and
acute Rb deletion in terminally differentiated mouse neurons was sufficient to
induce ectopic cell-cycle-protein expression and neuronal loss without a
classical `Apaf1`/`Puma` apoptotic gene program (Andrusiak et al. 2012).

**Same-experiment analogs.** The direct measured downstream arm was quiet in
this assay. `E2f1`, `E2f5`, and `Tfdp2` were all 0-DEG in the focal group;
`Tfdp1` had only two upregulated noncanonical genes; and the Distributed Agents corpus
summarized the same reports as showing no coordinated canonical G1/S,
replication, mitotic, or apoptotic nuclear transcriptomic program after single
E2F/DP perturbations in settled postnatal neurons. The upstream tumor-suppressor
comparator `Cdkn2a` was also 0 in the focal group and was curated as lacking
RB/E2F derepression, p53-effector suppression, or a coherent SASP-like module.
The p53 axis itself was flat: `Trp53` had 0 focal DEGs and the same-experiment
corpus records it as a 23-cell-group transcriptional null under basal P16 CRISPR
conditions, with no `Cdkn1a`, `Mdm2`, `Bax`, `Bbc3/PUMA`, `Pmaip1/NOXA`, or
`Gadd45a` movement. The growth/proliferation side was likewise quiet:
`Myc`, `Mycn`, `Mnt`, and `Mlxip` were 0 in the focal group, and the two-gene
`Mga` response was a PRC1.6/Stag3-like up-response, not an E2F-family
phenocopy.

**Prediction.** I predict that a single acute `Rb1` perturbation will be FDR-null
in this recovered thalamic neuronal population: `0` DEGs. The external Rb prior
prevents treating `Rb1` as an arbitrary housekeeping zero, but the requested
endpoint is a BH-corrected survivor-nucleus RNA count. In that endpoint, the
closest training perturbations around the pathway repeatedly show that
postnatal NeuN+ neurons did not expose the canonical Rb/E2F, replication, MYC,
or p53 modules as FDR 0.05 signatures. If `Rb1` CRISPR killed a subset of
strongly edited cells, that would also be largely invisible to this endpoint
except as a state among the recovered surviving nuclei.

## Limits of the reasoning

- The ideal paralogs `Rbl1`/`p107` and `Rbl2`/`p130`, the activators `E2f2` and
  `E2f3`, and direct CDK4/6 perturbations were not in the focal training
  endpoint, so the transfer rests on E2F/DP, `Cdkn2a`, MYC, and p53 relatives
  rather than on same-pocket-protein loss.
- `Rb1` is more proximal to E2F release than `E2f1` or `Tfdp1` loss. The
  measured E2F/DP perturbations test whether reducing an output arm is visible,
  not whether derepressing activator E2Fs through pRB loss can fire in every
  nucleus.
- Andrusiak et al. used acute genetic Rb inactivation in terminally
  differentiated neurons with more complete deletion than sparse AAV
  Perturb-seq CRISPR. A strong full knockout could have earlier or more lethal
  effects than the recovered P37-P44 mosaic nuclei show.
- DE is survivor-conditioned and single-endpoint. Selective loss of Rb-null
  neurons, electrophysiological changes, DNA-content changes, or low-level
  ectopic cell-cycle-protein expression without stable nuclear RNA shifts would
  not be counted by `n_degs`.
- The zero call is therefore a statement about crossing the FDR 0.05 RNA
  threshold in `151 TH Prkcd Grin2c Glut`, not a claim that pRB is dispensable
  for postmitotic neurons.
