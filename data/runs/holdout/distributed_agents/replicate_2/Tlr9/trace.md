# Tlr9 DEG-count prediction trace

## Question interpreted

The requested readout is the number of measured genes with `pvals_adj < 0.05` after loss of the held-out target in `151 TH Prkcd Grin2c Glut` thalamic glutamatergic neurons. The run manifest contains one held-out target, `Tlr9`. I treated a prediction of `0` as "no gene reaches the focal FDR threshold", not as a claim that TLR9 biology is globally absent.

## Sources used

- Run inputs:
  - Held-out manifest: `240_Tlr9.csv`, one requested target, `Tlr9`.
  - Training DEG-count CSV: 1,674 non-held-out perturbations with `n_degs` in the focal cell group.
  - Training DE Parquet: raw per-gene Wilcoxon statistics for non-held-out perturbations.
- Local Distributed Agents resources:
  - Distributed Agents dataset context for the PerturbAI whole-brain atlas derivative.
  - Distributed Agents corpus release `perturbai-july-260713-sourceguard-1773-v1`, queried for TLR, CD14, NF-kappaB/IRF, and innate-receptor findings and claims.
  - Distributed Agents runtime `profile_compare` over the focal `151 TH Prkcd Grin2c Glut` log2-fold-change profiles.
- External biology:
  - Hemmi et al. 2000, Nature, DOI `10.1038/35047123`, PMID `11130078`: TLR9 is the CpG-DNA Toll-like receptor.
  - Latz et al. 2004, Nature Immunology, DOI `10.1038/ni1028`, PMID `14716310`: TLR9 traffics from ER to CpG-containing lysosomal compartments where MyD88 is recruited.
  - Lee et al. 2013, eLife, DOI `10.7554/eLife.00291`, PMID `23426999`: UNC93B1 controls endosomal TLR trafficking, including TLR9 delivery to endolysosomes.
  - Honda et al. 2005, Nature, DOI `10.1038/nature03464`, PMID `15800576`: MyD88-dependent TLR9-family interferon induction in plasmacytoid dendritic cells requires IRF7.
  - Butchi et al. 2010, Glia, DOI `10.1002/glia.20952`, PMID `19998480`, and Rosenberger et al. 2014, Journal of Neuroinflammation, DOI `10.1186/s12974-014-0166-7`, PMID `25239168`: TLR7/TLR9 and other TLR responses in the CNS are mainly ligand- and glial/inflammatory-context dependent.

## Dataset calibration

The focal training-count file is highly zero-inflated:

| class | training targets |
| --- | ---: |
| `n_degs = 0` | 1,205 |
| `1 <= n_degs < 10` | 363 |
| `10 <= n_degs < 100` | 63 |
| `n_degs >= 100` | 43 |

The median training count is zero and 71.98% of training perturbations are zero in this focal class. Therefore I only assigned a nonzero count when the held-out target had a strong mechanistic and in-dataset reason to deviate from zero.

## Raw focal analog checks

I first selected represented genes in the same innate pathway lane as `Tlr9`: other TLRs, CD14/CD36 innate receptor comparators, and IRF/NF-kappaB-side downstream nodes. I then filtered the Parquet to `group_name == "151 TH Prkcd Grin2c Glut"` and to those targets and counted `pvals_adj < 0.05`.

| training perturbation | relationship to Tlr9 | focal `n_degs` | minimum focal `pvals_adj` |
| --- | --- | ---: | ---: |
| `Tlr7` | closest represented endosomal nucleic-acid TLR, MyD88-coupled | 0 | 1.000000 |
| `Tlr8` | represented endosomal RNA-sensing TLR | 0 | 1.000000 |
| `Tlr3` | endosomal nucleic-acid TLR, but TRIF/TICAM1-coupled | 0 | 1.000000 |
| `Tlr2` | surface MyD88-coupled TLR counterexample | 0 | 1.000000 |
| `Tlr4` | LPS receptor, TRIF and MyD88 arms | 0 | 1.000000 |
| `Tlr5` | surface flagellin TLR counterexample | 0 | 1.000000 |
| `Cd14` | TLR4/TLR innate co-receptor context | 0 | 1.000000 |
| `Cd36` | sterile-inflammatory receptor comparator | 0 | 1.000000 |
| `Nfkb1` | canonical inflammatory transcriptional output node | 0 | 1.000000 |
| `Traf3` | innate TLR/IRF signaling adaptor | 0 | 1.000000 |
| `Irf1` | interferon-regulatory transcription factor | 0 | 1.000000 |
| `Irf2` | interferon-regulatory transcription factor | 0 | 1.000000 |
| `Irf3` | IRF branch downstream of several PRRs | 0 | 1.000000 |
| `Irf5` | MyD88/TLR-associated IRF | 0 | 0.788907 |
| `Irf8` | immune-lineage IRF; possible pathway boundary | 0 | 0.121418 |
| `Irf9` | ISGF3/type-I-interferon response node | 0 | 1.000000 |

The closest endosomal analogs, `Tlr7` and `Tlr8`, had only 89 matched perturbed nuclei in this class, so there is limited power to see very subtle effects. Still, neither produced even a near-threshold focal gene.

I also ran a focal signed-profile comparison using `Tlr2`, `Tlr3`, `Tlr4`, `Tlr5`, `Tlr7`, `Tlr8`, `Cd14`, `Cd36`, `Nfkb1`, `Irf3`, and `Traf3` as anchors and the 1,674 training targets as the eligible universe. All 11 anchors had `significant_feature_count = 0`. Among inspected TLR/CD14 pairs, the positive and negative FDR-significant intersections were all zero, and top-50 signed-tail overlaps were tiny. The top all-universe neighbors of quiet TLR profiles were unrelated genes such as `Ndufs4`, `Acvr1`, `Flnb`, and `Dcc`, so I treated the whole-vector similarities as low-information quiet-profile behavior rather than evidence for a real TLR/NF-kappaB module.

## Internal corpus evidence

The selected Distributed Agents corpus had no direct `Tlr9` findings or claims, consistent with `Tlr9` being held out. It did have a high-confidence synthesized claim that represented `Tlr3`, `Tlr4`, `Tlr5`, `Tlr7`, `Tlr8`, and `Cd14` perturbations in unchallenged neuronal Perturb-seq conditions do not form a coherent shared TLR/PRR-to-NF-kappaB/IRF transcriptional module, except for isolated target-specific singleton responses.

Specific relevant corpus findings were:

- `Tlr7`: loss of function was transcriptionally silent in every measured neuronal cell group; neither the canonical TLR7 inflammatory program nor a reported neuronal MyD88/c-Fos/IL-6 axis was recovered.
- `Tlr8`: the only robust atlas-wide downstream response was `Cnpy3` up-regulation in `054 CNU-MGE GABA`, not in the focal thalamic glutamatergic class; the event did not generalize to `Tlr3`, `Tlr4`, `Tlr7`, `Nfkb1`, or `Irf5`.
- `Tlr3`, `Tlr4`, and `Tlr5`: either pan-neuronal null or singleton, nonconvergent events outside the focal class; represented TLR-family and IFN/NF-kappaB relatives did not phenocopy them.
- `Cd14` and `Cd36`: no sustained basal neuronal innate-inflammatory response, reinforcing that the screen is not observing tonic microglial-like PRR signaling in NeuN-positive nuclei.

Those corpus findings also record an important boundary: `Myd88`, `Unc93b1`, `Irak1`, `Irak4`, `Traf6`, and `Ticam1` were not direct training perturbations. The zero prediction therefore comes from represented receptors and terminal pathway nodes, not from direct measurement of every adaptor in the TLR9 cascade.

## Target-specific prediction

### `Tlr9`

`Tlr9` encodes the endosomal receptor for unmethylated CpG DNA. Canonically, ligand-bound TLR9 signals from endolysosomal compartments through MyD88 to NF-kappaB and IRF-family outputs, and proper localization depends on UNC93B1-mediated trafficking. In this experiment, there was no CpG ligand, viral DNA, bacterial challenge, injury, or systemic inflammation, and the sorted NeuN-positive nuclear population largely excludes microglia and other immune cells where TLR9 signaling is strongest.

The best represented in-dataset analogs are the endosomal TLRs `Tlr7` and `Tlr8`. Both had `n_degs = 0` in the focal class; `Tlr7` was flat across the whole atlas in the Distributed Agents corpus, and the isolated `Tlr8` response occurred in a GABAergic class rather than `151 TH Prkcd Grin2c Glut`. Broader TLR-family, CD14/CD36, NF-kappaB, TRAF3, and IRF perturbations were also all zero in the focal class. This makes it unlikely that knocking out another unstimulated endosomal TLR would push even a handful of thalamic glutamatergic genes past BH FDR 0.05.

Prediction: `0` DEGs.

## Limits

- `Tlr9` itself was held out, and the most proximal TLR9 adaptors and trafficking genes that would have been ideal checks, especially `Myd88`, `Unc93b1`, `Irak1`, `Irak4`, and `Traf6`, were not available as training perturbations.
- The closest assayed endosomal analogs, `Tlr7` and `Tlr8`, recognize RNA rather than CpG DNA; `Tlr3` uses TRIF rather than MyD88; and surface TLRs are weaker counterexamples.
- `Tlr7` and `Tlr8` each had 89 matched perturbed nuclei in the focal group, which limits sensitivity to a one-gene or very weak `Tlr9` event.
- TLR9 can have important glial, immune, infection, injury, and Alzheimer-model biology. The prediction is restricted to acute sparse loss of function in unstimulated postnatal NeuN-positive neuronal nuclei and should not be generalized to microglia or ligand-stimulated CNS inflammation.
