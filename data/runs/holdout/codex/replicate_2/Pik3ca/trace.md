target_name: Pik3ca
predicted_n_degs: 0

Evidence used
- Declared target: the one-row holdout manifest and biology bundle both specify `Pik3ca`.
- Endpoint: `n_degs` is the count of measured genes in `151 TH Prkcd Grin2c Glut` with BH-adjusted Wilcoxon `pvals_adj < 0.05`.
- Declared training count table: 1,674 non-held-out targets in this cell class had a highly skewed response distribution: 1,205/1,674 were zero, the median was 0, the 75th percentile was 1, the 90th percentile was 2, and the 95th percentile was 18.
- Exact in-assay target reach from the `Pik3ca` biology bundle: `Pik3ca` was measured in this focal population and expressed in 16,402/23,679 non-target cells, 69.27%, with mean log1p(CP10K) 0.5205. I therefore did not treat the forecast as a target-absence null.
- Functional stock card: p110-alpha is a renewable class-IA PI3K catalytic component; the card adjudicates functional stock as likely substantially depleted by the P16-to-P37/P44 harvest, while noting that the strongest timing evidence is heterologous and that endogenous postmitotic thalamic kinetics are not directly measured.
- Functional prior: mouse POMC/AgRP neuron Pik3ca deletion supports postnatal neural relevance and incomplete rescue by related p110 isoforms, but the bundle rates that transfer only low-confidence because the evidence is hypothalamic and developmental rather than acute thalamic CRISPR.
- Declared count table and exact Parquet measurements for represented receptor/proximal PI3K-AKT nodes in `151`:
  `Igf1r 0`, `Insr 0`, `Irs1 0`, `Pik3cb 0`, `Pik3r1 0`, `Pik3r2 0`, `Akt3 0`, `Rptor 0`, `Mtor 2`, and `Gsk3b 6`.
- Nearby downstream controls were count-bearing but modest in this same cell class: `Tsc2 86`, `Depdc5 13`, and `Srebf2 7`. The exact significant overlap was branch-specific: for example, `Tsc2` and `Depdc5` shared 8 significant genes, `Depdc5` and `Srebf2` shared 3, and `Tsc2` and `Srebf2` shared 2.
- Same-experiment corpus for visible training genes interpreted `Tsc2` loss as an mTORC1 metabolic/endomembrane hyperactivation state and explicitly separated it from receptor-proximal and core class-IA PI3K losses. The `Akt3`, `Igf1r`, `Insr`, `Pik3cb`, `Pik3r1`, `Pik3r2`, and `Mtor` findings all recorded that upstream PI3K/receptor nodes were flat in this basal sparse postnatal neuronal readout even though the assay could detect a Tsc2/Depdc5-like downstream mTOR state.

Reasoning

`Pik3ca` is reachable: it is expressed in most focal non-target nuclei, and the biology-only bundle argues that a successful disruptive edit should deplete p110-alpha stock over 21-28 days. Those facts make a technical zero less likely than it would be for a non-expressed or persistent-stock target.

The scalar endpoint here, however, is a steady-state nuclear RNA burden in recovered thalamic glutamatergic neurons, not acute PIP3, pAKT, pS6, soma size, or survival. The best training evidence in the declared table puts single receptor/proximal class-IA perturbations at the zero floor: both assayed p85-family regulatory subunits, the assayed p110 catalytic paralog, insulin/IGF-side receptors, IRS1, and AKT3 were all 0 in `151`. Direct mTORC1 loss through `Mtor` and `Rptor` was also essentially silent. The nonzero training signals lie mainly downstream at TSC/GATOR/SREBP, especially `Tsc2`; that is an opposite-direction loss-of-brake state with a sterol/lysosomal feedback program, so I treated it as evidence that the pathway can become transcriptional when forced, not as a magnitude donor for upstream `Pik3ca` loss.

Balancing expression and expected stock depletion against the strong local buffering of represented upstream PI3K-AKT perturbations, I predict no BH-significant downstream genes for `Pik3ca` in `151 TH Prkcd Grin2c Glut`.
