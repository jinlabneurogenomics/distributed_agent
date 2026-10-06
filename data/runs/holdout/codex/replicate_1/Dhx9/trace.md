# Dhx9 n_degs forecast

Target and endpoint:

- Target: `Dhx9`
- Focal population: `151 TH Prkcd Grin2c Glut`
- Endpoint: measured genes with BH-adjusted Wilcoxon `p < 0.05`
- Prediction: `8`

Evidence used:

- The holdout manifest and biology bundle both identify the one requested target as `Dhx9`.
- The biology bundle reports exact in-assay reach for the focal population: `Dhx9` was detected in 20,305 of 23,679 recovered non-target nuclei, or 85.75%, with mean expression of 1.51 CP10K. This makes the transcript present enough for perturbation to matter in the assayed thalamic class, while not saying anything quantitative about editing efficiency.
- The functional-stock card judged `Dhx9` likely substantially depleted by P37-P44 after a P16 edit. The operative protein is a renewable ATP-dependent DNA/RNA helicase, and the best mouse proxy put peptide half-lives at roughly 50-71 hours, so the 21-28 day window should allow many replacement cycles.
- That biological evidence was not target-specific endpoint evidence. The same bundle flags the important dampers: no postnatal thalamic timing anchor, only developmental neural phenotype evidence, uncertain survivor conditioning, and no direct matched compensation test.
- The training count table for this exact cell class is highly sparse: 1,205 of 1,674 training perturbations have `n_degs = 0`, the median is `0`, the 75th percentile is `1`, and only 103 are above `10`.
- I generated typed Dhx9 analog nominations against the explicit 1,674-gene training universe. The top RISC/siRNA branch around `Ago2`, `Dicer1`, `Ago1`, `Tnrc6a`, `Tnrc6b`, and `Fmr1` has observed counts `0,0,1,0,0,0`. The closest ATP-helicase / DHX9-associated flank was also mostly quiet: `Ddx3x=8`, `Ddx39b=0`, `Adar=0`, `Prkdc=0`, `Setx=0`, `Wrn=0`, `Ski=2`, and `Ascc3=18`.
- I separately checked broader RNA-processing comparators. Several core spliceosome or nuclear RBP perturbations are huge in this class, including `U2af2=828`, `Prpf6=454`, `Cdc40=624`, `Hnrnpu=733`, and `Rnpc3=868`, but these are proximal losses of constitutive splicing/export or structural RBP functions rather than Dhx9-like structured-nucleic-acid helicase loss.
- A 24-node focal profile comparison of the selected RNA/helicase/RBP cohort found all selected profiles present, with 9 having no significant focal genes, 5 having 1-49, and 10 having at least 50. The profile diagnostic therefore supported treating the broad RNA-processing set as heterogeneous rather than pooling its count scale.

Reasoning:

`Dhx9` is expressed and probably depleted by harvest, so I did not forecast a pure null. I also did not transfer the hundreds-of-DEGs behavior from core spliceosome factors, because the direct DHX9 complex partners and helicase comparators that most closely match Dhx9's molecular operation are near the floor in the focal training table. The best quantitative bearing came from the low RNA-helicase flank: `Ddx3x` at 8, `Hnrnpa2b1` at 11 as a small exact-complex/RBP comparator, and `Ascc3` at 18 as another ATP helicase, offset by direct `Adar`, `Prkdc`, and `Ddx39b` zeros.

I therefore used a low-single-digit to low-two-digit point and set the final integer to `8`.
