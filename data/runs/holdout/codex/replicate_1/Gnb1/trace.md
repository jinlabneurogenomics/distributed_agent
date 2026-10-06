# Gnb1 n_degs forecast

Target: `Gnb1`

Endpoint: number of measured genes in `151 TH Prkcd Grin2c Glut` with BH-adjusted Wilcoxon `p < 0.05`, using the held-out direct-forecast inputs only.

## Evidence used

- The one-row holdout manifest names `Gnb1`; the declared biology bundle for the same target reports no endpoint values and no labeled-neighbor outcomes.
- Exact focal-population reach from the `Gnb1` bundle supports that the target transcript is readily measurable in the assayed class: in non-target controls for `151 TH Prkcd Grin2c Glut`, `Gnb1` was detected in 19,830 / 23,679 nuclei, `83.745%`, with mean raw UMI `2.219`, mean CP10K `1.379`, and pseudobulk CPM `139.095`.
- The `Gnb1` biology card makes functional depletion plausible by harvest: Gbeta1 is a dynamic heterotrimeric G-protein beta component, disruptive editing stops new intact supply, and the P16 to P37-P44 interval exceeds typical neural-proteome turnover, although a matched Gbeta1 half-life is unknown.
- The strongest `Gnb1` loss evidence is developmental or from unmatched postnatal cortical/variant contexts, not complete P16 loss in juvenile thalamic glutamatergic neurons. The bundle therefore supports possible observability but not a large mature thalamic nuclear-RNA response.
- The same-experiment corpus had no target-specific Findings or Claims for `Gnb1`; the target is held out rather than semantically reported.
- The declared `151 TH Prkcd Grin2c Glut` training count table is extremely sparse: 1,205 / 1,674 training targets have `n_degs = 0`, 276 have `n_degs = 1`, and only 193 exceed 1.
- Closest measured G-protein or GPCR effector comparators in that same table were quiet in the focal class:
  - `Gnb5`, `Gnas`, `Gnal`, `Kcnj6`, `Adcy1`, `Adcy3`, `Adcy5`, and `Plcb1`: `0`
  - `Gnao1`, `Gabbr1`, `Gabbr2`, `Cnr1`, `Grm1`, `Grm7`, `Prkaca`, and `Prkar1a`: `1`
- Direct Parquet rows for those focal singletons showed that most of them were self-transcript events, not downstream programs:
  - self rows: `Gnao1`, `Gabbr1`, `Gabbr2`, `Grm1`, `Grm7`, `Prkaca`, `Prkar1a`
  - one non-self singleton among the inspected GPCR-pathway genes: `Cnr1` -> `Srcap`
- A symmetric observed-profile comparison over 17 GPCR/G-protein/cAMP nodes in the focal class found all 17 profiles available; 9 / 17 had no significant features and 8 / 17 had only 1-9 significant features. `Gnb5`, `Gnas`, and `Gnal` had zero significant genes in the inspected focal rows, while `Gnao1` and `Prkaca` each had exactly one.
- Packaged same-experiment reports for the measured pathway relatives consistently described downstream buffering rather than a hidden high-burden module: `Gnb5` had no robust downstream transcriptional response in any measured neuronal group; `Gnao1` was downstream-null in 21 / 22 groups; `Gnas` had a one-gene response in one non-focal group; `Adcy1/3/5`, `Grm1/5/7`, `Kcnj6`, `Plcb1`, `Prkaca`, and `Prkar1a` were null or near-null downstream across their measured neuronal groups.

## Reasoning

`Gnb1` is a more central GPCR signaling component than the single receptors or adenylyl-cyclase paralogs in the training set, is expressed in the exact focal class, and should lose newly synthesized Gbeta1 after editing. That argues against treating it like an unavailable or unexpressed target.

The best endpoint-matched measured evidence, however, points the other way for a broad downstream count. Perturbing basal GPCR inputs, alpha/beta pathway components, GIRK signaling, adenylyl cyclases, PLC, and PKA was almost always buffered in this sparse postnatal neuronal snRNA endpoint. In the focal class, the one-count analogs were usually just their own edited transcript crossing FDR, not a secondary thalamic state.

Because the requested `n_degs` includes the target transcript itself, `Gnb1`'s high focal expression makes one significant row plausible even if the mature downstream transcriptome remains buffered. The biological and measured-comparator evidence gives little support for more than a self-row or one isolated singleton. I therefore predict:

`predicted_n_degs = 1`
