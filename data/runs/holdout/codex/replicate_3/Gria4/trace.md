# Gria4 direct DEG-count forecast

## Declared target and endpoint

- Target manifest: `Gria4`
- Cell class: `151 TH Prkcd Grin2c Glut`
- Endpoint: `n_degs`, the number of measured genes in this cell class with BH-adjusted Wilcoxon `p < 0.05`
- The held-out `Gria4` contrast was not present in `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`; `Gria4` was also not used as an observed profile.

## Evidence used

### Gria4 biology-only bundle

- The exact focal-population reach is strong: `Gria4` is detected in 23,472 of 23,679 non-target nuclei in `151 TH Prkcd Grin2c Glut`, or 99.13%, with mean raw UMI 8.60 and pseudobulk CPM 539.25.
- GluA4 is an AMPA-receptor pore-forming subunit. The bundle adjudicates the operative entity as a dynamic receptor-complex component, with disruptive editing expected to stop new GluA4 synthesis but not acutely inactivate receptor subunits that were translated and assembled before editing.
- The functional-stock card rates the P37-P44 stock as likely substantially depleted after P16 editing because the cited GluR4 half-life is about one day, far shorter than the 21-28 day editing window. That makes target engagement plausible in recovered focal nuclei.
- The prior phenotype evidence is from constitutive Gria4 hypomorphic/null mice, not a P16 conditional loss. It supports a thalamic synaptic role, especially cortico-reticular-thalamic excitation, but it does not establish that acute postnatal loss in NeuN-positive thalamic nuclei creates a nuclear RNA-seq program by harvest.
- Other AMPAR subunits can buffer receptor composition. The germline phenotype despite remaining Gria3 argues against complete functional replacement in the reticular-thalamic circuit, but the bundle contains no evidence that this partial redundancy resolves into a large cell-autonomous transcriptional response in the assayed aggregate thalamic population.

### Training count table

- The declared training table contained 1,674 observed perturbations for this cell class; 1,205 had `n_degs = 0`, 276 had `n_degs = 1`, 31 had `n_degs = 2`, and only 193 had `n_degs >= 2`.
- The three closest measured AMPA-receptor pore-forming paralogs were all null:
  - `Gria1`: 0
  - `Gria2`: 0
  - `Gria3`: 0
- AMPAR-local accessory or postsynaptic candidates in the training table were also tiny:
  - `Cacng2`: 0
  - `Cacng3`: 0
  - `Dlg4`: 1
  - `Nsf`: 0
  - `Syngap1`: 0
  - `Camk2a`: 0
  - `Camk2b`: 1
  - `Shank2`: 0
  - `Shank3`: 2
- Broader ionotropic glutamate-receptor perturbations were mostly zero or one:
  - `Grid1`: 1
  - `Grid2`: 0
  - `Grik1`: 0
  - `Grik3`: 0
  - `Grik4`: 0
  - `Grik5`: 1
  - `Grin2a`: 1
  - `Grin2b`: 2
  - `Grin2d`: 0
  - `Grin1`: 89

### Profile analysis of the declared Parquet

I compared the measured `151 TH Prkcd Grin2c Glut` expression profiles for the same glutamate-receptor and postsynaptic cohort in `training_de_all_cell_groups.parquet`.

- All 22 supplied training nodes had available profiles.
- In that cohort, 14/22 nodes had no BH < 0.05 features, 7/22 had 1-9 significant features, and only 1/22 had at least 50.
- `Gria1`, `Gria2`, and `Gria3` each had exactly 0 positive and 0 negative significant features.
- The profile table again singled out `Grin1`, with 40 positive and 49 negative significant features. I treated it as an informative boundary rather than a close local analog: `Grin1` is the obligatory NMDAR subunit and its 89-DEG footprint was not shared by the AMPAR paralogs or the receptor-accessory perturbations.

## Synthesis

The biology bundle argues that `Gria4` is genuinely expressed and should be functionally depleted by harvest, so I did not collapse the forecast just to a generic zero-inflated prior. The endpoint, however, is a survivor-conditioned nuclear RNA response, not synaptic current, seizure susceptibility, or receptor composition. The best operation-level quantitative anchors in the same focal class are the other AMPAR core subunits, and all three were exactly silent at BH < 0.05. Nearby receptor-trafficking and postsynaptic genes stayed between 0 and 2 significant genes, while the large `Grin1` response appears to mark NMDAR-core loss rather than a transferable AMPAR pore-subunit scale.

I therefore expect any acute `Gria4` signal in this aggregated thalamic neuronal class to be absent or at most a one-to-two-gene edge case. The integer point forecast is:

`Gria4`: `0`
