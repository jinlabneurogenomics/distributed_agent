# Atp6v0c direct DEG-count forecast

## Requested target

- `target_name`: `Atp6v0c`
- focal cell group: `151 TH Prkcd Grin2c Glut`
- endpoint: number of measured genes with Wilcoxon BH-adjusted `p < 0.05`

## Evidence used

### Declared Atp6v0c biology bundle

The declared biology-only bundle for `Atp6v0c` reports exact in-assay reach in the focal non-target cells: the transcript was detected in 23,481 of 23,679 nuclei, or 99.16%, with mean raw UMI 9.16 and mean log1p CP10K 1.816 in `151 TH Prkcd Grin2c Glut`. That makes the target transcript itself technically easy to observe if editing drives nonsense-mediated decay or destabilization.

The same bundle places the protein in a membrane-installed V0 proton-pore complex. Its functional-stock adjudication calls the P16-to-P37/P44 window "partially_depleted_or_leading_edge": productive editing should stop new Atp6v0c synthesis, but pre-existing V0 complexes and vesicular/lysosomal membrane pools can keep operating until the relevant membranes turn over. The closest kinetic evidence in the bundle is a mouse cortical synaptic-vesicle Atp6v0c lifetime of about 20.29 days, comparable to the 21-28 day assay interval. The bundle found no target-specific postnatal neural loss-of-function timing study that would force a large, fast recovered-nucleus transcriptional response.

### Training counts in the same focal class

The declared `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` table contains 1,674 observed training targets. The distribution is very sparse: 1,205/1,674 targets are zero, 307 are in the 1-2 DEG bin, and 1,512/1,674 are <=2. Only 59/1,674 have >=50 DEGs.

The closest represented V-ATPase training perturbations in this same endpoint were all in the 0-2 range:

| target | n_degs in 151 TH Prkcd Grin2c Glut |
|---|---:|
| Atp6v1a | 0 |
| Atp6v1b2 | 0 |
| Atp6v1e1 | 0 |
| Atp6v0a1 | 1 |
| Atp6ap2 | 2 |

Other lysosome/autophagy-adjacent training targets mostly supported the same low-count baseline: `Atg5`, `Atg16l1`, `Becn1`, and `Lamp2` had 0; `Atp13a2` and `Sqstm1` had 1. Some more indirect trafficking or stress perturbations were detectably larger, notably `Rab7` at 501, `Psmb4` at 742, `Atp2a2` at 187, `Vps35` at 17, and `Vps54` at 31, so the class was not globally unable to call organelle-stress DE.

### Parquet-level inspection of selected training profiles

I checked the declared training Parquet in the exact `151 TH Prkcd Grin2c Glut` context for the V-ATPase/endolysosomal cohort above. The V-ATPase-nearest profiles had almost no FDR<0.05 downstream genes:

| target | matched perturbed nuclei | FDR<0.05 genes | downstream FDR<0.05 genes |
|---|---:|---:|---:|
| Atp6v1a | 76 | 0 | 0 |
| Atp6v1b2 | 32 | 0 | 0 |
| Atp6v1e1 | 52 | 0 | 0 |
| Atp6v0a1 | 197 | 1 | 0 |
| Atp6ap2 | 116 | 2 | 1 |

`Atp6v0a1`'s sole FDR<0.05 row was its own transcript, while `Atp6ap2` called its own transcript plus `Atp6v0a1`. `Atp6v1a`, `Atp6v1b2`, and `Atp6v1e1` had no called genes in this class. A run-local symmetric profile comparison over V-ATPase, autophagy, lysosomal, endosomal, proteasome, and ER-calcium controls found no FDR-level overlap from these near-null V-ATPase signatures into the large `Rab7`, `Psmb4`, or `Atp2a2` stress signatures.

### Same-experiment corpus context

The selected same-experiment corpus had no direct `Atp6v0c` Finding or Claim. Its V-ATPase comparator Findings were still material because they describe the represented neighbors in the same experiment. `Atp6v0a1:F003`, `Atp6ap2:F004`, `Atp6v1a:F004`, and the higher-order Claim containing `Atp6ap2`, `Atp6v0a1`, `Atp6v1a`, and `Atp6v1e1` all state the same boundary: membership in the V-ATPase pump was not sufficient to produce a shared postnatal neuronal snRNA-seq module; the measured subunits/regulators were flat, sparse, divergent, or non-overlapping. `Rab7` Findings supply a positive control that a late-endosome/lysosome compensation module was visible in these thalamic/midbrain glutamatergic cells when the perturbation crossed a nuclear response threshold.

## Synthesis

The target is well expressed in the focal cells and encodes a nonredundant V0 c-ring subunit, so I do not want to copy the complete zeros from `Atp6v1a`, `Atp6v1b2`, and `Atp6v1e1` verbatim. High Atp6v0c mRNA reach makes one self-transcript call plausible if enough edited cells reduce nuclear target RNA.

The downstream forecast is nevertheless near-null. The operative protein is a preassembled membrane complex with a turnover time comparable to the assay interval; the direct postnatal-neural loss evidence is missing; and the closest same-complex perturbations did not launch a canonical lysosomal, autophagy, or stress module in recovered P37-P44 neurons. `Rab7`, `Atp2a2`, and `Psmb4` show that broad thalamic organelle-stress signatures exist in this assay, but the represented V-ATPase subunits sit on the sparse side of that boundary rather than on the 100s-of-DEGs side.

I therefore predict a single FDR<0.05 row: most likely the `Atp6v0c` self transcript or one isolated V-ATPase-adjacent compensatory gene, with no broad downstream program.

## Prediction

`Atp6v0c`: `1`
