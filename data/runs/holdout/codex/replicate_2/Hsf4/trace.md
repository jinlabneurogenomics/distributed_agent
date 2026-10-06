# Hsf4 n_degs forecast

## Declared target

- Held-out target: `Hsf4`
- Requested population: `151 TH Prkcd Grin2c Glut`
- Endpoint: count of measured genes with Wilcoxon BH-adjusted `p < 0.05`

## Evidence used

- The prediction-safe `Hsf4` biology bundle reports measurable target reach in the exact focal population: 6,879 of 23,679 matched non-target nuclei expressed `Hsf4`, with 29.051% expressing cells, mean raw UMI 0.38245, mean CP10K 0.23713, mean log1p CP10K 0.16631, and pseudobulk CPM 23.969.
- Its functional-stock card calls HSF4 a dynamic, diffusible, heat-shock-element transcription factor whose pre-edit protein stock is likely substantially depleted over the P16 to P37-P44 CRISPR window. That makes the perturbation reachable by harvest, not just a developmental installed-structure loss.
- The same bundle leaves juvenile thalamic demand unresolved: the clean isolated-loss phenotype is lens differentiation and cataract, the neural evidence is an aged `Hsf1`/`Hsf4` compound-mutant interaction, and possible buffering by related `Hsf1`/`Hsf2` has not been tested in the assayed thalamic neurons.
- The declared `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` has 1,674 held-in targets and is extremely sparse:
  - 1,205 / 1,674 targets have `n_degs = 0`
  - median = 0
  - 75th percentile = 1
  - 90th percentile = 2
  - 95th percentile = 18
- The closest measured HSF/proteostasis perturbations in this population were small:
  - `Hsf1`: 6
  - `Hspa8`: 9
  - `Hspa5`: 5
  - `Hsp90ab1`: 1
  - `Dnajc5`: 1
  - `Dnajc13`: 1
  - `Dnajb4`, `Dnajb6`, `Dnajc19`: 0
- Direct Parquet inspection of `151 TH Prkcd Grin2c Glut` showed that `Hsf1` has a small all-negative chaperone output: `Hsph1`, `Hsp90aa1`, `Rsrp1`, `Hsp90ab1`, `Mat2a`, and `Ahsa2`. In contrast, `Hsp90ab1`, `Dnajc5`, and `Dnajc13` were self-transcript-only one-DEG perturbations in this group; `Hspa5` and `Hspa8` had only small stress/chaperone signatures.
- The packaged `Hsf1` report from the same experiment matched the Parquet: postnatal `Hsf1` loss depressed only a small HSP90/HSP110 co-chaperone module and did not itself create a broad proteotoxic-stress, UPR/ISR, proteasome-bounce-back, redox, apoptosis, or mitochondrial-stress transcriptome. This report is interpretive context for the `Hsf1` training measurement, not independent replication.
- A nine-node profile comparison of `Hsf1`, `Hspa5`, `Hspa8`, `Hsp90ab1`, and DNAJ co-chaperones found 6 active nodes with only 1 to 9 significant genes and 3 nodes with no significant genes. The cohort showed little overlap of the positive or negative significant programs, so I did not treat the chaperones as one coherent centroid.
- Strong proteasome-subunit perturbations were treated as an upper boundary rather than direct analogues: `Psmb4` and `Psmc1` have hundreds of DEGs, while the direct HSF/chaperone losses remain one-digit in the same count table.

## Synthesis

The focal cells express `Hsf4` often enough that an on-target or direct transcriptional effect is plausible, and the stock card argues that a successful P16 edit should deplete new HSF4 protein by harvest. That moved the prediction above the all-target median of zero.

The magnitude evidence still points to a very small footprint. The closest available family perturbation, `Hsf1`, is the central heat-shock transcription factor and produced only 6 DEGs in the requested thalamic population. `Hsf4` has weaker evidence for a juvenile thalamic role than `Hsf1`: its isolated genetic requirement is ocular, the CNS signal needs aged `Hsf1` sensitization, and unquantified HSF-family buffering remains possible. The exact in-assay expression reach also means the signature is diluted across an aggregate in which about 71% of matched control nuclei had no detected `Hsf4` molecule.

I therefore forecast a count near the self/direct end of the measured HSF/proteostasis set rather than a broad stress response:

`predicted_n_degs = 1`
