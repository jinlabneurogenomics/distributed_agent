# Direct outcome-blind DEG-count prediction

## Target and endpoint

- Target: `Rrn3`
- Cell class: `151 TH Prkcd Grin2c Glut`
- Endpoint: `n_degs`, the count of measured genes with BH-adjusted Wilcoxon `p < 0.05`
- Declared holdout: one target in `Rrn3.csv`; `Rrn3` is absent from the 151 training count table and from the declared training profile Parquet.

## Evidence used

### Declared Rrn3 biology bundle

The canonical `Rrn3.json` bundle reports focal expression of `Rrn3` in the
matched non-target 151-class population:

- 18,688 of 23,679 non-target nuclei expressed `Rrn3`.
- `pct_cells_expressing = 78.9223`
- `mean_raw_umi = 1.8419`
- `mean_cp10k = 1.1466`

Its endpoint-blind biological adjudication supports target reach and short-window
realization: RRN3/TIF-IA is required for Pol I initiation and nascent pre-rRNA
synthesis, the operative RRN3-dependent initiation pool should be substantially
depleted by the P37-P44 harvest after a P16 disruptive edit, and adult mouse
postmitotic hippocampal Rrn3 deletion shows inhibited 47S pre-rRNA production by
about one month. The same bundle also cautions that mature 18S rRNA remained
largely buffered at that timepoint, so acute Rrn3 loss should not be scaled as a
full loss of installed ribosomes.

### 151-class training counts

The declared `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` has 1,674
training targets.

- Median `n_degs`: 0
- 1,205 / 1,674 targets: 0 DEGs
- 469 / 1,674 targets: at least 1 DEG
- 106 / 1,674 targets: at least 10 DEGs
- 59 / 1,674 targets: at least 50 DEGs
- 95th percentile: 18 DEGs

Counts for the closest measured growth, Pol-I-adjacent, and ribosome/RNA
biogenesis training perturbations were:

| target | 151-class `n_degs` |
| --- | ---: |
| `Taf1b` | 0 |
| `Myc` | 0 |
| `Mycn` | 0 |
| `Rptor` | 0 |
| `Mtor` | 2 |
| `Polr3b` | 8 |
| `Wdr26` | 13 |
| `Xrn1` | 20 |
| `Nop56` | 25 |
| `Tsc2` | 86 |

### Parquet profile checks on selected training analogs

I checked the raw 151-class rows from
`training_de_all_cell_groups.parquet` for the same measured candidates. The
Parquet counts exactly reproduced the count table:

- `Nop56`: 25 DEGs, including a significant negative self row and a compact
  negative SR-splicing/RNA-processing branch (`Rsrp1`, `Ddx17`, `Srsf5`,
  `Srsf11`, `Ddx5`, `Srsf6`, `Pabpn1`, `Clk4`).
- `Mtor`: 2 DEGs.
- `Polr3b`: 8 DEGs.
- `Wdr26`: 13 DEGs.
- `Xrn1`: 20 DEGs.
- `Tsc2`: 86 DEGs, dominated by sterol, lysosomal/endosomal, PI3K feedback, and
  mTORC1 metabolic genes.
- `Taf1b`, `Rptor`, `Myc`, and `Mycn`: 0 151-class DEGs.

I also compared ten of these observed candidates in a run-local 151-class
profile comparison. The review-node activity bins were four nodes with no
significant features, two with 1-9 significant features, three with 10-49, and
only `Tsc2` at 50 or more. This kept `Tsc2` from being treated as the center of
the Rrn3 estimate: it is a high-side mTORC1 gain-state comparator, whereas the
direct Pol I and ribosome-biogenesis perturbations land at 0-25 DEGs in this
exact endpoint.

### Same-experiment corpus for measured analogs

The packaged same-experiment Findings for the observed training perturbations
agree with the Parquet interpretation:

- `Taf1b` was transcriptionally flat across the juvenile neuronal surface, and
  canonical p53, unfolded-protein, and integrated-stress sentinels were not
  induced.
- `Myc` loss did not recover the expected growth/ribosome-biogenesis/translation
  program; `Mycn` likewise did not recover the canonical MYC proliferative
  growth program.
- `Rptor` had no downstream FDR < 0.10 genes in any recovered neuronal group,
  and `Mtor` itself produced only a very small mixed module.
- `Nop56` produced a narrow response, concentrated in this 151 thalamic class,
  and its main branch was RNA-processing/SR-splicing plus synaptic/vesicle genes,
  not a canonical p53/apoptosis, ISR, or autophagy program.
- `Tsc2` produced a larger, selective postmitotic mTORC1 metabolic response;
  mechanistically that is an mTORC1 activation/output state rather than a direct
  Pol I initiation-loss state.

## Synthesis

Rrn3 has strong biological reach in the focal thalamic population and should
lose its operative Pol I initiation stock by harvest, so I do not forecast a
strict null. The relevant endpoint is still survivor-conditioned polyadenylated
snRNA, not direct 47S pre-rRNA abundance. Mature rRNA persistence at about one
month and the flat `Taf1b`/`Myc`/`Rptor` training results argue against a broad
generic nucleolar-stress or growth-collapse signature.

`Nop56` is the best measured local positive anchor because it is a
ribosome-biogenesis factor with a real 151-class response, but even it reaches
only 25 DEGs and does not show the canonical p53/ISR/autophagy programs. I
therefore put Rrn3 below `Nop56` but well above the `Taf1b` and MYC nulls,
roughly at the 151-class training table's 95th percentile.

Predicted `n_degs`: **18**
