# Scn9a DEG-count forecast

## Target and endpoint

- Target perturbation: `Scn9a`
- Context: `151 TH Prkcd Grin2c Glut`
- Endpoint: count of measured genes in the focal cell class with BH-adjusted Wilcoxon `pvals_adj < 0.05`
- Prediction: `0`

## Biology used

The declared biology bundle supports real functional engagement but only in a
restricted focal population. `Scn9a` was detected in the focal non-target
population in 2,753 of 23,679 cells, or 11.626%, with mean raw expression
0.1606 UMI/cell and pseudobulk CPM 10.07. Nav1.7 stock is expected to decline
over the P16 to P37-P44 editing interval: adult sensory-neuron deletion data
show week-scale Nav1.7 protein loss after intact transcript is removed. The
direct timing and turnover evidence is peripheral sensory-neuron evidence,
however, while thalamic protein evidence places Nav1.7 in restricted thalamic
nuclei. I treated that as evidence that a successfully edited expressing cell
could be perturbed, not as evidence for a broad aggregate thalamic RNA state.

## Training distribution and comparators

The focal training table contains 1,674 perturbations. It is sparse and
zero-heavy for this endpoint:

- 1,205 / 1,674 targets have `n_degs = 0`.
- Median = 0, 75th percentile = 1, 90th percentile = 2, 95th percentile = 18.
- The mean is 14.05 only because a small set of high-burden regulators reach
hundreds to thousands of DE genes.

Typed analog nomination against the actual training universe put the measured
Nav alpha subunits first: `Scn2a`, `Scn3a`, `Scn1a`, and `Scn8a`, followed by
broader channel comparators `Hcn1`, `Cacna1g`, `Hcn2`, and the exact
human-ortholog projected SCN9A-SCN1B-SCN2B complex member `Scn1b`. I also
checked `Fgf13`, the FGF13-SCN9A complex nominee, plus `Fgf12`, `Dpp6`,
`Snta1`, and `Ptchd1` as channel-associated boundaries surfaced by Claims or
related annotations.

Focal measured counts for the closest sodium-channel set were:

| training perturbation | focal `n_degs` | material significant calls |
| --- | ---: | --- |
| `Scn3a` | 0 | none |
| `Scn1a` | 1 | `Scn1a` self transcript |
| `Scn2a` | 1 | `Scn2a` self transcript |
| `Scn8a` | 1 | `Scn8a` self transcript |
| `Scn1b` | 2 | `Scn1b` self transcript plus `Jun` |
| `Fgf13` | 2 | `Fgf13` self transcript plus `Rell2` |
| `Hcn2` | 1 | `Hcn2` self transcript |
| `Hcn1` | 0 | none |
| `Cacna1g` | 12 | larger T-type calcium-channel response |

The same-experiment Claim layer reinforced a boundary rather than an
amplification: Findings for `Scn1a`, `Scn2a`, `Scn3a`, `Scn8a`, and `Scn1b`
jointly support the Claim that represented Nav alpha/beta subunits and FHF
modulators generate sparse, target- and context-specific RNA responses rather
than a shared pan-Nav or Nav-complex module. In the `151 TH Prkcd Grin2c Glut`
profile comparison, the five Nav subunit perturbations had no shared
FDR-significant genes; their positive top-tail overlaps were only 2-6 of the
top 100 features for most pairs and negative top-tail sharing was still weak.

Graph expansion of the top channel nominees returned five recurrent
same-corpus neighbors. `Psmb4` and `Rnpc3` had very large focal burdens
(`742` and `868`) and were kept only as high-burden divergent boundaries;
`Wdr26` had 13 DE genes but was a divergent non-Nav expansion; `Fbxo11` and
`Stxbp1` were low-count boundaries rather than sodium-conductance analogs.
None provided a reason to raise `Scn9a` above the sparse Nav scale.

## Synthesis

The biology says the perturbation is credible in Nav1.7-positive neurons, but
the focal expression is low and anatomically restricted inside the aggregated
thalamic class. The best measured analogues are stronger CNS sodium-channel
or beta/FHF perturbations, and in this same focal class they are either null or
nearly null, usually with the self transcript as the only significant feature.
Because measured self-transcript reduction is not a quantitative readout of
functional editing, and because `Scn9a` is less broadly expressed here than
several of those analogues, the most likely aggregate BH<0.05 outcome is no
DEG. A one-gene self-transcript call is plausible, but I put the integer point
on the zero side of that boundary.

Predicted `n_degs`: 0
