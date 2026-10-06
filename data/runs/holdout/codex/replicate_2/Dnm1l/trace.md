# Dnm1l n_degs forecast

Target: `Dnm1l` in `151 TH Prkcd Grin2c Glut`

Predicted `n_degs`: `1`

## Evidence used

- The one-row manifest and biology bundle identify the held-out perturbation as `Dnm1l`.
- The biology-only bundle reports that `Dnm1l` is expressed in the exact focal non-target population: 22,992 of 23,679 nuclei expressed the feature, or 97.10%, with mean raw UMI 4.81 and mean CP10K 3.02.
- The same bundle adjudicates DRP1 as a dynamic mitochondrial/peroxisomal fission GTPase whose operative stock should be substantially depleted by the P37-P44 harvest after P16 editing. The main timing evidence was a roughly 3-day neuronal DNM1L half-life and maximal DRP1 depletion within 14 days after adult forebrain deletion, so a no-stock-persistence explanation for a null is unlikely.
- The direct same-cell count table is zero inflated: among 1,674 training perturbations in `151 TH Prkcd Grin2c Glut`, 1,205 had 0 DEGs, the median was 0, the 75th percentile was 1, the 90th percentile was 2, and the 95th percentile was 18.
- Closest measured mitochondrial-dynamics references in that count table were sparse:
  - `Mff`, the represented outer-membrane DRP1-recruitment/fission-side comparator: 0
  - `Gdap1`, another fission-linked target: 0
  - `Slc25a46`, mitochondrial-dynamics carrier: 1
  - `Yme1l1`, `Afg3l2`, `Clpp`, `Clpx`, and `Agk`, OPA1-processing or adjacent mitochondrial proteostasis/lipid targets: 0
  - `Opa1`, inner-membrane fusion/cristae positive control: 37
- Other represented mitochondrial controls that the corpus uses to bound broad mtISR transfer were mostly 0 or 1 in this class: `Ndufb8` 1, `Ndufs4` 0, `Ndufs2` 1, `Ndufv1` 0, `Gfm2` 0, `Isca2` 1, `Ndufa4` 1, `Sucla2` 1, `Coa8` 0, `Sdha` 1, and `Lrpprc` 0.
- Same-experiment reports package the same pattern: `Mff` produced no FDR<0.10 downstream response in any recovered neuronal group and did not enter the `Opa1` ATF4/mitochondrial-ISR state; `Opa1` was a detectable positive control but its stress program was explicitly branch-specific rather than a generic mitochondrial or fission-side response.
- Raw profile comparison of the selected mitochondrial/fission/stress training nodes in the focal class showed weak profile cohesion. Across 78 selected pairs, the mean positive and negative top-tail overlaps were 0.031 and 0.036, significant-program overlap was 0, and the `Mff`-`Opa1` whole-profile Pearson similarity was only 0.034.

## Reasoning

The target-expression reach and stock card argue that a successful `Dnm1l` edit should be biologically realized in these thalamic glutamatergic neurons; unlike a very long-lived chromatin mark or a nonexpressed target, DRP1 should turn over within the 21-28 day experimental window. That moved the point above a pure screen-median prediction of 0.

The training evidence kept the point in the singleton regime. `Mff` is the nearest measured fission-side perturbation and was completely flat, and the represented OPA1-processing/fission/peroxisomal neighbors were also 0 or 1. `Dnm1l` itself is the core fission GTPase, so I lifted it slightly above `Mff`; however, the `Opa1` response is an inner-membrane/cristae mtISR branch that the same-experiment corpus and raw score profiles show is not shared by outer-membrane `Mff` loss or most mitochondrial lesions. I therefore predicted one BH-significant measured gene rather than an OPA1-scale multi-dozen response.

No withheld `Dnm1l` expression signature or `Dnm1l` DEG count was used.
