# Direct Fth1 n_degs forecast

Target: `Fth1` in `151 TH Prkcd Grin2c Glut`.

Requested endpoint: number of measured genes in the focal population with
BH-adjusted Wilcoxon `p < 0.05`.

## Evidence used

- The held-out manifest contains only `Fth1`; the declared focal-population
  training table contains 1,674 other perturbations.
- The focal training count distribution is sparse: median `n_degs = 0`, 75th
  percentile `= 1`, 90th percentile `= 2`, 95th percentile `= 18`, and 1,205 of
  1,674 training perturbations have no FDR-significant genes. The mean of
  `14.1` is driven by a small heavy tail.
- Fth1 has strong measured reach in the exact focal population but is not a
  ubiquitous high-abundance neuronal transcript: the non-target baseline is
  17,566/23,679 expressing nuclei, `74.18%` cells expressing, mean CP10k
  `1.0016`, and pseudobulk CPM `103.84`.
- The biology card supports real target engagement by harvest but with
  incomplete timing evidence. FTH1 is the ferroxidase component of the assembled
  24-subunit ferritin iron-storage shell; a disruptive edit should stop new FTH1
  supply but should not immediately dismantle pre-existing ferritin particles or
  release their mineral cores. Non-neural ferritin-turnover data make
  substantial stock depletion over the 21-28 day P16-to-P37/P44 window plausible,
  while the postmitotic thalamic-neuron turnover rate, iron-state dependence,
  Ftl1-containing residual shells, and survivor conditioning are unresolved.
- The most direct named partner/turnover genes in the Fth1 card, `Ftl1` and
  `Ncoa4`, were absent from the training count table, so they could not be used
  as measured comparators.
- Training perturbations that do cover the closest iron, mitochondrial-iron, and
  antioxidant contexts were mostly transcriptionally quiet in the same
  population:
  `Ireb2 = 1`, `Tfrc = 0`, `Aco2 = 0`, `Abcb7 = 0`, `Gpx4 = 0`,
  `Nfe2l2 = 0`, `Prdx1 = 0`, and `Gclc = 0`.
- Ferritin-turnover-adjacent autophagy or lysosome genes were also mostly quiet:
  `Atg5 = 0`, `Becn1 = 0`, `Lamp2 = 0`, `Sqstm1 = 1`, and `Ctsb = 1`; `Gclm`
  and `Sod2` each had one significant gene.
- A focal-class profile comparison over 17 selected iron/redox/autophagy
  training perturbations produced 10 nodes with no significant features, 5 with
  only 1-9 significant features, `Vps35` with 17, and `Rab7` with 501. I treated
  the `Rab7` footprint as a boundary rather than as a magnitude anchor for
  Fth1, because Rab7 loss perturbs broad late-endosomal/lysosomal trafficking
  and produced a wide lysosome/cholesterol/stress program rather than an
  Fth1-specific iron-storage response.

## Synthesis

The focal class is permissive enough that strong global regulators can generate
hundreds to thousands of DE genes, so the endpoint has dynamic range. Fth1 also
has unusually good in-class expression reach and likely loses functional
ferroxidase stock by harvest, which argues against forcing the forecast to the
training median of zero.

The analog evidence pulls the prediction back to a very small number. Available
iron handling, mitochondrial iron use, antioxidant, and core autophagy
perturbations mostly had 0-1 DE genes in the same thalamic population despite
similar recovered-cell sample sizes. The target biology also points to a buffered
installed ferritin pool, Ftl1-containing particles, unknown neuronal turnover,
and survivor-conditioned nuclear RNA rather than an acute unbuffered
transcription-factor-like perturbation.

I therefore predicted a minimal detectable response, above the strict null but
far below the broad `Rab7` lysosomal-trafficking boundary:

`predicted_n_degs = 1`
