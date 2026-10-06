# Pdss2 direct forecast

Target: `Pdss2`

Focal population: `151 TH Prkcd Grin2c Glut`

Predicted `n_degs`: **0**

## Evidence used

The declared Pdss2 biology bundle supports target reach but not a guaranteed
acute transcriptional footprint. Pdss2 was detected in the focal non-target
cells with 12,352 of 23,679 nuclei expressing it, mean raw UMI 0.791, mean
CP10k 0.501, and pseudobulk CPM 49.56. The functional-stock card judged
Pdss2/CoQ function as likely substantially depleted by the P37-P44 harvest,
because a disruptive P16 edit should stop new Pdss2-dependent CoQ-side-chain
synthesis, brain CoQ9 can fall strongly on a month scale in Pdss2 mutant mice,
and the assay window is 21-28 days. The same card also preserved the main
counterweight: existing Pdss1/Pdss2 synthase and membrane CoQ persist at edit
onset, and no matched P16-to-harvest Pdss2 protein or neuronal CoQ clearance
series was available.

The selected same-experiment corpus had no Pdss2 report context in this release
(`target_context` returned zero Findings, Claims, and explicit references), so
the prediction relied on training perturbations chosen from Pdss2 biology.

The focal count table is sparse overall: among 1,674 training perturbations,
1,205 had `n_degs = 0`, 1,481 had `n_degs <= 1`, and the 75th percentile was
1. Directly mitochondrial respiratory-chain training targets were even more
concentrated near zero: 34 complex-I/III/IV hits had median 0 and mean 0.41,
with every member at either 0 or 1 DEG.

Typed mouse analog nomination against the actual training universe placed the
available CoQ-side-chain neighbor `Coq5` first and the ubiquinol-biosynthesis
neighbor `Stard7` second. Both had zero DEGs in the focal class. Other
high-priority narrow-module hits also favored a zero response:

| training target | relationship to Pdss2 | n_degs |
| --- | --- | ---: |
| Coq5 | Reactome ubiquinol biosynthesis / metabolism of cofactors | 0 |
| Stard7 | Reactome ubiquinol biosynthesis / metabolism of cofactors | 0 |
| Cit | prenyltransferase activity / terpenoid-backbone module | 0 |
| Fntb | prenyltransferase activity / terpenoid-backbone module | 0 |
| Hmgcr | terpenoid-backbone / isoprenoid biosynthesis | 0 |
| Ndufa9 | broad ubiquinone-biosynthesis, mitochondrial-matrix fallback | 0 |

`Dhdds` was the important exception among the narrow prenyltransferase nominees
at 116 DEGs, but it points to dolichol/protein-glycosylation biology rather
than CoQ synthesis. `Calm1` was broader still and had 14 DEGs. The graph
expansion around the top eight nominees produced 11 further observed neighbors;
several were explicitly connected through no-convergence, divergent, or weak
similarity Findings, and the high-count nodes in that expanded set (`Psmc1`,
430; `Atp2a2`, 187) represented proteasome or calcium-stress boundaries rather
than Pdss2-like CoQ-side-chain loss.

I compared the 19 initial-plus-expanded observed profiles in the exact
`151 TH Prkcd Grin2c Glut` context. The comparison found 11 of 19 with no
FDR-significant feature, three with 1-9 significant features, two with 10-49,
and only three with at least 50. In the projected key inspection, `Coq5` and
`Stard7` both had 17,259 measured features and zero FDR-significant positive
or negative features, while the high-count boundaries were `Dhdds`,
`Psmc1`, and `Atp2a2`.

## Reasoning

Pdss2 has enough focal expression and enough post-edit time for a real CoQ
biochemical lesion to be possible, so I did not treat it as an assay null.
However, the assay asks for BH-significant survivor-state nuclear RNA changes
only three to four weeks after a sparse postnatal edit. The most task-matched
training perturbations inside ubiquinol biosynthesis and immediately adjacent
isoprenoid/prenyl chemistry were transcriptionally silent in the same thalamic
class, and the respiratory-chain complex genes that could phenocopy impaired
electron transport were almost all zero or one DEG. The nonzero analogs were
mechanistically broader boundaries rather than equal-scale Pdss2 donors.

Balancing likely partial CoQ depletion against that local low-response
training evidence, the point estimate that best matches the biology and
measured comparator outcomes is a fully quiet focal signature.
