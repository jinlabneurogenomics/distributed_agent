# Rrn3 direct n_degs forecast

## Target and endpoint

- Target: `Rrn3`, the only row in the declared holdout manifest.
- Focal population: `151 TH Prkcd Grin2c Glut`.
- Endpoint: number of measured genes with BH-adjusted Wilcoxon `pvals_adj < 0.05`.
- I did not use a held-out `Rrn3` expression signature or a held-out `Rrn3` DEG count.

## Biology bundle

The canonical `Rrn3` bundle argues that the perturbation should reach its proximal target in the assay window but that the captured protein-coding mRNA response can be buffered:

- Exact focal expression is broad but modest: 18,688 of 23,679 non-target nuclei expressed `Rrn3` in `151 TH Prkcd Grin2c Glut` and the mean was 1.84 raw UMI.
- RRN3/TIF-IA is the initiation factor for RNA polymerase I pre-rRNA transcription.
- Functional stock by harvest is likely substantially depleted: editing stops new RRN3 supply, the target protein is expected to turn over within the 21-28 day interval, and adult postmitotic hippocampal neuron deletion suppresses RRN3-dependent 47S pre-rRNA synthesis by about one month.
- The same adult-neuron evidence is not a reason to predict a huge acute snRNA-seq footprint: mature 18S rRNA remained detectable at one month and cell death was delayed, so pre-existing ribosomes can buffer downstream state in recovered nuclei.

## Training scalar surface

From the declared `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`:

- `Rrn3` is absent from the 1,674-row training table.
- The focal DEG-count distribution is sparse and skewed: 1,205 of 1,674 training perturbations have `n_degs = 0`; median 0; 75th percentile 1; 90th percentile 2; 95th percentile 18; 99th percentile 430.
- Proximal Pol I or nucleolar/rRNA-processing rows in the training table are low:
  - `Taf1b`: 0
  - `Rbm28`: 0
  - `Las1l`: 0
  - `Nop56`: 25
- Nearby RNA-production controls were also low in this cell class:
  - `Bdp1`: 8
  - `Polr3b`: 8
  - `Mtor`: 2
- Larger stress and proteostasis responses are possible in the same recovered thalamic population, but they are biologically indirect upper boundaries for `Rrn3`:
  - `Ufc1`: 572
  - `Uba5`: 2677
  - `Tnpo3`: 618
  - `Hnrnpu`: 733

Narrow Parquet checks in the same focal group confirmed that the key low rows were measured with recovered perturbed nuclei rather than missing: `Taf1b` had 0 significant rows with 106 matched perturbed nuclei, `Rbm28` had 0 with 143, `Las1l` had 0 with 171, `Bdp1` had 8 with 93, `Polr3b` had 8 with 72, and `Nop56` had 25 with 206.

## Same-experiment comparator interpretation

Packaged reports for the measured training comparators support the same low-count bracket:

- `Taf1b`, a core SL1/Pol I initiation factor, was flat across recovered juvenile neurons and did not induce captured p53, unfolded-protein, or integrated-stress sentinel mRNAs. This is the closest Pol I initiation counterweight to the `Rrn3` biology prior.
- `Rbm28` and `Las1l` were flat while `Nop56` produced a modest, cell-restricted nucleolar/rRNA-processing response, showing that the assay can see some ribosome-biogenesis perturbations but that the response is factor-specific.
- `Nop56` lacked a canonical nucleolar-stress, p53/apoptosis, ISR, or autophagy transcriptional program in surviving nuclei, despite a real narrow response in 151.
- `Polr3b` and `Bdp1` showed that direct RNA-production machinery can yield an 8-DEG focal response without a broad transcriptional shutdown.

## Numeric synthesis

The `Rrn3` prior is stronger than a generic flat ribosome-assembly target because focal expression is broad and adult-neuron deletion demonstrates proximal loss of pre-rRNA synthesis. That argues against copying the strict zeros for `Taf1b`, `Rbm28`, or `Las1l`. At the same time, the persistent mature rRNA pool, delayed degeneration, and the quiet same-experiment Pol I/nucleolar boundaries argue against projecting the hundreds-to-thousands DEG UFMylation, spliceosome, or proteasome rows.

I therefore placed `Rrn3` in the low, nonzero RNA-production range bracketed by `Polr3b`/`Bdp1` at 8 and `Nop56` at 25, with the closest point at the repeated 8-DEG value because the most proximal Pol I comparator `Taf1b` was 0. The final direct forecast is:

`predicted_n_degs = 8`
