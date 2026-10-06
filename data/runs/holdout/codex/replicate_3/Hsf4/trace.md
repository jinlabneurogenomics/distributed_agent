# Hsf4 151 TH DEG-count forecast

## Declared target and endpoint

- Target manifest: `Hsf4`.
- Focal class: `151 TH Prkcd Grin2c Glut`.
- Endpoint: number of measured genes with BH-adjusted Wilcoxon `pvals_adj < 0.05` in the held-out perturbation.
- Prediction scale: one non-negative integer for the held-out `Hsf4` count; no target `Hsf4` expression signature or target count was used.

## Biology used

The Hsf4 bundle supports target engagement as plausible but gives only weak support for a large juvenile-thalamic transcriptional consequence.

- Exact focal-population reach was present but partial: in non-target 151-TH cells, `Hsf4` had mean raw UMI `0.3824`, mean CP10K `0.2371`, pseudobulk CPM `23.97`, and was detected in `6879 / 23679 = 29.05%` of nuclei.
- HSF4 is a dynamic heat-shock-element DNA-binding transcription factor. Its pre-edit functional stock is expected to be substantially reduced over the P16 to P37-P44 interval, because the 21-28 day interval is longer than the 3-13 day lifetime interval covering most measured adult mouse cortex proteins and HSF4 has no installed structural stock.
- The clearest isolated-loss phenotype was developmental lens differentiation, not postmitotic thalamic neurons.
- The neural evidence was only an aged, sensitized `Hsf1`/`Hsf4` compound-mutant interaction. It did not establish an isolated Hsf4 requirement in juvenile thalamus.
- Hsf1/Hsf2 redundancy was unresolved: they are related heat-shock transcription factors, but no source established same-context compensation for Hsf4 loss.

Those facts move the forecast above a pure null for a nonexpressed or stable structural target, but keep it below the measured `Hsf1` transcription-factor response.

## Training counts used

The declared 151-TH training count table was extremely sparse:

- 1,674 perturbations in the training table.
- 1,205 had `n_degs = 0` (`71.98%`).
- Median `n_degs = 0`; 75th percentile `= 1`; 90th percentile `= 2`.
- Only 106 perturbations reached 10 or more DEGs and only 43 reached 100 or more.

For heat-shock and chaperone/proteostasis targets available in the declared training table:

| perturbation | 151-TH `n_degs` | interpretation |
| --- | ---: | --- |
| `Hsf1` | 6 | nearest mechanism-level heat-shock-factor comparator; small HSP90/HSP110 module |
| `Hspa8` | 9 | small cytosolic Hsp70 counterinduction program |
| `Hspa5` | 5 | small ER folding/ERAD response at `pvals_adj < 0.05` |
| `Hsp90ab1` | 1 | only the self transcript was significant |
| `Dnajb4` | 0 | DnaJ-family chaperone perturbation, flat in this class |
| `Dnajb6` | 0 | DnaJ-family chaperone perturbation, flat in this class |
| `Dnajc13` | 1 | only the self transcript was significant |
| `Dnajc19` | 0 | flat |
| `Dnajc5` | 1 | only the self transcript was significant |

Direct Parquet inspection of the `Hsf1`, `Hspa5`, `Hspa8`, and `Hsp90ab1` 151-TH rows confirmed that the low counts came from real small signatures, not from misreading the count table:

- `Hsf1` had six significant genes: `Hsph1`, `Hsp90aa1`, `Rsrp1`, `Hsp90ab1`, `Mat2a`, and `Ahsa2`, all down.
- `Hspa8` had nine significant genes, including up-regulated `Dnaja1`, `Hspa4l`, `Syt4`, `Hsp90aa1`, and `Cct6a`.
- `Hspa5` had five significant genes at `pvals_adj < 0.05`, including up-regulated `Hsp90b1`, `Nfe2l1`, `Pdia4`, and `Derl3`.
- `Hsp90ab1` had one significant gene, `Hsp90ab1` itself.

## Same-experiment corpus checks

Packaged Findings from the same experiment supported using those rows as low-response local bounds:

- `Hsf1` loss was interpreted as a small, cell-type-restricted depression of an HSP90/HSP110 co-chaperone module rather than a broad stress program.
- `Hspa8`, `Hspa5`, and `Hsp90ab1` were explicitly not interchangeable: cytosolic Hsp70, ER BiP, HSP90 beta, and HSF1 losses separated into different sparse outcomes rather than one generic chaperone-loss state.
- Single heat-shock/chaperone/DnaJ nodes were described as mostly buffered in basal juvenile neurons, with core proteasome subunits providing a broad-response contrast that is not mechanistically transferable to Hsf4.

I also ran the local gene-analog nominator against the exact 151-TH training universe. It found no `Hsf4` candidate in any high-specificity tier: zero exact-complex/paralog, reciprocal corpus-comparator, narrow-module, or direct-interaction nominees. All 1,008 available nominees were broad functional fallbacks dominated by eye-development and generic DNA-binding transcription-factor annotations, so I did not use them as quantitative donors.

## Synthesis

The count-table prior favors zero, and `Hsf4` lacks evidence for a broad HSF1-like constitutive program in juvenile thalamic neurons. `Hsf1 = 6` is therefore an upper local heat-shock-factor bound rather than a direct transfer estimate. Partial `Hsf4` expression reach in 151-TH nuclei, plausible depletion of a diffusible transcription factor by harvest, and the small but detectable `Hsf1`/`Hspa8`/`Hspa5` training signatures keep the mean forecast slightly above a strict null.

I chose the final point as a one-gene tail:

```text
predicted_n_degs = 1
```
