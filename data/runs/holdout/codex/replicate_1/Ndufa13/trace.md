# Direct forecast for Ndufa13 in 151 TH Prkcd Grin2c Glut

## Target and endpoint

- Held-out target: `Ndufa13`.
- Endpoint: `n_degs`, the count of measured genes in `151 TH Prkcd Grin2c Glut` with BH-adjusted Wilcoxon `pvals_adj < 0.05`.
- The declared focal count table contains 1,674 visible training targets and excludes `Ndufa13`.

## Evidence used

The canonical Ndufa13 biology bundle exposed no target outcome. Its endpoint-blind evidence placed NDUFA13 in mitochondrial respiratory complex I and judged the operative stock to be the already assembled NDUFA13-containing holoenzyme. The assayed thalamic population had exact in-assay target expression, with 22,743 of 23,679 non-target nuclei expressing `Ndufa13` and a mean of 2.846 CP10k. The functional-stock card judged the P16 edit likely to stop new NDUFA13 supply while leaving pre-existing complex I to persist until turnover; the closest neuronal mitochondrial-proteome proxy had a median half-life near 25.7 days, so the P37-P44 harvest interval is roughly one proxy half-life rather than an acute complete depletion.

Typed analogue nomination from the 1,674 training genes found a specific exact-complex cohort of 20 training-available complex-I structural perturbations:

`Ndufa12`, `Ndufs2`, `Ndufs4`, `Ndufs7`, `Ndufs8`, `Ndufv1`, `Ndufv2`, `Ndufa11`, `Ndufa6`, `Ndufa4`, `Ndufa9`, `Ndufb7`, `Ndufb11`, `Ndufa10`, `Ndufb10`, `Ndufa8`, `Ndufc2`, `Ndufb8`, `Ndufb3`, `Ndufb9`.

These were supported by mouse CORUM complex-I membership, strict one-to-one projected human CORUM complex-I membership for most members, STRING physical edges, and shared respiratory-chain annotations. Their focal training counts were:

| cohort | genes | focal n_degs |
| --- | ---: | ---: |
| exact complex-I structural cohort | 20 | `0,1,0,0,1,0,1,0,1,1,0,0,1,1,1,0,1,1,0,1` |
| Ndufa13 direct interactors outside that exact complex tier | 4 | `0,0,0,0` |

Thus the direct exact-complex cohort had a mean focal count of 0.55, a median of 1, and no member above 1 DEG. The four lower-specificity direct interactors or assembly neighbors, `Ndufaf4`, `Ndufaf2`, `Timmdc1`, and `Stat3`, were all focal-zero and therefore did not justify moving above the structural-complex scale.

Same-experiment corpus checks supported using the structural cohort as a buffered respiratory-chain module, with the caveat that corpus reports and the Parquet are alternate representations of the same Perturb-seq experiment rather than replication. The 20 exact-complex candidates formed one explicit-Finding component in the report-derived topology: 175 of 190 possible pairs were connected by directed comparator mentions, and all 20 were represented. The buffered-response Finding inventory for the exact and direct Ndufa13 nominees contained 22 buffered-response records, including Ndufa8, Ndufa9, Ndufs4, Ndufv1, Ndufb7, Ndufb10, Ndufs2, Ndufs8, and the NDUFAF assembly factors, each reporting near-null downstream transcriptomes and absent ISR/UPRmt/redox/mitophagy or OXPHOS-compensation signatures across recovered neuronal groups.

The focal profile comparison over those 24 exact/direct candidates in `151 TH Prkcd Grin2c Glut` found no broad response: 13 candidates had no significant feature in the focal class and the other 11 had only 1 significant feature. The 20 exact-complex members were directionally coherent mainly in the negative tail, consistent with a very weak shared perturbation surface rather than a large mitochondrial-stress state.

## Synthesis

Ndufa13 is expressed in the focal thalamic neurons and has a credible complex-I loss mechanism, so I did not treat it as an expression-null or biologically absent perturbation. The best matched training perturbations, however, show that acute mosaic postnatal loss of complex-I subunits is usually transcriptionally buffered in this assay: in the exact complex-I cohort every focal count is either 0 or 1, assembly neighbors are 0, and the same-experiment reports repeatedly flag absent canonical stress responses even for measured Nduf knockdowns.

The Ndufa13-specific card reinforces partial realization rather than complete acute collapse: new NDUFA13 production should stop, but installed complex I can persist over the 21-28 day window. That keeps the point forecast at the complex-I empirical center and far below Opa1-like or proteostasis-like broad responders. Because Ndufa13 is a nonredundant, well-expressed structural component rather than an assembly factor with only indirect contact, I rounded the exact-complex mean of 0.55 up to the only nonzero value seen in that cohort.

Predicted `n_degs`: 1
