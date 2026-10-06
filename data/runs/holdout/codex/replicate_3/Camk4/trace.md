# Camk4 DEG-count forecast

Target and endpoint: `Camk4` in `151 TH Prkcd Grin2c Glut`; `n_degs` counts measured genes with Wilcoxon BH-adjusted `p < 0.05` in this cell class.

Evidence used:

- Declared biology bundle for `Camk4`:
  - CAMK4 is a monomeric Ca2+/calmodulin-dependent kinase in the CaMKK-CAMK4 cascade with transcriptional outputs through regulators including CREB1, MEF2D, JUN, and RORA.
  - Existing protein stock should not be an insurmountable obstacle: the card adjudicates CAMK4 as a renewable free/diffusible product and concludes it is likely substantially depleted across the P16 to P37-P44 editing window, with the important caveat that the quantitative 2.37-day lifetime came from cultured rat cortical neurons rather than juvenile mouse thalamus.
  - Exact focal-population expression is strong: `Camk4` is available in the 151-class expression table, with mean CP10k `1.5459`, mean raw UMI `2.4649`, and `20002 / 23679 = 84.47%` non-target cells expressing.
  - Mature-neuron thalamic dependence is not directly established. Germline mouse loss supports a neural CREB/plasticity role, but matched postnatal thalamic loss, phenotype latency, and compensation by related CaM kinases or parallel CREB kinases remain unresolved.

- Declared `151 TH Prkcd Grin2c Glut` training count table:
  - The response distribution is zero-heavy even in this high-yield class: among 1,674 training perturbations, 1,205 have `n_degs = 0`; the median is `0`, the 90th percentile is `2`, and the 95th percentile is `18`.
  - Nearby calcium/CaM perturbations are mostly quiet or compact: `Calm1` 14, `Calm2` 0, `Calm3` 1, `Camk2a` 0, `Camk2b` 1, `Camk2g` 0, `Prkaca` 1, `Ppp3ca` 4, `Ppp3cc` 0, `Ppp3r1` 9.
  - The calcium-channel branch is also mostly small with one compact T-type response: `Cacna1g` 12, `Cacna1a` 0, `Cacna1d` 0, `Cacna1e` 0, `Cacna2d1` 1, `Cacna2d2` 0, `Cacnb2` 0, `Cacnb4` 1, `Cacng2` 0, `Cacng3` 0.
  - The direct transcriptional branch gives the closest scale for a nuclear CAMK4 loss: `Creb1` 10, `Crebbp` 8, `Mef2a` 4, `Mef2c` 1, `Mef2d` 0. `Rora` has 278 DEGs, but the same-experiment report layer describes a broad Rora-selective thalamic nuclear-receptor program not phenocopied by `Rorb`/`Rorc`, so I treated it as an existence proof for a large maintained thalamic transcription-factor program rather than a magnitude donor for upstream CAMK4.

- Declared expression Parquet for selected training rows:
  - The 151-class signatures behind these analog counts were narrow: `Calm1` had 14 FDR<0.05 genes, `Cacna1g` had 12, `Creb1` had 10, `Crebbp` had 8, and `Mef2a` had 4.
  - The significant genes were not a shared large immediate-early/CREB module. Packaged same-experiment findings for `Calm1` and `Cacna1g` likewise note that those responses did not activate broad Fos/Junb/Arc/Npas4/Egr/Nr4a activity-dependent or CREB/BDNF programs.

Reasoning:

`Camk4` is well expressed in the focal population and should lose functional kinase stock during the assay window, so a strict zero forecast would ignore target reach and the short-lived kinase prior. At the same time, the postnatal thalamic endpoint is upstream-signaling loss, not direct removal of CREB1, CREBBP, MEF2, JUN, or RORA protein. The training data show that perturbing this calcium-to-transcription neighborhood usually produces either zero/singleton responses or compact 4-14 gene footprints, with `Rora` being a downstream transcription-factor outlier rather than a local analogue.

I therefore placed `Camk4` in the low but nonzero part of the compact-response band, centered near the `Creb1`/`Crebbp` counts and below the stronger `Calm1`/`Cacna1g` counts to reflect expected buffering through parallel CREB and CaM-kinase routes.

Point forecast: `8`.
