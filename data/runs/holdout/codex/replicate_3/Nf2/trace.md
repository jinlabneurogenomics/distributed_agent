# Nf2 n_degs forecast

Target: `Nf2` in `151 TH Prkcd Grin2c Glut`.

## Evidence used

- The declared `Nf2` biology bundle reports exact in-assay reach in the focal
  non-target thalamic population: `Nf2` is detected in 13,221 / 23,679 nuclei
  (`55.834%`), with mean raw UMI `0.909` and mean log1p CP10k `0.371`.
  Thus the target is present in a sizeable but not universal fraction of the
  assayed recovered cells.
- The same bundle adjudicates merlin functional stock as
  `likely_substantially_depleted`: a P16 disruptive edit should block new
  merlin supply, merlin is a dynamic FERM/ERM membrane-cytoskeleton/signaling
  adaptor rather than a durable installed product, and the only direct kinetic
  half-life quoted in the card is short relative to the 21-28 day harvest
  window. This made complete non-engagement unlikely.
- The positive Nf2 functional evidence is not a matched thalamic RNA endpoint:
  the postnatal mouse neuronal phenotype is cerebellar synaptic-terminal /
  excitatory-current disruption with a non-transferable timing anchor, and
  ERM-family compensation in thalamic neurons is unresolved. I therefore used
  it as evidence for possible local neuronal biology, not as evidence for a
  high whole-nucleus transcriptional response.
- The focal training count table is very sparse: among 1,674 observed training
  perturbations in `151 TH Prkcd Grin2c Glut`, 1,205 have `n_degs = 0` and
  another 276 have `n_degs = 1`; the median is 0 and the 90th percentile is
  only 2.
- Curated analogue nomination over the actual training universe found no exact
  merlin paralog/complex donor. The nine non-fallback Nf2-adjacent observed
  genes were:
  `Rac1 = 0`, `Rdx = 1`, `Cdc42 = 1`, `Limk1 = 0`, `Tead1 = 0`,
  `Pak2 = 0`, `Pak3 = 0`, `Calm1 = 14`, `Pak1 = 1`, and
  `Ctnnb1 = 383`.
- I treated `Ctnnb1` as an upper/context boundary rather than a direct scale
  donor. Its 383-gene response is a canonical thalamic Wnt/beta-catenin/TCF
  state in the same-experiment Findings, whereas the closer Rho/PAK/ERM and
  Hippo/TEAD perturbations in the training table were flat or near-flat.
- The bounded profile comparison of
  `Rac1`, `Rdx`, `Cdc42`, `Limk1`, `Tead1`, `Pak2`, `Pak3`, `Calm1`, `Pak1`,
  and `Ctnnb1` in the focal class gave five no-DEG profiles, three 1-9 DEG
  profiles, one 10-49 profile, and `Ctnnb1` as the only `>=50` profile.
  The ERM/Rho/PAK/Hippo cohort had 36 / 36 pairwise profiles available but no
  recurrent significant program: its same-direction significant-program
  overlap coefficient was zero in all emitted cases.
- The explicit significant genes in that focal profile check were consistent
  with mostly self or isolated hits for the closest low-count nodes:
  `Rdx` had only `Rdx` itself, `Cdc42` had only `Cdc42`, and `Pak1` had only
  `Pak1` at BH-adjusted `p < 0.05`.
- Packaged Findings for `Rdx` and `Rac1` also favored transcriptomic buffering
  of this local cytoskeletal/synaptic axis: `Rdx` had measurable self-transcript
  loss in `151 TH Prkcd Grin2c Glut` with no FDR-significant downstream genes,
  and `Rac1` Findings reported that represented Rac/Cdc42/PAK/WRC/GEF/GAP
  relatives failed to form a shared nuclear mRNA module.

## Synthesis

Nf2 is expressed and merlin protein should be depleted in many edited focal
neurons, so I did not assign a pure absent-target prior. The expected biology,
however, is a membrane/cytoskeletal and synaptic adaptor phenotype with
possible local protein-localization or electrophysiology effects; the closest
observable ERM and Rho/PAK training perturbations show that this axis is often
buffered in the acute juvenile NeuN-positive snRNA-seq endpoint.

I therefore placed the forecast at the low end of the focal training
distribution. `Rdx`, the nearest observed ERM-family perturbation, is an
especially relevant scale check because its focal thalamic count was one and
that one gene was the self-transcript, not a downstream module. The possibility
that Nf2 self-transcript depletion is significant moved the point from `0` to
`1`, while the flat `Tead1` and Rho/PAK candidates and the distinct Ctnnb1/Wnt
profile argued against forecasting a multi-gene Hippo/Wnt-like response.

Predicted `n_degs`: `1`.
