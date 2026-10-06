target_name: Hnrnpa1
predicted_n_degs: 15

Evidence used

- Declared target and endpoint:
  - The holdout manifest declares the only target as Hnrnpa1.
  - The endpoint is n_degs in 151 TH Prkcd Grin2c Glut, counted as measured genes with Wilcoxon BH-adjusted p < 0.05.
  - The focal-cell training table contains 1,674 non-held-out targets; Hnrnpa1 is absent.

- Hnrnpa1 biology bundle:
  - Hnrnpa1 is expressed in the exact focal population: 11,396 / 23,679 non-target nuclei express it, 48.13%, with mean_log1p_cp10k = 0.2999 and pseudobulk_cpm = 44.22.
  - The card adjudicates hnRNP A1 as a dynamic nuclear/cytoplasmic RNA-binding RNP component.
  - Available turnover evidence, 5.27 days in cultured rat cortical neurons, makes a P16-to-P37/P44 CRISPR loss likely to substantially deplete the protein stock by harvest.
  - The phenotype evidence supports possible neuronal observability but is not target-context matched: mouse primary cortical neurons showed splicing, dendritic, and synaptic abnormalities after hnRNP A1/A2 depletion, while the direct Hnrnpa1-null mouse evidence is embryonic and non-neural.
  - The bundle's own caveat that survivor conditioning may attenuate the recovered nuclear RNA signature is important for not projecting a large lethal signature.

- Focal training-count background:
  - The 151 TH count table is very sparse: 1,205 / 1,674 targets are zero, 276 are exactly one, and the median is zero.
  - Only 50 / 1,674 targets are in the 6-20 DEG band; only 42 exceed 100.
  - The close measured A/B-family comparator Hnrnpa2b1 has 11 focal DEGs.
  - Other measured hnRNP-family perturbations are also weak except for distinct broad RBP states: Hnrnpdl has 1 focal DEG and Hnrnph2 has 4, whereas Hnrnpc has 122 and Hnrnpu has 733.
  - Broader essential RNA/splicing perturbations are in the heavy tail: Tardbp 210, Snrnp70 213, Prpf6 454, U2af2 828, and Rnpc3 868.

- Same-experiment corpus context:
  - Hnrnpa2b1 generated only 25 downstream FDR < 0.10 calls across six measured cell groups, with the largest signatures in 151 TH Prkcd Grin2c Glut and 155 MB Glut.
  - Hnrnpa2b1's strongest RNA/RNP hits included Hnrnpa1 up in its main glutamatergic responders and Hnrnpu down in two responders, consistent with a small compensatory hnRNP/RNP rebalancing state rather than a collapse of RNA processing.
  - A high-confidence corpus Claim states that measured hnRNP-family perturbations were not interchangeable; Hnrnpa2b1 and Hnrnpdl were weak/flat while Hnrnpu/Hnrnpc-like RBP responses were distinct.

- Profile analysis of the declared expression parquet:
  - A focal 151 TH profile comparison over Hnrnpa2b1, Hnrnpc, Hnrnpdl, Hnrnph2, Hnrnpu, Tardbp, Matr3, U2af2, Prpf6, and Snrnp70 recovered the same split: Hnrnpa2b1 had 7 positive and 4 negative FDR < 0.05 features, Hnrnpdl had 1, Hnrnph2 had 4, Hnrnpc had 122, and Hnrnpu had 733.
  - Hnrnpa2b1's whole-profile correlations to the broad RBP/splicing comparators were tiny: Pearson 0.014-0.072 across Hnrnpc, Matr3, Tardbp, U2af2, Prpf6, and Snrnp70. This argues against using the hundreds-of-DEG core-splicing/RBP burdens as quantitative proxies for the A1/A2-like state.

Synthesis

Hnrnpa1 should not be forecast as a pure null: it is detectable in the focal
neurons, the edited protein stock should have time to turn over by harvest, and
the biology bundle plus the Hnrnpa2b1 signature both point to neuronal RNP
rewiring. The best same-family measured anchor is Hnrnpa2b1 with 11 focal DEGs.
I moved modestly upward from 11 because the Hnrnpa1 bundle reports stronger
single-gene loss evidence and incomplete A2/B1 compensation outside neurons, but
not into the Hnrnpc/Hnrnpu or U2af2/Prpf6 range because those observed broad
states were target-specific and poorly aligned with Hnrnpa2b1. The focal
expression reach is also moderate rather than ubiquitous, so a low nonzero value
in the 6-20 training band is the most plausible point estimate.
