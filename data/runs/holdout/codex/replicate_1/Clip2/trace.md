# Clip2 direct DEG-count forecast

## Target and endpoint

- Target: `Clip2` from the one-row `Clip2.csv` holdout manifest.
- Focal population: `151 TH Prkcd Grin2c Glut`.
- Endpoint: number of measured genes with BH-adjusted Wilcoxon `p < 0.05`.
- Withheld target outcome: not used.

## Biology that set the expected response scale

The canonical biology-only bundle places `Clip2` in a reachable but buffered
microtubule-plus-end/linker regime:

- `Clip2` is expressed in the exact focal population: 18,303 of 23,679
  non-target nuclei expressed it, or 77.3%, with mean log1p CP10K 0.642.
- Functional stock by harvest is judged `likely_substantially_depleted` because
  the P16 disruptive edit should stop new CLIP2 supply and 21-28 days is longer
  than the 3-13 day lifetime of most measured brain proteins, but no
  CLIP2-specific thalamic or postnatal depletion time course is known.
- CLIP2 is a dynamic microtubule/plus-end and dendritic-organelle linker, not a
  core tubulin, dynactin, or dynein component.
- Loss has a direct buffering route: CLIP1/CLIP-170 and dynactin redistribute
  to growing microtubule tips after Clip2 loss, while germline neural phenotypes
  show that compensation is incomplete.
- The mouse loss phenotype is developmental and centered on whole-brain,
  hippocampal, and motor readouts, so it supports biological relevance but not
  a large acute P16 thalamic nuclear-RNA response.

## Training counts and focal Parquet profiles

The declared 151-class count table contains 1,674 non-`Clip2` training targets
and is zero-heavy:

- median `n_degs`: 0
- mean `n_degs`: 14.05
- targets with any focal DEG: 469 / 1,674
- 75th percentile: 1
- 90th percentile: 2
- 95th percentile: 18

I used a caller-chosen cytoskeletal/microtubule cohort from the count table and
the declared expression Parquet to bracket CLIP2's likely scale:

| target | focal `n_degs` |
| --- | ---: |
| Dctn1 | 75 |
| Tuba1a | 7 |
| Kifbp | 2 |
| Tuba4a | 2 |
| Kif1a | 1 |
| Kif21a | 1 |
| Kif5a | 1 |
| Kif5c | 1 |
| Map1b | 1 |
| Mapre2 | 1 |
| Mapt | 1 |
| Myo5a | 1 |
| Sptan1 | 1 |
| Stmn2 | 1 |
| Tubb4b | 1 |
| Tubb5 | 1 |
| Add1 | 0 |
| Add2 | 0 |
| Add3 | 0 |
| Ank1 | 0 |
| Ank2 | 0 |
| Kif1b | 0 |
| Kif11 | 0 |
| Kif2a | 0 |
| Kif3b | 0 |
| Map6 | 0 |
| Rhot1 | 0 |
| Spast | 0 |

Across these 28 observed profiles, the median was 1 DEG: 12 had no significant
focal-class gene, 15 had 1-9 significant genes, and only `Dctn1` reached the
`>=50` profile-activity bucket in the Parquet comparison.

Same-experiment corpus context made `Dctn1` a high-side boundary rather than the
best scale donor: its response is a recurrent SREBF2-like sterol/cholesterol
module, and the corpus explicitly reports that sampled microtubule-associated
and tubulin-related perturbations usually do not form a shared mRNA compensation
or cytoskeletal-stress module. `Tuba1a` is the restricted positive exception,
with a tubulin-isotype dosage-compensation response in `151` and one Pvalb
class. `Mapre2`, an EB-family microtubule end-binding perturbation nearer to
CLIP2's plus-end biology than DCTN1 core dynactin or alpha-tubulin dosage, had
no downstream FDR-supported response and only one focal significant gene from
its self-transcript.

## Synthesis

`Clip2` should be reached in this cell class, and the edit-to-harvest interval
is long enough that a fully silent forecast would undercount the functional
stock prior. The operation is nevertheless an accessory/plus-end linker with
paralog buffering and no matched acute thalamic phenotype, while the training
neighbors show that most represented motor/MAP/plus-end/cytoskeletal targets
are flat or have one isolated count. I therefore predict a near-flat focal
signature, below `Tuba1a` and far below `Dctn1`, with a single FDR-significant
measured gene.

Predicted `n_degs`: 1
