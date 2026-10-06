# Uqcc2 focal DEG-count forecast

Target manifest: `Uqcc2`

Prediction target: `n_degs` in `151 TH Prkcd Grin2c Glut`, counted as measured genes with BH-adjusted Wilcoxon `p < 0.05`.

The declared biology bundle supports real focal engagement but not a broad expected nuclear-RNA state. `Uqcc2` is expressed in the matched non-target focal population: 16,471 of 23,679 nuclei expressed it, or 69.6%, with mean raw UMI 1.42 and pseudobulk 89.2 CPM. The stock card identifies UQCC2 as an early UQCC1-linked cytochrome-b / complex-III assembly factor. Acute CRISPR loss at P16 should stop new UQCC2-dependent complex-III assembly, while mature complex III made before editing initially persists and must decay by mitochondrial renewal before the lesion is fully realized at P37-P44. Multi-day respiratory-chain turnover proxies make substantial depletion by harvest plausible, but the evidence is partial and extrapolated from human-cell mitochondrial proteomics rather than matched mouse thalamic neurons.

The closest measured focal analogs were respiratory complex III perturbations. In the declared `151 TH Prkcd Grin2c Glut` count table, the direct structural comparators were all flat or singleton-scale:

| target | focal `n_degs` |
|---|---:|
| `Uqcrb` | 0 |
| `Uqcrc2` | 1 |
| `Uqcrfs1` | 0 |
| `Uqcrh` | 0 |
| `Uqcrq` | 1 |
| `Ttc19` | 1 |

The same pattern held for a broader respiratory-chain cohort: among 41 represented complex-I, complex-III, complex-IV, SDH, TOMM/TIMM, and mitochondrial-proteostasis targets that I checked, 25 had zero focal DEGs and the median focal count was 0. The nonzero close rows were usually just one formal hit, frequently the perturbed transcript itself. Direct Parquet inspection in the focal class showed no shared corrected downstream program among the retained complex-III comparators: `Uqcrc2` contributed only its self-transcript, `Uqcrq` contributed only `Gpr180`, `Ttc19` contributed only its self-transcript, and `Uqcrb`, `Uqcrfs1`, and `Uqcrh` had no FDR<0.05 focal genes.

The same-experiment corpus reinforced that these are not hidden broad mitochondrial signatures. Its complex-III Claim summarizes `Cyc1`, `Ttc19`, `Uqcrb`, `Uqcrc2`, `Uqcrfs1`, `Uqcrh`, and `Uqcrq` as largely transcriptionally buffered structural complex-III perturbations without a shared complex-III depletion RNA signature. Individual reports for `Uqcrc2`, `Uqcrq`, `Uqcrfs1`, `Uqcrb`, `Uqcrh`, and `Ttc19` describe either no mitochondrial ISR / UPRmt / redox / mitophagy program or singleton, target-private events. By contrast, `Opa1` and `Nrf1` were clear positive mitochondrial-axis controls in this same focal class, with 37 and 138 DEGs respectively in the training table, so the respiratory-chain flatness is not simply an inability of the focal population or Wilcoxon readout to detect mitochondrial stress.

Those data argue against assigning `Uqcc2` a moderate or large focal DEG count despite the source biology being credible. I placed it slightly above zero because UQCC2 has good focal expression and a realized assembly-factor lesion could yield a formal singleton, either through the target transcript or one idiosyncratic downstream feature. The point forecast is therefore one FDR-significant measured gene.
