# Bbip1 `n_degs` forecast

Target: `Bbip1` in `151 TH Prkcd Grin2c Glut`

## Evidence used

- The declared holdout manifest contains the single target `Bbip1`.
- The endpoint is the count of measured genes with BH-adjusted Wilcoxon `p < 0.05` in `151 TH Prkcd Grin2c Glut`.
- The 1,674 training perturbations in the declared 151-count table are highly zero-inflated:
  - 1,205 have `n_degs = 0`.
  - 276 have `n_degs = 1`.
  - Only 193 have `n_degs > 1`.
  - The median is 0 and the 75th percentile is 1.
- The nearest represented BBSome/ciliary perturbations in the same focal class are null or self/singleton scale:
  - `Bbs5`: 0
  - `Ttc8`: 1
  - `Ift88`: 0
  - `Lztfl1`: 0
  - `Cep290`: 0
  - `Rpgrip1l`: 0
- A broader ciliary/IFT/Hedgehog sentinel set was also nearly all 0 in the focal class: `Adcy3`, `Dync2h1`, `Dync2i1`, `Ift43`, `Ift81`, `Kif3b`, `Ttc21b`, `Cplane1`, `B9d1`, `Cspp1`, `Dzip1`, `Smo`, `Gli1`, `Gli2`, `Ptch1`, `Lepr`, `Htr6`, `Mchr1`, and `Gpr161` were 0; `Arl3` and `Prkaca` were 1.
- Same-experiment Findings for the measured BBSome and ciliary training perturbations interpret those low counts as genuine absence of a broad basal neuronal nuclear-RNA program, not as an isolated 151-class accident:
  - `Bbs5` had only one FDR<0.10 downstream event atlas-wide and the represented BBSome/ciliary relatives did not phenocopy it.
  - `Ttc8` was transcriptionally buffered across recovered neuronal groups; its ciliary comparators were nearly orthogonal and zero- or singleton-only.
  - `Ift88`, `Cep290`, and `Rpgrip1l` reports independently describe absent or nearly absent Hedgehog, GPCR, transition-zone, and BBSome/IFT transcriptional responses in this postnatal NeuN+ snRNA assay.
- The `Bbip1` biology bundle supports target engagement plausibility but not a large DEG burden:
  - BBIP1/BBS18 is an obligate BBSome scaffold and operative BBSome stock is expected to substantially decline over the 21-28 day P16-to-harvest interval.
  - Congenital Bbip1 loss causes postnatal neuronal ciliary cargo-localization phenotypes in hippocampal and hypothalamic neurons, but those are other neural contexts and protein-localization/circuit phenotypes rather than a matched thalamic RNA state.
  - Exact focal-population expression makes the target transcript measurable in `151 TH Prkcd Grin2c Glut`: Bbip1 is detected in 16,951 of 23,679 non-target nuclei, with mean raw UMI 1.44 and mean CP10K 0.93.

## Synthesis

The closest measured operations say that acute postnatal disruption of BBSome/ciliary trafficking genes is usually below this assay's FDR-level basal nuclear RNA threshold in thalamic glutamatergic neurons. That argues strongly against a multi-gene `Bbip1` response.

The main upward adjustment from a pure downstream-null forecast is the target transcript itself. `Bbip1` is expressed in most focal non-target nuclei, so a realized edit could produce a single significant self-transcript even if downstream ciliary biology stays subcellular and off-modality. Among the closest available comparators, `Ttc8` is exactly that pattern in the requested count table: a BBSome component at `n_degs = 1` with no interpreted downstream mRNA program.

I therefore forecast a self/singleton-sized response rather than a many-gene ciliary state.

Predicted `n_degs`: **1**
