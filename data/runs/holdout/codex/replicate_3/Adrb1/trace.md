target: Adrb1
cell_group: 151 TH Prkcd Grin2c Glut

Prediction: 0 DEGs.

Evidence used:

- The task target is Adrb1, from the one-row declared holdout manifest.
- The endpoint is the focal-class count of measured genes with Wilcoxon
  BH-adjusted p < 0.05.
- The Adrb1 biology bundle supports a realized loss-of-function perturbation
  by harvest rather than durable pre-edit stock: Adrb1 encodes a renewable
  beta-1 adrenergic GPCR, a heterologous total-receptor pulse-chase measured an
  approximately 13 hour half-life, and a postnatal mouse mPFC conditional
  deletion produced a neural phenotype four weeks after AAV-Cre.
- Exact target reach in the assayed focal population was present but modest:
  in non-target 151 TH Prkcd Grin2c Glut nuclei, Adrb1 had mean 0.328 CP10K,
  mean 0.539 raw UMI, and 9,071 of 23,679 cells expressing it (38.31%).
- The 151 TH Prkcd Grin2c Glut training count table is strongly zero-heavy:
  1,205 of 1,674 training perturbations had n_degs = 0; the median was 0, the
  90th percentile was 2, and only 43 training perturbations had at least 100
  DEGs.
- Close receptor training perturbations in this exact class were silent:
  Adrb2 = 0, Adrb3 = 0, Adra1a = 0, Adra2a = 0, Adra2b = 0, and Drd2/Drd4/Drd5
  were all 0. Extending the same table to serotonin and muscarinic aminergic
  GPCRs that were present also gave 0 for Htr1a, Htr1b, Htr1f, Htr2a, Htr2b,
  Htr2c, Htr4, Htr6, Htr7, Chrm2, and Chrm3.
- Focal Parquet rows for proximal beta-adrenergic/cAMP effectors did not show a
  recurrent downstream footprint: Gnas and Adcy1/3/5 were all 0; Pde1c, Pde4b,
  Pde4d, Pde10a, and Rgs6 were 0 in the count table; Prkaca and Prkar1a each
  had one significant gene in the Parquet but it was the self-target transcript
  only. Creb1 and Crebbp had 10 and 8 DEGs respectively, but those are nuclear
  transcriptional regulators rather than close cell-surface receptor analogs.

Reasoning:

Adrb1 loss should clear functional receptor during the P16-to-P37/P44 interval
if edited, so I did not treat the perturbation as unrealized. The expected
transcriptional footprint is nevertheless small: the receptor is a modulatory
cell-surface input, its Adrb1 RNA reach in the aggregate thalamic class covers
only 38% of non-target nuclei at low UMI depth, and every measured catecholamine
or aminergic GPCR comparator in the focal training table had 0 DEGs. The
nearest cAMP-pathway rows also argue against a broad state change, with
nonzero counts appearing only for self-transcripts of PKA genes or for more
global transcriptional cofactors.

The best point forecast is therefore the modal no-call state, 0 BH-significant
genes. I did not add an expected self-target DEG for Adrb1 because target mRNA
loss is neither guaranteed nor coupled to downstream response in this screen,
and the biology bundle provides no reason to expect Adrb1 transcript depletion
to be the lone significant gene.
