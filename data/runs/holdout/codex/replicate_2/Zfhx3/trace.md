# Zfhx3 direct DEG-count prediction

## Declared target and endpoint

- Target manifest: one row, `Zfhx3`.
- Cell group: `151 TH Prkcd Grin2c Glut`.
- Endpoint: `n_degs`, the number of measured genes with Wilcoxon BH-adjusted `pvals_adj < 0.05`.
- The declared training count table contains 1,674 target rows and no `Zfhx3` row.
- The declared DE parquet contains the available training profiles and omits the held-out Zfhx3 outcome.

## Biology used

The run-local Zfhx3 expected-impact bundle supports target engagement but not a large thalamic response by itself:

- Exact focal reach in non-target nuclei for `151 TH Prkcd Grin2c Glut`: `Zfhx3` was detected in 16,679 of 23,679 nuclei, `70.4379%`, with mean log1p CP10K `0.5396` and pseudobulk CPM `88.8716`.
- ZFHX3 is a large nuclear AT-motif transcription factor.
- Existing ZFHX3 protein should turn over within the 21-28 day P16-to-harvest window: adult inducible neural deletion removed detectable SCN ZFHX3 protein after a five-day induction plus seven-day recovery.
- Adult neural Zfhx3 loss produces a circadian phenotype despite Zfhx2/Zfhx4 paralogs, so a postmitotic single-gene effect is biologically reachable.
- The strongest functional evidence is adult hypothalamic SCN, not the assayed juvenile thalamic glutamatergic population, so it is cross-context support rather than a direct same-cell estimate.

The same-experiment corpus had no Findings, Claims, or explicit comparator references for `Zfhx3`; the forecast therefore used direct measurement from the declared count table and DE parquet rather than a packaged Zfhx3 report analogue.

## Training measurements used

In the declared `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`:

- overall distribution: `n=1674`, median `0`, 75th percentile `1`, 90th percentile `2`, 95th percentile `18`, mean `14.054`;
- 469 of 1,674 targets had any DEG; only 43 had at least 100 DEGs;
- a log1p-space background center over all training targets was `expm1(mean(log1p(n_degs))) = 0.595`;
- close sequence-specific or developmental TF rows were mostly silent: `Bcl11a=0`, `Bcl11b=0`, `Foxp2=0`, `Lhx3=0`, `Lhx4=0`, `Nfia=0`, `Tshz3=0`, `Zfp292=0`, `Mef2c=1`, `Sox2=2`, `Mef2a=4`;
- some generic or thalamus-coupled transcriptional regulators were much larger: `Tcf7l2=106`, `Rora=278`, `Cic=576`, `Yy1=720`, `Zbtb7a=841`.

The DE parquet confirmed the count-table values in the focal cell group for those profiles and showed that the large TF/chromatin responses were not a single tight module to transfer wholesale to Zfhx3: for example, Rora and Tcf7l2 shared only 19 FDR-significant measured genes, while the low sequence-specific TFs had almost no significant overlap with the high-response Cic/Yy1/Zbtb7a programs.

## Synthesis

Zfhx3 is broadly detectable enough in the focal nuclei, and its functional stock is likely depleted by harvest, so I did not use the training-table median of zero as the entire forecast. The better biological class is still a sequence-specific neuronal transcription factor with a documented postnatal phenotype in SCN rather than a core chromatin complex, spliceosome, proteasome, or housekeeping transcriptional regulator. The closer measured TFs in this thalamic class are overwhelmingly 0-4 DEGs, and the exceptional 100-800 DEG regulators carry target-specific programs that are not justified as Zfhx3 magnitude analogues.

I therefore forecast a small, detectable but sparse response:

```text
predicted_n_degs = 2
```
