# Guk1 direct DEG-count forecast

## Requested target

- Target: `Guk1`
- Cell class: `151 TH Prkcd Grin2c Glut`
- Endpoint: `n_degs`, measured genes with Wilcoxon `pvals_adj < 0.05`

## Evidence used

I used the declared one-row manifest and biology-only `Guk1` bundle. The exact
in-assay reach for the target class was moderate rather than absent:
`Guk1` was detected in 13,809 of 23,679 matched non-target thalamic nuclei
(`58.3175%`), with `mean_raw_umi = 1.0069` and `pseudobulk_cpm = 63.1076`.

The biology card supports realized but not perfectly timed loss. Guk1 is the
cytosolic and mitochondrial guanylate kinase that phosphorylates GMP and dGMP
to GDP and dGDP. The expected functional-stock adjudication was
`likely_substantially_depleted` by the P37-P44 harvest after P16 editing,
because continued synthesis should stop and a soluble metabolic enzyme should
turn over over 21-28 days. The same bundle also leaves the endpoint coupling
uncertain: the documented mouse phenotype is systemic preweaning lethality,
the human phenotype is chronic multisystem mitochondrial disease, and no
matched acute postnatal thalamic-neuron loss phenotype or Guk1-specific
neuronal half-life was available.

The declared training count table for this class was sparse. Among 1,674
training perturbations, 1,205 had `n_degs = 0`; the median was 0, the 75th
percentile was 1, the 90th percentile was 2, and the 95th percentile was 18.
This made a high count require more than generic essentiality.

I nominated training-available Guk1 analogs with the offline gene-analog tool
using the 1,674-gene training universe. It found no exact complex member or
paralog in the assayed set. The most specific hit was `Nt5c2`, through GMP and
dGMP metabolic-process annotations, but this is a phosphatase/catabolic
neighbor rather than a direct guanylate-kinase substitute. Broader purine or
cyclic-nucleotide candidates were also weak. I therefore combined the closest
purine/nucleotide context with a small mitochondrial nucleotide-balance context
from genes adjacent to mtDNA-depletion or mitochondrial-metabolism biology:

| training perturbation | relationship used | `n_degs` |
| --- | --- | ---: |
| `Nt5c2` | closest GMP/dGMP process neighbor | 0 |
| `Fhit` | broader purine-nucleotide metabolism | 0 |
| `Adk` | broader purine salvage kinase | 0 |
| `Pde4b` | loose cyclic-nucleotide boundary | 0 |
| `Sucla2` | indirect mitochondrial dNTP-balance context | 1 |
| `Suclg1` | indirect mitochondrial dNTP-balance context | 0 |
| `Ndufs2` | broad mitochondrial stress context | 1 |
| `Aco2` | broad mitochondrial metabolism context | 0 |

The exact selected cohort had mean `n_degs = 0.25`, median `0`, and rounded
back-transformed mean `expm1(mean(log1p(n_degs))) = 0`.

I also inspected the corresponding `151 TH Prkcd Grin2c Glut` profiles in the
declared Parquet. All eight selected profiles were present with 17,259 measured
features. Six of eight had no FDR-significant genes; only `Sucla2` and
`Ndufs2` had one significant gene each, both downregulated. A profile-cohort
diagnostic found no coherent positive significant program and only weak
negative-tail recurrence, so these profiles supported a low response scale
rather than a hidden high-response module.

Corpus topology over the same eight measured nodes separated a purine component
(`Adk`, `Nt5c2`, `Pde4b`) from a mitochondrial component (`Aco2`, `Ndufs2`,
`Sucla2`, `Suclg1`), with `Fhit` isolated in explicit Finding-reference space.
That reinforced the interpretation that the count forecast should be anchored
on several weak, low-response contextual observations, not on a single direct
analogue or a unified high-response state.

## Synthesis

The upward evidence was that Guk1 itself is expressed in the focal population,
its active cytosolic and mitochondrial enzyme pools are likely to decline by
harvest, and no same-reaction paralog was found. The downward evidence was
that expression covers only about 58% of matched thalamic nuclei, the matched
loss phenotypes do not prove a postnatal thalamic transcriptional state, the
observed nucleotide and mitochondrial training perturbations in this exact cell
class were all zero or one DEG, and the analog profiles did not expose a shared
significant program.

I therefore forecast a very small nonzero footprint, above a hard null because
Guk1 is plausibly depleted and nonredundant, but still on the zero-to-one scale
set by the closest measured training perturbations.

`predicted_n_degs = 1`
