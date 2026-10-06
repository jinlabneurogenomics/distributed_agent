# Tlr9 in `151 TH Prkcd Grin2c Glut`

## Point prediction

I predict `n_degs = 0` for `Tlr9`.

## Evidence used

- The declared holdout manifest contains the single target `Tlr9`; the declared biology bundle is the biology-only `Tlr9` card, and the target outcome was not consulted.
- Exact focal expression in the bundle is extremely low in matched non-target cells: `Tlr9` has 35 target UMIs across 23,679 `151 TH Prkcd Grin2c Glut` non-target nuclei, `0.147810296%` nuclei expressing, mean raw UMI `0.0014781`, and pseudobulk CPM `0.092638`.
- The same bundle argues that the edited receptor stock is not permanently installed: TLR9 must be trafficked and proteolytically processed, and adult neuron-specific loss can reduce neuronal TLR9. The best stock conclusion is therefore `likely_substantially_depleted` by the P16 to P37-P44 harvest interval, with no matched thalamic half-life.
- The held-in `151 TH Prkcd Grin2c Glut` count table has 1,205 zero-count targets among 1,674 training targets; the distribution is sparse and heavy-tailed, with mean `14.05` and maximum `2677`.
- Every close represented TLR-family or innate-signaling training comparator I found in that count table is zero in the focal class:
  `Tlr2 = 0`, `Tlr3 = 0`, `Tlr4 = 0`, `Tlr5 = 0`, `Tlr7 = 0`, `Tlr8 = 0`, `Irf3 = 0`, `Nfkb1 = 0`, `Chuk = 0`, and `Map3k7 = 0`.
- A matched `151 TH Prkcd Grin2c Glut` profile comparison over the training parquet for `Tlr7`, `Tlr3`, `Tlr4`, `Irf3`, `Nfkb1`, `Chuk`, and `Map3k7` found `0` BH-adjusted `p < 0.05` genes for each node across 17,259 measured features.
- Packaged same-experiment reports for the held-in comparators support the null interpretation rather than merely a missing named marker:
  `Tlr7` was silent in measured neuronal groups; `Tlr3` and `Tlr4` were near-pan-null outside one non-focal `Tlr3` call; and `Chuk`, `Nfkb1`, and `Map3k7` were flat across the basal juvenile NeuN-positive neuronal surface. These records consistently place the expected TLR/NF-kB/IRF response in ligand-activated, immune/glial, injury, or earlier developmental contexts, not in unstimulated postmitotic thalamic nuclei.

## Reasoning

TLR9 is a real neuronal target in some postnatal contexts, so I did not treat the perturbation as an editing impossibility: the biology bundle favors substantial loss of functional receptor by harvest. The deciding quantitative issue is reach and state. In this focal thalamic class, `Tlr9` is barely detected in the matched baseline population, so even a molecularly effective edit is unlikely to remove an active constitutive regulon from enough assayed nuclei to produce many BH-significant genes.

The training data point in the same direction. The closest measured TLR-family receptors and downstream innate hubs all have zero focal DEGs, and the full-signature comparison confirms that their focal profiles have no corrected features rather than small named cytokine panels being missed. Their corpus reports explain the flatness by the resting NeuN-positive assay state: without CpG/ssRNA/dsRNA/LPS-like ligand challenge and without glial or immune effector compartments, this pathway is not driving a basal transcriptional program.

I therefore expect `Tlr9` to join the TLR-family null group in `151 TH Prkcd Grin2c Glut`. A hidden hippocampal or activity-dependent TLR9 effect could have been missed in this thalamic, survivor-conditioned nuclear RNA assay, but that uncertainty is not enough to move the focal BH-count point estimate above zero.
